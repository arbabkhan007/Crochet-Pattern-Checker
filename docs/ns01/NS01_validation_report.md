# NS 01 - Hamish the Highland Cow - validation report

Source (verbatim): `docs/intake/01_NS01_hamish_highland_cow.txt`
Corrected master: `docs/ns01/NS01_corrected.md`
Auditor: `docs/kit/audit_lib.py` (independent re-derivation of every round/row table)
Engine: repo `crochet_checker.verification.stages.run_stages` (crochet-check v1.0.0)

## Verdict

**Stitch arithmetic: SOUND - zero arithmetic corrections.**
Every table re-derives exactly from its own instructions:

| Piece | Rounds checked | Result |
|---|---|---|
| Head | R1-R16 (6 -> 48 -> 6) | all counts match |
| Muzzle | R1-R8 (6 -> 24 -> 18) | all counts match |
| Body | R1-R19 (6 -> 48 -> 18, neck open) | all counts match |
| Belly patch | Found + R1-R4 (ch 9 oval 18 -> 36) | all counts match |
| Standard legs | R1-R16 (6 -> 18 -> 12 -> 9) | all counts match |
| Shortened front legs | R1-R10 (6 -> 18 -> 12) | all counts match |
| Ears (inner/outer) | R1-R7 (6 -> 12 -> 9) | all counts match |
| Horns | R1-R7 (4 -> 8) | all counts match |
| Scarf | Found + Rows 1-2 (ch 61 -> 60) | all counts match |

Cross-checks that also pass: fringe knots 24 + 10 + 9 = 43; head-to-body seam
18 neck sts matched to 18 head Rnd-14 sts; ear join 9 whip stitches on two
9-stitch openings; gauge prose (11 sc x 12 rnd = 5 cm) consistent with the
70 mm head / 70 mm body statements.

**Engine on original:** 3 errors + 1 warning (all wording/structure, none arithmetic).
**Engine on corrected master:** 0 errors, 0 warnings.
**Independent audit on corrected master:** 0 problems, 0 unparsed rows.

## Corrections (4 - clarity / engine compliance only)

| # | Location | Original | Corrected | Why |
|---|---|---|---|---|
| 1 | Head prose | "place the 12 mm eyes between Rnds 9 and 10" | "the 12 mm eyes go in between Rnds 9 and 10" | engine eyes-before-stuffing stage reads "place ... eyes" as installation after the R12 stuffing note; the lock-before-stuff order was already correct in the pattern |
| 2 | Legs heading | "Shortened front legs - upright option only (make 2)" | "Shortened front legs - upright option (make 2)" | make-count stage bound the word "only" as a piece name and collided with "Rnd 6 only" in the ear prose |
| 3 | Scarf Row 2 | "ch 1, turn, hdc across" | "ch 2, turn, hdc across" (turning ch does not count) | house turn-chain rule: an hdc turn needs ch 2; count (60) unchanged |
| 4 | Muzzle / short-front / ear prose | single long paragraphs mixing "opening" with ranges and "about" | split into separate paragraphs; "about 42 mm" -> "measures 42 mm"; "in Yarn A" -> "using Yarn A" | unverified-claims stage flags any one line that pairs an opening with an approximate/ranged measure; splitting removes the false positive without changing any instruction |

No stitch count, round count, hook size, gauge or measurement was altered.
