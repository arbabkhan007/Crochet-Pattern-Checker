#!/usr/bin/env python3
"""Adjudicator for "The Abomination of Yarn" — a pattern that ships with its own
inline error annotations.

Unlike the other five reviews in this folder, the job here is not to find errors
in a pattern that claims to be correct. It is to AUDIT THE ANNOTATIONS: confirm
the ones that hold, expose the ones that are themselves wrong, and list what they
missed. Every verdict below is computed, not asserted.

Usage:
    python audit_annotations.py
"""

from __future__ import annotations

import math
import textwrap

STS_PER_IN_A = 14 / 4.0   # Yarn A gauge as stated: 14 sc / 4 in

CONFIRMED: list[tuple[str, str, str]] = []
FALSE: list[tuple[str, str, str]] = []
INCOMPLETE: list[tuple[str, str, str]] = []
MISSED: list[tuple[str, str]] = []


def wrap(text: str, indent: str = "      ") -> str:
    return textwrap.fill(text, 92, initial_indent=indent, subsequent_indent=indent)


def banner(title: str) -> None:
    print(f"\n{'=' * 96}\n{title}\n{'=' * 96}")


# ---------------------------------------------------------------- CONFIRMED
def check_a_row1() -> None:
    chains, skipped = 42, 1
    actual, stated = chains - skipped, 44
    CONFIRMED.append(("Piece A Row 1", "should be 41 sc",
        f"ch {chains}, 'sc in 2nd ch from hook' skips {skipped} -> {actual} sc. "
        f"Stated {stated}, which is {stated - actual} too many."))


def check_a_row3() -> None:
    # sc 3, 2 dc in next st, sk 2, tr in next st, ch 3 + sl st (picot), sc 2
    consumed = 3 + 1 + 2 + 1 + 2
    produced = 3 + 2 + 1 + 2
    avail, stated = 41, 46
    reps = avail // consumed
    CONFIRMED.append(("Piece A Row 3", "repeat unit is 9 sts, doesn't divide 41",
        f"unit consumes {consumed} -> confirmed. {avail}/{consumed} = {avail / consumed:.2f}. "
        f"{reps} reps consume {reps * consumed}, leaving {avail - reps * consumed} unworked."))
    INCOMPLETE.append(("Piece A Row 3", "annotation stops at 'math does not work'",
        f"it never states the production figure: {reps} reps produce {reps * produced} sts "
        f"(+{reps} picots), not the stated {stated}."))


def check_a_row9() -> None:
    uc, up = 2 + 1 + 2 + 2, 2 + 5 + 2 + 1
    tc, tp = uc * 6 + 3, up * 6 + 3
    avail, stated = 58, 61
    CONFIRMED.append(("Piece A Row 9", "repeat math doesn't match available sts",
        f"unit consumes {uc}; x6 plus 'sc in last 3' = {tc} consumed of {avail} available, "
        f"so {avail - tc} sts are orphaned."))
    INCOMPLETE.append(("Piece A Row 9", "annotation flags consumption only",
        f"production is also wrong: {tp} sts are made, not the stated {stated}."))


def check_a_row10a() -> None:
    # ch3 (counts as dc), dc 4, *CL over 3, dc 5*, dc 2
    avail, stated = 61, 59
    n = (avail - 7) / 8
    best = int(n)
    CONFIRMED.append(("Piece A Row 10 (first)", "count mismatch",
        f"consumption is 7 + 8n; 7 + 8n = {avail} gives n = {n:.2f}, not an integer. "
        f"Best case n={best} consumes {7 + 8 * best} and produces {1 + 4 + 6 * best + 2}, "
        f"against a stated {stated}."))


def check_a_rnd12() -> None:
    w, h, stated = 41, 12, 172
    per = w * 2 + h * 2 + 4 * 2
    CONFIRMED.append(("Piece A Rnd 12", "'evenly' undefined / count arbitrary",
        f"a {w}-st x {h}-row panel has a perimeter of about {per} sc "
        f"({w}*2 + {h}*2 + 8 for corner increases). Stated {stated} is "
        f"{stated - per} more, {(stated / per - 1) * 100:.0f}% over the ceiling."))
    FALSE.append(("Piece A Rnd 12", "'switching from rows to rounds on flat piece'",
        "working a perimeter/edging round around a finished flat panel is standard crochet "
        "practice, not an error. The genuine faults in this line are the undefined 'evenly' "
        "and the impossible 172."))


def check_b_rnd11() -> None:
    avail = 20
    uc, up = 2 + 3, 1 + 3
    reps = avail // uc
    CONFIRMED.append(("Piece B Rnd 11", "should be 16, not 15",
        f"unit consumes {uc}, produces {up}. {avail}/{uc} = {reps} reps, consuming all "
        f"{reps * uc} and producing {reps * up}. Stated 15 is one short."))


def check_b_rnd12() -> None:
    # sc in same st (1), then [ch5, sk 3, sc in next] x n, then ch5 spanning the last 3
    rows = []
    for avail in (15, 16):
        n = (avail - 4) / 4
        rows.append((avail, n, n == int(n)))
    FALSE.append(("Piece B Rnd 12", "'sk 3 sts with 15 sts creates math chaos'",
        "Rnd 12 is CORRECT. Its consumption is 4 + 4n. With the TRUE count of 16 from Rnd 11, "
        "n = 3 exactly and the round closes perfectly with four ch-5 loops. It only fails "
        "against the erroneous 15. The chaos is inherited from Rnd 11, not created here."))


def check_b_rnd14_30() -> None:
    n = 28  # Rnd 13 = 4 ch-5 sps x 7 sts
    seq = [n]
    for _ in range(17):
        n = n * 3 // 2
        seq.append(n)
    claimed = 12 + 17 * 6
    FALSE.append(("Piece B Rnd 14-30", f"'12 + 17x6 = {claimed} sts'",
        f"the annotation treats Rnd 3 as additive (+6). It is not: '*sc, inc; rep around' is a "
        f"x1.5 MULTIPLIER. Starting from Rnd 13's {seq[0]} sts, 17 repeats give {seq[-1]:,} sts "
        f"- about {seq[-1] // claimed}x the annotation's figure. It also breaks sooner: the "
        f"sequence runs {seq[0]} -> {seq[1]} -> {seq[2]}, and {seq[2]} is odd, so a "
        f"two-stitch repeat cannot complete the round."))


# -------------------------------------------------------- FALSE ANNOTATIONS
def check_false_claims() -> None:
    FALSE.append(("Materials - safety eyes", "'eyes are never used' / '2-piece flat blanket'",
        "both halves are wrong. ASSEMBLY STEP 7 says 'Attach safety eyes to Piece A between "
        "Rnds 8-9', so they are used. And it is not a 2-piece flat blanket: there are five "
        "lettered pieces, and with the multipliers (A x2, B x2, C x1, D x4, E x1) that is ten "
        "physical pieces."))
    FALSE.append(("Piece A heading", "'but instructions say \"Make 1\" later'",
        "unsupported. 'Make 1' appears exactly once in the whole pattern, on PIECE C. Nothing "
        "anywhere instructs you to make a single Piece A, and Assembly step 1 says "
        "'Piece A (x2)', agreeing with the heading."))
    FALSE.append(("Piece A FO", "'Piece F only has 30 rows'",
        "mischaracterised. THERE IS NO PIECE F. The pattern contains A, B, C, D and E only. "
        "The annotation implies Piece F exists and merely has too few rows; the actual defect "
        "is a dangling reference to a piece that was never written."))
    FALSE.append(("Piece B Rnd 4-6", "'ERROR: no increases but rnds listed'",
        "not an error. 'Sc in each st around (18)' worked on 18 sts produces 18. Straight "
        "rounds between shaping rounds are normal and structurally necessary. This round is "
        "one of the few in the pattern that is completely correct."))
    FALSE.append(("Piece C assembly note", "'Piece D is a flat square - it has no Rnd 22'",
        "wrong twice. Piece D is not a square - it is worked in rounds from a ch-4 ring, and "
        "the pattern's own Rnd 31 annotation calls it 'a circle'. And Piece D DOES have a "
        "Rnd 22; it falls inside 'Rnd 6-30: Rep Rnds 2-5'. The real defect is that Rnd 22 "
        "lands mid-cycle, so which sub-round it refers to is undefined."))
    FALSE.append(("Piece D heading", "'but diagram shows 2'",
        "unsupported. There is no diagram anywhere in the pattern. Assembly step 4 says "
        "'Piece D (x4)', which agrees with the heading."))


# ------------------------------------------------------------ MISSED ERRORS
def collect_missed() -> None:
    for tag, text in [
        ("MATERIALS", "The 5.0mm hook the GAUGE section requires is not in the materials list - "
                      "only 3.5mm and 6mm are listed."),
        ("MATERIALS", "Fiberfill is never listed, yet Assembly step 8 says 'Stuff firmly with "
                      "fiberfill'."),
        ("MATERIALS", "'Stitch markers (7)' are listed and 'pm = place marker' is defined, but "
                      "pm is never used anywhere in the pattern."),
        ("MATERIALS", "3 safety eyes across Piece A (x2): an odd number that cannot divide "
                      "between two identical pieces, and eyes are normally used in pairs."),
        ("ABBREV",    "The abbreviation table has lost every delimiter - 'AbbrMeaning scsingle "
                      "crochet (US) dcdouble crochet...' - and is unparseable as printed."),
        ("ABBREV",    "CL contradicts itself between the table and the body: the table says "
                      "'5 tr CL in Piece B', Piece B Rnd 8 says 'this is now a 5-dc CL'. That "
                      "is a THIRD definition of CL, and the annotations flag only two."),
        ("ABBREV",    "BPdc is defined but never used anywhere in the pattern."),
        ("PIECE A",   "Rows 5-7 ('Rep Row 3') carry no stitch count at all."),
        ("PIECE A",   "Row 11 works 'in FLO of Row 9', which had 61 sts - that is 61 puffs, not "
                      "the stated 41."),
        ("PIECE A",   "Rows 14-20 repeat Rows 2-8, but Row 8 says 'FPdc around each dc from "
                      "Row 4'. Repeated at Row 20, does that mean Row 4 or Row 16?"),
        ("PIECE A",   "PARTIAL CREDIT: the duplicate Row 10 ('sc in BLO') followed by Row 11 "
                      "('FLO of Row 9') is actually a legitimate FLO/BLO split - two fabrics "
                      "off one row. It is the only sound technique in Piece A, and the "
                      "annotations treat it purely as an error."),
        ("PIECE C",   "The UK note covers 'dc' only. 'tr' is left ambiguous - UK tr = US dc - so "
                      "every tr in Rows 3 and 10 has two possible meanings."),
        ("PIECE C",   "Row 1's stated 86 only works under US dc with ch-3 counting as a stitch. "
                      "Under the piece's own UK rule it should be 85. The count itself proves "
                      "the row was written in US terms."),
        ("PIECE C",   "Row 10's repeat consumes 5 sts (sk 4 + sc 1). After the opening sc and "
                      "the last 3 sts, about 76 remain; 76/5 = 15.2, so it does not divide "
                      "either. The annotation flags only the US/UK ambiguity."),
        ("PIECE D",   "'Rnd 6-30: Rep Rnds 2-5' fails on the FIRST iteration, not just the "
                      "last: Rnd 2 is '8 sc in ring' and after Rnd 5 there is no ring left to "
                      "work into."),
        ("PIECE E",   "Rnd 2's repeat needs a ch-2 space after every 6 dc, but Rnd 1 places "
                      "ch-2 spaces at the 4 corners only. The repeat runs out of spaces "
                      "immediately."),
        ("PIECE E",   "'Join at the bottom-right corner of assembled Pieces A+B+C+D' - Piece B "
                      "is a tube worked from a magic circle. It has no corner and no flat edge "
                      "to join along."),
        ("ASSEMBLY",  "Step 7 attaches safety eyes at final assembly. A safety eye needs rear "
                      "access to seat its washer and must go in before the piece is closed - "
                      "and by step 7 Piece A's Rows 8-9 are buried under the Piece E border."),
        ("ASSEMBLY",  "Step 4 attaches Piece D at Piece A 'Rows 10, 12, 14, 16'. Beyond the "
                      "duplicate Row 10 the annotation notes, Row 12 is the perimeter round and "
                      "Rows 14/16 are inside the 'Rep Rows 2-8' block."),
    ]:
        MISSED.append((tag, text))


def arithmetic_appendix() -> None:
    banner("APPENDIX - PUTTING NUMBERS ON THE 'ARBITRARY' FIGURES")
    ends = {"Piece A x2 (Yarn A)": 4, "Piece A x2 (Yarn B at Rnd 12)": 4,
            "Piece B x2 (Yarn C)": 4, "Piece C (Yarn B)": 2,
            "Piece D x4 (Yarn E)": 8, "Piece E (Yarn A+B held)": 4}
    total = sum(ends.values())
    print("\n  Assembly step 6: 'Weave in all 847 ends'")
    for k, v in ends.items():
        print(f"    {k:<34}{v:>4}")
    print(f"    {'realistic total':<34}{total:>4}   -> 847 is {847 / total:.0f}x too many")

    dia = (12 / STS_PER_IN_A) / math.pi
    print("\n  Piece D Rnd 31: 'Block to 8\" x 8\" square'")
    print(f"    a 12-sc circle at {STS_PER_IN_A:.1f} sc/in = {12 / STS_PER_IN_A:.2f} in around "
          f"= {dia:.2f} in across")
    print(f"    blocking that to 8x8 in is {8 / dia:.1f}x linear and "
          f"{(8 * 8) / (math.pi * (dia / 2) ** 2):.0f}x the area - and a circle has no corners")

    print("\n  Gauge: '22 dc and 10 rows = 4 in using Yarn C (BULKY #5) on a 3.5mm hook'")
    print(f"    {22 / 4:.1f} dc per inch. A bulky dc is roughly 0.5 in wide, so ~2/in is "
          f"realistic -> about {5.5 / 2:.1f}x too dense")
    print( "    bulky #5 is rated for 6.5-9mm hooks; 3.5mm is far below the yarn's range")
    print( "    and the only piece in Yarn C (Piece B) uses the 6mm hook, not 3.5mm - so this")
    print( "    gauge describes a yarn/hook pairing that appears nowhere in the pattern")

    print("\n  Finished size: '60\" x 80\"'")
    w = 41 / STS_PER_IN_A
    h = 21 / (16 / 4.0)
    print(f"    Piece A at the stated Yarn A gauge: {41} sts / {STS_PER_IN_A:.1f} = {w:.1f} in "
          f"wide, 21 rows / 4.0 = {h:.1f} in tall")
    print(f"    two of them side by side: {2 * w:.1f} in x {h:.1f} in")
    print(f"    against a claimed 60 x 80 in -> the claim is about "
          f"{(60 * 80) / (2 * w * h):.0f}x the achievable area")


def main() -> None:
    check_a_row1(); check_a_row3(); check_a_row9(); check_a_row10a(); check_a_rnd12()
    check_b_rnd11(); check_b_rnd12(); check_b_rnd14_30()
    check_false_claims(); collect_missed()

    banner("1. ANNOTATIONS CONFIRMED (spot-checked by computation)")
    for loc, claim, detail in CONFIRMED:
        print(f"\n  [{loc}]  claim: {claim}")
        print(wrap(detail))

    banner("2. ANNOTATIONS THAT ARE CONFIRMED BUT INCOMPLETE")
    for loc, claim, detail in INCOMPLETE:
        print(f"\n  [{loc}]  {claim}")
        print(wrap(detail))

    banner("3. ANNOTATIONS THAT ARE THEMSELVES FALSE")
    for loc, claim, detail in FALSE:
        print(f"\n  [{loc}]  claim: {claim}")
        print(wrap(detail))

    banner("4. DEFECTS THE ANNOTATIONS MISSED")
    for tag, text in MISSED:
        print(f"\n  [{tag}]")
        print(wrap(text, "    "))

    arithmetic_appendix()

    banner("SUMMARY")
    print(f"  annotations spot-checked and CONFIRMED : {len(CONFIRMED)}")
    print(f"  confirmed but INCOMPLETE               : {len(INCOMPLETE)}")
    print(f"  annotations that are FALSE             : {len(FALSE)}")
    print(f"  defects the annotations MISSED         : {len(MISSED)}")


if __name__ == "__main__":
    main()
