# NS07–NS12 written-pattern review

Reviewed 13 November 2026 against the six user uploads named `NS07_corrected.md` through `NS12_corrected.md`. This batch was reviewed separately from the repository's existing pattern masters and the earlier NS01–NS06 batch.

## Result and files

Use `NS07_reviewed.md` through `NS12_reviewed.md`. Original uploads, master patterns and existing PDFs/archives were not overwritten. These editions have been checked in writing, **not physically crocheted or certified for product safety**.

The main stitch-count sequences were largely consistent already. The substantive changes concern closure, stuffing order, attachment placement, alternatives and misleading construction advice. No count was arbitrarily changed merely to make the generic checker return PASS.

## Changes

### NS07 — Pocket Positivity Trio

- Added explicit six-front-loop cinches for Sunny and Waddle, before Sunny's petals and after Waddle's body respectively.
- Moved Spud's first stuffing to the wider opening after face work, rather than waiting until only eight stitches remain; specified two matched pairs for the final four-stitch seam and clarified that only the opening is flattened.
- Listed optional pink blush yarn. Retained the existing eye-before-stuffing pauses and Sunny's 18 exposed petal anchors.
- Corrected the larger-version advice: a 1.3× stitch-width change alone cannot establish the same height scale; round gauge must also scale, and completed samples must be measured.

### NS08 — Ember the Baby Dragon

- Moved the snout's attachment rim clear of the open R11 head/neck seam, approximately over R8–10. Pinning and physical fit still need testing.
- Specified catching the ninth leg-rim stitch separately instead of simply tucking it into a fold.
- Clarified a single wing foundation, turning after Rows 1–3 only, and mirroring the wing pair.
- Replaced the ambiguous advice to add foundation chains to a completed spine with an explicit remake formula: N spikes need ch (3N + 7), (3N + 6) sc, two three-stitch tabs, and N three-anchor repeats. Ten spikes therefore need ch 37 and 36 sc.
- Removed the presentation of summed round heights and wing dimensions as proof of finished size. Head motion can also arise from seam security, filling and balance, not just a count mismatch.

### NS09 — Shelby the Sea Turtle

- Kept the correct 24-to-35 small appendage round and 42-to-53 large alternative; the seam uses 24 or 42 exposed front loops, not the appendage stitch count.
- Replaced the arbitrary “5 cm of seam remains” instruction with a deliberate rear access gap of 6–8 seam pairs for knotting the ring attachment inside. Begin at the rear and finish that gap last.
- Clarified orientation relative to the rear keyring rather than a nonexistent separate shell tail.
- Removed the unmeasured internal-capacity claim and identified the perimeter-derived diameter as a model, not a measured disc.

### NS10 — Willow the Bunny Lovey

- Clarified that blanket starting chains do not mean turn the blanket.
- Separated head sc gauge from granny-square blanket measurements. Dc counts alone omit group gaps, corner chains and border width; they cannot establish an exact side length.
- Clarified the head join: move inward far enough that the full 18-stitch attachment circle has blanket fabric under it. A fixed 3 cm diagonal overlap alone does not guarantee that. Anchor to actual stitch posts and bridge granny gaps rather than fastening into empty space.
- Replaced advice that the sc border necessarily fixes curling with checks for missing groups and uneven tension. Kept 12n dc in blanket round n and the 252-sc border after R20.
- Preserved embroidered-face requirements and infant sleep-space warnings; this review does not establish suitability for a particular age.

### NS11 — No-Sew Christmas Gnome

- Corrected the claim that joining only at colour changes creates perfectly level stripes. The optional joined-round method now specifies joining every round from the start and excluding joining slip stitches/starting chains from counts; a jog may remain.
- Specified the optional brim as 30 surface slip stitches, separate from the body count.
- Changed bobble direction from “toward you” to the outside/right side, which does not depend on how the maker holds the piece.
- Retained the consistent R14 nose, R15 plain face round, R16 hat change and after-R15 eye-fitting pause. Mini and larger variants were checked separately.

### NS12 — Bobble Christmas Tree

- Reconciled firm-stuffing language and the untested 25 g quantity with the actual light-fill instructions. Fill by shape without stretching; no replacement measured gram quantity was invented.
- Corrected the base description: R1–8 are the base increases; R9 is the fold/wall transition.
- Added the sc2tog method and explicit outward bobble placement. Correct arithmetic does not ensure a bobble pops outward by itself.
- Clarified that R10 does not decrease and only R12, 14, 16, 18, 20 and 22 are decreasing bobble tiers. The intervening plain rounds do not decrease. Fixed repeat placement does not guarantee visually straight columns in spiral crochet.
- Clarified the insert as 3–5 mm smaller in **diameter** than the measured inside base, avoiding ambiguity about radial clearance.
- Replaced advice to remove stuffing from an already closed tip with instructions to undo sufficient closing rounds, adjust and rework. Drooping can have several causes, not just too much stuffing.

All six: repaired blank lines within Markdown tables and added a clear review-status statement. Dimensions, timings and material allowances remain estimates requiring sample testing.

## Reproducible validation

From the repository root:

```sh
python reviews/ns07-ns12/verify.py
python -m pytest tests/validation/test_ns01_ns06_review.py tests/validation/test_ns07_ns12_review.py -q
```

Observed: **201 expanded round/row records, 834 assertions, zero errors.** **10 tests passed** across the two batches (7 for this batch, 3 for the earlier batch).

The batch-specific audit reuses the repository's Markdown-table parser, canonical arithmetic, exact-text noncanonical cases and US-to-UK translation. It explicitly reads the uploaded `UK equivalent` column because the shared parser expects a different header. It checks both NS11/NS12 terminology columns, expands round ranges, checks range lengths, carries context between continuation tables, and rejects unknown count-bearing instructions instead of silently passing them.

`stitch-ledger.json` records the expanded table arithmetic, including all R3–20 blanket rounds. Identical components are not multiplied by the number made. A canonical record counts stitches consumed and produced; granny records count corner and side-group spaces, not individual old dc anchors.

`prose-checks.json` adds exact-text-bound arithmetic checks for the spike foundation and nine-repeat spine, variable spine formula, larger turtle shell/appendages, blanket border, gnome variants, petal anchors, attachment seams and final tree bobble tier. These are explicit reviewed cases, not a general prose interpreter. Mutations test wrong counts, wrong UK translation, inconsistent range lengths, changed larger-turtle prose, unknown instructions and a changed border count.

### Independent construction calculations

- Sunny: 9 pairs of exposed front loops = 18 anchors; 9 slip stitches + 9 × 3 petal stitches = 36. Closing join is not an extra counted stitch.
- Ember: head and body each end at 18; the wing edge uses 8 plain slip-stitch anchors plus 2 fan anchors and makes 18 stitches. Spine: 3 + 9×3 + 3 = 33 anchors, 3 + 9×8 + 3 = 78 counted edge stitches, with nine additional uncounted picots.
- Shelby: small shell 108 stitches + underside base 60 + appendage round 35 = 203 counted stitches, excluding finishing joins, embroidery and seam. Large appendage round consumes 42 anchors and makes 53, retaining 42 seam loops.
- Willow: round n has 12n dc, excluding corner chains and slip-stitch joins; at R20, 240 dc + four 3-sc border corners = 252 border sc. The head attachment uses R12's 18 stitches rather than the six-stitch cinch.
- Gnome: nose round 14 + 1 bobble + 15 = 30; mini closure 12 → 6 after omitting the plain R22; larger option adds three 30-stitch rounds without changing subsequent shaping.
- Tree: decreasing bobble tiers 48 → 42 → 36 → 30 → 24 → 18 → 12; R22's [BO, sc2tog] consumes three and produces two, repeated six times. Final tip 12 → 6 → 6 → 3.

### General checker limitations

Also ran `crochet-check check --json` on all six reviewed files. It reported **zero stitches counted on all six**, so its verdicts cannot validate these tables. It returned ERROR for NS07 (1 finding), NS08 (2) and NS11 (1), and PASS for NS09/10/12. Its “Review status” eye-after-stuffing finding conflicts with the explicit early fitting pauses; it also misread Ember's prose 33-sc foundation as producing one stitch. These results were inspected, not concealed or used as proof. The table/prose checks above are the relevant arithmetic evidence; the application engine was not altered.

## Remaining checks before publication or sale

Make full samples, including any alternative size or construction that will be offered. Test Ember's snout/neck clearance, spine path and sitting balance; Willow's full head-to-blanket seam on real granny fabric; gnome brim/eye clearance; turtle keyring anchors and flipper placement; and the tree's insert fit, bobble projection and stability. Pin and adjust before sewing. Printed round heights and stitch spacing are not physical measurements or proof of silhouette.

Weigh actual yarn/fill use, time the work, measure after finishing and test the proposed cleaning method on complete samples. Cardboard inserts must remain dry. Review loose strands, hanging loops, metal rings, eyes, fibre shedding and every attachment for the intended use and market. An embroidered face or a workshop pull check does not establish legal compliance.

Resources used: all six uploads, repository documentation and audit/checker code, manual arithmetic/construction review, and local regression tests. No physical sample, certification, external standards verification or new web research is claimed.
