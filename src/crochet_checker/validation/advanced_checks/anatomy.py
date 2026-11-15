"""Conservative bottom-up/top-down anatomical round normalization."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from .common import AdvancedFinding, ROUND_HEADER, split_sections
from .spatial import attachment_bounds_from_text

TorsoDirection = Literal["BOTTOM_UP", "TOP_DOWN"]


@dataclass(frozen=True)
class TorsoAxis:
    direction: TorsoDirection
    max_round: int
    section_name: str


def normalized_anatomical_height(
    round_number: int, max_round: int, direction: TorsoDirection
) -> float | None:
    """Map an explicit round into [0, 1] only when the axis is known."""
    if (
        direction not in {"BOTTOM_UP", "TOP_DOWN"}
        or max_round <= 1
        or round_number < 1
        or round_number > max_round
    ):
        return None
    fraction = (round_number - 1) / (max_round - 1)
    return fraction if direction == "BOTTOM_UP" else 1.0 - fraction


def detect_torso_axes(text: str) -> list[TorsoAxis]:
    axes: list[TorsoAxis] = []
    for heading, body, _line in split_sections(text):
        section = f"{heading}\n{body}"
        if not re.search(r"\b(?:torso|body)\b", heading, re.IGNORECASE):
            continue
        bottom = bool(
            re.search(
                r"\b(?:worked|crocheted)\s+bottom[- ]up\b|\bfrom\s+(?:the\s+)?(?:base|belly|pelvis)\s+to\s+(?:the\s+)?(?:neck|head)\b",
                section,
                re.IGNORECASE,
            )
        )
        top = bool(
            re.search(
                r"\b(?:worked|crocheted)\s+top[- ]down\b|\bfrom\s+(?:the\s+)?(?:neck|head)\s+to\s+(?:the\s+)?(?:base|belly|pelvis)\b",
                section,
                re.IGNORECASE,
            )
        )
        if bottom == top:
            continue
        numbers = [
            int(match.group(1))
            for line in body.splitlines()
            if (match := ROUND_HEADER.match(line.strip()))
        ]
        if not numbers:
            continue
        axes.append(
            TorsoAxis("BOTTOM_UP" if bottom else "TOP_DOWN", max(numbers), heading)
        )
    return axes


_UPPER = {
    "wings",
    "wing",
    "arms",
    "arm",
    "shoulders",
    "shoulder",
    "neck ruff",
    "forelegs",
    "foreleg",
    "fore legs",
    "fore leg",
}
_LOWER = {
    "tail",
    "tails",
    "hind legs",
    "hind leg",
    "hindlegs",
    "hindleg",
    "pelvis",
}


def check_anatomical_attachment(
    feature: str,
    round_min: int,
    round_max: int,
    max_round: int,
    direction: TorsoDirection,
) -> list[AdvancedFinding]:
    """Flag only placements beyond the explicit high-confidence inversion thresholds."""
    name = feature.casefold().strip()
    lower = name in _LOWER
    upper = name in _UPPER
    if not (lower or upper) or round_min < 1 or round_max < round_min:
        return []
    heights = [
        normalized_anatomical_height(round_min, max_round, direction),
        normalized_anatomical_height(round_max, max_round, direction),
    ]
    if any(value is None for value in heights):
        return []
    low_z, high_z = min(heights), max(heights)
    if upper and high_z < 0.40:
        return [
            AdvancedFinding(
                "AnatomicalZAxisInversion",
                f"{feature.title()} is assigned to rounds {round_min}–{round_max}, below the stated upper-body zone on a {direction.lower().replace('_', '-')} torso (z={high_z:.0%} at the highest round).",
                "warning",
            )
        ]
    if lower and low_z > 0.60:
        return [
            AdvancedFinding(
                "AnatomicalZAxisInversion",
                f"{feature.title()} is assigned to rounds {round_min}–{round_max}, above the stated lower-body zone on a {direction.lower().replace('_', '-')} torso (z={low_z:.0%} at the lowest round).",
                "warning",
            )
        ]
    return []


def anatomy_findings(text: str) -> list[AdvancedFinding]:
    axes = detect_torso_axes(text)
    if not axes:
        return []
    placements = attachment_bounds_from_text(text)
    findings: list[AdvancedFinding] = []
    for placement in placements:
        if placement.parent is None or placement.parent.casefold() not in {
            "body",
            "torso",
        }:
            continue
        if placement.round_min is None or placement.round_max is None:
            continue
        matching_axes = [
            axis
            for axis in axes
            if re.search(
                rf"\b{re.escape(placement.parent)}\b", axis.section_name, re.IGNORECASE
            )
        ]
        if not matching_axes and len(axes) == 1:
            matching_axes = axes
        if len(matching_axes) != 1:
            continue
        axis = matching_axes[0]
        for finding in check_anatomical_attachment(
            placement.feature,
            placement.round_min,
            placement.round_max,
            axis.max_round,
            axis.direction,
        ):
            findings.append(
                AdvancedFinding(
                    finding.code,
                    finding.message,
                    finding.severity,
                    placement.line_number,
                )
            )
    return findings
