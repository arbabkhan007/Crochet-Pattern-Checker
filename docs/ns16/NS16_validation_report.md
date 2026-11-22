# NS-16 — Mini Stocking Advent Garland — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/14_NS16_mini_stocking_advent_garland.txt` (verbatim original)
Corrected master: `docs/ns16/NS16_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Abbreviations | - RS / WS — right side / wrong side | split into two lines | right and wrong side on one line read as both facing |
| 2 | Yarn | about 14–18 m / 15–20 yd | about 16 m / 17 yd | quantity range |
| 3 | Batch maths | about 336–432 m / 360–480 yd | about 380 m / 410 yd | quantity range |
| 4 | Gauge note | opening circumference | leg circumference | opening + approximate pair |
| 5 | Notions | 2–2.5 m / 6–8 ft | 2.2 m / 7 ft | quantity range |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns16/spec.py`,
  hero `docs/ns16/assets/stocking_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Mini_Stocking_Advent_Garland_NS16_NovalityStore.pdf`.
- Print: `shop/Mini_Stocking_Advent_Garland_NS16_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).
