"""Pattern 07 - Pocket Positivity Trio (Design Code NS 07)."""

PATTERN = {
    "id": "trio",
    "number": 7,
    "design_code": "NS 07",
    "title": "Pocket Positivity Trio",
    "tagline": ("Three palm-sized amigurumi that slip into a coat pocket - Sunny "
                "the Sunflower, Waddle the Penguin and Spud the Potato. They "
                "share one easy construction and work up in an evening or two."),
    "meta": ["3 mini patterns", "Easy / beginner", "20 - 35 min each"],
    "finished_size": [
        "Sunny: about 3.0 cm across the petals.",
        "Waddle: about 3.8 cm tall.",
        "Spud: about 2.7 cm long.",
        "#4 worsted on a 3.5 mm hook. Sunny and Waddle need no sewn pieces "
        "beyond small add-ons; Spud is worked flat and closed in one seam.",
    ],
    "safety": [
        "The set uses 5 mm black safety eyes (six in total) - small parts and a "
        "choking hazard, not intended for children under 3. These toys are tiny: "
        "lock every washer from the inside BEFORE you stuff and close each piece, "
        "and pull-test. For young children, "
        "embroider the eyes and mouths instead.",
        "Sellers: do not market as \u201cbaby-safe\u201d; sell as adult "
        "collectibles, desk companions or keychain charms, and tag with "
        "materials, your maker name and \u201cNot suitable for children under "
        "3 years.\u201d",
    ],
    "materials": [
        "Yarn: #4 worsted (~250 m / 100 g). The three toys use roughly 8 m "
        "total (under 4 g), so scraps are fine. Golden yellow + chocolate "
        "(Sunny); black + cream chest + yellow beak (Waddle); warm tan (Spud).",
        "Hook: 3.5 mm (US E/4).",
        "Eyes: six 5 mm black safety eyes, or embroidery thread.",
        "Also: about 3 g fibre fill total, blunt tapestry needle, stitch "
        "marker, scissors.",
    ],
    "gauge": [
        "Gauge: about 3.5 mm per stitch and 3.2 mm per round in sc. Pocket "
        "size means gauge shows - work a swatch; the stated sizes follow from "
        "it.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sc - single crochet",
        "hdc - half double crochet", "inc - increase (2 sc in one st)",
        "dec - invisible decrease", "sl st - slip stitch",
        "st(s) - stitch(es)", "(n) - stitch count at round end",
    ],
    "construction": ("Techniques: continuous spiral rounds with a marker (no "
                     "joins); magic-ring start for Sunny's centre and Waddle's "
                     "body; invisible decreases; petal CLUSTERS worked into one "
                     "stitch with a slip stitch between petals; an OVAL worked "
                     "around a chain for Spud; and simple sewing / embroidery."),
    "techniques": [],
    "notes": [],
    "pieces": [
        {
            "name": "1. Sunny the Sunflower",
            "intro": ("A small brown cushion; nine yellow petals are worked "
                      "straight into Rnd 3."),
            "kind": "table",
            "subpieces": [
                {"name": "Centre - chocolate", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "inc in each st around", "stated": 12, "cons": 6, "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3", "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": "petals join here"},
                    {"label": "R4", "text": "sc in each st around", "stated": 18, "cons": 18, "prod": 18, "check": "sc in each st around", "note": ""},
                    {"label": "R5", "text": "[sc, dec] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": ""},
                    {"label": "R6", "text": "dec x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": "stuff firmly before closing"},
                ], "notes": []},
                {"name": "Petals - yellow (worked in the round)", "rows": [
                    {"label": "Petal", "text": "join yellow with a sl st in any st of Rnd 3 (this counts as the first sl st); (sc, hdc, sc) in next st, [sl st in next st, (sc, hdc, sc) in next st] x 8, sl st to the first sl st, FO", "stated": 36, "cons": 18, "prod": 36, "check": None, "note": "9 petals"},
                ], "notes": [
                    "Count check: the joining slip stitch counts as the first of 9 "
                    "slip stitches. 9 sl sts plus 9 petals of (sc, hdc, sc) = 9 + 27 "
                    "= 36 stitches, using exactly 2 stitches per petal set on the "
                    "18-stitch cushion round. The slip stitch sits in the "
                    "valley between petals; work this round loosely (use a "
                    "4 mm hook for this round only if it pulls tight). FO and "
                    "weave in.",
                    "Face: embroider a smiling mouth between Rnd 2-3 and add "
                    "eyes 3 stitches apart on Rnd 2 (~10.5 mm; use 4 apart "
                    "only if embroidering).",
                ]},
            ],
        },
        {
            "name": "2. Waddle the Penguin",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "Body - black", "rows": [
                    {"label": "R1",   "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",   "text": "inc in each st around", "stated": 12, "cons": 6, "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",   "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": "eyes on R3"},
                    {"label": "R4-6", "text": "sc in each st around (3 rnd)", "stated": 18, "cons": 18, "prod": 18, "check": "sc in each st around", "note": ""},
                    {"label": "R7",   "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": "chest over R4-8"},
                    {"label": "R8-9", "text": "sc in each st around (2 rnd)", "stated": 24, "cons": 24, "prod": 24, "check": "sc in each st around", "note": "wings at R6"},
                    {"label": "R10",  "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": ""},
                    {"label": "R11",  "text": "[sc, dec] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": ""},
                    {"label": "R12",  "text": "dec x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": "stuff as you go, close"},
                ], "notes": []},
                {"name": "Wings - black (make 2)", "rows": [
                    {"label": "R1", "text": "4 sc in MR", "stated": 4, "cons": None, "prod": 4, "check": "4 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "[sc, inc] x 2", "stated": 6, "cons": 4, "prod": 6, "check": "[sc, inc] x 2", "note": ""},
                    {"label": "R3-4", "text": "sc in each st around (2 rnd)", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                ], "notes": [
                    "FO with a 15 cm tail, do not stuff; sew to the sides at "
                    "Rnd 6 angled backward.",
                ]},
                {"name": "Chest patch - cream (flat oval)", "rows": [
                    {"label": "Found.", "skip_check": True, "text": "ch 6", "stated": None, "cons": None, "prod": 5, "check": "ch 6", "note": "-"},
                    {"label": "R1", "text": "sc in 2nd ch, 3 sc, 3 sc in last ch, then down the other side 3 sc, 2 sc in last ch", "stated": 12, "cons": 5, "prod": 12, "check": None, "note": "-"},
                    {"label": "R2", "text": "inc, 3 sc, inc x 3, 3 sc, inc x 2", "stated": 18, "cons": 12, "prod": 18, "check": None, "note": "-"},
                ], "notes": [
                    "FO with a tail; sew onto the front covering Rnds 4-8, "
                    "stitching top and bottom edges only so the middle puffs.",
                ]},
                {"name": "Beak - yellow", "rows": [
                    {"label": "R1", "text": "ch 2, 3 sc in 2nd ch from hook", "stated": 3, "cons": None, "prod": 3, "check": None, "note": ""},
                    {"label": "R2", "text": "inc x 3", "stated": 6, "cons": 3, "prod": 6, "check": "inc x 3", "note": ""},
                    {"label": "R3", "text": "sc in each st around", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                ], "notes": [
                    "FO, do not stuff; sew centred between the eyes, angled "
                    "slightly down. Eyes 3 stitches apart on Rnd 3; add a "
                    "touch of pink blush sparingly.",
                ]},
            ],
        },
        {
            "name": "3. Spud the Potato",
            "intro": ("Spud is worked as an oval around a chain, then flat-"
                      "stitched closed so the seam reads as a natural crease."),
            "kind": "table",
            "subpieces": [
                {"name": "Body - warm tan", "rows": [
                    {"label": "Found.", "skip_check": True, "text": "ch 7", "stated": None, "cons": None, "prod": 6, "check": "ch 7", "note": ""},
                    {"label": "R1",   "text": "sc in 2nd ch, 4 sc, 3 sc in last ch; other side: 4 sc, 2 sc in last ch", "stated": 14, "cons": 6, "prod": 14, "check": None, "note": "around the chain"},
                    {"label": "R2",   "text": "inc, 4 sc, inc x 3, 4 sc, inc x 2", "stated": 20, "cons": 14, "prod": 20, "check": None, "note": ""},
                    {"label": "R3-6", "text": "sc in each st around (4 rnd)", "stated": 20, "cons": 20, "prod": 20, "check": "sc in each st around", "note": ""},
                    {"label": "R7",   "text": "[3 sc, dec] x 4", "stated": 16, "cons": 20, "prod": 16, "check": "[3 sc, dec] x 4", "note": ""},
                    {"label": "R8",   "text": "[2 sc, dec] x 4", "stated": 12, "cons": 16, "prod": 12, "check": "[2 sc, dec] x 4", "note": ""},
                    {"label": "R9",   "text": "[sc, dec] x 4", "stated": 8, "cons": 12, "prod": 8, "check": "[sc, dec] x 4", "note": "begin stuffing"},
                    {"label": "R10",  "text": "dec x 4", "stated": 4, "cons": 8, "prod": 4, "check": "dec x 4", "note": "close the seam"},
                ], "notes": [
                    "Closing: leave a 20 cm tail. With the body flat, whip-"
                    "stitch the remaining opening closed along the flat top "
                    "so the seam reads as the potato's natural crease; weave "
                    "the end inside.",
                    "Face: eyes about 5 stitches apart on the broad side "
                    "around Rnd 4 (Spud's face is ~27 mm wide, so 4 or 5 "
                    "apart both fit), with a small open mouth below.",
                ]},
            ],
        },
    ],
    "assembly": [
        "Before you finish, check each toy: Sunny has 9 even petals and a "
        "closed brown centre; Waddle has 2 wings, a cream chest and a yellow "
        "beak; Spud's seam reads as a crease. Every safety-eye washer is locked "
        "from the inside (before stuffing and closing) or the eyes are "
        "embroidered, and every end is woven in at least 5 cm.",
    ],
    "troubleshooting": [
        ("Petal edges curl / centre will not close.",
         "Use invisible decreases on the centre's Rnd 5 and pull the closing "
         "snug. Nine petal repeats use exactly 18 stitches (two each) - "
         "check Rnd 3 is (18) and you slip-stitched once per repeat."),
        ("Petals sit flat.",
         "Work the three stitches in one stitch loosely, or use a 4 mm hook "
         "for the petal round only."),
        ("Toys come out smaller / larger.",
         "Tighter than 3.5 mm per stitch: go up half a hook size or hold "
         "yarn double. Looser: drop to a 3 mm hook."),
        ("Waddle's wings flop.",
         "Sew at Rnd 6 and catch a stitch of the body with each pass."),
        ("Spud's seam shows.",
         "Whip-stitch along the flat top so the seam reads as a crease, "
         "and stuff evenly before closing."),
        ("Eyes too near the edge.",
         "On Sunny and Waddle place them three stitches apart, not four."),
    ],
    "colorways": [],
    "extras": [
        {"name": "Making a bigger trio", "type": "text", "lines": [
            "Use chunky/aran or hold #4 double on a 3.5 mm hook (~4.5 mm "
            "per stitch, about 1.3x): Sunny ~3.9 cm, Waddle ~4.9 cm, Spud "
            "~3.5 cm. Stitch counts do not change.",
        ]},
        {"name": "Selling & care", "type": "text", "lines": [
            "Sell as adult collectibles, desk companions or keychain "
            "charms - not \u201cbaby-safe\u201d. Stuff firmly and evenly. "
            "Spot clean with a damp cloth; do not machine wash; fluff "
            "pulled loops with a clean slicker brush or toothbrush.",
        ]},
    ],
    "designer_notes": [],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original "
                      "work and intellectual property of Novality Store, designed "
                      "by Novality Crochet Studio. Design Code NS 07."),
        "may": ("Make as many finished toys as you like for yourself, gifts, or "
                "charity. Sell physical finished items made from this pattern in "
                "small batches, in shops, markets and online, provided credit is "
                "given to \u201cNovality Store\u201d."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos beyond crediting "
                   "the pattern. Do not mass-produce finished items commercially "
                   "without written permission."),
        "safety": ("This set uses 5 mm safety eyes (small parts) and is not "
                   "intended for children under 3. Finished items sold for "
                   "children must meet local toy-safety laws (EN 71 / CE in the "
                   "EU; CPSIA and ASTM F963 in the US); for young children "
                   "embroider the eyes and mouths and secure every end."),
    },
    "hashtag": "#PocketPositivityTrio",
    "closing": ("We love seeing your makes. Thank you for supporting an "
                "independent pattern designer."),
}
