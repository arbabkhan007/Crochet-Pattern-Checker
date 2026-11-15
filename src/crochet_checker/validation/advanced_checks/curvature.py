"""Count-based curvature checks for explicitly flat, centered sc pieces."""

from __future__ import annotations

import re
from collections.abc import Iterable

from .common import AdvancedFinding, ROUND_HEADER, STATED_COUNT, split_sections

_FLAT_INTENT = re.compile(
    r"\b(?:flat|disc|disk|medallion|base|coaster)\b", re.IGNORECASE
)
_CENTER_START = re.compile(
    r"\b(?:magic\s+ring|center(?:ed)?\s+ring|centre(?:d)?\s+ring|central\s+ring)\b",
    re.IGNORECASE,
)
_NON_SC = re.compile(
    r"\b(?:hdc|dc|tr|dtr|treble|double\s+crochet|half\s+double)\b",
    re.IGNORECASE,
)


def check_flat_curvature(
    round_counts: Iterable[tuple[int, int]],
    *,
    flat_intent: bool,
    center_start: bool,
    single_crochet: bool,
) -> list[AdvancedFinding]:
    """Flag large accelerations in explicit counts, not ordinary circle growth.

    At least three consecutive, positive round counts are needed before a
    change in growth rate is compared. The initial increase is not judged:
    common foundation counts vary, and a 6- or 8-stitch increase can be
    intentional. Results are warnings because gauge, tension, and shaping can
    affect whether a piece actually lies flat.
    """
    if not (flat_intent and center_start and single_crochet):
        return []

    counts = sorted(
        (int(round_number), int(count)) for round_number, count in round_counts
    )
    if not counts or any(number < 1 or count <= 0 for number, count in counts):
        return []
    by_round: dict[int, int] = {}
    for number, count in counts:
        if number in by_round:
            return []
        by_round[number] = count

    findings: list[AdvancedFinding] = []
    for number in sorted(by_round):
        if number < 3 or number - 1 not in by_round or number - 2 not in by_round:
            continue
        current_delta = by_round[number] - by_round[number - 1]
        previous_delta = by_round[number - 1] - by_round[number - 2]
        if current_delta <= 0 or previous_delta <= 0:
            continue
        if current_delta >= 2 * previous_delta and current_delta - previous_delta >= 6:
            findings.append(
                AdvancedFinding(
                    "HyperbolicCurvatureOverflow",
                    f"Explicit flat single-crochet counts accelerate from an increase of {previous_delta} to {current_delta} stitches at Round {number}. Review the count sequence and intended shaping; flatness cannot be determined from counts alone.",
                    "warning",
                )
            )
        elif current_delta - previous_delta >= 6:
            findings.append(
                AdvancedFinding(
                    "FlatCircleIncreaseOutsideCommonRange",
                    f"The increase grows from {previous_delta} to {current_delta} stitches at Round {number} in an explicitly flat single-crochet circle. Verify the intended shaping and stitch count.",
                    "warning",
                )
            )
    return findings


def curvature_findings(text: str) -> list[AdvancedFinding]:
    findings: list[AdvancedFinding] = []
    for heading, body, _line in split_sections(text):
        section = f"{heading}\n{body}"
        if not _FLAT_INTENT.search(section) or not _CENTER_START.search(section):
            continue
        if _NON_SC.search(section):
            continue
        if not re.search(r"\bsc\b", section, re.IGNORECASE):
            continue

        round_counts: list[tuple[int, int]] = []
        line_by_round: dict[int, int] = {}
        body_start = _line + (1 if heading else 0)
        for line_number, line in enumerate(body.splitlines(), start=body_start):
            header = ROUND_HEADER.match(line.strip())
            stated = STATED_COUNT.search(line.strip())
            if header and stated:
                round_number = int(header.group(1))
                round_counts.append((round_number, int(stated.group(1))))
                line_by_round[round_number] = line_number

        for finding in check_flat_curvature(
            round_counts,
            flat_intent=True,
            center_start=True,
            single_crochet=True,
        ):
            match = re.search(r"\bRound\s+(\d+)\b", finding.message)
            line_number = line_by_round.get(int(match.group(1)), 0) if match else 0
            findings.append(
                AdvancedFinding(
                    finding.code,
                    finding.message,
                    finding.severity,
                    line_number,
                )
            )
    return findings
