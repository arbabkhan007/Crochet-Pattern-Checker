# Validation Report — Novality Pattern Line (Design Codes NS 01–NS 10)

**Validated with:** Crochet Pattern Checker (deterministic round-chain engine + size-claim model)
**Drivers:** `tools/validate_willow.py` (Willow) · `tools/validate_pattern.py` (NS 01–09)
**Sources of truth:** `patterns/*_v1_*` (as received) → `patterns/*_v2_*` (validated & corrected)
**Deliverables:** 20 PDFs in `deliverables/` (retail + print edition × 10 patterns)

---

## Results at a glance

| Code | Pattern | Rounds checked | Errors found | Status after fixes |
|---|---|---|---|---|
| NS 01 | Hamish the Highland Cow | 79 (8 pieces) | 0 math · 2 presentation | PASS |
| NS 02 | Kawaii Halloween Mini Set | 71 (11 pieces) | 0 math · 3 interleaved tables + 2 claims | PASS |
| NS 03 | Axel the Axolotl | 52 (4 pieces) | 0 | PASS |
| NS 04 | Coco the Capybara | 37 (4 pieces) | 0 math · 1 interleaved table | PASS |
| NS 05 | Little Duck Plushie | 29 (3 pieces) | 0 · 1 internal note removed | PASS |
| NS 06 | Momo the Loaf Cat | 27 (3 pieces) | 0 math · 1 size claim | PASS |
| NS 07 | Pocket Positivity Trio | 38 (7 pieces) | 0 | PASS |
| NS 08 | Ember the Baby Dragon | 58 (7 pieces) | 0 | PASS |
| NS 09 | Shelby the Sea Turtle | 28 (4 pieces) | 0 | PASS |
| NS 10 | Willow the Bunny Lovey | 40 (3 pieces) | **10 blocking** | PASS (see v1 log below) |

**Totals: 419 rounds verified · 46 size-claim checks computed from stated gauge · all 10 patterns PASS.**

## Willow NS 10 — the only pattern with blocking errors (fixed)

Full findings log in the v1 section of the Git history; summary:

1. **HEAD missing Rnds 3, 5, 10** — count chain broken (R4 needs 18 sts, R2 leaves 12; R6 needs 30, R4 leaves 24; only 3 of 5 plain 36-st rounds present).
2. **HEAD R11 `[3 sc, dec] x 6` impossible after 36 sts** — consumes only 30; corrected to `[4 sc, dec] x 6 (30)` and the ladder completed 36→30→24→18→12→6 → **head is 15 rounds** (height claim 5.3 → 5.7 cm).
3. **EARS missing Rnd 3 and Rnd 10** — stated (12) after a 9-st round; R11 left 3 sts unworked.
4. **Blanket gauge probe impossible “after Rnd 3”** — Rnd 2 has no side spaces; moved to Rnd 4 + written Rnd 3 setup round added.
5. **“33 cm ear tips to corner” not reproducible** → ~25 cm assembled (37 cm bare diagonal).
6. **“Cotton will felt” is wrong** (wool property) → shrinkage/clumping wording.
7. “Turning chain” vs no-turn contradiction standardised (ch-3 counts as dc, never turn).
8. Yarn qty now also in metres (140–150 m; two 50 g balls).
9. Ear attachment rounds clarified (head Rnds 4–6; ears sewn flat).
10. Blanket math kept: +12 dc/round, checkpoints 36/60/120/180/240, border 252 sc, sizes 23/26/28 cm — all verified against 4.3 mm/dc.

## Non-blocking findings on NS 01–09 (all corrected in v2 files)

- **Interleaved tables (layout corruption in the source):** Coco's Ear+Muzzle table, Kawaii's Arm/Base, Stem/Leaf and Outer/Inner-ear tables, Hamish's Inner/Outer-ear table — each arrived as two tables printed into one. All decoded, separated and re-verified (decoded counts consume/produce exactly).
- **Kawaii:** Boo's head is 26 sts ≈ **29 mm** (source said 27 mm); witch-hat brim is 20 sts ≈ **22 mm**, snug-by-design (source said 26 mm). Troubleshooting line updated to match.
- **Hamish:** fringe says “44 strands” but 24+10+9 = **43 knots** → “43 knots + 1 spare”.
- **Momo:** “stopping at 36 gives a body about 34 mm across” → a 36-st oval is **~60 x 40 mm** at the stated gauge.
- **Duck:** removed the internal “(tentative — confirm with studio)” note from the design code line.

## Checks that PASS unchanged (verified, kept)

Highlights per pattern (full lists in each PDF's validation-summary page):

- **Axel:** 36-round one-piece chain 6→36→18→36→12→9→6; 51.6 mm sphere head; 43 mm tail = exactly 5 scallops × 2 ridge sts; sturdier-neck option R13=20 → R14=24 consumes fully.
- **Coco:** leg-join arithmetic R4 = 3+9+3+9 = 24, R5 = 7-3-10-3-7 = 30; standing height 20×4.3 + 17 = 103 mm.
- **Ember:** matched open 18-st head/neck; wing scallops consume 2+1+2+1+4 = 10; 10-spike strip; 103 mm seated; 124 mm wingspan.
- **Hamish:** 48-st head ≈ 69.5 mm; muzzle face 34.8/rim 26.1 mm; 67 mm legs; three-size table counts identical.
- **Kawaii:** hem 4-in/8-out ×6 = 24→48; Bramble wing Row 3 consumes 2+3+2+2+3 scallops = 12.
- **Duck:** 23 rnds × 7 mm = 161 mm; beak around 5-ch = 11 then 15; smaller-head option 24→18→12→6.
- **Momo:** oval ladder 18→48 consumes fully; ear rows 5→3→2 exact; BLO ridge placement.
- **Trio:** petal round 18→36 exactly (9 × [1+3]); scaling ×1.3 = 3.9/4.9/3.5 cm.
- **Shelby:** cluster round 24→35 with bumps on sts 4/9/13/18/22; join 24-to-24 via 19 plain + 5 cluster anchors; whole charm = 203 sts; big version 42→53.

## Deliverables

```
deliverables/
  Hamish_the_Highland_Cow_Crochet_Pattern_NS01.pdf        (+ _print)
  Kawaii_Halloween_Mini_Set_Crochet_Pattern_NS02.pdf      (+ _print)
  Axel_the_Axolotl_Crochet_Pattern_NS03.pdf               (+ _print)
  Coco_the_Capybara_Crochet_Pattern_NS04.pdf              (+ _print)
  Little_Duck_Plushie_Crochet_Pattern_NS05.pdf            (+ _print)
  Momo_the_Loaf_Cat_Crochet_Pattern_NS06.pdf              (+ _print)
  Pocket_Positivity_Trio_Crochet_Pattern_NS07.pdf         (+ _print)
  Ember_the_Baby_Dragon_Crochet_Pattern_NS08.pdf          (+ _print)
  Shelby_the_Sea_Turtle_Bag_Charm_Crochet_Pattern_NS09.pdf(+ _print)
  Willow_the_Bunny_Lovey_Crochet_Pattern_NS10.pdf         (+ _print)
```

Every PDF: illustrated cover + badges, safety box, materials/gauge/abbreviations, techniques,
round tables with count-check callouts, assembly & listing copy, colorways, troubleshooting,
terms of use, and a validation-summary page. QA: zero out-of-bounds glyphs, no orphan pages,
print editions greyscale/low-ink.

## Repo repairs made to run the above

- `src/crochet_checker/validation/__init__.py` imported a nonexistent `validator` module, breaking
  every validation import (incl. the CLI). Restored the working pipeline imports (kept in
  `__init__.py.backup`) while retaining `multipiece`.
- `src/crochet_checker/pdf/generator.py` remains a placeholder (writes .txt); out of scope — this
  run used `tools/pattern_pdf_lib.py` (fpdf2), since WeasyPrint is unavailable here (no Pango, no root).

Re-run anytime:
```bash
.venv/bin/python tools/validate_pattern.py                 # all NS01-09 files → PASS
.venv/bin/python tools/validate_willow.py patterns/willow_bunny_lovey_v2_fixed.txt
.venv/bin/python tools/generate_novality_pdfs.py           # all 18 PDFs
.venv/bin/python tools/generate_willow_pdf.py              # Willow's 2 PDFs
```
