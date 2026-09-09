"""Pattern 05 - Little Duck Plushie (Design Code NS 05)."""

PATTERN = {
    "id": "duck",
    "number": 5,
    "design_code": "NS 05",
    "title": "Little Duck Plushie",
    "tagline": ("A round, squashy duckling in fluffy chenille, worked as a single "
                "piece from tail to crown - no body-to-head seam. Only the wings "
                "and the beak are sewn on."),
    "meta": ["Embroidered eyes", "Confident beginner", "1.5 - 2 hours"],
    "finished_size": [
        "About 16 cm (6.25 in) tall and 7.5 cm (3 in) wide in super-bulky "
        "chenille (#6) on a 4.5 mm hook.",
        "One seamless body; 2 wings + 1 beak to sew.",
    ],
    "safety": [
        "This duck uses EMBROIDERED eyes, which avoids the small-parts hazard of "
        "safety eyes - a real advantage if you sell finished toys. If you sell "
        "them as toys, EU items need CE marking under EN 71 and US items must "
        "meet CPSIA and ASTM F963; independent testing is the only way to "
        "confirm. Check seams hold under a firm pull and that the chenille pile "
        "does not shed, and tag each piece with materials, your maker name and "
        "an age recommendation.",
    ],
    "materials": [
        "Body yarn: super-bulky chenille (#6), yellow, about 25-35 g. A 100 g "
        "ball makes two ducks comfortably. Fluffy chenille is the whole look.",
        "Details: a small amount of orange yarn for the beak; black yarn or "
        "embroidery floss for the eyes.",
        "Hook: 4.5 mm (US 7).",
        "Stuffing & notions: fibre fill about 25-35 g packed firmly; yarn "
        "needle, stitch marker, pins.",
    ],
    "gauge": [
        "Gauge: about 8 mm per stitch and 7 mm per round in super-bulky "
        "chenille. Chenille varies between brands, so measure a 12-stitch swatch "
        "(about 10 cm) first. Finished size: about 16 cm tall and 7.5 cm wide - "
        "23 rounds at 7 mm and a widest point of 30 stitches at 8 mm.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sc - single crochet",
        "inc - increase (2 sc in one st)", "dec - invisible decrease",
        "sl st - slip stitch", "FLO - front loops only", "FO - fasten off",
        "(n) - stitch count",
    ],
    "construction": ("Work in a continuous spiral - no join, no chain 1 between "
                     "rounds - with a marker in the first stitch of every round."),
    "techniques": [
        ("Magic ring & spiral",
         "The start of the body and each wing is a magic ring. Work in a "
         "continuous spiral - no join, no chain 1 between rounds - with a marker "
         "in the first stitch of every round."),
        ("Invisible decrease",
         "Insert the hook under the FRONT loop only of the next two stitches, "
         "yarn over and pull through the first two loops (three loops on the "
         "hook), then yarn over and pull through both remaining loops. A flatter "
         "join than a standard decrease - it shows at this scale."),
        ("Around a chain (the beak)",
         "The beak is worked around both sides of a starting chain: along one "
         "side, corner increases into the end chain, then back along the other "
         "side. Rnd 1 of a 5-chain totals 11 stitches; all five chains are "
         "used."),
        ("Through both layers",
         "To close each flat wing, fold it and single-crochet across both layers "
         "at once - 6 sc take the 12 stitches down to 6 and leave a flat "
         "half-disc."),
        ("Embroidery & sewing",
         "The eyes are embroidered (no safety eyes). The wings and the "
         "flattened, unstuffed beak are sewn on; sew through a whole stitch so "
         "they cannot pull out."),
    ],
    "notes": [],
    "pieces": [
        {
            "name": "1. Body - yellow chenille",
            "intro": ("The waist at R10-R12 and the reflare at R13-R14 separate "
                      "body from head with no seam. Body and head are the same "
                      "diameter (30 stitches, about 76 mm); the 18-stitch waist "
                      "reads as the neck. Start stuffing at R10 - once the waist "
                      "closes you cannot reach the body."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6,  "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",  "text": "inc in each st around", "stated": 12, "cons": 6,  "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4",  "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": ""},
                    {"label": "R5",  "text": "[3 sc, inc] x 6", "stated": 30, "cons": 24, "prod": 30, "check": "[3 sc, inc] x 6", "note": "body full width"},
                    {"label": "R6",  "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": "wings attach R6 - R9"},
                    {"label": "R7",  "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R8",  "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R9",  "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R10", "text": "[3 sc, dec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": "START STUFFING NOW"},
                    {"label": "R11", "text": "sc in each st around", "stated": 24, "cons": 24, "prod": 24, "check": "sc in each st around", "note": ""},
                    {"label": "R12", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": "waist closing"},
                    {"label": "R13", "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": ""},
                    {"label": "R14", "text": "[3 sc, inc] x 6", "stated": 30, "cons": 24, "prod": 30, "check": "[3 sc, inc] x 6", "note": "head begins"},
                    {"label": "R15", "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R16", "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": "eyes at R16 - R17"},
                    {"label": "R17", "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R18", "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": "beak across R16 - R18"},
                    {"label": "R19", "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R20", "text": "[3 sc, dec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": ""},
                    {"label": "R21", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": "stuff head, shape cheeks"},
                    {"label": "R22", "text": "[sc, dec] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": "add final stuffing"},
                    {"label": "R23", "text": "dec x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": "close via FLO"},
                ], "notes": [
                    "Finish: FO with a long tail; thread through the FLO of the "
                    "6 remaining stitches, pull tight, knot and bury.",
                    "Smaller head option: skip the R14 reflare (keep R14-R19 at "
                    "24) and close with R20 [2 sc, dec] x 6 (18), R21 [sc, dec] "
                    "x 6 (12), R22 dec x 6 (6).",
                ]},
            ],
        },
        {
            "name": "2. Wings - yellow chenille (make 2)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "inc in each st around", "stated": 12, "cons": 6, "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R4", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": "flatten, sc 6 across both layers"},
                ], "notes": [
                    "Do not stuff. Flatten and sc 6 across both layers to close "
                    "(12 sts to 6), leaving a flat half-disc about 30 mm across. "
                    "Sew to the sides spanning R6-R9, angled slightly back.",
                ]},
            ],
        },
        {
            "name": "3. Beak - orange (make 1, worked around a chain)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "Found.", "skip_check": True, "text": "ch 5", "stated": None, "cons": None, "prod": 4, "check": "ch 5", "note": "-"},
                    {"label": "Rnd 1", "text": "from the 2nd ch: sc in next 3, 3 sc in last ch, rotate, sc in next 3, 2 sc in last loop", "stated": 11, "cons": 4, "prod": 11, "check": None, "note": "-"},
                    {"label": "Rnd 2", "text": "inc, 2 sc, inc, 2 sc, inc, 2 sc, inc, sc", "stated": 15, "cons": 11, "prod": 15, "check": None, "note": "-"},
                ], "notes": [
                    "Sl st and FO with a long tail. Do NOT stuff - flatten it to "
                    "a flat lens. As written it is a bold ~50 mm cartoon beak; "
                    "for a daintier duck work Rnd 1 only (11 sts, about 37 mm).",
                ]},
            ],
        },
    ],
    "assembly": [
        "Face & assembly - work in this order:",
        "1. Stuff from R10: fill the body firmly as the waist begins to close - "
        "the neck narrows fast.",
        "2. Eyes: embroider black eyes between R16 and R17, about 7-8 stitches "
        "apart (56-64 mm around the 76 mm head), before the head closes.",
        "3. Beak: pin horizontally across R16-R18, centred between the eyes, "
        "and sew around the outer edge.",
        "4. Wings: sew one to each side at R6-R9, angled slightly back.",
        "5. Close: top up stuffing through R22, then close via the FLO and bury "
        "the end.",
        "The flat orange beak and embroidered eyes - no plastic parts, so a "
        "safer seller.",
    ],
    "troubleshooting": [
        ("Much taller than 16 cm.",
         "Your chenille is thicker than gauge. A 12-stitch swatch at 10 mm "
         "per stitch finishes near 20 cm."),
        ("Much shorter.",
         "Finer yarn - see the size table; DK on 3.0 mm gives 7-8 cm, not "
         "10-12."),
        ("Wings sit on the neck.",
         "Too high. R6-R9 is the body; R10-R12 is the waist."),
        ("Beak leaves a gap / puffs.",
         "Each side must use four chains (no chain left over). Do not stuff; "
         "flatten before pinning."),
        ("Stuffing shows / head flops.",
         "Hook too large for the yarn, or the waist was under-packed. Pack "
         "R10-R12 firmly before the reflare."),
        ("Cannot reach the body to stuff.",
         "You started too late - begin at R10 while the waist is still 24 "
         "stitches wide."),
    ],
    "colorways": [],
    "extras": [
        {"name": "Making a smaller duck", "type": "table",
         "headers": ["Yarn", "Finished height"],
         "rows": [
             ["Velvet / bulky (#5) - 3.0 mm hook", "10 - 12 cm"],
             ["Aran / worsted (#4)", "9 - 10 cm"],
             ["DK / light worsted (#3)", "7.5 - 8.5 cm"],
         ],
         "outro": ""},
        {"name": "Care", "type": "text",
         "lines": [
             "Surface clean with a damp cloth and mild soap; do not machine "
             "wash - chenille mats and sheds in agitation. Dry flat away from "
             "heat, and fluff the pile with a clean pet slicker brush once "
             "dry.",
         ]},
    ],
    "designer_notes": [],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original "
                      "work and intellectual property of Novality Store, designed "
                      "by Novality Crochet Studio. Design Code NS 05."),
        "may": ("Make as many finished ducks as you like for yourself, gifts, or "
                "charity. Sell physical finished items made from this pattern in "
                "small batches, in shops, markets and online, provided credit is "
                "given to \u201cNovality Store\u201d."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos beyond crediting "
                   "the pattern. Do not mass-produce finished items commercially "
                   "without written permission."),
        "safety": ("Eyes are embroidered (no small plastic parts). Finished toys "
                   "sold for children must still meet local toy-safety laws "
                   "(EN 71 / CE in the EU; CPSIA and ASTM F963 in the US) - "
                   "independent testing confirms compliance. Secure every seam "
                   "and check the chenille does not shed."),
    },
    "hashtag": "#LittleDuckPlushie",
    "closing": ("We love seeing your ducklings. Thank you for supporting an "
                "independent pattern designer."),
}
