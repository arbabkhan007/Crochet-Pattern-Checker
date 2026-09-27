#!/usr/bin/env python3
"""Independent deterministic verifier for the "Celestial Wyvern" pattern.

Written from scratch so no finding depends on the repository's own parser, which
cannot read this pattern's flat rows, multi-piece joins or edging.

Every round/row is modelled as (stitches consumed, stitches produced):
    sc  -> 1 / 1        inc -> 1 / 2        dec -> 2 / 1
    hdc, dc, tr, sl st  -> 1 / 1  (height only; they still consume one base st)

A round is valid only when BOTH hold:
  * consumed == stitches available from the previous round
  * produced == the count stated in the pattern

Usage:
    python verify_wyvern.py            # pattern as submitted
    python verify_wyvern.py --fixed    # corrected pattern
"""

from __future__ import annotations

import math
import sys

# Gauge from the pattern: 20 sts x 22 rows = 4 in
STS_PER_IN = 5.0
ROWS_PER_IN = 5.5

COST = {"sc": (1, 1), "inc": (1, 2), "dec": (2, 1)}


def repeat(unit: list[tuple[str, int]], times: int) -> tuple[int, int]:
    """Cost of repeating `unit` (a list of (stitch, count)) `times` times."""
    consumed = produced = 0
    for stitch, n in unit:
        c, p = COST[stitch]
        consumed += c * n
        produced += p * n
    return consumed * times, produced * times


class Checker:
    def __init__(self) -> None:
        self.defects: list[tuple[str, str, str]] = []

    def head(self, title: str) -> None:
        print(f"\n{'=' * 86}\n{title}\n{'=' * 86}")
        print(f"  {'Rnd':<10}{'Avail':>6}{'Used':>6}{'Made':>6}{'Stated':>8}   Verdict")

    def row(
        self,
        piece: str,
        label: str,
        available: int | None,
        consumed: int,
        produced: int,
        stated: int | None,
        foundation: bool = False,
        note: str = "",
    ) -> int:
        verdicts: list[str] = []
        if not foundation and available is not None and consumed != available:
            if consumed < available:
                verdicts.append(f"ORPHAN: {available - consumed} st unworked")
                self.defects.append(
                    (piece, label, f"consumes {consumed} of {available} available "
                                   f"sts, leaving {available - consumed} unworked")
                )
            else:
                verdicts.append(f"IMPOSSIBLE: needs {consumed}, has {available}")
                self.defects.append(
                    (piece, label, f"requires {consumed} sts but only {available} exist")
                )
        if stated is not None and produced != stated:
            verdicts.append(f"COUNT: makes {produced}, states {stated}")
            self.defects.append(
                (piece, label, f"makes {produced} sts but states {stated}")
            )
        print(
            f"  {label:<10}{str(available):>6}{consumed:>6}{produced:>6}"
            f"{str(stated):>8}   {'; '.join(verdicts) or 'ok'}"
            + (f"   [{note}]" if note else "")
        )
        return stated if stated is not None else produced

    def note(self, piece: str, label: str, message: str) -> None:
        self.defects.append((piece, label, message))
        print(f"     -> {message}")


def run(fixed: bool) -> int:
    c = Checker()
    plain = lambda n: (n, n)  # noqa: E731  - "sc in each st around"

    # ---------------------------------------------------------------- head
    c.head("1. HEAD & NECK")
    a = c.row("Head", "1", None, 0, 6, 6, foundation=True)
    a = c.row("Head", "2", a, *repeat([("inc", 1)], 6), 12)
    a = c.row("Head", "3", a, *repeat([("sc", 1), ("inc", 1)], 6), 18)
    a = c.row("Head", "4", a, *repeat([("sc", 2), ("inc", 1)], 6), 24)
    a = c.row("Head", "5-9", a, *plain(a), 24)
    a = c.row("Head", "10", a, *repeat([("sc", 2), ("dec", 1)], 6), 18)
    a = c.row("Head", "11", a, *repeat([("sc", 1), ("dec", 1)], 6), 12)
    a = c.row("Head", "12", a, *repeat([("sc", 3), ("inc", 1)], 3), 15, note="BLO, Color B")
    a = c.row("Head", "13-16", a, *plain(a), 15)
    neck_top = c.row("Head", "17", a, *repeat([("sc", 4), ("inc", 1)], 3), 18)

    # ----------------------------------------------------------------- toe
    c.head("2a. TOE  (make 3 per leg)")
    t = c.row("Toe", "1", None, 0, 4, 4, foundation=True)
    t = c.row("Toe", "2", t, *repeat([("sc", 1), ("inc", 1)], 2), 6)
    toe = c.row("Toe", "3", t, *plain(t), 6)

    # ------------------------------------------------------------ foot/leg
    c.head("2b. FOOT / LEG")
    pool = 3 * toe
    print(f"  join pool: 3 toes x {toe} sts = {pool} sts available")
    a = c.row("Leg", "4 join", pool, 3 + 3 + 6 + 3 + 3, 3 + 3 + 6 + 3 + 3, 18)
    a = c.row("Leg", "5", a, *repeat([("sc", 4), ("dec", 1)], 3), 15)
    a = c.row("Leg", "6", a, *repeat([("sc", 3), ("dec", 1)], 3), 12)
    a = c.row("Leg", "7-10", a, *plain(a), 12)
    leg_top = c.row("Leg", "11", a, *repeat([("sc", 2), ("dec", 1)], 3), 9 if fixed else 8)

    # --------------------------------------------------------------- torso
    c.head("3. TORSO")
    a = c.row("Torso", "1", None, 0, 6, 6, foundation=True)
    a = c.row("Torso", "2", a, *repeat([("inc", 1)], 6), 12)
    a = c.row("Torso", "3", a, *repeat([("sc", 1), ("inc", 1)], 6), 18)
    a = c.row("Torso", "4", a, *repeat([("sc", 2), ("inc", 1)], 6), 24)
    a = c.row("Torso", "5", a, *repeat([("sc", 3), ("inc", 1)], 6), 30)
    a = c.row("Torso", "6", a, *repeat([("sc", 4), ("inc", 1)], 6), 36)
    a = c.row("Torso", "7-12", a, *plain(a), 36)

    if fixed:
        body_worked, body_skipped, leg_worked = 15 + 15, 3 + 3, 6 + 6
    else:
        body_worked, body_skipped, leg_worked = 10 + 12 + 8, 0, 6 + 6
    print(
        f"  R13 join: body sts worked {body_worked}, explicitly skipped {body_skipped}, "
        f"of {a}  |  leg sts worked {leg_worked} of {2 * leg_top}"
    )
    if body_worked + body_skipped < a:
        c.note("Torso", "13",
               f"only {body_worked} of the {a} body sts are accounted for - "
               f"{a - body_worked - body_skipped} body sts left unworked with no instruction")
    leftover_leg = 2 * leg_top - leg_worked
    if fixed:
        print(f"     -> {leftover_leg} leg sts + {body_skipped} skipped body sts are "
              f"sewn together to close the crotch ({'balanced' if leftover_leg == body_skipped else 'UNBALANCED'})")
    elif leftover_leg:
        c.note("Torso", "13",
               f"only 6 of each leg's {leg_top} top sts are worked - {leftover_leg} leg "
               f"sts left unworked with no instruction")
    a = c.row("Torso", "13", None, body_worked + leg_worked, body_worked + leg_worked, 42,
              foundation=True)
    a = c.row("Torso", "14", a, *plain(a), 42)
    a = c.row("Torso", "15", a, *repeat([("sc", 5), ("dec", 1)], 6), 36)
    a = c.row("Torso", "16-18", a, *plain(a), 36)
    a = c.row("Torso", "19", a, *repeat([("sc", 4), ("dec", 1)], 6), 30)
    a = c.row("Torso", "20", a, *repeat([("sc", 3), ("dec", 1)], 6), 24)
    torso_top = c.row("Torso", "21", a, *repeat([("sc", 2), ("dec", 1)], 6), 18)

    # ---------------------------------------------------------------- wing
    c.head("4. WING  (flat rows)")
    if fixed:
        w = c.row("Wing", "1", None, 0, 21, 21, foundation=True, note="ch 22 -> 21 sc")
        counts = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10]
        for i, stated in enumerate(counts, start=2):
            body = w - 2
            w = c.row("Wing", str(i), w, *repeat([("sc", body), ("dec", 1)], 1), stated)
        wing_rows, wing_width = 12, 21
    else:
        w = c.row("Wing", "1", None, 0, 15, 15, foundation=True, note="ch 16 -> 15 sc")
        w = c.row("Wing", "2", w, *repeat([("sc", 13), ("dec", 1)], 1), 14, note="FLO")
        w = c.row("Wing", "3", w, *repeat([("dec", 1), ("sc", 12)], 1), 13, note="BLO")
        w = c.row("Wing", "4", w, *repeat([("sc", 11), ("dec", 1)], 1), 12, note="FLO")
        w = c.row("Wing", "5", w, *repeat([("sc", 10), ("dec", 1)], 1), 11,
                  note="no loop spec - inconsistent with rows 2-4")
        wing_rows, wing_width = 5, 15

    fan = 7
    print(f"\n  Edging along the row ends: {wing_rows} rows = {wing_rows} row ends")
    if fixed:
        per_fan = 3
        fans = wing_rows // per_fan
        print(f"     fan spans {per_fan} row ends, {fans} fans consume "
              f"{fans * per_fan} of {wing_rows} row ends  -> ok")
    else:
        print(f"     Reading A - all {fan} sts into ONE row end, repeated into every row end:")
        print(f"       {fan} sts x {wing_rows} row ends = {fan * wing_rows} sts on a "
              f"{wing_rows / ROWS_PER_IN:.2f} in edge = {fan} sts per row end")
        print( "       a standard shell/feather edging is 2-3.5 sts per row end -> 2-3.5x too dense,")
        print( "       and there is no anchoring st between fans to control the ruffle")
        print(f"     Reading B - the {fan} sts spread across {fan} consecutive row ends:")
        print(f"       one fan needs {fan} row ends, the wing only has {wing_rows}")
        c.note("Wing", "6",
               f"edging is ambiguous and fails both readings: {fan} sts per row end is "
               f"2-3.5x the standard density, while a {fan}-st fan spread across row ends "
               f"needs {fan} row ends and only {wing_rows} exist")

    # ---------------------------------------------------------------- tail
    c.head("5. TAIL")
    a = c.row("Tail", "1", None, 0, 4, 4, foundation=True)
    a = c.row("Tail", "2-5", a, *plain(a), 4)
    a = c.row("Tail", "6", a, *repeat([("sc", 1), ("inc", 1)], 2), 6)
    a = c.row("Tail", "7-10", a, *plain(a), 6)
    a = c.row("Tail", "11", a, *repeat([("sc", 2), ("inc", 1)], 2), 8)
    a = c.row("Tail", "12-15", a, *plain(a), 8)
    a = c.row("Tail", "16", a, *repeat([("sc", 3), ("inc", 1)], 2), 10)
    if fixed:
        a = c.row("Tail", "17", a, *repeat([("sc", 4), ("inc", 1)], 2), 12)
        a = c.row("Tail", "18-20", a, *plain(a), 12)
    else:
        a = c.row("Tail", "17-20", a, *plain(a), 12)

    # ----------------------------------------------------------- interfaces
    print(f"\n{'=' * 86}\n6. ASSEMBLY INTERFACE & PROPORTION CHECK\n{'=' * 86}")
    match = "MATCH" if neck_top == torso_top else "MISMATCH"
    print(f"  Neck R17 = {neck_top} sts  vs  Torso top = {torso_top} sts  ->  {match}")
    dia = lambda s: (s / STS_PER_IN) / math.pi  # noqa: E731
    print(f"  Head diameter      {dia(24):.2f} in ({dia(24) * 25.4:.0f} mm); "
          f"a 12 mm safety eye is {12 / (dia(24) * 25.4) * 100:.0f}% of that")
    print(f"  Torso diameter     {dia(42):.2f} in, height R1-21 {21 / ROWS_PER_IN:.2f} in")
    print(f"  Legs join at R13   {13 / ROWS_PER_IN:.2f} in up = {13 / 21 * 100:.0f}% of torso height")
    print(f"  Wing               {wing_width / STS_PER_IN:.2f} x {wing_rows / ROWS_PER_IN:.2f} in "
          f"= {(wing_width / STS_PER_IN) / (wing_rows / ROWS_PER_IN):.1f}:1 aspect ratio")
    print(f"  Neck length        {6 / ROWS_PER_IN:.2f} in")
    print(f"  Approx. height     {(21 + 17 + 11) / ROWS_PER_IN:.1f} in")

    print(f"\n{'#' * 86}")
    print(f"TOTAL DEFECTS: {len(c.defects)}")
    for piece, label, message in c.defects:
        print(f"  - {piece} Round/Row {label}: {message}")
    return len(c.defects)


if __name__ == "__main__":
    use_fixed = "--fixed" in sys.argv
    print("CORRECTED PATTERN" if use_fixed else "PATTERN AS SUBMITTED")
    sys.exit(1 if run(use_fixed) else 0)
