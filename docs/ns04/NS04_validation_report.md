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
| 6 | Rnd 5 arithmetic note | parenthesised '(7 stitches made)' counts | spelled 'making nine/twelve/three' (re-spaced in round 3) | one line stated more than one stitch count |
| 7 | Muzzle seam | Sew about three quarters ... through the remaining opening | 'three quarters'; opening sentence reworded | opening + approximate pair on one line |
No stitch count, repeat multiplier, chain length or decrease schedule was altered.

## Round 3 correction — Rnd 5 leg spacing (geometry, not arithmetic)

The Rnd 5 row put the front legs over stitches 6-8 and 16-18 of the Rnd-4 round while the back legs
sit over 1-3 and 13-15. That leaves 2 plain stitches between the left pair, 4 across the front,
**0** between the right back leg and the right front leg, and 6 across the back. Four feet cannot
form a rectangle from those positions, and two legs almost side by side is exactly the tip-forward /
tip-back failure the troubleshooting section warns about.

Rnd 5 now reads `[sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc`:

- made 9 - 3 - 12 - 3 - 3 = 30 (the stated total is unchanged);
- worked 6 + 3 + 9 + 3 + 3 = 24 (every stitch of Rnd 4, unchanged);
- front legs over stitches 7-9 and 19-21, back legs over 1-3 and 13-15, so all four joins have
  exactly 3 plain stitches between neighbours and sit at the corners of a square.

The Rnd 5 explanation, the stitch-arithmetic sentence and the "Coco tips forward or backward"
bullet were reworded to match. The footprint sentence now uses the pattern's own gauge
(36 sc = 52 mm, i.e. 4.5 mm per stitch): 30 stitches = 135 mm round, about 43 mm across at Rnd 5,
and 24 stitches about 34 mm at Rnd 4. The previous "about 65 mm across and 29 mm front to back"
was not derivable from that gauge.

Re-verified after the change: auditor 0 problems / 0 unparsed, engine 0 errors / 0 warnings.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns04/spec.py`,
  hero `docs/ns04/assets/coco_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Coco_the_Capybara_NS04_NovalityStore.pdf`.
- Print: `shop/Coco_the_Capybara_NS04_PRINT_EDITION_BW.pdf` (greyscale spread 0 on every page).
