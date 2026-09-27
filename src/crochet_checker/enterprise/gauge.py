"""Gauge calibration and dimensional tolerance analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class GaugeMeasurement:
    stitches_per_10cm: float
    rows_per_10cm: float
    source: str = "manual"
    confidence: float = 0.8

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GaugeCalibrationReport:
    target: GaugeMeasurement
    measured: GaugeMeasurement
    stitch_difference_percent: float
    row_difference_percent: float
    width_correction_percent: float
    height_correction_percent: float
    within_tolerance: bool
    sample_required: bool
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class GaugeCalibrator:
    """
    Compare pattern gauge against measured or image-detected gauge.

    A future computer-vision adapter can produce GaugeMeasurement from a
    photograph. This engine remains independent of the image library.
    """

    def __init__(self, tolerance_percent: float = 5.0):
        if tolerance_percent <= 0:
            raise ValueError("tolerance_percent must be positive")

        self.tolerance_percent = tolerance_percent

    def calibrate(
        self,
        target: GaugeMeasurement,
        measured: GaugeMeasurement,
    ) -> GaugeCalibrationReport:
        if target.stitches_per_10cm <= 0:
            raise ValueError("Target stitch gauge must be positive")

        if target.rows_per_10cm <= 0:
            raise ValueError("Target row gauge must be positive")

        if measured.stitches_per_10cm <= 0:
            raise ValueError("Measured stitch gauge must be positive")

        if measured.rows_per_10cm <= 0:
            raise ValueError("Measured row gauge must be positive")

        stitch_difference = (
            measured.stitches_per_10cm
            - target.stitches_per_10cm
        ) / target.stitches_per_10cm * 100

        row_difference = (
            measured.rows_per_10cm
            - target.rows_per_10cm
        ) / target.rows_per_10cm * 100

        # More stitches per 10 cm means smaller stitches and smaller output.
        width_correction = -stitch_difference
        height_correction = -row_difference

        within_tolerance = (
            abs(stitch_difference) <= self.tolerance_percent
            and abs(row_difference) <= self.tolerance_percent
        )

        if within_tolerance:
            recommendation = (
                "Gauge is within tolerance. Continue with calibrated "
                "dimensions."
            )
        elif abs(stitch_difference) > abs(row_difference):
            recommendation = (
                "Adjust hook size or tension to correct stitch gauge."
            )
        else:
            recommendation = (
                "Adjust row tension or hook size to correct row gauge."
            )

        return GaugeCalibrationReport(
            target=target,
            measured=measured,
            stitch_difference_percent=round(stitch_difference, 3),
            row_difference_percent=round(row_difference, 3),
            width_correction_percent=round(width_correction, 3),
            height_correction_percent=round(height_correction, 3),
            within_tolerance=within_tolerance,
            sample_required=not within_tolerance,
            recommendation=recommendation,
        )


def gauge_from_counts(
    stitch_count: int,
    row_count: int,
    width_cm: float,
    height_cm: float,
    source: str = "measured",
) -> GaugeMeasurement:
    """Create a gauge measurement from a physical or image measurement."""

    if stitch_count <= 0 or row_count <= 0:
        raise ValueError("Counts must be positive")

    if width_cm <= 0 or height_cm <= 0:
        raise ValueError("Dimensions must be positive")

    return GaugeMeasurement(
        stitches_per_10cm=stitch_count / width_cm * 10,
        rows_per_10cm=row_count / height_cm * 10,
        source=source,
        confidence=0.85,
    )
