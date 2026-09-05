# -*- coding: utf-8 -*-
"""Pattern specs NS 01-03: Hamish, Kawaii Halloween Mini Set, Axel."""

HAMISH = dict(
    slug="hamish", code="NS 01", file_stem="Hamish_the_Highland_Cow_Crochet_Pattern_NS01",
    title="Hamish the Highland Cow",
    subtitle="A shaggy, sturdy Highland cow with a flattened brow, a wide cream muzzle and a weather-beaten fringe",
    cover="assets/hamish_cover.png",
    badges=["US terms", "Intermediate", "6–8 hours"],
    size_line="About 15 cm (6 in) sitting  •  70 mm wide body  •  70 x 67 mm head  •  worsted/aran on a 3.5 mm hook",
    materials_line="Yarn A ginger ~25 g  •  Yarn B oat cream ~12 g  •  Yarn C dark chocolate ~5 g  •  "
                   "optional rust scarf  •  2 x 12 mm safety eyes",
    terms_name="Hamishes", tags="#HamishTheHighlandCow",
    theme=dict(dark=(122, 74, 32), accent=(168, 96, 40), soft=(246, 238, 228),
               box_bg=(249, 240, 232), box_edge=(168, 96, 40)),
    safety=dict(title="SAFETY — READ THIS FIRST", lines=[
        ("Hamish has two 12 mm safety eyes — small parts. Lock the washers firmly from the "
         "inside (this pattern locks them after the muzzle is sewn) and pull-test each eye.", True),
        "The horns, ears, muzzle, legs and tail are sewn on, and the fringe and tail are knotted "
        "yarn: sew every seam twice, weave ends in at least 5 cm, and knot the fringe and tail securely.",
        "Not tested to ASTM F963 or EN 71 — do not describe finished Hamishes as “baby-safe”. "
        "For children under three, embroider the eyes with black floss instead of safety eyes.",
    ]),
    materials=[
        ("Yarn A — ginger:", "worsted/aran (#4), about 25 g used. Caramel, toffee or ginger gold. One "
         "80 g / 150 m ball covers several cows and re-dos."),
        ("Yarn B — oat cream:", "worsted/aran (#4), about 12 g. Muzzle, horns, inner ears, optional belly patch."),
        ("Yarn C — dark chocolate:", "worsted/aran (#4), about 5 g. Hooves and nostrils."),
        ("Yarn D — rust (optional):", "about 6 g for the scarf, or 28 cm of 12 mm tartan ribbon."),
        ("Hook:", "3.5 mm (US E-4) — smaller than the ball band so stuffing cannot show."),
        ("Eyes:", "2 x 12 mm black safety eyes, or embroider for under-threes."),
        ("Also:", "polyester fibre fill about 30 g (buy 50 g to over-stuff the base); stitch marker, "
         "tapestry needle, pins, scissors."),
    ],
    gauge=[("11 sc x 12 rounds = 5 cm / 2 in in Yarn A.", True),
           "Not critical, but loose tension lets stuffing show — drop half a hook size if your fabric is gappy. "
           "Finished size about 15 cm / 6 in sitting."],
    abbrev="MR magic ring  •  ch chain  •  sl st slip stitch  •  sc single crochet  •  hdc half double crochet  •  "
           "inc 2 sc in one st  •  dec invisible decrease  •  BLO back loop only  •  FO fasten off  •  "
           "(n) stitch count at round end.",
    construction=[
        ("Spiral.", "work in a continuous spiral unless a round says join; mark the first stitch of every "
         "round. Leave 30–40 cm tails on every piece you will sew."),
        ("Invisible decrease.", "insert the hook through the FRONT loops only of the next two stitches, "
         "yarn over and pull through both, then yarn over and pull through the remaining two. Every dec is "
         "worked this way — no ridge on visible rounds."),
        ("Back loop only (BLO).", "work into the far loop only; the unused loops form a raised ridge. "
         "Hamish's hoof line is one BLO round."),
        ("Working around a chain.", "for the belly patch, crochet into both sides of a starting chain — "
         "turning a chain into a flat oval."),
        ("Lark's head knot.", "fold a strand in half, push the folded loop under a stitch with the hook, "
         "pull the two loose ends through the loop and cinch. Used for every fringe strand and the tail."),
        ("Ladder stitch.", "the invisible seam: out on one side, pick up one bar on the opposite side, then "
         "one bar back, alternating, pulling snug every few stitches. The head-to-body join needs two full passes."),
    ],
    pieces_summary=(
        ["Piece", "Qty", "Rounds", "Finished size"],
        [["Head", "1", "1–16", "~ 70 x 67 mm, closed ball"],
         ["Muzzle", "1", "1–8", "face ~ 35 mm, rim ~ 26 mm"],
         ["Body", "1", "1–19", "~ 70 mm wide, neck open at 18"],
         ["Belly patch (opt.)", "1", "R1–R4", "flat oval, 36 sts"],
         ["Legs", "4", "1–16", "~ 67 mm, hoof + BLO ridge"],
         ["Ears (inner+outer)", "2+2", "1–3 / 1–7", "cupped forward"],
         ["Horns", "2", "1–7", "short, curved, tip-stuffed"],
         ["Fringe & tail", "—", "—", "lark's head knotted yarn"]],
        ["L", "C", "C", "L"]),
    techniques_title="Seven techniques Hamish uses",
    sizing_tables=[dict(
        title="Three sizes, one pattern",
        headers=["Version", "Yarn / hook", "Eyes", "Height"],
        rows=[["Wee Hamish", "DK / #3  •  2.75 mm", "8–9 mm", "~ 12 cm"],
              ["Classic", "Worsted / #4  •  3.5 mm", "12 mm", "~ 15 cm"],
              ["Cuddle Hamish", "Bulky chenille / #5  •  5.0 mm", "16–18 mm", "~ 21 cm"]],
        aligns=["L", "L", "C", "C"],
        note="Stitch counts stay the same; only yarn, hook and stuffing change. Yarn scales with the "
             "square of the height and stuffing with the cube — buy generously for the big chenille version.")],
    pieces=[
        dict(title="1 · Head — worked crown down, one straight round only",
             note="One straight round (R9) is what keeps the brow flat and wide instead of egg-shaped. "
                  "Close to 6 stitches at the end.",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "[3 sc, inc] x 6", "30", ""],
                              ["6", "[4 sc, inc] x 6", "36", "fringe row 3"],
                              ["7", "[5 sc, inc] x 6", "42", "fringe row 2 / horns"],
                              ["8", "[6 sc, inc] x 6", "48", "fringe row 1 / ears"],
                              ["9", "sc in each st around", "48", "eyes at R9–R10"],
                              ["10", "[6 sc, dec] x 6", "42", ""],
                              ["11", "[5 sc, dec] x 6", "36", ""],
                              ["12", "[4 sc, dec] x 6", "30", "stuff firmly, flatten front to back"],
                              ["13", "[3 sc, dec] x 6", "24", ""],
                              ["14", "[2 sc, dec] x 6", "18", ""],
                              ["15", "[sc, dec] x 6", "12", "last pinch of stuffing"],
                              ["16", "dec x 6", "6", "close the hole"]]),
             finish=[("Eyes & head size.", "place the 12 mm eyes between Rnds 9 and 10, 7 stitches apart and a "
                      "touch low on the face (7 sts ~ 32 mm, just under half the head width). Leave washers off "
                      "until the muzzle is pinned. Finished head ~ 70 mm wide x 67 mm tall.")]),
        dict(title="2 · Muzzle — Yarn B, make 1",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "sc in each st around", "24", "face at full width, 35 mm"],
                              ["6", "sc in each st around", "24", ""],
                              ["7", "sc in each st around", "24", ""],
                              ["8", "[2 sc, dec] x 6", "18", "rim = 26 mm across"]]),
             paras=["Fasten off with a 40 cm tail and stuff lightly. The muzzle FACE is about 35 mm across "
                    "(the wide cream patch you see); the RIM it sews by is about 26 mm, spanning roughly six "
                    "rounds of head. Pin the top edge just under the eyes at Rnd 10 and let the lower edge fall "
                    "at Rnd 15–16 near the chin. Centre it, let the face sit a little wider than the eye spacing, "
                    "and sew with small whip stitches, adding a whisper more stuffing before you close.",
                    "Nostrils (Yarn C): two short vertical satin stitches, 3 stitches apart, on the lower third. "
                    "Mouth: one tiny horizontal stitch or a shallow V below them. LOCK THE SAFETY-EYE WASHERS NOW."],
             boxes=[dict(lines=["The wide cream muzzle, low-set eyes and shaggy fringe give the Highland stare."])]),
        dict(title="3 · Body — worked bottom up, neck left open at 18 stitches",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "[3 sc, inc] x 6", "30", ""],
                              ["6", "[4 sc, inc] x 6", "36", ""],
                              ["7", "[5 sc, inc] x 6", "42", ""],
                              ["8", "[6 sc, inc] x 6", "48", "front legs join R8–R9"],
                              ["9", "sc in each st around", "48", ""],
                              ["10", "sc in each st around", "48", "body at full width, 70 mm"],
                              ["11", "sc in each st around", "48", ""],
                              ["12", "sc in each st around", "48", ""],
                              ["13", "sc in each st around", "48", ""],
                              ["14", "[6 sc, dec] x 6", "42", ""],
                              ["15", "sc in each st around", "42", ""],
                              ["16", "[5 sc, dec] x 6", "36", ""],
                              ["17", "[4 sc, dec] x 6", "30", "stuff firmly, pack the base"],
                              ["18", "[3 sc, dec] x 6", "24", ""],
                              ["19", "[2 sc, dec] x 6", "18", "leave neck OPEN"]]),
             paras=["Fasten off with a 40 cm tail; do not close. Body is ~19 rounds (79 mm); with the head "
                    "seated on the neck ring the finished sitting height is about 15 cm / 6 in."]),
        dict(title="4 · Belly patch — Yarn B, optional (flat oval around a chain)",
             paras=["Ch 9. R1: sc in 2nd ch, sc in next 6, 3 sc in last ch, sc in next 6, 2 sc in last loop (18). "
                    "R2: inc, 6 sc, inc x3, 6 sc, inc x2 (24). R3: sc, inc, 6 sc, [sc, inc] x3, 6 sc, [sc, inc] x2 (30). "
                    "R4: 2 sc, inc, 6 sc, [2 sc, inc] x3, 6 sc, [2 sc, inc] x2 (36). Sl st, FO with a long tail; "
                    "sew centred on the front with the lower edge about 3 rounds up from the base. Skip it for a "
                    "plain ginger front — both are correct."]),
        dict(title="5 · Legs — make 4, identical (the sit comes from where you sew them)",
             note="Sixteen rounds = a 67 mm leg.",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR (Yarn C)", "6", "hoof"],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "sc in each st around", "18", ""],
                              ["5", "sc in each st around", "18", ""],
                              ["6", "BLO sc around", "18", "change to Yarn A — ridge"],
                              ["7", "sc in each st around", "18", ""],
                              ["8", "[sc, dec] x 6", "12", "stuff hoof firmly"],
                              ["9", "sc in each st around", "12", ""],
                              ["10", "sc in each st around", "12", ""],
                              ["11", "sc in each st around", "12", ""],
                              ["12", "sc in each st around", "12", ""],
                              ["13", "sc in each st around", "12", "upper leg light"],
                              ["14", "[2 sc, dec] x 3", "9", ""],
                              ["15", "sc in each st around", "9", ""],
                              ["16", "sc in each st around", "9", "leave top open"]]),
             boxes=[dict(title="Leg length — read before you sew", lines=[
                 "A 67 mm leg joins much lower than it is long, so it splays: front ~55 degrees from vertical, "
                 "back ~68–70 degrees (near horizontal) — that is the low Highland sit. For a tidier upright sit, "
                 "work the FRONT pair only to Rnd 10 (42 mm); leave the back pair at 16 rounds as haunches."])]),
        dict(title="6 · Ears — make 2 of each layer",
             paras=["INNER ear — Yarn B (make 2): R1: 6 sc in MR (6). R2: [sc, inc] x 3 (9). R3: [2 sc, inc] x 3 (12).",
                    "OUTER ear — Yarn A (make 2): R1: 6 sc in MR (6). R2: [sc, inc] x 3 (9). R3: [2 sc, inc] x 3 (12). "
                    "R4: sc around (12). R5: sc around (12). R6: [2 sc, dec] x 3 (9). R7: sc around (9).",
                    "Place the inner ear on the outer (cream facing you) before the outer's Rnd 4 and work Rnd 4 "
                    "through both layers. Flatten, fasten off, and pinch the base with 2–3 stitches so the ear "
                    "cups forward."]),
        dict(title="7 · Horns — Yarn B, make 2",
             paras=["R1: 4 sc in MR (4). R2: [sc, inc] x 2 (6). R3: sc around (6). R4: sc around (6). "
                    "R5: [2 sc, inc] x 2 (8). R6: sc around (8). R7: sc around (8). "
                    "Fasten off with a tail; stuff the tip only. Short and slightly curved — tilt each horn out "
                    "and a little back when you sew."]),
        dict(title="8 · Tail & 9 · the fringe — Yarn A, knotted yarn",
             paras=["Tail: cut 6 strands, each 22 cm / 8.5 in. Fold the bundle in half and attach with a lark's "
                    "head at the centre-back just above the last increase round: pull the folded loop through a "
                    "stitch, then the tails through the loop. Folding gives 12 hanging ends; divide into 3 groups "
                    "of 4, braid 4 cm, knot firmly and trim into a small tassel.",
                    "Fringe: attach AFTER the horns and ears so you can part the hair around them. Cut 43 strands, "
                    "each 14 cm / 5.5 in (swap 6 for Yarn C for depth; cut a 44th as a spare). Attach with lark's "
                    "head knots in a horseshoe from one ear, across the brow, to the other, filling three rows: "
                    "every stitch on Rnd 8 (front row, ~24 knots), then every other stitch on Rnds 7 and 6 — "
                    "about 24 + 10 + 9 = 43 knots. Tousle, then trim so the fringe grazes the eyes and breaks "
                    "into uneven points. Highland hair is weather-beaten, not a salon fringe."]),
        dict(title="10 · Optional tartan scarf — Yarn D",
             paras=["Ch 61. Row 1: hdc in 2nd ch from hook and across (60). Row 2: ch 1, turn, hdc across (60). "
                    "Fasten off; add a 3-strand tassel at each end or weave a second colour as a slip-stitch "
                    "stripe to hint at tartan, then tie loosely under the muzzle. "
                    "Ribbon shortcut: 28 cm of 12 mm rust tartan ribbon, knotted once."]),
    ],
    assembly=dict(
        title="Assembly — work in this order",
        bullets=[
            ("1 Muzzle & face:", "sewn and washers locked (section 2)."),
            ("2 Horns:", "between Rnds 5 and 7, 6 stitches apart, angled out and slightly back."),
            ("3 Ears:", "just outside and below each horn, centred on Rnds 8–9, cupped forward."),
            ("4 Fringe:", "attach and trim (section 9), parting around horns and ears."),
            ("5 Head to body:", "closed head on the open 18-st neck ring (Rnd 19). Ball-on-ring join — pack the "
             "neck firmly, ladder-stitch around TWICE, tilt the muzzle slightly down."),
            ("6 Back legs:", "lower sides across Rnds 3–6, almost on the base, splayed near horizontal."),
            ("7 Front legs:", "across Rnds 8–9, about 8 sts apart, angled forward ~55 degrees."),
            ("8 Belly patch:", "only if you made it."),
            ("9 Tail & scarf:", "attach the tassel tail, tie the scarf, weave in every end and fluff the fringe."),
        ],
        checklist=["1 head (closed at R16)  •  1 muzzle  •  1 body (open neck ring)  •  1 belly patch (optional)  •  "
                   "4 legs (hooves forward)  •  2 outer + 2 inner ears  •  2 horns  •  1 tassel tail  •  1 fringe  •  "
                   "1 scarf."]),
    troubleshooting=[
        ("He will not sit.", "restuff the body base firmly and sew the back legs lower and wider — closer to "
         "horizontal than you think."),
        ("Front hooves float.", "sewn too high — they belong on Rnds 8–9, not under the neck. If they still "
         "float, the legs are too long: work the front pair to Rnd 10."),
        ("Stuffing shows.", "drop half a hook size, or hold a matching thread with the yarn on visible rounds."),
        ("Face looks blank.", "the eyes are too high. Low eyes plus a wide muzzle is the Highland stare."),
        ("Fringe is sparse.", "add a fourth row behind the horns and mix in one darker shade."),
        ("Horns flop.", "under-stuffed at the tip, or sewn only at the edge — stitch a full round into the head fabric."),
        ("Head tips forward.", "the neck ring grips the head only about 8 mm up. Pack the neck before closing "
         "and make the second ladder-stitch pass tight."),
    ],
    colorways=[("Ginger", (188, 108, 43)), ("Caramel", (198, 141, 76)),
               ("Highland black", (72, 66, 62)), ("Cream", (232, 222, 204)),
               ("Roan red", (146, 74, 66))],
    checks=[
        ["Head Rnds 1–16: 6 → 48 → 6, stated counts match", "✓ verified"],
        ["Muzzle 24 → 18: face 34.8 mm / rim 26.1 mm at gauge", "✓ verified"],
        ["Body Rnds 1–19: 6 → 48 → 18 (open neck ring)", "✓ verified"],
        ["Belly patch oval 18 → 24 → 30 → 36", "✓ verified"],
        ["Legs: 18 → 12 → 9 ladder; 16 rnds = 67 mm", "✓ verified"],
        ["Head 48 sts ≈ 69.5 mm wide; 16 rnds ≈ 66.7 mm tall", "✓ verified"],
        ["Body 19 rnds ≈ 79 mm; fringe 24+10+9 = 43 knots", "✓ verified"],
    ],
    safety_reminder="This pattern has not been tested to a toy-safety standard (ASTM F963 / EN 71) and uses "
                    "12 mm safety eyes and knotted yarn fringe. Finished items made for sale must be assessed "
                    "by the seller against local toy-safety laws; for young children, embroider the eyes and "
                    "secure every seam and knot.",
)

KAWAII = dict(
    slug="kawaii", code="NS 02", file_stem="Kawaii_Halloween_Mini_Set_Crochet_Pattern_NS02",
    title="Kawaii Halloween Mini Set",
    subtitle="Three pocket-sized spookies — Boo the ruffled ghost, Pip the sculpted pumpkin and Bramble the picot-winged bat",
    cover="assets/kawaii_cover.png",
    badges=["3 patterns", "Intermediate", "5–5.5 cm each"],
    size_line="Boo the Ghost (open bell, ruffled hem)  •  Pip the Pumpkin (needle-sculpted ribs)  •  "
              "Bramble the Bat (scalloped picot wings)  •  ~5 cm / 2 in each",
    materials_line="DK cotton on a 2.5 mm hook  •  cream ~8 g, orange ~10 g, lavender ~9 g, sage ~4 g, "
                   "pink ~2 g  •  Boo & Bramble: 6 mm safety eyes; Pip embroidered",
    terms_name="minis and garlands", tags="#KawaiiHalloweenSet",
    theme=dict(dark=(94, 52, 47), accent=(206, 106, 42), soft=(249, 236, 226),
               box_bg=(250, 238, 229), box_edge=(206, 106, 42)),
    safety=dict(title="SAFETY — SMALL PARTS", lines=[
        ("Boo and Bramble use 6 mm safety eyes — small parts and a choking hazard. Lock the washers from "
         "the inside and pull-test each eye.", True),
        "These minis are decorative pieces, not toys for young children, and have not been tested to "
        "ASTM F963 or EN 71. To give them to a child, embroider the faces instead and check every seam first.",
        "Pip has an embroidered face and no safety eyes.",
    ]),
    materials=[
        ("Yarn:", "DK / light worsted (#3) cotton: cream ~8 g (Boo), pastel orange ~10 g (Pip), lavender ~9 g "
         "(Bramble), sage green ~4 g (stem/tendril/leaf), pale pink ~2 g (ear linings). One small ball of each is plenty."),
        ("Hook:", "2.5 mm (US C-2) — tight enough that stuffing cannot show."),
        ("Safety eyes:", "2 pairs of 6 mm: one for Boo, one for Bramble. Pip needs none."),
        ("Floss:", "black for Boo's smile and Pip's face, pink for blush, white for Bramble's fangs."),
        ("Stuffing & notions:", "polyester fibre fill (~5 g covers the set; Pip ~2 g, Bramble ~1 g, Boo none). "
         "Tapestry needle, stitch markers, pins, scissors."),
    ],
    gauge=[("About 3.5 mm per stitch and 3.2 mm per round.", True),
           "Check on Pip after Rnd 6 — 36 stitches should measure about 40 mm around a firmly stuffed body. "
           "Finished minis are 48–51 mm tall."],
    abbrev="MR magic ring  •  ch chain  •  sl st slip stitch  •  sc single crochet  •  hdc half double crochet  •  "
           "dc double crochet  •  inc increase (2 sc in one st)  •  dec invisible decrease  •  "
           "FLO / BLO front / back loop only  •  picot ch 3, sl st in 3rd ch from hook  •  (n) stitch count.",
    construction=[
        ("Spiral.", "work the bodies in a continuous spiral — no joins, no chain 1 between rounds; mark the "
         "first stitch of every round."),
        ("Turned rows.", "Bramble's wings are the exception: worked flat in turned rows."),
    ],
    techniques=[
        ("The picot", "chain 3, then slip stitch into the 3rd chain from the hook — one small pointed bump. "
         "Picots edge Bramble's wings and make them read as bat wings rather than leaves. Keep tension even: "
         "a loose picot loops, a tight one curls under."),
        ("One loop only (FLO / BLO)", "Boo's ruffled hem is worked into the FRONT loops of Rnd 12, leaving the "
         "back loops free as a clean ring to sew the optional base onto. The unused loop stays as a ridge — "
         "that ridge is the join line and is meant to be there."),
        ("The ruffle shell", "Boo's hem repeats: 2 sl st, then (sc, hdc, dc, hdc, sc) all into the NEXT single "
         "stitch, then 1 sl st. Each repeat takes 4 stitches and returns 8, so the edge doubles in length. Six "
         "repeats use all 24 stitches of Rnd 12 = 48 stitches, six ruffles."),
        ("Needle sculpting", "turns Pip from an orange ball into a pumpkin using the long tail. Six evenly "
         "spaced passes make six ribs. OVERSTUFF FIRST — sculpting compresses the filling and a soft pumpkin "
         "will not hold a rib."),
    ],
    pieces=[
        dict(title="1 · Boo the Ghost — worked top-down, an OPEN BELL",
             note="No closed bottom and NO stuffing; he stands on the weight of his ruffled hem. Do not fasten "
                  "off after Rnd 12 — continue straight into the hem.",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "sc in each st around", "24", ""],
                              ["6", "sc in each st around", "24", ""],
                              ["7", "sc in each st around", "24", ""],
                              ["8", "[11 sc, inc] x 2", "26", "eyes at R8–R9"],
                              ["9", "sc in each st around", "26", ""],
                              ["10", "sc in each st around", "26", "arms at R10"],
                              ["11", "sc in each st around", "26", ""],
                              ["12", "[11 sc, dec] x 2", "24", "live edge — hem & base here"],
                              ["13", "FLO: [sl st 2, (sc,hdc,dc,hdc,sc) in next st, sl st 1] x 6", "48",
                               "RUFFLED HEM"]]),
             paras=["Each hem repeat takes 4 stitches and returns 8; six repeats close all 24 stitches and make "
                    "six ruffles (48 sts). The hem adds ~10 mm of depth, included in Boo's 48 mm height. Fasten "
                    "off and weave in. Boo stands on his ruffled hem — an open bell with no stuffing and no "
                    "closed bottom.",
                    "Eyes: insert the 6 mm safety eyes BEFORE you sew anything, while the open bottom lets you "
                    "reach the washers. Place them on Rnd 8–9, about 5 stitches apart, centred on the front (the "
                    "widest round is 26 stitches ≈ 29 mm, so 5 apart keeps them well inside the face). Smile & "
                    "blush: black floss curved smile centred below the eyes, pink floss horizontal stitches "
                    "either side for blush."]),
        dict(title="Boo's arms (make 2) and optional flat base (make 1)",
             paras=["ARMS — cream, make 2 (no stuffing): R1: 5 sc in MR (5). R2: sc around (5). R3: sc around (5). "
                    "Fasten off with a tail; sew to the sides at Rnd 10, angled slightly forward.",
                    "FLAT BASE — optional, make 1: R1: 6 sc in MR (6). R2: inc x 6 (12). R3: [sc, inc] x 6 (18). "
                    "R4: [2 sc, inc] x 6 (24). The flat disc matches the 24 back loops of Rnd 12. Sew it to the "
                    "BACK loops from inside, leaving the hem free to flare below; a few stitches can be lightly "
                    "padded for weight."]),
        dict(title="Bonus mini witch hat",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "4 sc in MR", "4", ""],
                              ["2", "[sc, inc] x 2", "6", ""],
                              ["3", "[2 sc, inc] x 2", "8", ""],
                              ["4", "[3 sc, inc] x 2", "10", ""],
                              ["5", "sc in each st around", "10", ""],
                              ["6", "FLO: inc in each st around", "20", "brim"]]),
             paras=["Sl st, fasten off. The brim stops at 20 stitches — a snug ~22 mm crown that stretches to "
                    "sit on Boo's ~29 mm head instead of swamping him (cotton gives). Sew it on tilted."]),
        dict(title="2 · Pip the Pumpkin — worked bottom-up, overstuff before sculpting",
             note="Only two straight rounds — that keeps Pip squat rather than tall like a lemon. Do NOT cut the "
                  "yarn short: leave a 25 in / 65 cm tail for sculpting.",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "[3 sc, inc] x 6", "30", ""],
                              ["6", "[4 sc, inc] x 6", "36", "full width — check gauge"],
                              ["7", "sc in each st around", "36", ""],
                              ["8", "sc in each st around", "36", ""],
                              ["9", "[4 sc, dec] x 6", "30", ""],
                              ["10", "[3 sc, dec] x 6", "24", "stuff firmly, then OVERSTUFF"],
                              ["11", "[2 sc, dec] x 6", "18", ""],
                              ["12", "[sc, dec] x 6", "12", ""],
                              ["13", "dec x 6", "6", "leave 65 cm tail"]]),
             paras=["Sculpting six ribs: thread the tail; anchor points are the top centre (R13) and bottom "
                    "centre (R1). Bring the needle down through the top and out the bottom, pull gently until "
                    "the surface dimples (do not strangle it). Move 6 stitches sideways along the bottom, come "
                    "back up to the top centre, pull and anchor with a small stitch. Repeat — six passes divide "
                    "the 36-stitch body into six even ribs. Pull every rib to the SAME tension; finish by "
                    "knotting, running the needle out the side, and pulling the knot inside.",
                    "Face: with black floss, embroider two small triangle eyes on the front, roughly level with "
                    "the middle of the body and about 6 stitches apart, then a short zigzag mouth below. Keep "
                    "the face inside one rib panel so the sculpting does not cross it."]),
        dict(title="Pip's stem, leaf & tendril — sage green",
             paras=["STEM CONE — make 1: R1: 6 sc in MR (6). R2: sc around (6). R3: [sc, inc] x 3 (9). R4: sc "
                    "around (9). R5: [2 sc, inc] x 3 (12). Fasten off with a tail, stuff very lightly, sew to "
                    "the top centre over the R13 opening.",
                    "LEAF — make 1 (flat): Found: ch 7. Row 1: sc 5, 3 sc in last ch, then down the other side "
                    "sc 4, inc in the last loop (14). Row 2: ch 1, turn; sc 4, inc x3, sc 4 (14; the row is "
                    "worked over 11 of the 14 stitches so the leaf tapers — the remaining edge is closed by the "
                    "next row). Row 3: ch 1, turn; sl st around; fasten off. The final sl-st row gives a firm "
                    "rolled edge — sew to the stem base, angled out to one side.",
                    "TENDRIL: ch 20; from the 2nd ch, work sl st in each chain to the end, fasten off with a "
                    "tail. The slip stitches make the chain curl into a tight spiral — wind it once around the "
                    "stem base and sew the end down (a few chains longer and looser if it will not hold a curl)."]),
        dict(title="3 · Bramble the Bat — worked top-down in lavender",
             note="Eyes go in after Rnd 8, before Rnd 9 narrows the body — that is your last chance to fit the "
                  "washers from inside.",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", "ears at R4–R5"],
                              ["5", "sc in each st around", "24", ""],
                              ["6", "sc in each st around", "24", ""],
                              ["7", "sc in each st around", "24", "eyes at R7–R8"],
                              ["8", "sc in each st around", "24", "fit washers now"],
                              ["9", "[3 sc, inc] x 6", "30", "wings at R9–R11"],
                              ["10", "sc in each st around", "30", ""],
                              ["11", "sc in each st around", "30", ""],
                              ["12", "sc in each st around", "30", ""],
                              ["13", "[3 sc, dec] x 6", "24", "stuff firmly"],
                              ["14", "[2 sc, dec] x 6", "18", ""],
                              ["15", "[sc, dec] x 6", "12", ""],
                              ["16", "dec x 6", "6", "weave & close"]]),
             paras=["Eyes: place on Rnd 7–8, just 4 stitches apart and centred — close on purpose, since the "
                    "head is only 24 stitches around and wide eyes wrap to the sides. Fangs: two small white "
                    "V-stitches just under the eyes; add pink blush."]),
        dict(title="Bramble's ears (make 2 pairs)",
             paras=["OUTER EAR — lavender, make 2: R1: 4 sc in MR (4). R2: [sc, inc] x 2 (6). R3: [2 sc, inc] x 2 (8).",
                    "INNER EAR — pink, make 2: R1: 4 sc in MR (4). R2: [sc, inc] x 2 (6). R3: [2 sc, inc] x 2 (8). "
                    "R4: [3 sc, inc] x 2 (10).",
                    "Flatten and do not stuff. Sew a pink inner onto each lavender outer, then sew the pairs to "
                    "the top of the head at about Rnd 4–5, angled slightly outward."]),
        dict(title="Bramble's wings — worked FLAT in turned rows, make 2",
             paras=["Ch 13. Row 1: from the 2nd ch, sc in 4, hdc in 4, dc in 4. Ch 1, turn. [12]",
                    "Row 2: sc in 3, hdc in 4, dc in 5. Ch 1, turn. [12]",
                    "Row 3 (scalloped edge): sl st in the first 2, (sc, hdc, dc, picot, dc, hdc, sc) in the next "
                    "st, sl st in the next 3, (sc, hdc, picot, hdc, sc) in the next st, sl st in the next 2, "
                    "(sc, hdc, picot, hdc, sc) in the next st, sl st in the last 2. Fasten off with a 10 in tail.",
                    "The slip-stitch groups are 2 + 3 + 2 + 2 = 9 stitches; the three scallops each fan from a "
                    "single stitch (3 more), so all 12 stitches of Row 2 are consumed and nothing is left over. "
                    "The three scallops are deliberately different sizes — the middle is 7 stitches tall with a "
                    "dc peak (the pointed wing tip), the two outer are 5 stitches with an hdc peak; each carries "
                    "exactly one picot.",
                    "Assembly: pin the wings to the back and sides between Rnd 9 and Rnd 11, angled out and "
                    "slightly up, then sew along the straight inner edge (leave the scalloped edge free). Each "
                    "wing is about 42 mm long; with a 33 mm body that gives a wingspan of roughly 11.5 cm."]),
        dict(title="Display — Halloween garland",
             paras=["Cut 6 ft of jute twine, or chain about 450 in sage (a chained cord is shorter than it "
                    "looks — 150 chains is only ~60 cm). Make 3 of each mini, thread 20 mm felt balls between "
                    "them, and tie or slip-stitch each piece 4–5 in apart. A full garland uses about 25 g cream, "
                    "30 g orange, 27 g lavender, 12 g sage."]),
    ],
    assembly=dict(
        title="Before you assemble",
        bullets=[
            ("Boo:", "1 body with ruffled hem, 2 arms, 1 optional flat base, 1 witch hat."),
            ("Pip:", "1 sculpted body, 1 stem cone, 1 tendril, 1 leaf."),
            ("Bramble:", "1 body, 2 lavender outer ears, 2 pink inner ears, 2 picot wings."),
        ],
        checklist=["Lay every component out and check it against the pattern; pin each piece and look at the "
                   "toy from the front before committing a single stitch."],
        listing=[("Eyes:", "Boo and Bramble use 6 mm safety eyes; Pip's face is embroidered. For child-safe "
                  "versions, embroider all faces."),
                 ("Sell as:", "decorative pieces — not toys for children under 3.")]),
    troubleshooting=[
        ("Pumpkin looks tall.", "more than two straight rounds at Rnd 7–8 — extra plain rounds turn a pumpkin "
         "into a lemon."),
        ("Ribs vanish.", "overstuff before sculpting and pull each rib firmly to the same tension; one "
         "over-tight rib pulls the body out of round."),
        ("Ruffle gaps at the marker.", "each hem repeat must take exactly 4 stitches (2 sl st, shell into 1, "
         "1 sl st); six repeats use all 24."),
        ("Wing row runs short.", "the Row 3 groups are 2 / 3 / 2 / 2 — count the slip stitches, not the scallops."),
        ("Wing scallops look uneven.", "they are meant to be — the middle scallop is the largest; check you "
         "have not swapped their order."),
        ("Ghost leans / will not stand.", "the two Rnd 8 increases must sit opposite each other ([11 sc, inc] x 2). "
         "Boo takes no stuffing; if he falls, sew on the optional flat base."),
        ("Hat swamps the ghost.", "stop the brim at Rnd 6, 20 stitches — a wider brim flares past Boo's ~29 mm head."),
        ("Cannot fit the eye washers.", "you closed the piece first. Boo's eyes go in through his open bottom; "
         "Bramble's go in after Rnd 8 before the body narrows."),
    ],
    colorways=[("Classic cream", (240, 232, 214)), ("Pumpkin orange", (214, 116, 42)),
               ("Bat lavender", (154, 130, 178)), ("Ghostly white", (247, 245, 240)),
               ("Charcoal", (86, 82, 80)), ("Sage & oat", (154, 166, 138))],
    checks=[
        ["Boo Rnds 1–13: 6 → 26 → 24 → hem 48 (4 sts in, 8 out x 6)", "✓ verified"],
        ["Boo arms (5) & base 6 → 24 = 24 back loops", "✓ verified"],
        ["Pip Rnds 1–13: 6 → 36 → 6; stem 6 → 12; leaf 14 sts", "✓ verified"],
        ["Bramble Rnds 1–16: 6 → 24 → 30 → 6; ears 4 → 8 / 10", "✓ verified"],
        ["Bramble wing Row 3 consumes 2+3+2+2+3 scallops = 12 sts", "✓ verified"],
        ["Boo height 12 rnds x 3.2 mm + 10 mm hem ≈ 48 mm", "✓ verified"],
        ["Boo head 26 sts ≈ 29 mm; brim 20 sts ≈ 22 mm (snug)", "✓ verified"],
        ["Pip gauge 36 sts ≈ 40 mm around a stuffed body", "✓ verified"],
    ],
    safety_reminder="This pattern has not been tested to a toy-safety standard (ASTM F963 / EN 71) and uses "
                    "6 mm safety eyes. Finished items made for sale must be assessed by the seller against "
                    "local toy-safety laws; for young children, embroider the faces and secure every seam.",
)

AXEL = dict(
    slug="axel", code="NS 03", file_stem="Axel_the_Axolotl_Crochet_Pattern_NS03",
    title="Axel the Axolotl",
    subtitle="A soft pink axolotl with six fluffy gills, a round head and a shell-edged paddle tail — head, neck, body and tail in one continuous spiral, no neck seam to sew",
    cover="assets/axel_cover.png",
    badges=["US terms", "Advanced beginner", "2.5–3 hours"],
    size_line="About 11.5 cm (4.5 in) tall seated  •  ~10 cm (4 in) gill tip to gill tip  •  4.3 cm tail  •  "
              "head a near-true sphere at ~52 mm wide x 51.6 mm tall",
    materials_line="Worsted #4 pale pink ~15 g  •  fuzzy/eyelash dark pink ~8 g  •  worsted dark pink ~3 g  •  "
                   "3.5 mm hook  •  two 6 mm safety eyes",
    terms_name="Axels", tags="#AxelTheAxolotl",
    theme=dict(dark=(140, 62, 88), accent=(199, 106, 132), soft=(247, 236, 240),
               box_bg=(249, 238, 242), box_edge=(199, 106, 132)),
    safety=dict(title="SAFETY — READ THIS FIRST", lines=[
        ("Axel has two 6 mm safety eyes. Safety eyes are small parts: lock the washers firmly from the "
         "inside before stuffing, and pull-test every eye on the finished toy — a properly locked washer "
         "will not come off by hand.", True),
        "The gills, arms, feet and tail fin are all sewn or worked on: sew each seam twice and weave every "
        "end in for at least 5 cm, then trim close — a loose gill is the first thing a child will pull.",
        "This pattern has not been tested to ASTM F963 or EN 71, so do not describe finished Axels as "
        "“baby-safe”. For children under 3, skip the safety eyes and stitch the eyes with black floss instead.",
    ]),
    materials=[
        ("Main yarn:", "worsted #4, pale pink, about 15 g. Cotton or acrylic with a smooth matte finish — one "
         "25 g ball covers the whole axolotl."),
        ("Gill yarn:", "fuzzy / eyelash / fur yarn, dark pink, about 8 g. Essential: smooth worsted will not "
         "give fluffy gills, and the gills are the whole look."),
        ("Fin yarn:", "worsted #4, dark pink, about 3 g, smooth — so the shell edging stays crisp."),
        ("Hook & eyes:", "3.5 mm (US E/4) for a tight gauge so stuffing cannot show through. Two 6 mm safety "
         "eyes (9 mm reads as buggy on this head)."),
        ("Also:", "polyester filling about 8 g; tapestry needle; black embroidery floss; pink pastel or chalk; "
         "stitch marker."),
    ],
    gauge=[("36 sc around measures about 52 mm across when stuffed (4.5 mm per stitch, 4.3 mm per round).", True),
           "Wider than 55 mm? Drop to a 3.0 mm hook; under 48 mm? Go up to a 4.0 mm hook."],
    abbrev="MR magic ring  •  ch chain  •  sc single crochet  •  dc double crochet  •  inc increase (2 sc in one st)  •  "
           "invdec invisible decrease  •  sl st slip stitch  •  st(s) stitch(es)  •  FO fasten off  •  "
           "(n) stitch count at round end.",
    construction=[
        ("One piece.", "head, neck, body and tail are worked in a single spiral from the top of the head "
         "straight through to the tail tip — there is no neck seam to sew."),
        ("Shared width.", "head and body are both 36 stitches around; the neck at R13 is the only waist. "
         "Three straight rounds at the head keep it spherical rather than egg-shaped."),
    ],
    techniques=[
        ("The magic ring", "every piece begins with a magic ring; pull the tail to close it tight once the "
         "first round is complete."),
        ("Work in a spiral", "do not join and do not chain 1 between rounds. Keep a stitch marker in the first "
         "stitch of every round and move it up each time; there is no join to count from."),
        ("The invisible decrease", "insert the hook through the front loops only of the next two stitches, "
         "yarn over and pull through both, then yarn over and pull through the remaining two loops. It leaves "
         "no ridge, which matters on the head and neck where decreases are visible."),
        ("Closing through both layers", "to close a flat opening, fold the piece flat so the front and back "
         "layers lie together, then work one sc through each matched pair of stitches. Axel's 6-stitch tail "
         "tip folds into 3 pairs and closes with 3 sc."),
        ("The shell (scallop)", "work all the stitches of the group into one stitch, then slip stitch into the "
         "next stitch to anchor it. The group fans into a cup. Working the dc loosely makes each scallop cup "
         "outward instead of lying flat."),
    ],
    pieces=[
        dict(title="1 · Head, body & tail — one continuous spiral, 36 rounds",
             table=dict(widths=[13, 62, 15, 88],
                        headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", "start at top of head"],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[1 sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "[3 sc, inc] x 6", "30", ""],
                              ["6", "[4 sc, inc] x 6", "36", "head at full width"],
                              ["7", "sc in each st around", "36", "eyes between R7 / R8"],
                              ["8", "sc in each st around", "36", ""],
                              ["9", "sc in each st around", "36", "smile on R8–R9"],
                              ["10", "[4 sc, invdec] x 6", "30", ""],
                              ["11", "[3 sc, invdec] x 6", "24", "STUFF HEAD FIRMLY"],
                              ["12", "[2 sc, invdec] x 6", "18", ""],
                              ["13", "sc in each st around", "18", "NECK — narrowest point"],
                              ["14", "[2 sc, inc] x 6", "24", "body flares out"],
                              ["15", "[3 sc, inc] x 6", "30", ""],
                              ["16", "[4 sc, inc] x 6", "36", "body at full width"],
                              ["17", "sc in each st around", "36", "arms at R17–R18"],
                              ["18", "sc in each st around", "36", ""],
                              ["19", "sc in each st around", "36", ""],
                              ["20", "sc in each st around", "36", ""],
                              ["21", "sc in each st around", "36", ""],
                              ["22", "sc in each st around", "36", ""],
                              ["23", "[4 sc, invdec] x 6", "30", ""],
                              ["24", "[3 sc, invdec] x 6", "24", "FEET attach at R24–R25"],
                              ["25", "[2 sc, invdec] x 6", "18", "stuff body LIGHTLY"],
                              ["26", "[1 sc, invdec] x 6", "12", ""],
                              ["27", "sc in each st around", "12", "tail begins"],
                              ["28", "[2 sc, invdec] x 3", "9", ""],
                              ["29", "sc in each st around", "9", ""],
                              ["30", "sc in each st around", "9", ""],
                              ["31", "sc in each st around", "9", ""],
                              ["32", "[1 sc, invdec] x 3", "6", "light stuffing to here"],
                              ["33", "sc in each st around", "6", ""],
                              ["34", "sc in each st around", "6", ""],
                              ["35", "sc in each st around", "6", ""],
                              ["36", "sc in each st around", "6", "taper to tip"]]),
             paras=["Finish: fold the last 6 stitches flat so 3 pairs line up (3 front + 3 back), then work 1 sc "
                    "through each pair — 3 sc in total — to close the tip cleanly. Fasten off and weave the end "
                    "back through the tail tip and out along the top ridge; you will crochet the fin directly "
                    "onto that ridge in step 4. The tail runs R27–R36 — ten rounds, about 43 mm — giving the fin "
                    "a long enough ridge to sit on."]),
        dict(title="2 · Arms & feet — sewn on, not worked into the body",
             note="Bobbles will not give you rounded limbs.",
             paras=["ARMS — make 2: R1: 6 sc in MR (6). R2–R6: sc around (6), then fasten off. Fasten off with a "
                    "long tail, do not stuff. Flatten the open end and sew it closed as you attach, so the arms "
                    "hang softly.",
                    "FEET — make 2: R1: 6 sc in MR (6). R2: [1 sc, inc] x 3 (9). R3–R4: sc around (9). "
                    "R5: [1 sc, invdec] x 3 (6). Fasten off, cinch closed with a long tail and stuff lightly — "
                    "do not flatten them, they are plump little balls; sew the cinched nub toward the body."]),
        dict(title="3 · Gills — make 6 (3 per side, fuzzy dark pink)",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "sc around", "12", ""],
                              ["4", "sc around", "12", ""],
                              ["5", "[1 sc, invdec] x 4", "8", "open edge sewn to head"]]),
             paras=["Working with fuzzy yarn: you cannot see the stitches. Hold a thin strand of matching smooth "
                    "yarn together with the fur yarn so you can find the stitches, or count by feel with the "
                    "hook tip and trust the round count. Small errors are invisible in the finished fluff.",
                    "Finish gills: fasten off with a long tail. The open edge sewn straight to the head "
                    "disappears in the fluff — simply whip-stitch the 8-st opening flat against the head (or "
                    "cinch the front loops first if you prefer a rounded lobe). Three fluffy gills fan behind "
                    "each eye — upper angled up, middle out, lower down."]),
        dict(title="4 · The shell-edged tail fin",
             paras=["With smooth dark pink yarn, join with a sl st to the top ridge of the tail at the very tip "
                    "(join into the tip end-closure corner). Working along the ridge back toward the body: "
                    "* 5 dc in the next ridge stitch, sl st in the next ridge stitch. Repeat from * a total of "
                    "5 times (5 scallops). Fasten off and weave in.",
                    "Each scallop uses 2 ridge stitches, so the fin spans 10 stitches. The tail from R27 to R36 "
                    "gives a ridge of about 10 workable stitches along one side, so 5 scallops fit it exactly — "
                    "start at the tip and work back toward the body, then anchor the last sl st into the body "
                    "junction. Work the dc groups loosely so each scallop cups outward. For a fuller paddle, "
                    "work a second identical 5-scallop row along the underside ridge rather than stretching one "
                    "row around the tip."],
             boxes=[dict(title="A note on fullness", lines=[
                 "Five shells over ten rounds is meant to ruffle — the cupped, frilly edge is the look, not a "
                 "mistake. If the scallops seem crowded, work the dc even more loosely, use half a hook size "
                 "larger for the fin yarn only, or work 4 scallops on a shorter ridge."])]),
    ],
    assembly=dict(
        title="5 · Face, eyes & assembly",
        bullets=[
            ("Eyes:", "insert the 6 mm safety eyes between R7 and R8, 6 stitches apart, centred on the front of "
             "the head. Six stitches spans about 27 mm on the 52 mm head — about half the width. Fix the "
             "washers before stuffing, and pull-test each eye once it is locked."),
            ("Smile:", "with black floss, embroider a wide shallow U across R8–R9, centred between the eyes and "
             "about 5 stitches wide. Keep it shallow; a deep curve reads as a frown."),
            ("Blush:", "brush soft pink pastel or chalk in a small circle directly under each eye, just outside "
             "the eye line."),
            ("Gills:", "sew 3 lobes to each side of the head, behind the eyes, anchored at about R6 (upper), "
             "R7–R8 (middle) and R9 (lower). Angle the top lobe upward, the middle one straight out and the "
             "bottom one downward so they fan, then tease the fibres apart with a slicker brush or your fingers."),
            ("Arms:", "sew one arm to each side at R17–R18, about 6 stitches out from the centre front, angled "
             "slightly forward."),
            ("Feet:", "sew one foot to each side of the centre front at R24–R25, about 4 stitches out from "
             "centre, so Axel sits flat and upright."),
        ],
        checklist=["1 body (head to tail in one piece)  •  2 arms  •  2 feet  •  6 gills  •  1 fin. "
                   "Check each against the pattern before attaching anything."],
        listing=[("Care:", "spot clean or hand wash cool, squeeze in a towel and air dry; do not tumble dry. "
                  "Fuzzy gills: fluff with a slicker brush once dry."),
                 ("Safety note for listings:", "decorative plush with 6 mm safety eyes — not suitable for "
                  "children under 3 unless the eyes are embroidered.")]),
    troubleshooting=[
        ("Head firm, body soft.", "stuff the head hard at R11 so it holds a sphere and the eyes stay level. "
         "Keep the body light so Axel stays squishy and sits down."),
        ("Neck collapsing.", "the 18-stitch neck is deliberately narrow. First pack a little more stuffing into "
         "the neck through the body opening before closing R25. For a permanently sturdier neck, work R13 as "
         "[7 sc, inc] x 2, 2 sc (20), then change R14 to [4 sc, inc] x 4 (24) so it consumes all 20 stitches; "
         "R15 onward is unchanged."),
        ("Fin runs out of tail.", "the ridge holds 10 stitches and 5 scallops need exactly 10. If you shortened "
         "the tail, work fewer scallops rather than crowding them."),
        ("Want a wider gill span?", "as written the gills give about 10 cm tip to tip. Work each gill two rounds "
         "longer — add 2 plain rounds at 12 stitches before R5 — for a span of about 12 cm."),
        ("Stuffing shows through.", "go down to a 3.0 mm hook. Loose gauge on a 3.5 mm hook is the usual cause."),
        ("Axel will not sit.", "move the feet one round lower and make sure the R23–R26 decreases are centred "
         "on the underside, not the back."),
    ],
    colorways=[("Classic pink", (222, 154, 172)), ("White leucistic", (240, 236, 230)),
               ("Melanoid black", (74, 70, 70)), ("Mint", (162, 196, 173)),
               ("Lavender", (180, 160, 200))],
    checks=[
        ["Body Rnds 1–36: 6 → 36 → 18 → 36 → 12 → 9 → 6 chain", "✓ verified"],
        ["Arms 6 sts; feet 6 → 9 → 6; gills 6 → 12 → 8", "✓ verified"],
        ["Head sphere: 36 sts x 4.5 mm = 51.6 mm; 12 rnds = 51.6 mm tall", "✓ verified"],
        ["Tail R27–36 = 10 rnds = 43 mm; fin = 5 scallops x 2 ridge sts = 10", "✓ verified"],
        ["Eye gap 6 sts = 27 mm ~ half the 52 mm head", "✓ verified"],
        ["Sturdier-neck option: R13 = 20 sts, R14 [4 sc, inc] x 4 = 24", "✓ verified"],
    ],
    safety_reminder="This pattern has not been tested to a toy-safety standard such as ASTM F963 or EN 71. Axel "
                    "uses two 6 mm safety eyes (small parts): for children under 3, embroider the eyes instead. "
                    "Finished items made for sale must be assessed by the seller against local toy-safety laws.",
)
