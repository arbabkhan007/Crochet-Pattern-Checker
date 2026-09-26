"""
Row and Round models for crochet patterns.

A Row is a single line of work in flat crochet (worked back and forth).
A Round is a single circuit in circular/tubular crochet (worked in the round).
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .instruction import Instruction


class Row(BaseModel):
    """A single row in a flat crochet pattern."""

    row_number: int
    instructions: list[Instruction] = Field(default_factory=list)
    source_text: str = ""
    is_wrong_side: bool = False
    turning_chain: int | None = None
    starting_stitch_count: int | None = None
    expected_ending_stitch_count: int | None = None

    @property
    def computed_stitch_count(self) -> int:
        """Calculate the total stitches produced by all instructions in this row."""
        return sum(inst.total_stitches_produced for inst in self.instructions)

    @property
    def computed_stitches_consumed(self) -> int:
        """Calculate the total stitches consumed from the previous row."""
        return sum(inst.total_stitches_consumed for inst in self.instructions)

    def compute_stitch_count_with_context(self, previous_stitch_count: int) -> int:
        """
        Calculate stitches produced, using context for operations like
        'each st across' or 'remaining'.

        Args:
            previous_stitch_count: The number of stitches in the previous row.

        Returns:
            The computed stitch count for this row.
        """
        from ..model.stitch import STITCH_CONSUMPTION, STITCH_PRODUCTION

        remaining = previous_stitch_count
        total_produced = 0

        for inst in self.instructions:
            if inst.is_repeat_block and inst.repeat_unit and inst.repeat_count:
                unit_produced = sum(op.stitches_produced for op in inst.repeat_unit)
                total_produced += unit_produced * inst.repeat_count
                unit_consumed = sum(op.stitches_consumed for op in inst.repeat_unit)
                remaining -= unit_consumed * inst.repeat_count
                continue

            for op in inst.operations:
                if op.into_stitch in ("each_stitch_around", "remaining"):
                    per = STITCH_PRODUCTION.get(op.stitch_type, 1)
                    total_produced += remaining * per
                    remaining = 0
                else:
                    per = STITCH_PRODUCTION.get(op.stitch_type, 1)
                    cons = STITCH_CONSUMPTION.get(op.stitch_type, 1)
                    total_produced += op.count * per
                    remaining -= op.count * cons

        return total_produced

    def validate_internal_consistency(self) -> list[str]:
        """Check for internal inconsistencies within this row."""
        issues: list[str] = []

        # Check if stated count matches computed count
        for inst in self.instructions:
            if inst.stated_stitch_count is not None:
                computed = inst.total_stitches_produced
                if computed != inst.stated_stitch_count:
                    issues.append(
                        f"Instruction '{inst.source_text}' states "
                        f"{inst.stated_stitch_count} stitches but operations "
                        f"produce {computed}."
                    )

        return issues


class Round(BaseModel):
    """A single round in a circular/tubular crochet pattern."""

    round_number: int
    instructions: list[Instruction] = Field(default_factory=list)
    source_text: str = ""
    starting_stitch_count: int | None = None
    expected_ending_stitch_count: int | None = None
    join_at_end: bool = False
    is_continuous: bool = True

    @property
    def computed_stitch_count(self) -> int:
        """Calculate the total stitches produced by all instructions in this round."""
        return sum(inst.total_stitches_produced for inst in self.instructions)

    @property
    def computed_stitches_consumed(self) -> int:
        """Calculate the total stitches consumed from the previous round."""
        return sum(inst.total_stitches_consumed for inst in self.instructions)

    def compute_stitch_count_with_context(self, previous_stitch_count: int) -> int:
        """
        Calculate stitches produced, using context for operations like
        'each st around' or 'remaining'.

        Args:
            previous_stitch_count: The number of stitches in the previous round.

        Returns:
            The computed stitch count for this round.
        """
        from ..model.stitch import STITCH_CONSUMPTION, STITCH_PRODUCTION

        remaining = previous_stitch_count
        total_produced = 0

        for inst in self.instructions:
            if inst.is_repeat_block and inst.repeat_unit and inst.repeat_count:
                # Repeat blocks don't need context
                unit_produced = sum(op.stitches_produced for op in inst.repeat_unit)
                total_produced += unit_produced * inst.repeat_count
                unit_consumed = sum(op.stitches_consumed for op in inst.repeat_unit)
                remaining -= unit_consumed * inst.repeat_count
                continue

            for op in inst.operations:
                if op.into_stitch == "each_stitch_around":
                    # Each remaining stitch gets this operation
                    per = STITCH_PRODUCTION.get(op.stitch_type, 1)
                    total_produced += remaining * per
                    remaining = 0
                elif op.into_stitch == "remaining":
                    per = STITCH_PRODUCTION.get(op.stitch_type, 1)
                    total_produced += remaining * per
                    remaining = 0
                else:
                    per = STITCH_PRODUCTION.get(op.stitch_type, 1)
                    cons = STITCH_CONSUMPTION.get(op.stitch_type, 1)
                    total_produced += op.count * per
                    remaining -= op.count * cons

        return total_produced

    def validate_internal_consistency(self) -> list[str]:
        """Check for internal inconsistencies within this round."""
        issues: list[str] = []

        for inst in self.instructions:
            if inst.stated_stitch_count is not None:
                computed = inst.total_stitches_produced
                if computed != inst.stated_stitch_count:
                    issues.append(
                        f"Instruction '{inst.source_text}' states "
                        f"{inst.stated_stitch_count} stitches but operations "
                        f"produce {computed}."
                    )

        return issues


class RowOrRound(BaseModel):
    """Unified wrapper for either a row or a round."""

    is_round: bool = True
    row: Row | None = None
    round_: Round | None = Field(default=None, alias="round")

    @property
    def number(self) -> int:
        if self.is_round and self.round_:
            return self.round_.round_number
        elif self.row:
            return self.row.row_number
        raise ValueError("RowOrRound has neither row nor round set")

    @property
    def instructions(self) -> list[Instruction]:
        if self.is_round and self.round_:
            return self.round_.instructions
        elif self.row:
            return self.row.instructions
        return []

    @property
    def computed_stitch_count(self) -> int:
        if self.is_round and self.round_:
            return self.round_.computed_stitch_count
        elif self.row:
            return self.row.computed_stitch_count
        return 0

    @property
    def computed_stitches_consumed(self) -> int:
        if self.is_round and self.round_:
            return self.round_.computed_stitches_consumed
        elif self.row:
            return self.row.computed_stitches_consumed
        return 0

    model_config = {"populate_by_name": True}
