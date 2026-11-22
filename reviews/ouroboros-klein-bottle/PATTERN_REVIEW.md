# Pattern Review — "The Ouroboros Klein Bottle"

**Verdict: ❌ FAILS — 17 defects. Every round of actual crochet is correct except one, and
every structural claim about how they fit together is wrong.**

| | |
|---|---|
| Sections checked | 3 (Outer Bulb, Inner Shaft, Ouroboros Neck) |
| Rounds / rows checked | 28 instruction lines = 66 physical rounds & rows |
| **Hard defects** | **17** |
| **Topology-matrix rows audited** | **3 — 0 correct** |
| Rounds with arithmetic errors | **1 of 66** |
| Sections with perfect arithmetic | **Section 1 (all 25) and Section 2 (all 21)** |

This pattern has a split personality. **65 of its 66 rounds are arithmetically flawless** — Section 1
and Section 2 don't contain a single miscount, and the port round's own check (`20 + 16 + 20 = 56`)
is exact. Then the "MANIFOLD TOPOLOGY GRAPH MATRIX" asserts three edge pairings and **all three are
wrong**, the one join that does work isn't in the matrix, and the glossary omits every stitch the
pattern uses.

---

## 1. The topology matrix: 0 of 3

| Claimed | Actual | |
|---|---|---|
| Sec 2 R21 Flange (48) ↔ Sec 1 R8 Skipped Loop (48) | 48 ↔ **16** | ❌ |
| Sec 2 R1 Open Ring (16) ↔ Sec 1 R1 Magic Ring (16) | 16 ↔ **8**, *and closed* | ❌ |
| Sec 3 R42 (18) ↔ Sec 2 R18 Tunnel End (18) | 18 ↔ **16** | ❌ |

### 🔴 D1 — Row 1: the flange meets 16 stitches, not 48

Round 8 skips **16** stitches. Even counting the port's *entire* boundary — 16 skipped stitches
below plus the 16 chain stitches above — you get **32 positions**, never 48.

The assembly directive gives the game away: *"Align Section 2 Round 21 (48 sts) with the 16 skipped
stitches **and adjacent wall spaces** of Section 1 Round 8."* Those "adjacent wall spaces" are
**32 stitches that are defined nowhere in the pattern.** A 48-stitch flange is 6.86 in around; the
port boundary is 4.57 in. It is 1.5× too big and there is nothing to sew the surplus to.

### 🔴 D2 — Row 2: there is no edge there at all

Section 1 Round 1 is `magic ring 8 sc` — **8 stitches, and a magic ring is pulled shut.** By the time
you reach assembly it is the sealed centre of the bulb, buried under 25 rounds of fabric.

So the claim fails twice: the count is 8 not 16, and there is no open edge to whipstitch to under
any count.

**The pattern knows the fix.** Section 2 Round 1 is `ch 16, sl st to first ch to form open ring`,
and Section 3 depends on Section 1's open 24-stitch neck. Open rings are used correctly twice — just
not at the one place the topology requires one.

### 🔴 D3 — Row 3: 18 appears nowhere in Section 2

Section 2 runs `R1: 16 sts`, `R2–18: sc in each st around (16 sts)`. **Round 18 is 16 stitches.**
The matrix pairs it with Section 3's 18, and the number 18 does not occur anywhere in Section 2.

### ✅ And the one join that works isn't listed

*"Attach Color A to open 24 sts of Section 1 Round 25"* — Section 1 R25 is 24 sts and Section 3
starts on 24. **Exact.** It is the only correct interface in the pattern and the matrix omits it.

---

## 2. Is it actually non-orientable?

The approach is sound. A true Klein bottle cannot be embedded in 3-space, so every crocheted one is
an **immersion** with a physical pass-through instead of a self-intersection. This pattern does that
correctly, and the geometry works:

> a 16-stitch slit is **2.29 in** long and opens to a hole of perimeter ~**4.57 in**; the inner shaft
> is **2.29 in** around. It passes through comfortably. ✅

The **`inv-flip` is also the right idea** — reversing one end of a handle before seaming is exactly
how an orientable handle becomes a cross-handle, which is what makes a Klein bottle. It is the one
part of the non-orientability argument that survives.

But the realisation fails on two counts.

### 🔴 D4 — Section 1 Round 1 is a closed cap where the topology needs an opening
(see D2 above — the matrix depends on sewing to it.)

### 🔴 D5 — Round 18 of Section 2 is a *branch line*, not a seam

Round 19 is worked **FLO** of Round 18, so Round 18's back loops stay free. The matrix then grafts
Section 3 onto **those same back loops**. That puts **three sheets along one circle**:

| | |
|---|---|
| sheet 1 | the tunnel below Round 18 |
| sheet 2 | the flange above it, via the front loops |
| sheet 3 | Section 3's neck, via the back loops |

**A Klein bottle is a 2-manifold — exactly two sheets meet everywhere.** A triple line disqualifies
the "Non-Orientable" classification regardless of what the stitch counts say. Fix every number in
the matrix and this is still not a manifold.

The fix is structural: move the flange to Section 2's **Round 1** so the tunnel has two genuine
boundaries (flange and far end) and no FLO split at all.

---

## 3. The single arithmetic error

### 🔴 D6 — Row 29d: three faults in one line

> `Row 29d (Rejoin Round): ch 1, skip sl st, sc 8 across short row, sc 2 down row ends, sc 12 across remaining unworked Round 28 sts.` **(24 sts total perimeter restored)**

**(a)** Components sum to 8 + 2 + 12 = **22**, not the stated 24.

**(b)** *"sc 12 across remaining unworked Round 28 sts"* — Row 29a consumed 13 of Round 28's 24
(`sc 12, sl st 1`), so only **11** remain. There is no twelfth stitch.

**(c)** The true open perimeter after the short rows:

| | |
|---|---|
| Row 29c live (less the skipped sl st) | 8 |
| Row 29b leftover | 1 |
| Row 29a leftover | 1 |
| Round 28 unworked | 11 |
| raw row-ends (3 rows × 2 sides) | 6 |
| **true perimeter** | **27** |

The round closes **22 of 27** — the Row 29a/29b leftovers and 4 of the 6 row-ends are left open
along the outside of the curve.

Short rows **29a, 29b and 29c are each exactly right** (13/11/9, every consumption and production
balancing). Only the rejoin is wrong.

**Fix:**
```
Row 29d: ch 1, skip the sl st, sc 8 across Row 29c, dec over the two leftover sts of
         Rows 29b and 29a, work [sc 1, dec] into the 3 row-ends on the first side,
         sc 11 across the remaining Round 28 sts, work [sc 1, dec] into the 3 row-ends
         on the second side. (24 sts)
```
Consumes 8 + 2 + 3 + 11 + 3 = 27 ✔  Produces 8 + 1 + 2 + 11 + 2 = 24 ✔

---

## 4. The glossary is inverted

### 🔴 D7 — All seven basic operations are undefined

`sc`, `inc`, `dec`, `ch`, `sl st`, `FLO`, `BLO` — every operation the pattern is actually built
from — appear throughout and **none is defined.**

### 🔴 D8 — Three of the five glossary entries are never used

`ch-sp`, `3-st-inc` and `3-st-dec` are defined and never appear in a single round. Only `split-sc`
and `inv-flip` earn their place, and `split-sc` is used exactly once.

### 🔴 D9 — `inv-flip`'s definition doesn't match its use

Defined as *"turn the **work** inside-out through an open neck ring."* Used as *"flip the open
**edge** of Section 3 Round 42 inside-out."* Inverting a whole tube through a ring and flipping a
single open edge before seaming are different manoeuvres, and only the second one is what the
topology needs.

---

## 5. Gauge, dimensions, materials

### 🔴 D10 — The gauge measures a fabric the pattern never makes

> `28 sts × 30 rnds = 4 inches in **split-sc** with 2.25 mm hook`

**`split-sc` appears exactly once in the entire pattern** — in the final assembly join. All 66
rounds are plain `sc`. Waistcoat stitch also runs roughly 10 % denser than sc, so the number is
wrong for the actual fabric as well as measured on the wrong one.

### 🔴 D11 — Both finished dimensions are overstated

| | Claimed | Actual at the stated gauge | |
|---|---|---|---|
| Outer bulb diameter | 4.5 in | 56 sts = 8.00 in around = **2.55 in** | **1.8× over** |
| Total loop length | 11 in | 63 rounds = **8.4 in** | 1.3× over |

### 🔴 D12–D15 — Materials

| | |
|---|---|
| **No tapestry needle** | yet the assembly says *"Whipstitch"* three times |
| **Floral wire / plastic tubing** | listed for "structural tunnel lining" and **never referenced by any instruction** |
| **Stitch markers, "at least 8 distinct colors required"** | **never referenced by any instruction** |
| **No yarn quantities** | neither colour |

### 🔴 D16 — Section 2 never says to save Round 18's back loops

Round 19 is FLO, so the back loops are free — and the matrix depends on them. Section 1 is explicit
about its port; Section 2 is silent about the loops its own assembly needs. (Moot once D5 is fixed,
since the corrected Section 2 has no FLO split.)

### 🔴 D17 — Row 29d's row-end count is unstated

*"sc 2 down row ends"* — there are 3 row-ends on each side of a 3-row short-row block, and the round
never says which side or why only 2.

---

## 6. What is correct — and it is almost all the crochet

- **Section 1, all 25 rounds.** The 8→56 expansion, the port round, the closing round, the neck
  constriction, the open neck tube. **Not one miscount.**
- **Round 8's own self-check** `20 + 16 + 20 = 56` — **exact**, and Round 9 closes over the
  chain-bridge correctly. This is a textbook buttonhole port.
- **Section 2, all 21 rounds.** Including the FLO flange expansion `[inc] × 16 → 32` and the two
  shaping rounds to 48. Arithmetically perfect (the flange's *size* is the problem, not its maths).
- **Section 3 Rounds 26–28, 30–35, 36, 37–42** — all exact. `[sc 2, dec] × 6` on 24 is exact.
- **Short rows 29a, 29b, 29c** — all three balance consumption and production exactly, with the
  nested `skip sl st` structure handled correctly. Only the rejoin fails.
- **The pass-through port geometry works** — a 2.29 in slit admits a 2.29 in shaft with room to
  spare.
- **Using a physical port rather than a true self-intersection is the correct, standard way** to
  crochet a Klein bottle immersion.
- **The `inv-flip` is conceptually right** — an orientation-reversing seam is exactly what converts
  a handle into a cross-handle.
- **Open rings are used correctly** in Section 2 Round 1 and at Section 1 Round 25.
- **Section 3's attachment to Section 1 R25 (24 ↔ 24)** — exact.
- **Both colours are used**; Color A for Sections 1 and 3, Color B for Section 2.

---

## 7. Corrected pattern

[`ouroboros-klein-bottle-CORRECTED.md`](./ouroboros-klein-bottle-CORRECTED.md) — validates with
**0 defects**, and the corrected structure is **genuinely non-orientable**.

| Where | Was | Now |
|---|---|---|
| Sec 2 R1 | `ch 16` open ring | **`ch 32` open ring — this IS the flange edge** |
| Sec 2 R2–3 | *(none)* | `[sc 2, dec] ×8` → 24, `[sc 1, dec] ×8` → 16 |
| Sec 2 R4–18 | R2–18 at 16 | 16 sts, **a true boundary — no FLO split, no branch line** |
| Sec 2 R19–21 | FLO flange to 48 | **deleted** — the flange moved to R1 |
| Sec 3 R29d | 22 sts, stated 24 | full 27-position walk, 3 decs → **(24 sts)** |
| Sec 3 R36 | `[sc 2, dec] ×6` → 18 | `[sc 1, dec] ×8` → **16**, matching Sec 2 R18 |
| Matrix | 3 rows, 0 correct | **2 rows, both verified** |
| Glossary | 7 undefined, 3 dead | all 9 used operations defined, dead entries removed |
| Gauge | in split-sc | in sc |
| Materials | no needle, 2 unused items | needle added, unused items removed |

**The corrected manifold:**

| boundary | resolution |
|---|---|
| Sec 1 R1 | closed magic-ring cap ✔ |
| port (32 positions) | ↔ Sec 2 R1 flange (32) ✔ |
| Sec 3 R42 (16) | ↔ Sec 2 R18 (16), seamed with the inv-flip ✔ |

No free boundary, exactly two sheets at every seam, and one orientation-reversing join.
**Sphere + one cross-handle = Klein bottle.** The classification is earned.

---

## 8. How this was tested

```bash
python reviews/ouroboros-klein-bottle/verify_klein.py           # -> 17 defects
python reviews/ouroboros-klein-bottle/verify_klein.py --fixed   # -> 0 defects
```

`verify_klein.py` adjudicates each topology-matrix row against the actual piece counts, runs a
round-by-round pass over all three sections, computes the short-row perimeter, tests the port's
slit-to-tube geometry, counts sheets per seam to test the manifold claim, and audits the glossary
and gauge.

---

## All eight patterns

| | Bear | Wyvern | Dragon | Leviathan | Chimera | Abomination | Astral | **Ouroboros** |
|---|---|---|---|---|---|---|---|---|
| Hard defects | 5 | 5 | 14 | 12 | 17 | (annotated) | 14 | **17** |
| Rounds checked | 48 | 75 | 93 | 108 | 77 | ~100 | 93 | **66** |
| **Rounds with bad arithmetic** | 5 | 5 | 9 | 7 | 9 | many | 3 | **1** |
| Self-verification shipped | ❌ | ❌ | ❌ | ❌ | ❌ | partial | ✅ 7/9 | ❌ **0/3** |
| All interfaces match | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ |

### The sharpest contrast in the series

**This pattern has the best per-round arithmetic of all eight — 1 bad round in 66 — and the worst
structural claims.** The Astral Leviathan shipped nine self-verification claims and seven held up;
this one ships three and none does.

That is worth naming precisely, because it is the opposite of the failure mode in the first five
patterns. Those got the inside of a piece wrong. This one gets every piece right and then asserts
connections between them that were never computed — a 48-stitch edge that doesn't exist, a seam to a
closed magic ring, and a stitch count (18) that appears nowhere in the piece it names.

**A matrix of interface claims is only worth as much as the derivation behind it.** Three rules
would have caught every one of these:

```
1. every edge cited in an assembly table must be traceable to a round that
   produced it, with its count read off that round — not asserted
2. an edge can only be sewn to if it was left OPEN; a magic ring is not an edge
3. at every seam, count the sheets. Exactly two, or it is not a manifold.
```

Rule 1 alone kills all three matrix rows.
