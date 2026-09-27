# Pattern Review — "Void-Warped Chimera"

**Verdict: ❌ FAILS — 17 defects, and every single assembly directive is impossible.**

| | |
|---|---|
| Pieces checked | 4 (Cranial Core, Internal Partition, Trifurcating Tentacle, Mantle/Torso) |
| Rounds / rows checked | 44 instruction lines = 77 physical rounds & rows |
| **Hard defects** | **17** |
| Technique concerns | 4 |
| Missing content | 6 |
| **Assembly directives that work** | **0 of 4** |
| Pieces that are 100 % correct | Internal Partition |

This is the highest defect rate of the five patterns — **22 %**, against 7–15 % for the others.

It is also the first one where **the assembly section is a total loss**. All four directives fail:
the partition doesn't fit the round it grafts into, the head doesn't fit the torso, the tentacle
gusset is arithmetically impossible, and two of the four safety eyes are mounted somewhere a safety
eye physically cannot go.

---

## ⚠ Two systematic faults

**Fault 1 — the off-by-two cascade.** Cranial Rounds 15, 17 and 18 are *the same error three times
running*: a `[sc n, dec] × 6` repeat sized for a round 2 stitches smaller than the one before it.

| Round | Available | Repeat consumes | Short by | Makes | States |
|---|---|---|---|---|---|
| R15 | 44 | 42 | **2** | 36 | 38 |
| R17 | 38 | 36 | **2** | 30 | 32 |
| R18 | 32 | 30 | **2** | 24 | 26 |

Every one of them follows a round that produced a **non-multiple of 6** (44, 38, 32). This is the
identical habit that produced 5 of the Clockwork Dragon's 14 defects. The pattern even names the
section *"Irregular Modulo Drift"* — that is precisely what has gone wrong, just not on purpose.

**Fault 2 — no cross-piece checking.** Each piece was clearly worked out on its own; nothing was
checked against the piece it attaches to. Hence 0 of 4 assembly directives.

---

## 1. Show-stoppers

### 🔴 S1 — The Trifurcating Tentacle has no opening anywhere

| End | State |
|---|---|
| Round 1 — the base | `magic ring 9 sc` → **pulled closed** |
| Branch 1, R19a | *"Fasten off and **cinch shut**"* |
| Branch 2, R19b | *"Fasten off and **cinch shut**"* |
| Branch 3, R19c | *"Fasten off and **cinch shut**"* |

Four ends, all sealed. But Torso Round 7 says `sc 3 across inner edge of Trifurcating Tentacle 1`,
which requires an **open ring to crochet into**. There isn't one.

The stitch count, at least, is right: the base is 9 sts and the socket wants 3 + 6 = 9.

**Fix:** `Round 1: With Color A, ch 9, join with sl st to form a ring. Leave this end open — it is
the body socket. (9 sts)`

### 🔴 S2 — Torso Round 7: the tentacle gusset is arithmetically impossible

> R7 works: `sc 2 Body … sc 6 Body … sc 13 Body` = **21** of the body's 24 stitches.
> Assembly 3: *"Cinch the **6** outer held stitches of Trifurcating Tentacles to the **6** skipped
> body stitches under each socket."*

Six skipped body stitches per tentacle means **12 skipped**. But the round already works 21, and

**21 worked + 12 skipped = 33 > 24 body stitches.**

There are not enough stitches in the body to do what the assembly asks. Separately, only
24 − 21 = **3** body stitches are unaccounted for in R7, which matches neither 12 nor any even split
between two sockets.

**Fix:** work the tentacle's **outer** majority into the round and hold the small inner group — the
opposite of what the pattern does:
```
Round 7: sc 3 Body, sc 6 across OUTER edge of Tentacle 1 (3 inner sts held), skip 3 Body sts,
         sc 9 Body, sc 6 across OUTER edge of Tentacle 2 (3 held),        skip 3 Body sts,
         sc 6 Body. (30 sts)
```
Body: 18 worked + 6 skipped = 24 ✔  Made: 18 + 12 = 30 ✔  Gusset: 6 held ↔ 6 skipped ✔

### 🔴 S3 — Assembly 1: the partition is 8 stitches too small

> *"Graft the Internal Partition (Round 5, **30 sts**) into Round 15 of Cranial Core"*

Cranial Round 15 is **38 sts** as stated (36 as it actually works out). A 30-stitch disc cannot be
grafted into either. The Internal Partition is, ironically, the only piece in the pattern with no
internal errors at all — it is just the wrong size for its job.

**Fix:** add `Round 6: [sc 4, inc] 6 times. (36 sts)` to the partition and graft it into Cranial
Round 13, which the corrected pattern lands on 36. *And say when* — it has to go in as you reach
Round 13, not afterwards, because the head closes over it.

### 🔴 S4 — Assembly 2: the head is 26 stitches, the torso is 18

> *"Sew Cranial Core base (Round 18, **26 sts**) to Torso top (Round 16, **18 sts**)."*

The pattern states both numbers correctly and then instructs you to sew them together anyway.
26 ≠ 18, and a 44 % gather at the neck is not a seam, it is a pucker.

**Fix:** carry the cranial decreases down to 18: `Round 20: [sc 1, dec] 8 times, sc 2. (18 sts)` —
consumes 26 ✔, makes 18 ✔.

### 🔴 S5 — Assembly 4: you cannot put a safety eye on a frill

> *"Mount 2 safety eyes on the Cranial Vault, and **2 safety eyes on the Hyperbolic Frill**"*

A safety eye needs flat, stable fabric and **rear access to seat its washer**. The Hyperbolic Frill
is a free-hanging edge of treble fans — no flat area, no reachable back, and nothing to clamp
against. The washer would simply fall off inside the ruffle.

**Fix:** put all four eyes on the cranial vault (it is an *asymmetric* chimera — four eyes on one
head suits it), or use embroidered eyes / glued cabochons on the frill.

---

## 2. Count errors

### 🔴 D1 — Cranial Round 15: two errors

> `Round 15: [sc 5, dec] 6 times. (38 sts)`

From 44: consumes 6 × 7 = **42** (2 orphaned), makes 6 × 6 = **36**, not 38.
**Fix:** `[sc 5, dec] 6 times, sc 2. (38 sts)` — consumes 44 ✔, makes 38 ✔.

### 🔴 D2 — Cranial Round 17: two errors

> `Round 17: [sc 4, dec] 6 times. (32 sts)`

From 38: consumes **36** (2 orphaned), makes **30**, not 32.
**Fix:** `[sc 4, dec] 6 times, sc 2. (32 sts)`.

### 🔴 D3 — Cranial Round 18: two errors

> `Round 18: [sc 3, dec] 6 times. (26 sts)`

From 32: consumes **30** (2 orphaned), makes **24**, not 26.
**Fix:** `[sc 3, dec] 6 times, sc 2. (26 sts)`.

---

## 3. Structural & geometric defects

### 🔴 D4 — Cranial Round 13: one raw row-end per side is left unworked

> `Round 13: sc 8 across Row 12c, sc 2 down raw row ends, sc 24 across unworked Round 11 sts, sc 2 up raw row ends. (36 sts)`

The short-row block is 3 rows tall, so it has **3 row-ends on each side**. The rejoining round works
only **2** into each.

| | |
|---|---|
| live stitches on Row 12c | 8 |
| untouched Round 11 stitches | 24 |
| raw row-ends (3 × 2 sides) | 6 |
| **true perimeter** | **38** |
| Round 13 works | 36 |

Two positions — one per side — are skipped, leaving a small hole at each corner of the brow wedge.
This is much milder than the Clockwork Dragon (which dropped all 6), and the produced count of 36 is
self-consistent, which is why it hides well.

**Fix:** work all three row-ends per side and absorb the extra with a decrease at each corner:
```
Round 13: sc 8 across Row 12c; dec over the first 2 raw row-ends, sc 1 in the third;
          sc 24 across the unworked Round 11 sts;
          sc 1 in the first raw row-end, dec over the last 2. (36 sts)
```
Consumes all 38 ✔, still makes 36 ✔.

### 🔴 D5 — The trifurcation leaves Bridge 1's underside unworked

The three-way fork is built as two sequential bifurcations, which is the right idea. But trace the
bridges:

| Bridge side | Used by |
|---|---|
| Bridge 1 — top | Branch 1 |
| **Bridge 1 — underside** | **nobody** |
| Bridge 2 — top | Branch 2 |
| Bridge 2 — underside | Branch 3 |

Bridge 1 spans across the whole 6-stitch opening that Branches 2 and 3 come out of. Nothing is ever
worked into its underside, so there is a **2-chain slit between Branch 1 and the Branch 2/3 pair**.

The instruction is also ambiguous: Branch 3 says *"sc 2 across underside of **the** bridge"* when two
bridges exist.

**Fix:** treat the lower group as a proper ring that includes Bridge 1's underside, then fork it:
```
Lower group ring = 6 skipped base sts + 2 Bridge-1 underside sts = 8 sts
Round 11b (fork 2): sc 4, ch 2 (Bridge 2), skip 4 sts.   Branch 2 = 4 + 2 = 6 sts
Branch 3 = the 4 skipped sts + Bridge 2's underside      = 4 + 2 = 6 sts
```
All four bridge sides now used, nothing orphaned. Branch closings become `[dec] 3 times. (3 sts)`.

### 🔴 D6 — Torso Round 12: the frill is 21× the circumference it hangs from

> `Round 12: [sl st, hdc, dc, tr, dc, hdc, sl st] in each st around. (756 sts)`

The arithmetic is right — 7 × 108 = 756 ✔. The object is not.

| | |
|---|---|
| base round (R11) | 108 sts = 19.6 in |
| frill produced | **756 sts = 137 in = 11.5 feet of edge** |
| torso it hangs from (R9, 36 sts) | 6.5 in circumference |
| **fullness vs. that circumference** | **21×** |
| density | **7 sts per base stitch** (a shell edging runs 2–2.5) |
| yarn in this one round | ≈ 34 yds / 17 g |

Rounds 10 and 11 are legitimate hyperbolic growth — `inc` in every stitch (2×) then `[sc 1, inc]`
(1.5×). That part is correct technique. Round 12 is not hyperbolic growth, it is an **edging**, and
at 7 stitches per base stitch with trebles and **no anchoring stitch between fans**, 11½ feet of
treble fabric has nowhere to go. It will compress into a solid ball around a 2-inch torso.

**Fix:** anchor it and halve the density — `*[hdc, dc, hdc] in next st, sl st in next st*; repeat
around` = 216 sts, 39 in of edge, 2.0 sts per base stitch, still a dramatic 6× frill.

### 🔴 D7 — Cranial Round 16: the post stitch is anchored into single crochet, two rounds down

> `Round 16: Switch to Color B, [sc 2, **fptr 1 into Round 14**] 12 times, sc 2. (38 sts)`

Two problems in one instruction.

**(a) Round 14 is a round of `sc`.** A *treble* post stitch has to wrap the post of the stitch below,
and standard references are explicit that you need a row of taller stitches to work around
[1](https://www.hanjancrochet.com/front-post-and-back-post-double-crochet/)[2](https://hearthookhome.com/crochet-front-post-and-back-post-crochet-stitches/);
post stitches into sc are rare precisely because the post is too short
[3](https://www.marymaxim.com/blogs/beginner-crochet/how-to-front-post-double-crochet-for-advanced-beginners).
A treble is taller than the double crochet those sources discuss, so this is the most extreme version
of the problem seen in any of these patterns — and it also has to span Round 15 on the way, which
will pucker the fabric into a vertical dart.

### 🔴 D8 — Cranial Round 16: the ridge cannot stack vertically

The 12 posts are spaced every 3 stitches around a **38-stitch** round but anchored into a
**44-stitch** round. 38 and 44 do not share that spacing, so each post lands progressively further
around than the last. The "eyestalk ridge" will spiral around the head rather than run straight up it.

**Fix for D7 + D8:** insert a plain `hdc` round immediately below the post round and anchor into
*that*, with matching stitch counts:
```
Round 16: hdc in each st around. (38 sts)
Round 17: Switch to Color B, [sc 2, fptr 1 around the post of the corresponding
          Round 16 st] 12 times, sc 2. (38 sts)
```

---

## 4. Technique concerns

### 🟠 T1 — Joined or spiral is never resolved
Piece 1's heading says "continuous spiral." The Torso opens `ch 24, join with sl st to form a ring`
and then says only "sc in each st around" — joined start, unstated continuation. The Tentacle and
Partition say nothing at all. Three of four pieces are ambiguous.

### 🟠 T2 — The Cranial Core is never stuffed
It ends `Round 18 … Fasten off.` with no stuffing instruction — and with the Internal Partition
grafted inside, it has **two separate chambers** that each need stuffing at different moments. The
pattern addresses neither.

### 🟠 T3 — The Tentacles are never stuffed
Sealed at four ends and crocheted into the torso at Round 7, so there is no later access.

### 🟠 T4 — "Dual Eyestalk Cavity" promises a piece that doesn't exist
The section title and the "Post-Stitch Eyestalk Ridges" heading both refer to eyestalks; no eyestalk
is ever made, and assembly mounts the eyes flat on the vault. Either add the piece or rename the
sections.

---

## 5. Missing content

| | |
|---|---|
| 🟡 M1 | **No yarn quantities** — three colours, no grams or yards for any |
| 🟡 M2 | **No finished size** — it works out to roughly 7 in / 18 cm plus tentacles |
| 🟡 M3 | **No eye placement** — assembly says how many and roughly where, but no round numbers or spacing |
| 🟡 M4 | **No note on when to graft the partition** — it must go in before the head closes over it |
| 🟡 M5 | **Round 12's fan has no stated repeat anchor** — "in each st around" with no sl st between fans |
| 🟡 M6 | **No warning about the frill's bulk** — 756 stitches is roughly 1½–2 hours for a single round |

---

## 6. What is correct

- **The Internal Partition** — all five rounds exact. The only piece in the pattern with no internal
  errors.
- **Cranial Rounds 1–11 and the short-row block (12a–12c)** — exact, including both double-decrease
  short rows.
- **Cranial Round 14** — `sc 10, [inc] 8 times, sc 18` consumes all 36 and makes exactly 44. An
  irregular, asymmetric expansion round done correctly, which is harder than it looks.
- **Cranial Round 16's stitch count** — 12 × 3 + 2 = 38 ✔ (only its anchoring is wrong).
- **The trifurcation's branch arithmetic** — every branch ring is 3 + 2 = 5, every branch round
  consumes and produces 5, and every closing round (`dec 2, sc 1` → 3) balances exactly. The
  *topology* has a hole, but not one stitch count is wrong.
- **Torso Round 1 opens with `ch 24, join`** — an open foundation ring, exactly the right call for a
  piece that has to attach at the bottom. (The Leviathan got this wrong; this pattern got it right.)
- **Torso Rounds 9–11** — correct hyperbolic growth, and `[sc 2, inc] × 9` on 27 is exact.
- **The FLO/BLO split (Rounds 10 and 13)** — Round 10 works the front loops of Round 9 to grow the
  frill, then Round 13 comes back and picks up Round 9's **36 free back loops** to continue the
  torso behind it. Both counts are right and the technique is genuinely elegant. This is the single
  best idea in the pattern.
- **Torso Rounds 13–16** — exact.
- **The glossary is complete** — all 11 abbreviations defined, all 11 used, none dead.
- **Safety-eye quantity is specified (×4)** and all four are accounted for in assembly — the first
  pattern of the five to manage that.

---

## 7. Corrected pattern

[`void-warped-chimera-CORRECTED.md`](./void-warped-chimera-CORRECTED.md) — validates with
**0 defects**.

| Piece | Where | Was | Now |
|---|---|---|---|
| Cranial | R13 | 2 sc per raw edge, 2 positions dropped | all 3 worked, 2 decs absorb them |
| Cranial | R15 / R17 / R18 | `[sc n, dec] x6` | `[sc n, dec] x6, sc 2` (each) |
| Cranial | R16 | *(none)* | new `hdc` round as the post foundation |
| Cranial | R17 | `fptr into Round 14` (sc, 2 down) | `fptr` into R16's hdc posts |
| Cranial | R20 | *(ended at 26)* | `[sc 1, dec] x8, sc 2. (18)` — matches torso |
| Partition | R6 | *(ended at 30)* | `[sc 4, inc] x6. (36)` — matches Cranial R13 |
| Tentacle | R1 | `magic ring 9 sc` (closed) | `ch 9, join` — **open** body socket |
| Tentacle | fork 2 | lost Bridge 1's underside | 8-st group ring, all 4 bridge sides used |
| Torso | R7 | inner edges worked, gusset impossible | **outer** edges worked, 6 held ↔ 6 skipped, (30) |
| Torso | R9 | `[sc 2, inc] x9` | `[sc 4, inc] x6. (36)` |
| Torso | R12 | 7 sts into every st → 756 | anchored fan every 2nd st → 216 |
| Assembly | 4 | 2 eyes on the frill | all 4 on the vault, with rounds and spacing |

---

## 8. How this was tested

1. **`StitchCountValidator`** (this repo) per piece — caught **D1, D2, D3** (the count errors) and
   flagged Torso R7. 3 of 17.
2. **`PatternValidator`** multi-pass compiler (this repo).
3. **An independent verifier written from scratch** (`verify_chimera.py`) modelling short-row
   perimeters, **bridge-side accounting for the three-way fork**, the FLO/BLO split that runs two
   fabrics off one round, limb-socket worked/skipped/held arithmetic, tentacle end-state, and
   edging fullness. It caught all 17 — including every show-stopper, none of which is an arithmetic
   error a stitch-count engine could see.
4. **External verification** of the post-stitch claim (D7) against three crochet references.
5. **Gauge-based geometry** for every dimensional claim, from the pattern's own stated gauge.

```bash
python reviews/void-warped-chimera/verify_chimera.py           # -> 17 defects
python reviews/void-warped-chimera/verify_chimera.py --fixed   # -> 0 defects
```

---

## All five patterns

| | Bear | Wyvern | Dragon | Leviathan | **Chimera** |
|---|---|---|---|---|---|
| Level claimed | Beginner | Advanced | Master | Grandmaster | Beyond GM |
| Hard defects | 5 | 5 | 14 | 12 | **17** |
| Rounds checked | 48 | 75 | 93 | 108 | 77 |
| Defect rate | 10 % | 7 % | 15 % | 11 % | **22 %** |
| Glossary complete | ❌ | ✅ | ❌ | ✅ | ✅ |
| Eyes usable | ✅ | ✅ | ❌ none | ❌ none | ⚠ 2 of 4 |
| Head↔body match | n/a | ✅ | ❌ | ✅ | ❌ |
| Cross-piece (join) defects | 0 | 2 | 3 | 4 | **4** |
| Show-stoppers | 1 | 1 | 2 | 2 | **5** |

### The one finding that spans all five

**These patterns get the inside of a piece right and the join between pieces wrong.**
The wyvern abandoned 6 body stitches at the leg join; the dragon sewed 3 stitches to 4; the leviathan
dropped 20 body stitches *and* built a tentacle with no opening; the chimera does both of those plus
a partition and a neck that don't fit.

The totals across all five:

| | |
|---|---|
| rounds checked | **401** |
| defects found | **53** |
| of those, cross-piece / join defects | **13 (25 %)** |
| show-stoppers (project cannot be completed) | **11** |
| …of which are join failures | **8 of 11** |

The arithmetic **within** a tube is nearly always right — and often impressive. The arithmetic
**between** two pieces accounts for a quarter of all defects and **eight of the eleven
show-stoppers**.

**The check that would have caught most of it.** For every join, write three numbers and verify two
equations:

```
worked  = limb stitches crocheted into the body round
skipped = body stitches passed over beneath the limb
held    = limb stitches left for the gusset

(body worked + skipped) must equal the body's previous round
(held)                  must equal (skipped)
```

And for every seam, write the two stitch counts side by side and confirm they are equal.

That single discipline would have caught **13 of the 53 defects** found across these five patterns —
and, more to the point, **8 of the 11 show-stoppers**. It is the highest-yield check available, and
none of the five patterns applies it.
