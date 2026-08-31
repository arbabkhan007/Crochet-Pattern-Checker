# Pattern Check — NS 04 “Coco the Capybara” (revised copy)

**Reviewed:** 2026-08-30 · US terms · Intermediate · 2.5–3 h

**Verdict:** The revised version is **mathematically sound** and most of the earlier dimensional/wording issues are fixed. **One real instruction-flow problem remains** in the Rnd 5 joining box, plus one small hook-size precision note and one layout concern in the pasted ear/muzzle table.

---

## 1. Machine / deterministic verification

I normalized the revised components to `Round N: … (count)` syntax and ran the `crochet-pattern-checker` validation on each:

| Component | Rounds | Status | Score |
|---|---|---|---|
| Body & head | 20 | PASS | 100 |
| Leg (8/9 rounds) | 9 | PASS | 100 |
| Ear | 3 | PASS | 100 |
| Muzzle | 5 | PASS | 100 |

All stated stitch counts and round-to-round transitions are correct:

- Body: 6 → 12 → 18 → 24 → 30 → 36 → 36 → 36 → 36 → 32 → 36 → 36 → 36 → 36 → 36 → 30 → 24 → 18 → 12 → 6 ✓
- Legs: 6 → 9 → 9 × 7 ✓
- Ears: 6 → 9 → 9 ✓
- Muzzle: 6 → 9 → 12 → 12 → 12 ✓
- Rnd 4 join: `3 + [1 sc, inc]×3 + 3 + [1 sc, inc]×3 = 24` ✓
- Rnd 10 / Rnd 11 waist: `(7 sc, invdec)×4` → 32, then `(7 sc, inc)×4` → 36 ✓

---

## 2. Remaining issues

### High — Rnd 5 joining box still omits the increases

The Rnd 5 table is correct:

```
[3 sc, inc] × 6       (30)
```

The joining box says:

> Work 7 sc · join a leg over the next 3 sc · work 10 sc · join a leg over the next 3 sc · work 7 sc to the end.
> That is 7 – 3 – 10 – 3 – 7 = 30.

This is an improvement because the box now opens with *“Work Rnd 5 as the plain increase round in the body table…”*, which clues an experienced reader to keep the increases. But if a maker follows only the numbered spacing, they work 30 single crochets from a round that produced 24 — physically impossible. I reproduced this with the checker: the literal 7-3-10-3-7 sequence gives

```
Round 5 consumes 30 but Round 4 produced 24  →  ERROR
```

**Suggested rewrite (while keeping the 7-3-10-3-7 positions):**

> Work Rnd 5 as `[3 sc, inc] × 6`, keeping the 6 increases. Place the 7-3-10-3-7 spacing on the single-crochet sections, not on the increases: work 7 sc, join a leg over the next 3 sc, work 10 sc, join a leg over the next 3 sc, work 7 sc to the end. The 6 increases are already included in those sections; Rnd 5 still totats 30.

---

### Minor — Hook size label is still approximate

“3.0 mm (US C-2 or D-3)” — 3.0 mm is between US **C-2 (2.75 mm)** and **D-3 (3.25 mm)**. The gauge is what matters, so this won’t break the pattern, but the exact wording would be:

> 3.0 mm (between US C-2 and D-3), or just 3.0 mm.

---

### Medium (layout, if it reproduces in the final PDF) — Ear/Muzzle table reads merged

The copy you pasted shows the Ear and Muzzle tables collapsed into one:

| Rnd | Instruction | Sts | Note |
|---|---|---|---|
| R1 | (6) R1 6 sc in MR 6 sc in MR | (6) | |
| R2 | (9) R2 [1 sc, inc] x 3 [1 sc, inc] x 3 | (9) | |
| R3 | (9) R3 sc around [2 sc, inc] x 3 | (12) | |

If this is a copy/paste artifact of two side-by-side columns, ignore it. If the PDF actually renders this way, the ear and muzzle rows are ambiguous (an ear shouldn’t end at 12 stitches). Best practice is to keep them as two clearly separated tables or explicitly label **Ear** and **Muzzle** on every row.

---

## 3. Earlier issues that are now resolved

| Previous issue | Status |
|---|---|
| “Equal-length legs leave the back feet about 9 mm lower” | ✅ Removed in the revised copy; the troubleshooting bullet now just gives the correct front-9 / back-8 rule. |
| Ear “about 20 mm across” contradicted a 9-stitch cup at gauge | ✅ Removed; ears are now just described as a shallow cup. |
| Eye spacing math (27 mm / 5 mm claim) | ✅ Simplified to “6 stitches apart,” which matches the gauge. |
| Height table overfocused on leg lengths | ✅ Cleaned up to body (86 mm) + leg lift (17 mm) = 103 mm. |
| Safety wording | ✅ Expanded and clearer; still appropriately conservative (no toy-safety standard claim). |

---

## 4. Checker-tool caveats (unchanged)

- The raw table format is not parseable without normalizing to `Round N:` lines.
- `invdec` isn’t recognized by the parser; normalizing it to `dec` gives the correct validation (important only if you run the tool directly on the raw text).
- `measure` / `explain` use default 6 mm × 6 mm stitch dimensions, not the pattern’s 4.5 mm × 4.3 mm gauge, so the built-in tool reports larger sizes than the pattern claims. This is a tool limitation, not a pattern error.

---

## Recommended final edits

1. **Rewrite the Rnd 5 joining box** so the 6 increases are explicit (the one edit I would not skip).
2. Verify the ear/muzzle table renders as two clean tables (copy/paste artifact or actual PDF issue).
3. Optional: tighten the hook-size wording.

Otherwise the revised pattern is solid and ready to use.
