# NS-12 — Bobble Christmas Tree — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/11_NS12_bobble_christmas_tree.txt` (verbatim original)
Corrected master: `docs/ns12/NS12_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Dialect | 'UK terms' header | 'UK equivalent' | marked UK while using US 'sc' |
| 2 | Finished size | About 15-16 cm tall in chunky | About 15.5 cm tall in chunky | target range |
| 3 | Materials | 60-80 g | 70 g | quantity range |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns12/spec.py`,
  hero `docs/ns12/assets/tree_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Bobble_Christmas_Tree_NS12_NovalityStore.pdf`.
- Print: `shop/Bobble_Christmas_Tree_NS12_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 — hand-review corrections (7 October 2026)

1. **Finished height counted the flat base rounds (geometry).** Rnds 1-9 are worked flat and form the tree's base disc; they add width, not standing height. The remaining 17 rounds taper by six decreases every two rounds, which gives a cone about 7 cm tall — not the stated 12 cm, which is what counting all 26 rounds produces. **Fix:** finished size now reads about 7 cm (2.8 in) tall and 7 cm wide, with the reasoning stated and labelled a paper estimate. The chunky-yarn option follows: 15.5 cm → about 9.5 cm.
2. **Three-size set range.** "Sizes stair-step from about 9 cm to 16 cm" was derived from the same over-count. **Fix:** about 5.5 cm to 9.5 cm (DK + 3 mm, worsted + 4 mm, chunky + 5 mm).
3. **Yarn quantity inflated.** ~700 made stitches plus 42 bobbles is about 15 g at 1.6 g per 100 stitches (bobbles consume several times the yarn of a plain stitch, which is why the estimate sits above the bare stitch count), against the 70 g previously listed. **Fix:** main yarn 70 g → about 15 g, labelled a paper estimate. Stuffing unchanged.

**Sampling caveat:** as for NS-11, the cone height is arithmetic, not a measurement; confirm on a sample.

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 7 pp, print 7 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
