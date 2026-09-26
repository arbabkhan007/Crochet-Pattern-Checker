"""
Stitch count validation engine.

This is the core mathematical validation that checks whether stitch counts
are consistent across rows/rounds. It is fully deterministic - no AI involved.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from ..model.instruction import Instruction
from ..model.pattern import Pattern
from ..model.row import Round, Row
from ..model.stitch import STITCH_CONSUMPTION, STITCH_PRODUCTION, StitchType


class Severity(str, Enum):
    """Severity level for validation findings."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ValidationFinding(BaseModel):
    """A single finding from the validation engine."""

    validator: str
    severity: Severity
    location: str = ""
    message: str
    original_instruction: str | None = None
    expected: int | None = None
    actual: int | None = None
    suggested_fix: str | None = None
    confidence: float = 1.0


class StitchCountReport(BaseModel):
    """Report of stitch count validation for the entire pattern."""

    pattern_title: str = ""
    is_consistent: bool = True
    total_rows_checked: int = 0
    findings: list[ValidationFinding] = Field(default_factory=list)
    row_by_row: list[dict] = Field(default_factory=list)

    @property
    def errors(self) -> list[ValidationFinding]:
        return [
            f
            for f in self.findings
            if f.severity in (Severity.ERROR, Severity.CRITICAL)
        ]

    @property
    def warnings(self) -> list[ValidationFinding]:
        return [f for f in self.findings if f.severity == Severity.WARNING]

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0


class StitchCountValidator:
    """
    Validates stitch counts across all rows/rounds of a pattern.

    For each row/round, calculates:
    - Expected starting count (from previous row's ending count)
    - Stitches consumed from previous row
    - Stitches produced in current row
    - Expected ending count
    - Stated ending count (if provided)

    Then checks consistency between all of these.
    """

    def __init__(self) -> None:
        self.findings: list[ValidationFinding] = []

    def _detect_pieces(self, rounds: list) -> list[tuple[int, int]]:
        """Detect piece boundaries based on round number resets."""
        pieces = []
        current_start = 0

        for i in range(1, len(rounds)):
            # If round number decreases, it's a new piece
            if rounds[i].round_number < rounds[i - 1].round_number:
                pieces.append((current_start, i))
                current_start = i

        # Add last piece
        pieces.append((current_start, len(rounds)))
        return pieces

    def validate(self, pattern: Pattern) -> StitchCountReport:
        """Run full stitch count validation on a pattern."""
        self.findings = []
        report = StitchCountReport(
            pattern_title=pattern.metadata.title or "Untitled Pattern"
        )

        if pattern.rounds:
            self._validate_rounds(pattern.rounds, report)
        elif pattern.rows:
            self._validate_rows(pattern.rows, report)
        else:
            self.findings.append(
                ValidationFinding(
                    validator="stitch_counts",
                    severity=Severity.WARNING,
                    message="Pattern has no rows or rounds to validate.",
                )
            )

        report.findings = self.findings
        report.total_rows_checked = report.total_rows_checked
        report.is_consistent = not report.has_errors

        return report

    def _validate_rounds(self, rounds: list[Round], report: StitchCountReport) -> None:
        """Validate stitch counts across rounds."""
        if not rounds:
            return

        expected_next_start: int | None = None

        for i, current_round in enumerate(rounds):
            round_num = current_round.round_number
            location = f"Round {round_num}"

            # Calculate what this round produces
            produced = 0
            consumed = 0
            has_ambiguous = False

            for inst in current_round.instructions:
                if inst.is_ambiguous:
                    has_ambiguous = True
                    continue

                # Check for "each st around" or "remaining" which need context
                for op in inst.operations:
                    if op.into_stitch in ("each_stitch_around", "remaining"):
                        has_ambiguous = True
                        continue

                inst_produced = inst.total_stitches_produced
                inst_consumed = inst.total_stitches_consumed

                # If instruction has "each st around", resolve against expected start
                if self._has_context_dependent_ops(inst):
                    if expected_next_start is not None:
                        # Recalculate with context
                        resolved_produced = self._resolve_context_dependent(
                            inst, expected_next_start
                        )
                        resolved_consumed = expected_next_start
                        produced += resolved_produced
                        consumed += resolved_consumed
                    else:
                        has_ambiguous = True
                else:
                    produced += inst_produced
                    consumed += inst_consumed

            # Record row-by-row data
            row_data = {
                "round": round_num,
                "source_text": current_round.source_text,
                "stitches_produced": produced,
                "stitches_consumed": consumed,
                "expected_start": expected_next_start,
            }

            # Check 1: Does starting count match what previous round produced?
            if expected_next_start is not None:
                if consumed != expected_next_start and not has_ambiguous:
                    self.findings.append(
                        ValidationFinding(
                            validator="stitch_counts",
                            severity=Severity.ERROR,
                            location=location,
                            message=(
                                f"Round {round_num} consumes {consumed} stitches "
                                f"but Round {round_num - 1} produced {expected_next_start} stitches."
                            ),
                            expected=expected_next_start,
                            actual=consumed,
                            suggested_fix=f"Review instructions in Round {round_num} for missing or extra stitches.",
                        )
                    )
                row_data["start_matches"] = (
                    consumed == expected_next_start or has_ambiguous
                )

            # Check 2: Does stated count match computed count?
            stated = self._get_stated_total(current_round)
            if stated is not None and not has_ambiguous:
                if stated != produced:
                    self.findings.append(
                        ValidationFinding(
                            validator="stitch_counts",
                            severity=Severity.ERROR,
                            location=location,
                            message=(
                                f"Round {round_num} states {stated} stitches "
                                f"but instructions produce {produced} stitches."
                            ),
                            expected=stated,
                            actual=produced,
                            original_instruction=current_round.source_text,
                            suggested_fix=f"Check if the instructions in Round {round_num} are correct.",
                        )
                    )
                row_data["stated_count_matches"] = stated == produced
                row_data["stated_count"] = stated
            elif stated is not None and has_ambiguous:
                row_data["stated_count"] = stated
                row_data["stated_count_matches"] = None  # Can't verify

            # Check 3: First round special handling
            if i == 0 and expected_next_start is None:
                # First round - check if it starts from magic ring or chain
                first_stitches = (
                    current_round.instructions[0].operations
                    if current_round.instructions
                    else []
                )
                if any(
                    op.stitch_type == StitchType.MAGIC_RING for op in first_stitches
                ):
                    # Magic ring - the produced count becomes the starting count for next round
                    row_data["starts_from_magic_ring"] = True
                else:
                    self.findings.append(
                        ValidationFinding(
                            validator="stitch_counts",
                            severity=Severity.INFO,
                            location=location,
                            message="First round does not start from a magic ring. Starting count unknown.",
                        )
                    )

            # Update expected_next_start for next round
            if not has_ambiguous:
                expected_next_start = produced
            else:
                # If we have a stated count, use that as the expected next start
                if stated is not None:
                    expected_next_start = stated

            row_data["expected_end"] = expected_next_start
            report.row_by_row.append(row_data)
            report.total_rows_checked += 1

            if has_ambiguous:
                self.findings.append(
                    ValidationFinding(
                        validator="stitch_counts",
                        severity=Severity.WARNING,
                        location=location,
                        message=f"Round {round_num} contains context-dependent operations that cannot be fully verified without stitch count context.",
                        confidence=0.7,
                    )
                )

    def _validate_rows(self, rows: list[Row], report: StitchCountReport) -> None:
        """Validate stitch counts across rows."""
        if not rows:
            return

        expected_next_start: int | None = None

        for i, current_row in enumerate(rows):
            row_num = current_row.row_number
            location = f"Row {row_num}"

            produced = 0
            consumed = 0
            has_ambiguous = False

            for inst in current_row.instructions:
                if inst.is_ambiguous:
                    has_ambiguous = True
                    continue

                if self._has_context_dependent_ops(inst):
                    has_ambiguous = True
                else:
                    produced += inst.total_stitches_produced
                    consumed += inst.total_stitches_consumed

            row_data = {
                "row": row_num,
                "source_text": current_row.source_text,
                "stitches_produced": produced,
                "stitches_consumed": consumed,
                "expected_start": expected_next_start,
            }

            if expected_next_start is not None and not has_ambiguous:
                if consumed != expected_next_start:
                    self.findings.append(
                        ValidationFinding(
                            validator="stitch_counts",
                            severity=Severity.ERROR,
                            location=location,
                            message=(
                                f"Row {row_num} consumes {consumed} stitches "
                                f"but Row {row_num - 1} produced {expected_next_start} stitches."
                            ),
                            expected=expected_next_start,
                            actual=consumed,
                        )
                    )

            stated = self._get_stated_total(current_row)
            if stated is not None and not has_ambiguous:
                if stated != produced:
                    self.findings.append(
                        ValidationFinding(
                            validator="stitch_counts",
                            severity=Severity.ERROR,
                            location=location,
                            message=(
                                f"Row {row_num} states {stated} stitches "
                                f"but instructions produce {produced} stitches."
                            ),
                            expected=stated,
                            actual=produced,
                        )
                    )
                row_data["stated_count"] = stated
                row_data["stated_count_matches"] = stated == produced

            if not has_ambiguous:
                expected_next_start = produced
            elif stated is not None:
                expected_next_start = stated

            row_data["expected_end"] = expected_next_start
            report.row_by_row.append(row_data)
            report.total_rows_checked += 1

    def _has_context_dependent_ops(self, instruction: Instruction) -> bool:
        """Check if an instruction has operations that depend on row context."""
        for op in instruction.operations:
            if op.into_stitch in ("each_stitch_around", "remaining"):
                return True
        return False

    def _resolve_context_dependent(
        self, instruction: Instruction, available_stitches: int
    ) -> int:
        """
        Resolve context-dependent operations given the available stitch count.

        For "sc in each st around" with N stitches available, produces N stitches.
        """
        total = 0
        remaining = available_stitches

        for op in instruction.operations:
            if op.into_stitch == "each_stitch_around":
                # Each stitch around = use all remaining stitches
                produced_per = STITCH_PRODUCTION.get(op.stitch_type, 1)
                total += remaining * produced_per
                remaining = 0
            elif op.into_stitch == "remaining":
                produced_per = STITCH_PRODUCTION.get(op.stitch_type, 1)
                total += remaining * produced_per
                remaining = 0
            else:
                produced_per = STITCH_PRODUCTION.get(op.stitch_type, 1)
                consumed_per = STITCH_CONSUMPTION.get(op.stitch_type, 1)
                total += op.count * produced_per
                remaining -= op.count * consumed_per

        return total

    def _get_stated_total(self, row_or_round) -> int | None:
        """Get the stated total stitch count from a row or round."""
        # Check if any instruction has a stated count at the end
        for inst in row_or_round.instructions:
            if inst.stated_stitch_count is not None:
                return inst.stated_stitch_count

        # Check the expected ending count on the row/round itself
        if hasattr(row_or_round, "expected_ending_stitch_count"):
            return row_or_round.expected_ending_stitch_count
        return None


def validate_stitch_counts(pattern: Pattern) -> StitchCountReport:
    """Convenience function to validate stitch counts."""
    validator = StitchCountValidator()
    return validator.validate(pattern)
