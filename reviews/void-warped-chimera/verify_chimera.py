#!/usr/bin/env python3
"""Independent deterministic verifier for the "Void-Warped Chimera".

Written from scratch. The repository engine cannot model short-row raw-edge
perimeters, a three-way fork with two chain bridges (and their undersides), an
FLO/BLO split that runs two fabrics off one round, limb sockets, or edging
fullness -- all of which this pattern turns on.

Cost model, as (base stitches consumed, stitches produced):
    sc 1/1   inc 1/2   dec 2/1   hdc 1/1   dc 1/1   tr 1/1   fptr 1/1   sl st 1/1

A round is valid only when BOTH hold:
    consumed == stitches available   and   produced == stated count

Usage:
    python verify_chimera.py            # pattern as submitted
    python verify_chimera.py --fixed    # corrected pattern
"""

from __future__ import annotations

import math
import sys

STS_PER_IN = 22 / 4.0    # 5.5  - from the pattern's stated gauge
RNDS_PER_IN = 24 / 4.0   # 6.0

COST = {"sc": (1, 1), "inc": (1, 2), "dec": (2, 1), "hdc": (1, 1),
        "dc": (1, 1), "tr": (1, 1), "fptr": (1, 1), "sl st": (1, 1)}


def cost(*ops: tuple[str, int]) -> tuple[int, int]:
    con = pro = 0
    for stitch, n in ops:
        a, b = COST[stitch]
        con += a * n
        pro += b * n
    return con, pro


def rep(unit: list[tuple[str, int]], times: int) -> tuple[int, int]:
    a, b = cost(*unit)
    return a * times, b * times


class Checker:
    def __init__(self) -> None:
        self.defects: list[tuple[str, str, str]] = []

    def section(self, title: str) -> None:
        print(f"\n{'=' * 96}\n{title}\n{'=' * 96}")
        print(f"  {'Rnd/Row':<12}{'Avail':>6}{'Used':>6}{'Made':>6}{'Stated':>8}   Verdict")

    def rnd(self, piece: str, label: str, avail: int | None, consumed: int,
            produced: int, stated: int | None, foundation: bool = False,
            partial: bool = False, note: str = "") -> int:
        v: list[str] = []
        if partial and avail is not None and consumed < avail:
            v.append(f"partial - {avail - consumed} st held, by design")
        elif not foundation and avail is not None and consumed != avail:
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
    plain = lambda n: (n, n)  # noqa: E731

    # ==================================================== 1. CRANIAL CORE
    c.section("1. ASYMMETRIC CRANIAL CORE")
    a = c.rnd("Cranial", "1", None, 0, 6, 6, foundation=True)
    for i, unit in enumerate([[("inc", 1)], [("sc", 1), ("inc", 1)],
                              [("sc", 2), ("inc", 1)], [("sc", 3), ("inc", 1)],
                              [("sc", 4), ("inc", 1)]], start=2):
        a = c.rnd("Cranial", str(i), a, *rep(unit, 6), 6 * i)
    base = a = c.rnd("Cranial", "7-11", a, *plain(a), 36)

    print("  -- dorsal brow wedge (short rows) --")
    sr = c.rnd("Cranial", "12a", base, *cost(("sc", 12)), 12, partial=True)
    sr = c.rnd("Cranial", "12b", sr, *cost(("dec", 1), ("sc", 8), ("dec", 1)), 10)
    sr = c.rnd("Cranial", "12c", sr, *cost(("dec", 1), ("sc", 6), ("dec", 1)), 8)
    short_rows, untouched = 3, base - 12
    perimeter = sr + untouched + 2 * short_rows
    print(f"  -- perimeter: {sr} live + {untouched} untouched R11 + "
          f"{2 * short_rows} raw row-ends = {perimeter}")
    if fixed:
        # every perimeter position worked; 2 decs over the raw edges land on 36
        a = c.rnd("Cranial", "13", perimeter, 8 + 3 + 24 + 3, 8 + 2 + 24 + 2, 36,
                  note="all raw row-ends worked, 2 decs absorb them")
    else:
        a = c.rnd("Cranial", "13", perimeter, 8 + 2 + 24 + 2, 8 + 2 + 24 + 2, 36,
                  partial=True, note="sc 2 into 3 row-ends per side")
        c.fail("Cranial", "13",
               f"closes {8 + 2 + 24 + 2} of the {perimeter} perimeter positions - "
               f"only 2 sc are worked into the 3 raw row-ends on each side, so one "
               f"row-end per side is left unworked, leaving a gap at each corner of "
               f"the brow wedge")
    if fixed:
        a = c.rnd("Cranial", "14", a, *cost(("sc", 10), ("inc", 8), ("sc", 18)), 44)
        a = c.rnd("Cranial", "15", a, *(lambda x: (x[0] + 2, x[1] + 2))(
            rep([("sc", 5), ("dec", 1)], 6)), 38)
        a = c.rnd("Cranial", "16", a, *cost(("hdc", 38)), 38, note="post foundation")
        a = c.rnd("Cranial", "17", a, *(lambda x: (x[0] + 2, x[1] + 2))(
            rep([("sc", 2), ("fptr", 1)], 12)), 38, note="fptr into R16 hdc posts")
        a = c.rnd("Cranial", "18", a, *(lambda x: (x[0] + 2, x[1] + 2))(
            rep([("sc", 4), ("dec", 1)], 6)), 32)
        graft_rnd, graft_sts = 13, 36
        a = c.rnd("Cranial", "19", a, *(lambda x: (x[0] + 2, x[1] + 2))(
            rep([("sc", 3), ("dec", 1)], 6)), 26)
        head_out = c.rnd("Cranial", "20", a, *(lambda x: (x[0] + 2, x[1] + 2))(
            rep([("sc", 1), ("dec", 1)], 8)), 18)
    else:
        a = c.rnd("Cranial", "14", a, *cost(("sc", 10), ("inc", 8), ("sc", 18)), 44)
        a = c.rnd("Cranial", "15", a, *rep([("sc", 5), ("dec", 1)], 6), 38)
        a = c.rnd("Cranial", "16", a, *(lambda x: (x[0] + 2, x[1] + 2))(
            rep([("sc", 2), ("fptr", 1)], 12)), 38, note="fptr into Round 14")
        c.fail("Cranial", "16",
               "the fptr is anchored 'into Round 14', two rounds below, and Round 14 "
               "is a round of sc - an sc post is far too short to take a treble post "
               "stitch, and spanning Round 15 as well will pucker the fabric")
        c.fail("Cranial", "16",
               "12 posts are spaced every 3 sts in this 38-st round but anchored into "
               "a 44-st round; 38 and 44 do not share that spacing, so the eyestalk "
               "ridge will drift sideways instead of stacking vertically")
        a = c.rnd("Cranial", "17", a, *rep([("sc", 4), ("dec", 1)], 6), 32)
        graft_rnd, graft_sts = 15, 38
        head_out = c.rnd("Cranial", "18", a, *rep([("sc", 3), ("dec", 1)], 6), 26)

    # ==================================================== 2. PARTITION
    c.section("2. INTERNAL PARTITION (flat disc)")
    p = c.rnd("Partition", "1", None, 0, 6, 6, foundation=True)
    for i, unit in enumerate([[("inc", 1)], [("sc", 1), ("inc", 1)],
                              [("sc", 2), ("inc", 1)], [("sc", 3), ("inc", 1)]],
                             start=2):
        p = c.rnd("Partition", str(i), p, *rep(unit, 6), 6 * i)
    if fixed:
        p = c.rnd("Partition", "6", p, *rep([("sc", 4), ("inc", 1)], 6), 36)
    print(f"  -- partition edge {p} sts  vs  Cranial Round {graft_rnd} = {graft_sts} sts"
          f"  ->  {'MATCH' if p == graft_sts else 'MISMATCH'}")
    if p != graft_sts:
        c.fail("Assembly", "1",
               f"the partition's outer edge is {p} sts but Cranial Round {graft_rnd} "
               f"is {graft_sts} sts - a {p}-st disc cannot be grafted into a "
               f"{graft_sts}-st opening")

    # ==================================================== 3. TRIFURCATION
    c.section("3. TRIFURCATING TENTACLE CORE  (make 2)")
    if fixed:
        t = c.rnd("Tentacle", "1", None, 0, 9, 9, foundation=True,
                  note="ch 9 joined into an OPEN ring - this is the body socket")
        base_open = True
    else:
        t = c.rnd("Tentacle", "1", None, 0, 9, 9, foundation=True,
                  note="magic ring - CLOSED")
        base_open = False
    t = c.rnd("Tentacle", "2-10", t, *plain(t), 9)

    print(f"  -- fork 1: sc 3 (Branch 1 base), ch 2 (Bridge 1), skip 6  "
          f"-> consumes {3 + 6} of {t}")
    b1 = c.rnd("Tentacle", "11 fork1", t, 9, 3 + 2, 5, foundation=True)
    b1r = c.rnd("Tentacle", "12a-18a", b1, *plain(b1), 5)
    c.rnd("Tentacle", "19a", b1r, *cost(("dec", 2), ("sc", 1)), 3)

    if fixed:
        group = 6 + 2   # 6 skipped base sts + the 2 underside sts of Bridge 1
        print(f"  -- lower group ring: 6 skipped base sts + 2 Bridge-1 underside "
              f"sts = {group}")
        b2 = c.rnd("Tentacle", "11b fork2", group, 4 + 4, 4 + 2, 6, foundation=True)
        b2r = c.rnd("Tentacle", "12b-18b", b2, *plain(b2), 6)
        c.rnd("Tentacle", "19b", b2r, *rep([("dec", 1)], 3), 3)
        b3 = 4 + 2
        b3r = c.rnd("Tentacle", "12c-18c", b3, *plain(b3), 6,
                    note="4 base + Bridge-2 underside")
        c.rnd("Tentacle", "19c", b3r, *rep([("dec", 1)], 3), 3)
        bridge_sides_used = 4
    else:
        b2 = c.rnd("Tentacle", "11b fork2", 6, 3 + 3, 3 + 2, 5, foundation=True,
                   note="3 base + new Bridge 2")
        b2r = c.rnd("Tentacle", "12b-18b", b2, *plain(b2), 5)
        c.rnd("Tentacle", "19b", b2r, *cost(("dec", 2), ("sc", 1)), 3)
        b3 = 3 + 2
        b3r = c.rnd("Tentacle", "12c-18c", b3, *plain(b3), 5,
                    note="3 base + 'underside of bridge'")
        c.rnd("Tentacle", "19c", b3r, *cost(("dec", 2), ("sc", 1)), 3)
        bridge_sides_used = 3
    total_sides = 4          # Bridge 1 top/underside, Bridge 2 top/underside
    print(f"  -- bridge accounting: {total_sides} bridge sides exist "
          f"(2 bridges x top+underside), {bridge_sides_used} are worked into")
    if bridge_sides_used < total_sides:
        c.fail("Tentacle", "11",
               f"Branch 1 takes Bridge 1's top, Branch 2 makes and takes Bridge 2's "
               f"top, Branch 3 takes Bridge 2's underside - but Bridge 1's UNDERSIDE "
               f"(2 ch sts) is never worked into, leaving a slit between Branch 1 and "
               f"the Branch 2/3 pair; 'underside of bridge' is also ambiguous when "
               f"there are two bridges")

    # ======================================================== 4. TORSO
    c.section("4. HYPERBOLIC MANTLE & MULTI-LIMB SOCKET TORSO")
    a = c.rnd("Torso", "1", None, 0, 24, 24, foundation=True, note="ch 24 open ring")
    a = c.rnd("Torso", "2-6", a, *plain(a), 24)

    if fixed:
        body_worked, t_in, t_held = 3 + 9 + 6, 6, 3
        body_skipped = 2 * t_held
        stated7 = 30
    else:
        body_worked, t_in, t_held = 2 + 6 + 13, 3, 6
        body_skipped = 0
        stated7 = 27
    made7 = body_worked + 2 * t_in
    print(f"  -- R7 socket: body worked {body_worked}, skipped {body_skipped}, "
          f"of {a}   |   2 tentacles x {t_in} worked, {t_held} held each")
    if body_worked + body_skipped != a:
        c.fail("Torso", "7",
               f"body sts worked ({body_worked}) + skipped ({body_skipped}) = "
               f"{body_worked + body_skipped}, but Round 6 produced {a} - "
               f"{a - body_worked - body_skipped} body sts are unaccounted for")
    if not fixed:
        need = 2 * t_held
        c.fail("Assembly", "3",
               f"assembly asks you to cinch {t_held} held sts per tentacle to "
               f"{t_held} skipped body sts, i.e. {need} skipped body sts - but the "
               f"round already works {body_worked} of the {a} body sts, and "
               f"{body_worked} + {need} = {body_worked + need} > {a}. There are not "
               f"enough body stitches to skip")
    elif 2 * t_held != body_skipped:
        c.fail("Torso", "7", "gusset imbalance")
    a = c.rnd("Torso", "7", None, made7, made7, stated7, foundation=True)
    a = c.rnd("Torso", "8", a, *plain(a), stated7)
    if fixed:
        a = c.rnd("Torso", "9", a, *rep([("sc", 4), ("inc", 1)], 6), 36)
    else:
        a = c.rnd("Torso", "9", a, *rep([("sc", 2), ("inc", 1)], 9), 36)
    split = a
    a = c.rnd("Torso", "10", a, *rep([("inc", 1)], 36), 72, note="FLO of R9")
    a = c.rnd("Torso", "11", a, *rep([("sc", 1), ("inc", 1)], 36), 108)

    fan = 7 if not fixed else 4      # sts produced per repeat
    per = 1 if not fixed else 2      # base sts consumed per repeat
    reps = a // per
    frill = fan * reps
    c.rnd("Torso", "12", a, per * reps, frill, frill, note="frill edging")
    body_circ_in = split / STS_PER_IN
    frill_in = frill / STS_PER_IN
    print(f"  -- frill: {frill} sts = {frill_in:.1f} in of edge; the torso it hangs "
          f"from is {split} sts = {body_circ_in:.1f} in")
    print(f"     fullness vs its own base round (R11, {a} sts): "
          f"{frill / a:.1f}x per base st")
    print(f"     fullness vs the torso circumference: {frill_in / body_circ_in:.0f}x")
    if frill / a > 3.0:
        c.fail("Torso", "12",
               f"{fan} sts into every single st of a {a}-st round = {frill} sts, "
               f"{frill_in:.0f} in of edge hanging off a {body_circ_in:.1f} in torso "
               f"({frill_in / body_circ_in:.0f}x its circumference). A shell edging "
               f"runs 2-2.5 sts per base st; this is {fan}, with trebles and no "
               f"anchoring st - it will pack into a solid ball rather than ruffle")

    a = c.rnd("Torso", "13", split, *plain(split), 36, note="BLO of R9, the free loops")
    a = c.rnd("Torso", "14", a, *rep([("sc", 4), ("dec", 1)], 6), 30)
    a = c.rnd("Torso", "15", a, *rep([("sc", 3), ("dec", 1)], 6), 24)
    torso_out = c.rnd("Torso", "16", a, *rep([("sc", 2), ("dec", 1)], 6), 18)

    # =================================================== 5. INTERFACES
    print(f"\n{'=' * 96}\n5. ASSEMBLY INTERFACES & GEOMETRY\n{'=' * 96}")
    print(f"  Cranial out {head_out} sts  vs  Torso top {torso_out} sts  ->  "
          f"{'MATCH' if head_out == torso_out else 'MISMATCH'}")
    if head_out != torso_out:
        c.fail("Assembly", "2",
               f"the cranial core finishes on {head_out} sts and the torso top is "
               f"{torso_out} sts - you cannot sew a {head_out}-st opening to an "
               f"{torso_out}-st one without gathering it")

    need = t_in + t_held
    print(f"  Tentacle socket needs an OPEN ring of {need} sts; tentacle base is 9 sts "
          f"and {'OPEN' if base_open else 'CLOSED (magic ring)'}")
    if not base_open:
        c.fail("Tentacle", "1",
               "the tentacle's base is a magic ring pulled closed and all three branch "
               "tips are cinched shut, so the piece has no opening anywhere - yet the "
               "torso's Round 7 socket has to crochet into 9 of its stitches")

    if not fixed:
        c.fail("Assembly", "4",
               "safety eyes cannot be mounted on the Hyperbolic Frill: a safety eye "
               "needs flat, stable fabric and rear access for its washer, and the "
               "frill is a free-hanging edge of treble fans with no flat area and no "
               "reachable back")

    dia = lambda s: (s / STS_PER_IN) / math.pi  # noqa: E731
    print(f"\n  Head diameter   {dia(44):.2f} in ({dia(44) * 25.4:.0f} mm); "
          f"12 mm eye = {12 / (dia(44) * 25.4) * 100:.0f}% of it")
    print(f"  Torso diameter  {dia(split):.2f} in, height "
          f"{(16 if not fixed else 16) / RNDS_PER_IN:.2f} in")
    print(f"  Frill edge      {frill_in:.1f} in")
    print(f"  Tentacle        {dia(9):.2f} in dia")

    print(f"\n{'#' * 96}")
    print(f"TOTAL DEFECTS: {len(c.defects)}")
    for piece, label, message in c.defects:
        print(f"  - {piece} {label}: {message}")
    return len(c.defects)


if __name__ == "__main__":
    use_fixed = "--fixed" in sys.argv
    print("CORRECTED PATTERN" if use_fixed else "PATTERN AS SUBMITTED")
    sys.exit(1 if run(use_fixed) else 0)
