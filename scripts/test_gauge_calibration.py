#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.enterprise import (
    GaugeCalibrator,
    GaugeMeasurement,
    gauge_from_counts,
)


target = GaugeMeasurement(
    stitches_per_10cm=18,
    rows_per_10cm=20,
    source="pattern",
    confidence=1.0,
)

measured = gauge_from_counts(
    stitch_count=18,
    row_count=20,
    width_cm=10,
    height_cm=10,
    source="manual-swatch",
)

report = GaugeCalibrator(tolerance_percent=5).calibrate(
    target,
    measured,
)

assert report.within_tolerance is True
assert report.sample_required is False
assert report.stitch_difference_percent == 0
assert report.row_difference_percent == 0

out_of_tolerance = GaugeMeasurement(
    stitches_per_10cm=15,
    rows_per_10cm=17,
    source="measured",
)

risk_report = GaugeCalibrator(tolerance_percent=5).calibrate(
    target,
    out_of_tolerance,
)

assert risk_report.within_tolerance is False
assert risk_report.sample_required is True

print("Gauge calibration: PASS")
print(report.to_dict())
print(risk_report.to_dict())
