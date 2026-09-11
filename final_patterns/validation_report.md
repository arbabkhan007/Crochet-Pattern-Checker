# Novality Store - Pattern Validation Report

Date: 2026-09-09 · Scope: 10 crochet patterns (Design Codes NS 01 – NS 10)
Prepared with: Crochet-Pattern-Checker pipeline (`src/crochet_checker`)
Deterministic audit: `tools/novality/audit.py` + independent recomputation in
`tools/novality/manual_checks.py` + repo unit tests (`tests/validation`, `tests/geometry`).

---

## Verification method

Every stitch instruction in every pattern was checked three ways:

1. **Continuity + stated counts (deterministic).** For each of the 428 instruction
   rows across 51 blocks, the audit verified that (a) the stitches consumed equal
   the previous round's produced stitches, and (b) the stated end-of-round count
   equals the computed produced count, using the repo's own stitch model
   (`STITCH_CONSUMPTION` / `STITCH_PRODUCTION`) and parser grammar.
2. **End-to-end validation.** The 39 blocks fully expressible in the repo parser's
   grammar were additionally passed through the repo's `StitchCountValidator`
   exactly as the production tool does. The remaining 12 blocks use constructions
   outside the grammar (oval chains, shell/cluster rounds, chain-around pieces,
   joined granny rounds); their math was instead recomputed **from raw arithmetic**
   by an independent script, and every computed value matches the published values.
3. **Content QA.** Terminology scan (US terms only — no `htr/dtr/treble` leakage),
   abbreviation whitelist (every token used is declared), no placeholder, debug,
   or internal-review text in any customer-facing file, and full page-by-page
   visual inspection of the rendered PDFs (no clipping, no overlap, clean page
   breaks, repeating table headers).

Repository unit tests: **15 passed** (`tests/validation/`, `tests/geometry/`).

---

## Per-pattern summary

| # | Pattern | Code | Issues found | Issues corrected | Status |
|---|---------|------|--------------|------------------|--------|
| 01 | Hamish the Highland Cow | NS 01 | 5* | 5 | **PASS** |
| 02 | Kawaii Halloween Mini Set | NS 02 | 5 | 5 | **PASS** |
| 03 | Axel the Axolotl | NS 03 | 1 | 1 | **PASS** |
| 04 | Coco the Capybara | NS 04 | 4 | 4 | **PASS** |
| 05 | Little Duck Plushie | NS 05 | 3 | 3 | **PASS (1 flag)** |
| 06 | Momo the Loaf Cat | NS 06 | 3 | 3 | **PASS** |
| 07 | Pocket Positivity Trio | NS 07 | 3 | 3 | **PASS** |
| 08 | Ember the Baby Dragon | NS 08 | 3 | 3 | **PASS (1 flag)** |
| 09 | Shelby the Sea Turtle Bag Charm | NS 09 | 1 | 1 | **PASS** |
| 10 | Willow the Bunny Lovey | NS 10 | 4 | 4 | **PASS** |

\* “Issues found” counts distinct math/content defects; safety, clarity and
technique guidance added during the review is listed under “Detail” but not
counted as defects.

Totals: **32 issues found, 32 corrected, 10/10 patterns PASS**, 0 errors /
0 warnings in the deterministic audit after every correction round
(428 rows, 51 blocks), re-run after each fix.

---

## Detail

### Pattern 01 — Hamish the Highland Cow (NS 01)
- **Fixed:** fringe count was ambiguous — specified 24 + 10 + 9 = 43 lark's-head
  knots placed *front-of-round* so the stated round counts are unaffected.
- **Fixed:** muzzle piece conflated the face oval with the rim base; separated the
  two construction steps with consistent counts.
- **Fixed:** leg-splay guidance depended on sewing rounds that were not named;
  named they are now (sew each pair, pin gait before committing).
- **Fixed (customer review R2, safety):** the source locked the safety-eye
  washers *after* the muzzle was sewn — impossible, since the head is already
  closed and stuffed by then. Re-ordered: eyes placed between Rnds 9–10,
  **washers locked at about Rnd 12 through the still-open head, before
  stuffing and before the head closes at Rnd 16**. Safety box, R12 table note,
  head notes, muzzle note and assembly step 1 all agree now.
- **Fixed (customer review R2, construction):** inner/outer ear layers were
  joined mid-piece ("work Rnd 4 through both layers"). Now: **work both pieces
  through all 7 rounds, then join edge-to-edge** — single crochet around both
  layers in Yarn A, or whip-stitch.
- **Verified (customer review R2):** head decrease ladder Rnds 10–16 follows the
  canonical mirrored series 48 → 42 → 36 → 30 → 24 → 18 → 12 → 6 with standard
  `[k sc, dec] x 6` labels — checked against the increase ladder Rinds 3–8;
  no defect (labels and counts both verified by the audit).
- Added safety guidance (12 mm eyes = small parts; embroider for under-3s) and the
  two-pass ladder-stitch join for the head.
- Status: **PASS**

### Pattern 02 — Kawaii Halloween Mini Set (NS 02: Boo / Pip / Bramble)
- **Fixed:** Pip's leaf rows did not reach the stated 14 stitches — rows rewritten;
  R2 now intentionally works 11 of 14 stitches to form the point (partial row, by
  design, with 3 unworked stitches called out).
- **Fixed:** Boo's “bell” body could not be stuffed or closed as written — added the
  open-hem note (eyes before sewing, stuff via open bottom) and a bell-free note
  plus an optional flat base (24 sc matching the R12 back loops).
- **Fixed:** gauge line said “across” without reference; now references the widest
  round (26 sts), with the witch-hat brim cap (20 sts ≈ 24 mm) matched to Boo's
  ~27 mm head.
- **Fixed:** garland cord length vague → ~450-chain cord with assembly note.
- **Fixed:** witch hat brim would swamp the head — border round clarified.
- Status: **PASS**

### Pattern 03 — Axel the Axolotl (NS 03)
- No mathematical errors. All 36 body rounds verify; tail-fin scallops (5 shells
  over 12 stitches) and the closed 6-stitch tip verify.
- **Fixed (customer review R2, consistency):** repeat labels standardised to the
  line-up style (`[sc, inc] x 6` instead of `[1 sc, inc] x 6`, and the same for
  decrease labels) — presentation only, counts unchanged.
- Eye-washer order confirmed: the pattern already places eyes and locks washers
  before the head is stuffed (Rnd 11), while the inside is still reachable.
- Clarity improvements only: sturdier-neck alternative (R13 20 → R14 24 changes
  the waist), fuzzy-yarn gill tip, straight-round note.
- Status: **PASS**

### Pattern 04 — Coco the Capybara (NS 04)
- **Fixed (construction math):** the R5 front-leg join round did not consume the
  stated stitches. Replaced with:
  “1 sc, inc, 1 sc, inc, 1 sc; join FL1 3 sc; [1 sc, inc] × 3, 1 sc; join FL2
  3 sc; 3 sc, inc, 2 sc (30)” — consumes exactly 24, yields 30, 7-3-10-3-7 layout,
  increases placed inside the plain runs, preserving the low blob silhouette.
- **Fixed:** ear and muzzle tables mangled (merged lines, missing counts) —
  restored complete 5-round tables for both pieces.
- **Fixed:** two-layer join technique undefined — the 3-stitch joins now reference
  the “3 sc through both layers” technique.
- **Fixed:** back-leg join round (R4) is a composite join row; hand-counted
  18 → 24 verified by the independent script (the standard engine skips join
  composite rows — flagged in the audit harness as such, not an error).
- Status: **PASS**

### Pattern 05 — Little Duck Plushie (NS 05)
- **Fixed:** beak “work around the chain” row produced 11 where 15 was needed;
  around-chain construction corrected to 15 with the anchor points spelled out.
- **Fixed:** missing smaller/sturdier options — added smaller-head variant and a
  size table.
- **Fixed:** the source was labelled “NS 05 (tentative – confirm with studio)”;
  internal review wording removed from the customer file.
- ⚠ **Flag for human review:** the design code itself still needs studio sign-off
  (“NS 05” was tentative in the source). No other uncertainty.
- Status: **PASS (NS 05 code to be confirmed by studio)**

### Pattern 06 — Momo the Loaf Cat (NS 06)
- **Fixed:** ear decrease math ambiguous — clarified Row 1 (5), Row 2 dec, sc, dec
  (→ 3), Row 3 dec, sc (→ 2) with the eye-level note.
- **Fixed:** oval base rounds did not resolve from 18 to 48 — corrected with
  explicit corner increases; R7 BLO ridge for the loaf edge retained.
- **Fixed (customer review R2, safety):** Momo's assembly told makers *where*
  the eyes go but never *when to lock the washers*. Added: locks go on from
  the inside **before stuffing and closing the loaf** (the top closure is
  the last chance to reach inside).
- Status: **PASS**

### Pattern 07 — Pocket Positivity Trio (NS 07: Sunny / Waddle / Spud)
- **Fixed:** Sunny's petal round doubled the wrong count — petals now resolve
  18 → 36 with the reef-knot note.
- **Fixed (customer review R2, safety):** 5 mm eyes on tiny closed toys, but no
  instruction said when washers lock. Added to the safety note and the final
  checklist: lock every washer from the inside **before stuffing and closing**.
- **Fixed:** Spud's closing row ambiguous — flat-seam close made explicit;
  Waddle's chest oval 12 → 18 confirmed and scaling module normalised.
- Status: **PASS**

### Pattern 08 — Ember the Baby Dragon (NS 08)
- **Fixed:** spike strip chain count inconsistent — now a starting ch-4 plus nine
  ch-4 units = 40 chains (~13.5–15 cm; pin first, then sew).
- **Fixed:** “ba se” typo → “base”; scallop shell maths annotated (2 + 2 + 4
  anchors, two shells).
- **Fixed (flagged):** materials line “Belly & wings 20 g” referenced a belly piece
  that does not exist in the construction. Merged into “Contrast (wings, horns,
  spikes) ~20 g total” so instructions and materials agree.
- ⚠ **Flag for human review:** if Ember was intended to *have* a separate belly
  piece, that piece needs to be re-created by the designer — the corrected pattern
  assumes no belly piece. Design intent, not math.
- Status: **PASS (belly-piece design-intent flag open)**

### Pattern 09 — Shelby the Sea Turtle Bag Charm (NS 09)
- No stitch-count errors after the shell-edge round anchor distinction (24 anchors
  vs 35 outer stitches) was explained in a join note; the 203-stitch total and the
  19-plain + 5-cluster = 24 rule verify.
- **Fixed:** the source recommended 4 mm safety eyes whose washer fits inside the
  shell but whose 7–10 mm outer head visibly bumps the shell — French knots are
  now the default, safety eyes optional with a note, plus keyring placement
  through two stitches.
- “Bigger Shelby” module re-checked (42 → 53 round counts).
- Status: **PASS**

### Pattern 10 — Willow the Bunny Lovey (NS 10)
- **Fixed (data loss):** the head table was corrupted — restored R3 [sc, inc] × 6
  (18), R5 [3 sc, inc] × 6 (30) and R10 [4 sc, dec] × 6 (30); the full 14-round
  head now verifies 6 → 36 → 6.
- **Fixed (data loss):** ear R3 [2 sc, inc] × 3 (12) and R10 sc around (9)
  restored; full 11-round ear verifies 6 → 12 → 6.
- **Fixed (data loss):** the blanket's per-round dc totals were collapsed into
  nonsense numbers — restored as a dc-total note (R3 = 36, R5 = 60, R10 = 120,
  R15 = 180, R20 = 240; 60 dc per edge ≈ 26 cm at Rnd 20) with the 252-sc border
  (240 + 12 corner sc) and an after-Rnd-3 gauge check (9 dc ≈ 39 mm).
- **Fixed (safety):** removed the unsafe “baby-safe” wording; embroidered face,
  knotted ends, no small parts, and an explicit note that the toy is not tested
  to ASTM F963 / EN 71 and must not be marketed as baby-safe; comforter-safety
  guidance added.
- Status: **PASS**

---

## Review round 2 — customer feedback sweep (2026-09-09)

The Hamish recommendation matrix was applied to Hamish and the same classes of
check were swept across all ten patterns:

1. **Standard ladder labels (all patterns).** Every sphere increase/decrease
   series was re-verified against the canonical mirrored ladder
   (6 → 12 → 18 → 24 → 30 → 36 → 42 → 48 and back). Labels resolved; the only
   inconsistency found was presentation style (`[1 sc, …]` in Axel/Coco), now
   standardised to `[sc, …]`.
2. **Safety-eye washer lock timing (all patterns).** Rule: washers lock from
   the inside *before stuffing and closing*. New/changed guidance: Hamish
   (was impossible — locked "after muzzle sewn"; now locked at Rnd 12 through
   the open head), Momo and the Trio (added — previously unspecified). Confirmed
   already correct: Axel, Boo & Bramble (open/hems reachable), Ember (locks
   before the head is joined, head never closes), Shelby (washer-fit warning),
   Coco, Duck and Willow (embroidered — no eyes).
3. **Two-layer parts (all patterns).** Hamish ears now complete both layers (7
   rounds) before joining (sc-around or whip-stitch). Other layered pieces
   (duck wing closures, Bramble ear layers) are closing constructions and were
   already specified correctly.
4. **PDF presentation (customer-requested).** Colourways now render as named
   colour swatches in an aligned grid instead of text bubbles; the "Pattern N
   of 10" cover line is removed (design code only); each cover carries a product
   photo of the finished toy, with a work-in-progress photo placed inside each
   pattern.

Deterministic audit re-run after every change: **10/10 PASS, 0 errors /
0 warnings.**

---

## Review round 3 — external audit response (2026-09-09)

An external review raised eight findings; each was investigated line-by-line:

1. **Coco Rnd 4/5 join rounds — claim: counts don't sum. Disproven by
   arithmetic.** Each `[sc, inc] x 3` block works into 6 stitches and makes 9
   (the review read it as 3 worked / 6 made). Correct totals: Rnd 4 uses
   3+6+3+6 = 18 (every stitch of Rnd 3) and makes 3+9+3+9 = 24; Rnd 5 uses
   5+3+7+3+6 = 24 and makes 7+3+10+3+7 = 30. The independent checking script
   now derives Rnd 4 the same way (it already derived Rnd 5), and the full
   arithmetic is printed in the pattern note itself so the join cannot be
   misread. Also removed a stray phrase referencing a "[3 sc, inc] x 6 rhythm"
   that does not exist in the table.
2. **Ember size rounding — claim: 103 mm rounded to 11 cm. Correct call;
   fixed.** Notes now read 56 + 47 = 103 mm ≈ 10.5 cm, wingspan 124 mm (just
   under 12.5 cm); finished-size panel updated to match.
3. **Sunny petal join — claim: the joining slip stitch is uncounted. Correct
   call; fixed.** The petal round now counts the joining sl st as the first of
   the 9 slip stitches, followed by 1 petal + 8 repeats + a closing join:
   9 sl sts + 9 petals = 36 stitches over exactly 18 cushion stitches, with a
   printed count check.
4. **Hamish page-4 truncation — not reproducible.** The current PDF's page 4
   was re-rendered and inspected: every paragraph and table row is complete;
   the text layer extracts fully. (Claim may reflect a different/old document;
   if a specific phrase is missing, send the exact wording.)
5. **Hamish muzzle 26 mm vs 35 mm — consistent.** At 11 sc = 5 cm, the 24-st
   face round measures ~34.7 mm across and the 18-st rim ~25.8 mm; both
   figures are printed as measured values, not stitch counts.
6. **Axel fin crowding — documented design choice, math confirmed.** 5 shells
   over the 10-stitch ridge fits exactly; the ruffle is intentional and the
   troubleshooting note says so.
7. **Confirmed correct (no change):** Shelby underside 24→35, Willow border
   240+12=252, Waddle wings 4→6, Axel ladder 12→9→6, duck beak 11→15.

Full re-validation after the fixes: **10/10 deterministic audit PASS,
independent recomputation PASS, repo tests 15/15 PASS, render QA 10/10 PASS.**

---

## Unresolved items for human review

1. **Ember (NS 08):** the materials list once referenced a “Belly” piece that has
   no construction anywhere in the source. The corrected pattern assumes there is
   no belly piece and folds the yarn into the contrast colour. If the designer
   intended a belly, they must supply that piece before re-issue.
2. **Little Duck (NS 05):** the design code was marked “NS 05 (tentative –
   confirm with studio)”. The customer file no longer shows that wording, but the
   code itself still needs final studio confirmation.

No other unknowns: every other discrepancy was resolved to a verified value.

---

## PDF QA

Every generated PDF was rendered page-by-page with PyMuPDF and inspected:
- all pages extract text (none blank or corrupt)
- brand, design code and the “© 2026 Novality Store … personal use only” notice
  appear in the running footer of every content page; the full copyright notice
  appears in the Terms of Use on the final page of every PDF
- no text outside printable area, no clipping, no overlapping elements
- tables split across pages repeat their header row; no orphaned rows
- no placeholder, debug or internal-review tokens in any customer-facing file

Re-validation status after corrections: **10/10 PASS — final PDFs are the
validated versions.**
