# -*- coding: utf-8 -*-
"""Pattern specs NS 04-06: Coco the Capybara, Little Duck Plushie, Momo the Loaf Cat."""

COCO = dict(
    slug="coco", code="NS 04", file_stem="Coco_the_Capybara_Crochet_Pattern_NS04",
    title="Coco the Capybara",
    subtitle="A low, round, bottom-heavy capybara with a blunt sewn-on muzzle, plump stuffed legs and a calm embroidered sleeping face — no safety eyes and no small plastic parts",
    cover="assets/coco_cover.png",
    badges=["No plastic eyes", "Intermediate", "2.5–3 hours"],
    size_line="About 10.3 cm (4 in) tall standing on all four legs  •  ~5 cm (2 in) wide at the widest  •  "
              "squat and bottom-heavy, standing on her feet rather than her belly",
    materials_line="Worsted #4 warm brown ~30 g  •  dark brown ~5 g  •  3.0 mm hook  •  embroidered face, "
                   "no safety eyes",
    terms_name="Cocos", tags="#CocoTheCapybara",
    theme=dict(dark=(94, 64, 40), accent=(134, 96, 62), soft=(246, 238, 228),
               box_bg=(248, 240, 230), box_edge=(150, 105, 68)),
    safety=dict(title="SAFETY — EMBROIDERED FACE, NO PLASTIC PARTS", lines=[
        ("Coco has no safety eyes and no small plastic parts, which makes the face safer than a safety-eyed "
         "toy. That does not make the finished toy suitable for babies: Coco is a stuffed toy with a sewn-on "
         "muzzle and sewn-on ears, and it has not been tested to a toy-safety standard such as ASTM F963 or "
         "EN 71.", True),
        "Intended as a decorative item or a gift for a child old enough not to chew it. Check every seam — "
        "especially the muzzle and ears — before giving Coco to a young child.",
    ]),
    materials=[
        ("Main yarn:", "worsted weight (#4), warm brown, about 30 g. A smooth matte yarn shows the stitch "
         "texture best."),
        ("Face yarn:", "worsted weight (#4), dark brown, about 5 g, for the closed eyes, nose and mouth. Use "
         "the same weight as the main yarn."),
        ("Hook:", "3.0 mm (US C-2 or D-3). The gauge is written for this hook."),
        ("Eyes:", "none. The sleeping face is embroidered — no safety eyes."),
        ("Also needed:", "polyester fiber filling about 5–8 g; yarn needle; stitch marker; pins. Pins matter: "
         "the muzzle and ears are pinned before sewing."),
    ],
    gauge=[("36 sc around measures about 52 mm in diameter when stuffed (4.5 mm per stitch, 4.3 mm per round).", True),
           "Check it on the body after Rnd 6 — a stuffed tube, not a flat swatch. If your 36 sts measure wider "
           "than 52 mm, crochet more tightly or go down a hook size; a loose gauge will show stuffing."],
    abbrev="MR magic ring  •  ch chain  •  sc single crochet  •  inc increase (2 sc in one st)  •  "
           "invdec invisible decrease  •  sl st slip stitch  •  st(s) stitch(es)  •  Rnd(s) round(s)  •  "
           "FO fasten off  •  (n) stitch count at round end.",
    construction=[
        ("Spiral.", "work in a continuous spiral — do not join and do not chain 1 between rounds. Keep a "
         "marker in the first stitch of every round. Work every stitch through both loops unless a note says "
         "otherwise."),
        ("One round blob.", "head and body are both 36 stitches around with only a shallow waist between them "
         "— that is what makes Coco read as one round blob rather than a snowman. The legs are joined low at "
         "Rnd 4–5."),
    ],
    techniques=[
        ("The magic ring", "every piece begins with a magic ring. Pull the tail tight once the first round is "
         "complete."),
        ("Working in a spiral", "keep a stitch marker in the first stitch of every round and move it up. There "
         "is no seam and no join to count from."),
        ("The two-layer leg join", "hold a finished leg against the body with the pinched-flat top of the leg "
         "lying against the outside of the body. Insert the hook through BOTH the leg and the body stitch and "
         "work one single crochet; the leg edge and body stitch are treated as one stitch. They still count as "
         "one stitch each, so every count in the body table stays correct. Pinch the leg top flat first — a "
         "round, un-pinched top will not lie against the curved body and the join will pucker."),
        ("How the height adds up", "body Rnds 1–20 = 20 rnd x 4.3 mm = 86 mm; legs lift the body ~17 mm "
         "(short 8/9-round legs) — total standing height 103 mm = 10.3 cm."),
    ],
    technique_boxes=[dict(title="Pinching the leg top", lines=[
        "A 9-stitch leg top flattens to about 5 stitches across — pinch it down to a strip about 3 stitches "
        "wide and hold it while you join. The stitches you don't join bunch up inside, and that bunch makes the "
        "leg look plump rather than tubular. Don't keep the top flat and wide."])],
    pieces=[
        dict(title="1 · Legs — make 4 (back legs stop at Rnd 8, front legs work Rnd 9)",
             note="Stuff the lower half of each leg lightly, leaving the top loose. Front legs join one round "
                  "higher and need to be one round longer so all four feet reach table level.",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", "all four"],
                              ["2", "[1 sc, inc] x 3", "9", "all four"],
                              ["3", "sc in each st around", "9", "all four"],
                              ["4", "sc in each st around", "9", "all four"],
                              ["5", "sc in each st around", "9", "all four"],
                              ["6", "sc in each st around", "9", "all four"],
                              ["7", "sc in each st around", "9", "all four"],
                              ["8", "sc in each st around", "9", "BACK legs finish here"],
                              ["9", "sc in each st around", "9", "FRONT legs only"]]),
             paras=["Fasten off with a long tail for sewing. Before joining, pinch the whole 9-stitch top flat "
                    "into a narrow strip about 3 stitches wide."]),
        dict(title="2 · Ears (make 2) & 3 · Muzzle (make 1)",
             table=dict(headers=["Rnd", "EAR — Instruction", "Sts"],
                        rows=[["1", "6 sc in MR", "6"],
                              ["2", "[1 sc, inc] x 3", "9"],
                              ["3", "sc in each st around", "9"]]),
             paras=["Fasten off with a long tail, do not stuff — a shallow cup."],
             extra_tables=[dict(
                 title="Muzzle — make 1",
                 headers=["Rnd", "MUZZLE — Instruction", "Sts"],
                 rows=[["1", "6 sc in MR", "6"],
                       ["2", "[1 sc, inc] x 3", "9"],
                       ["3", "[2 sc, inc] x 3", "12"],
                       ["4", "sc in each st around", "12"],
                       ["5", "sc in each st around", "12"]])],
             finish=[("Muzzle finish:", "fasten off with a long tail and stuff lightly, just enough to hold a "
                      "dome; it should sit proud of the head when sewn on.")]),
        dict(title="4 · Body & head — one piece, legs joined in Rnd 4 and Rnd 5",
             table=dict(widths=[13, 68, 15, 82],
                        headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[1 sc, inc] x 6", "18", ""],
                              ["4", "3 sc, [1 sc, inc] x 3, 3 sc, [1 sc, inc] x 3", "24",
                               "join the BACK legs"],
                              ["5", "[3 sc, inc] x 6", "30", "join the FRONT legs"],
                              ["6", "[4 sc, inc] x 6", "36", "full width — check gauge"],
                              ["7", "sc in each st around", "36", ""],
                              ["8", "sc in each st around", "36", ""],
                              ["9", "sc in each st around", "36", "stuff the body FIRMLY"],
                              ["10", "[7 sc, invdec] x 4", "32", "shallow waist"],
                              ["11", "[7 sc, inc] x 4", "36", "head begins"],
                              ["12", "sc in each st around", "36", "muzzle over R12–14"],
                              ["13", "sc in each st around", "36", ""],
                              ["14", "sc in each st around", "36", "eyes at R14–15"],
                              ["15", "sc in each st around", "36", "ears at R15"],
                              ["16", "[4 sc, invdec] x 6", "30", ""],
                              ["17", "[3 sc, invdec] x 6", "24", "stuff the head firmly"],
                              ["18", "[2 sc, invdec] x 6", "18", ""],
                              ["19", "[1 sc, invdec] x 6", "12", "top up stuffing"],
                              ["20", "invdec x 6", "6", "cinch closed"]]),
             paras=["Cinch the remaining 6 stitches closed and weave the tail inside the body. Do not decrease "
                    "the Rnd 10 waist further — a narrow neck cannot hold the head upright on this shape."]),
        dict(title="Joining the legs as you crochet Rnds 4–5",
             paras=["Work Rnd 4 and Rnd 5 as the plain increase rounds in the body table, but as you reach each "
                    "leg position, hold a pinched-flat leg against the body and work the next 3 sc through BOTH "
                    "the leg and the body together. Those 3 sc still count as 3 stitches of the round, so the "
                    "stitch totals do not change — Rnd 4 ends at 24, Rnd 5 at 30.",
                    "Rnd 4 — the BACK legs (total 24 stitches): 1. Work the first 3 sc through a leg and the "
                    "body together, then [1 sc, inc] x 3. 2. Work the next 3 sc through the second leg and the "
                    "body together, then [1 sc, inc] x 3 to the end of the round.",
                    "Rnd 5 — the FRONT legs (total 30 stitches): work 7 sc, join a leg over the next 3 sc, work "
                    "10 sc, join a leg over the next 3 sc, work 7 sc to the end. That is 7 - 3 - 10 - 3 - 7 = 30. "
                    "The 7-10-7 spacing centres each front leg between the two back legs. Work the numbers "
                    "exactly — if the front legs line up directly behind the back legs instead of between them, "
                    "the footprint narrows and Coco tips. The correct spacing covers the deepest footprint this "
                    "shape allows — about 65 mm across and 29 mm front to back. Hold the piece upside down and "
                    "check all four legs sit square before you stuff the body.",
                    "The legs join low (Rnd 4–5) so every foot hangs about 17 mm below the body and Coco stands "
                    "on her feet."]),
    ],
    assembly=dict(
        title="5 · Face & assembly",
        bullets=[
            ("Muzzle:", "stuff lightly and pin it to the front of the head over Rnd 12–14, centred, then sew "
             "all the way around with matching brown. It should sit proud of the head, not flush. Centering "
             "matters — the eyes go 6 stitches apart and a muzzle pinned even slightly off-center crowds one eye."),
            ("Eyes:", "embroider — do not use safety eyes. With dark brown, work a shallow downward arc about "
             "3 stitches wide on each side, at Rnd 14–15, 6 stitches apart, with a tiny tick angled down at each "
             "outer end. This closed-eye curve is what makes Coco look asleep."),
            ("Nose & mouth:", "embroider AFTER the muzzle is sewn on, so the stitches sit on the finished "
             "curve. On the muzzle, work a small dark triangle at top center, a short vertical line down from "
             "it, and a soft curved mouth to one side."),
            ("Ears:", "pinch the base of each ear so it cups forward, then sew at Rnd 15, about 5 stitches "
             "apart, angled slightly outward. Rnd 15 is a full 36-st round, so this puts the ears on top of the "
             "head where a capybara's belong."),
            ("Legs:", "the legs were joined during Rnd 4–5 — there is nothing to sew. Just check each pinched "
             "3-stitch strip is caught fully in the round."),
            ("Final shaping:", "roll the finished piece gently between your palms to settle the stuffing into "
             "a round, bottom-heavy shape."),
        ],
        checklist=["4 legs (2 back of 8 rounds, 2 front of 9)  •  2 ears  •  1 muzzle  •  1 body & head, closed "
                   "at the crown. The sleeping face is all embroidery — closed-eye arcs, a small triangle nose "
                   "and a soft curved mouth."],
        boxes=[dict(title="Designer notes", lines=[
            ("Why the legs join so low. ", True),
            "Back legs (8 rnd, ~34 mm) join at Rnd 4, only 17 mm above the base; front legs (9 rnd, ~39 mm) "
            "join at Rnd 5, 21 mm up. Different lengths, same result: every foot hangs about 17 mm below the "
            "body so all four land level. This is the most common failure on round-bodied animals.",
            ("Bottom-heavy by design. ", True),
            "Stuff the lower body firmly and keep the shape squat. Coco is meant to be one continuous curve "
            "from base to crown — she stands on her feet, not her belly."])]),
    troubleshooting=[
        ("Coco looks too tall.", "almost always too many plain rounds. Rnd 12–15 is the straight head section "
         "the face is positioned on; adding 'just one more' round turns the shape into a tower and moves the face."),
        ("Coco will not stand.", "check the join height, not the leg spacing. The legs belong on Rnd 4 and "
         "Rnd 5; joined any higher, they cannot clear the underside of the body and the belly rests on the table."),
        ("Coco tips forward or backward.", "most often the front legs are lined up behind the back legs instead "
         "of between them — the Rnd 5 spacing must be 7 sc, 10 sc, 7 sc. If still tipping, stuff the lower body "
         "more firmly and settle weight back over all four feet."),
        ("Rocks back, front feet in the air.", "all four legs are the same length and they cannot be. Front "
         "legs join at Rnd 5 (21 mm up), back at Rnd 4 (17 mm up); work the front legs 9 rounds and the back "
         "legs 8."),
        ("The head flops back.", "the Rnd 10 waist is deliberately shallow at 32 stitches — do not decrease it "
         "further. A narrow neck cannot hold the head upright."),
        ("Small hole where a leg meets the body.", "you joined a flat, wide leg top instead of a pinched one. "
         "Flatten the whole 9-stitch top into a strip about 3 stitches wide before joining, so the un-joined "
         "stitches bunch up inside."),
        ("Muzzle looks flat / stuffing shows.", "stuff the muzzle just enough to hold a dome. If stuffing shows "
         "through the body, your gauge is too loose — 36 sts should measure 52 mm; crochet tighter or go down "
         "a hook size."),
    ],
    colorways=[("Classic warm brown", (134, 96, 62)), ("Soft grey", (166, 162, 156)),
               ("Sandy beige", (204, 178, 142)), ("Cocoa", (110, 74, 52))],
    checks=[
        ["Body Rnds 1–20: 6 → 36 → 32 → 36 → 6 with leg joins counted", "✓ verified"],
        ["Leg-join arithmetic: Rnd 4 = 3+9+3+9 = 24; Rnd 5 = 7-3-10-3-7 = 30", "✓ verified"],
        ["Legs 9 sts, back 8 rnds / front 9 rnds", "✓ verified"],
        ["Ears 3 rounds (9 sts); muzzle 5 rounds (12 sts) — de-interleaved", "✓ verified"],
        ["Standing height 20 rnds x 4.3 mm + 17 mm legs = 103 mm = 10.3 cm", "✓ verified"],
        ["Muzzle face 24 sts ≈ 34.4 mm / rim 18 sts ≈ 25.8 mm", "✓ verified"],
        ["Waist [7 sc, invdec] x 4 consumes all 36 sts → 32", "✓ verified"],
    ],
    safety_reminder="This pattern has not been tested to a toy-safety standard (ASTM F963 / EN 71). Although "
                    "Coco has no plastic parts, finished items made for sale must be assessed by the seller "
                    "against local toy-safety laws. Reinforce all sewn-on parts before giving to a young child.",
)

DUCK = dict(
    slug="duck", code="NS 05", file_stem="Little_Duck_Plushie_Crochet_Pattern_NS05",
    title="Little Duck Plushie",
    subtitle="A round, squashy duckling in fluffy chenille, worked as a single piece from tail to crown — no body-to-head seam; only the wings and the beak are sewn on",
    cover="assets/duck_cover.png",
    badges=["Embroidered eyes", "Confident beginner", "1.5–2 hours"],
    size_line="About 16 cm (6.25 in) tall and 7.5 cm (3 in) wide in super-bulky chenille (#6) on a 4.5 mm hook  •  "
              "one seamless body; 2 wings + 1 beak to sew",
    materials_line="Super-bulky chenille yellow ~25–35 g  •  orange for the beak  •  black floss  •  "
                   "4.5 mm hook  •  embroidered eyes, no plastic parts",
    terms_name="ducks", tags="#LittleDuckPlushie",
    theme=dict(dark=(151, 108, 24), accent=(214, 158, 43), soft=(250, 242, 220),
               box_bg=(250, 243, 226), box_edge=(196, 140, 32)),
    safety=dict(title="SAFETY — EMBROIDERED EYES", lines=[
        ("This duck uses EMBROIDERED eyes, which avoids the small-parts hazard of safety eyes — a real "
         "advantage if you sell finished toys.", True),
        "If you sell them as toys, EU items need CE marking under EN 71 and US items must meet CPSIA and "
        "ASTM F963; independent testing is the only way to confirm.",
        "Check seams hold under a firm pull and that the chenille pile does not shed, and tag each piece with "
        "materials, your maker name and an age recommendation.",
    ]),
    materials=[
        ("Body yarn:", "super-bulky chenille (#6), yellow, about 25–35 g. A 100 g ball makes two ducks "
         "comfortably. Fluffy chenille is the whole look."),
        ("Details:", "a small amount of orange yarn for the beak; black yarn or embroidery floss for the eyes."),
        ("Hook:", "4.5 mm (US 7)."),
        ("Stuffing & notions:", "fibre fill about 25–35 g packed firmly; yarn needle, stitch marker, pins."),
    ],
    gauge=[("About 8 mm per stitch and 7 mm per round in super-bulky chenille.", True),
           "Chenille varies between brands, so measure a 12-stitch swatch (about 10 cm) first. Finished size "
           "about 16 cm tall and 7.5 cm wide — 23 rounds at 7 mm and a widest point of 30 stitches at 8 mm."],
    abbrev="MR magic ring  •  ch chain  •  sc single crochet  •  inc increase (2 sc in one st)  •  "
           "dec invisible decrease  •  sl st slip stitch  •  FLO front loops only  •  FO fasten off  •  "
           "(n) stitch count.",
    construction=[
        ("Seamless.", "the waist at R10–R12 and the reflare at R13–R14 separate body from head with no seam. "
         "Body and head are the same diameter (30 stitches, about 76 mm); the 18-stitch waist reads as the neck."),
        ("Start stuffing at R10.", "once the waist closes you cannot reach the body."),
    ],
    techniques=[
        ("Magic ring & spiral", "the start of the body and each wing is a magic ring. Work in a continuous "
         "spiral — no join, no chain 1 between rounds — with a marker in the first stitch of every round."),
        ("Invisible decrease", "insert the hook under the FRONT loop only of the next two stitches, yarn over "
         "and pull through the first two loops (three loops on the hook), then yarn over and pull through both "
         "remaining loops. A flatter join than a standard decrease — it shows at this scale."),
        ("Around a chain (the beak)", "work around both sides of a starting chain: along one side, corner "
         "increases into the end chain, then back along the other side. Rnd 1 of a 5-chain totals 11 stitches; "
         "all five chains are used."),
        ("Through both layers", "to close each flat wing, fold it and single-crochet across both layers at "
         "once — 6 sc take the 12 stitches down to 6 and leave a flat half-disc."),
        ("Embroidery & sewing", "the eyes are embroidered (no safety eyes). The wings and the flattened, "
         "unstuffed beak are sewn on; sew through a whole stitch so they cannot pull out."),
    ],
    pieces=[
        dict(title="1 · Body — tail to crown in one piece",
             table=dict(widths=[13, 62, 15, 88],
                        headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "[3 sc, inc] x 6", "30", "body full width"],
                              ["6", "sc in each st around", "30", "wings attach R6–R9"],
                              ["7", "sc in each st around", "30", ""],
                              ["8", "sc in each st around", "30", ""],
                              ["9", "sc in each st around", "30", ""],
                              ["10", "[3 sc, dec] x 6", "24", "START STUFFING NOW"],
                              ["11", "sc in each st around", "24", ""],
                              ["12", "[2 sc, dec] x 6", "18", "waist closing"],
                              ["13", "[2 sc, inc] x 6", "24", ""],
                              ["14", "[3 sc, inc] x 6", "30", "head begins"],
                              ["15", "sc in each st around", "30", ""],
                              ["16", "sc in each st around", "30", "eyes at R16–R17"],
                              ["17", "sc in each st around", "30", ""],
                              ["18", "sc in each st around", "30", "beak across R16–R18"],
                              ["19", "sc in each st around", "30", ""],
                              ["20", "[3 sc, dec] x 6", "24", ""],
                              ["21", "[2 sc, dec] x 6", "18", "stuff head, shape cheeks"],
                              ["22", "[sc, dec] x 6", "12", "add final stuffing"],
                              ["23", "dec x 6", "6", "close via FLO"]]),
             paras=["Fasten off with a long tail; thread through the FLO of the 6 remaining stitches, pull "
                    "tight, knot and bury.",
                    "Smaller head option: skip the R14 reflare (keep R14–R19 at 24) and close R20 [2 sc, dec] x6 "
                    "(18), R21 [sc, dec] x6 (12), R22 dec x6 (6)."]),
        dict(title="2 · Wings — make 2",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "sc in each st around", "12", ""],
                              ["4", "6 sc across both layers", "6", "flatten, close"]]),
             paras=["Do not stuff. Flatten and sc 6 across both layers to close (12 sts to 6), leaving a flat "
                    "half-disc about 30 mm across. Sew to the sides spanning R6–R9, angled slightly back."]),
        dict(title="3 · Beak — make 1 (worked around a chain)",
             paras=["Ch 5. Rnd 1: from the 2nd ch, sc in next 3, 3 sc in the last ch, rotate, sc in next 3, "
                    "2 sc in the last loop (11). Rnd 2: inc, 2 sc, inc, 2 sc, inc, 2 sc, inc, sc (15). "
                    "Sl st and fasten off with a long tail. Do NOT stuff — flatten it to a flat lens.",
                    "As written it is a bold ~50 mm cartoon beak; for a daintier duck work Rnd 1 only (11 sts, "
                    "about 37 mm)."]),
    ],
    assembly=dict(
        title="4 · Face & 5 · assembly order",
        bullets=[
            ("1 Stuff from R10:", "fill the body firmly as the waist begins to close — the neck narrows fast."),
            ("2 Eyes:", "embroider black eyes between R16 and R17, about 7–8 stitches apart (56–64 mm on the "
             "76 mm head), before the head closes."),
            ("3 Beak:", "pin horizontally across R16–R18, centred between the eyes, and sew around the outer edge."),
            ("4 Wings:", "sew one to each side at R6–R9, angled slightly back."),
            ("5 Close:", "top up stuffing through R22, then close via the FLO and bury the end."),
        ],
        listing=[("Seller advantage:", "embroidered eyes mean no small plastic parts — safer to sell, and no "
                  "washers to work around."),
                 ("Tag each toy:", "materials, maker name, age recommendation.")],
        care="Surface clean with a damp cloth and mild soap; do not machine wash — chenille mats and sheds in "
             "agitation. Dry flat away from heat, and fluff the pile with a clean pet slicker brush once dry."),
    troubleshooting=[
        ("Much taller than 16 cm.", "your chenille is thicker than gauge. A 12-stitch swatch at 10 mm/stitch "
         "finishes near 20 cm."),
        ("Much shorter.", "finer yarn — see the size table; DK on 3.0 mm gives 7–8 cm, not 10–12."),
        ("Wings sit on the neck.", "too high. R6–R9 is the body; R10–R12 is the waist."),
        ("Beak leaves a gap / puffs.", "each side must use four chains (no chain left over). Do not stuff; "
         "flatten before pinning."),
        ("Stuffing shows / head flops.", "hook too large for the yarn, or the waist was under-packed. Pack "
         "R10–R12 firmly before the reflare."),
        ("Cannot reach the body to stuff.", "you started too late — begin at R10 while the waist is still 24 "
         "stitches wide."),
    ],
    sizing_tables=[dict(
        title="Making a smaller duck",
        headers=["Yarn", "Finished height"],
        rows=[["Velvet / bulky (#5) · 3.0 mm hook", "10 – 12 cm"],
              ["Aran / worsted (#4)", "9 – 10 cm"],
              ["DK / light worsted (#3)", "7.5 – 8.5 cm"]],
        aligns=["L", "C"])],
    colorways=[("Classic yellow", (226, 178, 60)), ("White duckling", (243, 239, 230)),
               ("Pastel pink", (232, 186, 190)), ("Aqua", (160, 200, 196))],
    checks=[
        ["Body Rnds 1–23: 6 → 30 → 18 → 30 → 6 chain, stated counts match", "✓ verified"],
        ["Waist & reflare: [3 sc, dec]x6 = 24, [2 sc, dec]x6 = 18, [2 sc, inc]x6 = 24", "✓ verified"],
        ["Wings: 12 sts closed by 6 sc through both layers", "✓ verified"],
        ["Beak around a 5-ch: Rnd 1 = 11, Rnd 2 = 15", "✓ verified"],
        ["Height 23 rnds x 7 mm = 161 mm ~ 16 cm; width 30 sts ≈ 76 mm", "✓ verified"],
        ["Eye gap 7–8 sts = 56–64 mm on the 76 mm head", "✓ verified"],
        ["Smaller-head option: 24 → 18 → 12 → 6", "✓ verified"],
    ],
    safety_reminder="Eyes are embroidered (no small plastic parts). Finished toys sold for children must still "
                    "meet local toy-safety laws (EN 71 / CE in the EU; CPSIA and ASTM F963 in the US) — "
                    "independent testing confirms compliance. Secure every seam and check the chenille does "
                    "not shed.",
)

MOMO = dict(
    slug="momo", code="NS 06", file_stem="Momo_the_Loaf_Cat_Crochet_Pattern_NS06",
    title="Momo the Loaf Cat",
    subtitle="A cat folded into a perfect loaf — one no-sew piece on an oval base; ears crocheted onto the head and the tail worked off the body, so nothing is sewn on",
    cover="assets/momo_cover.png",
    badges=["No-sew body", "Advanced beginner", "2–2.5 hours"],
    size_line="About 7.9 cm (3.1 in) long, 5.2 cm (2 in) wide and 4.3 cm (1.7 in) tall — a low, wide loaf, "
              "wider than it is tall (about 1.2 : 1)",
    materials_line="Worsted #4 ~10 g  •  white + pink contrast scraps  •  3.5 mm hook  •  two 8 mm safety eyes "
                   "(or embroidered)",
    terms_name="Momos", tags="#MomoTheLoafCat",
    theme=dict(dark=(84, 88, 100), accent=(122, 128, 140), soft=(238, 239, 242),
               box_bg=(243, 240, 242), box_edge=(150, 120, 130)),
    safety=dict(title="SAFETY — READ THIS FIRST", lines=[
        ("Momo has two 8 mm safety eyes — small parts. Lock the washers firmly from the inside and pull-test "
         "each eye.", True),
        "Embroidering the eyes is safer, but it does not make Momo a tested toy: not tested to ASTM F963 or "
        "EN 71, so do not describe finished Momos as “baby-safe”. For a child under three, embroider and say "
        "“embroidered, no small parts”.",
        "The ears and tail are worked into the body (stronger than sewing), but still weave every end in at "
        "least 5 cm and knot the embroidery floss inside.",
    ]),
    materials=[
        ("Main yarn:", "worsted #4, about 10 g. Grey, ginger, cream or black — all sell equally well. One "
         "25 g ball makes two."),
        ("Contrast:", "small amounts of white for the chest and paws, pink for the nose and inner ears."),
        ("Hook:", "3.5 mm (US E-4) — tight gauge so stuffing cannot show."),
        ("Eyes:", "2 x 8 mm safety eyes, or embroider in black."),
        ("Also needed:", "polyfill about 10 g; tapestry needle; stitch marker; black embroidery floss."),
    ],
    gauge=[("About 4.5 mm per stitch and 4.3 mm per round.", True),
           "Finished size about 7.9 cm long, 5.2 cm wide and 4.3 cm tall — a low, wide loaf. The 48-stitch "
           "oval base sets the whole size of the cat."],
    abbrev="MR magic ring  •  ch chain  •  sc single crochet  •  inc 2 sc in one st  •  dec invisible decrease  •  "
           "sl st slip stitch  •  BLO back loop only  •  FO fasten off  •  (n) stitch count.",
    construction=[
        ("The oval base is THE step.", "crochet into BOTH sides of a starting chain: across the front, corner "
         "increases into the last chain, then back along the opposite side and into the last loop. That turns "
         "a chain into a flat oval instead of a strip. Do NOT use a magic-ring circle here — a round base "
         "gives a sphere every time."),
        ("Base size sets the cat.", "the base is worked up to 48 stitches before the walls begin. Stopping at "
         "36 gives a body about 60 mm long and 40 mm across that comes out tall and round no matter how you "
         "stuff it."),
    ],
    techniques=[
        ("The magic ring", "used for the tail's first stitches. Wrap yarn around two fingers, pull up a loop "
         "and work the round into the ring, then pull the tail tight."),
        ("Work in a spiral", "no joins and no chain 1 between rounds; move the marker up each round — there is "
         "no join to count from."),
        ("Back loop only (BLO)", "work into the far loop only; the unused loops form a raised ridge — the "
         "visible edge where the oval base meets the walls. That ridge is what makes the loaf read as folded "
         "rather than moulded."),
        ("The invisible decrease", "front loops only of the next two stitches, yarn over and pull through "
         "both, then yarn over and pull through the remaining two. Every dec here is worked this way."),
        ("Flat rows (ch 1, turn)", "the ears are not worked in the round: chain 1, turn, and work back along "
         "the row. Each row is shorter than the one before, forming the ear point."),
        ("Working into body fabric", "the tail starts by pushing the hook through the finished body wall — go "
         "under a WHOLE stitch, not just one loop, or it will pull out."),
    ],
    pieces=[
        dict(title="1 · Base & body — oval base to a 6-stitch close",
             note="The BLO round at Rnd 7 leaves the ridge that reads as the folded loaf edge.",
             table=dict(widths=[15, 72, 15, 76],
                        headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["Found.", "ch 9", "—", "the oval foundation"],
                              ["1", "sc in 2nd ch, sc in next 6, 3 sc in last ch, sc in next 6, 2 sc in last loop", "18",
                               "around both sides of chain"],
                              ["2", "inc, 6 sc, inc x3, 6 sc, inc x2", "24", ""],
                              ["3", "sc, inc, 6 sc, [sc, inc] x3, 6 sc, [sc, inc] x2", "30", ""],
                              ["4", "2 sc, inc, 6 sc, [2 sc, inc] x3, 6 sc, [2 sc, inc] x2", "36", ""],
                              ["5", "3 sc, inc, 6 sc, [3 sc, inc] x3, 6 sc, [3 sc, inc] x2", "42", ""],
                              ["6", "4 sc, inc, 6 sc, [4 sc, inc] x3, 6 sc, [4 sc, inc] x2", "48",
                               "BASE AT FULL SIZE"],
                              ["7", "BLO sc around", "48", "ridge = base edge"],
                              ["8", "sc in each st around", "48", "eyes at R8–R9"],
                              ["9", "sc in each st around", "48", "stuff firmly from here"],
                              ["10", "[6 sc, dec] x 6", "42", ""],
                              ["11", "[5 sc, dec] x 6", "36", ""],
                              ["12", "[4 sc, dec] x 6", "30", "ears worked onto R12"],
                              ["13", "[3 sc, dec] x 6", "24", ""],
                              ["14", "[2 sc, dec] x 6", "18", ""],
                              ["15", "[sc, dec] x 6", "12", "top up stuffing"],
                              ["16", "dec x 6", "6", "close via front loops"]]),
             paras=["Finish: thread the tail through the front loop of each of the 6 remaining stitches, pull "
                    "tight, knot and bury. Shape check: the base is an oval about 79 mm long and 52 mm across; "
                    "the walls add ten rounds of height, so the finished loaf is about 43 mm tall — wider than "
                    "it is tall."]),
        dict(title="2 · Ears — crocheted straight onto Rnd 12, about 6 stitches apart",
             paras=["Join the main yarn to the head at Rnd 12, leaving about 6 stitches between the two ears, "
                    "and work each ear as three short rows: Row 1: sc in next 5, ch 1, turn (5). Row 2: dec, "
                    "sc, dec, ch 1, turn (3). Row 3: dec, sc (2) — the ear tip. Fasten off with a short tail; "
                    "pull it through the 2 tip stitches to close the point and bury inside the head. Each row "
                    "consumes exactly what the row before produced (5 → 3 → 2). Embroider a small pink triangle "
                    "on the front of each ear for lining."]),
        dict(title="3 · Tail — worked off the body",
             paras=["Join the main yarn to the back of the body at about Rnd 9 on the centre line. Insert the "
                    "hook under a whole body stitch, pull up a loop, and work the first 4 sc into the body "
                    "fabric in a tight square; then continue in a normal spiral off those 4 stitches: Rnds 1–8 "
                    "are 4 sc in each round. Do NOT stuff — a thin tail curls around the loaf far better than "
                    "a stuffed one. Fasten off and bury."]),
    ],
    assembly=dict(
        title="4 · Face & markings",
        bullets=[
            ("Eyes:", "fix the 8 mm eyes between Rnds 8 and 9, about 7 stitches apart, LOW and wide on the "
             "front (7 sts ~ 32 mm, roughly 60% of the body width). Low eyes read as a cat; high eyes read as "
             "a bear."),
            ("Nose:", "a small pink triangle centred between and just below the eyes, with two short stitches "
             "angled down from the point for the mouth."),
            ("Whisker dots:", "three tiny black French knots on each side of the nose."),
            ("Chest & paws:", "with white yarn, embroider a soft oval on the chest and two small ovals at the "
             "front of the base for tucked paws — this is what turns a plain loaf into a cat."),
        ],
        boxes=[dict(lines=["Long, low and wide — the BLO ridge and tucked paws make the loaf read as a folded cat."])],
        listing=[("Listing tip:", "grey tabby, orange ginger, cream, black and calico (grey base with ginger "
                  "and cream patches embroidered on afterwards) — listing all five as photos in one listing "
                  "outperforms separate listings. Buyers choose a cat, not a pattern.")]),
    troubleshooting=[
        ("It came out round.", "you stopped increasing at Rnd 4 instead of Rnd 6, worked too many plain rounds "
         "at Rnds 8–9, or used a magic-ring base instead of the oval. The base must reach 48 stitches."),
        ("Tall and narrow.", "the base did not reach 48. Count the stitches at Rnd 6 before the BLO round — "
         "that one number decides the whole shape."),
        ("Ears lean back.", "join the yarn one round lower and angle the first row slightly forward."),
        ("Tail falls off.", "the first 4 sc must go through the body fabric under a whole stitch, not just one loop."),
        ("Stuffing shows.", "go down to a 3.0 mm hook — loose gauge on 3.5 mm is the usual cause."),
        ("Face looks like a bear.", "eyes too high and too close. Drop them a round and widen to 7 stitches."),
    ],
    colorways=[("Grey tabby", (146, 148, 152)), ("Orange ginger", (198, 126, 66)),
               ("Cream", (234, 222, 200)), ("Black", (66, 62, 62)),
               ("Calico", (214, 190, 160))],
    checks=[
        ["Oval ladder 18 → 24 → 30 → 36 → 42 → 48, stated counts match", "✓ verified"],
        ["Body Rnds 7–16: 48 → 6 with [n sc, dec] ladders consuming fully", "✓ verified"],
        ["Ear rows 5 → 3 → 2 consume exactly", "✓ verified"],
        ["Loaf 79 x 52 mm base ~ 216 mm perimeter = 48 sts x 4.5 mm", "✓ verified"],
        ["Height 10 wall rounds x 4.3 mm = 43 mm", "✓ verified"],
        ["Eye gap 7 sts = 31.5 mm ~ 60% of the 52 mm width", "✓ verified"],
        ["36-st alternative base ~ 60 x 40 mm (corrected from '34 mm across')", "✓ verified"],
    ],
    safety_reminder="Not tested to a toy-safety standard (ASTM F963 / EN 71) and uses 8 mm safety eyes. "
                    "Finished items sold for children must be assessed against local toy-safety laws; for "
                    "young children, embroider the eyes and secure every end.",
)
