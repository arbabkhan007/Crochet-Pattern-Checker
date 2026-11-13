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

## Review round 2 — hand-review corrections (7 October 2026)

1. **Lamb collar could not fit the neck (size, and a genuine count change).** The collar was founded on ch 22 — about 10.5 cm relaxed at DK gauge — to be sewn around an assembled 12-stitch neck of about 6 cm, so it would hang loose by roughly 4 cm. **Fix:** ch 14 (about 6.5 cm relaxed) with Row 1 `sc in 2nd ch and next 12 ch` = 13 stitches and Row 2 = 13 stitches. **This does change a stitch count** (21 → 13 for this component); it is recorded here and in the collection front matter rather than hidden behind a "counts never changed" claim. The auditor re-derives Row 1 = 13 from ch 14 and Row 2 = 13 with 0 problems, and the instruction still tells the maker to check the relaxed chain around the assembled neck before working Row 1.
2. **Collar yarn quantity followed the chain.** 9 m / 10 yd → about 6 m / 7 yd for the shorter collar.
3. **Unverifiable citation removed.** The calendar reference cited a Smithsonian URL (`si.edu/spotlight/lunar-year-goat`) that could not be resolved from the build environment, so it is no longer safe to print as a source. **Fix:** the reference now states only what can be checked from the calendar system itself — the 6 February 2027 lunar-new-year date and the Fire Goat (Ding Wei) naming follow the traditional sixty-year sexagenary cycle. Both facts were confirmed correct and are unchanged; only the citation was removed.
4. **Branding unified.** Hashtag #NovalityCrochetStudio → #NovalityStore; copyright/credit line now matches NS-01 to NS-15.
5. **Verification framing corrected.** Cover chip now *5-AXIOM MATH VERIFIED ON PAPER*, cover card "Paper-verified: no sample crocheted". No NS-17 animal has been crocheted; the seated-height conflict noted in the file's own front matter remains open until a sample is measured.

Note for the collection front matter: the leg Rnd 13 correction (the source's 12 → 9 final round was changed to 12 → 8 so the flattened seam has no unmatched stitch) *is* a change to a decrease schedule, so the earlier blanket claim that no decrease schedule was ever changed does not hold for NS-17.

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 14 pp, print 14 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
