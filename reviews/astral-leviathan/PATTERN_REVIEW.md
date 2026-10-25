# Pattern Review — "The Astral Leviathan"

**Verdict: ⚠️ THE BEST OF THE SEVEN — 14 defects, but 3 of the hardest problems in the series are
solved correctly for the first time.**

| | |
|---|---|
| Sections checked | 4 (Cranial Vault, Tentacle Hub, Torso, Wings) |
| Rounds / rows checked | 64 instruction lines = 93 physical rounds & rows |
| **Hard defects** | **14** |
| Defect rate | **15 %** |
| **Self-verification claims audited** | **9 — 7 correct, 2 wrong** |
| Sections that are 100 % correct | **Section 2 (the entire trifurcation, 38 rounds)** |

This pattern does something none of the previous six did: **it verifies itself.** It carries a
"Body Conservation" sum, a "Gusset Parity" statement, a "Fullness Ratio", a bridge-conservation
table and a formal assembly matrix. So the first job is to audit those claims — and **seven of the
nine hold up.**

The two that don't are the two biggest defects in the pattern, and one of them is a proof that
*looks* rigorous and isn't.

---

## ⚠ The headline: a self-verification that is itself invalid

### 🔴 D1 — Torso Round 17: the "Body Conservation" proof cheats

> **Body Conservation:** 14 (worked) + 6 (skipped) + 24 (worked) + **12 (outer root)** = 56 input
> body sts accounted for.

**The 12 is a tentacle stitch count. It has been added into a sum of body stitches.**

Count the body alone:

| | |
|---|---|
| body worked (`sc 14` + `sc 24`) | 38 |
| body skipped | 6 |
| **body accounted for** | **44** |
| body available from Round 16 | **56** |
| **body stitches silently dropped** | **12** |

The sum only reaches 56 by borrowing 12 stitches from a different piece. This is the most dangerous
kind of error in the whole series: a proof that *reads* as rigorous, uses the right vocabulary, and
gives a confident-looking total — while smuggling in a term that doesn't belong.

The round's own output is wrong by the same 12: it produces 14 + 12 + 24 = **50**, not the stated 62.

**Interesting:** the stated **62 is correct** for the intended construction. 56 body − 6 skipped = 50
body worked, plus 12 tentacle = 62. So the *total* is right and the *written segments are 12 short*.

**Fix:**
```
Round 17: sc 20 Body, sc 12 across OUTER edge of Tentacle Hub Root (holding 6 inner sts),
          skip 6 Body sts, sc 30 Body. (62 sts)
```
Body: 20 + 6 + 30 = 56 ✔ Made: 20 + 12 + 30 = 62 ✔
And Round 19 follows: `sc 20, [dec] 6 times across the join, sc 30. (56 sts)`

### 🔴 D2 — Row 13c: the perimeter claim doesn't add up

> `Row 13c: ch 1, skip sl st, sc 16 down row ends and across brow, sc 27 across remaining unworked Round 12 sts.` **(54 sts total perimeter restored)**

The round's own components are **16 + 27 = 43**, not 54. Off by 11.

And 54 wouldn't be right either. The true open perimeter after the short rows:

| | |
|---|---|
| Row 13b live sts (less the skipped sl st) | 16 |
| Row 13a sts Row 13b never reached | 13 |
| Round 12 sts never touched | 27 |
| raw row-ends (2 rows × 2 sides) | 4 |
| **true perimeter** | **60** |

Row 13c closes **43 of 60** — leaving **17 positions unworked** around the brow ridge.

**Fix:**
```
Row 13c: ch 1, skip the sl st, sc 16 across Row 13b, 2 sc down the first raw row-end edge,
         sc 13 across the exposed Row 13a sts, 2 sc down the second row-end edge,
         sc 27 across the unworked Round 12 sts. (60 sts)
```

---

## 1. The other hard defects

### 🔴 D3 — Torso Round 15: two errors

> `Round 15: [sc 3, 3-st-inc] 8 times. (56 sts)`

`3-st-inc` consumes 1 and produces 3, so the unit consumes 4 and produces 6.
From 40 sts: consumes 8 × 4 = **32** — **8 orphaned** — and produces 8 × 6 = **48**, not 56.

The *increase* count is right (8 × 2 net = +16, and 40 + 16 = 56). Only the plain-sc run is wrong.

**Fix:** `[sc 4, 3-st-inc] 8 times. (56 sts)` — consumes 8 × 5 = 40 ✔, produces 8 × 7 = 56 ✔

### 🔴 D4 — Wing Row 8: two errors

> `Row 8: ch 1, turn, sc 4, hdc 4, dc 4, tr 4, 3-st-inc in tr (3 tr in last st). (20 sts)`

From 18 sts: consumes 4 + 4 + 4 + 4 + 1 = **17** — **1 orphaned** — and produces 4 + 4 + 4 + 4 + 3 =
**19**, not 20.

**Fix:** `sc 4, hdc 4, dc 4, tr 5, 3 tr in last st. (20 sts)` — consumes 18 ✔, produces 20 ✔

### 🔴 D5 — Wing Row 8 contradicts the glossary

The glossary defines **`3-st-inc` = 3 **sc** in same st**. Row 8 writes `3-st-inc in tr (3 tr in
last st)` — three **trebles**. Same abbreviation, different stitch. Use a distinct name
(`3-tr-inc`) or spell it out.

### 🔴 D6 — Wing Row 9: the post stitch reaches three rows down

> `Row 9: ch 2, turn, hdc 1 in each st, working [fptr 1 into R6 hdc] every 4th st across.`

Row 6 is three rows below (Rows 7 and 8 intervene). A *treble* post stitch spanning three rows will
drag the fabric into a vertical dart.

**This pattern already knows better.** Section 1 does it correctly: Round 16 is a plain `hdc` round
described as *"(Provides post-stitch foundation row)"*, and Round 17 posts into it **adjacent**.
That is textbook. Section 4 simply doesn't follow its own example.

**Fix:** anchor into **Row 8** instead — it contains 4 dc and 5 tr, which are real posts, and it has
20 sts against Row 9's 20, so they align 1:1.

### 🔴 D7 — Wing Row 9: the posts cannot align

5 posts spaced every 4th stitch of a **20-stitch** row, anchored into a **12-stitch** row. 20 and 12
don't share that spacing, so each post lands further round than the last and the ridge skews.
Fixed automatically by D6's fix (20 ↔ 20).

### 🔴 D8 — Glossary: `ch` and `sl st` are never defined

Both are used constantly — `ch 18`, `ch 24`, `ch 7`, `ch 6`, `ch 3`, `ch 2`, `ch 1`, and `sl st` to
close every foundation ring. Neither appears in the glossary. (`ch-sp` is defined, which makes the
omission of `ch` itself more conspicuous.)

### 🔴 D9 — Glossary: four dead entries

`bpdc`, `ch-sp`, `3-st-dec` and `split-sc` are all defined and **never used**. `split-sc` is the
standout — it gets a full three-line definition explaining the Waistcoat Stitch ("worked directly
into the center V of the stitch post, not under top loops") and then never appears in a single round.

### 🔴 D10 — Finished dimensions are overstated

At the pattern's own stated gauge (6.5 sts/in, 7 rnds/in):

| | Claimed | Actual | |
|---|---|---|---|
| Length | 18 in | Cranial 2.71 + Torso 3.57 + Tentacle 3.00 = **9.3 in** | **1.9× over** |
| Wingspan | 12 in | 2 × 1.29 (wing projection) + 1.18 (torso dia) = **3.7 in** | **3.2× over** |

**Fix:** state ~9 in / ~4 in — or, to actually hit 18 in, rework the identical pattern in **worsted
weight on a 5.5 mm hook** (1.94× linear).

---

## 2. Secondary issues

### 🟡 S1 — Row 13b's key instruction is ambiguous
`dc 2 in next 2 sts` has two readings: *"dc in the next 2 sts"* (produces 13) or *"2 dc in each of
the next 2 sts"* (produces 17). **Only the stated count of 17 disambiguates it** — the wording never
does. Write it as `2 dc in each of the next 2 sts`.

### 🟡 S2 — No safety eyes, despite an entire eye subsystem
Section 1 builds an "Internal Eye-Shelf", "hollow eye sockets" and a dedicated FLO/BLO split to
create the shelf — and the materials list contains **no eyes of any kind**. Either add them (with a
placement round) or say the sockets are for embroidery.

### 🟡 S3 — The eye-shelf sealing is ordered after stuffing
Section 1 ends *"Fasten off… **Stuff Cranial Vault**."* Assembly step 2 then says to tack the brow
ridge to the internal eye shelf *"using the tail from Cranial Vault Round 19"* — an internal seam,
reached from the neck, through a head that is already stuffed. Move the sealing before the stuffing.

### 🟡 S4 — No spiral-vs-joined statement
Nothing says whether the Cranial Vault and Torso are continuous spirals or joined rounds. Tentacle
Round 9a says *"join to first sc of this round"*, so at least one section clearly joins — which makes
the silence elsewhere genuinely ambiguous rather than merely sloppy.

### 🟡 S5 — The tentacle branches are never stuffed
All three are sealed at the tip and the root is crocheted into the torso at Round 17. There is no
later access.

### 🟡 S6 — Wing tab: 3 rows or 4?
The note says *"This 6 sts × **3 rows** tab slides into the Torso socket"*, but Rows 1–4 are four
rows and Assembly says *"Insert **Row 1–4** Tab"*.

### 🟡 S7 — No yarn quantities, and the mantle's colour is unstated
Three colours, no grams or yards. Rounds 10–12 (the hyperbolic mantle) never say which colour —
Round 13 switches to Color C, implying 10–12 stay in Color A, but it is never said.

---

## 3. The seven self-verification claims that hold

This is what separates this pattern from the previous six. Each of these was checked independently:

| # | Claim | Verdict |
|---|---|---|
| 1 | Row 13a "(27 worked, 27 left)" | ✅ 18+1+1+2+1+1+2+1 = 27; 54 − 27 = 27 |
| 2 | Row 13b "(17 sts worked)" | ✅ under the "2 dc in each" reading |
| 4 | Torso R7 "4 + 6 + 8 + 6 = 24" | ✅ body consumed 24, produced 24 |
| 5 | Torso R12 "Fullness Ratio 150/90 = 1.67×" | ✅ 30 fans × 5 = 150; **1.67×** |
| 6 | Trifurcation "9 + 12 + 9" | ✅ 18 base + 12 bridge sides = 30 = 9+12+9 |
| 8 | Torso R17 "Gusset Parity 6 ↔ 6" | ✅ 18 root − 12 worked = 6 held = 6 skipped |
| 9 | Formal Assembly Graph Matrix (4 rows) | ✅ **all four interfaces correct** |

---

## 4. What this pattern gets right that none of the others did

### ✅ The trifurcation is topologically perfect — all 38 rounds

The Void-Warped Chimera's three-way fork left **Bridge 1's underside unworked**, leaving a slit.
This one accounts for every bridge side:

| Bridge side | Consumed by |
|---|---|
| Bridge 1 — top | Branch 1 (R9a) |
| Bridge 1 — underside | Branch 2 (R9b) |
| Bridge 2 — top | Branch 2 (R9b creates it) |
| Bridge 2 — underside | Branch 3 (R9c) |

**18 base sts + 12 bridge-side positions = 30 = 9 + 12 + 9.** Conservation holds exactly, nothing is
orphaned, and every branch round balances. This is the hardest construction in the series and it is
flawless.

### ✅ The post-stitch foundation is correct (Section 1)

Every previous pattern anchored post stitches into a round of **sc**, which has no usable post.
This one writes `Round 16: hdc in each st around. (Provides post-stitch foundation row)` and then
posts into it from the adjacent Round 17. **Exactly right** — and the reason Section 4's version
stands out as a lapse.

### ✅ The gusset parity is correct — a first

Bear: no join. Wyvern: 6 body sts abandoned. Dragon: 3 sewn to 4. Leviathan: 20 dropped.
Chimera: arithmetically impossible. **Astral Leviathan: 6 held ↔ 6 skipped, exact.**

### ✅ Every attachment interface matches

- Cranial R19 (24) ↔ Torso R1 (24)
- Wing tab Row 1 (6) ↔ Torso socket (6), twice
- Hub inner gusset (6) ↔ Torso skipped R17 (6)

Torso Round 7 creates the wing sockets with exact perimeter conservation (`4 + 6 + 8 + 6 = 24`), and
Round 8 closes over both chain bridges. The 6-stitch tab is 0.92 in wide and the 6-stitch slot is
0.92 in wide — **they physically fit**, which the Dragon's and Chimera's did not.

### ✅ Two FLO/BLO splits, both executed and counted correctly

- **Cranial:** R9 works FLO of R8's 48 sts; R14 returns to R8's 48 free back loops. Both exact.
- **Torso:** R10 works FLO of R9's 30 sts to grow the mantle; R13 returns to R9's 30 free back
  loops. Both exact.

### ✅ The frill is actually controlled

150 / 90 = **1.67×**, against the Chimera's **7.0×** per base stitch. The pattern's parenthetical
*"no self-entanglement"* is earned.

### ✅ Also correct
Cranial R1–R12 and R14–R19; Torso R1–R14, R16, R18–R25 (the whole closing sequence); Wing Rows 1–7;
the open `ch 18` hub root and `ch 24` neck ring, both left open for their sockets.

---

## 5. Corrected pattern

[`astral-leviathan-CORRECTED.md`](./astral-leviathan-CORRECTED.md) — validates with **0 defects**.

| Where | Was | Now |
|---|---|---|
| Row 13b | `dc 2 in next 2 sts` | `2 dc in each of the next 2 sts` |
| Row 13c | 16 + 27 = 43, stated 54 | full perimeter walk, **(60 sts)** |
| Torso R15 | `[sc 3, 3-st-inc] x8` | `[sc 4, 3-st-inc] x8. (56)` |
| Torso R17 | `sc 14 … sc 24` (38 body) | `sc 20 … sc 30` (50 body), **(62)** |
| Torso R17 note | invalid conservation sum | body-only sum: 20 + 6 + 30 = 56 |
| Torso R19 | `sc 14, [dec] x6, sc 36` | `sc 20, [dec] x6, sc 30. (56)` |
| Wing Row 8 | `tr 4, 3-st-inc` | `tr 5, 3 tr in last st. (20)` |
| Wing Row 9 | `fptr into R6` (3 rows down) | `fptr around Row 8's dc/tr posts` (adjacent, 20↔20) |
| Glossary | no `ch`/`sl st`; 4 dead entries | both added; dead entries removed |
| Materials | no eyes, no quantities | 2 × 8 mm eyes with placement, quantities added |
| Dimensions | 18 in / 12 in | ~9 in / ~4 in, with a worsted-weight upsize note |

---

## 6. How this was tested

1. **`StitchCountValidator`** and the multi-pass compiler (this repo).
2. **An independent verifier** (`verify_astral.py`) that adjudicates all nine self-verification
   claims and then runs its own round-by-round pass over everything the self-checks don't cover —
   including bridge-side accounting, both FLO/BLO splits, socket-vs-tab geometry, glossary coverage
   and gauge-derived dimensions.
3. **Gauge-based geometry** for every dimensional claim.

```bash
python reviews/astral-leviathan/verify_astral.py           # -> 14 defects
python reviews/astral-leviathan/verify_astral.py --fixed   # -> 0 defects
```

> **A note on my own method.** My first run reported 18 defects. Three were bugs in *my* harness:
> I modelled Torso R13 as a plain round when it is `[sc 4, inc] × 6`, mis-coded R19's second body
> run, and flagged R12's edging spacing as orphaned stitches when skipping 2 between fans is
> standard scallop spacing. All three were the pattern being right and my model being wrong. The
> figure of 14 is after those corrections.

---

## All seven patterns

| | Bear | Wyvern | Dragon | Leviathan | Chimera | Abomination | **Astral** |
|---|---|---|---|---|---|---|---|
| Hard defects | 5 | 5 | 14 | 12 | 17 | (annotated) | **14** |
| Rounds checked | 48 | 75 | 93 | 108 | 77 | ~100 | **93** |
| Defect rate | 10 % | 7 % | 15 % | 11 % | 22 % | — | **15 %** |
| Glossary complete | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Post stitch has a real post | — | — | ❌ | ❌ | ❌ | — | **✅ (§1) / ❌ (§4)** |
| Fork topology closed | — | — | — | — | ❌ | — | **✅** |
| Gusset parity | ❌ | ❌ | ❌ | ❌ | ❌ | — | **✅** |
| All interfaces match | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | **✅** |
| Self-verifies | ❌ | ❌ | ❌ | ❌ | ❌ | partial | **✅ 7/9** |

**The running finding across the whole series has been that patterns get the inside of a piece right
and the join between pieces wrong.** Across the first five, 13 of 53 defects were cross-piece joins,
and 8 of 11 show-stoppers.

**This pattern breaks that streak.** Every join is correct — gusset parity, both wing sockets, the
neck graft, the open hub root, the fork topology. Its 14 defects are all *inside* pieces: three
miscounted rounds, a post row that ignores the pattern's own good practice, and glossary and
documentation gaps.

That is a meaningfully different — and much more fixable — failure profile. The three arithmetic
errors (R15, R17, Wing Row 8) are each a one-line change.

**The one habit still worth adopting:** the R17 "Body Conservation" line shows that a self-check is
only as good as its terms. When you write a conservation sum, **label every term with the piece it
comes from** and confirm each side draws from one piece only:

```
body worked + body skipped        == body's previous round     (body terms only)
limb worked + limb held           == limb's open count         (limb terms only)
limb held                         == body skipped
round total                       == body worked + limb worked
```

Applied to Round 17 as written, line 1 gives 38 + 6 = 44 ≠ 56 and the error surfaces immediately.
