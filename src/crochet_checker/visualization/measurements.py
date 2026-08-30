"""Measurement calculations for crochet patterns."""
from __future__ import annotations
import math
from typing import Optional
from pydantic import BaseModel, Field, computed_field, computed_field
from ..model.pattern import ConstructionType, Pattern

class StitchDimensions(BaseModel):
    width_mm: float = 6.0
    height_mm: float = 6.0
    @classmethod
    def from_gauge(cls, stitches_per_4in: int, rows_per_4in: int):
        return cls(width_mm=(4*25.4)/stitches_per_4in, height_mm=(4*25.4)/rows_per_4in)
    @classmethod
    def for_worsted(cls): return cls(width_mm=6.0, height_mm=6.0)
    @classmethod
    def for_dk(cls): return cls(width_mm=5.0, height_mm=5.0)

class RoundMeasurement(BaseModel):
    round_number: int
    stitch_count: int
    radius_mm: float = 0.0
    circumference_mm: float = 0.0
    height_mm: float = 0.0

class PatternMeasurements(BaseModel):
    total_rounds: int = 0
    max_stitch_count: int = 0
    max_radius_mm: float = 0.0
    max_circumference_mm: float = 0.0
    total_height_mm: float = 0.0
    round_measurements: list[RoundMeasurement] = Field(default_factory=list)

    @computed_field
    @computed_field
    @property
    def total_height_inches(self) -> float:
        return self.total_height_mm / 25.4
    @computed_field
    @computed_field
    @property
    def max_radius_inches(self) -> float:
        return self.max_radius_mm / 25.4
    @computed_field
    @computed_field
    @property
    def max_circumference_inches(self) -> float:
        return self.max_circumference_mm / 25.4
    @computed_field
    @computed_field
    @property
    def max_diameter_inches(self) -> float:
        return (self.max_radius_mm * 2) / 25.4

class MeasurementEngine:
    def __init__(self, stitch_dims=None):
        self.dims = stitch_dims or StitchDimensions.for_worsted()
    def measure(self, pattern):
        result = PatternMeasurements()
        if pattern.rounds: self._rounds(pattern, result)
        elif pattern.rows: self._rows(pattern, result)
        return result
    def _rounds(self, pattern, result):
        result.total_rounds = len(pattern.rounds)
        cum_h = 0.0
        for r in pattern.rounds:
            sc = r.computed_stitch_count
            if sc == 0:
                prev = result.round_measurements[-1].stitch_count if result.round_measurements else 0
                sc = r.compute_stitch_count_with_context(prev)
            circ = sc * self.dims.width_mm
            radius = circ / (2 * math.pi) if circ > 0 else 0
            cum_h += self.dims.height_mm
            rm = RoundMeasurement(round_number=r.round_number, stitch_count=sc,
                radius_mm=radius, circumference_mm=circ, height_mm=cum_h)
            result.round_measurements.append(rm)
            if sc > result.max_stitch_count: result.max_stitch_count = sc
            if radius > result.max_radius_mm: result.max_radius_mm = radius
            if circ > result.max_circumference_mm: result.max_circumference_mm = circ
        result.total_height_mm = cum_h
    def _rows(self, pattern, result):
        result.total_rounds = len(pattern.rows)
        max_w = max((r.computed_stitch_count for r in pattern.rows), default=1)
        result.max_stitch_count = max_w
        result.max_radius_mm = (max_w * self.dims.width_mm) / 2
        result.max_circumference_mm = max_w * self.dims.width_mm * 2
        result.total_height_mm = len(pattern.rows) * self.dims.height_mm

def measure_pattern(pattern, stitch_dims=None):
    return MeasurementEngine(stitch_dims).measure(pattern)
