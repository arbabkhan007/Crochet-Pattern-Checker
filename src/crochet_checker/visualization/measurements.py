"""
Measurement calculations for crochet patterns.

Computes physical dimensions from pattern data:
- Stitch counts per round
- Estimated radius and circumference
- Estimated height
- Finished object dimensions
"""

from __future__ import annotations

import math

from pydantic import BaseModel, Field

from ..model.pattern import Pattern


class StitchDimensions(BaseModel):
    """Physical dimensions of a single stitch."""

    width_mm: float = Field(default=6.0, description="Width of one stitch in mm")
    height_mm: float = Field(default=6.0, description="Height of one row in mm")

    @classmethod
    def from_gauge(cls, stitches_per_4in: int, rows_per_4in: int) -> StitchDimensions:
        """Create from gauge swatch measurements."""
        width = (4 * 25.4) / stitches_per_4in  # 4 inches to mm
        height = (4 * 25.4) / rows_per_4in
        return cls(width_mm=width, height_mm=height)

    @classmethod
    def for_worsted(cls) -> StitchDimensions:
        """Typical dimensions for worsted weight yarn with 5mm hook."""
        return cls(width_mm=6.0, height_mm=6.0)

    @classmethod
    def for_dk(cls) -> StitchDimensions:
        """Typical dimensions for DK weight yarn with 4mm hook."""
        return cls(width_mm=5.0, height_mm=5.0)

    @classmethod
    def for_sport(cls) -> StitchDimensions:
        """Typical dimensions for sport weight yarn with 3.5mm hook."""
        return cls(width_mm=4.5, height_mm=4.5)


class RoundMeasurement(BaseModel):
    """Measurements for a single round."""

    round_number: int
    stitch_count: int
    radius_mm: float = 0.0
    circumference_mm: float = 0.0
    height_mm: float = 0.0


class PatternMeasurements(BaseModel):
    """Complete measurements for a pattern."""

    total_rounds: int = 0
    max_stitch_count: int = 0
    max_radius_mm: float = 0.0
    max_circumference_mm: float = 0.0
    total_height_mm: float = 0.0
    total_height_inches: float = 0.0
    max_diameter_inches: float = 0.0
    round_measurements: list[RoundMeasurement] = Field(default_factory=list)

    @property
    def max_radius_inches(self) -> float:
        return self.max_radius_mm / 25.4

    @property
    def max_circumference_inches(self) -> float:
        return self.max_circumference_mm / 25.4


class MeasurementEngine:
    """
    Calculates physical measurements from a crochet pattern.

    Uses stitch dimensions (from gauge or defaults) to estimate
    the physical size of the finished object.
    """

    def __init__(self, stitch_dims: StitchDimensions | None = None) -> None:
        self.dims = stitch_dims or StitchDimensions.for_worsted()

    def measure(self, pattern: Pattern) -> PatternMeasurements:
        """Calculate all measurements for a pattern."""
        result = PatternMeasurements()

        if pattern.rounds:
            self._measure_rounds(pattern, result)
        elif pattern.rows:
            self._measure_rows(pattern, result)

        result.total_height_inches = result.total_height_mm / 25.4
        result.max_diameter_inches = (result.max_radius_mm * 2) / 25.4

        return result

    def _measure_rounds(self, pattern: Pattern, result: PatternMeasurements) -> None:
        """Measure a pattern worked in rounds."""
        result.total_rounds = len(pattern.rounds)

        # For circular/flat work, estimate radius from stitch counts
        # Using the formula: circumference = stitch_count * stitch_width
        # And: radius = circumference / (2 * pi)

        cumulative_height = 0.0

        for r in pattern.rounds:
            sc = r.computed_stitch_count
            if sc == 0:
                # Try context-aware
                prev_count = 0
                if result.round_measurements:
                    prev_count = result.round_measurements[-1].stitch_count
                sc = r.compute_stitch_count_with_context(prev_count)

            circumference = sc * self.dims.width_mm
            radius = circumference / (2 * math.pi) if circumference > 0 else 0

            cumulative_height += self.dims.height_mm

            rm = RoundMeasurement(
                round_number=r.round_number,
                stitch_count=sc,
                radius_mm=radius,
                circumference_mm=circumference,
                height_mm=cumulative_height,
            )
            result.round_measurements.append(rm)

            result.max_stitch_count = max(result.max_stitch_count, sc)
            result.max_radius_mm = max(result.max_radius_mm, radius)
            result.max_circumference_mm = max(
                result.max_circumference_mm, circumference
            )

        result.total_height_mm = cumulative_height

    def _measure_rows(self, pattern: Pattern, result: PatternMeasurements) -> None:
        """Measure a pattern worked in rows (flat)."""
        result.total_rounds = len(pattern.rows)

        max_width_stitches = 0
        for r in pattern.rows:
            sc = r.computed_stitch_count
            max_width_stitches = max(max_width_stitches, sc)

        width_mm = max_width_stitches * self.dims.width_mm
        height_mm = len(pattern.rows) * self.dims.height_mm

        result.max_stitch_count = max_width_stitches
        result.max_radius_mm = width_mm / 2  # Half width as "radius"
        result.max_circumference_mm = width_mm * 2
        result.total_height_mm = height_mm

        for r in pattern.rows:
            sc = r.computed_stitch_count
            rm = RoundMeasurement(
                round_number=r.row_number,
                stitch_count=sc,
                radius_mm=(sc * self.dims.width_mm) / 2,
                circumference_mm=sc * self.dims.width_mm,
                height_mm=r.row_number * self.dims.height_mm,
            )
            result.round_measurements.append(rm)


def measure_pattern(
    pattern: Pattern, stitch_dims: StitchDimensions | None = None
) -> PatternMeasurements:
    """Convenience function to measure a pattern."""
    engine = MeasurementEngine(stitch_dims)
    return engine.measure(pattern)
