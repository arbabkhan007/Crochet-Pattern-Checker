from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class StitchType(str, Enum):
    CHAIN = "chain"
    SLIP_STITCH = "slip_stitch"
    SINGLE_CROCHET = "single_crochet"
    HALF_DOUBLE_CROCHET = "half_double_crochet"
    DOUBLE_CROCHET = "double_crochet"
    TREBLE_CROCHET = "treble_crochet"
    MAGIC_RING = "magic_ring"
    INCREASE = "increase"
    DECREASE = "decrease"
    FRONT_LOOP_ONLY = "front_loop_only"
    BACK_LOOP_ONLY = "back_loop_only"
    SKIP = "skip"
    UNKNOWN = "unknown"

STITCH_CONSUMPTION = {
    StitchType.CHAIN: 0, StitchType.SLIP_STITCH: 1, StitchType.SINGLE_CROCHET: 1,
    StitchType.HALF_DOUBLE_CROCHET: 1, StitchType.DOUBLE_CROCHET: 1,
    StitchType.TREBLE_CROCHET: 1, StitchType.INCREASE: 1, StitchType.DECREASE: 2,
    StitchType.SKIP: 1, StitchType.MAGIC_RING: 0,
}

STITCH_PRODUCTION = {
    StitchType.CHAIN: 0, StitchType.SLIP_STITCH: 1, StitchType.SINGLE_CROCHET: 1,
    StitchType.HALF_DOUBLE_CROCHET: 1, StitchType.DOUBLE_CROCHET: 1,
    StitchType.TREBLE_CROCHET: 1, StitchType.INCREASE: 2, StitchType.DECREASE: 1,
    StitchType.SKIP: 0, StitchType.MAGIC_RING: 0,
}

class StitchAbbreviationMap:
    def __init__(self):
        self._map = {}
        self._build_map()
    def _build_map(self):
        s = {"ch":StitchType.CHAIN,"sl st":StitchType.SLIP_STITCH,"slst":StitchType.SLIP_STITCH,
             "sc":StitchType.SINGLE_CROCHET,"hdc":StitchType.HALF_DOUBLE_CROCHET,
             "dc":StitchType.DOUBLE_CROCHET,"tr":StitchType.TREBLE_CROCHET,
             "inc":StitchType.INCREASE,"2sc":StitchType.INCREASE,"dec":StitchType.DECREASE,
             "sc2tog":StitchType.DECREASE,"mr":StitchType.MAGIC_RING,
             "magic ring":StitchType.MAGIC_RING,"sk":StitchType.SKIP}
        self._map = {k.lower(): v for k, v in s.items()}
    def lookup(self, abbr): return self._map.get(abbr.lower().strip())
    def get_all_abbreviations(self): return dict(self._map)

ABBREVIATION_MAP = StitchAbbreviationMap()
