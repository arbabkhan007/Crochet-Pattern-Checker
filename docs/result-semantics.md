# What a result means

This page preserves the detailed result contract and limitations; the README contains a short overview.

`CPC-RULESET-1` identifies the current deterministic rule set. JSON reports include structured findings with stable rule IDs, severities, locations, and source lines where available; legacy prose errors and warnings remain available. `NEEDS_REVIEW` means an explicit Row/Round body was not fully parsed. It is not a stitch-count error.

A large shaping step is a review warning, not a requirement to add a particular round or proof of fit. The small golden fixture set is provisional; independent craft review and broader real-pattern review remain pending.

`PASS` means the written checks that ran found no error and no warning. It does not mean a photo was counted, a chart image was read, or every English sentence was understood.

## Optional AI review and non-goals

When explicitly enabled, the coordinated specialist-review feature may use hosted language models to review the written pattern. Its participation and failures are reported separately. These reviews do not replace or override the deterministic checker verdict, and they cannot verify a physical object, inspect photos or chart images, measure gauge, or confirm that construction or testing happened. `PASS` remains the result of deterministic written-pattern checks, not AI consensus.

The checker does not run a chart-image detector, photo stitch classifier, support chat, cover-image generator, vision-training set, or process cluster.

Two assembly lines are read. They are still not a made piece and not a photo:

- `Cinch shut`, with no stitch count, closes the last stated round. It is an error when no counted round comes before it.
- `sew head to body` is a piece reference. It is an error when head or body never starts.

An instruction line the parser did not count is named under Not checked. It is not treated as a passed round.

A sew line that names a made piece but gives no number is named. The count is not guessed. A flatten line with fewer than two stitch counts is named. The seam is not compared.

A check is not a purchase. A photo was not opened, the piece was not made, and a gauge swatch was not measured.

A finished-size range, a request to match stitch and round gauge with no tested sample, a yarn range that was not weighed, and an approximate opening are warnings. The missing measurements are not invented.

A hook size of 0 mm is an error in any sentence. The line does not have to say `Hook: 0 mm`. A size such as 3.0 mm or 10 mm is not that error.

A chain of 0, work of zero stitches, a skip of zero, and a repeat of zero times are errors in any sentence. A hook size written in centimeters is an error in any sentence. These do not have to match one lesson line.

A hook of 40 mm or more is a warning in any sentence, not only after `Hook:`. Chain zero and work 0 are the same errors as `ch 0` and `work 0 stitches`. A hook size written as centimeters is the same error as cm.

The words zero and one are the same defects as 0 and 1 in those written checks. Decrease five times across eleven stitches is the same error as dec x 5 on 11 stitches.

Those arithmetic checks also accept the words twelve, six, and the other number words, and they do not have to be the first words of the line. A hook letter such as H/8 can be named in any sentence. A hook written as millimeters is the same size check as mm.

A line that starts with `>` is a quote. A line that says `do not` is a prohibition. Neither is treated as an instruction.

`Inc from 12 to 6`, `rnd 8 to rnd 5`, `colour A to colour A`, and `ch-1 counts as dc` are the same errors as the longer sentences. A line that says `or` is still a choice. No length is invented. This is not a physical proof, and it is not a reason to pay for a pattern.

`ch1, turn for dc`, `8in = 8cm`, and `H/8 = 2.25mm` are the same errors without the space. A real conversion such as `4 inches = 10.16 cm` is not that error. No length is invented.

`I-cord uses no stitch`, `cable crosses no stitch`, and `make none` are the same empty counts. `No stitches are left unworked` is not that error. No length is invented.

`Puff is one stitch`, `picot = 0`, and `round goes side to side` are the same written errors. `sc (UK double)` stays correct. No length is invented.

`Righties and lefties`, `Fsc and ch 12 to start`, and `increase shrinks, 12 to 6` are the same written rules. A line that says `or` stays a choice. No length is invented.

`I-cord of no stitches`, `round number 0`, and `repeat x zero` are the same empty counts. `No stitches are left unworked` is not that error. No length is invented.

`Cable that crosses nothing`, `yardage listed as nothing`, and `round numbered nothing` are the same empty counts. `Leave nothing unworked` is not that error. No length is invented.


`Inc that shrinks from 12 to 6`, `gauge of minus 1 sc`, and `colour B back to colour B` are the same written rules. A line that says `or` stays a choice. The kept scripts do not set a price, a score, or a gauge. No length is invented.
