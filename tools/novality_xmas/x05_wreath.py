"""Christmas Collection - NS 15 - Interchangeable Christmas Wreath (validated).

Data module for the audit harness. Source: user's Q4 draft #2 part B.
Correction baked in (see designer_notes / audit report):
- Poinsettia petal round clarified: one petal per centre stitch, six petals
  using all six centre stitches (draft's "six times in the same centre
  stitch" was ambiguous).
"""

def row(label, text, stated=None, cons=None, prod=None, note=""):
    return {"label": label, "text": text, "stated": stated,
            "cons": cons, "prod": prod, "check": None, "note": note}


PATTERN = {
    "id": "wreath",
    "design_code": "NS 15",
    "hashtag": "#NovalityWreath",
    "closing": "swap the decoration, swap the mood",
    "title": "Interchangeable Christmas Wreath",
    "tagline": ("A stuffed spiral tube joined into a ring, dressed for the "
                "season with three REMOVABLE decorations: poinsettia, lace "
                "snowflake and a gift-bow. Swap them as the holidays change. "
                "Mini ornament, standard door and large door sizes."),
    "meta": ["US terms", "Beginner", "tube grows by length"],
    "finished_size": [
        "Mini ornament wreath: 20-24 in (51-61 cm) tube, about 16-19 cm across.",
        "Standard door wreath: 34-38 in (86-97 cm) tube, about 10-12 in (25-30 cm) across.",
        "Large door wreath: 47-52 in (119-132 cm) tube, about 38-42 cm across.",
        "Poinsettia approx. 3-4 in; snowflake approx. 4 in; bow approx. 3-4 in wide.",
    ],
    "safety": [
        "Home decor, not a toy. A stuffed wreath is heavier than it looks - "
        "hang it on a proper hook, not a suction cup.",
    ],
    "materials": [
        "Wreath base: 150-200 g green worsted/aran (#4), 4 mm hook, fibre fill.",
        "Decorations: small amounts of red, white, yellow, green, optional "
        "black and gold thread; 3.5-4 mm hook.",
        "Optional jingle bell, ribbon, gold thread.",
        "Notions: stitch marker, scissors, tapestry needle.",
    ],
    "gauge": [
        "Gauge is not critical - the tube is a constant 12 stitches and "
        "wreath size comes from tube LENGTH. Measure the tube, not the round "
        "count.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sl st - slip stitch",
        "sc - single crochet", "hdc - half double crochet",
        "dc - double crochet", "tr - treble crochet",
        "st(s) - stitch(es)", "R - round",
        "(n) - stitch count at round end",
    ],
    "abbreviations_uk": [
        "MR - magic ring", "ch - chain", "sl st - slip stitch",
        "dc - double crochet", "htr - half treble crochet",
        "tr - treble crochet", "dtr - double treble crochet",
        "st(s) - stitch(es)", "R - round",
        "(n) - stitch count at round end",
    ],
    "construction": ("Wreath base: continuous spiral rounds (no joins - use "
                     "a marker). Decorations: joined rounds for flowers and "
                     "snowflake, short worked rows for the bow."),
    "techniques": [
        ("The constant stitch tube",
         "Every tube round is exactly 12 sc - no increases, no decreases. "
         "Tube length sets wreath size: measure against the door/table and "
         "stop after a complete round."),
        ("Joining the tube",
         "Flatten both ends, sl st through matching stitches of near and "
         "far ends across all 12 pairs, then massage the tube into a circle."),
        ("Snowflake arm (shared with NS 13)",
         "Into each ch-5 space: (sl st, ch 3, 3 tr, ch 3, sl st). First sl "
         "st loose, last sl st snug so the arm lies flat and stands upright."),
        ("Removable attachments",
         "Every decoration gets a ch-18 loop so it lifts off the wreath; "
         "never sew decorations permanently - interchangeability is the point."),
    ],
    "notes": [
        "US rounds counts are written by hand below; the wreath grows by "
        "LENGTH, so these remain reference counts - always measure the "
        "tube.",
    ],
    "pieces": [
        {"name": "1. Wreath base - padded tube",
         "intro": ("Continuous spiral, constant 12 sts. Stuff lightly every "
                   "5-8 rounds; keep it bendable, and do not overstuff the "
                   "last 10 rounds."),
         "subpieces": [
            {"name": "Starting ring & tube",
             "rows": [
                 row("", "Ch 12, sl st to first ch to form a ring; place marker",
                     None, None, None, "ring"),
                 row("R1", "Sc in each ch around", 12, None, 12),
                 row("R2+", "Sc in each st around until tube measures the "
                     "target length (see table)", 12, 12, 12,
                     "estimate: mini 90-105 rnds / standard 140-160 / "
                     "large 190-215 - MEASURE the tube"),
                 row("Join", "Sl st through matching sts of both tube ends "
                     "across all 12 pairs, FO", None, None, None, "skip-check: "
                     "joins 12 near-end + 12 far-end pairs = 12 joins"),
                 row("Loop", "Join green at top, ch 20, sl st to same point, FO",
                     None, None, None, "hanging loop"),
             ]},
         ]},
        {"name": "2. Poinsettia (removable)",
         "intro": "Yellow centre, six red petals, three green leaves.",
         "subpieces": [
            {"name": "Flower",
             "rows": [
                 row("R1", "With yellow: 6 sc in MR, sl st to first sc, FO",
                     6, None, 6, "centre"),
                 row("Petals", "Join red in any centre sc; [ch 4, 3 tr, ch 4, sl st] "
                     "in the same st, then repeat once in each of the "
                     "remaining 5 centre sc", None, 6, 24, "CORRECTED: one "
                     "petal per centre st - 6 petals total; per petal 3 tr "
                     "+ 1 sl st = 4 sts + 2 ch-4 loops"),
                 row("Leaves", "With green: per leaf - ch 8, sc in 2nd ch "
                     "from hook, hdc, dc in next 3, hdc, sc, sl st to "
                     "flower centre; make 3 leaves", None, None, None,
                     "skip-check: 7 of 8 chains used per leaf, 3 leaves"),
                 row("Loop", "Join green at back, ch 18, sl st to same point, FO",
                     None, None, None, "removable attachment"),
             ]},
         ]},
        {"name": "3. Snowflake (removable)",
         "intro": "White, joined rounds; block flat.",
         "subpieces": [
            {"name": "Snowflake",
             "rows": [
                 row("R1", "With white: MR, ch 3 (counts as first dc), 11 dc "
                     "in ring, sl st to top of ch-3", 12, None, 12, "12 spokes"),
                 row("R2", "[Ch 5, skip next dc, sl st in next dc] x 6",
                     6, 12, 6, "6 ch-5 spaces; skip-check counts as spaces"),
                 row("R3", "Sl st into each ch-5 space in turn; in each space "
                     "work (sl st, ch 3, 3 tr, ch 3, sl st)", 6, None, None,
                     "skip-check: 6 arms; per arm 3 tr + 2 sl st = 5 sts"),
                 row("Loop", "Join white/silver in one point, ch 18, sl st "
                     "to same point, FO", None, None, None,
                     "optional second loop on opposite point for centred hang"),
             ]},
         ]},
        {"name": "4. Holiday bow (removable)",
         "intro": "Two chain loops, two tails, one little centre band.",
         "subpieces": [
            {"name": "Bow",
             "rows": [
                 row("Loops", "With red: ch 24, sl st to first ch (loop 1 - "
                     "untwisted); ch 24 again, sl st to same base point (loop 2)",
                     None, None, None, "skip-check: two 24-ch loops"),
                 row("Tails", "Ch 15, sc in 2nd ch from hook and across "
                     "(14 sc), sl st to bow base; repeat for second tail",
                     14, None, 14, "15 chains make 14 sc, x2 tails"),
                 row("Band", "Ch 6, sc in 2nd ch from hook and across (5); "
                     "rows 2-4: ch 1, turn, sc across (5)", 5, None, 5,
                     "separate little rectangle: 4 rows of 5; wrap around "
                     "bow centre, sl st short ends"),
             ]},
         ]},
        {"name": "5. Mini wreath ornament (optional)",
         "intro": "DK yarn, 3 mm hook, 8-st tube.",
         "subpieces": [
            {"name": "Mini tube",
             "rows": [
                 row("", "Ch 8 ring; sc in each ch (8); spiral rounds of 8 sc "
                     "until 20-24 cm; join ends as base; ch 14 hanging loop",
                     8, None, 8, "skip-check: constant 8-st tube"),
             ]},
         ]},
    ],
    "assembly": [
        "Stuff the tube as you go - after every 5-8 rounds is far easier "
        "than stuffing a finished tube.",
        "Join the tube LAST: slip stitch across all 12 stitch pairs, then "
        "massage it circular on a flat table.",
        "Every decoration hangs from a ch-18 loop; wrap loops around one "
        "wreath stitch or tie to ribbon - nothing is sewn forever.",
    ],
    "troubleshooting": [
        ("Tube is stiff like a rope.", "Over-stuffed - pull a pinch of fill "
         "per handful back out; the wreath must flex into a circle."),
        ("Wreath will not hold a circle.", "Under-stuffed at the join - add "
         "a thin worm of fill through the join stitches, or wrap the join "
         "with spare yarn like a bandage."),
        ("Poinsettia petals cluster on one side.", "Each petal goes into "
         "its OWN centre stitch, moving stitch by stitch around the six - "
         "not all six into one stitch."),
    ],
    "colorways": ["Classic green & red", "Winter white & gold",
                  "Berry wreath", "Neutral farmhouse green"],
    "extras": [
        {"name": "Sizes at a glance", "type": "table",
         "headers": ["Wreath", "Tube length", "Est. rounds", "Approx. diameter"],
         "rows": [["Mini ornament", "20-24 in / 51-61 cm", "90-105", "16-19 cm"],
                  ["Standard door", "34-38 in / 86-97 cm", "140-160", "25-30 cm"],
                  ["Large door", "47-52 in / 119-132 cm", "190-215", "38-42 cm"]],
         "outro": "Rounds are estimates only - measure the tube."},
    ],
    "designer_notes": [
        "Validation correction (from the Q4 draft): the poinsettia petal "
        "instruction is now pinned to one petal per centre stitch - six "
        "petals using all six centre stitches. The draft's 'six times in "
        "the same centre stitch' would stack every petal on one stitch.",
    ],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, "
                      "stitch counts, photography and design elements - is "
                      "the original work and intellectual property of "
                      "Novality Store, designed by Novality Crochet Studio. "
                      "Design Code NS 15."),
        "may": ("Make as many finished wreaths as you like for yourself, "
                "gifts, or charity. Sell physical finished items made from "
                "this pattern in small quantities with credit to Novality "
                "Store."),
        "maynot": ("Sell, share, copy or redistribute this pattern or any "
                   "part of it. Claim the pattern as your own design. "
                   "Produce items from this pattern as a factory or "
                   "manufacturer."),
        "safety": ("Home decor item - not a toy. Keep away from open "
                   "flames; hang securely."),
    },
}
