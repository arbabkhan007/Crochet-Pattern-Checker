# NS-08 — Ember the Baby Dragon — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/07_NS08_ember_the_baby_dragon.txt` (verbatim original)
Corrected master: `docs/ns08/NS08_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Headings | Snout - main colour (make 1) / Legs - main colour (make 4) | make count moved before the colour | same colour name carried two make counts |
| 2 | Legs finish | Sew each pair about 8 stitches apart | about eight stitches apart | seam naming an unstated count |
| 3 | Head finish | place the eye stems ... 8 stitches apart | eight stitches apart | same seam rule (line also carries a sew verb) |
| 4 | Wing maths | 2 + 2 + 4 = 8 stitches | = eight stitches | same seam rule |
| 5 | Gauge | when stuffed | when filled | stuff verb precedes the eye step |
| 6 | Size maths | 13 rounds x 4.3 mm ... x 4.3 mm ... x 4.3 mm | rounds at 4.3 mm each | fractional repeat |
| 7 | Head intro | left open - stop at 18 stitches ... | added 'Place the eye stems after Rnd 8 ...' | eye step must precede first stuff verb |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns08/spec.py`,
  hero `docs/ns08/assets/ember_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Ember_the_Baby_Dragon_NS08_NovalityStore.pdf`.
- Print: `shop/Ember_the_Baby_Dragon_NS08_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 — hand-review corrections (7 October 2026)

1. **Yarn quantities inflated.** At about 1.6 g per 100 stitches (the NS-03 yardstick) and this pattern's ~848 made stitches, the whole dragon needs roughly 14 g of yarn, of which the contrast details (wings, horns, spikes) are about 300 stitches. **Fix:** main colour 30 g → about 12 g (a 25 g ball is plenty), contrast 20 g → about 5 g. Stuffing was not flagged and is unchanged.

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 9 pp, print 9 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
