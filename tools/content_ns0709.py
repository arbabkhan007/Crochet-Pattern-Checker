# -*- coding: utf-8 -*-
"""Pattern specs NS 07-09: Pocket Positivity Trio, Ember the Baby Dragon, Shelby the Sea Turtle."""

TRIO = dict(
    slug="trio", code="NS 07", file_stem="Pocket_Positivity_Trio_Crochet_Pattern_NS07",
    title="Pocket Positivity Trio",
    subtitle="Three palm-sized amigurumi that slip into a coat pocket — Sunny the Sunflower, Waddle the Penguin and Spud the Potato; one easy construction, an evening or two of work",
    cover="assets/trio_cover.png",
    badges=["3 mini patterns", "Easy / beginner", "20–35 min each"],
    size_line="Sunny ~3.0 cm across the petals  •  Waddle ~3.8 cm tall  •  Spud ~2.7 cm long  •  "
              "#4 worsted on a 3.5 mm hook  •  Sunny and Waddle need no sewn pieces",
    materials_line="Worsted scraps (~8 m / under 4 g total)  •  six 5 mm safety eyes (or embroidery)  •  "
                   "3.5 mm hook  •  ~3 g fibre fill",
    terms_name="toys", tags="#PocketPositivityTrio",
    theme=dict(dark=(140, 96, 20), accent=(198, 142, 32), soft=(250, 242, 218),
               box_bg=(250, 240, 224), box_edge=(188, 128, 30)),
    safety=dict(title="SAFETY — SMALL PARTS", lines=[
        ("The set uses 5 mm black safety eyes (six in total) — small parts and a choking hazard, not "
         "intended for children under 3.", True),
        "For young children, embroider the eyes and mouths instead.",
        "Sellers: do not market as “baby-safe”; sell as adult collectibles, desk companions or keychain "
        "charms, and tag with materials, your maker name and “Not suitable for children under 3 years”.",
    ]),
    materials=[
        ("Yarn:", "#4 worsted (~250 m / 100 g). The three toys use roughly 8 m total (under 4 g), so scraps "
         "are fine. Golden yellow + chocolate (Sunny); black + cream chest + yellow beak (Waddle); warm tan (Spud)."),
        ("Hook & eyes:", "3.5 mm (US E/4). Six 5 mm black safety eyes, or embroidery thread."),
        ("Also:", "about 3 g fibre fill total, blunt tapestry needle, stitch marker, scissors."),
    ],
    gauge=[("About 3.5 mm per stitch and 3.2 mm per round in sc.", True),
           "Pocket size means gauge shows — work a swatch; the stated sizes follow from it."],
    abbrev="MR magic ring  •  sc single crochet  •  hdc half double crochet  •  inc (2 sc in one st)  •  "
           "dec (invisible decrease)  •  sl st slip stitch  •  ch chain  •  sts stitches.",
    construction=[
        ("Shared recipe.", "continuous spiral rounds with a marker (no joins); magic-ring start for Sunny's "
         "centre and Waddle's body; invisible decreases; petal clusters worked into one stitch with a slip "
         "stitch between petals; an oval worked around a chain for Spud; simple sewing/embroidery."),
    ],
    techniques=[
        ("Petal clusters", "the (sc, hdc, sc) group is worked into ONE stitch with a slip stitch in the "
         "valley between petals — each repeat takes 2 stitches and returns 4."),
        ("Ovals around a chain", "Spud and Waddle's chest patch are worked around both sides of a foundation "
         "chain — flat ovals, not circles."),
    ],
    pieces=[
        dict(title="1 · Sunny the Sunflower — brown centre, nine petals worked into Rnd 3",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", "petals join here"],
                              ["4", "sc in each st around", "18", ""],
                              ["5", "[sc, dec] x 6", "12", ""],
                              ["6", "dec x 6", "6", "stuff firmly before closing"]]),
             paras=["PETALS — yellow, one round: join yellow with a sl st into any st of Rnd 3, then "
                    "[sl st in next st, (sc, hdc, sc) in next st] x 9 (36).",
                    "Each repeat uses 2 stitches (a slip stitch, then three stitches into the next), so nine "
                    "petals close the 18-stitch round exactly. The slip stitch sits in the valley between "
                    "petals; work this round loosely (use a 4 mm hook for this round only if it pulls tight). "
                    "Fasten off and weave in.",
                    "Face: embroider a smiling mouth between Rnd 2–3 and add eyes 3 stitches apart on Rnd 2 "
                    "(~10.5 mm; use 4 apart only if embroidering)."]),
        dict(title="2 · Waddle the Penguin — bottom-up with a chest patch",
             table=dict(widths=[15, 60, 15, 88],
                        headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", "eyes on R3"],
                              ["4", "sc in each st around", "18", ""],
                              ["5", "sc in each st around", "18", ""],
                              ["6", "sc in each st around", "18", "wings at R6"],
                              ["7", "[2 sc, inc] x 6", "24", "chest over R4–8"],
                              ["8", "sc in each st around", "24", ""],
                              ["9", "sc in each st around", "24", ""],
                              ["10", "[2 sc, dec] x 6", "18", ""],
                              ["11", "[sc, dec] x 6", "12", ""],
                              ["12", "dec x 6", "6", "stuff as you go, close"]]),
             paras=["WINGS (black, make 2): 4 sc in MR (4); [sc, inc] x 2 (6); sc around for 2 rnds (6). Fasten "
                    "off with a 15 cm tail, do not stuff; sew to the sides at Rnd 6 angled backward.",
                    "CHEST PATCH (cream, flat oval): ch 6, sc in 2nd ch, 3 sc, 3 sc in last ch, then down the "
                    "other side 3 sc, 2 sc in last ch (12); Rnd 2: inc, 3 sc, inc x3, 3 sc, inc x2 (18). Fasten "
                    "off with a tail; sew onto the front covering Rnds 4–8, stitching top and bottom edges only "
                    "so the middle puffs.",
                    "BEAK (yellow): ch 2, 3 sc in 2nd ch (3); inc x3 (6); sc around (6). Fasten off, do not "
                    "stuff; sew centred between the eyes, angled slightly down. Eyes 3 stitches apart on Rnd 3; "
                    "add a touch of pink blush sparingly."]),
        dict(title="3 · Spud the Potato — oval base, one flat seam",
             table=dict(widths=[15, 72, 15, 76],
                        headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["Found.", "ch 7", "—", "foundation"],
                              ["1", "sc in 2nd ch, 4 sc, 3 sc in last ch; other side: 4 sc, 2 sc in last ch", "14",
                               "around the chain"],
                              ["2", "inc, 4 sc, inc x3, 4 sc, inc x2", "20", ""],
                              ["3", "sc in each st around", "20", ""],
                              ["4", "sc in each st around", "20", "face around here"],
                              ["5", "sc in each st around", "20", ""],
                              ["6", "sc in each st around", "20", ""],
                              ["7", "[3 sc, dec] x 4", "16", ""],
                              ["8", "[2 sc, dec] x 4", "12", ""],
                              ["9", "[sc, dec] x 4", "8", "begin stuffing"],
                              ["10", "dec x 4", "4", "close the seam"]]),
             paras=["Closing: leave a 20 cm tail. With the body flat, whip-stitch the remaining opening closed "
                    "along the flat top so the seam reads as the potato's natural crease; weave the end inside. "
                    "Face: eyes about 5 stitches apart on the broad side around Rnd 4 (Spud's face is ~27 mm "
                    "wide, so 4 or 5 apart both fit), with a small open mouth below."]),
        dict(title="Making a bigger trio",
             paras=["Use chunky/aran or hold #4 double on a 3.5 mm hook (~4.5 mm/stitch, about 1.3x): Sunny "
                    "~3.9 cm, Waddle ~4.9 cm, Spud ~3.5 cm. Stitch counts do not change."]),
    ],
    assembly=dict(
        title="Selling & care",
        bullets=[
            ("Sell as:", "adult collectibles, desk companions or keychain charms — not “baby-safe”."),
            ("Stuff:", "firmly and evenly."),
            ("Care:", "spot clean with a damp cloth; do not machine wash; fluff pulled loops with a clean "
             "slicker brush or toothbrush."),
        ],
        boxes=[dict(title="Before you finish", lines=[
            "Check each toy: Sunny has 9 even petals and a closed brown centre; Waddle has 2 wings, a cream "
            "chest and a yellow beak; Spud's seam reads as a crease. All eyes are locked or embroidered and "
            "every end is woven in at least 5 cm."])],
        listing=[("Also try:", "all-white with silver wings, charcoal with orange, or sage-and-oatmeal for a "
                  "muted autumn set. Jewel and pastel tones both photograph well against a pale background.")]),
    troubleshooting=[
        ("Petal edges curl / will not close.", "use invisible decreases on the centre's Rnd 5 and pull the "
         "closing snug. Nine petal repeats use exactly 18 stitches (two each) — check Rnd 3 is (18) and you "
         "slip-stitched once per repeat."),
        ("Petals sit flat.", "work the three stitches in one stitch loosely, or use a 4 mm hook for the petal "
         "round only."),
        ("Toys come out smaller / larger.", "tighter than 3.5 mm/stitch: go up half a hook size or hold yarn "
         "double. Looser: drop to a 3 mm hook."),
        ("Waddle's wings flop.", "sew at Rnd 6 and catch a stitch of the body with each pass."),
        ("Spud's seam shows.", "whip-stitch along the flat top so the seam reads as a crease, and stuff evenly "
         "before closing."),
        ("Eyes too near the edge.", "on Sunny and Waddle place them three stitches apart, not four."),
    ],
    colorways=[("Golden yellow", (222, 168, 42)), ("Warm tan", (188, 142, 96)),
               ("Penguin black", (56, 54, 56)), ("Cream chest", (240, 232, 216)),
               ("Chocolate centre", (110, 74, 48))],
    checks=[
        ["Sunny centre 6 → 18 → 6; petal round 18 → 36 (9 x [1 sl st + 3-st cluster])", "✓ verified"],
        ["Waddle 6 → 18 → 24 → 6; wings 4 → 6; chest 12 → 18; beak 3 → 6", "✓ verified"],
        ["Spud oval 14 → 20 → 20 → 8 → 4; ch-7 foundation consumes fully", "✓ verified"],
        ["Waddle height 12 rnds x 3.2 mm = 38.4 mm ~ 3.8 cm", "✓ verified"],
        ["Bigger trio x1.3: 3.9 / 4.9 / 3.5 cm", "✓ verified"],
        ["Six 5 mm eyes accounted for (2 + 2 + 2)", "✓ verified"],
    ],
    safety_reminder="This set uses 5 mm safety eyes (small parts) and is not intended for children under 3. "
                    "Finished items sold for children must meet local toy-safety laws (EN 71 / CE in the EU; "
                    "CPSIA and ASTM F963 in the US); for young children embroider the eyes and mouths and "
                    "secure every end.",
)

EMBER = dict(
    slug="ember", code="NS 08", file_stem="Ember_the_Baby_Dragon_Crochet_Pattern_NS08",
    title="Ember the Baby Dragon",
    subtitle="A chunky, big-headed baby dragon with a stubby snout, scalloped wings and a ridge of spikes down the back — she sits, with folding haunches and splayed front legs",
    cover="assets/ember_cover.png",
    badges=["US terms", "Intermediate", "4–5 hours"],
    size_line="About 11 cm (4.3 in) tall seated  •  12.5 cm (5 in) wingspan  •  5 cm (2 in) tail  •  "
              "a sitting dragon — her body rests on the table and her legs pose rather than lift her",
    materials_line="Worsted #4 sage ~30 g  •  cream/pale gold contrast ~20 g + 10 g  •  3.5 mm hook  •  "
                   "two 10 mm safety eyes",
    terms_name="Embers", tags="#EmberTheBabyDragon",
    theme=dict(dark=(36, 88, 96), accent=(56, 122, 128), soft=(230, 240, 238),
               box_bg=(234, 242, 238), box_edge=(56, 122, 128)),
    safety=dict(title="SAFETY — 10 mm SAFETY EYES", lines=[
        ("Ember uses 10 mm safety eyes, which are a small part and a choking hazard. Lock the washers from "
         "the inside before the head is joined to the body, and pull-test each eye.", True),
        "She is a decorative piece, not a toy for young children, and has not been tested to ASTM F963 or "
        "EN 71. To give her to a child, embroider the eyes instead and check every seam first.",
    ]),
    materials=[
        ("Main yarn:", "worsted #4, about 30 g used (buy a 50 g ball) — sage green, dusty teal, lilac or "
         "charcoal. The extra allows for tails, sewing and a second attempt."),
        ("Belly & wings:", "worsted #4, about 20 g in a contrast cream or pale gold."),
        ("Spikes:", "worsted #4, about 10 g in the contrast colour (horns, spikes and wings match)."),
        ("Hook:", "3.5 mm (US E/4)."),
        ("Eyes:", "2 x 10 mm safety eyes — slit-pupil dragon eyes if you can get them."),
        ("Also needed:", "polyester fibre fill about 10 g; tapestry needle; stitch markers; pins."),
    ],
    gauge=[("About 4.5 mm per stitch and 4.3 mm per round.", True),
           "Check on the body after Rnd 5 — 30 stitches should measure about 43 mm across when stuffed. If "
           "your stitches are wider, crochet more tightly or drop to a 3.0 mm hook or the stuffing will show."],
    abbrev="MR magic ring  •  ch chain  •  sc single crochet  •  hdc half double crochet  •  dc double crochet  •  "
           "inc increase (2 sc in one st)  •  dec invisible decrease  •  sl st slip stitch  •  FO fasten off  •  "
           "(n) stitch count at round end.",
    construction=[
        ("Spiral.", "work in a continuous spiral unless a row says to turn; mark the first stitch of every "
         "round. Work every stitch through both loops unless a note says otherwise."),
        ("Flat pieces.", "the wings and the spike strip are the exceptions — both are worked flat, in turned rows."),
    ],
    techniques=[
        ("The magic ring", "every piece begins with a magic ring; pull the tail tight once the first round is "
         "complete."),
        ("Work in a spiral", "keep a stitch marker in the first stitch of every round; there is no join to "
         "count from."),
        ("Matched open joins", "Ember's head and her neck are BOTH left open at 18 stitches, so the two edges "
         "are the same size and can be ladder-stitched together cleanly. This is the single most important "
         "structural detail — the head is heavy and this joint carries all of it. Do not close the head down "
         "to a point; stop at 18 stitches."),
        ("How the size adds up", "body Rnds 1–13 = 13 rnd x 4.3 mm = 56 mm; head Rnds 1–11 = 11 rnd x 4.3 mm "
         "= 47 mm; seated height head + body ~ 103 mm = 11 cm. Wingspan 45 + 34 + 45 ~ 124 mm = 12.5 cm. "
         "Tail 12 rnd x 4.3 mm = 52 mm = 5 cm."),
    ],
    technique_boxes=[dict(title="Why the head stays open at 18", lines=[
        "Closing a heavy dragon head down to 6 stitches leaves a small gathered point sewn to a wide neck "
        "ring — a tiny seam carrying a big head, which is exactly why a dragon's head flops. Stopping the head "
        "at 18 stitches matches the 18-stitch neck, so the ladder-stitched join is strong and even."])],
    pieces=[
        dict(title="1 · Head — worked top-down and LEFT OPEN at 18 stitches",
             note="Do not close it and do not fasten off. A big head is what makes a dragon read as a baby "
                  "dragon. Two straight rounds only, then the decreases.",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "[3 sc, inc] x 6", "30", ""],
                              ["6", "[4 sc, inc] x 6", "36", "head at full width"],
                              ["7", "sc in each st around", "36", "eyes at R7–R8"],
                              ["8", "sc in each st around", "36", ""],
                              ["9", "[4 sc, dec] x 6", "30", ""],
                              ["10", "[3 sc, dec] x 6", "24", "stuff firmly"],
                              ["11", "[2 sc, dec] x 6", "18", "LEAVE OPEN — matches neck"]]),
             paras=["Finish: stuff the head firmly. Leave the open 18-stitch edge for sewing to the body's neck "
                    "(a long tail is optional). The snout is sewn on next, then the eyes, BEFORE the head is "
                    "joined."]),
        dict(title="2 · Snout — main colour, make 1",
             table=dict(headers=["Rnd", "Instruction", "Sts"],
                        rows=[["1", "6 sc in MR", "6"],
                              ["2", "[sc, inc] x 3", "9"],
                              ["3", "[2 sc, inc] x 3", "12"],
                              ["4", "sc in each st around", "12"],
                              ["5", "sc in each st around", "12"]]),
             paras=["Fasten off with a long tail and stuff lightly. Pin centred on Rnds 8–11 of the head, just "
                    "below the eye line, and sew all the way around. It must project past the curve of the "
                    "head, not sit flush — a dragon without a projecting snout reads as a bear. Embroider two "
                    "small nostrils at the tip."]),
        dict(title="3 · Body — worked bottom-up, neck left open at 18 stitches",
             note="Pack the neck firmly before you join the head — a soft neck is what lets the head flop forward.",
             table=dict(widths=[13, 62, 15, 88],
                        headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", "tail attaches R4–R6"],
                              ["5", "[3 sc, inc] x 6", "30", "full width — check gauge"],
                              ["6", "sc in each st around", "30", "back legs at R6"],
                              ["7", "sc in each st around", "30", ""],
                              ["8", "sc in each st around", "30", "front legs at R8"],
                              ["9", "sc in each st around", "30", ""],
                              ["10", "[3 sc, dec] x 6", "24", "wings at R10–R11"],
                              ["11", "sc in each st around", "24", ""],
                              ["12", "[2 sc, dec] x 6", "18", "stuff firmly"],
                              ["13", "sc in each st around", "18", "LEAVE THE NECK OPEN"]]),
             paras=["Fasten off with a 40 cm tail; do not close. When you join the head, ladder-stitch all the "
                    "way around and then make a second pass and pull it tight — this joint carries the whole head."]),
        dict(title="4 · Legs — make 4 (back stop Rnd 6, front work Rnds 7–8)",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", "all four"],
                              ["2", "[sc, inc] x 3", "9", "all four"],
                              ["3", "sc in each st around", "9", "all four"],
                              ["4", "sc in each st around", "9", "all four"],
                              ["5", "sc in each st around", "9", "all four"],
                              ["6", "sc in each st around", "9", "BACK legs finish here"],
                              ["7", "sc in each st around", "9", "front legs only"],
                              ["8", "sc in each st around", "9", "front legs only"]]),
             paras=["Finish: stuff the lower half lightly, flatten the top 3 stitches, fasten off with a long "
                    "tail. The pairs are different lengths on purpose: back legs (6 rnd / 26 mm) attach at "
                    "Rnd 6, 26 mm up; front legs (8 rnd / 34 mm) attach at Rnd 8, 34 mm up. A higher join needs "
                    "a longer leg so all four feet reach the table. Sew each pair about 8 stitches apart; angle "
                    "the back legs under as haunches and the front legs slightly forward. The body rests on the "
                    "table — the legs pose, they don't lift her."]),
        dict(title="5 · Horns — contrast colour, make 2",
             paras=["R1: 4 sc in MR (4). R2: sc around (4). R3: [sc, inc] x 2 (6). R4: sc around (6). R5: sc "
                    "around (6). Do not stuff; fasten off with a long tail. Sew to the crown of the head, "
                    "6 stitches apart, angled back."]),
        dict(title="6 · Tail — contrast-free, worked from the tip up so it tapers naturally",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "4 sc in MR", "4", "tip"],
                              ["2", "sc in each st around", "4", ""],
                              ["3", "[sc, inc] x 2", "6", ""],
                              ["4", "sc in each st around", "6", ""],
                              ["5", "sc in each st around", "6", ""],
                              ["6", "[2 sc, inc] x 2", "8", ""],
                              ["7", "sc in each st around", "8", ""],
                              ["8", "sc in each st around", "8", ""],
                              ["9", "[3 sc, inc] x 2", "10", ""],
                              ["10", "sc in each st around", "10", ""],
                              ["11", "sc in each st around", "10", ""],
                              ["12", "sc in each st around", "10", "base"]]),
             paras=["Finish: stuff lightly, fasten off with a long tail, flatten the open end and sew it to the "
                    "back of the body at Rnds 4–6."]),
        dict(title="7 · Wings — contrast colour, worked flat, make 2",
             paras=["Ch 11. Work in turned rows (ch 1 and turn at each row end):",
                    "Row 1: from the 2nd ch, sc in 4, hdc in 3, dc in 3 (10).",
                    "Row 2: sc in 3, hdc in 3, dc in 4 (10).",
                    "Row 3: sc in 2, hdc in 4, dc in 4 (10).",
                    "Row 4 (scalloped edge): sl st in the first 2, (sc, hdc, dc, hdc, sc) all in the next st, "
                    "sl st in the next 2, (sc, hdc, dc, hdc, sc) all in the next st, sl st in the last 4. "
                    "Fasten off with a 25 cm tail."],
             boxes=[dict(title="The scallop maths", lines=[
                 "The slip-stitch anchors are 2 + 2 + 4 = 8 stitches; the two shells each fan from a single "
                 "stitch (2 more), so all 10 stitches of Row 3 are consumed and nothing is left over. Pin the "
                 "straight inner edge across Rnds 10–11 and sew the WHOLE edge so the scalloped edge stays free."])]),
        dict(title="8 · Spike strip — one continuous ridge from crown to tail tip",
             paras=["Nine spikes: 3 on the head, 4 on the body, 2 on the tail. Ch 4, sc in the 2nd ch from the "
                    "hook, then work this group NINE times: ch 4, sl st in the 2nd ch from the hook, sc in the "
                    "next ch, hdc in the next ch. Then sc in the next 2 and fasten off with a long tail.",
                    "Each group makes one small cone (about 10 mm tall); the last stitch of one group is where "
                    "the next begins, so the ten chain-4 units form one continuous ridge with no gaps. The strip "
                    "is about 13.5–15 cm long — slightly under the crown-to-tail path, so it goes on slightly "
                    "snug. PIN it from crown to tail tip first; if it runs short add one more spike "
                    "(about 13.5 mm), if long unpick from the plain end. The spikes deliberately touch — do not "
                    "add plain stitches between them."]),
    ],
    assembly=dict(
        title="9 · Assembly — work in this order",
        bullets=[
            ("1 Snout:", "to the head, centred on Rnds 8–11, below the eye line."),
            ("2 Eyes:", "between Rnds 7 and 8, 8 stitches apart, just above the snout. Fit the washers BEFORE "
             "the head is joined — once closed you cannot reach inside."),
            ("3 Horns:", "to the crown, 6 stitches apart, angled back."),
            ("4 Head to body:", "both edges open at 18 stitches. Pack the neck firmly, seat the head and "
             "ladder-stitch around, then a second tight pass."),
            ("5 Legs:", "back pair to Rnd 6, front pair to Rnd 8, angled as described."),
            ("6 Tail:", "to the back of the body at Rnds 4–6."),
            ("7 Wings:", "across Rnds 10–11, sewn along the whole straight edge."),
            ("8 Spike strip LAST:", "pin from crown to tail tip before you sew a single stitch."),
        ],
        checklist=["1 head (open at 18)  •  1 snout  •  1 body (open neck at 18)  •  4 legs (2 short, 2 long)  •  "
                   "2 horns  •  1 tail  •  2 wings  •  1 spike strip of 10 cones."]),
    troubleshooting=[
        ("Head flops forward.", "pack the neck firmly before closing and make the second ladder-stitch pass "
         "tight. If it still moves, the edges did not match — both head and neck must be open at 18 stitches."),
        ("Rocks back onto haunches.", "the legs are all the same length and they cannot be. Back legs attach "
         "26 mm up, front 34 mm up — work the back legs 6 rounds and the front 8."),
        ("Will not sit.", "legs sewn too high, or the base is under-stuffed. Back legs on Rnd 6, front on "
         "Rnd 8; keep the lower body firm enough to sit on."),
        ("Wings droop.", "sew along the whole straight inner edge, not just the top corner."),
        ("Spike strip is wrong length / curves.", "it is ten chain-4 units worked end to end (not a single "
         "40-chain). Pin the entire strip from crown to tail before sewing; add or unpick a spike as needed. "
         "This is the most visible seam."),
        ("Looks like a bear.", "the snout is missing or under-stuffed — it must project past the dome of the head."),
        ("Stuffing shows through.", "gauge too loose — 30 stitches should measure 43 mm across. Crochet tighter "
         "or drop to a 3.0 mm hook."),
    ],
    colorways=[("Sage green", (122, 148, 108)), ("Dusty teal", (92, 142, 142)),
               ("Lilac", (172, 150, 190)), ("Charcoal", (82, 80, 80)),
               ("Blush pink", (222, 172, 172))],
    checks=[
        ["Head Rnds 1–11: 6 → 36 → 18 (left open, matches neck)", "✓ verified"],
        ["Body Rnds 1–13: 6 → 30 → 18 (left open)", "✓ verified"],
        ["Legs 9 sts: back 6 rnds = 26 mm, front 8 rnds = 34 mm", "✓ verified"],
        ["Tail Rnds 1–12: 4 → 10; 12 rnds = 52 mm = 5 cm", "✓ verified"],
        ["Wing rows 10 sts; Row 4 scallops consume 2+1+2+1+4 = 10", "✓ verified"],
        ["Spike strip = 10 ch-4 cone units (1 + 9 groups)", "✓ verified"],
        ["Sizes: head 47.3 mm + body 55.9 mm = 103 mm seated; wingspan 124 mm", "✓ verified"],
        ["Gauge probe: 30 sts ≈ 42.9 mm across when stuffed", "✓ verified"],
    ],
    safety_reminder="This pattern has not been tested to a toy-safety standard (ASTM F963 / EN 71) and uses "
                    "10 mm safety eyes. Finished items made for sale must be assessed by the seller against "
                    "local toy-safety laws; for young children, embroider the eyes.",
)

SHELBY = dict(
    slug="shelby", code="NS 09", file_stem="Shelby_the_Sea_Turtle_Bag_Charm_Crochet_Pattern_NS09",
    title="Shelby the Sea Turtle Bag Charm",
    subtitle="A pocket sea turtle on a keyring — the classic market impulse buy; under half an hour, a couple of grams of yarn, and the head and flippers are worked straight into the shell so there is almost nothing to sew",
    cover="assets/shelby_cover.png",
    badges=["30 minutes", "Easy", "~3 g of yarn"],
    size_line="About 3.7 cm (1.5 in) across the flippers, 3.2 cm long and 1.9 cm deep  •  DK cotton on a "
              "2.5 mm hook  •  shell and underside both finish at 24 stitches  •  bigger 5.7 cm version included",
    materials_line="DK cotton ~1 g shell + ~1 g body  •  2.5 mm hook  •  two 4 mm safety eyes or French knots  •  "
                   "one 25 mm keyring per turtle",
    terms_name="charms", tags="#ShelbyTheSeaTurtle",
    theme=dict(dark=(28, 92, 96), accent=(46, 122, 124), soft=(228, 240, 238),
               box_bg=(232, 242, 240), box_edge=(46, 122, 124)),
    safety=dict(title="SAFETY — EYES & KEYRING", lines=[
        ("Two 4 mm safety eyes are small parts. At this size French knots are the better fit (see section 4). "
         "Not tested to ASTM F963 or EN 71; for children under 3 use French knots.", True),
        "The keyring is the other hazard: attach it through TWO stitches at the back of the shell and knot "
        "the yarn inside — a charm that comes off a bag is a small part with a metal ring.",
    ]),
    materials=[
        ("Shell yarn:", "DK / light worsted (#3) cotton, about 1 g — sage, teal, mustard or rust."),
        ("Body yarn:", "DK cotton, about 1 g in contrast cream, sand or pale green."),
        ("Hook & eyes:", "2.5 mm (US C-2). Two 4 mm safety eyes or two black French knots."),
        ("Also:", "a pinch of polyfill (under 1 g), tapestry needle, one 25 mm keyring or lobster clasp per turtle."),
    ],
    gauge=[("About 3.5 mm per stitch and 3.2 mm per round.", True),
           "The whole charm is 203 stitches (~3 m of DK); 24 stitches = a 26.7 mm disc that sets the size."],
    abbrev="MR magic ring  •  sc single crochet  •  hdc half double crochet  •  inc increase  •  sl st slip stitch  •  "
           "BLO back loop only  •  FLO front loops only  •  FO fasten off.",
    construction=[
        ("Almost no sewing.", "the head and flippers are clusters worked straight into the underside's last "
         "round; only shell and underside are whip-stitched together."),
    ],
    techniques=[
        ("Magic ring & spiral", "start in a magic ring and work continuous spiral rounds with a marker — no "
         "joins, no chain 1 between rounds."),
        ("Back loop only (BLO)", "work into the far loop only; the unused loops form a raised ridge. On the "
         "shell that ridge is the rim — it makes the dome read as a shell rather than a bun."),
        ("Clusters into one stitch", "the trick of the head and flippers: work every stitch of the group into "
         "ONE stitch of the previous round so they share an anchor and fan into a bump. Each cluster consumes "
         "one stitch and produces as many as it contains — so a 24-stitch round produces 35."),
        ("Whip stitch & French knots", "join shell and underside with an even whip stitch so the seam does not "
         "pucker. Eyes: bring the needle up, wrap the floss once or twice around the needle, push back down "
         "close by and pull slowly."),
    ],
    pieces=[
        dict(title="1 · Shell — make 1",
             table=dict(headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", ""],
                              ["5", "BLO sc around", "24", "rim ridge"],
                              ["6", "sc in each st around", "24", "FO, 30 cm tail"]]),
             paras=["Before joining, embroider five or six shallow V shapes in a darker shade across the dome "
                    "— two minutes, and the difference between a turtle and a green blob."]),
        dict(title="2 · Underside — contrast flat disc with head & flippers worked in",
             table=dict(widths=[13, 118, 15, 32],
                        headers=["Rnd", "Instruction", "Sts", "Notes"],
                        rows=[["1", "6 sc in MR", "6", ""],
                              ["2", "inc in each st around", "12", ""],
                              ["3", "[sc, inc] x 6", "18", ""],
                              ["4", "[2 sc, inc] x 6", "24", "do NOT fasten off"],
                              ["5", "3 sc, (sc,hdc,hdc,sc) in next st, 4 sc, (sc,hdc,sc) in next, 3 sc, "
                                    "(sc,hdc,sc) in next, 4 sc, (sc,hdc,sc) in next, 3 sc, (sc,hdc,sc) in next, "
                                    "2 sc", "35", "head & flippers"]]),
             paras=["Rnd 5 consumes 3+1+4+1+3+1+4+1+3+1+2 = 24 stitches (closing the disc) and produces 35. The "
                    "first four-stitch bump is the HEAD; the four smaller bumps are flippers. Sl st in the next "
                    "stitch and fasten off with a 20 cm tail. The bumps land on stitches 4, 9, 13, 18 and 22, "
                    "placing the front flippers either side of the head."]),
        dict(title="4 · Face — read before you join",
             paras=["The head bump is only ~7–10 mm across, and a 4 mm safety-eye washer (6–7 mm) often will "
                    "not fit inside it. Use two small black FRENCH KNOTS, 2 stitches apart, low on the head "
                    "bump. If you do use safety eyes, place them 1 stitch apart and seat the washers BEFORE "
                    "joining — once the shell is on you cannot reach inside."]),
        dict(title="5 · Joining & keyring",
             paras=["Fix the eyes first. Hold the shell to the underside, wrong sides together, head pointing "
                    "away from the shell's tail. Whip-stitch with the shell's 30 cm tail, matching 24 to 24 — "
                    "NOT 24 to 35: the underside's outer round has 35 stitches but only 24 anchor positions "
                    "(19 plain + 5 clusters). Put one shell stitch against each anchor; at a bump, pass through "
                    "the BASE stitch the bump was worked into, not the bump itself. Add a small pinch of "
                    "stuffing about three-quarters of the way round (keep it flat — the shell holds only "
                    "~8 cm3). Weave in ends. Attach the keyring through TWO stitches at the back, opposite the "
                    "head, and knot inside."],
             boxes=[dict(lines=["The BLO rim ridge and embroidered V markings turn the dome into a shell."])]),
        dict(title="6 · Bigger Shelby (~5.7 cm across)",
             paras=["Shell: R1: 6 sc in MR (6). R2: inc x6 (12). R3: [sc, inc] x6 (18). R4: [2 sc, inc] x6 (24). "
                    "R5: [3 sc, inc] x6 (30). R6: [4 sc, inc] x6 (36). R7: [5 sc, inc] x6 (42). R8: BLO sc "
                    "around (42). R9: sc around (42).",
                    "Underside: R1–R7 the same to 42, do not fasten off. Rnd 8: 7 sc, (sc,hdc,hdc,sc) in next, "
                    "8 sc, (sc,hdc,sc) in next, 7 sc, (sc,hdc,sc) in next, 8 sc, (sc,hdc,sc) in next, 7 sc, "
                    "(sc,hdc,sc) in next = 53, consuming 42 anchors. Join 42 to 42 by the same rule. Allow "
                    "45–50 minutes and ~4 g."]),
    ],
    assembly=dict(
        title="Finishing touches",
        bullets=[
            ("Shell markings:", "embroider 5–6 shallow Vs on the dome before joining."),
            ("Keyring:", "through two back stitches, knotted inside — the strongest anchor for a bag charm."),
            ("Stuffing:", "a pinch only; the charm should stay flat against a bag."),
        ],
        listing=[("Sell as:", "bag charm / keyring — a market-stall impulse buy at a pocket price."),
                 ("Care:", "spot clean; cotton DK is machine washable in a mesh bag, but the keyring hardware "
                  "prefers hand washing.")]),
    troubleshooting=[
        ("Flippers uneven.", "count the plain runs between bumps: 3, 4, 3, 4, 3, then 2 at the end."),
        ("Keyring pulls out / too fat to hang.", "attach through two stitches and knot inside. Use less "
         "stuffing so the charm stays flat against a bag."),
        ("Shell and base won't pair.", "count anchor positions (19 plain + 5 bumps = 24), not the 35 outer "
         "stitches."),
    ],
    colorways=[("Sage", (150, 170, 132)), ("Teal", (72, 142, 138)),
               ("Mustard", (208, 162, 52)), ("Rust", (176, 96, 52))],
    checks=[
        ["Shell 6 → 24 with BLO rim; underside disc 6 → 24", "✓ verified"],
        ["Cluster round: consumes 3+1+4+1+3+1+4+1+3+1+2 = 24 → produces 35", "✓ verified"],
        ["Bump positions land on stitches 4, 9, 13, 18, 22", "✓ verified"],
        ["Joining 24-to-24: 19 plain + 5 cluster anchors = 24", "✓ verified"],
        ["Whole charm = 108 + 95 = 203 stitches (~3 m of DK)", "✓ verified"],
        ["24 sts x 3.5 mm = 26.7 mm disc; big disc 42 sts = 46.8 mm ~ 5.7 cm with bumps", "✓ verified"],
        ["Big cluster round: consumes 42 → produces 53", "✓ verified"],
    ],
    safety_reminder="Shelby uses 4 mm safety eyes (French knots recommended at this size) and a metal keyring. "
                    "Sold as a keyring/bag charm; not tested to ASTM F963 or EN 71. For children under 3 use "
                    "French knots, attach the ring through two stitches and knot inside.",
)
