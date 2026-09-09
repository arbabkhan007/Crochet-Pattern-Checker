"""Pattern 04 - Coco the Capybara (Design Code NS 04)."""

PATTERN = {
    "id": "coco",
    "number": 4,
    "design_code": "NS 04",
    "title": "Coco the Capybara",
    "tagline": ("A low, round, bottom-heavy capybara with a blunt sewn-on muzzle, "
                "plump stuffed legs and a calm embroidered sleeping face. No safety "
                "eyes and no small plastic parts."),
    "meta": ["No plastic eyes", "Intermediate", "2.5 - 3 hours"],
    "finished_size": [
        "About 10.3 cm (4 in) tall standing on all four legs.",
        "About 5 cm (2 in) wide at the widest part of the body.",
        "Squat and bottom-heavy, standing on her feet rather than her belly.",
    ],
    "safety": [
        "Coco has no safety eyes and no small plastic parts, which makes the face "
        "safer than a safety-eyed toy. That does not make the finished toy suitable "
        "for babies: Coco is a stuffed toy with a sewn-on muzzle and sewn-on ears, "
        "and it has not been tested to a toy-safety standard such as ASTM F963 or "
        "EN 71.",
        "Intended as a decorative item or a gift for a child old enough not to "
        "chew it. Check every seam - especially the muzzle and ears - before giving "
        "Coco to a young child.",
    ],
    "materials": [
        "Main yarn: worsted weight (#4), warm brown, about 30 g. A smooth matte "
        "yarn shows the stitch texture best.",
        "Face yarn: worsted weight (#4), dark brown, about 5 g, for the closed "
        "eyes, nose and mouth. Use the same weight as the main yarn.",
        "Hook: 3.0 mm. The gauge is written for this hook.",
        "Eyes: none. The sleeping face is embroidered - no safety eyes.",
        "Also needed: polyester fiber filling about 5-8 g; yarn needle; stitch "
        "marker; pins. Pins matter: the muzzle and ears are pinned before sewing.",
    ],
    "gauge": [
        "Gauge: 36 sc around measures about 52 mm in diameter when stuffed "
        "(4.5 mm per stitch, 4.3 mm per round). Check it on the body after Rnd 6 - "
        "a stuffed tube, not a flat swatch. If your 36 sts measure wider than "
        "52 mm, crochet more tightly or go down a hook size; a loose gauge will "
        "show stuffing.",
        "Finished size: about 10.3 cm (4 in) tall, 5 cm (2 in) wide.",
    ],
    "abbreviations": [
        "MR - magic ring", "ch - chain", "sc - single crochet",
        "inc - increase (2 sc in one st)", "invdec - invisible decrease",
        "sl st - slip stitch", "st(s) - stitch(es)", "Rnd(s) - round(s)",
        "FO - fasten off", "(n) - stitch count at round end",
    ],
    "construction": ("Work in a continuous spiral - do not join and do not chain 1 "
                     "between rounds. Keep a marker in the first stitch of every "
                     "round. Work every stitch through both loops unless a note "
                     "says otherwise."),
    "techniques": [
        ("The magic ring",
         "Every piece begins with a magic ring. Pull the tail tight once the first "
         "round is complete."),
        ("Working in a spiral",
         "Keep a stitch marker in the first stitch of every round and move it up. "
         "There is no seam and no join to count from."),
        ("The two-layer leg join",
         "This is the only fiddly step - worth practising once on a scrap magic "
         "ring. Hold a finished leg against the body with the pinched-flat top of "
         "the leg lying against the outside of the body. Insert the hook through "
         "BOTH the leg and the body stitch and work one single crochet; the leg "
         "edge and body stitch are treated as one stitch. They still count as one "
         "stitch each, so every count in the body table stays correct. Pinch the "
         "leg top flat first - a round, un-pinched top will not lie against the "
         "curved body and the join will pucker. A 9-stitch leg top flattens to "
         "about 5 stitches across - pinch it down to a strip about 3 stitches wide "
         "and hold it while you join. The stitches you don't join bunch up inside, "
         "and that bunch makes the leg look plump rather than tubular."),
    ],
    "notes": [
        "How the height adds up: the body (Rnd 1-20) is 20 rounds x 4.3 mm = "
        "86 mm; the short 8/9-round legs lift the body about 17 mm off the table, "
        "for a total standing height of about 103 mm = 10.3 cm.",
    ],
    "pieces": [
        {
            "name": "1. Legs - make 4",
            "intro": ("Stuff the lower half of each leg lightly, leaving the top "
                      "loose. Back legs stop after Rnd 8; front legs work Rnd 9 "
                      "too - they join one round higher and need to be one round "
                      "longer so all four feet reach the table level."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": "all four"},
                    {"label": "R2", "text": "[sc, inc] x 3", "stated": 9, "cons": 6, "prod": 9, "check": "[sc, inc] x 3", "note": "all four"},
                    {"label": "R3", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "all four"},
                    {"label": "R4", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "all four"},
                    {"label": "R5", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "all four"},
                    {"label": "R6", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "all four"},
                    {"label": "R7", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "all four"},
                    {"label": "R8", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "BACK legs finish here"},
                    {"label": "R9", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": "FRONT legs only"},
                ], "notes": [
                    "Finish: FO with a long tail for sewing. Before joining, pinch "
                    "the whole 9-stitch top flat into a narrow strip about 3 "
                    "stitches wide (see technique 3).",
                ]},
            ],
        },
        {
            "name": "2. Ears (make 2) & muzzle (make 1)",
            "intro": "",
            "kind": "table",
            "subpieces": [
                {"name": "Ears - make 2 (do not stuff)", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "[sc, inc] x 3", "stated": 9, "cons": 6, "prod": 9, "check": "[sc, inc] x 3", "note": ""},
                    {"label": "R3", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": ""},
                    {"label": "R4", "text": "sc in each st around", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": ""},
                    {"label": "R5", "text": "sc in each st around, then FO", "stated": 9, "cons": 9, "prod": 9, "check": "sc in each st around", "note": ""},
                ], "notes": []},
                {"name": "Muzzle - make 1 (stuff lightly)", "rows": [
                    {"label": "R1", "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6, "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2", "text": "[sc, inc] x 3", "stated": 9, "cons": 6, "prod": 9, "check": "[sc, inc] x 3", "note": ""},
                    {"label": "R3", "text": "[2 sc, inc] x 3", "stated": 12, "cons": 9, "prod": 12, "check": "[2 sc, inc] x 3", "note": ""},
                    {"label": "R4", "text": "sc in each st around", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                    {"label": "R5", "text": "sc in each st around, then FO", "stated": 12, "cons": 12, "prod": 12, "check": "sc in each st around", "note": ""},
                ], "notes": [
                    "Ears: FO with a long tail, do not stuff - a shallow cup. "
                    "Muzzle: FO with a long tail and stuff lightly, just enough to "
                    "hold a dome; it should sit proud of the head when sewn on.",
                ]},
            ],
        },
        {
            "name": "3. Body & head - one piece",
            "intro": ("Both are 36 stitches around with only a shallow waist between "
                      "them - that is what makes Coco read as one round blob rather "
                      "than a snowman. The legs are joined low at Rnd 4-5 (see "
                      "below)."),
            "kind": "table",
            "subpieces": [
                {"name": "", "rows": [
                    {"label": "R1",  "text": "6 sc in MR", "stated": 6, "cons": None, "prod": 6,  "check": "6 sc in magic ring", "note": ""},
                    {"label": "R2",  "text": "inc in each st around", "stated": 12, "cons": 6,  "prod": 12, "check": "inc in each st around", "note": ""},
                    {"label": "R3",  "text": "[sc, inc] x 6", "stated": 18, "cons": 12, "prod": 18, "check": "[sc, inc] x 6", "note": ""},
                    {"label": "R4",  "text": "join BL1: 3 sc, [sc, inc] x 3, join BL2: 3 sc, [sc, inc] x 3", "stated": 24, "cons": 18, "prod": 24, "check": None, "note": "join the BACK legs"},
                    {"label": "R5",  "text": "1 sc, inc, 1 sc, inc, 1 sc, join FL1: 3 sc, [sc, inc] x 3, 1 sc, join FL2: 3 sc, 3 sc, inc, 2 sc", "stated": 30, "cons": 24, "prod": 30, "check": None, "note": "join the FRONT legs"},
                    {"label": "R6",  "text": "[4 sc, inc] x 6", "stated": 36, "cons": 30, "prod": 36, "check": "[4 sc, inc] x 6", "note": "full width - check gauge"},
                    {"label": "R7",  "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": ""},
                    {"label": "R8",  "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": ""},
                    {"label": "R9",  "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": "stuff the body FIRMLY"},
                    {"label": "R10", "text": "[7 sc, invdec] x 4", "stated": 32, "cons": 36, "prod": 32, "check": "[7 sc, dec] x 4", "note": "shallow waist"},
                    {"label": "R11", "text": "[7 sc, inc] x 4", "stated": 36, "cons": 32, "prod": 36, "check": "[7 sc, inc] x 4", "note": "head begins"},
                    {"label": "R12", "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": "muzzle over R12 - R14"},
                    {"label": "R13", "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": ""},
                    {"label": "R14", "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": "eyes at R14 - R15"},
                    {"label": "R15", "text": "sc in each st around", "stated": 36, "cons": 36, "prod": 36, "check": "sc in each st around", "note": "ears at R15"},
                    {"label": "R16", "text": "[4 sc, invdec] x 6", "stated": 30, "cons": 36, "prod": 30, "check": "[4 sc, dec] x 6", "note": ""},
                    {"label": "R17", "text": "[3 sc, invdec] x 6", "stated": 24, "cons": 30, "prod": 24, "check": "[3 sc, dec] x 6", "note": "stuff the head firmly"},
                    {"label": "R18", "text": "[2 sc, invdec] x 6", "stated": 18, "cons": 24, "prod": 18, "check": "[2 sc, dec] x 6", "note": ""},
                    {"label": "R19", "text": "[sc, invdec] x 6", "stated": 12, "cons": 18, "prod": 12, "check": "[sc, dec] x 6", "note": "top up stuffing"},
                    {"label": "R20", "text": "invdec x 6", "stated": 6, "cons": 12, "prod": 6, "check": "dec x 6", "note": ""},
                ], "notes": [
                    "Finish: cinch the remaining 6 stitches closed and weave the "
                    "tail inside the body. Do not decrease the Rnd 10 waist further "
                    "- a narrow neck cannot hold the head upright on this shape.",
                    "How the leg joins work: work Rnd 4 and Rnd 5 following the "
                    "full written rounds below. Wherever a round says \u201cjoin\u201d, "
                    "hold a pinched-flat leg against the body and work the next 3 sc "
                    "through BOTH the leg and the body together (technique 3). "
                    "Those 3 sc still count as 3 stitches of the round, so the "
                    "stitch totals do not change - Rnd 4 ends at 24, Rnd 5 at 30. "
                    "The joined stitches are always plain single crochet - never "
                    "work an increase through a leg.",
                    "Rnd 4 - the BACK legs (24 stitches): work the first 3 sc "
                    "through a leg and the body together, then [sc, inc] x 3; "
                    "work the next 3 sc through the second leg and the body "
                    "together, then [sc, inc] x 3 to the end of the round.",
                    "Rnd 5 - the FRONT legs (30 stitches): work 1 sc, inc, 1 sc, "
                    "inc, 1 sc (7 stitches made); join a leg over the next 3 sc; "
                    "work [sc, inc] x 3 and 1 sc (10 stitches made); join the "
                    "second leg over the next 3 sc; work 3 sc, inc, 2 sc to the end "
                    "(7 stitches made). In the finished round that is 7 - 3 - 10 - "
                    "3 - 7 = 30, and all six increases fall inside the plain runs, "
                    "exactly as the [3 sc, inc] x 6 rhythm of the table. The 7-10-7 "
                    "spacing centres each front leg between the two back legs.",
                    "Work the numbers exactly. If the front legs line up directly "
                    "behind the back legs instead of between them, the footprint "
                    "narrows and Coco tips. The correct spacing covers the deepest "
                    "footprint this shape allows - about 65 mm across and 29 mm "
                    "front to back. Hold the piece upside down and check all four "
                    "legs sit square before you stuff the body.",
                    "The legs join low (Rnd 4-5) so every foot hangs about 17 mm "
                    "below the body and Coco stands on her feet.",
                ]},
            ],
        },
    ],
    "assembly": [
        "Muzzle: stuff lightly and pin it to the front of the head over Rnd 12-14, "
        "centred, then sew all the way around with matching brown. It should sit "
        "proud of the head, not flush. Centring matters - the eyes go 6 stitches "
        "apart and a muzzle pinned even slightly off-centre crowds one eye.",
        "Eyes: embroider - do not use safety eyes. With dark brown, work a "
        "shallow downward arc about 3 stitches wide on each side, at Rnd 14-15, "
        "6 stitches apart, with a tiny tick angled down at each outer end. This "
        "closed-eye curve is what makes Coco look asleep.",
        "Nose & mouth: embroider AFTER the muzzle is sewn on, so the stitches sit "
        "on the finished curve. On the muzzle, work a small dark triangle at top "
        "centre, a short vertical line down from it, and a soft curved mouth to "
        "one side.",
        "Ears: pinch the base of each ear so it cups forward, then sew at Rnd 15, "
        "about 5 stitches apart, angled slightly outward. Rnd 15 is a full 36-st "
        "round, so this puts the ears on top of the head where a capybara's "
        "belong.",
        "Legs: the legs were joined during Rnd 4-5 - there is nothing to sew. "
        "Just check each pinched 3-stitch strip is caught fully in the round.",
        "Final shaping: roll the finished piece gently between your palms to "
        "settle the stuffing into a round, bottom-heavy shape.",
        "Before you sew - lay every component out and check: 4 legs (2 back of 8 "
        "rounds, 2 front of 9), 2 ears, 1 muzzle, 1 body & head, closed at the "
        "crown. The sleeping face is all embroidery - closed-eye arcs, a small "
        "triangle nose and a soft curved mouth.",
    ],
    "troubleshooting": [
        ("Coco looks too tall.",
         "Almost always too many plain rounds. Rnd 12-15 is the straight head "
         "section the face is positioned on; adding 'just one more' round turns "
         "the shape into a tower and moves the face."),
        ("Coco will not stand.",
         "Check the join height, not the leg spacing. The legs belong on Rnd 4 "
         "and Rnd 5; joined any higher, they cannot clear the underside of the "
         "body and the belly rests on the table."),
        ("Coco tips forward or backward.",
         "Most often the front legs are lined up behind the back legs instead of "
         "between them - the Rnd 5 spacing must be 7 sc, 10 sc, 7 sc. If still "
         "tipping, stuff the lower body more firmly and settle weight back over "
         "all four feet."),
        ("Rocks back, front feet in the air.",
         "All four legs are the same length and they cannot be. Front legs join "
         "at Rnd 5 (21 mm up), back at Rnd 4 (17 mm up); work the front legs 9 "
         "rounds and the back legs 8."),
        ("The head flops back.",
         "The Rnd 10 waist is deliberately shallow at 32 stitches - do not "
         "decrease it further. A narrow neck cannot hold the head upright."),
        ("Small hole where a leg meets the body.",
         "You joined a flat, wide leg top instead of a pinched one. Flatten the "
         "whole 9-stitch top into a strip about 3 stitches wide before joining, "
         "so the un-joined stitches bunch up inside."),
        ("Muzzle looks flat / stuffing shows.",
         "Stuff the muzzle just enough to hold a dome. If stuffing shows through "
         "the body, your gauge is too loose - 36 sts should measure 52 mm; "
         "crochet tighter or go down a hook size."),
    ],
    "colorways": ["Classic warm brown", "Soft grey", "Sandy beige", "Cocoa"],
    "extras": [],
    "designer_notes": [
        "Why the legs join so low: back legs (8 rnd, ~34 mm) join at Rnd 4, only "
        "17 mm above the base; front legs (9 rnd, ~39 mm) join at Rnd 5, 21 mm "
        "up. Different lengths, same result: every foot hangs about 17 mm below "
        "the body so all four land level. This is the most common failure on "
        "round-bodied animals.",
        "Bottom-heavy by design: stuff the lower body firmly and keep the shape "
        "squat. Coco is meant to be one continuous curve from base to crown - "
        "she stands on her feet, not her belly.",
    ],
    "terms": {
        "ownership": ("This crochet pattern - including all instructions, stitch "
                      "counts, photography and design elements - is the original "
                      "work and intellectual property of Novality Store, designed "
                      "by Novality Crochet Studio. Design Code NS 04."),
        "may": ("Make as many finished Coco plushies as you like for yourself, "
                "gifts, or charity. Sell physical finished items made from this "
                "pattern in small batches, in shops, markets and online, provided "
                "credit is given to \u201cNovality Store\u201d (a link or tag is "
                "always appreciated)."),
        "maynot": ("Do not resell, share, redistribute, translate, rewrite, publish "
                   "or upload this digital PDF or its contents in any form. Do not "
                   "alter, copy or recolor the pattern and claim it as your own. Do "
                   "not use the Novality Store name, logo or photos in your own "
                   "listings beyond crediting the pattern. Do not mass-produce "
                   "finished items commercially without written permission."),
        "safety": ("This pattern has not been tested to a toy-safety standard "
                   "(ASTM F963 / EN 71). Although Coco has no plastic parts, "
                   "finished items made for sale must be assessed by the seller "
                   "against local toy-safety laws. Reinforce all sewn-on parts "
                   "before giving to a young child."),
    },
    "hashtag": "#CocoTheCapybara",
    "closing": ("We love seeing your Cocos. Thank you for supporting an "
                "independent pattern designer."),
}
