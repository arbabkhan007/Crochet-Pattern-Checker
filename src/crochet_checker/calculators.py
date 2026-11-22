"""World-class crochet calculators: gauge, size, yarn, hooks, conversion.

Pure functions built on the published Craft Yarn Council standards in
:mod:`crochet_checker.standards.reference`. No pattern parsing, no AI,
no network. Every estimate names its assumptions so it is never
mistaken for a measurement.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from .standards.reference import CROCHET_HOOKS, YARN_WEIGHTS

INCH_TO_CM = 2.54
CM_TO_INCH = 1.0 / INCH_TO_CM

# Average yarn used per stitch, in centimetres of yarn, by stitch type.
# These are working estimates for planning only.
YARN_PER_STITCH_CM: dict[str, float] = {
    "sc": 4.5,
    "hdc": 6.0,
    "dc": 7.5,
    "tr": 9.0,
    "sl st": 2.0,
    "ch": 2.0,
}

# US <-> UK stitch terminology. Order matters: longest tokens first so
# e.g. "sc2tog" is replaced before "sc".
US_TO_UK: dict[str, str] = {
    "sc2tog": "dc2tog",
    "hdc2tog": "htr2tog",
    "dc2tog": "tr2tog",
    "hdc": "htr",
    "sc": "dc",
    "dc": "tr",
    "tr": "dtr",
    "dtr": "trtr",
    "sl st": "ss",
}
UK_TO_US: dict[str, str] = {
    "dc2tog": "sc2tog",
    "htr2tog": "hdc2tog",
    "tr2tog": "dc2tog",
    "htr": "hdc",
    "dc": "sc",
    "tr": "dc",
    "dtr": "tr",
    "trtr": "dtr",
    "ss": "sl st",
}


@dataclass(frozen=True)
class GaugeResult:
    """Finished size from a gauge swatch. Estimates, not measurements."""

    width_in: float
    height_in: float
    width_cm: float
    height_cm: float
    stitches: int
    rows: int
    sts_per_4in: float
    rows_per_4in: float
    note: str = (
        "Estimate from your swatch. Block the swatch, measure the middle "
        "4 inches, and re-check before starting the project."
    )


@dataclass(frozen=True)
class YarnEstimate:
    """Rough yardage estimate. Not weighed, not a finished size."""

    total_stitches: int
    stitch: str
    yards: float
    metres: float
    balls_100g: float
    note: str = (
        "Rough planning estimate only. Buy extra yarn for colour changes, "
        "weaving in ends, and gauge differences."
    )


@dataclass(frozen=True)
class HookRecommendation:
    """Hook range for a yarn weight, from the published standard."""

    weight_number: int
    weight_name: str
    hook_mm_low: float | None
    hook_mm_high: float | None
    hook_us: str
    gauge_sts_per_4in: tuple[int, int] | None
    source: str = "Source: Craft Yarn Council's www.YarnStandards.com"


def gauge_to_size(
    stitches: int,
    rows: int,
    sts_per_4in: float,
    rows_per_4in: float,
) -> GaugeResult:
    """Compute finished width/height from stitch counts and gauge.

    >>> r = gauge_to_size(40, 40, 20, 20)
    >>> round(r.width_in, 2)
    8.0
    """
    if stitches <= 0 or rows <= 0:
        raise ValueError("stitches and rows must be positive")
    if sts_per_4in <= 0 or rows_per_4in <= 0:
        raise ValueError("gauge must be positive (stitches/rows per 4 inches)")
    width_in = stitches / sts_per_4in * 4
    height_in = rows / rows_per_4in * 4
    return GaugeResult(
        width_in=round(width_in, 2),
        height_in=round(height_in, 2),
        width_cm=round(width_in * INCH_TO_CM, 1),
        height_cm=round(height_in * INCH_TO_CM, 1),
        stitches=stitches,
        rows=rows,
        sts_per_4in=sts_per_4in,
        rows_per_4in=rows_per_4in,
    )


def stitches_for_size(
    target_in: float, sts_per_4in: float, *, round_to: int = 1
) -> int:
    """Stitches needed for a target width at the given gauge."""
    if target_in <= 0 or sts_per_4in <= 0:
        raise ValueError("target size and gauge must be positive")
    if round_to <= 0:
        raise ValueError("round_to must be positive")
    raw = target_in / 4 * sts_per_4in
    if round_to > 1:
        return int(round(raw / round_to) * round_to)
    return int(round(raw))


def estimate_yarn(
    total_stitches: int,
    stitch: str = "sc",
    *,
    yards_per_100g: float = 210.0,
) -> YarnEstimate:
    """Rough yardage for a stitch count. Planning estimate only."""
    if total_stitches < 0:
        raise ValueError("total_stitches cannot be negative")
    key = stitch.strip().lower()
    if key not in YARN_PER_STITCH_CM:
        raise ValueError(f"Unsupported stitch {stitch!r}. Choose one of {', '.join(YARN_PER_STITCH_CM)}.")
    if yards_per_100g <= 0:
        raise ValueError("yards_per_100g must be positive")
    per_stitch_cm = YARN_PER_STITCH_CM[key]
    total_cm = total_stitches * per_stitch_cm
    metres = total_cm / 100.0
    yards = metres * 1.09361
    balls = yards / yards_per_100g if yards_per_100g > 0 else 0.0
    return YarnEstimate(
        total_stitches=total_stitches,
        stitch=key,
        yards=round(yards, 1),
        metres=round(metres, 1),
        balls_100g=round(balls, 2),
    )


def recommend_hook(weight: int | str) -> HookRecommendation:
    """Hook range for a yarn weight number (0-7) or name."""
    entry = None
    if isinstance(weight, int):
        entry = next((w for w in YARN_WEIGHTS if w["number"] == weight), None)
    else:
        w = str(weight).strip().lower()
        if w.isdigit():
            entry = next((x for x in YARN_WEIGHTS if x["number"] == int(w)), None)
        else:
            entry = next(
                (
                    x
                    for x in YARN_WEIGHTS
                    if w in x["name"].lower()
                    or any(w == t.lower() for t in x["types"])
                ),
                None,
            )
    if entry is None:
        raise ValueError(f"Unknown yarn weight: {weight!r}. Use 0-7 or a name like 'worsted'.")
    hook_mm = entry.get("hook_mm")
    low = hook_mm[0] if hook_mm else None
    high = hook_mm[1] if hook_mm else None
    gauge = entry.get("crochet_gauge")
    return HookRecommendation(
        weight_number=entry["number"],
        weight_name=entry["name"],
        hook_mm_low=low,
        hook_mm_high=high,
        hook_us=entry.get("hook_us", ""),
        gauge_sts_per_4in=gauge,
    )


def nearest_hook(mm: float) -> tuple[float, str | None]:
    """Nearest standard hook size in millimetres and its US label."""
    if mm <= 0:
        raise ValueError("hook size must be positive")
    return min(CROCHET_HOOKS, key=lambda h: abs(h[0] - mm))


def wpi_to_weight(wpi: float) -> int:
    """Wraps-per-inch to yarn weight number (Craft Yarn Council ranges)."""
    if wpi <= 0:
        raise ValueError("wpi must be positive")
    # Midpoint-based mapping from the published WPI ranges.
    ranges = [
        (30, 0),
        (14, 1),
        (12, 2),
        (11, 3),
        (9, 4),
        (6, 5),
        (5, 6),
        (0, 7),
    ]
    for threshold, number in ranges:
        if wpi >= threshold:
            return number
    return 7


def convert_terminology(text: str, direction: str = "us-to-uk") -> str:
    """Convert stitch abbreviations between US and UK terminology.

    Word-boundary aware: "sc" inside "scale" is left alone.
    """
    direction = direction.strip().lower().replace("_", "-")
    if direction in ("us-to-uk", "us", "to-uk"):
        mapping = US_TO_UK
    elif direction in ("uk-to-us", "uk", "to-us"):
        mapping = UK_TO_US
    else:
        raise ValueError("direction must be 'us-to-uk' or 'uk-to-us'")
    # Single pass: each token is replaced exactly once, so "sc" -> "dc"
    # is not then cascaded into "tr" -> "dtr".
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(k) for k in sorted(mapping, key=len, reverse=True)) + r")\b"
    )
    return pattern.sub(lambda m: mapping[m.group(1)], text)


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a length between in/cm/mm/yd/m."""
    # Inches per unit.
    factors = {"in": 1.0, "cm": CM_TO_INCH, "mm": CM_TO_INCH / 10, "yd": 36.0, "m": 39.3701}
    f = from_unit.strip().lower()
    t = to_unit.strip().lower()
    if f not in factors or t not in factors:
        raise ValueError(f"Units must be one of {sorted(factors)}")
    return round(value * factors[f] / factors[t], 3)


def stitch_count_chart(counts: list[int]) -> list[dict]:
    """Bar-chart data for a per-round stitch-count ladder."""
    if not counts:
        return []
    peak = max(counts) or 1
    return [
        {
            "round": i + 1,
            "stitches": c,
            "pct_of_max": round(c / peak * 100, 1),
        }
        for i, c in enumerate(counts)
    ]


def shape_from_counts(counts: list[int]) -> str:
    """Name the silhouette from a stitch-count ladder (written counts only)."""
    if not counts:
        return "unknown"
    if len(counts) == 1:
        return "single round"
    peak = max(counts)
    first, last = counts[0], counts[-1]
    if all(c == first for c in counts):
        return "tube"
    if last < first and peak == first:
        return "cone"
    if last > first and peak == last:
        return "bowl"
    if peak in (first, last):
        return "taper"
    return "sphere" if math.isclose(first, last, rel_tol=0.2) else "organic"


__all__ = [
    "GaugeResult",
    "YarnEstimate",
    "HookRecommendation",
    "gauge_to_size",
    "stitches_for_size",
    "estimate_yarn",
    "recommend_hook",
    "nearest_hook",
    "wpi_to_weight",
    "convert_terminology",
    "convert_length",
    "stitch_count_chart",
    "shape_from_counts",
]
