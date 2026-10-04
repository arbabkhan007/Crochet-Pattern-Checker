# NS 14 — Bobble Snowflake Tree Skirt · Check Report

**Checked:** 2026-10-04 · `crochet-check` v1.0.0 · Novality Crochet Studio, printer-saver edition

---

## Verdict

**The stitch mathematics are clean.** All 32 growth rounds, all three size stop-points and all three
borders reconcile exactly. I found **no stitch-count error**.

| Size | Growth rounds | Final count | Border scallops | Checker verdict |
|---|---|---|---|---|
| Mini / tabletop | R1–R14 | 168 | 28 | PASS 100/100 |
| Standard | R1–R23 | 276 | 46 | PASS 100/100 |
| Large | R1–R32 | 384 | 64 | PASS 100/100 |

> Those PASS results are after neutralizing one hardcoded checker rule that misfires on this
> construction — see *False positive* below. Unmodified, the tool reports `ERROR` on R2 for all
> three sizes, and that report is wrong.

**A PASS here means the written checks found nothing.** Nothing was crocheted, no photo was read,
no gauge swatch was measured, and no finished skirt was fitted to a stand.

---

## What verified clean

**Stitch ladder — 32/32 rounds, zero mismatches.** The pattern's own rule (*Round N consumes N−1 old
stitches and produces N new stitches in each of 12 repeats, ending at 12 × N*) holds for every single
round. Each round consumes exactly the previous round's total — no stitches left unworked anywhere,
and every printed count equals 12 × N.

**The R11→R12 worked example is correct, including its counterfactual.** R11 consumes 10 and makes 11
(132); R12 consumes 11 and makes 12 (144). The claim that using 9 plain dc "would leave 12 old stitches
unworked and produce only 132" is arithmetically exact. This is the round most likely to be miscounted
by hand, and the pattern pre-empts it correctly.

**Border closes exactly at all three sizes.** Each repeat consumes 6 anchors and produces 6 worked
stitches (1 sc + 5-dc shell), so worked total = anchor total. 168/6 = 28, 276/6 = 46, 384/6 = 64 —
all exact, no partial shell.

**Bobble loop count is right.** Five incomplete dc legs leave exactly six loops on the hook
(1 working + 5), closed with one pull-through. "Repeat four more times" = 5 legs total. Consistent.

**Bobble placement is consistent.** R5, 8, 11, 14, 17, 20, 23, 26, 29, 32 — every third round with no
gaps, and all three size stop-points land on a bobble round. That's deliberate and it works.

**12 increases per round is the correct rate for a dc circle** (not 6 — that's the sc rule). The
geometry is sound.

**Hook sizes check out against the Craft Yarn Council tables** in this repo: H-8 = 5.0 mm,
I-9 = 5.5 mm. The pattern's "5–5.5 mm (US H/8–I/9)" is exact.

**US/UK translation is correct throughout.** dc→tr, sc→dc, 5-dc bobble→5-tr bobble. I checked every
round pair and the border; counts are identical on both sides, as claimed.

**Diameter arithmetic is correct.** 168/3 = 56 in → 17.8 in; 276/3 = 92 → 29.3 in; 384/3 = 128 → 40.7 in.
All three match, and the cm conversions are right.

---

## Findings worth your attention

### 1. The two gauge targets are ~5% inconsistent with each other — the only genuine technical issue

The pattern asks you to match **both** 12 sts = 4 in **and** 6 rounds = 4 in radially, and says
"Match both measures."

For a flat circle growing by 12 stitches per round at 3 sts/in, the radius can only grow by
12 ÷ 3 ÷ 2π = **0.637 in per round**. The stated round gauge demands 4 ÷ 6 = **0.667 in per round** —
**4.7% more radius than the circumference can support.**

A maker who hits both targets exactly would be adding radius slightly faster than stitches allow,
which tends toward **cupping**. Notably, the Troubleshooting section already has an entry for cupping.

The internally consistent round gauge would be **6 rounds ≈ 3.8 in / 9.7 cm**, not 4 in / 10 cm.

This is within blocking tolerance and the pattern does say to measure a sample — but as written the
two targets cannot both be met on a flat circle.

### 2. The "large" lower bound of 38 in is unreachable at gauge

At the stated gauge the unbordered R32 circle is already **40.7 in**, and the border only adds more.
The advertised 38–43 in band has a floor the skirt can never hit if gauge is met. Effectively it's a
41–43+ in skirt.

Conversely the **mini** floor is tight the other way: unbordered R14 is 17.8 in against an
18–21 in target, so the border has to contribute at least 0.2 in of diameter to reach the floor.
Achievable, but it's the border doing the work, not the body.

### 3. The 700–1,200 g yarn allowance looks high

My rough per-stitch cross-check (including bobbles, border and the 12 surface spokes):

| Size | Estimated yarn |
|---|---|
| Mini (R14) | ~220–270 yd · ~120–150 g |
| Standard (R23) | ~520–640 yd · ~280–350 g |
| Large (R32) | ~950–1,150 yd · ~510–625 g |

The stated "700–1,200 g for a standard or large skirt" sits **well above** my standard-size estimate
and **above** my large-size estimate. A maker buying to the top of that range could over-buy
substantially.

To the pattern's credit, it explicitly labels this allowance unmeasured and tells you to weigh a
sample first. My numbers are a rough model, not a weighing — but the gap is large enough to test
before buying.

### 4. `crochet-check measure` disagrees with the pattern, and the pattern is right

The tool reports ~28.9 in across for the full 32 rounds. That uses the tool's **built-in default
gauge (~4.2 sts/in)**, not this pattern's 3 sts/in. At the pattern's own stated gauge, 40.7 in is
correct. Ignore the tool's figure here.

---

## False positive — the checker is wrong, the pattern is right

Unmodified, the checker reports on every size:

```
ERROR  Round 2: 12 stitches jump to 24. Insert an 18-stitch round before returning to 24.
```

**Disregard this.** It comes from `NeckJumpChecker` in `validation/audit_rules.py`, which is
hardcoded to fire on *exactly* the 12→24 pair:

```python
if previous != 12 or produced != 24:
    continue
```

It's an amigurumi heuristic for a neck widening too fast in single crochet. It has no awareness of
stitch type or construction. I confirmed it's a literal constant match:

| Round 1 → Round 2 | Rule fires? |
|---|---|
| 10 dc → 20 (doubling) | no |
| **12 dc → 24 (doubling)** | **yes** |
| 14 dc → 28 (doubling) | no |

So the rule doesn't object to doubling in general — the repo's own PASS example doubles 6→12 in R2.
It objects only to the literal number 12 becoming 24.

**"2 dc in each st around" from 12 to 24 is the textbook round 2 of every double-crochet flat circle.**
It is correct here. Inserting an 18-stitch round, as the message suggests, would break the 12-repeat
structure, the 12 × N ladder, and the border's divisibility by 6.

---

## Parser limitations — not pattern faults

Running the raw PDF text produced ~25 bogus count errors and dozens of "undefined abbreviation"
complaints. That output is noise. The parser could not read:

- **`[...]` repeats containing "dc in next N sts"** — inside a bracket repeat this collapses to 1
  stitch instead of N. (Standalone it parses fine; the repeat-unit path uses a simpler rule.)
- **`2 dc in each st around`** — read as 2 stitches total rather than a doubling to 24.
- **`BO`** — the custom bobble abbreviation isn't in the glossary.
- **Prose glued onto round lines** — the size notes and the R11→R12 explanatory paragraph were parsed
  as if they were rounds, inventing phantom rounds 11, 14, 23 and 32.

To get a real result I translated the pattern into the checker's native idiom, preserving every
stated count verbatim:

- `[dc in next N sts, 2 dc in next st] x 12` → `(N dc, inc) x 12`
- `[BO in next st, dc in next N sts, 2 dc in next st] x 12` → `((N+1) dc, inc) x 12`
- `2 dc in each st around` → `inc in each st around`

Reading **BO as a dc is sound for counting**: a bobble consumes one stitch and produces one stitch,
exactly like a dc. The pattern's own abbreviation list says "counts as 1 stitch." This translation
changes no count — and because I verified the arithmetic by hand independently first, it isn't
quietly fixing anything.

---

## Not checked

Honest about the gaps:

- **Surface spokes** — these are surface slip stitches that "do not replace or add to the growth-round
  counts," and the pattern says their number varies. There is no count to verify, and none was invented.
- **Centre ring fit** — whether a relaxed ch-20 or ch-24 ring clears a real stand is physical, not written.
  (The arithmetic is at least plausible: ch-20 ≈ 1.6 in and ch-24 ≈ 1.9 in diameter, both inside the
  stated 1.5–2 in target.)
- **Blocking, drape, flammability, wash behaviour, finished fit** — all physical.
- **Active time** — no claim made, correctly.
- The Contents lists a "Safety — read this first" heading that doesn't appear as a labelled heading in
  the extracted text; most likely a PDF-extraction artifact rather than a missing section. Low confidence.

---

## Bottom line

This is an unusually well-constructed pattern. The 12-repeat ladder is internally consistent across
all 32 rounds, the border divisibility is designed in rather than lucky, the bobble rounds land on the
size stop-points deliberately, and the one round most likely to be miscounted by hand (R12) has a
correct worked explanation attached.

If I were sending one note back to the designer, it would be the **gauge inconsistency (#1)** —
asking makers to match both 12 sts = 4 in and 6 rounds = 4 in is asking for something a flat circle
can't do, and it points at the cupping the Troubleshooting section then has to address.

The **38 in lower bound** and the **yarn allowance** are worth a second look too, though the pattern
already flags the latter as unverified.

---

### Files

| File | Contents |
|---|---|
| `ns14_raw.txt` | Your pasted text, cleaned of PDF table artifacts |
| `ns14_body_native.txt` | All 32 rounds in parser-native idiom |
| `ns14_body_annotated.txt` | Same, with bobble rounds marked |
| `ns14_mini.txt` / `ns14_standard.txt` / `ns14_large.txt` | Each size + its border |
| `NS14_REPORT.md` | This report |
