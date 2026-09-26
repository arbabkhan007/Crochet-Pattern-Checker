"""Compiler-authoritative AI quality and consensus layer."""

from __future__ import annotations

import hashlib
import json
import os
import re
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
    round_number: int | None = None
    compiler_count: int | None = None
    ai_count: int | None = None
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
            sum(claim.confidence for claim in self.claims) / len(self.claims),
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
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class AIQualityChecker:
    """
    Safe AI layer.

    The deterministic compiler is always authoritative. AI output is advisory,
    explicitly labeled, cached, and never directly applied to source patterns.
    """

    def __init__(
        self,
        mode: str = "offline",
        cache_dir: str | None = None,
    ):
        allowed = {"offline", "cloud", "consensus", "local"}
        if mode not in allowed:
            raise ValueError(f"mode must be one of {sorted(allowed)}")

        self.mode = mode
        self.cache_dir = Path(
            cache_dir
            or os.environ.get(
                "CROCHET_AI_CACHE",
                ".crochet_cache/ai",
            )
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def pattern_hash(pattern_text: str) -> str:
        return hashlib.sha256(
            pattern_text.strip().encode("utf-8")
        ).hexdigest()[:24]

    def _compiler_errors(self, report) -> list[str]:
        return [
            getattr(item, "message", str(item))
            for item in getattr(report, "errors", [])
        ]

    def _compiler_counts(self, pattern) -> dict[int, int]:
        result: dict[int, int] = {}

        for item in getattr(pattern, "rounds", []) or getattr(pattern, "rows", []):
            number = getattr(
                item,
                "round_number",
                getattr(item, "row_number", 0),
            )
            result[int(number)] = int(
                getattr(item, "computed_stitch_count", 0)
            )

        return result

    def _cache_path(self, pattern_text: str) -> Path:
        return self.cache_dir / f"{self.pattern_hash(pattern_text)}.json"

    def load_cache(self, pattern_text: str) -> dict[str, Any] | None:
        path = self._cache_path(pattern_text)
        if not path.exists():
            return None

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def save_cache(self, pattern_text: str, report: AIQualityReport) -> None:
        path = self._cache_path(pattern_text)
        path.write_text(report.to_json(), encoding="utf-8")

    def check(self, pattern, report) -> AIQualityReport:
        pattern_text = getattr(pattern, "source_text", str(pattern))
        compiler_errors = self._compiler_errors(report)
        compiler_counts = self._compiler_counts(pattern)

        cached = self.load_cache(pattern_text)
        if cached and self.mode != "offline":
            return self._from_cached(cached)

        result = AIQualityReport(
            pattern_hash=self.pattern_hash(pattern_text),
            compiler_valid=bool(getattr(report, "valid", False)),
            compiler_errors=compiler_errors,
            mode=self.mode,
        )

        # Always provide deterministic compiler claims.
        for number, count in compiler_counts.items():
            result.claims.append(
                AIClaim(
                    provider="compiler",
                    model="deterministic",
                    claim_type="stitch_count",
                    message=f"Round {number} computes {count} stitches.",
                    round_number=number,
                    compiler_count=count,
                    ai_count=count,
                    confidence=1.0,
                    status="VERIFIED",
                )
            )

        if self.mode in {"cloud", "consensus"}:
            self._add_cloud_claims(result, pattern, report)

        if self.mode == "local":
            result.disagreements.append(
                "Local AI mode requires an Ollama adapter; compiler result retained."
            )

        if compiler_errors:
            result.recommendation = (
                "Fix deterministic compiler errors first. "
                "AI suggestions cannot override compiler arithmetic."
            )
        elif result.disagreements:
            result.recommendation = (
                "AI providers disagree. Keep the compiler result authoritative "
                "and review the conflicting rounds manually."
            )
        else:
            result.recommendation = (
                "Pattern passed deterministic validation. "
                "AI output is advisory only."
            )

        if self.mode != "offline":
            self.save_cache(pattern_text, result)

        return result

    def _add_cloud_claims(self, result, pattern, report) -> None:
        try:
            from .provider import AIConfig, AIProvider
        except ImportError as exc:
            result.disagreements.append(f"AI provider unavailable: {exc}")
            return

        configurations = [
            ("openai", AIConfig(
                provider="openai",
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            )),
            ("gemini", AIConfig(
                provider="gemini",
                model=os.environ.get("GEMINI_MODEL", "gemini-1.5-flash"),
            )),
        ]

        responses: dict[str, str] = {}

        for provider_name, config in configurations:
            if provider_name == "openai" and not os.environ.get("OPENAI_API_KEY"):
                continue
            if provider_name == "gemini" and not os.environ.get("GOOGLE_API_KEY"):
                continue

            started = time.perf_counter()

            try:
                provider = AIProvider(config)
                response = provider.explain_pattern(pattern, report)
                latency = int((time.perf_counter() - started) * 1000)

                responses[provider_name] = response
                result.providers_used.append(provider_name)
                result.claims.append(
                    AIClaim(
                        provider=provider_name,
                        model=config.model or "default",
                        claim_type="explanation",
                        message=response,
                        confidence=0.5,
                        status="UNVERIFIED",
                        latency_ms=latency,
                    )
                )
            except Exception as exc:
                result.disagreements.append(
                    f"{provider_name} failed safely: "
                    f"{type(exc).__name__}: {exc}"
                )

        if len(responses) >= 2:
            values = list(responses.values())
            if values[0].strip() != values[1].strip():
                result.disagreements.append(
                    "ChatGPT and Gemini returned different explanations."
                )

    @staticmethod
    def _from_cached(data: dict[str, Any]) -> AIQualityReport:
        return AIQualityReport(
            pattern_hash=data["pattern_hash"],
            compiler_valid=data["compiler_valid"],
            compiler_errors=data.get("compiler_errors", []),
            claims=[
                AIClaim(**item) for item in data.get("claims", [])
            ],
            repairs=[
                RepairProposal(**item) for item in data.get("repairs", [])
            ],
            disagreements=data.get("disagreements", []),
            providers_used=data.get("providers_used", []),
            mode=data.get("mode", "cached"),
            recommendation=data.get("recommendation", ""),
        )


def quality_check(pattern, report, mode: str = "offline") -> AIQualityReport:
    """Convenience API for AI quality checking."""
    return AIQualityChecker(mode=mode).check(pattern, report)
