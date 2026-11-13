# NS-11 — No-Sew Christmas Gnome — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/10_NS11_no_sew_christmas_gnome.txt` (verbatim original)
Corrected master: `docs/ns11/NS11_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor (body-table continuation fragments carried as explicit expected counts).

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Dialect | 'UK terms' column header and banner | 'UK equivalent' | piece marked UK while using US 'sc' |
| 2 | Finished size | About 11-12.5 cm (4.5-5 in) | About 12 cm (4.75 in) | target range |
| 3 | Materials | 40-50 g / 10-15 g / 20-30 g | 45 g / 12 g / 25 g | quantity ranges |
| 4 | Safety | Lock their washers ... BEFORE stuffing | Insert the safety eyes and lock their washers ... BEFORE stuffing | eye verb before first stuff verb |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns11/spec.py`,
  hero `docs/ns11/assets/gnome_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/NoSew_Christmas_Gnome_NS11_NovalityStore.pdf`.
- Print: `shop/NoSew_Christmas_Gnome_NS11_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 — hand-review corrections (7 October 2026)

1. **Finished height counted the flat base rounds (geometry).** Rnds 1-5 are worked flat and become the gnome's base; they add width, not standing height. Counting only what stands up — wall rounds R6-R15 at about 4.6 cm plus the eight tapering hat rounds at about 3.2 cm — gives about 8 cm, not the stated 12 cm. The 12 cm figure is what you get by treating all 23 rounds as height. **Fix:** finished size now reads about 8 cm (3.25 in) with the reasoning stated and the figure labelled a paper estimate.
2. **Knock-on size options.** The mini option (through Rnd 21, omitting the plain Rnd 22) drops roughly two rounds of height: 8-9 cm → about 6 to 6.5 cm. The large option adds three 30-stitch body rounds on chunky yarn and a 5 mm hook: 15 cm → about 11 to 12 cm.
3. **Yarn quantities inflated.** ~530 stitches for the whole gnome is about 9 g at 1.6 g per 100 stitches, against the 67 g previously listed. **Fix:** body + hat 45 g → about 9 g, beard 12 g → about 2 g, face 10 g → about 1 g, stuffing 25 g → about 10 g, all labelled as paper estimates.
4. **Nose position wrong.** "The nose sits on the round before the hat-colour change" — the nose bobble is Rnd 14 and the colour change is Rnd 16, two rounds later. **Fix:** the sentence now names both rounds.

**Sampling caveat:** the height arithmetic is sound on paper but was not measured on a sample; confirm with a swatch or the first gnome before repeating the figure in a listing.

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 7 pp, print 7 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
