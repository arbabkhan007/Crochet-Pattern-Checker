# NS-10 — Willow the Bunny Lovey — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/09_NS10_willow_the_bunny_lovey.txt` (verbatim original)
Corrected master: `docs/ns10/NS10_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly. The corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor (granny Rnd 2 and the Rnds 3-20 continuation carried as explicit expected counts).

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Troubleshooting | go up a hook or add rounds (22 rounds = ~28 cm) | go up one hook size or add rounds; 22 rounds measure about 28 cm | hook within 32 chars of a cm value |
| 2 | Finished size | approximately 40-44 cm (16-17.5 in) | about 42 cm (16.5 in) | finished size must not be a target range |
| 3 | Head finish | opening ... The finished head is about 4.9 cm | measurements moved to their own line | opening + approximate pair |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns10/spec.py`,
  hero `docs/ns10/assets/willow_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Willow_the_Bunny_Lovey_NS10_NovalityStore.pdf`.
- Print: `shop/Willow_the_Bunny_Lovey_NS10_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).

## Review round 2 (7 October 2026)

The round-2 hand review of 7 October 2026 examined geometry, finished sizes and gauge, yarn quantities, front-matter claims, leftover editorial text and branding across all seventeen masters. **No defect was raised for NS-10** and the pattern text is unchanged from the version audited in this report.

Both store PDFs were nevertheless recompiled so that all seventeen editions carry the same cover framing: the chip now reads *5-AXIOM MATH VERIFIED ON PAPER*, the verification card reads "Paper-verified: no sample crocheted", and the cover carries the explicit note that no sample was crocheted, blocked, weighed or measured. Page counts are unchanged (colour 7 pp, print 7 pp, greyscale spread 0 on every page).
