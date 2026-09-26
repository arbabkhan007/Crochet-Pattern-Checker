# NS 14 Bobble Snowflake Tree Skirt — verification report

**Verdict on the pattern as submitted: FAIL — 3 errors, 3 warnings.**
**Verdict on `corrected.md`: PASS — 0 errors, 0 warnings.**

Reproduce:

```bash
python3 verify.py original.md    # exit 1
python3 verify.py corrected.md   # exit 0
python3 build_pattern.py         # regenerates corrected.md from the count rule
python3 render_columns.py        # regenerates spoke-comparison.svg
```

---

## How it was checked

The repository's bundled validator was tried first and rejected as unfit for this
job: it reports `1 stitch` for every round and returns `PASS` for any input,
including a deliberately broken one. So the pattern was checked with a purpose-built
**stitch-level simulator** (`verify.py`).

It does not compare printed numbers. It walks a virtual hook around a virtual
fabric, creating an object for every one of the **6,336 stitches** in the large size
and recording, for each one, the parent stitch it was worked into. Twelve
independent checks then run against that fabric:

| # | Check | What it proves |
|---|---|---|
| 1 | Tokenising | every instruction fragment parses; nothing is silently skipped |
| 2 | US ↔ UK | both columns reduce to a byte-identical operation stream |
| 3 | Exhaustion | each round consumes exactly the previous round's stitches |
| 4 | Counts | stitches made = printed `(n)` = 12 × N |
| 5 | Cadence | bobble rounds fall every 3rd round from R5 |
| 6 | **Columns** | repeat *k* consumes only stitches made by repeat *k* last round |
| 7 | Anchor | the wording's round-start vs. the one the construction notes require |
| 8 | Border | shell repeats exhaust the edge exactly; scallops = 2 × N |
| 9 | Bobble | the 5-dc bobble is simulated loop by loop |
| 10 | Geometry | flat-circle test from the stated gauge; diameters both ways |
| 11 | Yarn | yardage and weight derived from the gauge, not guessed |
| 12 | Prose | every number quoted in the prose and summary tables re-derived |

Check 6 is the one that matters most here, and it is the reason a count-checker
was not enough.

---

## What passed, unchanged

The core of this design is sound, and most of it verified exactly:

- **All 32 growth rounds.** Every round consumes exactly the previous total and
  produces exactly 12 × N. Every printed `(n)` is correct — all 32 of them. There
  is not a single stitch-count error in the pattern.
- **The count rule** ("round N consumes N-1 and produces N per repeat") holds for
  every round, and the prose's worked examples (R9 = 7 plain dc, R10 = 8) match it.
- **Bobble cadence** R5, 8, 11, 14, 17, 20, 23, 26, 29, 32 — exactly "every third
  round from R5", with 12 bobbles on each.
- **The 5-dc bobble.** Simulated loop by loop: 2 → 3 → 4 → 5 → **6** loops on the
  hook, closed with one yarn-over through all 6. The written instruction is right.
- **US/UK columns.** All 32 rounds plus the border are exact equivalents — zero
  mismatches. (This is unusually well done; dual-terminology patterns often slip.)
- **The scallop border.** Consumes 168 / 276 / 384 stitches exactly, giving 28 / 46
  / 64 scallops as printed.
- **Flat-circle geometry.** +12 sts/round = +10 cm circumference needs +1.59 cm of
  radius; the stated row gauge gives +1.67 cm. A 4.7% difference — well inside
  blocking tolerance. The two gauge figures are genuinely consistent.
- **Mini and Standard diameters**, and every figure in the "Sizes at a glance" table.

---

## Errors found and corrected

### E1 + E2 — the snowflake spirals (structural, and invisible to stitch counts)

**This is the significant one.**

The construction notes say:

> "Work the first dc or BO into the SAME stitch as the join"

But every one of the 31 round instructions says `[dc in next st, …]`. Read
literally — which is how a crocheter reads the table, not the preamble — "next st"
is the stitch *after* the one the joining slip stitch sits in. So the round starts
one stitch late.

The counts survive this perfectly. Each repeat still consumes N-1 stitches, twelve
repeats still consume 12(N-1) = the whole previous round, and you still end on
12 × N. A stitch-count checker sees nothing wrong, which is exactly why this kind
of error ships.

What the fabric simulation shows is that the **repeat boundaries slide one stitch
sideways every round**:

```
rounds whose repeats straddle two parent repeats : 30 of 31
cumulative column rotation R1 -> R32             : 120.8 degrees
bearing of increase column 1 at R2/8/16/24/32    : 45, 104, 128, 141, 150 deg
```

The twelve increase columns and the bobbles sitting on them wind about **121°**
around the skirt between the centre and the edge — a third of a full turn. The
"twelve-spoke snowflake" comes out as a pinwheel, and the optional surface
slip-stitch spokes, which the pattern tells you to run "up each of the 12 increase
columns", have no straight column to follow.

**Fix.** Every round now states its anchor explicitly, and the first repeat is
written out so the bracket runs × 11:

> R9 — `Ch 2, dc in same st as join, dc in next 6 sts, 2 dc in next st, [dc in next 7 sts, 2 dc in next st] x 11, sl st to first dc` (108)

Same 108 stitches, same 7-plain-dc repeat, unambiguous start. After the fix:

```
rounds whose repeats straddle two parent repeats : 0 of 31
cumulative column rotation R1 -> R32             : 0.0 degrees
bearing of increase column 1 at R8/16/24/32      : 26.2, 28.1, 28.7, 29.1 deg  (-> 30)
```

See `spoke-comparison.svg` for the two geometries drawn side by side from the
simulation.

A bonus fell out of the fix: because every repeat now begins at the join, the
repeat-1 bobble lands *on* the joining column and the twelfth increase sits
immediately before it, so **the seam hides inside a spoke**. That is now written up
as Construction note 5.

### E3 — yarn quantity overstated by roughly 2–3×

Stated: *"700-1,200 g for standard or large"*.

Derived from the pattern's own gauge (12 dc = 10 cm, 6 rows = 10 cm; ~10 cm of
yarn per dc; worsted 180 m/100 g, aran 150 m/100 g), including bobble extras and
the border:

| Size | Body sts | Yarn | Worsted | Aran |
|---|---|---|---|---|
| Mini (R14) | 1,260 | 161 m / 176 yd | 89 g | 107 g |
| Standard (R23) | 3,312 | 390 m / 427 yd | 217 g | 260 g |
| Large (R32) | 6,336 | 717 m / 784 yd | 398 g | 478 g |

A maker following the stated figure buys two to three times too much yarn for a
standard skirt. **Fix:** a per-size materials table (100-150 g / 250-350 g /
450-600 g, ~20% margin included) with an MC/CC split, since CC bobble rounds
account for a large share of the total.

---

## Warnings corrected

### W1 — centre hole size

The ch-20 ring measures up to 15.8 cm of chain, but R1's 12 dc span only 10.0 cm,
so the ring gathers. The relaxed opening is about **3.2 cm / 1.25 in**, not the
claimed "1.5-2 in unstretched" — it only reaches 2 in when stretched over a stand.
**Fix:** quoted as 1.25-1.75 in (3-4.5 cm) at rest, opening to about 2 in, with the
ch-24 alternative measured the same way, plus a note under the centre-ring table
explaining the gathering.

### W2 — large diameter understated

Simulated R32 finished diameter, including the border, is 41.5 in (stitch gauge) to
44.7 in (row gauge). The printed "38-43 in (97-109 cm)" sits below that, so a maker
sizing to a stand could be 2 in out. **Fix:** Large is now 41-45 in (104-114 cm).
Mini tightened to 19-21 in, Standard to 30-33 in — both were already close.

### W3 — gauge units

The gauge is taken on a "flat swatch" but quoted as "6 rounds = 4 in". A flat
swatch has rows. **Fix:** "6 rows = 4 in", plus a short paragraph explaining how the
two gauge numbers interact (+1.59 cm of radius needed vs +1.67 cm supplied) so a
maker knows which one to match first.

---

## Improvements added (not errors)

- **Any round is a valid stopping point.** The pattern says "all three endings are
  divisible by 6". True, but understated: every round total is 12 × N, and 12 × N is
  *always* divisible by 6. The border closes cleanly after **any** round, with
  scallops = 2 × N. That makes the skirt fully size-flexible; it is now stated.
- **Border join tidied** to `sc in same st` so the joining stitch is worked rather
  than falling inside a "skip 2".
- **Bobbles at the edge.** All three sizes stop on a bobble round, so a few edge
  bobbles land inside the border's "skip 2". Cosmetic only, but a troubleshooting
  entry now offers the extra plain round (R15/R24/R33) that avoids it — the maths
  holds, since 12 × N and 2 × N apply to any round.
- **Troubleshooting entry for spiralling spokes**, pointing at the round-start
  anchor.
- **Hook sizes split** — 5-5.5 mm for the skirt, 4-4.5 mm for the surface spokes
  (the pattern said "a smaller hook" without a number).
- The construction note about the join now says "from R2 onward", since R1 is worked
  into the ring and has no join.

Everything else — the design, the safety section, care and storage, and the full
Terms of Use and copyright text — is carried over verbatim.

---

## Files

| File | What it is |
|---|---|
| `corrected.md` | the publication-ready pattern (**this is the deliverable**) |
| `original.md` | the pattern exactly as submitted, kept for diffing |
| `verify.py` | the stitch-level simulator, no dependencies |
| `build_pattern.py` | generates `corrected.md`'s tables from the count rule |
| `render_columns.py` | draws the spoke geometry for both readings |
| `spoke-comparison.svg` | spiral vs. radial, side by side |
| `run-original.log` | full simulator output for the submitted pattern |
| `run-corrected.log` | full simulator output for the corrected pattern |
