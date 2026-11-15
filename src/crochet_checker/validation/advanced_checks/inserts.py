"""Explicit insert-diameter and flattened-tube closure checks."""

from __future__ import annotations

import math
import re

from .common import AdvancedFinding, ROUND_HEADER, STATED_COUNT, split_sections
from .spatial import _gauge_cm


def check_insert_diameter(
    insert_diameter_cm: float,
    opening_stitches: int,
    gauge_stitches_per_cm: float,
) -> AdvancedFinding | None:
    """Compare an explicit rigid insert and opening using an explicit gauge.

    This is an idealized circumference-to-diameter estimate, not a stretch or
    fit guarantee. The result is therefore a warning to verify the materials.
    """
    if insert_diameter_cm <= 0 or opening_stitches <= 0 or gauge_stitches_per_cm <= 0:
        return None
    opening_diameter_cm = opening_stitches / (gauge_stitches_per_cm * math.pi)
    if insert_diameter_cm <= opening_diameter_cm:
        return None
    required = math.ceil(insert_diameter_cm * math.pi * gauge_stitches_per_cm)
    return AdvancedFinding(
        "InsertDiameterOverflow",
        f"A {insert_diameter_cm:g} cm insert exceeds the estimated {opening_diameter_cm:.2f} cm opening at the stated gauge; about {required} stitches would be needed around its circumference. Verify the fit and gauge.",
        "warning",
    )


def check_folded_tube_closure(
    tube_stitches: int, closure_stitches: int
) -> list[AdvancedFinding]:
    """Compare explicit closing stitches with a two-layer flattened tube."""
    if tube_stitches <= 0 or closure_stitches < 0:
        return []
    expected = (tube_stitches + 1) // 2
    if closure_stitches < expected:
        joins_left = expected - closure_stitches
        return [
            AdvancedFinding(
                "PartialTubeClosure",
                f"A {tube_stitches}-stitch tube typically needs about {expected} joining stitches when flattened, but only {closure_stitches} are written; approximately {joins_left} joins may remain unclosed. Verify the intended closure method.",
                "warning",
            )
        ]
    if closure_stitches > expected:
        return [
            AdvancedFinding(
                "FoldedTubeClosureMismatch",
                f"The written closure uses {closure_stitches} stitches for a {tube_stitches}-stitch tube; the simple two-layer estimate is {expected}. Verify the closure construction.",
                "warning",
            )
        ]
    return []


_INSERT = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*cm\s+(dowel|rod|core|ring|disc|disk|tube)\b"
    r"[^.\n]{0,80}?\b(?:inside|in)\b[^.\n]{0,50}?"
    r"(?:opening\s+of\s+|opening\s*[:=]\s*|)(\d+)\s*[- ]?stitch(?:es)?\b",
    re.IGNORECASE,
)
_CLOSURE = re.compile(
    r"\bflatten(?:ed|ing)?\b[^.\n]{0,70}?\b(?:close|sew|cinch|graft|seam)\w*\b"
    r"[^.\n]{0,50}?\b(\d+)\s+(?:sc|single\s+crochet)\b",
    re.IGNORECASE,
)


def insert_findings(text: str) -> list[AdvancedFinding]:
    findings: list[AdvancedFinding] = []
    gauge = _gauge_cm(text)
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = _INSERT.search(line)
        if match and gauge:
            item = check_insert_diameter(
                float(match.group(1)),
                int(match.group(3)),
                gauge[0],
            )
            if item:
                findings.append(
                    AdvancedFinding(item.code, item.message, item.severity, line_number)
                )

    for _heading, body, start_line in split_sections(text):
        counts: list[tuple[int, int, int]] = []
        body_start = start_line + (1 if _heading else 0)
        for local_index, line in enumerate(body.splitlines()):
            header = ROUND_HEADER.match(line.strip())
            stated = STATED_COUNT.search(line.strip())
            if header and stated:
                counts.append(
                    (
                        int(header.group(1)),
                        int(stated.group(1)),
                        body_start + local_index,
                    )
                )
        if not counts:
            continue
        for local_index, line in enumerate(body.splitlines()):
            if not re.search(r"\bflatten(?:ed|ing)?\b", line, re.IGNORECASE):
                continue
            closure = _CLOSURE.search(line)
            if not closure:
                continue
            closing_count = int(closure.group(1))
            line_number = body_start + local_index
            preceding = [record for record in counts if record[2] <= line_number]
            if not preceding:
                continue
            tube_count = preceding[-1][1]
            for finding in check_folded_tube_closure(tube_count, closing_count):
                findings.append(
                    AdvancedFinding(
                        finding.code,
                        finding.message,
                        finding.severity,
                        line_number,
                    )
                )
    return findings
