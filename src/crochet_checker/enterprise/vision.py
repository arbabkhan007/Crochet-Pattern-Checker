"""Safe gauge-swatch image ingestion and calibration."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .gauge import GaugeMeasurement, gauge_from_counts


@dataclass
class ImageMetadata:
    path: str
    sha256: str
    width_pixels: int
    height_pixels: int
    format: str
    file_size_bytes: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GaugeImageResult:
    image: ImageMetadata
    measurement: GaugeMeasurement
    confirmed_by_user: bool
    automatic_detection: bool
    confidence: float
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["image"] = self.image.to_dict()
        result["measurement"] = self.measurement.to_dict()
        return result


class GaugeImageIngestor:
    """
    Ingest a gauge image and convert confirmed measurements into gauge data.

    Stitch and row counts must be confirmed by a user or a separately
    validated computer-vision detector. This module never invents counts.
    """

    ALLOWED_FORMATS = {"PNG", "JPEG", "JPG", "WEBP"}

    def inspect_image(self, image_path: str) -> ImageMetadata:
        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")

        if not path.is_file():
            raise ValueError(f"Not a file: {path}")

        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError(
                "Pillow is required for gauge image ingestion."
            ) from exc

        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()

        with Image.open(path) as image:
            image_format = (image.format or "").upper()
            width, height = image.size

        if image_format not in self.ALLOWED_FORMATS:
            raise ValueError(
                f"Unsupported image format: {image_format}. "
                f"Use: {', '.join(sorted(self.ALLOWED_FORMATS))}"
            )

        if width < 100 or height < 100:
            raise ValueError(
                "Image is too small for reliable gauge inspection."
            )

        return ImageMetadata(
            path=str(path),
            sha256=digest,
            width_pixels=width,
            height_pixels=height,
            format=image_format,
            file_size_bytes=len(raw),
        )

    def calibrate_confirmed_measurement(
        self,
        image_path: str,
        *,
        stitch_count: int,
        row_count: int,
        width_cm: float,
        height_cm: float,
        confirmed_by_user: bool = True,
        confidence: float = 0.90,
    ) -> GaugeImageResult:
        if not confirmed_by_user:
            raise ValueError(
                "Gauge counts must be user-confirmed or supplied by a "
                "validated detector."
            )

        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

        metadata = self.inspect_image(image_path)

        measurement = gauge_from_counts(
            stitch_count=stitch_count,
            row_count=row_count,
            width_cm=width_cm,
            height_cm=height_cm,
            source="confirmed-gauge-image",
        )

        recommendation = (
            "Gauge image accepted. Use this calibration in certification."
            if confidence >= 0.90
            else
            "Low-confidence image measurement. A physical swatch review "
            "is recommended."
        )

        return GaugeImageResult(
            image=metadata,
            measurement=measurement,
            confirmed_by_user=confirmed_by_user,
            automatic_detection=False,
            confidence=confidence,
            recommendation=recommendation,
        )
