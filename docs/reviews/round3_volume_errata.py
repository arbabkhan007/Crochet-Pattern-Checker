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
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# (id, description, old, new). Idempotent: if `new` is already present it counts as done.
FIXES: list[tuple[str, str, str, str]] = [
    (
        "NS-04-leg-gaps",
        "troubleshooting bullet prescribed the faulty 7/10/7 spacing",
        "the Rnd 5 spacing must be 7 sc, 10 sc, 7 sc.",
        "keep all four leg joins three plain stitches apart all the way round "
        "(back legs over stitches 1-3 and 13-15 of the Rnd-4 round, front legs over "
        "7-9 and 19-21).",
    ),
    (
        "NS-04-rnd5-row",
        "Rnd 5 row must match the 9-3-12-3-3 explanation (front legs at 7-9 / 19-21)",
        "| R5 | 1 sc, inc, 1 sc, inc, 1 sc, join FL1: 3 sc, [sc, inc] x 3, 1 sc, "
        "join FL2: 3 sc, 3 sc, inc, 2 sc | (30) | join the FRONT legs |",
        "| R5 | [sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc | "
        "(30) | join the FRONT legs |",
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
