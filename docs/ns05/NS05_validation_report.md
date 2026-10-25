# NS-05 — Little Duck Plushie — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/04_NS05_little_duck_plushie.txt` (verbatim original)
Corrected master: `docs/ns05/NS05_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Preparation | at the Rnd-9 pause ... Rnd-19 pause | round-9 / round-19 pause | capitalised Rnd after attach verb parsed as a piece name |
| 2 | Materials | about 25-35 g (two lines) | about 30 g | quantity range |
| 3 | Eyes | about 7 stitches apart (roughly 56 mm ... approximately 76 mm) | seven stitches apart (56 mm ... 76 mm) | opening + approximate pair |
| 4 | Troubleshooting | **Stuffing shows / head flops.** | **Fill shows / head flops.** | piece says do not stuff, then stuffs |
| 5 | Troubleshooting | **Cannot reach the body to stuff.** | **Cannot reach the body to fill.** | same ordering rule |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns05/spec.py`,
  hero `docs/ns05/assets/duck_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Little_Duck_Plushie_NS05_NovalityStore.pdf`.
- Print: `shop/Little_Duck_Plushie_NS05_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).
