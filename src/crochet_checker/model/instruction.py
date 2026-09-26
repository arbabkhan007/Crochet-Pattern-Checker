from __future__ import annotations

from pydantic import BaseModel, Field

from .stitch import StitchType


class ParsedOperation(BaseModel):
    stitch_type: StitchType
    count: int = Field(default=1, ge=0)
    into_stitch: str | None = None
    is_part_of_repeat: bool = False
    repeat_count: int | None = None

    @property
    def stitches_consumed(self):
        from .stitch import STITCH_CONSUMPTION

        return STITCH_CONSUMPTION.get(self.stitch_type, 1) * self.count

    @property
    def stitches_produced(self):
        from .stitch import STITCH_PRODUCTION

        return STITCH_PRODUCTION.get(self.stitch_type, 1) * self.count


class Instruction(BaseModel):
    source_text: str
    normalized_text: str | None = None
    operations: list[ParsedOperation] = Field(default_factory=list)
    is_repeat_block: bool = False
    repeat_unit: list[ParsedOperation] | None = None
    repeat_count: int | None = None
    stated_stitch_count: int | None = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    is_ambiguous: bool = False
    parse_warnings: list[str] = Field(default_factory=list)

    @property
    def total_stitches_consumed(self):
        if self.is_repeat_block and self.repeat_unit and self.repeat_count:
            return (
                sum(op.stitches_consumed for op in self.repeat_unit) * self.repeat_count
            )
        return sum(op.stitches_consumed for op in self.operations)

    @property
    def total_stitches_produced(self):
        if self.is_repeat_block and self.repeat_unit and self.repeat_count:
            return (
                sum(op.stitches_produced for op in self.repeat_unit) * self.repeat_count
            )
        return sum(op.stitches_produced for op in self.operations)
