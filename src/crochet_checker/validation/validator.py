"""Validation pipeline that combines the individual pattern validators."""

from __future__ import annotations

from ..model.pattern import Pattern
from .consistency import ConsistencyReport, ConsistencyValidator
from .row_transitions import RowTransitionValidator, TransitionReport
from .stitch_counts import (
    Severity,
    StitchCountReport,
    StitchCountValidator,
    ValidationFinding,
)


class OverallStatus:
    """String constants used for the collection-wide validation result."""

    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    ERROR = "ERROR"


class ValidationReport:
    """Combined findings from stitch, transition, and consistency checks."""

    def __init__(self) -> None:
        self.stitch_counts: StitchCountReport | None = None
        self.row_transitions: TransitionReport | None = None
        self.consistency: ConsistencyReport | None = None

    @property
    def all_findings(self) -> list[ValidationFinding]:
        findings: list[ValidationFinding] = []
        if self.stitch_counts:
            findings.extend(self.stitch_counts.findings)
        if self.row_transitions:
            findings.extend(self.row_transitions.findings)
        if self.consistency:
            findings.extend(self.consistency.findings)
        return findings

    @property
    def errors(self) -> list[ValidationFinding]:
        return [
            finding
            for finding in self.all_findings
            if finding.severity in (Severity.ERROR, Severity.CRITICAL)
        ]

    @property
    def warnings(self) -> list[ValidationFinding]:
        return [
            finding
            for finding in self.all_findings
            if finding.severity == Severity.WARNING
        ]

    @property
    def infos(self) -> list[ValidationFinding]:
        return [
            finding
            for finding in self.all_findings
            if finding.severity == Severity.INFO
        ]

    @property
    def overall_status(self) -> str:
        if not self.all_findings:
            return OverallStatus.PASS
        if self.errors:
            if len(self.errors) > 2 or any(
                finding.severity == Severity.CRITICAL for finding in self.errors
            ):
                return OverallStatus.ERROR
            return OverallStatus.NEEDS_REVIEW
        if self.warnings:
            return OverallStatus.PASS_WITH_WARNINGS
        return OverallStatus.PASS

    @property
    def score(self) -> int:
        score = 100
        penalties = {
            Severity.CRITICAL: 25,
            Severity.ERROR: 15,
            Severity.WARNING: 5,
            Severity.INFO: 1,
        }
        for finding in self.all_findings:
            score -= penalties[finding.severity]
        return max(0, min(100, score))

    def to_dict(self) -> dict:
        """Return the stable dictionary representation used by the CLI and API."""

        return {
            "overall_status": self.overall_status,
            "score": self.score,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "findings": [finding.model_dump() for finding in self.all_findings],
        }


class ValidationPipeline:
    """Run each core validator against a parsed pattern."""

    def __init__(self, strict: bool = False) -> None:
        self.strict = strict

    def validate(self, pattern: Pattern) -> ValidationReport:
        report = ValidationReport()
        report.stitch_counts = StitchCountValidator().validate(pattern)
        report.row_transitions = RowTransitionValidator().validate(pattern)
        report.consistency = ConsistencyValidator().validate(pattern)

        if self.strict:
            for finding in report.all_findings:
                if finding.severity == Severity.WARNING:
                    finding.severity = Severity.ERROR
        return report


def validate_pattern(pattern: Pattern, strict: bool = False) -> ValidationReport:
    """Validate a parsed pattern and return one combined report."""

    return ValidationPipeline(strict=strict).validate(pattern)
