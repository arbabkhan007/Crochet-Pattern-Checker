"""Christmas Collection - NS 14 - Bobble Snowflake Tree Skirt (validated).

Data module for the audit harness. Source: user's Q4 draft #2 part A.
Corrections baked in (see designer_notes / audit report):
- R9: [dc 7, inc] (draft said 6) - consumption must divide 96
- R10: [dc 8, inc] (draft said 7) - consumption must divide 108
"""

def row(label, text, stated=None, cons=None, prod=None, note=""):
    return {"label": label, "text": text, "stated": stated,
            "cons": cons, "prod": prod, "check": None, "note": note}


PATTERN = {
    "id": "treeskirt",
    "design_code": "NS 14",
    "hashtag": "#NovalityTreeSkirt",
    "closing": "lay it under the tree, plug in the lights, and step back",
    "title": "Bobble Snowflake Tree Skirt",
    "tagline": ("A flat twelve-spoke circle of double crochet with a bobble "
                "snowflake blooming every third round. Closed centre ring - "
                "slip it over the stand before the tree goes up. Mini, "
                "standard and large sizes from the same twelve-columns math."),
    "meta": ["US terms", "Easy - Intermediate", "grows by size"],
    "finished_size": [
        "Mini / tabletop: stop after R14 - 18-21 in (46-53 cm) across.",
        "Standard: stop after R23 - 29-33 in (74-84 cm) across.",
        "Large: stop after R32 - 38-43 in (97-109 cm) across.",
        "Centre hole approximately 1.5-2 in unstretched (verify against your "
        "tree stand; ch 24 at the start for a larger opening).",
    ],
    "safety": [
        "Home decor, not a toy. Keep loose skirts away from open flames and "
        "hot lights; use LED tree lights."
    ],
    "materials": [
        "Worsted or aran (#4) yarn, 700-1,200 g for standard or large skirt.",
        "Hook: 5-5.5 mm.",
        "Optional contrast yarn (CC) for bobble rounds and surface lines.",
        "Notions: stitch marker, scissors, tapestry needle.",
    ],
    "gauge": [
        "Flat swatch in US dc, blocked lightly: 12 dc = 4 in (10 cm); "
        "6 rounds = 4 in (10 cm). Measure the actual skirt as it grows.",
    ],
    "abbreviations": [
        "MR - slip knot ring (ch 20 here)", "ch - chain", "sl st - slip stitch",
        "sc - single crochet", "dc - double crochet",
        "BO - 5-dc bobble (counts as 1 st)", "MC - main colour",
        "CC - contrast colour", "st(s) - stitch(es)", "R - round",
        "(n) - stitch count at round end",
    ],
    "abbreviations_uk": [
        "MR - slip knot ring (ch 20 here)", "ch - chain", "sl st - slip stitch",
        "dc - double crochet", "tr - treble crochet",
        "BO - 5-tr bobble (counts as 1 st)", "MC - main colour",
        "CC - contrast colour", "st(s) - stitch(es)", "R - round",
        "(n) - stitch count at round end",
    ],
    "construction": ("Closed rounds, joined - do not turn. Ch 2 at round "
                     "start never counts as a stitch; slip stitch to the "
                     "first actual dc at the end of each round. Twelve "
                     "increase columns, +12 stitches every round; every "
                     "third round from R5 is a bobble round (in CC if you "
                     "like)."),
    "techniques": [
        ("The 12-spoke circle",
         "Round N of the growth ladder consumes N-1 and produces N stitches "
         "per each of its 12 repeats, so the stitch total after round N is "
         "always exactly 12 x N. R9 needs 7 plain dc and R10 needs 8 - one "
         "fewer and you run out of stitches before the round closes."),
        ("The 5-dc bobble",
         "Yarn over, insert hook, pull up a loop, yarn over, pull through 2 "
         "loops (incomplete dc). Repeat 4 more times in the same stitch "
         "(6 loops on hook). Yarn over, pull through all 6. One bobble "
         "counts as ONE stitch; push it to the front."),
        ("Changing colour at a join",
         "Work the final slip stitch of the round with the new colour, then "
         "begin the next round with it - no visible step."),
        ("Surface snowflake spokes",
         "Surface slip stitches up each of the 12 increase columns in CC "
         "with a smaller hook. Keep them loose so the skirt stays flat."),
    ],
    "notes": [
        "Sizes are approximate - yarn, hook and tension change the diameter. "
        "Measure the lying-flat skirt against your tree stand before "
        "committing to a border.",
    ],
    "pieces": [
        {"name": "1. Skirt - center ring and growth rounds",
         "intro": ("Ch 2 starts every round (never counted). End every "
                   "round with sl st to the first dc (first BO on bobble "
                   "rounds). Worked flat and circular throughout."),
         "subpieces": [
            {"name": "Centre ring",
             "rows": [
                 row("", "Ch 20, sl st to first ch to form a ring", None,
                     None, None, "trunk opening; ch 24 for a larger one"),
             ]},
            {"name": "Rounds 1-8",
             "rows": [
                 row("R1", "Ch 2, 12 dc in ring, sl st to first dc", 12,
                     None, 12),
                 row("R2", "Ch 2, 2 dc in each st around, sl st to first dc",
                     24, 12, 24),
                 row("R3", "Ch 2, [dc in next st, 2 dc in next st] x 12, sl st to first dc",
                     36, 24, 36),
                 row("R4", "Ch 2, [dc in next 2 sts, 2 dc in next st] x 12, sl st to first dc",
                     48, 36, 48),
                 row("R5", "Ch 2, [BO in next st, dc in next 2 sts, 2 dc in next st] x 12, sl st to first BO",
                     60, 48, 60, "first bobble round"),
                 row("R6", "Ch 2, [dc in next 4 sts, 2 dc in next st] x 12, sl st to first dc",
                     72, 60, 72),
                 row("R7", "Ch 2, [dc in next 5 sts, 2 dc in next st] x 12, sl st to first dc",
                     84, 72, 84),
                 row("R8", "Ch 2, [BO in next st, dc in next 5 sts, 2 dc in next st] x 12, sl st to first BO",
                     96, 84, 96),
             ]},
            {"name": "Rounds 9-16",
             "rows": [
                 row("R9", "Ch 2, [dc in next 7 sts, 2 dc in next st] x 12, sl st to first dc",
                     108, 96, 108, "CORRECTED from draft (was dc 6)"),
                 row("R10", "Ch 2, [dc in next 8 sts, 2 dc in next st] x 12, sl st to first dc",
                     120, 108, 120, "CORRECTED from draft (was dc 7)"),
                 row("R11", "Ch 2, [BO in next st, dc in next 8 sts, 2 dc in next st] x 12, sl st to first BO",
                     132, 120, 132),
                 row("R12", "Ch 2, [dc in next 10 sts, 2 dc in next st] x 12, sl st to first dc",
                     144, 132, 144),
                 row("R13", "Ch 2, [dc in next 11 sts, 2 dc in next st] x 12, sl st to first dc",
                     156, 144, 156),
                 row("R14", "Ch 2, [BO in next st, dc in next 11 sts, 2 dc in next st] x 12, sl st to first BO",
                     168, 156, 168, "MINI SIZE - continue to border here"),
                 row("R15", "Ch 2, [dc in next 13 sts, 2 dc in next st] x 12, sl st to first dc",
                     180, 168, 180),
                 row("R16", "Ch 2, [dc in next 14 sts, 2 dc in next st] x 12, sl st to first dc",
                     192, 180, 192),
             ]},
            {"name": "Rounds 17-24",
             "rows": [
                 row("R17", "Ch 2, [BO in next st, dc in next 14 sts, 2 dc in next st] x 12, sl st to first BO",
                     204, 192, 204),
                 row("R18", "Ch 2, [dc in next 16 sts, 2 dc in next st] x 12, sl st to first dc",
                     216, 204, 216),
                 row("R19", "Ch 2, [dc in next 17 sts, 2 dc in next st] x 12, sl st to first dc",
                     228, 216, 228),
                 row("R20", "Ch 2, [BO in next st, dc in next 17 sts, 2 dc in next st] x 12, sl st to first BO",
                     240, 228, 240),
                 row("R21", "Ch 2, [dc in next 19 sts, 2 dc in next st] x 12, sl st to first dc",
                     252, 240, 252),
                 row("R22", "Ch 2, [dc in next 20 sts, 2 dc in next st] x 12, sl st to first dc",
                     264, 252, 264),
                 row("R23", "Ch 2, [BO in next st, dc in next 20 sts, 2 dc in next st] x 12, sl st to first BO",
                     276, 264, 276, "STANDARD SIZE - continue to border here"),
                 row("R24", "Ch 2, [dc in next 22 sts, 2 dc in next st] x 12, sl st to first dc",
                     288, 276, 288),
             ]},
            {"name": "Rounds 25-32",
             "rows": [
                 row("R25", "Ch 2, [dc in next 23 sts, 2 dc in next st] x 12, sl st to first dc",
                     300, 288, 300),
                 row("R26", "Ch 2, [BO in next st, dc in next 23 sts, 2 dc in next st] x 12, sl st to first BO",
                     312, 300, 312),
                 row("R27", "Ch 2, [dc in next 25 sts, 2 dc in next st] x 12, sl st to first dc",
                     324, 312, 324),
                 row("R28", "Ch 2, [dc in next 26 sts, 2 dc in next st] x 12, sl st to first dc",
                     336, 324, 336),
                 row("R29", "Ch 2, [BO in next st, dc in next 26 sts, 2 dc in next st] x 12, sl st to first BO",
                     348, 336, 348),
                 row("R30", "Ch 2, [dc in next 28 sts, 2 dc in next st] x 12, sl st to first dc",
                     360, 348, 360),
                 row("R31", "Ch 2, [dc in next 29 sts, 2 dc in next st] x 12, sl st to first dc",
                     372, 360, 372),
                 row("R32", "Ch 2, [BO in next st, dc in next 29 sts, 2 dc in next st] x 12, sl st to first BO",
                     384, 372, 384, "LARGE SIZE - continue to border here"),
             ]},
            {"name": "Scalloped border (skip-check: motif edge)",
             "rows": [
                 row("", "Join CC in any st; ch 1, [sc in next st, skip 2 sts, 5 dc in next st, skip 2 sts] around, sl st to first sc, FO",
                     None, None, None, "repeats consume 6 sts each; R14 "
                     "gives 28, R23 gives 46, R32 gives 64 scallops"),
             ]},
            {"name": "Surface snowflake lines (optional, skip-check)",
             "rows": [
                 row("", "Join CC beside an increase column at the centre; "
                     "surface sl st outward over each of the 12 columns, FO",
                     None, None, None, "12 spokes, one per increase column"),
             ]},
         ]},
    ],
    "assembly": [
        "Weave all ends on the wrong side.",
        "Block lightly to a flat circle; a gentle border wave is the design.",
        "Measure the centre opening against the tree stand before listing "
        "photos; photograph under a decorated tree AND flat on the floor.",
    ],
    "troubleshooting": [
        ("Skirt ruffles like a lettuce leaf.", "Too many increases for your "
         "tension - the ladder is exactly +12 per round, so the fix is "
         "tension or a smaller hook, not extra stitches."),
        ("Skirt cups like a bowl.", "Too few increases reaching the round "
         "end - check R9 (7 plain dc) and R10 (8) first; one plain dc short "
         "leaves 12 stitches unworked at round end."),
        ("Bobbles will not pop.", "Work the 5 dc loosely and push each bobble "
         "to the front as it closes; CC bobbles read best."),
    ],
    "colorways": ["Forest & cream", "Snow white & red scallops",
                  "Navy & silver", "Single-colour cream"],
    "extras": [
        {"name": "Sizes at a glance", "type": "table",
         "headers": ["Size", "Stop after round", "Stitches", "Border scallops", "Approx. diameter"],
         "rows": [["Mini/tabletop", "R14", "168", "28", "18-21 in / 46-53 cm"],
                  ["Standard", "R23", "276", "46", "29-33 in / 74-84 cm"],
                  ["Large", "R32", "384", "64", "38-43 in / 97-109 cm"]],
         "outro": "All three endings are divisible by 6, so the scallop "
                  "border closes cleanly at every size."},
    ],
    "designer_notes": [
        "Validation corrections (from the Q4 draft): R9 needs 7 plain dc "
        "(96 to 108) and R10 needs 8 (108 to 120); the draft's 6 and 7 "
        "consume too few stitches and the round cannot close at the stated "
        "count. Round N always consumes N-1 per repeat.",
    ],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, "
                      "stitch counts, photography and design elements - is "
                      "the original work and intellectual property of "
                      "Novality Store, designed by Novality Crochet Studio. "
                      "Design Code NS 14."),
        "may": ("Make as many finished skirts as you like for yourself, "
                "gifts, or charity. Sell physical finished items made from "
                "this pattern in small quantities with credit to Novality "
                "Store."),
        "maynot": ("Sell, share, copy or redistribute this pattern or any "
                   "part of it. Claim the pattern as your own design. "
                   "Produce items from this pattern as a factory or "
                   "manufacturer."),
        "safety": ("Home decor item - not a toy and not flameproof. Use "
                   "cool LED lights on the tree."),
    },
}
