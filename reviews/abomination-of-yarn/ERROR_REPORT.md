# Error Report — "The Abomination of Yarn"

**This one is different.** It arrives pre-annotated with its own error markers — 23 explicit
`← ERROR` flags plus roughly 45 parenthetical notes. Simply re-listing them back would be worthless.

So the job here is to **audit the annotations**. Every claim below was computed, not asserted.

| | |
|---|---|
| Annotations spot-checked and **confirmed** | 6 (representative sample) |
| Confirmed but **incomplete** — understate the error | 2 |
| Annotations that are **themselves false** | **9** |
| Defects the annotations **missed entirely** | **19** |
| Rows/rounds with no stitch count at all | 18 |
| Rows/rounds with an *approximate* count | 3 |

**Headline: 9 of the pattern's own error markers are wrong, and it missed 19 real defects.**
Two of the things it flags as errors are perfectly correct crochet.

---

## 1. Nine annotations that are themselves false

### ❌ F1 — "9mm safety eyes (×3) — *pattern is for a 2-piece flat blanket, eyes are never used*"

Wrong twice.

- **Assembly step 7 literally says** *"Attach safety eyes to Piece A between Rnds 8–9."* They are used.
- It is not a 2-piece flat blanket. There are five lettered pieces, and with the multipliers
  (A ×2, B ×2, C ×1, D ×4, E ×1) that is **ten physical pieces**.

*The real eye defect, which the annotation misses:* 3 eyes across Piece A ×2 is an odd number that
cannot divide between two identical pieces.

### ❌ F2 — Piece A: "*(Make 2, but instructions say "Make 1" later)*"

Unsupported. The string **"Make 1" appears exactly once in the entire pattern — on Piece C.**
Nothing anywhere tells you to make a single Piece A, and Assembly step 1 says "Piece A (×2)",
which agrees with the heading. There is no contradiction to find.

### ❌ F3 — Piece A Rnd 12: "*switching from rows to rounds on flat piece*"

**Not an error.** Working a perimeter/edging round around a finished flat panel is completely
standard crochet — it is how you border a blanket square. Calling this a defect is a false positive.

The genuine faults in that line are the undefined "evenly" and the count — see D5 below.

### ❌ F4 — Piece A: "*seaming to Piece F Row 44 (Piece F only has 30 rows)*"

Mischaracterised. **There is no Piece F.** The pattern contains A, B, C, D and E. The annotation
implies Piece F exists and merely has too few rows; the actual defect is a **dangling reference to a
piece that was never written** — a considerably worse problem, and a different one.

### ❌ F5 — Piece B Rnd 4–6: "*ERROR: no increases but rnds listed*"

**Not an error.** `Sc in each st around. (18 sc)` worked on 18 stitches produces 18 stitches.
Straight rounds between shaping rounds are normal and structurally necessary — they are what gives
a sleeve its length. This is one of the few rounds in the whole pattern that is entirely correct,
and it has been flagged as broken.

### ❌ F6 — Piece C assembly note: "*Piece D is a flat square — it has no "Rnd 22"*"

Wrong twice.

- Piece D is **not a square**. It is worked in rounds from a ch-4 ring, and the pattern's own
  Rnd 31 annotation calls it *"a circle."* The two annotations contradict each other.
- Piece D **does have a Rnd 22** — it falls inside `Rnd 6–30: Rep Rnds 2–5`.

*The real defect:* Rnd 22 lands mid-repeat-cycle, so which of the four sub-rounds it means is
undefined.

### ❌ F7 — Piece B Rnd 14–30: "*12 + 17×6 = 114 sts*"

**The annotation's own arithmetic is wrong.** It treats Rnd 3 as additive (+6 per round). Rnd 3 is
`*sc in next st, inc; rep around` — a **×1.5 multiplier**.

Starting from Rnd 13's 28 stitches (4 ch-5 spaces × 7):

| After n repeats | 0 | 1 | 2 | 3 | … | 17 |
|---|---|---|---|---|---|---|
| stitches | 28 | 42 | 63 | 94 | … | **27,310** |

That is **about 240× the annotation's figure.** And it breaks sooner than either number suggests:
**63 is odd**, so a two-stitch repeat cannot complete the round on the third iteration.

### ❌ F8 — Piece D: "*(Make 4, but diagram shows 2)*"

Unsupported. **There is no diagram anywhere in the pattern.** Assembly step 4 says "Piece D (×4)",
agreeing with the heading.

### ❌ F9 — Piece B Rnd 12: "*'sk 3 sts' with 15 sts and sc between creates math chaos*"

**Rnd 12 is correct.** Its consumption is `1 (opening sc) + 4n + 3 (final skip)` = 4 + 4n.

| Available | n | Result |
|---|---|---|
| 15 (as Rnd 11 states) | 2.75 | fails |
| **16 (what Rnd 11 actually makes)** | **3** | **divides exactly — four ch-5 loops, round closes** |

The chaos is **inherited from Rnd 11's miscount, not created here.** Fix Rnd 11 and Rnd 12 works
perfectly. Flagging Rnd 12 sends you to repair a round that isn't broken.

---

## 2. Nineteen defects the annotations missed

### Materials and abbreviations

| # | Defect |
|---|---|
| **M1** | **The 5.0mm hook the gauge section requires is not in the materials list.** Only 3.5mm and 6mm are listed. The annotation notes the hook *mismatch* but never that the hook is missing entirely. |
| **M2** | **Fiberfill is never listed**, yet Assembly step 8 says "Stuff firmly with fiberfill." |
| **M3** | **"Stitch markers (7)" are listed and `pm` is defined — but `pm` is never used anywhere.** Both the tool and its abbreviation are dead. |
| **M4** | **3 safety eyes across Piece A (×2)** — an odd number that cannot divide between two identical pieces. |
| **M5** | **The abbreviation table has lost every delimiter.** It reads `AbbrMeaning scsingle crochet (US) dcdouble crochet…` — unparseable as printed, by human or machine. |
| **M6** | **`CL` has a *third* definition the annotations miss.** The table says "**5 tr** CL in Piece B"; Piece B Rnd 8 says "this is now a **5-dc** CL". So CL means 3-dc (A), 5-tr (table), and 5-dc (body). The annotations flag only two. |
| **M7** | **`BPdc` is defined but never used** anywhere in the pattern. |

### Piece A

| # | Defect |
|---|---|
| **M8** | **Rows 5–7 carry no stitch count at all.** Three consecutive rows, no counts. |
| **M9** | **Row 11 works "in FLO of Row 9", which had 61 sts** — that is 61 puffs, not the stated 41. |
| **M10** | **Rows 14–20 repeat Rows 2–8, but Row 8 references "each dc from Row 4."** Repeated at Row 20, does that mean Row 4 or Row 16? Undefined. |

### Piece C

| # | Defect |
|---|---|
| **M11** | **The UK note covers `dc` only — `tr` is left ambiguous.** UK tr = US dc, so every `tr` in Rows 3 and 10 has two readings. The annotations chase the `dc`/`sc` ambiguity and never notice `tr`. |
| **M12** | **Row 1's stated 86 is itself the evidence.** 86 only works under **US** dc with ch-3 counting as a stitch. Under the piece's own UK rule it should be **85**. The count proves the row was written in US terms and relabelled afterwards. |
| **M13** | **Row 10 doesn't divide either.** Its repeat consumes 5 sts (sk 4 + sc 1); after the opening sc and the last 3 sts, ~76 remain, and 76/5 = 15.2. The annotation flags only the US/UK question. |

### Pieces D and E

| # | Defect |
|---|---|
| **M14** | **"Rnd 6–30: Rep Rnds 2–5" fails on the *first* iteration, not just the last.** Rnd 2 is "8 sc **in ring**" and after Rnd 5 there is no ring to work into. The annotation only objects that 25 ÷ 4 = 6.25. |
| **M15** | **Piece E Rnd 2's repeat needs a ch-2 space after every 6 dc**, but Rnd 1 places ch-2 spaces at the **4 corners only**. The repeat runs out of spaces immediately. |
| **M16** | **"Join at the bottom-right corner of assembled Pieces A+B+C+D"** — Piece B is a tube worked from a magic circle. It has no corner and no flat edge to join along. |

### Assembly

| # | Defect |
|---|---|
| **M17** | **Step 7's safety eyes are attached at the wrong time.** A safety eye needs rear access to seat its washer and must go in before the piece is closed. By step 7, Piece A's Rows 8–9 are buried under the Piece E border. |
| **M18** | **Step 4 is worse than noted.** Beyond the duplicate Row 10, **Row 12 is the perimeter round** and **Rows 14/16 are inside the "Rep Rows 2–8" block**. Three of the four attachment points are undefined, not one. |
| **M19** | **Partial credit the annotations withhold.** The duplicate Row 10 ("sc in BLO of each st") followed by Row 11 ("working in FLO of Row 9") is a **legitimate FLO/BLO split** — two fabrics grown off one row. Row 10 takes the back loops, leaving the front loops free for Row 11. It is the only structurally sound technique in Piece A, and it is buried under an error flag. |

---

## 3. Sample of annotations confirmed — with the numbers filled in

These hold up. Where the annotation stops short, the precise figure is added.

| Location | Annotation | Verified |
|---|---|---|
| **A Row 1** | "should be 41 sc" | ✅ ch 42, skip 1 → **41**. Stated 44 is 3 too high. |
| **A Row 3** | "repeat unit is 9, doesn't divide 41" | ✅ unit consumes exactly 9. 41/9 = 4.56; 4 reps consume 36, leaving **5 unworked**. ⚠️ *Incomplete:* they produce **32 sts**, not the stated 46 — never stated. |
| **A Row 9** | "repeat math doesn't match" | ✅ consumes 45 of 58 → **13 orphaned**. ⚠️ *Incomplete:* it also **produces 63, not the stated 61**. |
| **A Row 10 (1st)** | "count mismatch" | ✅ consumption is 7 + 8n; 7 + 8n = 61 gives n = 6.75. Best case consumes 55 and produces **43** against a stated 59. |
| **A Rnd 12** | "count is arbitrary" | ✅ a 41-st × 12-row panel has a perimeter of ~**114** sc. Stated 172 is **51 % over the ceiling**. |
| **B Rnd 11** | "should be 16, not 15" | ✅ 20/5 = 4 reps → **16**. |

The repo's own `StitchCountValidator` independently reproduced A-R1 (44 vs 41) and B-R11 (15 vs 16)
from the machine-readable fragments.

---

## 4. Putting numbers on the "arbitrary" figures

**Assembly step 6 — "Weave in all 847 ends"**

| Source | Ends |
|---|---|
| Piece A ×2 (Yarn A) | 4 |
| Piece A ×2 (Yarn B at Rnd 12) | 4 |
| Piece B ×2 (Yarn C) | 4 |
| Piece C (Yarn B) | 2 |
| Piece D ×4 (Yarn E) | 8 |
| Piece E (Yarn A + B held) | 4 |
| **Realistic total** | **26** |

847 is **33× too many.**

**Piece D — "Block to 8″ × 8″ square"**
A 12-sc circle at 3.5 sc/in is 3.43 in around = **1.09 in across**. Blocking that to 8 × 8 in is
**7.3× linear and 68× the area** — and a circle has no corners to block into.

**Gauge — "22 dc and 10 rows = 4″ using Yarn C on a 3.5mm hook"**
That is **5.5 dc per inch in bulky #5 yarn**. A bulky dc is roughly 0.5 in wide, so ~2/in is
realistic — about **2.8× too dense**. Bulky #5 is rated for 6.5–9mm hooks; 3.5mm is far below the
yarn's range. And the only Yarn C piece (Piece B) uses the **6mm** hook — so this gauge describes a
yarn/hook pairing that **appears nowhere in the pattern.**

**Finished size — "60″ × 80″"**
Piece A at the stated Yarn A gauge is 11.7 in wide × 5.2 in tall; two side by side is **23.4 in**
wide. The annotation's "23 in" checks out. Against a claimed 60 × 80, that is roughly **39× the
achievable area**.

---

## 5. Why there is no corrected pattern in this folder

The other five reviews each ship a corrected pattern that validates clean. This one does not, and
deliberately.

A correction needs a design intent to correct *toward*. This pattern has none — it ends
*"Enjoy your finished **Amigurumi Blanket Sweater Hat**,"* four mutually exclusive garment
categories, and the materials, gauge and assembly each describe a different object (a 60×80 blanket,
a stuffed toy with eyes, and a sweater with sleeves and a neckline). There is no single artefact to
repair it into. Producing one would mean writing a new pattern and calling it a fix.

What is actionable is the list above: **9 false flags to remove, 19 real defects to add, and 2
annotations to sharpen.**

---

## 6. What this reveals about the checker

Run against this pattern, the repo's tooling is mostly blind — and the reason is instructive.

| Obstacle | Count | Can a stitch-count engine see it? |
|---|---|---|
| Rows/rounds with **no stitch count** | 18 | No — nothing to check against |
| **Approximate** counts ("approximately 80", "~400 sc") | 3 | No — no exact value exists |
| **Duplicate row numbers** | 1 | No — the parser silently keeps one |
| **Empty rows** (Piece C Row 12: "Turn.") | 1 | No |
| **Unbounded repeats** (Piece E "Rnd 5–∞") | 1 | No — non-terminating |
| **Cross-piece row references** (A→F, C→A R2, E→C R2) | 3 | No — requires a symbol table |
| **References to things that don't exist** (Piece F, Yarn E) | 2 | No — requires a symbol table |
| **Terminology mode switches** (US→UK mid-pattern) | 1 | No — requires a dialect flag |
| **Abbreviation redefinition** (CL ×3, puff ×2, mc ×2) | 3 | No — requires scoped definitions |

That is the useful finding for the checker itself: **the failures that make this pattern unusable are
almost all *referential*, not arithmetic.** Dangling piece references, redefined abbreviations,
duplicate labels, missing materials, unbounded loops. A stitch-count validator cannot reach any of
them.

If the goal is to catch patterns like this, the highest-value additions would be, in order:

1. **A symbol table** — every piece, yarn, hook, row and round declared once; flag every reference
   to an undeclared symbol (catches Piece F, Yarn E, the 5.0mm hook, Rnd 22, the duplicate Row 10).
2. **Scoped abbreviation definitions** — flag any abbreviation redefined after first use, and any
   defined-but-unused entry (catches CL ×3, puff ×2, mc ×2, BPdc, pm).
3. **A completeness pass** — flag any row with no count, an approximate count, or no instruction.
4. **A terminology-dialect flag** — one declared mode per pattern, error on any switch.
5. **Termination checking** — reject any repeat without a bound.

None of these needs stitch arithmetic. All five are cheap. Together they would have caught
**about three quarters** of what is actually wrong with this document.

---

## Reproduce

```bash
python reviews/abomination-of-yarn/audit_annotations.py
```
