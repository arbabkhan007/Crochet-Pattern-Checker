# Pattern Review — "Celestial Wyvern"

**Verdict: ⚠️ CLOSE, BUT NOT RELEASEABLE — 5 hard defects, 3 of them in the leg-to-body join.**

| | |
|---|---|
| Pieces checked | 6 (Head & Neck, Toe, Foot/Leg, Torso, Wing, Tail) |
| Rounds / rows checked | 46 instruction lines = 75 physical rounds & rows |
| **Hard defects** | **5** |
| Structural / instruction gaps | 7 |
| Documentation gaps | 6 |
| Proportion advisories | 4 |
| Pieces that are 100 % correct | Head & Neck, Toe, Wing rows 1–5 |

This is a far stronger pattern than most. The abbreviation list is **complete** (every one of
`sc inc dec hdc dc tr sl st ch BLO FLO` is defined *and* used), the head/neck shaping is flawless,
the three-toe join arithmetic is exactly right, and — the thing patterns most often get wrong —
**the Neck (Round 17, 18 sts) and the Torso (Round 21, 18 sts) interface matches perfectly.**

The problems are concentrated in three places: the leg top, the leg-to-body join, and the wing.

---

## 1. Hard defects

Notation: `sc` consumes 1 / makes 1. `inc` consumes 1 / makes 2. `dec` consumes 2 / makes 1.
A round is valid only when **consumed = available** *and* **made = stated**.

### 🔴 D1 — Leg, Round 11: stated count is wrong by 1

> `Round 11: [sc 2, dec] 3 times. (8 sts)`

You arrive with 12 sts. Each `[sc 2, dec]` eats 2 + 2 = **4**, so 3 repeats eat **12 ✔** — consumption
is correct. But each repeat makes 2 + 1 = **3**, so 3 repeats make **9 sts, not the stated 8**.

**This one matters more than it looks — see D3.**

**Fix:** `Round 11: [sc 2, dec] 3 times. (9 sts)`

### 🔴 D2 — Torso, Round 13: 6 body stitches are silently abandoned

> `Round 13: sc 10 across Body, sc 6 across inner side of Leg 1, sc 12 across Body, sc 6 across inner side of Leg 2, sc 8 across Body. (42 sts)`

The body arrives with **36 sts**. The round works 10 + 12 + 8 = **30 of them**.
**6 body stitches are never worked into and are never mentioned again.** They are not skipped, not
joined, not sewn — they simply vanish from the pattern, leaving a 6-stitch hole at the crotch.

(The stated total is fine: 10 + 6 + 12 + 6 + 8 = 42 ✔. The round produces the right number; it just
doesn't consume the right number.)

### 🔴 D3 — Torso, Round 13: the leftover leg stitches are also abandoned — and they prove D1 is a typo

Each leg arrives at the join with 8 sts (as stated) and only **6** are worked. That leaves 2 per leg,
4 in total, unaccounted for — against 6 abandoned body stitches. Those don't match, so there is no
clean way to close the gap.

Now substitute the **mathematically correct** leg top from D1:

| Leg top | Leftover leg sts | Skipped body sts | Do they close? |
|---|---|---|---|
| 8 (as stated) | 4 | 6 | ❌ no |
| **9 (actual math)** | **6** | **6** | ✅ **exactly** |

So the `(8)` in Leg Round 11 is a **typo for `(9)`**, and the pattern is missing one instruction:
*join the 3 remaining stitches of each leg to the 3 skipped body stitches to close the crotch.*
With 9-stitch legs the whole join balances to the stitch. Without it, every maker will improvise a
different lumpy crotch.

**Fix:** correct Leg R11 to `(9 sts)`, then rewrite Round 13 symmetrically:
```
Round 13: sc 15 across Body, sc 6 across outer side of Leg 1, skip next 3 Body sts,
          sc 15 across Body, sc 6 across outer side of Leg 2, skip next 3 Body sts. (42 sts)
```
Body: 15 + 3 + 15 + 3 = 36 ✔  Made: 15 + 6 + 15 + 6 = 42 ✔
Then: *"Using each leg's tail, sew its 3 remaining sts to the 3 skipped Body sts to close the crotch."*

This also fixes an asymmetry: as written, the legs sit 12 sts apart on one side and **18 on the
other**, so the wyvern is knock-kneed. 15 / 15 puts them level.

### 🔴 D4 — Tail, Rounds 17–20: stated count is wrong by 2

> `Round 17–20: sc around. (12 sts)`

You arrive from Round 16 with **10 sts**. "sc around" makes exactly one stitch per stitch, so these
rounds give **10, not 12**. A plain round can never change the stitch count.

**Fix (keeps the author's 12):**
```
Round 17:    [sc 4, inc] 2 times. (12 sts)
Rounds 18-20: sc around. (12 sts)
```

### 🔴 D5 — Wing, Row 6: the feather edging is ambiguous and fails under *both* readings

> `Row 6: *[sl st, hdc, dc, tr, dc, hdc, sl st]* into first row end, repeat across remaining row ends.`

The wing has 5 rows, so **5 row ends**. There are only two ways to read this and neither works:

**Reading A — all 7 stitches into one row end (a shell), repeated into every row end.**
That is 7 × 5 = **35 stitches crammed onto a 0.91 in edge**, a density of **7 stitches per row end**.
A standard shell or feather edging runs a 5–7 stitch fan every *2nd or 3rd* row end — 2 to 3.5
stitches per row end. This is **2–3.5× too dense**, and because there is no anchoring sc or sl st
*between* fans there is nothing to control the fullness. The edge will ruffle into a cabbage frill.

**Reading B — the 7 stitches spread across 7 consecutive row ends (the classic feather fan).**
One fan needs **7 row ends. The wing has 5.** You cannot complete even a single fan.

Also: "Row 6" is not a row — it is an edging worked perpendicular to Rows 1–5. And the pattern never
says *which* of the two row-end edges to work along.

---

## 2. Structural & instruction gaps

### 🟠 S1 — The Head & Neck direction note is backwards
> *"(Worked top to snout, then transitioning to neck in continuous spiral)"*

The shaping says otherwise. Rounds 1–4 increase to 24, Rounds 5–9 run straight, Rounds 10–11
decrease to 12, and **Rounds 12–17 are the neck**. Since the neck must leave the *back* of the head,
Round 1 has to be the **snout tip** and Round 11 the nape. As written, the note tells you to start at
the top of the skull — which puts the neck growing out of the snout.

This is not cosmetic: it determines which end you stuff, and it determines whether the eyes at
Rounds 6–7 land on the face or the back of the head.

**Fix:** *"Worked from the snout tip back to the nape, then continuing into the neck in a continuous spiral."*

### 🟠 S2 — The spiral instruction only covers one piece
"continuous spiral" appears once, in the Head & Neck heading. The Torso, Legs, Toes and Tail are all
spirals too and never say so. Promote it to a global Notes section: *"All pieces except the Wings are
worked in continuous spirals. Do not join or turn. Mark the first stitch of each round."*

### 🟠 S3 — The neck is never stuffed
The pattern says stuff the head, the leg and the torso — but Rounds 12–17 are the neck and it is
never mentioned. An unstuffed 15-stitch neck under a stuffed head is the classic head-flop failure.

### 🟠 S4 — The tail is never stuffed
"Fasten off." is the last word on the tail. A 20-round unstuffed tail will hang limp.

### 🟠 S5 — The toes are never stuffed, and no order is given
Once Round 4 joins the three toes, the toes are sealed. They must be stuffed before or during the
join, and the pattern doesn't say so.

### 🟠 S6 — Wing loop treatment is inconsistent
Row 2 FLO, Row 3 BLO, Row 4 FLO, **Row 5 unspecified**. Either the alternating FLO/BLO ridge texture
is intentional — in which case Row 5 breaks it and needs a loop specified — or it is accidental.
Note also that FLO/BLO work produces a looser, floppier fabric, which is the opposite of what a wing
that has to hold its shape wants.

### 🟠 S7 — Assembly step 4 is empty
The pattern literally ends on a bare `4.` with nothing after it. The document is truncated.
Whatever it was — eyes, spinal crest, horns, closing the crotch — it's missing.

---

## 3. Documentation gaps

### 🟡 M1 — No yarn quantities
Three colours are listed with no grams or yards for any of them. Color B (Gold) is used for six
rounds and Color C (Silver) only for the wings, so the amounts are wildly different and a maker has
no way to shop for this.

### 🟡 M2 — No quantity for the safety eyes
"12 mm safety eyes" — you need **2**. Say so.

### 🟡 M3 — No finished size
For an Advanced pattern that bothers to specify gauge, the finished measurement should be stated.
At the given gauge it works out to roughly **8½–9 in / 22 cm tall** with about a **6 in wingspan**.

### 🟡 M4 — Gauge is given in rows, but almost everything is worked in rounds
Row gauge and round gauge differ. Only the wings are flat. Give the round gauge too, or state the
gauge as a swatch diameter.

### 🟡 M5 — Assembly calls torso rounds "Rows"
> "Attach Wings to **Rows** 16–18 on back of Torso"

The Torso is worked in rounds. Small, but in a pattern that also contains a genuinely row-worked
piece (the wings) it is a real source of confusion.

### 🟡 M6 — Assembly never says which wing edge attaches
The wing has a 15-stitch foundation edge, an 11-stitch final-row edge, and two row-end edges — one of
which carries the feather edging. Which one gets sewn to the torso is never stated, and "Rows 16–18"
(3 rounds ≈ 0.55 in) doesn't match the length of any of them.

---

## 4. Proportion advisories

Measured at the pattern's own stated gauge (5 sts/in, 5.5 rows/in).

### 🔵 P1 — The wings are ribbons, not wings
3.00 in wide × **0.91 in tall** — a **3.3 : 1** strip, and only **24 %** of the torso height.
A wyvern is *defined* by its wings. These would read as fins. Suggest roughly doubling the depth
(the corrected pattern takes it to 4.2 × 2.2 in, a 1.9 : 1 wing).

### 🔵 P2 — 12 mm safety eyes are oversized for this head
The head is 24 sts around = **1.53 in / 39 mm** diameter. A 12 mm eye is **31 % of the head's entire
diameter**. Placement at 5 sts apart is fine, but the scale reads as a kawaii plush, not a wyvern.
**8–9 mm** would suit a head this size.

### 🔵 P3 — The legs attach at 62 % of the torso height
Round 13 sits **2.36 in up a 3.82 in torso**. That is waist height, not hip height, and it puts the
legs only 3 rounds below the wings. If a standing pose is intended, join the legs around Round 7–9.

### 🔵 P4 — The neck is 1.09 in long
Six rounds. For a *celestial wyvern* the long serpentine neck is a signature feature; consider
extending Rounds 13–16 to 10–12 rounds.

---

## 5. What is correct (and it's a lot)

- **Head & Neck, all 17 rounds** — verified exact, including the BLO colour change at Round 12.
- **Toes, all 3 rounds** — exact.
- **The three-toe join (Leg Round 4)** — `3 + 3 + 6 + 3 + 3 = 18` consumes all three 6-stitch toes
  perfectly, and the Toe 3 → Toe 2 → Toe 1 → Toe 2 → Toe 3 path is a geometrically coherent
  perimeter walk. Genuinely well done, and the hardest thing in the pattern.
- **"Make 3 per leg = 6 total"** — correct.
- **Torso Rounds 1–12 and 14–21** — all exact.
- **Wing Rows 1–5** — all exact, including `ch 16 → 15 sc` and the turning chain correctly not
  counting as a stitch.
- **Tail Rounds 1–16** — exact.
- **Neck R17 (18 sts) ↔ Torso R21 (18 sts)** — the assembly interface matches. Most multi-piece
  patterns get this wrong.
- **The abbreviation list is complete** — all 10 abbreviations are defined and all are actually used.
- **Stuffing prompts exist** for head, leg and torso, correctly placed before each closes.
- **Two legs, two wings** — correct wyvern anatomy (wyverns are bipedal; dragons are not).

---

## 6. Corrected pattern

See [`celestial-wyvern-CORRECTED.md`](./celestial-wyvern-CORRECTED.md). It validates with
**0 defects**.

| Piece | Where | Was | Now |
|---|---|---|---|
| Head & Neck | heading | "worked top to snout" | "snout tip back to the nape, then the neck" |
| Leg | R11 | `(8 sts)` | `(9 sts)` |
| Torso | R13 | 30 of 36 body sts, asymmetric | 15 / 15 symmetric, 3 sts skipped per leg |
| Torso | after R13 | *(missing)* | sew each leg's 3 leftover sts to the 3 skipped body sts |
| Tail | R17–20 | `sc around. (12)` | `R17 [sc 4, inc] x2 (12)`, `R18–20 sc around (12)` |
| Wing | Rows 1–12 | 5 rows, 15 sts | 12 rows, 21 sts — and consistent loop treatment |
| Wing | edging | 7 sts into every row end | 4 fans over 12 row ends, 3 row ends per fan |
| Assembly | step 4 | *(empty)* | completed |

Plus: yarn quantities, 2 safety eyes at 9 mm, finished size, a global spiral note, and stuffing
instructions for the neck, tail and toes.

---

## 7. How this was tested

1. **`StitchCountValidator`** (this repo) run per piece — caught **D1** and **D2**.
2. **`PatternValidator`** multi-pass compiler (this repo) — run on the whole document and per piece.
3. **An independent verifier written from scratch** (`verify_wyvern.py`) that models flat rows,
   the three-toe join, the leg-to-body join and the edging geometry — the repo's engine handles none
   of these. It caught all five, including **D4 and D5, which the repo's engine missed entirely**
   (it marks plain "sc around" rounds as context-dependent and skips them, and it cannot parse
   flat rows at all — it reported all five wing rows as producing 0 stitches).
4. **Gauge-based geometry** for every proportion claim, using the pattern's own stated gauge.

Reproduce:

```bash
python reviews/celestial-wyvern/verify_wyvern.py           # as submitted -> 5 defects
python reviews/celestial-wyvern/verify_wyvern.py --fixed   # corrected    -> 0 defects
```

### Comparison with the Classic Amigurumi Bear

| | Bear | Wyvern |
|---|---|---|
| Blocking math errors | 5 | 5 |
| …of which make a round *impossible* | 1 | 0 |
| Abbreviations complete | ❌ (`ch`, `sl st` undefined) | ✅ |
| Stuffing instructions | ❌ none at all | ⚠️ 3 of 5 pieces |
| Assembly interfaces match | n/a | ✅ |
| Assembly detail | ❌ vague | ⚠️ specific but truncated |

The wyvern's errors are typos and omissions in an otherwise sound design. The bear's were
structural. This one is much closer to shippable.
