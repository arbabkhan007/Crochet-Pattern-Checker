#!/usr/bin/env python3
"""
Generates `corrected.md` for NS 14 Bobble Snowflake Tree Skirt.

The 32 growth rounds are emitted from the count rule itself
(round N consumes N-1 and produces N stitches in each of 12 repeats)
rather than typed by hand, so the tables cannot drift from the maths.
The UK column is generated from the US column by a single substitution,
so the two columns are equivalent by construction.
"""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).parent

LAST_ROUND = 32
SIZES = {14: "MINI SIZE - continue to border here",
         23: "STANDARD SIZE - continue to border here",
         32: "LARGE SIZE - continue to border here"}


def is_bobble(n: int) -> bool:
    return n >= 5 and (n - 5) % 3 == 0


def sts(stitch: str, n: int) -> str:
    """'dc in next 5 sts' / 'dc in next st'."""
    return f"{stitch} in next st" if n == 1 else f"{stitch} in next {n} sts"


def us_round(n: int) -> str:
    if n == 1:
        return "Ch 2, 12 dc in ring, sl st to first dc"
    if n == 2:
        return ("Ch 2, 2 dc in same st as join, 2 dc in each of next 11 sts, "
                "sl st to first dc")
    parts = ["Ch 2"]
    if is_bobble(n):
        parts.append("BO in same st as join")
        if n - 3 > 0:
            parts.append(sts("dc", n - 3))
        parts.append("2 dc in next st")
        inner = [f"BO in next st"]
        if n - 3 > 0:
            inner.append(sts("dc", n - 3))
        inner.append("2 dc in next st")
        parts.append("[" + ", ".join(inner) + "] x 11")
        parts.append("sl st to first BO")
    else:
        parts.append("dc in same st as join")
        if n - 3 > 0:
            parts.append(sts("dc", n - 3))
        parts.append("2 dc in next st")
        inner = []
        if n - 2 > 0:
            inner.append(sts("dc", n - 2))
        inner.append("2 dc in next st")
        parts.append("[" + ", ".join(inner) + "] x 11")
        parts.append("sl st to first dc")
    return ", ".join(parts)


def to_uk(text: str) -> str:
    mapping = {"dc": "tr", "sc": "dc", "hdc": "htr", "tr": "dtr"}
    import re
    tokens = re.split(r"(\W+)", text)
    # single pass, no cascading (dc->tr must not then become dtr)
    return "".join(mapping.get(t, t) if t.isalpha() else t for t in tokens)


BORDER_US = ("Join CC in any st; ch 1, sc in same st, skip 2 sts, 5 dc in next st, "
             "skip 2 sts, [sc in next st, skip 2 sts, 5 dc in next st, skip 2 sts] "
             "around, sl st to first sc, FO")

RING_US = "Ch 20, sl st to first ch to form a ring"

SURFACE_US = ("Join CC beside an increase column at the centre; surface sl st outward "
              "over each of the 12 columns, FO")


def table(rows: list[tuple[str, str, str, str, str]]) -> str:
    out = ["| Rnd | US terms | UK terms | Sts | Note |", "|---|---|---|---|---|"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def growth_table(lo: int, hi: int) -> str:
    rows = []
    for n in range(lo, hi + 1):
        us = us_round(n)
        note = SIZES.get(n, "-")
        if n == 5:
            note = "first bobble round"
        rows.append((f"R{n}", us, to_uk(us), f"({12 * n})", note))
    return table(rows)


# ---------------------------------------------------------------- yarn model
ST_WIDTH_CM = 10.0 / 12
YARN_CM_PER_DC = 10.0


def yarn(last: int) -> tuple[int, int, int]:
    body = sum(12 * n for n in range(1, last + 1))
    extra = sum(48 for n in range(1, last + 1) if is_bobble(n))
    scallops = 2 * last
    cm = (body + extra + scallops * 5) * YARN_CM_PER_DC + scallops * 5.5
    m = cm / 100
    return int(round(m)), int(round(m / 180 * 100)), int(round(m / 150 * 100))


def diam(last: int) -> tuple[float, float]:
    d_stitch = (12 * last * ST_WIDTH_CM) / math.pi + 3.6
    hole_r = (12 * ST_WIDTH_CM / math.pi) / 2
    d_row = 2 * (hole_r + last * (10.0 / 6)) + 3.6
    return min(d_stitch, d_row), max(d_stitch, d_row)


def main() -> None:
    for n in (14, 23, 32):
        m, gw, ga = yarn(n)
        lo, hi = diam(n)
        print(f"R{n}: {m} m, {gw}-{ga} g, {lo/2.54:.1f}-{hi/2.54:.1f} in "
              f"({lo:.0f}-{hi:.0f} cm), {2*n} scallops")

    doc = TEMPLATE.format(
        t1=growth_table(1, 8),
        t2=growth_table(9, 16),
        t3=growth_table(17, 24),
        t4=growth_table(25, 32),
        ring=table([("-", RING_US, to_uk(RING_US), "-",
                     "trunk opening; ch 24 for a larger one")]),
        border=table([("-", BORDER_US, to_uk(BORDER_US), "(12 x N)",
                       "6 sts per repeat; scallops = 2 x N, so it closes after any round")]),
        surface=table([("-", SURFACE_US, to_uk(SURFACE_US), "-",
                        "12 spokes, one per increase column")]),
    )
    (HERE / "corrected.md").write_text(doc, encoding="utf-8")
    print("\nwrote corrected.md")


TEMPLATE = """# Bobble Snowflake Tree Skirt

> **US + UK terms · Easy - Intermediate · grows by size** — Design Code NS 14

A flat twelve-spoke circle of double crochet with a bobble snowflake blooming every third round. Closed centre ring - slip it over the stand before the tree goes up. Mini, standard and large sizes from the same twelve-columns math.

**FINISHED SIZE** Mini / tabletop: stop after R14 - 19-21 in (48-53 cm) across. Standard: stop after R23 - 30-33 in (76-84 cm) across. Large: stop after R32 - 41-45 in (104-114 cm) across. Centre hole approximately 1.25-1.75 in (3-4.5 cm) at rest, opening to about 2 in (5 cm) when stretched over a stand (verify against your tree stand; ch 24 at the start for an opening about 1.5-2.1 in / 4-5.5 cm at rest).

---

## Safety — read this first

This design is intended as home decor, not a toy. It is not flameproof: keep the skirt away from open flames, heaters and hot lamps, and use only cool-running lights that are approved for the tree and location.

No finished skirt has been independently assessed by Novality Store for flammability or another product-safety requirement. Before supply, the finished-item maker or seller must assess the actual yarn and construction and meet all classification, testing, documentation, labelling and traceability duties for every destination market. A "home decor" label does not replace requirements arising from intended or reasonably foreseeable use.

## Materials

- Worsted or aran (#4) yarn. Amounts below are calculated from the gauge in this pattern and include the border; buy about 20% extra for tension differences and swatching.

| Size | Total yarn | If worked in one colour | MC | CC (bobble rounds + border) |
|---|---|---|---|---|
| Mini (R14) | approx. 160 m / 175 yd | 100-150 g | approx. 55-80 g | approx. 45-70 g |
| Standard (R23) | approx. 390 m / 425 yd | 250-350 g | approx. 130-190 g | approx. 110-160 g |
| Large (R32) | approx. 720 m / 785 yd | 450-600 g | approx. 250-340 g | approx. 190-260 g |

- Hook: 5-5.5 mm for the skirt; 4-4.5 mm for the optional surface slip-stitch spokes.

- Optional contrast yarn (CC) for bobble rounds and surface lines. If you work the bobble rounds entirely in CC, the CC column above is what you need; if only the bobbles themselves are CC, allow about a quarter of it.

- Notions: stitch marker, scissors, tapestry needle.

## Gauge & size

Flat swatch in US dc, blocked lightly: 12 dc = 4 in (10 cm); 6 rows = 4 in (10 cm). Measure the actual skirt as it grows.

Why both numbers matter: +12 stitches per round adds 10 cm (4 in) of circumference, which a flat circle turns into 1.59 cm (0.63 in) of extra radius. The row gauge above gives 1.67 cm (0.66 in) per round - within 5%, which blocks flat. If your rows run much taller than that the skirt will cup; if they run much shorter it will ruffle. Match the stitch gauge first.

## Abbreviations (US + UK)

MC - main colour · CC - contrast colour

ch - chain · sl st - slip stitch

st(s) - stitch(es) · FO - fasten off

sc = dc - single crochet / double crochet · R - round

dc = tr - double crochet / treble crochet · (n) - stitch count at round end

BO - 5-dc bobble (counts as 1 st) / UK: 5-tr bobble (counts as 1 st)

How to read this dual pattern: every round appears twice side by side - the US-terms instruction in the left column, the exact UK equivalent in the right column. Stitch counts are identical for both terminologies. Prose tips use US terms.

## Construction & techniques

Closed rounds, joined - do not turn. Ch 2 at round start never counts as a stitch. Twelve increase columns add 12 stitches every round; every third round from R5 is a bobble round (in CC if you like).

1. **Where each round starts - read this before R2.** From R2 onward the first stitch of every round goes into the SAME stitch that the joining slip stitch sits in, not into the stitch after it. Every round below spells this out as "dc in same st as join" or "BO in same st as join". Mark that first stitch and slip stitch into it at the end of the round. This is not a stylistic preference: the twelve repeats are what keep the increases stacked in straight radial columns. If you start one stitch late the counts still come out right, but each round's columns slip one stitch sideways, and by R32 the spokes and bobbles have wound about 120 degrees around the skirt - a spiral, not a snowflake.

2. **The 12-spoke circle** - Round N of the growth ladder consumes N-1 and produces N stitches per each of its 12 repeats, so the stitch total after round N is always exactly 12 x N. R9 needs 7 plain dc and R10 needs 8 - one fewer and you run out of stitches before the round closes.

3. **The 5-dc bobble** - Yarn over, insert hook, pull up a loop, yarn over, pull through 2 loops (incomplete dc - you now have 2 loops on the hook). Repeat 4 more times in the same stitch, adding one loop each time, until 6 loops are on the hook. Yarn over, pull through all 6. One bobble counts as ONE stitch; push it to the front as it closes.

4. **Changing colour at a join** - Work the final slip stitch of the round with the new colour, then begin the next round with it - no visible step.

5. **Where the join hides** - Because every repeat begins at the join, the bobble of repeat 1 lands directly on the joining column, and the twelfth increase sits immediately before it. The seam therefore disappears into a spoke instead of wandering across the plain fabric.

6. **Surface snowflake spokes** - Surface slip stitches up each of the 12 increase columns in CC with a smaller hook. Keep them loose so the skirt stays flat. This only works if the columns are straight - see note 1.

## Instructions

### 1. Skirt - center ring and growth rounds

Ch 2 starts every round and is never counted. From R2 onward, work the first dc (or first BO on a bobble round) into the same stitch as the join, then end with sl st to that first actual stitch. Worked flat and circular throughout.

#### Centre ring

{ring}

The 12 dc of R1 gather the chain ring slightly, so the relaxed opening is smaller than the chain itself: expect roughly 1.25-1.75 in (3-4.5 cm) at rest, stretching to about 2 in (5 cm). Measure your tree stand's post and use ch 24 if you need more.

#### Rounds 1-8

{t1}

#### Rounds 9-16

{t2}

#### Rounds 17-24

{t3}

#### Rounds 25-32

{t4}

#### Scalloped border

{border}

Scallops by size: R14 -> 28, R23 -> 46, R32 -> 64. The last repeat's second "skip 2 sts" takes you back to the joining stitch, so the round closes with no gap.

Because every round total is 12 x N and 12 x N is always divisible by 6, this border closes cleanly after **any** round, not only the three named sizes. Stop wherever the skirt fits your stand and work 2 x N scallops.

#### Surface snowflake lines (optional)

{surface}

Sizes are approximate - yarn, hook and tension change the diameter. Measure the lying-flat skirt against your tree stand before committing to a border.

## Finishing & assembly

- Weave all ends on the wrong side.

- Block lightly to a flat circle; a gentle border wave is the design.

- Measure the centre opening against the tree stand before listing photos; photograph under a decorated tree AND flat on the floor.

## Troubleshooting

- **Skirt ruffles like a lettuce leaf.** Too many increases for your tension - the ladder is exactly +12 per round, so the fix is tension or a smaller hook, not extra stitches.

- **Skirt cups like a bowl.** Too few increases reaching the round end - check R9 (7 plain dc) and R10 (8) first; one plain dc short leaves 12 stitches unworked at round end.

- **The spokes spiral instead of radiating.** You are starting each round one stitch late. The first stitch of the round belongs in the same stitch as the join - see Construction note 1.

- **Bobbles will not pop.** Work the 5 dc loosely and push each bobble to the front as it closes; CC bobbles read best.

- **The border swallows some bobbles.** Each size ends on a bobble round, so a few edge bobbles fall inside a "skip 2". If you would rather keep every bobble clear, work one extra plain round before the border (R15, R24 or R33); the totals stay 12 x N and the scallop count becomes 2 x N.

## Colorways

Forest & cream · Snow white & red scallops · Navy & silver · Single-colour cream

## Helpful tips

### Sizes at a glance

| Size | Stop after round | Stitches | Border scallops | Approx. diameter |
|---|---|---|---|---|
| Mini/tabletop | R14 | 168 | 28 | 19-21 in / 48-53 cm |
| Standard | R23 | 276 | 46 | 30-33 in / 76-84 cm |
| Large | R32 | 384 | 64 | 41-45 in / 104-114 cm |

Every round total is 12 x N, which is always divisible by 6, so the scallop border closes cleanly at every size - and after any round you choose to stop on.

- Count rule: Round N always consumes N-1 existing stitches and produces N stitches in each of 12 repeats. On a plain round that is (N-2) plain dc plus one increase; on a bobble round, one of those plain dc is replaced by one BO. Use this rule to verify any added rounds.

## Care & storage

Follow the actual yarn label. Before publishing a cleaning claim or supplying finished skirts, wash and dry a full-size sample by the proposed method, then remeasure the diameter and centre opening and inspect for dye transfer, shrinkage, bobble distortion and stretched joins. Until that test passes, make no machine-wash or tumble-dry claim. Store completely dry and away from heat, flame, damp and pests; lay flat or roll rather than sharply creasing the bobble design.

## Terms of Use

### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 14.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

### You may

Make as many finished skirts as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small quantities with credit to Novality Store.

### You may not

Sell, share, copy or redistribute this pattern or any part of it. Claim the pattern as your own design. Produce items from this pattern as a factory or manufacturer.

### Safety reminder

Intended as home decor, not a toy, and not flameproof. Keep away from ignition and heat sources and use only cool-running lights approved for the tree and location. No finished skirt has been independently assessed by Novality Store; the finished-item maker or seller is responsible for all market-specific product-safety evidence and duties before supply.

## Happy crocheting!

Tag your makes with **#NovalityStore** and **#NovalityTreeSkirt** - lay it under the tree, plug in the lights, and step back. Thank you for supporting an independent pattern designer.
"""

if __name__ == "__main__":
    main()
