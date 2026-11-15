"""Stateful FLO/BLO occupancy and explicit hoof/sole crease alignment."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from .common import AdvancedFinding, ROUND_HEADER, split_sections


@dataclass(frozen=True)
class RoundLoopState:
    round_number: int
    flo_free: bool | None
    blo_free: bool | None
    established_by_round: int | None = None


def build_loop_states(round_modes: Mapping[int, str]) -> dict[int, RoundLoopState]:
    """Build previous-round loop banks from each round's written loop mode.

    ``BLO`` consumes the prior round's BLO and leaves its FLO free; ``FLO``
    does the converse. ``BOTH`` consumes both. A missing/ambiguous next-round
    mode stays unknown.
    """
    states: dict[int, RoundLoopState] = {}
    for number in sorted(round_modes):
        next_number = number + 1
        mode = round_modes.get(next_number, "UNKNOWN").upper()
        if mode == "BLO":
            flo_free, blo_free = True, False
        elif mode == "FLO":
            flo_free, blo_free = False, True
        elif mode == "BOTH":
            flo_free, blo_free = False, False
        else:
            flo_free, blo_free = None, None
        states[number] = RoundLoopState(
            number,
            flo_free,
            blo_free,
            next_number if mode in {"BLO", "FLO", "BOTH"} else None,
        )
    return states


def check_surface_loop_join(
    target_round: int,
    requested_loop: str,
    states: Mapping[int, RoundLoopState],
) -> str | None:
    """Return a collision message only when the requested bank is known occupied."""
    requested = requested_loop.upper()
    if requested not in {"FLO", "BLO"}:
        raise ValueError("requested_loop must be 'FLO' or 'BLO'.")
    state = states.get(target_round)
    if state is None:
        return None
    free = state.flo_free if requested == "FLO" else state.blo_free
    if free is not False:
        return None
    occupied_by = state.established_by_round
    source = f"Round {occupied_by}" if occupied_by is not None else "a later round"
    remaining = "BLO" if requested == "FLO" else "FLO"
    return (
        f"LoopCollisionError: Round {target_round} {requested} was already "
        f"consumed by {source}; only {remaining} remains available."
    )


def _mode(body: str) -> str:
    front = bool(re.search(r"\bFLO\b|front\s+loops?\s+only", body, re.IGNORECASE))
    back = bool(re.search(r"\bBLO\b|back\s+loops?\s+only", body, re.IGNORECASE))
    both = bool(re.search(r"\b(?:through\s+)?both\s+loops\b", body, re.IGNORECASE))
    if both and not (front or back):
        return "BOTH"
    if front and back:
        return "UNKNOWN"
    if front:
        return "FLO"
    if back:
        return "BLO"
    # Ordinary crochet stitches are conventionally worked through both top
    # loops. Restrict this default to lines with an explicit stitch token.
    if re.search(
        r"\b(?:sc|hdc|dc|tr|dtr|inc|dec|sc2tog|dc2tog)\b", body, re.IGNORECASE
    ):
        return "BOTH"
    return "UNKNOWN"


_LOOP_ACTION = re.compile(
    r"\b(?:join|attach|sew|work|graft|crochet|insert|use)\b", re.IGNORECASE
)
_LOOP_REFERENCE = re.compile(
    r"\b(?P<loop>FLO|BLO|front\s+loops?|back\s+loops?)\b"
    r"[^.\n]{0,55}?\b(?:of|from|in)\s+(?:round|rnd|r)\s*(?P<number>\d+)\b",
    re.IGNORECASE,
)


def loop_occupancy_findings(text: str) -> list[AdvancedFinding]:
    findings: list[AdvancedFinding] = []
    mode_candidates: dict[int, set[str]] = {}
    sections = split_sections(text)

    # Round and assembly instructions commonly live under different headings.
    # Build one conservative round map before checking any cross-section joins.
    for heading, body, section_line in sections:
        body_start = section_line + (1 if heading else 0)
        for _local_line, line in enumerate(body.splitlines(), start=body_start):
            header = ROUND_HEADER.match(line.strip())
            if header:
                number = int(header.group(1))
                mode_candidates.setdefault(number, set()).add(_mode(header.group(2)))

    modes = {
        number: next(iter(candidates)) if len(candidates) == 1 else "UNKNOWN"
        for number, candidates in mode_candidates.items()
    }
    states = build_loop_states(modes)
    seen_targets: set[tuple[int, int, str]] = set()

    for heading, body, section_line in sections:
        body_start = section_line + (1 if heading else 0)
        for local_line, line in enumerate(body.splitlines(), start=body_start):
            action = _LOOP_ACTION.search(line)
            if not action:
                continue
            # One assembly verb can govern multiple loop banks, e.g. "join ...
            # BLO of Round 13 and FLO of Round 14". Check every explicit target.
            for match in _LOOP_REFERENCE.finditer(line, action.end()):
                loop = "FLO" if match.group("loop").upper().startswith("F") else "BLO"
                number = int(match.group("number"))
                target = (local_line, number, loop)
                if target in seen_targets:
                    continue
                seen_targets.add(target)
                message = check_surface_loop_join(number, loop, states)
                if message:
                    findings.append(
                        AdvancedFinding(
                            "LoopOccupancyCollision", message, "error", local_line
                        )
                    )
    findings.extend(color_crease_findings(text))
    return findings


_COLOR_CHANGE = re.compile(
    r"(?:\b(?:color|colour)\s+change\b[^.\n]{0,50}?\b(?:round|rnd)\s*(\d+)\b|"
    r"\b(?:round|rnd)\s*(\d+)\b[^.\n]{0,50}?\b(?:change|switch)\s+(?:the\s+)?(?:color|colour)\b)",
    re.IGNORECASE,
)
_BLO_ROUND = re.compile(
    r"\bBLO\b[^.\n]{0,35}?\b(?:round|rnd)\s*(\d+)\b|"
    r"\b(?:round|rnd)\s*(\d+)\b[^.\n]{0,35}?\bBLO\b",
    re.IGNORECASE,
)


def color_crease_findings(text: str) -> list[AdvancedFinding]:
    """Flag explicit hoof/sole color changes whose BLO crease is one round off."""
    lines = list(enumerate(text.splitlines(), start=1))
    changes: list[tuple[int, int]] = []
    crease_rounds: list[tuple[int, int]] = []
    relevant = re.compile(r"\b(?:hoof|sole|shoe|boot)\b", re.IGNORECASE)
    for number, line in lines:
        if not relevant.search(line):
            continue
        change = _COLOR_CHANGE.search(line)
        if change:
            raw = change.group(1) or change.group(2)
            changes.append((int(raw), number))
        for match in _BLO_ROUND.finditer(line):
            raw = match.group(1) or match.group(2)
            crease_rounds.append((int(raw), number))
    findings: list[AdvancedFinding] = []
    for change_round, line_number in changes:
        for crease_round, _crease_line in crease_rounds:
            if abs(change_round - crease_round) == 1:
                findings.append(
                    AdvancedFinding(
                        "ColorChangeCreaseMisalignment",
                        f"The stated BLO sole/hoof crease is Round {crease_round}, "
                        f"one round away from the explicit color change at Round {change_round}. "
                        "Check whether the crease should be on the color-change round.",
                        "warning",
                        line_number,
                    )
                )
    return findings
