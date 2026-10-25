# NS-02 — Kawaii Halloween Mini Set (Boo · Pip · Bramble) — Validation Report

Auditor: `docs/kit/audit_lib.py` v2 (independent re-derivation of every round/row table)
Engine: `docs/kit/engine_run.py` over `src/crochet_checker` deterministic stages
Source: `docs/intake/02_NS02_kawaii_halloween_mini_set.txt` (verbatim original)
Corrected master: `docs/ns02/NS02_corrected.md`

## Verdict: SOUND — zero arithmetic corrections

Every instruction table re-derives exactly; the corrected master runs **0 errors / 0 warnings**
on the engine and **0 problems / 0 unparsed rows** on the independent auditor (100 % of rows
simulated, including picot fans, FLO shell repeats and the corkscrew cord).

## Tables re-derived (all exact)

| Piece | Span | Count path |
|---|---|---|
| Boo body | R1-R12 + hem R13 | 6 → 26 (R8 `[11 sc, inc] x 2`) → 24 (R12) → hem into FLO of R12 |
| Boo arms (make 2) | R1-R2 | 6 → 8, no stuffing |
| Boo base (optional) | R1-R2 | 6 → 24 edge sts, matched 1:1 to the 24 free back loops of R12 |
| Pip body | R1-R14 | 6 → 36 (R6) → 24 (R10 `[3 sc, dec] x 6`, overfill) → close |
| Pip stem | R1-R4 | 6 → 8, sewn over the round-13 opening |
| Pip curl | Foundation | ch + 2 sc per chain corkscrew |
| Bramble body | R1-R16 | 6 → 24 (R7) → 30 (R9) → 24 (R13) → close |
| Bramble ears (2 pairs) | R1-R3 | 6 → 12 → flat, no stuffing |
| Bramble wings (make 2) | Rows 1-3 | Row 2 = 12; Row 3 = 9 sl st + 6 + 4 + 4 fan sts = 23 counted + 3 picots |
| Cord (optional) | Found. | ch 20; 2 sc in each of 19 chains from the 2nd = 38 |

Cross-checks: wing anchor maths 2 + 3 + 2 + 2 = 9 slip-stitch anchors + 3 fan anchors = the 12
Row-2 stitches (stated in the pattern and confirmed); Boo eye spacing five stitches on the
26-stitch widest round stays inside the face; garland yarn totals (25/30/27/12/6 g) consistent
with three of each mini; gauge line 36 sts ≈ 40 mm across a stuffed Pip body matches 3.5 mm/st.

## Corrections made (clarity / engine grammar only — no counts changed)

| # | Where | Original wording | Corrected wording | Why |
|---|---|---|---|---|
| 1 | Pip stem finish | "sew to the top centre over the Rnd 13 opening" | "…over the round-13 opening" | engine parsed capitalised "Rnd" after a sew-verb as a piece name |
| 2 | Boo eyes | "about 5 stitches apart … so 5 apart keeps them…" | "about five stitches apart … so five apart…" | a seam verb + digit + "stitches" must name a previously stated count; spacing is not a seam |
| 3 | Wing anchor maths | "9 Row-2 stitches … all 12 Row-2 stitches" | "9 stitches of Row 2 … all 12 stitches of Row 2" | "-2 stitches" read as a negative measure |
| 4 | Picot technique | "a loose picot loops, a tight one curls under" | "a slack picot loops, while an over-tight one curls under" | tight/loose pair inside one line reads as one round worked both ways |
| 5 | Pip face order | face paragraph after stuffing references | added "Embroidered face order: place the two triangle eyes … before any filling goes in" at the head of the Pip section | engine requires the eye step to precede the first stuff verb in the piece |
| 6 | Bramble R13 note | "stuff firmly" | "fill firmly" | same eye-before-stuff ordering rule (eyes paragraph follows the table) |
| 7 | Garland yarn | "an extra 3-5 g of sage", "allow another 3-5 g sage" | "an extra 4 g of sage", "allow another 4 g sage" | yarn quantity must be a weighed amount, not a range |

No stitch count, repeat multiplier, chain length or finished measurement was altered.

## Store edition

- Compiler: `docs/kit/build_store_pdf.py` (generic, spec-file driven), spec `docs/ns02/spec.py`,
  hero `docs/ns02/assets/halloween_trio_hero.png` (illustrative render, labelled as such on the cover).
- Colour: `shop/Kawaii_Halloween_Mini_Set_NS02_NovalityStore.pdf` (9 pp).
- Print: `shop/Kawaii_Halloween_Mini_Set_NS02_PRINT_EDITION_BW.pdf` (9 pp, greyscale spread 0 on
  every page, ink coverage 4.2 - 10.8 % per page).
