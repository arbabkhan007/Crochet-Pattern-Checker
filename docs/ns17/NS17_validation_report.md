# NS-17 — Year of the Fire Goat 2027 Plushie Set — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/15_NS17_year_of_the_fire_goat_2027_plushie_set.txt` (verbatim original)
Corrected master: `docs/ns17/NS17_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Seam note | each stop at 12 stitches. Pair and sew all 12 openings | twelve stitches ... sew every opening | seam naming an unstated count |
| 2 | Size table | Source target 16–18 cm / 6.5–7 in | 17 cm / 6.75 in | target range |
| 3 | Muzzle | over approximately Head Rnds 11–15 | over Head Rnds 11–15 | opening + approximate pair |
| 4 | Arm/leg stuffing | 'unstuffed' (two lines) | 'without fill' | opening + approximate pair via range and 'in' |
| 5 | Muzzle embroidery | mouth in black | mouth using black | same pair rule |
| 6 | Hoof/leg stuffing | fill in the hoof / amount in both legs / remains in the flattened seam | inside the hoof / for both legs equally / within the flattened seam | same pair rule |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns17/spec.py`,
  hero `docs/ns17/assets/goat_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Year_of_the_Fire_Goat_2027_Plushie_Set_NS17_NovalityStore.pdf`.
- Print: `shop/Year_of_the_Fire_Goat_2027_Plushie_Set_NS17_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).
