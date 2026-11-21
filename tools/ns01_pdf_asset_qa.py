"""Resolution preflight for the two current NS 01 PDF illustrations.

This tool can measure pixels and effective placed DPI. It cannot decide whether
an image truly shows the written yarn colours, a correctly engraved hook, or a
physically verified sample; those remain explicit human review items.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

try:  # Support both ``python -m tools.ns01_pdf_asset_qa`` and direct script use.
    from .ns01_pdf_model import (
        COVER_IMAGE_BOX_MM,
        HERO_ASSET,
        MATERIALS_ASSET,
        MATERIALS_IMAGE_BOX_MM,
        MIN_PRINT_DPI,
        ROOT,
    )
except ImportError:  # pragma: no cover - exercised by direct CLI invocation.
    from ns01_pdf_model import (
        COVER_IMAGE_BOX_MM,
        HERO_ASSET,
        MATERIALS_ASSET,
        MATERIALS_IMAGE_BOX_MM,
        MIN_PRINT_DPI,
        ROOT,
    )

CHECKLIST = ROOT / "docs/ns01_pdf_photo_qa.md"


@dataclass(frozen=True)
class AssetResult:
    name: str
    path: Path
    pixel_width: int
    pixel_height: int
    placed_width_mm: float
    placed_height_mm: float
    dpi_x: float
    dpi_y: float
    is_concept_named: bool

    @property
    def meets_resolution_target(self) -> bool:
        return min(self.dpi_x, self.dpi_y) >= MIN_PRINT_DPI


def inspect_asset(
    name: str, path: Path, target_box_mm: tuple[float, float]
) -> AssetResult:
    if not path.is_file():
        raise FileNotFoundError(f"Missing NS01 PDF image asset: {path}")
    with Image.open(path) as image:
        pixel_width, pixel_height = image.size
        image.verify()
    if pixel_width <= 0 or pixel_height <= 0:
        raise ValueError(f"Invalid image dimensions for {path}")

    target_width_mm, target_height_mm = target_box_mm
    scale = min(target_width_mm / pixel_width, target_height_mm / pixel_height)
    placed_width_mm = pixel_width * scale
    placed_height_mm = pixel_height * scale
    dpi_x = pixel_width / (placed_width_mm / 25.4)
    dpi_y = pixel_height / (placed_height_mm / 25.4)
    return AssetResult(
        name=name,
        path=path,
        pixel_width=pixel_width,
        pixel_height=pixel_height,
        placed_width_mm=placed_width_mm,
        placed_height_mm=placed_height_mm,
        dpi_x=dpi_x,
        dpi_y=dpi_y,
        is_concept_named="concept" in path.stem.lower(),
    )


def unchecked_human_items(path: Path = CHECKLIST) -> list[str]:
    if not path.is_file():
        return ["Human-review checklist file is missing"]
    pending: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ] "):
            pending.append(stripped[6:])
    return pending


def audit_assets() -> tuple[list[AssetResult], list[str]]:
    results = [
        inspect_asset("Cover illustration", HERO_ASSET, COVER_IMAGE_BOX_MM),
        inspect_asset(
            "Materials illustration", MATERIALS_ASSET, MATERIALS_IMAGE_BOX_MM
        ),
    ]
    pending = unchecked_human_items()
    return results, pending


def format_report(results: list[AssetResult], pending: list[str]) -> str:
    lines = ["NS 01 PDF image preflight", ""]
    for result in results:
        status = "PASS" if result.meets_resolution_target else "BELOW 300 DPI"
        lines.append(
            f"{result.name}: {result.pixel_width}x{result.pixel_height}px; "
            f"placed {result.placed_width_mm:.1f}x{result.placed_height_mm:.1f}mm; "
            f"{result.dpi_x:.0f}x{result.dpi_y:.0f} effective DPI — {status}"
        )
        if result.is_concept_named:
            lines.append(
                "  Note: filename identifies this asset as concept artwork, not a photograph of a verified sample."
            )
    if pending:
        lines.extend(["", "Human review pending:"])
        lines.extend(f"- {item}" for item in pending)
    else:
        lines.extend(["", "Human-review checklist: all items are marked complete."])

    ready = (
        all(
            result.meets_resolution_target and not result.is_concept_named
            for result in results
        )
        and not pending
    )
    lines.extend(["", f"Photo-asset release status: {'READY' if ready else 'HOLD'}"])
    if not ready:
        lines.append(
            "The PDF can still be generated for layout review; HOLD is not a physical or product-quality verdict."
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return nonzero unless every image meets 300 effective DPI and human review is complete",
    )
    args = parser.parse_args()
    try:
        results, pending = audit_assets()
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"NS 01 image preflight: FAIL — {exc}", file=sys.stderr)
        return 2

    report = format_report(results, pending)
    print(report)
    ready = (
        all(
            result.meets_resolution_target and not result.is_concept_named
            for result in results
        )
        and not pending
    )
    return 0 if ready or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
