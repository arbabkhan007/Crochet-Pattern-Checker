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
