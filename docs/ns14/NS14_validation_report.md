# NS 14 "Bobble Snowflake" Tree Skirt — validation report

**Pattern:** Novality Crochet Studio, Design Code NS 14, printer-saver edition
**Validated:** 2026-10-07
**Tool:** `arbabkhan007/Crochet-Pattern-Checker` v1.0.0 (deterministic written checker) + an independent arithmetic audit written for this pattern
**Deliverables:** `NS14_corrected.md` (corrected pattern), `audit_ns14.py` (reproducible count proof), checker inputs listed in §6

---

## 1. Verdict

**The stitch mathematics in this pattern is correct.** All 32 growth rounds, the bobble cadence, all three size stops and the scalloped border were verified stitch-for-stitch, and every stated count is right. No count, repeat, increase-rate or closure error exists in the ladder — this pattern does **not** need a stitch correction.

What it does need is editorial repair: one paragraph of leftover amigurumi instructions that tell the maker to work eyes and embroidery that do not exist in this design, a yarn allowance roughly 3–5× larger than the stitch counts imply, a pair of gauge targets that cannot both be exact on this circle, two sentences whose wording makes automated count checkers report false errors, an unlabelled progress row, and pervasive word-join typos inside the instruction cells.

| Area | Result |
|---|---|
| Growth rounds R1–R32 (consumption, production, repeats, totals) | **32/32 correct** |
| Bobble cadence and colour route | **correct** |
| Size stops and border closure (28 / 46 / 64 scallops) | **correct** |
| Bobble technique, marker tracking, join method | **correct** |
| US ↔ UK term pairs (36 rows) | **correct** |
| Hook and yarn-weight conversions | **correct** |
| Gauge → diameter arithmetic | **correct** |
| Editorial content, yarn allowance, dual gauge targets, layout | **12 findings — all addressed; 2 need confirmation against the source PDF** |

Severity scale: **High** = misleads the maker or their wallet · **Medium** = internally inconsistent or unverifiable claim · **Low** = wording, layout or automation hygiene.

---

## 2. How this was validated

The supplied text is a flattened PDF: instruction cells are glued together and the US and UK columns share one line, so the checker's count engine cannot read it directly (it mis-parses `2 dc in next st` and reports nonsense totals). Four independent routes were used instead.

1. **Independent arithmetic audit** (`audit_ns14.py`). Extracts the US column of all 32 rows from the pasted table and tests each against the pattern's own stated rule — *Round N consumes N−1 old stitches and produces N new stitches in each of 12 repeats, ending at exactly 12 × N*. It also confirms that each repeat consumes exactly the stitches the previous round made, so nothing is left unworked. **Result: 32/32 rounds pass, zero violations.**
2. **Structure-preserving transcription run through the repo's checker.** `dc` and `BO` each consume 1 / produce 1 → written as `sc`; `2 dc in next st` consumes 1 / produces 2 → written as `inc`. Counts, repeats and consumption are identical to the source. **Result: the full R1–R32 ladder validates clean** (the single hit is discussed in §5.1).
3. **Border closure, with a negative control.** The border was transcribed as `(sc, skip 2 sts, 5 sc in next st, skip 2 sts) x 28 (168)` on the mini ladder — it consumes 168 and produces 168 exactly, for all three sizes (28/46/64). A deliberate control with 27 repeats fails with `worked 162 stitches into 168 without a decrease`, which proves the check is actually exercising the border rather than skipping it.
4. **Row-by-row diff of the corrected file against the source.** After editing, all 32 ladder rows were re-extracted from `NS14_corrected.md` and compared field-by-field (bobble flag, plain-dc count, increase, repeat count, stated total) with the source: **no differences** — the corrections touched prose and layout only, never the ladder. The UK column was also machine-checked to be the exact dialect translation of the US column in all 36 rows (`sc→dc`, `dc→tr`, `ch`/`sl st`/`BO`/`skip` unchanged): **no mismatches**.

Hook and yarn-weight claims were cross-checked against the Craft Yarn Council tables the repo publishes in `docs/standards.md`.

---

## 3. Verified correct — do not change these

Each item below was checked numerically, not skimmed.

- **Every growth round.** R1 `12 dc in ring` (12) → R32 `[BO, dc in next 29 sts, 2 dc in next st] x 12` (384). Each repeat consumes exactly N−1 old stitches and produces exactly N; 12 repeats consume precisely the previous round's total with **zero stitches left unworked**, and every printed total equals 12 × N.
- **R12 — the row that looks wrong and is not.** It reads `dc in next 10 sts`, and 10 is correct: R11 leaves 132 stitches, so each repeat may consume 11, and `10 plain dc + 1 increase anchor` = 11 consumed / 12 produced → 144 ✓. Changing it to `9 sts` consumes 120 of 132, leaves **12 stitches unworked** and yields 132, contradicting the printed (144). The pattern's own count-check paragraph says exactly this and is arithmetically sound in all four of its claims. **Anyone re-editing this pattern will be tempted to "fix" R12 to 9; that is the error, not the cure.**
- **The count rule and its two worked examples.** `N−2 plain dc plus one increase` holds for all 22 plain rounds; `one plain dc replaced by one BO` holds for all 10 bobble rounds. Construction note 2's specific claims are right: R9 = 7 plain dc ✓, R10 = 8 ✓.
- **Bobble cadence.** R5, R8, R11, R14, R17, R20, R23, R26, R29, R32 — gaps all exactly 3 ✓, matching technique 4 and the colour route. All three size stops land on bobble rounds, so the final growth round is always CC and the border joins into CC.
- **Border arithmetic.** 6 anchors consumed and 6 worked stitches produced per repeat ✓; 168÷6 = 28, 276÷6 = 46, 384÷6 = 64 ✓; all three totals divisible by 6 ✓. The stitch you join into is taken by the *final* skip of the last repeat, which is exactly what makes the repeat close — the closing slip stitch therefore lands one stitch past the join. **Correct as written; do not "tidy" it** by working the first sc into the join stitch (that would consume 1 + 6k anchors and no longer divide evenly).
- **Five-dc bobble.** One loop on the hook, each incomplete dc leaves one extra → after five incomplete dc exactly **six loops** remain, then yo and pull through all six ✓. Counting the BO as 1 stitch ✓ is consistent with every total in the ladder.
- **Increase-column marker tracking.** R2 (`2 dc in each st around` over 12 stitches) contains exactly **12 increases**, so "the second dc of each R2 increase" yields exactly 12 markers — and those are precisely the 12 increase anchors of R3 ✓. The claim that the marked stitch is "the last old stitch consumed by its repeat" holds on every later round ✓, so the 12 outer endpoints stay evenly spaced for the spokes.
- **Join method.** `ch 2` never counted + first dc/BO into the same stitch as the join + `sl st` to that first actual stitch is self-consistent, and every printed total works with it ✓.
- **Hook and yarn.** 5 mm = US H/8 and 5.5 mm = US I/9 ✓ (`docs/standards.md`). Worsted/aran #4 with 12 dc = 4 in ✓ sits inside the published #4 gauge range.
- **Gauge → diameter.** 168÷3 = 56 in → 17.8 in / 45 cm ✓; 276÷3 = 92 → 29.3 in / 74 cm ✓; 384÷3 = 128 → 40.7 in / 103 cm ✓. The header's `TARGET 46–109 CM`, the description's three ranges and the *Sizes at a glance* table all agree ✓, as do the finishing step, the border note and the finish checklist (168/276/384, 28/46/64, 12 spokes) ✓.
- **US ↔ UK pairs.** All 36 construction rows machine-verified as exact translations ✓, including the border (`sc … 5 dc` → `dc … 5 tr`). The abbreviation table's `dc = tr` and `sc = dc` are the correct Craft Yarn Council equivalences ✓.

---

## 4. Findings and corrections

All fixes are applied in `NS14_corrected.md`; its closing *Revision notes* section repeats them and is marked "delete before publishing".

### F1 · High · Instructions for work that does not exist
**Source:** *Read before making* — "Complete internal eyes, embroidery, knots and joins while the relevant opening remains accessible."
**Problem:** template residue from an amigurumi pattern. A tree skirt has no internal eyes and no embroidery, and its only opening is the closed centre ring. The sentence sends the maker looking for steps that are not in this design, and it is the one place the document contradicts its own component list (ring, growth rounds, spokes, border, tails, blocking).
**Fix:** "Complete the centre-ring join, the optional surface spokes and the border in that order, and weave every tail while the centre opening is still open and accessible." This also reinforces the pattern's real ordering constraint (spokes before border).

### F2 · High · Yarn allowance is 3–5× what the stitch counts imply
**Source:** *Materials* — "The source planning allowance of 700–1,200 g for a standard or large skirt has not been measured and provides neither a mini allowance nor a verified colour split."
**Problem:** the disclaimer is honest, but the number is still printed, and it is far outside what the written counts support. First-principles estimate (worsted at ~200 yd/100 g; 3–4 in of yarn per US dc; a 5-dc bobble uses five dc of yarn while counting as one stitch; border and 12 spokes included):

| Size | Stop | Growth stitches | dc-equivalents | Estimated yarn | CC share |
|---|---|---|---|---|---|
| Mini | R14 | 1,260 | ~1,680 | **70–95 g** | ~52 % |
| Standard | R23 | 3,312 | ~4,020 | **165–225 g** | ~47 % |
| Large | R32 | 6,336 | ~7,330 | **305–410 g** | ~44 % |

Cross-check by fabric area: the large skirt is ~1,300 in² of dc fabric at ~4.5 stitches/in² ≈ 5,850 body stitches, within 8 % of the 6,336 counted (the gap is the extra yarn inside the bobbles, plus the border and spokes). A maker buying to the printed allowance would buy roughly two to three times too much yarn. The colour split matters too: because every bobble round is worked **entirely** in CC (technique 4 says so explicitly) and CC also covers the spokes and border, CC is close to half the yarn — highest in the mini.
**Fix:** keep the "not weighed" framing, replace the single unusable figure with the per-size estimated ranges and the near-even MC/CC split, and add the missing mini figure plus a single-dye-lot warning. The checker correctly reports this as `Yarn quantity is a range, not a weighed amount` — which is the intended, honest state.

### F3 · Medium · The two gauge targets cannot both be exact on this circle
**Source:** *Gauge & size* — "12 stitches = 4 in / 10 cm across the stitch direction and 6 completed rounds = 4 in / 10 cm radially. Match both measures."
**Problem:** these are presented as two independent targets, but on a flat twelve-increase circle the second is *derived* from the first. Stitch width w = 4/12 = 0.333 in; each round adds 12 stitches = 4 in of circumference, so a flat disk's radius must grow 4 ÷ 2π = **0.637 in per round ≈ 6¼ rounds per 4 in**, i.e. round height h/w = 12/2π = 1.910. The stated 6 rounds = 4 in gives h = 0.667 in and h/w = 2.00 — about **4.7 % taller than flat geometry wants**. Meeting both numbers exactly leaves the radius long for its circumference (at R32: 21.3 in of radius against the 20.4 in that 128 in of edge requires), which is a mild cupping tendency the blocking must absorb. Real worsted dc fabric is close to 2:1, so a 12-increase circle wants ~12.6 increases per round for mathematical flatness; 12 is the standard, workable choice and the small cup is normal — but it should be *predicted*, not left for the maker to discover and then suspect their counting.
**Fix:** present the radial figure as derived (0.64 in / 1.6 cm per round, ≈6¼ rounds = 4 in), state that a rounded "6 rounds = 4 in" carries a mild cupping tendency that blocking removes, and tell the maker to match stitch gauge first and then confirm flatness. The *Troubleshooting* "body cups" entry now points at this instead of implying only a counting fault.

### F4 · Low · Wording that reads as "make zero"
**Source:** *Care & storage* — "Until that complete-sample test passes, make no machine-wash or tumble-dry claim."
**Problem:** the checker's zero-work rule reports `Make 0 asks for none of that piece.` — a spurious error, because "make no … claim" is a prohibition, not an instruction to make zero of a component. Any automated QA pass on this file will show a false failure here.
**Fix:** "do not make a machine-wash or tumble-dry claim" — identical meaning, and the checker treats a `do not` line as a prohibition. Verified: the rewritten line passes clean.

### F5 · Low · A prose note that parsers read as a second Round 11
**Source:** the count-check paragraph printed between R16 and *Rounds 17–24*, beginning "R11-to-R12 count check: R11 consumes 10 old stitches…".
**Problem:** a line that starts with a round token is read as a round header, so R11 appears to occur again after R16 → `Round 11 repeats or goes backwards. Number the rounds in order.` The note's arithmetic is entirely correct (verified in §3); only its opening words and its placement after a page break are at fault.
**Fix:** begin the line with words — "Count check for the R11-to-R12 step:" — and place it directly under the R12 row it explains. Verified: passes clean, and the arithmetic is unchanged.

### F6 · Low · Surface-crochet wording trips the both-sides rule
**Source:** *Construction & techniques* 6 — "with the yarn held on the wrong side, insert the hook from the right side…".
**Problem:** the technique is physically correct, but one line naming both sides makes the checker report `The right side and the wrong side cannot both face the worker.`
**Fix:** "hold the yarn behind the work, then insert the hook from the front of the fabric… The bobbles mark the front; the yarn supply stays behind it for the whole spoke." Same technique, unambiguous, and verified to pass clean.

### F7 · Low · Progress row with no identifier
**Source:** *Centre ring* table — the `Rnd` cell is empty, so its `[ ]` box is the only one in the document with no label, while *Progress tracking* promises every row can be ticked against a stated count.
**Fix:** label the row `Ring`.

### F8 · Low · Print styling reads as a colourway
**Source:** cover — "BLACK + WHITE · WHITE BACKGROUNDS · PROGRESS BOXES", two lines above the yarn colourway block FOREST GREEN / OAT CREAM.
**Problem:** in a document whose next colour statement is a yarn palette, "BLACK + WHITE" reads as a fourth colourway option, and the *Colourways* section offers three alternatives (none of them black and white).
**Fix:** prefix `DOCUMENT INK:`.

### F9 · Low · Bobble cadence imprecise in the description
**Source:** *Design description* — "a contrast bobble round every third round".
**Problem:** read literally, that puts bobbles on R3, R6, R9 …; the ladder's bobble rounds are every third round **from R5**. Technique 4 states it correctly, so the document contradicts itself in the one sentence a maker reads first.
**Fix:** "every third round from R5", plus the explicit list R5, R8, R11 … R32 under *Helpful tips*.

### F10 · Low · Empty section heading
**Source:** "Helpful tips" is followed by a blank gap and then *Sizes at a glance*, so the heading the Contents advertises at page 9 has no content of its own.
**Fix:** the sizes table, the count rule and the time note are now placed under it as labelled sub-sections.

### F11 · Low (verify in source) · Word joins inside instruction cells
**Source:** at least 19 distinct glued tokens in the supplied text, including `against thestand`, `slst to first dc`, `2 dcin next st`, `x12`, `stopgrowth; optional spokes,then border`, `final growthround`, `consumes 6edge sts and makes 1scallop`, `writtenlarger-opening option;recheck`, `relaxedsurface sl sts`, `pinnedguide`, `FO atthe outer edge`, `noreverse-side float`, `immediatelyoutside`, `routeseparately`, `markedcolumn`, `sl stto first tr`.
**Problem:** these may be copy/paste artifacts from the two-column PDF table — but if they are printed in the PDF they are missing spaces **inside the instruction cells**, the worst possible place for a typo, because `slst` and `2 dcin next st` are exactly the tokens a maker's eye skips.
**Fix:** all repaired in `NS14_corrected.md`, and the construction tables are now real tables (US | UK | Sts | Note), which removes the line-wrap gluing permanently. **Action for the studio:** confirm against the source PDF whether these are print defects or extraction artifacts.

### F12 · Low (verify in source) · Missing section heading
The Contents advertises "Safety — read this first 4" as the first section, but in the supplied text the three safety paragraphs appear with no heading, after the design description. The heading is restored in `NS14_corrected.md`; confirm it exists in the PDF.

---

## 5. Checker artifacts — findings that are **not** defects

These are reported so nobody "fixes" the pattern in response to them.

### 5.1 `Round 2: 12 stitches jump to 24. Insert an 18-stitch round before returning to 24.`
Fires only on the structure-preserving transcription, because that rule requires the literal token `inc` and the pattern never writes `inc` — it writes `2 dc in each st around`. It does not fire on the pattern's own wording. Domain-wise the rule's intent is a **change of increase rate mid-piece** (its lesson file goes from 6 increases per round to 12). NS 14 keeps a constant **+12 stitches per round** from R1 to R32, and doubling the foundation ring in round 2 is the standard flat-circle construction for every stitch height (6→12 for sc, 8→16 for hdc, 12→24 for dc). **Inserting an 18-stitch round would destroy this design:** 18 is not a multiple of 12, so the 12 increase columns, the 12 spokes and the ÷6 border closure would all break.

### 5.2 `… is marked UK, but it uses the US term 'sc'.`
The dialect-scope rule assumes one dialect per piece. NS 14 deliberately prints both side by side, so any section that mentions UK terms and also contains a US term is flagged. There is no real dialect defect: all 36 rows were machine-verified as exact translations (§2.4), and the abbreviation table's equivalences are correct. This finding cannot be cleared without abandoning the dual-column format.

### 5.3 Raw-text parsing
Run on the pasted PDF text, the count engine reports nonsense (`Round 1: 464 stitches`, `stated 132 but operations produce 36`) and 40 `Undefined abbreviation` errors for ordinary prose words (`per`, `inch`, `pi`, `cm`, `diameter`). That is the flattened two-column table defeating the line parser, not a pattern fault — hence the transcription route in §2.2. The three honest warnings it does return (finished size is a target range, gauge has no tested sample result, the opening is approximate) are claims the pattern itself already labels unverified.

---

## 6. Reproduction

```bash
cd Crochet-Pattern-Checker
python3 -m venv .venv && .venv/bin/pip install pydantic click rich

# 1. independent arithmetic audit of all 32 rounds (exits 1 on any violation)
python3 ../audit_ns14.py ../ns14_original.txt

# 2. the repo's engine on the structure-preserving transcription
PYTHONPATH=src .venv/bin/python -m crochet_checker.cli check ../ns14_checker_input_nocomments.txt --json

# 3. border closure for all three sizes, plus the 27-repeat negative control
PYTHONPATH=src .venv/bin/python -m crochet_checker.cli check ../ns14_border_shell.txt --json   # 28 scallops, clean
PYTHONPATH=src .venv/bin/python -m crochet_checker.cli check ../ns14_border_std.txt  --json   # 46 scallops, clean
PYTHONPATH=src .venv/bin/python -m crochet_checker.cli check ../ns14_border_lge.txt  --json   # 64 scallops, clean
PYTHONPATH=src .venv/bin/python -m crochet_checker.cli check ../ns14_border_bad.txt  --json   # control: fails as expected

# 4. the corrected document
PYTHONPATH=src .venv/bin/python -m crochet_checker.cli check ../NS14_corrected.md
```

Artifacts in the workspace: `ns14_original.txt` (pattern as supplied) · `audit_ns14.py` (count proof) · `ns14_checker_input.txt` / `ns14_checker_input_nocomments.txt` (transcription) · `ns14_border_shell.txt`, `ns14_border_std.txt`, `ns14_border_lge.txt`, `ns14_border_bad.txt` (border + control) · `NS14_corrected.md` (deliverable). The repository itself is unmodified.

---

## 7. What was not verified

Consistent with the checker's own limits and the pattern's disclaimers: no photo or chart image was read, no sample was crocheted, no gauge swatch was measured, no yarn was weighed, no blocked dimension was confirmed, and no flammability, toy-safety or consumer-product assessment was performed. The yarn figures in F2 are an estimate from written stitch counts with stated assumptions, not a weighed result — weigh a complete sample before publishing any quantity. The finished-size ranges remain the pattern's own unverified targets.
