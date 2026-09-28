# What this repo has against the full verification spec

The specification describes a multi-year system. This file says what the current code does. It does not claim the missing engines exist.

## Have

- A custom text parser for US rounds, rows, repeats, increases, and decreases. It is not tree-sitter.
- A deterministic checker. The compiler, not a model, decides stitch counts.
- Proved rules: stated count, repeat cover, post foundation, ghost eyes, equal socket, edging fullness in checker dialect, span match in checker dialect, tab fit, clause total, 12-to-24 neck jump, unequal stitch seam, unequal inch seam.
- A shape mesh that can export a sphere, hat, tube, cone, or bowl. It does not track each stitch's loops.
- US/UK term translation and a mixed-term warning. It is not a per-piece dialect scope.
- PDF text reading, a FastAPI app, and a learning store that does not change the rules by itself.
- Gauge image intake that stores a photo only after a person confirms the stitch and row counts.

## Partial

- Materials, hook, and gauge lines are read when they match the parser.
- Assembly joins are checked when the counts are written as numbers.
- Yarn and gauge estimates are formulas, not trained models.
- Optional cloud explanation runs only when an API key is set. It cannot override the checker.

## Do not have

- Chart symbol detection.
- Photo classification of stitch type.
- A stitch mesh that can say whether a loop is still reachable.
- A hosted 70B model, a vision training set, or a benchmark corpus.
- Kubernetes, a job queue, or automatic pattern generation.

`verify_pattern` runs only the text checker. Its result lists the engines that were skipped.
