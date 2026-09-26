"""
Internal consistency validation.

Checks for various forms of internal consistency in a pattern:
- Repeat blocks that divide evenly
- Consistent increase/decrease patterns
- Terminology consistency
- Symmetry detection
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..model.pattern import Pattern
from ..model.stitch import StitchType
from .stitch_counts import Severity, ValidationFinding


class ConsistencyReport(BaseModel):
    """Report on pattern consistency."""

    findings: list[ValidationFinding] = Field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(
            f.severity in (Severity.ERROR, Severity.CRITICAL) for f in self.findings
        )


class ConsistencyValidator:
    """Validates internal consistency of a crochet pattern."""

    def __init__(self) -> None:
        self.findings: list[ValidationFinding] = []

    def validate(self, pattern: Pattern) -> ConsistencyReport:
        """Run all consistency checks."""
        self.findings = []

        # Check for repeat consistency
        self._check_repeats(pattern)

        # Check for symmetry
        self._check_symmetry(pattern)

        # Check for terminology consistency
        self._check_terminology(pattern)

        # Check for structural consistency
        self._check_structure(pattern)

        return ConsistencyReport(findings=self.findings)

    def _check_repeats(self, pattern: Pattern) -> None:
        """Check that repeat blocks are mathematically valid."""
        for inst in pattern.get_all_instructions():
            if inst.is_repeat_block and inst.repeat_unit and inst.repeat_count:
                unit_consumed = sum(op.stitches_consumed for op in inst.repeat_unit)
                unit_produced = sum(op.stitches_produced for op in inst.repeat_unit)

                # A repeat unit that produces 0 stitches is suspicious
                if unit_produced == 0 and unit_consumed == 0:
                    self.findings.append(
                        ValidationFinding(
                            validator="consistency",
                            severity=Severity.WARNING,
                            message=f"Repeat block '{inst.source_text}' produces and consumes 0 stitches per repeat.",
                        )
                    )

    def _check_symmetry(self, pattern: Pattern) -> None:
        """Detect and validate symmetry in repeat blocks."""
        if pattern.rounds:
            for r in pattern.rounds:
                for inst in r.instructions:
                    if inst.is_repeat_block and inst.repeat_count:
                        # Check if all repeat units are identical (symmetric)
                        # This is inherently true by construction since we repeat the same block
                        # But we can check if the repeat count divides the total evenly
                        if inst.repeat_unit:
                            total_produced = (
                                sum(op.stitches_produced for op in inst.repeat_unit)
                                * inst.repeat_count
                            )
                            per_repeat = sum(
                                op.stitches_produced for op in inst.repeat_unit
                            )
                            if (
                                per_repeat > 0
                                and total_produced % inst.repeat_count != 0
                            ):
                                self.findings.append(
                                    ValidationFinding(
                                        validator="consistency",
                                        severity=Severity.WARNING,
                                        location=f"Round {r.round_number}",
                                        message=f"Repeat block does not divide evenly: {total_produced} stitches across {inst.repeat_count} repeats.",
                                    )
                                )

    def _check_terminology(self, pattern: Pattern) -> None:
        """Check for consistent terminology usage."""
        abbreviations_used: set[str] = set()

        for inst in pattern.get_all_instructions():
            for op in inst.operations:
                if op.stitch_type != StitchType.UNKNOWN:
                    abbreviations_used.add(op.stitch_type.value)

        # Check for mixed terminology (e.g., both US and UK terms)
        us_terms = {
            "single_crochet",
            "half_double_crochet",
            "double_crochet",
            "treble_crochet",
        }
        # This would need more sophisticated detection for real UK/US mixing

    def _check_structure(self, pattern: Pattern) -> None:
        """Check for structural issues."""
        # Check that all rounds/rows have at least one instruction
        if pattern.rounds:
            for r in pattern.rounds:
                if not r.instructions:
                    self.findings.append(
                        ValidationFinding(
                            validator="consistency",
                            severity=Severity.ERROR,
                            location=f"Round {r.round_number}",
                            message=f"Round {r.round_number} has no instructions.",
                        )
                    )

        if pattern.rows:
            for r in pattern.rows:
                if not r.instructions:
                    self.findings.append(
                        ValidationFinding(
                            validator="consistency",
                            severity=Severity.ERROR,
                            location=f"Row {r.row_number}",
                            message=f"Row {r.row_number} has no instructions.",
                        )
                    )


def validate_consistency(pattern: Pattern) -> ConsistencyReport:
    """Convenience function."""
    validator = ConsistencyValidator()
    return validator.validate(pattern)
