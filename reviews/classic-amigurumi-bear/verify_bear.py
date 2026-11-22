#!/usr/bin/env python3
"""Independent deterministic verifier for the "Classic Amigurumi Bear" pattern.

Written from scratch so that no finding depends on the repository's own parser.
It reads the pattern in its ORIGINAL notation (square-bracket repeats, "N times",
"around") and models every round as a sequence of atomic operations:

    sc  -> consumes 1 stitch, produces 1
    inc -> consumes 1 stitch, produces 2
    dec -> consumes 2 stitches, produces 1

Foundation rounds (magic ring / chain ring) consume nothing.

A round is valid only when BOTH hold:
  * stitches consumed == stitches available from the previous round
  * stitches produced == the count stated in the pattern

Usage:
    python verify_bear.py            # check the pattern as submitted
    python verify_bear.py --fixed    # check the corrected pattern
"""

from __future__ import annotations

import re
import sys

COST = {"sc": (1, 1), "inc": (1, 2), "dec": (2, 1)}

_TOKEN = re.compile(r"(?:(sc|inc|dec)\s*(\d+)?|(\d+)\s*(sc|inc|dec))\Z", re.I)


def _normalise(text: str) -> str:
    """En/em dashes and smart quotes break naive parsers - fold them first."""
    return text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")


def _token_cost(token: str) -> tuple[int, int] | None:
    """Return (consumed, produced) for a single token such as 'sc 3' or '3 sc'."""
    match = _TOKEN.match(token.strip())
    if not match:
        return None
    stitch_a, count_a, count_b, stitch_b = match.groups()
    if stitch_a:
        stitch, count = stitch_a.lower(), int(count_a) if count_a else 1
    else:
        stitch, count = stitch_b.lower(), int(count_b)
    consumed, produced = COST[stitch]
    return consumed * count, produced * count


def parse_round(body: str, available: int) -> tuple[int, int, bool]:
    """Return (consumed, produced, is_foundation) for one round instruction."""
    body = _normalise(body).strip().rstrip(".")
    lowered = body.lower()

    # --- foundation rounds -------------------------------------------------
    if "magic ring" in lowered:
        found = re.search(r"(\d+)\s*sc|sc\s*(\d+)", body, re.I)
        made = int(found.group(1) or found.group(2)) if found else 6
        return 0, made, True
    if re.search(r"\bch\s*\d+.*\bring\b", body, re.I):
        # "Ch 4, join with sl st to form a ring" creates no stitches at all.
        return 0, 0, True
    if re.search(r"sc\s+into\s+(the\s+)?ring", body, re.I):
        found = re.search(r"(\d+)\s*sc", body, re.I)
        return 0, int(found.group(1)), True

    # --- plain round -------------------------------------------------------
    if re.fullmatch(r"sc(\s+in\s+each\s+st)?\s+around", body, re.I):
        return available, available, False

    consumed = produced = 0

    # --- bracketed repeats: "[...] N times" or "[...] around" --------------
    for inner, repeat in re.findall(r"\[([^\]]*)\]\s*(around|\d+\s*times)", body, re.I):
        unit_consumed = unit_produced = 0
        for token in inner.split(","):
            cost = _token_cost(token)
            if cost:
                unit_consumed += cost[0]
                unit_produced += cost[1]
        if repeat.lower() == "around":
            times = available // unit_consumed if unit_consumed else 0
        else:
            times = int(re.search(r"\d+", repeat).group())
        consumed += unit_consumed * times
        produced += unit_produced * times

    # --- loose operations outside any bracket, e.g. "..., sc 4" ------------
    remainder = re.sub(r"\[[^\]]*\]\s*(around|\d+\s*times)", "", body, flags=re.I)
    for token in re.split(r"[,;]", remainder):
        cost = _token_cost(token)
        if cost:
            consumed += cost[0]
            produced += cost[1]

    return consumed, produced, False


# (round label, instruction, stated count or None)
ORIGINAL: dict[str, list[tuple[str, str, int | None]]] = {
    "Head & Body": [
        ("1", "Magic ring with 6 sc", 6),
        ("2", "[inc] around", 12),
        ("3", "[sc 1, inc] 6 times", 18),
        ("4", "[sc 2, inc] 6 times", 24),
        ("5", "[sc 3, inc] 6 times", 30),
        ("6-10", "sc in each st around", 30),
        ("11", "[sc 3, dec] 6 times", 24),
        ("12", "[sc 1, dec] 6 times", 12),
        ("13", "[sc 2, inc] 6 times", 30),
        ("14-18", "sc around", 30),
        ("19", "[sc 3, dec] 6 times", 24),
        ("20", "[sc 2, dec] 6 times", 18),
        ("21", "[sc 1, dec] 6 times", 12),
        ("22", "[dec] around", 6),
    ],
    "Ears (make 2)": [
        ("1", "Ch 4, join with sl st to form a ring", None),
        ("2", "6 sc into ring", 6),
        ("3", "[sc, inc] 3 times", 9),
        ("4", "sc in each st around", 12),
    ],
    "Muzzle": [
        ("1", "Magic ring, sc 6", 6),
        ("2", "[inc] around", 12),
        ("3", "[sc 3, inc] 3 times", 15),
    ],
    "Arms (make 2)": [
        ("1", "Magic ring 5 sc", 5),
        ("2", "[inc] around", 10),
        ("3-8", "sc in each st around", 10),
        ("9", "[dec] 3 times, sc 4", 6),
    ],
    "Legs (make 2)": [
        ("1", "Magic ring 6 sc", 6),
        ("2", "[inc] around", 12),
        ("3", "[sc 1, inc] 6 times", 18),
        ("4-8", "sc around", 18),
        ("9", "[sc 1, dec] 6 times", 12),
        ("10", "[dec] 6 times", 6),
    ],
}

CORRECTED: dict[str, list[tuple[str, str, int | None]]] = {
    "Head & Body": [
        ("1", "Magic ring with 6 sc", 6),
        ("2", "[inc] around", 12),
        ("3", "[sc 1, inc] 6 times", 18),
        ("4", "[sc 2, inc] 6 times", 24),
        ("5", "[sc 3, inc] 6 times", 30),
        ("6-10", "sc in each st around", 30),
        ("11", "[sc 3, dec] 6 times", 24),
        ("12", "[sc 2, dec] 6 times", 18),
        ("13", "[sc 2, inc] 6 times", 24),
        ("14", "[sc 3, inc] 6 times", 30),
        ("15-19", "sc in each st around", 30),
        ("20", "[sc 3, dec] 6 times", 24),
        ("21", "[sc 2, dec] 6 times", 18),
        ("22", "[sc 1, dec] 6 times", 12),
        ("23", "[dec] around", 6),
    ],
    "Ears (make 2)": [
        ("1", "Magic ring with 6 sc", 6),
        ("2", "[sc 1, inc] 3 times", 9),
        ("3", "[sc 2, inc] 3 times", 12),
        ("4", "sc in each st around", 12),
    ],
    "Muzzle": [
        ("1", "Magic ring with 6 sc", 6),
        ("2", "[inc] around", 12),
        ("3", "[sc 3, inc] 3 times", 15),
    ],
    "Arms (make 2)": [
        ("1", "Magic ring with 5 sc", 5),
        ("2", "[inc] around", 10),
        ("3-8", "sc in each st around", 10),
        ("9", "[dec] 5 times", 5),
    ],
    "Legs (make 2)": [
        ("1", "Magic ring with 6 sc", 6),
        ("2", "[inc] around", 12),
        ("3", "[sc 1, inc] 6 times", 18),
        ("4-8", "sc in each st around", 18),
        ("9", "[sc 1, dec] 6 times", 12),
        ("10", "[dec] 6 times", 6),
    ],
}


def run(pieces: dict[str, list[tuple[str, str, int | None]]], label: str) -> int:
    defects: list[str] = []
    print(f"\n{'=' * 78}\n{label}\n{'=' * 78}")

    for piece, rounds in pieces.items():
        print(f"\n{piece}")
        print(f"  {'Rnd':<8}{'Avail':>6}{'Used':>6}{'Made':>6}{'Stated':>8}   Verdict")
        available = 0
        for number, body, stated in rounds:
            consumed, produced, foundation = parse_round(body, available)
            verdicts = []

            if available and not foundation and consumed != available:
                if consumed < available:
                    msg = (
                        f"consumes {consumed} of {available} available sts, "
                        f"leaving {available - consumed} unworked"
                    )
                    verdicts.append(f"ORPHAN: {available - consumed} st left unworked")
                else:
                    msg = f"requires {consumed} sts but only {available} exist"
                    verdicts.append(f"IMPOSSIBLE: needs {consumed}, only {available}")
                defects.append(f"{piece} Round {number}: {msg}")

            if stated is not None and produced != stated:
                verdicts.append(f"COUNT: makes {produced}, states {stated}")
                defects.append(
                    f"{piece} Round {number}: makes {produced} sts "
                    f"but the round states {stated}"
                )

            print(
                f"  {number:<8}{available:>6}{consumed:>6}{produced:>6}"
                f"{str(stated):>8}   {'; '.join(verdicts) or 'ok'}"
            )
            # Trust the stated count going forward so one bad round does not
            # cascade false positives into every round after it.
            available = stated if stated is not None else produced

    print(f"\n{'#' * 78}")
    print(f"TOTAL MATHEMATICAL DEFECTS: {len(defects)}")
    for defect in defects:
        print(f"  - {defect}")
    return len(defects)


if __name__ == "__main__":
    use_fixed = "--fixed" in sys.argv
    count = run(
        CORRECTED if use_fixed else ORIGINAL,
        "CORRECTED PATTERN" if use_fixed else "PATTERN AS SUBMITTED",
    )
    sys.exit(1 if count else 0)
