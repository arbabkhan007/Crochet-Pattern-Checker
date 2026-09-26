"""
Row/round transition validation.

Checks that transitions between rows/rounds are valid:
- Consistent stitch count changes
- Valid increase/decrease patterns
- No impossible transitions
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..model.pattern import Pattern
from ..model.row import Round, Row
from .stitch_counts import Severity, ValidationFinding


class TransitionReport(BaseModel):
    """Report on row/round transitions."""

    total_transitions_checked: int = 0
    findings: list[ValidationFinding] = Field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(
            f.severity in (Severity.ERROR, Severity.CRITICAL) for f in self.findings
        )


class RowTransitionValidator:
    """Validates transitions between rows/rounds."""

    def __init__(self) -> None:
        self.findings: list[ValidationFinding] = []

    def validate(self, pattern: Pattern) -> TransitionReport:
        """Validate all row/round transitions."""
        self.findings = []
        report = TransitionReport()

        if pattern.rounds:
            self._validate_round_transitions(pattern.rounds, report)
        elif pattern.rows:
            self._validate_row_transitions(pattern.rows, report)

        report.findings = self.findings
        return report

    def _validate_round_transitions(
        self, rounds: list[Round], report: TransitionReport
    ) -> None:
        """Check transitions between consecutive rounds."""
        if len(rounds) < 2:
            return

        for i in range(1, len(rounds)):
            prev = rounds[i - 1]
            curr = rounds[i]
            report.total_transitions_checked += 1

            prev_count = prev.computed_stitch_count
            curr_consumed = curr.computed_stitches_consumed

            # Check for impossible stitch count drops (more than 50% decrease without explanation)
            if prev_count > 0 and curr_consumed > 0:
                ratio = curr_consumed / prev_count
                if ratio < 0.5:
                    self.findings.append(
                        ValidationFinding(
                            validator="row_transitions",
                            severity=Severity.WARNING,
                            location=f"Round {curr.round_number}",
                            message=(
                                f"Stitch count drops from {prev_count} to {curr_consumed} "
                                f"({ratio:.0%}). Large decreases should be verified."
                            ),
                            suggested_fix="Verify that the decreases in this round are intentional.",
                        )
                    )

                # Check for unexplained large increases
                curr_produced = curr.computed_stitch_count
                if curr_produced > prev_count * 2:
                    self.findings.append(
                        ValidationFinding(
                            validator="row_transitions",
                            severity=Severity.WARNING,
                            location=f"Round {curr.round_number}",
                            message=(
                                f"Stitch count increases from {prev_count} to {curr_produced} "
                                f"(more than doubled). Verify increases are intentional."
                            ),
                        )
                    )

            # Check for consistent numbering (no skipped round numbers)
            if curr.round_number != prev.round_number + 1:
                self.findings.append(
                    ValidationFinding(
                        validator="row_transitions",
                        severity=Severity.WARNING,
                        location=f"Round {curr.round_number}",
                        message=(
                            f"Round numbering jumps from {prev.round_number} to {curr.round_number}. "
                            f"Expected consecutive numbering."
                        ),
                    )
                )

    def _validate_row_transitions(
        self, rows: list[Row], report: TransitionReport
    ) -> None:
        """Check transitions between consecutive rows."""
        if len(rows) < 2:
            return

        for i in range(1, len(rows)):
            prev = rows[i - 1]
            curr = rows[i]
            report.total_transitions_checked += 1

            # Check consistent numbering
            if curr.row_number != prev.row_number + 1:
                self.findings.append(
                    ValidationFinding(
                        validator="row_transitions",
                        severity=Severity.WARNING,
                        location=f"Row {curr.row_number}",
                        message=(
                            f"Row numbering jumps from {prev.row_number} to {curr.row_number}."
                        ),
                    )
                )


def validate_row_transitions(pattern: Pattern) -> TransitionReport:
    """Convenience function."""
    validator = RowTransitionValidator()
    return validator.validate(pattern)
