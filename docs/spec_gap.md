# What this repo has against the full verification spec

The specification describes a multi-year system. This file says what the current code does. It does not claim the missing engines exist.

## Stages that run on written text

1. Dialect scope. A piece marked UK cannot use `sc` or `hdc`. A piece marked US cannot use `htr` or `trtr`. Pieces may declare different dialects. `dc` is not treated as proof of either dialect.
2. Termination. `Repeat until the piece is long enough` is an error. A stitch, round, or inch stop passes.
3. Stitch reachability. The 9th stitch is an error when the previous round has 6. A skip past the live stitches is an error. An unused loop is an error when that round already worked both loops.
4. References. `Join to Round 9` is an error when Round 9 never starts. `Sew the Ear to the Head` is an error when Ear never starts. A lowercase sentence such as `sew head to body` is still unread.
5. Chart text. `Chart row 1: X V X (4)` is an error because the symbols produce 3. The legend in the pattern defines the symbols.
6. Ambiguity. `sc in next st`, with no count and no around or across, warns. This is a written rule, not a language model.
7. Gauge band. A count outside half to double the Craft Yarn Council crochet single-crochet band warns. Worsted is 11 to 14 per 4 inches, so 40 warns and 12 does not. A tight amigurumi gauge such as 20 does not warn. Lace is not banded. Source: https://www.craftyarncouncil.com/standards/yarn-weight-system
8. Short-row gap. After short rows, `works 28 of 34` is an error until the 6 row-ends are written. A normal decrease is not a short row.

`verify_pattern` runs these stages with the existing text checker. `Sew the Ear` is a missing piece only when Ear is capitalized. `attach the safety eyes` and `Attach the tentacle externally` are not piece names.

## Still not run

- A chart image is not detected. `read_chart_image` does not invent symbols.
- A photo is not classified. `inspect_photo` does not open the file and does not invent stitch or row counts.
- No hosted language model is installed.
- No vision training set is installed.
- No process cluster is installed. The stages run in this process, in order.

## Already had

- A custom text parser for US rounds, rows, repeats, increases, and decreases. It is not tree-sitter.
- Stated count, repeat cover, post foundation, ghost eyes, equal socket, edging fullness, span match, tab fit, clause total, 12-to-24 neck jump, unequal stitch seam, and unequal inch seam.
- A shape mesh for a sphere, hat, tube, cone, or bowl. It does not track each loop. Stage 3 is the written reachability check, not that shape mesh.
- PDF text reading, a small web app, and a learning store that does not change the rules by itself.
