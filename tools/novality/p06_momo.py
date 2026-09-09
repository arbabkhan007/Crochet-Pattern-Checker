"""Pattern 06 - Momo the Loaf Cat (Design Code NS 06)."""

PATTERN = {
    "id": "momo",
    "number": 6,
    "design_code": "NS 06",
    "title": "Momo the Loaf Cat",
    "tagline": ("A cat folded into a perfect loaf. One no-sew piece on an oval "
                "base - ears crocheted onto the head and the tail worked off the "
                "body, so nothing is sewn on."),
    "meta": ["No-sew body", "Advanced beginner", "2 - 2.5 hours"],
    "finished_size": [
        "About 7.9 cm (3.1 in) long, 5.2 cm (2 in) wide and 4.3 cm (1.7 in) "
        "tall.",
        "A low, wide loaf, wider than it is tall (about 1.2 : 1).",
    ],
    "safety": [
        "Momo has two 8 mm safety eyes - small parts. Lock the washers firmly "
        "from the inside and pull-test each eye. Embroidering the eyes is safer, "
        "but it does not make Momo a tested toy: not tested to ASTM F963 or "
        "EN 71, so do not describe finished Momos as \u201cbaby-safe\u201d. For a "
        "child under three, embroider and say \u201cembroidered, no small "
        "parts\u201d.",
        "The ears and tail are worked into the body (stronger than sewing), but "
        "still weave every end in at least 5 cm and knot the embroidery floss "
        "inside.",
    ],
    "materials": [
        "Main yarn: worsted #4, about 10 g. Grey, ginger, cream or black - all "
        "sell equally well. One 25 g ball makes two.",
        "Contrast: small amounts of white for the chest and paws, pink for the "
        "nose and inner ears.",
        "Hook: 3.5 mm (US E-4) - tight gauge so stuffing cannot show.",
        "Eyes: 2 x 8 mm safety eyes, or embroider in black.",
        "Also needed: polyfill about 10 g; tapestry needle; stitch marker; "
        "black embroidery floss.",
    ],
    "gauge": [
        "Gauge: about 4.5 mm per stitch and 4.3 mm per round. Finished size "
        "about 7.9 cm long, 5.2 cm wide and 4.3 cm tall - a low, wide loaf. "
        "The 48-stitch oval base sets the whole size of the cat.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sc - single crochet",
        "inc - increase (2 sc in one st)", "dec - invisible decrease",
        "sl st - slip stitch", "BLO - back loop only", "FO - fasten off",
        "(n) - stitch count",
    ],
    "construction": ("Work in a continuous spiral unless a piece says otherwise - "
                     "no joins, no chain 1 between rounds; move the marker up "
                     "each round."),
    "techniques": [
        ("Around a chain (oval base)",
         "THE step that makes the loaf. Crochet into BOTH sides of a starting "
         "chain: across the front, corner increases into the last chain, then "
         "back along the opposite side and into the last loop. That turns a "
         "chain into a flat oval instead of a strip. Do NOT use a magic-ring "
         "circle here - a round base gives a sphere every time."),
        ("The magic ring",
         "Used for the tail's first stitches. Wrap yarn around two fingers, "
         "pull up a loop and work the round into the ring, then pull the tail "
         "tight."),
        ("Working in a spiral",
         "No joins and no chain 1 between rounds; move the marker up each "
         "round - there is no join to count from."),
        ("Back loop only (BLO)",
         "Work into the far loop only; the unused loops form a raised ridge - "
         "the visible edge where the oval base meets the walls. That ridge is "
         "what makes the loaf read as folded rather than moulded."),
        ("The invisible decrease",
         "Front loops only of the next two stitches, yarn over and pull "
         "through both, then yarn over and pull through the remaining two. "
         "Every dec here is worked this way."),
        ("Flat rows (ch 1, turn)",
         "The ears are not worked in the round: chain 1, turn, and work back "
         "along the row. Each row is shorter than the one before, forming the "
         "ear point."),
        ("Working into body fabric",
         "The tail starts by pushing the hook through the finished body wall - "
         "go under a WHOLE stitch, not just one loop, or it will pull out."),
    ],
    "notes": [],
    "pieces": [
        {
            "name": "1. Body - one no-sew piece",
            "intro": ("The base is worked up to 48 stitches before the walls "
                      "begin; the base size sets the whole cat. Stopping at 36 "
                      "gives a body about 34 mm across that comes out tall and "
                      "round no matter how you stuff it."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "Found.", "skip_check": True, "text": "ch 9", "stated": None, "cons": None, "prod": 8, "check": "ch 9", "note": "-"},
                    {"label": "R1",  "text": "sc in 2nd ch, sc in next 6, 3 sc in last ch, sc in next 6, 2 sc in last loop", "stated": 18, "cons": 8, "prod": 18, "check": None, "note": "around both sides of chain"},
                    {"label": "R2",  "text": "inc, 6 sc, inc x 3, 6 sc, inc x 2", "stated": 24, "cons": 18, "prod": 24, "check": None, "note": ""},
                    {"label": "R3",  "text": "sc, inc, 6 sc, [sc, inc] x 3, 6 sc, [sc, inc] x 2", "stated": 30, "cons": 24, "prod": 30, "check": None, "note": ""},
                    {"label": "R4",  "text": "2 sc, inc, 6 sc, [2 sc, inc] x 3, 6 sc, [2 sc, inc] x 2", "stated": 36, "cons": 30, "prod": 36, "check": None, "note": ""},
                    {"label": "R5",  "text": "3 sc, inc, 6 sc, [3 sc, inc] x 3, 6 sc, [3 sc, inc] x 2", "stated": 42, "cons": 36, "prod": 42, "check": None, "note": ""},
                    {"label": "R6",  "text": "4 sc, inc, 6 sc, [4 sc, inc] x 3, 6 sc, [4 sc, inc] x 2", "stated": 48, "cons": 42, "prod": 48, "check": None, "note": "BASE AT FULL SIZE"},
                    {"label": "R7",  "text": "BLO sc around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": "ridge = base edge"},
                    {"label": "R8",  "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": "eyes at R8 - R9"},
                    {"label": "R9",  "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": "stuff firmly from here"},
                    {"label": "R10", "text": "[6 sc, dec] x 6", "stated": 42, "cons": 48, "prod": 42, "check": "[6 sc, dec] x 6", "note": ""},
                    {"label": "R11", "text": "[5 sc, dec] x 6", "stated": 36, "cons": 42, "prod": 36, "check": "[5 sc, dec] x 6", "note": ""},
                    {"label": "R12", "text": "[4 sc, dec] x 6", "stated": 30, "cons": 36, "prod": 30, "check": "[4 sc, dec] x 6", "note": "ears worked onto R12"},
                    {"label": "R13", "text": "[3 sc, dec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": ""},
                    {"label": "R14", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": ""},
                    {"label": "R15", "text": "[sc, dec] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": "top up stuffing"},
                    {"label": "R16", "text": "dec x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": "close via front loops"},
                ], "notes": [
                    "Finish: thread the tail through the front loop of each of "
                    "the 6 remaining stitches, pull tight, knot and bury. Shape "
                    "check: the base is an oval about 79 mm long and 52 mm "
                    "across; the walls add ten rounds of height, so the "
                    "finished loaf is about 43 mm tall - wider than it is tall.",
                ]},
            ],
        },
        {
            "name": "2. Ears - worked onto the head (make 2)",
            "intro": ("Join the main yarn to the head at Rnd 12, leaving about 6 "
                      "stitches between the two ears, and work each ear as three "
                      "short rows:"),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "Row 1", "text": "sc in next 5, ch 1, turn", "stated": 5, "cons": 5, "prod": 5, "check": "sc in next 5 sts", "note": ""},
                    {"label": "Row 2", "text": "dec, sc, dec, ch 1, turn", "stated": 3, "cons": 5, "prod": 3, "check": "dec, sc, dec", "note": ""},
                    {"label": "Row 3", "text": "dec, sc", "stated": 2, "cons": 3, "prod": 2, "check": "dec, sc", "note": "the ear tip"},
                ], "notes": [
                    "The row maths: Row 1 makes 5 stitches; Row 2 works dec, "
                    "sc, dec (consumes 5, makes 3); Row 3 works dec, sc "
                    "(consumes 3, makes 2) - those 2 stitches form the tip.",
                    "FO with a short tail; pull it through the 2 tip stitches "
                    "to close the point and bury inside the head. Embroider a "
                    "small pink triangle on the front of each ear for lining.",
                ]},
            ],
        },
        {
            "name": "3. Tail - worked off the body",
            "intro": "",
            "kind": "text",
            "subpieces": [
                {"name": "", "rows": [], "notes": [
                    "Join the main yarn to the back of the body at about Rnd 9 "
                    "on the centre line. Insert the hook under a whole body "
                    "stitch, pull up a loop, and work the first 4 sc into the "
                    "body fabric in a tight square; then continue in a normal "
                    "spiral off those 4 stitches: Rnds 1-8 are 4 sc in each "
                    "round. Do NOT stuff - a thin tail curls around the loaf "
                    "far better than a stuffed one. FO and bury.",
                ]},
            ],
        },
    ],
    "assembly": [
        "Face & markings:",
        "Eyes: fix the 8 mm eyes between Rnds 8 and 9, about 7 stitches apart, "
        "LOW and wide on the front (7 sts is about 32 mm, roughly 60% of the "
        "body width). Low eyes read as a cat; high eyes read as a bear.",
        "Nose: a small pink triangle centred between and just below the eyes, "
        "with two short stitches angled down from the point for the mouth.",
        "Whisker dots: three tiny black French knots on each side of the nose.",
        "Chest & paws: with white yarn, embroider a soft oval on the chest and "
        "two small ovals at the front of the base for tucked paws - this is "
        "what turns a plain loaf into a cat.",
        "Long, low and wide - the BLO ridge and tucked paws make the loaf read "
        "as a folded cat.",
    ],
    "troubleshooting": [
        ("It came out round.",
         "You stopped increasing at Rnd 4 instead of Rnd 6, worked too many "
         "plain rounds at Rnds 8-9, or used a magic-ring base instead of the "
         "oval. The base must reach 48 stitches."),
        ("Tall and narrow.",
         "The base did not reach 48. Count the stitches at Rnd 6 before the "
         "BLO round - that one number decides the whole shape."),
        ("Ears lean back.",
         "Join the yarn one round lower and angle the first row slightly "
         "forward."),
        ("Tail falls off.",
         "The first 4 sc must go through the body fabric under a whole "
         "stitch, not just one loop."),
        ("Stuffing shows.",
         "Go down to a 3.0 mm hook - loose gauge on 3.5 mm is the usual "
         "cause."),
        ("Face looks like a bear.",
         "Eyes too high and too close. Drop them a round and widen to 7 "
         "stitches."),
    ],
    "colorways": ["Grey tabby", "Orange ginger", "Cream", "Black", "Calico"],
    "extras": [],
    "designer_notes": [
        "Grey tabby, orange ginger, cream, black, and calico (grey base with "
        "ginger and cream patches embroidered on afterwards). Listing all five "
        "as photos in one listing outperforms separate listings - buyers "
        "choose a cat, not a pattern.",
    ],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original "
                      "work and intellectual property of Novality Store, designed "
                      "by Novality Crochet Studio. Design Code NS 06."),
        "may": ("Make as many finished Momos as you like for yourself, gifts, or "
                "charity. Sell physical finished items made from this pattern in "
                "small batches, in shops, markets and online, provided credit is "
                "given to \u201cNovality Store\u201d."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos beyond crediting "
                   "the pattern. Do not mass-produce finished items commercially "
                   "without written permission."),
        "safety": ("Not tested to a toy-safety standard (ASTM F963 / EN 71) and "
                   "uses 8 mm safety eyes. Finished items sold for children must "
                   "be assessed against local toy-safety laws; for young "
                   "children, embroider the eyes and secure every end."),
    },
    "hashtag": "#MomoTheLoafCat",
    "closing": ("We love seeing your loaves. Thank you for supporting an "
                "independent pattern designer."),
}
