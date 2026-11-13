# NS-15 — Interchangeable Christmas Wreath — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/13_NS15_interchangeable_christmas_wreath.txt` (verbatim original)
Corrected master: `docs/ns15/NS15_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor (prose component rows carried as continuation rows in `audit_overrides.py`).

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Dialect | 'UK terms' headers (5 tables) | 'UK equivalent' | marked UK while using US 'sc' |
| 2 | Dialect | UK column 'htr' | 'half treble' | US-marked piece may not carry UK-only term |
| 3 | Band row | UK 'ch 1, turn, dc across' | 'ch 1, turn, 1 dc in each st across' | literal short dc turning chain |
| 4 | Finished size | three tube ranges + poinsettia/bow ranges | single nominal values (22/92/125 cm; 3.5 in) | target ranges |
| 5 | Materials | 150-200 g | 175 g | quantity range |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns15/spec.py`,
  hero `docs/ns15/assets/wreath_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Interchangeable_Christmas_Wreath_NS15_NovalityStore.pdf`.
- Print: `shop/Interchangeable_Christmas_Wreath_NS15_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 — hand-review corrections (7 October 2026)

1. **One yarn figure for three different wreath sizes, and no stuffing figure.** The materials listed a single "175 g" for a base that can be made in three tube lengths (22 cm mini, 92 cm standard, 125 cm large) and gave no stuffing quantity at all, even though the join instructions require stuffing the tube. The 92 cm tube alone is about 2,500 single crochets ≈ 40 g at 1.6 g per 100 stitches, so 175 g was roughly four times the standard size and eight times the mini.
   **Fix:** per-length yarn estimates — mini (22 cm tube) about 12 g including attachments, standard (92 cm tube) about 40 g, large (125 cm tube) about 55 g — plus the missing stuffing estimates (mini about 2 g, standard about 8 g, large about 12 g of fibre fill). All are labelled paper estimates to be weighed on the first tube. No counts involved.

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 11 pp, print 11 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
