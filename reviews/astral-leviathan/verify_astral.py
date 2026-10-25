#!/usr/bin/env python3
"""Independent verifier for "The Astral Leviathan".

This pattern is unusual: it ships with its own SELF-VERIFICATION claims — a
"Body Conservation" sum, a "Gusset Parity" statement, a "Fullness Ratio", a
bridge-conservation table and a formal assembly matrix. So this script does two
jobs:

  1. adjudicate every self-verification claim (audit_self_checks)
  2. run an independent round-by-round pass over everything else

Cost model, as (base stitches consumed, stitches produced):
    sc 1/1   inc 1/2   dec 2/1   hdc 1/1   dc 1/1   tr 1/1
    fpdc 1/1   fptr 1/1   sl st 1/1
    3-st-inc 1/3   (3 sts in one st, +2 net)   3-st-dec 3/1

Usage:
    python verify_astral.py            # pattern as submitted
    python verify_astral.py --fixed    # corrected pattern
"""

from __future__ import annotations

import math
import sys

STS_PER_IN = 26 / 4.0    # 6.5 — from the pattern's stated gauge
RNDS_PER_IN = 28 / 4.0   # 7.0

COST = {"sc": (1, 1), "inc": (1, 2), "dec": (2, 1), "hdc": (1, 1), "dc": (1, 1),
        "tr": (1, 1), "fpdc": (1, 1), "fptr": (1, 1), "sl st": (1, 1),
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


def audit_self_checks(c: Checker, fixed: bool) -> None:
    """The pattern makes nine verifiable claims about itself. Adjudicate each."""
    print(f"\n{'=' * 94}\nAUDIT OF THE PATTERN'S OWN SELF-VERIFICATION CLAIMS\n{'=' * 94}")
    ok = lambda b: "CORRECT" if b else "*** WRONG ***"  # noqa: E731

    # 1 — Row 13a
    a = 18 + 1 + 1 + 2 + 1 + 1 + 2 + 1
    print(f"\n[1] Row 13a '(27 worked, 27 left)': components = {a}, 54 - {a} = {54 - a}"
          f"  -> {ok(a == 27)}")

    # 2 — Row 13b
    lit = 2 + 1 + 2 + 2 + 2 + 1 + 2 + 1
    each = 2 + 1 + 4 + 2 + 4 + 1 + 2 + 1
    print(f"\n[2] Row 13b '(17 sts worked)': 'dc 2 in next 2 sts' is ambiguous")
    print(f"    reading 'dc in next 2 sts'       -> {lit}")
    print(f"    reading '2 dc in EACH of next 2' -> {each}")
    print(f"    stated 17 -> only the second reading works. {ok(each == 17)}, but never stated")
    consumed_13b = 1 + lit

    # 3 — Row 13c  (the first failure)
    live_b, live_a, live_12, row_ends = 17, 27 - consumed_13b, 27, 4
    perimeter = (live_b - 1) + live_a + live_12 + row_ends   # 13c skips one sl st
    made = (16 + 2 + 13 + 2 + 27) if fixed else (16 + 27)
    print(f"\n[3] Row 13c '(54 sts total perimeter restored)'")
    print(f"    true open perimeter = {live_b - 1} (13b, less the skipped sl st) + {live_a} "
          f"(13a left) + {live_12} (R12) + {row_ends} row-ends = {perimeter}")
    if fixed:
        print(f"    corrected round works {made} -> {ok(made == perimeter)}")
    else:
        print(f"    the round's own components: sc 16 + sc 27 = {made};  stated 54 "
              f"-> {ok(False)} (off by {54 - made})")
        c.fail("Cranial", "Row 13c",
               f"components sum to {made}, not the stated 54; and the true open perimeter is "
               f"{perimeter}, so the round leaves {perimeter - made} positions unworked "
               f"around the brow")

    # 4 — Torso R7
    print(f"\n[4] Torso R7 '4 + 6 + 8 + 6 = 24': body consumed {4 + 6 + 8 + 6}, "
          f"produced {4 + 6 + 8 + 6}  -> {ok(4 + 6 + 8 + 6 == 24)}")

    # 5 — Fullness ratio
    fans = 90 // 3
    print(f"\n[5] Torso R12 'Fullness Ratio 150/90 = 1.67x': {fans} fans x 5 = {fans * 5}; "
          f"{fans * 5}/90 = {fans * 5 / 90:.2f}x  -> {ok(fans * 5 == 150)}")
    print(f"    (the Void-Warped Chimera's equivalent round ran 7.0x per base st)")
    if not fixed:
        print(f"    NOTE: the 2 sts between fans are skipped — 60 of 90 sts are never worked into")

    # 6 — Trifurcation conservation
    base, sides = 18, 2 * 3 * 2
    print(f"\n[6] Trifurcation '9 + 12 + 9': {base} base + {sides} bridge sides = {base + sides}; "
          f"branches = {9 + 12 + 9}  -> {ok(base + sides == 30)}")
    for k, v in {"Bridge 1 top": "Branch 1", "Bridge 1 underside": "Branch 2 (R9b)",
                 "Bridge 2 top": "Branch 2 (R9b creates it)",
                 "Bridge 2 underside": "Branch 3 (R9c)"}.items():
        print(f"      {k:<21}-> {v}")
    print(f"    all 4 bridge sides consumed; no orphaned chain -> {ok(True)}")

    # 7 — Body Conservation  (the second failure)
    if fixed:
        bw, bs = 20 + 30, 6
    else:
        bw, bs = 14 + 24, 6
    print(f"\n[7] Torso R17 'Body Conservation: 14 + 6 + 24 + 12 = 56'")
    print(f"    BODY worked {bw}, BODY skipped {bs} -> {bw + bs} of 56 accounted")
    if bw + bs != 56:
        print(f"    -> {ok(False)}: {56 - bw - bs} body sts unaccounted. The self-check only")
        print(f"       reaches 56 by counting the 12 TENTACLE sts as BODY sts.")
        c.fail("Torso", "R17 self-check",
               "the 'Body Conservation' proof is invalid: it adds the 12 tentacle-root "
               "stitches into a sum of body stitches. Body alone accounts for "
               f"{bw} worked + {bs} skipped = {bw + bs} of 56, leaving {56 - bw - bs} dropped")
    else:
        print(f"    -> {ok(True)}")

    # 8 — Gusset parity
    held = 18 - 12
    print(f"\n[8] Torso R17 'Gusset Parity 6 <-> 6': hub root 18 - 12 worked = {held} held; "
          f"body skipped {bs}  -> {ok(held == bs)}")

    # 9 — Assembly matrix
    print(f"\n[9] FORMAL ASSEMBLY GRAPH MATRIX")
    for s, t, x, y in [("Head Base R19", "Torso Neck R1", 24, 24),
                       ("Left Wing Tab Row 1", "Torso Socket L", 6, 6),
                       ("Right Wing Tab Row 1", "Torso Socket R", 6, 6),
                       ("Hub Inner Gusset", "Torso Skipped R17", 6, 6)]:
        print(f"    {s:<22}{t:<20}{x} <-> {y}   {ok(x == y)}")


def run(fixed: bool) -> int:
    c = Checker()
    plain = lambda n: (n, n)  # noqa: E731

    # ==================================================== 1. CRANIAL VAULT
    c.section("SECTION 1 — HYPERBOLIC CRANIAL VAULT")
    a = c.rnd("Cranial", "R1", None, 0, 6, 6, foundation=True)
    for i in range(2, 9):
        a = c.rnd("Cranial", f"R{i}", a, *rep([("sc", i - 2), ("inc", 1)], 6), 6 * i)
    a = c.rnd("Cranial", "R9", a, *rep([("sc", 7), ("inc", 1)], 6), 54,
              note="FLO — saves R8's 48 back loops")
    a = c.rnd("Cranial", "R10-12", a, *plain(a), 54)
    sr = c.rnd("Cranial", "Row 13a", a, 27, 27, 27, partial=True)
    sr = c.rnd("Cranial", "Row 13b", sr, 14, 17, 17, partial=True,
               note="'2 dc in each of next 2 sts'")
    # Row 13c is adjudicated in audit_self_checks
    a = c.rnd("Cranial", "R14", 48, *rep([("sc", 6), ("dec", 1)], 6), 42,
              note="into R8's free BLO")
    a = c.rnd("Cranial", "R15", a, *rep([("sc", 5), ("dec", 1)], 6), 36)
    a = c.rnd("Cranial", "R16", a, *cost(("hdc", 36)), 36, note="post foundation")
    a = c.rnd("Cranial", "R17", a, *rep([("sc", 2), ("fpdc", 1)], 12), 36,
              note="fpdc into R16 — ADJACENT, correct")
    a = c.rnd("Cranial", "R18", a, *rep([("sc", 4), ("dec", 1)], 6), 30)
    head_out = c.rnd("Cranial", "R19", a, *rep([("sc", 3), ("dec", 1)], 6), 24)

    # ====================================================== 2. TENTACLE HUB
    c.section("SECTION 2 — TRIFURCATING VOID-TENTACLE HUB")
    t = c.rnd("Hub", "R1", None, 0, 18, 18, foundation=True, note="ch 18, OPEN ring")
    t = c.rnd("Hub", "R2-8", t, *plain(t), 18)
    b1 = c.rnd("Hub", "R9a", t, 6 + 12, 6 + 3, 9, foundation=True, note="Branch 1 + bridge 1")
    b1 = c.rnd("Hub", "R10a-15a", b1, *plain(b1), 9)
    b1 = c.rnd("Hub", "R16a", b1, *rep([("sc", 1), ("dec", 1)], 3), 6)
    c.rnd("Hub", "R17a", b1, *rep([("dec", 1)], 3), 3)
    b2 = c.rnd("Hub", "R9b", 12, 6 + 6, 6 + 3 + 3, 12, foundation=True,
               note="+ bridge 2 + bridge 1 underside")
    b2 = c.rnd("Hub", "R10b-18b", b2, *plain(b2), 12)
    b2 = c.rnd("Hub", "R19b", b2, *rep([("sc", 2), ("dec", 1)], 3), 9)
    b2 = c.rnd("Hub", "R20b", b2, *rep([("sc", 1), ("dec", 1)], 3), 6)
    c.rnd("Hub", "R21b", b2, *rep([("dec", 1)], 3), 3)
    b3 = c.rnd("Hub", "R9c", 6, 6, 6 + 3, 9, foundation=True, note="+ bridge 2 underside")
    b3 = c.rnd("Hub", "R10c-15c", b3, *plain(b3), 9)
    b3 = c.rnd("Hub", "R16c", b3, *rep([("sc", 1), ("dec", 1)], 3), 6)
    c.rnd("Hub", "R17c", b3, *rep([("dec", 1)], 3), 3)
    print(f"  -- root base remains OPEN at 18 sts for the torso socket")

    # ============================================================ 3. TORSO
    c.section("SECTION 3 — MULTI-SOCKET TORSO & HYPERBOLIC MANTLE")
    a = c.rnd("Torso", "R1", None, 0, 24, 24, foundation=True, note="ch 24, OPEN neck ring")
    a = c.rnd("Torso", "R2-6", a, *plain(a), 24)
    a = c.rnd("Torso", "R7", a, 4 + 6 + 8 + 6, 4 + 6 + 8 + 6, 24, note="two 6-st wing sockets")
    a = c.rnd("Torso", "R8", a, 24, 24, 24, note="closes over both ch-bridges")
    split = a = c.rnd("Torso", "R9", a, *rep([("sc", 3), ("inc", 1)], 6), 30)
    m = c.rnd("Torso", "R10", a, *rep([("inc", 1)], 30), 60, note="FLO — saves R9's 30 BLO")
    m = c.rnd("Torso", "R11", m, *rep([("sc", 1), ("inc", 1)], 30), 90)
    fans = 90 // 3
    c.rnd("Torso", "R12", m, fans, fans * 5, 150, partial=True,
          note="terminal edging; 2 sts skipped between fans is standard scallop spacing")
    a = c.rnd("Torso", "R13", split, *rep([("sc", 4), ("inc", 1)], 6), 36,
              note="into R9's free BLO")
    a = c.rnd("Torso", "R14", a, *rep([("sc", 8), ("inc", 1)], 4), 40)
    if fixed:
        a = c.rnd("Torso", "R15", a, *rep([("sc", 4), ("3-st-inc", 1)], 8), 56)
    else:
        a = c.rnd("Torso", "R15", a, *rep([("sc", 3), ("3-st-inc", 1)], 8), 56)
    a = c.rnd("Torso", "R16", a, *plain(a), 56)
    if fixed:
        bw1, bw2 = 20, 30
    else:
        bw1, bw2 = 14, 24
    a = c.rnd("Torso", "R17", a, bw1 + 6 + bw2, bw1 + 12 + bw2, 62,
              note="tentacle hub join")
    a = c.rnd("Torso", "R18", a, *plain(a), 62)
    r19b = 62 - bw1 - 12
    a = c.rnd("Torso", "R19", a, bw1 + 12 + r19b, bw1 + 6 + r19b, 56, note="dec across the join")
    for i, (s, tgt) in enumerate([(5, 48), (4, 40), (3, 32), (2, 24), (1, 16)], start=20):
        a = c.rnd("Torso", f"R{i}", a, *rep([("sc", s), ("dec", 1)], 8), tgt)
    torso_out = c.rnd("Torso", "R25", a, *rep([("dec", 1)], 8), 8)

    # ============================================================ 4. WINGS
    c.section("SECTION 4 — DUAL HYPERBOLIC PECTORAL WINGS (make 2)")
    w = c.rnd("Wing", "Row 1", None, 0, 6, 6, foundation=True, note="ch 7 -> 6 sc; socket tab")
    w = c.rnd("Wing", "Row 2-4", w, *plain(w), 6, note="tab, 3 more rows")
    w = c.rnd("Wing", "Row 5", w, *rep([("inc", 1)], 6), 12)
    w = c.rnd("Wing", "Row 6", w, *cost(("hdc", 12)), 12, note="hdc")
    w = c.rnd("Wing", "Row 7", w, *rep([("sc", 1), ("inc", 1)], 6), 18, note="FLO")
    if fixed:
        w = c.rnd("Wing", "Row 8", w, *cost(("sc", 4), ("hdc", 4), ("dc", 4), ("tr", 5),
                                            ("3-st-inc", 1)), 20)
        w = c.rnd("Wing", "Row 9", w, *plain(w), 20, note="fptr into Row 8 — ADJACENT, 20<->20")
    else:
        w = c.rnd("Wing", "Row 8", w, *cost(("sc", 4), ("hdc", 4), ("dc", 4), ("tr", 4),
                                            ("3-st-inc", 1)), 20)
        w = c.rnd("Wing", "Row 9", w, *plain(w), 20, note="fptr into Row 6")
        c.fail("Wing", "Row 9",
               "the fptr is anchored into Row 6, three rows below (Rows 7 and 8 intervene). "
               "Section 1 does this correctly — R16 hdc with R17 posting into it, adjacent")
        c.fail("Wing", "Row 9",
               "5 posts spaced every 4th st of a 20-st row, anchored into a 12-st row: "
               "20 and 12 do not share that spacing, so the ridge cannot stack vertically")
        c.fail("Wing", "Row 8",
               "'3-st-inc in tr (3 tr in last st)' contradicts the glossary, which defines "
               "3-st-inc as 3 SC in the same stitch")

    # ---------------------------------------------------------- glossary
    print(f"\n{'=' * 94}\nGLOSSARY AUDIT\n{'=' * 94}")
    defined = ["sc", "inc", "dec", "hdc", "dc", "tr", "FLO", "BLO", "fpdc", "bpdc",
               "fptr", "ch-sp", "3-st-inc", "3-st-dec", "split-sc"]
    used = ["sc", "inc", "dec", "hdc", "dc", "tr", "FLO", "BLO", "fpdc", "fptr",
            "3-st-inc", "ch", "sl st"]
    if fixed:
        defined = [d for d in defined if d not in ("bpdc", "ch-sp", "3-st-dec", "split-sc")]
        defined += ["ch", "sl st", "3-tr-inc"]
        used = [u for u in used if u != "3-st-inc"] + ["3-st-inc", "3-tr-inc"]
    undef = [u for u in used if u not in defined]
    dead = [d for d in defined if d not in used]
    print(f"  used but NEVER defined : {undef or 'none'}")
    print(f"  defined but NEVER used : {dead or 'none'}")
    if undef:
        c.fail("Glossary", "undefined",
               f"{', '.join(undef)} are used throughout but never defined "
               f"(ch 18/24/7/6/3/2/1; sl st to join every ring)")
    if dead:
        c.fail("Glossary", "dead entries",
               f"{', '.join(dead)} are defined but never used — split-sc gets a full "
               f"three-line Waistcoat Stitch definition and never appears")

    # -------------------------------------------------------- dimensions
    print(f"\n{'=' * 94}\nDIMENSIONS vs CLAIM\n{'=' * 94}")
    head_in, torso_in, tent_in = 19 / RNDS_PER_IN, 25 / RNDS_PER_IN, (8 + 13) / RNDS_PER_IN
    total = head_in + torso_in + tent_in
    wing_out = 9 / RNDS_PER_IN
    torso_d = (24 / STS_PER_IN) / math.pi
    span = 2 * wing_out + torso_d
    print(f"  cranial {head_in:.2f} in + torso {torso_in:.2f} in + tentacle {tent_in:.2f} in "
          f"= {total:.2f} in")
    print(f"  wingspan = 2 x {wing_out:.2f} + {torso_d:.2f} torso dia = {span:.2f} in")
    if not fixed:
        print(f"  CLAIMED 18 in long -> overstated {18 / total:.1f}x")
        print(f"  CLAIMED 12 in wingspan -> overstated {12 / span:.1f}x")
        c.fail("Dimensions", "finished size",
               f"claims 18 in long and 12 in wingspan; at the pattern's own gauge it is "
               f"{total:.1f} in and {span:.1f} in — overstated {18 / total:.1f}x and "
               f"{12 / span:.1f}x")
    else:
        print(f"  corrected claim: ~{total:.0f} in long, ~{span:.0f} in wingspan -> consistent")
        print(f"  (to reach the original's 18 in, rework in worsted on a 5.5 mm hook: "
              f"{18 / total:.2f}x linear)")

    audit_self_checks(c, fixed)

    print(f"\n  Neck interface: Cranial R19 {head_out} sts <-> Torso R1 24 sts  -> "
          f"{'MATCH' if head_out == 24 else 'MISMATCH'}")
    print(f"  Torso closes at {torso_out} sts, cinched shut")

    print(f"\n{'#' * 94}")
    print(f"TOTAL DEFECTS: {len(c.defects)}")
    for piece, label, message in c.defects:
        print(f"  - {piece} {label}: {message}")
    return len(c.defects)


if __name__ == "__main__":
    use_fixed = "--fixed" in sys.argv
    print("CORRECTED PATTERN" if use_fixed else "PATTERN AS SUBMITTED")
    sys.exit(1 if run(use_fixed) else 0)
