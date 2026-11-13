# Edition 2 Change Report — All 17 Patterns

Scope: Edition 2 was regenerated from the Edition 1 review files with every confirmed correction from the critique assessments applied. Masters (`patterns/`) and all PDFs are unchanged; Edition 1 files (`reviews/ns01-ns06/`, `reviews/ns07-ns12/`, `reviews/ns13-ns17/`, `deliverables/All_17_Reviewed_Patterns_For_Checking.md`) are preserved untouched for comparison.

Every Edition 2 pattern states near its top that the edition is **untested**: no pattern has been test-crocheted, and arithmetic agreement is not physical validation. Where Edition 2 changes construction or proportions (NS01, NS04, NS05, NS06, NS08, NS10), the headline dimensions were replaced with "pending sample" language rather than carrying over Edition 1 estimates.

**Validation performed (written arithmetic only):** table-driven audit re-run over all 17 files — 710 counted records, 15 explicit scoped records, 3,074 assertions, 0 errors — plus a 6-test regression suite (`reviews/edition-2/check_tests.py`) covering mutation detection, the NS04 reference map, NS09 turtle symmetry, the NS13 star wrap and NS17 sash modules. The shared audit module is `tools/pattern_release_audit.py` (also bundled inside the ZIP's `tools/` folder so `verify.py` runs standalone).

Below, per design: **Fixed** = confirmed defect corrected; **Retained** = critique proposed a redesign but the existing workable choice was kept with an accurate description; **Untested** = a redesign was adopted or a physical property asserted that still needs a sample.

## NS01 — Hamish the Highland Cow
- **Fixed:** Head rebuilt to 48 sts with seven plain rounds (R9–15) and decreases R16–20 to an 18-st opening that now matches Body R19 (open 18). Eyes now placed at R11/12, muzzle R13–16.
- **Fixed:** Ears rebuilt as flat layered 18-st pieces; belly reduced to a smaller 24-st oval; hoof back-loop round moved to the colour-change round; fringe count made flexible; scarf changed to a measured candidate (ch 91 / 90 hdc) with a 40 cm ribbon allowance to fit.
- **Untested:** New head/body proportions and finished size; sample must be measured before any dimension is published.

## NS02 — Kawaii Halloween Mini Set
- **Fixed:** Wing rewritten (ch 15, skip 3, then 4 dc / 4 hdc / 4 sc) with a short End B root attachment; partial leaf corrected 12→14; narrow pumpkin eye spacing corrected.
- **Fixed:** Bulky inner ears replaced with pink embroidery; ghost optional base/filling clarified.
- **Untested:** Wing stiffness and leaf curl in the specified yarn.

## NS03 — Axel the Axolotl
- **Fixed:** New neck variant (R12→20, R13 plain 20, R14→24). Tail given a side-to-side closure with dorsal anchor and a flexible unfilled transition.
- **Retained:** The ruffled fin is kept and now explicitly described as a decorative ruffle, not an anatomical flat paddle.
- **Untested:** Neck join behaviour and tail posture once stuffed.

## NS04 — Coco the Capybara
- **Fixed:** All four legs now identical 8-round pieces. Join map corrected with an explicit reference grid: R4 joins BL1 new sts 1–3 and BL2 new sts 7–9; R5 joins FL1 old sts 13–15 and FL2 old sts 19–21; centres at 2, 8, 14, 20. A physical marker between the front-leg pair replaces the old spiral-start assumption.
- **Untested:** Stance/elevation is no longer guaranteed in the text; the sample must stand unaided before any stability claim returns.

## NS05 — Little Duck Plushie
- **Fixed:** Wing reduced 12→8, flattened into 4 pairs. Eyes at R17/18; beak placed below (near R15–17) and pinned before sewing; smaller R1-only beak is now the primary candidate.
- **Fixed:** Chenille alternate start secured.
- **Untested:** Beak size in chenille vs worsted; both candidates need samples.

## NS06 — Momo the Loaf Cat
- **Fixed:** Front/back narrow oval ends defined; five plain wall rounds (R8–12); closure at R19; face worked after R12 before stuffing; diagonal four-anchor ear surface rows 4→2→1; tail placed near rear R10.
- **Untested:** Loaf silhouette and wall height with the new plain-round structure.

## NS07 — Pocket Positivity Trio
- **Fixed:** Smaller 10-st chest patch from ch 5. Assembly order corrected: eyes/washers first, then patch and beak, then stuffing. Sunflower petal right side made explicit and handedness-neutral.
- **Retained:** No total yarn metreage is stated, because none could be substantiated; makers are directed to weigh a sample instead of the pattern inventing a figure.
- **Untested:** Patch scale against the sunflower face.

## NS08 — Ember the Baby Dragon
- **Fixed:** Head gains 3 plain rounds, opening at R14 = 18. Eyes R8/9 placed after R11; snout R10–12. Wing Row 2 gradient corrected; ch 2 used for the starting dc; short End A root attachment.
- **Fixed:** Spikes made modular with a measured fit; legs no longer carry estimated elevations.
- **Untested:** Head/snout proportions and spike spacing along the back seam.

## NS09 — Shelby the Sea Turtle Bag Charm
- **Fixed:** Symmetric anchor points: small — head 4, flippers 9, 13, 19, 23; large — head 8, flippers 16, 24, 34, 42. Outputs 35/53 sts.
- **Fixed:** Appendage rounds worked in FLO so the reserved BLO can be used as the seam loop; the shell's own BLO rim is unchanged. A physical orientation check is included before seaming.
- **Untested:** Whether FLO appendages sit correctly against the BLO seam in both sizes; the exact-text case was updated with the FLO change and orientation flagged untested.

## NS10 — Willow the Bunny Lovey
- **Fixed:** Ears rebuilt to 21 rounds, open 8 / fold 4 pairs; head sphere/height assertion removed.
- **Retained:** The blanket is kept as designed.
- **Untested:** The "9 cm ear" claim was removed; ear length must be measured on a sample.

## NS11 — No-Sew Christmas Gnome
- **Retained:** Full-circumference bands kept intentionally and now described accurately as full bands rather than implied decorative stripes.
- **Fixed:** Optional BLO R6 base fold added; text no longer guarantees stability from it.
- **Untested:** Base fold benefit at finished size.

## NS12 — Bobble Christmas Tree
- **Retained:** Six bobbles per tier kept; text now states accurately that density increases upward.
- **Fixed:** A rigid disc is inserted after R11 before narrowing closes the base.
- **Untested:** Disc diameter must be confirmed against a worked base.

## NS13 — Christmas Ornament Bundle
- **Fixed:** Star wrap clarified: "original 1" is the last fan anchor. Snowflake's redundant final join removed.
- **Retained:** The snowflake edge is described as rounded lace, not picot-pointed.
- **Untested:** Wrap tension and star point definition.

## NS14 — Bobble Snowflake Tree Skirt
- **Retained:** Ladder/border kept, with the non-identical 12-sector motif phase now disclosed.
- **Fixed:** Border now starts on the same joining stitch. The guaranteed 4–5 cm centre opening claim removed: the completed gauge piece must pass the pole, otherwise another design is required.
- **Untested:** Centre opening at real gauge; motif phase appearance.

## NS15 — Interchangeable Christmas Wreath
- **Fixed:** Soft loop restricted to supported flat display; the pattern no longer guarantees an unsupported door wreath.
- **Fixed:** Bow rebuilt as a fabric loop with a separate 49 sc × 2 strip, two 14-sc tails and a 5 sc × 4 band. Snowflake rounded; redundant join removed.
- **Untested:** Loop firmness and bow proportions at full size.

## NS16 — Crochet Mini Stocking Advent Garland
- **Fixed:** Row 10 now reads "2 sc, dec; ch 1, turn" (WS turn restoring RS). Pickup arithmetic corrected: 3 heel + 5 side + 10 instep + 5 side = 23; R2 `7sc, dec, 5sc, dec, 5sc, dec` → 20. This row is now under exact-text prose coverage so a regression to "do not turn" fails the audit.
- **Retained:** Cuff described as "horizontally ridged", matching what the stitch actually produces.
- **Untested:** The sparse stepped-heel pickup is explicitly flagged; the pattern instructs stopping if the fabric puckers or holes appear, and makes no physical decrease-equivalence claim.

## NS17 — Year of the Fire Goat 2027 Plushie Set
- **Fixed:** Goat tail R8–10 / lamb tail R9–11 placed low on the back; natural ear-base footprint added; sash made modular — measured before selecting the module count.
- **Fixed:** Yarn statement corrected to a shared tan 250 sts plus goat 32 inner-ear sts, replacing unsupported differing metre allowances.
- **Untested:** Sash module fit on both bodies; tail placement on a stuffed sample.

## What was deliberately NOT done
- No blind redesigns: where a critique proposed changing a workable aesthetic choice (NS03 fin, NS11 bands, NS12 bobble density, NS13 snowflake edge, NS14 motif phase), the design was retained and the **description** corrected instead.
- No physical claims were upgraded. Every fit, size, stability, capacity and safety statement still requires a complete sample; toy-safety compliance (ASTM F963 / EN 71 etc.) remains the maker/seller's responsibility as stated in each pattern.
- Masters and PDFs were not regenerated; PDF/print editions still reflect the pre-Edition-2 text and should not be reissued until Edition 2 is sample-tested.
