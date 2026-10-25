# Pattern Review — "Abyssal Leviathan"

**Verdict: ❌ FAILS — 12 defects, and one of them means a whole piece cannot be attached at all.**

| | |
|---|---|
| Pieces checked | 5 (Cranial Vault, Primary Tentacle, Lateral Arm, Body Hub, Dorsal Fin) |
| Rounds / rows checked | 56 instruction lines = 108 physical rounds & rows |
| **Hard defects** | **12** |
| Technique concerns | 5 |
| Missing content | 5 |
| Proportion advisories | 2 |
| Pieces that are 100 % correct | Secondary Lateral Arms; the entire bifurcating fork |

This pattern is the strongest of the four in places and the weakest in others. It **fixed the exact
mistake the Clockwork Dragon made** — the short-row rejoining round here correctly works the raw
row-ends (12 + 3 + 26 + 3 = 44, a perfect perimeter closure). The bifurcating tentacle, with its
ch-2 bridge shared between two branches, is flawless across all 38 rounds. The glossary has **no
undefined abbreviations**.

But the six-limb hub in Round 15 is broken four different ways, and the Primary Tentacle — the
signature piece — **has no opening anywhere on it**.

---

## 1. Hard defects

Cost model: `sc` 1→1, `inc` 1→2, `dec` 2→1, `hdc`/`dc`/`bpdc`/`sl st` 1→1.
A round is valid only when **consumed = available** *and* **produced = stated**.

### 🔴 D1 — Primary Tentacle: the piece has no open end. It cannot be attached.

This is the one that stops the project.

| End of the tentacle | State |
|---|---|
| Round 1 — the base | `magic ring 8 sc` → **pulled closed** |
| Branch Alpha, R29a | `[dec] 4 times` → *"Fasten off and **cinch shut**"* |
| Branch Beta, R30b | `[dec] 3 times` → *"Fasten off and **cinch shut**"* |

Every end is sealed. It is a closed sausage that forks into two closed fingers.

Meanwhile the Body's Round 15 says:

> `sc 4 across inner edge of Primary Tentacle 1 (leaving 8 sts outer)`

That requires an **open ring of 4 + 8 = 12 stitches** to crochet into. There isn't one — and even if
you left the magic ring loose, **the base is only 8 stitches, not 12**. Two independent mismatches:
closed vs. open, and 8 vs. 12.

**Fix:** work the trunk from an open chain ring sized to the socket, and drop the two increase rounds
that are no longer needed:
```
Round 1: With Color A, ch 12, join with sl st to form a ring, careful not to twist.
         Leave this end open - it is the body socket. (12 sts)
Rounds 2-20: sc in each st around. (12 sts)
Round 21 (Fork): sc 6, ch 2, skip 6 sts.  (8 sts)     <- unchanged, still correct
```
Everything from the fork onward already works and needs no change.

### 🔴 D2 — Body Round 15: 20 body stitches are silently dropped

> `sc 4 across Body … sc 4 across Body … sc 12 across Body … sc 4 across Body … sc 4 across Body`

Body stitches worked: 4 + 4 + 12 + 4 + 4 = **28**. Round 14 produced **48**.
The round never says to skip anything. **20 body stitches are neither worked, skipped, nor joined** —
they simply fall out of the pattern, leaving a 20-stitch hole spread around the limb hub.

### 🔴 D3 — Body Round 15: stated count is wrong by 6

Everything the round actually makes:

| Source | Stitches |
|---|---|
| Body | 4 + 4 + 12 + 4 + 4 = 28 |
| 2 Primary Tentacles × 4 | 8 |
| 4 Lateral Arms × 3 | 12 |
| **Total produced** | **48** |
| **Stated** | **54** |

Off by 6.

### 🔴 D4 — Body Round 16 is self-contradictory

> `Round 16: sc in all 54 sts around (working across outer remaining sts of attached limbs). (54 sts)`

Round 15 **explicitly excluded** the limbs' outer stitches — 2 × 8 + 4 × 5 = **36** of them. So either:

- those 36 are still excluded, and the round is the **48** that Round 15 actually made (not 54); or
- Round 16 now works them in, and the round is 48 + 36 = **84** (not 54).

**54 is not reachable under either reading.** A plain "sc around" round cannot add stitches, so the
parenthetical and the number contradict each other.

### 🔴 D5 — Body Round 17 then becomes impossible

> `Round 17: [sc 7, dec] 6 times. (48 sts)`

This consumes 6 × 9 = **54**. Round 15 actually delivers **48**. You are **6 stitches short** and the
round cannot be completed. (This is a consequence of D3, not a separate authoring error — but it is
where the maker actually grinds to a halt.)

### 🔴 D6 — The limb gusset cannot be sewn: 5 to 3, and 8 to 4

> Assembly 4: *"Cinch unworked inner gap stitches of Secondary Arms to Body sockets using yarn tails."*

Each arm leaves **5** outer stitches; each tentacle leaves **8**. For Round 15's own arithmetic to
balance, the body can only skip **3** stitches under each arm and **4** under each tentacle
(3 × 4 + 4 × 2 = 20, exactly the shortfall in D2).

So the gusset asks you to sew a 5-stitch edge to a 3-stitch edge four times, and an 8-stitch edge to
a 4-stitch edge twice. None of them match.

The root cause is that the pattern works the limb's **inner** (body-facing) stitches into the round
and leaves the **outer** ones loose — that is backwards. The outward-facing majority should go into
the round, and the small body-facing remainder is what gets sewn to the skipped body stitches.

**Fix:** invert it and state the skips:
```
Round 15: sc 4 Body, sc 8 across OUTER edge of Tentacle 1 (4 inner sts held), skip 4 Body sts,
          sc 4 Body, sc 5 across OUTER edge of Arm 1 (3 held), skip 3 Body sts,
                     sc 5 across OUTER edge of Arm 2 (3 held), skip 3 Body sts,
          sc 12 Body, sc 5 across OUTER edge of Arm 3 (3 held), skip 3 Body sts,
                      sc 5 across OUTER edge of Arm 4 (3 held), skip 3 Body sts,
          sc 4 Body, sc 8 across OUTER edge of Tentacle 2 (4 held), skip 4 Body sts,
          sc 4 Body. (64 sts)
```
Body: 28 worked + 20 skipped = 48 ✔  Made: 28 + 16 + 20 = 64 ✔  Gusset: 20 held limb sts ↔ 20
skipped body sts ✔ — every one pairs off.

### 🔴 D7 — Cranial Round 19: 2 stitches left unworked

> `Round 19: [sc 5, dec] 6 times. (36 sts)`

From 44 sts: consumes 6 × 7 = **42**, leaving **2 unworked**. (The stated 36 happens to be right,
which is why this one is easy to miss.)

**Fix:** `[sc 4, dec] 4 times, [sc 3, dec] 4 times. (36 sts)` — consumes 44 ✔, makes 36 ✔.

### 🔴 D8 — Cranial Round 15: the ridge stitch is the wrong one

> Heading: *"Bio-Luminescent Ridge (**Front Post** Alignment)"*
> Instruction: `[sc 5, **bpdc** 1 in previous round] 7 times`

`bpdc` is a **back** post double crochet. The heading says front post. They are opposites, and the
difference is not cosmetic: a back post stitch pushes the raised ridge **to the inside of the work**.
Worked in the round with the right side out, this bio-luminescent ridge ends up buried inside the
stuffed cranial vault where nobody will ever see it.

**Fix:** `fpdc` — and add it to the glossary, which currently defines only `bpdc`.

### 🔴 D9 — Cranial Round 15: the post stitch has nothing to grip

Round 14 is a round of **sc**. A double-crochet post stitch has to wrap around the post of the stitch
below, and standard references are explicit that you need a row of taller stitches to do that — dc is
the normal choice [1](https://www.hanjancrochet.com/front-post-and-back-post-double-crochet/)[2](https://hearthookhome.com/crochet-front-post-and-back-post-crochet-stitches/),
and post stitches into sc are rare precisely because the post is too short [3](https://www.marymaxim.com/blogs/beginner-crochet/how-to-front-post-double-crochet-for-advanced-beginners).

It is compounded by `Switch to Color B in FLO` in the same breath — see T1 below.

**Fix:** make Round 14 the last plain round an `hdc` round so Round 15 has a real post to work around.

### 🔴 D10 — Dorsal Fin Row 4: two errors

> `Row 4: Ch 1, FLO sc 15, inc, turn. (18 sts)`

From 17 sts: consumes 15 + 1 = **16**, leaving **1 unworked**, and makes 15 + 2 = **17**, not 18.

**Fix:** `FLO sc 16, inc` — consumes 17 ✔, makes 18 ✔.

> This is character-for-character the same error as the Clockwork Dragon's Wing Row 4
> (`FLO sc 12, inc` on 14 sts). Same shape, same row number, same piece type.

### 🔴 D11 — Dorsal Fin Row 6: the webbing is 5.4× too full

> `Row 6: Working down raw row ends: [sl st, hdc, dc, hdc, sl st] into each row end across. (25 sts)`

The count is self-consistent (5 sts × 5 row ends = 25 ✔ — better than the Wyvern managed). The
geometry is not:

| | |
|---|---|
| edge available | 5 rows ÷ 6.5 rows/in = **0.77 in** |
| edging worked | 25 sts ÷ 6 sts/in = **4.17 in** |
| fullness | **5.4×** |
| typical shell/webbing edging | 2 – 2.5× |

At **5 stitches per row end** with no anchoring stitch between fans, this will not read as fin
webbing — it will bunch into a tight frill.

### 🔴 D12 — Assembly 3: the fin is twice as long as the span it is sewn to

> *"Sew Dorsal Fin Sail foundation row (Row 1, 20 sts) to back of Body across Rounds 8–18."*

Fin foundation: 20 sts ÷ 6 sts/in = **3.33 in**.
Body Rounds 8–18: 11 rounds ÷ 6.5 rounds/in = **1.69 in**.

The fin is **2.0× too long** for the span it is assigned to. You cannot ease in 100 % excess; it
would have to be gathered into a ruffle down the spine.

**Fix:** sew across Rounds 6–26 instead (21 rounds = 3.23 in, a 1.03 ratio).

---

## 2. Technique concerns

### 🟠 T1 — "Switch to Color B in FLO" on a post-stitch round
A post stitch does not enter the top loops at all — it wraps the post. So "in FLO" cannot apply to
the `bpdc`, and the pattern never says whether the five `sc` between posts are FLO or both loops.
Combining FLO with post stitches in one round needs spelling out or dropping.

### 🟠 T2 — The Primary Tentacles and Lateral Arms are never stuffed
The tentacles are crocheted into the body at Round 15 and sealed at both branch tips, so there is no
later opportunity at all. With 1.5 mm wire running through them the maker will probably guess, but
the pattern should say so and say *when*.

### 🟠 T3 — The craft wire is never secured
Assembly 1 inserts 1.5 mm wire and then nothing. There is no instruction to bend the ends into loops,
cap them, or bind them — and no warning that the piece is therefore not a child's toy. Exposed wire
ends will work their way through fingering-weight fabric.

### 🟠 T4 — The spiral instruction covers one piece out of five
"continuous spiral" appears once, in the Cranial Vault heading. The Tentacles, Arms and Body never
say, and Branch Beta ("attach Color A to the 6 skipped sts") is exactly the kind of place where a
maker needs to know whether to join.

### 🟠 T5 — Fingering on a 3.0 mm hook is at the loose end for amigurumi
24 sts / 4 in is within the standard range for fingering, but it is the *open* end of it. With three
dark colours (midnight blue, teal, deep purple) over white polyfill, the stuffing may ghost through.
Worth a note recommending dark stuffing or a lining, or dropping to a 2.75 mm hook.

---

## 3. Missing content

### 🟡 M1 — The 14 mm safety eyes are never placed
Listed in materials. The word *eye* appears **nowhere else in the pattern** — not in the Cranial
Vault section, not in assembly. The leviathan has no face.
*(This is now the second pattern in a row with this exact omission.)*
The size itself is well judged: 14 mm on a 57 mm head is 25 %.

### 🟡 M2 — No yarn quantities
Three colours, no grams or yards for any.

### 🟡 M3 — No finished size
It works out to roughly **9 in / 23 cm** body-and-head, plus tentacles.

### 🟡 M4 — "Leave 2-inch tail for attachment" is too short
Four arms, each gusseted to the body. A 2 in tail will not survive threading a needle and sewing a
3-stitch seam. 8–10 in is realistic.

### 🟡 M5 — Row 6 doesn't say which row-end edge
The fin has two. One of them is the shaped/decreasing side; the other is straight. The webbing
belongs on one specific edge and the pattern doesn't say which.

---

## 4. Proportion advisories

### 🔵 P1 — The fin is a strip
3.33 in × **0.77 in** — a 4.3 : 1 ribbon against a 3.85 in tall body. For a piece named a
"Dorsal Fin **Sail**" it should be substantially deeper. The corrected pattern takes it to 12 rows
(1.85 in), which also gives the webbing enough row ends to be spaced properly.

### 🔵 P2 — The lateral arms are very fine
8 sts = **0.42 in** diameter over 2.31 in of length. In fingering weight that is a 10 mm noodle —
correct for a deep-sea creature, but they will need the wire to hold any shape, and the pattern only
wires the *primary* tentacles.

---

## 5. What is correct — and some of it is excellent

- **The short-row rejoining round (Cranial R18).** `sc 12 across Row 17c, sc 3 down raw row-end edge,
  sc 26 across unworked Round 16 sts, sc 3 up raw row-end edge` = **44**, and the true perimeter is
  12 + 26 + (3 × 2) = **44**. Every position accounted for. **This is precisely what the Clockwork
  Dragon got wrong**, and it is handled perfectly here.
- **The entire bifurcating tentacle — 38 rounds, not one error.** The fork round consumes all 12
  stitches (6 worked + 6 skipped) and hands 8 to each branch via a shared ch-2 bridge; Branch Alpha
  takes the bridge's top and Branch Beta its underside; both branches and all four closing rounds
  balance exactly. This is genuinely advanced construction, executed correctly.
- **Secondary Lateral Arms** — all 15 rounds exact, and the 8-stitch open end matches the body
  socket's 3 + 5 exactly.
- **Cranial Vault Rounds 1–18 and 20–22** — exact, including the short-row block itself.
- **Body Rounds 1–14 and 17–25** — exact. The closing sequence 48→42→36→30→24→18 is textbook.
- **Dorsal Fin Rows 1, 2, 3, 5** — exact, including `ch 21 → 20 sc`.
- **Fin Row 6's stitch count is self-consistent** (25 = 5 × 5) — the Wyvern's equivalent round wasn't.
- **The glossary has no undefined abbreviations.** All ten are defined; `sc inc dec hdc dc bpdc ch
  sl st BLO FLO` are all genuinely used.
- **Cranial R22 (18 sts) ↔ Body R25 (18 sts)** — the head-to-body interface matches exactly.
- **Gauge is stated in rounds**, correct for a piece worked almost entirely in the round.

---

## 6. Corrected pattern

[`abyssal-leviathan-CORRECTED.md`](./abyssal-leviathan-CORRECTED.md) — validates with **0 defects**.

| Piece | Where | Was | Now |
|---|---|---|---|
| Tentacle | R1–R13 | magic ring 8, inc to 12 | **`ch 12` open ring**, straight 12-st trunk |
| Cranial | R15 | `bpdc` after an sc round | `fpdc` after an **hdc** round |
| Cranial | R19 | `[sc 5, dec] x6` | `[sc 4, dec] x4, [sc 3, dec] x4` |
| Body | R15 | inner edges worked, 20 sts dropped, (54) | **outer** edges worked, skips stated, **(64)** |
| Body | R16–18 | contradictory | `sc around (64)`, then 64→56→48 |
| Fin | Row 4 | `FLO sc 15, inc (18)` | `FLO sc 16, inc (18)` |
| Fin | Rows 6–12 | *(fin ended at 5 rows)* | extended to 12 rows |
| Fin | edging | 5 sts into every row end | fan every 2 row ends → 2.2× fullness |
| Assembly | 3 | Rounds 8–18 | Rounds 6–26 (matches the 3.33 in edge) |

Plus: eye placement, stuffing for tentacles and arms, wire-end securing and a safety note, a global
spiral note, yarn quantities, finished size, and longer attachment tails.

---

## 7. How this was tested

1. **`StitchCountValidator`** (this repo) per piece — caught **D7** and pointed at Body R15. 1 of 12.
2. **`PatternValidator`** multi-pass compiler (this repo).
3. **An independent verifier written from scratch** (`verify_leviathan.py`) modelling short-row
   perimeters, the bifurcating fork with its shared bridge, the six-limb hub with separate
   worked/skipped/held accounting, tentacle end-state (open vs. cinched), and edging fullness.
   It caught all 12 — including **D1, D2, D4, D6, D11 and D12, which no stitch-count engine can see
   because they are geometry and cross-piece consistency, not arithmetic.**
4. **External verification** of the post-stitch claim (D9) against three crochet references.
5. **Gauge-based geometry** for every dimensional claim.

```bash
python reviews/abyssal-leviathan/verify_leviathan.py           # -> 12 defects
python reviews/abyssal-leviathan/verify_leviathan.py --fixed   # -> 0 defects
```

The verifier deliberately treats Row 17a as a **legitimate** short row rather than 26 orphaned
stitches — a naive "consumed ≠ available" rule reports a false positive there.

---

## All four patterns

| | Bear | Wyvern | Dragon | Leviathan |
|---|---|---|---|---|
| Level claimed | Beginner | Advanced | Master | Grandmaster |
| Hard defects | 5 | 5 | 14 | **12** |
| Rounds checked | 48 | 75 | 93 | **108** |
| Defect rate | 10 % | 7 % | 15 % | **11 %** |
| Glossary complete | ❌ | ✅ | ❌ | ✅ |
| Eyes placed | ✅ | ✅ | ❌ | ❌ |
| Head↔body interface | n/a | ✅ | ❌ | ✅ |
| Short-row rejoin | n/a | n/a | ❌ | ✅ |
| A piece that can't attach | ❌ wings | ❌ wings | ❌ wings | ❌ **tentacles** |

**The recurring pattern across all four is the limb-to-body join.** Every single one of these
patterns gets its main body tube right and then fails where two pieces meet: the bear had no join at
all, the wyvern abandoned 6 body stitches, the dragon sewed 3 stitches to 4, and the leviathan drops
20 body stitches *and* builds a tentacle with no opening. The arithmetic inside a piece is
consistently good; the arithmetic *between* pieces is consistently not checked.

If the designer adopts one habit, it should be this: **for every join, write down three numbers —
stitches worked into the round, stitches skipped on the body, stitches held on the limb — and
confirm that (worked + skipped) equals the body's previous round, and that (held) equals (skipped).**
That single check would have caught 9 of the 36 defects found across these four patterns, including
every one of the show-stoppers.
