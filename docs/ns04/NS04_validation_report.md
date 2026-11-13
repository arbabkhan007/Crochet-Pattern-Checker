# NS-04 — Coco the Capybara — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/03_NS04_coco_the_capybara.txt` (verbatim original)
Corrected master: `docs/ns04/NS04_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Materials | fibre filling about 5-8 g | about 6 g | yarn/fill quantity must be a weighed amount, not a range |
| 2 | Size maths | 20 rounds x 4.3 mm = 86 mm | 20 rounds at 4.3 mm each, about 86 mm | 'x 4.3' reads as a fractional repeat |
| 3 | Spiral note | do not join and do not chain 1 | there is no join and no turning chain | join verb + prohibition reads as join and not join |
| 4 | Leg-join technique | The stitches you don't join bunch up | The stitches you skip bunch up | same join/prohibition pair |
| 5 | Ears & muzzle finish | Ears: ... do not stuff - a shallow cup. Muzzle: ... stuff lightly | split into two lines; ears 'leave them empty' | one line may not stuff and not stuff |
| 6 | Rnd 5 arithmetic note | parenthesised '(7 stitches made)' counts | spelled 'making seven/ten/seven' | one line stated more than one stitch count |
| 7 | Muzzle seam | Sew about three quarters ... through the remaining opening | 'three quarters'; opening sentence reworded | opening + approximate pair on one line |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns04/spec.py`,
  hero `docs/ns04/assets/coco_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Coco_the_Capybara_NS04_NovalityStore.pdf`.
- Print: `shop/Coco_the_Capybara_NS04_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 — hand-review corrections (7 October 2026)

1. **Front-leg layout was lopsided (geometry).** The back legs are joined in Rnd 4 over body columns 1-3 and 13-15, i.e. centred on columns 2 and 14, exactly opposite each other with nine columns between them on each side. The previous Rnd 5 joined the front legs over columns 6-8 and 16-18, which puts the four leg centres at columns 2, 7, 14 and 17 — gaps of 5 / 7 / 3 / 9 columns. That is not a rectangle, and the text's claim that "the 7-10-7 spacing centres each front leg between the two back legs" was false: one front leg sat four columns off centre, the other two columns off.
   **Fix (count-preserving):** Rnd 5 is now `[sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc`. The joins fall on columns 7-9 and 19-21, so every neighbouring pair of legs is separated by exactly three plain columns (3 / 3 / 3 / 3) and each front leg is centred halfway between the back legs. Worked = 6 + 3 + 9 + 3 + 3 = 24 (every stitch of Rnd 4), made = 9 + 3 + 12 + 3 + 3 = 30, still six increases and none worked through a leg. The auditor re-derives Rnd 5 = 30 from Rnd 4 = 24 with 0 problems; the prose was rewritten to state the new groups (9-3-12-3-3) and the column positions.
2. **Footprint figure not derivable (size).** "About 65 mm across and 29 mm front to back" cannot come from the stitch count: 30 stitches at roughly 3.5 mm each give about 105 mm of circumference, i.e. about 34 mm across the body at the leg joins, with the splayed legs adding some width beyond that. **Fix:** the sentence now gives the derived body width (about 34 mm) and tells the maker to measure the splayed footprint on the finished piece instead of quoting a printed number.
3. **Yarn quantity inflated.** At the collection's own yardstick (NS-03: about 940 stitches ≈ 15 g, i.e. roughly 1.6 g per 100 stitches) and this pattern's ~707 made stitches, the main colour needs about 11-12 g of fabric plus tails, seaming and swatch allowance. **Fix:** main 30 g → about 16 g, face yarn 5 g → about 2 g, both labelled as paper estimates to be weighed on the first Coco.

**Sampling caveat:** items 1 and 2 were established by column and circumference arithmetic on paper, not by crocheting a sample. They are very likely correct, but the leg alignment and footprint should still be confirmed on the first Coco before the figures are repeated in a listing.

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 8 pp, print 8 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
