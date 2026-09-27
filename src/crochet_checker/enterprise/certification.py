"""Enterprise-grade digital certification for crochet patterns."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class CertificationLevel(str, Enum):
    REJECTED = "REJECTED"
    SAMPLE_REQUIRED = "SAMPLE_REQUIRED"
    CONDITIONALLY_CERTIFIED = "CONDITIONALLY_CERTIFIED"
    CERTIFIED = "CERTIFIED"


@dataclass
class RiskItem:
    category: str
    severity: str
    message: str
    recommendation: str = ""


@dataclass
class CertificationReport:
    pattern_hash: str
    level: CertificationLevel
    compiler_valid: bool
    confidence: float
    tolerance_pass_probability: float
    sample_required: bool
    risks: list[RiskItem] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    created_at: str = ""
    engine_version: str = "1.0.0"

    @property
    def approved_for_production(self) -> bool:
        return self.level in {
            CertificationLevel.CERTIFIED,
            CertificationLevel.CONDITIONALLY_CERTIFIED,
        }

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["level"] = self.level.value
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class EnterpriseCertifier:
    """
    Converts deterministic validation evidence into a production risk report.

    This engine does not silently approve unknown yarn behavior. Unknown
    material, missing gauge, and uncertain geometry reduce confidence.
    """

    def __init__(
        self,
        tolerance_percent: float = 5.0,
        minimum_confidence: float = 0.90,
        require_gauge: bool = True,
        require_yarn_profile: bool = False,
    ):
        if tolerance_percent <= 0:
            raise ValueError("tolerance_percent must be positive")

        if not 0 < minimum_confidence <= 1:
            raise ValueError("minimum_confidence must be between 0 and 1")

        self.tolerance_percent = tolerance_percent
        self.minimum_confidence = minimum_confidence
        self.require_gauge = require_gauge
        self.require_yarn_profile = require_yarn_profile

    @staticmethod
    def pattern_hash(pattern) -> str:
        source = getattr(pattern, "source_text", repr(pattern))
        return hashlib.sha256(
            source.strip().encode("utf-8")
        ).hexdigest()[:24]

    @staticmethod
    def _errors(report) -> list[str]:
        return [
            getattr(item, "message", str(item))
            for item in getattr(report, "errors", [])
        ]

    @staticmethod
    def _warnings(report) -> list[str]:
        return [
            getattr(item, "message", str(item))
            for item in getattr(report, "warnings", [])
        ]

    @staticmethod
    def _items(pattern):
        return getattr(pattern, "rounds", []) or getattr(pattern, "rows", [])

    def certify(
        self,
        pattern,
        compiler_report,
        *,
        gauge_verified: bool = False,
        yarn_profile_known: bool = False,
        geometry_verified: bool = False,
        ai_conflicts: bool = False,
        safety_passed: bool = True,
        tolerance_passed: bool = True,
    ) -> CertificationReport:
        risks: list[RiskItem] = []
        assumptions: list[str] = []
        evidence: list[str] = []

        errors = self._errors(compiler_report)
        warnings = self._warnings(compiler_report)
        compiler_valid = bool(getattr(compiler_report, "valid", False))

        if compiler_valid and not errors:
            evidence.append("Deterministic compiler validation passed.")
        else:
            risks.append(
                RiskItem(
                    category="compiler",
                    severity="critical",
                    message="Deterministic validation found errors.",
                    recommendation="Correct compiler errors before production.",
                )
            )

        if warnings:
            risks.append(
                RiskItem(
                    category="compiler",
                    severity="medium",
                    message=f"{len(warnings)} compiler warning(s) remain.",
                    recommendation="Review all warnings manually.",
                )
            )

        if self.require_gauge and gauge_verified:
            evidence.append("Gauge profile has been verified.")
        elif self.require_gauge:
            assumptions.append("Gauge profile has not been verified.")
            risks.append(
                RiskItem(
                    category="gauge",
                    severity="high",
                    message="Gauge is unverified.",
                    recommendation="Measure or upload a gauge swatch.",
                )
            )

        if yarn_profile_known:
            evidence.append("Yarn behavior profile is known.")
        elif self.require_yarn_profile:
            assumptions.append("Yarn behavior is unknown.")
            risks.append(
                RiskItem(
                    category="material",
                    severity="high",
                    message="Yarn profile is unknown.",
                    recommendation="Select a verified yarn profile.",
                )
            )

        if geometry_verified:
            evidence.append("Geometry simulation passed.")
        else:
            assumptions.append("Geometry simulation has not been verified.")
            risks.append(
                RiskItem(
                    category="geometry",
                    severity="medium",
                    message="Geometry has not been simulated.",
                    recommendation="Run geometry simulation before production.",
                )
            )

        if ai_conflicts:
            risks.append(
                RiskItem(
                    category="ai",
                    severity="medium",
                    message="AI providers disagree.",
                    recommendation=(
                        "Use deterministic compiler results and review "
                        "the disagreement."
                    ),
                )
            )

        if not safety_passed:
            risks.append(
                RiskItem(
                    category="safety",
                    severity="critical",
                    message="Safety checks failed.",
                    recommendation="Do not approve for production.",
                )
            )

        if tolerance_passed:
            evidence.append(
                f"Predicted dimensions are within ±{self.tolerance_percent}% "
                "tolerance."
            )
        else:
            risks.append(
                RiskItem(
                    category="tolerance",
                    severity="high",
                    message="Predicted dimensions exceed tolerance.",
                    recommendation="Recalibrate gauge or adjust the pattern.",
                )
            )

        confidence = 1.0

        for risk in risks:
            confidence -= {
                "critical": 0.35,
                "high": 0.20,
                "medium": 0.08,
                "low": 0.03,
            }.get(risk.severity, 0.05)

        confidence = max(0.0, min(1.0, confidence))

        critical = any(
            risk.severity == "critical"
            for risk in risks
        )

        sample_required = (
            critical
            or not gauge_verified
            or not geometry_verified
            or not tolerance_passed
            or confidence < self.minimum_confidence
        )

        if critical:
            level = CertificationLevel.REJECTED
        elif sample_required:
            level = CertificationLevel.SAMPLE_REQUIRED
        elif confidence >= self.minimum_confidence:
            level = CertificationLevel.CERTIFIED
        else:
            level = CertificationLevel.CONDITIONALLY_CERTIFIED

        return CertificationReport(
            pattern_hash=self.pattern_hash(pattern),
            level=level,
            compiler_valid=compiler_valid and not errors,
            confidence=round(confidence, 3),
            tolerance_pass_probability=round(
                max(0.0, min(1.0, confidence)),
                3,
            ),
            sample_required=sample_required,
            risks=risks,
            assumptions=assumptions,
            evidence=evidence,
            created_at=datetime.now(timezone.utc).isoformat(),
        )


def certify_pattern(
    pattern,
    compiler_report,
    **kwargs,
) -> CertificationReport:
    """Convenience certification function."""
    return EnterpriseCertifier().certify(
        pattern,
        compiler_report,
        **kwargs,
    )
