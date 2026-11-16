#!/usr/bin/env python3
"""Apply the round-3 corrections to a copy of the Grand Collection volume.

The pasted/compiled volume can be newer than this repo's own copy, so some of the
corrected sentences only exist there. This script applies every round-3 edit to a
Markdown file idempotently — it skips a fix that is already in place and reports a
fix whose source text it cannot find, without failing the run.

    python3 docs/reviews/round3_volume_errata.py path/to/NovalityStore_Grand_Collection.md
    python3 docs/reviews/round3_volume_errata.py --dry-run path/to/volume.md

Exit code is 0 when every fix is either applied or already present, and 1 when at
least one fix could not be located (so a CI job can flag a stale volume).

Run against this repo's own volume, the handful of fixes marked "paste only" (the
review-table rows and the NS-14 cover brand line) report as not located: those
texts never existed here. Everything else should report applied/present.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KEEP_GAPS = (
    "- **Coco tips sideways or front to back.** Most often the two legs of a pair are on "
    "opposite sides of the body instead of together - keep all four leg joins three plain "
    "stitches apart AND paired: both back legs at the rear (stitches 1-3 and 7-9 of the "
    "Rnd-4 round, 90 degrees apart), both front legs at the chest (13-15 and 19-21, opposite "
    "them). If still tipping, stuff the lower body more firmly and settle weight back over "
    "all four feet."
)
R4_ROW_PAIRED = ("| R4 | join BL1: 3 sc, sc, inc, join BL2: 3 sc, [sc, inc] x 5 | (24) | "
                 "join BOTH back legs |")
R5_ROW_PAIRED = ("| R5 | [2 sc, inc] x 4, join FL1: 3 sc, sc, inc, sc, join FL2: 3 sc, sc, "
                 "inc, sc | (30) | join BOTH front legs |")
R10_ROW_TURNED = ("| Row 10 | 2 sc, dec, ch 1, turn | (3) | heel centre; the turn brings the "
                  "RIGHT side out for the pickup round |")

# Whole sections that must not ship inside a pattern. (id, description, regex, replacement)
BLOCK_FIXES: list[tuple[str, str, str, str]] = [
    (
        "NS-14-revision-notes",
        "'delete before publishing' notes were left at the end of the pattern",
        r"\n*## Revision notes[^\n]*\n.*\Z",
        "\n",
    ),
]

# (id, description, old, new). Idempotent: if `new` is already present it counts as done.
FIXES: list[tuple[str, str, str, str]] = [
    (
        "NS-04-leg-gaps",
        "troubleshooting bullet prescribed the faulty 7/10/7 spacing",
        "the Rnd 5 spacing must be 7 sc, 10 sc, 7 sc.",
        KEEP_GAPS,
    ),
    (
        "NS-04-leg-gaps-r3",
        "round-3 bullet spaced the legs evenly but split each pair across the body",
        "- **Coco tips forward or backward.** Most often the front legs are lined up behind "
        "the back legs instead of between them - keep all four leg joins three plain stitches "
        "apart all the way round (back legs over stitches 1-3 and 13-15 of the Rnd-4 round, "
        "front legs over 7-9 and 19-21).",
        KEEP_GAPS,
    ),
    (
        "NS-04-rnd5-row",
        "Rnd 5 row must match the 9-3-12-3-3 explanation (front legs at 7-9 / 19-21)",
        "| R5 | 1 sc, inc, 1 sc, inc, 1 sc, join FL1: 3 sc, [sc, inc] x 3, 1 sc, "
        "join FL2: 3 sc, 3 sc, inc, 2 sc | (30) | join the FRONT legs |",
        R5_ROW_PAIRED,
    ),
    (
        "NS-04-rnd4-row",
        "Rnd 4 must join BOTH back legs, not one at each end of the body",
        "| R4 | join BL1: 3 sc, [sc, inc] x 3, join BL2: 3 sc, [sc, inc] x 3 | (24) | "
        "join the BACK legs |",
        R4_ROW_PAIRED,
    ),
    (
        "NS-04-rnd5-row-r3",
        "round-3 Rnd 5 spaced the legs evenly but split each pair across the body",
        "| R5 | [sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc | "
        "(30) | join the FRONT legs |",
        R5_ROW_PAIRED,
    ),
    (
        "NS-04-rnd4-prose",
        "Rnd 4's prose joined one leg at each end of the body",
        "Rnd 4 - the BACK legs (24 stitches): work the first 3 sc through a leg and the body "
        "together, then [sc, inc] x 3; work the next 3 sc through the second leg and the body "
        "together, then [sc, inc] x 3 to the end of the round.",
        "Rnd 4 - the BACK legs (24 stitches): work the first 3 sc through a leg and the body "
        "together, work sc, inc, then work the next 3 sc through the SECOND leg and the body "
        "together - that is both back legs, three plain stitches apart at the rear - then "
        "[sc, inc] x 5 to the end of the round. In the finished round the back legs sit on "
        "stitches 1-3 and 7-9 of Rnd 4, three plain stitches apart.",
    ),
    (
        "NS-04-rnd5-prose",
        "Rnd 5's prose put the front legs on the opposite quarters from the back legs",
        "In the finished round that is 9 - 3 - 12 - 3 - 3 = 30, all six increases falling "
        "inside the two plain runs. That puts the front legs over stitches 7-9 and 19-21 of "
        "Rnd 4 while the back legs sit over 1-3 and 13-15, so every neighbouring pair of legs "
        "is three plain stitches apart all the way round and the four feet form a rectangle.",
        "In the finished round that is 16 - 3 - 4 - 3 - 4 = 30, all six increases falling "
        "inside the plain runs. Both front legs now sit on the chest, over stitches 13-15 and "
        "19-21 of the Rnd-4 round - three plain stitches apart, and opposite the two back "
        "legs. Each side of the body therefore shows one front and one back leg, never two of "
        "the same pair, and the four feet form a rectangle.",
    ),
    (
        "NS-04-arithmetic",
        "the arithmetic line followed the old increase blocks",
        "Rnd 4: worked = 3 + 6 + 3 + 6 = 18, using EVERY stitch of Rnd 3; made = 3 + 9 + 3 + 9 "
        "= 24. Rnd 5: worked = 6 + 3 + 9 + 3 + 3 = 24, using every stitch of Rnd 4; made = 9 + "
        "3 + 12 + 3 + 3 = 30.",
        "Rnd 4: worked = 3 + 2 + 3 + 10 = 18, using EVERY stitch of Rnd 3; made = 3 + 3 + 3 + "
        "15 = 24. Rnd 5: worked = 12 + 3 + 3 + 3 + 3 = 24, using every stitch of Rnd 4; made = "
        "16 + 3 + 4 + 3 + 4 = 30.",
    ),
    (
        "NS-16-heel-prose",
        "the pickup round began on the wrong side",
        "After Row 10, do not turn. The hook is at one edge of the three-stitch heel centre.",
        "After Row 10, turn - do NOT start the pickup with the row you have just finished "
        "facing you. Ten heel rows is an even number, so a panel worked with a turn at the end "
        "of every row leaves the wrong side out; this last ch 1 and turn put the right side out "
        "for the whole foot. The hook is now at one edge of the three-stitch heel centre.",
    ),
    (
        "NS-04-width",
        "30 stitches at the pattern's 4.5 mm/stitch gauge measure 43 mm, not 34 mm",
        "At thirty stitches and roughly 3.5 mm per stitch the body itself measures about "
        "34 mm across at the leg joins in Rnds 4 and 5",
        "At thirty stitches and 4.5 mm per stitch the body itself measures about 43 mm "
        "across at the Rnd-5 leg join (about 34 mm at Rnd 4)",
    ),
    (
        "NS-04-review-row",
        "review table compared leg centres with plain-stitch gaps",
        "Leg gaps 5/7/3/9 columns: not a rectangle",
        "Plain gaps 2/4/0/6 (leg centres 5/7/3/9 apart) were not a rectangle",
    ),
    (
        "NS-04-review-fix",
        "the row called 7/10/7 the fix — it is the layout that produces 2/4/0/6",
        "resolved with explicit 7/10/7 joins",
        "resolved by re-spacing Rnd 5 so all four joins are 3 plain stitches apart "
        "(7/10/7 was the faulty layout)",
    ),
    (
        "NS-04-review-gauge",
        "review table reused the 3.5 mm/stitch figure",
        "30 stitches at ~3.5 mm give ~34 mm across the body",
        "30 stitches at 4.5 mm give about 43 mm across the body (34 mm at Rnd 4)",
    ),
    (
        "NS-06-base-width",
        "36-stitch cat base is 39 mm across at 4.5 mm/stitch, not 34 mm",
        "Stopping at 36 gives a body about 34 mm across",
        "Stopping at 36 gives a body about 39 mm across",
    ),
    (
        "NS-12-stuffing",
        "25 g contradicts 'a little only'; the piece holds under 150 cm3",
        "fibre fill about 25 g (a little only",
        "fibre fill about 5 g (a little only",
    ),
    (
        "NS-13-star-size",
        "a 10-stitch ring plus five 6-stitch fans makes a ~4.5 cm star, not 9 cm",
        "star about 9 cm (3.5 in)",
        "star about 4.5 cm (1.75 in)",
    ),
    (
        "NS-14-brand",
        "cover brand line should match the other 16 covers",
        "# NOVALITY CROCHET STUDIO — PRINTER-SAVER EDITION",
        "# NOVALITY STORE — PRINTER-SAVER EDITION",
    ),
    (
        "NS-16-heel-turn",
        "ten flat heel rows finish wrong side out; the pickup round must start on the RS",
        "| Row 10 | 2 sc, dec; do not turn | (3) | heel centre |",
        R10_ROW_TURNED,
    ),
    (
        "NS-01-hoof-change",
        "the hoof colour change belongs in the row, not in the note column",
        "| R6 | BLO sc around | (18) | change to Yarn A - ridge |",
        "| R6 | BLO sc in 17, BLO sc in last st; change to Yarn A | (18) | hooves start here - ridge |",
    ),
    (
        "NS-03-tail-pairs",
        "'3 front + 3 back' reads like six stitches that need three sc each",
        "fold the last 6 stitches flat so 3 pairs line up (3 front + 3 back)",
        "fold the last 6 stitches flat so they line up as 3 pairs (each pair is one front "
        "and one back stitch)",
    ),
    (
        "NS-17-collar-gauge",
        "NS-17 is worked in worsted, and 5 mm/stitch gives the stated 6.5 cm",
        "about 6.5 cm relaxed at DK gauge",
        "about 6.5 cm relaxed at the pattern's worsted gauge",
    ),
]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    text = args.path.read_text(encoding="utf-8")
    applied, present, missing = [], [], []

    for fix_id, why, pattern, repl in BLOCK_FIXES:
        if re.search(pattern, text, flags=re.S):
            text = re.sub(pattern, repl, text, flags=re.S)
            applied.append(fix_id)
            print(f"applied  {fix_id:20s} {why}")
        else:
            present.append(fix_id)

    for fix_id, why, old, new in FIXES:
        if new in text:
            present.append(fix_id)
        elif old in text:
            text = text.replace(old, new)
            applied.append(fix_id)
            print(f"applied  {fix_id:20s} {why}")
        else:
            missing.append(fix_id)
            print(f"MISSING  {fix_id:20s} {why}\n         expected to find: {old[:90]!r}")

    if args.dry_run:
        print(f"\ndry run: {len(applied)} fixable, {len(present)} already present, "
              f"{len(missing)} not located")
    else:
        args.path.write_text(text, encoding="utf-8")
        print(f"\n{args.path}: {len(applied)} applied, {len(present)} already present, "
              f"{len(missing)} not located")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
