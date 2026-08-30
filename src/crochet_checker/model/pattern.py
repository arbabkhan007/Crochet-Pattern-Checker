from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from .instruction import Instruction
from .row import Row, Round
from .yarn import Yarn, Hook, Gauge

class ConstructionType(str, Enum):
    FLAT = "flat"; IN_THE_ROUND = "in_the_round"; JOINED_ROUNDS = "joined_rounds"

class PatternMetadata(BaseModel):
    title: Optional[str] = None; designer: Optional[str] = None
    version: str = "1.0"; created_at: datetime = Field(default_factory=datetime.now)

class Pattern(BaseModel):
    metadata: PatternMetadata = Field(default_factory=PatternMetadata)
    source_text: str = ""
    construction: ConstructionType = Field(default=ConstructionType.FLAT)
    yarn: Optional[Yarn] = None; hook: Optional[Hook] = None; gauge: Optional[Gauge] = None
    rows: list[Row] = Field(default_factory=list)
    rounds: list[Round] = Field(default_factory=list)
    @property
    def total_rows_or_rounds(self): return len(self.rounds) if self.rounds else len(self.rows)
    def get_all_instructions(self):
        inst = []
        if self.rounds:
            for r in self.rounds: inst.extend(r.instructions)
        elif self.rows:
            for r in self.rows: inst.extend(r.instructions)
        return inst
