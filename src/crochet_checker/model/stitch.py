"""
Stitch definitions and operations for crochet patterns.

This module defines the fundamental stitch vocabulary used throughout the system.
Each stitch type has properties describing how it affects stitch counts, height,
and other relevant attributes.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class StitchType(str, Enum):
    """All supported crochet stitch types (US terminology)."""

    # Basic stitches
    CHAIN = "chain"
    SLIP_STITCH = "slip_stitch"
    SINGLE_CROCHET = "single_crochet"
    HALF_DOUBLE_CROCHET = "half_double_crochet"
    DOUBLE_CROCHET = "double_crochet"
    TREBLE_CROCHET = "treble_crochet"

    # Structural operations
    MAGIC_RING = "magic_ring"
    INCREASE = "increase"
    DECREASE = "decrease"

    # Loop placement
    FRONT_LOOP_ONLY = "front_loop_only"
    BACK_LOOP_ONLY = "back_loop_only"

    # Post stitches
    FRONT_POST = "front_post"
    BACK_POST = "back_post"

    # Specialty stitches
    CLUSTER = "cluster"
    SHELL = "shell"
    BOBBLE = "bobble"
    POPCORN = "popcorn"
    PICOT = "picot"

    # Assembly
    JOIN = "join"
    CHAIN_SPACE = "chain_space"
    SEW = "sew"
    FASTEN_OFF = "fasten_off"

    # Special
    SKIP = "skip"
    TURNING_CHAIN = "turning_chain"
    COLOR_CHANGE = "color_change"
    REPEAT = "repeat"

    # Unknown
    UNKNOWN = "unknown"


# Stitch height in relative units (chain = 1)
STITCH_HEIGHT: dict[StitchType, float] = {
    StitchType.CHAIN: 1.0,
    StitchType.SLIP_STITCH: 0.5,
    StitchType.SINGLE_CROCHET: 1.0,
    StitchType.HALF_DOUBLE_CROCHET: 1.5,
    StitchType.DOUBLE_CROCHET: 2.0,
    StitchType.TREBLE_CROCHET: 3.0,
}

# Standard turning chain counts per stitch type
TURNING_CHAIN_COUNTS: dict[StitchType, int] = {
    StitchType.SINGLE_CROCHET: 1,
    StitchType.HALF_DOUBLE_CROCHET: 2,
    StitchType.DOUBLE_CROCHET: 3,
    StitchType.TREBLE_CROCHET: 4,
}

# How many stitches a single instance of this stitch consumes from the previous row
STITCH_CONSUMPTION: dict[StitchType, int] = {
    StitchType.CHAIN: 0,
    StitchType.SLIP_STITCH: 1,
    StitchType.SINGLE_CROCHET: 1,
    StitchType.HALF_DOUBLE_CROCHET: 1,
    StitchType.DOUBLE_CROCHET: 1,
    StitchType.TREBLE_CROCHET: 1,
    StitchType.INCREASE: 1,
    StitchType.DECREASE: 2,
    StitchType.SKIP: 1,
    StitchType.MAGIC_RING: 0,
}

# How many stitches a single instance of this stitch produces
STITCH_PRODUCTION: dict[StitchType, int] = {
    StitchType.CHAIN: 0,  # chains don't count as stitch body
    StitchType.SLIP_STITCH: 1,
    StitchType.SINGLE_CROCHET: 1,
    StitchType.HALF_DOUBLE_CROCHET: 1,
    StitchType.DOUBLE_CROCHET: 1,
    StitchType.TREBLE_CROCHET: 1,
    StitchType.INCREASE: 2,
    StitchType.DECREASE: 1,
    StitchType.SKIP: 0,
    StitchType.MAGIC_RING: 0,  # magic ring is a starting method, not a stitch
}


class StitchDefinition(BaseModel):
    """Definition of a single stitch type."""

    type: StitchType
    name: str
    abbreviation: str
    uk_equivalent: Optional[str] = None
    consumes_stitches: int = 1
    produces_stitches: int = 1
    relative_height: float = 1.0
    description: str = ""


# Complete stitch definitions
STITCH_DEFINITIONS: dict[StitchType, StitchDefinition] = {
    StitchType.CHAIN: StitchDefinition(
        type=StitchType.CHAIN,
        name="Chain",
        abbreviation="ch",
        uk_equivalent="ch",
        consumes_stitches=0,
        produces_stitches=0,
        relative_height=1.0,
        description="Foundation chain or chain stitch between other stitches",
    ),
    StitchType.SLIP_STITCH: StitchDefinition(
        type=StitchType.SLIP_STITCH,
        name="Slip Stitch",
        abbreviation="sl st",
        uk_equivalent="sl st",
        consumes_stitches=1,
        produces_stitches=1,
        relative_height=0.5,
        description="Flat stitch used for joining and moving yarn",
    ),
    StitchType.SINGLE_CROCHET: StitchDefinition(
        type=StitchType.SINGLE_CROCHET,
        name="Single Crochet",
        abbreviation="sc",
        uk_equivalent="dc",
        consumes_stitches=1,
        produces_stitches=1,
        relative_height=1.0,
        description="Basic crochet stitch",
    ),
    StitchType.HALF_DOUBLE_CROCHET: StitchDefinition(
        type=StitchType.HALF_DOUBLE_CROCHET,
        name="Half Double Crochet",
        abbreviation="hdc",
        uk_equivalent="tr",
        consumes_stitches=1,
        produces_stitches=1,
        relative_height=1.5,
        description="Medium height stitch",
    ),
    StitchType.DOUBLE_CROCHET: StitchDefinition(
        type=StitchType.DOUBLE_CROCHET,
        name="Double Crochet",
        abbreviation="dc",
        uk_equivalent="tr",
        consumes_stitches=1,
        produces_stitches=1,
        relative_height=2.0,
        description="Tall stitch, common in many patterns",
    ),
    StitchType.TREBLE_CROCHET: StitchDefinition(
        type=StitchType.TREBLE_CROCHET,
        name="Treble Crochet",
        abbreviation="tr",
        uk_equivalent="dtr",
        consumes_stitches=1,
        produces_stitches=1,
        relative_height=3.0,
        description="Very tall stitch",
    ),
    StitchType.INCREASE: StitchDefinition(
        type=StitchType.INCREASE,
        name="Increase",
        abbreviation="inc",
        uk_equivalent="inc",
        consumes_stitches=1,
        produces_stitches=2,
        relative_height=1.0,
        description="Two stitches in one stitch from previous row",
    ),
    StitchType.DECREASE: StitchDefinition(
        type=StitchType.DECREASE,
        name="Decrease",
        abbreviation="dec",
        uk_equivalent="dec",
        consumes_stitches=2,
        produces_stitches=1,
        relative_height=1.0,
        description="Two stitches combined into one",
    ),
    StitchType.MAGIC_RING: StitchDefinition(
        type=StitchType.MAGIC_RING,
        name="Magic Ring",
        abbreviation="MR",
        uk_equivalent="magic circle",
        consumes_stitches=0,
        produces_stitches=0,
        relative_height=0.0,
        description="Adjustable ring for starting circular work",
    ),
    StitchType.SKIP: StitchDefinition(
        type=StitchType.SKIP,
        name="Skip",
        abbreviation="sk",
        uk_equivalent="miss",
        consumes_stitches=1,
        produces_stitches=0,
        relative_height=0.0,
        description="Skip one or more stitches from previous row",
    ),
}


class StitchAbbreviationMap:
    """Maps abbreviations to stitch types for parsing."""

    def __init__(self) -> None:
        self._map: dict[str, StitchType] = {}
        self._build_map()

    def _build_map(self) -> None:
        """Build the abbreviation-to-type mapping."""
        # Standard US abbreviations
        standard: dict[str, StitchType] = {
            "ch": StitchType.CHAIN,
            "sl st": StitchType.SLIP_STITCH,
            "slst": StitchType.SLIP_STITCH,
            "sc": StitchType.SINGLE_CROCHET,
            "hdc": StitchType.HALF_DOUBLE_CROCHET,
            "dc": StitchType.DOUBLE_CROCHET,
            "tr": StitchType.TREBLE_CROCHET,
            "inc": StitchType.INCREASE,
            "2sc": StitchType.INCREASE,  # common amigurumi notation
            "dec": StitchType.DECREASE,
            "sc2tog": StitchType.DECREASE,
            "mr": StitchType.MAGIC_RING,
            "magic ring": StitchType.MAGIC_RING,
            "magic circle": StitchType.MAGIC_RING,
            "sk": StitchType.SKIP,
            "skip": StitchType.SKIP,
            "flo": StitchType.FRONT_LOOP_ONLY,
            "blo": StitchType.BACK_LOOP_ONLY,
            "fp": StitchType.FRONT_POST,
            "bp": StitchType.BACK_POST,
            "fod": StitchType.FASTEN_OFF,
            "fasten off": StitchType.FASTEN_OFF,
        }
        self._map = {k.lower(): v for k, v in standard.items()}

    def lookup(self, abbreviation: str) -> Optional[StitchType]:
        """Look up a stitch type from its abbreviation."""
        return self._map.get(abbreviation.lower().strip())

    def add_alias(self, alias: str, stitch_type: StitchType) -> None:
        """Add a custom alias mapping."""
        self._map[alias.lower().strip()] = stitch_type

    def get_all_abbreviations(self) -> dict[str, StitchType]:
        """Return the full abbreviation map."""
        return dict(self._map)


# Global instance
ABBREVIATION_MAP = StitchAbbreviationMap()
