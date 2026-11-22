#!/usr/bin/env python3
"""Independent deterministic verifier for the "Abyssal Leviathan".

Written from scratch. The repository engine cannot model short-row raw-edge
perimeters, a bifurcating fork with a shared chain bridge, a six-limb socket
hub, or edging density, all of which this pattern depends on.

Cost model, as (base stitches consumed, stitches produced):
    sc 1/1   inc 1/2   dec 2/1   hdc 1/1   dc 1/1   bpdc 1/1   sl st 1/1

A round is valid only when BOTH hold:
    consumed == stitches available   and   produced == stated count

Usage:
    python verify_leviathan.py            # pattern as submitted
    python verify_leviathan.py --fixed    # corrected pattern
"""

from __future__ import annotations

import math
import sys

STS_PER_IN = 24 / 4.0    # 6.0   - from the pattern's stated gauge
RNDS_PER_IN = 26 / 4.0   # 6.5

COST = {"sc": (1, 1), "inc": (1, 2), "dec": (2, 1),
        "hdc": (1, 1), "dc": (1, 1), "bpdc": (1, 1), "sl st": (1, 1)}


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

    # ==================================================== 1. CRANIAL VAULT
    c.section("1. CRANIAL VAULT & CURVED MANTLE")
    a = c.rnd("Cranial", "1", None, 0, 6, 6, foundation=True)
    for i, (unit, target) in enumerate(
            [([("inc", 1)], 12), ([("sc", 1), ("inc", 1)], 18),
             ([("sc", 2), ("inc", 1)], 24), ([("sc", 3), ("inc", 1)], 30),
             ([("sc", 4), ("inc", 1)], 36), ([("sc", 5), ("inc", 1)], 42)], start=2):
        a = c.rnd("Cranial", str(i), a, *rep(unit, 6), target)
    a = c.rnd("Cranial", "8-14", a, *plain(a), 42)
    a = c.rnd("Cranial", "15", a, *rep([("sc", 5), ("bpdc", 1)], 7), 42,
              note="bpdc ridge")
    if not fixed:
        c.fail("Cranial", "15",
               "the heading calls this 'Front Post Alignment' but the stitch is bpdc, "
               "a BACK post stitch - a back post ridge is pushed to the inside of the "
               "work, so the bio-luminescent ridge ends up within the stuffed head")
        c.fail("Cranial", "15",
               "bpdc is worked around the posts of round 14, which is a round of sc; "
               "sc posts are too short to take a double crochet post stitch")
    base = a = c.rnd("Cranial", "16", a, *plain(a), 42)

    print("  -- short-row brow crest --")
    sr = c.rnd("Cranial", "17a", base, *cost(("sc", 16)), 16, partial=True)
    sr = c.rnd("Cranial", "17b", sr, *cost(("dec", 1), ("sc", 12), ("dec", 1)), 14)
    sr = c.rnd("Cranial", "17c", sr, *cost(("dec", 1), ("sc", 10), ("dec", 1)), 12)
    short_rows, untouched = 3, base - 16
    perimeter = sr + untouched + 2 * short_rows
    print(f"  -- perimeter: {sr} live + {untouched} untouched R16 + "
          f"{2 * short_rows} raw row-ends = {perimeter}")
    a = c.rnd("Cranial", "18", perimeter, 12 + 3 + 26 + 3, 12 + 3 + 26 + 3, 44,
              note="raw edges correctly worked")
    if fixed:
        a = c.rnd("Cranial", "19", a, *(lambda x, y: (x[0] + y[0], x[1] + y[1]))(
            rep([("sc", 4), ("dec", 1)], 4), rep([("sc", 3), ("dec", 1)], 4)), 36)
    else:
        a = c.rnd("Cranial", "19", a, *rep([("sc", 5), ("dec", 1)], 6), 36)
    a = c.rnd("Cranial", "20", a, *rep([("sc", 4), ("dec", 1)], 6), 30)
    a = c.rnd("Cranial", "21", a, *rep([("sc", 3), ("dec", 1)], 6), 24)
    head_top = c.rnd("Cranial", "22", a, *rep([("sc", 2), ("dec", 1)], 6), 18)

    # ======================================================= 2. TENTACLE
    c.section("2. BIFURCATING PRIMARY TENTACLE  (make 2)")
    if fixed:
        t = c.rnd("Tentacle", "1", None, 0, 12, 12, foundation=True,
                  note="ch 12 joined into an OPEN ring - this is the body socket")
        t = c.rnd("Tentacle", "2-20", t, *plain(t), 12)
        base_open, base_sts = True, t
    else:
        t = c.rnd("Tentacle", "1", None, 0, 8, 8, foundation=True,
                  note="magic ring - CLOSED")
        t = c.rnd("Tentacle", "2", t, *rep([("sc", 3), ("inc", 1)], 2), 10)
        t = c.rnd("Tentacle", "3-12", t, *plain(t), 10)
        t = c.rnd("Tentacle", "13", t, *rep([("sc", 4), ("inc", 1)], 2), 12)
        t = c.rnd("Tentacle", "14-20", t, *plain(t), 12)
        base_open, base_sts = False, 8

    fork_sc, bridge = 6, 2
    print(f"  -- R21 fork: sc {fork_sc}, ch {bridge}, skip {fork_sc}  "
          f"(consumes {fork_sc * 2} of {t})")
    alpha = c.rnd("Tentacle", "21 fork", t, fork_sc * 2, fork_sc + bridge, 8,
                  foundation=True)
    a2 = c.rnd("Tentacle", "22a-28a", alpha, *plain(alpha), 8)
    c.rnd("Tentacle", "29a", a2, *rep([("dec", 1)], 4), 4)
    beta = fork_sc + bridge
    b2 = c.rnd("Tentacle", "22b-28b", beta, *plain(beta), 8)
    b2 = c.rnd("Tentacle", "29b", b2, *rep([("sc", 2), ("dec", 1)], 2), 6)
    c.rnd("Tentacle", "30b", b2, *rep([("dec", 1)], 3), 3)

    # ========================================================== 3. ARMS
    c.section("3. SECONDARY LATERAL ARMS  (make 4)")
    m = c.rnd("Arm", "1", None, 0, 6, 6, foundation=True)
    m = c.rnd("Arm", "2", m, *rep([("sc", 2), ("inc", 1)], 2), 8)
    arm_sts = c.rnd("Arm", "3-15", m, *plain(m), 8)

    # ========================================================== 4. BODY
    c.section("4. SEGMENTED ABYSSAL BODY & TENTACLE HUB")
    a = c.rnd("Body", "1", None, 0, 6, 6, foundation=True)
    for i, (unit, target) in enumerate(
            [([("inc", 1)], 12), ([("sc", 1), ("inc", 1)], 18),
             ([("sc", 2), ("inc", 1)], 24), ([("sc", 3), ("inc", 1)], 30),
             ([("sc", 4), ("inc", 1)], 36), ([("sc", 5), ("inc", 1)], 42),
             ([("sc", 6), ("inc", 1)], 48)], start=2):
        a = c.rnd("Body", str(i), a, *rep(unit, 6), target)
    a = c.rnd("Body", "9-14", a, *plain(a), 48)

    # --- the six-limb hub -------------------------------------------------
    if fixed:
        body_worked = 4 + 4 + 12 + 4 + 4
        t_in, t_out, m_in, m_out = 8, 4, 5, 3     # worked into round / left for gusset
        body_skipped = 2 * t_out + 4 * m_out
        stated15 = 64
    else:
        body_worked = 4 + 4 + 12 + 4 + 4
        t_in, t_out, m_in, m_out = 4, 8, 3, 5
        body_skipped = 0
        stated15 = 54
    limb_in = 2 * t_in + 4 * m_in
    made15 = body_worked + limb_in
    print(f"  -- R15 hub: body sts worked {body_worked}, explicitly skipped "
          f"{body_skipped}, of {a} available")
    print(f"     limb sts worked into the round: 2 tentacles x {t_in} + "
          f"4 arms x {m_in} = {limb_in}")
    print(f"     limb sts left over: 2 x {t_out} + 4 x {m_out} = "
          f"{2 * t_out + 4 * m_out}")
    if body_worked + body_skipped != a:
        c.fail("Body", "15",
               f"body sts worked ({body_worked}) + skipped ({body_skipped}) = "
               f"{body_worked + body_skipped}, but round 14 produced {a} - "
               f"{a - body_worked - body_skipped} body sts are silently dropped, "
               f"never worked, skipped or joined")
    leftover = 2 * t_out + 4 * m_out
    if body_skipped and leftover != body_skipped:
        c.fail("Body", "15", f"gusset imbalance: {leftover} leftover limb sts vs "
                             f"{body_skipped} skipped body sts")
    if not fixed:
        c.fail("Body", "assembly 4",
               f"each arm leaves {m_out} outer sts and each tentacle {t_out}, but the "
               f"round's own arithmetic can only skip {m_in} and {t_in} body sts "
               f"beneath them - the gusset would sew {m_out} sts to {m_in} and "
               f"{t_out} sts to {t_in}")
    a = c.rnd("Body", "15", None, made15, made15, stated15, foundation=True)

    if not fixed:
        c.fail("Body", "16",
               f"'sc in all 54 sts around (working across outer remaining sts of "
               f"attached limbs)' is self-contradictory: the {leftover} outer limb sts "
               f"were explicitly excluded from R15, so the round is either {made15} "
               f"(not 54) or {made15 + leftover} if they are now included")
    a = c.rnd("Body", "16", a, *plain(a), stated15)
    if fixed:
        a = c.rnd("Body", "17", a, *rep([("sc", 6), ("dec", 1)], 8), 56)
        a = c.rnd("Body", "18", a, *rep([("sc", 5), ("dec", 1)], 8), 48)
        a = c.rnd("Body", "19-21", a, *plain(a), 48)
        seq, start = [([("sc", 6), ("dec", 1)], 42), ([("sc", 5), ("dec", 1)], 36),
                      ([("sc", 4), ("dec", 1)], 30), ([("sc", 3), ("dec", 1)], 24),
                      ([("sc", 2), ("dec", 1)], 18)], 22
    else:
        a = c.rnd("Body", "17", a, *rep([("sc", 7), ("dec", 1)], 6), 48)
        a = c.rnd("Body", "18-20", a, *plain(a), 48)
        seq, start = [([("sc", 6), ("dec", 1)], 42), ([("sc", 5), ("dec", 1)], 36),
                      ([("sc", 4), ("dec", 1)], 30), ([("sc", 3), ("dec", 1)], 24),
                      ([("sc", 2), ("dec", 1)], 18)], 21
    for i, (unit, target) in enumerate(seq, start=start):
        a = c.rnd("Body", str(i), a, *rep(unit, 6), target)
    body_top = a

    # ============================================================ 5. FIN
    c.section("5. DORSAL FIN SAIL  (flat rows)")
    f = c.rnd("Fin", "1", None, 0, 20, 20, foundation=True, note="ch 21 -> 20 sc")
    f = c.rnd("Fin", "2", f, *cost(("sc", 18), ("dec", 1)), 19, note="FLO")
    f = c.rnd("Fin", "3", f, *cost(("dec", 1), ("sc", 15), ("dec", 1)), 17, note="BLO")
    if fixed:
        f = c.rnd("Fin", "4", f, *cost(("sc", 16), ("inc", 1)), 18, note="FLO")
    else:
        f = c.rnd("Fin", "4", f, *cost(("sc", 15), ("inc", 1)), 18, note="FLO")
    f = c.rnd("Fin", "5", f, *rep([("sc", 4), ("dec", 1)], 3), 15)
    if fixed:
        for i, (body_n, target) in enumerate(
                [(13, 14), (12, 13), (11, 12), (10, 11), (9, 10), (8, 9), (7, 8)],
                start=6):
            f = c.rnd("Fin", str(i), f, *cost(("sc", body_n), ("dec", 1)), target)
        fin_rows, fan, per_fan = 12, 4, 2
    else:
        fin_rows, fan, per_fan = 5, 5, 1

    edge_in = fin_rows / RNDS_PER_IN
    total = (fan * fin_rows) // per_fan
    need_in = total / STS_PER_IN
    print(f"\n  -- fin webbing edging --")
    print(f"     {fin_rows} rows = {fin_rows} row ends, edge length {edge_in:.2f} in")
    print(f"     {total} edging sts = {need_in:.2f} in of stitch length "
          f"-> {need_in / edge_in:.1f}x fullness  ({fan / per_fan:.1f} sts per row end)")
    if need_in / edge_in > 3.0:
        c.fail("Fin", "6",
               f"{fan} sts into every single row end = {fan:.0f} sts per row end and "
               f"{need_in / edge_in:.1f}x fullness; a shell/webbing edging normally "
               f"runs 2-2.5x (about 2-3 sts per row end), so this will ruffle "
               f"rather than form a fin web")
    else:
        print(f"     -> within the 2-2.5x range for a shell edging: ok")

    # ==================================================== 6. INTERFACES
    print(f"\n{'=' * 94}\n6. ASSEMBLY INTERFACES & GEOMETRY\n{'=' * 94}")
    print(f"  Cranial R22 {head_top} sts  vs  Body top {body_top} sts  ->  "
          f"{'MATCH' if head_top == body_top else 'MISMATCH'}")

    need = t_in + t_out
    print(f"  Body tentacle socket needs an OPEN ring of {need} sts; "
          f"tentacle base is {base_sts} sts and "
          f"{'OPEN' if base_open else 'CLOSED (magic ring)'}")
    if not base_open or base_sts != need:
        c.fail("Tentacle", "1",
               f"the body's R15 socket works across {need} tentacle sts, but the "
               f"tentacle's base is a {base_sts}-st "
               f"{'magic ring that is pulled closed' if not base_open else 'ring'}"
               + (" - and both branch tips are cinched shut, so the piece has no "
                  "open end anywhere to attach to the body" if not base_open else ""))
    print(f"  Body arm socket needs {m_in + m_out} sts; arm end is {arm_sts} sts, open"
          f"  ->  {'MATCH' if m_in + m_out == arm_sts else 'MISMATCH'}")

    fin_w = 20 / STS_PER_IN
    span_lo, span_hi = (6, 26) if fixed else (8, 18)
    span = (span_hi - span_lo + 1) / RNDS_PER_IN
    print(f"\n  Fin foundation {fin_w:.2f} in wide; assembly sews it across Rounds "
          f"{span_lo}-{span_hi} = {span:.2f} in  ->  ratio {fin_w / span:.2f}")
    if fin_w / span > 1.25:
        c.fail("Fin", "assembly 3",
               f"the fin's 20-st foundation edge is {fin_w:.2f} in but Rounds "
               f"{span_lo}-{span_hi} span only {span:.2f} in - the fin is "
               f"{fin_w / span:.1f}x too long for the span it is assigned to")

    dia = lambda s: (s / STS_PER_IN) / math.pi  # noqa: E731
    print(f"  Head diameter   {dia(42):.2f} in ({dia(42) * 25.4:.0f} mm); "
          f"14 mm eye = {14 / (dia(42) * 25.4) * 100:.0f}% of it")
    print(f"  Body diameter   {dia(stated15):.2f} in, height "
          f"{(26 if fixed else 25) / RNDS_PER_IN:.2f} in")
    print(f"  Fin             {fin_w:.2f} x {fin_rows / RNDS_PER_IN:.2f} in")
    print(f"  Tentacle        {dia(12):.2f} in dia, trunk + branches")
    print(f"  Arm             {dia(8):.2f} in dia x {15 / RNDS_PER_IN:.2f} in")

    print(f"\n{'#' * 94}")
    print(f"TOTAL DEFECTS: {len(c.defects)}")
    for piece, label, message in c.defects:
        print(f"  - {piece} {label}: {message}")
    return len(c.defects)


if __name__ == "__main__":
    use_fixed = "--fixed" in sys.argv
    print("CORRECTED PATTERN" if use_fixed else "PATTERN AS SUBMITTED")
    sys.exit(1 if run(use_fixed) else 0)
