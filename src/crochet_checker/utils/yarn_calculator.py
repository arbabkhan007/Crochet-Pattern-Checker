"""Yarn Calculator - Estimate yarn requirements."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from ..visualization.measurements import measure_pattern

STITCH_YARN_USAGE = {"chain": 0.5, "slip_stitch": 0.3, "single_crochet": 1.2, "half_double_crochet": 1.5, "double_crochet": 2.0, "treble_crochet": 2.5, "increase": 2.4, "decrease": 1.8, "magic_ring": 4.0}
WEIGHT_MULTIPLIERS = {"lace": 0.4, "fingering": 0.6, "sport": 0.8, "dk": 0.9, "worsted": 1.0, "aran": 1.1, "bulky": 1.3, "super_bulky": 1.6, "jumbo": 2.0}

class YarnEstimate(BaseModel):
    total_inches: float = 0
    total_yards: float = 0
    total_meters: float = 0
    total_grams: Optional[float] = None
    skeins_needed: Optional[float] = None
    confidence: str = "medium"
    notes: list[str] = Field(default_factory=list)
    breakdown: list[dict] = Field(default_factory=list)

class YarnCalculator:
    def __init__(self, yarn_weight="worsted", grams_per_skein=100, yards_per_skein=200):
        self.yarn_weight = yarn_weight
        self.grams_per_skein = grams_per_skein
        self.yards_per_skein = yards_per_skein
        self.weight_multiplier = WEIGHT_MULTIPLIERS.get(yarn_weight, 1.0)
    
    def estimate(self, pattern):
        measurements = measure_pattern(pattern)
        rounds = pattern.rounds or []
        if not rounds:
            return YarnEstimate(confidence="low", notes=["No rounds found"])
        
        total_inches = sum(self._round_yarn(r) for r in rounds) * self.weight_multiplier
        total_yards = total_inches / 36
        total_meters = total_inches * 0.0254
        total_grams = total_yards * (self.grams_per_skein / self.yards_per_skein)
        skeins = (total_yards / self.yards_per_skein) * 1.15
        
        notes = [f"Based on {self.yarn_weight} weight yarn"]
        if pattern.hook: notes.append(f"Hook size: {pattern.hook.size_mm}mm")
        if measurements.max_diameter_inches > 0: notes.append(f"Finished size: ~{measurements.max_diameter_inches:.1f} diameter")
        
        return YarnEstimate(total_inches=round(total_inches, 1), total_yards=round(total_yards, 1), total_meters=round(total_meters, 2),
                           total_grams=round(total_grams, 1), skeins_needed=round(skeins, 2), confidence="high" if pattern.hook and pattern.yarn else "medium",
                           notes=notes)
    
    def _round_yarn(self, round_obj):
        return sum(STITCH_YARN_USAGE.get(op.stitch_type.value, 1.5) * op.count for inst in round_obj.instructions for op in inst.operations)

def estimate_yarn(pattern, yarn_weight="worsted", grams_per_skein=100, yards_per_skein=200):
    return YarnCalculator(yarn_weight, grams_per_skein, yards_per_skein).estimate(pattern)
