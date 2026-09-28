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
9. Prose frill. `756 stitches worked into 108 base stitches` warns at 7.0x. The same 2.5x line used for edging applies. One stitch per base stitch does not warn.
10. Eyes on a frill. `Mount 2 safety eyes on the frill` is an error. `not on the frill` does not fail.
11. Closed join. `Join 3 stitches of a closed tentacle` is an error. `Cinch the last round shut and sew it flat` is an error. `Cinch shut` alone is still unread.
12. Chain underside. A stated 30 that needs both sides of `ch 3`, while the line crosses the chain once, is an error.
13. Dropped body stitches. `Work 21 body stitches from a 24-stitch body` is an error until the skip of 3 is written.
14. Front and back post. `bpdc` in `FLO` is an error. A line that starts with `>` is a quote, not an instruction.
15. Eyes before stuffing. Safety eyes written after `Stuff the head` are an error.
16. Row-end density. `5 stitches in each row end` warns. One stitch in each row end does not.
17. Incoming cover. `(5 sc, dec) x 6` on 44 stitches is an error because the repeat uses 42.
18. Missing color. `Color B` is an error when the yarn line lists only `Color A`. A fragment with no color list is not checked.
19. Round order. A repeated round number inside one piece is an error. A new piece may start again at Round 1.
20. Every base stitch. `5 stitches worked into every base stitch` warns. One stitch does not.
21. Chain length. `ch 10`, started in the second chain, cannot hold a stated 12. Nine is the most.
22. Unclosed repeat. A round whose parentheses do not balance is an error.
23. Missing star. `Rep from *` with no opening star is an error.
24. Decrease cover. `dec x 5 on 11 stitches` is an error because the decrease uses 10.
25. Over-double increase. A stated jump from 6 to 18 is an error. A jump from 6 to 12 is not.
26. Written-as count. A 30-stitch edge written as 38 is an error.
27. Eye count. Materials `(x2)` and `Mount 4 safety eyes` is an error. Counts are compared only inside one pattern section.
28. Future round. Round 2 cannot work into Round 5.
29. Make count. `Ears (make 2)` cannot be sewn as 3 ears. A line with no number is still unread.
30. Zero repeat. `Repeat x 0` is an error.

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
