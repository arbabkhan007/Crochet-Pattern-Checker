# Synthetic lesson fixture report

This file is rewritten by `scripts/check_consensus.py`. It is the check result, not a fourth pattern.

The three viewpoints stay unedited:

- `docs/wrong_benchmarks.md`
- `docs/gemini_corrected.md`
- `docs/chatgpt_corrected.md`

The mechanical gate requires `wrong.txt` not to be a clean pass and `corrected.txt` to pass with no errors or warnings. This status comparison does not prove that the intended defect was detected or that the answer key is independently correct; those fixture reviews remain open.

## How to read a viewpoint check

A PASS on the Gemini or ChatGPT file is not proof. `[sc 1, inc] 6 times` and a backticked `×` repeat are not the checker's dialect. The counter does not expand them, so a wrong repeat can pass.

An ERROR made only of undefined abbreviations, or of `worked N stitches into` on a prose line, is parser noise. It is not the lesson.

A 12-to-24 shaping step and a greater-than-2x stated-count jump are review warnings, not proof of errors. A confidently parsed simple repeat that consumes more than the preceding verified count is a separate objective stitch-consumption error. Unequal stated seam counts can be mechanically compared; inch-span, gauge, fullness, shaping, fit, and fabric behavior remain advice for review or sample measurements. This generated report records the current checker output on the repository fixtures. It is not independent craft review, a complete coverage metric, or evidence that the rules generalize to real patterns. A photo is still not classified.

## Synthetic lesson checks

These synthetic pairs record current checker behavior. The result table is not a vote, independent craft review, or proof of broad real-pattern coverage; expected findings and answer keys still need independent review.

### 01_stated_count: Stated count

Wrong result: ERROR.
- Round 1 states 16 stitches, but operations produce 14.
Corrected result: PASS.

Fixture explanation (unreviewed): (5 sc, dec) makes 6. Twice is 12. The last 2 sc makes 14. The line consumes 16 and produces 14, so a written 16 is false.

Lesson note (unreviewed): Gemini and ChatGPT both say this line cannot make 16. The consensus repair changes the stated count to 14. It does not rewrite the stitches, because the two files do not agree on a rewrite.

### 02_repeat_cover: Repeat cover

Wrong result: ERROR.
- Round 2 states 32 stitches, but operations produce 30.
- Non-modulo consumption: Round 2 has 38 incoming stitches, but the repeat consumes 6. 2 stitches would be left unworked.
Corrected result: PASS.

Fixture explanation (unreviewed): (4 sc, dec) uses 6 stitches and makes 5. Six repeats use 36 and make 30. Two stitches of the 38 are never written, and 32 is not what those repeats make.

Lesson note (unreviewed): both corrected files agree a decrease repeat must cover the round. The consensus writes the leftover 2 sc and states 32. This is the rule, not a vote on a 38-stitch start versus a 40-stitch start.

### 03_post_foundation: Post foundation

Wrong result: ERROR.
- Post stitch fpdc is worked into a short sc row. Post stitches need a foundation of hdc or taller.
Corrected result: PASS.

Fixture explanation (unreviewed): fpdc has to enter a stitch at least as tall as hdc. The previous round is sc, which is too short. (fpdc) x 6 keeps the count at 6 once the foundation is tall enough.

Lesson note (unreviewed): both corrected files agree. Do not work a post stitch into a short sc round. Change the previous round to hdc.

### 04_ghost_eyes: Ghost eyes

Wrong result: ERROR.
- Ghost material: 'safety eyes' is listed under Materials but never mentioned in the instructions.
Corrected result: PASS.

Fixture explanation (unreviewed): safety eyes are listed under Materials and never appear in the instructions. A materials line is not a placement.

Lesson note (unreviewed): both corrected files agree. Name the eyes in the head instructions, before stuffing. Do not leave them as an unused listing.

### 05_equal_socket: Equal socket

Wrong result: ERROR.
- Gusset Mismatch: Limb holds 3 sts, but body skips 4 sts.
Corrected result: PASS.

Fixture explanation (unreviewed): the body skips 4 stitches and the limb holds 3. A join closes only when those two numbers are equal. Worked plus skipped must also equal the previous body count.

Lesson note (unreviewed): both corrected files agree the seam counts must match. This pair makes them 4 and 4. When a pattern offers 3 and 3 as the other equal choice, that choice stays open.

### 06_edging_fullness: Edging fullness

Wrong result: PASS_WITH_WARNINGS.
- Frill Alert: Edging is 5.5x full (threshold 2.5x). Fabric will bunch severely.
Corrected result: PASS.

Fixture explanation (unreviewed): 70 stitches on 14 row-ends is 5 times the base. With this gauge the checker warns above 2.5 times full.

Lesson note (unreviewed): both corrected files agree 5 times full is too much. The consensus uses one stitch per row-end so the check can pass. A 35-stitch fan and a 42-stitch fan still warn, so neither model's fan is the consensus repair.

### 07_span_match: Span match

Wrong result: PASS_WITH_WARNINGS.
- Span Mismatch: Seam (3.33") and body span (1.69") differ by factor of 2.0x.
Corrected result: PASS.

Fixture explanation (unreviewed): 20 stitches at 24 stitches per 4 inches is 3.33 inches. 11 rounds at 26 rounds per 4 inches is 1.69 inches. The checker warns when those lengths differ by more than 1.25 times.

Lesson note (unreviewed): both corrected files agree those lengths cannot be sewn flat. The consensus matches the counts. A gather sentence is not something this checker can confirm.

### 08_tab_fit: Tab fit

Wrong result: ERROR.
- Spatial fit: Wing tab insertion is 12 stitches, wider than the 6-chain socket.
Corrected result: PASS.

Fixture explanation (unreviewed): the checker reads a skipped chain socket and the next stated tab width. A 12-stitch tab does not fit in a 6-chain socket.

Lesson note (unreviewed): both corrected files agree the tab must not be wider than the socket. Inch sizes in prose are not read. This pair uses stitch counts.

### 09_clause_total: Clause total

Wrong result: ERROR.
- Round 15 states 54 stitches, but operations produce 48.
Corrected result: PASS.

Fixture explanation (unreviewed): the clauses add to 48. Writing 54 does not create the missing 6 stitches.

Lesson note (unreviewed): both corrected files agree 54 is not the sum of those clauses. The consensus changes the stated count to 48. It does not add stitches to build a different join.

### 10_neck_jump: Large shaping step review

Wrong result: PASS_WITH_WARNINGS.
- Round 2: 12 to 24 stitches doubles the count in one round. Review the intended shaping; this check cannot establish the target shape.
Corrected result: PASS.

Fixture explanation (unreviewed): the stated 12-to-24 increase is arithmetically consistent. It is a large shaping step, but the text checker has no swatch or target-shape evidence to prove that it is wrong.

Lesson note (unreviewed): report this as a warning for review, not an objective error and not a requirement to insert an 18-stitch round. The checker cannot establish the intended shape or fit. The corrected example shows one possible progression; it is not the only valid design.

### 11_seam_count: Seam count

Wrong result: ERROR.
- Seam mismatch: 3 stitches cannot close 4 stitches.
- Seam mismatch: 5 stitches cannot close 3 stitches.
- Seam mismatch: 26 stitches cannot close 18 stitches.
Corrected result: PASS.

Fixture explanation (unreviewed): a seam closes only when both edges have the same number of stitches. Sewing 3 to 4, cinching 5 to 3, or sewing a 26-stitch edge to an 18-stitch edge leaves stitches unmatched.

Lesson note (unreviewed): both corrected files agree the counts must match. The checker now reads those sentences. It does not choose 3 and 3 over 4 and 4 when a pattern offers both equal choices.

### 12_inch_span: Inch span

Wrong result: PASS_WITH_WARNINGS.
- Span mismatch: 3.33 inches sewn to 1.69 inches differ by 2.0x.
Corrected result: PASS.

Fixture explanation (unreviewed): 3.33 inches sewn flat to 1.69 inches is about twice as long. The edge puckers unless one side is resized or the pattern says to gather it.

Lesson note (unreviewed): both corrected files agree those lengths cannot be sewn flat. The checker now warns above 1.25 times. Matching the two inch lengths passes. A gather sentence is still not confirmed.

### 13_dialect_scope: Dialect scope

Wrong result: ERROR.
- Head is marked UK, but it uses the US term 'sc'.
Corrected result: PASS.

Fixture explanation (unreviewed): a piece marked UK cannot use sc, and a piece marked US cannot use htr. Two pieces may use different dialects when each one says so.

Lesson note (unreviewed): the corrected file keeps the US term inside the piece marked US. The checker does not treat dc as proof of either dialect, because both countries use that spelling.

### 14_termination: Termination

Wrong result: ERROR.
- This repeat does not terminate. Say the stitch count, the round count, or the length.
Corrected result: PASS.

Fixture explanation (unreviewed): a repeat until a length, a stitch count, or a round count can stop. A repeat until the piece is long enough cannot.

Lesson note (unreviewed): the corrected file gives the repeat a stitch stop. The checker does not invent the missing count.

### 15_reachability: Stitch reachability

Wrong result: ERROR.
- Line 2: worked 1 stitch into 6 without a decrease.
- Stitch 9 is not reachable. The previous round has 6 stitches.
Corrected result: PASS.

Fixture explanation (unreviewed): a later round cannot work the 9th stitch when the previous round has 6. A loop already used on both sides cannot be used again.

Lesson note (unreviewed): the corrected file works each of the 6 stitches. The checker tracks written indexes. It does not build a picture of the fabric.

### 16_references: References

Wrong result: ERROR.
- Round 9 is named but this pattern never starts it.
Corrected result: PASS.

Fixture explanation (unreviewed): join to Round 9 is an error when the pattern never starts Round 9.

Lesson note (unreviewed): the corrected file joins Round 1, which exists. Sew the Ear to the Head, when Ear never starts, is proved by the stage test. A lowercase sentence such as sew head to body is an error when that piece never starts.

### 17_chart_text: Chart text

Wrong result: ERROR.
- Chart row states 4 stitches but the symbols produce 3.
Corrected result: PASS.

Fixture explanation (unreviewed): written chart symbols are counted. X V X is 3 stitches, so a stated 4 is wrong. A chart picture is not read.

Lesson note (unreviewed): the corrected file has four symbols and states 4. The legend in the pattern defines the symbols.

### 18_ambiguity: Ambiguity

Wrong result: ERROR.
- Line 2: worked 1 stitch into 6 without a decrease.
- Round 2 does not say how many stitches to work.
Corrected result: PASS.

Fixture explanation (unreviewed): sc in next st, with no count and no around or across, does not say how many stitches to work.

Lesson note (unreviewed): the corrected file says each stitch around and states the count. This is a written rule, not a language model.

### 19_gauge_band: Gauge band

Wrong result: PASS_WITH_WARNINGS.
- Gauge 40 stitches per 4 inches is outside the Craft Yarn Council crochet band for worsted (11-14). This is a published-range check, not a trained model.
Corrected result: PASS.

Fixture explanation (unreviewed): 40 single crochet per 4 inches is far outside the Craft Yarn Council crochet band for worsted, which is 11 to 14. A count inside half to double that band does not warn.

Lesson note (unreviewed): the corrected file uses 12, inside the published band. This is not a trained gauge model. Tight amigurumi gauges such as 20 per 4 inches do not warn.

### 20_short_row_gap: Short-row gap

Wrong result: ERROR.
- Short-row gap: 28 of 34 leaves 6 row-ends unstated.
Corrected result: PASS.

Fixture explanation (unreviewed): short rows that work 28 of 34 perimeter stitches leave 6 row-ends. Those row-ends must be written. The checker does not invent them.

Lesson note (unreviewed): the corrected file states the 6 row-ends. A cinch with no number closes the last stated round.

### 21_prose_frill: Prose frill

Wrong result: PASS_WITH_WARNINGS.
- Prose frill: 756 stitches worked into 108 base stitches is 7.0x full. Above 2.5x the edge bunches.
Corrected result: PASS.

Fixture explanation (unreviewed): 756 stitches worked into 108 base stitches is 7 times full. The edge bunches above 2.5 times. This is a warning, not an error.

Lesson note (unreviewed): the corrected file works one stitch into each base stitch. A cinch with no number closes the last stated round.

### 22_eyes_on_frill: Eyes on a frill

Wrong result: ERROR.
- Safety eyes are mounted on the frill. A frill has no fabric behind it for the washer. Mount them on a solid single-crochet round.
Corrected result: PASS.

Fixture explanation (unreviewed): a safety eye mounted on a frill has no solid fabric behind it for the washer. The eye cannot lock.

Lesson note (unreviewed): the corrected file mounts the eyes on a solid single-crochet round and says not on the frill. A cinch with no number closes the last stated round.

### 23_closed_join: Closed join

Wrong result: ERROR.
- A closed tentacle has no live stitches to join. Leave an open edge and state how many stitches it holds.
Corrected result: PASS.

Fixture explanation (unreviewed): a closed tentacle has no live stitches. Joining 3 stitches of it cannot work.

Lesson note (unreviewed): the corrected file joins an open edge. A cinch with no sew-flat sentence closes the last stated round.

### 24_flat_cap: Flat cap

Wrong result: ERROR.
- Cinch shut has no counted round to close. State the round count before the cinch.
- A cinched round is a sealed cap. It cannot be sewn flat. Leave the last round open.
- A seam cannot target a closed magic ring or a cinched point. Leave an open edge and state its stitch count. The join was not invented.
Corrected result: PASS.

Fixture explanation (unreviewed): a round that is cinched shut is a sealed cap. It cannot also be sewn flat.

Lesson note (unreviewed): the corrected file leaves the last round open. Cinch shut by itself closes the last stated round. It is an error when no counted round comes before it.

### 25_chain_underside: Chain underside

Wrong result: ERROR.
- Chain underside missing: ch 3 is crossed once, but 30 counts both sides.
Corrected result: PASS.

Fixture explanation (unreviewed): sc 12, ch 3, sc 12, sc 3 across ch is 27 if the chain is crossed once. A stated 30 needs the underside as well.

Lesson note (unreviewed): the corrected file writes both sides of the chain. The checker does not invent the missing 3 stitches.

### 26_dropped_body: Dropped body stitches

Wrong result: ERROR.
- Dropped body stitches: 21 worked from 24 leaves 3 unwritten. Write the skip, or work the full count.
Corrected result: PASS.

Fixture explanation (unreviewed): 21 stitches worked from a 24-stitch body leave 3 stitches unwritten unless the skip is written.

Lesson note (unreviewed): the corrected file says skip 3. Working the full 24 would also pass.

### 27_front_back_post: Front and back post

Wrong result: ERROR.
- A back post in the front loop turns the ridge inward. Use a front post if the ridge should show.
Corrected result: PASS.

Fixture explanation (unreviewed): a back post in the front loop turns the ridge to the inside, where it cannot be seen.

Lesson note (unreviewed): the corrected file uses a front post. A quoted original line is not treated as an instruction.

### 28_eyes_before_stuff: Eyes before stuffing

Wrong result: ERROR.
- This piece: safety eyes are placed after stuffing. Insert them before the piece is stuffed.
Corrected result: PASS.

Fixture explanation (unreviewed): safety eyes placed after the head is stuffed have no opening for the washer.

Lesson note (unreviewed): the corrected file inserts the eyes before stuffing. A piece that never mentions eyes is not this rule.

### 29_row_end_density: Row-end density

Wrong result: PASS_WITH_WARNINGS.
- Row-end density: 5 stitches in each row end is above 3. The edge will bunch.
Corrected result: PASS.

Fixture explanation (unreviewed): 5 stitches in each row end is more than 3. The edge bunches. This is a warning.

Lesson note (unreviewed): the corrected file works one single crochet in each row end. Two or three would also pass.

### 30_incoming_cover: Incoming cover

Wrong result: ERROR.
- Incoming cover: the repeat uses 42 of 44 stitches. 2 are unaccounted for.
Corrected result: PASS.

Fixture explanation (unreviewed): (5 sc, dec) x 6 uses 42 stitches. Written on 44, it leaves 2 unaccounted for.

Lesson note (unreviewed): the corrected file says on 42 stitches, which is what the repeat uses.

### 31_missing_color: Missing color

Wrong result: ERROR.
- Color B is used but the yarn line never lists it.
Corrected result: PASS.

Fixture explanation (unreviewed): Color B is used, but the yarn line lists only Color A.

Lesson note (unreviewed): the corrected file lists Color B before it is used. A fragment with no color list is not this rule.

### 32_round_order: Round order

Wrong result: ERROR.
- Round 2 repeats or goes backwards. Number the rounds in order.
Corrected result: PASS.

Fixture explanation (unreviewed): Round 2 is written twice. The second one repeats a number that already passed.

Lesson note (unreviewed): the corrected file continues at Round 3. A new piece may start again at Round 1.

### 33_every_base: Every base stitch

Wrong result: PASS_WITH_WARNINGS.
- Every base stitch is worked 5 times. Above 2.5x the fabric bunches.
Corrected result: PASS.

Fixture explanation (unreviewed): 5 stitches worked into every base stitch is above 2.5 times. The fabric bunches. This is a warning.

Lesson note (unreviewed): the corrected file works 1 stitch into every base stitch.

### 34_chain_length: Chain length

Wrong result: ERROR.
- Row 1 states 12 stitches, but operations produce 9.
- Chain of 10 cannot hold 12 stitches. The most this line can hold is 9.
Corrected result: PASS.

Fixture explanation (unreviewed): a chain of 10, started in the second chain, can hold 9 stitches. A stated 12 does not fit.

Lesson note (unreviewed): the corrected file states 9. The checker does not add the missing chains.

### 35_unclosed_repeat: Unclosed repeat

Wrong result: ERROR.
- Line 3: worked 3 stitches into 12 without a decrease.
- Round 3 states 18 stitches, but operations produce 3.
- Round 3 has an unclosed parenthesis. Close the repeat.
Corrected result: PASS.

Fixture explanation (unreviewed): a round whose parentheses do not balance cannot be repeated as written.

Lesson note (unreviewed): the corrected file closes the repeat. The stitch count is the same 18.

### 36_missing_star: Missing star

Wrong result: ERROR.
- Rep from * has no opening star. Mark the start of the repeat with *.
Corrected result: PASS.

Fixture explanation (unreviewed): rep from * needs an opening star. One star at the end does not mark the start.

Lesson note (unreviewed): the corrected file marks *sc, inc* before rep from *.

### 37_decrease_cover: Decrease cover

Wrong result: ERROR.
- Decrease cover: dec x 5 uses 10 stitches, not 11.
Corrected result: PASS.

Fixture explanation (unreviewed): dec x 5 uses 10 stitches. Written on 11, one stitch is unaccounted for.

Lesson note (unreviewed): the corrected file says on 10 stitches, which is what the decrease uses.

### 38_over_double: Repeat overconsumption and large-increase review

Wrong result: ERROR.
- Line 2: this round consumes 12 stitches, but only 6 are available from the previous round; 6 extra stitches are requested.
- Line 2: Round 2 jumps from 6 to 18. More than doubling is a large increase; verify the shaping and count.
Corrected result: PASS.

Fixture explanation (unreviewed): `(sc, inc) x 6` consumes 12 input stitches, while the preceding round produces 6. That repeat cannot be worked as written. The separate 6-to-18 ratio message is a warning, not proof that an intermediate size is required.

Lesson note (unreviewed): this pair demonstrates only the objectively checkable repeat-consumption conflict. A greater-than-2x stated-count jump by itself remains a review warning; the checker does not prescribe shaping or fit.

### 39_written_as: Written-as count

Wrong result: ERROR.
- Written count 38 does not match the 30-stitch edge.
Corrected result: PASS.

Fixture explanation (unreviewed): a 30-stitch edge written as 38 does not close. The two numbers are on the same line.

Lesson note (unreviewed): the corrected file writes 30. The checker does not pick 38 over 30.

### 40_eye_count: Eye count

Wrong result: ERROR.
- Eye count: materials list 2 safety eyes, but the instructions place 4.
Corrected result: PASS.

Fixture explanation (unreviewed): materials list 2 safety eyes and the instructions place 4. The washer count cannot match.

Lesson note (unreviewed): the corrected file places 2. Counts are compared only inside the same pattern section.

### 41_future_round: Future round

Wrong result: ERROR.
- Round 2 works into Round 5, which has not been made yet.
Corrected result: PASS.

Fixture explanation (unreviewed): Round 2 cannot work into Round 5. That round has not been made.

Lesson note (unreviewed): the corrected file works into Round 5 only after Round 5 exists.

### 42_make_count: Make count

Wrong result: ERROR.
- Make count: ears is made 2 times, but the line uses 3.
Corrected result: PASS.

Fixture explanation (unreviewed): Ears (make 2) cannot be sewn as 3 ears. The made count and the sewn count disagree.

Lesson note (unreviewed): the corrected file sews 2 ears. A sew line that does not give a number is named. The count is not guessed.

### 43_zero_repeat: Zero repeat

Wrong result: ERROR.
- A repeat of zero does no work. Give the repeat a count above zero.
- A repeat of 0 does no work.
Corrected result: PASS.

Fixture explanation (unreviewed): a repeat of zero does no work. The instruction cannot be followed as a repeat.

Lesson note (unreviewed): the corrected file repeats 6 times.

### 44_hook_zero: Zero hook

Wrong result: ERROR.
- A hook of 0 mm cannot make a stitch.
Corrected result: PASS.

Fixture explanation (unreviewed): a hook of 0 mm cannot pull up a loop.

Lesson note (unreviewed): the corrected file uses a 5 mm hook.

### 45_hook_huge: Huge hook

Wrong result: PASS_WITH_WARNINGS.
- A hook of 40 mm or more is past normal crochet. This is a warning.
Corrected result: PASS.

Fixture explanation (unreviewed): a 40 mm hook is past even jumbo crochet. This warns.

Lesson note (unreviewed): the corrected file uses a 6 mm hook.

### 46_hook_cm: Hook in centimeters

Wrong result: ERROR.
- The hook is written in centimeters. Crochet hooks are written in millimeters.
Corrected result: PASS.

Fixture explanation (unreviewed): a hook written as 5 cm is 50 mm. Crochet hooks are written in millimeters.

Lesson note (unreviewed): the corrected file says 5 mm.

### 47_chain_zero: Zero chain

Wrong result: ERROR.
- ch 0 makes no chain.
Corrected result: PASS.

Fixture explanation (unreviewed): ch 0 makes no chain to work into.

Lesson note (unreviewed): the corrected file chains 4.

### 48_work_zero: Work zero

Wrong result: ERROR.
- Work 0 stitches does no work.
Corrected result: PASS.

Fixture explanation (unreviewed): work 0 stitches is an instruction that does nothing.

Lesson note (unreviewed): the corrected file works 6 stitches.

### 49_skip_zero: Skip zero

Wrong result: ERROR.
- Skip 0 does not move the hook.
Corrected result: PASS.

Fixture explanation (unreviewed): skip 0 does not move the hook.

Lesson note (unreviewed): the corrected file skips 2.

### 50_decrease_to_zero: Decrease to zero

Wrong result: ERROR.
- Decrease to 0 stitches leaves nothing to fasten.
Corrected result: PASS.

Fixture explanation (unreviewed): decreasing to 0 stitches leaves nothing to fasten or sew.

Lesson note (unreviewed): the corrected file decreases to 6 stitches.

### 51_until_zero: Until zero

Wrong result: ERROR.
- Repeat until 0 stitches is not a workable stop.
Corrected result: PASS.

Fixture explanation (unreviewed): repeat until 0 stitches is not a workable stop. A digit of 0 still counts as written, so the termination rule does not catch it.

Lesson note (unreviewed): the corrected file stops at 6 stitches.

### 52_round_zero: Round zero

Wrong result: ERROR.
- Round 0 is not a round. Start at Round 1.
Corrected result: PASS.

Fixture explanation (unreviewed): rounds are numbered from 1. Round 0 is not a round.

Lesson note (unreviewed): the corrected file starts at Round 1.

### 53_marker_zero: Marker at zero

Wrong result: ERROR.
- Stitch 0 does not exist. Place the marker in stitch 1 or later.
Corrected result: PASS.

Fixture explanation (unreviewed): stitch 0 does not exist. The first stitch is stitch 1.

Lesson note (unreviewed): the corrected file places the marker in stitch 1.

### 54_gauge_zero: Zero gauge

Wrong result: ERROR.
- A gauge of 0 sc is not a fabric.
Corrected result: PASS.

Fixture explanation (unreviewed): a gauge of 0 sc per 4 inches is not a fabric.

Lesson note (unreviewed): the corrected file uses 12 sc per 4 inches.

### 55_zero_inches: Zero inches

Wrong result: ERROR.
- A finished width of 0 inches is not a piece.
Corrected result: PASS.

Fixture explanation (unreviewed): a finished width of 0 inches is not a piece.

Lesson note (unreviewed): the corrected file is 4 inches wide.

### 56_picot_zero: Picot of zero

Wrong result: ERROR.
- A picot of 0 is not a picot.
Corrected result: PASS.

Fixture explanation (unreviewed): a picot of 0 chains is not a picot.

Lesson note (unreviewed): the corrected file uses a picot of 3.

### 57_ch0_space: Chain-zero space

Wrong result: ERROR.
- A ch-0 space has no chains to work into.
Corrected result: PASS.

Fixture explanation (unreviewed): a ch-0 space has no chains to work into.

Lesson note (unreviewed): the corrected file uses a ch-2 space.

### 58_shell_one: Shell of one

Wrong result: ERROR.
- A shell of 1 is not a shell. Use at least 3 stitches.
Corrected result: PASS.

Fixture explanation (unreviewed): a shell needs at least 3 stitches. A shell of 1 is a single stitch.

Lesson note (unreviewed): the corrected file uses a shell of 5.

### 59_cluster_one: Cluster of one

Wrong result: ERROR.
- A 1-dc cluster is one stitch, not a cluster.
Corrected result: PASS.

Fixture explanation (unreviewed): a 1-dc cluster is one double crochet, not a cluster.

Lesson note (unreviewed): the corrected file uses a 3-dc cluster.

### 60_bobble_one: Bobble of one

Wrong result: ERROR.
- A bobble of 1 has nothing to gather.
Corrected result: PASS.

Fixture explanation (unreviewed): a bobble of 1 has no stitches to gather.

Lesson note (unreviewed): the corrected file uses a bobble of 5.

### 61_puff_one: Puff of one

Wrong result: ERROR.
- A puff of 1 is not a puff.
Corrected result: PASS.

Fixture explanation (unreviewed): a puff of 1 is one yarn over, not a puff.

Lesson note (unreviewed): the corrected file uses a puff of 5.

### 62_popcorn_one: Popcorn of one

Wrong result: ERROR.
- A popcorn of 1 cannot be closed.
Corrected result: PASS.

Fixture explanation (unreviewed): a popcorn of 1 cannot be folded closed.

Lesson note (unreviewed): the corrected file uses a popcorn of 5.

### 63_yarn_over_zero: Zero yarn over

Wrong result: ERROR.
- yo 0 does not put yarn on the hook.
Corrected result: PASS.

Fixture explanation (unreviewed): yo 0 does not put yarn on the hook.

Lesson note (unreviewed): the corrected file uses yo 2.

### 64_pull_zero: Pull through zero

Wrong result: ERROR.
- Pull through 0 loops leaves the loops on the hook.
Corrected result: PASS.

Fixture explanation (unreviewed): pull through 0 loops leaves the loops on the hook.

Lesson note (unreviewed): the corrected file pulls through 2 loops.

### 65_decimal_stitch: Decimal stitch

Wrong result: ERROR.
- 6.5 sc is not a whole stitch.
- A decimal stitch is not a whole stitch.
Corrected result: PASS.

Fixture explanation (unreviewed): 6.5 sc is not a whole stitch. The hook cannot make half a single crochet.

Lesson note (unreviewed): the corrected file works 6 sc.

### 66_fraction_repeat: Fractional repeat

Wrong result: ERROR.
- x 2.5 is not a whole repeat.
- A fractional repeat is not a whole repeat.
Corrected result: PASS.

Fixture explanation (unreviewed): x 2.5 asks for half of a repeat. Repeats are whole numbers.

Lesson note (unreviewed): the corrected file repeats 3 times.

### 67_negative_repeat: Negative repeat

Wrong result: ERROR.
- A negative repeat count is not a repeat.
Corrected result: PASS.

Fixture explanation (unreviewed): x -1 is not a repeat count.

Lesson note (unreviewed): the corrected file repeats 4 times.

### 68_round_huge: Round 9000

Wrong result: ERROR.
- Round 9000 is not a usable round number.
Corrected result: PASS.

Fixture explanation (unreviewed): Round 9000 is not a usable round number in this pattern.

Lesson note (unreviewed): the corrected file says Round 9.

### 69_join_contradiction: Join contradiction

Wrong result: ERROR.
- The line says to join and not to join.
Corrected result: PASS.

Fixture explanation (unreviewed): the same line says to join and not to join.

Lesson note (unreviewed): the corrected file joins with a slip stitch.

### 70_spiral_and_join: Spiral and join

Wrong result: ERROR.
- A continuous spiral does not join every round. The join was not added.
- A continuous spiral cannot also join every round.
Corrected result: PASS.

Fixture explanation (unreviewed): a continuous spiral does not join every round. The two instructions disagree.

Lesson note (unreviewed): the corrected file keeps the spiral and says not to join.

### 71_blo_and_both: Both loop claims

Wrong result: ERROR.
- FLO and BLO cannot be the same stitch.
- BLO only and both loops cannot be the same stitch.
Corrected result: PASS.

Fixture explanation (unreviewed): BLO only and both loops cannot be the same stitch.

Lesson note (unreviewed): the corrected file keeps BLO only.

### 72_inc_and_dec: Increase and decrease

Wrong result: ERROR.
- inc and dec in each stitch contradict each other.
Corrected result: PASS.

Fixture explanation (unreviewed): inc and dec in each stitch cancel, and the line does not say which one.

Lesson note (unreviewed): the corrected file increases in each stitch.

### 73_both_directions: Both directions

Wrong result: ERROR.
- The line gives both directions and does not say or.
Corrected result: PASS.

Fixture explanation (unreviewed): left to right and right to left, with no or, gives two directions.

Lesson note (unreviewed): the corrected file works left to right.

### 74_two_joins: Two joins

Wrong result: ERROR.
- An invisible join and a slip-stitch join are two endings. The extra join was not invented.
- An invisible join and a slip-stitch join cannot both finish the round.
Corrected result: PASS.

Fixture explanation (unreviewed): an invisible join and a slip-stitch join are two finishes. The line requires both.

Lesson note (unreviewed): the corrected file uses the invisible join.

### 75_both_sides_facing: Both sides facing

Wrong result: ERROR.
- The right side and the wrong side cannot both face the worker.
Corrected result: PASS.

Fixture explanation (unreviewed): the right side and the wrong side cannot both face the worker.

Lesson note (unreviewed): the corrected file keeps the right side facing.

### 76_yarn_double_single: Double and single

Wrong result: ERROR.
- The yarn cannot be held double and single at the same time.
Corrected result: PASS.

Fixture explanation (unreviewed): the yarn cannot be held double and single at the same time.

Lesson note (unreviewed): the corrected file holds the yarn double.

### 77_inside_and_out: Inside and out

Wrong result: ERROR.
- Inside out and right side out disagree.
Corrected result: PASS.

Fixture explanation (unreviewed): turning inside out and keeping the right side out disagree.

Lesson note (unreviewed): the corrected file turns inside out.

### 78_tight_and_loose: Tight and loose

Wrong result: ERROR.
- One round cannot be worked tightly and loosely.
Corrected result: PASS.

Fixture explanation (unreviewed): one round cannot be worked tightly and loosely.

Lesson note (unreviewed): the corrected file works the round tightly.

### 79_same_color: Same color change

Wrong result: ERROR.
- Changing from Color A to Color A is not a color change.
Corrected result: PASS.

Fixture explanation (unreviewed): changing from Color A to Color A is not a color change.

Lesson note (unreviewed): the corrected file changes to Color B.

### 80_increase_same: Increase to the same count

Wrong result: ERROR.
- Increase from 12 to 12 does not rise.
- An increase from 12 to 12 does not increase.
Corrected result: PASS.

Fixture explanation (unreviewed): an increase from 12 to 12 does not increase.

Lesson note (unreviewed): the corrected file increases from 12 to 18.

### 81_increase_down: Increase that shrinks

Wrong result: ERROR.
- Increase from 12 to 6 does not rise.
- An increase from 12 to 6 shrinks. Call it a decrease, or reverse the numbers.
Corrected result: PASS.

Fixture explanation (unreviewed): an increase from 12 to 6 is a decrease. The word and the numbers disagree.

Lesson note (unreviewed): the corrected file increases from 6 to 12.

### 82_decrease_up: Decrease that grows

Wrong result: ERROR.
- Decrease from 6 to 12 does not fall.
- A decrease from 6 to 12 grows. Call it an increase, or reverse the numbers.
Corrected result: PASS.

Fixture explanation (unreviewed): a decrease from 6 to 12 grows. The word and the numbers disagree.

Lesson note (unreviewed): the corrected file decreases from 12 to 6.

### 83_chain_counts_twice: Chain counted twice

Wrong result: ERROR.
- A turning chain counted twice is added two times.
Corrected result: PASS.

Fixture explanation (unreviewed): a turning chain counted twice is added to the stitch count two times.

Lesson note (unreviewed): the corrected file counts the turning chain once.

### 84_post_around_chain: Post around a chain

Wrong result: ERROR.
- A chain has no post. Do not work fpdc around the chain.
- A chain has no post. Do not work a post around the chain.
Corrected result: PASS.

Fixture explanation (unreviewed): a chain has no post. fpdc cannot go around the chain.

Lesson note (unreviewed): the corrected file works the post around the dc.

### 85_slip_knot_stitch: Slip knot as a stitch

Wrong result: ERROR.
- The slip knot is not a chain stitch.
Corrected result: PASS.

Fixture explanation (unreviewed): the slip knot is not a chain stitch. Do not work into it.

Lesson note (unreviewed): the corrected file works into the second chain.

### 86_short_turning_chain: Short turning chain

Wrong result: ERROR.
- ch 1 is too short to turn for a dc. Use ch 3.
Corrected result: PASS.

Fixture explanation (unreviewed): ch 1 is the turning chain for sc, not for dc. A dc turn needs ch 3.

Lesson note (unreviewed): the corrected file uses ch 3 before the dc.

### 87_round_uses_across: Round says across

Wrong result: ERROR.
- A round says across. Rounds are worked around.
Corrected result: PASS.

Fixture explanation (unreviewed): a round is worked around. Across is the flat-row word.

Lesson note (unreviewed): the corrected file says around.

### 88_row_uses_around: Row says around

Wrong result: ERROR.
- A row says around. Rows are worked across.
Corrected result: PASS.

Fixture explanation (unreviewed): a flat row is worked across. Around is the round word.

Lesson note (unreviewed): the corrected file says across.

### 89_round_says_turn: Round says turn

Wrong result: ERROR.
- A round says turn. A continuous round does not turn.
Corrected result: PASS.

Fixture explanation (unreviewed): a continuous round does not turn. Turn belongs to a flat row.

Lesson note (unreviewed): the corrected file does not turn.

### 90_backward_range: Backward range

Wrong result: ERROR.
- Rounds 8-5 run backwards.
- Rounds 8-5 run backwards. Write the lower number first.
Corrected result: PASS.

Fixture explanation (unreviewed): Rounds 8-5 run backwards. A range has to climb.

Lesson note (unreviewed): the corrected file uses Rounds 5-8.

### 91_not_multiple: Not a multiple

Wrong result: ERROR.
- 10 is not divisible by 3.
- 10 is not a multiple of 3.
Corrected result: PASS.

Fixture explanation (unreviewed): a multiple of 3 cannot be 10 stitches. 10 is not divisible by 3.

Lesson note (unreviewed): the corrected file uses 12 stitches.

### 92_odd_when_even: Odd when even

Wrong result: ERROR.
- 7 is odd, but the line says the count must be even.
Corrected result: PASS.

Fixture explanation (unreviewed): a count that must be even cannot be 7.

Lesson note (unreviewed): the corrected file uses 8.

### 93_eyes_too_far: Eyes too far apart

Wrong result: ERROR.
- Eyes 8 stitches apart do not fit on a 6-stitch round.
Corrected result: PASS.

Fixture explanation (unreviewed): eyes 8 stitches apart cannot sit on a 6-stitch round.

Lesson note (unreviewed): the corrected file places them 4 stitches apart.

### 94_hook_letter_gap: Hook letter gap

Wrong result: ERROR.
- Hook H/8 is written as 2.25 mm, but the Craft Yarn Council nominal size is 5 mm. The gap is more than 1.5 mm.
Corrected result: PASS.

Fixture explanation (unreviewed): H/8 written as 2.25 mm is the B-1 size, not a brand variation. The Craft Yarn Council nominal for H-8 is 5 mm. This fires only when the written millimeter is more than 1.5 mm away.

Lesson note (unreviewed): the corrected file uses H/8 (5 mm).

### 95_yarn_weight_number: Yarn weight number

Wrong result: ERROR.
- Worsted is Craft Yarn Council category 4, not 1.
Corrected result: PASS.

Fixture explanation (unreviewed): worsted is Craft Yarn Council category 4, not 1.

Lesson note (unreviewed): the corrected file says worsted (4).

### 96_short_treble_turn: Short treble turn

Wrong result: ERROR.
- ch 1 is too short to turn for a tr. Use ch 4.
Corrected result: PASS.

Fixture explanation (unreviewed): ch 1 cannot turn for a treble. A treble turn needs ch 4. ch 2 for a double treble is short as well.

Lesson note (unreviewed): the corrected file uses ch 4 before the treble.

### 97_counts_as_mismatch: Counts-as mismatch

Wrong result: ERROR.
- ch 1 cannot count as a dc.
Corrected result: PASS.

Fixture explanation (unreviewed): ch 1 cannot count as a double crochet. A double crochet turning chain is ch 3.

Lesson note (unreviewed): the corrected file lets ch 3 count as the dc.

### 98_uk_gloss: UK gloss

Wrong result: ERROR.
- A US single crochet is a UK double, not a UK treble.
Corrected result: PASS.

Fixture explanation (unreviewed): a US single crochet is a UK double, not a UK treble.

Lesson note (unreviewed): the corrected file says sc (UK double).

### 99_steel_hook_order: Steel hook order

Wrong result: ERROR.
- A higher steel-hook number is smaller, not larger.
Corrected result: PASS.

Fixture explanation (unreviewed): on a steel hook, a higher number is smaller. Steel 14 is not larger than steel 1.

Lesson note (unreviewed): the corrected file says steel 14 is smaller.

### 100_spiral_turn: Spiral turn

Wrong result: ERROR.
- A continuous spiral does not turn every round.
Corrected result: PASS.

Fixture explanation (unreviewed): a continuous spiral does not turn every round.

Lesson note (unreviewed): the corrected file keeps the spiral and does not turn.

### 101_fasten_continue: Fasten and continue

Wrong result: ERROR.
- Fasten off ends the yarn.
- Fasten off ends the yarn. The same yarn was not continued.
Corrected result: PASS.

Fixture explanation (unreviewed): fasten off ends that yarn. The same line cannot continue in it.

Lesson note (unreviewed): the corrected file fastens off.

### 102_yarn_over_under: Yarn over and under

Wrong result: ERROR.
- Yarn over and yarn under cannot be the same stitch.
Corrected result: PASS.

Fixture explanation (unreviewed): one stitch cannot be both a yarn over and a yarn under.

Lesson note (unreviewed): the corrected file uses a yarn over.

### 103_reverse_sc_forward: Reverse sc direction

Wrong result: ERROR.
- Reverse single crochet is worked backward, not forward.
Corrected result: PASS.

Fixture explanation (unreviewed): reverse single crochet is worked backward, not forward.

Lesson note (unreviewed): the corrected file works it backward.

### 104_two_foundations: Two foundations

Wrong result: ERROR.
- Foundation single crochet replaces the starting chain.
Corrected result: PASS.

Fixture explanation (unreviewed): foundation single crochet replaces the starting chain for that row.

Lesson note (unreviewed): the corrected file starts with foundation sc.

### 105_both_hands: Both hands

Wrong result: ERROR.
- Right-handed and left-handed work need separate instructions.
Corrected result: PASS.

Fixture explanation (unreviewed): right-handed and left-handed work need separate instructions when both are required.

Lesson note (unreviewed): the corrected file is written for right-handed work.

### 106_two_starts: Two starts

Wrong result: ERROR.
- A piece cannot start with both a magic ring and a chain ring.
Corrected result: PASS.

Fixture explanation (unreviewed): a piece cannot have both a magic ring and a chain ring as its only start.

Lesson note (unreviewed): the corrected file starts with a magic ring.

### 107_two_seams: Two seam methods

Wrong result: ERROR.
- Whipstitch and mattress stitch are two seams. The extra seam was not invented.
- Whipstitch and mattress stitch are two seams.
Corrected result: PASS.

Fixture explanation (unreviewed): whipstitch and mattress stitch are different seams. One line cannot require both for the same seam.

Lesson note (unreviewed): the corrected file uses mattress stitch.

### 108_negative_gauge: Negative gauge

Wrong result: ERROR.
- A negative measure is not a size. No length was invented.
- A negative gauge is not a fabric.
Corrected result: PASS.

Fixture explanation (unreviewed): a gauge of -1 sc is not a fabric.

Lesson note (unreviewed): the corrected file uses 12 sc per 4 inches.

### 109_negative_length: Negative length

Wrong result: ERROR.
- A negative measure is not a size. No length was invented.
- A negative length is not a piece.
Corrected result: PASS.

Fixture explanation (unreviewed): a finished length of -1 inches is not a piece.

Lesson note (unreviewed): the corrected file is 8 inches long.

### 110_zero_rows_tall: Zero rows tall

Wrong result: ERROR.
- A piece that is 0 rows tall was not made.
Corrected result: PASS.

Fixture explanation (unreviewed): a piece that is 0 rows tall was not made.

Lesson note (unreviewed): the corrected file is 8 rows tall.

### 111_zero_rounds_tall: Zero rounds tall

Wrong result: ERROR.
- A piece that is 0 rounds tall was not made.
Corrected result: PASS.

Fixture explanation (unreviewed): a piece that is 0 rounds tall was not made.

Lesson note (unreviewed): the corrected file is 8 rounds tall.

### 112_row_zero: Row zero

Wrong result: ERROR.
- Row 0 is not a row. Start at Row 1.
- Row 0 is not a row.
Corrected result: PASS.

Fixture explanation (unreviewed): rows are numbered from 1. Row 0 is not a row.

Lesson note (unreviewed): the corrected file starts at Row 1.

### 113_make_zero: Make zero

Wrong result: ERROR.
- Make 0 asks for none of that piece.
- make 0 asks for none of that piece.
Corrected result: PASS.

Fixture explanation (unreviewed): make 0 asks for none of that piece.

Lesson note (unreviewed): the corrected file makes 2.

### 114_negative_times: Negative times

Wrong result: ERROR.
- -1 times is not a repeat count.
- A negative repeat count is not a repeat.
- A negative round or row number is not a round. Start at 1.
Corrected result: PASS.

Fixture explanation (unreviewed): repeating a row -1 times is not a repeat. This is not the x -1 form.

Lesson note (unreviewed): the corrected file repeats the row 4 times.

### 115_work_even_zero: Work even zero

Wrong result: ERROR.
- Work even for 0 rows does no work.
Corrected result: PASS.

Fixture explanation (unreviewed): work even for 0 rows does no work.

Lesson note (unreviewed): the corrected file works even for 4 rows.

### 116_place_zero_eyes: Place zero eyes

Wrong result: ERROR.
- Place 0 safety eyes mounts nothing.
Corrected result: PASS.

Fixture explanation (unreviewed): place 0 safety eyes is an instruction that mounts nothing.

Lesson note (unreviewed): the corrected file places 2 safety eyes.

### 117_yardage_zero: Zero yardage

Wrong result: ERROR.
- 0 yards cannot make the piece.
Corrected result: PASS.

Fixture explanation (unreviewed): 0 yards cannot make the piece.

Lesson note (unreviewed): the corrected file lists 200 yards.

### 118_stuff_zero: Stuff zero

Wrong result: ERROR.
- Stuff with 0 g leaves the piece empty.
- Stuff with 0 g does not stuff the piece.
- Stuffing with 0 does not fill the piece.
Corrected result: PASS.

Fixture explanation (unreviewed): stuff with 0 g leaves the piece empty while telling the crocheter to stuff.

Lesson note (unreviewed): the corrected file stuffs with 20 g.

### 119_color_every_zero: Color every zero

Wrong result: ERROR.
- Every 0 rows or rounds never happens.
- Change color every 0 rows never changes color.
Corrected result: PASS.

Fixture explanation (unreviewed): changing color every 0 rows never changes color.

Lesson note (unreviewed): the corrected file changes color every 2 rows.

### 120_increase_every_zero: Increase every zero

Wrong result: ERROR.
- Every 0 rows or rounds never happens.
- Increase every 0 rounds never increases.
Corrected result: PASS.

Fixture explanation (unreviewed): increasing every 0 rounds never increases.

Lesson note (unreviewed): the corrected file increases every 3 rounds.

### 121_decrease_every_zero: Decrease every zero

Wrong result: ERROR.
- Every 0 rows or rounds never happens.
- Decrease every 0 rows never decreases.
Corrected result: PASS.

Fixture explanation (unreviewed): decreasing every 0 rows never decreases.

Lesson note (unreviewed): the corrected file decreases every 2 rows.

### 122_v_stitch_one: V-stitch of one

Wrong result: ERROR.
- A V-stitch of 1 is not a V-stitch.
Corrected result: PASS.

Fixture explanation (unreviewed): a V-stitch needs two tall stitches and a chain. A V-stitch of 1 is one stitch.

Lesson note (unreviewed): the corrected file uses a V-stitch of 2 dc.

### 123_fan_one: Fan of one

Wrong result: ERROR.
- A fan of 1 is not a fan.
Corrected result: PASS.

Fixture explanation (unreviewed): a fan needs several stitches in one space. A fan of 1 is one stitch.

Lesson note (unreviewed): the corrected file uses a fan of 5.

### 124_bullion_zero: Bullion of zero

Wrong result: ERROR.
- A bullion of 0 wraps has no wraps.
Corrected result: PASS.

Fixture explanation (unreviewed): a bullion of 0 wraps has no wraps to coil.

Lesson note (unreviewed): the corrected file uses 7 wraps.

### 125_cable_zero: Cable of zero

Wrong result: ERROR.
- A cable over 0 stitches does not cross.
Corrected result: PASS.

Fixture explanation (unreviewed): a cable over 0 stitches does not cross.

Lesson note (unreviewed): the corrected file crosses 2 stitches.

### 126_fringe_zero: Fringe of zero

Wrong result: ERROR.
- A fringe of 0 strands is not a fringe.
Corrected result: PASS.

Fixture explanation (unreviewed): a fringe of 0 strands is not a fringe.

Lesson note (unreviewed): the corrected file uses 4 strands.

### 127_buttonhole_zero: Buttonhole of zero

Wrong result: ERROR.
- A buttonhole of 0 chains has no opening.
Corrected result: PASS.

Fixture explanation (unreviewed): a buttonhole of 0 chains has no opening.

Lesson note (unreviewed): the corrected file uses 3 chains.

### 128_icord_zero: I-cord of zero

Wrong result: ERROR.
- An i-cord of 0 stitches has no cord.
Corrected result: PASS.

Fixture explanation (unreviewed): an i-cord of 0 stitches has no cord.

Lesson note (unreviewed): the corrected file uses 4 stitches.

### 129_oval_zero: Oval of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- An oval cannot start with 0 chains.
Corrected result: PASS.

Fixture explanation (unreviewed): an oval cannot start with 0 chains.

Lesson note (unreviewed): the corrected file starts with 8 chains.

### 130_square_zero: Square of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- A square of 0 rounds was not worked.
Corrected result: PASS.

Fixture explanation (unreviewed): a square of 0 rounds was not worked.

Lesson note (unreviewed): the corrected file has 4 rounds.

### 131_solomon_zero: Solomon knot of zero

Wrong result: ERROR.
- A Solomon knot of 0 is not a knot.
Corrected result: PASS.

Fixture explanation (unreviewed): a Solomon knot of 0 is not a knot.

Lesson note (unreviewed): the corrected file uses 5.

### 132_surface_zero: Surface of zero

Wrong result: ERROR.
- Surface crochet of 0 chains draws no line.
Corrected result: PASS.

Fixture explanation (unreviewed): surface crochet of 0 chains draws no line.

Lesson note (unreviewed): the corrected file uses 12 chains.

### 133_bead_every_zero: Bead every zero

Wrong result: ERROR.
- A bead every 0 stitches is never placed.
Corrected result: PASS.

Fixture explanation (unreviewed): a bead every 0 stitches is never placed.

Lesson note (unreviewed): the corrected file places a bead every 4 stitches.

### 134_stripe_every_zero: Stripe every zero

Wrong result: ERROR.
- Every 0 rows or rounds never happens.
- A stripe every 0 rounds never stripes.
Corrected result: PASS.

Fixture explanation (unreviewed): a stripe every 0 rounds never stripes.

Lesson note (unreviewed): the corrected file stripes every 2 rounds.

### 135_pompom_zero: Pom-pom of zero

Wrong result: ERROR.
- A wrap count of 0 has nothing to tie.
- A pom-pom of 0 wraps has nothing to tie.
Corrected result: PASS.

Fixture explanation (unreviewed): a pom-pom of 0 wraps has nothing to tie.

Lesson note (unreviewed): the corrected file uses 40 wraps.

### 136_tassel_zero: Tassel of zero

Wrong result: ERROR.
- A wrap count of 0 has nothing to tie.
- A tassel of 0 wraps has nothing to hang.
Corrected result: PASS.

Fixture explanation (unreviewed): a tassel of 0 wraps has nothing to hang.

Lesson note (unreviewed): the corrected file uses 40 wraps.

### 137_pineapple_zero: Pineapple of zero

Wrong result: ERROR.
- A pineapple of 0 is not a pineapple motif.
Corrected result: PASS.

Fixture explanation (unreviewed): a pineapple of 0 is not a pineapple motif.

Lesson note (unreviewed): the corrected file uses 7.

### 138_spike_zero: Spike of zero

Wrong result: ERROR.
- A spike stitch down 0 rows does not leave the row.
- A spike stitch down 0 rows does not leave the current row.
Corrected result: PASS.

Fixture explanation (unreviewed): a spike stitch down 0 rows does not leave the current row.

Lesson note (unreviewed): the corrected file goes down 2 rows.

### 139_tube_zero: Tube of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- A tube of 0 stitches has no opening.
Corrected result: PASS.

Fixture explanation (unreviewed): a tube of 0 stitches has no opening.

Lesson note (unreviewed): the corrected file uses 6 stitches.

### 140_rectangle_zero: Rectangle of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- A rectangle of 0 rows was not worked.
Corrected result: PASS.

Fixture explanation (unreviewed): a rectangle of 0 rows was not worked.

Lesson note (unreviewed): the corrected file has 12 rows.

### 141_corner_zero: Corner of zero

Wrong result: ERROR.
- A count of 0 does not make that shape.
- A corner of 0 chains does not turn the corner.
Corrected result: PASS.

Fixture explanation (unreviewed): a corner of 0 chains does not turn the corner.

Lesson note (unreviewed): the corrected file uses 2 chains.

### 142_star_one: Star of one

Wrong result: ERROR.
- A star stitch of 1 cannot make a star.
Corrected result: PASS.

Fixture explanation (unreviewed): a star stitch of 1 cannot pull up the loops a star needs.

Lesson note (unreviewed): the corrected file uses a star stitch of 5.

### 143_loop_zero: Loop of zero

Wrong result: ERROR.
- A loop stitch of 0 has no loop.
Corrected result: PASS.

Fixture explanation (unreviewed): a loop stitch of 0 has no loop.

Lesson note (unreviewed): the corrected file uses 1 loop.

### 144_same_color_letter: Same color letter

Wrong result: ERROR.
- Changing from Color Q to Color Q is not a color change.
Corrected result: PASS.

Fixture explanation (unreviewed): changing from Color Q to Color Q is not a color change. The check is any repeated letter, not only A.

Lesson note (unreviewed): the corrected file changes to Color R.

### 145_increase_direction: Increase direction

Wrong result: ERROR.
- Increase from 9 to 4 does not rise.
Corrected result: PASS.

Fixture explanation (unreviewed): any increase whose second number is not higher fails. This is not limited to 12 to 6.

Lesson note (unreviewed): the corrected file rises.

### 146_decrease_direction: Decrease direction

Wrong result: ERROR.
- Decrease from 4 to 9 does not fall.
Corrected result: PASS.

Fixture explanation (unreviewed): any decrease whose second number is not lower fails. This is not limited to 6 to 12.

Lesson note (unreviewed): the corrected file falls.

### 147_multiple_mismatch: Multiple mismatch

Wrong result: ERROR.
- 6 is not divisible by 4.
Corrected result: PASS.

Fixture explanation (unreviewed): a stated count that is not divisible by the written multiple fails. This is not limited to 3 and 10.

Lesson note (unreviewed): the corrected file uses a divisible count.

### 148_plus_remainder: Plus remainder

Wrong result: ERROR.
- 10 is not a multiple of 6 plus 1.
Corrected result: PASS.

Fixture explanation (unreviewed): a count that is not the written multiple plus the written remainder fails.

Lesson note (unreviewed): the corrected file uses 13, which is a multiple of 6 plus 1.

### 149_backward_rounds: Backward round range

Wrong result: ERROR.
- Rounds 9-2 run backwards.
Corrected result: PASS.

Fixture explanation (unreviewed): a round range whose first number is higher runs backwards. This is not limited to 8-5.

Lesson note (unreviewed): the corrected file puts the lower number first.

### 150_backward_rows: Backward row range

Wrong result: ERROR.
- Rows 9-2 run backwards.
Corrected result: PASS.

Fixture explanation (unreviewed): a row range whose first number is higher runs backwards.

Lesson note (unreviewed): the corrected file puts the lower number first.

### 151_even_count: Even count

Wrong result: ERROR.
- 9 is odd, but the line says the count must be even.
Corrected result: PASS.

Fixture explanation (unreviewed): an odd number cannot be required to be even. This is not limited to 7.

Lesson note (unreviewed): the corrected file uses an even number.

### 152_odd_count: Odd count

Wrong result: ERROR.
- 8 is even, but the line says the count must be odd.
Corrected result: PASS.

Fixture explanation (unreviewed): an even number cannot be required to be odd.

Lesson note (unreviewed): the corrected file uses an odd number.

### 153_apart_span: Apart span

Wrong result: ERROR.
- Eyes 7 stitches apart do not fit on a 5-stitch round.
Corrected result: PASS.

Fixture explanation (unreviewed): eyes farther apart than the round cannot sit on it. This is not limited to 8 on 6.

Lesson note (unreviewed): the corrected file places them inside the round.

### 154_stitch_past_end: Stitch past end

Wrong result: ERROR.
- Stitch 9 is past a 4-stitch round.
Corrected result: PASS.

Fixture explanation (unreviewed): a marker past the last stitch cannot be placed.

Lesson note (unreviewed): the corrected file uses stitch 1.

### 155_skip_past_count: Skip past count

Wrong result: ERROR.
- Skip 9 does not fit on a 4-stitch row.
Corrected result: PASS.

Fixture explanation (unreviewed): a skip of the whole row or more does not fit.

Lesson note (unreviewed): the corrected file skips 1.

### 156_fractional_times: Fractional times

Wrong result: ERROR.
- x 1.5 is not a whole repeat.
- A fractional repeat is not a whole repeat.
Corrected result: PASS.

Fixture explanation (unreviewed): any repeat written as x N.N is not a whole repeat. This is not limited to 2.5.

Lesson note (unreviewed): the corrected file repeats a whole number of times.

### 157_copied_inch: Copied inch measure

Wrong result: ERROR.
- The line copies the same number into both units. The length was not converted.
- 4 inches is not 4 cm. The line copies the same number.
Corrected result: PASS.

Fixture explanation (unreviewed): writing the same number for inches and centimeters is not a conversion. One inch is 2.54 cm.

Lesson note (unreviewed): the corrected file converts 4 inches to 10.16 cm.

### 158_copied_cm: Copied centimeter measure

Wrong result: ERROR.
- The line copies the same number into both units. The length was not converted.
- 10 cm is not 10 inches. The line copies the same number.
Corrected result: PASS.

Fixture explanation (unreviewed): writing the same number for centimeters and inches is not a conversion.

Lesson note (unreviewed): the corrected file converts 10 cm to 3.94 inches.

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

| File | Section | Status | Errors | Warnings | Not checked | Seen, after dropping abbreviation noise |
|---|---|---|---:|---:|---:|---|
| `wrong_benchmarks.md` | whole file | ERROR | 83 | 11 | 24 | Line 121: worked 5 stitches into 15 without a decrease.; Line 185: this round consumes 17 stitches, but only 0 are available from the previous round; 17 extra stitches are requested.; Line 220: worked 1 stitch into 48 without a decrease. |
| `wrong_benchmarks.md` | 1: Classic Amigurumi Bear | ERROR | 2 | 1 | 1 | Round 9: plain round received 4 stitches without an increase or decrease; the row states 8.; Piece 'arms' is named in assembly but never started.; Round 11: 12 to 24 stitches doubles the count in one round. Review the intended shaping; this check cannot establish the target shape. |
| `wrong_benchmarks.md` | 2: Celestial Wyvern | ERROR | 9 | 3 | 3 | Line 43: worked 5 stitches into 15 without a decrease.; Round 13 states 30 stitches, but operations produce 0.; Row 1 states 14 stitches, but operations produce 0. |
| `wrong_benchmarks.md` | 3: Clockwork Dragon | ERROR | 13 | 0 | 13 | Line 67: this round consumes 17 stitches, but only 0 are available from the previous round; 17 extra stitches are requested.; Seam mismatch: 3 stitches cannot close 4 stitches.; Short-row gap: 28 of 34 leaves 6 row-ends unstated. |
| `wrong_benchmarks.md` | 4: Abyssal Leviathan | ERROR | 39 | 3 | 14 | Line 50: worked 1 stitch into 48 without a decrease.; Line 51: this round consumes 54 stitches, but only 1 are available from the previous round; 53 extra stitches are requested.; Line 68: this round consumes 8 stitches, but only 1 are available from the previous round; 7 extra stitches are requested. |
| `wrong_benchmarks.md` | 5: Void-Warped Chimera | ERROR | 22 | 4 | 8 | Line 38: this round consumes 38 stitches, but only 36 are available from the previous round; 2 extra stitches are requested.; Round 15 states 38 stitches, but operations produce 36.; Round 17 states 32 stitches, but operations produce 30. |
| `gemini_corrected.md` | whole file | NEEDS_REVIEW | 0 | 1 | 67 | Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
| `gemini_corrected.md` | 1: Classic Amigurumi Bear (Corrected) | NEEDS_REVIEW | 0 | 0 | 24 | none |
| `gemini_corrected.md` | 2: Celestial Wyvern (Corrected) | ERROR | 1 | 1 | 14 | Ghost material: '.25 mm hook, polyfill, 12 mm safety eyes (x2), tapestry needle' is listed under Materials but never mentioned in the instructions.; [OrphanedYarn] ORPHANED YARN IN BOM: 'Yarn TAIL' is listed in Materials but never used in the pattern. |
| `gemini_corrected.md` | 3: Clockwork Dragon (Corrected) | NEEDS_REVIEW | 0 | 2 | 16 | Row 11 turns with 9 stitches unworked; check the short-row shaping.; Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
| `gemini_corrected.md` | 4: Abyssal Leviathan (Corrected) | ERROR | 1 | 1 | 18 | Round 15 states 20 stitches, but operations produce 0.; Short-row turns create vertical row-end sites, but no row-end stitch count is stated. |
| `gemini_corrected.md` | 5: Void-Warped Chimera (Corrected) | NEEDS_REVIEW | 0 | 0 | 19 | none |
| `chatgpt_corrected.md` | whole file | ERROR | 1 | 0 | 63 | Seam mismatch: 3 stitches cannot close 4 stitches. |
| `chatgpt_corrected.md` | 1: Classic Amigurumi Bear — Corrected | NEEDS_REVIEW | 0 | 0 | 28 | none |
| `chatgpt_corrected.md` | 2: Celestial Wyvern — Corrected | NEEDS_REVIEW | 0 | 0 | 13 | none |
| `chatgpt_corrected.md` | 3: Clockwork Dragon — Corrected Defect Sections | ERROR | 1 | 0 | 15 | Seam mismatch: 3 stitches cannot close 4 stitches. |
| `chatgpt_corrected.md` | 4: Abyssal Leviathan — Corrected | NEEDS_REVIEW | 0 | 0 | 17 | none |
| `chatgpt_corrected.md` | 5: Void-Warped Chimera — Corrected | NEEDS_REVIEW | 0 | 0 | 15 | none |

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
