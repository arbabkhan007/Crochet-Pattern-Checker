# Wrong benchmark patterns

These five patterns are intentionally wrong. They are study notes, not passing samples.

Do not move them into `learning_pairs` until `scripts/check_learning_pairs.py` can prove the wrong file fails and a corrected file passes. The current checker does not see every defect marked below. Short-row gaps, shell frills, and assembly sentences written in plain prose are the usual misses.

Each pattern keeps the wrong text first. A corrected line is given only where the stitch numbers are complete enough to fix without inventing the rest of the pattern.

## Pattern 1: Classic Amigurumi Bear

Skill: beginner.

Gauge: 20 sts and 22 rnds = 4 inches in sc with a 3.5 mm hook.

Materials: worsted weight yarn, Color A brown; 3.5 mm hook; polyfill; tapestry needle; 10 mm safety eyes.

Abbreviations: sc, inc, dec, ch, sl st.

### Head and body

```text
Round 1: 6 sc into magic ring (6)
Round 2: inc x 6 (12)
Round 3: (sc, inc) x 6 (18)
Round 4: (2 sc, inc) x 6 (24)
Rounds 5-8: sc in each st around (24)
Round 9: (2 sc, dec) x 6 (18)
Insert safety eyes between rounds 6 and 7, 4 stitches apart.
Round 10: (sc, dec) x 6 (12)
Stuff head.
Round 11: inc x 12 (24)
Rounds 12-15: sc in each st around (24)
Round 16: (2 sc, dec) x 6 (18)
Round 17: (sc, dec) x 6 (12)
Round 18: dec x 6 (6)
Fasten off and cinch shut.
```

Defect: Round 11 doubles 12 stitches to 24 and skips the 18-stitch neck. The fabric puckers.

Corrected lines:

```text
Round 11: (sc, inc) x 6 (18)
Round 12: (2 sc, inc) x 6 (24)
```

Renumber the later body rounds after this insert. Do not jump from 12 to 24 in one round.

### Arms, make 2

```text
Round 1: 6 sc into magic ring (6)
Round 2: (2 sc, inc) x 2 (8)
Rounds 3-8: sc in each st around (8)
Round 9: dec x 4 (4)
Fasten off and cinch shut.
```

Defect: cinching the last round shut makes a sealed cap. It cannot be sewn flat to the body.

Corrected lines:

```text
Round 9: sc in each st around (8)
Fasten off, leaving a tail for sewing. Do not cinch.
```

### Assembly

```text
Sew arms to sides of body.
```

Defect: the assembly names no legs and no ears, and those pieces are not in the pattern.

Corrected addition: write a Leg section and an Ear section before this line, then sew the pieces that were actually made. Do not name a piece that has no rounds.

## Pattern 2: Celestial Wyvern

Skill: advanced.

Gauge: 22 sts and 24 rnds = 4 inches in sc with a 3.25 mm hook.

Materials: DK yarn, Color A indigo, Color B gold; 3.25 mm hook; polyfill; safety eyes.

Glossary: sc, inc, dec, hdc, dc, ch, sl st, BLO.

### Torso and leg join

```text
Rounds 1-12, legs, make 2: 12 sc around. Fasten off leg 1. Keep the working yarn on leg 2.
Round 13: sc 12 around leg 2, ch 3, sc 12 around leg 1, sc 3 across ch (30)
```

Defect: 12 + 12 + 3 + 3 = 30 only if both sides of the chain are worked. The line crosses the chain once, so 3 stitches under the crotch are never worked and a hole remains.

Corrected line:

```text
Round 13: sc 12 around leg 2, ch 3, sc 12 around leg 1, sc 3 across the chain, sc 3 across the underside of the chain (30)
```

### Wing edging

```text
Row 1: ch 15, sc in 2nd ch from hook and across (14)
Row 2: (sl st, hdc, dc, hdc, sl st) in each st across (70)
```

Defect: 5 stitches worked into every base stitch is a 5 times full frill. A wing membrane will bunch.

Corrected line:

```text
Row 2: sc in each st across (14)
```

## Pattern 3: Clockwork Dragon

Skill: master.

Gauge: 24 sts and 26 rnds = 4 inches in sc with a 3.0 mm hook.

Materials: fingering yarn; 3.0 mm hook; 10 mm safety eyes.

Glossary defines hdc and never uses it. Also defines sc, inc, dec, fpdc, and FLO.

These rounds are abbreviated on purpose. They record the defect, not a complete pattern.

```text
Rounds 1-11: standard sphere growth to 34 sts.
Rounds 11a-11c: short rows worked over 12 sts.
Round 12: works 28 of 34 perimeter positions.
Round 15: (5 sc, dec) x 2, 2 sc. Incoming 14. Stated 16.
Torso round 15: a 6-stitch decrease repeat meets 38 stitches, while the round expects 40.
Assembly: sew 3 unworked leg sts to 4 skipped torso sts.
Wing row 4: FLO, 12 sc, inc on 14 sts. Consumes 13, leaves 1, makes 14 not 15.
Wing row 5: fpdc worked into a row of sc.
Wing tab: 1.17 inches wide. Socket: 0.55 inches wide.
Tail rounds 22-24: stated 16, operations make 14.
Safety eyes are listed in Materials and never mentioned in the instructions.
```

Defects:

1. Round 12 leaves 6 raw row-ends unworked, so each jaw corner has an open 3-row gap.
2. Head round 15 states 16 and makes 14. The repeat does not tile 14.
3. Torso round 15 has 38 stitches for a formula that expects 40.
4. A 3-stitch leg edge is sewn to a 4-stitch torso skip.
5. Wing row 4 consumes 13 of 14 and makes 14, not 15.
6. fpdc is worked into sc.
7. The wing tab is about 2.1 times the socket.
8. Tail rounds 22-24 state 16 and make 14.
9. Safety eyes are a ghost material.

Corrected lines, using only the numbers above:

```text
Head round 15: (5 sc, dec) x 2 (12)
Assembly: previous body 4, worked 0, skipped 4, limb held 4
Wing row 4: sc in each st across (14)
Wing row 5: hdc in the previous row, then (fpdc) x 14
Wing tab: make the tab 0.55 inches wide, or widen the socket to 1.17 inches
Tail: change the stated count to 14, or add the 2 missing stitches
Instructions: attach the safety eyes. Remove hdc from the glossary if it is still unused.
```

The short-row gap and the inch measurements are real defects. This checker does not yet build those sites or read inch sizes written in prose.

## Pattern 4: Abyssal Leviathan

Skill: grandmaster.

Gauge: 24 sts and 26 rnds = 4 inches in sc with a 3.0 mm hook.

### Primary tentacle, make 2

```text
Round 1: 8 sc into magic ring (8)
Rounds 2-20: grow to 12 sts.
Rounds 21-30: split into branch alpha and branch beta.
Both tips: dec, then cinch shut.
```

Defect: the base is closed by the magic ring and both tips are cinched. The tentacle is a sealed tube. It has no open stitches for a socket.

Corrected ending: leave the base open, or leave one branch end uncinched, and state how many stitches are held for the join.

### Body hub

```text
Round 14: 48 sc (48)
Round 15: 4 sc body, 4 sc tentacle 1, 4 sc body, 3 sc arm 1, 3 sc arm 2, 12 sc body, 3 sc arm 3, 3 sc arm 4, 4 sc body, 4 sc tentacle 2, 4 sc body (54)
Round 16: sc in all 54 sts around, working across the outer remaining stitches of the attached limbs (54)
Round 17: (7 sc, dec) x 6 (48)
Assembly: cinch 5 unworked inner stitches of the secondary arms to 3 body socket stitches.
```

Defects:

1. Round 15 works 4 + 4 + 12 + 4 + 4 = 28 body stitches out of 48. Twenty body stitches disappear, and the round never says to skip them.
2. The clauses in round 15 add to 48, not the stated 54.
3. Round 16 says to work the outer limb stitches as well. That is a different count from 54, not a plain repeat of round 15.
4. Round 17 uses a 9-stitch repeat six times, which needs 54 stitches. Round 15 only produced 48.
5. Assembly sews 5 stitches to 3.

Corrected shape:

```text
Round 15: state every skipped body stitch. Worked body plus skipped body must equal 48. The stated count must equal the stitches actually worked.
Round 16: count the outer limb stitches, then write that number. Do not reuse 54 unless the sum is 54.
Round 17: (6 sc, dec) x 6 (42) only if 48 stitches are coming in.
Assembly: previous body 3, worked 0, skipped 3, limb held 3
```

### Cranial vault and fin

```text
Cranial round 15: switch to color B in FLO, (5 sc, bpdc) x 7
Cranial round 19: (5 sc, dec) x 6 (36) on 44 stitches
Fin row 4: FLO, 15 sc, inc (18) on 17 stitches
Fin row 6: 5 stitches in each row end
Assembly: sew a 3.33 inch fin to a 1.69 inch body span
```

Defects:

1. bpdc on the front loop pushes the ridge to the inside of the head, where it cannot be seen.
2. The post stitch is worked into sc.
3. Round 19 consumes 42 of 44 and leaves 2 unworked. It does not make 36.
4. Fin row 4 consumes 16 of 17, leaves 1, and makes 17, not 18.
5. Five stitches per row end is about 5.4 times full.
6. The fin seam is about twice the body span.

Corrected lines:

```text
Cranial round 15: (5 sc, fpdc) x 7, worked into an hdc or dc round
Cranial round 19: 32 sc, dec x 6 (38) if 44 stitches are coming in
Fin row 4: 15 sc, inc (17) only if 16 stitches are used and 1 remains, or work all 17
Fin row 6: sc in each row end
Assembly: match the fin length to 1.69 inches, or lengthen the body seam to 3.33 inches
```

## Pattern 5: Void-Warped Chimera

Skill: nightmare.

Gauge: 22 sts and 24 rnds = 4 inches in sc with a 3.5 mm hook.

### Cranial core

```text
Round 14: 44 sc (44)
Round 15: (5 sc, dec) x 6 (38)
Round 16: (2 sc, fptr) x 12, 2 sc, worked into round 14 (38)
Round 17: (4 sc, dec) x 6 (32)
Round 18: (3 sc, dec) x 6 (26)
```

Defects:

1. Round 15 does not tile 44. A 6-stitch unit leaves 2 stitches unworked, and the repeat does not make 38.
2. Round 16 works fptr into round 14, an sc round two rounds below. The post has no tall foundation.
3. Round 17 uses 36 of 38 and does not make 32.
4. Round 18 uses 30 of 32 and does not make 26.

Corrected lines if round 14 really has 44:

```text
Round 15: 32 sc, dec x 6 (38)
Round 16: (2 sc, fptr) x 12, 2 sc, worked into an hdc or dc round (38)
Round 17: 26 sc, dec x 6 (32)
Round 18: 20 sc, dec x 6 (26)
```

`(5 sc, dec)` makes as many stitches as it uses, so it cannot be the decrease. `32 sc, dec x 6` is the decrease that turns 44 into 38.

### Torso and frill

```text
Round 7: work 21 body stitches from a 24-stitch body, and join 3 stitches of a closed tentacle
Round 12: 756 stitches worked into 108 base stitches
```

Defects:

1. Three body stitches disappear. The tentacle was closed, so it has no live stitches to join.
2. 756 stitches on 108 base stitches is a 7 times full frill. It is not a usable edge.

Corrected lines:

```text
Round 7: work 24 body stitches, or write the skipped body stitches so worked plus skipped equals 24. Join only an open tentacle edge.
Round 12: sc in each st around (108)
```

### Assembly

```text
Graft a 30-stitch partition into cranial round 15, written as 38.
Sew a 26-stitch head to an 18-stitch torso.
Cinch 6 held tentacle stitches to 6 skipped body stitches.
Mount 2 safety eyes on the frill.
```

Defects:

1. 30 does not match 38.
2. 26 does not match 18.
3. Round 7 left only 3 body stitches, not 6.
4. A free treble frill has no fabric behind it for a safety-eye washer.

Corrected lines:

```text
Graft the partition into a 30-stitch round.
Sew the head to a 26-stitch torso opening, or decrease the head to 18 before sewing.
Assembly: previous body 24, worked 18, skipped 6, limb held 6
Mount safety eyes on a solid sc round, not on the frill.
```
