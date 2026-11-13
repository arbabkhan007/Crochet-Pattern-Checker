# NS-13 — Christmas Ornament Bundle — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/12_NS13_christmas_ornament_bundle.txt` (verbatim original)
Corrected master: `docs/ns13/NS13_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Dialect | 'UK terms' header | 'UK equivalent' | marked UK while using US 'sc' |
| 2 | Dialect | UK column abbreviation 'htr' | 'half treble' spelled out | US-marked piece may not carry UK-only term |
| 3 | Finished size | Bauble about 3.5-4 cm | about 3.75 cm | target range |
| 4 | Materials | (5-15 g) | (about 10 g each) | quantity range |
| 5 | Yarn table | 8-10 g / 6-8 g / 4-6 g | 9 g / 7 g / 5 g | quantity ranges |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns13/spec.py`,
  hero `docs/ns13/assets/ornament_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Christmas_Ornament_Bundle_NS13_NovalityStore.pdf`.
- Print: `shop/Christmas_Ornament_Bundle_NS13_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 — hand-review corrections (7 October 2026)

1. **Yarn quantities inflated across all three ornaments.** The bundle's ~177 made stitches total about 2.8 g at 1.6 g per 100 stitches, yet the table listed 9 g + 7 g + 5 g = 21 g. The bauble alone is about 144 stitches ≈ 2.3 g. **Fix:** bauble 9 g → 3 g, star 7 g → 2 g, snowflake 5 g → 2 g (each with a little allowance for tails and a hanging loop).

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 7 pp, print 7 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
