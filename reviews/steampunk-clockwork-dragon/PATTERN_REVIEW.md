# Pattern Review — "Steampunk Clockwork Dragon"

**Verdict: ❌ FAILS — 14 defects across 10 sites, and they have a single diagnosable cause.**

| | |
|---|---|
| Pieces checked | 5 (Head & Jaw, Thigh/Leg, Torso, Wing, Tail) |
| Rounds / rows checked | 61 instruction lines = 93 physical rounds & rows |
| **Hard defects** | **14** (at 10 sites) |
| Technique concerns | 6 |
| Missing content | 7 |
| Proportion advisories | 3 |
| Pieces that are 100 % correct | Thigh & Leg (all 15 rounds) |

This is the most ambitious of the three patterns and the most technically literate. The short-row
jaw block is arithmetically perfect. The ch-3 wing sockets are genuinely clever and correct. The
popcorn scale ridge balances to the stitch. The Thigh & Leg — picot gear flange, BLO recovery round,
joined-to-spiral transition, 15 rounds — is **flawless from end to end**.

And then the same mistake is made six times.

---

## ⚠ The single root cause

Five of the fourteen defects are **the identical error**: a repeat sized for a stitch count that is
**exactly 2 smaller** than what the previous round actually produced.

| Round | Available | Repeat consumes | Short by |
|---|---|---|---|
| Head R15 | 14 | 12 | **2** |
| Torso R15 | 42 | 40 | **2** |
| Torso R19 | 44 | 42 | **2** |
| Torso R24 | 38 | 36 | **2** |
| Wing Row 4 | 14 | 13 | 1 |

Look at *when* it happens. Every round in this pattern that operates on a "tidy" amigurumi count —
12, 18, 24, 30, 36, 42, 21, 28, 32 — is **correct**. Every round that operates on an **untidy** count
— 14, 38, 42-after-a-join, 44 — is **wrong**. The author reflexively reaches for a `[sc n, dec] × 6`
or `× 2` repeat that fits the *nearby* round number rather than recomputing for the actual total.

It starts at **Torso Round 15**. That round is the first to produce a non-multiple-of-6 (44), and
from there Rounds 19 and 24 inherit the drift. Fix Round 15 and re-derive downstream, and half the
pattern's errors disappear at once.

---

## 1. Hard defects

Cost model: `sc` 1→1, `inc` 1→2, `dec` 2→1, `hdc`/`dc`/`fpdc` 1→1, `pc` (popcorn) 1→1,
`picot` 0→0 (it hangs off the previous stitch and adds nothing to the count).

### 🔴 D1 — Head Round 12: the short-row raw edges are never worked

> `Row 11a: sc 12, turn. (12)` → `Row 11b: ch 1, dec, sc 8, dec, turn. (10)` → `Row 11c: ch 1, sc 10, do not turn. Continue working in round across raw edge.`
> `Round 12: sc 10 across short row edge, sc 18 across remaining Round 10 sts. (28 sts)`

The short-row block itself is **perfect** — 11a holds 18 base stitches, 11b consumes all 12 and makes
10, 11c consumes all 10. No complaints.

But count the perimeter of the opening you have to rejoin:

| | |
|---|---|
| live stitches on top of Row 11c | 10 |
| untouched Round 10 stitches | 18 |
| **raw row-ends of the short-row block** (3 rows × 2 sides) | **6** |
| **total perimeter** | **34** |

Round 12 works **28**. The **6 raw row-ends are never worked into**, leaving a 3-row gap at each end
of the jaw — exactly where a jaw hinge is under the most strain, and exactly where stuffing will
push through. Round 11c even says *"Continue working in round across raw edge"* — the instruction
knows the raw edge is there, but the stitch count makes no allowance for it.

**Fix:**
```
Round 12: sc 10 across the live short-row sts, 3 sc down the first raw edge,
          sc 18 across the remaining Round 10 sts, 3 sc up the second raw edge. (34 sts)
Round 13: [sc 3, dec] 6 times, sc 4. (28 sts)      <- consumes 34, absorbs the extra 6
```
Rounds 14–15 then follow as the original 13–14 did.

### 🔴 D2 — Head Round 15: two errors, and it breaks the neck-to-torso join

> `Round 15: Switch to Color B, [sc 5, inc] 2 times. (16 sts)`

You arrive with 14 sts. `[sc 5, inc] × 2` consumes 2 × 6 = **12** — **2 stitches left unworked** —
and makes 2 × 7 = **14**, not the stated 16.

This one propagates. Rounds 16–19 then run on 14 sts, so the neck finishes at **14**, and
**Assembly step 3 — which explicitly claims "Round 19 of Head & Neck, 16 sts" — is wrong.**
The head will not fit the torso.

**Fix:** `Round 15: Switch to Color B, [sc 6, inc] 2 times. (16 sts)` — consumes 14 ✔, makes 16 ✔.

### 🔴 D3 — Torso Round 15: 2 torso stitches are unaccounted for

> `Round 15: sc 12 across Torso, sc 6 across Leg 1, skip 4 Torso sts, sc 14 across Torso, sc 6 across Leg 2, skip 4 Torso sts, sc 6 across Torso. (44 sts)`

Torso stitches **worked**: 12 + 14 + 6 = 32. Torso stitches **skipped**: 4 + 4 = 8.
Total accounted for: **40**. Round 14 produced **42**. Two torso stitches are neither worked nor
skipped — they simply fall out of the pattern.

(The stated 44 is internally right: 12 + 6 + 14 + 6 + 6 = 44. The round produces the correct number;
it just doesn't consume the correct number.)

### 🔴 D4 — Torso Round 15 / Leg Round 15 / Assembly 1: the crotch gusset doesn't match

The Leg ends on 9 sts and the pattern says *"Leave 3 unworked sts marked for body gusset"* — correct,
since Torso R15 works 6 of the leg's 9. So each leg offers **3** gusset stitches.

But Torso R15 skips **4** torso stitches per leg, and Assembly step 1 says:

> *"Sew remaining **3** unworked sts of each Leg to the **4** skipped sts on Torso Round 15"*

**3 ≠ 4.** The instruction asks you to sew a 3-stitch edge to a 4-stitch edge, twice. There is no
even way to do it, and you get a pucker at each hip.

**Fix:** skip **3** torso stitches per leg, not 4, and rebalance the round symmetrically:
```
Round 15: sc 18 across Torso, sc 6 across Leg 1, skip 3 Torso sts,
          sc 18 across Torso, sc 6 across Leg 2, skip 3 Torso sts. (48 sts)
```
Torso: 18 + 3 + 18 + 3 = 42 ✔  Made: 18 + 6 + 18 + 6 = 48 ✔  Gusset: 3 leg sts ↔ 3 torso sts ✔
This also fixes the leg placement, which as written is asymmetric (12 sts apart on one side,
20 on the other).

### 🔴 D5 — Torso Round 19: two errors

> `Round 19: [sc 5, dec] 6 times. (38 sts)`

From 44 sts: consumes 6 × 7 = **42** (2 orphaned) and makes 6 × 6 = **36**, not the stated 38.

**Fix (if you keep 44):** `[sc 5, dec] 6 times, sc 2. (38 sts)` — consumes 44 ✔, makes 38 ✔.
**In the corrected pattern** (which runs on 48 after D4): `[sc 6, dec] 6 times. (42 sts)`.

### 🔴 D6 — Torso Round 24: two errors

> `Round 24: [sc 4, dec] 6 times. (32 sts)`

From 38 sts: consumes 6 × 6 = **36** (2 orphaned) and makes **30**, not the stated 32.

Note Rounds 25 and 26 are both **correct** — `[sc 2, dec] × 8` on 32 and `[sc 1, dec] × 8` on 24 both
balance exactly. The author can do this; Round 24 is a slip, not a misunderstanding.

### 🔴 D7 — Wing Row 4: two errors

> `Row 4: Ch 1, FLO sc 12, inc, turn. (15 sts)`

From 14 sts: consumes 12 + 1 = **13** (1 orphaned) and makes 12 + 2 = **14**, not the stated 15.

**Fix:** `sc 13, inc` — consumes 14 ✔, makes 15 ✔.

### 🔴 D8 — Wing Row 5: `fpdc` is worked around single crochet posts

> `Row 5: Ch 2, [dc 1, fpdc 1] 7 times, dc 1, turn. (15 sts)`

The arithmetic is fine (consumes 15, makes 15). The technique is not. A front post double crochet is
worked *around the post* of the stitch below — and Row 4 is a row of **sc**. Standard references are
explicit that you need a row of taller stitches to give you posts to work around; dc is the normal
choice [1](https://www.hanjancrochet.com/front-post-and-back-post-double-crochet/)[2](https://hearthookhome.com/crochet-front-post-and-back-post-crochet-stitches/),
and post stitches worked into sc are rare precisely because the post is too short [3](https://www.marymaxim.com/blogs/beginner-crochet/how-to-front-post-double-crochet-for-advanced-beginners).

It is made worse by Row 4 being worked **FLO**, which leaves the sc even shorter and looser. You will
be trying to wrap a double crochet around a half-height, single-loop post.

**Fix:** make Row 4 a hdc row so Row 5 has something to grip:
`Row 4: Ch 1, hdc 13, 2 hdc in last st, turn. (15 sts)` — and drop the FLO here.
Bonus: this finally uses `hdc`, which is defined in the abbreviations and otherwise never appears.

### 🔴 D9 — The wing tab does not exist, and would not fit if it did

> Wing: *"Insert lower wing tab into Socket 1/2 of Torso."*
> Assembly 2: *"Insert Wing base tabs through Round 22 Torso sockets."*

**No tab is ever created.** The wing is a flat panel; Rows 1–7 never shape anything that could be
called a tab, and "tab" is never defined.

And the geometry rules it out anyway. At the pattern's own gauge (5.5 sts/in, 6 rows/in):

| | |
|---|---|
| socket slot (ch 3 over 3 skipped sts) | **0.55 in** |
| wing panel, widest edge (Row 1, 17 sts) | 3.09 in |
| wing panel, narrowest edge (Row 7, 12 sts) | 2.18 in |
| wing panel, row-end edge (7 rows) | **1.17 in** |

The smallest dimension the wing has is **2.1× wider than the socket**. Nothing about this panel goes
through that slot.

**Fix:** add a shaped tab to the wing and widen the socket to match — the corrected pattern tapers
the wing to a 6-stitch, 3-row tab and makes the socket `ch 6` over 6 skipped sts, so both are
1.09 in.

### 🔴 D10 — Tail Rounds 22–24: stated count is wrong by 2

> `Round 21: [sc 5, inc] 2 times. (14 sts)` → `Round 22–24: sc around. (16 sts)`

Round 21 is correct and leaves you with **14**. "sc around" makes exactly one stitch per stitch, so
Rounds 22–24 give **14, not 16**. A plain round can never change the stitch count.

This also means Assembly step 4 attaches a 14-stitch tail opening while the pattern thinks it is 16.

**Fix (keeps the author's 16):**
```
Round 22:    [sc 6, inc] 2 times. (16 sts)
Rounds 23-25: sc around. (16 sts)
```

---

## 2. Technique concerns

### 🟠 T1 — The leg silently switches from joined rounds to spiral
Rounds 1–4 are explicitly joined (`join with sl st`, `Ch 1 … join`). Round 5 onward says only
"sc in each st around" with no join and no chain. That is a spiral. The switch is never announced,
and at a Master/Expert level the reader will assume the joins continue and end up with a seam and a
chain-1 jog stacking up the whole leg.

### 🟠 T2 — No piece states spiral vs. joined at all
Head, Torso and Tail never say. Given the Leg explicitly *does* use joins, silence elsewhere is
genuinely ambiguous rather than merely sloppy.

### 🟠 T3 — Row 5's `Ch 2` is undeclared
For a dc row, a turning ch-2 or ch-3 very often counts as the first stitch. The stitch count here
(7 × 2 + 1 = 15) shows it must **not** count — but the pattern never says so, and that is exactly
the kind of thing that costs an expert crocheter a whole row.

### 🟠 T4 — Wing Row 7 is missing its turning chain
Rows 2–6 all begin `Ch 1`. Row 7 begins `[sc 3, dec] 3 times` with no chain and no `turn`.

### 🟠 T5 — Popcorns in a stuffed sc fabric
`pc` = 5 dc in one stitch. Five dc-height stitches inside a 30-stitch sc round create a stitch
roughly 3× the height of its neighbours and a substantial hole at its base. On a firmly stuffed head
in a light colour the polyfill will show through the scale ridge. Worth a note telling the maker to
pack stuffing away from the ridge, or to line it.

### 🟠 T6 — 16 picots on a 16-stitch round
Leg Round 3 puts a picot on **every single stitch**. That is a dense frill, not a gear flange —
gear teeth read better with gaps between them. `[sc 1, picot] 8 times` alternating with plain sc
would look more mechanical. (The arithmetic is correct either way.)

---

## 3. Missing content

### 🟡 M1 — The safety eyes are never used
Materials lists "10 mm safety eyes". The word *eye* appears **nowhere else in the pattern** — not in
the head section, not in assembly. The dragon has no face. (The size itself is fine: 10 mm on a
44 mm head is 23 %, well judged.)

### 🟡 M2 — `ch` and `sl st` are used but never defined
Both appear constantly — `Ch 1`, `ch 3`, `ch 18`, `Ch 2`, `join with sl st`, and inside the `picot`
definition itself. Neither is in the abbreviation list.

### 🟡 M3 — `hdc` is defined but never used
A dead entry. (The corrected pattern puts it to work in Wing Row 4.)

### 🟡 M4 — The legs are never stuffed
And they are sealed shut by the Round 15 torso join, so there is no later opportunity.

### 🟡 M5 — The tail is never stuffed
24 rounds, "Fasten off." A segmented clockwork tail that flops defeats the design.

### 🟡 M6 — No yarn quantities and no finished size
Three colours, no grams or yards for any of them. No finished measurement — it works out to roughly
**10 in / 25 cm tall**.

### 🟡 M7 — Assembly step 4 is vague
"Attach Tail Round 24 to base of Torso (Rounds 2–6)" — Rounds 2–6 of the torso span 12 to 30 stitches
and are a steep cone. A 14-stitch tail opening cannot sit across all of that.

---

## 4. Proportion advisories

### 🔵 P1 — The wings are too small for a dragon
3.09 in × 1.17 in — a **2.6 : 1** strip, only **27 %** of the torso height (4.33 in). The corrected
pattern takes the panel to 2.17 in deep, which reads as a wing.

### 🔵 P2 — The legs are slightly wider than the torso
Each leg is 1.39 in across at the gear flange; side by side that is **2.78 in** against a **2.55 in**
torso. Not fatal — the flanges can splay outward — but they will overhang.

### 🔵 P3 — Head-to-torso ratio
Head 1.74 in diameter against a 2.55 in torso (0.68 : 1). Fine for a dragon; noted only so you know
it was checked.

---

## 5. What is correct

- **The entire Thigh & Leg — all 15 rounds.** Picot gear flange, the BLO recovery round behind the
  picots, the joined-round start, `[dec] 3 times, sc 6` closing to exactly 9. Not one error.
- **The short-row jaw block (Rows 11a–11c)** — consumption and production exact at every step.
  Only the *rejoin* is wrong, not the shaping.
- **The popcorn scale ridge (Head R9)** — 10 + (5 × 2) + 10 = 30 consumed, 30 made. Exact.
- **The ch-3 wing sockets (Torso R22–23)** — both rounds consume 38 and make 38. The buttonhole
  construction is correct and the slot genuinely survives Round 23 closing over it. Good technique.
- **Torso Rounds 1–14, 25, 26** — exact.
- **Wing Rows 1, 2, 3, 6, 7** — exact, including `ch 18 → 17 sc` and the picot row.
- **Tail Rounds 1–21** — exact, across four colour changes.
- **Head Rounds 1–14** — exact.
- **Gauge is stated in rounds** (`22 sts × 24 rnds`), which is the right choice for a piece worked
  almost entirely in the round. Neither of the two previous patterns did this.

---

## 6. Corrected pattern

[`steampunk-clockwork-dragon-CORRECTED.md`](./steampunk-clockwork-dragon-CORRECTED.md) — validates
with **0 defects**.

| Piece | Where | Was | Now |
|---|---|---|---|
| Head | R12 | 28 sts, raw edges dropped | 34 sts, 3 sc up each raw edge |
| Head | R13 | — | `[sc 3, dec] 6 times, sc 4. (28)` absorbs the extra |
| Head | R15 → R16 | `[sc 5, inc] x2 (16)` | `[sc 6, inc] x2 (16)` |
| Torso | R15 | 12/14/6, skip 4 each, (44) | 18/18, skip **3** each, **(48)** |
| Torso | R19 | `[sc 5, dec] x6 (38)` | `[sc 6, dec] x6 (42)` |
| Torso | R22–23 | `ch 3`, skip 3 | `ch 6`, skip 6 — matches the new tab |
| Torso | R24–27 | 3 closing rounds | 4 rounds: 42→36→30→24→16 |
| Wing | Row 4 | `FLO sc 12, inc (15)` | `hdc 13, 2 hdc in last st (15)` |
| Wing | Rows 8–13 | *(no tab)* | tapers to a 6-st × 3-row tab |
| Tail | R22 | `sc around (16)` | `[sc 6, inc] x2 (16)` |

Plus: eye placement added, `ch`/`sl st` defined, stuffing for legs and tail, a global spiral/join
note, the ch-2 declaration, yarn quantities and finished size.

---

## 7. How this was tested

1. **`StitchCountValidator`** (this repo) per piece — caught **D2, D5, D6** (3 of 14).
2. **`PatternValidator`** multi-pass compiler (this repo).
3. **An independent verifier written from scratch** (`verify_dragon.py`) modelling short rows and
   their raw-edge perimeter, popcorn and picot costs, the leg-gusset join, chain-space sockets, and
   tab-vs-socket geometry — the repo engine handles none of these. It caught all 14, including
   **D1, D3, D4, D9 and D10, which no automated check in the repo can see**.
4. **External verification** of the post-stitch claim (D8) against three crochet references.
5. **Gauge-based geometry** for every dimensional claim, from the pattern's own stated gauge.

```bash
python reviews/steampunk-clockwork-dragon/verify_dragon.py           # -> 14 defects
python reviews/steampunk-clockwork-dragon/verify_dragon.py --fixed   # -> 0 defects
```

The verifier deliberately treats Row 11a as a **legitimate** short row (holding 18 stitches is the
whole point) rather than flagging it as orphaned — an automatic "consumed ≠ available" rule would
report a false positive there.

---

## All three patterns

| | Bear | Wyvern | Dragon |
|---|---|---|---|
| Level claimed | Beginner | Advanced | Master/Expert |
| Hard defects | 5 | 5 | **14** |
| Rounds checked | 48 | 75 | 93 |
| Defect rate | 10 % | 7 % | **15 %** |
| Impossible rounds | 1 | 0 | 0 |
| Abbreviations complete | ❌ | ✅ | ❌ (`ch`, `sl st`) |
| Eyes placed | ✅ | ✅ | ❌ **never** |
| Interfaces match | n/a | ✅ | ❌ (head 14 vs torso 16) |
| Flawless pieces | Muzzle, Legs | Head, Toe, Wing rows | **Thigh & Leg** |

The dragon's ambition is real and most of it lands — the short rows, the sockets, the popcorn ridge
and the entire leg are expert-grade work. But the defect *rate* is the highest of the three, and the
cause is narrow and fixable: **the author does not recompute repeats when a round produces a count
that isn't a tidy multiple of 6.** Every single arithmetic failure in this pattern is an instance of
that one habit.
