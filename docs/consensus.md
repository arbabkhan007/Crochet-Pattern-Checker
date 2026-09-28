# Consensus learning

This file is rewritten by `scripts/check_consensus.py`. It is the check result, not a fourth pattern.

The three viewpoints stay unedited:

- `docs/wrong_benchmarks.md`
- `docs/gemini_corrected.md`
- `docs/chatgpt_corrected.md`

The checker does not change its own rules. A lesson is learned only when `wrong.txt` is not a clean pass and `corrected.txt` passes with no errors and no warnings.

## How to read a viewpoint check

A PASS on the Gemini or ChatGPT file is not proof. `[sc 1, inc] 6 times` and a backticked `×` repeat are not the checker's dialect. The counter does not expand them, so a wrong repeat can pass.

An ERROR made only of undefined abbreviations, or of `worked N stitches into` on a prose line, is parser noise. It is not the lesson.

A 12-to-24 increase is now an error. An unequal sew, cinch, or graft count is now an error. A cinch with no stitch counts is still unread.

## What the checker learned

These lessons are the consensus. Each one is agreed by both corrected files and proved by the checker.

### 01_stated_count: Stated count

Wrong result: ERROR.
- Round/row 1: stated 16 stitches but operations produce 14
Corrected result: PASS.

How: (5 sc, dec) makes 6. Twice is 12. The last 2 sc makes 14. The line consumes 16 and produces 14, so a written 16 is false.

What: Gemini and ChatGPT both say this line cannot make 16. The consensus repair changes the stated count to 14. It does not rewrite the stitches, because the two files do not agree on a rewrite.

### 02_repeat_cover: Repeat cover

Wrong result: ERROR.
- Round/row 2: stated 32 stitches but operations produce 30
- Non-modulo consumption: Round 2 has 38 incoming stitches, but the repeat consumes 6. 2 stitches would be left unworked.
Corrected result: PASS.

How: (4 sc, dec) uses 6 stitches and makes 5. Six repeats use 36 and make 30. Two stitches of the 38 are never written, and 32 is not what those repeats make.

What: both corrected files agree a decrease repeat must cover the round. The consensus writes the leftover 2 sc and states 32. This is the rule, not a vote on a 38-stitch start versus a 40-stitch start.

### 03_post_foundation: Post foundation

Wrong result: ERROR.
- Post stitch fpdc is worked into a short sc row. Post stitches need a foundation of hdc or taller.
Corrected result: PASS.

How: fpdc has to enter a stitch at least as tall as hdc. The previous round is sc, which is too short. (fpdc) x 6 keeps the count at 6 once the foundation is tall enough.

What: both corrected files agree. Do not work a post stitch into a short sc round. Change the previous round to hdc.

### 04_ghost_eyes: Ghost eyes

Wrong result: ERROR.
- Ghost material: 'safety eyes' is listed under Materials but never mentioned in the instructions.
Corrected result: PASS.

How: safety eyes are listed under Materials and never appear in the instructions. A materials line is not a placement.

What: both corrected files agree. Name the eyes in the head instructions, before stuffing. Do not leave them as an unused listing.

### 05_equal_socket: Equal socket

Wrong result: ERROR.
- Gusset Mismatch: Limb holds 3 sts, but body skips 4 sts.
Corrected result: PASS.

How: the body skips 4 stitches and the limb holds 3. A join closes only when those two numbers are equal. Worked plus skipped must also equal the previous body count.

What: both corrected files agree the seam counts must match. This pair makes them 4 and 4. When a pattern offers 3 and 3 as the other equal choice, that choice stays open.

### 06_edging_fullness: Edging fullness

Wrong result: PASS_WITH_WARNINGS.
- Frill Alert: Edging is 5.5x full (threshold 2.5x). Fabric will bunch severely.
Corrected result: PASS.

How: 70 stitches on 14 row-ends is 5 times the base. With this gauge the checker warns above 2.5 times full.

What: both corrected files agree 5 times full is too much. The consensus uses one stitch per row-end so the check can pass. A 35-stitch fan and a 42-stitch fan still warn, so neither model's fan is the consensus repair.

### 07_span_match: Span match

Wrong result: PASS_WITH_WARNINGS.
- Span Mismatch: Seam (3.33") and body span (1.69") differ by factor of 2.0x.
Corrected result: PASS.

How: 20 stitches at 24 stitches per 4 inches is 3.33 inches. 11 rounds at 26 rounds per 4 inches is 1.69 inches. The checker warns when those lengths differ by more than 1.25 times.

What: both corrected files agree those lengths cannot be sewn flat. The consensus matches the counts. A gather sentence is not something this checker can confirm.

### 08_tab_fit: Tab fit

Wrong result: ERROR.
- Spatial fit: Wing tab insertion is 12 stitches, wider than the 6-chain socket.
Corrected result: PASS.

How: the checker reads a skipped chain socket and the next stated tab width. A 12-stitch tab does not fit in a 6-chain socket.

What: both corrected files agree the tab must not be wider than the socket. Inch sizes in prose are not read. This pair uses stitch counts.

### 09_clause_total: Clause total

Wrong result: ERROR.
- Round/row 15: stated 54 stitches but operations produce 48
Corrected result: PASS.

How: the clauses add to 48. Writing 54 does not create the missing 6 stitches.

What: both corrected files agree 54 is not the sum of those clauses. The consensus changes the stated count to 48. It does not add stitches to build a different join.

### 10_neck_jump: Neck jump

Wrong result: ERROR.
- Round 2: 12 stitches jump to 24. Insert an 18-stitch round before returning to 24.
Corrected result: PASS.

How: 12 increases use the 12 stitches and make 24. The count is internally true, so the old checker passed it. The fabric still skips the 18-stitch step and puckers.

What: both corrected files insert an 18-stitch round, then return to 24. The checker now rejects a 12-to-24 jump and accepts the 12, 18, 24 step.

### 11_seam_count: Seam count

Wrong result: ERROR.
- Seam mismatch: 3 stitches cannot close 4 stitches.
- Seam mismatch: 5 stitches cannot close 3 stitches.
- Seam mismatch: 26 stitches cannot close 18 stitches.
Corrected result: PASS.

How: a seam closes only when both edges have the same number of stitches. Sewing 3 to 4, cinching 5 to 3, or sewing a 26-stitch edge to an 18-stitch edge leaves stitches unmatched.

What: both corrected files agree the counts must match. The checker now reads those sentences. It does not choose 3 and 3 over 4 and 4 when a pattern offers both equal choices.

## What was checked and not learned

| Pattern | Agreed defect | Why it is not a lesson |
|---|---|---|
| Bear | Do not cinch, with no stitch counts | Cinch and flatten are still prose when no two stitch counts are written. |
| Bear | Do not cinch the arm | Cinch and flatten are prose. The checker does not read them. |
| Bear | Add legs and ears | A missing piece is not an error unless the checker can see a count. |
| Wyvern | 24-stitch join versus a valid 30 | The models disagree. No consensus pattern is written. |
| Wyvern | 35-stitch fan versus 42-stitch fan | Both still warn above 2.5 times full. Neither is the lesson. |
| Dragon and Chimera | Which decrease formula to use | The models disagree on the target count. Only the cover-the-round rule is learned. |
| Leviathan | Rebuild the hub to 64 | One model changes the count to 48. The other rebuilds the join. Only the 48-clause total is learned. |
| All | Short rows, frills in prose, eyes on a frill, closed tentacle wording | The checker does not build those sites. |

## Viewpoint check

These rows are what the checker returned. They are not a vote.

| File | Section | Status | Errors | Warnings | Seen, after dropping abbreviation noise |
|---|---|---|---:|---:|---|
| `wrong_benchmarks.md` | whole file | ERROR | 71 | 0 | Line 121: worked 5 stitches into 15 without a decrease.; Line 220: worked 1 stitch into 48 without a decrease.; Line 221: Attempted to work stitch beyond available loops. Position: 1, Available: 1 |
| `wrong_benchmarks.md` | 1: Classic Amigurumi Bear | PASS | 0 | 0 | none |
| `wrong_benchmarks.md` | 2: Celestial Wyvern | ERROR | 8 | 0 | Line 43: worked 5 stitches into 15 without a decrease. |
| `wrong_benchmarks.md` | 3: Clockwork Dragon | ERROR | 11 | 0 | Seam mismatch: 3 stitches cannot close 4 stitches. |
| `wrong_benchmarks.md` | 4: Abyssal Leviathan | ERROR | 41 | 0 | Line 50: worked 1 stitch into 48 without a decrease.; Line 51: Attempted to work stitch beyond available loops. Position: 1, Available: 1; Line 68: Attempted to work stitch beyond available loops. Position: 1, Available: 1 |
| `wrong_benchmarks.md` | 5: Void-Warped Chimera | ERROR | 20 | 0 | Line 38: Attempted to work stitch beyond available loops. Position: 36, Available: 36; Post stitch fptr is worked into a short sc row. Post stitches need a foundation of hdc or taller.; Seam mismatch: 26 stitches cannot close 18 stitches. |
| `gemini_corrected.md` | whole file | PASS_WITH_WARNINGS | 0 | 1 | Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
| `gemini_corrected.md` | 1: Classic Amigurumi Bear (Corrected) | PASS | 0 | 0 | none |
| `gemini_corrected.md` | 2: Celestial Wyvern (Corrected) | ERROR | 1 | 0 | Ghost material: '.25 mm hook, polyfill, 12 mm safety eyes (x2), tapestry needle' is listed under Materials but never mentioned in the instructions. |
| `gemini_corrected.md` | 3: Clockwork Dragon (Corrected) | PASS_WITH_WARNINGS | 0 | 1 | Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
| `gemini_corrected.md` | 4: Abyssal Leviathan (Corrected) | PASS_WITH_WARNINGS | 0 | 1 | Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
| `gemini_corrected.md` | 5: Void-Warped Chimera (Corrected) | PASS | 0 | 0 | none |
| `chatgpt_corrected.md` | whole file | ERROR | 1 | 0 | Seam mismatch: 3 stitches cannot close 4 stitches. |
| `chatgpt_corrected.md` | 1: Classic Amigurumi Bear — Corrected | PASS | 0 | 0 | none |
| `chatgpt_corrected.md` | 2: Celestial Wyvern — Corrected | PASS | 0 | 0 | none |
| `chatgpt_corrected.md` | 3: Clockwork Dragon — Corrected Defect Sections | ERROR | 1 | 0 | Seam mismatch: 3 stitches cannot close 4 stitches. |
| `chatgpt_corrected.md` | 4: Abyssal Leviathan — Corrected | PASS | 0 | 0 | none |
| `chatgpt_corrected.md` | 5: Void-Warped Chimera — Corrected | PASS | 0 | 0 | none |

## Not merged

| Pattern | Gemini | ChatGPT |
|---|---|---|
| Bear arms | Flatten an 8-stitch opening | Decrease to 4, then flatten |
| Bear ears | 6, then 9 | 6, then 12, then 18 |
| Bear legs | Stay at 12 | Decrease 12 to 9 |
| Wyvern join | Rewrite to 24 | Keep 30 once the bridge is worked |
| Wyvern wing | 35 stitches | 42 stitches, or 28 for a flatter edge |
| Dragon rejoin | 36 perimeter positions | 34, or mark 6 as skipped |
| Leviathan hub | Rebuild to 64 | The written clauses are 48 |
| Chimera round 15 | 44 to 40 | 44 to 38 |
| Chimera frill | About 150 stitches | 324 stitches |
| Chimera graft | 24 to 24 | 36 to 36 |

Do not auto-merge a row in that table. A later file may choose one side only when a person says which source it follows.
