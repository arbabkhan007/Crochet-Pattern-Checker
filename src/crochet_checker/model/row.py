from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from .instruction import Instruction

class Row(BaseModel):
    row_number: int
    instructions: list[Instruction] = Field(default_factory=list)
    source_text: str = ""
    @property
    def computed_stitch_count(self):
        return sum(i.total_stitches_produced for i in self.instructions)
    @property
    def computed_stitches_consumed(self):
        return sum(i.total_stitches_consumed for i in self.instructions)
    def compute_stitch_count_with_context(self, prev):
        from .stitch import STITCH_PRODUCTION, STITCH_CONSUMPTION
        remaining, total = prev, 0
        for inst in self.instructions:
            if inst.is_repeat_block and inst.repeat_unit and inst.repeat_count:
                total += sum(o.stitches_produced for o in inst.repeat_unit) * inst.repeat_count
                remaining -= sum(o.stitches_consumed for o in inst.repeat_unit) * inst.repeat_count
                continue
            for op in inst.operations:
                if op.into_stitch in ("each_stitch_around", "remaining"):
                    total += remaining * STITCH_PRODUCTION.get(op.stitch_type, 1); remaining = 0
                else:
                    total += op.count * STITCH_PRODUCTION.get(op.stitch_type, 1)
                    remaining -= op.count * STITCH_CONSUMPTION.get(op.stitch_type, 1)
        return total

class Round(BaseModel):
    round_number: int
    instructions: list[Instruction] = Field(default_factory=list)
    source_text: str = ""
    @property
    def computed_stitch_count(self):
        return sum(i.total_stitches_produced for i in self.instructions)
    @property
    def computed_stitches_consumed(self):
        return sum(i.total_stitches_consumed for i in self.instructions)
    def compute_stitch_count_with_context(self, prev):
        from .stitch import STITCH_PRODUCTION, STITCH_CONSUMPTION
        remaining, total = prev, 0
        for inst in self.instructions:
            if inst.is_repeat_block and inst.repeat_unit and inst.repeat_count:
                total += sum(o.stitches_produced for o in inst.repeat_unit) * inst.repeat_count
                remaining -= sum(o.stitches_consumed for o in inst.repeat_unit) * inst.repeat_count
                continue
            for op in inst.operations:
                if op.into_stitch in ("each_stitch_around", "remaining"):
                    total += remaining * STITCH_PRODUCTION.get(op.stitch_type, 1); remaining = 0
                else:
                    total += op.count * STITCH_PRODUCTION.get(op.stitch_type, 1)
                    remaining -= op.count * STITCH_CONSUMPTION.get(op.stitch_type, 1)
        return total
