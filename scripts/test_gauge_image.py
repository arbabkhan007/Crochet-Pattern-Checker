#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PIL import Image

from crochet_checker.enterprise import GaugeImageIngestor


image_path = Path("/tmp/test-gauge-swatch.png")
Image.new("RGB", (800, 600), "white").save(image_path)

result = GaugeImageIngestor().calibrate_confirmed_measurement(
    str(image_path),
    stitch_count=18,
    row_count=20,
    width_cm=10,
    height_cm=10,
    confirmed_by_user=True,
    confidence=0.95,
)

assert result.image.width_pixels == 800
assert result.image.height_pixels == 600
assert result.measurement.stitches_per_10cm == 18
assert result.measurement.rows_per_10cm == 20
assert result.confirmed_by_user is True
assert result.automatic_detection is False
assert result.confidence == 0.95

print("Gauge image ingestion: PASS")
print(result.to_dict())
