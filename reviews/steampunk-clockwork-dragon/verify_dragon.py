#!/usr/bin/env python3
"""Independent deterministic verifier for the "Steampunk Clockwork Dragon".

Written from scratch. The repository engine cannot model any of the things that
matter in this pattern: short rows and their raw edges, popcorns, picots, post
stitches, chain-space sockets, or the leg-gusset join.

Stitch cost model, as (base stitches consumed, stitches produced):
    sc  1/1      inc 1/2      dec 2/1
    hdc 1/1      dc  1/1      fpdc 1/1   (taller, but still one base st)
    pc  1/1      (popcorn: 5 dc worked into ONE st, closed - occupies 1 position)
    picot 0/0    (ch 3 + sl st into the ch - hangs off the previous st,
                  consumes no base stitch and adds no stitch to the count)

A round is valid only when BOTH hold:
    consumed == stitches available   and   produced == stated count

Usage:
    python verify_dragon.py            # pattern as submitted
    python verify_dragon.py --fixed    # corrected pattern
"""

from __future__ import annotations

import math
import sys

STS_PER_IN = 22 / 4.0    # 5.5  - from the pattern's stated gauge
RNDS_PER_IN = 24 / 4.0   # 6.0

COST = {
    "sc": (1, 1), "inc": (1, 2), "dec": (2, 1),
    "hdc": (1, 1), "dc": (1, 1), "fpdc": (1, 1),
    "pc": (1, 1), "picot": (0, 0),
}


def cost(*ops: tuple[str, int]) -> tuple[int, int]:
    consumed = produced = 0
    for stitch, n in ops:
        c, p = COST[stitch]
        consumed += c * n
        produced += p * n
    return consumed, produced


def rep(unit: list[tuple[str, int]], times: int) -> tuple[int, int]:
    c, p = cost(*unit)
    return c * times, p * times


class Checker:
    def __init__(self) -> None:
        self.defects: list[tuple[str, str, str]] = []

    def section(self, title: str) -> None:
        print(f"\n{'=' * 92}\n{title}\n{'=' * 92}")
        print(f"  {'Rnd/Row':<12}{'Avail':>6}{'Used':>6}{'Made':>6}{'Stated':>8}   Verdict")

    def rnd(self, piece: str, label: str, avail: int | None, consumed: int,
            produced: int, stated: int | None, foundation: bool = False,
            note: str = "", partial: bool = False) -> int:
        """`partial=True` marks a deliberate short row, where leaving base
        stitches unworked is the whole point and is not a defect."""
        v: list[str] = []
        if partial and avail is not None and consumed < avail:
            v.append(f"partial row - {avail - consumed} st held, by design")
        if not foundation and not partial and avail is not None and consumed != avail:
            if consumed < avail:
                v.append(f"ORPHAN: {avail - consumed} st unworked")
                self.defects.append((piece, label,
                    f"consumes {consumed} of {avail} available sts, "
                    f"leaving {avail - consumed} unworked"))
            else:
                v.append(f"IMPOSSIBLE: needs {consumed}, has {avail}")
                self.defects.append((piece, label,
                    f"requires {consumed} sts but only {avail} exist"))
        if stated is not None and produced != stated:
            v.append(f"COUNT: makes {produced}, states {stated}")
            self.defects.append((piece, label,
                f"makes {produced} sts but states {stated}"))
        print(f"  {label:<12}{str(avail):>6}{consumed:>6}{produced:>6}{str(stated):>8}"
              f"   {'; '.join(v) or 'ok'}" + (f"   [{note}]" if note else ""))
        return stated if stated is not None else produced

    def fail(self, piece: str, label: str, message: str) -> None:
        self.defects.append((piece, label, message))
        print(f"     !! {message}")


def run(fixed: bool) -> int:
    c = Checker()
    flat = lambda n: (n, n)  # noqa: E731

    # ============================================================ 1. HEAD
    c.section("1. HEAD & CURVED JAW ASSEMBLY")
    a = c.rnd("Head", "1", None, 0, 6, 6, foundation=True)
    a = c.rnd("Head", "2", a, *rep([("inc", 1)], 6), 12)
    a = c.rnd("Head", "3", a, *rep([("sc", 1), ("inc", 1)], 6), 18)
    a = c.rnd("Head", "4", a, *rep([("sc", 2), ("inc", 1)], 6), 24)
    a = c.rnd("Head", "5", a, *rep([("sc", 3), ("inc", 1)], 6), 30)
    a = c.rnd("Head", "6-8", a, *flat(a), 30)
    # R9: sc 10 + [pc, sc] x5 + sc 10
    c9 = cost(("sc", 10)), rep([("pc", 1), ("sc", 1)], 5), cost(("sc", 10))
    a = c.rnd("Head", "9", a, sum(x[0] for x in c9), sum(x[1] for x in c9), 30,
              note="popcorn scale ridge")
    base = a = c.rnd("Head", "10", a, *flat(a), 30)

    # --- short rows -----------------------------------------------------
    print("  -- short-row jaw shaping --")
    sr = c.rnd("Head", "11a", base, *cost(("sc", 12)), 12, partial=True,
               note="short row: holds the remaining base sts for round 12")
    sr = c.rnd("Head", "11b", sr, *cost(("dec", 1), ("sc", 8), ("dec", 1)), 10)
    sr = c.rnd("Head", "11c", sr, *cost(("sc", 10)), 10)

    short_rows = 3                       # rows 11a, 11b, 11c
    raw_edges = 2 * short_rows           # row ends on each side of the block
    live_sr = sr                         # live sts on top of row 11c
    untouched = base - 12                # round-10 sts the short rows never touched
    perimeter = live_sr + untouched + raw_edges
    print(f"  -- opening perimeter after short rows: {live_sr} live short-row sts "
          f"+ {untouched} untouched R10 sts + {raw_edges} raw row-ends = {perimeter}")

    if fixed:
        r12_consumed = r12_made = live_sr + 3 + untouched + 3
        a = c.rnd("Head", "12", perimeter, r12_consumed, r12_made, 34,
                  note="raw edges now worked")
        a = c.rnd("Head", "13", a, *(lambda cp: (cp[0] + 4, cp[1] + 4))(
            rep([("sc", 3), ("dec", 1)], 6)), 28)
        a = c.rnd("Head", "14", a, *rep([("sc", 2), ("dec", 1)], 7), 21)
        a = c.rnd("Head", "15", a, *rep([("sc", 1), ("dec", 1)], 7), 14)
        a = c.rnd("Head", "16", a, *rep([("sc", 6), ("inc", 1)], 2), 16)
        neck_top = c.rnd("Head", "17-20", a, *flat(a), 16)
    else:
        a = c.rnd("Head", "12", perimeter, 10 + 18, 10 + 18, 28, partial=True,
                  note="'sc 10 across short row edge, sc 18 across R10'")
        c.fail("Head", "12",
               f"rejoining round accounts for only 28 of the {perimeter} perimeter "
               f"positions - the {raw_edges} raw row-ends of the short-row block are "
               f"never worked into, leaving two {short_rows}-row gaps at the jaw hinge")
        a = c.rnd("Head", "13", a, *rep([("sc", 2), ("dec", 1)], 7), 21)
        a = c.rnd("Head", "14", a, *rep([("sc", 1), ("dec", 1)], 7), 14)
        a = c.rnd("Head", "15", a, *rep([("sc", 5), ("inc", 1)], 2), 16)
        neck_top = c.rnd("Head", "16-19", a, *flat(a), 16)

    # ============================================================= 2. LEG
    c.section("2. CLOCKWORK THIGH & LEG  (make 2)")
    a = c.rnd("Leg", "1", None, 0, 8, 8, foundation=True, note="joined rounds")
    a = c.rnd("Leg", "2", a, *rep([("inc", 1)], 8), 16, note="joined")
    a = c.rnd("Leg", "3", a, *rep([("sc", 1), ("picot", 1)], 16), 16,
              note="16 sc + 16 picots")
    a = c.rnd("Leg", "4", a, *rep([("sc", 1), ("inc", 1)], 8), 24, note="BLO")
    a = c.rnd("Leg", "5-8", a, *flat(a), 24, note="switches to spiral, unannounced")
    a = c.rnd("Leg", "9", a, *rep([("sc", 2), ("dec", 1)], 6), 18)
    a = c.rnd("Leg", "10", a, *rep([("sc", 1), ("dec", 1)], 6), 12)
    a = c.rnd("Leg", "11-14", a, *flat(a), 12)
    leg_top = c.rnd("Leg", "15", a, *cost(("dec", 3), ("sc", 6)), 9)
    leg_into_body, leg_gusset = 6, leg_top - 6
    print(f"  -- leg top {leg_top} sts: {leg_into_body} worked into torso R15, "
          f"{leg_gusset} left for the crotch gusset")

    # =========================================================== 3. TORSO
    c.section("3. TORSO & INTEGRATED GEAR CHASSIS")
    a = c.rnd("Torso", "1", None, 0, 6, 6, foundation=True)
    a = c.rnd("Torso", "2", a, *rep([("inc", 1)], 6), 12)
    a = c.rnd("Torso", "3", a, *rep([("sc", 1), ("inc", 1)], 6), 18)
    a = c.rnd("Torso", "4", a, *rep([("sc", 2), ("inc", 1)], 6), 24)
    a = c.rnd("Torso", "5", a, *rep([("sc", 3), ("inc", 1)], 6), 30)
    a = c.rnd("Torso", "6", a, *rep([("sc", 4), ("inc", 1)], 6), 36)
    a = c.rnd("Torso", "7", a, *rep([("sc", 5), ("inc", 1)], 6), 42)
    a = c.rnd("Torso", "8-14", a, *flat(a), 42)

    # --- leg gusset join ------------------------------------------------
    if fixed:
        worked, skipped, seg = 18 + 18, 3 + 3, "18 / 18"
        stated15 = 48
    else:
        worked, skipped, seg = 12 + 14 + 6, 4 + 4, "12 / 14 / 6"
        stated15 = 44
    print(f"  -- R15 gusset join: torso sts worked {worked} ({seg}), "
          f"skipped {skipped}, of {a} available")
    if worked + skipped != a:
        c.fail("Torso", "15",
               f"torso stitches worked ({worked}) + skipped ({skipped}) = "
               f"{worked + skipped}, but round 14 produced {a} - "
               f"{a - worked - skipped} torso sts are unaccounted for")
    per_leg_skip = skipped // 2
    if per_leg_skip != leg_gusset:
        c.fail("Torso", "15",
               f"crotch mismatch: each leg leaves {leg_gusset} sts for the gusset but "
               f"the torso skips {per_leg_skip} sts per leg - "
               f"assembly step 1 sews {leg_gusset} sts to {per_leg_skip} sts")
    a = c.rnd("Torso", "15", None, worked + 2 * leg_into_body,
              worked + 2 * leg_into_body, stated15, foundation=True)
    a = c.rnd("Torso", "16-18", a, *flat(a), stated15)

    if fixed:
        a = c.rnd("Torso", "19", a, *rep([("sc", 6), ("dec", 1)], 6), 42)
        a = c.rnd("Torso", "20-21", a, *flat(a), 42)
        sock, gap, side = 6, 6, 12
    else:
        a = c.rnd("Torso", "19", a, *rep([("sc", 5), ("dec", 1)], 6), 38)
        a = c.rnd("Torso", "20-21", a, *flat(a), 38)
        sock, gap, side = 3, 12, 10

    # --- wing sockets ---------------------------------------------------
    s_consumed = side + sock + gap + sock + side
    s_made = side + sock + gap + sock + side
    a = c.rnd("Torso", "22", a, s_consumed, s_made, a,
              note=f"ch {sock} over {sock} skipped sts x2 = slots")
    a = c.rnd("Torso", "23", a, s_consumed, s_made, a, note="closes over the ch spaces")

    if fixed:
        a = c.rnd("Torso", "24", a, *rep([("sc", 5), ("dec", 1)], 6), 36)
        a = c.rnd("Torso", "25", a, *rep([("sc", 4), ("dec", 1)], 6), 30)
        a = c.rnd("Torso", "26", a, *rep([("sc", 3), ("dec", 1)], 6), 24)
        torso_top = c.rnd("Torso", "27", a, *rep([("sc", 1), ("dec", 1)], 8), 16)
    else:
        a = c.rnd("Torso", "24", a, *rep([("sc", 4), ("dec", 1)], 6), 32)
        a = c.rnd("Torso", "25", a, *rep([("sc", 2), ("dec", 1)], 8), 24)
        torso_top = c.rnd("Torso", "26", a, *rep([("sc", 1), ("dec", 1)], 8), 16)

    # ============================================================ 4. WING
    c.section("4. MECHANICAL WING PANELS  (make 2)")
    w = c.rnd("Wing", "1", None, 0, 17, 17, foundation=True, note="ch 18 -> 17 sc")
    w = c.rnd("Wing", "2", w, *cost(("sc", 15), ("dec", 1)), 16, note="FLO")
    w = c.rnd("Wing", "3", w, *cost(("dec", 1), ("sc", 12), ("dec", 1)), 14, note="BLO")
    if fixed:
        w = c.rnd("Wing", "4", w, *cost(("hdc", 13), ("inc", 1)), 15,
                  note="hdc, gives R5 a real post")
    else:
        w = c.rnd("Wing", "4", w, *cost(("sc", 12), ("inc", 1)), 15, note="FLO")
    w = c.rnd("Wing", "5", w, *(lambda cp: (cp[0] + 1, cp[1] + 1))(
        rep([("dc", 1), ("fpdc", 1)], 7)), 15, note="ch 2 not counted as a st")
    if not fixed:
        c.fail("Wing", "5",
               "fpdc is worked around the posts of row 4, which is a row of sc - "
               "sc posts are too short to take a front post dc, and row 4 is worked "
               "FLO which shortens them further")
    w = c.rnd("Wing", "6", w, *(lambda cp: (cp[0] + 10, cp[1] + 10))(
        rep([("picot", 1), ("sc", 1)], 5)), 15, note="+5 picots")
    w = c.rnd("Wing", "7", w, *rep([("sc", 3), ("dec", 1)], 3), 12)

    if fixed:
        w = c.rnd("Wing", "8", w, *cost(("dec", 1), ("sc", 8), ("dec", 1)), 10, note="tab")
        w = c.rnd("Wing", "9", w, *cost(("dec", 1), ("sc", 6), ("dec", 1)), 8, note="tab")
        w = c.rnd("Wing", "10", w, *cost(("dec", 1), ("sc", 4), ("dec", 1)), 6, note="tab")
        w = c.rnd("Wing", "11-13", w, *flat(w), 6, note="tab")
        tab_sts, tab_rows = 6, 3
    else:
        tab_sts, tab_rows = None, None

    # --- tab vs socket geometry -----------------------------------------
    socket_in = sock / STS_PER_IN
    print(f"\n  -- wing tab vs torso socket --")
    print(f"     socket slot is {sock} skipped sts wide = {socket_in:.2f} in")
    if tab_sts is None:
        edge_sts, edge_rows = 12, 7
        print(f"     the wing panel has no tab; its narrowest edge is row 7 "
              f"({edge_sts} sts = {edge_sts / STS_PER_IN:.2f} in) or the row-end edge "
              f"({edge_rows} rows = {edge_rows / RNDS_PER_IN:.2f} in)")
        c.fail("Wing", "assembly",
               f"assembly says to insert a 'lower wing tab' through the socket, but no "
               f"tab is ever created, and the panel's smallest edge "
               f"({edge_rows / RNDS_PER_IN:.2f} in) is "
               f"{(edge_rows / RNDS_PER_IN) / socket_in:.1f}x wider than the "
               f"{socket_in:.2f} in socket")
    else:
        tab_in = tab_sts / STS_PER_IN
        print(f"     tab is {tab_sts} sts x {tab_rows} rows = {tab_in:.2f} in wide "
              f"-> {'FITS' if abs(tab_in - socket_in) < 0.01 else 'MISMATCH'}")

    # ============================================================ 5. TAIL
    c.section("5. SEGMENTED CLOCKWORK TAIL")
    a = c.rnd("Tail", "1", None, 0, 4, 4, foundation=True)
    a = c.rnd("Tail", "2-4", a, *flat(a), 4)
    a = c.rnd("Tail", "5", a, *rep([("sc", 1), ("inc", 1)], 2), 6)
    a = c.rnd("Tail", "6-8", a, *flat(a), 6)
    a = c.rnd("Tail", "9", a, *rep([("sc", 2), ("inc", 1)], 2), 8)
    a = c.rnd("Tail", "10-12", a, *flat(a), 8)
    a = c.rnd("Tail", "13", a, *rep([("sc", 3), ("inc", 1)], 2), 10)
    a = c.rnd("Tail", "14-16", a, *flat(a), 10)
    a = c.rnd("Tail", "17", a, *rep([("sc", 4), ("inc", 1)], 2), 12)
    a = c.rnd("Tail", "18-20", a, *flat(a), 12)
    a = c.rnd("Tail", "21", a, *rep([("sc", 5), ("inc", 1)], 2), 14)
    if fixed:
        a = c.rnd("Tail", "22", a, *rep([("sc", 6), ("inc", 1)], 2), 16)
        tail_top = c.rnd("Tail", "23-25", a, *flat(a), 16)
    else:
        tail_top = c.rnd("Tail", "22-24", a, *flat(a), 16)

    # ======================================================= INTERFACES
    print(f"\n{'=' * 92}\n6. ASSEMBLY INTERFACES & GEOMETRY\n{'=' * 92}")
    ok = "MATCH" if neck_top == torso_top else "MISMATCH"
    print(f"  Neck opening {neck_top} sts  vs  Torso top {torso_top} sts  ->  {ok}")
    if neck_top != torso_top:
        c.fail("Assembly", "3",
               f"assembly claims both are 16 sts, but the head actually finishes on "
               f"{neck_top} sts because of the Round 15 error")
    print(f"  Leg gusset {leg_gusset} sts  vs  torso skip {per_leg_skip} sts  ->  "
          f"{'MATCH' if leg_gusset == per_leg_skip else 'MISMATCH'}")
    dia = lambda s: (s / STS_PER_IN) / math.pi  # noqa: E731
    print(f"\n  Head diameter   {dia(30):.2f} in ({dia(30) * 25.4:.0f} mm); "
          f"10 mm eye = {10 / (dia(30) * 25.4) * 100:.0f}% of it")
    print(f"  Torso diameter  {dia(max(44, stated15)):.2f} in, "
          f"height {(27 if fixed else 26) / RNDS_PER_IN:.2f} in")
    print(f"  Leg             {dia(24):.2f} in dia x {15 / RNDS_PER_IN:.2f} in long")
    print(f"  Wing panel      {17 / STS_PER_IN:.2f} x "
          f"{(13 if fixed else 7) / RNDS_PER_IN:.2f} in")
    print(f"  Tail length     {(25 if fixed else 24) / RNDS_PER_IN:.2f} in")

    print(f"\n{'#' * 92}")
    print(f"TOTAL DEFECTS: {len(c.defects)}")
    for piece, label, message in c.defects:
        print(f"  - {piece} {label}: {message}")
    return len(c.defects)


if __name__ == "__main__":
    use_fixed = "--fixed" in sys.argv
    print("CORRECTED PATTERN" if use_fixed else "PATTERN AS SUBMITTED")
    sys.exit(1 if run(use_fixed) else 0)
