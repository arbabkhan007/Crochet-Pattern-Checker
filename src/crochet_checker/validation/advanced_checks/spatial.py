"""Explicit 2D attachment boxes, stitch-to-angle mapping, and spiral warnings."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Mapping

from .common import AdvancedFinding, ROUND_HEADER, STATED_COUNT, split_sections

_FEATURE = re.compile(
    r"\b(snout\s+bridge|safety\s+eyes?|eyes?|muzzle|ears?|horns?|tails?|"
    r"fore\s+legs?|forelegs?|hind\s*legs?|arms?|legs?|wings?|shoulders?|neck\s+ruff|pelvis|limbs?)\b",
    re.IGNORECASE,
)
_PARENT = re.compile(
    r"\b(?:to|on|onto|in|into)\s+(?:the\s+)?(head|torso|body|face|chest|back)\b",
    re.IGNORECASE,
)
_ROUND_RANGE = re.compile(
    r"\b(?:rounds?|rnds?|r)\s*(\d+)\s*(?:[-–—]|to|through|and)\s*(?:r\s*)?(\d+)\b",
    re.IGNORECASE,
)
_ROUND_SINGLE = re.compile(r"\b(?:round|rnd|r)\s*(\d+)\b", re.IGNORECASE)
_STITCH_RANGE = re.compile(
    r"\b(?:stitch(?:es)?|sts?|stitch\s+indices)\s*(\d+)\s*(?:[-–—]|to|through|and|&)\s*(\d+)\b",
    re.IGNORECASE,
)
_STITCH_SINGLE = re.compile(r"\b(?:stitch(?:es)?|sts?)\s*(\d+)\b", re.IGNORECASE)
_ANGLE_RANGE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(?:°|degrees?)\s*(?:[-–—]|to|through|and)\s*"
    r"(\d+(?:\.\d+)?)\s*(?:°|degrees?)\b",
    re.IGNORECASE,
)
_ANGLE_SINGLE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:°|degrees?)\b", re.IGNORECASE)
_PLACEMENT = re.compile(
    r"\b(?:attach|sew|place|position|insert|mount|join|graft|embroider)\w*\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class FeatureBounds:
    feature: str
    parent: str | None
    round_min: int | None
    round_max: int | None
    horizontal_min: float | None
    horizontal_max: float | None
    horizontal_unit: str | None
    source: str
    line_number: int = 0


def stitch_to_angle(stitch_index: int, stitch_count: int) -> float:
    """Map a one-based stitch index to a clockwise-positive polar angle."""
    if stitch_count <= 0 or stitch_index < 1 or stitch_index > stitch_count:
        raise ValueError("Stitch index must be within a positive round stitch count.")
    return ((stitch_index - 0.5) / stitch_count) * 360.0


def boxes_overlap(a: FeatureBounds, b: FeatureBounds) -> bool:
    """Return True only for complete, comparable boxes on the same parent."""
    values = (
        a.round_min,
        a.round_max,
        b.round_min,
        b.round_max,
        a.horizontal_min,
        a.horizontal_max,
        b.horizontal_min,
        b.horizontal_max,
    )
    if any(value is None for value in values):
        return False
    if not a.parent or not b.parent or a.parent.casefold() != b.parent.casefold():
        return False
    if (
        not a.horizontal_unit
        or not b.horizontal_unit
        or a.horizontal_unit.casefold() != b.horizontal_unit.casefold()
    ):
        return False
    round_overlap = max(a.round_min, b.round_min) <= min(a.round_max, b.round_max)
    horizontal_overlap = max(a.horizontal_min, b.horizontal_min) <= min(
        a.horizontal_max, b.horizontal_max
    )
    return round_overlap and horizontal_overlap


def find_spatial_collisions(features: list[FeatureBounds]) -> list[AdvancedFinding]:
    findings: list[AdvancedFinding] = []
    for index, first in enumerate(features):
        for second in features[index + 1 :]:
            if first.feature.casefold() == second.feature.casefold():
                continue
            if boxes_overlap(first, second):
                unit = first.horizontal_unit or "coordinate"
                findings.append(
                    AdvancedFinding(
                        "SpatialBoundingBoxCollision",
                        f"{first.feature} and {second.feature} have overlapping explicit placement boxes on {first.parent} (rounds {first.round_min}–{first.round_max}, {unit} {first.horizontal_min:g}–{first.horizontal_max:g}). Verify the intended layout.",
                        "warning",
                        second.line_number,
                    )
                )
    return findings


def attachment_bounds_from_text(text: str) -> list[FeatureBounds]:
    """Extract only explicit round and stitch/angle intervals from placement lines."""
    found: list[FeatureBounds] = []
    for line_number, raw in enumerate(text.splitlines(), start=1):
        if not _PLACEMENT.search(raw):
            continue
        features = list(_FEATURE.finditer(raw))
        if not features:
            continue
        parent_match = _PARENT.search(raw)
        parent = parent_match.group(1) if parent_match else None
        round_range = _ROUND_RANGE.search(raw)
        if round_range:
            first_round, last_round = (
                int(round_range.group(1)),
                int(round_range.group(2)),
            )
            if first_round <= last_round:
                r0, r1 = first_round, last_round
            else:
                r0 = r1 = None
        else:
            round_single = _ROUND_SINGLE.search(raw)
            r0 = r1 = int(round_single.group(1)) if round_single else None
        stitch_range = _STITCH_RANGE.search(raw)
        if stitch_range:
            first_stitch, last_stitch = (
                float(stitch_range.group(1)),
                float(stitch_range.group(2)),
            )
            if first_stitch <= last_stitch:
                h0, h1 = first_stitch, last_stitch
                unit = "stitch"
            else:
                h0 = h1 = None
                unit = None
        else:
            angle_range = _ANGLE_RANGE.search(raw)
            if angle_range:
                first, second = float(angle_range.group(1)), float(angle_range.group(2))
                if first > second:
                    h0 = h1 = None
                    unit = None
                elif re.search(
                    r"\b(?:counterclockwise|counter-clockwise|anticlockwise|anti-clockwise)\b",
                    raw,
                    re.IGNORECASE,
                ):
                    h0, h1 = 360.0 - second, 360.0 - first
                    unit = "degree"
                else:
                    h0, h1 = first, second
                    unit = "degree"
            else:
                stitch_single = _STITCH_SINGLE.search(raw)
                angle_single = _ANGLE_SINGLE.search(raw)
                if stitch_single:
                    h0 = h1 = float(stitch_single.group(1))
                    unit = "stitch"
                elif angle_single:
                    angle = float(angle_single.group(1))
                    if re.search(
                        r"\b(?:counterclockwise|counter-clockwise|anticlockwise|anti-clockwise)\b",
                        raw,
                        re.IGNORECASE,
                    ):
                        angle = (-angle) % 360.0
                    h0 = h1 = angle % 360.0
                    unit = "degree"
                else:
                    h0 = h1 = None
                    unit = None
        for feature_match in features:
            name = re.sub(r"\s+", " ", feature_match.group(1).lower())
            if name.startswith("safety eye"):
                name = "safety eyes"
            elif name == "eye":
                name = "eyes"
            elif name == "ear":
                name = "ears"
            elif name == "horn":
                name = "horns"
            elif name in {"tail"}:
                name = "tails"
            found.append(
                FeatureBounds(
                    name, parent, r0, r1, h0, h1, unit, raw.strip(), line_number
                )
            )
    return found


def _gauge_cm(text: str) -> tuple[float, float] | None:
    pattern = re.compile(
        r"\b(?:gauge\s*:?\s*)?(\d+(?:\.\d+)?)\s*(?:sc\s*)?(?:sts?|stitches)\s*(?:and|[,/]?)\s*"
        r"(\d+(?:\.\d+)?)\s*(?:rows?|rnds?)\s*(?:=|in)\s*"
        r"(\d+(?:\.\d+)?)\s*(inches?|in|cm)\b",
        re.IGNORECASE,
    )
    gauges: set[tuple[float, float]] = set()
    for match in pattern.finditer(text):
        unit_size = float(match.group(3))
        unit = match.group(4).lower()
        centimeters = unit_size * 2.54 if unit.startswith("in") else unit_size
        if centimeters <= 0:
            continue
        gauges.add(
            (
                float(match.group(1)) / centimeters,
                float(match.group(2)) / centimeters,
            )
        )
    if len(gauges) != 1:
        return None
    return next(iter(gauges))


def seam_stretch_mismatch(
    seam_stitches: int,
    body_rounds: int,
    gauge_stitches_per_cm: float,
    gauge_rounds_per_cm: float,
    threshold: float = 1.5,
) -> str | None:
    """Compare explicit seam width and round span using an explicit gauge."""
    if (
        min(seam_stitches, body_rounds) < 0
        or min(gauge_stitches_per_cm, gauge_rounds_per_cm) <= 0
        or threshold <= 1
    ):
        return None
    width_cm = seam_stitches / gauge_stitches_per_cm
    height_cm = body_rounds / gauge_rounds_per_cm
    small = min(width_cm, height_cm)
    if small == 0 or max(width_cm, height_cm) <= threshold * small:
        return None
    return (
        f"SeamStretchMismatch: explicit seam width {width_cm:.2f} cm and round span "
        f"{height_cm:.2f} cm differ by more than {threshold:g}x. Verify the fit or gauge."
    )


def _circular_delta(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def _pair_midpoint(a: float, b: float) -> float | None:
    x = math.cos(math.radians(a)) + math.cos(math.radians(b))
    y = math.sin(math.radians(a)) + math.sin(math.radians(b))
    if math.hypot(x, y) < 1e-9:
        return None
    return math.degrees(math.atan2(y, x)) % 360.0


def _minimal_arc(angles: list[float]) -> float:
    ordered = sorted(angle % 360.0 for angle in angles)
    if len(ordered) < 2:
        return 0.0
    gaps = [ordered[i + 1] - ordered[i] for i in range(len(ordered) - 1)]
    gaps.append(ordered[0] + 360.0 - ordered[-1])
    return 360.0 - max(gaps)


def quadruped_compass_findings(
    attachments: Mapping[str, tuple[int, int, int]],
) -> list[AdvancedFinding]:
    """Check explicit four-leg positions under a defined polar reference.

    Mapping values are ``(round_number, one_based_stitch_index, round_stitch_count)``.
    The calling contract is that stitch 1 is centered on the explicitly defined
    front axis. Text input is checked only when it states that reference and
    explicitly identifies the attachment as JAYG.
    """
    normalized = {key.casefold(): value for key, value in attachments.items()}
    names = ("foreleg 1", "foreleg 2", "hind leg 1", "hind leg 2")
    if not all(name in normalized for name in names):
        return []
    positions = [normalized[name] for name in names]
    if any(not isinstance(item, (tuple, list)) or len(item) != 3 for item in positions):
        return []
    if any(
        not all(
            isinstance(value, int) and not isinstance(value, bool) for value in item
        )
        for item in positions
    ):
        return []
    if any(item[0] < 1 for item in positions):
        return []
    if (
        len({item[0] for item in positions}) != 1
        or len({item[2] for item in positions}) != 1
    ):
        return []
    try:
        front_axis = stitch_to_angle(1, positions[0][2])
        angles = {
            name: (
                stitch_to_angle(normalized[name][1], normalized[name][2]) - front_axis
            )
            % 360.0
            for name in names
        }
    except (TypeError, ValueError):
        return []
    all_angles = list(angles.values())
    findings: list[AdvancedFinding] = []
    if _minimal_arc(all_angles) <= 210.0:
        findings.append(
            AdvancedFinding(
                "QuadrupedHemisphereClustering",
                "The four explicitly mapped limb positions fit within a 210° arc; review their spacing around the body.",
                "warning",
            )
        )
    fore_mid = _pair_midpoint(angles["foreleg 1"], angles["foreleg 2"])
    hind_mid = _pair_midpoint(angles["hind leg 1"], angles["hind leg 2"])
    if fore_mid is not None and _circular_delta(fore_mid, 0.0) > 75.0:
        findings.append(
            AdvancedFinding(
                "QuadrupedForelimbHemisphere",
                "The explicit foreleg-pair midpoint falls outside ±75° of the defined front axis.",
                "warning",
            )
        )
    if hind_mid is not None and _circular_delta(hind_mid, 180.0) > 75.0:
        findings.append(
            AdvancedFinding(
                "QuadrupedHindlimbHemisphere",
                "The explicit hind-leg-pair midpoint falls outside ±75° of the defined back axis.",
                "warning",
            )
        )
    if fore_mid is not None and hind_mid is not None:
        separation = _circular_delta(fore_mid, hind_mid)
        if abs(separation - 90.0) <= 15.0:
            findings.append(
                AdvancedFinding(
                    "QuadrupedCompassCrossError",
                    "The explicit fore- and hind-pair midpoints are approximately orthogonal; review the stated limb quadrants.",
                    "warning",
                )
            )
    return findings


_JAYG_WORDING = re.compile(r"\b(?:JAYG|join\s+as\s+you\s+go)\b", re.IGNORECASE)
_FRONT_STITCH_REFERENCE = re.compile(
    r"\bstitch\s*1\b[^.\n]{0,35}\b(?:is\s+)?(?:at|centered\s+at|aligned\s+with|marks?)\s+"
    r"(?:(?:the\s+)?(?:center|centre)\s+)?front(?:\s+axis)?\b|"
    r"\b(?:front\s+axis|center\s+front|centre\s+front)\s+(?:is|aligns\s+with)\s+stitch\s*1\b",
    re.IGNORECASE,
)
_QUADRUPED_POSITION = re.compile(
    r"\b(?P<name>fore\s*leg\s*[12]|hind\s*leg\s*[12])\b"
    r"[^.\n]{0,50}?\b(?:round|rnd)\s*(?P<round>\d+)\b"
    r"[^.\n]{0,50}?\b(?:stitch|st)\s*(?P<stitch>\d+)\s+of\s+(?P<count>\d+)\b",
    re.IGNORECASE,
)


def quadruped_findings_from_text(text: str) -> list[AdvancedFinding]:
    """Check JAYG limb positions only with an explicit stitch-1/front reference."""
    findings: list[AdvancedFinding] = []
    for heading, body, _start_line in split_sections(text):
        body_start = _start_line + (1 if heading else 0)
        scope = f"{heading}\n{body}"
        if not _JAYG_WORDING.search(scope) or not _FRONT_STITCH_REFERENCE.search(scope):
            continue
        positions: dict[str, tuple[int, int, int]] = {}
        line_by_name: dict[str, int] = {}
        for line_number, line in enumerate(body.splitlines(), start=body_start):
            for match in _QUADRUPED_POSITION.finditer(line):
                raw_name = re.sub(r"\s+", " ", match.group("name").lower())
                digit = re.search(r"[12]", raw_name)
                if not digit:
                    continue
                limb = "foreleg" if raw_name.startswith("fore") else "hind leg"
                name = f"{limb} {digit.group(0)}"
                positions[name] = (
                    int(match.group("round")),
                    int(match.group("stitch")),
                    int(match.group("count")),
                )
                line_by_name[name] = line_number
        section_findings = quadruped_compass_findings(positions)
        line_number = min(line_by_name.values(), default=0)
        findings.extend(
            AdvancedFinding(item.code, item.message, item.severity, line_number)
            for item in section_findings
        )
    return findings


def _color_runs(body: str) -> tuple[tuple[int, str], ...]:
    matches = list(re.finditer(r"\b(\d+)\s+([A-Z])\b", body))
    if len(matches) < 3:
        return ()
    return tuple((int(m.group(1)), m.group(2)) for m in matches)


def spiral_colorwork_findings(text: str) -> list[AdvancedFinding]:
    """Warn only for four or more consecutive, identical explicit spiral color runs."""
    findings: list[AdvancedFinding] = []
    shift_every_round = re.compile(
        r"\bjogless\b|\b(?:shift|offset|move\s+the\s+start)\b[^.\n]{0,80}"
        r"\b(?:each|every|per)\s+round\b",
        re.IGNORECASE,
    )
    for heading, body, start_line in split_sections(text):
        body_start = start_line + (1 if heading else 0)
        if not re.search(
            r"\b(?:continuous\s+spiral|unjoined\s+spiral|worked\s+in\s+an?\s+unjoined\s+spiral)\b",
            body,
            re.IGNORECASE,
        ):
            continue
        if shift_every_round.search(body):
            continue
        records = []
        for local_index, line in enumerate(body.splitlines(), start=body_start):
            header = ROUND_HEADER.match(line.strip())
            if not header:
                continue
            signature = _color_runs(header.group(2))
            stated_count = STATED_COUNT.search(header.group(2))
            if (
                signature
                and stated_count
                and sum(count for count, _color in signature)
                == int(stated_count.group(1))
                and signature[0][1] == signature[-1][1]
            ):
                records.append((int(header.group(1)), signature, local_index))
        streak: list[tuple[int, tuple[tuple[int, str], ...], int]] = []
        for record in records:
            if streak and (
                record[0] != streak[-1][0] + 1 or record[1] != streak[-1][1]
            ):
                if len(streak) >= 4:
                    findings.append(_spiral_finding(streak))
                streak = []
            streak.append(record)
        if len(streak) >= 4:
            findings.append(_spiral_finding(streak))
    return findings


def _spiral_finding(streak):
    start, end = streak[0][0], streak[-1][0]
    return AdvancedFinding(
        "SpiralColorworkDrift",
        f"Rounds {start}–{end} repeat identical stitch-count color panels in a continuous unjoined spiral without an explicit shift. The panel may drift; consider a written offset or jog correction.",
        "warning",
        streak[0][2],
    )


_EXPLICIT_SEAM_SPAN = re.compile(
    r"\b(?:seam|attachment\s+span)\s*[:=]\s*(\d+)\s*(?:sc\s*)?(?:sts?|stitches)\b"
    r"[^.\n]{0,60}?\b(\d+)\s*(?:rounds?|rnds?|rows?)\b",
    re.IGNORECASE,
)


def seam_stretch_findings(text: str) -> list[AdvancedFinding]:
    gauge = _gauge_cm(text)
    if gauge is None:
        return []
    findings = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = _EXPLICIT_SEAM_SPAN.search(line)
        if not match:
            continue
        message = seam_stretch_mismatch(
            int(match.group(1)), int(match.group(2)), gauge[0], gauge[1]
        )
        if message:
            findings.append(
                AdvancedFinding("SeamStretchMismatch", message, "warning", line_number)
            )
    return findings


def spatial_findings(text: str) -> list[AdvancedFinding]:
    return (
        find_spatial_collisions(attachment_bounds_from_text(text))
        + seam_stretch_findings(text)
        + spiral_colorwork_findings(text)
    )
