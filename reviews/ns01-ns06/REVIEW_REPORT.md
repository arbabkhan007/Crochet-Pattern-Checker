# NS01–NS06 written-pattern review

Reviewed 13 November 2026. Source: the six user-uploaded `NS01_corrected.md` through `NS06_corrected.md` files, not the repository's separately revised masters.

## Deliverables

Use `NS01_reviewed.md` through `NS06_reviewed.md` in this folder. Original uploads and the existing master collection, PDFs and ZIPs were not overwritten. These are written-review editions, **not test-crocheted or safety-certified releases**.

## Corrections by pattern

| Pattern | Changes |
|---|---|
| NS01 — Hamish | Added the missing explicit head cinch; reconciled hoof colour-change timing between the two leg tables; corrected the floating-hoof advice (shortening is not inherently a solution); made shortened front legs start more upright rather than at the long-leg angle; replaced guaranteed ball yield and square-of-height yarn scaling; removed instructions to rely on a washer click or overstuff the base. |
| NS02 — Halloween set | Added the omitted optional hat yarn; explicitly closed Pip's six-stitch opening before sculpting; corrected the turned leaf row so increases actually land on its far-end three-stitch group; added wing-mirroring instructions; replaced overstuffing with firm filling without stretching. |
| NS03 — Axel | Corrected feet to be stuffed before closing; clarified that the main-yarn ball does not include contrast yarns; corrected advice that larger/looser fin stitches would reduce crowding; specified the eight-anchor route for the four-shell alternative; removed advice to ignore hidden fuzzy-yarn counting errors. |
| NS04 — Coco | Corrected the impossible three-pair join from a nine-stitch leg rim: back legs decrease to six on R8; front legs retain nine on R8 and decrease to six on R9. All six rim stitches are now caught by three joining sc. Kept body-round counts unchanged. Replaced stale `7 sc, 10 sc, 7 sc` troubleshooting with the actual R5 sequence; clarified R4 reference-anchor spacing; corrected the inconsistent 3.5 mm gauge calculation to 4.5 mm; removed the claim that stitch spacing proves a physical rectangle. |
| NS05 — Duck | Removed the apparent duplicate wing-closing instruction; explicitly omitted R23 in the smaller-head option and clarified its 24-stitch opening, stuffing and face fitting; kept the head empty until eye embroidery and beak attachment are complete. |
| NS06 — Momo | Reconciled the eye-installation pause to after R9; added the missing four-stitch tail-tip closure and starting-end security; removed absolute claims about round bases, 36-stitch bases and a single count determining shape. |

All six: repaired blank lines within Markdown tables and added a prominent review-status note identifying sizes, material allowances and timings as estimates. Preserved the uploaded safety/compliance cautions; no legal certification or age-suitability determination was made.

## Arithmetic and coverage

Run from the repository root:

```sh
python reviews/ns01-ns06/verify.py
python -m pytest tests/validation/test_ns01_ns06_review.py -q
```

Observed results: **299 table instruction records, 1,215 assertions, zero errors; 3 regression tests passed.** `stitch-ledger.json` lists the actual instruction text, line, consumed anchors and produced stitches. Counts are per written row, not multiplied by the number of identical components. Chain-only foundations are tracked as available working chains.

The audit reuses `tools/pattern_release_audit.py` for table reading, canonical arithmetic and exact-text manual cases. Noncanonical cases are explicit arithmetic checks, not a general-language parser; changed unknown instructions fail instead of being silently passed. Coco's branch row is checked explicitly. Pip's turned leaf deliberately consumes 11 of 14 anchors, leaves 3 unworked and produces 14 stitches. The tests include deliberate count and unknown-instruction mutations.

Manual construction checks additionally covered: Hamish's 18-to-18 head/body seam; 18-to-24-to-30-to-36 oval expansion; Boo's 24-anchor/48-stitch hem and matching optional base; Bramble's 12-anchor/23-counted-stitch wing edge plus picots; Axel's 6-to-3 tail closure and ten-anchor/five-shell fin; Coco's three-layer leg joins and 18-to-24-to-30 body join rounds; Duck's 4-working-chain/10-stitch beak and 16-stitch second round; Momo's 48-stitch base, 5-to-3-to-2 ears and four-stitch surface tail. These checks do not demonstrate the finished silhouette.

### General checker limitations

Also ran the repository's `crochet-check check --json` on all six reviewed files. It reported **zero stitches counted for every file**. It returned PASS for NS01/03/05 and ERROR for NS02/04/06 (1/50/1 errors respectively). Those verdicts are not proof of these tables: ordinary Coco prose was reported as undefined abbreviations, for example. No general-checker PASS was substituted for the table audit, and the application engine was not changed to hide warnings.

## Remaining sample-testing work

- Crochet at least one complete sample of each design, plus any alternate size, pose or smaller-head option to be sold. Verify the face placement, seams, fin fullness, wing orientation, leaf shape and stability.
- Coco's revised six-stitch leg openings are arithmetically sound but need physical testing for joining access and fit. R4/R5 attachment heights cannot be obtained reliably by simply multiplying round count by gauge.
- Momo's oval footprint does not guarantee its quoted width or loaf silhouette. Circularly distributed upper decreases, filling and tension affect the final shape.
- Hamish's muzzle rim and head seam can crowd each other; pin the muzzle below the eyes while leaving the neck seam accessible. Leg angles are starting suggestions, not measured support geometry.
- Gauge-based circumference/diameter estimates are not measured widths. Multiplying all rounds by row height overestimates vertical contribution on shaped surfaces. Measure and replace estimated dimensions before claiming an exact size.
- Weigh yarn (including fringe, seams and optional accessories) and filling, time sample production, and test the proposed cleaning method. The optional fuzzy-gill strand may change gauge and needs a material allowance.
- Face spacing measured along stitches is an arc, not a straight-line distance. Pin/mark symmetrically before inserting eyes or embroidering.
- Assess loose fringe, ribbons, long garland cords, small components, fibre shedding and attachments for the intended use. Workshop pull checks and embroidered eyes do not establish product compliance.

No external standards text or physical measurements were obtained. Resources actually used: all six uploads, repository documentation/source and table audit, the general checker, independent arithmetic/construction review, and local regression tests. No visual simulation or online resource can replace a made sample.
