# NS-07 — Pocket Positivity Trio — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/06_NS07_pocket_positivity_trio.txt` (verbatim original)
Corrected master: `docs/ns07/NS07_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor (petal row carried as an explicit expected count in `docs/kit/audit_overrides.py`).

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Safety | Calling a smiling, stuffed item | Calling a smiling, filled item | stuff verb precedes the eye step |
| 2 | Safety | lock every washer ... BEFORE stuffing | insert the six 5 mm safety eyes and lock every washer ... BEFORE stuffing | eye verb must appear before first stuff verb |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns07/spec.py`,
  hero `docs/ns07/assets/trio_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Pocket_Positivity_Trio_NS07_NovalityStore.pdf`.
- Print: `shop/Pocket_Positivity_Trio_NS07_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 — hand-review corrections (7 October 2026)

1. **Yarn weight and hook contradicted the gauge (the pattern's central sizing claim).** The materials listed #4 worsted on a 3.5 mm hook, but the stated gauge — about 3.5 mm per stitch and 3.2 mm per round — is the DK-on-2.5 mm gauge used in NS-02 and NS-09. Worsted on 3.5 mm measures about 4.5 mm per stitch and 4.3 mm per round in those patterns, which would make the trio about 3.9 / 4.9 / 3.5 cm rather than the stated 3.0 / 3.8 / 2.7 cm. The pattern's own "bigger trio" option confirms the DK reading: it calls 4.5 mm per stitch "about 1.3x the original gauge", which is only 1.3x if the original is 3.5 mm. Yarn use also matches DK — about 8 m for roughly 550 stitches is a DK-scale consumption, not a worsted one.
   **Fix:** materials changed to DK cotton (#3) on a 2.5 mm hook, keeping the gauge, the stitch counts and the finished sizes exactly as written. Knock-on hook references updated with it: the petal-round escape hook 4 mm → 3 mm (two places) and the "looser gauge" troubleshooting hook 3 mm → 2.25 mm. The doubled-yarn warning now refers to DK on 2.5 mm. The bulky #5 / 4.5 mm "bigger trio" option is unchanged and remains internally consistent.
   **Alternative not taken:** keeping worsted on 3.5 mm and enlarging the stated sizes to 3.9 / 4.9 / 3.5 cm. The DK reading was preferred because the gauge, the yarn consumption and the 1.3x comparison all point to DK, and the trio is described as pocket-sized.

Re-verification after these edits: engine **0 errors / 0 warnings**; independent table audit **0 problems / 0 unparsed rows**. Both store PDFs were recompiled from this master (colour 7 pp, print 7 pp, greyscale spread 0 on every page) and the cover now reads *5-AXIOM MATH VERIFIED ON PAPER* with an explicit paper-verified note: no sample was crocheted, blocked, weighed or measured, so sizes, yarn quantities and times remain targets.
