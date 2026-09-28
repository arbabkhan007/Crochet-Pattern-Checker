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

A 12-to-24 increase is now an error. An unequal stitch seam is now an error. An unequal inch edge is now a warning. A UK piece that uses sc, an unbounded repeat, an unreachable stitch, a missing round, a short chart-symbol row, an uncounted stitch line, a gauge far outside the Craft Yarn Council crochet band, a short-row span that drops 34 to 28 without stating the row-ends, a prose frill above 2.5 times full, and safety eyes mounted on a frill are now checked. A closed tentacle join, a chain crossed once, a dropped body count, a back post on the front loop, eyes placed after stuffing, more than 3 stitches in each row end, a repeat that misses its incoming count, an unlisted color, a repeated round number, and more than 2.5 stitches in every base stitch are now checked. A cinch with no numbers is still unread. A photo is still not classified.

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

### 12_inch_span: Inch span

Wrong result: PASS_WITH_WARNINGS.
- Span mismatch: 3.33 inches sewn to 1.69 inches differ by 2.0x.
Corrected result: PASS.

How: 3.33 inches sewn flat to 1.69 inches is about twice as long. The edge puckers unless one side is resized or the pattern says to gather it.

What: both corrected files agree those lengths cannot be sewn flat. The checker now warns above 1.25 times. Matching the two inch lengths passes. A gather sentence is still not confirmed.

### 13_dialect_scope: Dialect scope

Wrong result: ERROR.
- Head is marked UK, but it uses the US term 'sc'.
Corrected result: PASS.

How: a piece marked UK cannot use sc, and a piece marked US cannot use htr. Two pieces may use different dialects when each one says so.

What: the corrected file keeps the US term inside the piece marked US. The checker does not treat dc as proof of either dialect, because both countries use that spelling.

### 14_termination: Termination

Wrong result: ERROR.
- This repeat does not terminate. Say the stitch count, the round count, or the length.
Corrected result: PASS.

How: a repeat until a length, a stitch count, or a round count can stop. A repeat until the piece is long enough cannot.

What: the corrected file gives the repeat a stitch stop. The checker does not invent the missing count.

### 15_reachability: Stitch reachability

Wrong result: ERROR.
- Line 2: worked 1 stitch into 6 without a decrease.
- Stitch 9 is not reachable. The previous round has 6 stitches.
Corrected result: PASS.

How: a later round cannot work the 9th stitch when the previous round has 6. A loop already used on both sides cannot be used again.

What: the corrected file works each of the 6 stitches. The checker tracks written indexes. It does not build a picture of the fabric.

### 16_references: References

Wrong result: ERROR.
- Round 9 is named but this pattern never starts it.
Corrected result: PASS.

How: join to Round 9 is an error when the pattern never starts Round 9.

What: the corrected file joins Round 1, which exists. Sew the Ear to the Head, when Ear never starts, is proved by the stage test. A lowercase sentence such as sew head to body is still unread.

### 17_chart_text: Chart text

Wrong result: ERROR.
- Chart row states 4 stitches but the symbols produce 3.
Corrected result: PASS.

How: written chart symbols are counted. X V X is 3 stitches, so a stated 4 is wrong. A chart picture is not read.

What: the corrected file has four symbols and states 4. The legend in the pattern defines the symbols.

### 18_ambiguity: Ambiguity

Wrong result: ERROR.
- Line 2: worked 1 stitch into 6 without a decrease.
- Round 2 does not say how many stitches to work.
Corrected result: PASS.

How: sc in next st, with no count and no around or across, does not say how many stitches to work.

What: the corrected file says each stitch around and states the count. This is a written rule, not a language model.

### 19_gauge_band: Gauge band

Wrong result: PASS_WITH_WARNINGS.
- Gauge 40 stitches per 4 inches is outside the Craft Yarn Council crochet band for worsted (11-14). This is a published-range check, not a trained model.
Corrected result: PASS.

How: 40 single crochet per 4 inches is far outside the Craft Yarn Council crochet band for worsted, which is 11 to 14. A count inside half to double that band does not warn.

What: the corrected file uses 12, inside the published band. This is not a trained gauge model. Tight amigurumi gauges such as 20 per 4 inches do not warn.

### 20_short_row_gap: Short-row gap

Wrong result: ERROR.
- Short-row gap: 28 of 34 leaves 6 row-ends unstated.
Corrected result: PASS.

How: short rows that work 28 of 34 perimeter stitches leave 6 row-ends. Those row-ends must be written. The checker does not invent them.

What: the corrected file states the 6 row-ends. A cinch with no numbers is still unread.

### 21_prose_frill: Prose frill

Wrong result: PASS_WITH_WARNINGS.
- Prose frill: 756 stitches worked into 108 base stitches is 7.0x full. Above 2.5x the edge bunches.
Corrected result: PASS.

How: 756 stitches worked into 108 base stitches is 7 times full. The edge bunches above 2.5 times. This is a warning, not an error.

What: the corrected file works one stitch into each base stitch. A cinch with no numbers is still unread.

### 22_eyes_on_frill: Eyes on a frill

Wrong result: ERROR.
- Safety eyes are mounted on the frill. A frill has no fabric behind it for the washer. Mount them on a solid single-crochet round.
Corrected result: PASS.

How: a safety eye mounted on a frill has no solid fabric behind it for the washer. The eye cannot lock.

What: the corrected file mounts the eyes on a solid single-crochet round and says not on the frill. A cinch with no numbers is still unread.

### 23_closed_join: Closed join

Wrong result: ERROR.
- A closed tentacle has no live stitches to join. Leave an open edge and state how many stitches it holds.
Corrected result: PASS.

How: a closed tentacle has no live stitches. Joining 3 stitches of it cannot work.

What: the corrected file joins an open edge. A cinch with no sew-flat sentence is still unread.

### 24_flat_cap: Flat cap

Wrong result: ERROR.
- A cinched round is a sealed cap. It cannot be sewn flat. Leave the last round open.
Corrected result: PASS.

How: a round that is cinched shut is a sealed cap. It cannot also be sewn flat.

What: the corrected file leaves the last round open. Cinch shut by itself, with no sew-flat words, is still unread.

### 25_chain_underside: Chain underside

Wrong result: ERROR.
- Chain underside missing: ch 3 is crossed once, but 30 counts both sides.
Corrected result: PASS.

How: sc 12, ch 3, sc 12, sc 3 across ch is 27 if the chain is crossed once. A stated 30 needs the underside as well.

What: the corrected file writes both sides of the chain. The checker does not invent the missing 3 stitches.

### 26_dropped_body: Dropped body stitches

Wrong result: ERROR.
- Dropped body stitches: 21 worked from 24 leaves 3 unwritten. Write the skip, or work the full count.
Corrected result: PASS.

How: 21 stitches worked from a 24-stitch body leave 3 stitches unwritten unless the skip is written.

What: the corrected file says skip 3. Working the full 24 would also pass.

### 27_front_back_post: Front and back post

Wrong result: ERROR.
- A back post in the front loop turns the ridge inward. Use a front post if the ridge should show.
Corrected result: PASS.

How: a back post in the front loop turns the ridge to the inside, where it cannot be seen.

What: the corrected file uses a front post. A quoted original line is not treated as an instruction.

### 28_eyes_before_stuff: Eyes before stuffing

Wrong result: ERROR.
- This piece: safety eyes are placed after stuffing. Insert them before the piece is stuffed.
Corrected result: PASS.

How: safety eyes placed after the head is stuffed have no opening for the washer.

What: the corrected file inserts the eyes before stuffing. A piece that never mentions eyes is not this rule.

### 29_row_end_density: Row-end density

Wrong result: PASS_WITH_WARNINGS.
- Row-end density: 5 stitches in each row end is above 3. The edge will bunch.
Corrected result: PASS.

How: 5 stitches in each row end is more than 3. The edge bunches. This is a warning.

What: the corrected file works one single crochet in each row end. Two or three would also pass.

### 30_incoming_cover: Incoming cover

Wrong result: ERROR.
- Incoming cover: the repeat uses 42 of 44 stitches. 2 are unaccounted for.
Corrected result: PASS.

How: (5 sc, dec) x 6 uses 42 stitches. Written on 44, it leaves 2 unaccounted for.

What: the corrected file says on 42 stitches, which is what the repeat uses.

### 31_missing_color: Missing color

Wrong result: ERROR.
- Color B is used but the yarn line never lists it.
Corrected result: PASS.

How: Color B is used, but the yarn line lists only Color A.

What: the corrected file lists Color B before it is used. A fragment with no color list is not this rule.

### 32_round_order: Round order

Wrong result: ERROR.
- Round 2 repeats or goes backwards. Number the rounds in order.
Corrected result: PASS.

How: Round 2 is written twice. The second one repeats a number that already passed.

What: the corrected file continues at Round 3. A new piece may start again at Round 1.

### 33_every_base: Every base stitch

Wrong result: PASS_WITH_WARNINGS.
- Every base stitch is worked 5 times. Above 2.5x the fabric bunches.
Corrected result: PASS.

How: 5 stitches worked into every base stitch is above 2.5 times. The fabric bunches. This is a warning.

What: the corrected file works 1 stitch into every base stitch.

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
| All | Countless cinch, lowercase sew head to body | A closed tentacle join and a cinched round sewn flat are now errors. A cinch with no numbers is still unread. |

## Viewpoint check

These rows are what the checker returned. They are not a vote.

| File | Section | Status | Errors | Warnings | Seen, after dropping abbreviation noise |
|---|---|---|---:|---:|---|
| `wrong_benchmarks.md` | whole file | ERROR | 80 | 6 | Line 121: worked 5 stitches into 15 without a decrease.; Line 220: worked 1 stitch into 48 without a decrease.; Line 221: Attempted to work stitch beyond available loops. Position: 1, Available: 1 |
| `wrong_benchmarks.md` | 1: Classic Amigurumi Bear | ERROR | 1 | 0 | Round 1 repeats or goes backwards. Number the rounds in order. |
| `wrong_benchmarks.md` | 2: Celestial Wyvern | ERROR | 9 | 2 | Line 43: worked 5 stitches into 15 without a decrease.; Chain underside missing: ch 3 is crossed once, but 30 counts both sides.; Prose frill: 5 times full is above 2.5x. The edge will bunch. |
| `wrong_benchmarks.md` | 3: Clockwork Dragon | ERROR | 13 | 0 | Seam mismatch: 3 stitches cannot close 4 stitches.; Short-row gap: 28 of 34 leaves 6 row-ends unstated.; Round 11 repeats or goes backwards. Number the rounds in order. |
| `wrong_benchmarks.md` | 4: Abyssal Leviathan | ERROR | 43 | 2 | Line 50: worked 1 stitch into 48 without a decrease.; Line 51: Attempted to work stitch beyond available loops. Position: 1, Available: 1; Line 68: Attempted to work stitch beyond available loops. Position: 1, Available: 1 |
| `wrong_benchmarks.md` | 5: Void-Warped Chimera | ERROR | 23 | 2 | Line 38: Attempted to work stitch beyond available loops. Position: 36, Available: 36; Post stitch fptr is worked into a short sc row. Post stitches need a foundation of hdc or taller.; Seam mismatch: 26 stitches cannot close 18 stitches. |
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
