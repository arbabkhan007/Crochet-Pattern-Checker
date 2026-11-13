# NS13–NS17 written-pattern review

Reviewed 13 November 2026 against the five user-uploaded `NS13_corrected.md` through `NS17_corrected.md` files. These uploads, not the repository's independently revised master collection, are the source for this batch.

## Deliverables and status

Use `NS13_reviewed.md` through `NS17_reviewed.md`. Originals, existing masters, earlier review batches and existing PDFs/archives were not overwritten. The ZIP includes reviewed Markdown, this report, source checksums, a full source-to-review diff and reproducible checks.

**Written review only: not test-crocheted, load-tested, fit-tested or safety-certified.** Main count sequences were generally consistent already; most changes address instructions that could fail despite correct totals. Any new construction option also needs physical sample testing.

## Corrections by pattern

### NS13 — Christmas Ornament Bundle

- Added missing stitch marker and blocking pins to the notions; filling is required for the described stuffed bauble, not merely an optional material.
- Corrected the claim that the first six-stitch bauble round determines finished size, and clarified that start and closure are opposite poles.
- Added explicit fasten-off, reinforcement and end-weaving steps to hanging loops.
- Fixed the snowflake loop location. Its written arm has two ch-3 side arches around three tall stitches, not a single central ch-3 tip. The loop now attaches to the middle US tr / UK dtr's top loops, keeping the arm construction unchanged.
- Preserved the correct five-point star: ten centre anchors, five six-stitch fans and five anchoring slip stitches = 35 counted stitches, with tip chains excluded.

### NS14 — Bobble Snowflake Tree Skirt

- Preserved the complete, correct 12-per-round ladder, including R9, R10 and R12, all three stop counts, twelve independent surface spokes and the exact border route.
- Corrected the gauge discussion: twelve added stitches at 12 dc/10 cm imply approximately 1.59 cm additional radius only in an ideal flat-circle model. This does not prove actual round gauge or account for the finite centre opening and bobbles. Persistent cupping is not guaranteed to disappear with blocking.
- Used one metric planning gauge consistently rather than mixing exactly 3 stitches/in with exactly 1.2 stitches/cm. Unbordered model diameters are about 44.6, 73.2 and 101.9 cm at R14/23/32; these remain models, not measurements. The common 4 in/10 cm swatch label is rounded.
- Added centre-fit checks after R1 and the gauge piece: twelve dc worked into a 20- or 24-chain ring may draw it inward even if the bare chain fits.
- Limited the repeat-count formula to N ≥ 2; R1 is twelve dc into the ring, not twelve repeats consuming old stitches.
- Clarified “closed ring/no slit,” dye-lot purchasing per colour, and removed stale PDF page/bookmark claims and the assertion that this revision matches an unchanged full-colour edition.

### NS15 — Interchangeable Christmas Wreath

- Supplied a standard/large tube starting-hook recommendation instead of referring to a hook column absent from the size table; it still requires a fabric sample.
- Distinguished the 12-stitch standard/large tube from the 8-stitch mini throughout the gauge, construction and final seam instructions.
- Made the poinsettia's travel to each new centre anchor explicit before its ch-4 petal, avoiding an unintended bridging chain between petals.
- Clarified that loops/tails are one connected bow piece, followed by fastening off and making the band separately; normalized the equivalent UK band wording.
- Replaced the mini's ordinary doubled-yarn hanger with the same load-rated woven-cord/ribbon requirement stated in the safety section.
- Replaced advice to push filling through a closed seam or disguise the join with a wrap: reopen, adjust and resew the matched pairs. A large soft ring may still sag; no unsupported structural guarantee is made.

### NS16 — Mini Stocking Advent Garland

- Added the missing AC-to-MC transition after Heel Row 10 so Foot R1 actually returns to the stated main colour.
- Clarified that the cuff starting chain does not mean turn the joined rounds.
- Clarified the hanging-loop location above the midpoint of the ten-stitch heel, rather than automatically at the round-start join.
- Made toe-tail finishing workable using access through the open cuff instead of an unexplained instruction to knot inside an already cinched toe.
- Flagged the sparse five-pickups-per-side heel route as unverified. Pickups must cover the whole edge from the outset; “spread them over a longer span” cannot solve all puckering. If redistribution still fails, stop for a sample-led heel/gauge revision rather than silently changing the count.
- Retained the correct turned Row 6, partial rows 10 → 7 → 5 → 4 → 3, pickup 5 + 10 + 5 + 3 = 23, evening round 23 → 20, and toe 20 → 16 → 12 → 8 → 4. Arithmetic alone does not prove that the pickup lies flat.

### NS17 — Fire Goat and Companion Lamb

- Corrected the inference that summed head/body round depth contradicts seated height. Round depth follows shaped fabric, not a straight vertical line; it cannot prove or disprove the source height target.
- Moved muzzle embroidery and end security to the accessible open muzzle before attachment, avoiding reliance on hand access through a stuffed twelve-stitch neck. Clarified sewn-tail security for the head accessories and neck.
- Corrected the flame edging so every peak is a same-anchor ch-3 loop. Previously the first was a same-anchor loop but the remaining eleven bridged between consecutive edge stitches. Peak positions remain 1, 4, 7, …, 34, with stitch 35 as the final anchor.
- Added a complete modular sash fit option rather than instructing the maker to force a potentially too-short 35-stitch diagonal strip: M peaks need ch 3M, two rows of (3M − 1) sc, then the first peak plus (M − 1) three-stitch modules and the final anchor. Example: 13 peaks, ch 39, 38 sc per row. Pin the finished strip and allow additional yarn.
- Corrected the lamb collar's stray DK-gauge reference and required a fit check after both rows, since a starting chain is not a reliable finished-strip measurement.
- Clarified that two complete circuits around twelve matched neck pairs give 24 pair-wise sewing stitches, not 24 circuits. Kept the correct eight-stitch limb openings/four pairs and twelve-to-twelve neck seams. “Sit,” not “stand,” is now used for the seated-pose check.

All five received repaired Markdown table spacing and a clear written-review status note. Existing safety, care-testing and classification cautions were preserved.

## Validation and how to repeat it

From the repository root:

```sh
python reviews/ns13-ns17/verify.py
python -m pytest tests/validation/test_ns01_ns06_review.py \
  tests/validation/test_ns07_ns12_review.py \
  tests/validation/test_ns13_ns17_review.py -q
```

Observed final results:

- **235 counted row/round records**
- **16 explicitly handled noncount instruction records**
- **1,078 assertions; zero errors**
- **9 tests for this batch; all 19 tests across the three review batches passed**

`stitch-ledger.json` records counted instructions and separately identifies foundations, surface work, hangers, chain-space motifs, ties and borders whose counts require different treatment. A wreath round repeated to a measured length is checked as a representative round; no fixed total number of tube rounds is invented. Shared animal pieces are checked once per written table, not multiplied by the number of animals or limbs. The bow's four-row band is a composite instruction checked at its five-stitch row count.

The audit reuses the repository's canonical arithmetic, exact-text manual cases and US/UK term translator, with a batch-specific table reader that handles NS14's leading checkbox column and the `UK equivalent` headings. `half treble` and `htr` are treated as synonymous. It checks table widths, stated counts, consumption transitions, repeated-round lengths, both terminology columns where provided, and the partial heel rows explicitly.

`special-cases.json` binds exceptional table instructions to explicit reviewed arithmetic or a stated noncount scope. `prose-checks.json` binds the sash/flower/ear/collar/neck instructions, stocking colour and pickup route, garland spacing, border stop counts and snowflake hanger to reviewed text. These are exact-text reviewed cases, **not a general English interpreter or physical simulation**. Unknown changed instruction sequences fail rather than silently receiving a pass.

Mutation tests deliberately introduce: a wrong skirt increase, wrong UK translation, wrong partial-heel count, unknown instruction, inconsistent range length, wrong modular sash foundation, wrong border scallop count and a wrong heel-to-foot colour instruction. Each is rejected.

### Construction calculations checked separately

- NS13: star uses 2 × 5 = 10 anchors and makes (1 + 6) × 5 = 35 counted stitches. Snowflake round 2 uses all twelve ring stitches to form six ch-5 spaces; round 3 places one arm in each space, with three tall stitches and two slip stitches per arm, plus side chains.
- NS14: round N ends at 12N. Stop counts 168, 276 and 384 divide by six to give 28, 46 and 64 border scallops. Each repeat consumes 1 + 2 + 1 + 2 = 6 anchors and produces 1 + 5 = 6 stitches; the join-anchor final skip is intentional, not an extra stitch. Spokes remain separate join-to-FO routes with variable stitch counts.
- NS15: standard/large seams match twelve end pairs; mini matches eight. Six poinsettia petals each use their own centre anchor. Leaves use all seven working chains. Bow tails each have fourteen sc; band has four rows of five. Centreline diameter estimates use tube length divided by pi, not outside diameter.
- NS16: heel Row 7 consumes eight of ten, produces seven and leaves two; Row 8 consumes six of seven, produces five and leaves one. Rows 9/10 consume all active stitches. Pickup 23; three decreases consume all 23 and produce 20. Twenty-four stocking centres create 23 gaps; a 200 cm cord with 20 cm end allowances leaves 160 cm usable span, roughly 7 cm per gap.
- NS17: regular ear 6 → 4 → 4 → 2, longer ear 7 → 5 → 5 → 3; longer-ear base folds as three pairs plus the central stitch. Baseline sash: 1 + 11×3 + 1 = 35 edge anchors, twelve loops, last peak at 34. Thirteen-peak variant: ch 39 → 38 sc, last peak at 37, final anchor at 38. Neck two circuits × twelve pairs = 24 pair-wise sewing stitches.

### General checker results and limits

Also ran `crochet-check check --json` on all five reviewed files. It reported **zero stitches counted in every file**. It returned PASS for NS13/NS17 and ERROR for NS14/15/16 (2/4/13 findings). These are not evidence that the tables pass or fail: examples include treating US prose in a dual-terminology document as UK, misreading compound band/tube instructions, interpreting UK dc as US dc for a turning chain, and flagging ordinary stocking prose as undefined abbreviations.

The exact summary is saved as `general-checker-summary.json`. These findings were inspected rather than hidden; the application engine was not modified to suppress them. The dedicated audit above is the relevant written arithmetic evidence, not the zero-coverage PASS verdicts.

## Remaining sample/testing work — do not skip

1. **Tree skirt:** make the circular gauge piece and a full chosen size; verify relaxed centre opening after working into the ring, flatness, actual bobble/round gauge, spoke tension and border. No amount of arithmetic guarantees the closed centre will pass over the actual hardware. Do not cut a slit or force-block severe distortion.
2. **Stocking:** physically sample the whole turned heel and sparse five-pickup edges. Correct stitch totals do not establish adequate pickup density, heel projection or usable capacity. Do not market this route as physically validated.
3. **Wreath:** check whether the slender stuffed tube holds its intended ring under its own weight and decorated load. Assess the installed hook/cord/system; wrapping a rated cord does not make an untested crocheted object rated.
4. **Animals:** check diagonal sash overlap before edging, including any modular resize; collar fit after both rows; muzzle placement, stuffed-neck stability, horn curvature and seated balance. Check that the optional crown does not interfere with the horn bases.
5. **Ornaments:** sample the snowflake's arm shape and revised hanger, block with a fibre-appropriate method, and inspect all loop anchors. Do not promise that the written motif achieves a photograph's silhouette without making it.
6. Weigh materials, measure and time complete samples, and test the proposed cleaning method. Evaluate all loops, cords, hardware, detachable accessories, stuffing and seams for actual use and destination market. No certification or age-suitability conclusion is supplied.

The NS17 Lunar New Year paragraph was retained; no new external calendar citation or cultural-authenticity verification was obtained in this review. No external safety-standard verification is claimed. Resources actually used were all five uploads, repository audit/checker source and documentation, manual arithmetic/construction review and local tests. Existing PDFs and alternate editions are not synchronized with these Markdown revisions.
