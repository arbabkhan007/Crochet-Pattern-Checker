"""Validation pipeline: runs every deterministic validator and aggregates the findings.

This module is the single entry point used by the CLI, the web app, the AI
helpers and the tests (``validate_pattern``).  AI never decides correctness -
everything in here is plain arithmetic over the parsed pattern.
"""
from __future__ import annotations

from .stitch_counts import (
    Severity,
    StitchCountReport,
    StitchCountValidator,
    ValidationFinding,
    validate_stitch_counts,
)
from .row_transitions import RowTransitionValidator, TransitionReport
from .consistency import ConsistencyValidator, ConsistencyReport


class OverallStatus:
    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    ERROR = "ERROR"


class ValidationReport:
    def __init__(self):
        self.stitch_counts: StitchCountReport | None = None
        self.row_transitions: TransitionReport | None = None
        self.consistency: ConsistencyReport | None = None

    @property
    def all_findings(self) -> list[ValidationFinding]:
        f: list[ValidationFinding] = []
        if self.stitch_counts:
            f.extend(self.stitch_counts.findings)
        if self.row_transitions:
            f.extend(self.row_transitions.findings)
        if self.consistency:
            f.extend(self.consistency.findings)
        return f

    @property
    def errors(self):
        return [f for f in self.all_findings if f.severity in (Severity.ERROR, Severity.CRITICAL)]

    @property
    def warnings(self):
        return [f for f in self.all_findings if f.severity == Severity.WARNING]

    @property
    def infos(self):
        return [f for f in self.all_findings if f.severity == Severity.INFO]

    @property
    def overall_status(self) -> str:
        if not self.all_findings:
            return OverallStatus.PASS
        if self.errors:
            if len(self.errors) > 2 or any(f.severity == Severity.CRITICAL for f in self.errors):
                return OverallStatus.ERROR
            return OverallStatus.NEEDS_REVIEW
        if self.warnings:
            return OverallStatus.PASS_WITH_WARNINGS
        return OverallStatus.PASS

    @property
    def score(self) -> int:
        s = 100
        for f in self.all_findings:
            if f.severity == Severity.CRITICAL:
                s -= 25
            elif f.severity == Severity.ERROR:
                s -= 15
            elif f.severity == Severity.WARNING:
                s -= 5
            elif f.severity == Severity.INFO:
                s -= 1
        return max(0, min(100, s))

    def to_dict(self) -> dict:
        return {
            "overall_status": self.overall_status,
            "score": self.score,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "findings": [f.model_dump() for f in self.all_findings],
        }


class ValidationPipeline:
    def __init__(self, strict: bool = False):
        self.strict = strict

    def validate(self, pattern) -> ValidationReport:
        r = ValidationReport()
        r.stitch_counts = StitchCountValidator().validate(pattern)
        r.row_transitions = RowTransitionValidator().validate(pattern)
        r.consistency = ConsistencyValidator().validate(pattern)
        if self.strict:
            for f in r.all_findings:
                if f.severity == Severity.WARNING:
                    f.severity = Severity.ERROR
        return r


def validate_pattern(pattern, strict: bool = False) -> ValidationReport:
    return ValidationPipeline(strict).validate(pattern)


__all__ = [
    "OverallStatus",
    "Severity",
    "StitchCountReport",
    "StitchCountValidator",
    "ValidationFinding",
    "ValidationPipeline",
    "ValidationReport",
    "validate_pattern",
    "validate_stitch_counts",
]
