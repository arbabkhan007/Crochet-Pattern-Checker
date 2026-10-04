# What this repo has against the full verification spec

The specification describes a multi-year system. This file says what the current code does. It does not claim the missing engines exist.

## Stages that run on written text

1. Dialect scope. A piece marked UK cannot use `sc` or `hdc`. A piece marked US cannot use `htr` or `trtr`. Pieces may declare different dialects. `dc` is not treated as proof of either dialect.
2. Termination. `Repeat until the piece is long enough` is an error. A stitch, round, or inch stop passes.
3. Stitch reachability. The 9th stitch is an error when the previous round has 6. A skip past the live stitches is an error. An unused loop is an error when that round already worked both loops.
4. References. `Join to Round 9` is an error when Round 9 never starts. `Sew the Ear to the Head` is an error when Ear never starts. A lowercase sentence such as `sew head to body` is an error when head or body never starts.
5. Chart text. `Chart row 1: X V X (4)` is an error because the symbols produce 3. The legend in the pattern defines the symbols.
6. Ambiguity. `sc in next st`, with no count and no around or across, warns. This is a written rule, not a language model.
7. Gauge band. A count outside half to double the Craft Yarn Council crochet single-crochet band warns. Worsted is 11 to 14 per 4 inches, so 40 warns and 12 does not. A tight amigurumi gauge such as 20 does not warn. Lace is not banded. Source: https://www.craftyarncouncil.com/standards/yarn-weight-system
8. Short-row gap. After short rows, `works 28 of 34` is an error until the 6 row-ends are written. A normal decrease is not a short row.
9. Prose frill. `756 stitches worked into 108 base stitches` warns at 7.0x. The same 2.5x line used for edging applies. One stitch per base stitch does not warn.
10. Eyes on a frill. `Mount 2 safety eyes on the frill` is an error. `not on the frill` does not fail.
11. Closed join. `Join 3 stitches of a closed tentacle` is an error. `Cinch the last round shut and sew it flat` is an error. `Cinch shut` closes the last stated round, and is an error when no counted round comes before it.
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
29. Make count. `Ears (make 2)` cannot be sewn as 3 ears. A sew line that names those ears but gives no number is named. The count is not guessed.
30. Unverified claims. A finished-size range, a gauge the maker must match with no tested sample, a yarn range that was not weighed, and an approximate opening are warnings. No sample measurement is invented. `yarn-calc` and `explain` name an unweighed estimate. They do not call it a finished size.
30. Zero repeat. `Repeat x 0` is an error.

`verify_pattern` runs these stages with the existing text checker. `Sew the Ear` is a missing piece when Ear is capitalized. `sew head to body` is a missing piece when those pieces never start. `attach the safety eyes` and `Attach the tentacle externally` are not piece names.

A counted round that works stitches of another written piece does not add them to the local sum. A seam count that no earlier round states is an error, and the missing edge is not invented. A seam aimed at a magic ring or a cinched point is an error. A quoted line is not that seam. One line that names three written pieces is not drawn as a Y-branch, and the missing seams are not invented. None of these is a measured fit.

A seam that names the same piece on both sides is an error. The other side is not invented. Fasten off ends that yarn: a later counted round in the same piece is an error. A new heading, a new piece, a different numbered part, or a line that keeps the working yarn starts again. A round line that also says turn is an error. Turn belongs to a row. A quoted line is not that instruction.

Cinch shut closes the piece. A later counted round, stuffing, or safety eyes in that same piece are an error. A new heading or a new piece starts again. A second magic ring in the same piece is an error. A line that says a chain counts as a stitch and does not count is an error. A line that fastens off and does not fasten off is an error. A line with two different stitch counts is an error. A line that closes the piece and leaves it open is an error. An invisible join and a slip-stitch join on one line are two endings. A spiral that also joins the round is an error. Stuffing after "do not stuff" in the same piece is an error. One piece written as two different make counts is an error. The same contradiction is an error in any sentence, not only one copied line: both directions, both sides facing, yarn over and yarn under, reverse single crochet worked forward, both hands, two seam methods, a magic ring and a chain ring, FLO and BLO, in the round and back and forth, increase and decrease in the same stitch, a row that says around, a word that disagrees with its digit, a negative measure, a copied inch and centimetre number, and a line that does a thing and does not do it. A line that says or is a choice, not both. The same count rule also applies when the sentence is not the copied lesson line: a hook letter beside the wrong millimetre size, a yarn weight written as "worsted weight (1)", a US stitch given the wrong UK name, a steel hook whose higher number is called larger, a word count that must be even or odd, a stitch number past the written round, eyes or a skip that do not fit, a turning chain too short for sc, hdc, or dc, a slip knot counted as a stitch, the same color switched to twice, and "until it looks long enough" with no stop. A correct nominal size is not an error. The remaining copied rules also apply in any sentence: a multiple-plus count that does not add up, a chain counted twice, a width of 0 inches, a decimal stitch, a fractional or negative repeat, a round number of 200 or more, BLO and both loops, a post around a chain, a slip knot used as a stitch, fasten off then continue in that yarn, foundation sc and a starting chain, a spiral closed with a slip stitch, a stitch number past the written count, eyes or a skip that do not fit, an even count of an odd number, a hook letter written as the wrong millimetre size, a yarn category that disagrees with its name, a hook written as a centimetre word, a gauge of zero, a shell of fewer than 3, and a chain-0 space. A line that says or is still a choice. `Repeat until done` is not a stop, because `done` is not the number one. A cable, i-cord, spike, surface line, or pom-pom of 0 is an error. Stuffing with 0, a negative make count, and a negative round or row number are errors. A shell of zero, a post around `ch`, FLO and both loops, continuous rounds that also join, in the round and in rows, fasten off and keep working, stitch zero, stuffing and leaving empty, and a word count that does not fit the written row or round are errors. None of these is a measured fit.

## Still not run

- A chart image is not detected. `read_chart_image` does not invent symbols.
- A photo is not classified. `inspect_photo` does not open the file and does not invent stitch or row counts.
- No hosted language model is installed. A support chat is not called.
- A cover image is not generated. No photo is invented.
- No vision training set is installed.
- No process cluster is installed. The stages run in this process, in order.
- A physical comfort ratio is not calculated. No swatch was measured, so two parts are not declared to fit.

## Already had

- A custom text parser for US rounds, rows, repeats, increases, and decreases. It is not tree-sitter.
- Stated count, repeat cover, post foundation, ghost eyes, equal socket, edging fullness, span match, tab fit, clause total, 12-to-24 neck jump, unequal stitch seam, and unequal inch seam.
- A shape mesh for a sphere, hat, tube, cone, or bowl. It does not track each loop. `simulate` places one point per written stitch and writes a table of those points. A color is shown only when the round names one color letter. A missing color is not invented. That map is not a measured size and not a photo. An assembly line is drawn only when the line names two written pieces. A missing piece is not invented. The web render and simulate responses return that same map, the stitch map, and the geometry map. `render`, `render-3d`, and `simulate` write the same files. A round radius is the stitch count divided by 2 pi. z is the layer index. Neither is a millimetre. A color comment in the stitch file is a written label, not a measured dye. Stage 3 is the written reachability check, not that shape mesh.
- PDF text reading, a small web app, and a learning store that does not change the rules by itself.

Fifty phrase checks, lessons 44 through 93. A quoted line is not an instruction.

31. Zero hook. A hook of 0 mm cannot pull up a loop.
32. Huge hook. A 40 mm hook is past even jumbo crochet. This warns.
33. Hook in centimeters. A hook written as 5 cm is 50 mm. Crochet hooks are written in millimeters.
34. Zero chain. Ch 0 makes no chain to work into.
35. Work zero. Work 0 stitches is an instruction that does nothing.
36. Skip zero. Skip 0 does not move the hook.
37. Decrease to zero. Decreasing to 0 stitches leaves nothing to fasten or sew.
38. Until zero. Repeat until 0 stitches is not a workable stop. A digit of 0 still counts as written, so the termination rule does not catch it.
39. Round zero. Rounds are numbered from 1. Round 0 is not a round.
40. Marker at zero. Stitch 0 does not exist. The first stitch is stitch 1.
41. Zero gauge. A gauge of 0 sc per 4 inches is not a fabric.
42. Zero inches. A finished width of 0 inches is not a piece.
43. Picot of zero. A picot of 0 chains is not a picot.
44. Chain-zero space. A ch-0 space has no chains to work into.
45. Shell of one. A shell needs at least 3 stitches. A shell of 1 is a single stitch.
46. Cluster of one. A 1-dc cluster is one double crochet, not a cluster.
47. Bobble of one. A bobble of 1 has no stitches to gather.
48. Puff of one. A puff of 1 is one yarn over, not a puff.
49. Popcorn of one. A popcorn of 1 cannot be folded closed.
50. Zero yarn over. Yo 0 does not put yarn on the hook.
51. Pull through zero. Pull through 0 loops leaves the loops on the hook.
52. Decimal stitch. 6.5 sc is not a whole stitch. The hook cannot make half a single crochet.
53. Fractional repeat. X 2.5 asks for half of a repeat. Repeats are whole numbers.
54. Negative repeat. X -1 is not a repeat count.
55. Round 9000. Round 9000 is not a usable round number in this pattern.
56. Join contradiction. The same line says to join and not to join.
57. Spiral and join. A continuous spiral does not join every round. The two instructions disagree.
58. Both loop claims. BLO only and both loops cannot be the same stitch.
59. Increase and decrease. Inc and dec in each stitch cancel, and the line does not say which one.
60. Both directions. Left to right and right to left, with no or, gives two directions.
61. Two joins. An invisible join and a slip-stitch join are two finishes. The line requires both.
62. Both sides facing. The right side and the wrong side cannot both face the worker.
63. Double and single. The yarn cannot be held double and single at the same time.
64. Inside and out. Turning inside out and keeping the right side out disagree.
65. Tight and loose. One round cannot be worked tightly and loosely.
66. Same color change. Changing from Color A to Color A is not a color change.
67. Increase to the same count. An increase from 12 to 12 does not increase.
68. Increase that shrinks. An increase from 12 to 6 is a decrease. The word and the numbers disagree.
69. Decrease that grows. A decrease from 6 to 12 grows. The word and the numbers disagree.
70. Chain counted twice. A turning chain counted twice is added to the stitch count two times.
71. Post around a chain. A chain has no post. fpdc cannot go around the chain.
72. Slip knot as a stitch. The slip knot is not a chain stitch. Do not work into it.
73. Short turning chain. Ch 1 is the turning chain for sc, not for dc. A dc turn needs ch 3.
74. Round says across. A round is worked around. Across is the flat-row word.
75. Row says around. A flat row is worked across. Around is the round word.
76. Round says turn. A continuous round does not turn. Turn belongs to a flat row.
77. Backward range. Rounds 8-5 run backwards. A range has to climb.
78. Not a multiple. A multiple of 3 cannot be 10 stitches. 10 is not divisible by 3.
79. Odd when even. A count that must be even cannot be 7.
80. Eyes too far apart. Eyes 8 stitches apart cannot sit on a 6-stitch round.

Lessons 94 through 158. These are new written checks. Five thousand named copies were not added. The increase, decrease, range, multiple, and measure checks are proved on 5,000 sentences in tests/test_span.py. A quoted line is still not an instruction. A photo is still not classified.

81. Hook letter gap. H/8 written as 2.25 mm is the B-1 size, not a brand variation. The Craft Yarn Council nominal for H-8 is 5 mm. This fires only when the written millimeter is more than 1.5 mm away.
82. Yarn weight number. Worsted is Craft Yarn Council category 4, not 1.
83. Short treble turn. Ch 1 cannot turn for a treble. A treble turn needs ch 4. ch 2 for a double treble is short as well.
84. Counts-as mismatch. Ch 1 cannot count as a double crochet. A double crochet turning chain is ch 3.
85. UK gloss. A US single crochet is a UK double, not a UK treble.
86. Steel hook order. On a steel hook, a higher number is smaller. Steel 14 is not larger than steel 1.
87. Spiral turn. A continuous spiral does not turn every round.
88. Fasten and continue. Fasten off ends that yarn. The same line cannot continue in it.
89. Yarn over and under. One stitch cannot be both a yarn over and a yarn under.
90. Reverse sc direction. Reverse single crochet is worked backward, not forward.
91. Two foundations. Foundation single crochet replaces the starting chain for that row.
92. Both hands. Right-handed and left-handed work need separate instructions when both are required.
93. Two starts. A piece cannot have both a magic ring and a chain ring as its only start.
94. Two seam methods. Whipstitch and mattress stitch are different seams. One line cannot require both for the same seam.
95. Negative gauge. A gauge of -1 sc is not a fabric.
96. Negative length. A finished length of -1 inches is not a piece.
97. Zero rows tall. A piece that is 0 rows tall was not made.
98. Zero rounds tall. A piece that is 0 rounds tall was not made.
99. Row zero. Rows are numbered from 1. Row 0 is not a row.
100. Make zero. Make 0 asks for none of that piece.
101. Negative times. Repeating a row -1 times is not a repeat. This is not the x -1 form.
102. Work even zero. Work even for 0 rows does no work.
103. Place zero eyes. Place 0 safety eyes is an instruction that mounts nothing.
104. Zero yardage. 0 yards cannot make the piece.
105. Stuff zero. Stuff with 0 g leaves the piece empty while telling the crocheter to stuff.
106. Color every zero. Changing color every 0 rows never changes color.
107. Increase every zero. Increasing every 0 rounds never increases.
108. Decrease every zero. Decreasing every 0 rows never decreases.
109. V-stitch of one. A V-stitch needs two tall stitches and a chain. A V-stitch of 1 is one stitch.
110. Fan of one. A fan needs several stitches in one space. A fan of 1 is one stitch.
111. Bullion of zero. A bullion of 0 wraps has no wraps to coil.
112. Cable of zero. A cable over 0 stitches does not cross.
113. Fringe of zero. A fringe of 0 strands is not a fringe.
114. Buttonhole of zero. A buttonhole of 0 chains has no opening.
115. I-cord of zero. An i-cord of 0 stitches has no cord.
116. Oval of zero. An oval cannot start with 0 chains.
117. Square of zero. A square of 0 rounds was not worked.
118. Solomon knot of zero. A Solomon knot of 0 is not a knot.
119. Surface of zero. Surface crochet of 0 chains draws no line.
120. Bead every zero. A bead every 0 stitches is never placed.
121. Stripe every zero. A stripe every 0 rounds never stripes.
122. Pom-pom of zero. A pom-pom of 0 wraps has nothing to tie.
123. Tassel of zero. A tassel of 0 wraps has nothing to hang.
124. Pineapple of zero. A pineapple of 0 is not a pineapple motif.
125. Spike of zero. A spike stitch down 0 rows does not leave the current row.
126. Tube of zero. A tube of 0 stitches has no opening.
127. Rectangle of zero. A rectangle of 0 rows was not worked.
128. Corner of zero. A corner of 0 chains does not turn the corner.
129. Star of one. A star stitch of 1 cannot pull up the loops a star needs.
130. Loop of zero. A loop stitch of 0 has no loop.
131. Same color letter. Changing from Color Q to Color Q is not a color change. The check is any repeated letter, not only A.
132. Increase direction. Any increase whose second number is not higher fails. This is not limited to 12 to 6.
133. Decrease direction. Any decrease whose second number is not lower fails. This is not limited to 6 to 12.
134. Multiple mismatch. A stated count that is not divisible by the written multiple fails. This is not limited to 3 and 10.
135. Plus remainder. A count that is not the written multiple plus the written remainder fails.
136. Backward round range. A round range whose first number is higher runs backwards. This is not limited to 8-5.
137. Backward row range. A row range whose first number is higher runs backwards.
138. Even count. An odd number cannot be required to be even. This is not limited to 7.
139. Odd count. An even number cannot be required to be odd.
140. Apart span. Eyes farther apart than the round cannot sit on it. This is not limited to 8 on 6.
141. Stitch past end. A marker past the last stitch cannot be placed.
142. Skip past count. A skip of the whole row or more does not fit.
143. Fractional times. Any repeat written as x N.N is not a whole repeat. This is not limited to 2.5.
144. Copied inch measure. The same number in inches and centimeters is not a conversion. One inch is 2.54 cm.
145. Copied centimeter measure. The same number in centimeters and inches is not a conversion.

A hook letter written as `H/8 is 2.25 mm` is the same gap as the parenthetical size. `ch 1, turn for dc` is too short. `ch 1 counts as dc` cannot count as that stitch. A V-stitch, fan, star, or cluster of one is not that stitch. A loop of zero has no loop. An oval of zero chains and a rectangle of zero rows were not worked. Yarn held doubled and single is both. Eyes twelve apart on a round of six do not fit. Foundation sc and a chain used to start are two starts. A fringe of no strands is not a fringe. A quoted line is not an instruction. No length is invented.

`Work no stitches`, `round none`, and `made of zero` are the same empty counts. `ch one, turn for dc` is still too short. `Rounds 8 to 5` run backwards. A quoted line and a line that says `or` stay choices. No length is invented.

`Inc from 12 to 6`, `rnd 8 to rnd 5`, `colour A to colour A`, and `ch-1 counts as dc` are the same written rules. A line that says `or` stays a choice. No length is invented.

`ch1, turn for dc`, `8in = 8cm`, and `H/8 = 2.25mm` are the same written rules with the space left out. `4 inches = 10.16 cm` stays a real conversion. No length is invented.

`I-cord uses no stitch`, `cable crosses no stitch`, and `make none` are the same empty counts. `No stitches are left unworked` stays a valid sentence. No length is invented.

`Puff is one stitch`, `picot = 0`, and `round goes side to side` are the same written rules. `sc (UK double)` stays correct. No length is invented.

`Righties and lefties`, `Fsc and ch 12 to start`, and `increase shrinks, 12 to 6` are the same written rules. A line that says `or` stays a choice. No length is invented.
