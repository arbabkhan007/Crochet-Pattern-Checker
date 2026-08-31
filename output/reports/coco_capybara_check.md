# Pattern Check — NS 04 “Coco the Capybara”

**Reviewed:** 2026-08-30 · US terms · Intermediate · 2.5–3 h

**Overall verdict:** The core stitch-count math is **sound** — every body, leg, ear and muzzle round in the tables is consistent. I found **one high-visibility instructional problem**, **two dimensional/wording discrepancies**, and a few notes about the checker tool itself.

---

## 1. Deterministic / machine check

The repository’s `crochet-pattern-checker` was installed and run against the pattern. The original PDF-style tables are not directly machine-parseable, so I normalized each component into `Round N: … (count)` syntax for validation:

| Component | Rounds | Status | Score |
|---|---|---|---|
| Body & head | 20 | PASS | 100 |
| Leg (8/9 rounds) | 9 | PASS | 100 |
| Ear | 3 | PASS | 100 |
| Muzzle | 5 | PASS | 100 |

All stated stitch counts match the preceding-round counts when the instructions are followed exactly:

- Body: 6 → 12 → 18 → 24 → 30 → 36 → 36 → 36 → 36 → 32 → 36 → 36 → 36 → 36 → 36 → 30 → 24 → 18 → 12 → 6 ✓
- Legs: 6 → 9 → 9 × 7 ✓
- Ears: 6 → 9 → 9 ✓
- Muzzle: 6 → 9 → 12 → 12 → 12 ✓

The join counts also check out: each leg join takes 3 single-crochet stitches from both the leg and the body, and those stitches still count as 3 stitches of the body round, so Rnd 4 and Rnd 5 totals are unchanged.

---

## 2. Issues found

### High — Rnd 5 instruction box omits the increases

The Rnd 5 table is correct:

```
[3 sc, inc] × 6   (30)
```

But the “Joining the legs” box reads, in effect:

> Work 7 sc. Join a leg over the next 3 sc. Work 10 sc. Join a leg over the next 3 sc. Work 7 sc. Total 30 stitches.

If a maker follows **only** that worded sequence, they work 30 stitches **after** Rnd 4, but Rnd 4 produced only 24. As written, the literal sequence is physically impossible (`30` consumed from `24` produced).

This is the only place I’d call a real pattern flaw. **Suggested fix:** rewrite the Rnd 5 box around the actual repeat, e.g.:

> Work the Rnd 5 increase round as `[3 sc, inc] × 6`. When you reach the two marked leg positions, work 3 of the repeating `sc` stitches through both the front-leg top and the body. Keep the 6 increases; Rnd 5 still totals 30.

The same ambiguity does **not** affect Rnd 4, because that box correctly spells out the `[1 sc, inc] × 3` sections.

---

### Medium — “9 mm lower” in the troubleshooting section is not supported by the stated gauge

Under *Coco rocks back onto her haunches*, the pattern says:

> The front legs join at Rnd 5, 21 mm up, and the back legs at Rnd 4, 17 mm up, so equal-length legs leave the back feet about 9 mm lower.

With the stated gauge of **4.3 mm per round**, Rnd 5 vs Rnd 4 is **one round = ~4.3 mm** (17.2 → 21.5 mm), not about 9 mm. The practical takeaway is still correct — front legs should be 9 rounds and back legs 8 rounds — but the “9 mm” figure doesn’t follow from the pattern’s own numbers.

---

### Medium — Ear width doesn’t match gauge + stitch count

The ear is 9 stitches around (after R3). With the pattern’s gauge of **4.5 mm per stitch**, a 9-stitch circle is:

```
9 × 4.5 mm = 40.5 mm circumference
diameter ≈ 40.5 / π ≈ 12.9 mm
```

The pattern says each ear is **about 20 mm across**. The height (3 rounds × 4.3 mm ≈ 13 mm) matches, but the 20 mm width is about 55% larger than a 9-stitch opening at the stated gauge. Verify this against the physical ear; either reduce the stated width to ~13 mm, or the ear needs more stitches / a different shape.

The muzzle is fine by contrast: 12 stitches at 4.5 mm/stitch gives ~17.2 mm diameter, which matches the stated ~17 mm.

---

### Minor — Hook size label isn’t exact

“3.0 mm (US C-2 or D-3)” is approximate. Standard US sizing is:

- C-2 = 2.75 mm
- D-3 = 3.25 mm

3.0 mm sits between them. It’s a common informal label, but for precision the pattern should say **3.0 mm (between US C-2 and D-3)**, or simply list 3.0 mm only.

---

## 3. Checker-tool caveats (not pattern errors)

- The tool does not parse this pattern’s table format (`| R1 | … |`), so a raw paste fails; components must be normalized.
- The parser does not recognize `invdec` — it falls back to one generic `dec`, so Rnd 20 looks like it consumes 2 stitches instead of 12. Normalizing `invdec` to `dec` gave the correct 6-stitch finish.
- `measure`/`explain` use the built-in default **6.0 mm × 6.0 mm** worsted stitch dimensions, not the pattern’s declared gauge (**4.5 mm/stitch, 4.3 mm/round**). As a result the tool reports the body as ~**69 mm wide × 120 mm tall**, versus the pattern’s stated ~**52 mm wide × 86 mm body height**. Pass `StitchDimensions(width_mm=4.5, height_mm=4.3)` or use a gauge-aware measurement to get the pattern’s true numbers.
- Shape analysis classifies the body as a **sphere (90%)**, which is reasonable for the overall rounded-snowman silhouette, though the shallow waist (Rnd 10) is not enough to change that detection.

---

## 4. Things that check out

- ✅ Rnd 4 back-leg join math: `3 + [1 sc, inc]×3 + 3 + [1 sc, inc]×3 = 24`, with the two 3-stitch leg sections included.
- ✅ Front-leg join height is one round higher, and the front legs are one round longer — the intended level-foot logic is consistent.
- ✅ Eye spacing: 6 stitches × 4.5 mm ≈ 27 mm apart; muzzle ~17 mm wide leaves ~5 mm of clear face, matching the pattern’s own claim.
- ✅ Rnd 10 shallow waist: `(7 sc, invdec)×4` correctly turns 36 into 32; Rnd 11 `(7 sc, inc)×4` correctly returns 32 to 36.
- ✅ Rnd 20 close: `invdec × 6` correctly takes 12 to 6.
- ✅ No safety eyes/plastic parts; safety disclaimer is present and honest.

---

## Recommended priority

1. **Fix the Rnd 5 joining instruction box.** This is the one change that realistically could cause an unusable leg without a smaller fix.
2. Recheck the ear dimensions against the physical ear; update the dog-eared “20 mm” or the ear stitch count.
3. Optionally tighten the “9 mm” wording to “about one round (≈4 mm)” and note that the hook size is approximate.
