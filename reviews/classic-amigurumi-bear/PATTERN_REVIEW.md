# Pattern Review — "Classic Amigurumi Bear"

**Verdict: ❌ FAILS — the pattern cannot be crocheted as written.**

| | |
|---|---|
| Pieces checked | 5 (Head & Body, Ears, Muzzle, Arms, Legs) |
| Rounds checked | 31 instruction lines = 48 physical rounds |
| **Blocking math errors** | **5** |
| Structural / technique errors | 8 |
| Materials & documentation errors | 5 |
| Proportion advisories | 3 |
| Pieces that are 100 % correct | Muzzle, Legs |

Three of the five blocking errors are in **Head & Body Rounds 12–13**, and they stop the
project dead: a beginner physically cannot get from Round 12 to Round 13.

---

## 1. Blocking math errors

Notation: `sc` consumes 1 stitch / makes 1. `inc` consumes 1 / makes 2. `dec` consumes 2 / makes 1.
A round is valid only when **stitches consumed = stitches available** *and* **stitches made = the stated count**.

### 🔴 B1 — Head & Body, Round 12: leaves 6 stitches unworked

> `Round 12: [sc 1, dec] 6 times. (12 sts)`

You arrive with **24 sts**. Each `[sc 1, dec]` eats 1 + 2 = **3 sts**, so 6 repeats eat **18**.
That leaves **6 stitches of Round 11 never worked into** — a hole/step in the fabric.
It also cannot produce 12: 6 repeats make 6 × 2 = **12 made from only 18 consumed**, so the round
is simultaneously short and mis-stated.

`[sc 1, dec] × 6` is the standard recipe for **18 → 12**, not 24 → 12. You used it one round too early.

**Fix:** `Round 12: [sc 2, dec] 6 times. (18 sts)` — eats 6 × 4 = **24** ✔, makes 6 × 3 = **18** ✔.

> Standard formula: *(stitches before ÷ number of decreases) − 2 = sc between decreases*.
> 24 → 18 is 6 decreases, 24 ÷ 6 = 4, 4 − 2 = **2 sc between decreases**.

### 🔴 B2 — Head & Body, Round 13: requires more stitches than exist

> `Round 13: [sc 2, inc] 6 times. (30 sts)`

As written you arrive with **12 sts**. Each `[sc 2, inc]` eats 2 + 1 = **3 sts**, so 6 repeats need **18 sts**.
You are **6 stitches short**. The round is impossible — there is nothing left to crochet into.

### 🔴 B3 — Head & Body, Round 13: stated count is wrong by 6 even in the best case

Assume B1 and B2 were fixed and you arrive with 18 sts. `[sc 2, inc] × 6` makes 6 × 4 = **24 sts**,
**not the stated 30**. You cannot jump 18 → 30 (or 12 → 30) in one round; amigurumi shaping moves in
steps of 6 per round.

**Fix (splits Round 13 into two rounds):**
```
Round 13: [sc 2, inc] 6 times. (24 sts)
Round 14: [sc 3, inc] 6 times. (30 sts)
```
Everything after this shifts down by one round number.

### 🔴 B4 — Ears, Round 4: stated count is wrong by 3

> `Round 4: sc in each st around. (12 sts)`

You arrive with **9 sts**. "sc in each st around" makes exactly one stitch per stitch → **9 sts**, not 12.
A plain round can never change the stitch count.

**Fix:** either `Round 4: sc in each st around. (9 sts)` (keeps a small ear), or — if you wanted 12 —
`Round 4: [sc 2, inc] 3 times. (12 sts)`.

### 🔴 B5 — Arms, Round 9: stated count is wrong by 1

> `Round 9: [dec] 3 times, sc 4. (6 sts)`

You arrive with 10 sts. 3 × `dec` eats 6 and makes **3**; `sc 4` eats 4 and makes **4**.
Consumption is correct (6 + 4 = 10 ✔) but production is **3 + 4 = 7 sts**, not the stated 6.

**Fix:** `Round 9: [dec] 5 times. (5 sts)` — even, closes neatly, and mirrors the 5-st magic ring the
arm started from. (`[dec] 4 times, sc 2. (6 sts)` also works if you specifically want 6, but the
decreases bunch on one side.)

---

## 2. Structural & technique errors

### 🟠 S1 — There is no stuffing instruction anywhere
"Stuffing" is in the materials list but the word never appears in the instructions or assembly.
This is not a nicety: **Head & Body is worked in one piece**, so once Round 12 closes the neck the
head can only be reached through the neck opening. The pattern must say *"Stuff the head firmly
before beginning Round 13"* and *"Finish stuffing the body before Round 22"*. Published one-piece
bear patterns always carry these stop-and-stuff notes.

### 🟠 S2 — Never states spiral vs. joined rounds
Every count in this pattern assumes **continuous spiral rounds**, but the pattern never says so.
A beginner reading "Round" will slip-stitch and chain-1 to join each round, which adds a seam and
throws off every count. Needs a note: *"Work in continuous spirals. Do not join or turn. Mark the
first stitch of each round."*

### 🟠 S3 — No stitch marker in the materials list
Mandatory for spiral rounds. Without it a beginner will lose the round start within five rounds.

### 🟠 S4 — Ears Round 1 is not a round
> `Round 1: Ch 4, join with sl st to form a ring.`

This makes **zero stitches**, so it is a setup step, not a round. The consequence is that the ear's
round numbers are **off by one** against every other piece in the pattern — the ear's "Round 4" is
really the 3rd round of fabric. Renumber it as an unnumbered setup line.

### 🟠 S5 — Ears use a chain ring while everything else uses a magic ring
Inconsistent technique in the same pattern, and a `ch-4` ring cannot be cinched shut, so it leaves a
visible hole. Every other piece correctly uses a magic ring. Use a magic ring for the ears too.

### 🟠 S6 — The final opening is never closed
Head & Body Round 22 ends on 6 sts and the pattern just says "Fasten off and weave in ends."
It never tells you to **draw the yarn tail through the remaining 6 stitches and cinch the hole shut**.
A beginner will be left with an open hole in the bear's bottom.

### 🟠 S7 — Neck stability is not addressed
A one-piece head/body pinched to 12 sts at the neck produces a floppy head — the single most common
complaint with this construction. The pattern needs either a firmer-stuffing note at the neck or a
neck-support suggestion.

### 🟠 S8 — Assembly is too vague to follow
> "Sew ears to head. Sew muzzle to front of head. Sew arms and legs to body. Embroider eyes with black yarn."

No round numbers, no stitch spacing, no order of operations. Specifically missing:
- which rounds the ears sit between, and how many stitches apart
- which round the muzzle centres on
- eye placement round and stitch spacing (this is what determines whether the bear looks cute or unsettling)
- the instruction to attach the face **before** the body is stuffed closed
- how many stitches apart the legs sit

---

## 3. Materials & documentation errors

### 🟡 M1 — Black yarn is used but not listed
Assembly says "Embroider eyes with black yarn", but Materials only lists brown.

### 🟡 M2 — `ch` and `sl st` are used but never defined
The abbreviations list defines only `sc`, `inc`, `dec`, `st(s)`. Ears Round 1 uses **`Ch`** and
**`sl st`** — both undefined. For a pattern labelled "Easy / Beginner" that is a real barrier.

### 🟡 M3 — "1 skein" is not a quantity
Skeins run from 50 g to 200 g. Estimated yarn for this bear is **≈ 90–95 g** of worsted, so a 50 g
skein would leave you stranded mid-body. State the grams/yards.

### 🟡 M4 — No finished size, and gauge is waived
"Gauge: Not important" plus no finished measurement means the maker has no idea what they are making
and no way to tell whether their fabric is too loose for stuffing. For amigurumi, gauge does not need
to be exact but it *does* need to be tight — the note should say *"Gauge is not critical, but your
fabric must be dense enough that stuffing does not show through."* Estimated finished height at
4 sts/inch: **≈ 5 inches / 12.5 cm**.

### 🟡 M5 — Round ranges use en-dashes (`–`), not hyphens
`Round 6–10`, `Round 14–18`, `Round 3–8`, `Round 4–8` all use the en-dash character `U+2013`.
This breaks most pattern-parsing software, PDF pipelines and screen readers. It broke this
repository's own markdown parser during testing. Use plain hyphens.

---

## 4. Proportion advisories

These are not arithmetic errors — the pattern would work — but the finished toy will look wrong.
Measured at a realistic amigurumi gauge of 4 sts/inch, 4.5 rounds/inch on a 4.0 mm hook.

### 🔵 P1 — The head and body are exactly the same width
Both peak at **30 sts ≈ 2.4 in diameter**. A classic teddy silhouette wants the head **1.2–1.6×** the
body. At 1.00 you get a peanut/snowman, not a bear. See the optional variant in the corrected pattern.

### 🔵 P2 — The legs are too fat for the body
Each leg is 18 sts ≈ **1.43 in** across. Two side by side = **2.86 in**, which is *wider than the
2.39 in body* they attach to — and the body is tapering at that point. Consider 12–15 st legs, or
widen the body.

### 🔵 P3 — The arms are as long as the torso
Arms run ~2.0 in against a ~2.2 in body section. Dropping the arms to Rounds 3–6 instead of 3–8
gives a more bear-like stance.

---

## 5. What is correct (credit where due)

- **Head & Body Rounds 1–11** — a textbook flat-circle-into-sphere increase sequence. Perfect.
- **Head & Body Rounds 19–22** — the closing decrease sequence is perfect.
- **Muzzle** — all 3 rounds verified correct (6 → 12 → 15, consumption exact).
- **Legs** — all 10 rounds verified correct. The only flawless multi-round piece.
- **Arms Rounds 1–8** — correct.
- **4.0 mm hook with worsted weight** is the right call: tighter than the yarn label's usual
  5.0–5.5 mm, which is exactly what you want so stuffing does not show through.

---

## 6. Corrected pattern

A fully corrected, re-validated version is in
[`classic-amigurumi-bear-CORRECTED.md`](./classic-amigurumi-bear-CORRECTED.md).
It passes both checkers with **0 errors**.

Summary of the seven changes:

| Piece | Round | Was | Now |
|---|---|---|---|
| Head & Body | 12 | `[sc 1, dec] 6 times. (12)` | `[sc 2, dec] 6 times. (18)` |
| Head & Body | 13 | `[sc 2, inc] 6 times. (30)` | `[sc 2, inc] 6 times. (24)` |
| Head & Body | 14 | *(did not exist)* | `[sc 3, inc] 6 times. (30)` |
| Head & Body | 15–23 | rounds 14–22 | renumbered (+1) |
| Ears | 1 | `Ch 4, join with sl st…ring` | unnumbered "Setup: magic ring" — rounds renumbered (−1) |
| Ears | 4 → 3 | `sc in each st around. (12)` | `[sc 2, inc] 3 times. (12)` + a new plain Round 4 |
| Arms | 9 | `[dec] 3 times, sc 4. (6)` | `[dec] 5 times. (5)` |

Plus: black yarn and a stitch marker added to materials, `ch`/`sl st` defined, spiral-rounds note,
stop-and-stuff instructions at the neck and before closing, cinch-the-hole instruction, en-dashes
replaced with hyphens, finished size stated, and a specific assembly section with round numbers.

---

## 7. How this was tested

Four independent passes, so nothing rests on a single tool:

1. **`StitchCountValidator`** (this repo, `src/crochet_checker/validation/stitch_counts.py`) — run per
   piece. Caught B1, B2, B3, B5.
2. **`PatternValidator`** multi-pass compiler (this repo) — run on the whole document and per piece.
3. **An independent verifier written from scratch** (`verify_bear.py`, in this folder) that parses the
   *original* bracket-and-"N times" notation directly, so no finding depends on the repo's parser.
   Caught all five, including **B4, which the repo's validator missed** (it classes plain
   "sc in each st around" rounds as context-dependent and skips them).
4. **Manual cross-check against published amigurumi conventions** — the standard
   *(stitches ÷ decreases) − 2* spacing formula, the "shaping moves in 6s" rule, and the
   stop-and-stuff conventions used in published one-piece bear patterns.

Reproduce:

```bash
python reviews/classic-amigurumi-bear/verify_bear.py           # original  -> 5 defects
python reviews/classic-amigurumi-bear/verify_bear.py --fixed   # corrected -> 0 defects
```

### ⚠️ Note for the repo maintainer

Two tooling problems surfaced while testing, both worth fixing separately:

1. **`crochet-check` CLI is broken.** `src/crochet_checker/cli.py:14` does
   `from .validation import Severity`, but `validation/__init__.py` appends `"Severity"` to `__all__`
   without ever importing it. Every CLI command fails with `ImportError` at startup.
2. **The markdown pattern format is not parsed.** Fed the original `**Round 1:** …` markdown, the
   pipeline reported **PASS with 0 errors** — a false clean bill of health on a pattern with five
   blocking errors. It read the entire document as a single 7-"piece" blob with garbled names and
   extracted no glossary (the backtick-wrapped `` `sc` = single crochet `` form is not recognised).
   Range rounds also produce spurious *"stated 30 stitches but operations produce 1"* errors.
