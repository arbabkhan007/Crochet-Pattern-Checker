"""
AST Node Definitions for Crochet Pattern Parser
Defines the hierarchical structure for multi-piece patterns
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConstructionType(Enum):
    ROUNDS = "ROUNDS"
    ROWS = "ROWS"


class LoopStatus(Enum):
    AVAILABLE = "available"
    WORKED_INTO = "worked_into"
    SKIPPED = "skipped"


@dataclass
class StitchNode:
    """Represents a single stitch instruction"""

    stitch_type: str
    count: int = 1
    position: int | None = None
    line_number: int = 0
    raw_text: str = ""

    def __post_init__(self):
        self.count = max(self.count, 1)


@dataclass
class RoundNode:
    """Represents a single round or row"""

    number: int
    instructions: list[StitchNode] = field(default_factory=list)
    stitch_count: int = 0
    line_number: int = 0
    raw_text: str = ""

    def add_stitch(self, stitch: StitchNode):
        self.instructions.append(stitch)
        self.stitch_count += stitch.count

    def get_total_stitches(self) -> int:
        return sum(stitch.count for stitch in self.instructions)


@dataclass
class PieceNode:
    """Represents a distinct piece/module of the pattern"""

    name: str
    construction_type: ConstructionType
    rounds: list[RoundNode] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_round(self, round_node: RoundNode):
        self.rounds.append(round_node)

    def get_round(self, number: int) -> RoundNode | None:
        for r in self.rounds:
            if r.number == number:
                return r
        return None

    def get_total_stitches(self) -> int:
        return sum(r.get_total_stitches() for r in self.rounds)


@dataclass
class PatternNode:
    """Root node representing the entire pattern"""

    title: str = ""
    pieces: list[PieceNode] = field(default_factory=list)
    glossary: dict[str, str] = field(default_factory=dict)
    abbreviations: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_piece(self, piece: PieceNode):
        self.pieces.append(piece)

    def get_piece(self, name: str) -> PieceNode | None:
        for piece in self.pieces:
            if piece.name.lower() == name.lower():
                return piece
        return None

    def get_all_pieces(self) -> list[PieceNode]:
        return self.pieces

    def get_total_stitches(self) -> int:
        return sum(piece.get_total_stitches() for piece in self.pieces)


@dataclass
class InstructionNode:
    """Represents an expanded instruction after unrolling"""

    action: str
    stitch_type: str
    count: int = 1
    target_position: int | None = None
    is_turning_chain: bool = False
    counts_as_stitch: bool = False
    line_number: int = 0

    def __post_init__(self):
        self.count = max(self.count, 1)
