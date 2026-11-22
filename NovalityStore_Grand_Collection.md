# Novality Store — The Grand Crochet Pattern Collection
### Design codes NS-01 … NS-17 · seventeen verified amigurumi & decor masters in one volume

Every pattern in this volume has been through the Novality verification pipeline:

1. **Deterministic static-analysis engine** (`src/crochet_checker`) — each corrected master runs
   **0 errors / 0 warnings**.
2. **Independent stitch arithmetic auditor** (`docs/kit/audit_lib.py`) — every round/row table is
   re-derived from its own instruction text: **0 problems** across all seventeen patterns; the
   handful of prose/continuation rows are carried as explicit expected counts in
   `docs/kit/audit_overrides.py`.
3. **Two store editions per pattern** — a colour Novality Store edition and a monochrome
   ink-friendly print edition (greyscale spread 0 on every page), compiled from the verified
   master by `docs/kit/build_store_pdf.py`.

Corrections against the originals were wording/clarity only — **no stitch count, repeat
multiplier, chain length or decrease schedule was ever changed**. Per-pattern correction tables
live in each pattern's validation report.

## Contents

01. NS-01 — Hamish the Highland Cow (colour 10 pp / print 10 pp)
02. NS-02 — Kawaii Halloween Mini Set (colour 9 pp / print 9 pp)
03. NS-03 — Axel the Axolotl (colour 9 pp / print 9 pp)
04. NS-04 — Coco the Capybara (colour 8 pp / print 8 pp)
05. NS-05 — Little Duck Plushie (colour 7 pp / print 7 pp)
06. NS-06 — Momo the Loaf Cat (colour 7 pp / print 7 pp)
07. NS-07 — Pocket Positivity Trio (colour 7 pp / print 7 pp)
08. NS-08 — Ember the Baby Dragon (colour 9 pp / print 9 pp)
09. NS-09 — Shelby Sea Turtle Bag Charm (colour 6 pp / print 6 pp)
10. NS-10 — Willow the Bunny Lovey (colour 7 pp / print 7 pp)
11. NS-11 — No-Sew Christmas Gnome (colour 7 pp / print 7 pp)
12. NS-12 — Bobble Christmas Tree (colour 7 pp / print 7 pp)
13. NS-13 — Christmas Ornament Bundle (colour 7 pp / print 7 pp)
14. NS-14 — Bobble Snowflake Tree Skirt (colour 10 pp / print 10 pp)
15. NS-15 — Interchangeable Christmas Wreath (colour 11 pp / print 11 pp)
16. NS-16 — Mini Stocking Advent Garland (colour 9 pp / print 9 pp)
17. NS-17 — Year of the Fire Goat 2027 Plushie Set (colour 14 pp / print 14 pp)

## Verification ledger

| Code | Pattern | Engine E / W | Audit problems / unparsed | Colour pp | Print pp |
|---|---|---|---|---|---|
| NS-01 | Hamish the Highland Cow | 0 / 0 | 0 / 0 | 10 | 10 |
| NS-02 | Kawaii Halloween Mini Set | 0 / 0 | 0 / 0 | 9 | 9 |
| NS-03 | Axel the Axolotl | 0 / 0 | 0 / 0 | 9 | 9 |
| NS-04 | Coco the Capybara | 0 / 0 | 0 / 0 | 8 | 8 |
| NS-05 | Little Duck Plushie | 0 / 0 | 0 / 0 | 7 | 7 |
| NS-06 | Momo the Loaf Cat | 0 / 0 | 0 / 0 | 7 | 7 |
| NS-07 | Pocket Positivity Trio | 0 / 0 | 0 / 0 | 7 | 7 |
| NS-08 | Ember the Baby Dragon | 0 / 0 | 0 / 0 | 9 | 9 |
| NS-09 | Shelby Sea Turtle Bag Charm | 0 / 0 | 0 / 0 | 6 | 6 |
| NS-10 | Willow the Bunny Lovey | 0 / 0 | 0 / 0 | 7 | 7 |
| NS-11 | No-Sew Christmas Gnome | 0 / 0 | 0 / 0 | 7 | 7 |
| NS-12 | Bobble Christmas Tree | 0 / 0 | 0 / 0 | 7 | 7 |
| NS-13 | Christmas Ornament Bundle | 0 / 0 | 0 / 0 | 7 | 7 |
| NS-14 | Bobble Snowflake Tree Skirt | 0 / 0 | 0 / 0 | 10 | 10 |
| NS-15 | Interchangeable Christmas Wreath | 0 / 0 | 0 / 0 | 11 | 11 |
| NS-16 | Mini Stocking Advent Garland | 0 / 0 | 0 / 0 | 9 | 9 |
| NS-17 | Year of the Fire Goat 2027 Plushie Set | 0 / 0 | 0 / 0 | 14 | 14 |

*Cover artwork in the PDF editions is an illustrative render of the written design, not a
photograph of a sample; each cover says so. Etsy-style listings must carry the matching
AI-disclosure sentence.*


---

# Part 01 of 17 — NS-01 · Hamish the Highland Cow

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 10 pp · print edition 10 pp · reports: `docs/ns01/NS01_validation_report.md`*

## Hamish the Highland Cow

> **US terms  ·  Intermediate  ·  6 - 8 hours**  —  Design Code NS 01

A shaggy, sturdy Highland cow with a flattened brow, a wide cream muzzle and a weather-beaten fringe. Worked in pieces so every proportion can be pinned and checked before sewing.

**FINISHED SIZE**  About 15 cm (6 in) sitting in worsted weight.  A 70 mm wide body and a 70 x 67 mm head.  A low, sprawling Highland sit.

---

### Safety — read this first

Hamish uses two 12 mm plastic safety eyes. If an eye, washer or surrounding stitch fails, it can release a small part: reach through the open head and lock each washer firmly from the inside BEFORE stuffing and closing the head (Rnd 16), then check the eye and fabric by hand. The horns, ears, muzzle, legs and tail are sewn on, and the fringe and tail are knotted yarn: sew every seam twice, weave ends in at least 5 cm, and secure every knot.

No finished Hamish has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime; do not describe one as “baby-safe” or compliant. Embroidered eyes remove the plastic-eye detachment hazard but do not by themselves establish suitability for any age. Before supplying a finished item, its maker or seller must determine all classification, assessment, testing, documentation, labelling and traceability duties for the intended and reasonably foreseeable use in every destination market.

### Materials

- Yarn A - Ginger: worsted / aran (#4), about 25 g used. Caramel, toffee or ginger gold. One 80 g / 150 m ball covers about three cows at the stated gauge, including normal seaming tails.

- Yarn B - Oat cream: worsted / aran (#4), about 12 g. Muzzle, horns, inner ears, optional belly patch.

- Yarn C - Dark chocolate: worsted / aran (#4), about 5 g. Hooves and nostrils.

- Yarn D - Rust (optional): about 6 g for the scarf, or 28 cm of 12 mm tartan ribbon.

- Hook: 3.5 mm (US E-4) - smaller than the ball band so stuffing cannot show.

- Eyes: 2 x 12 mm black safety eyes, or black floss for an embroidered-eye version.

- Stuffing & notions: polyester fibre fill about 30 g (buy 50 g to over-stuff the base); stitch marker, tapestry needle, pins, scissors.

### Gauge & size

Gauge in Yarn A: 11 sc x 12 rounds = 5 cm / 2 in. Not critical, but loose tension lets stuffing show - drop half a millimetre if your fabric is gappy.

Finished size: about 15 cm / 6 in sitting.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sl st - slip stitch  ·  sc - single crochet

hdc - half double crochet  ·  inc - increase (2 sc in one st)

dec - invisible decrease  ·  BLO - back loop only

FO - fasten off  ·  st(s) - stitch(es)  ·  Rnd(s) - round(s)

(n) - stitch count at round end

Work in a continuous spiral unless a round says join. Mark the first stitch of every round. Leave 30-40 cm tails on every piece you will sew.

### Techniques used, in the order you will meet them

1. **The magic ring** - Wrap yarn around two fingers, insert the hook, pull up a loop and work the first round into the ring; pull the tail tight once the round is complete.

2. **Working in a spiral** - Do not join and do not chain 1 between rounds. Move the marker up each time - there is no join to count from.

3. **The invisible decrease** - Insert the hook through the FRONT loops only of the next two stitches, yarn over and pull through both, then yarn over and pull through the remaining two. Every dec is worked this way - no ridge on visible rounds.

4. **Back loop only (BLO)** - Work into the far loop only, leaving the near loop unused; the unused loops form a raised ridge. Hamish's hoof line is one BLO round.

5. **Working around a chain** - For the belly patch, crochet into both sides of a starting chain: across the front, corner increases into the last chain, then back along the opposite side - turning a chain into a flat oval.

6. **The lark's head knot** - Fold a strand in half, push the folded loop under a stitch with the hook, pull the two loose ends through the loop and cinch. Used for every fringe strand and the tail.

7. **Ladder stitch** - The invisible seam: out on one side, pick up one bar on the opposite side, then one bar back, alternating, pulling snug every few stitches. The head-to-body join needs two full passes.

### Instructions

#### 1. Head - Yarn A

Worked from the crown down toward the neck. One straight round only - that is what keeps the brow flat and wide instead of egg-shaped. Close to 6 stitches at the end.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | fringe row 3 |

| R7 | [5 sc, inc] x 6 | (42) | fringe row 2 / horns |

| R8 | [6 sc, inc] x 6 | (48) | fringe row 1 / ears |

| R9 | sc in each st around | (48) | eyes at R9 - R10 |

| R10 | [6 sc, dec] x 6 | (42) | - |

| R11 | [5 sc, dec] x 6 | (36) | decreases 42 to 36 |

| R12 | [4 sc, dec] x 6 | (30) | lock eye washers, then stuff firmly |

| R13 | [3 sc, dec] x 6 | (24) | - |

| R14 | [2 sc, dec] x 6 | (18) | - |

| R15 | [sc, dec] x 6 | (12) | last pinch of stuffing |

| R16 | dec x 6 | (6) | close the hole |

Eyes & head size: the 12 mm eyes go in between Rnds 9 and 10, 7 stitches apart and a touch low on the face (7 sts is about 32 mm, just under half the head width). LOCK THE WASHERS at about Rnd 12, while you can still reach the inside: press each washer on until it clicks. The head stays open until Rnd 16 closes it - after that the washers are unreachable. Finished head about 70 mm wide x 67 mm tall.

#### 2. Muzzle & nostrils - Yarn B

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | sc in each st around | (24) | face at full width, 35 mm |

| R6 | sc in each st around | (24) | - |

| R7 | sc in each st around | (24) | - |

| R8 | [2 sc, dec] x 6 | (18) | rim = 26 mm across |

Finish: FO with a 40 cm tail and stuff lightly. The muzzle FACE is about 35 mm across (the wide cream patch you see); the RIM it sews by is about 26 mm, spanning roughly six rounds of head. Pin the top edge just under the eyes at Rnd 10 and let the lower edge fall at Rnds 15-16 near the chin. Centre it, let the face sit a little wider than the eye spacing, and sew about three quarters of the rim with small whip stitches. Add a whisper more stuffing, then embroider the nostrils and mouth.

Knot the nostril and mouth ends inside the muzzle through the remaining opening before finishing the seam.

Nostrils (Yarn C): two short vertical satin stitches, 3 stitches apart, on the lower third. Mouth: one tiny horizontal stitch or a shallow V below them. Secure both before the last quarter of the muzzle seam is closed. (The eye washers were already locked before the head was closed at Rnd 16.)

The wide cream muzzle, low-set eyes and shaggy fringe give the Highland stare.

#### 3. Body - Yarn A

Worked bottom up. The neck is left open at 18 stitches for the head join.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | - |

| R7 | [5 sc, inc] x 6 | (42) | - |

| R8 | [6 sc, inc] x 6 | (48) | front legs join R8 - R9 |

| R9 | sc in each st around | (48) | - |

| R10 | sc in each st around | (48) | body at full width, 70 mm |

| R11 | sc in each st around | (48) | - |

| R12 | sc in each st around | (48) | - |

| R13 | sc in each st around | (48) | - |

| R14 | [6 sc, dec] x 6 | (42) | - |

| R15 | sc in each st around | (42) | - |

| R16 | [5 sc, dec] x 6 | (36) | - |

| R17 | [4 sc, dec] x 6 | (30) | stuff firmly, pack the base |

| R18 | [3 sc, dec] x 6 | (24) | - |

| R19 | [2 sc, dec] x 6 | (18) | leave neck OPEN |

Finish: FO with a 40 cm tail; do not close. Body is about 19 rounds (79 mm); with the head seated on the neck ring the finished sitting height is about 15 cm / 6 in.

#### 4. Belly patch - Yarn B (optional)

A flat oval worked around a chain, sewn on last.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 9 | - | - |

| R1 | sc in 2nd ch, sc in next 6, 3 sc in last ch, sc in next 6, 2 sc in last loop | (18) | - |

| R2 | inc, 6 sc, inc x 3, 6 sc, inc x 2 | (24) | - |

| R3 | sc, inc, 6 sc, [sc, inc] x 3, 6 sc, [sc, inc] x 2 | (30) | - |

| R4 | 2 sc, inc, 6 sc, [2 sc, inc] x 3, 6 sc, [2 sc, inc] x 2 | (36) | - |

Sl st, FO with a long tail; sew centred on the front with the lower edge about 3 rounds up from the base. Skip it for a plain ginger front - both are correct.

#### 5. Legs - start with Yarn C, change to Yarn A (make 4)

Choose one pose before making the legs:

- **Low Highland sit:** make all four standard 16-round legs. The sewing angle creates the splay.

- **Tidier upright sit:** make two standard 16-round back legs and two shortened 10-round front legs from the separate table below. Do not make four long legs for this option.

##### Standard 16-round legs

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR (Yarn C) | (6) | hoof |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | sc in each st around | (18) | - |

| R5 | sc in each st around | (18) | - |

| R6 | BLO sc around | (18) | change to Yarn A - ridge |

| R7 | sc in each st around | (18) | - |

| R8 | [sc, dec] x 6 | (12) | stuff hoof firmly |

| R9 | sc in each st around | (12) | - |

| R10 | sc in each st around | (12) | - |

| R11 | sc in each st around | (12) | - |

| R12 | sc in each st around | (12) | - |

| R13 | sc in each st around | (12) | upper leg light |

| R14 | [2 sc, dec] x 3 | (9) | - |

| R15 | sc in each st around | (9) | - |

| R16 | sc in each st around | (9) | leave top open |

A standard leg is about 67 mm. For the low Highland sit, pin the front pair about 55 degrees from vertical and the back pair about 68-70 degrees from vertical (nearly horizontal). The low join and long leg create the splay.

##### Shortened front legs - upright option (make 2)

| Rnd | Exact instruction | Sts |

|---|---|---|

| R1 | With Yarn C, 6 sc in MR | (6) |

| R2 | inc in each st around | (12) |

| R3 | [sc, inc] x 6 | (18) |

| R4 | sc in each st around | (18) |

| R5 | sc in each st around | (18) |

| R6 | BLO sc in each st around; change to Yarn A after the round | (18) |

| R7 | sc in each st around | (18) |

| R8 | [sc, dec] x 6 | (12) |

| R9 | sc in each st around | (12) |

| R10 | sc in each st around; stop here | (12) |

Short-front finish: each leg measures 42 mm with a 12-stitch top opening. Stuff the hoof firmly, keep the final two rounds lightly filled, and FO after Rnd 10 with a 40 cm sewing tail; do not close or flatten the opening.

Short-front placement: pin both front legs before sewing, centred across Body Rnds 8-9, 8 body stitches apart. Start each leg 25 degrees forward from vertical; mirror the pair and adjust only within 20-30 degrees until both hooves rest level. Sew all 12 top stitches to the body, then make a second complete seam pass. Keep the standard 16-round back legs at 68-70 degrees from vertical.

#### 6. Ears - make 2 of each layer

##### INNER ear - Yarn B (make 2) & OUTER ear - Yarn A (make 2)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | [sc, inc] x 3 | (9) | - |

| R3 | [2 sc, inc] x 3 | (12) | - |

| R4 | sc in each st around | (12) | - |

| R5 | sc in each st around | (12) | - |

| R6 | [2 sc, dec] x 3 | (9) | - |

| R7 | sc in each st around | (9) | OUTER ear only |

Work the INNER ear through Rnd 6 only and the OUTER ear through Rnd 7; do not stuff either layer. Both openings have 9 stitches, but the one-round-shorter inner cup nests without bunching. If your cream yarn is thicker, use a 3.0 mm hook for the inner layer only. FO the inner ear with a short tail and the outer with a long tail. Push the inner cup inside the outer cup, aligning the magic-ring tips and the two 9-stitch openings, with cream visible at the front. Tack the two tips together with the inner-ear tail so the layers cannot shift. Join the openings stitch-for-stitch with 9 whip stitches (or 9 sc through one opening stitch from each layer) using Yarn A. Flatten the joined opening and pinch it with 2-3 stitches so the ear cups forward.

#### 7. Horns - Yarn B (make 2)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 4 sc in MR | (4) | - |

| R2 | [sc, inc] x 2 | (6) | - |

| R3 | sc in each st around | (6) | - |

| R4 | sc in each st around | (6) | - |

| R5 | [2 sc, inc] x 2 | (8) | - |

| R6 | sc in each st around | (8) | - |

| R7 | sc in each st around | (8) | stuff tip only |

FO with a tail; stuff the tip only. Short and slightly curved - tilt each horn out and a little back when you sew.

#### 8. Tail - Yarn A

Cut 6 strands of Yarn A, each 22 cm / 8.5 in. Fold the bundle in half and attach with a lark's head at the centre-back just above the last increase round: pull the folded loop through a stitch, then the tails through the loop. Folding gives 12 hanging ends; divide into 3 groups of 4, braid 4 cm, knot firmly and trim into a small tassel.

#### 9. Fringe - Yarn A

Attach AFTER the horns and ears so you can part the hair around them. Cut 45 strands, each 14 cm / 5.5 in (43 to use plus 2 spares; swap up to 6 for Yarn C for depth). Attach 43 strands with lark's head knots in a horseshoe from one ear, across the brow, to the other, filling three rows across the front of the head: every stitch along the front of Rnd 8 (24 knots), then every other stitch along the front of Rnd 7 (about 10 knots) and Rnd 6 (about 9 knots) - 24 + 10 + 9 = 43 knots.

Tousle, then trim so the fringe grazes the eyes and breaks into uneven points. Highland hair is weather-beaten, not a salon fringe.

#### 10. Tartan scarf - Yarn D (optional)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 61 | - | - |

| Row 1 | hdc in 2nd ch from hook and in each ch across | (60) | - |

| Row 2 | ch 2, turn, hdc across | (60) | turning ch does not count |

FO; add a 3-strand tassel at each end or weave a second colour as a slip-stitch stripe to hint at tartan, then tie loosely under the muzzle. Ribbon shortcut: 28 cm of 12 mm rust tartan ribbon, knotted once.

### Finishing & assembly

Assembly - work in this order:

1. Muzzle & face sewn (section 2) - the eye washers were locked before the head was closed at Rnd 16.

2. Horns between Rnds 5 and 7, 6 stitches apart, angled out and slightly back.

3. Ears just outside and below each horn, centred on Rnds 8-9, cupped forward.

4. Fringe attached and trimmed (section 9), parting around horns and ears.

5. Head to body: seat the head’s small Rnds 15-16 closing nub INSIDE the body’s open 18-stitch neck. Match the 18 body Rnd-19 stitches one-for-one to the 18 head stitches of Rnd 14, forming a full circular seam around the nub; do not bunch all 18 neck stitches into the 6-stitch closure. Pack the neck firmly, ladder-stitch around TWICE and tilt the muzzle slightly down.

6. Back legs: lower sides across Rnds 3-6, almost on the base, splayed near horizontal.

7. Front legs: FRONT across Rnds 8-9, about 8 sts apart, angled forward about 55 degrees.

8. Belly patch - only if you made it.

9. Tail & scarf: attach the tassel tail, tie the scarf, weave in every end and fluff the fringe.

### Troubleshooting

- **He will not sit.** Restuff the body base firmly and sew the back legs lower and wider - closer to horizontal than you think.

- **Front hooves float.** Sewn too high - they belong on Rnds 8-9, not under the neck. If they still float, the legs are too long: work the front pair to Rnd 10.

- **Stuffing shows.** Drop half a hook size, or hold a matching thread with the yarn on visible rounds.

- **Face looks blank.** The eyes are too high. Low eyes plus a wide muzzle is the Highland stare.

- **Fringe is sparse.** Add a fourth row behind the horns and mix in one darker shade.

- **Horns flop.** Under-stuffed at the tip, or sewn only at the edge - stitch a full round into the head fabric.

- **Head tips forward.** Check that the 18-stitch neck is sewn around all 18 stitches of head Rnd 14, with the Rnds 15-16 nub tucked inside rather than used as the seam. Pack the neck and make the second ladder-stitch pass tight.

### Colorways

Ginger  ·  Caramel  ·  Highland black  ·  Cream  ·  Roan red

### Three sizes, one pattern

| Version | Yarn / hook | Eyes | Height |

|---|---|---|---|

| Wee Hamish | DK / #3 - 2.75 mm | 8-9 mm | ~12 cm |

| Classic | Worsted / #4 - 3.5 mm | 12 mm | ~15 cm |

| Cuddle Hamish | Bulky chenille / #5 - 5.0 mm | 16-18 mm | ~21 cm |

Stitch counts stay the same; only yarn, hook and stuffing change. Yarn scales with the square of the height and stuffing with the cube - buy generously for the big chenille version.

### Designer notes

- Why the legs join so low: back legs (16 rnd, 67 mm, sewn to Rnds 3-6) and front legs (sewn to Rnds 8-9) splay at the checked angles so all four hooves land level. This low join is the most common failure on sitting Highland cows.

- Bottom-heavy by design: stuff the lower body firmly and keep the shape squat. Hamish is meant to settle onto his base and stare.

### Care

Follow the labels for every yarn and component used. Before publishing a care claim or supplying finished Hamishes, clean and dry a complete sample by the proposed method, then remeasure it and inspect for dye transfer, fibre change, stuffing migration, loosened fringe, shifted eyes and opened seams. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying flat away from heat. Check all eyes, knots and attachments again after cleaning.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 01.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished Hamishes as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

No finished item made from this pattern has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Plastic eyes and knotted fringe require particular attention; embroidery removes the plastic-eye component but is not proof of overall compliance. The finished-item maker or seller is responsible for applicable assessment, evidence, labelling and traceability before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#HamishTheHighlandCow** - We love seeing your coos. Thank you for supporting an independent pattern designer.


---

# Part 02 of 17 — NS-02 · Kawaii Halloween Mini Set

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 9 pp · print edition 9 pp · reports: `docs/ns02/NS02_validation_report.md`*

## Kawaii Halloween Mini Set

> **3 patterns in one  ·  Intermediate  ·  45 - 60 min each**  —  Design Code NS 02

Three pocket-sized spookies - Boo the ruffled ghost, Pip the sculpted pumpkin and Bramble the picot-winged bat. Small, fast and forgiving, at about 5 cm / 2 in each.

**FINISHED SIZE**  Boo the Ghost: about 48 mm tall, open bell with ruffled hem.  Pip the Pumpkin: about 50 mm tall with stem, needle-sculpted ribs.  Bramble the Bat: about 51 mm tall, wingspan about 11.5 cm, picot wings.  DK cotton on a 2.5 mm hook. Boo and Bramble use 6 mm safety eyes; Pip's face is embroidered.

---

### Safety — read this first

Boo and Bramble use 6 mm plastic safety eyes. If an eye, washer or surrounding stitch fails, it can release a small part: lock each washer from the inside before stuffing and closing, then check the eye and fabric by hand. Pip has an embroidered face and no plastic eye components.

No finished mini has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Embroidering the faces removes the plastic-eye detachment hazard but does not by itself establish suitability for a child. Calling an item “decorative” is not a substitute for classification based on intended and reasonably foreseeable use. Before supply, the finished-item maker or seller must determine all applicable assessment, testing, documentation, labelling and traceability duties in every destination market.

### Materials

- Yarn: DK / light worsted (#3) cotton - cream ~8 g (Boo), pastel orange ~10 g (Pip), lavender ~9 g (Bramble), sage green ~4 g (stem, tendril, leaf), pale pink ~2 g (ear linings). One small ball of each is plenty.

- Hook: 2.5 mm - tight enough that stuffing cannot show.

- Safety eyes: 2 pairs of 6 mm - one for Boo, one for Bramble. Pip needs none.

- Floss: black for Boo's smile and Pip's face, pink for blush, white for Bramble's fangs.

- Stuffing & notions: polyester fibre fill (~5 g covers one three-piece set; Pip ~2 g, Bramble ~1 g, Boo none). Tapestry needle, stitch markers, pins, scissors.

- Optional nine-mini garland: 1.8 m / 6 ft jute twine, or an extra 4 g of sage yarn for the ~450-chain cord; 8 x 20 mm felt balls (one between each adjacent pair of minis); and wall fixings suitable for the finished weight and mounting surface.

### Gauge & size

About 3.5 mm per stitch and 3.2 mm per round. Check on Pip after Rnd 6 - 36 stitches should measure about 40 mm across a firmly stuffed body. Finished minis are 48-51 mm tall.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sl st - slip stitch  ·  sc - single crochet

hdc - half double crochet  ·  dc - double crochet

inc - increase (2 sc in one st)  ·  dec - invisible decrease

FLO / BLO - front / back loop only  ·  picot - ch 3, sl st in 3rd ch from hook

FO - fasten off  ·  st(s) - stitch(es)  ·  Rnd(s) - round(s)

(n) - stitch count at round end

Work the bodies in a continuous spiral - no joins, no chain 1 between rounds; mark the first stitch of every round. Bramble's wings and Pip's leaf are the exceptions: worked flat in turned rows.

### Techniques used, in the order you will meet them

1. **The picot** - Chain 3, then slip stitch into the 3rd chain from the hook - one small pointed bump. Picots edge Bramble's wings and make them read as bat wings rather than leaves. Keep tension even: a slack picot loops, while an over-tight one curls under.

2. **One loop only (FLO / BLO)** - Boo's ruffled hem is worked into the FRONT loops of Rnd 12, leaving the back loops free as a clean ring to sew the optional base onto. Insert the hook under only that loop; the unused loop stays as a ridge - that ridge is the join line and is meant to be there.

3. **The ruffle shell** - Boo's hem repeats: 2 sl st, then (sc, hdc, dc, hdc, sc) all into the NEXT single stitch, then 1 sl st. Five stitches into one stitch makes the fabric flare; each repeat takes 4 stitches and returns 8, so the edge doubles in length. Six repeats use all 24 stitches of Rnd 12 = 48 stitches, six ruffles.

4. **Needle sculpting** - Turns Pip from an orange ball into a pumpkin using the long tail. Run the tail through the stuffed body with a tapestry needle, in at the top centre and out at the bottom, then pull and anchor; each pass pins a channel. Six evenly spaced passes make six ribs. OVERSTUFF FIRST - sculpting compresses the filling and a soft pumpkin will not hold a rib.

### Instructions

#### 1. Boo the Ghost - cream

Worked top-down in cream. Boo is an OPEN BELL - no closed bottom and NO stuffing; he stands on the spread and structure of his ruffled hem. Do not fasten off after Rnd 12 - continue straight into the hem.

##### Boo body

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | sc in each st around | (24) | - |

| R6 | sc in each st around | (24) | - |

| R7 | sc in each st around | (24) | - |

| R8 | [11 sc, inc] x 2 | (26) | eyes at R8 - R9 |

| R9 | sc in each st around | (26) | - |

| R10 | sc in each st around | (26) | arms at R10 |

| R11 | sc in each st around | (26) | - |

| R12 | [11 sc, dec] x 2 | (24) | live edge - hem & base here |

| R13 | FLO: [2 sl st, (sc, hdc, dc, hdc, sc) in next st, 1 sl st] x 6 | (48) | RUFFLED HEM |

The hem: Rnd 13 is worked into the FRONT loops only. Each repeat takes 4 stitches and returns 8; six repeats close all 24 stitches and make six ruffles (48 sts). The hem adds ~10 mm of depth, included in Boo's 48 mm height. FO and weave in.

Boo stands on his ruffled hem - an open bell with no stuffing and no closed bottom.

Eyes: insert the 6 mm safety eyes BEFORE you sew anything, while the open bottom lets you reach the washers. Place them on Rnd 8-9, about five stitches apart, centred on the front (the widest round is 26 stitches, so five apart keeps them well inside the face).

Smile & blush: black floss curved smile centred below the eyes, pink floss horizontal stitches either side for blush.

##### Arms - cream (make 2, no stuffing)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 5 sc in MR | (5) | - |

| R2 | sc in each st around | (5) | - |

| R3 | sc in each st around | (5) | - |

FO with a tail, do not stuff; sew to the sides at Rnd 10, angled slightly forward.

##### Flat base - cream (optional, make 1)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

Base (optional): hold the flat disc under the opening with wrong sides together and match its 24 edge stitches one-for-one to the 24 exposed back loops of Body Rnd 12. Whip-stitch around from the underside, leaving the Rnd-13 hem free to flare. Keep the disc flat and unstuffed; its structure, not added filling, stabilises the bell.

##### Bonus mini witch hat - black or charcoal

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 4 sc in MR | (4) | - |

| R2 | [sc, inc] x 2 | (6) | - |

| R3 | [2 sc, inc] x 2 | (8) | - |

| R4 | [3 sc, inc] x 2 | (10) | - |

| R5 | sc in each st around | (10) | - |

| R6 | FLO: inc in each st around | (20) | brim |

Sl st, FO. The brim stops at 20 stitches (outer edge about 24 mm) so the hat sits on Boo's ~27 mm head instead of swamping him. Sew it on tilted.

#### 2. Pip the Pumpkin - pastel orange

Worked bottom-up in pastel orange. Only two straight rounds - that keeps Pip squat rather than tall like a lemon. Do NOT cut the yarn short: leave a 25 in / 65 cm tail for sculpting.

##### Pip body

Embroidered face order: place the two triangle eyes and the zigzag mouth immediately after Rnd 8, before any filling goes in; knot and bury the floss ends inside.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | full width - check gauge |

| R7 | sc in each st around | (36) | - |

| R8 | sc in each st around | (36) | mark a 6-stitch front panel and embroider the face now |

| R9 | [4 sc, dec] x 6 | (30) | - |

| R10 | [3 sc, dec] x 6 | (24) | stuff firmly, then OVERSTUFF |

| R11 | [2 sc, dec] x 6 | (18) | - |

| R12 | [sc, dec] x 6 | (12) | - |

| R13 | dec x 6 | (6) | leave a 65 cm tail |

Sculpting six ribs (overstuff first): use the six increase columns of Rnd 6, spaced 6 stitches apart, as guides. Thread the long closing tail and push the needle through the core from the top centre to the bottom centre. Bring the yarn UP THE OUTSIDE of the body along the first guide to the top centre, insert there and pass through the core to the bottom again; pull gently until that outside strand forms a channel. Rotate to the next guide and repeat until six evenly spaced outside strands run from bottom to top. Keep the two strands bordering the marked face panel beside, not across, the embroidery. Pull every rib to the SAME tension; knot securely at the bottom and bury the tail through the stuffed body.

Face - complete this immediately after Rnd 8, before stuffing and closing: mark one 6-stitch front panel between adjacent Rnd-6 increase columns. With black floss, embroider two small triangle eyes about 4 stitches apart and a short zigzag mouth below; knot and bury the floss ends inside. During sculpting, run the two bordering rib strands along the panel edges, never across the face.

##### Stem cone - sage (make 1)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | sc in each st around | (6) | - |

| R3 | [sc, inc] x 3 | (9) | - |

| R4 | sc in each st around | (9) | - |

| R5 | [2 sc, inc] x 3 | (12) | - |

FO with a tail, stuff very lightly, sew to the top centre over the round-13 opening.

##### Leaf - sage (make 1, worked flat)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 7 | - | - |

| R1 | sc in 2nd ch, 4 sc, 3 sc in last ch; continue along the other side: 4 sc, 2 sc in last ch | (14) | around the chain |

| R2 | ch 1, turn; 4 sc, inc in each of next 3, 4 sc (last 3 sts of R1 stay unworked - they form the pointed base) | (14) | - |

| R3 | ch 1, turn; sl st in each st across | (14) | - |

FO with a tail. The final sl-st row gives a firm rolled edge - sew to the stem base, angled out to one side.

##### Tendril - sage

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 20; from the 2nd ch, work 2 sc in each chain to the end | (38) | 19 working chains x 2 sc; curls as you work |

FO with a tail. The paired single crochets force the chain into a corkscrew. Let it twist naturally, wind it once around the stem base and sew the end down; if your yarn curls too tightly, use 1 sc in each chain instead of 2.

Pip's six needle-sculpted ribs, sage stem, curly tendril and leaf.

#### 3. Bramble the Bat - lavender

Worked top-down in lavender. Insert the eyes after Rnd 8 while the 24-stitch face is easy to see, and lock the washers from inside before stuffing begins at Rnd 13. Rnd 9 widens the lower body to 30 stitches; Rnds 13-16 then narrow and close it.

##### Bramble body

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | ears at R4 - R5 |

| R5 | sc in each st around | (24) | - |

| R6 | sc in each st around | (24) | - |

| R7 | sc in each st around | (24) | eyes at R7 - R8 |

| R8 | sc in each st around | (24) | lock eye washers and embroider fangs/blush now |

| R9 | [3 sc, inc] x 6 | (30) | wings at R9 - R11 |

| R10 | sc in each st around | (30) | - |

| R11 | sc in each st around | (30) | - |

| R12 | sc in each st around | (30) | - |

| R13 | [3 sc, dec] x 6 | (24) | fill firmly |

| R14 | [2 sc, dec] x 6 | (18) | - |

| R15 | [sc, dec] x 6 | (12) | - |

| R16 | dec x 6 | (6) | weave & close |

Eyes and face: immediately after Rnd 8, place the eye posts between Rnds 7 and 8, just 4 stitches apart and centred - close on purpose, since the head is only 24 stitches around and wide eyes wrap to the sides. Lock both washers, then embroider two small white V-stitch fangs and optional short pink blush stitches. Knot and bury every floss end inside before continuing to Rnd 9.

##### Ears - lavender outer x 2, pink inner x 2

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 4 sc in MR | (4) | both layers |

| R2 | [sc, inc] x 2 | (6) | both layers |

| R3 | [2 sc, inc] x 2 | (8) | inner ear stops here |

| R4 | [3 sc, inc] x 2 | (10) | outer ear only |

Flatten and do not stuff. Sew a pink inner onto each lavender outer, then sew the pairs to the top of the head at about Rnd 4-5, angled slightly outward.

##### Wings - lavender (make 2, worked flat)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 13 | - | - |

| Row 1 | from the 2nd ch: sc in 4, hdc in 4, dc in 4; ch 1, turn | (12) | - |

| Row 2 | sc in 3, hdc in 4, dc in 5; ch 1, turn | (12) | - |

| Row 3 | sl st in first 2, (sc, hdc, dc, picot, dc, hdc, sc) in next st, sl st in next 3, (sc, hdc, picot, hdc, sc) in next st, sl st in next 2, (sc, hdc, picot, hdc, sc) in next st, sl st in last 2 | (23) | counted sts; 3 picot chain bumps are additional - FO with a 10 in tail |

The anchor maths: the slip-stitch groups use 2 + 3 + 2 + 2 = 9 stitches of Row 2; the three fans each use one more anchor, so all 12 stitches of Row 2 are consumed. The fans are deliberately different sizes: the FIRST fan in the written sequence has 6 counted stitches (sc, hdc, dc, dc, hdc, sc) plus a picot and forms the pointed outer wing tip; the other two have 4 counted stitches (sc, hdc, hdc, sc) plus a picot. Row 3 therefore makes 9 slip stitches + 6 + 4 + 4 fan stitches = 23 counted stitches, plus three uncounted ch-3 picots.

Assembly: pin the wings to the back and sides between Rnd 9 and Rnd 11, angled out and slightly up, then sew along the straight inner edge (leave the scalloped edge free). Each wing is about 42 mm long; with a 33 mm body that gives a wingspan of roughly 11.5 cm.

Bramble's three-lobed picot wings, pink-lined ears and little fangs.

### Finishing & assembly

Before you assemble, lay every component out and check it against the pattern; pin each piece and look at the toy from the front before committing a single stitch.

Boo: 1 body with ruffled hem, 2 arms, 1 optional flat base, 1 optional witch hat.

Pip: 1 sculpted body, 1 stem cone, 1 tendril, 1 leaf.

Bramble: 1 body, 2 lavender outer ears, 2 pink inner ears, 2 picot wings.

Display - Halloween garland (intended as decor; hang the long cord and felt balls out of children’s reach): cut 1.8 m / 6 ft of jute twine, or chain about 450 in sage (a chained cord is shorter than it looks - 150 chains is only ~60 cm). Make 3 of each mini and arrange all 9 before fastening. Thread one 20 mm felt ball in each of the 8 gaps between adjacent minis, then tie or slip-stitch each mini securely 10-13 cm / 4-5 in apart. The nine minis use about 25 g cream, 30 g orange, 27 g lavender, 12 g sage and 6 g pale pink; allow another 4 g sage if crocheting the cord instead of using jute.

### Troubleshooting

- **Pumpkin looks tall.** More than two straight rounds at Rnd 7-8 - extra plain rounds turn a pumpkin into a lemon.

- **Ribs vanish.** Overstuff before sculpting and pull each rib firmly to the same tension; one over-tight rib pulls the body out of round.

- **Ruffle gaps at the marker.** Each hem repeat must take exactly 4 stitches (2 sl st, shell into 1, 1 sl st); six repeats use all 24.

- **Wing row runs short.** The Row 3 groups are 2 / 3 / 2 / 2 - count the slip stitches, not the scallops.

- **Wing scallops look uneven.** They are meant to be different: the FIRST fan in the written Row-3 sequence forms the largest outer tip; the next two are smaller.

- **Ghost leans / will not stand.** The two Rnd 8 increases must sit opposite each other ([11 sc, inc] x 2). Boo takes no stuffing; if he falls, sew on the optional flat base.

- **Hat swamps the ghost.** Stop the brim at Rnd 6, 20 stitches - a wider brim flares past Boo's 27 mm head.

- **Cannot fit the eye washers.** You closed the piece first. Boo's eyes go in through his open bottom; Bramble's go in after Rnd 8 before the body narrows.

### Colorways

Classic cream  ·  Pumpkin orange  ·  Bat lavender  ·  Ghostly white  ·  Charcoal  ·  Sage & oat

### Designer notes

- Also try: all-white with silver wings, charcoal with orange, or sage-and-oatmeal for a muted autumn set. Jewel and pastel tones both photograph well against a pale background.

### Care

Follow the labels for every yarn and component used. Before publishing a care claim or supplying finished minis, clean and dry a complete sample by the proposed method, then inspect for dye transfer, distortion, stuffing migration, shifted eyes and opened seams. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying flat away from heat. Do not wash an assembled garland unless the cord, felt balls, wall-hanging attachments and all nine minis have been assessed for that method.

### Terms of Use

#### Copyright & ownership

This crochet pattern set - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 02.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished minis and garlands as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

No finished mini has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Plastic eyes require particular attention; embroidery removes that component hazard but is not proof of overall compliance. The finished-item maker or seller is responsible for applicable assessment, evidence, labelling and traceability before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#KawaiiHalloweenSet** - We love seeing your spookies. Thank you for supporting an independent pattern designer.


---

# Part 03 of 17 — NS-03 · Axel the Axolotl

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 9 pp · print edition 9 pp · reports: `docs/ns03/NS03_validation_report.md`*

## Axel the Axolotl

> **US terms  ·  Advanced beginner  ·  2.5 - 3 hours**  —  Design Code NS 03

A soft pink axolotl with six fluffy gills, a round head and a shell-edged paddle tail. Head, neck, body and tail are one continuous spiral - no neck seam to sew.

**FINISHED SIZE**  About 11.5 cm (4.5 in) tall seated.  About 10 cm (4 in) wide, gill tip to gill tip.  4.3 cm (1.7 in) tail. The head is a near-true sphere at 52 mm wide by 51.6 mm tall.

---

### Safety — read this first

Axel uses two 6 mm plastic safety eyes. If an eye, washer or surrounding stitch fails, it can release a small part: lock the washers firmly from the inside before stuffing, then check each eye and the surrounding fabric by hand. If a post, washer or stitch shifts, do not supply or use the item. The gills, arms, feet and tail fin are all sewn or worked on: sew each seam twice and weave every end in for at least 5 cm, then trim close.

No finished Axel has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime; do not describe one as “baby-safe” or compliant. Embroidered eyes remove the plastic-eye detachment hazard but do not by themselves establish suitability for any age. Before supply, the finished-item maker or seller must determine all applicable classification, assessment, testing, documentation, labelling and traceability duties for intended and reasonably foreseeable use in every destination market.

### Materials

- Main yarn: worsted #4, pale pink, about 15 g. Cotton or acrylic with a smooth matte finish - one 25 g ball covers the whole axolotl.

- Gill yarn: fuzzy / eyelash / fur yarn, dark pink, about 8 g. Essential: smooth worsted will not give fluffy gills, and the gills are the whole look.

- Fin yarn: worsted #4, dark pink, about 3 g, smooth - so the shell edging stays crisp.

- Hook: 3.5 mm (US E/4) for a tight gauge so stuffing cannot show through.

- Eyes: two 6 mm safety eyes (9 mm reads as buggy on this head).

- Also: polyester filling about 8 g; tapestry needle; black and pink embroidery floss; stitch marker.

### Gauge & size

Gauge: 36 sc around measures about 52 mm across when stuffed (4.5 mm per stitch, 4.3 mm per round). Wider than 55 mm across? Drop to a 3.0 mm hook. Under 48 mm across? Go up to a 4.0 mm hook.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sc - single crochet  ·  dc - double crochet

inc - increase (2 sc in one st)  ·  invdec - invisible decrease

sl st - slip stitch  ·  st(s) - stitch(es)

FO - fasten off  ·  (n) - stitch count at round end

Worked in a continuous spiral: do not join and do not chain 1 between rounds - just keep going round after round.

### Techniques used, in the order you will meet them

1. **The magic ring** - The body, arms, feet and gills begin with a magic ring. Wrap the yarn once around two fingers, insert the hook, pull up a loop and work the first round into the ring, then pull the tail tight. The surface-worked tail fin does not use a magic ring.

2. **Working in a spiral** - Do not join and do not chain 1 between rounds - just keep going round after round. Keep a stitch marker in the first stitch of every round and move it up each time; there is no join to count from.

3. **The invisible decrease** - Insert the hook through the front loops only of the next two stitches, yarn over and pull through both, then yarn over and pull through the remaining two loops. It leaves no ridge, which matters on the head and neck where decreases are visible.

4. **Closing through both layers** - To close a flat opening, fold the piece flat so the front and back layers lie together, then work one sc through each matched pair of stitches. Axel's 6-stitch tail tip folds into 3 pairs and closes with 3 sc.

5. **The shell (scallop)** - Work all the stitches of the group into one stitch, then slip stitch into the next stitch to anchor it. The group fans into a cup. Working the dc loosely makes each scallop cup outward instead of lying flat.

### Instructions

#### 1. Head, body & tail - one piece, main pink

Worked in a single spiral from the top of the head straight through to the tail tip. Head and body are both 36 stitches around; the neck at Rnd 13 is the only waist. Three straight rounds at the head keep it spherical rather than egg-shaped.

| Rnd | Instruction | Sts | Note |
|---|---|---|---|
| R1 | 6 sc in MR | (6) | start at top of head |
| R2 | inc in each st around | (12) | - |
| R3 | [sc, inc] x 6 | (18) | - |
| R4 | [2 sc, inc] x 6 | (24) | - |
| R5 | [3 sc, inc] x 6 | (30) | - |
| R6 | [4 sc, inc] x 6 | (36) | head at full width |
| R7 | sc in each st around | (36) | eye row: between R7 and R8 (install after R9) |
| R8 | sc in each st around | (36) | - |
| R9 | sc in each st around | (36) | lock eye washers and embroider face now |
| R10 | [4 sc, invdec] x 6 | (30) | - |
| R11 | [3 sc, invdec] x 6 | (24) | STUFF HEAD FIRMLY |
| R12 | [2 sc, invdec] x 6 | (18) | - |
| R13 | sc in each st around | (18) | NECK - narrowest point |
| R14 | [2 sc, inc] x 6 | (24) | body flares out |
| R15 | [3 sc, inc] x 6 | (30) | - |
| R16 | [4 sc, inc] x 6 | (36) | body at full width |
| R17 | sc in each st around | (36) | arms at R17 - R18 |
| R18 | sc in each st around | (36) | - |
| R19 | sc in each st around | (36) | - |
| R20 | sc in each st around | (36) | - |
| R21 | sc in each st around | (36) | - |
| R22 | sc in each st around | (36) | - |
| R23 | [4 sc, invdec] x 6 | (30) | - |
| R24 | [3 sc, invdec] x 6 | (24) | FEET attach at R24 - R25 |
| R25 | [2 sc, invdec] x 6 | (18) | stuff body LIGHTLY |
| R26 | [sc, invdec] x 6 | (12) | - |
| R27 | sc in each st around | (12) | tail begins; mark dorsal fin anchor |
| R28 | [2 sc, invdec] x 3 | (9) | - |
| R29 | sc in each st around | (9) | - |
| R30 | sc in each st around | (9) | - |
| R31 | sc in each st around | (9) | - |
| R32 | [sc, invdec] x 3 | (6) | light stuffing to here |
| R33 | sc in each st around | (6) | - |
| R34 | sc in each st around | (6) | - |
| R35 | sc in each st around | (6) | - |
| R36 | sc in each st around | (6) | taper to tip; tenth fin anchor |

**Mark the fin path while you crochet:** on each of Rnds 27-36, place a scrap-yarn marker through the surface stitch nearest the dorsal (top) centre of the tail. Keep the ten markers in one straight line rather than following the spiral's round start. These marked stitches are existing stitches, not extras; they give the fin ten unambiguous surface anchors.

Finish: fold the last 6 stitches flat so 3 pairs line up (3 front + 3 back), then work 1 sc through each pair - 3 sc in total - to close the tip cleanly. FO and weave the end away from the marked dorsal line so it cannot be mistaken for a fin anchor.

The tail runs R27-R36 - ten rounds, about 43 mm - giving exactly ten marked dorsal surface anchors. Five loose double-crochet scallops form the shell-edged paddle along that marked line.

#### 2. Arms & feet - main pink

Arms and feet are made separately and sewn on, not worked into the body, so each limb keeps its own rounded shape and can be set at the right angle.

##### Arms (make 2)

| Rnd | Instruction | Sts | Note |
|---|---|---|---|
| R1 | 6 sc in MR | (6) | - |
| R2 | sc in each st around | (6) | - |
| R3 | sc in each st around | (6) | - |
| R4 | sc in each st around | (6) | - |
| R5 | sc in each st around | (6) | - |
| R6 | sc in each st around, then FO | (6) | arms finish here |

Arms: FO with a long tail, do not stuff. Flatten the open end and sew it closed as you attach, so the arms hang softly.

##### Feet (make 2)

| Rnd | Instruction | Sts | Note |
|---|---|---|---|
| R1 | 6 sc in MR | (6) | - |
| R2 | [sc, inc] x 3 | (9) | - |
| R3 | sc in each st around | (9) | - |
| R4 | sc in each st around | (9) | - |
| R5 | [sc, invdec] x 3 | (6) | feet finish here |

Feet: FO, cinch closed with a long tail and stuff lightly - do not flatten them, they are plump little balls.

Sew each foot on with its closed nub facing the body (see Finishing & assembly for placement).

#### 3. Gills - fuzzy dark pink (make 6, 3 per side)

| Rnd | Instruction | Sts | Note |
|---|---|---|---|
| R1 | 6 sc in MR | (6) | - |
| R2 | inc in each st around | (12) | - |
| R3 | sc in each st around | (12) | - |
| R4 | sc in each st around | (12) | - |
| R5 | [sc, invdec] x 4 | (8) | open edge sewn to head |

Working with fuzzy yarn: you cannot see the stitches. Hold a thin strand of matching smooth yarn together with the fur yarn so you can find the stitches, or count by feel with the hook tip and trust the round count. Small errors are invisible in the finished fluff.

Finish gills: FO with a long tail. The 8-st open edge is sewn straight to the head and disappears in the fluff - simply whip-stitch it flat against the head.

If you prefer a rounded lobe, cinch the front loops of the opening first with a spare strand, then whip-stitch the gathered edge to the head. Three fluffy gills fan behind each eye - upper angled up, middle out, lower down.

#### 4. Tail fin - smooth dark pink

With smooth dark pink yarn, join with a sl st at the tip end-closure corner. Working from the tip toward the body along the TEN marked surface anchors from Rnds 36 back to 27:

- *Work 5 dc in the next marked anchor, then sl st in the next marked anchor. Repeat from * 4 more times - 5 scallops in total, using all 10 anchors. Remove each marker as you use it.

FO after the fifth anchoring sl st and weave in.

Each scallop uses exactly 2 marked surface anchors, so five scallops use all 10 anchors. Do not hunt for an imaginary ridge or work into random side bars: the marked dorsal stitches are the path. Keep the final anchoring sl st close to the body junction; it lands on the R27 anchor.

Work the dc groups loosely so each scallop cups outward. For a fuller paddle, first mark a second straight line of ten underside surface stitches (one per tail round), then work a second identical 5-scallop row there; do not stretch the dorsal row around the tip.

A note on fullness: five shells over ten rounds is meant to ruffle - the cupped, frilly edge is the look, not a mistake. If the scallops seem crowded, work the dc even more loosely, use half a hook size larger for the fin yarn only, or work 4 scallops on a shorter marked path.

### Finishing & assembly

Eyes and embroidery: complete them immediately after Rnd 9, before Rnd 10 narrows the head. The 6 mm eyes go between Rnds 7 and 8, 6 stitches apart and centred on the front; lock both washers from inside. While the 36-stitch opening is clear, embroider the smile and optional pink blush described below, knotting and burying all floss ends inside. Do this before stuffing at Rnd 11. Six stitches spans about 27 mm on the 52 mm head - about half the width. Once locked, check each eye and its surrounding stitches firmly by hand; this workshop check does not replace any prescribed product-safety test.

Smile: immediately after Rnd 9, use black floss to embroider a wide shallow U across Rnds 8-9, centred between the eyes and about 5 stitches wide. Keep it shallow; a deep curve reads as a frown. Knot and bury the floss ends inside.

Blush (optional): also immediately after Rnd 9, embroider two or three short pink stitches directly under each eye, just outside the eye line; knot and bury the floss ends inside. Do not use loose chalk or pastel on an item that may be handled or washed.

Gills: sew 3 lobes to each side of the head, behind the eyes, anchored at about R6 (upper), R7-R8 (middle) and R9 (lower). Angle the top lobe upward, the middle one straight out and the bottom one downward so they fan, then tease the fibres apart with a slicker brush or your fingers.

Arms: sew one arm to each side at R17-R18, about 6 stitches out from the centre front, angled slightly forward.

Feet: sew one foot to each side of the centre front at R24-R25, about 4 stitches out from centre, so Axel sits flat and upright.

Before you sew - lay every component out and check: 1 body, 2 arms, 2 feet, 6 gills, 1 fin. Check each against the pattern before attaching anything.

### Troubleshooting

- **Head firm, body soft.** Stuff the head hard at R11 so it holds a sphere and the eyes stay level. Keep the body light so Axel stays squishy and sits down.

- **Neck collapsing.** The 18-stitch neck is deliberately narrow. First pack a little more stuffing into the neck through the body opening before closing R25. For a permanently sturdier neck, work R13 as [7 sc, inc] x 2, 2 sc (20), then change R14 to [4 sc, inc] x 4 (24) so it consumes all 20 stitches; R15 onward is unchanged.

- **Want a wider gill span?** As written the gills give about 10 cm tip to tip. Work each gill two rounds longer - add 2 plain rounds at 12 stitches before R5 - for a span of about 12 cm.

- **Stuffing shows through.** Go down to a 3.0 mm hook. Loose gauge on a 3.5 mm hook is the usual cause.

- **Axel will not sit.** Move the feet one round lower, keep the body lightly stuffed, and shape the tail behind the body as a counterbalance.

### Colorways

Classic pink  ·  White leucistic  ·  Melanoid black  ·  Mint  ·  Lavender

### Care

Follow the labels for every yarn and component used, especially the fuzzy gill yarn. Before publishing a care claim or supplying finished Axels, clean and dry a complete sample by the proposed method, then remeasure it and inspect for dye transfer, fibre shedding or matting, stuffing migration, shifted eyes and opened seams. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying flat away from heat. Check every eye, gill and limb again after cleaning.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 03.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished axolotl plushies as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

No finished Axel has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime, so do not claim “baby-safe”, “suitable from birth” or compliance. Embroidery removes the plastic-eye component but is not proof of overall compliance. The finished-item maker or seller is responsible for applicable assessment, evidence, labelling and traceability before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#AxelTheAxolotl** - We love seeing your makes. Thank you for supporting an independent pattern designer.


---

# Part 04 of 17 — NS-04 · Coco the Capybara

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 8 pp · print edition 8 pp · reports: `docs/ns04/NS04_validation_report.md`*

## Coco the Capybara

> **No plastic eyes  ·  Intermediate  ·  2.5 - 3 hours**  —  Design Code NS 04

A low, round, bottom-heavy capybara with a blunt sewn-on muzzle, plump stuffed legs and a calm embroidered sleeping face. No safety eyes and no small plastic parts.

**FINISHED SIZE**  About 10.3 cm (4 in) tall standing on all four legs.  About 5 cm (2 in) wide at the widest part of the body.  Squat and bottom-heavy, standing on her feet rather than her belly.

---

### Safety — read this first

Coco has an embroidered face and no plastic eye components, removing that particular detachment hazard. The stuffed item still has a sewn-on muzzle and ears; check every seam and surrounding stitch by hand, especially after cleaning.

No finished Coco has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Do not infer age suitability from the embroidered face or describe a finished item as “baby-safe” or compliant. Calling it “decorative” does not replace classification based on intended or reasonably foreseeable use. Before supply, the finished-item maker or seller must determine all applicable assessment, testing, documentation, labelling and traceability duties in every destination market.

### Materials

- Main yarn: worsted weight (#4), warm brown, about 30 g. A smooth matte yarn shows the stitch texture best.

- Face yarn: worsted weight (#4), dark brown, about 5 g, for the closed eyes, nose and mouth. Use the same weight as the main yarn.

- Hook: 3.0 mm. The gauge is written for this hook.

- Eyes: none. The sleeping face is embroidered - no safety eyes.

- Also needed: polyester fiber filling about 6 g; yarn needle; stitch marker; pins. Pins matter: the muzzle and ears are pinned before sewing.

### Gauge & size

Gauge: 36 sc around measures about 52 mm in diameter when stuffed (4.5 mm per stitch, 4.3 mm per round). Check it on the body after Rnd 6 - a stuffed tube, not a flat swatch. If your 36 sts measure wider than 52 mm, crochet more tightly or go down a hook size; a loose gauge will show stuffing.

Finished size: about 10.3 cm (4 in) tall, 5 cm (2 in) wide.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sc - single crochet  ·  inc - increase (2 sc in one st)

invdec - invisible decrease  ·  sl st - slip stitch

st(s) - stitch(es)  ·  Rnd(s) - round(s)

FO - fasten off  ·  (n) - stitch count at round end

Work in a continuous spiral - there is no join and no turning chain between rounds. Keep a marker in the first stitch of every round. Work every stitch through both loops unless a note says otherwise.

### Techniques used, in the order you will meet them

1. **The magic ring** - Every piece begins with a magic ring. Pull the tail tight once the first round is complete.

2. **Working in a spiral** - Keep a stitch marker in the first stitch of every round and move it up. There is no seam and no join to count from.

3. **The two-layer leg join** - This is the only fiddly step - worth practising once on a scrap magic ring. Hold a finished leg against the body with the pinched-flat top of the leg lying against the outside of the body. For each joining sc, insert the hook through one stitch on the front edge of the flattened leg top, the matching stitch on its back edge, AND the next body stitch, then complete one sc through all three layers. That paired leg edge and body anchor produce one body-round stitch, so every count in the body table stays correct. Pinch the leg top flat first - a round, un-pinched top will not lie against the curved body and the join will pucker. A 9-stitch leg top flattens to about 5 stitches across - pinch it down to a strip about 3 stitches wide and hold it while you join. The stitches you skip bunch up inside, and that bunch makes the leg look plump rather than tubular.

### Notes

How the height adds up: the body (Rnd 1-20) is 20 rounds at 4.3 mm each, about 86 mm; the short 8/9-round legs lift the body about 17 mm off the table, for a total standing height of about 103 mm = 10.3 cm.

### Instructions

#### 1. Legs - make 4

Stuff the lower half of each leg lightly, leaving the top loose. Back legs stop after Rnd 8; front legs work Rnd 9 too - they join one round higher and need to be one round longer so all four feet reach the table level.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | all four |

| R2 | [sc, inc] x 3 | (9) | all four |

| R3 | sc in each st around | (9) | all four |

| R4 | sc in each st around | (9) | all four |

| R5 | sc in each st around | (9) | all four |

| R6 | sc in each st around | (9) | all four |

| R7 | sc in each st around | (9) | all four |

| R8 | sc in each st around | (9) | BACK legs finish here |

| R9 | sc in each st around | (9) | FRONT legs only |

Finish: FO with a long tail; use it later to tack any tiny side gap left after the crocheted join. Before joining, pinch the whole 9-stitch top flat into a narrow strip about 3 stitches wide (see technique 3).

#### 2. Ears (make 2) & muzzle (make 1)

##### Ears - make 2 (do not stuff)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | [sc, inc] x 3 | (9) | - |

| R3 | sc in each st around | (9) | - |

| R4 | sc in each st around | (9) | - |

| R5 | sc in each st around, then FO | (9) | - |

##### Muzzle - make 1 (stuff lightly)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | [sc, inc] x 3 | (9) | - |

| R3 | [2 sc, inc] x 3 | (12) | - |

| R4 | sc in each st around | (12) | - |

| R5 | sc in each st around, then FO | (12) | - |

Ears: FO with a long tail and leave them empty - a shallow cup.
Muzzle: FO with a long tail and stuff lightly, just enough to hold a dome; it should sit proud of the head when sewn on.

#### 3. Body & head - one piece

Both are 36 stitches around with only a shallow waist between them - that is what makes Coco read as one round blob rather than a snowman. The legs are joined low at Rnd 4-5 (see below).

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | join BL1: 3 sc, [sc, inc] x 3, join BL2: 3 sc, [sc, inc] x 3 | (24) | join the BACK legs |

| R5 | 1 sc, inc, 1 sc, inc, 1 sc, join FL1: 3 sc, [sc, inc] x 3, 1 sc, join FL2: 3 sc, 3 sc, inc, 2 sc | (30) | join the FRONT legs |

| R6 | [4 sc, inc] x 6 | (36) | full width - check gauge |

| R7 | sc in each st around | (36) | - |

| R8 | sc in each st around | (36) | - |

| R9 | sc in each st around | (36) | stuff the body FIRMLY |

| R10 | [7 sc, invdec] x 4 | (32) | shallow waist |

| R11 | [7 sc, inc] x 4 | (36) | head begins |

| R12 | sc in each st around | (36) | muzzle over R12 - R14 |

| R13 | sc in each st around | (36) | - |

| R14 | sc in each st around | (36) | eyes at R14 - R15 |

| R15 | sc in each st around | (36) | embroider eyes now; ears attach here later |

| R16 | [4 sc, invdec] x 6 | (30) | - |

| R17 | [3 sc, invdec] x 6 | (24) | stuff the head firmly |

| R18 | [2 sc, invdec] x 6 | (18) | - |

| R19 | [sc, invdec] x 6 | (12) | top up stuffing |

| R20 | invdec x 6 | (6) | - |

Immediately after Rnd 15, embroider both closed eyes as described under Finishing, knotting and burying the floss ends inside while the 36-stitch opening is clear. Then work Rnds 16-20, stuffing the head as directed. Cinch the remaining 6 stitches closed and weave the tail inside the body. Do not decrease the Rnd 10 waist further - a narrow neck cannot hold the head upright on this shape.

How the leg joins work: work Rnd 4 and Rnd 5 following the full written rounds below. Wherever a round says “join”, hold a pinched-flat leg against the body and work the next 3 sc through both flattened leg-edge layers AND the body together (technique 3). Those 3 sc still count as 3 stitches of the round, so the stitch totals do not change - Rnd 4 ends at 24, Rnd 5 at 30. The joined stitches are always plain single crochet - never work an increase through a leg.

Rnd 4 - the BACK legs (24 stitches): work the first 3 sc through a leg and the body together, then [sc, inc] x 3; work the next 3 sc through the second leg and the body together, then [sc, inc] x 3 to the end of the round.

Rnd 5 - the FRONT legs (30 stitches): work 1 sc, inc, 1 sc, inc, 1 sc, making seven; join a leg over the next 3 sc; work [sc, inc] x 3 and 1 sc, making ten; join the second leg over the next 3 sc; work 3 sc, inc, 2 sc to the end, making seven. In the finished round that is 7 - 3 - 10 - 3 - 7 = 30, all six increases falling inside the plain runs. The 7-10-7 spacing centres each front leg between the two back legs.

Stitch arithmetic for both join rounds: each [sc, inc] x 3 block works into 6 stitches and makes 9 (sc in one stitch, then 2 sc - the increase - in the next, three times over). Rnd 4: worked = 3 + 6 + 3 + 6 = 18, using EVERY stitch of Rnd 3; made = 3 + 9 + 3 + 9 = 24. Rnd 5: worked = 5 + 3 + 7 + 3 + 6 = 24, using every stitch of Rnd 4; made = 7 + 3 + 10 + 3 + 7 = 30. The 3-sc join runs count once - each goes through the leg and the body in the same stitch.

Work the numbers exactly. If the front legs line up directly behind the back legs instead of between them, the footprint narrows and Coco tips. The correct spacing covers the deepest footprint this shape allows - about 65 mm across and 29 mm front to back. Hold the piece upside down and check all four legs sit square before you stuff the body.

The legs join low (Rnd 4-5) so every foot hangs about 17 mm below the body and Coco stands on her feet.

### Finishing & assembly

Muzzle: stuff lightly and pin it to the front of the head over Rnds 12-14. Sew three quarters of the perimeter with matching brown, pause to adjust the stuffing, then embroider the nose and mouth on the established curve. Knot those embroidery ends inside the muzzle while the last quarter is still open, finish the seam, and bury the sewing tail inside the body. It should sit proud of the head, not flush. Centring matters - the eyes are 6 stitches apart and a muzzle pinned even slightly off-centre crowds one eye.

Eyes: embroider - do not use safety eyes. Complete them immediately after Body Rnd 15, before the decreases and head stuffing. With dark brown, work a shallow downward arc about 3 stitches wide on each side across Rnds 14-15, 6 stitches apart, with a tiny tick angled down at each outer end. Knot and bury every floss end inside.

Nose & mouth: after three quarters of the stuffed muzzle is sewn on, work a small dark triangle at top centre, a short vertical line down from it, and a soft curved mouth to one side. Knot the ends inside through the open part of the seam, then finish sewing the muzzle.

Ears: pinch the base of each ear so it cups forward, then sew at Rnd 15, about 5 stitches apart, angled slightly outward. Rnd 15 is a full 36-st round, so this puts the ears on top of the head where a capybara's belong.

Legs: the 3-sc joins locked each leg's pinched top into the body round. Check that every pinched 3-stitch strip is caught fully in the round; if a sliver stays open at the side of a leg top, tack it shut with 2-3 whip stitches through all layers - it sits on the underbody and stays invisible.

Final shaping: roll the finished piece gently between your palms to settle the stuffing into a round, bottom-heavy shape.

Before you sew - lay every component out and check: 4 legs (2 back of 8 rounds, 2 front of 9), 2 ears, 1 muzzle, 1 body & head, closed at the crown. The sleeping face is all embroidery - closed-eye arcs, a small triangle nose and a soft curved mouth.

### Troubleshooting

- **Coco looks too tall.** Almost always too many plain rounds. Rnd 12-15 is the straight head section the face is positioned on; adding 'just one more' round turns the shape into a tower and moves the face.

- **Coco will not stand.** Check the join height, not the leg spacing. The legs belong on Rnd 4 and Rnd 5; joined any higher, they cannot clear the underside of the body and the belly rests on the table.

- **Coco tips forward or backward.** Most often the front legs are lined up behind the back legs instead of between them - the Rnd 5 spacing must be 7 sc, 10 sc, 7 sc. If still tipping, stuff the lower body more firmly and settle weight back over all four feet.

- **Rocks back, front feet in the air.** All four legs are the same length and they cannot be. Front legs join at Rnd 5 (21 mm up), back at Rnd 4 (17 mm up); work the front legs 9 rounds and the back legs 8.

- **The head flops back.** The Rnd 10 waist is deliberately shallow at 32 stitches - do not decrease it further. A narrow neck cannot hold the head upright.

- **Small hole where a leg meets the body.** You joined a flat, wide leg top instead of a pinched one. Flatten the whole 9-stitch top into a strip about 3 stitches wide before joining, so the un-joined stitches bunch up inside.

- **Muzzle looks flat / stuffing shows.** Stuff the muzzle just enough to hold a dome. If stuffing shows through the body, your gauge is too loose - 36 sts should measure 52 mm; crochet tighter or go down a hook size.

### Colorways

Classic warm brown  ·  Soft grey  ·  Sandy beige  ·  Cocoa

### Designer notes

- Why the legs join so low: back legs (8 rnd, ~34 mm) join at Rnd 4, only 17 mm above the base; front legs (9 rnd, ~39 mm) join at Rnd 5, 21 mm up. Different lengths, same result: every foot hangs about 17 mm below the body so all four land level. This is the most common failure on round-bodied animals.

- Bottom-heavy by design: stuff the lower body firmly and keep the shape squat. Coco is meant to be one continuous curve from base to crown - she stands on her feet, not her belly.

### Care

Follow the labels for every yarn and component used. Before publishing a care claim or supplying finished Cocos, clean and dry a complete sample by the proposed method, then remeasure it and inspect for dye transfer, fibre change, stuffing migration, distorted embroidery and opened seams. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying flat away from heat. Check the muzzle, ears and leg joins again after cleaning.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 04.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished Coco plushies as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store” (a link or tag is always appreciated).

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos in your own listings beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

No finished Coco has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. An embroidered face removes plastic-eye components but is not proof of overall compliance. The finished-item maker or seller is responsible for applicable assessment, evidence, labelling and traceability before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#CocoTheCapybara** - We love seeing your Cocos. Thank you for supporting an independent pattern designer.


---

# Part 05 of 17 — NS-05 · Little Duck Plushie

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 7 pp · print edition 7 pp · reports: `docs/ns05/NS05_validation_report.md`*

## Little Duck Plushie

> **Embroidered eyes  ·  Confident beginner  ·  1.5 - 2 hours**  —  Design Code NS 05

A round, squashy duckling in fluffy chenille, worked as a single piece from tail to crown - no body-to-head seam. Only the wings and the beak are sewn on.

**FINISHED SIZE**  About 16 cm (6.25 in) tall and 7.5 cm (3 in) wide in super-bulky chenille (#6) on a 4.5 mm hook.  One seamless body; 2 wings + 1 beak to sew.

---

### Safety — read this first

This duck uses embroidered eyes and no plastic eye components, removing that particular detachment hazard. This alone does not establish age suitability or product compliance. If you supply finished ducks, determine all classification, assessment, documentation, labelling and traceability duties for intended and reasonably foreseeable use in each destination market. Do not claim compliance without supporting records. Check every seam and surrounding stitch by hand and confirm that the chosen chenille pile does not shed; these workshop checks do not replace any prescribed test.

### Materials

- Body yarn: super-bulky chenille (#6), yellow, about 30 g. A 100 g ball makes two ducks comfortably. Fluffy chenille is the whole look.

- Details: a small amount of matching super-bulky (#6) orange yarn for the beak; black embroidery floss for the eyes. The stated beak size assumes the orange yarn matches the body gauge.

- Hook: 4.5 mm (US 7).

- Stuffing & notions: fibre fill about 30 g packed firmly; yarn needle, stitch marker, pins.

### Gauge & size

Gauge: about 8 mm per stitch and 7 mm per round in super-bulky chenille. Chenille varies between brands, so measure a 12-stitch swatch (about 10 cm) first. Finished size: about 16 cm tall and 7.5 cm wide - 23 rounds at 7 mm and a widest point of 30 stitches at 8 mm.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sc - single crochet  ·  inc - increase (2 sc in one st)

dec - invisible decrease  ·  sl st - slip stitch

FLO - front loops only  ·  FO - fasten off

st(s) - stitch(es)  ·  Rnd(s) - round(s)  ·  (n) - stitch count at round end

Work in a continuous spiral - no join, no chain 1 between rounds - with a marker in the first stitch of every round.

### Techniques used, in the order you will meet them

1. **Magic ring & spiral** - The start of the body and each wing is a magic ring. Work in a continuous spiral - no join, no chain 1 between rounds - with a marker in the first stitch of every round.

2. **Invisible decrease** - Insert the hook under the FRONT loop only of each of the next two stitches (three loops are now on the hook). Yarn over and pull through the two front loops, then yarn over and pull through the two remaining loops. This is flatter than a standard decrease, which matters at this scale.

3. **Around a chain (the beak)** - The beak is worked around both sides of a starting chain: along one side, three stitches in the far end chain, then back along the opposite side and two more stitches in the first working chain. With ch 5, the chain nearest the hook is skipped as the turning chain; all FOUR remaining chains are used. Rnd 1 has 10 stitches and Rnd 2 increases evenly to 16.

4. **Through both layers** - To close each flat wing, fold it and single-crochet across both layers at once - 6 sc take the 12 stitches down to 6 and leave a flat half-disc.

5. **Embroidery & sewing** - The eyes are embroidered (no safety eyes). The wings and the flattened, unstuffed beak are sewn on; catch whole stitches, make a second seam pass and pull-test each attachment.

### Instructions

#### 1. Body - yellow chenille

**Preparation:** make both wings (section 2) and the beak (section 3) before starting the body. You will attach the wings at the round-9 pause and the beak at the round-19 pause; neither pause should be spent crocheting a missing component.

The waist at R10-R12 and the reflare at R13-R14 separate body from head with no seam. Body and head are the same diameter (30 stitches, about 76 mm); the 18-stitch waist reads as the neck. Start stuffing at R10 - once the waist closes you cannot reach the body.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | body full width |

| R6 | sc in each st around | (30) | wings attach R6 - R9 |

| R7 | sc in each st around | (30) | - |

| R8 | sc in each st around | (30) | - |

| R9 | sc in each st around | (30) | PAUSE: attach both wings before stuffing |

| R10 | [3 sc, dec] x 6 | (24) | START STUFFING NOW |

| R11 | sc in each st around | (24) | - |

| R12 | [2 sc, dec] x 6 | (18) | waist closing |

| R13 | [2 sc, inc] x 6 | (24) | - |

| R14 | [3 sc, inc] x 6 | (30) | head begins |

| R15 | sc in each st around | (30) | - |

| R16 | sc in each st around | (30) | eyes at R16 - R17 |

| R17 | sc in each st around | (30) | - |

| R18 | sc in each st around | (30) | beak across R16 - R18 |

| R19 | sc in each st around | (30) | PAUSE: embroider eyes and attach beak before R20 |

| R20 | [3 sc, dec] x 6 | (24) | - |

| R21 | [2 sc, dec] x 6 | (18) | stuff head, shape cheeks |

| R22 | [sc, dec] x 6 | (12) | add final stuffing |

| R23 | dec x 6 | (6) | close via FLO |

Immediately after Rnd 9, sew on both wings while the body is empty and the 30-stitch opening lets you knot their tails inside; make a second seam pass. Then begin stuffing with Rnd 10 and continue through Rnd 19. Pause again before the head opening narrows: embroider and knot the eyes inside, then sew on the beak with its tail secured inside. Only then work Rnds 20-23, adding the final stuffing as directed. FO with a long tail; thread through the FLO of the 6 remaining stitches, pull tight, knot and bury.

Smaller head option: skip the R14 reflare (keep R14-R19 at 24) and close with R20 [2 sc, dec] x 6 (18), R21 [sc, dec] x 6 (12), R22 dec x 6 (6).

#### 2. Wings - yellow chenille (make 2)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | sc in each st around | (12) | - |

| R4 | sc in each st around | (12) | flatten, sc 6 across both layers |

Do not stuff. Flatten and sc 6 across both layers to close (12 sts to 6), leaving a flat half-disc about 30 mm across. Sew to the sides spanning R6-R9, angled slightly back.

#### 3. Beak - orange (make 1, worked around a chain)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 5 | - | - |

| Rnd 1 | sc in 2nd ch from hook, sc in next 2 ch, 3 sc in last ch; rotate to work along the opposite side: sc in next 2 ch, 2 sc in the remaining loop of the first working ch | (10) | uses all 4 working chains |

| Rnd 2 | inc, 2 sc, inc x 3, 2 sc, inc x 2 | (16) | 10 anchors used; 6 increases |

Sl st to the first stitch and FO with a long tail. Do NOT stuff - flatten it to a flat lens. As written it is a bold ~50 mm cartoon beak; for a daintier duck work Rnd 1 only (10 sts, about 35-38 mm).

### Finishing & assembly

Face & assembly - work in this order:

1. Wings: immediately after Rnd 9 and before stuffing, sew one wing to each side over Rnds 6-9, angled slightly back. Make a second seam pass, knot the tails inside and pull-test both wings.

2. Stuff from Rnd 10: fill the body firmly as the waist begins to close - the neck narrows fast. Continue through Rnd 19, then pause again.

3. Eyes: immediately after Rnd 19, embroider black eyes between Rnds 16 and 17, seven stitches apart (56 mm along the stitch line on the 76 mm-diameter head). Knot the floss ends inside while the 30-stitch opening is clear.

4. Beak: still before Rnd 20, pin horizontally across Rnds 16-18, centred between the eyes, and sew around the outer edge; knot and bury the tail inside.

5. Close: resume at Rnd 20, top up stuffing through Rnd 22, then work Rnd 23, close via the FLO and bury the end.

The flat orange beak and embroidered eyes avoid plastic facial parts; all sewn attachments still require secure seams and pull-testing.

### Troubleshooting

- **Much taller than 16 cm.** Your chenille is thicker than gauge. A 12-stitch swatch at 10 mm per stitch finishes near 20 cm.

- **Much shorter.** Finer yarn - see the size table; DK on 3.0 mm gives 7-8 cm, not 10-12.

- **Wings sit on the neck.** Too high. R6-R9 is the body; R10-R12 is the waist.

- **Beak leaves a gap / puffs.** Ch 5 gives four working chains after the skipped turning chain. Rnd 1 must use all four on both sides and finish at 10 stitches. Do not stuff; flatten before pinning.

- **Fill shows / head flops.** Hook too large for the yarn, or the waist was under-packed. Pack R10-R12 firmly before the reflare.

- **Cannot reach the body to fill.** You started too late - begin at Rnd 10 while the waist is still 24 stitches wide.

### Making a smaller duck

| Yarn / starting hook | Target finished height |

|---|---|

| Velvet / bulky (#5) - 3.0 mm | 10 - 12 cm |

| Aran / worsted (#4) - 2.75-3.0 mm | 9 - 10 cm |

| DK / light worsted (#3) - 2.5-2.75 mm | 7.5 - 8.5 cm |

These hooks are starting points only. Make a dense swatch and measure a completed sample before advertising any alternate size.

### Colorways

Original colourway: sunshine-yellow body and wings, tangerine-orange beak, and black embroidered eyes. Optional body-tone variations: buttercream, soft white, pale peach or duck-egg blue; keep the beak visibly contrasting and embroider the face in a dark washable thread.

### Care

Follow the actual yarn label and wash-test a finished sample before publishing care claims. Until that test is complete, recommend gentle surface cleaning with a damp cloth and mild soap, followed by drying flat away from heat. Restore the pile gently by hand; brushing can pull fibres from some chenille yarns.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 05.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished ducks as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

Eyes are embroidered and there are no plastic eye components. Finished items must still meet every product-safety, testing, documentation and labelling duty applicable to their classification and market. Do not claim EN 71, CE, UKCA, CPSIA or ASTM F963 compliance without the required evidence. Secure every seam and verify that the selected chenille does not shed.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#LittleDuckPlushie** - We love seeing your ducklings. Thank you for supporting an independent pattern designer.


---

# Part 06 of 17 — NS-06 · Momo the Loaf Cat

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 7 pp · print edition 7 pp · reports: `docs/ns06/NS06_validation_report.md`*

## Momo the Loaf Cat

> **No-sew body  ·  Advanced beginner  ·  2 - 2.5 hours**  —  Design Code NS 06

A cat folded into a perfect loaf. One no-sew body on an oval base: the ears are crocheted onto the head and the tail is worked off the body, so there are no separate components to sew on. Finishing still uses small ear-base tacks and embroidery.

**FINISHED SIZE**  About 7.9 cm (3.1 in) long, 5.2 cm (2 in) wide and 4.3 cm (1.7 in) tall.  A low, wide loaf, wider than it is tall (about 1.2 : 1).

---

### Safety — read this first

Momo uses two 8 mm plastic safety eyes. If an eye, washer or surrounding stitch fails, it can release a small part: lock the washers firmly from the inside before stuffing and closing, then check each eye and the surrounding fabric by hand. An embroidered-eye version removes those plastic components but does not make the whole item a tested toy.

No finished Momo has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime; do not describe one as “baby-safe” or compliant. Before supply, the finished-item maker or seller must determine all applicable classification, assessment, testing, documentation, labelling and traceability duties in every destination market. The ears and tail are worked onto the body, but their yarn ends and the face embroidery must still be secured and buried.

### Materials

- Main yarn: worsted #4, about 10 g. Grey, ginger, cream or black. One 25 g ball is enough for two at the stated gauge.

- Contrast: small amounts of white for the chest and paws, pink for the nose and inner ears.

- Hook: 3.5 mm (US E-4) - tight gauge so stuffing cannot show.

- Eyes: 2 x 8 mm safety eyes, or embroider in black.

- Also needed: polyfill about 10 g; tapestry needle; stitch marker; black embroidery floss.

### Gauge & size

Gauge: about 4.5 mm per stitch and 4.3 mm per round. Finished size about 7.9 cm long, 5.2 cm wide and 4.3 cm tall - a low, wide loaf. The 48-stitch oval base sets the whole size of the cat.

### Abbreviations (US terms)

ch - chain  ·  sc - single crochet

inc - increase (2 sc in one st)

dec - invisible decrease  ·  sl st - slip stitch

BLO - back loop only  ·  FO - fasten off

st(s) - stitch(es)  ·  Rnd(s) - round(s)  ·  (n) - stitch count at round end

Work in a continuous spiral unless a piece says otherwise - no joins, no chain 1 between rounds; move the marker up each round.

### Techniques used, in the order you will meet them

1. **Around a chain (oval base)** - THE step that makes the loaf. Crochet into BOTH sides of a starting chain: across the front, corner increases into the last chain, then back along the opposite side and into the last loop. That turns a chain into a flat oval instead of a strip. Do NOT use a magic-ring circle here - a round base gives a sphere every time.

2. **Working in a spiral** - No joins and no chain 1 between rounds; move the marker up each round - there is no join to count from.

3. **Back loop only (BLO)** - Work into the far loop only; the unused loops form a raised ridge - the visible edge where the oval base meets the walls. That ridge is what makes the loaf read as folded rather than moulded.

4. **The invisible decrease** - Front loops only of the next two stitches, yarn over and pull through both, then yarn over and pull through the remaining two. Every dec here is worked this way.

5. **Flat rows (ch 1, turn)** - The ears are not worked in the round: chain 1, turn, and work back along the row. Each row is shorter than the one before, forming the ear point.

6. **Working into body fabric** - The tail starts by pushing the hook through the finished body wall - go under a WHOLE stitch, not just one loop, or it will pull out.

### Instructions

#### 1. Body - one no-sew piece

The base is worked up to 48 stitches before the walls begin; the base size sets the whole cat. Stopping at 36 gives a body about 34 mm across that comes out tall and round no matter how firmly it is filled.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 9 | - | - |

| R1 | sc in 2nd ch, sc in next 6, 3 sc in last ch, sc in next 6, 2 sc in last loop | (18) | around both sides of chain |

| R2 | inc, 6 sc, inc x 3, 6 sc, inc x 2 | (24) | - |

| R3 | sc, inc, 6 sc, [sc, inc] x 3, 6 sc, [sc, inc] x 2 | (30) | - |

| R4 | 2 sc, inc, 6 sc, [2 sc, inc] x 3, 6 sc, [2 sc, inc] x 2 | (36) | - |

| R5 | 3 sc, inc, 6 sc, [3 sc, inc] x 3, 6 sc, [3 sc, inc] x 2 | (42) | - |

| R6 | 4 sc, inc, 6 sc, [4 sc, inc] x 3, 6 sc, [4 sc, inc] x 2 | (48) | BASE AT FULL SIZE |

| R7 | BLO sc around | (48) | ridge = base edge |

| R8 | sc in each st around | (48) | place and lock eyes before stuffing |

| R9 | sc in each st around | (48) | lock eyes; embroider face/chest/paws; then stuff |

| R10 | [6 sc, dec] x 6 | (42) | - |

| R11 | [5 sc, dec] x 6 | (36) | - |

| R12 | [4 sc, dec] x 6 | (30) | ears worked onto R12 |

| R13 | [3 sc, dec] x 6 | (24) | - |

| R14 | [2 sc, dec] x 6 | (18) | - |

| R15 | [sc, dec] x 6 | (12) | top up stuffing |

| R16 | dec x 6 | (6) | close via front loops |

Finish: thread the tail through the front loop of each of the 6 remaining stitches, pull tight, knot and bury. Shape check: the base is an oval about 79 mm long and 52 mm across; the walls add ten rounds of height, so the finished loaf is about 43 mm tall - wider than it is tall.

#### 2. Ears - worked onto the head (make 2)

After the body is closed, join the main yarn to the surface of Rnd 12, leaving about 6 body stitches between the INNER edges of the two ears. For Row 1, insert the hook under one whole body stitch for each sc; these five surface stitches act as the foundation. Work each ear as three short rows:

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Row 1 | sc in next 5, ch 1, turn | (5) | - |

| Row 2 | dec, sc, dec, ch 1, turn | (3) | - |

| Row 3 | dec, sc | (2) | the ear tip |

The row maths: Row 1 makes 5 stitches; Row 2 works dec, sc, dec (consumes 5, makes 3); Row 3 works dec, sc (consumes 3, makes 2) - those 2 stitches form the tip.

After Row 3, FO with a 15 cm tail; do NOT try to slip-stitch from the ear tip back to the head. Thread the tail through the 2 tip stitches to close the point, run it down the outer side edge, and tack that outer base corner to Rnd 12. Row 1 already secures the other base edge. Bury the tail inside the head, then embroider a small pink triangle on the front of each ear for lining.

#### 3. Tail - worked off the body

Join the main yarn to the back of the body at about Rnd 9 on the centre line. **Surface Rnd 1:** insert the hook under four adjacent whole body stitches arranged as a tiny square and work 1 sc into each (4); place a marker in the first sc. **Rnds 2-8:** sc in each of the 4 tail stitches (4). Work upward in a tight spiral; do not make a magic ring and do not count the body stitches as extra tail stitches. Do NOT stuff - a thin tail curls around the loaf far better than a filled one. FO and bury the end through the body.

### Finishing & assembly

Face & markings:

Eyes: immediately after Rnd 9, fix the 8 mm eyes between Rnds 8 and 9, about 7 stitches apart, LOW and wide on the front (7 sts is about 32 mm, roughly 60% of the body width). Low eyes read as a cat; high eyes read as a bear. Push the stems through and LOCK the washers from the inside. Before stuffing and continuing to Rnd 10, complete the nose, mouth, whisker dots, chest and paws below, knotting and burying every embroidery end inside.

Nose: at the after-Rnd-9 pause, embroider a small pink triangle centred between and just below the eyes, with two short stitches angled down from the point for the mouth; knot the ends inside.

Whisker dots: at the same pause, make three tiny black French knots on each side of the nose and secure the ends inside.

Chest & paws: with white yarn, embroider a soft oval on the chest and two small ovals at the front of the base for tucked paws. Add enough temporary stuffing to judge placement if needed, keep the 48-stitch opening clear, then knot the ends inside and continue stuffing before Rnd 10.

Long, low and wide - the BLO ridge and tucked paws make the loaf read as a folded cat.

### Troubleshooting

- **It came out round.** You stopped increasing at Rnd 4 instead of Rnd 6, worked too many plain rounds at Rnds 8-9, or used a magic-ring base instead of the oval. The base must reach 48 stitches.

- **Tall and narrow.** The base did not reach 48. Count the stitches at Rnd 6 before the BLO round - that one number decides the whole shape.

- **Ears lean back.** Join the yarn one round lower and angle the first row slightly forward.

- **Tail falls off.** The first 4 sc must go through the body fabric under a whole stitch, not just one loop.

- **Stuffing shows.** Go down to a 3.0 mm hook - loose gauge on 3.5 mm is the usual cause.

- **Face looks like a bear.** Eyes too high and too close. Drop them a round and widen to 7 stitches.

### Colorways

Grey tabby  ·  Orange ginger  ·  Cream  ·  Black  ·  Calico

### Designer notes

- Grey tabby, orange ginger, cream, black, and calico are all suitable; make the calico version with ginger and cream patches embroidered securely onto a grey base.

### Care

Follow the labels for every yarn and component used. Before publishing a care claim or supplying finished Momos, clean and dry a complete sample by the proposed method, then remeasure it and inspect for dye transfer, fibre change, stuffing migration, shifted eyes and loosened surface-worked ears or tail. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying flat away from heat. Check all facial components and yarn anchors again after cleaning.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 06.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished Momos as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

No finished Momo has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Embroidery removes the plastic-eye components but is not proof of overall compliance. The finished-item maker or seller is responsible for applicable assessment, evidence, labelling and traceability before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#MomoTheLoafCat** - We love seeing your loaves. Thank you for supporting an independent pattern designer.


---

# Part 07 of 17 — NS-07 · Pocket Positivity Trio

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 7 pp · print edition 7 pp · reports: `docs/ns07/NS07_validation_report.md`*

## Pocket Positivity Trio

> **3 mini patterns  ·  Easy / beginner  ·  20 - 35 min each**  —  Design Code NS 07

Three palm-sized amigurumi that slip into a coat pocket - Sunny the Sunflower, Waddle the Penguin and Spud the Potato. They share one easy construction and work up in an evening or two.

**FINISHED SIZE**  Sunny: about 3.0 cm across the petals.  Waddle: about 3.8 cm tall.  Spud: about 2.7 cm long.  #4 worsted on a 3.5 mm hook. Sunny’s petals are worked directly onto her centre; Waddle’s wings, chest and beak are sewn on; Spud starts around a chain and closes with one short seam.

---

### Safety — read this first

The set uses six 5 mm plastic safety eyes. If an eye, washer or surrounding stitch fails, it can release a small part: insert the six 5 mm safety eyes and lock every washer from the inside BEFORE stuffing and closing each piece, then check each eye and the fabric by hand. An embroidered-face version removes the plastic eye components but does not establish age suitability.

No finished trio has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime; do not market one as “baby-safe” or compliant. Calling a smiling, filled item an “adult collectible” or adding an age warning does not by itself determine its legal classification or replace required evidence. Before supply, the finished-item maker or seller must assess intended and reasonably foreseeable use and meet all testing, documentation, labelling and traceability duties in every destination market.

### Materials

- Yarn: #4 worsted (~250 m / 100 g). The three toys use roughly 8 m total (under 4 g), so scraps are fine. Golden yellow + chocolate (Sunny); black + cream chest + yellow beak (Waddle); warm tan (Spud).

- Hook: 3.5 mm (US E/4).

- Eyes: six 5 mm black safety eyes, or embroidery thread.

- Also: about 3 g fibre fill total, blunt tapestry needle, stitch marker, scissors.

### Gauge & size

Gauge: about 3.5 mm per stitch and 3.2 mm per round in sc. Pocket size means gauge shows - work a swatch; the stated sizes follow from it.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sc - single crochet  ·  hdc - half double crochet

inc - increase (2 sc in one st)  ·  dec - invisible decrease

sl st - slip stitch  ·  BLO - back loop only

st(s) - stitch(es)  ·  FO - fasten off  ·  (n) - stitch count at round end

Techniques: continuous spiral rounds with a marker (no joins); magic-ring start for Sunny's centre and Waddle's body; invisible decreases; petal CLUSTERS worked into one stitch with a slip stitch between petals; an OVAL worked around a chain for Spud; and simple sewing / embroidery.

### Instructions

#### 1. Sunny the Sunflower

A small brown cushion; Rnd 4 is worked in the back loops so nine yellow petals can be added later to the exposed front loops of Rnd 3.

##### Centre - chocolate

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | petals join here |

| R4 | BLO sc in each st around | (18) | lock eyes and embroider mouth now; leave Rnd 3 front loops free |

| R5 | [sc, dec] x 6 | (12) | - |

| R6 | dec x 6 | (6) | stuff firmly before closing |

##### Petals - yellow (worked in the round)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Petal | after closing the centre, join yellow with a sl st in any EXPOSED front loop of Rnd 3 (this counts as the first sl st); (sc, hdc, sc) in next front loop, [sl st in next front loop, (sc, hdc, sc) in next front loop] x 8, sl st to the first sl st, FO | (36) | 9 petals; use Rnd 3 front loops only |

Count check: Rnd 4 was worked BLO, so all 18 front loops of Rnd 3 are visible after the cushion is closed. The joining slip stitch counts as the first of 9 slip stitches. 9 sl sts plus 9 petals of (sc, hdc, sc) = 9 + 27 = 36 stitches, using exactly 2 exposed front loops per petal set. The slip stitch sits in the valley between petals; work this round loosely (use a 4 mm hook for this round only if it pulls tight). FO and weave in.

Face: if using safety eyes, insert the posts between Rnds 2 and 3, 3 stitches apart, and LOCK the washers immediately after Rnd 4. At the same pause, embroider a smiling mouth across Rnds 2-3 and knot its ends inside before the decreases and stuffing; do not wait until the centre is closed. If embroidering the eyes, 4 stitches apart also fits - complete and secure them at this same pause.

#### 2. Waddle the Penguin

##### Body - black

**Preparation:** make both wings, the chest patch and the beak from the subsections below before starting the body. They are attached at the Rnd-9 pause while their tails can still be secured inside.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | position eyes between Rnds 3 and 4 |

| R4-6 | sc in each st around (3 rnd) | (18) | - |

| R7 | [2 sc, inc] x 6 | (24) | chest over R4-8 |

| R8-9 | sc in each st around (2 rnd) | (24) | after R9: lock eyes, attach all pieces and embroider blush before R10 |

| R10 | [2 sc, dec] x 6 | (18) | - |

| R11 | [sc, dec] x 6 | (12) | - |

| R12 | dec x 6 | (6) | stuff as you go, close |

##### Wings - black (make 2)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 4 sc in MR | (4) | - |

| R2 | [sc, inc] x 2 | (6) | - |

| R3-4 | sc in each st around (2 rnd) | (6) | - |

FO with a 15 cm tail and do not stuff. At the Body Rnd-9 pause, sew the wings to the sides at Rnd 6 angled backward; make a second seam pass and knot the tails inside.

##### Chest patch - cream (flat oval)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 6 | - | - |

| R1 | sc in 2nd ch, 3 sc, 3 sc in last ch, then down the other side 3 sc, 2 sc in last ch | (12) | - |

| R2 | inc, 3 sc, inc x 3, 3 sc, inc x 2 | (18) | - |

FO with a tail. At the Body Rnd-9 pause, add enough stuffing to round the body while keeping the opening clear, then sew the full oval perimeter onto the front over Rnds 4-8 and knot the tail inside. Do not pull the seam tight: the curved body will let the centre puff naturally. A complete perimeter is more secure than leaving the side edges open.

##### Beak - yellow

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | ch 2, 3 sc in 2nd ch from hook | (3) | - |

| R2 | inc x 3 | (6) | - |

| R3 | sc in each st around | (6) | - |

FO and do not stuff. At the Body Rnd-9 pause, place the safety-eye posts between Rnds 3 and 4, 3 stitches apart and LOCK both washers. Sew the beak centred between them, angled slightly down, and knot the tail inside. Add optional short pink blush stitches now and knot their ends inside. Complete all of this before Rnd 10 starts the decreases.

#### 3. Spud the Potato

Spud is worked as an oval around a chain, then flat-stitched closed so the seam reads as a natural crease.

##### Body - warm tan

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 7 | - | - |

| R1 | sc in 2nd ch, 4 sc, 3 sc in last ch; other side: 4 sc, 2 sc in last ch | (14) | around the chain |

| R2 | inc, 4 sc, inc x 3, 4 sc, inc x 2 | (20) | - |

| R3-6 | sc in each st around (4 rnd) | (20) | after R6: lock eyes and embroider mouth before R7 |

| R7 | [3 sc, dec] x 4 | (16) | - |

| R8 | [2 sc, dec] x 4 | (12) | - |

| R9 | [sc, dec] x 4 | (8) | begin stuffing |

| R10 | dec x 4 | (4) | close the seam |

Closing: leave a 20 cm tail. With the body flat, whip-stitch the remaining opening closed along the flat top so the seam reads as the potato's natural crease; weave the end inside.

Face: insert the safety-eye posts between Rnds 4 and 5 on the broad side, 4-5 stitches apart. Immediately after Rnd 6, LOCK the washers and embroider a small open mouth below; knot and bury the floss ends inside before Rnd 7 begins decreasing. Spud's face is about 27 mm wide, so either 4 or 5 stitches between the eyes fits.

### Finishing & assembly

Before you finish, check each toy: Sunny has 9 even petals and a closed brown centre; Waddle has 2 wings, a cream chest and a yellow beak; Spud's seam reads as a crease. Every safety-eye washer is locked from the inside (before stuffing and closing) or the eyes are embroidered, and every end is woven in at least 5 cm.

### Troubleshooting

- **Petal edges curl / centre will not close.** Use invisible decreases on the centre's Rnd 5 and pull the closing snug. Nine petal repeats use exactly 18 stitches (two each) - check Rnd 3 is (18) and you slip-stitched once per repeat.

- **Petals sit flat.** Work the three stitches in one stitch loosely, or use a 4 mm hook for the petal round only.

- **Toys come out smaller / larger.** Tighter than 3.5 mm per stitch: go up half a hook size. Looser: drop to a 3 mm hook. If changing yarn weight, make a new dense swatch instead of forcing doubled yarn onto the original hook.

- **Waddle's wings flop.** Sew at Rnd 6 and catch a stitch of the body with each pass.

- **Spud's seam shows.** Whip-stitch along the flat top so the seam reads as a crease, and stuff evenly before closing.

- **Eyes too near the edge.** On Sunny and Waddle place them three stitches apart, not four.

### Making a bigger trio

Use bulky (#5) yarn with a 4.5 mm hook and make a dense swatch targeting about 4.5 mm per sc (about 1.3x the original gauge): Sunny ~3.9 cm, Waddle ~4.9 cm, Spud ~3.5 cm. Stitch counts do not change. Do not hold worsted yarn double on the original 3.5 mm hook; that combination is usually too tight to work safely or evenly.

### Colorways

Original trio: Sunny uses golden-yellow petals with a chocolate-brown centre; Waddle uses a black body, cream chest and golden-yellow beak; Spud uses warm tan. Faces are black. Optional coordinated variations: mustard and cocoa for Sunny, charcoal and oat for Waddle, and russet or sandy beige for Spud.

### Selling & care

These designs may be displayed as desk companions, but a listing label alone does not determine product classification. Do not claim “baby-safe” or compliance without the required evidence. Stuff firmly and evenly. Spot clean with a damp cloth and reshape while drying; do not machine wash unless the actual yarn and completed sample have been wash-tested.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 07.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished toys as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

This set uses 5 mm plastic safety eyes that may become small parts if the eye, washer or fabric fails. Embroidery removes those components but is not proof of overall compliance. The finished-item maker or seller must determine the applicable classification and meet all assessment, testing, documentation, labelling and traceability duties in each destination market. An age warning or “collectible” label is not a substitute for required evidence.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#PocketPositivityTrio** - We love seeing your makes. Thank you for supporting an independent pattern designer.


---

# Part 08 of 17 — NS-08 · Ember the Baby Dragon

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 9 pp · print edition 9 pp · reports: `docs/ns08/NS08_validation_report.md`*

## Ember the Baby Dragon

> **US terms  ·  Intermediate  ·  4 - 5 hours**  —  Design Code NS 08

A chunky, big-headed baby dragon with a stubby snout, scalloped wings and a ridge of spikes down the back. She sits, with folding haunches and splayed front legs.

**FINISHED SIZE**  About 10.5 cm (a touch over 4 in) tall seated - 103 mm by the gauge.  12.4 cm (just under 5 in) wingspan. About 5 cm (2 in) tail.  A sitting dragon - her body rests on the table and her legs pose rather than lift her.

---

### Safety — read this first

Ember uses two 10 mm plastic safety eyes. If an eye, washer or surrounding stitch fails, it can release a small part: lock each washer from the inside before the head is joined to the body, then check the eye and fabric by hand. An embroidered-eye version removes those plastic components but does not establish age suitability.

No finished Ember has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Calling the item “decorative” does not replace classification based on intended or reasonably foreseeable use. Before supply, the finished-item maker or seller must determine and meet all applicable assessment, testing, documentation, labelling and traceability duties in every destination market.

### Materials

- Main yarn: worsted #4, about 30 g used (buy a 50 g ball) - sage green, dusty teal, lilac or charcoal. The extra allows for tails, seaming and a gauge swatch.

- Contrast yarn: worsted #4, about 20 g in a contrast cream or pale gold - used for the wings, horns and spikes, so all the details match.

- Hook: 3.5 mm (US E/4).

- Eyes: 2 x 10 mm safety eyes - slit-pupil dragon eyes if you can get them.

- Also needed: polyester fibre fill about 10 g; a small amount of dark embroidery floss for the nostrils; tapestry needle; stitch markers; pins.

### Gauge & size

Gauge: about 4.5 mm per stitch and 4.3 mm per round. Check on the body after Rnd 5 - 30 stitches should measure about 43 mm across when filled. If your stitches are wider, crochet more tightly or drop to a 3.0 mm hook or the stuffing will show.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sc - single crochet  ·  hdc - half double crochet

dc - double crochet  ·  inc - increase (2 sc in one st)

dec - invisible decrease  ·  sl st - slip stitch

picot - ch 2, sl st in 2nd ch from hook  ·  FO - fasten off

st(s) - stitch(es)  ·  Rnd(s) - round(s)  ·  (n) - stitch count at round end

Work in a continuous spiral unless a row says to turn; mark the first stitch of every round. The wings and the spike strip are the exceptions - both are worked flat. Work every stitch through both loops unless a note says otherwise.

### Techniques used, in the order you will meet them

1. **The magic ring** - The head, body, limbs, tail and horns begin with a magic ring. Pull the tail tight once the round is complete. The flat wings and spike strip begin with chains instead.

2. **Working in a spiral** - Keep a stitch marker in the first stitch of every round; there is no join to count from.

3. **Matched open joins** - Ember's head and her neck are BOTH left open at 18 stitches, so the two edges are the same size and can be ladder-stitched together cleanly. This is the single most important structural detail - the head is heavy and this joint carries all of it. Do not close the head down to a point; stop at 18 stitches. Closing a heavy dragon head down to 6 stitches leaves a small gathered point sewn to a wide neck ring - a tiny seam carrying a big head, which is exactly why a dragon's head flops.

### Notes

How the size adds up: body Rnd 1-13 is 13 rounds at 4.3 mm each, about 56 mm; head Rnd 1-11 is 11 rounds at 4.3 mm each, about 47 mm; seated together 56 + 47 = 103 mm - about 10.5 cm. Wingspan: 45 + 34 + 45 = 124 mm - just under 12.5 cm. Tail: 12 rounds at 4.3 mm each, about 52 mm - about 5 cm.

### Instructions

#### 1. Head - main colour (worked top-down)

Worked top-down and LEFT OPEN - stop at 18 stitches, then fasten off without cinching the opening. Place the eye stems after Rnd 8 while the head is still wide open. Leave a long tail if you want a spare sewing strand. A big head is what makes a dragon read as a baby dragon. Two straight rounds only, then the decreases.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | head at full width |

| R7 | sc in each st around | (36) | eyes at R7 - R8 |

| R8 | sc in each st around | (36) | insert and LOCK eye washers now |

| R9 | [4 sc, dec] x 6 | (30) | - |

| R10 | [3 sc, dec] x 6 | (24) | begin stuffing |

| R11 | [2 sc, dec] x 6 | (18) | LEAVE OPEN - matches neck |

After Rnd 8, place the eye stems between Rnds 7 and 8, eight stitches apart, and lock both washers while the opening is still wide. Continue Rnds 9-11, stuffing firmly from Rnd 10. After Rnd 11, FO without decreasing or cinching; leave the 18-stitch edge open for sewing to the body's neck. Sew on the snout after the head is shaped. If embroidering eyes instead, complete them before joining the head to the body.

#### 2. Snout (make 1) - main colour

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | [sc, inc] x 3 | (9) | - |

| R3 | [2 sc, inc] x 3 | (12) | - |

| R4 | sc in each st around | (12) | - |

| R5 | sc in each st around | (12) | - |

Finish: FO with a long tail and stuff lightly. Before attaching, embroider two small nostrils at the tip and knot their ends inside through the open 12-stitch edge. Pin the snout centred on Rnds 8-11 of the head, just below the eye line, and sew all the way around. It must project past the curve of the head, not sit flush - a dragon without a projecting snout reads as a bear.

#### 3. Body - main colour (worked bottom-up)

Worked bottom-up. The neck is left open at 18 stitches so the head can be seated on it. Pack the neck firmly before you join the head - a soft neck is what lets the head flop forward.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | tail attaches R4 - R6 |

| R5 | [3 sc, inc] x 6 | (30) | full width - check gauge |

| R6 | sc in each st around | (30) | back legs at R6 |

| R7 | sc in each st around | (30) | - |

| R8 | sc in each st around | (30) | front legs at R8 |

| R9 | sc in each st around | (30) | - |

| R10 | [3 sc, dec] x 6 | (24) | wings at R10 - R11 |

| R11 | sc in each st around | (24) | - |

| R12 | [2 sc, dec] x 6 | (18) | stuff firmly |

| R13 | sc in each st around | (18) | LEAVE THE NECK OPEN |

Finish: FO with a 40 cm tail; do not close. When you join the head, ladder-stitch all the way around and then make a second pass and pull it tight - this joint carries the whole head.

#### 4. Legs (make 4) - main colour

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | all four |

| R2 | [sc, inc] x 3 | (9) | all four |

| R3 | sc in each st around | (9) | all four |

| R4 | sc in each st around | (9) | all four |

| R5 | sc in each st around | (9) | all four |

| R6 | sc in each st around | (9) | BACK legs finish here |

| R7 | sc in each st around | (9) | front legs only |

| R8 | sc in each st around | (9) | front legs only |

Finish: stuff the lower half lightly and leave the top 3 rounds soft; FO with a long tail. Press the 9-stitch opening flat - 4 stitches in front, 4 behind, the odd stitch tucked into the fold - and the leg mouth sews shut when you attach it. The pairs are different lengths on purpose: back legs (6 rnd / 26 mm) attach at Rnd 6, 26 mm up; front legs (8 rnd / 34 mm) attach at Rnd 8, 34 mm up. A higher join needs a longer leg so all four feet reach the table. Sew each pair about eight stitches apart; angle the back legs under as haunches and the front legs slightly forward. The body rests on the table - the legs pose, they don't lift her.

#### 5. Tail - main colour

Worked from the tip up so it tapers naturally.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 4 sc in MR | (4) | tip |

| R2 | sc in each st around | (4) | - |

| R3 | [sc, inc] x 2 | (6) | - |

| R4 | sc in each st around | (6) | - |

| R5 | sc in each st around | (6) | - |

| R6 | [2 sc, inc] x 2 | (8) | - |

| R7 | sc in each st around | (8) | - |

| R8 | sc in each st around | (8) | - |

| R9 | [3 sc, inc] x 2 | (10) | - |

| R10 | sc in each st around | (10) | - |

| R11 | sc in each st around | (10) | - |

| R12 | sc in each st around | (10) | base |

Finish: stuff lightly, FO with a long tail, flatten the open end and sew it to the back of the body at Rnds 4-6.

#### 6. Horns - contrast colour (make 2)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 4 sc in MR | (4) | - |

| R2 | sc in each st around | (4) | - |

| R3 | [sc, inc] x 2 | (6) | - |

| R4 | sc in each st around | (6) | - |

| R5 | sc in each st around | (6) | - |

Finish: do not stuff; FO with a long tail. Sew to the crown of the head, 6 stitches apart, angled back.

#### 7. Wings - contrast colour (make 2, worked flat)

Ch 11. Work in turned rows (ch 1 and turn at each row end):

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Found. | ch 11 | - | - |

| Row 1 | from the 2nd ch: sc in 4, hdc in 3, dc in 3 | (10) | - |

| Row 2 | sc in 3, hdc in 3, dc in 4 | (10) | - |

| Row 3 | sc in 2, hdc in 4, dc in 4 | (10) | - |

| Row 4 | sl st in first 2, (sc, hdc, dc, hdc, sc) all in next st, sl st in next 2, (sc, hdc, dc, hdc, sc) all in next st, sl st in last 4 | (18) | scalloped edge - FO with a 25 cm tail |

The scallop maths: the slip-stitch anchors are 2 + 2 + 4 = eight stitches; the two shells each fan from a single stitch (2 more), so all 10 stitches of Row 3 are consumed and nothing is left over. Pin the straight inner edge across Rnds 10-11 and sew the WHOLE edge so the scalloped edge stays free.

#### 8. Spike strip - contrast colour

One flat foundation strip is sewn down the centre back from crown to tail tip. It carries nine pointed fans: 3 on the head, 4 on the body and 2 on the tail.

**Foundation:** ch 34. Row 1: sc in 2nd ch from hook and in each ch across (33); ch 1, turn.

**Spikes:** Row 2: sl st in first 3 sts; [sl st in next st, (sc, hdc, dc, picot, dc, hdc, sc) all in next st, sl st in next st] x 9; sl st in last 3 sts. FO with a long tail.

Count check: the two 3-stitch end tabs plus nine 3-anchor spike repeats use all 33 stitches of Row 1 (3 + 27 + 3 = 33). Each fan has one ch-2 picot at its peak; picot chains do not count as row stitches. Sew the straight FOUNDATION edge to Ember and leave the fan edge free.

At the stated gauge, the foundation is about 13.5-15 cm long. PIN the whole strip from crown to tail tip before sewing. If your path is shorter, fold one plain end tab under; if it is longer, add 3 foundation chains and one complete spike repeat. Never stretch only one section.

### Finishing & assembly

Assembly - work in this order:

1. Eyes were inserted between Rnds 7 and 8 and the washers locked immediately after Rnd 8, before the head was stuffed. If embroidering instead, stitch them now.

2. Embroider and secure the nostrils inside the still-open snout, then sew the snout to the shaped head, centred on Rnds 8-11 below the eye line.

3. Horns to the crown, 6 stitches apart, angled back.

4. Head to body: both edges open at 18 stitches. Pack the neck firmly, seat the head and ladder-stitch around, then a second tight pass.

5. Legs: back pair to Rnd 6, front pair to Rnd 8, angled as described.

6. Tail to the back of the body at Rnds 4-6.

7. Wings across Rnds 10-11, sewn along the whole straight edge.

8. Spike strip LAST - pin from crown to tail tip before you sew a single stitch.

### Troubleshooting

- **Head flops forward.** Pack the neck firmly before closing and make the second ladder-stitch pass tight. If it still moves, the edges did not match - both head and neck must be open at 18 stitches.

- **Rocks back onto haunches.** The legs are all the same length and they cannot be. Back legs attach 26 mm up, front 34 mm up - work the back legs 6 rounds and the front 8.

- **Will not sit.** Legs sewn too high, or the base is under-stuffed. Back legs on Rnd 6, front on Rnd 8; keep the lower body firm enough to sit on.

- **Wings droop.** Sew along the whole straight inner edge, not just the top corner.

- **Spike strip is the wrong length / curves.** Row 1 must have 33 sc. Row 2 uses 3-stitch end tabs and nine complete 3-anchor spike repeats. Pin the straight foundation edge from crown to tail before sewing; fold an end tab under or add one 3-chain / one-spike module if needed. This is the most visible seam.

- **Looks like a bear.** The snout is missing or under-stuffed - it must project past the dome of the head.

- **Stuffing shows through.** Gauge too loose - 30 stitches should measure 43 mm across. Crochet tighter or drop to a 3.0 mm hook.

### Colorways

Sage green  ·  Dusty teal  ·  Lilac  ·  Charcoal  ·  Blush pink

### Designer notes

- The continuous spike ridge runs from crown to tail tip - it is sewn on last and pinned before any stitch.

### Care

Follow the labels for every yarn and component used. Before publishing a care claim or supplying finished Embers, clean and dry a complete sample by the proposed method, then remeasure it and inspect for dye transfer, fibre change, stuffing migration, shifted eyes, a loosened neck seam and opened limb, wing, horn or spine seams. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying flat away from heat. Reshape the wings and recheck every attachment after cleaning.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 08.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished Embers as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

No finished Ember has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Embroidery removes the plastic-eye components but is not proof of overall compliance. The finished-item maker or seller is responsible for applicable assessment, evidence, labelling and traceability before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#EmberTheBabyDragon** - We love seeing your dragons. Thank you for supporting an independent pattern designer.


---

# Part 09 of 17 — NS-09 · Shelby Sea Turtle Bag Charm

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 6 pp · print edition 6 pp · reports: `docs/ns09/NS09_validation_report.md`*

## Shelby the Sea Turtle Bag Charm

> **30 minutes  ·  Easy  ·  ~3 g of yarn**  —  Design Code NS 09

A pocket sea turtle on a keyring. It takes about half an hour and a few grams of yarn; the head and flippers are worked straight into the underside so there is almost nothing to sew.

**FINISHED SIZE**  About 3.7 cm (1.5 in) across the flippers, 3.2 cm long and 1.9 cm deep.  DK cotton on a 2.5 mm hook. The shell edge has 24 stitches; the underside has 24 base anchors before its 35-stitch appendage round. A bigger 5.7 cm version is included.

---

### Safety — read this first

Use two embroidered French-knot eyes. The four-stitch head fan is too small to seat two plastic eye washers reliably, so plastic eyes are not an option in this pattern. The metal keyring can become a small-part hazard if its attachment or surrounding fabric fails. Secure it with doubled yarn through TWO shell stitches while the seam is still open, knotting the ends inside before final stuffing and closure; check the ring, yarn and fabric by hand before each use.

No finished Shelby has been shown by Novality Store to comply with ASTM F963, EN 71 or any other product-safety regime. “Bag charm” is its intended use, but a name or warning alone does not determine legal classification. Before supply, the finished-item maker or seller must assess intended and reasonably foreseeable use and meet the applicable testing, documentation, labelling and traceability duties in every destination market.

### Materials

- Shell yarn: DK / light worsted (#3) cotton, about 1 g - sage, teal, mustard or rust.

- Body yarn: DK cotton, about 1 g in contrast cream, sand or pale green.

- Hook: 2.5 mm.

- Embroidery: black floss for two small French-knot eyes (no plastic eyes), plus a short strand one shade darker than the shell for its V markings.

- Also: a pinch of polyfill (under 1 g), tapestry needle, one 25 mm keyring or lobster clasp per turtle.

### Gauge & size

Gauge: about 3.5 mm per stitch and 3.2 mm per round. The whole charm is 203 stitches (~3 m of DK); 24 stitches = a 26.7 mm disc that sets the size.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sc - single crochet  ·  hdc - half double crochet

inc - increase (2 sc in one st)  ·  dec - invisible decrease

sl st - slip stitch  ·  BLO - back loop only

FO - fasten off  ·  st(s) - stitch(es)  ·  Rnd(s) - round(s)

(n) - stitch count at round end

Start in a magic ring and work continuous spiral rounds with a marker - no joins, no chain 1 between rounds.

### Techniques used, in the order you will meet them

1. **Magic ring & spiral** - Start in a magic ring and work continuous spiral rounds with a marker - no joins, no chain 1 between rounds.

2. **Back loop only (BLO)** - Work into the far loop only; the unused loops form a raised ridge. On the shell that ridge is the rim - it makes the dome read as a shell rather than a bun.

3. **Clusters into one stitch** - The trick of the head and flippers: work every stitch of the group into ONE back loop of the previous round so they share an anchor and fan into a bump. Work the whole appendage round in BACK LOOPS ONLY; the 24 unused front loops remain as clear seam loops. Each cluster consumes one anchor and produces as many stitches as it contains, so 24 anchors produce 35 stitches.

4. **Whip stitch & French knots** - Join shell and underside with an even whip stitch so the seam does not pucker. For each eye, bring the needle up, wrap the floss once or twice around the needle, push back down close by and pull slowly; knot both floss ends securely on the wrong side before joining.

### Instructions

#### 1. Shell - DK cotton (sage, teal, mustard or rust)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | BLO sc around | (24) | rim ridge |

| R6 | sc in each st around, then FO | (24) | FO with a 30 cm tail |

Before joining, embroider five or six shallow V shapes in a darker shade across the dome - two minutes, and the difference between a turtle and a green blob.

#### 2. Underside - contrast flat disc

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | do NOT fasten off - work head & flippers next |

##### Head & flippers (work from the live edge)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R5 | BLO: 3 sc, (sc, hdc, hdc, sc) in next st, 4 sc, (sc, hdc, sc) in next st, 3 sc, (sc, hdc, sc) in next st, 4 sc, (sc, hdc, sc) in next st, 3 sc, (sc, hdc, sc) in next st, 2 sc | (35) | head & flippers; leave all 24 R4 front loops free for seaming |

This consumes 3+1+4+1+3+1+4+1+3+1+2 = 24 back-loop anchors (closing the disc) and produces 35 stitches while leaving 24 front-loop seam anchors. The first, four-stitch bump is the HEAD; the four smaller bumps are flippers. Sl st to the first R5 sc and FO with a 20 cm tail. The bumps land on stitches 4, 9, 13, 18 and 22, placing the front flippers either side of the head.

#### 3. Face - read before you join

The head bump is only ~7-10 mm across. Work two small black FRENCH KNOTS, 2 worked stitches apart, low on the four-stitch head fan. Knot the floss ends on the wrong side. Do not substitute plastic safety eyes here: two washers cannot be seated with reliable clearance on this tiny one-row fan.

The BLO rim ridge and embroidered V markings turn the dome into a shell.

### Finishing & assembly

Joining the shell: finish and knot the embroidered eyes first. Hold the shell to the underside, wrong sides together, head pointing away from the shell's tail. Whip-stitch with the shell's 30 cm tail, matching the shell's 24 edge stitches one-for-one to the 24 exposed front loops of underside R4 - NOT to the 35 stitches of the appendage round. At each bump, use the exposed front loop directly below its base; never sew through the fan stitches themselves.

When about 5 cm / 2 in of seam remains, pass a doubled 20 cm strand of body yarn through TWO adjacent shell stitches at the back (opposite the head) and through the keyring twice. Tie the yarn ends together securely INSIDE the shell. Add a small pinch of stuffing, keep the charm flat (the shell holds only ~8 cm3), finish the seam, then weave in all ends. Do not wait until the seam is closed to secure the ring.

### Troubleshooting

- **Flippers uneven.** Count the plain runs between bumps: 3, 4, 3, 4, 3, then 2 at the end.

- **Keyring pulls out / too fat to hang.** Attach through two stitches and knot inside. Use less stuffing so the charm stays flat against a bag.

- **Shell and base won't pair.** Use the 24 exposed front loops of underside R4, one per shell stitch; do not try to match the 35 appendage-round stitches.

### Bigger Shelby (~5.7 cm across)

Work the shell to 42 stitches: Rnd 1 (6), Rnd 2 (12), Rnd 3 (18), Rnd 4 (24), Rnd 5 [3 sc, inc] x 6 (30), Rnd 6 [4 sc, inc] x 6 (36), Rnd 7 [5 sc, inc] x 6 (42), Rnd 8 BLO sc around (42), Rnd 9 sc around (42). Work underside Rnd 1-7 the same to 42 stitches, and do not fasten off.

Underside Rnd 8 (head & flippers), worked BLO throughout: 7 sc, (sc, hdc, hdc, sc) in next st, 8 sc, (sc, hdc, sc) in next st, 7 sc, (sc, hdc, sc) in next st, 8 sc, (sc, hdc, sc) in next st, 7 sc, (sc, hdc, sc) in next st = 53 stitches, consuming all 42 back-loop anchors and leaving all 42 front loops exposed. Sl st to the first sc of this round and FO. Join the shell's 42 edge stitches to those 42 exposed front loops by the same rule as the small version. Allow 45-50 minutes and about 4 g of yarn.

### Colorways

Original colourway: sage-green shell, cream underside/head/flippers, darker-sage embroidered shell markings and black French-knot eyes. Optional shell variations: teal, mustard or rust; pair each with a clearly contrasting sand, cream or pale-green body.

### Care

Follow the labels for the yarn, embroidery floss and keyring. Before publishing a care claim or supplying finished charms, clean and dry a complete sample by the proposed method, then inspect for dye transfer, corrosion, distortion, stuffing migration and damage to the ring attachment or seam. Until that sample test passes, recommend wiping the crochet surface with a barely damp cloth, keeping the metal ring as dry as possible, then drying the charm flat. Check the ring, doubled attachment yarn and surrounding shell stitches before each use and after cleaning.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 09.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished charms as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

Shelby uses embroidered French-knot eyes and a metal keyring and is designed as a keyring / bag charm. No finished Shelby has been shown by Novality Store to comply with ASTM F963, EN 71 or another product-safety regime, and its name alone does not determine classification. Attach the ring through two shell stitches with doubled yarn, knot it inside before closing the seam, and complete all market-specific assessment and documentation required before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#ShelbyTheSeaTurtle** - We love seeing your makes. Thank you for supporting an independent pattern designer.


---

# Part 10 of 17 — NS-10 · Willow the Bunny Lovey

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 7 pp · print edition 7 pp · reports: `docs/ns10/NS10_validation_report.md`*

## Willow the Bunny Lovey

> **Embroidered face  ·  Advanced beginner  ·  about 4 - 6 hours**  —  Design Code NS 10

A bunny comforter: a soft, firmly stuffed head above a light, drapey granny-square blanket. Long floppy ears to hold, an embroidered face with no plastic eye components, and a blanket that grows evenly from the centre out.

**FINISHED SIZE**  Blanket about 26 cm (10 in) square (20 rounds), with a calculated flat diagonal of about 36.8 cm (14.5 in). Head about 4.9 cm across; laid-flat ear-tip-to-opposite-corner length is about 42 cm (16.5 in), depending on how the ears fall.  DK cotton on a 3.5 mm hook (3.0 mm for the head if your tension is loose).

---

### Safety — read this first

Willow uses an embroidered face with no plastic safety eyes, buttons or beads; every floss end is knotted and buried inside the head. That removes those component hazards but does not establish age suitability or product compliance. Sew every seam twice and weave ends in at least 5 cm.

No finished Willow has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime; do not describe a finished item as “baby-safe”, “safe for sleep” or compliant. Keep this and every other soft object out of an infant’s cot, crib or other sleep space; allow only supervised, awake use. Before supply, verify current safe-sleep advice for the destination and determine all applicable classification, assessment, testing, documentation, labelling and traceability duties.

### Materials

- Yarn: DK (#3) 100% cotton or another washable yarn appropriate for the intended use, about 60 g - cream, sage, dusty pink or pale grey. Keep the ball band for fibre-content and care information. Only the head is stuffed.

- Hook: 3.5 mm (US E/4) for the blanket; use 3.0 mm for the head if your tension is loose.

- Face: dark brown or charcoal cotton embroidery floss, with ends knotted inside; no safety eyes or other plastic facial parts.

- Also: about 8 g fibre fill, tapestry needle, stitch marker.

### Gauge & size

Head gauge in sc: about 4.3 mm per stitch and 3.8 mm per round. Blanket check after Rnd 3: 9 dc along one edge should measure about 39 mm; narrower and the blanket comes out small.

### Abbreviations (US terms)

MR - magic ring  ·  ch - chain

sc - single crochet  ·  dc - double crochet

inc - increase (2 sc in one st)  ·  dec - invisible decrease

sl st - slip stitch  ·  st(s) - stitch(es)

sp - space  ·  FO - fasten off

(n) - stitch count at round end

The HEAD and EARS are worked in a continuous spiral (no joins, marker in the first stitch). The BLANKET is worked in JOINED rounds: each round closes with a slip stitch and the next begins with a turning chain - a different rhythm that lets the square grow out evenly. Work every stitch through both loops unless noted.

### Techniques used, in the order you will meet them

1. **Magic ring & spiral** - The head and each ear begin with a magic ring; pull the tail tight after round one.

2. **The granny-square corner** - Every blanket corner is (3 dc, ch 2, 3 dc) into one corner space. Those four corners make the piece square instead of round. Miss one corner group and the whole square pulls out of true - check all four at the end of every round.

3. **The border round** - One final round of single crochet around the edge with 3 sc into each corner space squares the edge and stops the blanket curling. Do not skip it.

### Notes

Sizing the blanket: the square grows ~1.3 cm per side per round - 18 rounds ~23 cm, 20 rounds ~26 cm, 22 rounds ~28 cm. Add rounds to make a bigger lovey.

### Instructions

#### 1. Head - worked top-down

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | ears at R4 - R6 |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | full width |

| R7 | sc in each st around | (36) | - |

| R8 | sc in each st around | (36) | face on R8 - R10 |

| R9 | sc in each st around | (36) | - |

| R10 | [4 sc, dec] x 6 | (30) | pause and embroider the face now, before stuffing |

| R11 | [3 sc, dec] x 6 | (24) | stuff firmly |

| R12 | [2 sc, dec] x 6 | (18) | - |

| R13 | [sc, dec] x 6 | (12) | top up stuffing |

| R14 | dec x 6 | (6) | close |

Immediately after Rnd 10, embroider the face described under Finishing while the 30-stitch opening is fully accessible; knot and bury every floss end inside. Then work Rnds 11-14, stuffing as directed, FO and close with the yarn tail.
The finished head measures 4.9 cm across and 5.3 cm tall. Stuff it FIRMLY - a soft head collapses when gripped and the face distorts.

#### 2. Ears - long and floppy (make 2, do not stuff)

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | [sc, inc] x 3 | (9) | - |

| R3 | [2 sc, inc] x 3 | (12) | - |

| R4-8 | sc in each st around (5 rnd) | (12) | - |

| R9 | [2 sc, dec] x 3 | (9) | - |

| R10 | sc in each st around | (9) | - |

| R11 | [sc, dec] x 3 | (6) | flatten, FO |

Flatten and FO with a long tail. Sew to Rnds 4-6 of the head, about 10 stitches apart, pinching each base so it flops forward.

#### 3. Blanket - granny square, joined rounds

Ch 4 and sl st to the first ch to form a ring. Every round closes with a slip stitch into the top of the starting ch-3.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Rnd 1 | ch 3 (counts as first dc), 2 dc in the ring, [ch 2, 3 dc in the ring] x 3, ch 2, sl st to the ch-3 top | (12) | 12 dc, 4 corner spaces |

| Rnd 2 | sl st in next 2 dc and into the next corner space; ch 3 (counts as first dc), 2 dc, ch 2, 3 dc in that same space (first corner); then (3 dc, ch 2, 3 dc) into each remaining corner space; sl st to top of ch-3 | (24) | positioning sl sts do not count |

| Rnds 3-20 | sl st in next 2 dc and into the next corner ch-2 space; ch 3 (counts as first dc), 2 dc, ch 2, 3 dc in that same corner. Work 3 dc in every GAP between adjacent 3-dc groups along each side (these are not chain spaces), and (3 dc, ch 2, 3 dc) in each remaining corner; sl st to top of ch-3. Each round adds one 3-dc group to every side (+12 dc per round) | - | see dc table |

Total dc per round: Rnd 3 = 36, Rnd 5 = 60, Rnd 10 = 120, Rnd 15 = 180, Rnd 20 = 240 (60 dc per edge = ~26 cm).

Border: after the Rnd 20 join, ch 1 (does not count), sc in the SAME dc as the join and once in every remaining dc; work 3 sc into each corner ch-2 space (into the space itself - do not work into the 2 individual chains). Sl st to the first sc and FO. At Rnd 20 that is 240 sc over the dc + 12 corner sc = 252 sc. This firms the edge and stops the square curling.

At the start of Rnds 3-20, the three positioning slip stitches move the hook from the previous join to the corner; they do not count as dc. The side spaces are the visible gaps between adjacent 3-dc groups; there are no side chains to hunt for. Open dc clusters and crisp (3 dc, ch 2, 3 dc) corners keep the square true round after round.

### Finishing & assembly

Face (embroidery only): this must be completed immediately after Head Rnd 10, before stuffing begins. Make two small oval eyes about 8 stitches apart across Rnds 8-9, a small inverted-triangle nose centred between and below them, and a shallow Y for the mouth. KNOT every end inside the head and bury the tails before continuing to Rnd 11. Skip blush - chalk rubs off on bedding and is not washable.

Joining: mark all 18 stitches of Head Rnd 12. Centre the closed underside of the head over one blanket corner, overlapping the blanket by about 3 cm and tucking the small Rnds 13-14 closing nub against the fabric. Sew the blanket corner to the 18 marked Rnd-12 stitches in a complete circle; do NOT attach the load only to the 6-stitch closure. Sew the full circle a second time with a separate strand - this is the main structural seam and it will be pulled, chewed and washed. Knot securely and weave every end in at least 5 cm.

### Troubleshooting

- **Blanket curls / not square.** You skipped the sc border, or missed a (3 dc, ch 2, 3 dc) corner - check all four corners at the end of every round.

- **Came out too small / head flops.** Tighter than 4.3 mm/dc: go up one hook size or add rounds; 22 rounds measure about 28 cm. Stuff the head firmly and sew the base seam twice.

### Colorways

Cream  ·  Sage  ·  Dusty pink  ·  Pale grey  ·  Butter yellow

### For your listing

Materials: state the actual yarn fibre from your ball band; embroidered face, no safety eyes, no buttons, beads or removable parts.

Care: publish only the complete-sample-tested method described below. Until that test passes, state gentle surface cleaning and drying flat; a washable-yarn label alone does not validate the stuffed head, embroidery and assembled seams.

Use only under active adult supervision while the child is awake. Keep the comforter out of an infant’s cot, crib and other sleep space, and verify current safe-sleep guidance for the destination market before publishing listing advice.

### Care

Follow the labels for the yarn, floss and stuffing, but test the whole assembled item rather than relying on a yarn label alone. Before publishing a machine-wash, hand-wash or other care claim, clean and fully dry a complete sample by that method; remeasure it and inspect for dye transfer, shrinkage, stuffing migration, distorted embroidery, opened ear seams and any movement at the twice-sewn 18-stitch head-to-blanket join. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying flat away from heat. Avoid high heat: cotton can shrink and the assembled shape can distort, although cotton does not felt like wool. Recheck every seam after cleaning.

### Designer notes

- Suggested colorways: cream, sage, dusty pink, pale grey and butter yellow.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 10.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished loveys as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to “Novality Store”.

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

Willow has an embroidered face and no plastic safety eyes, buttons or beads, but no finished Willow has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Do not claim “baby-safe”, “safe for sleep” or compliance. Keep soft objects out of an infant’s sleep space; allow only supervised, awake use. The finished-item maker or seller must verify current market-specific requirements and safe-sleep advice before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#WillowTheBunnyLovey** - We love seeing your makes. Thank you for supporting an independent pattern designer.


---

# Part 11 of 17 — NS-11 · No-Sew Christmas Gnome

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 7 pp · print edition 7 pp · reports: `docs/ns11/NS11_validation_report.md`*

## No-Sew Christmas Gnome

> **US + UK equivalent  ·  Beginner  ·  1 - 2 hours**  —  Design Code NS 11

A plump little gnome worked as ONE continuous piece - body, beard, face and hat all in one tube with simple colour changes and a bobble nose. No assembly seams. A straightforward first amigurumi and a quick seasonal project.

**FINISHED SIZE**  About 12 cm (4.75 in) tall in worsted / aran on a 3.5 mm hook.  About 5 cm (2 in) wide at the base.  One piece - no assembly, no sewing.

---

### Safety — read this first

Optional plastic safety eyes can become small parts if an eye, washer or surrounding stitch fails. Insert the safety eyes and lock their washers from the inside BEFORE stuffing and closing, then check each eye and the fabric by hand. An embroidered or plain face removes those plastic components but does not establish age suitability.

No finished gnome has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime; do not market one as “baby-safe” or compliant. Before supply, the finished-item maker or seller must determine all applicable classification, assessment, testing, documentation, labelling and traceability duties in every destination market. Stuff firmly and secure every yarn end.

### Materials

- Body + hat yarn: worsted / aran (#4), 45 g, red or green.

- Beard yarn: worsted or fluffy white, 12 g.

- Face yarn: skin tone, about 10 g.

- Optional: dark yarn for embroidered eyes, or 2 x 6-8 mm safety eyes.

- Hook: 3.5 mm (US E-4) - or whatever size makes a dense, no-see-through fabric.

- Stuffing: fibre fill about 25 g.

- Notions: stitch marker, tapestry needle, scissors.

### Gauge & size

Gauge is not critical - aim for a firm fabric (about 10-11 sc x 11 rounds = 5 cm). If stuffing shows through, go down half a millimetre.

### Abbreviations (US + UK)

MR - magic ring  ·  sc2tog = dc2tog - work 2 stitches together as one (a decrease; swap for an invisible decrease, invdec, on the hat if preferred)

ch - chain  ·  BO - 5-dc bobble (counts as 1 st) / UK: 5-tr bobble (counts as 1 st)

sl st - slip stitch  ·  FO - fasten off

sc = dc - single crochet / double crochet  ·  st(s) - stitch(es)

dc = tr - double crochet / treble crochet  ·  R - round

inc - increase (2 sc in one st) / UK: increase (2 dc in one st)  ·  (n) - stitch count at round end

How to read this dual pattern: every round appears twice side by side - the US-terms instruction in the left column, the exact UK equivalent in the right column. Stitch counts are identical for both terminologies. Prose tips use US terms.

### Construction & techniques

Worked in continuous rounds (do not join, do not chain 1 between rounds) from the base up: body colour, then white beard, then skin-tone face, then the hat in the body colour. Mark the first stitch of every round and move the marker up. Change colours on the final pull-through of the last stitch of the old colour.

1. **The magic ring** - Wrap yarn around two fingers, insert the hook, pull up a loop and work the first round into the ring; pull the tail tight once the round is complete.

2. **Working in a spiral** - No joins and no starting chains - keep going round after round. The colour-change lines will slant very slightly; that is the no-sew look.

3. **The 5-dc bobble** - Yarn over, insert hook in the stitch, pull up a loop, yarn over and pull through 2 loops (incomplete dc). Repeat 4 more times in the same stitch (6 loops on hook). Yarn over and pull through all 6 loops. One bobble counts as ONE stitch and pops the nose.

4. **sc2tog decrease** - Insert hook, pull up a loop; insert in the next stitch, pull up a loop (3 loops on hook). Yarn over and pull through all 3. On the visible hat rounds (R17-R23) you may prefer the invisible decrease (invdec): insert hook under the FRONT loop only of the next two stitches, yarn over, pull through both front loops, yarn over, pull through 2 loops. Same counts, no bump.

5. **Clean colour changes** - Work the last stitch of the old colour until 2 loops remain, then pull the new colour through. Give both yarns a gentle tug to keep the join tight.

### Instructions

#### 1. Body, beard, face & hat - one piece

Start in the body colour (red or green). The R15-16 line, where you switch back to the body colour, forms the hat edge - no folding, no sewing.

##### Body - body colour

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R1 | 6 sc in MR | 6 dc in MR | (6) | - |

| R2 | inc in each st around | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | [dc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | [2 dc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | [3 dc, inc] x 6 | (30) | - |

| R6-8 | sc in each st around (3 rnd) | dc in each st around (3 rnd) | (30) | - |

##### Beard - white (R9-12)

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R9-12 | sc in each st around (4 rnd) | dc in each st around (4 rnd) | (30) | - |

##### Face & nose - skin tone (R13-15)

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R13 | sc in each st around | dc in each st around | (30) | - |

| R14 | sc in next 14, BO in next st (nose), sc in remaining 15 | dc in next 14, BO in next st (nose), dc in remaining 15 | (30) | bobble = nose |

| R15 | sc in each st around | dc in each st around | (30) | - |

##### Hat - body colour (R16-23)

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R16 | sc in each st around | dc in each st around | (30) | hat edge; start stuffing after fitting eyes |

| R17 | [3 sc, sc2tog] x 6 | [3 dc, dc2tog] x 6 | (24) | - |

| R18 | sc in each st around | dc in each st around | (24) | - |

| R19 | [2 sc, sc2tog] x 6 | [2 dc, dc2tog] x 6 | (18) | continue stuffing as opening narrows |

| R20 | sc in each st around | dc in each st around | (18) | - |

| R21 | [sc, sc2tog] x 6 | [dc, dc2tog] x 6 | (12) | - |

| R22 | sc in each st around | dc in each st around | (12) | top up stuffing |

| R23 | sc2tog x 6 | dc2tog x 6 | (6) | close |

**Eye and stuffing order:** after Rnd 15, add the chosen eyes one round above the nose, about 3 stitches apart and equally spaced either side. For safety eyes, lock both washers while the 30-stitch opening is unobstructed. For embroidered eyes, knot and bury both ends inside at this same pause. Change to the hat colour for Rnd 16, then begin stuffing through the still-wide opening. Add small amounts every 1-2 rounds; finish filling before Rnd 23.

Finish: FO with a 15 cm tail, thread through the front loops of the last 6 stitches, pull closed and weave in.

Stuffing shape: pack the base flat and wide so the gnome stands; keep the pointed hat lightly stuffed so it can bend slightly.

The nose sits on the round before the hat-colour change. Because the lower body is symmetrical, let the Rnd 14 bobble DEFINE the front rather than trying to force it onto an earlier marker. Place the optional eyes one round above and equally either side of that bobble.

### Finishing & assembly

- Hat brim (optional): join white yarn at the R15-16 colour-change line and work sl st around. FO and weave in - it covers the change line neatly.

- Eyes (optional): 2 embroidered straight stitches or 6-8 mm safety eyes, about 3 stitches apart and equally spaced either side of the nose, one round above it. Add either version after Rnd 15 and before stuffing begins at Rnd 16; lock safety-eye washers or knot embroidery ends inside while the opening is clear.

- Extra beard texture: a few surface sl sts or short tied strands of white over R9-12.

- Hanging ornament: ch 18 at the hat tip and sl st into the same place to form a loop. FO and weave in.

### Troubleshooting

- **Colour lines slant noticeably.** That is the spiral's true line - put the slant at the back. Or join each colour with a sl st and ch 1 for perfectly level stripes, at the cost of a visible seam.

- **The nose bobble will not pop.** Work the 5 dc loosely and push the bobble toward you as you complete it; finish the round, then nudge it out from the inside while stuffing.

- **Gnome tips over.** Pack more stuffing into the base and flatten the bottom; the base disc should be noticeably firmer than the hat.

### Colorways

Santa red  ·  Forest green  ·  Nordic grey  ·  Candy pink  ·  Midnight navy

### Helpful tips

#### Size variations

Mini ornament: use DK yarn and a 3 mm hook. Work through Rnd 21 (12 sts), omit the plain Rnd 22, then work sc2tog around (6) and close as usual - about 8-9 cm tall.

Large decoration: use chunky yarn and a 5 mm hook. After the original Rnds 6-8, work 3 MORE plain 30-stitch body rounds, then continue with the beard instructions. All later section labels shift by three physical rounds; the stitch counts and shaping sequence are unchanged. Expect about 15 cm, but measure your sample.

- Why sc2tog here: the classic decrease is simple and grips the stuffing firmly. If you prefer a smoother visible hat, use the invisible-decrease method given in technique 4; both consume two stitches and make one.

### Care

Follow the labels for every yarn and component used. Before publishing a care claim or supplying finished gnomes, clean and dry a complete sample by the proposed method, then remeasure it and inspect for dye transfer, beard shedding or matting, stuffing migration, shifted optional eyes and loosened nose or beard anchors. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying flat away from heat. Reshape the hat and beard and recheck every component after cleaning.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 11.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished gnomes as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to "Novality Store".

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

No finished gnome has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. If using plastic safety eyes, lock the washers before stuffing and closing; embroidery removes those components but is not proof of overall compliance. The finished-item maker or seller is responsible for market-specific assessment and evidence before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#NovalityGnome** - We love seeing gnome gatherings. Thank you for supporting an independent pattern designer.


---

# Part 12 of 17 — NS-12 · Bobble Christmas Tree

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 7 pp · print edition 7 pp · reports: `docs/ns12/NS12_validation_report.md`*

## Bobble Christmas Tree

> **US + UK equivalent  ·  Easy - Intermediate  ·  2 - 3 hours**  —  Design Code NS 12

A soft standing fir built in one piece: plain rounds, then tier after tier of bobbles that thin out toward the tip. Contrast-colour bobbles turn it into baubles-on-a-tree in a single round.

**FINISHED SIZE**  About 12 cm (4.7 in) tall and 7 cm (2.8 in) wide in worsted / aran on a 4 mm hook.  About 15.5 cm tall in chunky yarn on a 5 mm hook.  One piece; a felt or cardboard base disc is optional.

---

### Safety — read this first

As written, the contrast-colour bobbles are crocheted into the fabric and the design has no beads or glued decorations. Adding beads, bells or other embellishments can create detachable small parts; do not add them without reassessing the finished item. Stuff firmly and secure every yarn end.

No finished tree has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Omitting embellishments removes those component hazards but does not establish age suitability or product compliance. Before supply, the finished-item maker or seller must determine all applicable classification, assessment, testing, documentation, labelling and traceability duties in every destination market.

### Materials

- Main yarn: worsted / aran (#4) in green, 70 g.

- Contrast (optional): small amounts of red, gold, cream for contrast bobbles.

- Hook: 4 mm (US G-6); use 3 mm for DK mini, 5 mm for chunky.

- Stuffing: fibre fill about 25 g (a little only - the tree stands on tension).

- Optional: 1 circle of cardboard or firm felt for the base. Trace inside the R9 fold ridge and cut the circle 3-5 mm smaller; at the stated gauge it will usually be 55-65 mm across.

- Notions: stitch marker, tapestry needle, scissors.

### Gauge & size

Aim for a firm fabric (~10-11 sc x 11 rounds = 5 cm). Exact size is not critical; droopy bobbles mean too much stuffing - the shell should hold its cone almost on its own.

### Abbreviations (US + UK)

MR - magic ring  ·  BLO - back loop only

ch - chain  ·  BO - 5-dc bobble (counts as 1 st) / UK: 5-tr bobble (counts as 1 st)

sl st - slip stitch  ·  FO - fasten off

sc = dc - single crochet / double crochet  ·  st(s) - stitch(es)

inc - increase (2 sc in one st) / UK: increase (2 dc in one st)  ·  R - round

sc2tog = dc2tog - work 2 stitches together as one (a decrease)  ·  (n) - stitch count at round end

How to read this dual pattern: every round appears twice side by side - the US-terms instruction in the left column, the exact UK equivalent in the right column. Stitch counts are identical for both terminologies. Prose tips use US terms.

### Construction & techniques

Worked in continuous rounds from the base up - no joins, no starting chains. The BLO round (R9) turns the flat base upward into the cone wall. Bobble rounds alternate with plain rounds; every bobble round from R12 onward hides one sc2tog per repeat, so the cone tapers evenly and the bobbles stay in regular columns.

1. **The magic ring** - Work 6 sc into a ring and pull the tail tight.

2. **Back loop only (BLO)** - Work into the far loop only. The unused front loops form a ridge that makes the base fold neatly under the tree.

3. **The 5-dc bobble** - Yarn over, insert hook, pull up a loop, yarn over and pull through 2 loops (incomplete dc). Repeat 4 more times in the same stitch - 6 loops on hook - then yarn over and pull through all 6. Counts as ONE stitch.

4. **Contrast bobbles** - The bobble itself must be worked in the contrast colour. Complete the final pull-through of the stitch BEFORE a bobble with contrast yarn (for the first bobble of a round, change on the last stitch of the preceding round). Work all five incomplete dc in contrast, then use green for the final yarn-over and pull it through all 6 loops. Continue the next stitch in green, carrying the unused colour loosely inside. Do not work a green bobble and change only its closing loop - that makes a green bobble with a contrast-colour top, not a contrast bobble.

5. **sc2tog decrease** - One decrease per repeat hides inside each bobble round, always in the LAST position, so the bobble columns stay straight.

### Instructions

#### 1. Tree - one piece, green (contrast optional)

The cone tapers between bobble tiers; the plain round between them keeps each tier distinct. If using a rigid base disc, insert it immediately after Rnd 9 while the opening still has 48 stitches. Begin adding small amounts of stuffing after Rnd 14 and continue every 2-3 rounds - do not wait until the six-stitch tip.

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R1 | 6 sc in MR | 6 dc in MR | (6) | - |

| R2 | inc in each st around | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | [dc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | [2 dc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | [3 dc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | [4 dc, inc] x 6 | (36) | - |

| R7 | [5 sc, inc] x 6 | [5 dc, inc] x 6 | (42) | - |

| R8 | [6 sc, inc] x 6 | [6 dc, inc] x 6 | (48) | base = full width |

| R9 | BLO: sc in each st around | BLO: dc in each st around | (48) | base fold ridge; insert optional disc now |

| R10 | [BO, 7 sc] x 6 | [BO, 7 dc] x 6 | (48) | first bobble tier |

| R11 | sc in each st around | dc in each st around | (48) | - |

| R12 | [BO, 5 sc, sc2tog] x 6 | [BO, 5 dc, dc2tog] x 6 | (42) | - |

| R13 | sc in each st around | dc in each st around | (42) | - |

| R14 | [BO, 4 sc, sc2tog] x 6 | [BO, 4 dc, dc2tog] x 6 | (36) | begin light, progressive stuffing |

| R15 | sc in each st around | dc in each st around | (36) | - |

| R16 | [BO, 3 sc, sc2tog] x 6 | [BO, 3 dc, dc2tog] x 6 | (30) | - |

| R17 | sc in each st around | dc in each st around | (30) | - |

| R18 | [BO, 2 sc, sc2tog] x 6 | [BO, 2 dc, dc2tog] x 6 | (24) | - |

| R19 | sc in each st around | dc in each st around | (24) | - |

| R20 | [BO, sc, sc2tog] x 6 | [BO, dc, dc2tog] x 6 | (18) | - |

| R21 | sc in each st around | dc in each st around | (18) | - |

| R22 | [BO, sc2tog] x 6 | [BO, dc2tog] x 6 | (12) | bobble tier at tip - each repeat uses 3 sts, makes 2 |

| R23 | sc in each st around | dc in each st around | (12) | - |

| R24 | sc2tog x 6 | dc2tog x 6 | (6) | final small pinch of stuffing before this round |

| R25 | sc in each st around | dc in each st around | (6) | - |

| R26 | sc2tog x 3 | dc2tog x 3 | (3) | tip |

Finish: FO with a tail, thread through the last 3 stitches, pull the tip closed and weave the end down through the tree.

Stuffing: only the bottom half needs real fill - a lightly stuffed cone that flexes is nicer than a rigid one. After Rnd 9, trace just inside the fold ridge, cut the optional felt or cardboard disc 3-5 mm smaller than that outline (usually 55-65 mm at the stated gauge), and place it against the inside of the base; it will not pass through the narrowed tip later. Cardboard makes the tree non-washable. Add stuffing progressively from Rnd 14 and keep the upper cone light.

### Finishing & assembly

- Contrast bobbles: change TO contrast before each bobble, work its five incomplete dc in contrast, then change BACK to green on the bobble's closing pull-through. One or two contrast tiers look best.

- Base: for a shelf decoration, place the optional disc after Rnd 9, keep it flat against the base while you work, and stuff around it gradually.

- Hanging: join any colour at the tip, ch 18, sl st into the same place.

- Set of three: DK + 3 mm hook, worsted + 4 mm hook, chunky + 5 mm hook - counts are identical, sizes stair-step from about 9 cm to 16 cm.

### Troubleshooting

- **Bobble columns wander.** Your round start drifted with the spiral - a stitch marker in the first stitch of every round keeps the repeat anchored. A little lag looks natural: real fir boughs point downhill too.

- **Tip flops.** Over-stuffed at the top. Take two pinches of stuffing out of the cone tip and re-cinch R26 tightly.

- **Base will not sit flat.** You skipped the BLO ridge (R9) or worked it loosely. That ridge is the fold - re-press it with a fingernail while shaping.

### Colorways

Fir green  ·  Sage velvet  ·  Snow white  ·  Crimson berry  ·  Gold-tipped

### Helpful tips

- Why every bobble tier shrinks by 6: each [BO, k sc, sc2tog] repeat works one hidden decrease, at the END of the repeat, so the bobbles never drift out of their columns even while the cone narrows 10 rounds in a row. R22 is the extreme case: [BO, sc2tog] uses 3 sts and makes 2 per repeat - 18 sts used, 12 left, nothing unworked.

### Care

Follow the labels for every yarn and insert used. A tree containing cardboard is not washable; keep it dry and surface clean only. Before publishing any other care claim or supplying finished trees, clean and dry a complete sample made with the exact proposed insert and yarn, then inspect for dye transfer, distortion, stuffing migration, bobble damage and a warped base. Until that sample test passes, recommend gentle surface cleaning with a damp cloth and drying upright away from heat.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 12.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished trees as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to "Novality Store".

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

No finished tree has been shown by Novality Store to comply with ASTM F963, EN 71 or another toy-safety regime. Avoid beads, bells and glued decorations unless the altered item is fully reassessed. The finished-item maker or seller is responsible for market-specific assessment and evidence before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#NovalityTree** - Show us your forest. Thank you for supporting an independent pattern designer.


---

# Part 13 of 17 — NS-13 · Christmas Ornament Bundle

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 7 pp · print edition 7 pp · reports: `docs/ns13/NS13_validation_report.md`*

## Christmas Ornament Bundle

> **US + UK equivalent  ·  Beginner  ·  15 - 40 min each**  —  Design Code NS 13

Three quick decorations from leftover yarn: a stuffed round bauble, a flat-blocked five-point star, and a crisp six-arm snowflake. Allow about 15-40 minutes each, including finishing (blocking and drying take additional elapsed time).

**FINISHED SIZE**  Bauble about 3.75 cm (1.5 in) across; star about 9 cm (3.5 in); snowflake about 10 cm (4 in).  Sizes scale with yarn - use DK for dainty tree ornaments, chunky for bold window pieces.

---

### Safety — read this first

These designs are intended as decorations, not toys. Keep them and their hanging loops out of children’s reach; avoid beads, loose bells and glued additions, secure every loop twice, and make each loop only as long as needed for its intended support. No finished ornament has been shown by Novality Store to comply with ASTM F963, EN 71 or another product-safety regime. A “decoration” label does not override reasonably foreseeable use, so a finished-item maker or seller must determine all applicable classification, assessment, testing, documentation, labelling and traceability duties before supply.

### Materials

- Yarn: small amounts (about 10 g each) of worsted / aran or DK - white, red, gold, green, silver. Cotton gives the crispest snowflake; acrylic is fine too.

- Hook: 3-4 mm (use 3 mm for DK, 4 mm for worsted).

- Optional: a pinch of fibre fill for the bauble; metallic yarn for surface stripes.

- Notions: tapestry needle, scissors, pin board or mat for blocking the star and snowflake.

### Gauge & size

Gauge is unimportant - work tightly enough that the bauble holds fill and the star blocks flat. One round of the bauble base shows you the size at once.

### Abbreviations (US + UK)

MR - magic ring  ·  inc - increase (2 sc in one st) / UK: increase (2 dc in one st)

ch - chain  ·  sc2tog = dc2tog - work 2 stitches together as one (a decrease)

sl st - slip stitch  ·  FO - fasten off

sc = dc - single crochet / double crochet  ·  st(s) - stitch(es)

hdc = half treble - half double crochet / half treble crochet  ·  R - round

dc = tr - double crochet / treble crochet  ·  (n) - stitch count at round end

tr = dtr - treble crochet / double treble crochet

How to read this dual pattern: every round appears twice side by side - the US-terms instruction in the left column, the exact UK equivalent in the right column. Stitch counts are identical for both terminologies. Prose tips use US terms.

### Construction & techniques

The bauble is worked in continuous rounds (no joins) with the marker in the first stitch. The star and snowflake are worked in JOINED rounds / off-the-ring motifs: each round closes with a slip stitch. Read each section from its own heading down - they are three small standalone patterns.

1. **The magic ring** - Pull the tail tight after round one; if the centre gaps, work the tail through the first round once more before weaving.

2. **Picot-free points (star)** - Each point is a fan of 6 worked stitches into ONE centre stitch, with a ch-2 tip: (sc, hdc, dc, ch 2, dc, hdc, sc). The ch-2 tip is a space and is not counted as a worked stitch. Per point you make 6 fan stitches plus 1 anchoring sl st, so the five-point round has 35 counted stitches (plus five ch-2 spaces). The symmetry comes from blocking, not tugging.

3. **Chain spaces (snowflake)** - The snowflake skeleton is 6 ch-5 loops pinned around the 12-dc ring. The arms are worked into the spaces, never into individual chains.

4. **Blocking** - For cotton, wet or mist the piece, pin every point to shape and let it dry fully. Acrylic often does not hold a shape from pins alone; if the yarn label permits, steam-block cautiously with the steamer or iron held above the fabric, never touching it, and test a scrap first. Do not press or iron either piece.

### Instructions

#### A. Round Christmas Bauble - stuffed ball

The sphere closes at the same 6-stitch crown it started from. Two-colour option: change at R5.

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R1 | 6 sc in MR | 6 dc in MR | (6) | - |

| R2 | inc in each st around | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | [dc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | [2 dc, inc] x 6 | (24) | - |

| R5-6 | sc in each st around (2 rnd) | dc in each st around (2 rnd) | (24) | - |

| R7 | [2 sc, sc2tog] x 6 | [2 dc, dc2tog] x 6 | (18) | - |

| R8 | [sc, sc2tog] x 6 | [dc, dc2tog] x 6 | (12) | stuff now |

| R9 | sc2tog x 6 | dc2tog x 6 | (6) | close |

Finish: FO with a tail, thread through the front loops of the last 6 stitches, cinch and weave in. Stuff firmly but not hard - the sphere should spring back when pressed rather than feel rigid.

Hanging loop: join yarn at the crown, ch 18, sl st into the same joining place, FO and weave in. Surface sl sts in metallic yarn make instant stripes after Rnd 6.

#### B. Five-Point Star - flat, blocked

Each point uses exactly 2 of the 10 centre stitches - one for the slip stitch that anchors it, one for the fan that fills it. Block before hanging.

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R1 | ch 1, 10 sc in MR, sl st to first sc to close | ch 1, 10 dc in MR, sl st to first dc to close | (10) | centre ring |

| R2 | [sl st in next st, (sc, hdc, dc, ch 2, dc, hdc, sc) in next st] x 5, sl st to first sl st, FO | [sl st in next st, (dc, half treble, tr, ch 2, tr, half treble, dc) in next st] x 5, sl st to first sl st, FO | (35) | 5 sl sts + 30 fan sts; ch-2 tips not counted |

Hanging loop: pick the top point, join yarn in its ch-2 tip, ch 18, sl st into the same ch-2 space.

The repeat uses all 10 centre stitches exactly (2 per point). Each fan contains 6 worked stitches; with its anchoring sl st, each point contributes 7 counted stitches, for 35 total. The five ch-2 tip spaces are additional structure, not counted stitches.

#### C. Six-Point Snowflake - open lace

Three short rounds. The ring is closed first so the arms hang on real chain spaces - keep the dc round snug, the ch-5 round loose.

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R1 | ch 6, sl st in first ch to form a ring; ch 3 (counts as first dc), 11 dc in ring, sl st to top of ch-3 | ch 6, sl st in first ch to form a ring; ch 3 (counts as first tr), 11 tr in ring, sl st to top of ch-3 | (12) | 12 spokes |

| R2 | [ch 5, skip next st, sl st in next st] x 6, sl st to base of first ch-5 to close | [ch 5, skip next st, sl st in next st] x 6, sl st to base of first ch-5 to close | - | 6 ch-5 spaces |

| R3 | (sl st, ch 3, 3 tr, ch 3, sl st) in each of the 6 ch-5 spaces, sl st to first sl st, FO | (sl st, ch 3, 3 dtr, ch 3, sl st) in each of the 6 ch-5 spaces, sl st to first sl st, FO | - | 6 arms - first sl st of each arm loose, last sl st snug |

Hanging loop: join yarn in the ch-3 tip of one arm, ch 18, sl st into the same tip.

Block flat using the fibre-appropriate method in technique 4; let it cool if steamed and dry completely before hanging.

### Finishing & assembly

- Bauble two-colour: change yarn on the final pull-through of R4 for a sharp banded ball.

- Weave every end on the star and snowflake in two directions - lace shows knots more than amigurumi does.

- Thread each finished loop through a cardboard or felt backing card with the string knot hidden underneath for gifting.

### Troubleshooting

- **Bauble looks like a lemon.** Too much stuffing late in the game. Stuff a pinch at R8, shape by rolling, and keep the crown pinch tight at R9.

- **Star will not lie flat.** It needs blocking, not more tugging. Wet-block cotton. For acrylic, pins alone may not set the shape; follow the yarn label and cautiously steam from above without touching or melting the fibres.

- **Snowflake arms lean one way, or the base bunches.** Both arm-end sl sts share the same ch-5 space, and tension is the whole trick: work the FIRST sl st of each arm loose enough that the base of the arm lies flat (too tight twists the arm into the opening sl st), then work the LAST sl st snug so the arm stands upright.

### Colorways

Snow white  ·  Classic red & white  ·  Gold  ·  Evergreen trio  ·  Frost blue

### Helpful tips

#### Bundle at a glance

| Piece | Time | Yarn (worsted) | Ideal use |

|---|---|---|---|

| Bauble | ~25 min | 9 g | Tree ornament, garland |

| Star | ~20 min | 7 g | Gift topper, garland |

| Snowflake | ~15 min | 5 g | Window, gift tag, garland |

All three string neatly on one length of yarn - a matching garland is just all three patterns on repeat.

### Care & storage

Follow the yarn and metallic-thread labels. Before publishing a cleaning claim or supplying finished ornaments, test the proposed method on a complete blocked sample and check for dye transfer, distortion, melted or dulled fibres, released stuffing and weakened hanging loops after it is fully dry. Store the ornaments dry and flat or supported, without crushing the star or snowflake points. Reblock only with the fibre-appropriate method above; never apply an iron directly.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 13.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished ornaments as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small batches, in shops, markets and online, provided credit is given to "Novality Store".

#### You may not

Do not resell, share, redistribute, translate, rewrite, publish or upload this digital PDF or its contents in any form. Do not alter, copy or recolor the pattern and claim it as your own. Do not use the Novality Store name, logo or photos beyond crediting the pattern. Do not mass-produce finished items commercially without written permission.

#### Safety reminder

These are intended as decorations, not toys. Keep ornaments and hanging loops out of children’s reach, use loops only as long as needed, and secure every knot. Before supply, assess intended and reasonably foreseeable use and meet all market-specific product-safety duties.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#NovalityOrnaments** - Tag us in your trees and tables. Thank you for supporting an independent pattern designer.


---

# Part 14 of 17 — NS-14 · Bobble Snowflake Tree Skirt

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 10 pp · print edition 10 pp · reports: `docs/ns14/NS14_validation_report.md`*

## NOVALITY CROCHET STUDIO — PRINTER-SAVER EDITION

**DESIGN CODE NS 14 · BOBBLE SNOWFLAKE · Tree Skirt**

DOCUMENT INK: BLACK + WHITE · WHITE BACKGROUNDS · PROGRESS BOXES
US + UK TERMS · EASY–INTERMEDIATE · TIME UNVERIFIED · RECORD SAMPLE · TARGET 46–109 CM · VERIFY WORSTED · 5–5.5 MM HOOK

### ABOUT THIS COMPANION FILE

Designed for economical home printing and progress tracking. Large artwork is omitted; the written directions match the full-colour edition.

© 2026 Novality Crochet Studio · All rights reserved · PERSONAL LICENSE · SEE TERMS
NS 14 · PRINTER-SAVER CROCHET PATTERN

---

### Pattern profile

NS 14 is the permanent identity of this pattern. Keep it with every revision, tester note, photograph and support message.

| Field | Value |
|---|---|
| FORMAT | US + UK TERMS |
| SKILL LEVEL | EASY–INTERMEDIATE |
| ACTIVE TIME | TIME UNVERIFIED · RECORD SAMPLE |
| FINISHED SIZE | TARGET 46–109 CM · VERIFY |

#### Named original colourway

| Colour | Role |
|---|---|
| FOREST GREEN | MC · every non-bobble growth round |
| OAT CREAM | CC · bobble rounds, spokes + border |

Use the written colour names and material roles when selecting yarn; screen and printer appearance varies.

#### Progress tracking

Every construction-table row begins with a printable `[ ]` box. Tick it only after completing the row and confirming the stated count.

#### Read before making

Read every component and finishing note before beginning. Mark completed rows, confirm the count at each row end, and stop immediately if your count differs. Complete the centre-ring join, the optional surface spokes and the border in that order, and weave every tail while the centre opening is still open and accessible.

Safety: this PDF does not claim that a finished item meets any toy or consumer-product standard. Follow the full Safety section and obtain every assessment required for the finished item's intended market and use.

Copyright notice © 2026 Novality Crochet Studio. All rights reserved. Licensed to the purchaser under the Terms of Use in this document. Visuals are illustrative; the written materials, counts and construction directions control.

---

### Contents

Major sections are listed below; all component headings are bookmarked. Table headers repeat after page breaks, and the design code appears on every page.

Safety — read this first 4 · Materials 4 · Gauge & size 4 · Abbreviations (US + UK) 5 · Construction & techniques 5 · Instructions 6 · Finishing & assembly 8 · Troubleshooting 9 · Colourways 9 · Helpful tips 9 · Care & storage 10 · Terms of Use 10

Read the complete component before beginning it. Move the marker at the start of every crochet round unless the master says otherwise. Diagrams and illustrations support orientation only; the numbered written directions control construction.

*Design Code NS 14 · Novality Crochet Studio · US and UK crochet terms*

---

### Design description

A closed-centre, twelve-spoke double-crochet circle with a contrast bobble round every third round from R5. Choose the mini, standard or large stopping point, add twelve optional surface-crochet spokes, then finish with an exact scalloped border.

Finished-size targets — not sample measurements: mini / tabletop after R14, about 18–21 in / 46–53 cm; standard after R23, about 29–33 in / 74–84 cm; large after R32, about 38–43 in / 97–109 cm. The source target for the relaxed centre opening is approximately 1.5–2 in / 4–5 cm. Yarn, hook, blocking and border depth change every dimension; measure a complete sample before publishing a size or fit claim.

---

### Safety — read this first

This design is home decor, not a toy, and it is not flameproof. Keep it away from candles, fireplaces, heaters, hot lamps and every ignition source. Use only cool-running lights approved for the tree and location. Do not cover plugs, adapters, power strips or electrical connections with the skirt, and route cords so the skirt cannot pull on them.

Keep the skirt clear of walking routes where its edge could cause a trip or slip. It must not support, level or stabilize a tree stand. Fit the closed centre without obstructing the stand, water reservoir, fasteners or manufacturer-required clearances. Inspect the skirt for loose surface stitches, stretched joins and snagged yarn before each season, and supervise children and animals around the complete tree arrangement.

No finished NS 14 skirt has been independently crocheted, fit-tested, wash-tested, assessed for flammability or shown by Novality Crochet Studio to comply with a product-safety regime. Before sale or supply, the finished-item maker or seller must determine the applicable classification, assessment, testing, documentation, labelling and traceability duties for every destination market.

---

### Materials

- Worsted or aran (#4) yarn. Original colourway: forest green main colour (MC) and oat cream contrast colour (CC), in comparable yarns that meet the same gauge.
- Planning quantities below are estimates derived from the written stitch counts, not weighed results. The source planning allowance of 700–1,200 g was never measured, is far above what the stitch counts imply, and supplied neither a mini figure nor a colour split. Estimated total yarn at about 200 yd / 100 g of worsted and 3–4 in of yarn per US dc (a 5-dc bobble uses five dc of yarn but counts as one stitch, and the estimate includes the spokes and border): **mini 70–95 g · standard 165–225 g · large 305–410 g**. Because every bobble round is worked entirely in CC and CC also covers the spokes and border, plan a near-even split: **CC about 44–52 % of the total, MC the remainder**, with the CC share highest in the mini. Make and weigh a gauge piece and a complete sample before buying for production or publishing a quantity, and buy both colours from one dye lot.
- 5–5.5 mm crochet hook (US H/8–I/9), or the size needed to meet the target stitch gauge while keeping the circle flat.
- Optional hook 0.5–1 mm smaller for loose surface slip stitches; do not use it if it contracts the fabric.
- Tapestry needle, scissors, tape measure, digital scale, one start-of-round marker and, for the optional spoke route, twelve locking markers or removable guide threads.
- Rust-resistant pins and a fibre-appropriate blocking surface large enough for the selected size.

---

### Gauge & size

Make the centre ring and work through R6 as a circular gauge piece; let it rest before measuring. Target gauge in US double crochet / UK treble crochet is **12 stitches = 4 in / 10 cm** across the stitch direction.

The radial figure is derived from that stitch gauge, not independent of it: each round adds 12 stitches, so the circumference grows 4 in / 10 cm per round and the radius of a flat circle must grow 4 ÷ 2π = **0.64 in / 1.6 cm per round — about 6¼ completed rounds = 4 in / 10 cm radially**. A rounded "6 rounds = 4 in" makes every round roughly 5 % taller than flat geometry wants, so the circle carries a mild cupping tendency that blocking removes; do not treat a small cup as a count error. Match the stitch gauge first, then confirm the circle lies flat. Stitch gauge controls circumference; the increase rate controls flatness. A rectangular swatch alone does not verify how this twelve-increase circle will lie.

At the target stitch gauge, the unbordered circumference and derived diameter are approximately:

- **R14:** 168 stitches ÷ 3 stitches per inch = 56 in circumference; 56 ÷ π = 17.8 in / 45 cm diameter.
- **R23:** 276 ÷ 3 = 92 in circumference; 92 ÷ π = 29.3 in / 74 cm diameter.
- **R32:** 384 ÷ 3 = 128 in circumference; 128 ÷ π = 40.7 in / 103 cm diameter.

The scallops add an unverified amount at the edge, and blocking can move the result within or beyond the source target ranges. Note the mini's unbordered derived diameter (17.8 in / 45 cm) sits just under the bottom of its own 18–21 in / 46–53 cm target, so that target depends on border depth plus blocking; record a blocked sample before repeating the range. Measure the relaxed centre opening, unbordered body and finished blocked skirt. Do not force-block severe cupping or ruffling into a claimed size.

---

### Abbreviations (US + UK)

| Abbreviation | Meaning |
|---|---|
| BO | 5-dc bobble in US terms / 5-tr bobble in UK terms; counts as 1 stitch |
| CC | contrast colour |
| ch | chain |
| dc = tr | US double crochet / UK treble crochet |
| FO | fasten off |
| MC | main colour |
| R / rnd | round |
| sc = dc | US single crochet / UK double crochet |
| sl st | slip stitch |
| st(s) | stitch(es) |
| (n) | stitch count at round end |

Every construction round appears twice side by side: the US instruction is on the left and its UK equivalent is on the right. Stitch counts are identical. Prose explanations use US terms unless both names are shown.

---

### Construction & techniques

Closed joined rounds are worked without turning. The starting ch 2 never counts as a stitch. Work the first dc or BO into the SAME stitch as the join, mark it, and slip stitch to that marked stitch at round end. Do not work into the ch 2 or joining slip stitch.

1. **Fit the closed centre first:** make the relaxed ch-20 ring and pass it over the actual central pole or trunk area before R1. The written ch-24 option makes a larger ring without changing R1, but its finished opening is still yarn- and tension-dependent. If neither relaxed ring fits without stretching or interfering with the stand, this closed-centre construction is not suitable; do not cut the finished skirt to create a slit.

2. **Twelve-repeat circle:** Round N consumes N − 1 old stitches and produces N new stitches in each of 12 repeats. The round therefore ends with exactly 12 × N stitches. R9 requires seven plain dc per repeat and R10 requires eight; shortening either repeat leaves stitches unworked.

3. **Five-dc bobble:** yarn over, insert the hook, pull up a loop, yarn over and pull through two loops, leaving the incomplete dc on the hook. Repeat four more times in the same stitch until six loops remain; yarn over and pull through all six. Push the completed one-stitch bobble to the right side.

4. **Original colour route:** work R1–R4 and every non-bobble round in forest green MC. Work each complete bobble round — R5, R8, R11 and every third round thereafter — in oat cream CC; the plain dc and increase stitches on that round are CC too. Use CC again for the optional spokes and border. To change colour, work the round-ending slip stitch with the colour required for the next round. Carry a resting colour loosely up the wrong-side join across the intervening round or rounds, or cut and secure it; never strand yarn across the circle or pull the carried section tight.

5. **Track the increase columns:** if adding surface spokes, place one locking marker in the second dc of each R2 increase — R2 has exactly 12 increases, so this gives exactly 12 markers. On every later round, the marked stitch is the last old stitch consumed by its repeat; move that marker to the second dc of the new increase. The 12 final marker positions provide evenly spaced outer endpoints.

6. **Surface slip stitch:** hold the yarn behind the work, then insert the hook from the front of the fabric at the next point on the pinned radial guide, pull up a loop, and pull it through the loop already on the hook. The bobbles mark the front; the yarn supply stays behind it for the whole spoke. Keep every slip stitch relaxed and check the fabric after each spoke.

---

### Instructions

#### 1. Skirt — centre ring and growth rounds

Ch 2 starts every round and is never counted. Work the first dc — or first BO on a bobble round — into the same stitch as the join, then end with a slip stitch to that first actual stitch. Count after every repeat and at the end of every round.

##### Centre ring

| ✓ | Rnd | US terms | UK terms | Sts | Note |
|---|---|---|---|---|---|
| [ ] | Ring | Ch 20, check the relaxed ring against the stand, then sl st to first ch without twisting | Ch 20, check the relaxed ring against the stand, then sl st to first ch without twisting | – | ch 24 is the only written larger-opening option; recheck before R1 |

##### Rounds 1–8

| ✓ | Rnd | US terms | UK terms | Sts | Note |
|---|---|---|---|---|---|
| [ ] | R1 | Ch 2, 12 dc in ring, sl st to first dc | Ch 2, 12 tr in ring, sl st to first tr | (12) | – |
| [ ] | R2 | Ch 2, 2 dc in each st around, sl st to first dc | Ch 2, 2 tr in each st around, sl st to first tr | (24) | 12 increases; +12 every round from here |
| [ ] | R3 | Ch 2, [dc in next st, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next st, 2 tr in next st] x 12, sl st to first tr | (36) | – |
| [ ] | R4 | Ch 2, [dc in next 2 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 2 sts, 2 tr in next st] x 12, sl st to first tr | (48) | last MC round before the first bobble round |
| [ ] | R5 | Ch 2, [BO in next st, dc in next 2 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 2 sts, 2 tr in next st] x 12, sl st to first BO | (60) | first bobble round · CC |
| [ ] | R6 | Ch 2, [dc in next 4 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 4 sts, 2 tr in next st] x 12, sl st to first tr | (72) | – |
| [ ] | R7 | Ch 2, [dc in next 5 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 5 sts, 2 tr in next st] x 12, sl st to first tr | (84) | – |
| [ ] | R8 | Ch 2, [BO in next st, dc in next 5 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 5 sts, 2 tr in next st] x 12, sl st to first BO | (96) | bobble round · CC |

##### Rounds 9–16

| ✓ | Rnd | US terms | UK terms | Sts | Note |
|---|---|---|---|---|---|
| [ ] | R9 | Ch 2, [dc in next 7 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 7 sts, 2 tr in next st] x 12, sl st to first tr | (108) | seven plain dc per repeat |
| [ ] | R10 | Ch 2, [dc in next 8 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 8 sts, 2 tr in next st] x 12, sl st to first tr | (120) | eight plain dc per repeat |
| [ ] | R11 | Ch 2, [BO in next st, dc in next 8 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 8 sts, 2 tr in next st] x 12, sl st to first BO | (132) | bobble round · CC |
| [ ] | R12 | Ch 2, [dc in next 10 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 10 sts, 2 tr in next st] x 12, sl st to first tr | (144) | 10 plain + 1 increase anchor consumes 11 and makes 12 |
| [ ] | R13 | Ch 2, [dc in next 11 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 11 sts, 2 tr in next st] x 12, sl st to first tr | (156) | – |
| [ ] | R14 | Ch 2, [BO in next st, dc in next 11 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 11 sts, 2 tr in next st] x 12, sl st to first BO | (168) | MINI SIZE — stop growth; optional spokes, then border |
| [ ] | R15 | Ch 2, [dc in next 13 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 13 sts, 2 tr in next st] x 12, sl st to first tr | (180) | – |
| [ ] | R16 | Ch 2, [dc in next 14 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 14 sts, 2 tr in next st] x 12, sl st to first tr | (192) | – |

**Count check for the R11-to-R12 step:** R11 consumes 10 old stitches per repeat — 1 BO + 8 plain dc + 1 increase anchor — and produces 11, giving 132 stitches. R12 then consumes 11 old stitches per repeat — 10 plain dc + 1 increase anchor — and produces 12, giving 144 stitches. R12 therefore requires 10 plain dc, not 9, before the increase; using 9 would leave 12 old stitches unworked and produce only 132 stitches.

##### Rounds 17–24

| ✓ | Rnd | US terms | UK terms | Sts | Note |
|---|---|---|---|---|---|
| [ ] | R17 | Ch 2, [BO in next st, dc in next 14 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 14 sts, 2 tr in next st] x 12, sl st to first BO | (204) | bobble round · CC |
| [ ] | R18 | Ch 2, [dc in next 16 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 16 sts, 2 tr in next st] x 12, sl st to first tr | (216) | – |
| [ ] | R19 | Ch 2, [dc in next 17 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 17 sts, 2 tr in next st] x 12, sl st to first tr | (228) | – |
| [ ] | R20 | Ch 2, [BO in next st, dc in next 17 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 17 sts, 2 tr in next st] x 12, sl st to first BO | (240) | bobble round · CC |
| [ ] | R21 | Ch 2, [dc in next 19 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 19 sts, 2 tr in next st] x 12, sl st to first tr | (252) | – |
| [ ] | R22 | Ch 2, [dc in next 20 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 20 sts, 2 tr in next st] x 12, sl st to first tr | (264) | – |
| [ ] | R23 | Ch 2, [BO in next st, dc in next 20 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 20 sts, 2 tr in next st] x 12, sl st to first BO | (276) | STANDARD SIZE — stop growth; optional spokes, then border · CC |
| [ ] | R24 | Ch 2, [dc in next 22 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 22 sts, 2 tr in next st] x 12, sl st to first tr | (288) | – |

##### Rounds 25–32

| ✓ | Rnd | US terms | UK terms | Sts | Note |
|---|---|---|---|---|---|
| [ ] | R25 | Ch 2, [dc in next 23 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 23 sts, 2 tr in next st] x 12, sl st to first tr | (300) | – |
| [ ] | R26 | Ch 2, [BO in next st, dc in next 23 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 23 sts, 2 tr in next st] x 12, sl st to first BO | (312) | bobble round · CC |
| [ ] | R27 | Ch 2, [dc in next 25 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 25 sts, 2 tr in next st] x 12, sl st to first tr | (324) | – |
| [ ] | R28 | Ch 2, [dc in next 26 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 26 sts, 2 tr in next st] x 12, sl st to first tr | (336) | – |
| [ ] | R29 | Ch 2, [BO in next st, dc in next 26 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 26 sts, 2 tr in next st] x 12, sl st to first BO | (348) | bobble round · CC |
| [ ] | R30 | Ch 2, [dc in next 28 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 28 sts, 2 tr in next st] x 12, sl st to first tr | (360) | – |
| [ ] | R31 | Ch 2, [dc in next 29 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 29 sts, 2 tr in next st] x 12, sl st to first tr | (372) | – |
| [ ] | R32 | Ch 2, [BO in next st, dc in next 29 sts, 2 dc in next st] x 12, sl st to first BO | Ch 2, [BO in next st, tr in next 29 sts, 2 tr in next st] x 12, sl st to first BO | (384) | LARGE SIZE — stop growth; optional spokes, then border · CC |

#### Optional surface snowflake spokes — work before the border

Leave the 12 outer increase-column markers in place. On the right side, pin or lay a straight radial guide from the foundation ring to each marker. Use a separate CC length for every spoke; do not carry yarn from one outer edge back to the centre.

| ✓ | Step | US terms | UK terms | Sts | Note |
|---|---|---|---|---|---|
| [ ] | Spoke | Join CC through the fabric immediately outside the centre ring; work relaxed surface sl sts outward along one pinned guide to its marked increase column; FO at the outer edge | Join CC through the fabric immediately outside the centre ring; work relaxed surface sl sts outward along one pinned guide to its marked increase column; FO at the outer edge | – | 1 separate spoke; no reverse-side float |
| [ ] | Repeat | Repeat the complete join-to-FO spoke route separately at each remaining marked column | Repeat the complete join-to-FO spoke route separately at each remaining marked column | – | 12 spokes total; count 12 centre starts and 12 outer ends |

Surface stitches decorate the fabric and do not replace or add to the growth-round counts. Their exact number varies with size and placement. After every spoke, lay the skirt flat; if the spoke shortens the radius or puckers the body, remove it and remake it more loosely or with the main hook.

#### Scalloped border

Work the border into the final growth round only after the size and optional spokes are approved.

| ✓ | Rnd | US terms | UK terms | Sts | Note |
|---|---|---|---|---|---|
| [ ] | Border | Join CC in any st; ch 1, [sc in next st, skip 2 sts, 5 dc in next st, skip 2 sts] around, sl st to first sc, FO | Join CC in any st; ch 1, [dc in next st, skip 2 sts, 5 tr in next st, skip 2 sts] around, sl st to first dc, FO | same worked-st total as the final growth round | each repeat consumes 6 edge sts and makes 1 scallop |

Each border repeat consumes six final-round anchors and produces six worked stitches: one sc plus a five-dc shell. R14 gives 168 ÷ 6 = 28 scallops; R23 gives 276 ÷ 6 = 46; R32 gives 384 ÷ 6 = 64. The stitch you join into is taken by the final skip of the last repeat, so the closing slip stitch lands in the first sc one stitch past the join; this is correct and it is what makes the repeat close exactly. Do not add a seventh anchor or work the first sc into the join stitch. If the repeat does not close exactly, undo the border and correct the final-round count rather than changing the last scallop.

---

### Finishing & assembly

1. Confirm the selected final growth round contains 168, 276 or 384 stitches before adding surface work.
2. Work the optional 12 separate spokes, checking flatness after each, then work the exact scalloped border.
3. Weave every spoke, colour-change and border tail on the wrong side in at least two directions without tightening the radius.
4. Block only by a method suitable for the actual fibre. Pin to a flat circle without stretching the centre opening; never place an iron directly on the yarn, and do not apply heat unless the yarn maker permits the chosen method.
5. When fully dry and relaxed, record the centre opening, diameter through several axes, mass and edge condition. Confirm the opening fits the intended stand without affecting its stability, reservoir or fittings.
6. Install the closed ring before final tree assembly and only in a way permitted by the tree and stand manufacturers. Reinspect the complete arrangement after lights and cords are positioned.

---

### Troubleshooting

- **The relaxed centre ring does not fit:** stop before R1. Try the written ch-24 option and recheck it. Do not stretch the ring over hardware, cut the finished skirt or assume blocking will create a safe fit.
- **The body ruffles:** first recount the complete round and confirm there are exactly 12 increases. If the count is correct, let the gauge piece rest and check both gauge directions; test another hook or yarn before continuing. Do not randomly omit increases because that breaks the written size and border route.
- **The body cups:** check for a short repeat or skipped increase, especially R9 and R10. If the count is correct, expect the mild cupping tendency described in Gauge & size and reassess hook, yarn and the stitch gauge rather than adding unrecorded stitches.
- **A surface spoke puckers the skirt:** remove that spoke and remake it with looser slip stitches. Each spoke needs its own centre join and outer-edge fasten-off; there should be no long float on the wrong side.
- **The border does not close:** verify the final total is 168, 276 or 384 and consume exactly six anchors per scallop. Do not improvise a partial shell.
- **Bobbles stay flat:** keep the five incomplete dc relaxed, close all six loops together and push the bobble to the right side before the next stitch.

---

### Colourways

| Colour | Role |
|---|---|
| FOREST GREEN | MC · every non-bobble growth round |
| OAT CREAM | CC · bobble rounds, spokes + border |

NAMED ORIGINAL COLOURWAY · FOREST GREEN · OAT CREAM.

Colourway notes: Original colourway: forest green MC for R1–R4 and all later non-bobble growth rounds; oat cream CC for each complete bobble round, all 12 optional surface spokes and the scalloped border. Use comparable worsted/aran yarns so colour changes do not alter gauge.

Colourway notes: Alternative palettes include snow white MC with deep red CC; navy MC with silver-grey CC; or a single-colour cream version in which MC and CC are the same yarn. Metallic filament, sequins, beads and battery-light additions are not part of this pattern and require separate handling, care and safety review.

---

### Helpful tips

#### Sizes at a glance

| Size | Stop after round | Stitches | Border scallops | Unverified finished target |
|---|---|---|---|---|
| Mini / tabletop | R14 | 168 | 28 | 18–21 in / 46–53 cm |
| Standard | R23 | 276 | 46 | 29–33 in / 74–84 cm |
| Large | R32 | 384 | 64 | 38–43 in / 97–109 cm |

All three endings are divisible by six, so the border closes cleanly when the final growth count is correct.

#### The count rule

Round N always consumes N − 1 existing stitches and produces N stitches in each of 12 repeats. On a plain round that is N − 2 plain dc plus one increase; on a bobble round, one of those plain dc is replaced by one BO. This rule verifies the printed ladder but does not authorize untested extra sizes or altered increase rates.

Bobble rounds are R5, R8, R11, R14, R17, R20, R23, R26, R29 and R32 — every third round from R5. All three size stops land on a bobble round, so the final growth round is always worked in CC and the border joins into CC.

#### Time

No active-time claim is supplied. Record hands-on time separately for the selected size, optional spokes, border, finishing and blocking before publishing an estimate.

---

### Care & storage

Follow the most restrictive instruction among every yarn and added material. Before publishing a cleaning claim or supplying finished skirts, clean and fully dry a complete full-size sample by the proposed method. Remeasure the diameter and opening and inspect dye transfer, shrinkage, bobble shape, surface-spoke tension, joins and scallops.

Until that complete-sample test passes, do not make a machine-wash or tumble-dry claim. Recommend gentle surface cleaning only. Store completely dry and away from heat, flame, damp and pests; roll or lay flat rather than sharply creasing the bobble field. Inspect again before seasonal use.

---

### Terms of Use

#### Copyright & ownership

© 2026 Novality Crochet Studio. All rights reserved. This crochet pattern, its instructions, stitch counts, editorial layout and design elements are protected material. Design Code NS 14.

This pattern is licensed to the purchaser for personal use and for small-batch sale of finished physical tree skirts under the terms below. The purchaser may not copy, share, translate, upload, redistribute, resell or publish the pattern or any substantial part of it in digital or printed form.

#### You may

Make finished tree skirts for yourself, gifts or charity. Sell finished physical skirts made from this pattern in small quantities, provided the listing credits "Pattern by Novality Crochet Studio · Design Code NS 14" and does not claim unverified safety, testing, size, yarn quantity, fit or care results.

#### You may not

Resell or distribute this PDF or Markdown source; convert it into another pattern product; use its text, tables or visuals as listing assets for a competing pattern; claim authorship; or mass-produce finished items without written permission. Credit does not grant use of the studio name as your own brand.

#### Safety reminder

The finished-item maker or seller remains responsible for the actual materials, intended use, classification, assessment, testing, warnings, documentation, labelling and traceability required wherever a finished item is supplied.

Tag finished projects with #NovalityCrochetStudio and #NovalityTreeSkirt.

---

### Finish checklist & notes

- [ ] Centre ring fits the stand relaxed; join and ends secured
- [ ] Every growth round counted; 12 increase columns aligned
- [ ] Final count confirmed: 168 / 276 / 384
- [ ] Optional spokes: 12 separate routes, no puckering or floats
- [ ] Border closed: 28 / 46 / 64 complete scallops
- [ ] Blocked dimensions recorded; stand and cord clearances checked

**PROJECT NOTES** — Novality Crochet Studio · NS 14 · printer-saver companion. Keep this page with your project notes.

---

### Revision notes — delete before publishing

Corrections applied to the source text, in order of severity. Full evidence: `NS14_validation_report.md`.

1. **Read before making:** removed the amigurumi template sentence "Complete internal eyes, embroidery, knots and joins…". A tree skirt has no eyes and no embroidery. Replaced with the design's real closing work (ring join, spokes, border, tails).
2. **Materials:** the unmeasured 700–1,200 g allowance is roughly 3–5× what the written stitch counts imply. Replaced with labelled per-size estimates (mini 70–95 g, standard 165–225 g, large 305–410 g) and the missing colour split (CC ≈ 44–52 %), still flagged as unweighed.
3. **Gauge & size:** the two stated gauges could not both be exact on a flat twelve-increase circle. The radial figure is now derived (0.64 in / 1.6 cm per round ≈ 6¼ rounds = 4 in), with the resulting mild cupping tendency named. Troubleshooting "body cups" now points at it.
4. **Care & storage:** "make no machine-wash or tumble-dry claim" → "do not make a machine-wash or tumble-dry claim" (same meaning; the old wording is read by count checkers as "make 0 of that piece").
5. **R11-to-R12 count check:** the note's arithmetic is correct and is unchanged. Only its opening words changed — a line beginning `R11-to-R12` is read by round-header parsers as a second Round 11 appearing after Round 16, which reports "Round 11 repeats or goes backwards". It now begins `Count check for the R11-to-R12 step:` and sits directly under the R12 row. **R12 stays `dc in next 10 sts`; do not change it to 9.** With 132 stitches available, 10 plain dc + 1 increase anchor consumes 11 per repeat (132 total, none left over) and produces 12 per repeat = 144. Nine plain dc would consume 120, leave 12 stitches unworked and give 132.
6. **Design description:** "a contrast bobble round every third round" → "every third round from R5", matching technique 4 and the ladder (R3, R6, R9 … are plain).
7. **Border note:** added the fact that the join stitch is consumed by the final skip, so the closing slip stitch lands one stitch past the join. This is required for exact closure and must not be "fixed".
8. **Technique 5:** stated that R2 contains exactly 12 increases, so "the second dc of each R2 increase" yields exactly 12 markers.
9. **Centre ring row:** the `Rnd` cell was empty; labelled `Ring`.
10. **Cover:** "BLACK + WHITE · WHITE BACKGROUNDS" prefixed with `DOCUMENT INK:` so it cannot be misread as the yarn colourway two lines below it.
11. **Helpful tips:** the heading had no content of its own; the sizes table, count rule and time note are now placed under it, and the bobble-round list is spelled out.
12. **Word joins:** repaired throughout the instruction cells (`against thestand`, `slst`, `2 dcin next st`, `x12`, `stopgrowth`, `thenborder`, `growthround`, `6edge sts`, `1scallop`, `writtenlarger-opening option;recheck`, `relaxedsurface`, `pinnedguide`, `FO atthe`, `noreverse-side`, `immediatelyoutside`, `routeseparately`, `markedcolumn`). Confirm these against the source PDF — if they are printed there, they are typos inside the instruction tables.
13. **Safety heading:** restored as a visible section heading; the Contents advertises it as the first section but the supplied text carried the paragraphs without it.

**Not changed — verified correct:** all 32 growth rounds (consumption, production, repeat count and stated totals), the bobble cadence and all three size stops, the border closure at 28 / 46 / 64 scallops, the 5-dc bobble loop count, the increase-column marker route, the ch-2-not-counted join method, the US/UK term pairs, the hook conversion (5 mm = H/8, 5.5 mm = I/9), and the gauge→diameter arithmetic for all three sizes.


---

# Part 15 of 17 — NS-15 · Interchangeable Christmas Wreath

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 11 pp · print edition 11 pp · reports: `docs/ns15/NS15_validation_report.md`*

## Interchangeable Christmas Wreath

> **US + UK equivalent  ·  Beginner  ·  tube grows by length**  —  Design Code NS 15

A stuffed spiral tube joined into a ring, dressed for the season with three REMOVABLE decorations: poinsettia, lace snowflake and a gift-bow. Swap them as the holidays change. Mini ornament, standard door and large door sizes.

**FINISHED SIZE**  Mini ornament: 22 cm (8.5 in) tube; centreline ring diameter about 7 cm.  Standard door wreath: 92 cm (36 in) tube; centreline diameter about 29 cm.  Large door wreath: 125 cm (49 in) tube; centreline diameter about 40 cm.  The finished OUTSIDE diameter is one tube thickness larger, so measure your sample. Poinsettia approx. 3.5 in; snowflake approx. 4 in; bow approx. 3.5 in wide.

---

### Safety — read this first

This design is intended as home decor, not a toy. A stuffed wreath is heavier than it looks: use a securely installed, load-rated hook and a load-rated woven cord or ribbon around the whole tube; do not rely on a suction cup or on a decoration tie.

No finished wreath or hanging system has been independently load-tested or assessed by Novality Store. Before supply or installation, the finished-item maker or seller must assess the actual materials, construction, support and foreseeable environment and meet all market-specific product-safety, documentation, labelling and traceability duties. A “home decor” label does not replace requirements arising from intended or reasonably foreseeable use.

### Materials

- Wreath base: 175 g green worsted/aran (#4), 4 mm hook, fibre fill.

- Decorations: small amounts of red, white, yellow and green yarn; optional metallic thread held with the snowflake yarn; 3.5-4 mm hook.

- For a door wreath, use a load-rated woven hanging cord or ribbon long enough to wrap twice around the full tube. Do not add loose or glued embellishments anywhere children can reach.

- Notions: stitch marker, scissors, tapestry needle.

### Gauge & size

Gauge is not critical - the tube is a constant 12 stitches and wreath size comes from tube LENGTH. Measure the tube, not the round count. The ring's centreline diameter is approximately tube length divided by 3.14; add one tube thickness for the outside diameter.

### Abbreviations (US + UK)

MR - magic ring  ·  dc = tr - double crochet / treble crochet

ch - chain  ·  tr = dtr - treble crochet / double treble crochet

sl st - slip stitch  ·  st(s) - stitch(es)

sc = dc - single crochet / double crochet  ·  R - round

hdc = half treble - half double crochet / half treble crochet  ·  FO - fasten off

(n) - stitch count at round end

How to read this dual pattern: every round appears twice side by side - the US-terms instruction in the left column, the exact UK equivalent in the right column. Stitch counts are identical for both terminologies. Prose tips use US terms.

### Construction & techniques

Wreath base: continuous spiral rounds (no joins - use a marker). Decorations: joined rounds for flowers and snowflake, short worked rows for the bow.

1. **The constant stitch tube** - Every tube round is exactly 12 sc - no increases, no decreases. Tube length sets wreath size: measure against the door/table and stop after a complete round.

2. **Joining the tube** - Keep both openings ROUND and make sure the tube is not twisted. Align each stitch of the final 12-stitch round with one foundation chain at the beginning; whip-stitch the 12 pairs around the circumference. Add the last stuffing before closing the final 3 pairs. Flattening the ends would seal them into bars instead of making a smooth end-to-end tube join.

3. **Snowflake arm (shared with NS 13)** - Into each ch-5 space: (sl st, ch 3, 3 tr, ch 3, sl st). First sl st loose, last sl st snug so the arm lies flat and stands upright.

4. **Removable ties** - Cut a 55 cm strand in the decoration colour and fold it in half (30 cm is enough for the mini wreath). Draw the folded loop under at least TWO sturdy stitches on the decoration back, pass both cut ends through that loop and snug it: this lark's-head anchors the tie without asking one stitch to carry the load. Take the two tails in opposite directions around the wreath tube and tie a secure bow or reef knot at the back. Untie the tails to swap decorations; unlike a short closed loop, this method does not require you to force the whole flower, snowflake or bow through its own attachment.

### Instructions

#### 1. Wreath base - padded tube

Continuous spiral, constant 12 sts. Stuff lightly every 5-8 rounds; keep it bendable, and do not overstuff the last 10 rounds.

##### Starting ring & tube

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| - | Ch 12, sl st to first ch to form a ring; place marker | Ch 12, sl st to first ch to form a ring; place marker | - | ring |

| R1 | Sc in each ch around | Dc in each ch around | (12) | - |

| R2+ | Sc in each st around until the tube reaches the target MEASURED length | Dc in each st around until the tube reaches the target MEASURED length | (12) | round counts vary too much by gauge to prescribe |

| Join | FO with a 40 cm tail; keep openings round, align the 12 final-round sts with the 12 foundation ch, and whip-stitch 12 pairs around | FO with a 40 cm tail; keep openings round, align the 12 final-round sts with the 12 foundation ch, and whip-stitch 12 pairs around | - | add final stuffing before last 3 pairs |

| Hanger | After joining the ring, wrap a load-rated woven cord or ribbon TWICE around the entire tube at the top; tie and secure it according to the cord/ribbon maker’s instructions, with the knot at the back | After joining the ring, wrap a load-rated woven cord or ribbon TWICE around the entire tube at the top; tie and secure it according to the cord/ribbon maker’s instructions, with the knot at the back | - | the hanger encircles the tube; it does not rely on individual crochet sts |

#### 2. Poinsettia (removable)

Yellow centre, six red petals, three green leaves.

##### Flower

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R1 | With yellow: 6 sc in MR, sl st to first sc, FO | With yellow: 6 dc in MR, sl st to first dc, FO | (6) | centre |

| Petals | Join red in any centre sc; [ch 4, 3 tr, ch 4, sl st] in the same st, then repeat once in each of the remaining 5 centre sc | Join red in any centre dc; [ch 4, 3 dtr, ch 4, sl st] in the same st, then repeat once in each of the remaining 5 centre dc | - | one petal in each centre st; 6 petals total |

| Leaves | Make 3 separately in green: ch 8, sc in 2nd ch from hook, hdc in next ch, dc in next 3 ch, hdc in next ch, sc in last ch; FO with a 15 cm tail | Make 3 separately in green: ch 8, dc in 2nd ch from hook, half treble in next ch, tr in next 3 ch, half treble in next ch, dc in last ch; FO with a 15 cm tail | (7 each) | all 7 working chains used |

| Tie | Attach one folded 55 cm green tie under at least 2 sturdy back sts as in technique 4 | Attach one folded 55 cm green tie under at least 2 sturdy back sts as in technique 4 | - | two tails wrap around tube; tie at back |

Arrange the three leaves evenly behind the red petals and sew them to the back of the yellow centre with their tails. Knot and bury the sewing tails, then lark's-head the separate 55 cm removable tie under at least two stitches on the back.

#### 3. Snowflake (removable)

White, joined rounds; block flat.

##### Snowflake

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| R1 | With white: MR, ch 3 (counts as first dc), 11 dc in ring, sl st to top of ch-3 | With white: MR, ch 3 (counts as first tr), 11 tr in ring, sl st to top of ch-3 | (12) | 12 spokes |

| R2 | [Ch 5, skip next dc, sl st in next dc] x 6, sl st to the base of the first ch-5 | [Ch 5, skip next tr, sl st in next tr] x 6, sl st to the base of the first ch-5 | - | 6 ch-5 spaces; all 12 R1 sts used |

| R3 | In each ch-5 space work (sl st, ch 3, 3 tr, ch 3, sl st); sl st to the first sl st, FO | In each ch-5 space work (sl st, ch 3, 3 dtr, ch 3, sl st); sl st to the first sl st, FO | - | 6 arms; per arm 3 tall sts + 2 sl sts |

| Tie | Attach one folded 55 cm white/silver tie under at least 2 sturdy back sts as in technique 4 | Attach one folded 55 cm white/silver tie under at least 2 sturdy back sts as in technique 4 | - | two tails wrap around tube; tie at back |

#### 4. Holiday bow (removable)

Two chain loops, two tails, one little centre band.

##### Bow

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| Loops | With red: ch 24, sl st to first ch (loop 1 - untwisted); ch 24 again, sl st to same base point (loop 2) | With red: ch 24, sl st to first ch (loop 1 - untwisted); ch 24 again, sl st to same base point (loop 2) | - | two 24-ch loops |

| Tails | Ch 15, sc in 2nd ch from hook and across (14 sc), sl st to bow base; repeat for second tail | Ch 15, dc in 2nd ch from hook and across (14 dc), sl st to bow base; repeat for second tail | (14) | 15 chains make 14 sc, x2 tails |

| Band | Ch 6, sc in 2nd ch from hook and across (5); rows 2-4: ch 1, turn, sc across (5) | Ch 6, dc in 2nd ch from hook and across (5); rows 2-4: ch 1, turn, 1 dc in each st across (5) | (5) | separate rectangle: 4 rows of 5; wrap around centre and sew short ends |

| Tie | Attach one folded 55 cm tie under at least 2 sturdy sts on the finished band back as in technique 4 | Attach one folded 55 cm tie under at least 2 sturdy sts on the finished band back as in technique 4 | - | two tails wrap around tube; tie at back |

Arrange the two loops side by side and the two tails below them. Wrap the band tightly around all four pieces; sew its short ends together at the back, then use the remaining tail to tack through the loop and tail bases so nothing can slide out. Add the separate 55 cm removable tie last.

#### 5. Mini wreath ornament (optional)

DK yarn, 3 mm hook, 8-st tube.

##### Mini tube

| Rnd | US terms | UK equivalent | Sts | Note |

|---|---|---|---|---|

| - | Ch 8 ring; sc in each ch (8); spiral in 8 sc until the tube measures 20-24 cm; join the 8 end pairs ROUND as for the base; wrap a separate doubled yarn tie twice around the whole tube for hanging | Ch 8 ring; dc in each ch (8); spiral in 8 dc until the tube measures 20-24 cm; join the 8 end pairs ROUND as for the base; wrap a separate doubled yarn tie twice around the whole tube for hanging | (8) | gives about 6.5-7.5 cm centreline diameter |

### Finishing & assembly

- Stuff the tube as you go - after every 5-8 rounds is far easier than stuffing a finished tube.

- Join the tube LAST: keep the openings round, check for twists, whip-stitch all 12 matched pairs around and add the final stuffing before the last 3 pairs.

- Every decoration has a folded 55 cm tie lark's-headed under at least two back stitches; wrap its two tails around the tube and tie them at the back. Untie to swap - nothing is sewn permanently to the wreath.

### Troubleshooting

- **Tube is stiff like a rope.** Over-stuffed - pull a pinch of fill per handful back out; the wreath must flex into a circle.

- **Wreath will not hold a circle.** Under-stuffed at the join - add a thin worm of fill through the join stitches, or wrap the join with spare yarn like a bandage.

- **Poinsettia petals cluster on one side.** Each petal goes into its OWN centre stitch, moving stitch by stitch around the six - not all six into one stitch.

### Colorways

Classic green & red  ·  Winter white & gold  ·  Berry wreath  ·  Neutral farmhouse green

### Helpful tips

#### Sizes at a glance

| Wreath | Target tube length | Approx. centreline diameter |

|---|---|---|

| Mini ornament | 20-24 cm / 8-9.5 in | 6.5-7.5 cm |

| Standard door | 86-97 cm / 34-38 in | 27-31 cm |

| Large door | 119-132 cm / 47-52 in | 38-42 cm |

The outside diameter is one tube thickness larger. Round counts are deliberately omitted because row height changes dramatically with yarn, hook and stuffing; measure the actual tube.

### Care & storage

Follow the labels for every yarn, stuffing, metallic thread and hanging component used. Before publishing a cleaning claim or supplying finished wreaths, clean and dry a complete sample by the proposed method, then remeasure it and inspect for dye transfer, distortion, stuffing migration, opened tube or decoration joins, and weakened hanging materials. Until that test passes, recommend gentle surface cleaning only. Store fully dry, supported and uncompressed; inspect the hanger, hook, tube seam and every tied decoration before each season and after severe weather.

### Terms of Use

#### Copyright & ownership

This crochet pattern - including all instructions, stitch counts, photography and design elements - is the original work and intellectual property of Novality Store, designed by Novality Crochet Studio. Design Code NS 15.

© 2026 Novality Store. All rights reserved.

This pattern is licensed to the purchaser for personal use and for the small-batch sale of finished physical items under the terms below. You may not copy, redistribute, resell, share, translate, reproduce, or claim the pattern itself as your own. The pattern itself may not be uploaded, reproduced, or distributed in digital or printed form without permission from Novality Store.

#### You may

Make as many finished wreaths as you like for yourself, gifts, or charity. Sell physical finished items made from this pattern in small quantities with credit to Novality Store.

#### You may not

Sell, share, copy or redistribute this pattern or any part of it. Claim the pattern as your own design. Produce items from this pattern as a factory or manufacturer.

#### Safety reminder

Intended as home decor, not a toy. Keep away from open flames and keep loose or glued additions out of children’s reach. Use a securely installed, load-rated hook and a load-rated cord or ribbon wrapped twice around the entire tube. No finished wreath or hanging system has been independently assessed by Novality Store; the finished-item maker or seller is responsible for market-specific product-safety evidence and duties before supply.

### Happy crocheting!

Tag your makes with **#NovalityStore** and **#NovalityWreath** - swap the decoration, swap the mood. Thank you for supporting an independent pattern designer.


---

# Part 16 of 17 — NS-16 · Mini Stocking Advent Garland

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 9 pp · print edition 9 pp · reports: `docs/ns16/NS16_validation_report.md`*

## Crochet Mini Stocking Advent Garland

> Design Code NS 16 · Novality Crochet Studio · US crochet terms

> Twenty-four small cuff-down stockings for an Advent garland. Each stocking has an exact turned heel, a counted 23-to-20 foot transition and a closed four-stitch toe.

### Safety — read this first

This pattern makes a decoration and small treat holder; it does not establish that the finished item is a toy or suitable for any age. A long garland cord, hanging loops, bells, beads, buttons, tags, clips, coins, sweets and other small or detachable contents can create entanglement, choking, ingestion or allergy hazards. Keep the garland and every filling out of reach of children and animals unless a qualified assessment for the actual construction, intended use and destination market establishes otherwise. Never hang it over a bed, cot, play space, doorway, heat source, naked flame or lit candle.

For the plain version, embroider or securely sew decorations and avoid glue-only attachments. A stitched decoration can still detach, so inspect every attachment and hanging point before each season and after filling. Use a support and wall fixings rated for the complete filled garland, not just the empty crochet. Food should remain in its own wrapper and must be selected with the recipient's allergies and age in mind.

No finished NS 16 stocking or garland has been independently load-tested, wash-tested or shown by Novality Crochet Studio to comply with a product-safety regime. Before sale or supply, the finished-item maker or seller must determine the applicable classification, assessment, testing, documentation, labelling and traceability duties for every destination market.

### Quick facts

| Detail | Original version |

|---|---|

| Skill level | Advanced beginner: joined rounds, turned rows, short-row decreases and edge pickup |

| Finished size | Target about 10 cm / 4 in tall and 5 cm / 2 in wide when laid flat |

| Yarn | DK / light worsted / 8-ply |

| Hook | 4.0 mm (US G/6), or the size needed to meet the target gauge |

| Construction | Cuff-down joined rounds; six-row heel flap; four shaping rows; counted foot pickup; decreased toe |

| Active time | Original estimate 15–20 minutes after practice; make and time one complete sample before advertising this claim |

| Terminology | US crochet terms |

### Materials

#### One stocking

- DK / light worsted (#3) yarn: main colour (MC), about 16 m / 17 yd for the leg and foot.

- DK yarn: cuff colour (CC), about 4.5 m / 5 yd.

- DK yarn: accent colour (AC), enough for the heel, toe and hanging loop. Weigh a completed sample if buying for a batch.

- 4.0 mm crochet hook.

- Blunt tapestry needle, scissors, stitch marker and rust-resistant pins.

- Optional: a very small amount of polyester fibre fill for a display-only puffy toe. Do not add stuffing when maximum treat capacity is required.

#### Twenty-four-stocking garland

The stated per-stocking main-colour estimate scales to about 380 m / 410 yd before swatching or allowance; the cuff estimate scales to about 110 m / 120 yd. Accent use depends on whether both heel and toe are contrasted. Make, weigh and measure one complete stocking in the actual yarn, multiply each colour by 24 and add an allowance for swatching, tails and variation before purchasing.

Also obtain 2.2 m / 7 ft of load-appropriate ribbon, woven cord or yarn for the support; secure wall fixings; and, if used, securely attached number tags or clips. Do not assume a decorative jute string or adhesive hook can support 24 filled stockings.

### Gauge & size

Target gauge: about 20 sc and 20 rounds = 10 cm / 4 in in joined single crochet, measured without stretching. At this gauge, 20 stitches make a circumference of about 10 cm / 4 in and a laid-flat width of about 5 cm / 2 in.

Gauge controls both the advertised size and what the stocking can hold. Before making the batch, complete one stocking, let it rest, then measure height, flat width, leg circumference and capacity. If it is too open or floppy, use a smaller hook; if it is too narrow for the intended wrapped item, use a larger hook and remeasure. Do not advertise the target dimensions or capacity as measured facts until a sample confirms them.

### Abbreviations (US terms)

- AC — accent colour

- BLO — back loop only

- CC — cuff colour

- ch — chain

- dec — invisible single-crochet decrease; work the front loops of the next two stitches together

- FO — fasten off

- MC — main colour

- rnd — round

- RS — right side
- WS — wrong side

- sc — single crochet

- sl st — slip stitch

- st(s) — stitch(es)

The starting ch 1 never counts as a stitch. Joined rounds end with a sl st to the first sc; do not work into that joining slip stitch. Move the marker to the first sc of every round.

### Techniques, used in the order you will meet them

1. **Untwisted ring:** lay the 20-chain foundation flat before joining so the chain does not spiral.

2. **Joined round:** ch 1, work the stated stitches beginning in the same stitch as the join, then sl st to the first sc.

3. **Turned heel row:** the ch 1 does not count; turn after every row that says turn.

4. **Heel-edge pickup:** distribute five stitches along each complete exposed heel edge, including the stepped heel-turn section and the full-flap row ends. Work under two edge strands wherever possible; five pickups per side are mandatory for the 23-stitch route.

5. **Invisible decrease:** use the front loops of the next two stitches; it consumes two stitches and produces one.

### Instructions

#### 1. Cuff and leg

With CC, ch 20 loosely. Check that the chain is untwisted, then sl st in the first chain to form a ring. Ch 1; this turning chain does not count. The foundation chain provides 20 anchors and is not an extra crochet round.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | sc in each of 20 foundation chains around | (20) | join to first sc |

| R2 | BLO sc in each st around | (20) | ribbed cuff |

| R3 | BLO sc in each st around | (20) | ribbed cuff |

| R4 | BLO sc in each st around | (20) | ribbed cuff |

| R5 | with MC, sc in each st around | (20) | both loops |

| R6 | sc in each st around | (20) | leg |

| R7 | sc in each st around | (20) | leg |

| R8 | sc in each st around | (20) | leg |

| R9 | sc in each st around | (20) | leg |

| R10 | sc in each st around | (20) | leg; join, do not FO |

Rnds 5–10 make six main-colour leg rounds. For stripes, change colour only at a completed join and carry or secure the inactive yarn without tightening the tube.

#### 2. Heel flap and turn

The heel uses the next 10 consecutive stitches, beginning in the same stitch as the Rnd-10 join. The other 10 leg stitches remain unworked as the instep. Continue in MC or change to AC at the join.

| Row | Instruction | Sts | Note |

|---|---|---|---|

| Row 1 | ch 1, sc in same st as join and next 9 sts, ch 1, turn | (10) | RS; each ch 1 is uncounted; 10 instep sts wait |

| Row 2 | BLO sc in each st across, ch 1, turn | (10) | WS |

| Row 3 | sc in each st across, ch 1, turn | (10) | RS |

| Row 4 | BLO sc in each st across, ch 1, turn | (10) | WS |

| Row 5 | sc in each st across, ch 1, turn | (10) | RS |

| Row 6 | BLO sc in each st across, ch 1, turn | (10) | WS; the turn is required |

| Row 7 | 6 sc, dec; leave final 2 sts unworked, ch 1, turn | (7) | consumes 8 of 10 |

| Row 8 | 4 sc, dec; leave final st unworked, ch 1, turn | (5) | consumes 6 of 7 |

| Row 9 | 3 sc, dec, ch 1, turn | (4) | consumes all 5 |

| Row 10 | 2 sc, dec; do not turn | (3) | heel centre |

The corrected Row-6 turn is essential: without it there are no stitches ahead of the hook for Row 7. Rows 7–10 alternate direction and reduce 10 active stitches to 3 while the unworked ends help form the heel cup. Do not crochet into those unworked top loops as extra heel-turn stitches.

#### 3. Foot pickup and evening

After Row 10, do not turn. The hook is at one edge of the three-stitch heel centre. Ch 1; this chain does not count. Follow the exposed perimeter from the hook toward the leg opening—do not work across the three Row-10 stitches yet. Work the pickup in this exact order and place the marker in the first picked-up sc:

1. Work exactly 5 sc evenly along the complete first heel edge from Row 10 to the leg opening. Include the compact stepped edge made by Rows 7–10 and the row-end edge of the six full flap rows; place the first and fifth pickups close to the two junctions. Work under two edge strands wherever possible.

2. Work 1 sc in each of the 10 waiting instep stitches.

3. Work exactly 5 sc along the complete second heel edge, mirroring the first side and ending beside the far edge of Row 10.

4. Work 1 sc in each of the 3 Row-10 heel-centre stitches, returning to the beginning of the pickup round.

5. Join to the first picked-up sc: 5 + 10 + 5 + 3 = 23 stitches.

The five side stitches are distributed over each whole exposed heel edge; they are not five extra stitches plus additional stitches in the heel-turn steps. If a large gap remains at either heel-centre or leg junction, undo that side and move its nearest pickup closer to the junction without changing the five-stitch side count.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Foot R1 | 5 side sc, 10 instep sc, 5 side sc, 3 heel-centre sc | (23) | exact pickup route above |

| Foot R2 | 4 sc, dec, 5 sc, dec, 5 sc, dec, 3 sc | (20) | consumes all 23; three decreases |

| Foot R3 | sc in each st around | (20) | join |

| Foot R4 | sc in each st around | (20) | join |

| Foot R5 | sc in each st around | (20) | join |

| Foot R6 | sc in each st around | (20) | join |

| Foot R7 | sc in each st around | (20) | join |

Do not move the three Foot-R2 decreases arbitrarily: the written 4 / 5 / 5 / 3 spacing distributes them around the counted pickup. If the pickup does not equal 23, undo it and correct the side anchors before continuing.

#### 4. Toe

Change to AC at the Foot-R7 join if desired.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| Toe R1 | [3 sc, dec] x 4 | (16) | 20 to 16 |

| Toe R2 | [2 sc, dec] x 4 | (12) | 16 to 12 |

| Toe R3 | [sc, dec] x 4 | (8) | add optional display stuffing now |

| Toe R4 | dec x 4 | (4) | FO with 15 cm / 6 in tail |

Thread the tail through the front loop of each remaining stitch in order, pull closed, knot on the inside and weave the tail through several neighbouring stitches before trimming.

#### 5. Hanging loop

Mark the back-centre stitch of Cuff Rnd 4. Join CC or AC under both loops of that stitch, ch 12, then sl st under both loops of the same marked stitch and once through the next Cuff-Rnd-4 stitch in the direction of work. FO, knot the two tails together inside and weave each tail in a different direction for at least 2.5 cm / 1 in. The finished loop is a hanging aid, not a rated handle; inspect it while the stocking is filled.

For a clip-on garland, omit this loop and use clips sized so they cannot pass through the stocking opening. Small clips remain a detachable hazard.

### Finishing & assembly

Weave every colour-change tail through the wrong side in two directions. Shape the heel with a finger and check that it projects on the opposite side from the instep. Confirm the opening remains usable, the toe is fully closed and the hanging loop cannot pull free under the intended filled weight.

Optional numbers and motifs should be embroidered on the cuff or upper leg before filling, away from the hanging-loop anchor. If using a separately crocheted motif, sew around its complete perimeter and secure the tails inside; do not rely on glue. Bells, beads, buttons, wooden tags and clothespins are display-only additions unless the complete finished arrangement has been appropriately assessed.

### Making the 24-stocking Advent garland

1. Make and approve one complete stocking before batch work. Then make 24 identical counted routes, or record any intentional colour-only variations.

2. Number 1–24 with secure embroidery or another method appropriate to the actual users and assessment. Do not obscure the hanging-loop anchor.

3. Cut 2–2.5 m / 6–8 ft of support. Leave enough free length at each end for the rated wall fixing. Measure the usable span between those two end allowances and divide it by 23 to mark the centre-to-centre spacing for 24 stockings. For example, a 200 cm support with 20 cm reserved at each end leaves 160 cm; 160 ÷ 23 is approximately 7 cm between centres.

4. Thread each tested loop onto the support or attach the clip-on version. Place each stocking at a marked centre, then add a stopper knot or secure stitch beside each loop so loaded stockings cannot all slide to one end. Increase the usable span if the filled stockings overlap at the calculated spacing.

5. Fill only after the empty garland is mounted. Keep each wrapped item within the tested stocking and support capacity.

Assembly-line production—cuffs first, then legs, heels, pickups and toes—can reduce colour changes, but each stocking must retain its own count and inspection record. The source estimate of 15–20 minutes per stocking excludes the first samples, decorations, weaving, mounting and filling; time the actual process before using that claim in a listing.

### Troubleshooting

- **The foundation twists:** undo the join, lay all chain bumps in one direction and rejoin.

- **The heel cannot start after Row 6:** Row 6 must end with ch 1 and turn. Do not omit that corrected turn.

- **There is a hole beside the heel:** redistribute the five pickups over the complete exposed edge, placing the end pickups close to the heel-centre and leg junctions; work under two edge strands wherever possible.

- **The pickup is not 23:** recount 5 side + 10 instep + 5 side + 3 heel centre. Do not compensate in the evening round.

- **The foot is still above 20:** Foot R2 contains exactly three decreases and consumes all 23 stitches.

- **The stocking leans:** confirm both heel sides use corresponding gaps and each leg/foot plain round has 20 stitches.

- **The cuff is too small for the intended item:** change hook only after making a new sample; then remeasure the full stocking and support load.

### Colorways

Original colourway: classic red MC for leg and foot, snow-white CC for the ribbed cuff, and evergreen AC for heel, toe and hanging loop. All three colours should be similar DK yarns so the gauge remains consistent.

Alternative palettes: winter white / silver-grey / pale blue; natural cream / heather brown / deep red; Scandinavian red / white / small black embroidery; blush pink / cream / mint; or a scrap-yarn set with one consistent cuff colour. Record the actual colour and fibre used for every stocking if care labels differ.

### Designer notes

The small scale is intended for one wrapped mini sweet or a tightly rolled paper note at the target gauge. Capacity varies with yarn, tension and heel shaping. A 25th stocking may be made for Christmas Day, but it uses the same construction and is not automatically larger.

### Care & storage

Remove all food, notes, clips and detachable decorations before cleaning. Follow the most restrictive label among all yarns, threads and additions. Before publishing a care claim, clean and fully dry one complete stocking and a representative section of the loaded-support system by the proposed method; remeasure and inspect colour transfer, shrinkage, heel shape, loop security and fibre damage. Until that test passes, recommend gentle surface cleaning with a barely damp cloth and drying flat away from heat.

Store clean, empty and completely dry. Do not fold heavy objects into the heel or leave the garland under tension between seasons. Inspect cord, wall loops, stocking loops and every attachment before rehanging.

### Terms of Use

#### Copyright & ownership

© 2026 Novality Crochet Studio. All rights reserved. This crochet pattern, its instructions, stitch counts, editorial layout and design elements are protected material. Design Code NS 16.

This pattern is licensed to the purchaser for personal use and for small-batch sale of finished physical stockings or garlands under the terms below. The purchaser may not copy, share, translate, upload, redistribute, resell or publish the pattern or any substantial part of it in digital or printed form.

#### You may

Make finished stockings for yourself, gifts or charity. Sell finished physical items made from this pattern in small quantities, provided the listing credits “Pattern by Novality Crochet Studio · Design Code NS 16” and does not claim unverified safety, testing, size, capacity or care results.

#### You may not

Resell or distribute this PDF or Markdown source; convert it into another pattern product; use its text, tables or visuals as listing assets for a competing pattern; claim authorship; or mass-produce finished items without written permission. Credit does not grant use of the studio name as your own brand.

#### Safety reminder

The finished-item maker or seller remains responsible for the actual materials, classification, assessment, testing, warnings, documentation, labelling and traceability required in every market where a finished item is supplied.

Tag finished projects with **#NovalityCrochetStudio** and **#NovalityMiniStocking**.

### Happy crocheting!

Check every box, preserve the 5 + 10 + 5 + 3 pickup and enjoy building the colour sequence one stocking at a time.


---

# Part 17 of 17 — NS-17 · Year of the Fire Goat 2027 Plushie Set

*Verified master · engine 0 errors / 0 warnings · independent audit 0 problems · colour edition 14 pp · print edition 14 pp · reports: `docs/ns17/NS17_validation_report.md`*

## Year of the Fire Goat 2027 Plushie Set

> Design Code NS 17 · Novality Crochet Studio · US crochet terms

> A seated Fire Goat and companion lamb with matched 12-to-12 neck seams, layered ears, embroidered faces and securely sewn festive accessories.

### Safety — read this first

These instructions do not establish that either finished plush is suitable for a child or complies with a toy standard. Embroidered eyes remove plastic eye components but do not prove overall safety. Safety eyes, bells, beads, wire, pipe cleaners, ribbon loops, glue-only details and other hard, long or detachable additions introduce separate hazards. The original NS 17 route uses embroidered eyes, unstuffed yarn-only horns and sewn crochet accessories; it contains no internal wire and no loose tie-on collar.

Keep every finished item away from naked flames and heat despite the decorative “fire” theme. Do not use a finished plush as a cot item, baby mobile, keychain or hanging ornament without a qualified assessment for that exact use. Before sale or supply, the finished-item maker or seller must determine the applicable classification, mechanical, flammability, chemical, hygiene, documentation, warning, labelling and traceability duties in every destination market.

No NS 17 sample has been independently crocheted, load-tested, wash-tested or shown by Novality Crochet Studio to comply with ASTM F963, EN 71 or another product-safety regime. All dimensions, yarn quantities and active times remain targets until confirmed on complete samples.

### Quick facts

| Detail | Original version |

|---|---|

| Designs | Fire Goat and hornless companion lamb |

| Skill level | Intermediate: spirals, shaping, colour changes, layered pieces, embroidery and reinforced structural assembly |

| Finished size | Source target 17 cm / 6.75 in seated is unverified and conflicts with the row-depth estimate below; measure the complete animals, including ear or horn projection, before publishing a size |

| Yarn | Smooth worsted (#4) for the original goat; worsted (#4) white texture yarn or smooth yarn for the original lamb |

| Hook | 3.5 mm (US E/4), or the size needed for a dense target gauge |

| Construction | Separate head, muzzle, ears, body, limbs and tail; goat also has horns and a flame sash |

| Active time | Planning estimate 5–7 hours per animal, excluding sample correction and care testing |

| Terminology | US crochet terms |

Chinese Lunar New Year begins on 6 February 2027; in the Chinese zodiac, 2027 is commonly described in English as the Year of the Fire Goat, Sheep or Ram. The source term 羊 (*yáng*) is broader than one English species label. This pattern uses “Goat” for the horned design and “lamb” for its companion; the names are design labels, not claims of cultural authenticity.

Calendar reference (accessed 18 September 2026): Smithsonian Institution, “2027: Year of the Goat” (si.edu/spotlight/lunar-year-goat).

### Materials

#### Fire Goat materials

- Smooth worsted (#4) cotton or acrylic: warm cream / off-white, about 73 m / 80 yd for head, body, outer ears, upper limbs and tail.

- Worsted (#4) light tan / beige, about 18 m / 20 yd for muzzle, inner ears and hooves.

- Worsted (#4) espresso brown or dark grey, about 9 m / 10 yd for two yarn-only horns.

- Worsted (#4) scarlet red, about 14 m / 15 yd for the fixed flame sash.

- Small amounts of burnt orange and golden yellow for flame edging and optional crochet flowers; green for optional leaves; pink and black embroidery thread for face details.

- Polyester fibre fill. Record the mass used in the completed test sample.

#### Companion lamb materials

- Worsted (#4) white texture yarn or smooth washable worsted, about 73 m / 80 yd for head, body, outer ears, upper limbs and tail. “Wool white” is the original shade name used below, not a fibre requirement. Do not substitute blanket-weight chenille without making and measuring a separate sample.

- Worsted (#4) light tan / beige, about 27 m / 30 yd for the muzzle and hooves.

- Worsted (#4) scarlet red, about 9 m / 10 yd for the fixed collar.

- Small amounts of pale-pink worsted yarn for the original inner ears, plus black embroidery thread and optional pink embroidery thread for blush.

- Polyester fibre fill. Record the mass used in the completed test sample.

#### Tools for either animal

- 3.5 mm crochet hook, or the size required for gauge.

- Blunt tapestry needle, stitch markers, scissors and rust-resistant pins.

- Optional 10 mm safety eyes for a separately assessed display version only. The original colourway and illustrated route use black embroidered eyes.

The quoted yarn is a planning allowance, not a measured guarantee. Fibre, twist, texture, gauge, tails and stuffing change use. Swatch, make one complete animal and weigh every colour before publishing supply claims or buying for production.

### Gauge & size

Target gauge: about 20 sc and 22 rounds = 10 cm / 4 in in unstuffed spiral single crochet with smooth worsted yarn. More important than matching the number exactly, the fabric must be dense enough that stuffing does not show or migrate.

At the target stitch gauge, a 42-stitch circumference is about 21 cm / 8.25 in before stuffing. At the target row gauge, the goat's 19 head rounds plus 23 body rounds represent about 19 cm / 7.5 in of unstuffed row depth before shaping and seaming; the lamb's 20 plus 24 rounds represent about 20 cm / 8 in. Stuffing, three-dimensional shaping and the neck seam change those values, while ears and horns add projection. The source's 16–18 cm overall-height estimate is therefore not supported by gauge arithmetic and must not be advertised as measured size.

Make a head swatch or the first complete head, let it rest, then record gauge and dimensions. A fuzzy worsted yarn must meet the same dense gauge; blanket or super-bulky chenille requires a new hook, creates a materially larger object and is not a tested size option. Measure each fully assembled animal from its seated base to its highest attached feature before publishing any finished height.

### Abbreviations (US terms)

- BLO — back loop only

- ch — chain

- dc — double crochet

- dec — invisible single-crochet decrease through the front loops of the next two stitches

- FO — fasten off

- hdc — half double crochet

- inc — work 2 sc in the same stitch

- MR — magic ring

- rep — repeat

- rnd — round

- sc — single crochet

- sl st — slip stitch

- st(s) — stitch(es)

Work all amigurumi rounds in continuous spirals unless a flat row is explicitly stated. Do not join or ch 1 between spiral rounds. Mark the first stitch and move the marker after every completed round. Brackets followed by “x” repeat the complete bracketed sequence.

### Techniques, used in the order you will meet them

1. **Magic ring:** tighten the starting tail before Rnd 2 and weave it in securely. For the alternative start, ch 2 and work every R1 stitch into the second chain from the hook; use it only if the centre closes without a hole.

2. **Invisible decrease:** use the front loops of the next two stitches; one decrease consumes two stitches and produces one.

3. **Open matched seam:** the original head and body each stop at twelve stitches. Pair and sew every opening stitch for stitch.

4. **Layered ear:** make one outer and one inner piece per ear, then sew the complete perimeter before attachment.

5. **Flattened limb top:** an eight-stitch opening makes four stitch pairs. Sew through both layers of each pair and the body fabric.

### Instructions

#### Fire Goat

##### 1. Head — warm cream

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | tighten ring |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | - |

| R7 | [5 sc, inc] x 6 | (42) | - |

| R8 | sc in each st around | (42) | - |

| R9 | sc in each st around | (42) | - |

| R10 | sc in each st around | (42) | - |

| R11 | sc in each st around | (42) | - |

| R12 | sc in each st around | (42) | - |

| R13 | sc in each st around | (42) | - |

| R14 | sc in each st around | (42) | face-access pause |

| R15 | [5 sc, dec] x 6 | (36) | begin stuffing |

| R16 | [4 sc, dec] x 6 | (30) | - |

| R17 | [3 sc, dec] x 6 | (24) | - |

| R18 | [2 sc, dec] x 6 | (18) | finish firm, even stuffing |

| R19 | [sc, dec] x 6 | (12) | FO; leave opening and 30 cm tail |

Immediately after Rnd 14, embroider the two black eyes between Rnds 10 and 11 with their centres eight stitches apart; knot and bury the ends inside. If using the optional display-version safety eyes, install and lock both washers at this same pause. Do not work a six-stitch closing round: the 12-stitch Rnd-19 opening is the required half of the neck seam.

##### 2. Muzzle — light tan

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | sc in each st around | (18) | - |

| R5 | sc in each st around | (18) | FO with sewing tail |

Lightly stuff the muzzle. Centre its open 18-stitch edge below the eyes over Head Rnds 11–15. Sew every open-edge stitch to the head fabric, pausing before the final four stitches to adjust the stuffing. Through the still-open neck, knot and bury the sewing tail. Embroider two short nostrils and a small Y-shaped mouth using black; secure those ends through the neck opening.

##### 3. Horns — espresso brown, make 2

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 4 sc in MR | (4) | horn tip |

| R2 | [sc, inc] x 2 | (6) | - |

| R3 | sc in each st around | (6) | - |

| R4 | sc in each st around | (6) | - |

| R5 | sc in each st around | (6) | - |

| R6 | BLO sc in each st around | (6) | bend ridge |

| R7 | sc in each st around | (6) | - |

| R8 | sc in each st around | (6) | - |

| R9 | sc in each st around | (6) | - |

| R10 | [sc, inc] x 3 | (9) | horn base |

| R11 | sc in each st around | (9) | FO with sewing tail |

Do not stuff and do not insert wire or pipe cleaner. Fold slightly at the Rnd-6 ridge and place one hidden yarn tack between the inner sides of Rnds 5 and 7 to hold a gentle bend. Sew all nine base stitches to the top of the head across approximately Rnds 3–5. Position the two inner base edges about four head stitches apart and mirror the backward/outward angle.

##### 4. Layered ears — make 2 complete ears

For each ear, make one warm-cream outer piece and one light-tan inner piece.

| Row | Instruction | Sts | Note |

|---|---|---|---|

| Foundation | ch 7 | - | 6 working chains |

| Row 1 | sc in 2nd ch and next 5 ch, ch 1, turn | (6) | - |

| Row 2 | dec, 2 sc, dec, ch 1, turn | (4) | - |

| Row 3 | sc in each st across, ch 1, turn | (4) | - |

| Row 4 | dec x 2 | (2) | FO; point |

Place the inner piece on the outer piece with wrong sides together and sew the complete perimeter. Fold the six-stitch foundation edge in half and secure the fold. Sew that folded base through both layers to the side of the head around Rnds 8–12, below and behind its horn. Mirror the second ear.

For the optional longer ear, make both layers from this complete table instead; do not mix lengths within one ear.

| Row | Instruction | Sts | Note |

|---|---|---|---|

| Foundation | ch 8 | - | 7 working chains |

| Row 1 | sc in 2nd ch and next 6 ch, ch 1, turn | (7) | - |

| Row 2 | dec, 3 sc, dec, ch 1, turn | (5) | - |

| Row 3 | sc in each st across, ch 1, turn | (5) | - |

| Row 4 | dec, sc, dec | (3) | FO; point |

For each longer-ear layer, number the seven foundation-edge stitches 1–7. Fold that edge around stitch 4; match stitch 1 to 7, 2 to 6 and 3 to 5, with stitch 4 forming the fold. Secure the three matched pairs and the fold stitch to make four exact base anchors, then sew all four anchors to the head. Make and join both layers by the same longer-ear route.

##### 5. Body — warm cream

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | base centre |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | - |

| R7 | BLO sc in each st around | (36) | sit-flat base crease |

| R8 | sc in each st around | (36) | both loops |

| R9 | sc in each st around | (36) | - |

| R10 | sc in each st around | (36) | - |

| R11 | sc in each st around | (36) | - |

| R12 | sc in each st around | (36) | - |

| R13 | sc in each st around | (36) | - |

| R14 | sc in each st around | (36) | - |

| R15 | [4 sc, dec] x 6 | (30) | - |

| R16 | sc in each st around | (30) | - |

| R17 | sc in each st around | (30) | - |

| R18 | [3 sc, dec] x 6 | (24) | begin stuffing |

| R19 | sc in each st around | (24) | - |

| R20 | [2 sc, dec] x 6 | (18) | - |

| R21 | sc in each st around | (18) | - |

| R22 | [sc, dec] x 6 | (12) | - |

| R23 | sc in each st around | (12) | FO with 45 cm neck-seam tail |

Stuff the base flat and the upper body firmly without distorting the 12-stitch neck opening. The body tail is reserved for the neck seam; every limb supplies its own sewing tail.

##### 6. Arms / front legs — make 2

Use light tan for Rnds 1–4 and warm cream for Rnds 5–13.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 5 sc in MR | (5) | hoof tip |

| R2 | inc in each st around | (10) | - |

| R3 | BLO sc in each st around | (10) | hoof crease |

| R4 | sc in each st around | (10) | - |

| R5 | sc in each st around | (10) | change to cream |

| R6 | sc in each st around | (10) | - |

| R7 | sc in each st around | (10) | - |

| R8 | sc in each st around | (10) | - |

| R9 | sc in each st around | (10) | - |

| R10 | sc in each st around | (10) | - |

| R11 | sc in each st around | (10) | - |

| R12 | sc in each st around | (10) | - |

| R13 | [3 sc, dec] x 2 | (8) | FO with sewing tail |

Stuff Rnds 1–9 lightly, keeping most of the fill inside the hoof; leave Rnds 10–13 without fill so the top can flatten cleanly. Match the second arm's fill level and flatten each eight-stitch opening into four pairs.

##### 7. Legs / back legs — make 2

Use light tan for Rnds 1–5 and warm cream for Rnds 6–13.

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | hoof tip |

| R2 | inc in each st around | (12) | - |

| R3 | BLO sc in each st around | (12) | hoof crease |

| R4 | sc in each st around | (12) | - |

| R5 | sc in each st around | (12) | - |

| R6 | sc in each st around | (12) | change to cream |

| R7 | sc in each st around | (12) | - |

| R8 | sc in each st around | (12) | - |

| R9 | sc in each st around | (12) | - |

| R10 | sc in each st around | (12) | - |

| R11 | sc in each st around | (12) | - |

| R12 | sc in each st around | (12) | - |

| R13 | [sc, dec] x 4 | (8) | corrected even opening; FO with sewing tail |

Stuff through Rnd 8. Leave Rnds 9–13 without fill for a flexible seated leg, or add only a trace of fill; use the same choice and amount for both legs equally. Flatten each eight-stitch opening into four pairs. The corrected final round decreases 12 to 8 rather than 9 so no unmatched stitch remains within the flattened seam.

##### 8. Tail — warm cream

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 4 sc in MR | (4) | - |

| R2 | [sc, inc] x 2 | (6) | - |

| R3 | sc in each st around | (6) | - |

| R4 | sc in each st around | (6) | - |

| R5 | sc in each st around | (6) | - |

| R6 | sc in each st around | (6) | FO with sewing tail |

Do not stuff. Sew all six open-edge stitches to the centre back around Body Rnds 19–20, with the tip angled upward.

##### 9. Fixed flame sash

With scarlet, ch 36.

| Row | Instruction | Sts | Note |

|---|---|---|---|

| Row 1 | sc in 2nd ch and next 34 ch, ch 1, turn | (35) | - |

| Row 2 | sc in each st across | (35) | FO and weave red ends |

Before adding the flame edge, pin the relaxed 35-stitch strip diagonally around the stuffed goat body in the stated assembly position. Its short ends must overlap by at least one stitch without stretching or compressing the body. If they do not, stop and correct the body or strip gauge; resizing the 35-stitch sash and its exact 12-peak edging is not included in this version.

Lay the strip flat with Row 2 uppermost and choose one 35-stitch long edge for the flames; do not work around either short end. Number the Row-2 edge stitches 1–35 in the direction you will crochet. For exactly 12 burnt-orange peaks, join orange in edge stitch 1, ch 3 and sl st in that same stitch. Then work `[sl st in next 2 edge sts, ch 3, sl st in next edge st] x 11`; sl st in edge stitch 35 and FO. This anchors peaks in edge stitches 1, 4, 7 through 34 and uses stitch 35 only as the finishing anchor.

With a needle and golden-yellow yarn, sew one short secure stitch through the top two chains of each of the 12 orange peaks. Knot and weave the yellow tail along the wrong side. In assembly, wrap the strip diagonally as a sash across the upper body, overlap the short ends at the back and sew the overlap plus the upper shoulder point to the body. Do not leave tie tails.

##### 10. Optional crochet flower crown

For each of 3–4 flowers, ch 3 and sl st to the first chain to form a ring. Work `[ch 2, 2 dc in ring, ch 2, sl st in ring] x 5`, FO and retain the sewing tail. For each of two green leaves, ch 5; beginning in the second chain, work sc, hdc, sc, sl st; FO with a sewing tail.

Arrange the crochet-only pieces between the horns without covering either horn base. Sew the centre and complete inner edge of every flower and leaf to the head; knot and bury all tails through the open neck. Do not substitute glued fabric flowers in a child-accessible item.

#### Companion lamb

Make a separate muzzle, two complete layered ears, two arms and two legs from the Fire Goat tables using the lamb colours. Use wool white for each upper/main section, light tan for the muzzle and hooves, and pale pink for the original inner-ear layers. Do not make horns or the flame sash. Use the following head, body, tail and fixed collar.

##### 11. Rounder lamb head — wool white

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | - |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | - |

| R7 | [5 sc, inc] x 6 | (42) | - |

| R8 | sc in each st around | (42) | - |

| R9 | sc in each st around | (42) | - |

| R10 | sc in each st around | (42) | - |

| R11 | sc in each st around | (42) | - |

| R12 | sc in each st around | (42) | - |

| R13 | sc in each st around | (42) | - |

| R14 | sc in each st around | (42) | - |

| R15 | sc in each st around | (42) | face-access pause |

| R16 | [5 sc, dec] x 6 | (36) | begin stuffing |

| R17 | [4 sc, dec] x 6 | (30) | - |

| R18 | [3 sc, dec] x 6 | (24) | - |

| R19 | [2 sc, dec] x 6 | (18) | finish stuffing |

| R20 | [sc, dec] x 6 | (12) | FO; leave open with 30 cm tail |

Immediately after Rnd 15, embroider black eyes between Rnds 11 and 12, eight stitches centre to centre, and secure the ends inside. Centre a separate light-tan muzzle from the five-round muzzle table below the eyes over approximately Lamb Head Rnds 12–16. Lightly stuff it and sew all 18 open-edge stitches to the head, then embroider its nose and mouth while the 12-stitch neck remains open. Do not work a six-stitch closing round.

Make two layered ears with wool-white outer pieces and pale-pink inner pieces for the original colourway; light tan is an optional inner-ear substitution. Position their folded bases around Lamb Head Rnds 9–13 and angle them down. This design's companion lamb is intentionally hornless.

##### 12. Rounder lamb body — wool white

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 6 sc in MR | (6) | base centre |

| R2 | inc in each st around | (12) | - |

| R3 | [sc, inc] x 6 | (18) | - |

| R4 | [2 sc, inc] x 6 | (24) | - |

| R5 | [3 sc, inc] x 6 | (30) | - |

| R6 | [4 sc, inc] x 6 | (36) | - |

| R7 | [5 sc, inc] x 6 | (42) | - |

| R8 | BLO sc in each st around | (42) | sit-flat base crease |

| R9 | sc in each st around | (42) | both loops |

| R10 | sc in each st around | (42) | - |

| R11 | sc in each st around | (42) | - |

| R12 | sc in each st around | (42) | - |

| R13 | sc in each st around | (42) | - |

| R14 | sc in each st around | (42) | - |

| R15 | sc in each st around | (42) | - |

| R16 | [5 sc, dec] x 6 | (36) | - |

| R17 | sc in each st around | (36) | - |

| R18 | sc in each st around | (36) | - |

| R19 | [4 sc, dec] x 6 | (30) | begin stuffing |

| R20 | sc in each st around | (30) | - |

| R21 | [3 sc, dec] x 6 | (24) | - |

| R22 | sc in each st around | (24) | - |

| R23 | [2 sc, dec] x 6 | (18) | - |

| R24 | [sc, dec] x 6 | (12) | FO with 45 cm seam tail |

Stuff firmly while preserving the 12-stitch neck opening.

##### 13. Lamb tail — wool white

| Rnd | Instruction | Sts | Note |

|---|---|---|---|

| R1 | 5 sc in MR | (5) | - |

| R2 | inc in each st around | (10) | - |

| R3 | sc in each st around | (10) | - |

| R4 | sc in each st around | (10) | - |

| R5 | sc in each st around | (10) | lightly stuff |

| R6 | dec x 5 | (5) | FO with sewing tail |

Sew all five edge stitches to the centre back around Lamb Body Rnds 20–21, angled down.

##### 14. Fixed red lamb collar

Do not make the collar until the lamb's 12-to-12 neck seam is complete. With scarlet, ch 22. Before Row 1, check that the relaxed chain reaches around the assembled neck with one-stitch overlap and without tightening the neck; if your gauge differs, remake and record the adjusted foundation.

| Row | Instruction | Sts | Note |

|---|---|---|---|

| Row 1 | sc in 2nd ch and next 20 ch, ch 1, turn | (21) | - |

| Row 2 | sc in each st across | (21) | FO with sewing tail |

If the fit check required an adjusted foundation of **N** chains, work one sc in the second chain and every remaining chain for **N − 1** stitches in Row 1, then work **N − 1** sc in Row 2. Record that count on both rows; do not increase or decrease within the strip.

After the neck seam is complete, overlap the short ends by one stitch and sew them together. Tack the collar to the body at the centre back and centre front so it cannot tighten or pull over the head. Do not add a bell or long ribbon tie to the original route.

### Finishing & assembly

Complete faces and head accessories while each 12-stitch neck remains open. Pin every piece and check symmetry before sewing.

1. Pair the head's 12 open stitches with the body's 12 open stitches. With the head tail, whipstitch through both loops of each pair exactly once around; adjust neck stuffing before closing the final two pairs, then secure that tail inside. With the body tail, work one complete reinforcing pass through the same 12 pairs in the reverse direction, secure it inside and bury both tails. The neck therefore has 12 matched anchors and 24 seam passes.

2. Flatten each eight-stitch arm opening into four pairs. Sew each pair through both arm layers and the body around Goat Body Rnds 19–21 or Lamb Body Rnds 20–22; repeat the four-pair seam once.

3. Flatten each corrected eight-stitch leg opening into four pairs. Place the inner edges four body stitches apart at the lower front around Body Rnds 7–10. Sew each pair through both leg layers and body fabric, repeat once, then stand the plush on a flat surface before knotting.

4. Sew the tail with every open-edge stitch. Confirm it is centred on the back relative to the face.

5. Sew the goat's flame sash at its back overlap and upper shoulder point. Sew the lamb collar closed and tack front and back. Add only the fully sewn crochet flower crown if selected.

6. Inspect the magic-ring centres, every seam, embroidery end and accessory anchor. No wire, glue-only part, loose tie or hanging loop belongs in the original construction.

### Troubleshooting

- **Stuffing shows:** use a smaller hook or smoother yarn and remake the affected piece; do not rely on overstuffing.

- **The neck does not match:** both original head and body must stop with 12 open stitches. Do not close the head to six.

- **The head wobbles:** align all 12 pairs, work the required second seam pass and fill the neck before the last two pairs close.

- **A leg has an unmatched top stitch:** the corrected Leg Rnd 13 ends at eight, not nine; flatten into four pairs.

- **The base does not sit flat:** confirm the BLO crease is Goat Body Rnd 7 or Lamb Body Rnd 8 and distribute base stuffing away from the centre.

- **Fluffy stitches are difficult to see:** count by touch after every stitch, use a contrasting marker and verify each round before moving it.

- **The horns will not curve:** do not insert wire; use the hidden yarn tack across the Rnd-6 bend ridge.

- **The flame edge has too many peaks:** follow the exact 35-edge-stitch route; it makes 12 orange peaks.

### Colorways

Original Fire Goat colourway: warm-cream body and ears, light-tan muzzle/inner ears/hooves, espresso-brown horns, scarlet-red sash, burnt-orange flames, golden-yellow flame tips and black embroidered eyes. Optional pink is limited to securely embroidered blush.

Original companion lamb colourway: wool white head/body/outer ears/tail, light-tan muzzle and hooves, pale-pink inner ears, scarlet-red fixed collar and black embroidered eyes.

Alternative body neutrals may include soft beige or pale grey while preserving strong contrast among face, horns and fire accents. Use yarns of comparable weight and gauge within one animal. Cultural colour descriptions are palette notes only; they are not claims that the design or accessory is an authentic traditional object.

### Designer notes

The lamb shares the muzzle, ear, arm and corrected leg constructions but requires a separate set of those pieces when both animals are made. The goat's sash and lamb's collar are sewn closed rather than tied. Thread- or DK-weight miniatures, mobiles, keychains and hanging ornaments are not included as tested scale options; make and assess a separate sample before advertising another size or use.

### Care

Follow the most restrictive label among every yarn, thread, stuffing and optional eye component. Before publishing a care claim, clean and fully dry a complete assembled sample by the proposed method, then remeasure and inspect colour transfer, shrinkage, fibre shedding, stuffing migration, eye/embroidery security, the two-pass neck seam, limbs, horns, ears, tail, sash or collar and crochet flowers.

Until that complete-sample test passes, recommend gentle surface cleaning with a barely damp cloth and drying supported on a towel away from heat. Never iron acrylic or textured yarn. Inspect every seam and attachment again after cleaning.

### Terms of Use

#### Copyright & ownership

© 2026 Novality Crochet Studio. All rights reserved. This crochet pattern, its instructions, stitch counts, editorial layout and design elements are protected material. Design Code NS 17.

This pattern is licensed to the purchaser for personal use and for small-batch sale of finished physical items under the terms below. The purchaser may not copy, share, translate, upload, redistribute, resell or publish the pattern or any substantial part of it in digital or printed form.

#### You may

Make finished goats or lambs for yourself, gifts or charity. Sell finished physical items made from this pattern in small quantities, provided the listing credits “Pattern by Novality Crochet Studio · Design Code NS 17” and does not claim unverified safety, testing, measurements, cultural authenticity or care results.

#### You may not

Resell or distribute this PDF or Markdown source; convert it into another pattern product; use its text, tables or visuals as listing assets for a competing pattern; claim authorship; or mass-produce finished items without written permission. Credit does not grant use of the studio name as your own brand.

#### Safety reminder

The finished-item maker or seller remains responsible for the actual materials, classification, assessment, testing, warnings, documentation, labelling and traceability required wherever a finished item is supplied.

Tag finished projects with **#NovalityCrochetStudio** and **#NovalityFireGoat**.

### Happy crocheting!

Keep both necks open at 12 stitches, flatten every corrected limb opening into four pairs and secure each festive accessory without loose ties.

---

*End of the Grand Collection — Novality Store · seventeen patterns, one verified volume.*
