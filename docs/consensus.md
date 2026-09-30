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

A 12-to-24 increase is now an error. An unequal stitch seam is now an error. An unequal inch edge is now a warning. A UK piece that uses sc, an unbounded repeat, an unreachable stitch, a missing round, a short chart-symbol row, an uncounted stitch line, a gauge far outside the Craft Yarn Council crochet band, a short-row span that drops 34 to 28 without stating the row-ends, a prose frill above 2.5 times full, and safety eyes mounted on a frill are now checked. A closed tentacle join, a chain crossed once, a dropped body count, a back post on the front loop, eyes placed after stuffing, more than 3 stitches in each row end, a repeat that misses its incoming count, an unlisted color, a repeated round number, and more than 2.5 stitches in every base stitch are now checked. A short chain, an unclosed parenthesis, a missing star, a decrease that misses its count, an increase that more than doubles, a written-as mismatch, an eye-count mismatch, a future round, a make-count mismatch, and a repeat of zero are now checked. Fifty phrase checks, lessons 44 through 93, now catch a zero hook, a one-stitch shell, a backward range, and the other written impossibilities. Lessons 94 through 158 add hook-letter, yarn-weight, UK-gloss, turning-chain, and zero-measure checks, plus general increase, decrease, range, multiple, and measure checks. Those general checks are proved on 5,000 sentences. Five thousand named copies were not added. A cinch with no number closes the last stated round, and is an error when no counted round comes before it. A lowercase sew line is a piece reference. A photo is still not classified.

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

What: the corrected file joins Round 1, which exists. Sew the Ear to the Head, when Ear never starts, is proved by the stage test. A lowercase sentence such as sew head to body is an error when that piece never starts.

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

What: the corrected file states the 6 row-ends. A cinch with no number closes the last stated round.

### 21_prose_frill: Prose frill

Wrong result: PASS_WITH_WARNINGS.
- Prose frill: 756 stitches worked into 108 base stitches is 7.0x full. Above 2.5x the edge bunches.
Corrected result: PASS.

How: 756 stitches worked into 108 base stitches is 7 times full. The edge bunches above 2.5 times. This is a warning, not an error.

What: the corrected file works one stitch into each base stitch. A cinch with no number closes the last stated round.

### 22_eyes_on_frill: Eyes on a frill

Wrong result: ERROR.
- Safety eyes are mounted on the frill. A frill has no fabric behind it for the washer. Mount them on a solid single-crochet round.
Corrected result: PASS.

How: a safety eye mounted on a frill has no solid fabric behind it for the washer. The eye cannot lock.

What: the corrected file mounts the eyes on a solid single-crochet round and says not on the frill. A cinch with no number closes the last stated round.

### 23_closed_join: Closed join

Wrong result: ERROR.
- A closed tentacle has no live stitches to join. Leave an open edge and state how many stitches it holds.
Corrected result: PASS.

How: a closed tentacle has no live stitches. Joining 3 stitches of it cannot work.

What: the corrected file joins an open edge. A cinch with no sew-flat sentence closes the last stated round.

### 24_flat_cap: Flat cap

Wrong result: ERROR.
- Cinch shut has no counted round to close. State the round count before the cinch.
- A cinched round is a sealed cap. It cannot be sewn flat. Leave the last round open.
Corrected result: PASS.

How: a round that is cinched shut is a sealed cap. It cannot also be sewn flat.

What: the corrected file leaves the last round open. Cinch shut by itself closes the last stated round. It is an error when no counted round comes before it.

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

### 34_chain_length: Chain length

Wrong result: ERROR.
- Round/row 1: stated 12 stitches but operations produce 9
- Chain of 10 cannot hold 12 stitches. The most this line can hold is 9.
Corrected result: PASS.

How: a chain of 10, started in the second chain, can hold 9 stitches. A stated 12 does not fit.

What: the corrected file states 9. The checker does not add the missing chains.

### 35_unclosed_repeat: Unclosed repeat

Wrong result: ERROR.
- Line 3: worked 3 stitches into 12 without a decrease.
- Round/row 3: stated 18 stitches but operations produce 3
- Round 3 has an unclosed parenthesis. Close the repeat.
Corrected result: PASS.

How: a round whose parentheses do not balance cannot be repeated as written.

What: the corrected file closes the repeat. The stitch count is the same 18.

### 36_missing_star: Missing star

Wrong result: ERROR.
- Rep from * has no opening star. Mark the start of the repeat with *.
Corrected result: PASS.

How: rep from * needs an opening star. One star at the end does not mark the start.

What: the corrected file marks *sc, inc* before rep from *.

### 37_decrease_cover: Decrease cover

Wrong result: ERROR.
- Decrease cover: dec x 5 uses 10 stitches, not 11.
Corrected result: PASS.

How: dec x 5 uses 10 stitches. Written on 11, one stitch is unaccounted for.

What: the corrected file says on 10 stitches, which is what the decrease uses.

### 38_over_double: Over-double increase

Wrong result: ERROR.
- Round 2 jumps from 6 to 18. More than doubling in one round skips a size.
Corrected result: PASS.

How: a round that goes from 6 to 18 more than doubles. It skips the 12-stitch size.

What: the corrected file inserts the 12-stitch round. Doubling exactly, 6 to 12, still passes this rule.

### 39_written_as: Written-as count

Wrong result: ERROR.
- Written count 38 does not match the 30-stitch edge.
Corrected result: PASS.

How: a 30-stitch edge written as 38 does not close. The two numbers are on the same line.

What: the corrected file writes 30. The checker does not pick 38 over 30.

### 40_eye_count: Eye count

Wrong result: ERROR.
- Eye count: materials list 2 safety eyes, but the instructions place 4.
Corrected result: PASS.

How: materials list 2 safety eyes and the instructions place 4. The washer count cannot match.

What: the corrected file places 2. Counts are compared only inside the same pattern section.

### 41_future_round: Future round

Wrong result: ERROR.
- Round 2 works into Round 5, which has not been made yet.
Corrected result: PASS.

How: Round 2 cannot work into Round 5. That round has not been made.

What: the corrected file works into Round 5 only after Round 5 exists.

### 42_make_count: Make count

Wrong result: ERROR.
- Make count: ears is made 2 times, but the line uses 3.
Corrected result: PASS.

How: Ears (make 2) cannot be sewn as 3 ears. The made count and the sewn count disagree.

What: the corrected file sews 2 ears. A line that does not give a number is still unread.

### 43_zero_repeat: Zero repeat

Wrong result: ERROR.
- A repeat of zero does no work. Give the repeat a count above zero.
Corrected result: PASS.

How: a repeat of zero does no work. The instruction cannot be followed as a repeat.

What: the corrected file repeats 6 times.

### 44_hook_zero: Zero hook

Wrong result: ERROR.
- A hook of 0 mm cannot make a stitch.
Corrected result: PASS.

How: a hook of 0 mm cannot pull up a loop.

What: the corrected file uses a 5 mm hook.

### 45_hook_huge: Huge hook

Wrong result: PASS_WITH_WARNINGS.
- A hook of 40 mm or more is past normal crochet. This is a warning.
Corrected result: PASS.

How: a 40 mm hook is past even jumbo crochet. This warns.

What: the corrected file uses a 6 mm hook.

### 46_hook_cm: Hook in centimeters

Wrong result: ERROR.
- The hook is written in centimeters. Crochet hooks are written in millimeters.
Corrected result: PASS.

How: a hook written as 5 cm is 50 mm. Crochet hooks are written in millimeters.

What: the corrected file says 5 mm.

### 47_chain_zero: Zero chain

Wrong result: ERROR.
- ch 0 makes no chain.
Corrected result: PASS.

How: ch 0 makes no chain to work into.

What: the corrected file chains 4.

### 48_work_zero: Work zero

Wrong result: ERROR.
- Work 0 stitches does no work.
Corrected result: PASS.

How: work 0 stitches is an instruction that does nothing.

What: the corrected file works 6 stitches.

### 49_skip_zero: Skip zero

Wrong result: ERROR.
- Skip 0 does not move the hook.
Corrected result: PASS.

How: skip 0 does not move the hook.

What: the corrected file skips 2.

### 50_decrease_to_zero: Decrease to zero

Wrong result: ERROR.
- Decrease to 0 stitches leaves nothing to fasten.
Corrected result: PASS.

How: decreasing to 0 stitches leaves nothing to fasten or sew.

What: the corrected file decreases to 6 stitches.

### 51_until_zero: Until zero

Wrong result: ERROR.
- Repeat until 0 stitches is not a workable stop.
Corrected result: PASS.

How: repeat until 0 stitches is not a workable stop. A digit of 0 still counts as written, so the termination rule does not catch it.

What: the corrected file stops at 6 stitches.

### 52_round_zero: Round zero

Wrong result: ERROR.
- Round 0 is not a round. Start at Round 1.
Corrected result: PASS.

How: rounds are numbered from 1. Round 0 is not a round.

What: the corrected file starts at Round 1.

### 53_marker_zero: Marker at zero

Wrong result: ERROR.
- Stitch 0 does not exist. Place the marker in stitch 1 or later.
Corrected result: PASS.

How: stitch 0 does not exist. The first stitch is stitch 1.

What: the corrected file places the marker in stitch 1.

### 54_gauge_zero: Zero gauge

Wrong result: ERROR.
- A gauge of 0 sc is not a fabric.
Corrected result: PASS.

How: a gauge of 0 sc per 4 inches is not a fabric.

What: the corrected file uses 12 sc per 4 inches.

### 55_zero_inches: Zero inches

Wrong result: ERROR.
- A finished width of 0 inches is not a piece.
Corrected result: PASS.

How: a finished width of 0 inches is not a piece.

What: the corrected file is 4 inches wide.

### 56_picot_zero: Picot of zero

Wrong result: ERROR.
- A picot of 0 is not a picot.
Corrected result: PASS.

How: a picot of 0 chains is not a picot.

What: the corrected file uses a picot of 3.

### 57_ch0_space: Chain-zero space

Wrong result: ERROR.
- A ch-0 space has no chains to work into.
Corrected result: PASS.

How: a ch-0 space has no chains to work into.

What: the corrected file uses a ch-2 space.

### 58_shell_one: Shell of one

Wrong result: ERROR.
- A shell of 1 is not a shell. Use at least 3 stitches.
Corrected result: PASS.

How: a shell needs at least 3 stitches. A shell of 1 is a single stitch.

What: the corrected file uses a shell of 5.

### 59_cluster_one: Cluster of one

Wrong result: ERROR.
- A 1-dc cluster is one stitch, not a cluster.
Corrected result: PASS.

How: a 1-dc cluster is one double crochet, not a cluster.

What: the corrected file uses a 3-dc cluster.

### 60_bobble_one: Bobble of one

Wrong result: ERROR.
- A bobble of 1 has nothing to gather.
Corrected result: PASS.

How: a bobble of 1 has no stitches to gather.

What: the corrected file uses a bobble of 5.

### 61_puff_one: Puff of one

Wrong result: ERROR.
- A puff of 1 is not a puff.
Corrected result: PASS.

How: a puff of 1 is one yarn over, not a puff.

What: the corrected file uses a puff of 5.

### 62_popcorn_one: Popcorn of one

Wrong result: ERROR.
- A popcorn of 1 cannot be closed.
Corrected result: PASS.

How: a popcorn of 1 cannot be folded closed.

What: the corrected file uses a popcorn of 5.

### 63_yarn_over_zero: Zero yarn over

Wrong result: ERROR.
- yo 0 does not put yarn on the hook.
Corrected result: PASS.

How: yo 0 does not put yarn on the hook.

What: the corrected file uses yo 2.

### 64_pull_zero: Pull through zero

Wrong result: ERROR.
- Pull through 0 loops leaves the loops on the hook.
Corrected result: PASS.

How: pull through 0 loops leaves the loops on the hook.

What: the corrected file pulls through 2 loops.

### 65_decimal_stitch: Decimal stitch

Wrong result: ERROR.
- 6.5 sc is not a whole stitch.
Corrected result: PASS.

How: 6.5 sc is not a whole stitch. The hook cannot make half a single crochet.

What: the corrected file works 6 sc.

### 66_fraction_repeat: Fractional repeat

Wrong result: ERROR.
- x 2.5 is not a whole repeat.
Corrected result: PASS.

How: x 2.5 asks for half of a repeat. Repeats are whole numbers.

What: the corrected file repeats 3 times.

### 67_negative_repeat: Negative repeat

Wrong result: ERROR.
- A negative repeat count is not a repeat.
Corrected result: PASS.

How: x -1 is not a repeat count.

What: the corrected file repeats 4 times.

### 68_round_huge: Round 9000

Wrong result: ERROR.
- Round 9000 is not a usable round number.
Corrected result: PASS.

How: Round 9000 is not a usable round number in this pattern.

What: the corrected file says Round 9.

### 69_join_contradiction: Join contradiction

Wrong result: ERROR.
- The line says to join and not to join.
Corrected result: PASS.

How: the same line says to join and not to join.

What: the corrected file joins with a slip stitch.

### 70_spiral_and_join: Spiral and join

Wrong result: ERROR.
- A continuous spiral cannot also join every round.
Corrected result: PASS.

How: a continuous spiral does not join every round. The two instructions disagree.

What: the corrected file keeps the spiral and says not to join.

### 71_blo_and_both: Both loop claims

Wrong result: ERROR.
- BLO only and both loops cannot be the same stitch.
Corrected result: PASS.

How: BLO only and both loops cannot be the same stitch.

What: the corrected file keeps BLO only.

### 72_inc_and_dec: Increase and decrease

Wrong result: ERROR.
- inc and dec in each stitch contradict each other.
Corrected result: PASS.

How: inc and dec in each stitch cancel, and the line does not say which one.

What: the corrected file increases in each stitch.

### 73_both_directions: Both directions

Wrong result: ERROR.
- The line gives both directions and does not say or.
Corrected result: PASS.

How: left to right and right to left, with no or, gives two directions.

What: the corrected file works left to right.

### 74_two_joins: Two joins

Wrong result: ERROR.
- An invisible join and a slip-stitch join cannot both finish the round.
Corrected result: PASS.

How: an invisible join and a slip-stitch join are two finishes. The line requires both.

What: the corrected file uses the invisible join.

### 75_both_sides_facing: Both sides facing

Wrong result: ERROR.
- The right side and the wrong side cannot both face the worker.
Corrected result: PASS.

How: the right side and the wrong side cannot both face the worker.

What: the corrected file keeps the right side facing.

### 76_yarn_double_single: Double and single

Wrong result: ERROR.
- The yarn cannot be held double and single at the same time.
Corrected result: PASS.

How: the yarn cannot be held double and single at the same time.

What: the corrected file holds the yarn double.

### 77_inside_and_out: Inside and out

Wrong result: ERROR.
- Inside out and right side out disagree.
Corrected result: PASS.

How: turning inside out and keeping the right side out disagree.

What: the corrected file turns inside out.

### 78_tight_and_loose: Tight and loose

Wrong result: ERROR.
- One round cannot be worked tightly and loosely.
Corrected result: PASS.

How: one round cannot be worked tightly and loosely.

What: the corrected file works the round tightly.

### 79_same_color: Same color change

Wrong result: ERROR.
- Changing from Color A to Color A is not a color change.
Corrected result: PASS.

How: changing from Color A to Color A is not a color change.

What: the corrected file changes to Color B.

### 80_increase_same: Increase to the same count

Wrong result: ERROR.
- Increase from 12 to 12 does not rise.
- An increase from 12 to 12 does not increase.
Corrected result: PASS.

How: an increase from 12 to 12 does not increase.

What: the corrected file increases from 12 to 18.

### 81_increase_down: Increase that shrinks

Wrong result: ERROR.
- Increase from 12 to 6 does not rise.
- An increase from 12 to 6 shrinks. Call it a decrease, or reverse the numbers.
Corrected result: PASS.

How: an increase from 12 to 6 is a decrease. The word and the numbers disagree.

What: the corrected file increases from 6 to 12.

### 82_decrease_up: Decrease that grows

Wrong result: ERROR.
- Decrease from 6 to 12 does not fall.
- A decrease from 6 to 12 grows. Call it an increase, or reverse the numbers.
Corrected result: PASS.

How: a decrease from 6 to 12 grows. The word and the numbers disagree.

What: the corrected file decreases from 12 to 6.

### 83_chain_counts_twice: Chain counted twice

Wrong result: ERROR.
- A turning chain counted twice is added two times.
Corrected result: PASS.

How: a turning chain counted twice is added to the stitch count two times.

What: the corrected file counts the turning chain once.

### 84_post_around_chain: Post around a chain

Wrong result: ERROR.
- A chain has no post. Do not work fpdc around the chain.
Corrected result: PASS.

How: a chain has no post. fpdc cannot go around the chain.

What: the corrected file works the post around the dc.

### 85_slip_knot_stitch: Slip knot as a stitch

Wrong result: ERROR.
- The slip knot is not a chain stitch.
Corrected result: PASS.

How: the slip knot is not a chain stitch. Do not work into it.

What: the corrected file works into the second chain.

### 86_short_turning_chain: Short turning chain

Wrong result: ERROR.
- ch 1 is too short to turn for a dc. Use ch 3.
Corrected result: PASS.

How: ch 1 is the turning chain for sc, not for dc. A dc turn needs ch 3.

What: the corrected file uses ch 3 before the dc.

### 87_round_uses_across: Round says across

Wrong result: ERROR.
- A round says across. Rounds are worked around.
Corrected result: PASS.

How: a round is worked around. Across is the flat-row word.

What: the corrected file says around.

### 88_row_uses_around: Row says around

Wrong result: ERROR.
- A row says around. Rows are worked across.
Corrected result: PASS.

How: a flat row is worked across. Around is the round word.

What: the corrected file says across.

### 89_round_says_turn: Round says turn

Wrong result: ERROR.
- A round says turn. A continuous round does not turn.
Corrected result: PASS.

How: a continuous round does not turn. Turn belongs to a flat row.

What: the corrected file does not turn.

### 90_backward_range: Backward range

Wrong result: ERROR.
- Rounds 8-5 run backwards.
- Rounds 8-5 run backwards. Write the lower number first.
Corrected result: PASS.

How: Rounds 8-5 run backwards. A range has to climb.

What: the corrected file uses Rounds 5-8.

### 91_not_multiple: Not a multiple

Wrong result: ERROR.
- 10 is not divisible by 3.
- 10 is not a multiple of 3.
Corrected result: PASS.

How: a multiple of 3 cannot be 10 stitches. 10 is not divisible by 3.

What: the corrected file uses 12 stitches.

### 92_odd_when_even: Odd when even

Wrong result: ERROR.
- 7 is odd, but the line says the count must be even.
Corrected result: PASS.

How: a count that must be even cannot be 7.

What: the corrected file uses 8.

### 93_eyes_too_far: Eyes too far apart

Wrong result: ERROR.
- Eyes 8 stitches apart do not fit on a 6-stitch round.
Corrected result: PASS.

How: eyes 8 stitches apart cannot sit on a 6-stitch round.

What: the corrected file places them 4 stitches apart.

### 94_hook_letter_gap: Hook letter gap

Wrong result: ERROR.
- Hook H/8 is written as 2.25 mm, but the Craft Yarn Council nominal size is 5 mm. The gap is more than 1.5 mm.
Corrected result: PASS.

How: H/8 written as 2.25 mm is the B-1 size, not a brand variation. The Craft Yarn Council nominal for H-8 is 5 mm. This fires only when the written millimeter is more than 1.5 mm away.

What: the corrected file uses H/8 (5 mm).

### 95_yarn_weight_number: Yarn weight number

Wrong result: ERROR.
- Worsted is Craft Yarn Council category 4, not 1.
Corrected result: PASS.

How: worsted is Craft Yarn Council category 4, not 1.

What: the corrected file says worsted (4).

### 96_short_treble_turn: Short treble turn

Wrong result: ERROR.
- ch 1 is too short to turn for a tr. Use ch 4.
Corrected result: PASS.

How: ch 1 cannot turn for a treble. A treble turn needs ch 4. ch 2 for a double treble is short as well.

What: the corrected file uses ch 4 before the treble.

### 97_counts_as_mismatch: Counts-as mismatch

Wrong result: ERROR.
- ch 1 cannot count as a dc.
Corrected result: PASS.

How: ch 1 cannot count as a double crochet. A double crochet turning chain is ch 3.

What: the corrected file lets ch 3 count as the dc.

### 98_uk_gloss: UK gloss

Wrong result: ERROR.
- A US single crochet is a UK double, not a UK treble.
Corrected result: PASS.

How: a US single crochet is a UK double, not a UK treble.

What: the corrected file says sc (UK double).

### 99_steel_hook_order: Steel hook order

Wrong result: ERROR.
- A higher steel-hook number is smaller, not larger.
Corrected result: PASS.

How: on a steel hook, a higher number is smaller. Steel 14 is not larger than steel 1.

What: the corrected file says steel 14 is smaller.

### 100_spiral_turn: Spiral turn

Wrong result: ERROR.
- A continuous spiral does not turn every round.
Corrected result: PASS.

How: a continuous spiral does not turn every round.

What: the corrected file keeps the spiral and does not turn.

### 101_fasten_continue: Fasten and continue

Wrong result: ERROR.
- Fasten off ends the yarn.
Corrected result: PASS.

How: fasten off ends that yarn. The same line cannot continue in it.

What: the corrected file fastens off.

### 102_yarn_over_under: Yarn over and under

Wrong result: ERROR.
- Yarn over and yarn under cannot be the same stitch.
Corrected result: PASS.

How: one stitch cannot be both a yarn over and a yarn under.

What: the corrected file uses a yarn over.

### 103_reverse_sc_forward: Reverse sc direction

Wrong result: ERROR.
- Reverse single crochet is worked backward, not forward.
Corrected result: PASS.

How: reverse single crochet is worked backward, not forward.

What: the corrected file works it backward.

### 104_two_foundations: Two foundations

Wrong result: ERROR.
- Foundation single crochet replaces the starting chain.
Corrected result: PASS.

How: foundation single crochet replaces the starting chain for that row.

What: the corrected file starts with foundation sc.

### 105_both_hands: Both hands

Wrong result: ERROR.
- Right-handed and left-handed work need separate instructions.
Corrected result: PASS.

How: right-handed and left-handed work need separate instructions when both are required.

What: the corrected file is written for right-handed work.

### 106_two_starts: Two starts

Wrong result: ERROR.
- A piece cannot start with both a magic ring and a chain ring.
Corrected result: PASS.

How: a piece cannot have both a magic ring and a chain ring as its only start.

What: the corrected file starts with a magic ring.

### 107_two_seams: Two seam methods

Wrong result: ERROR.
- Whipstitch and mattress stitch are two seams.
Corrected result: PASS.

How: whipstitch and mattress stitch are different seams. One line cannot require both for the same seam.

What: the corrected file uses mattress stitch.

### 108_negative_gauge: Negative gauge

Wrong result: ERROR.
- A negative gauge is not a fabric.
Corrected result: PASS.

How: a gauge of -1 sc is not a fabric.

What: the corrected file uses 12 sc per 4 inches.

### 109_negative_length: Negative length

Wrong result: ERROR.
- A negative length is not a piece.
Corrected result: PASS.

How: a finished length of -1 inches is not a piece.

What: the corrected file is 8 inches long.

### 110_zero_rows_tall: Zero rows tall

Wrong result: ERROR.
- A piece that is 0 rows tall was not made.
Corrected result: PASS.

How: a piece that is 0 rows tall was not made.

What: the corrected file is 8 rows tall.

### 111_zero_rounds_tall: Zero rounds tall

Wrong result: ERROR.
- A piece that is 0 rounds tall was not made.
Corrected result: PASS.

How: a piece that is 0 rounds tall was not made.

What: the corrected file is 8 rounds tall.

### 112_row_zero: Row zero

Wrong result: ERROR.
- Row 0 is not a row. Start at Row 1.
- Row 0 is not a row.
Corrected result: PASS.

How: rows are numbered from 1. Row 0 is not a row.

What: the corrected file starts at Row 1.

### 113_make_zero: Make zero

Wrong result: ERROR.
- Make 0 asks for none of that piece.
- make 0 asks for none of that piece.
Corrected result: PASS.

How: make 0 asks for none of that piece.

What: the corrected file makes 2.

### 114_negative_times: Negative times

Wrong result: ERROR.
- -1 times is not a repeat count.
Corrected result: PASS.

How: repeating a row -1 times is not a repeat. This is not the x -1 form.

What: the corrected file repeats the row 4 times.

### 115_work_even_zero: Work even zero

Wrong result: ERROR.
- Work even for 0 rows does no work.
Corrected result: PASS.

How: work even for 0 rows does no work.

What: the corrected file works even for 4 rows.

### 116_place_zero_eyes: Place zero eyes

Wrong result: ERROR.
- Place 0 safety eyes mounts nothing.
Corrected result: PASS.

How: place 0 safety eyes is an instruction that mounts nothing.

What: the corrected file places 2 safety eyes.

### 117_yardage_zero: Zero yardage

Wrong result: ERROR.
- 0 yards cannot make the piece.
Corrected result: PASS.

How: 0 yards cannot make the piece.

What: the corrected file lists 200 yards.

### 118_stuff_zero: Stuff zero

Wrong result: ERROR.
- Stuff with 0 g leaves the piece empty.
- Stuff with 0 g does not stuff the piece.
Corrected result: PASS.

How: stuff with 0 g leaves the piece empty while telling the crocheter to stuff.

What: the corrected file stuffs with 20 g.

### 119_color_every_zero: Color every zero

Wrong result: ERROR.
- Every 0 rows or rounds never happens.
- Change color every 0 rows never changes color.
Corrected result: PASS.

How: changing color every 0 rows never changes color.

What: the corrected file changes color every 2 rows.

### 120_increase_every_zero: Increase every zero

Wrong result: ERROR.
- Every 0 rows or rounds never happens.
- Increase every 0 rounds never increases.
Corrected result: PASS.

How: increasing every 0 rounds never increases.

What: the corrected file increases every 3 rounds.

### 121_decrease_every_zero: Decrease every zero

Wrong result: ERROR.
- Every 0 rows or rounds never happens.
- Decrease every 0 rows never decreases.
Corrected result: PASS.

How: decreasing every 0 rows never decreases.

What: the corrected file decreases every 2 rows.

### 122_v_stitch_one: V-stitch of one

Wrong result: ERROR.
- A V-stitch of 1 is not a V-stitch.
Corrected result: PASS.

How: a V-stitch needs two tall stitches and a chain. A V-stitch of 1 is one stitch.

What: the corrected file uses a V-stitch of 2 dc.

### 123_fan_one: Fan of one

Wrong result: ERROR.
- A fan of 1 is not a fan.
Corrected result: PASS.

How: a fan needs several stitches in one space. A fan of 1 is one stitch.

What: the corrected file uses a fan of 5.

### 124_bullion_zero: Bullion of zero

Wrong result: ERROR.
- A bullion of 0 wraps has no wraps.
Corrected result: PASS.

How: a bullion of 0 wraps has no wraps to coil.

What: the corrected file uses 7 wraps.

### 125_cable_zero: Cable of zero

Wrong result: ERROR.
- A cable over 0 stitches does not cross.
Corrected result: PASS.

How: a cable over 0 stitches does not cross.

What: the corrected file crosses 2 stitches.

### 126_fringe_zero: Fringe of zero

Wrong result: ERROR.
- A fringe of 0 strands is not a fringe.
Corrected result: PASS.

How: a fringe of 0 strands is not a fringe.

What: the corrected file uses 4 strands.

### 127_buttonhole_zero: Buttonhole of zero

Wrong result: ERROR.
- A buttonhole of 0 chains has no opening.
Corrected result: PASS.

How: a buttonhole of 0 chains has no opening.

What: the corrected file uses 3 chains.

### 128_icord_zero: I-cord of zero

Wrong result: ERROR.
- An i-cord of 0 stitches has no cord.
Corrected result: PASS.

How: an i-cord of 0 stitches has no cord.

What: the corrected file uses 4 stitches.

### 129_oval_zero: Oval of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- An oval cannot start with 0 chains.
Corrected result: PASS.

How: an oval cannot start with 0 chains.

What: the corrected file starts with 8 chains.

### 130_square_zero: Square of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- A square of 0 rounds was not worked.
Corrected result: PASS.

How: a square of 0 rounds was not worked.

What: the corrected file has 4 rounds.

### 131_solomon_zero: Solomon knot of zero

Wrong result: ERROR.
- A Solomon knot of 0 is not a knot.
Corrected result: PASS.

How: a Solomon knot of 0 is not a knot.

What: the corrected file uses 5.

### 132_surface_zero: Surface of zero

Wrong result: ERROR.
- Surface crochet of 0 chains draws no line.
Corrected result: PASS.

How: surface crochet of 0 chains draws no line.

What: the corrected file uses 12 chains.

### 133_bead_every_zero: Bead every zero

Wrong result: ERROR.
- A bead every 0 stitches is never placed.
Corrected result: PASS.

How: a bead every 0 stitches is never placed.

What: the corrected file places a bead every 4 stitches.

### 134_stripe_every_zero: Stripe every zero

Wrong result: ERROR.
- Every 0 rows or rounds never happens.
- A stripe every 0 rounds never stripes.
Corrected result: PASS.

How: a stripe every 0 rounds never stripes.

What: the corrected file stripes every 2 rounds.

### 135_pompom_zero: Pom-pom of zero

Wrong result: ERROR.
- A wrap count of 0 has nothing to tie.
- A pom-pom of 0 wraps has nothing to tie.
Corrected result: PASS.

How: a pom-pom of 0 wraps has nothing to tie.

What: the corrected file uses 40 wraps.

### 136_tassel_zero: Tassel of zero

Wrong result: ERROR.
- A wrap count of 0 has nothing to tie.
- A tassel of 0 wraps has nothing to hang.
Corrected result: PASS.

How: a tassel of 0 wraps has nothing to hang.

What: the corrected file uses 40 wraps.

### 137_pineapple_zero: Pineapple of zero

Wrong result: ERROR.
- A pineapple of 0 is not a pineapple motif.
Corrected result: PASS.

How: a pineapple of 0 is not a pineapple motif.

What: the corrected file uses 7.

### 138_spike_zero: Spike of zero

Wrong result: ERROR.
- A spike stitch down 0 rows does not leave the row.
- A spike stitch down 0 rows does not leave the current row.
Corrected result: PASS.

How: a spike stitch down 0 rows does not leave the current row.

What: the corrected file goes down 2 rows.

### 139_tube_zero: Tube of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- A tube of 0 stitches has no opening.
Corrected result: PASS.

How: a tube of 0 stitches has no opening.

What: the corrected file uses 6 stitches.

### 140_rectangle_zero: Rectangle of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- A rectangle of 0 rows was not worked.
Corrected result: PASS.

How: a rectangle of 0 rows was not worked.

What: the corrected file has 12 rows.

### 141_corner_zero: Corner of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- A corner of 0 chains does not turn the corner.
Corrected result: PASS.

How: a corner of 0 chains does not turn the corner.

What: the corrected file uses 2 chains.

### 142_star_one: Star of one

Wrong result: ERROR.
- A star stitch of 1 cannot make a star.
Corrected result: PASS.

How: a star stitch of 1 cannot pull up the loops a star needs.

What: the corrected file uses a star stitch of 5.

### 143_loop_zero: Loop of zero

Wrong result: ERROR.
- A loop stitch of 0 has no loop.
Corrected result: PASS.

How: a loop stitch of 0 has no loop.

What: the corrected file uses 1 loop.

### 144_same_color_letter: Same color letter

Wrong result: ERROR.
- Changing from Color Q to Color Q is not a color change.
Corrected result: PASS.

How: changing from Color Q to Color Q is not a color change. The check is any repeated letter, not only A.

What: the corrected file changes to Color R.

### 145_increase_direction: Increase direction

Wrong result: ERROR.
- Increase from 9 to 4 does not rise.
Corrected result: PASS.

How: any increase whose second number is not higher fails. This is not limited to 12 to 6.

What: the corrected file rises.

### 146_decrease_direction: Decrease direction

Wrong result: ERROR.
- Decrease from 4 to 9 does not fall.
Corrected result: PASS.

How: any decrease whose second number is not lower fails. This is not limited to 6 to 12.

What: the corrected file falls.

### 147_multiple_mismatch: Multiple mismatch

Wrong result: ERROR.
- 6 is not divisible by 4.
Corrected result: PASS.

How: a stated count that is not divisible by the written multiple fails. This is not limited to 3 and 10.

What: the corrected file uses a divisible count.

### 148_plus_remainder: Plus remainder

Wrong result: ERROR.
- 10 is not a multiple of 6 plus 1.
Corrected result: PASS.

How: a count that is not the written multiple plus the written remainder fails.

What: the corrected file uses 13, which is a multiple of 6 plus 1.

### 149_backward_rounds: Backward round range

Wrong result: ERROR.
- Rounds 9-2 run backwards.
Corrected result: PASS.

How: a round range whose first number is higher runs backwards. This is not limited to 8-5.

What: the corrected file puts the lower number first.

### 150_backward_rows: Backward row range

Wrong result: ERROR.
- Rows 9-2 run backwards.
Corrected result: PASS.

How: a row range whose first number is higher runs backwards.

What: the corrected file puts the lower number first.

### 151_even_count: Even count

Wrong result: ERROR.
- 9 is odd, but the line says the count must be even.
Corrected result: PASS.

How: an odd number cannot be required to be even. This is not limited to 7.

What: the corrected file uses an even number.

### 152_odd_count: Odd count

Wrong result: ERROR.
- 8 is even, but the line says the count must be odd.
Corrected result: PASS.

How: an even number cannot be required to be odd.

What: the corrected file uses an odd number.

### 153_apart_span: Apart span

Wrong result: ERROR.
- Eyes 7 stitches apart do not fit on a 5-stitch round.
Corrected result: PASS.

How: eyes farther apart than the round cannot sit on it. This is not limited to 8 on 6.

What: the corrected file places them inside the round.

### 154_stitch_past_end: Stitch past end

Wrong result: ERROR.
- Stitch 9 is past a 4-stitch round.
Corrected result: PASS.

How: a marker past the last stitch cannot be placed.

What: the corrected file uses stitch 1.

### 155_skip_past_count: Skip past count

Wrong result: ERROR.
- Skip 9 does not fit on a 4-stitch row.
Corrected result: PASS.

How: a skip of the whole row or more does not fit.

What: the corrected file skips 1.

### 156_fractional_times: Fractional times

Wrong result: ERROR.
- x 1.5 is not a whole repeat.
Corrected result: PASS.

How: any repeat written as x N.N is not a whole repeat. This is not limited to 2.5.

What: the corrected file repeats a whole number of times.

### 157_copied_inch: Copied inch measure

Wrong result: ERROR.
- 4 inches is not 4 cm. The line copies the same number.
Corrected result: PASS.

How: writing the same number for inches and centimeters is not a conversion. One inch is 2.54 cm.

What: the corrected file converts 4 inches to 10.16 cm.

### 158_copied_cm: Copied centimeter measure

Wrong result: ERROR.
- 10 cm is not 10 inches. The line copies the same number.
Corrected result: PASS.

How: writing the same number for centimeters and inches is not a conversion.

What: the corrected file converts 10 cm to 3.94 inches.

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
| All | Countless cinch, lowercase sew head to body | A cinch with no number closes the last stated round. A lowercase sew line is a piece reference. The viewpoints do not agree on one written pattern, so this is not a lesson. A photo is still not classified. |

## Viewpoint check

These rows are what the checker returned. They are not a vote.

| File | Section | Status | Errors | Warnings | Seen, after dropping abbreviation noise |
|---|---|---|---:|---:|---|
| `wrong_benchmarks.md` | whole file | ERROR | 96 | 9 | Line 121: worked 5 stitches into 15 without a decrease.; Line 220: worked 1 stitch into 48 without a decrease.; Line 221: Attempted to work stitch beyond available loops. Position: 1, Available: 1 |
| `wrong_benchmarks.md` | 1: Classic Amigurumi Bear | ERROR | 4 | 0 | Round/row 9: plain round received 4 stitches and has no increase or decrease, but states 8.; Round 11: 12 stitches jump to 24. Insert an 18-stitch round before returning to 24.; Piece 'arms' is named in assembly but never started. |
| `wrong_benchmarks.md` | 2: Celestial Wyvern | ERROR | 14 | 2 | Line 43: worked 5 stitches into 15 without a decrease.; Round/row 13: stated 30 stitches but operations produce 0; Round/row 1: stated 14 stitches but operations produce 0 |
| `wrong_benchmarks.md` | 3: Clockwork Dragon | ERROR | 13 | 0 | Seam mismatch: 3 stitches cannot close 4 stitches.; Short-row gap: 28 of 34 leaves 6 row-ends unstated.; Round 11 repeats or goes backwards. Number the rounds in order. |
| `wrong_benchmarks.md` | 4: Abyssal Leviathan | ERROR | 45 | 3 | Line 50: worked 1 stitch into 48 without a decrease.; Line 51: Attempted to work stitch beyond available loops. Position: 1, Available: 1; Line 68: Attempted to work stitch beyond available loops. Position: 1, Available: 1 |
| `wrong_benchmarks.md` | 5: Void-Warped Chimera | ERROR | 28 | 4 | Line 38: Attempted to work stitch beyond available loops. Position: 36, Available: 36; Round/row 15: stated 38 stitches but operations produce 36; Round/row 17: stated 32 stitches but operations produce 30 |
| `gemini_corrected.md` | whole file | PASS_WITH_WARNINGS | 0 | 1 | Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
| `gemini_corrected.md` | 1: Classic Amigurumi Bear (Corrected) | PASS | 0 | 0 | none |
| `gemini_corrected.md` | 2: Celestial Wyvern (Corrected) | ERROR | 1 | 0 | Ghost material: '.25 mm hook, polyfill, 12 mm safety eyes (x2), tapestry needle' is listed under Materials but never mentioned in the instructions. |
| `gemini_corrected.md` | 3: Clockwork Dragon (Corrected) | PASS_WITH_WARNINGS | 0 | 1 | Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
| `gemini_corrected.md` | 4: Abyssal Leviathan (Corrected) | ERROR | 1 | 1 | Round/row 15: stated 20 stitches but operations produce 0; Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
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
