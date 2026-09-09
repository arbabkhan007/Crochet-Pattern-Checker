"""Pattern 01 - Hamish the Highland Cow (Design Code NS 01)."""

PATTERN = {
    "id": "hamish",
    "number": 1,
    "design_code": "NS 01",
    "title": "Hamish the Highland Cow",
    "tagline": ("A shaggy, sturdy Highland cow with a flattened brow, a wide cream "
                "muzzle and a weather-beaten fringe. Worked in pieces so every "
                "proportion can be pinned and checked before sewing."),
    "meta": ["US terms", "Intermediate", "6 - 8 hours"],
    "finished_size": [
        "About 15 cm (6 in) sitting in worsted weight.",
        "A 70 mm wide body and a 70 x 67 mm head.",
        "A low, sprawling Highland sit.",
    ],
    "safety": [
        "Hamish has two 12 mm safety eyes - small parts. Reach through the open head "
        "and lock the washers firmly from the inside BEFORE you stuff and close the "
        "head (Rnd 16) - once closed you cannot get back inside. Pull-test each "
        "eye. The horns, ears, muzzle, legs and tail are sewn on, and the fringe and tail "
        "are knotted yarn: sew every seam twice, weave ends in at least 5 cm, and knot "
        "the fringe and tail securely.",
        "Not tested to ASTM F963 or EN 71 - do not describe finished Hamishes as "
        "\u201cbaby-safe\u201d. For children under three, embroider the eyes with black "
        "floss instead of safety eyes.",
    ],
    "materials": [
        "Yarn A - Ginger: worsted / aran (#4), about 25 g used. Caramel, toffee or "
        "ginger gold. One 80 g / 150 m ball covers several cows and re-dos.",
        "Yarn B - Oat cream: worsted / aran (#4), about 12 g. Muzzle, horns, inner "
        "ears, optional belly patch.",
        "Yarn C - Dark chocolate: worsted / aran (#4), about 5 g. Hooves and nostrils.",
        "Yarn D - Rust (optional): about 6 g for the scarf, or 28 cm of 12 mm tartan "
        "ribbon.",
        "Hook: 3.5 mm (US E-4) - smaller than the ball band so stuffing cannot show.",
        "Eyes: 2 x 12 mm black safety eyes, or embroider for under-threes.",
        "Stuffing & notions: polyester fibre fill about 30 g (buy 50 g to over-stuff "
        "the base); stitch marker, tapestry needle, pins, scissors.",
    ],
    "gauge": [
        "Gauge: 11 sc x 12 rounds = 5 cm / 2 in in Yarn A. Not critical, but loose "
        "tension lets stuffing show - drop half a millimetre if your fabric is gappy.",
        "Finished size: about 15 cm / 6 in sitting.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sl st - slip stitch", "sc - single crochet",
        "hdc - half double crochet", "inc - increase (2 sc in one st)",
        "dec - invisible decrease", "BLO - back loop only", "FO - fasten off",
        "(n) - stitch count at round end",
    ],
    "construction": ("Work in a continuous spiral unless a round says join. Mark the "
                     "first stitch of every round. Leave 30-40 cm tails on every piece "
                     "you will sew."),
    "techniques": [
        ("The magic ring",
         "Wrap yarn around two fingers, insert the hook, pull up a loop and work the "
         "first round into the ring; pull the tail tight once the round is complete."),
        ("Working in a spiral",
         "Do not join and do not chain 1 between rounds. Move the marker up each time - "
         "there is no join to count from."),
        ("The invisible decrease",
         "Insert the hook through the FRONT loops only of the next two stitches, yarn "
         "over and pull through both, then yarn over and pull through the remaining two. "
         "Every dec is worked this way - no ridge on visible rounds."),
        ("Back loop only (BLO)",
         "Work into the far loop only, leaving the near loop unused; the unused loops "
         "form a raised ridge. Hamish's hoof line is one BLO round."),
        ("Working around a chain",
         "For the belly patch, crochet into both sides of a starting chain: across the "
         "front, corner increases into the last chain, then back along the opposite "
         "side - turning a chain into a flat oval."),
        ("The lark's head knot",
         "Fold a strand in half, push the folded loop under a stitch with the hook, "
         "pull the two loose ends through the loop and cinch. Used for every fringe "
         "strand and the tail."),
        ("Ladder stitch",
         "The invisible seam: out on one side, pick up one bar on the opposite side, "
         "then one bar back, alternating, pulling snug every few stitches. The "
         "head-to-body join needs two full passes."),
    ],
    "notes": [],
    "pieces": [
        {
            "name": "1. Head - Yarn A",
            "intro": ("Worked from the crown down toward the neck. One straight round "
                      "only - that is what keeps the brow flat and wide instead of "
                      "egg-shaped. Close to 6 stitches at the end."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6,  "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",  "text": "inc in each st around", "stated": 12, "cons": 6,  "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4",  "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": ""},
                    {"label": "R5",  "text": "[3 sc, inc] x 6", "stated": 30, "cons": 24, "prod": 30, "check": "[3 sc, inc] x 6", "note": ""},
                    {"label": "R6",  "text": "[4 sc, inc] x 6", "stated": 36, "cons": 30, "prod": 36, "check": "[4 sc, inc] x 6", "note": "fringe row 3"},
                    {"label": "R7",  "text": "[5 sc, inc] x 6", "stated": 42, "cons": 36, "prod": 42, "check": "[5 sc, inc] x 6", "note": "fringe row 2 / horns"},
                    {"label": "R8",  "text": "[6 sc, inc] x 6", "stated": 48, "cons": 42, "prod": 48, "check": "[6 sc, inc] x 6", "note": "fringe row 1 / ears"},
                    {"label": "R9",  "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": "eyes at R9 - R10"},
                    {"label": "R10", "text": "[6 sc, dec] x 6", "stated": 42, "cons": 48, "prod": 42, "check": "[6 sc, dec] x 6", "note": ""},
                    {"label": "R11", "text": "[5 sc, dec] x 6", "stated": 36, "cons": 42, "prod": 36, "check": "[5 sc, dec] x 6", "note": ""},
                    {"label": "R12", "text": "[4 sc, dec] x 6", "stated": 30, "cons": 36, "prod": 30, "check": "[4 sc, dec] x 6", "note": "lock eye washers, then stuff firmly"},
                    {"label": "R13", "text": "[3 sc, dec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": ""},
                    {"label": "R14", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": ""},
                    {"label": "R15", "text": "[sc, dec] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": "last pinch of stuffing"},
                    {"label": "R16", "text": "dec x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": "close the hole"},
                ], "notes": [
                    "Eyes & head size: place the 12 mm eyes between Rnds 9 and 10, "
                    "7 stitches apart and a touch low on the face (7 sts is about "
                    "32 mm, just under half the head width). LOCK THE WASHERS at "
                    "about Rnd 12, while you can still reach the inside: press each "
                    "washer on until it clicks. The head stays open until Rnd 16 "
                    "closes it - after that the washers are unreachable. Finished "
                    "head about 70 mm wide x 67 mm tall.",
                ]},
            ],
        },
        {
            "name": "2. Muzzle & nostrils - Yarn B",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "inc in each st around", "stated": 12, "cons": 6, "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3", "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4", "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": ""},
                    {"label": "R5", "text": "sc in each st around", "stated": 24, "cons": 24, "prod": 24, "check": "sc in each st around", "note": "face at full width, 35 mm"},
                    {"label": "R6", "text": "sc in each st around", "stated": 24, "cons": 24, "prod": 24, "check": "sc in each st around", "note": ""},
                    {"label": "R7", "text": "sc in each st around", "stated": 24, "cons": 24, "prod": 24, "check": "sc in each st around", "note": ""},
                    {"label": "R8", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": "rim = 26 mm across"},
                ], "notes": [
                    "Finish: FO with a 40 cm tail and stuff lightly. The muzzle FACE is "
                    "about 35 mm across (the wide cream patch you see); the RIM it sews "
                    "by is about 26 mm, spanning roughly six rounds of head. Pin the top "
                    "edge just under the eyes at Rnd 10 and let the lower edge fall at "
                    "Rnd 15-16 near the chin. Centre it, let the face sit a little wider "
                    "than the eye spacing, and sew with small whip stitches, adding a "
                    "whisper more stuffing before you close.",
                    "Nostrils (Yarn C): two short vertical satin stitches, 3 stitches "
                    "apart, on the lower third. Mouth: one tiny horizontal stitch or a "
                    "shallow V below them. (The eye washers were already locked before "
                    "the head was closed at Rnd 16.)",
                    "The wide cream muzzle, low-set eyes and shaggy fringe give the "
                    "Highland stare.",
                ]},
            ],
        },
        {
            "name": "3. Body - Yarn A",
            "intro": "Worked bottom up. The neck is left open at 18 stitches for the head join.",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6,  "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",  "text": "inc in each st around", "stated": 12, "cons": 6,  "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4",  "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": ""},
                    {"label": "R5",  "text": "[3 sc, inc] x 6", "stated": 30, "cons": 24, "prod": 30, "check": "[3 sc, inc] x 6", "note": ""},
                    {"label": "R6",  "text": "[4 sc, inc] x 6", "stated": 36, "cons": 30, "prod": 36, "check": "[4 sc, inc] x 6", "note": ""},
                    {"label": "R7",  "text": "[5 sc, inc] x 6", "stated": 42, "cons": 36, "prod": 42, "check": "[5 sc, inc] x 6", "note": ""},
                    {"label": "R8",  "text": "[6 sc, inc] x 6", "stated": 48, "cons": 42, "prod": 48, "check": "[6 sc, inc] x 6", "note": "front legs join R8 - R9"},
                    {"label": "R9",  "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": ""},
                    {"label": "R10", "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": "body at full width, 70 mm"},
                    {"label": "R11", "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": ""},
                    {"label": "R12", "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": ""},
                    {"label": "R13", "text": "sc in each st around", "stated": 48, "cons": 48, "prod": 48, "check": "sc in each st around", "note": ""},
                    {"label": "R14", "text": "[6 sc, dec] x 6", "stated": 42, "cons": 48, "prod": 42, "check": "[6 sc, dec] x 6", "note": ""},
                    {"label": "R15", "text": "sc in each st around", "stated": 42, "cons": 42, "prod": 42, "check": "sc in each st around", "note": ""},
                    {"label": "R16", "text": "[5 sc, dec] x 6", "stated": 36, "cons": 42, "prod": 36, "check": "[5 sc, dec] x 6", "note": ""},
                    {"label": "R17", "text": "[4 sc, dec] x 6", "stated": 30, "cons": 36, "prod": 30, "check": "[4 sc, dec] x 6", "note": "stuff firmly, pack the base"},
                    {"label": "R18", "text": "[3 sc, dec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": ""},
                    {"label": "R19", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": "leave neck OPEN"},
                ], "notes": [
                    "Finish: FO with a 40 cm tail; do not close. Body is about 19 "
                    "rounds (79 mm); with the head seated on the neck ring the finished "
                    "sitting height is about 15 cm / 6 in.",
                ]},
            ],
        },
        {
            "name": "4. Belly patch - Yarn B (optional)",
            "intro": "A flat oval worked around a chain, sewn on last.",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "Found.", "skip_check": True, "text": "ch 9", "stated": None, "cons": None, "prod": 8, "check": "ch 9", "note": "-"},
                    {"label": "R1", "text": "sc in 2nd ch, sc in next 6, 3 sc in last ch, sc in next 6, 2 sc in last loop", "stated": 18, "cons": 8, "prod": 18, "check": None, "note": "-"},
                    {"label": "R2", "text": "inc, 6 sc, inc x 3, 6 sc, inc x 2", "stated": 24, "cons": 18, "prod": 24, "check": None, "note": "-"},
                    {"label": "R3", "text": "sc, inc, 6 sc, [sc, inc] x 3, 6 sc, [sc, inc] x 2", "stated": 30, "cons": 24, "prod": 30, "check": None, "note": "-"},
                    {"label": "R4", "text": "2 sc, inc, 6 sc, [2 sc, inc] x 3, 6 sc, [2 sc, inc] x 2", "stated": 36, "cons": 30, "prod": 36, "check": None, "note": "-"},
                ], "notes": [
                    "Sl st, FO with a long tail; sew centred on the front with the "
                    "lower edge about 3 rounds up from the base. Skip it for a plain "
                    "ginger front - both are correct.",
                ]},
            ],
        },
        {
            "name": "5. Legs - start with Yarn C, change to Yarn A (make 4)",
            "intro": ("All four identical; the sitting pose comes from where and at "
                      "what angle you sew them. Sixteen rounds = a 67 mm leg."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "6 sc in MR (Yarn C)", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": "hoof"},
                    {"label": "R2",  "text": "inc in each st around", "stated": 12, "cons": 6, "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4",  "text": "sc in each st around", "stated": 18, "cons": 18, "prod": 18, "check": "sc in each st around", "note": ""},
                    {"label": "R5",  "text": "sc in each st around", "stated": 18, "cons": 18, "prod": 18, "check": "sc in each st around", "note": ""},
                    {"label": "R6",  "text": "BLO sc around", "stated": 18, "cons": 18, "prod": 18, "check": "sc in each st around", "note": "change to Yarn A - ridge"},
                    {"label": "R7",  "text": "sc in each st around", "stated": 18, "cons": 18, "prod": 18, "check": "sc in each st around", "note": ""},
                    {"label": "R8",  "text": "[sc, dec] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": "stuff hoof firmly"},
                    {"label": "R9",  "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R10", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R11", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R12", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R13", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": "upper leg light"},
                    {"label": "R14", "text": "[2 sc, dec] x 3", "stated": 9, "cons": 12, "prod": 9, "check": "[2 sc, dec] x 3", "note": ""},
                    {"label": "R15", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": ""},
                    {"label": "R16", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "leave top open"},
                ], "notes": [
                    "Leg length - read before you sew. A 67 mm leg joins much lower "
                    "than it is long, so it splays: front about 55 degrees from "
                    "vertical, back about 68-70 degrees (near horizontal) - that is "
                    "the low Highland sit. For a tidier upright sit, work the FRONT "
                    "pair only to Rnd 10 (42 mm); leave the back pair at 16 rounds as "
                    "haunches.",
                ]},
            ],
        },
        {
            "name": "6. Ears - make 2 of each layer",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "INNER ear - Yarn B (make 2) & OUTER ear - Yarn A (make 2)", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "[sc, inc] x 3", "stated": 9, "cons": 6, "prod": 9, "check": "[sc, inc] x 3", "note": ""},
                    {"label": "R3", "text": "[2 sc, inc] x 3", "stated": 12, "cons": 9, "prod": 12, "check": "[2 sc, inc] x 3", "note": ""},
                    {"label": "R4", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R5", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R6", "text": "[2 sc, dec] x 3", "stated": 9, "cons": 12, "prod": 9, "check": "[2 sc, dec] x 3", "note": ""},
                    {"label": "R7", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": ""},
                ], "notes": [
                    "Work BOTH layers through all 7 rounds. FO the inner ear with a "
                    "short tail; FO the outer with a long tail. Lay the inner on the "
                    "outer, cream side facing you, and join them around the edge: "
                    "either single crochet around the edge through both layers in "
                    "Yarn A (about 1 sc per stitch, plus extras at the corners), or "
                    "whip-stitch around with the outer's tail. Flatten and pinch the "
                    "base with 2-3 stitches so the ear cups forward.",
                ]},
            ],
        },
        {
            "name": "7. Horns - Yarn B (make 2)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "4 sc in MR", "stated": 4, "cons": None, "prod": 4, "check": "4 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "[sc, inc] x 2", "stated": 6, "cons": 4, "prod": 6, "check": "[sc, inc] x 2", "note": ""},
                    {"label": "R3", "text": "sc in each st around", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                    {"label": "R4", "text": "sc in each st around", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                    {"label": "R5", "text": "[2 sc, inc] x 2", "stated": 8, "cons": 6, "prod": 8, "check": "[2 sc, inc] x 2", "note": ""},
                    {"label": "R6", "text": "sc in each st around", "stated": 8, "cons": 8, "prod": 8, "check": "sc in each st around", "note": ""},
                    {"label": "R7", "text": "sc in each st around", "stated": 8, "cons": 8, "prod": 8, "check": "sc in each st around", "note": "stuff tip only"},
                ], "notes": [
                    "FO with a tail; stuff the tip only. Short and slightly curved - "
                    "tilt each horn out and a little back when you sew.",
                ]},
            ],
        },
        {
            "name": "8. Tail - Yarn A",
            "intro": "",
            "kind": "text",
            "subpieces": [
                {"name": "", "rows": [], "notes": [
                    "Cut 6 strands of Yarn A, each 22 cm / 8.5 in. Fold the bundle in "
                    "half and attach with a lark's head at the centre-back just above "
                    "the last increase round: pull the folded loop through a stitch, "
                    "then the tails through the loop. Folding gives 12 hanging ends; "
                    "divide into 3 groups of 4, braid 4 cm, knot firmly and trim into "
                    "a small tassel.",
                ]},
            ],
        },
        {
            "name": "9. Fringe - Yarn A",
            "intro": "",
            "kind": "text",
            "subpieces": [
                {"name": "", "rows": [], "notes": [
                    "Attach AFTER the horns and ears so you can part the hair around "
                    "them. Cut 44 strands, each 14 cm / 5.5 in (swap 6 for Yarn C for "
                    "depth). Attach with lark's head knots in a horseshoe from one ear, "
                    "across the brow, to the other, filling three rows across the front "
                    "of the head: every stitch along the front of Rnd 8 (24 knots), then "
                    "every other stitch along the front of Rnd 7 (about 10 knots) and "
                    "Rnd 6 (about 9 knots) - about 24 + 10 + 9 = 43 knots.",
                    "Tousle, then trim so the fringe grazes the eyes and breaks into "
                    "uneven points. Highland hair is weather-beaten, not a salon "
                    "fringe.",
                ]},
            ],
        },
        {
            "name": "10. Tartan scarf - Yarn D (optional)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "Found.", "skip_check": True, "text": "ch 61", "stated": None, "cons": None, "prod": 60, "check": "ch 61", "note": "-"},
                    {"label": "Row 1", "text": "hdc in 2nd ch from hook and in each ch across", "stated": 60, "cons": 60, "prod": 60, "check": "hdc in each st around", "note": "-"},
                    {"label": "Row 2", "text": "ch 1, turn, hdc across", "stated": 60, "cons": 60, "prod": 60, "check": "hdc in each st around", "note": "-"},
                ], "notes": [
                    "FO; add a 3-strand tassel at each end or weave a second colour as "
                    "a slip-stitch stripe to hint at tartan, then tie loosely under the "
                    "muzzle. Ribbon shortcut: 28 cm of 12 mm rust tartan ribbon, "
                    "knotted once.",
                ]},
            ],
        },
    ],
    "assembly": [
        "Assembly - work in this order:",
        "1. Muzzle & face sewn (section 2) - the eye washers were locked before "
        "the head was closed at Rnd 16.",
        "2. Horns between Rnds 5 and 7, 6 stitches apart, angled out and slightly back.",
        "3. Ears just outside and below each horn, centred on Rnds 8-9, cupped forward.",
        "4. Fringe attached and trimmed (section 9), parting around horns and ears.",
        "5. Head to body: closed head on the open 18-st neck ring (Rnd 19). "
        "Ball-on-ring join - pack the neck firmly, ladder-stitch around TWICE, "
        "tilt the muzzle slightly down.",
        "6. Back legs: lower sides across Rnds 3-6, almost on the base, splayed "
        "near horizontal.",
        "7. Front legs: FRONT across Rnds 8-9, about 8 sts apart, angled forward "
        "about 55 degrees.",
        "8. Belly patch - only if you made it.",
        "9. Tail & scarf: attach the tassel tail, tie the scarf, weave in every end "
        "and fluff the fringe.",
    ],
    "troubleshooting": [
        ("He will not sit.",
         "Restuff the body base firmly and sew the back legs lower and wider - "
         "closer to horizontal than you think."),
        ("Front hooves float.",
         "Sewn too high - they belong on Rnds 8-9, not under the neck. If they still "
         "float, the legs are too long: work the front pair to Rnd 10."),
        ("Stuffing shows.",
         "Drop half a hook size, or hold a matching thread with the yarn on visible "
         "rounds."),
        ("Face looks blank.",
         "The eyes are too high. Low eyes plus a wide muzzle is the Highland stare."),
        ("Fringe is sparse.",
         "Add a fourth row behind the horns and mix in one darker shade."),
        ("Horns flop.",
         "Under-stuffed at the tip, or sewn only at the edge - stitch a full round "
         "into the head fabric."),
        ("Head tips forward.",
         "The neck ring grips the head only about 8 mm up. Pack the neck before "
         "closing and make the second ladder-stitch pass tight."),
    ],
    "colorways": ["Ginger", "Caramel", "Highland black", "Cream", "Roan red"],
    "extras": [
        {"name": "Three sizes, one pattern", "type": "table",
         "headers": ["Version", "Yarn / hook", "Eyes", "Height"],
         "rows": [
             ["Wee Hamish", "DK / #3 - 2.75 mm", "8-9 mm", "~12 cm"],
             ["Classic", "Worsted / #4 - 3.5 mm", "12 mm", "~15 cm"],
             ["Cuddle Hamish", "Bulky chenille / #5 - 5.0 mm", "16-18 mm", "~21 cm"],
         ],
         "outro": ("Stitch counts stay the same; only yarn, hook and stuffing change. "
                   "Yarn scales with the square of the height and stuffing with the "
                   "cube - buy generously for the big chenille version.")},
    ],
    "designer_notes": [
        "Why the legs join so low: back legs (16 rnd, 67 mm, sewn to Rnds 3-6) and "
        "front legs (sewn to Rnds 8-9) splay at the checked angles so all four "
        "hooves land level. This low join is the most common failure on sitting "
        "Highland cows.",
        "Bottom-heavy by design: stuff the lower body firmly and keep the shape "
        "squat. Hamish is meant to settle onto his base and stare.",
    ],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original work "
                      "and intellectual property of Novality Store, designed by "
                      "Novality Crochet Studio. Design Code NS 01."),
        "may": ("Make as many finished Hamishes as you like for yourself, gifts, or "
                "charity. Sell physical finished items made from this pattern in "
                "small batches, in shops, markets and online, provided credit is "
                "given to \u201cNovality Store\u201d."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos beyond crediting "
                   "the pattern. Do not mass-produce finished items commercially "
                   "without written permission."),
        "safety": ("This pattern has not been tested to a toy-safety standard "
                   "(ASTM F963 / EN 71) and uses 12 mm safety eyes and knotted yarn "
                   "fringe. Finished items made for sale must be assessed by the "
                   "seller against local toy-safety laws; for young children, "
                   "embroider the eyes and secure every seam and knot."),
    },
    "hashtag": "#HamishTheHighlandCow",
    "closing": ("We love seeing your coos. Thank you for supporting an independent "
                "pattern designer."),
}
