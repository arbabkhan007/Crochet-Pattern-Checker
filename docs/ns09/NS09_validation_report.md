# NS-09 — Shelby Sea Turtle Bag Charm — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/08_NS09_shelby_sea_turtle_bag_charm.txt` (verbatim original)
Corrected master: `docs/ns09/NS09_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Shell join | Sl st to the first Rnd-8 sc | Sl st to the first sc of this round | '-8 sc' read as a negative measure |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns09/spec.py`,
  hero `docs/ns09/assets/shelby_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Shelby_Sea_Turtle_Bag_Charm_NS09_NovalityStore.pdf`.
- Print: `shop/Shelby_Sea_Turtle_Bag_Charm_NS09_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 — hand-review corrections (7 October 2026)

1. **Header and materials disagreed.** The header promised "~3 g of yarn" while the materials listed 1 g shell + 1 g body = 2 g. The stitch count supports the header: ~203 made stitches ≈ 3.2 g at 1.6 g per 100 stitches. **Fix:** shell yarn 1 g → about 2 g, so the list totals about 3 g and matches the header. (The header figure is grams of yarn, not metres; ~203 stitches is about 3 m of DK, which is where the slip came from.)

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 6 pp, print 6 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
