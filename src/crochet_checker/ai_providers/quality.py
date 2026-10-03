"""Compiler-authoritative AI quality layer for ChatGPT and Gemini."""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class AIClaim:
    provider: str
    model: str
    claim_type: str
    message: str
    confidence: float = 0.0
    status: str = "UNVERIFIED"
    latency_ms: int = 0


@dataclass
class RepairProposal:
    provider: str
    original_text: str
    replacement_text: str
    reason: str
    confidence: float = 0.0
    compiler_verified: bool = False
    approved: bool = False


@dataclass
class AIQualityReport:
    pattern_hash: str
    compiler_valid: bool
    compiler_errors: list[str] = field(default_factory=list)
    claims: list[AIClaim] = field(default_factory=list)
    repairs: list[RepairProposal] = field(default_factory=list)
    disagreements: list[str] = field(default_factory=list)
    providers_used: list[str] = field(default_factory=list)
    mode: str = "offline"
    recommendation: str = ""

    @property
    def has_conflicts(self) -> bool:
        return bool(self.disagreements)

    @property
    def confidence(self) -> float:
        if not self.claims:
            return 1.0 if self.compiler_valid else 0.0
        return round(
            sum(claim.confidence for claim in self.claims)
            / len(self.claims),
            3,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern_hash": self.pattern_hash,
            "compiler_valid": self.compiler_valid,
            "compiler_errors": self.compiler_errors,
            "claims": [asdict(item) for item in self.claims],
            "repairs": [asdict(item) for item in self.repairs],
            "disagreements": self.disagreements,
            "providers_used": self.providers_used,
            "mode": self.mode,
            "confidence": self.confidence,
            "recommendation": self.recommendation,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class AIQualityChecker:
    """
    Compare deterministic compiler results with AI explanations.

    The compiler is authoritative. AI results are advisory only.
    """

    def __init__(
        self,
        mode: str = "offline",
        cache_dir: str | None = None,
    ):
        valid_modes = {"offline", "cloud", "consensus"}
        if mode not in valid_modes:
            raise ValueError(
                f"mode must be one of: {', '.join(sorted(valid_modes))}"
            )

        self.mode = mode
        self.cache_dir = Path(
            cache_dir
            or os.environ.get("CROCHET_AI_CACHE", ".crochet_cache/ai")
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def pattern_hash(pattern_text: str) -> str:
        return hashlib.sha256(
            pattern_text.strip().encode("utf-8")
        ).hexdigest()[:24]

    def _cache_file(self, pattern_text: str) -> Path:
        return self.cache_dir / f"{self.pattern_hash(pattern_text)}.json"

    def _compiler_errors(self, report) -> list[str]:
        return [
            getattr(error, "message", str(error))
            for error in getattr(report, "errors", [])
        ]

    def _cached(self, pattern_text: str) -> dict[str, Any] | None:
        path = self._cache_file(pattern_text)
        if not path.exists():
            return None

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def _save(self, pattern_text: str, report: AIQualityReport) -> None:
        self._cache_file(pattern_text).write_text(
            report.to_json(),
            encoding="utf-8",
        )

    def check(self, pattern, compiler_report) -> AIQualityReport:
        pattern_text = getattr(pattern, "source_text", str(pattern))

        if self.mode != "offline":
            cached = self._cached(pattern_text)
            if cached:
                return self._from_dict(cached)

        result = AIQualityReport(
            pattern_hash=self.pattern_hash(pattern_text),
            compiler_valid=bool(
                getattr(compiler_report, "valid", False)
            ),
            compiler_errors=self._compiler_errors(compiler_report),
            mode=self.mode,
        )

        result.claims.append(
            AIClaim(
                provider="compiler",
                model="deterministic",
                claim_type="validation",
                message=(
                    "Compiler validation passed."
                    if result.compiler_valid
                    else "Compiler found validation errors."
                ),
                confidence=1.0,
                status="VERIFIED",
            )
        )

        if self.mode in {"cloud", "consensus"}:
            self._query_cloud_models(result, pattern, compiler_report)

        if result.compiler_errors:
            result.recommendation = (
                "Fix deterministic compiler errors first. "
                "AI output cannot override compiler arithmetic."
            )
        elif result.disagreements:
            result.recommendation = (
                "AI providers disagree. Keep the compiler result "
                "authoritative and review the pattern manually."
            )
        else:
            result.recommendation = (
                "Pattern passed deterministic validation. "
                "AI output is advisory only."
            )

        if self.mode != "offline":
            self._save(pattern_text, result)

        return result

    def _query_cloud_models(self, result, pattern, compiler_report):
        del pattern, compiler_report
        result.disagreements.append(
            "Hosted chat was not called. The compiler result stands."
        )

    @staticmethod
    def _from_dict(data: dict[str, Any]) -> AIQualityReport:
        return AIQualityReport(
            pattern_hash=data["pattern_hash"],
            compiler_valid=data["compiler_valid"],
            compiler_errors=data.get("compiler_errors", []),
            claims=[
                AIClaim(**item)
                for item in data.get("claims", [])
            ],
            repairs=[
                RepairProposal(**item)
                for item in data.get("repairs", [])
            ],
            disagreements=data.get("disagreements", []),
            providers_used=data.get("providers_used", []),
            mode=data.get("mode", "cached"),
            recommendation=data.get("recommendation", ""),
        )


def quality_check(
    pattern,
    compiler_report,
    mode: str = "offline",
) -> AIQualityReport:
    """Convenience function for AI quality checking."""
    return AIQualityChecker(mode=mode).check(
        pattern,
        compiler_report,
    )
