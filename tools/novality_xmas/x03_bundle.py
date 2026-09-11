"""Christmas Collection - NS X03 - Christmas Ornament Bundle (US terms)."""

PATTERN = {
    "id": "bundle",
    "assets_key": "x03",
    "number": 103,
    "design_code": "NS X03",
    "title": "Christmas Ornament Bundle",
    "tagline": ("Three quick decorations from leftover yarn: a stuffed round "
                "bauble, a flat-blocked five-point star, and a crisp six-arm "
                "snowflake. Ten to thirty minutes each, perfect for swaps, gift "
                "tags and stall fillers."),
    "meta": ["US terms", "Beginner", "15 - 40 min each"],
    "finished_size": [
        "Bauble about 3.5-4 cm (1.5 in) across; star about 9 cm (3.5 in); "
        "snowflake about 10 cm (4 in).",
        "Sizes scale with yarn - use DK for dainty tree ornaments, chunky for "
        "bold window pieces.",
    ],
    "safety": [
        "These are decorations, not toys. For anything within a child's reach, "
        "avoid beads and loose bells, knot every hanging loop twice, and keep "
        "loops under 10 cm to avoid tangle hazards. Not tested to a toy-safety "
        "standard (ASTM F963 / EN 71).",
    ],
    "materials": [
        "Yarn: small amounts (5-15 g) of worsted / aran or DK - white, red, gold, "
        "green, silver. Cotton gives the crispest snowflake; acrylic is fine too.",
        "Hook: 3-4 mm (use 3 mm for DK, 4 mm for worsted).",
        "Optional: a pinch of fibre fill for the bauble; metallic yarn for surface stripes.",
        "Notions: tapestry needle, scissors, pin board or mat for blocking the "
        "star and snowflake.",
    ],
    "gauge": [
        "Gauge is unimportant - work tightly enough that the bauble holds fill "
        "and the star blocks flat. One round of the bauble base shows you the "
        "size at once.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sl st - slip stitch",
        "sc - single crochet", "hdc - half double crochet",
        "dc - double crochet", "tr - treble crochet",
        "inc - increase (2 sc in one st)",
        "sc2tog - single crochet 2 together (a decrease)",
        "FO - fasten off", "st(s) - stitch(es)", "R - round",
        "(n) - stitch count at round end",
    ],
    "abbreviations_uk": [
        "MR - magic ring", "ch - chain", "sl st - slip stitch",
        "dc - double crochet", "htr - half treble crochet",
        "tr - treble crochet", "dtr - double treble crochet",
        "inc - increase (2 dc in one st)",
        "dc2tog - double crochet 2 together (a decrease)",
        "FO - fasten off", "st(s) - stitch(es)", "R - round",
        "(n) - stitch count at round end",
    ],
    "construction": ("The bauble is worked in continuous rounds (no joins) with "
                     "the marker in the first stitch. The star and snowflake are "
                     "worked in JOINED rounds / off-the-ring motifs: each round "
                     "closes with a slip stitch. Read each section from its own "
                     "heading down - they are three small standalone patterns."),
    "techniques": [
        ("The magic ring", "Pull the tail tight after round one; if the centre "
         "gaps, work the tail through the first round once more before weaving."),
        ("Picot-free points (star)",
         "Each point is a fan of 7 stitches into ONE centre stitch, with a ch-2 "
         "tip: (sc, hdc, dc, ch 2, dc, hdc, sc). The symmetry comes from "
         "blocking, not from tugging."),
        ("Chain spaces (snowflake)",
         "The snowflake skeleton is 6 ch-5 loops pinned around the 12-dc ring. "
         "The arms are worked into the spaces, never into individual chains."),
        ("Blocking",
         "Star and snowflake only look sharp when pinned: damp the piece, pin "
         "each point out, let it dry fully. Do not iron."),
    ],
    "notes": [],
    "pieces": [
        {
            "name": "A. Round Christmas Bauble - stuffed ball",
            "intro": ("The sphere closes at the same 6-stitch crown it started "
                      "from. Two-colour option: change at R5."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "inc in each st around", "stated": 12, "cons": 6, "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3", "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4", "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": ""},
                    {"label": "R5-6", "text": "sc in each st around (2 rnd)", "stated": 24, "cons": 24, "prod": 24, "check": "sc in each st around", "note": ""},
                    {"label": "R7", "text": "[2 sc, sc2tog] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": ""},
                    {"label": "R8", "text": "[sc, sc2tog] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": "stuff now"},
                    {"label": "R9", "text": "sc2tog x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": "close"},
                ], "notes": [
                    "Finish: FO with a tail, thread through the front loops of "
                    "the last 6 stitches, cinch and weave in. Stuff firmly but "
                    "not hard - the sphere should roll when pressed, not crack.",
                    "Hanging loop: join yarn at the crown, ch 18, sl st into the "
                    "same joining place, FO and weave in. Surface sl sts in "
                    "metallic yarn make instant stripes after Rnd 6.",
                ]},
            ],
        },
        {
            "name": "B. Five-Point Star - flat, blocked",
            "intro": ("Each point uses exactly 2 of the 10 centre stitches - one "
                      "for the slip stitch that anchors it, one for the fan that "
                      "fills it. Block before hanging."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "ch 1, 10 sc in MR, sl st to first sc to close", "stated": 10, "cons": None, "prod": 10, "check": None, "note": "centre ring"},
                    {"label": "R2", "text": "[sl st in next st, (sc, hdc, dc, ch 2, dc, hdc, sc) in next st] x 5, sl st to first sl st, FO", "stated": None, "cons": 10, "prod": 40, "check": None, "note": "5 points = 40 edge sts"},
                ], "notes": [
                    "Hanging loop: pick the top point, join yarn in its ch-2 tip, "
                    "ch 18, sl st into the same ch-2 space.",
                    "The repeat uses all 10 centre stitches exactly (2 per "
                    "point); the fan of 7 stitches per point = the scalloped edge.",
                ]},
            ],
        },
        {
            "name": "C. Six-Point Snowflake - open lace",
            "intro": ("Three short rounds. The ring is closed first so the arms "
                      "hang on real chain spaces - keep the dc round snug, the "
                      "ch-5 round loose."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "ch 6, sl st in first ch to form a ring; ch 3 (counts as first dc), 11 dc in ring, sl st to top of ch-3", "stated": 12, "cons": None, "prod": 12, "check": None, "note": "12 spokes"},
                    {"label": "R2", "text": "[ch 5, skip next st, sl st in next st] x 6, sl st to base of first ch-5 to close", "stated": None, "cons": 12, "prod": 6, "check": None, "note": "6 ch-5 spaces"},
                    {"label": "R3", "text": "(sl st, ch 3, 3 tr, ch 3, sl st) in each of the 6 ch-5 spaces, sl st to first sl st, FO", "stated": None, "cons": None, "prod": None, "check": None, "note": "6 arms"},
                ], "notes": [
                    "Hanging loop: join yarn in the ch-3 tip of one arm, ch 18, "
                    "sl st into the same tip.",
                    "Block flat with pins and a light mist - the snowflake is "
                    "not finished until it is cold, dry and perfectly flat.",
                ]},
            ],
        },
    ],
    "assembly": [
        "Bauble two-colour: change yarn on the final pull-through of R4 for a "
        "sharp banded ball.",
        "Weave every end on the star and snowflake in two directions - lace "
        "shows knots more than amigurumi does.",
        "Twine each finished loop through a cardboard or felt backing card with "
        "the string knot hidden underneath for gifting.",
    ],
    "troubleshooting": [
        ("Bauble looks like a lemon.",
         "Too much stuffing late in the game. Stuff a pinch at R8, shape by "
         "rolling, and keep the crown pinch tight at R9."),
        ("Star will not lie flat.",
         "It needs blocking, not more tugging. Mist, pin all five points, let "
         "dry; cotton needs the mist, acrylic just the pins."),
        ("Snowflake arms lean one way.",
         "The ch-3s at the arm ends are worked over the same space - keep the "
         "first and last sl st of each arm snug so the arm stands upright."),
    ],
    "colorways": ["Snow white", "Classic red & white", "Gold", "Evergreen trio", "Frost blue"],
    "extras": [
        {"name": "Bundle at a glance", "type": "table",
         "headers": ["Piece", "Time", "Yarn (worsted)", "Ideal use"],
         "rows": [
             ["Bauble", "~25 min", "8-10 g", "Tree ornament, garland"],
             ["Star", "~20 min", "6-8 g", "Gift topper, garland"],
             ["Snowflake", "~15 min", "4-6 g", "Window, gift tag, garland"],
         ],
         "outro": ("All three string neatly on one length of yarn - a matching "
                   "garland is just all three patterns on repeat.")},
    ],
    "designer_notes": [],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original work "
                      "and intellectual property of Novality Store, designed by "
                      "Novality Crochet Studio. Design Code NS X03."),
        "may": ("Make as many finished ornaments as you like for yourself, gifts, or "
                "charity. Sell physical finished items made from this pattern in "
                "small batches, in shops, markets and online, provided credit is "
                "given to \"Novality Store\"."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos beyond crediting "
                   "the pattern. Do not mass-produce finished items commercially "
                   "without written permission."),
        "safety": ("These are decorations, not toys. Keep hanging loops short "
                   "around young children and secure every knot."),
    },
    "hashtag": "#NovalityOrnaments",
    "closing": ("Tag us in your trees and tables. Thank you for supporting an "
                "independent pattern designer."),
}
