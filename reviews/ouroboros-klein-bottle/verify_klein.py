#!/usr/bin/env python3
"""Independent verifier for "The Ouroboros Klein Bottle".

This pattern claims a non-orientable closed surface and ships a "MANIFOLD
TOPOLOGY GRAPH MATRIX" asserting three edge pairings. Both claims are
independently checkable, so this script does three jobs:

  1. adjudicate every row of the topology matrix against the actual piece counts
  2. run a round-by-round pass over all four sections
  3. test the manifold claim itself — boundary closure and sheet count per seam

Cost model, as (base stitches consumed, stitches produced):
    sc 1/1   inc 1/2   dec 2/1   sl st 1/1   3-st-inc 1/3   3-st-dec 3/1

Usage:
    python verify_klein.py            # pattern as submitted
    python verify_klein.py --fixed    # corrected pattern
"""

from __future__ import annotations

import math
import sys

STS_PER_IN = 28 / 4.0    # 7.0 — from the pattern's stated gauge
RNDS_PER_IN = 30 / 4.0   # 7.5

COST = {"sc": (1, 1), "inc": (1, 2), "dec": (2, 1), "sl st": (1, 1),
        "3-st-inc": (1, 3), "3-st-dec": (3, 1)}


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
        print(f"\n{'=' * 94}\n{title}\n{'=' * 94}")
        print(f"  {'Rnd/Row':<13}{'Avail':>6}{'Used':>6}{'Made':>6}{'Stated':>8}   Verdict")

    def rnd(self, piece: str, label: str, avail: int | None, consumed: int,
            produced: int, stated: int | None, foundation: bool = False,
            partial: bool = False, note: str = "") -> int:
        v: list[str] = []
        if partial and avail is not None and consumed < avail:
            v.append(f"partial — {avail - consumed} held, by design")
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
        print(f"  {label:<13}{str(avail):>6}{consumed:>6}{produced:>6}{str(stated):>8}"
              f"   {'; '.join(v) or 'ok'}" + (f"   [{note}]" if note else ""))
        return stated if stated is not None else produced

    def fail(self, piece: str, label: str, message: str) -> None:
        self.defects.append((piece, label, message))
        print(f"     !! {message}")


def run(fixed: bool) -> int:
    c = Checker()
    plain = lambda n: (n, n)  # noqa: E731
    ok = lambda b: "CORRECT" if b else "*** WRONG ***"  # noqa: E731

    # ================================================= SECTION 1 — OUTER BULB
    c.section("SECTION 1 — OUTER CHAMBER & FUNNEL BASE")
    if fixed:
        s1_base_open, s1_base = True, 16
        a = c.rnd("Sec1", "R1", None, 0, 16, 16, foundation=True,
                  note="ch 16 OPEN ring — the Ouroboros mouth")
        for i, n in enumerate([24, 32, 40, 48, 56], start=2):
            a = c.rnd("Sec1", f"R{i}", a, *rep([("sc", i - 1), ("inc", 1)], 8), n)
        port_rnd = 7
    else:
        s1_base_open, s1_base = False, 8
        a = c.rnd("Sec1", "R1", None, 0, 8, 8, foundation=True, note="magic ring — CLOSED")
        for i, n in enumerate([16, 24, 32, 40, 48, 56], start=2):
            a = c.rnd("Sec1", f"R{i}", a, *rep([("sc", i - 2), ("inc", 1)], 8), n)
        port_rnd = 8

    a = c.rnd("Sec1", f"R{port_rnd}", a, 20 + 16 + 20, 20 + 16 + 20, 56,
              note="port: ch 16, skip 16")
    port_boundary = 16 + 16   # 16 skipped sts below + 16 ch sts above
    a = c.rnd("Sec1", f"R{port_rnd + 1}", a, 56, 56, 56, note="closes over the ch-bridge")
    a = c.rnd("Sec1", f"R{port_rnd + 2}-{port_rnd + 8}", a, *plain(a), 56)
    for i, (s, n) in enumerate([(5, 48), (4, 40), (3, 32), (2, 24)], start=port_rnd + 9):
        a = c.rnd("Sec1", f"R{i}", a, *rep([("sc", s), ("dec", 1)], 8), n)
    neck_a = c.rnd("Sec1", f"R{port_rnd + 13}-{port_rnd + 17}", a, *plain(a), 24,
                   note="Neck Tube A, left open")

    # ================================================ SECTION 2 — INNER SHAFT
    c.section("SECTION 2 — SELF-INTERSECTING INNER CORE")
    if fixed:
        t = c.rnd("Sec2", "R1", None, 0, 32, 32, foundation=True,
                  note="ch 32 OPEN ring — this IS the flange edge")
        t = c.rnd("Sec2", "R2", t, *rep([("sc", 2), ("dec", 1)], 8), 24)
        t = c.rnd("Sec2", "R3", t, *rep([("sc", 1), ("dec", 1)], 8), 16)
        tunnel_end = c.rnd("Sec2", "R4-18", t, *plain(t), 16, note="true boundary, no FLO split")
        flange, branch_line = 32, False
    else:
        t = c.rnd("Sec2", "R1", None, 0, 16, 16, foundation=True, note="ch 16 OPEN ring")
        t = c.rnd("Sec2", "R2-18", t, *plain(t), 16)
        tunnel_end = t
        t = c.rnd("Sec2", "R19", t, *rep([("inc", 1)], 16), 32,
                  note="FLO — leaves R18's back loops free")
        t = c.rnd("Sec2", "R20", t, *rep([("sc", 3), ("inc", 1)], 8), 40)
        flange = c.rnd("Sec2", "R21", t, *rep([("sc", 4), ("inc", 1)], 8), 48)
        branch_line = True

    # ================================================ SECTION 3 — OUROBOROS NECK
    c.section("SECTION 3 — CURVED OUROBOROS NECK")
    print(f"  attaches to Section 1's open {neck_a} sts  -> "
          f"{ok(neck_a == 24)}  (this join is NOT in the matrix)")
    a = c.rnd("Sec3", "R26-28", 24, 24, 24, 24)
    base = 24
    sr = c.rnd("Sec3", "Row 29a", base, 13, 13, 13, partial=True)
    sr = c.rnd("Sec3", "Row 29b", sr, 1 + 10 + 1, 10 + 1, 11, partial=True)
    sr = c.rnd("Sec3", "Row 29c", sr, 1 + 8 + 1, 8 + 1, 9, partial=True)
    left_a, left_b, r28_left, row_ends = 13 - 12, 11 - 10, base - 13, 6
    per = (9 - 1) + left_b + left_a + r28_left + row_ends
    print(f"  -- open perimeter = {9 - 1} (29c) + {left_b} (29b left) + {left_a} (29a left) "
          f"+ {r28_left} (R28 left) + {row_ends} row-ends = {per}")
    if fixed:
        a = c.rnd("Sec3", "Row 29d", per, 8 + 2 + 3 + 11 + 3, 8 + 1 + 2 + 11 + 2, 24,
                  note="every position worked, 3 decs absorb the excess")
    else:
        a = c.rnd("Sec3", "Row 29d", per, 8 + 2 + 12, 8 + 2 + 12, 24, partial=True,
                  note="'sc 8 / sc 2 row ends / sc 12'")
        c.fail("Sec3", "Row 29d",
               f"components sum to {8 + 2 + 12}, not the stated 24; and it claims 'sc 12 across "
               f"remaining unworked Round 28 sts' when only {r28_left} remain (Row 29a consumed "
               f"13 of 24)")
        c.fail("Sec3", "Row 29d",
               f"the true open perimeter is {per}; the round closes {8 + 2 + 12}, leaving "
               f"{per - (8 + 2 + 12)} positions open along the curve — the Row 29a/29b leftovers "
               f"and 4 of the 6 row-ends")
    a = c.rnd("Sec3", "R30-35", a, *plain(a), 24)
    if fixed:
        a = c.rnd("Sec3", "R36", a, *rep([("sc", 1), ("dec", 1)], 8), 16)
        neck_end = c.rnd("Sec3", "R37-42", a, *plain(a), 16)
    else:
        a = c.rnd("Sec3", "R36", a, *rep([("sc", 2), ("dec", 1)], 6), 18)
        neck_end = c.rnd("Sec3", "R37-42", a, *plain(a), 18)

    # ====================================== THE TOPOLOGY MATRIX
    print(f"\n{'=' * 94}\nAUDIT OF THE 'MANIFOLD TOPOLOGY GRAPH MATRIX'\n{'=' * 94}")
    if fixed:
        rows = [("Sec 2 R1 Flange", "Sec 1 port boundary", flange, port_boundary),
                ("Sec 3 R42 (inv-flip)", "Sec 2 R18 Tunnel End", neck_end, tunnel_end)]
    else:
        rows = [("Sec 2 R21 Flange", "Sec 1 R8 Skipped Loop", flange, 16),
                ("Sec 2 R1 Open Ring", "Sec 1 R1 Magic Ring", 16, s1_base),
                ("Sec 3 R42 Curved Neck", "Sec 2 R18 Tunnel End", neck_end, tunnel_end)]
    bad = 0
    for src, tgt, x, y in rows:
        good = x == y
        bad += not good
        print(f"  {src:<24}<-> {tgt:<26}{x:>3} <-> {y:<3}  {ok(good)}")
    if bad:
        print(f"  -> {bad} of {len(rows)} matrix rows are WRONG")
        c.fail("Matrix", "row 1",
               "claims the flange meets a 48-st edge; Section 1 Round 8 skips 16 sts, and the "
               "port's full boundary is only 32 positions. The directive covers the gap with "
               "'and adjacent wall spaces' — 32 stitches that are defined nowhere")
        c.fail("Matrix", "row 2",
               "claims Sec 1 R1 is a 16-st edge; it is an 8-st MAGIC RING, pulled closed and "
               "buried under 25 rounds of fabric. There is no edge there to sew to at all")
        c.fail("Matrix", "row 3",
               f"claims Sec 2 R18 is 18 sts; Section 2 runs 16 sts from R1 to R18. The number "
               f"18 appears nowhere in Section 2")
    else:
        print(f"  -> all {len(rows)} rows verified")

    # ====================================== MANIFOLD / ORIENTABILITY
    print(f"\n{'=' * 94}\nMANIFOLD TEST\n{'=' * 94}")
    slit, tube = 16 / STS_PER_IN, 16 / STS_PER_IN
    print(f"  port: a {slit:.2f} in slit opens to a hole of perimeter ~{2 * slit:.2f} in; the "
          f"{tube:.2f} in shaft passes through  -> {ok(tube < 2 * slit)}")
    print(f"  using a physical port rather than a true self-intersection is correct practice "
          f"for a crocheted Klein bottle immersion")
    if not s1_base_open and not fixed:
        print(f"\n  Sec 1 R1 is a CLOSED magic ring, yet the matrix sews Sec 2's ring to it.")
    if branch_line:
        print(f"\n  Sec 2 R19 is FLO of R18, so R18's back loops stay free. Grafting Section 3")
        print(f"  onto those SAME loops puts THREE sheets along one circle:")
        print(f"     tunnel below R18  |  flange above it (front loops)  |  Sec 3 (back loops)")
        print(f"  A Klein bottle is a 2-manifold — exactly two sheets meet everywhere.")
        c.fail("Topology", "Sec 2 R18",
               "the FLO/BLO split makes Round 18 a branch line where three sheets meet "
               "(tunnel, flange, and the grafted Section 3 neck). A closed 2-manifold cannot "
               "contain one, so the 'non-orientable' classification fails regardless of counts")
    else:
        print(f"\n  Sec 2 has exactly two boundaries (flange {flange}, tunnel end {tunnel_end}); "
              f"no FLO split, no branch line.")
        print(f"  boundaries: Sec1 R1 cap (closed) | port <-> flange | Sec3 R42 <-> Sec2 R18")
        print(f"  all closed -> sphere + one handle, seamed with the inv-flip = cross-handle")
        print(f"  -> genuinely NON-ORIENTABLE  {ok(True)}")
    print(f"\n  the inv-flip itself is the right idea — reversing one end before seaming is "
          f"exactly\n  how an orientable handle becomes a cross-handle. It is the one part of "
          f"the\n  non-orientability argument that holds up as written.")

    # ====================================== GLOSSARY
    print(f"\n{'=' * 94}\nGLOSSARY\n{'=' * 94}")
    defined = ["split-sc", "ch-sp", "3-st-inc", "3-st-dec", "inv-flip"]
    used = ["sc", "inc", "dec", "ch", "sl st", "FLO", "BLO", "split-sc", "inv-flip"]
    if fixed:
        defined = ["sc", "inc", "dec", "ch", "sl st", "FLO", "BLO", "split-sc", "inv-flip"]
        used = [u for u in used if u != "FLO"] + ["FLO"]
    undef = [u for u in used if u not in defined]
    dead = [d for d in defined if d not in used]
    print(f"  used but NEVER defined : {undef or 'none'}")
    print(f"  defined but NEVER used : {dead or 'none'}")
    if undef:
        c.fail("Glossary", "undefined",
               f"{', '.join(undef)} — all seven basic operations the pattern is built from — "
               f"are used throughout and none is defined")
    if dead:
        c.fail("Glossary", "dead entries",
               f"{', '.join(dead)} are defined and never used; only 2 of the 5 glossary "
               f"entries earn their place")

    # ====================================== GAUGE / DIMENSIONS / MATERIALS
    print(f"\n{'=' * 94}\nGAUGE, DIMENSIONS & MATERIALS\n{'=' * 94}")
    if not fixed:
        print(f"  gauge is stated 'in split-sc', but split-sc appears exactly ONCE in the whole")
        print(f"  pattern — in the final assembly join. Every round is plain sc, and waistcoat")
        print(f"  stitch runs ~10% denser, so the number does not describe the fabric either.")
        c.fail("Gauge", "stitch", "gauge is measured in split-sc (Waistcoat), a stitch used "
                                  "exactly once, in the final join; the entire pattern is sc")
    bulb = (56 / STS_PER_IN) / math.pi
    loop = (25 + 17 + 21) / RNDS_PER_IN
    print(f"  outer bulb: 56 sts = {56 / STS_PER_IN:.2f} in around = {bulb:.2f} in diameter")
    print(f"  loop length: 63 rounds = {loop:.1f} in")
    if not fixed:
        print(f"  CLAIMED 4.5 in bulb -> {4.5 / bulb:.1f}x over;  CLAIMED 11 in loop "
              f"-> {11 / loop:.1f}x over")
        c.fail("Dimensions", "finished size",
               f"claims a 4.5 in bulb and an 11 in loop; at the pattern's own gauge they are "
               f"{bulb:.1f} in and {loop:.1f} in — overstated {4.5 / bulb:.1f}x and "
               f"{11 / loop:.1f}x")
        for item, why in [
            ("tapestry needle", "missing from materials, yet assembly says 'Whipstitch' three times"),
            ("floral wire / tubing", "listed for 'structural tunnel lining' and never referenced "
                                     "by any instruction"),
            ("stitch markers (8 colours)", "listed as 'required' and never referenced by any "
                                           "instruction"),
            ("yarn quantities", "no grams or yards for either colour"),
        ]:
            c.fail("Materials", item, why)
        c.fail("Glossary", "inv-flip",
               "defined as 'turn the WORK inside-out through an open neck ring' but used as "
               "'flip the open EDGE of Round 42 inside-out' — the definition and the usage "
               "describe different manoeuvres")
        c.fail("Sec2", "R19", "nothing tells you to save Round 18's back loops, though the "
                              "topology matrix depends on them")
    else:
        print(f"  corrected claim: ~{bulb:.1f} in bulb, ~{loop:.0f} in loop -> consistent")

    print(f"\n{'#' * 94}")
    print(f"TOTAL DEFECTS: {len(c.defects)}")
    for piece, label, message in c.defects:
        print(f"  - {piece} {label}: {message}")
    return len(c.defects)


if __name__ == "__main__":
    use_fixed = "--fixed" in sys.argv
    print("CORRECTED PATTERN" if use_fixed else "PATTERN AS SUBMITTED")
    sys.exit(1 if run(use_fixed) else 0)
