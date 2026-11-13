# Corrections Applied — User-Supplied NS01–NS17

Source: the 17 “neat and clean” patterns supplied for checking. Output: `reviews/user-supplied-v2/NS01_corrected.md` … `NS17_corrected.md`, combined in `deliverables/All_17_User_Supplied_Patterns_Corrected.md`.

## Blocking defects fixed

- **NS04 Coco** — Leg tops now close exactly: legs decrease 9 → 6, then flatten to a true 3-st strip that the body join consumes. Join map rebuilt around marked centre lines: R4 back legs over R3 sts 1–3 / 8–10 (producing R4 sts 1–3 / 10–12); R5 front legs through R4 sts **14–16** and **21–23**, centred on front-centre R4 st 19, fully clear of both back legs. R5 still consumes 24 → produces 30.
- **NS06 Momo** — R5 rewritten to `11 sc, inc, sc, inc, 11 sc, inc, sc, inc, 16 sc` = **44 consumed → 48 produced** (supplied line was 36 → 40 against a claimed 48), with increase pairs directed to the narrow ends. Ear geometry fixed with centre-line counting: bases occupy sts 3–6 each side, leaving exactly 4 unworked stitches between inner edges; eye positions restated the same way.
- **NS10 Willow** — Border rewritten to scallop **all 9 interior clusters** per side, with a per-side count check (1 corner fan + 9 scallops + sl sts in all 10 spaces); R2 corner entry now states the slip-stitch path.
- **NS11 Gnome** — Base disc corrected to **4.5 cm flexible** (30-st base Ø ≈ 4.55 cm at gauge), inserted after R8 by flexing it flat onto the base; R12 insertion note removed. R17 clarified (back loops of R16, not the reserved R15 loops). Height restated to ≈14.5 cm (32 rnds at gauge).
- **NS12 Tree** — 7.5 cm disc moved to **after R9** (opening still 48 sts, Ø ≈ 7.6 cm) instead of R15 (30 sts, Ø ≈ 4.8 cm — impossible). Finished size corrected to ≈10.5 × 7.6 cm at gauge.
- **NS14 Tree Skirt** — Centre opening corrected to **≈6.4 cm Ø** (24-ch ring = 20 cm circumference) with an explicit pole-fit check; Mini scallop count corrected **24 → 28**; Alt-Large (R29) diameter separated (≈96 cm) from Large R31 (≈102 cm); BO defined as a bobble only (“popcorn” removed).
- **NS16 Stocking** — Foot R2 rewritten to `7 sc, dec, 5 sc, dec, 5 sc, dec` = **23 consumed → 20 produced** (supplied line was 19 → 16 against a claimed 20). Pickup points specified (2 step stitches + 3 row-ends per side) with a first-stocking hole check; hanging loop restated over the two centre stitches (5/6) of the heel.

## Local fixes and claim corrections

- **NS01** — Passed; assembly now assigns one pass per sewing tail, belly patch moved to R10–R17 (stops at the first decrease round), ear layers aligned by marked first stitches, safety note added.
- **NS02** — Ghost arm closure completed: 5-st opening flattened 3-over-2 with the unpaired fold stitch closed by a sl st and caught in the seam. Safety note added for 6 mm eyes in miniatures.
- **NS03** — Limb closure specifies the 9th (fold) stitch; ventral fin pass now names its exact rounds (centre stitch of R38–R33) and stopping point. Safety note added.
- **NS05** — Feet fixed by decreasing to 8 before the toe round, so the flattened front is exactly 4 pairs; wing base width corrected 28 → 32 mm at gauge; safety-eye guidance added.
- **NS07** — Materials reconciled: per-pal amounts total **≈11.5 g** (DK metreage ≈23–29 m by brand) instead of the contradictory “~16–18 m / ~6 g total”. Waddle base now decreases through both loops (no loop ridge). Strong embroidered-eye recommendation for the 4 cm pals.
- **NS08** — Dorsal spike strip lengthened 21 → 29 sts (spikes at sts 1, 5, 9, 13, 17, 21, 25) so the crown-to-tail-tip path is actually reachable; “check it reaches on your sample” retained.
- **NS09** — Stitch/symmetry maps were already exact and are unchanged; finished sizes corrected to gauge (**Standard ≈3.5 cm, Bigger ≈5.5 cm** long including head fan) in place of the impossible 6.0 / 8.5 cm.
- **NS13** — Star/snowflake/bauble counts were already exact; bauble cap now has an explicit closure (flatten, sl st through 3 pairs) before the ch-16 loop.
- **NS15** — Torus sizing kept; added the missing **gauge** (10 sc × 11 rnds = 5 cm) that the tube thickness/diameters depend on, and the support sequence made explicit: crochet the tube straight, thread/gather it onto the ring or insert wire, stuff around the support, *then* whipstitch the ends.
- **NS17** — Sash changed from a fixed 44-st strip with an unsupported 1–2 st overlap claim to a **measured, modular** strip (tape-measure the diagonal; 2 sts per cm; flame-peak repeat works to any length; 44 sts still gives exactly 15 peaks). Long-ear folded base corrected to 4 sts outer / 3 sts inner (≈2 cm). Lamb collar given a try-on adjustment (±2 ch = 1 cm).

## Verification

`reviews/user-supplied-v2/verify.py` — file inventory (17), NS06 R5 44→48, NS16 Foot R2 23→20 and pickup 3+5+10+5=23, NS04 R5 24→30 with front legs clear of back-leg sts 10–12, NS14 scallop division 168/288/360/384 → 28/48/60/64, NS09 underside 24 loops → 35 sts, and absence of the supplied defective instruction lines. **Result: OK, 0 errors.**

## Still requires a physical sample

Arithmetic is now internally consistent, but NS04 (new join map), NS06 (new R5 shaping), NS08 (strip reach), NS09 (restated sizes), NS10 (border drape), NS11/NS12 (disc fit), NS14 (pole opening), NS16 (heel pickup density) and NS17 (sash/collar fit) should each be test-crocheted once before commercial release. Yarn quantities and “approx.” sizes remain gauge-based estimates.
