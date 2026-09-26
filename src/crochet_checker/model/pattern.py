"""
Pattern model - the top-level representation of a crochet pattern.

This is the central data structure that all other components operate on.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .instruction import Instruction
from .row import Row, Round, RowOrRound
from .yarn import Yarn, Hook, Gauge


class ConstructionType(str, Enum):
    """How the pattern is constructed."""

    FLAT = "flat"           # Worked in rows, back and forth
    IN_THE_ROUND = "in_the_round"  # Worked in continuous rounds
    JOINED_ROUNDS = "joined_rounds"  # Rounds joined with slip stitch
    MOTIF = "motif"         # Multiple motifs joined together
    ASSEMBLY = "assembly"   # Multiple pieces sewn together


class PatternMetadata(BaseModel):
    """Metadata about the pattern."""

    title: Optional[str] = None
    designer: Optional[str] = None
    difficulty: Optional[str] = None  # beginner, easy, intermediate, advanced
    category: Optional[str] = None  # hat, scarf, amigurumi, blanket, etc.
    description: Optional[str] = None
    pattern_id: Optional[str] = None
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    checker_version: str = "0.1.0"


class PatternPiece(BaseModel):
    """A single piece/component of a multi-piece crochet pattern."""
    
    name: str = Field(description="Piece name (e.g., 'HEAD', 'ARMS', 'GILLS')")
    make_count: Optional[int] = Field(default=None, description="How many to make (e.g., 2 for 'make 2')")
    rounds: list[Round] = Field(default_factory=list, description="Rounds for this piece")
    rows: list[Row] = Field(default_factory=list, description="Rows for this piece")
    notes: list[str] = Field(default_factory=list, description="Piece-specific notes")
    
    @property
    def is_rounds(self) -> bool:
        """Whether this piece uses rounds (vs rows)."""
        return len(self.rounds) > 0
    
    @property
    def total_rows_or_rounds(self) -> int:
        """Total number of rows or rounds in this piece."""
        return len(self.rounds) if self.is_rounds else len(self.rows)


class Pattern(BaseModel):
    """
    Top-level representation of a crochet pattern.

    This is the structured intermediate representation that all validators,
    simulators, and visualizers operate on.
    """

    metadata: PatternMetadata = Field(default_factory=PatternMetadata)
    source_text: str = Field(default="", description="Original full pattern text")
    construction: ConstructionType = Field(default=ConstructionType.FLAT)
    yarn: Optional[Yarn] = None
    hook: Optional[Hook] = None
    gauge: Optional[Gauge] = None
    abbreviations: dict[str, str] = Field(
        default_factory=dict,
        description="Custom abbreviation mappings",
    )
    notes: list[str] = Field(default_factory=list)
    rows: list[Row] = Field(default_factory=list)
    rounds: list[Round] = Field(default_factory=list)
    finishing: list[str] = Field(default_factory=list)
    special_stitches: dict[str, str] = Field(default_factory=dict)
    pieces: list[PatternPiece] = Field(default_factory=list, description="For multi-piece patterns, each component")
    pieces: list[PatternPiece] = Field(default_factory=list, description="For multi-piece patterns, each component")

    @property
    def rows_or_rounds(self) -> list[RowOrRound]:
        """Get all rows or rounds as a unified list."""
        result: list[RowOrRound] = []
        if self.rounds:
            for r in self.rounds:
                result.append(RowOrRound(is_round=True, **{"round": r}))
        elif self.rows:
            for r in self.rows:
                result.append(RowOrRound(is_round=False, row=r))
        return result

    @property
    def total_rows_or_rounds(self) -> int:
        """Total number of rows or rounds."""
        if self.rounds:
            return len(self.rounds)
        return len(self.rows)

    @property
    def stitch_counts(self) -> list[tuple[int, int]]:
        """
        Returns a list of (row/round number, stitch count) tuples.
        This is the key data for stitch-count validation.
        """
        counts: list[tuple[int, int]] = []
        if self.rounds:
            for r in self.rounds:
                counts.append((r.round_number, r.computed_stitch_count))
        elif self.rows:
            for r in self.rows:
                counts.append((r.row_number, r.computed_stitch_count))
        return counts

    def get_round(self, number: int) -> Optional[Round]:
        """Get a round by number."""
        for r in self.rounds:
            if r.round_number == number:
                return r
        return None

    def get_row(self, number: int) -> Optional[Row]:
        """Get a row by number."""
        for r in self.rows:
            if r.row_number == number:
                return r
        return None

    def get_all_instructions(self) -> list[Instruction]:
        """Get all instructions from all rows/rounds."""
        instructions: list[Instruction] = []
        if self.rounds:
            for r in self.rounds:
                instructions.extend(r.instructions)
        elif self.rows:
            for r in self.rows:
                instructions.extend(r.instructions)
        return instructions


class Project(BaseModel):
    """A project wrapping a pattern with additional context for validation and publishing."""

    pattern: Pattern
    validation_report: Optional[dict] = None
    output_directory: Optional[str] = None
    images: list[str] = Field(default_factory=list)
    pdf_path: Optional[str] = None


class PatternPiece(BaseModel):
    """A single piece/component of a multi-piece crochet pattern."""
    
    name: str = Field(description="Piece name (e.g., 'HEAD', 'ARMS', 'GILLS')")
    make_count: Optional[int] = Field(default=None, description="How many to make (e.g., 2 for 'make 2')")
    rounds: list[Round] = Field(default_factory=list, description="Rounds for this piece")
    rows: list[Row] = Field(default_factory=list, description="Rows for this piece")
    notes: list[str] = Field(default_factory=list, description="Piece-specific notes")
    
    @property
    def is_rounds(self) -> bool:
        """Whether this piece uses rounds (vs rows)."""
        return len(self.rounds) > 0
    
    @property
    def total_rows_or_rounds(self) -> int:
        """Total number of rows or rounds in this piece."""
        return len(self.rounds) if self.is_rounds else len(self.rows)
