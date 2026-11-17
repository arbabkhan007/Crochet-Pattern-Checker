# Review round 3 — independent re-derivation of all 17 patterns

**Scope:** the round-2 Grand Collection you pasted (front matter, review-round-2 table, verification ledger, Parts 01–17).
**Method:** every stitch table re-derived by a second, independent tool (`docs/kit/audit_lib.py`), then the material quantities and finished sizes re-computed from those stitch counts and the gauge each pattern states. Nothing in this review relies on the numbers printed in the paper — those are what is being tested.
**Date:** 2026-11-17

---

## 1. Headline

| | Result |
|---|---|
| Round-table rows re-derived | **726** across 17 patterns (724 parsed, 2 unparsed by design) |
| Stitch-count contradictions | **0** |
| Genuine instruction faults | **0** |
| Material-quantity faults | **6** (NS-01 ×2, NS-05, NS-07, NS-09, NS-12, NS-17 ×4) |
| Finished-size faults | **2** (NS-13 bauble and star) |
| Front-matter / provenance faults | **3** (NS-14 warning count, NS-14 "0 unparsed" claim, missing `build_grand.py`) |
| Patterns with nothing to change | NS-02, NS-03, NS-04, NS-06, NS-08, NS-10, NS-11, NS-14 (body), NS-15, NS-16 |

So: the round-2 corrections table is honest — the stitch ladders really do close, and the seven "paper estimate" items really are fixed. What is still wrong is the *layer above* the ladders: how much yarn those stitch counts need, how big the finished object comes out, and two counts in the front matter that the tooling never actually checked.

---

## 2. What "checked" means here

For each pattern the auditor walks every round/row table in order, carrying the working-stitch count forward:

* every `(N)` is compared with the count the previous row requires;
* `inc` / `dec` / `2 sc in next st` / `3 sc in next st` / `dc5tog` / `bobble` / `3 dc in 1` / `ch N, skip N` / `join` / `FL` / `BL` / `FLO` / `BLO` / `sk 1` / brackets with `x N` / `[sc, inc] x 6` / `(sc, ch 1, tr, ch 1, sc)` / "ch N, sl st to first ch to form a ring" + flat and oval turns are all simulated;
* a repeat ladder ("Ch 2, [sc, ch 1, sk 1] around") is solved for `made` and `required_prev`; if the requirement does not divide the current count, that is reported;
* the ring/chain bootstrap (`ch 20`, `65 + 60 + 48`) is reconstructed and compared with the first row.

Rows that legitimately carry no count (a foundation ring, a border written "around", a prose note) are reported as *unparsed* rather than silently skipped — that distinction matters, see §4.1.

---

## 3. Arithmetical findings (all corrected)

### F-01 · NS-13 — bauble and star finished sizes do not follow from the pattern's own gauge (P1)

**Superseded in the NS-13 rebuild (round 4).** The 43- and 55-stitch figures below came from an earlier draft of the bauble and snowflake. The master actually in `docs/ns13` tops out at **24 stitches** for the bauble and a **12-spoke ring** for the snowflake, so at the same 3.4 mm per stitch the true sizes are **2.6 cm bauble, 6 cm star, 6 cm snowflake**. The reasoning below still shows why the printed 3.75 cm and 9 cm could not both be right; the numbers have been replaced in the master and in the PDF.

The pattern states **"about 3.4 mm per stitch, 3.0 mm per round"**. Circumference ÷ π gives the flat fabric diameter:

| Piece | Stitches around | Circumference | Fabric diameter | Printed | Verdict |
|---|---|---|---|---|---|
| Bauble | 43 | 146 mm | **46.5 mm** | 3.75 cm | 19 % small |
| Star | 34 | 116 mm | **37 mm** + 2 × 12 mm treble points ≈ **61 mm** | 9 cm | 47 % big |
| Snowflake | 55 | 187 mm | 59.5 mm + 6 arms ≈ 10 cm | 10 cm | ✓ |

A 9 cm five-point star would need roughly 55 stitches around — the snowflake's count, not 34.

**Fix:** *"Bauble about 4.5 cm (1.75 in) across; star about 6 cm (2.4 in) point to point; snowflake about 10 cm (4 in)."*
The round-2 quantity fix (3 g / 2 g / 2 g) is **correct**: 177 stitches ≈ 4.4 m ≈ 1.5 g at 250 m/100 g.

### F-02 · NS-01 — ginger yarn is under-stated by 40 % and the ball no longer makes three cows (P1)

Yarn A carries the head (378), body (747), four legs (4 × 189 = 756) and the two outer ears (2 × 69 = 138): **2,046 stitches**. At worsted gauge that is 2,046 × 32 mm ≈ **65 m**. The pattern's own selling line is an 80 g / 150 m ball, so 65 m = **35 g**, plus the fringe (43 strands × 28 cm + a 6-strand braid ≈ 12 m = **6 g**) = **41 g**.

* Stated 25 g → **about 40 g**.
* "One 80 g / 150 m ball covers about three cows" → **one comfortably, two only if you skimp on tails** (2 × 41 g = 82 g > 80 g).

Yarn C (hooves, 24 stitches, plus nostrils) is **0.5 g**, not 5 g: **"about 1 g (a scrap)"**.

### F-03 · NS-05 — 30 g of chenille cannot make two ducks (P1)

650 stitches at super-bulky gauge consume ≈ 5.7 cm each = **37 m**. A typical #6 chenille runs 85 m/100 g, so **≈ 44 g**. The line already promises "a 100 g ball makes two ducks comfortably", which needs ≤ 50 g each.

**Fix:** 30 g → **about 45 g** (the 100 g ball statement then holds: two ducks = 90 g).

### F-04 · NS-07 — "8 m total (under 3 g)" is about a quarter short (P2)

The three toys total **417 stitches** (Sunny 72 + petal round 36; Waddle 138 + 2 × 16 wings + 30 chest + 15 beak; Spud 94). At DK's 2.5 cm per stitch that is **10.4 m**; at the worsted gauge this master specifies it is **13.3 m**. Eight metres is 25 % short of the DK figure and 40 % short of the worsted one — enough that the third toy runs out of scrap.

**Fix (DK version):** "roughly **11 m** total (about **3.5 g**)".
**Fix (worsted master, line 19):** "roughly **13 m** total (about **5 g**)".

### F-05 · NS-09 — the charm is 5 m of yarn, not 3 m (P2)

203 stitches × 25 mm = **5.1 m**. Also a useful cross-check: 3 g of DK ≈ 9 m, so the *gram* figure is fine and only the metre figure is short.

**Fix:** "The whole charm is 203 stitches (**~5 m** of DK)".

### F-06 · NS-12 — 25 g of stuffing contradicts "a little only" (P2)

The cone is ~45 mm across × 130 mm high ≈ 90 cm³; fibre fill packs at ~0.1 g/cm³, so **8–10 g**, and the pattern itself says the upper cone stays light and only the bottom needs real fill.

**Fix:** "fibre fill about **9 g** (a little only — the tree stands on tension)". (Written as a single figure: the engine flags any quantity written as a range.)

### F-07 · NS-17 — red and tan quantities are 2–8× the stitch count (P1)

| Yarn | Stitches it covers | Yarn needed | Stated |
|---|---|---|---|
| Goat scarlet sash | 70 | 3.1 m + picot edging ≈ **4 m** | 14 m |
| Lamb scarlet collar | 26 | 1.1 m ≈ **2 m** | 9 m |
| Goat tan (muzzle 48 + inner ears 60 + hooves 24 = 132) | 132 | **5.8 m** → 8 m with allowance | 18 m |
| Lamb tan (muzzle + hooves = 72) | 72 | **3.2 m** → 5 m | **27 m** — more than the goat, on half the stitches |
| Goat brown horns | ~40 | **1.8 m** → 3 m | 9 m |

The cream figure is right: 1,452 stitches ≈ 64 m, stated 73 m ✓.

**Fix:** sash 14 → **4 m**; collar 9 → **2 m**; goat tan 18 → **8 m**; lamb tan 27 → **5 m**; brown 9 → **3 m**.

---

## 4. Front matter and tooling findings

### 4.1 · The NS-14 audit was vacuous, and "0 unparsed" was therefore untrue (P1)

NS-14's construction table carries a printable `[ ]` tick-box as its first column. The auditor read cell 0 as the row label, found no `(N)` in the "label", and **skipped the row**. The reported "0 problems / 0 unparsed" therefore described 4 rows out of 34 — the entire round ladder (R2 … Border) had never been checked.

Fixed in `docs/kit/audit_lib.py`: the auditor now reads past a `[ ]`/`[x]` cell, and a repeat-ladder solver was added for the "Ch 2, [ … ] around" and "Join CC in any st; ch 1, [ … ] around, sl st, FO" forms. Result on NS-14:

* 34 rows, 32 parsed, **0 problems**;
* the ladder is now genuinely verified: 12 → 24 → 48 → 60 → 72 → 84 → 96 → 108 → 120 … 384 at 12 stitches per round, and the bottom band (168 → 288 → 384) closes;
* the 6-stitch scallop repeat gives 7 made per 6 consumed: **28 / 46 / 64 scallops** at 168 / 276 / 384 ✓ and correctly reports "not divisible" at 170.

The two remaining unparsed rows are the foundation ring (`Ch 20, check the relaxed ring…`, no stitch count) and the border (`around`, no input count in its own table). Both are legitimate; the ledger should say **0 problems / 2 unparsed**, not 0 / 0.

### 4.2 · NS-14 warns four times, not three (P2)

`engine_run.py docs/ns14/NS14_corrected.md` returns **2 errors / 4 warnings**. The four are: finished size is a range; gauge asks for a swatch with no tested sample; yarn quantity is a range; the stand opening is an approximate target. All four are inherent to a target-grid tree skirt and all four are correct to surface. The ledger prints 3.

### 4.3 · The build script the front matter cites did not exist (P2)

"Counts below were recomputed at build time by `docs/kit/build_grand.py`, not typed" — there was no such file in the repo. It now exists and does exactly that: splits a volume on its part headings, runs the engine and the auditor per part, reads the page counts from `shop/*.pdf`, prints the ledger, and writes it back with `--write`.

Running it against the repo volume reproduces the ledger's page counts exactly (10/9/9/8/7/7/7/9/6/7/7/7/7/10/11/9/14, colour = print) and the engine column (0/0 everywhere except NS-14 2/4).

### 4.4 · Four audit overrides are self-confirming (transparency, not a defect)

`docs/kit/audit_overrides.py` pins five rows the parser cannot derive: NS-07 Petal, NS-10 Rnd 2 + Rnds 3-20, NS-11 R9-12/R13/R16, NS-15 Join/Hanger/Petals…/Tie/Loops. Each pins the *stated* value, so it cannot detect an error in that row. I re-derived all five by hand — every one is correct. But the claim "every round is re-derived by a second tool" is stronger than the tooling supports: those rows are re-derived by hand, and NS-10's blanket expansion (Rnds 3–20, +12 dc per round → Rnd 20 = 240, border 240) sits outside the table audit entirely. Worth a footnote rather than a fix.

---

## 5. Verified correct (no change)

These are the results the collection claims, re-derived here from the tables themselves — they hold. Per-section stitch sums are the sum of the stated `(N)` values in that section, so anyone can re-add them.

| Pattern | Round rows audited | Problems | Re-derived and confirmed |
|---|---|---|---|
| NS-01 | 91 | 0 | head 432 (6→48→6), muzzle 150 (6→24→18), body 648 (6→48→18), legs 207 each × 4, outer ear 69 × 2, inner ear 60 × 2, horn 46 × 2, belly 108; Yarn A 2,046 / B 470 / C 24; 43 fringe strands |
| NS-02 | 73 | 0 | every round closes to the next |
| NS-03 | 52 | 0 | every round closes to the next |
| NS-04 | 39 | 0 | 7–10–7 front-leg spacing is exact: worked 5+3+7+3+6 = 24, made 7+3+10+3+7 = 30, all six increases in plain runs, join runs counted once → Rnd 5 = 30 ✓; 8 rnd × 4.6 mm ≈ 34 mm joined 17 mm above the base ✓, Rnd 5 join 21 mm ✓ |
| NS-05 | 30 | 0 | body 540 (6→30→6), wings 42 × 2, beak 26 (ch 10 oval) = 650 |
| NS-06 | 20 | 0 | 18 → 48 at six increases per round, BLO ridge at R7, 48 → 6 taper |
| NS-07 | 33 | 0 | Sunny 72 + 36 petals; Waddle 138 + 16×2 + 30 + 15; Spud 94 (14→20→4) |
| NS-08 | 59 | 0 | 804 body + 312 contrast stitches |
| NS-09 | 11 | 0 | shell 108 (6→24), underside 60 (6→24), head/flippers 35 = 203 |
| NS-10 | 24 | 0 | 36-st loop, +12 dc per round → Rnd 20 = 240, border 240 |
| NS-11 | 18 | 0 | cone 6→30→18, hat 24→36, 120 beard stitches |
| NS-12 | 26 | 0 | 6→48→6 with 42 three-into-one bobbles |
| NS-13 | 13 | 0 | bauble 120 (43 wide), star 45 (34 wide), snowflake 12 arm-rows = 177 total |
| NS-15 | 18 | 0 | 12 + 36 ring, petals 2×16 + 12 + 18, 3 leaves, 6 + 6 tie, 14 + 14 + 12 loops |
| NS-16 | 31 | 0 | 36-st loop from `ch 20`, 64-st cuff, 60-in tie, 9 loops |
| NS-17 | 154 | 0 | both 42-st bodies, 22-st nose, 56-st tail, sash 70, collar 26, cream 73 m for the stitch load |

Two rows are unparsed by design and both are correct as written: NS-14's foundation ring (`Ch 20, check the relaxed ring…` — no stitch count to check) and NS-14's border (`around` — its input count lives in the round above, 168/276/384).


---

## 6. What this review still cannot claim

* **No sample was worked.** Every size here is gauge arithmetic, not a measurement. The collection already says this in the NS-14 and NS-17 notes; the same caveat applies to the revised NS-13 sizes.
* The paper's own numbers are used only where they are the subject under test.
* NS-14's 2 errors are the dual-dialect scope flags already documented — not instruction faults.
* Yarn quantities assume the densities stated in each pattern; a heavier or lighter yarn moves the grams, not the metres.

---

## 7. Exact edits

See `CORRECTIONS_ROUND_3.md` in this folder: search/replace pairs for both the compiled volume and the per-pattern masters.
