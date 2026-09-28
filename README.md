# Crochet Pattern Checker

A deterministic checker for written crochet patterns. It parses US rounds and rows, counts the stitches, and reports contradictions. It does not decide those counts with a language model.

Version 1.0.0. Repository: [arbabkhan007/Crochet-Pattern-Checker](https://github.com/arbabkhan007/Crochet-Pattern-Checker).

## What a result means

`PASS` means the written checks that ran found no error and no warning. It does not mean a photo was counted, a chart image was read, or every English sentence was understood.

These engines are not run:

- a chart image detector
- a photo stitch classifier
- a hosted language model
- a vision training set
- a process cluster

Two written cases stay unread on purpose, and the checker says so instead of guessing:

- a cinch with no stitch count, such as `Cinch shut`
- a lowercase sew line, such as `sew head to body`

An instruction line the parser did not count is named under Not checked. It is not treated as a passed round.

A hook size of 0 mm is an error in any sentence. The line does not have to say `Hook: 0 mm`. A size such as 3.0 mm or 10 mm is not that error.

A chain of 0, work of zero stitches, a skip of zero, and a repeat of zero times are errors in any sentence. A hook size written in centimeters is an error in any sentence. These do not have to match one lesson line.

A hook of 40 mm or more is a warning in any sentence, not only after `Hook:`. Chain zero and work 0 are the same errors as `ch 0` and `work 0 stitches`. A hook size written as centimeters is the same error as cm.

The words zero and one are the same defects as 0 and 1 in those written checks. Decrease five times across eleven stitches is the same error as dec x 5 on 11 stitches.

A line that starts with `>` is a quote. A line that says `do not` is a prohibition. Neither is treated as an instruction.

## Install

```bash
git clone https://github.com/arbabkhan007/Crochet-Pattern-Checker.git
cd Crochet-Pattern-Checker
python -m pip install -e ".[dev]"
```

PDF generation also needs WeasyPrint and its system libraries. The other checks do not.

## Check a pattern

```bash
crochet-check check examples/amigurumi.txt
```

A correct start for a 6-stitch sphere is:

```text
Round 1: 6 sc into magic ring (6)
Round 2: inc x 6 (12)
Round 3: (sc, inc) x 6 (18)
Round 4: (2 sc, inc) x 6 (24)
```

`Round 2: (sc, inc) x 6 (18)` after a 6-stitch round is an error. That round uses 12 stitches and more than doubles the count. It is not a valid example.

Exit status is 1 when the report has an error. Warnings do not change the exit status. `PASS_WITH_WARNINGS` is still a completed check.

## What the checker catches

On written US instructions it checks stitch counts, repeats, increases that more than double, decreases that miss their count, round order, dialect scope, a chain that is too short for the stated count, a missing repeat star, an eye count that disagrees with its materials line, a seam whose two stitch counts disagree, and an inch edge sewn to a much shorter edge. The lesson files under `consensus_lessons/` are the proofs: each wrong file is not clean, and each corrected file passes.

`docs/spec_gap.md` is the inventory. If this README and that file disagree, the file is the detailed list and this page is the contract.

## Commands that also exist

| Command | What it does | What it does not do |
|---|---|---|
| `crochet-check check` | Runs the written checker | Does not invent counts from a photo |
| `crochet-check render` | Writes 2D SVG diagrams from parsed rounds | Does not read a chart image |
| `crochet-check render-3d` | Writes an OBJ mesh for a detected sphere, hat, tube, cone, or bowl | Does not track each loop |
| `crochet-check measure` | Estimates measurements from the parsed piece | Does not replace a gauge swatch |
| `crochet-check pdf` | Writes an HTML pattern sheet, and a PDF when WeasyPrint is installed | Does not certify the pattern |
| `crochet-check explain` | Rule-based explanation. `--ai` can call a configured provider | AI output cannot override the stitch count |
| `crochet-check image` | Writes a placeholder cover unless a provider is configured | Does not count stitches in the image |
| `crochet-check yarn-calc` | Rough yardage estimate | Not a substitute for a measured swatch |
| `crochet-check progress` | Local round checklist | Not a validator |

## Examples

| File | Result |
|---|---|
| `examples/amigurumi.txt` | PASS |
| `examples/simple_hat.txt` | PASS |
| `examples/scarf.txt` | PASS |
| `examples/baby_booties.txt` | ERROR, 4 |
| `examples/intentionally_broken_pattern.txt` | ERROR, 3 |
| `examples/mini_sphere.txt` | ERROR, 4, plus 1 warning |

## Benchmarks that still report a finding

The three viewpoint files are kept as pasted. The checker is not edited to hide their findings.

- `docs/gemini_corrected.md`, whole file: `PASS_WITH_WARNINGS`. A short-row turn does not state the row-end stitches.
- `docs/chatgpt_corrected.md`, whole file: `ERROR`. A seam of 3 stitches cannot close 4 stitches.

Those are findings in the source text, not a failed install.

## Tests

```bash
python -m pytest tests/test_contract.py tests/test_stages.py tests/test_verdict.py tests/test_span.py tests/validation -q
python scripts/check_consensus.py
```

`tests/test_span.py` proves 5,000 impossible sentences. Those sentences are cases of the general checks. They are not 5,000 named engines.

## Not in this package

`experimental/` is not imported and is not part of this contract. A module that is not named on this page is not a feature of the checker.
