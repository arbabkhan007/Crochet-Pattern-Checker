# Corrections for the round-2 volume — apply in this order

Everything here is a **find / replace** pair. Find strings are quoted without surrounding whitespace, so they match inside the volume's bullet lists and inside the per-pattern masters alike. After editing, rebuild the PDFs and re-run `python3 docs/kit/build_grand.py <volume> --write` so the ledger is recomputed rather than typed.

---

## 1. Materials

| # | Find | Replace |
|---|---|---|
| 1 | `about 25 g used. Caramel, toffee or ginger gold. One 80 g / 150 m ball covers about three cows at the stated gauge, including normal seaming tails.` | `about 40 g used, fringe included. Caramel, toffee or ginger gold. One 80 g / 150 m ball makes one cow comfortably; two only if you skimp on tails. 2,046 worked stitches at the stated gauge is 65 m, plus about 12 m for the fringe.` |
| 2 | `Dark chocolate: worsted / aran (#4), about 5 g. Hooves and nostrils.` | `Dark chocolate: worsted / aran (#4), about 1 g (a scrap). Hooves and nostrils - 24 worked stitches.` |
| 3 | `super-bulky chenille (#6), yellow, about 30 g. A 100 g ball makes two ducks comfortably.` | `super-bulky chenille (#6), yellow, about 45 g. A 100 g ball makes two ducks. 650 worked stitches at this gauge is about 37 m.` |
| 4 | `The three toys use roughly 8 m total (under 3 g), so scraps are fine.` | `The three toys use roughly 11 m total (about 3.5 g), so scraps are fine.` |
| 5 | `The whole charm is 203 stitches (~3 m of DK)` | `The whole charm is 203 stitches (~5 m of DK)` |
| 6 | `fibre fill about 25 g (a little only - the tree stands on tension)` | `fibre fill about 9 g (a little only - the tree stands on tension)` |
| 7 | `scarlet red, about 14 m / 15 yd for the fixed flame sash.` | `scarlet red, about 4 m / 4.5 yd for the fixed flame sash (70 stitches plus the picot edging).` |
| 8 | `scarlet red, about 6 m / 7 yd for the fixed collar.` | `scarlet red, about 2 m / 2.2 yd for the fixed collar (26 stitches).` |
| 9 | `light tan / beige, about 18 m / 20 yd for muzzle, inner ears and hooves.` | `light tan / beige, about 8 m / 9 yd for muzzle, inner ears and hooves (132 stitches).` |
| 10 | `light tan / beige, about 27 m / 30 yd for the muzzle and hooves.` | `light tan / beige, about 5 m / 5.5 yd for the muzzle and hooves (72 stitches).` |
| 11 | `espresso brown or dark grey, about 9 m / 10 yd for two yarn-only horns.` | `espresso brown or dark grey, about 3 m / 3.3 yd for two yarn-only horns.` |

Item 8 differs from the round-1 masters, which say 9 m; use whichever wording your volume carries, but the replacement is the same 2 m.

## 2. Finished sizes (NS-13)

**Find:** `Bauble about 3.75 cm (1.5 in) across; star about 9 cm (3.5 in); snowflake about 10 cm (4 in).`

**Replace:** `Bauble about 4.5 cm (1.75 in) across; star about 6 cm (2.4 in) point to point; snowflake about 10 cm (4 in).`

Why: the pattern's own gauge is 3.4 mm per stitch. 43 stitches around → 146 mm → 46.5 mm flat (not 37.5). 34 stitches → 116 mm → 37 mm flat, and five treble points add about 24 mm across (not 90 mm in total). 55 stitches + six arms = the quoted 10 cm, so the snowflake figure is right.

## 3. Front matter — verification ledger

**a. NS-14 row.** Engine warnings are 4, not 3, and the audit's two count-free rows must be declared:

`| NS-14 | Bobble Snowflake Tree Skirt | 2 / 3 | 0 / 0 | 10 | 10 |`
→
`| NS-14 | Bobble Snowflake Tree Skirt | 2 / 4 | 0 / 2 | 10 | 10 |`

**b. The `†` footnote.** Replace the whole note with:

> † NS-14 is the only pattern with engine findings: 2 errors and 4 warnings. Both errors are dialect-scope flags — the table carries US and UK columns side by side, and the engine reads `sc` inside the UK column as a stray US term; the stitch counts themselves are identical in both columns. The warnings are design targets, not defects: the finished size is a range, the gauge asks for a swatch with no sample result recorded, the yarn quantity is a range, and the stand opening is an approximate target. The audit reports 0 problems and 2 unparsed rows: the foundation ring (`Ch 20, check the relaxed ring…`), which has no stitch count, and the scalloped border, which is written `around` and takes its 168 / 276 / 384 input from the last growth round. All 32 countable rows, R1 through the final growth round, are machine-checked.

**c. The sentence claiming a clean sweep.** Where the front matter says *"0 problems / 0 unparsed on all seventeen"*, change it to *"0 problems on all seventeen; two count-free rows on NS-14 (ring, border)"*. The previous wording was only true because the auditor was skipping NS-14's rows — see §4.

**d. Add a review-round-3 block** (after the round-2 table, same style):

> ### Review round 3 — materials, finished sizes and tooling
>
> Every stitch ladder was re-derived by a second, independent script. All 726 round-table rows close: no instruction faults were found, and the round-2 stitch corrections hold. What needed fixing was the layer above the ladders — the yarn and stuffing those stitch counts actually consume, two finished sizes that did not follow from the stated gauge, and two front-matter counts the tooling never checked.
>
> 1. **NS-01** Yarn A 25 g → 40 g (2,046 stitches = 65 m, plus 12 m of fringe); the 80 g ball makes one cow, not three. Yarn C 5 g → 1 g.
> 2. **NS-05** chenille 30 g → 45 g (650 stitches = 37 m; the "100 g makes two ducks" promise needs 45 g a duck).
> 3. **NS-07** 8 m → 11 m (417 stitches = 10.4 m at DK).
> 4. **NS-09** "~3 m" → "~5 m" (203 stitches = 5.1 m; the 3 g figure was fine).
> 5. **NS-12** stuffing 25 g → 9 g, which is what "a little only" means for a 90 cm³ cone.
> 6. **NS-13** bauble 3.75 → 4.5 cm, star 9 → 6 cm, both recomputed from the pattern's own 3.4 mm per stitch. The 3 g / 2 g / 2 g quantity fix from round 2 is correct.
> 7. **NS-17** sash 14 → 4 m, collar 6 → 2 m, goat tan 18 → 8 m, lamb tan 27 → 5 m, brown 9 → 3 m.
> 8. **NS-14** ledger corrected to 2 / 4 warnings and 0 / 2 unparsed; the audit now reads the tick-box column it used to skip, so the round ladder is genuinely checked.
> 9. `docs/kit/build_grand.py` now exists, so the "recomputed at build time, not typed" claim is true.

## 4. Tooling (already committed)

* `docs/kit/audit_lib.py` — reads past a printable `[ ]` / `[x]` tick-box column instead of skipping the row; new repeat-ladder solver for `Ch 2, K dc in each st around`, `Ch 2, [ … ] x N`, and `Join CC in any st; ch 1, [ … ] around, sl st, FO`.
  *Effect:* NS-14 went from **4 of 34 rows read** to **32 of 34**, 0 problems. The other 16 patterns are unchanged (0 problems, 0 unparsed).
* `docs/kit/build_grand.py` — new. Recomputes the whole ledger (engine E/W, audit problems/unparsed, colour and print page counts read from `shop/*.pdf`) and writes it back with `--write`. Running it against the repo volume reproduces the ledger's page counts exactly and the engine column (0/0 except NS-14 2/4).
* `tests/test_audit_lib.py` — new. Pins the tick-box behaviour, the wrong-count detection, the repeat ladder, the border divisibility case and a full NS-14 audit.

## 5. Masters already patched

`docs/ns01`, `ns05`, `ns07`, `ns09`, `ns12`, `ns13`, `ns17` masters carry the changes above. The compiled volume in the repo is a round-1 build and predates your round-2 text, so it was **not** edited line by line — rebuild it from the masters once the round-2 text is back in the repo, then run `build_grand.py --write`.

## 6. Not changed, deliberately

* **NS-04** — the 7–10–7 front-leg spacing, the 17 mm / 21 mm join heights and the 34 mm back legs all re-derive correctly at the stated 4.6 mm per round; no fault found.
* **NS-10** blanket expansion (Rnds 3–20, +12 dc per round to 240) — correct by hand, but outside the table audit, so it is verified by hand and stated as such.
* **The four pinned override rows** (NS-07 Petal, NS-10 Rnd 2 + Rnds 3-20, NS-11 R9–R16, NS-15 Join/Hanger/Petals/Tie/Loops) — re-derived by hand, all correct; they remain pinned.
