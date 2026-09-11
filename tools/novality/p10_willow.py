"""Pattern 10 - Willow the Bunny Lovey (Design Code NS 10)."""

PATTERN = {
    "id": "willow",
    "number": 10,
    "design_code": "NS 10",
    "title": "Willow the Bunny Lovey",
    "tagline": ("A bunny comforter: a soft, firmly stuffed head above a light, "
                "drapey granny-square blanket. Long floppy ears to hold, an "
                "embroidered face with no small parts, and a blanket that "
                "grows evenly from the centre out."),
    "meta": ["No small parts", "Advanced beginner", "2 - 3 hours"],
    "finished_size": [
        "Blanket about 26 cm (10 in) square (20 rounds).",
        "Head about 4.9 cm across; roughly 33 cm from ear tips to the "
        "opposite corner.",
        "DK cotton on a 3.5 mm hook (3.0 mm for the head if your tension "
        "is loose).",
    ],
    "safety": [
        "No safety eyes, buttons, beads or removable parts; the face is "
        "embroidered and every floss end is knotted inside the head. That is "
        "safer, but it is not a tested toy - do not describe Willow as "
        "\u201cbaby-safe\u201d without ASTM F963 / EN 71 testing.",
        "Comforters are not recommended in the cot for babies under 12 "
        "months and should be used with supervision; put that in your "
        "listing. Sew every seam twice and weave ends in at least 5 cm. Say "
        "\u201cembroidered face, no small parts\u201d - a claim you can "
        "stand behind.",
    ],
    "materials": [
        "Yarn: DK (#3) 100% cotton (or a baby-safe certified blend), about "
        "60 g - cream, sage, dusty pink or pale grey. Only the head is "
        "stuffed.",
        "Hook: 3.5 mm (US E/4) for the blanket; use 3.0 mm for the head if "
        "your tension is loose.",
        "Eyes / floss: none - the face is embroidered in dark brown or "
        "charcoal cotton floss, ends knotted inside.",
        "Also: about 8 g fibre fill, tapestry needle, stitch marker.",
    ],
    "gauge": [
        "Gauge: about 4.3 mm per stitch and 3.8 mm per round. Check on the "
        "blanket after Rnd 3: 9 dc along an edge should measure ~39 mm; "
        "narrower and the blanket comes out small.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sc - single crochet",
        "dc - double crochet", "inc - increase (2 sc in one st)",
        "dec - invisible decrease", "sl st - slip stitch",
        "st(s) - stitch(es)", "sp - space", "FO - fasten off",
        "(n) - stitch count at round end",
    ],
    "construction": ("The HEAD and EARS are worked in a continuous spiral "
                     "(no joins, marker in the first stitch). The BLANKET is "
                     "worked in JOINED rounds: each round closes with a slip "
                     "stitch and the next begins with a turning chain - a "
                     "different rhythm that lets the square grow out evenly. "
                     "Work every stitch through both loops unless noted."),
    "techniques": [
        ("Magic ring & spiral",
         "The head and each ear begin with a magic ring; pull the tail "
         "tight after round one."),
        ("The granny-square corner",
         "Every blanket corner is (3 dc, ch 2, 3 dc) into one corner "
         "space. Those four corners make the piece square instead of "
         "round. Miss one corner group and the whole square pulls out of "
         "true - check all four at the end of every round."),
        ("The border round",
         "One final round of single crochet around the edge with 3 sc "
         "into each corner space squares the edge and stops the blanket "
         "curling. Do not skip it."),
    ],
    "notes": [
        "Sizing the blanket: the square grows ~1.3 cm per side per round - "
        "18 rounds ~23 cm, 20 rounds ~26 cm, 22 rounds ~28 cm. Add rounds "
        "to make a bigger lovey.",
    ],
    "pieces": [
        {
            "name": "1. Head - worked top-down",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6,  "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",  "text": "inc in each st around", "stated": 12, "cons": 6,  "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4",  "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": "ears at R4 - R6"},
                    {"label": "R5",  "text": "[3 sc, inc] x 6", "stated": 30, "cons": 24, "prod": 30, "check": "[3 sc, inc] x 6", "note": ""},
                    {"label": "R6",  "text": "[4 sc, inc] x 6", "stated": 36, "cons": 30, "prod": 36, "check": "[4 sc, inc] x 6", "note": "full width"},
                    {"label": "R7",  "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": ""},
                    {"label": "R8",  "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": "face on R8 - R10"},
                    {"label": "R9",  "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": ""},
                    {"label": "R10", "text": "[4 sc, dec] x 6", "stated": 30, "cons": 36, "prod": 30, "check": "[4 sc, dec] x 6", "note": ""},
                    {"label": "R11", "text": "[3 sc, dec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": "stuff firmly"},
                    {"label": "R12", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": ""},
                    {"label": "R13", "text": "[sc, dec] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": "top up stuffing"},
                    {"label": "R14", "text": "dec x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": "close"},
                ], "notes": [
                    "FO and close with the tail. The finished head is "
                    "about 4.9 cm across and 5.3 cm tall. Stuff it "
                    "FIRMLY - a soft head collapses when gripped and "
                    "the face distorts.",
                ]},
            ],
        },
        {
            "name": "2. Ears - long and floppy (make 2, do not stuff)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",   "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",   "text": "[sc, inc] x 3", "stated": 9, "cons": 6, "prod": 9, "check": "[sc, inc] x 3", "note": ""},
                    {"label": "R3",   "text": "[2 sc, inc] x 3", "stated": 12, "cons": 9, "prod": 12, "check": "[2 sc, inc] x 3", "note": ""},
                    {"label": "R4-8", "text": "sc in each st around (5 rnd)", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R9",   "text": "[2 sc, dec] x 3", "stated": 9, "cons": 12, "prod": 9, "check": "[2 sc, dec] x 3", "note": ""},
                    {"label": "R10",  "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": ""},
                    {"label": "R11",  "text": "[sc, dec] x 3", "stated": 6, "cons": 9, "prod": 6, "check": "[sc, dec] x 3", "note": "flatten, FO"},
                ], "notes": [
                    "Flatten and FO with a long tail. Sew to Rnds 4-6 of "
                    "the head, about 10 stitches apart, pinching each "
                    "base so it flops forward.",
                ]},
            ],
        },
        {
            "name": "3. Blanket - granny square, joined rounds",
            "intro": ("Ch 4 and sl st to the first ch to form a ring. Every "
                      "round closes with a slip stitch into the top of the "
                      "starting ch-3."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "Rnd 1", "text": "ch 3 (counts as first dc), 2 dc in the ring, [ch 2, 3 dc in the ring] x 3, ch 2, sl st to the ch-3 top", "stated": 12, "cons": None, "prod": 12, "check": None, "note": "12 dc, 4 corner spaces"},
                    {"label": "Rnd 2", "text": "sl st into the next corner space; ch 3, 2 dc in that space, ch 2, 3 dc in the same space (first corner); then (3 dc, ch 2, 3 dc) into each remaining corner space; sl st to close", "stated": 24, "cons": 12, "prod": 24, "check": None, "note": "+12 dc"},
                    {"label": "Rnds 3-20", "text": "into every corner space work (3 dc, ch 2, 3 dc), and into every space along a side work 3 dc; sl st to close. Each round adds one 3-dc group to every side (+12 dc per round)", "stated": None, "cons": None, "prod": None, "check": None, "note": "see dc table"},
                ], "notes": [
                    "Total dc per round: Rnd 3 = 36, Rnd 5 = 60, Rnd 10 = "
                    "120, Rnd 15 = 180, Rnd 20 = 240 (60 dc per edge = "
                    "~26 cm).",
                    "Border: work one final round of sc all the way "
                    "around - 1 sc into each dc, and 3 sc into each corner "
                    "space (into the space itself; the 2 corner chains are "
                    "not worked into) - then sl st to join and FO. At Rnd 20 that is "
                    "240 sc + 12 corner sc = 252 sc. This firms the edge "
                    "and stops the square curling.",
                    "Open dc clusters and crisp (3 dc, ch 2, 3 dc) "
                    "corners keep the square true round after round.",
                ]},
            ],
        },
    ],
    "assembly": [
        "Face (embroidery only): two small oval eyes about 8 stitches "
        "apart across Rnds 8-9, a small inverted-triangle nose centred "
        "between and below them, and a shallow Y for the mouth. KNOT "
        "every end inside the head and bury the tails before closing. "
        "Skip blush - chalk rubs off on bedding and is not washable.",
        "Joining: centre the head over one corner of the square, "
        "overlapping the blanket by about 3 cm. Sew all the way around "
        "the base of the head, THEN sew it a second time - this is the "
        "only structural seam and it will be pulled, chewed and washed. "
        "Weave every end in at least 5 cm.",
    ],
    "troubleshooting": [
        ("Blanket curls / not square.",
         "You skipped the sc border, or missed a (3 dc, ch 2, 3 dc) "
         "corner - check all four corners at the end of every round."),
        ("Came out too small / head flops.",
         "Tighter than 4.3 mm/dc: go up a hook or add rounds (22 rounds "
         "= ~28 cm). Stuff the head firmly and sew the base seam "
         "twice."),
    ],
    "colorways": ["Cream", "Sage", "Dusty pink", "Pale grey", "Butter yellow"],
    "extras": [
        {"name": "For your listing", "type": "text", "lines": [
            "Materials: 100% cotton, embroidered face, no safety eyes, "
            "no buttons, beads or removable parts.",
            "Care: machine wash cool on a gentle cycle inside a mesh "
            "bag; reshape while damp and dry flat. Do not tumble dry - "
            "it will felt and shrink.",
            "Supervision: comforters are not recommended in the cot for "
            "babies under 12 months; use with supervision.",
        ]},
    ],
    "designer_notes": [
        "Colorways: cream, sage, dusty pink, pale grey and butter "
        "yellow - neutrals outsell brights in the baby category.",
    ],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original "
                      "work and intellectual property of Novality Store, designed "
                      "by Novality Crochet Studio. Design Code NS 10."),
        "may": ("Make as many finished loveys as you like for yourself, gifts, "
                "or charity. Sell physical finished items made from this "
                "pattern in small batches, in shops, markets and online, "
                "provided credit is given to \u201cNovality Store\u201d."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos beyond crediting "
                   "the pattern. Do not mass-produce finished items commercially "
                   "without written permission."),
        "safety": ("Willow has NO safety eyes, buttons, beads or removable "
                   "parts - the face is embroidered and floss ends are knotted "
                   "inside the head. Even so she is not a tested toy "
                   "(ASTM F963 / EN 71): do not claim \u201cbaby-safe\u201d. "
                   "Comforters are not recommended in a cot for babies under "
                   "12 months and should be used with supervision; sew every "
                   "seam twice and weave ends in at least 5 cm."),
    },
    "hashtag": "#WillowTheBunnyLovey",
    "closing": ("We love seeing your makes. Thank you for supporting an "
                "independent pattern designer."),
}
