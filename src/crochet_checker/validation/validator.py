"""Validation orchestrator — composes all validators into a single report.

This module was reconstructed to restore the documented pipeline:
    Pattern Text -> Parser -> Validators -> ValidationReport -> Report/AI/PDF

All validation remains deterministic — AI never decides mathematical correctness.
"""
from __future__ import annotations
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from ..model.pattern import Pattern
from .stitch_counts import (
    Severity,
    ValidationFinding,
    StitchCountReport,
    StitchCountValidator,
    validate_stitch_counts,
)
from .row_transitions import RowTransitionValidator, TransitionReport
from .consistency import ConsistencyValidator, ConsistencyReport
from .terminology import TerminologyValidator


class OverallStatus(str, Enum):
    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    ERROR = "ERROR"

    @classmethod
    def values(cls):
        return [s.value for s in cls]


class ValidationReport(BaseModel):
    """Aggregate validation report for one parsed pattern."""

    pattern_title: str = ""
    overall_status: OverallStatus = OverallStatus.PASS
    score: int = 100
    stitch_counts: Optional[StitchCountReport] = None
    row_transitions: Optional[TransitionReport] = None
    consistency: Optional[ConsistencyReport] = None
    terminology_issues: List[dict] = Field(default_factory=list)
    findings: List[ValidationFinding] = Field(default_factory=list)

    # ---- aliases kept for backwards compatibility with older call sites ----
    @property
    def status(self) -> OverallStatus:
        return self.overall_status

    @property
    def overall_score(self) -> int:
        return self.score

    # ---- severity helpers ----
    @property
    def errors(self) -> List[ValidationFinding]:
        return [f for f in self.findings if f.severity in (Severity.ERROR, Severity.CRITICAL)]

    @property
    def warnings(self) -> List[ValidationFinding]:
        return [f for f in self.findings if f.severity == Severity.WARNING]

    @property
    def infos(self) -> List[ValidationFinding]:
        return [f for f in self.findings if f.severity == Severity.INFO]

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def is_consistent(self) -> bool:
        return not self.has_errors

    def to_dict(self) -> dict:
        def _f(f: ValidationFinding) -> dict:
            return {
                "validator": f.validator,
                "severity": f.severity.value if isinstance(f.severity, Severity) else str(f.severity),
                "location": f.location,
                "message": f.message,
                "expected": f.expected,
                "actual": f.actual,
                "suggested_fix": f.suggested_fix,
                "confidence": f.confidence,
            }

        d = {
            "pattern_title": self.pattern_title,
            "overall_status": self.overall_status.value,
            "score": self.score,
            "is_consistent": self.is_consistent,
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "errors": [_f(f) for f in self.errors],
            "warnings": [_f(f) for f in self.warnings],
            "findings": [_f(f) for f in self.findings],
        }
        if self.stitch_counts is not None:
            d["stitch_counts"] = {
                "pattern_title": self.stitch_counts.pattern_title,
                "is_consistent": self.stitch_counts.is_consistent,
                "total_rows_checked": self.stitch_counts.total_rows_checked,
            }
        if self.row_transitions is not None:
            d["row_transitions"] = {
                "total_transitions_checked": self.row_transitions.total_transitions_checked,
            }
        d["terminology_issues"] = self.terminology_issues
        return d


def validate_pattern(pattern: Pattern, strict: bool = False) -> ValidationReport:
    """Run every deterministic validator over a parsed pattern.

    Args:
        pattern: parsed :class:`~crochet_checker.model.pattern.Pattern`.
        strict: when True, warnings are promoted to errors for status/scoring.
    """
    # ---- run the individual validators ----
    sc = StitchCountValidator().validate(pattern)
    tr = RowTransitionValidator().validate(pattern)
    co = ConsistencyValidator().validate(pattern)

    findings: List[ValidationFinding] = []
    findings.extend(sc.findings)
    findings.extend(tr.findings)
    findings.extend(co.findings)

    # ---- terminology (informational; deterministic US/UK detection) ----
    terminology_issues: List[dict] = []
    try:
        terminology_issues = TerminologyValidator().validate_pattern(pattern)
        for issue in terminology_issues:
            findings.append(ValidationFinding(
                validator="terminology",
                severity=Severity.INFO,
                location=f"Round {issue.get('round', '?')}" if issue.get("round") is not None else "",
                message=issue.get("message", "Terminology issue"),
                suggested_fix=issue.get("suggestion"),
                confidence=0.6,
            ))
    except Exception:
        terminology_issues = []

    # ---- score & status ----
    error_count = len([f for f in findings if f.severity in (Severity.ERROR, Severity.CRITICAL)])
    warning_count = len([f for f in findings if f.severity == Severity.WARNING])
    if strict:
        error_count += warning_count
        warning_count = 0

    score = max(0, 100 - 25 * error_count - 5 * warning_count)

    if error_count:
        status = OverallStatus.ERROR
    elif warning_count:
        status = OverallStatus.PASS_WITH_WARNINGS
    elif not (pattern.rounds or pattern.rows):
        status = OverallStatus.NEEDS_REVIEW
    else:
        status = OverallStatus.PASS

    title = ""
    try:
        title = pattern.metadata.title or ""
    except Exception:
        pass

    return ValidationReport(
        pattern_title=title,
        overall_status=status,
        score=score,
        stitch_counts=sc,
        row_transitions=tr,
        consistency=co,
        terminology_issues=terminology_issues,
        findings=findings,
    )
