"""Christmas Collection - NS 12 - Bobble Christmas Tree (US terms)."""

PATTERN = {
    "id": "tree",
    "assets_key": "x02",
    "number": 102,
    "design_code": "NS 12",
    "title": "Bobble Christmas Tree",
    "tagline": ("A soft standing fir built in one piece: plain rounds, then tier "
                "after tier of popcorn bobbles that thin out toward the tip. "
                "Contrast-colour bobbles turn it into baubles-on-a-tree in a "
                "single round."),
    "meta": ["US terms", "Easy - Intermediate", "2 - 3 hours"],
    "finished_size": [
        "About 12 cm (4.7 in) tall and 7 cm (2.8 in) wide in worsted / aran on "
        "a 4 mm hook.",
        "About 15-16 cm tall in chunky yarn on a 5 mm hook.",
        "One piece; a felt or cardboard base disc is optional.",
    ],
    "safety": [
        "No small parts unless you add decorations or beads for baubles - for "
        "young children, use only the contrast-colour bobbles (worked in) and "
        "no glued or sewn embellishments.",
        "Not tested to a toy-safety standard (ASTM F963 / EN 71). Stuff firmly "
        "and weave every end in at least 5 cm.",
    ],
    "materials": [
        "Main yarn: worsted / aran (#4) in green, 60-80 g.",
        "Contrast (optional): small amounts of red, gold, cream for contrast bobbles.",
        "Hook: 4 mm (US G-6); use 3 mm for DK mini, 5 mm for chunky.",
        "Stuffing: fibre fill about 25 g (a little only - the tree stands on tension).",
        "Optional: 1 circle (~45 mm) of cardboard or felt for a firmer base.",
        "Notions: stitch marker, tapestry needle, scissors.",
    ],
    "gauge": [
        "Aim for a firm fabric (~10-11 sc x 11 rounds = 5 cm). Exact size is not "
        "critical; droopy bobbles mean too much stuffing - the shell should hold "
        "its cone almost on its own.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sl st - slip stitch",
        "sc - single crochet", "inc - increase (2 sc in one st)",
        "sc2tog - work 2 stitches together as one (a decrease)",
        "BLO - back loop only", "BO - 5-dc bobble (counts as 1 st)",
        "FO - fasten off", "st(s) - stitch(es)", "R - round",
        "(n) - stitch count at round end",
    ],
    "abbreviations_uk": [
        "MR - magic ring", "ch - chain", "sl st - slip stitch",
        "dc - double crochet", "inc - increase (2 dc in one st)",
        "dc2tog - work 2 stitches together as one (a decrease)",
        "BLO - back loop only", "BO - 5-tr bobble (counts as 1 st)",
        "FO - fasten off", "st(s) - stitch(es)", "R - round",
        "(n) - stitch count at round end",
    ],
    "construction": ("Worked in continuous rounds from the base up - no joins, no "
                     "starting chains. The BLO round (R9) kicks the fabric out from "
                     "the flat base into the cone. Bobble rounds alternate with "
                     "plain rounds; every bobble round from R12 onward hides one "
                     "sc2tog per repeat, so the cone tapers evenly and the bobbles "
                     "stay in straight columns."),
    "techniques": [
        ("The magic ring", "Work 6 sc into a ring and pull the tail tight."),
        ("Back loop only (BLO)",
         "Work into the far loop only. The unused front loops form a ridge that "
         "makes the base fold neatly under the tree."),
        ("The 5-dc bobble",
         "Yarn over, insert hook, pull up a loop, yarn over, pull through 2 loops "
         "(incomplete dc). Repeat 4 more times in the same stitch - 6 loops on "
         "hook - then yarn over and pull through all 6. Counts as ONE stitch."),
        ("Contrast bobbles",
         "Change to the contrast colour on the final yarn-over of each bobble, "
         "work the closing pull-through in contrast, then pick the green back up "
         "in the very next stitch. The green floats behind the fabric."),
        ("sc2tog decrease", "One decrease per repeat hides inside each bobble "
         "round, always in the LAST position, so the bobble columns stay straight."),
    ],
    "notes": [],
    "pieces": [
        {
            "name": "1. Tree - one piece, green (contrast optional)",
            "intro": ("The cone grows between every two bobble rows; the plain "
                      "round between them keeps each tier distinct. Begin stuffing "
                      "at R24 - before then the cone should stay fairly flat."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "inc in each st around", "stated": 12, "cons": 6, "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3", "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4", "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": ""},
                    {"label": "R5", "text": "[3 sc, inc] x 6", "stated": 30, "cons": 24, "prod": 30, "check": "[3 sc, inc] x 6", "note": ""},
                    {"label": "R6", "text": "[4 sc, inc] x 6", "stated": 36, "cons": 30, "prod": 36, "check": "[4 sc, inc] x 6", "note": ""},
                    {"label": "R7", "text": "[5 sc, inc] x 6", "stated": 42, "cons": 36, "prod": 42, "check": "[5 sc, inc] x 6", "note": ""},
                    {"label": "R8", "text": "[6 sc, inc] x 6", "stated": 48, "cons": 42, "prod": 48, "check": "[6 sc, inc] x 6", "note": "base = full width"},
                    {"label": "R9", "text": "BLO: sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": "base fold ridge"},
                    {"label": "R10", "text": "[BO, 7 sc] x 6", "stated": 48, "cons": 48, "prod": 48, "check": None, "note": "first bobble tier"},
                    {"label": "R11", "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": ""},
                    {"label": "R12", "text": "[BO, 5 sc, sc2tog] x 6", "stated": 42, "cons": 48, "prod": 42, "check": None, "note": ""},
                    {"label": "R13", "text": "sc in each st around", "stated": 42, "cons": 42, "prod": 42, "check": "sc in each st around", "note": ""},
                    {"label": "R14", "text": "[BO, 4 sc, sc2tog] x 6", "stated": 36, "cons": 42, "prod": 36, "check": None, "note": ""},
                    {"label": "R15", "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": ""},
                    {"label": "R16", "text": "[BO, 3 sc, sc2tog] x 6", "stated": 30, "cons": 36, "prod": 30, "check": None, "note": ""},
                    {"label": "R17", "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R18", "text": "[BO, 2 sc, sc2tog] x 6", "stated": 24, "cons": 30, "prod": 24, "check": None, "note": ""},
                    {"label": "R19", "text": "sc in each st around", "stated": 24, "cons": 24, "prod": 24, "check": "sc in each st around", "note": ""},
                    {"label": "R20", "text": "[BO, sc, sc2tog] x 6", "stated": 18, "cons": 24, "prod": 18, "check": None, "note": ""},
                    {"label": "R21", "text": "sc in each st around", "stated": 18, "cons": 18, "prod": 18, "check": "sc in each st around", "note": ""},
                    {"label": "R22", "text": "[BO, sc2tog] x 6", "stated": 12, "cons": 18, "prod": 12, "check": None, "note": "bobble tier at tip - each repeat uses 3 sts, makes 2"},
                    {"label": "R23", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R24", "text": "sc2tog x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": "stuff cone lightly now"},
                    {"label": "R25", "text": "sc in each st around", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                    {"label": "R26", "text": "sc2tog x 3", "stated": 3, "cons": 6, "prod": 3, "check": "dec x 3", "note": "tip"},
                ], "notes": [
                    "Finish: FO with a tail, thread through the last 3 stitches, "
                    "pull the tip closed and weave the end down through the tree.",
                    "Stuffing: only the bottom half needs real fill - a lightly "
                    "stuffed cone that flexes is nicer than a rigid one. Slip the "
                    "cardboard or felt disc inside the base BEFORE the final "
                    "stuffing if you add one.",
                ]},
            ],
        },
    ],
    "assembly": [
        "Contrast bobbles: change colour on the bobble's final pull-through, "
        "change back on the next stitch. One or two contrast tiers look best.",
        "Base: for a shelf-keeper, pinch the R9 ridge flat and hold the felt or "
        "cardboard disc to the base while you finish stuffing, then close.",
        "Hanging: join any colour at the tip, ch 18, sl st into the same place.",
        "Set of three: DK + 3 mm hook, worsted + 4 mm hook, chunky + 5 mm hook - "
        "counts are identical, sizes stair-step from about 9 cm to 16 cm.",
    ],
    "troubleshooting": [
        ("Bobble columns wander.",
         "Your round start drifted with the spiral - a stitch marker in the first "
         "stitch of every round keeps the repeat anchored. A little lag looks "
         "natural: real fir boughs point downhill too."),
        ("Tip flops.",
         "Over-stuffed at the top. Take two pinches of stuffing out of the cone "
         "tip and re-cinch R26 tightly."),
        ("Base will not sit flat.",
         "You skipped the BLO ridge (R9) or worked it loosely. That ridge is the "
         "fold - re-press it with a fingernail while shaping."),
    ],
    "colorways": ["Fir green", "Sage velvet", "Snow white", "Crimson berry", "Gold-tipped"],
    "extras": [],
    "designer_notes": [
        "Why every bobble tier shrinks by 6: each [BO, k sc, sc2tog] repeat works "
        "one hidden decrease, at the END of the repeat, so the bobbles never "
        "drift out of their columns even while the cone narrows 10 rounds in a "
        "row. R22 is the extreme case: [BO, sc2tog] uses 3 sts and makes 2 per "
        "repeat - 18 sts used, 12 left, nothing unworked.",
    ],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original work "
                      "and intellectual property of Novality Store, designed by "
                      "Novality Crochet Studio. Design Code NS 12."),
        "may": ("Make as many finished trees as you like for yourself, gifts, or "
                "charity. Sell physical finished items made from this pattern in "
                "small batches, in shops, markets and online, provided credit is "
                "given to \"Novality Store\"."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos beyond crediting "
                   "the pattern. Do not mass-produce finished items commercially "
                   "without written permission."),
        "safety": ("This pattern has not been tested to a toy-safety standard "
                   "(ASTM F963 / EN 71). Avoid beads or glued decorations for items "
                   "intended for young children."),
    },
    "hashtag": "#NovalityTree",
    "closing": ("Show us your forest. Thank you for supporting an independent "
                "pattern designer."),
}
