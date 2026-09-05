# Validation Report — Willow the Bunny Lovey (Design Code NS 10)

**Validated with:** Crochet Pattern Checker (deterministic stitch-count engine + granny-square growth model)
**Files:** `patterns/willow_bunny_lovey_v1_original.txt` (as received) → `patterns/willow_bunny_lovey_v2_fixed.txt` (corrected)
**Driver:** `tools/validate_willow.py` · **PDFs:** `deliverables/Willow_the_Bunny_Lovey_Crochet_Pattern_NS10.pdf` (+ `_print` edition)

**Result: v1 = 18 findings / 10 blocking errors · v2 = PASS (0 errors, 12/12 checks green)**

---

## Errors found in the pattern as received (v1)

| # | Location | Problem | Fix applied in v2 |
|---|----------|---------|-------------------|
| 1 | HEAD | **Round 3 missing** (jumps R2→R4). R4 `(2 sc, inc) x 6` needs 18 sts but R2 leaves 12 — count chain broken | Added `R3: (sc, inc) x 6 (18)` |
| 2 | HEAD | **Round 5 missing.** R6 needs 30 sts but R4 leaves 24 | Added `R5: (3 sc, inc) x 6 (30)` |
| 3 | HEAD | **Round 10 missing** — only 3 of 5 plain rounds at 36 sts were written | Added `R10: sc in each st around (36)` |
| 4 | HEAD | **R11 `[3 sc, dec] x 6` consumes only 30 of 36 sts** — 6 stitches left unworked; count chain broken (36 → 24 is impossible with `[3 sc, dec]`) | R11 is now `[4 sc, dec] x 6 (30)`; ladder runs 36→30→24→18→12→6 |
| 5 | HEAD | Decrease ladder had only 4 decrease rounds from 36 sts (36→24→18→12→6), skipping 30 — head would pucker | **Head is now 15 rounds**: `[4 sc, dec]`, `[3 sc, dec]`, `[2 sc, dec]`, `[sc, dec]`, `dec` — one round each. Height claim updated 5.3 → 5.7 cm |
| 6 | EARS | **Round 3 missing.** R4 states 12 sts but R2 leaves 9 — validator flagged Rnds 4–8 stating (12) while producing (9) | Added `R3: (2 sc, inc) x 3 (12)` |
| 7 | EARS | **Round 10 missing.** R11 `(sc, dec) x 3` consumes only 6 of the 9 available sts; 9 → 6 needs an intermediate round | Added `R10: sc in each st around (9)`; R11 now consumes 9 → produces 6 |
| 8 | BLANKET | Gauge section said “Check on the blanket after **Rnd 3**: 9 dc…”, but Rnd 2 has **no side spaces** — the earliest a 9-dc edge measurement can exist is **Rnd 4** (Rnd 3 has one 3-dc group per side) | Reworded to “after Rnd 4” |
| 9 | BLANKET | Rnd 2 as printed leaves you on the far side of the square; the standard “sl st into the next corner space” join was described only implicitly | Made the corner-space join explicit for Rnd 2 and added a written **Rnd 3 setup round** |
| 10 | Spec | “Roughly **33 cm from ear tips to the opposite corner**” is not reproducible from the stated gauge (26 cm square ⇒ 36.8 cm bare diagonal; assembled distance with the head is ≈ 25 cm) | Replaced with “approx. 25 cm from ear tips to corner, depending on ear flop”; noted 37 cm blanket diagonal |

## Non-blocking issues also fixed

- Yarn quantity given only in grams — added **approx. 140–150 m** and a “buy two 50 g balls” tip.
- “Do not tumble dry — it will felt” — cotton **does not felt** (that is a wool property). Reworded to shrinkage/clumping risk.
- Joined-round instruction said “turning chain” while also saying “no turns” on the blanket — standardised as **ch-3 starting chain that counts as a dc, never turn**.
- Construction of blanket Rnds 3–20 (“+12 dc per round”) had no worked example of a side-space round — Rnd 3 is now written out in full.
- Ears note said “sew to Rnds 4-6” — ambiguity between attachment rounds and ear rounds clarified on both head and ear tables.

## Checks that PASS unchanged (verified, not touched)

| Check | Result |
|---|---|
| Granny-square checkpoints R3=36, R5=60, R10=120, R15=180, R20=240 dc | ✓ (+12 dc/round model) |
| 60 dc per edge at R20 ≈ 26 cm at 4.3 mm/dc | ✓ (25.8 cm) |
| Growth ≈ 1.3 cm per side per round; 18/20/22 rounds ≈ 23/26/28 cm | ✓ (23.2 / 25.8 / 28.4 cm) |
| Border = 240 sc + 12 corner sc = 252 sc | ✓ |
| Gauge probe 9 dc ≈ 39 mm | ✓ (38.7 mm) |
| Head diameter 36 sts ≈ 4.9 cm | ✓ (4.93 cm) |

## Repo repairs made to run the above

- `src/crochet_checker/validation/__init__.py` imported a nonexistent `validator` module, breaking every import of the validation package (including the CLI). Restored the working pipeline imports (kept in `__init__.py.backup`) while retaining `multipiece`.
- `src/crochet_checker/pdf/generator.py` was a placeholder that wrote `.txt` instead of PDFs; `crochet-check pdf` therefore could not produce a PDF. Left untouched (out of scope) — this run used `tools/generate_willow_pdf.py` (fpdf2), since WeasyPrint is unavailable in this environment (no Pango system libraries, no root).

Re-run anytime:
```bash
.venv/bin/python tools/validate_willow.py patterns/willow_bunny_lovey_v2_fixed.txt   # → PASS
.venv/bin/python tools/generate_willow_pdf.py                                        # → deliverables/*.pdf
```
