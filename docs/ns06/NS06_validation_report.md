# NS-06 — Momo the Loaf Cat — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/05_NS06_momo_the_loaf_cat.txt` (verbatim original)
Corrected master: `docs/ns06/NS06_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Tail | better than a stuffed one | better than a filled one | line stuffs and does not stuff |
| 2 | Base note | no matter how you stuff it | no matter how firmly it is filled | stuff verb precedes the eye step in the piece |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns06/spec.py`,
  hero `docs/ns06/assets/momo_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Momo_the_Loaf_Cat_NS06_NovalityStore.pdf`.
- Print: `shop/Momo_the_Loaf_Cat_NS06_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).
