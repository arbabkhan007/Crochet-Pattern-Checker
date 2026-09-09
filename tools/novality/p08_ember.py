"""Pattern 08 - Ember the Baby Dragon (Design Code NS 08)."""

PATTERN = {
    "id": "ember",
    "number": 8,
    "design_code": "NS 08",
    "title": "Ember the Baby Dragon",
    "tagline": ("A chunky, big-headed baby dragon with a stubby snout, scalloped "
                "wings and a ridge of spikes down the back. She sits, with "
                "folding haunches and splayed front legs."),
    "meta": ["US terms", "Intermediate", "4 - 5 hours"],
    "finished_size": [
        "About 11 cm (4.3 in) tall seated.",
        "12.5 cm (5 in) wingspan. 5 cm (2 in) tail.",
        "A sitting dragon - her body rests on the table and her legs pose "
        "rather than lift her.",
    ],
    "safety": [
        "Ember uses 10 mm safety eyes, which are a small part and a choking "
        "hazard. Lock the washers from the inside before the head is joined to "
        "the body, and pull-test each eye. She is a decorative piece, not a "
        "toy for young children, and has not been tested to ASTM F963 or "
        "EN 71. To give her to a child, embroider the eyes instead and check "
        "every seam first.",
    ],
    "materials": [
        "Main yarn: worsted #4, about 30 g used (buy a 50 g ball) - sage "
        "green, dusty teal, lilac or charcoal. The extra allows for tails, "
        "sewing and a second attempt.",
        "Contrast yarn: worsted #4, about 20 g in a contrast cream or pale "
        "gold - used for the wings, horns and spikes, so all the details "
        "match.",
        "Hook: 3.5 mm (US E/4).",
        "Eyes: 2 x 10 mm safety eyes - slit-pupil dragon eyes if you can get "
        "them.",
        "Also needed: polyester fibre fill about 10 g; tapestry needle; "
        "stitch markers; pins.",
    ],
    "gauge": [
        "Gauge: about 4.5 mm per stitch and 4.3 mm per round. Check on the "
        "body after Rnd 5 - 30 stitches should measure about 43 mm across "
        "when stuffed. If your stitches are wider, crochet more tightly or "
        "drop to a 3.0 mm hook or the stuffing will show.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sc - single crochet",
        "hdc - half double crochet", "dc - double crochet",
        "inc - increase (2 sc in one st)", "dec - invisible decrease",
        "sl st - slip stitch", "FO - fasten off",
        "(n) - stitch count at round end",
    ],
    "construction": ("Work in a continuous spiral unless a row says to turn; "
                     "mark the first stitch of every round. The wings and the "
                     "spike strip are the exceptions - both are worked flat. "
                     "Work every stitch through both loops unless a note says "
                     "otherwise."),
    "techniques": [
        ("The magic ring",
         "Every piece begins with a magic ring. Pull the tail tight once the "
         "first round is complete."),
        ("Working in a spiral",
         "Keep a stitch marker in the first stitch of every round; there is "
         "no join to count from."),
        ("Matched open joins",
         "Ember's head and her neck are BOTH left open at 18 stitches, so "
         "the two edges are the same size and can be ladder-stitched "
         "together cleanly. This is the single most important structural "
         "detail - the head is heavy and this joint carries all of it. Do "
         "not close the head down to a point; stop at 18 stitches. Closing "
         "a heavy dragon head down to 6 stitches leaves a small gathered "
         "point sewn to a wide neck ring - a tiny seam carrying a big head, "
         "which is exactly why a dragon's head flops."),
    ],
    "notes": [
        "How the size adds up: body Rnd 1-13 is 13 rounds x 4.3 mm = 56 mm; "
        "head Rnd 1-11 is 11 rounds x 4.3 mm = 47 mm; seated together about "
        "103 mm = 11 cm. Wingspan: 45 + 34 + 45 = about 124 mm = 12.5 cm. "
        "Tail: 12 rounds x 4.3 mm = 52 mm = 5 cm.",
    ],
    "pieces": [
        {
            "name": "1. Head - main colour (worked top-down)",
            "intro": ("Worked top-down and LEFT OPEN - do not close it and do "
                      "not fasten off. A big head is what makes a dragon read "
                      "as a baby dragon. Two straight rounds only, then the "
                      "decreases."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6,  "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",  "text": "inc in each st around", "stated": 12, "cons": 6,  "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4",  "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": ""},
                    {"label": "R5",  "text": "[3 sc, inc] x 6", "stated": 30, "cons": 24, "prod": 30, "check": "[3 sc, inc] x 6", "note": ""},
                    {"label": "R6",  "text": "[4 sc, inc] x 6", "stated": 36, "cons": 30, "prod": 36, "check": "[4 sc, inc] x 6", "note": "head at full width"},
                    {"label": "R7",  "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": "eyes at R7 - R8"},
                    {"label": "R8",  "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": ""},
                    {"label": "R9",  "text": "[4 sc, dec] x 6", "stated": 30, "cons": 36, "prod": 30, "check": "[4 sc, dec] x 6", "note": ""},
                    {"label": "R10", "text": "[3 sc, dec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": "stuff firmly"},
                    {"label": "R11", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": "LEAVE OPEN - matches neck"},
                ], "notes": [
                    "Finish: stuff the head firmly. Leave the open 18-stitch "
                    "edge for sewing to the body's neck (a long tail is "
                    "optional). The snout is sewn on next, then the eyes, "
                    "BEFORE the head is joined.",
                ]},
            ],
        },
        {
            "name": "2. Snout - main colour (make 1)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "[sc, inc] x 3", "stated": 9, "cons": 6, "prod": 9, "check": "[sc, inc] x 3", "note": ""},
                    {"label": "R3", "text": "[2 sc, inc] x 3", "stated": 12, "cons": 9, "prod": 12, "check": "[2 sc, inc] x 3", "note": ""},
                    {"label": "R4", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R5", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                ], "notes": [
                    "Finish: FO with a long tail and stuff lightly. Pin "
                    "centred on Rnds 8-11 of the head, just below the eye "
                    "line, and sew all the way around. It must project past "
                    "the curve of the head, not sit flush - a dragon "
                    "without a projecting snout reads as a bear. Embroider "
                    "two small nostrils at the tip.",
                ]},
            ],
        },
        {
            "name": "3. Body - main colour (worked bottom-up)",
            "intro": ("Worked bottom-up. The neck is left open at 18 stitches "
                      "so the head can be seated on it. Pack the neck firmly "
                      "before you join the head - a soft neck is what lets "
                      "the head flop forward."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6,  "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",  "text": "inc in each st around", "stated": 12, "cons": 6,  "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4",  "text": "[2 sc, inc] x 6", "stated": 24, "cons": 18, "prod": 24, "check": "[2 sc, inc] x 6", "note": "tail attaches R4 - R6"},
                    {"label": "R5",  "text": "[3 sc, inc] x 6", "stated": 30, "cons": 24, "prod": 30, "check": "[3 sc, inc] x 6", "note": "full width - check gauge"},
                    {"label": "R6",  "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": "back legs at R6"},
                    {"label": "R7",  "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R8",  "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": "front legs at R8"},
                    {"label": "R9",  "text": "sc in each st around", "stated": 30, "cons": 30, "prod": 30, "check": "sc in each st around", "note": ""},
                    {"label": "R10", "text": "[3 sc, dec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": "wings at R10 - R11"},
                    {"label": "R11", "text": "sc in each st around", "stated": 24, "cons": 24, "prod": 24, "check": "sc in each st around", "note": ""},
                    {"label": "R12", "text": "[2 sc, dec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": "stuff firmly"},
                    {"label": "R13", "text": "sc in each st around", "stated": 18, "cons": 18, "prod": 18, "check": "sc in each st around", "note": "LEAVE THE NECK OPEN"},
                ], "notes": [
                    "Finish: FO with a 40 cm tail; do not close. When you "
                    "join the head, ladder-stitch all the way around and "
                    "then make a second pass and pull it tight - this "
                    "joint carries the whole head.",
                ]},
            ],
        },
        {
            "name": "4. Legs - main colour (make 4)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": "all four"},
                    {"label": "R2", "text": "[sc, inc] x 3", "stated": 9, "cons": 6, "prod": 9, "check": "[sc, inc] x 3", "note": "all four"},
                    {"label": "R3", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "all four"},
                    {"label": "R4", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "all four"},
                    {"label": "R5", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "all four"},
                    {"label": "R6", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "BACK legs finish here"},
                    {"label": "R7", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "front legs only"},
                    {"label": "R8", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "front legs only"},
                ], "notes": [
                    "Finish: stuff the lower half lightly, flatten the top "
                    "3 stitches, FO with a long tail. The pairs are "
                    "different lengths on purpose: back legs (6 rnd / "
                    "26 mm) attach at Rnd 6, 26 mm up; front legs (8 rnd / "
                    "34 mm) attach at Rnd 8, 34 mm up. A higher join needs "
                    "a longer leg so all four feet reach the table. Sew "
                    "each pair about 8 stitches apart; angle the back "
                    "legs under as haunches and the front legs slightly "
                    "forward. The body rests on the table - the legs "
                    "pose, they don't lift her.",
                ]},
            ],
        },
        {
            "name": "5. Tail - main colour",
            "intro": "Worked from the tip up so it tapers naturally.",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "4 sc in MR", "stated": 4, "cons": None, "prod": 4, "check": "4 sc in magic ring", "note": "tip"},
                    {"label": "R2",  "text": "sc in each st around", "stated": 4, "cons": 4, "prod": 4, "check": "sc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 2", "stated": 6, "cons": 4, "prod": 6, "check": "[sc, inc] x 2", "note": ""},
                    {"label": "R4",  "text": "sc in each st around", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                    {"label": "R5",  "text": "sc in each st around", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                    {"label": "R6",  "text": "[2 sc, inc] x 2", "stated": 8, "cons": 6, "prod": 8, "check": "[2 sc, inc] x 2", "note": ""},
                    {"label": "R7",  "text": "sc in each st around", "stated": 8, "cons": 8, "prod": 8, "check": "sc in each st around", "note": ""},
                    {"label": "R8",  "text": "sc in each st around", "stated": 8, "cons": 8, "prod": 8, "check": "sc in each st around", "note": ""},
                    {"label": "R9",  "text": "[3 sc, inc] x 2", "stated": 10, "cons": 8, "prod": 10, "check": "[3 sc, inc] x 2", "note": ""},
                    {"label": "R10", "text": "sc in each st around", "stated": 10, "cons": 10, "prod": 10, "check": "sc in each st around", "note": ""},
                    {"label": "R11", "text": "sc in each st around", "stated": 10, "cons": 10, "prod": 10, "check": "sc in each st around", "note": ""},
                    {"label": "R12", "text": "sc in each st around", "stated": 10, "cons": 10, "prod": 10, "check": "sc in each st around", "note": "base"},
                ], "notes": [
                    "Finish: stuff lightly, FO with a long tail, flatten "
                    "the open end and sew it to the back of the body at "
                    "Rnds 4-6.",
                ]},
            ],
        },
        {
            "name": "6. Horns - contrast colour (make 2)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "4 sc in MR", "stated": 4, "cons": None, "prod": 4, "check": "4 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "sc in each st around", "stated": 4, "cons": 4, "prod": 4, "check": "sc in each st around", "note": ""},
                    {"label": "R3", "text": "[sc, inc] x 2", "stated": 6, "cons": 4, "prod": 6, "check": "[sc, inc] x 2", "note": ""},
                    {"label": "R4", "text": "sc in each st around", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                    {"label": "R5", "text": "sc in each st around", "stated": 6, "cons": 6, "prod": 6, "check": "sc in each st around", "note": ""},
                ], "notes": [
                    "Finish: do not stuff; FO with a long tail. Sew to "
                    "the crown of the head, 6 stitches apart, angled "
                    "back.",
                ]},
            ],
        },
        {
            "name": "7. Wings - contrast colour (make 2, worked flat)",
            "intro": "Ch 11. Work in turned rows (ch 1 and turn at each row end):",
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "Found.", "skip_check": True, "text": "ch 11", "stated": None, "cons": None, "prod": 10, "check": "ch 11", "note": "-"},
                    {"label": "Row 1", "text": "from the 2nd ch: sc in 4, hdc in 3, dc in 3", "stated": 10, "cons": 10, "prod": 10, "check": None, "note": "-"},
                    {"label": "Row 2", "text": "sc in 3, hdc in 3, dc in 4", "stated": 10, "cons": 10, "prod": 10, "check": None, "note": "-"},
                    {"label": "Row 3", "text": "sc in 2, hdc in 4, dc in 4", "stated": 10, "cons": 10, "prod": 10, "check": None, "note": "-"},
                    {"label": "Row 4", "text": "sl st in first 2, (sc, hdc, dc, hdc, sc) all in next st, sl st in next 2, (sc, hdc, dc, hdc, sc) all in next st, sl st in last 4", "stated": None, "cons": 10, "prod": None, "check": None, "note": "scalloped edge - FO with a 25 cm tail"},
                ], "notes": [
                    "The scallop maths: the slip-stitch anchors are "
                    "2 + 2 + 4 = 8 stitches; the two shells each fan "
                    "from a single stitch (2 more), so all 10 stitches "
                    "of Row 3 are consumed and nothing is left over. "
                    "Pin the straight inner edge across Rnds 10-11 and "
                    "sew the WHOLE edge so the scalloped edge stays "
                    "free.",
                ]},
            ],
        },
        {
            "name": "8. Spike strip - contrast colour",
            "intro": ("One continuous strip sewn down the centre back from "
                      "crown to tail tip - nine spikes: 3 on the head, 4 on "
                      "the body, 2 on the tail."),
            "kind": "text",
            "subpieces": [
                {"name": "", "rows": [], "notes": [
                    "Ch 4. Sc in the 2nd ch from the hook, then work "
                    "this group NINE times: ch 4, sl st in the 2nd ch "
                    "from the hook, sc in the next ch, hdc in the next "
                    "ch. Then sc in the next 2 and FO with a long tail.",
                    'The strip is one starting chain of 4 plus nine '
                    "chain-4 spike units - ten chain-4 groups and 40 "
                    "chains in total, worked end to end (not a single "
                    "40-chain). Each group makes one small cone (about "
                    "10 mm tall); the last stitch of one group is where "
                    "the next begins, so the nine spikes form one "
                    "continuous ridge with no gaps.",
                    "The strip is about 13.5-15 cm long - slightly "
                    "under the crown-to-tail path, so it goes on "
                    "slightly snug. PIN it from crown to tail tip "
                    "first; if it runs short add one more spike (about "
                    "13.5 mm), if long unpick from the plain end. The "
                    "spikes deliberately touch - do not add plain "
                    "stitches between them.",
                ]},
            ],
        },
    ],
    "assembly": [
        "Assembly - work in this order:",
        "1. Snout to the head, centred on Rnds 8-11, below the eye line.",
        "2. Eyes between Rnds 7 and 8, 8 stitches apart, just above the "
        "snout. Fit the washers BEFORE the head is joined - once closed "
        "you cannot reach inside.",
        "3. Horns to the crown, 6 stitches apart, angled back.",
        "4. Head to body: both edges open at 18 stitches. Pack the neck "
        "firmly, seat the head and ladder-stitch around, then a second "
        "tight pass.",
        "5. Legs: back pair to Rnd 6, front pair to Rnd 8, angled as "
        "described.",
        "6. Tail to the back of the body at Rnds 4-6.",
        "7. Wings across Rnds 10-11, sewn along the whole straight edge.",
        "8. Spike strip LAST - pin from crown to tail tip before you sew "
        "a single stitch.",
    ],
    "troubleshooting": [
        ("Head flops forward.",
         "Pack the neck firmly before closing and make the second "
         "ladder-stitch pass tight. If it still moves, the edges did "
         "not match - both head and neck must be open at 18 stitches."),
        ("Rocks back onto haunches.",
         "The legs are all the same length and they cannot be. Back "
         "legs attach 26 mm up, front 34 mm up - work the back legs "
         "6 rounds and the front 8."),
        ("Will not sit.",
         "Legs sewn too high, or the base is under-stuffed. Back legs "
         "on Rnd 6, front on Rnd 8; keep the lower body firm enough "
         "to sit on."),
        ("Wings droop.",
         "Sew along the whole straight inner edge, not just the top "
         "corner."),
        ("Spike strip is the wrong length / curves.",
         "It is nine chain-4 spike units on one starting chain - ten "
         "chain-4 groups worked end to end, not a single 40-chain. "
         "Pin the entire strip from crown to tail before sewing; add "
         "or unpick a spike as needed. This is the most visible seam."),
        ("Looks like a bear.",
         "The snout is missing or under-stuffed - it must project "
         "past the dome of the head."),
        ("Stuffing shows through.",
         "Gauge too loose - 30 stitches should measure 43 mm across. "
         "Crochet tighter or drop to a 3.0 mm hook."),
    ],
    "colorways": ["Sage green", "Dusty teal", "Lilac", "Charcoal", "Blush pink"],
    "extras": [],
    "designer_notes": [
        "The continuous spike ridge runs from crown to tail tip - it is "
        "sewn on last and pinned before any stitch.",
    ],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original "
                      "work and intellectual property of Novality Store, designed "
                      "by Novality Crochet Studio. Design Code NS 08."),
        "may": ("Make as many finished Embers as you like for yourself, gifts, "
                "or charity. Sell physical finished items made from this "
                "pattern in small batches, in shops, markets and online, "
                "provided credit is given to \u201cNovality Store\u201d."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos beyond crediting "
                   "the pattern. Do not mass-produce finished items commercially "
                   "without written permission."),
        "safety": ("This pattern has not been tested to a toy-safety standard "
                   "(ASTM F963 / EN 71) and uses 10 mm safety eyes. Finished "
                   "items made for sale must be assessed by the seller against "
                   "local toy-safety laws; for young children, embroider the "
                   "eyes."),
    },
    "hashtag": "#EmberTheBabyDragon",
    "closing": ("We love seeing your dragons. Thank you for supporting an "
                "independent pattern designer."),
}
