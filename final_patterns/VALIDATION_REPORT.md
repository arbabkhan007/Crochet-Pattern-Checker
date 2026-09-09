# Novality Store — Final Validation Report

**Date:** 2026-09-09
**Scope:** All 10 customer-facing crochet patterns in `examples/`, plus the repository's
pattern-validation toolchain used to check them.
**Result:** All 10 patterns validated clean by two independent implementations;
all 10 customer-facing PDFs generated and quality-checked.

---

## 1. Method

Every pattern was checked four independent ways:

1. **Repository validator** (`crochet-check` / `validate_pattern`) — deterministic
   stitch-count, transition, and consistency validators from `src/crochet_checker/validation/`.
2. **Independent from-scratch math checker** (`output/audit/independent_math_check.py`) —
   written separately, using its own regex parsing and stitch consumption/production
   tables (increase = +1, decrease = −1, works in every previous stitch, chain ring =
   N stitches). Agrees with the repository validator on every round of every pattern.
3. **Manual line-by-line review** — title, materials, terminology, repeats, turning,
   joins, references, missing/contradictory instructions, typos, formatting.
4. **PDF quality check** (`output/audit/qa_all_pdfs.py`) — every page of every final PDF
   rendered to an image and inspected; text, branding, copyright, and the complete
   round/row + stitch-count sequence cross-checked against the validated source.

A pattern is only marked **PASS** after corrections were re-run through checks 1–4.

> `examples/intentionally_broken_pattern.txt` is **not** a customer pattern — it is a
> validator test fixture. After the fixes below it still correctly fails with 5 errors
> (sanity check that the validators genuinely catch mistakes).

## 2. Toolchain repairs (repo's own code)

The validation tooling itself had defects that would have masked or misreport errors.
These were fixed **before** any pattern was declared valid:

| # | Defect | Fix |
|---|--------|-----|
| T1 | `validation/__init__.py` imported a non-existent `validator` module — the CLI crashed on every command | Restored the repo's own working interface (from `__init__.py.backup`) exporting `validate_pattern`, `OverallStatus`, `Severity` |
| T2 | `visualization/__init__.py` and `pdf/__init__.py` were missing exports the test suite, CLI, and web app require (`generate_circle_diagram`, `measure_pattern`, `PDFConfig`, `PDFGenerator`, `generate_pdf_html`, …); the PDF generator was an empty stub writing a text file | Re-exported the existing modules; implemented the full HTML document generator to the interface defined by `tests/pdf/test_pdf.py` (cover, materials, abbreviations, instructions, measurements, validation report) |
| T3 | Parser silently **dropped every instruction group after the first** in comma-separated lines: `10 sc, dec x 5, 5 sc` parsed as `10 sc` only; flat rows `ch 1, turn, sc in each st across` parsed as `ch 1` only (the scarf was therefore never actually checked) | Added a multi-group instruction parser (comma groups, `st x N` multipliers, `turn` noise, nested repeat blocks) |
| T4 | Parser dropped `sl st to join` — a joined chain foundation (`ch 40, sl st to join (40)`) validated as 0 stitches, so the cowl falsely failed 12× | A joined chain ring now models as N stitches for the next round (standard crochet convention; matches the pattern's own stated count of 40) |
| T5 | Parser mis-parsed `sc in 2nd ch from hook` and `sc in each ch/st across` (chain-foundation rows) | Added `second_chain` (consumes 2 chains, produces 1 stitch) and `remaining`-across context operations to parser, model context math, and validators |
| T6 | Stitch-count validator's flat-row path skipped context-dependent operations entirely and never checked stated counts — the scarf "passed" vacuously | Row validation now mirrors round validation (context-aware consume/produce + stated-count check; chain foundations resolve against the foundation chain length) |
| T7 | Transition validator flagged false "Big drop: 42 to 1" warnings because it used non-context counts | Transition math now resolves `sc in each st around` against the previous round's count |
| T8 | Multi-piece patterns (bunny): round numbering restart at each piece was treated as errors ("Round 1 consumes 4 but Round 0 produced 18") and section headers polluted the previous round | Numbering restart is now recognised as a new-piece boundary; non-instruction lines no longer attach to rounds |

Regression tests for T3–T8 were added in `tests/parser/test_parser.py` (8 new tests).
Full suite: **100/100 passing** (was unrunnable: 3 test modules couldn't even import).

## 3. Pattern-by-pattern results

| # | Pattern (source) | PDF | Issues found | Issues corrected | Validation | Final |
|---|------------------|-----|--------------|------------------|------------|-------|
| 1 | Classic Amigurumi Ball (`amigurumi.txt`) | `NovalityStore_Pattern_01_classicamigurumiball.pdf` | None in instructions. No title/materials in source (publisher metadata added for sale) | — | PASS 100/100, both checkers agree (17 rounds: 6→12→18→24→30→36→36×6→30→24→18→12→6) | **PASS** |
| 2 | Amigurumi Bunny (`amigurumi_bunny.txt`) | `NovalityStore_Pattern_02_amigurumibunny.pdf` | None in instructions. Source lacked multi-piece metadata handling (tool gap T8) | Tool fix only | PASS 100/100; all 5 pieces verified (head 17r, body 12r, ears 10r ×2, arms 7r ×2, legs 7r ×2; assembly steps preserved) | **PASS** |
| 3 | Baby Booties (`baby_booties.txt`) | `NovalityStore_Pattern_03_babybooties.pdf` | **Round 8** `10 sc, dec x 5, 5 sc (15)` works in **25** stitches but the round only has **20** — impossible. **Round 9** `7 sc, dec x 4, 4 sc (11)` works in **19** but only has **15**. Round 10 count (11) only reachable if 8/9 were fixed | **Round 8 → `5 sc, dec x 5, 5 sc (15)`** (works in 20, ends 15). **Round 9 → `3 sc, dec x 4, 4 sc (11)`** (works in 15, ends 11). Preserves the designer's bunched-decrease opening style and the stated counts 15 and 11. Round 10 unchanged | PASS 100/100 after fix; both checkers agree end-to-end (4→8→12→16→20→20→20→15→11→11) | **PASS** |
| 4 | Simple Round Basket (`basket.txt`) | `NovalityStore_Pattern_04_simpleroundbasket.pdf` | None (earlier false "big drop" warning was tool bug T7) | — | PASS 100/100 (12 rounds, 42 sts at widest) | **PASS** |
| 5 | Simple Round Coaster (`flat_coaster.txt`) | `NovalityStore_Pattern_05_simpleroundcoaster.pdf` | None | — | PASS 100/100 (8 rounds: 6→12→18→24→30→36→42→48) | **PASS** |
| 6 | Crochet Bowl (`gradual_bowl.txt`) | `NovalityStore_Pattern_06_crochetbowl.pdf` | None | — | PASS 100/100 (10 rounds: 6→…→60) | **PASS** |
| 7 | Mini Amigurumi Ball (`mini_sphere.txt`) | `NovalityStore_Pattern_07_miniamigurumiball.pdf` | **Rounds 7–10 repeat text off by one stage** vs the stated counts: `(3 sc, dec) x 6` works in 30 but R6 has 36, and so on (stated counts 30/24/18/12 were internally consistent and correct). **Sphere not closed** — ended at 12 sts, leaving a large hole (README describes it as a sphere) | **R7 → `(4 sc, dec) x 6 (30)`, R8 → `(3 sc, dec) x 6 (24)`, R9 → `(2 sc, dec) x 6 (18)`, R10 → `(sc, dec) x 6 (12)`. Added missing **Round 11 `dec x 6 (6)`** to close the sphere the standard way (same closing as the Classic ball) | PASS 100/100 after fix; both checkers agree (6→12→18→24→30→36→30→24→18→12→6) | **PASS** |
| 8 | Beginner Scarf (`scarf.txt`) | `NovalityStore_Pattern_08_beginnerscarf.pdf` | Instructions were mathematically fine (19 sts/row) but were never actually checked (tool gap T3/T5) and the 5-row source is a swatch, not a wearable scarf | Customer version adds the standard presentation: "repeat rows 2–5 until desired length, end on a row that works like row 5". Source instructions unchanged | PASS 100/100 after tool fixes; both checkers agree (5 rows × 19 sts, chain-20 foundation resolves to 19) | **PASS** |
| 9 | Everyday Beanie (`simple_hat.txt`) | `NovalityStore_Pattern_09_everydaybeanie.pdf` | Rounds 1–24 all correct, but **crown left open at 24 sts** — a beanie with a 24-stitch hole is not a finished hat. README listed it as "10 rounds" (stale) | **Added standard closing rounds R25 `(2 sc, dec) x 6 (18)`, R26 `(sc, dec) x 6 (12)`, R27 `dec x 6 (6)`** (mirror of the opening increases; closes flat). README table updated (27 rounds; all 10 patterns listed) | PASS 100/100 after fix; both checkers agree (6→…→60→60×8→54→48→42→36→30→24→18→12→6) | **PASS** |
| 10 | Simple Round Cowl (`tube_cowl.txt`) | `NovalityStore_Pattern_10_simpleroundcowl.pdf` | None in instructions. Falsely failed 12× under the broken toolchain (tool gap T4 — joined chain ring not modelled) | Tool fix only (T4); pattern text unchanged | PASS 100/100 after tool fixes; both checkers agree (ch-40 ring = 40 sts, 12 rounds × 40) | **PASS** |

**All 10 patterns: PASS.** No pattern required a change to its design intent —
corrections only removed impossibilities and completed closings the designs obviously
required.

## 4. Customer-facing PDFs

Location: **`final_patterns/`** — 10 PDFs, A4, built by
`python -m crochet_checker.publish.build` (branded publisher module
`src/crochet_checker/publish/`).

Verified per PDF (automated + rendered-page inspection of all 32 pages):

- Cover: NOVALITY STORE brand, pattern title, tagline, difficulty/time/size — present on all 10
- Sections: Overview · Materials · Gauge · Abbreviations · Notes · Instructions ·
  Finishing · Helpful Tips (only where relevant; bunny adds per-piece headers)
- Every round/row renders with badge, instruction, and stitch-count chip; identical
  consecutive rounds merged into readable ranges with helper notes
  (e.g. "Rounds 2–12 — Work this round 11 times")
- Full instruction sequence in each PDF cross-checked against the validated source — exact match
- Copyright notice (exact wording from the brief) appears in the boxed
  "Copyright & Licence" block on the final page of **every** PDF, and the short form
  "© 2026 Novality Store · Personal use only" runs in the footer of every page
- No clipped/overlapping text, no blank pages, correct "Page X of Y" footers,
  special characters (×, —, –, ©, ·) render correctly
- No placeholder, debug, or internal-process text anywhere (automated leak check)

## 5. Publisher-supplied information (not in the original sources)

The raw source files contain only stitch instructions (the bunny additionally states
yarn/hook, which were kept as-is). For sale, each pattern needed standard product
information, supplied by the publisher in the customer-facing versions:

- Titles, taglines, overviews, difficulty and time estimates
- Yarn weights/quantities and hook sizes (worsted + 4.0 mm as the house default;
  DK + 3.5 mm for the bunny/booties, consistent with the bunny's own stated spec)
- Finished sizes — **estimates** calculated from the stitch counts at a typical
  6 mm single-crochet stitch, and labelled "about" in the PDFs
- Gauge lines, notes, finishing steps, and tips (standard, non-controversial guidance)

A human should confirm yarn quantities and finished sizes after test-making, before
publishing on Etsy. Nothing here changes any stitch instruction.

## 6. Unresolved / for human review

1. **Yarn quantities & finished sizes** are publisher estimates (see §5) — test-make.
2. **Bunny eye placement** — the source only says "add safety eyes"; the PDF says
   "sew on the safety eyes and embroider a small nose" without a specific round.
   Add a placement note (e.g. between rounds 7–8, 6 sts apart) if desired.
3. **Beanie/cowl sizing** — 60-stitch head ≈ 35–38 cm and 40-stitch cowl ≈ 24 cm
   circumference are stated as-is from the math; confirm intended wearer (child/snug
   adult for the cowl).
4. All other design questions were resolvable from the patterns themselves;
   **no unresolved mathematical or logical issues remain.**

## 7. Re-validation confirmation

- After corrections, all 10 patterns were re-run through the repository validator
  (100/100 each), the independent from-scratch checker (PASS, 0 bad rounds), and
  the broken-fixture sanity check (still fails, 5 errors).
- Full test suite: **100/100 passing** (`pytest tests/`).
- All 10 final PDFs re-checked after generation (text + rendered pages).
