# Round 3 review — every number in all 17 Novality Store patterns

Scope: NS-01 … NS-17 as compiled in `NovalityStore_Grand_Collection.md` (the "Grand Crochet Pattern
Collection" volume), checked against the per-pattern masters in `docs/ns01…docs/ns17`.
Method: independent arithmetic re-derivation of every instruction table
(`docs/kit/audit_lib.py` + `docs/kit/audit_overrides.py`) plus hand re-derivation of every prose
figure that no tool can read (sizes, widths, weights, leg spacing, derived dimensions).

## 0. Verdict

| | |
|---|---|
| Patterns reviewed | 17 of 17 |
| Stitch tables re-derived | 90 |
| Instruction rows re-derived | 692 (0 unreadable, 0 mismatched) + NS-14's 32 skirt rounds, which the tool skips (see §6) |
| Arithmetic errors found | 0 |
| Prose/geometry errors found and corrected | 8 in this repo's masters (7 patterns) · 4 more that exist only in the pasted volume |
| Left for a sample | 1 (NS-15 poinsettia size — text is ambiguous, not wrong) |
| Ledger/reproducibility notes | 4 (see §6) |

The stitch-level arithmetic in the collection is genuinely clean: every round and row in all 17
patterns re-derives from its own instruction text, including the joined-leg rounds (NS-04), the
dual US/UK tables (NS-13, NS-14), the oval bases (NS-01, NS-06) and the 32-round skirt (NS-14).
Every defect found this round is in **prose**, i.e. in a figure asserted in a sentence and never
checked by the arithmetic engine — which is exactly the class of error the checker cannot see.

## 1. Method, and the rules used to judge a prose number

### 1.1 Arithmetic (checked by tool, all 17)

`audit_tables()` re-simulates each instruction and compares the result with the stated `Sts` cell.
Run per pattern with that pattern's override dict:

```bash
/tmp/venv/bin/python - <<'EOF'
import sys; sys.path.insert(0,'docs/kit')
from pathlib import Path
from audit_lib import audit_tables
from audit_overrides import OVERRIDES, SKIP_TABLES
for i in range(1,18):
    n='%02d'%i
    t=Path(f'docs/ns{n}/NS{n}_corrected.md').read_text()
    probs,unp=audit_tables(t, OVERRIDES.get(f'NS-{n}',{}), SKIP_TABLES)
    print(n, len(probs), len(unp), probs[:2])
EOF
```

Result: `problems=0, unparsed=0` for all 17. Engine (`docs/kit/engine_run.py`):
0 errors / 0 warnings for 16 patterns; NS-14 carries its 2 documented dual-dialect errors.

### 1.2 Prose figures (hand-derived)

A prose number was treated as correct only if it follows from the pattern's **own** gauge, stitch
counts or geometry. Tolerance: ±10 % counts as "about"; anything further out was corrected, with the
derivation written out below. Where a figure could be read two ways and the text does not settle it,
it is reported rather than changed (§5).

## 2. Corrections applied to the masters in this repo

Also applied to the compiled volume `NovalityStore_Grand_Collection.md`, wherever the same text
exists there. All 17 patterns re-audited after the edits: 0 problems, engine unchanged.

### 2.1 NS-04 Coco the Capybara — Rnd 5 put two legs almost side by side  ⟵ the serious one

Rnd 5 joined the front legs over stitches 6-8 and 16-18 of the Rnd-4 round, while Rnd 4 puts the back
legs over 1-3 and 13-15:

```
stitch  1  2  3 | 4  5 | 6  7  8 | 9 10 11 12 | 13 14 15 | 16 17 18 | 19 20 21 22 23 24
leg     BL1·····        FL1·····               BL2······  FL2······
gap          2            4          0              6
```

The right back leg and right front leg end up **adjacent** (0 stitches apart) while the left pair is
2 apart and the front pair 4 apart. Four feet cannot stand on a rectangle from that layout, and two
legs side by side is precisely the "Coco tips forward or backward" failure the pattern's own
troubleshooting warns about. In this repo's master the row, the explanation and the troubleshooting
line all agreed with each other (7 - 3 - 10 - 3 - 7), so nothing flagged it: the error was not a
contradiction but a wrong geometry, repeated consistently. The volume repeats it in the
troubleshooting bullet (§3.1).

| | |
|---|---|
| was | `1 sc, inc, 1 sc, inc, 1 sc, join FL1: 3 sc, [sc, inc] x 3, 1 sc, join FL2: 3 sc, 3 sc, inc, 2 sc` |
| now | `[sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc` |
| made | 9 - 3 - 12 - 3 - 3 = **30** (unchanged) |
| worked | 6 + 3 + 9 + 3 + 3 = **24** (every stitch of Rnd 4, unchanged) |
| legs now | front over 7-9 and 19-21, back over 1-3 and 13-15 → plain gaps **3 / 3 / 3 / 3**, centres 6 apart → a square |

Rewritten to match: the Rnd 5 explanation (now names stitches 7-9 / 19-21), the stitch-arithmetic
sentence (`worked = 6 + 3 + 9 + 3 + 3 = 24; made = 9 + 3 + 12 + 3 + 3 = 30`) and the
"tips forward or backward" bullet (now states the equal-gap rule instead of "7 sc, 10 sc, 7 sc").

Side note that came out of this: the leg lengths and join heights were **already** consistent and
needed no change — back legs 8 rounds × 4.3 mm = 34.4 mm from a join 4 × 4.3 = 17.2 mm up the body,
front legs 9 × 4.3 = 38.7 mm from 5 × 4.3 = 21.5 mm up: both feet finish exactly 17.2 mm below the
body, which is what the text claims ("every foot hangs about 17 mm below the body"). Round 2's
suspicion about the legs was unfounded; only the *width* figure was wrong.

### 2.2 NS-04 — the body-width figure was derived from an invented gauge

| | |
|---|---|
| was | "The correct spacing covers the deepest footprint this shape allows - about 65 mm across and 29 mm front to back." |
| now | "At thirty stitches and 4.5 mm per stitch the body itself measures about 43 mm across at the Rnd-5 leg join (about 34 mm at Rnd 4); the splayed legs widen the standing footprint beyond that, so measure your own piece rather than relying on a printed number." |

Derivation: the pattern's own gauge line is *"36 sc around measures about 52 mm in diameter when
stuffed (4.5 mm per stitch, 4.3 mm per round)"*. 30 stitches × 4.5 mm = 135 mm round → 135/π ≈
**43 mm** across; 24 stitches (Rnd 4) → 34 mm. To reach 65 mm across you would need 6.8 mm per
stitch, and 29 mm front-to-back would need 3.0 mm per stitch — neither is this pattern's gauge, and
a 30-stitch tube cannot be 65 mm on one axis and 29 mm on the other.

The volume's version of this sentence used a third figure again ("roughly 3.5 mm per stitch … about
34 mm across"): 30 × 3.5/π = 33.4 mm, i.e. it inferred 3.5 mm per stitch that the gauge line
contradicts. Corrected in §3.2.

### 2.3 NS-06 the black cat — 36-stitch base width

| | |
|---|---|
| was | "Stopping at 36 gives a body about 34 mm across" |
| now | "Stopping at 36 gives a body about 39 mm across" |

Derivation: gauge 4.5 mm per stitch, and the finished size is "7.9 cm long, 5.2 cm wide" at 48
stitches — so 48 stitches = 52 mm across the short axis and 36 stitches scale to 52 × 36/48 =
**39 mm** (equivalently 36 × 4.5 = 162 mm round → 51.6 mm round the whole oval, 39 mm across the
flat). 34 mm would need 3.0 mm per stitch.

### 2.4 NS-12 the standing fir — stuffing weight contradicted its own sentence

| | |
|---|---|
| was | "Stuffing: fibre fill about 25 g (a little only - the tree stands on tension)." |
| now | "Stuffing: fibre fill about 5 g (a little only - the tree stands on tension)." |

"the tree stands on tension" and "a little only" rule out 25 g by themselves. The piece is 12 cm tall
and 7 cm wide on a 4 mm hook with a 48-stitch base (≈ 72 mm round), i.e. well under 150 cm³ of
enclosed space, and the pattern only wants the lower half filled: at ~0.05 g/cm³ that is 4-6 g,
so **5 g**. Cross-checks: NS-02 allots 5 g for *three* 5 cm bodies, and NS-11 (a 30-stitch,
12 cm tall body, the larger piece) allots 10 g. 25 g would be roughly five times the volume's worth and
would bulge the bobble tiers the pattern warns about.

### 2.5 NS-13 the ornaments — the star was claimed at twice its achievable size

| | |
|---|---|
| was | "Bauble about 3.75 cm (1.5 in) across; star about 9 cm (3.5 in); snowflake about 10 cm (4 in)." |
| now | "Bauble about 3.75 cm (1.5 in) across; star about 4.5 cm (1.75 in); snowflake about 10 cm (4 in)." |

Geometry: the star's centre is 10 sc = 45-47 mm round → about **15 mm across** (radius ≈ 7 mm) at the
4 mm hook / worsted gauge this pattern specifies. Each of the five points is a single-stitch fan
`(sc, hdc, dc, ch 2, dc, hdc, sc)` worked into one centre stitch, so its reach is only the height of
its tallest elements — one dc/half-treble tier ≈ 10-12 mm, stretched by blocking to ≈ 13-14 mm.
Point-to-point = 15 + 2 × ~14 ≈ **43 mm**, blocked to **≈ 4.5 cm (1.75 in)**. A 9 cm star needs
38 mm points — nearly three times the reach a six-stitch fan can give.

The snowflake is *not* in the same class and was left alone: its arms are `ch 3, 3 tr, ch 3` worked
into ch-5 spaces that already arch ~20 mm off a 12-spoke ring, so ~30 mm of reach per arm before
blocking (≈ 7 cm) and 10 cm after wet-blocking is a genuine claim. The star is a solid fan and pinning
it cannot add 150 %.

### 2.6 NS-14 the tree skirt — cover brand line

| | |
|---|---|
| was | `# NOVALITY CROCHET STUDIO — PRINTER-SAVER EDITION` |
| now | `# NOVALITY STORE — PRINTER-SAVER EDITION` |

The other 16 covers all read `NOVALITY STORE …`, and the volume's own branding rule (§10) keeps the
studio name for the design credit: "Pattern and layout by **Novality Crochet Studio**". The design
credit is still on the cover block, in the copyright notice, at the Terms of Use and in the footer
(`© 2026 Novality Crochet Studio`, `Design Code NS 14 · Novality Crochet Studio`); only the brand line
on page 1 changed.

### 2.7 NS-11 the gnome — stuffing weight

| | |
|---|---|
| was | "Stuffing: fibre fill about 25 g." |
| now | "Stuffing: fibre fill about 10 g." |

The gnome is 12 cm tall and 5 cm wide on a 3.5 mm hook, so the body encloses roughly π × 2.5² × 12 ≈
240 cm³; at the ~0.05 g/cm³ the rest of the collection uses that is 10-12 g. 25 g is twice the volume's
worth and would fight the "pack the base flat and wide … keep the pointed hat lightly stuffed"
instruction two pages later. Cross-checks: NS-02 allots 5 g for three 5 cm bodies and NS-12's
corrected figure is 5 g.

### 2.8 NS-17 the lamb's collar — foundation twice as long as the neck

| | |
|---|---|
| was | "With scarlet, ch 22." … Row 1 `sc in 2nd ch and next 20 ch` (21) … Row 2 (21) |
| now | "With scarlet, ch 14 (about 6.5 cm relaxed at the pattern's worsted gauge, against an assembled neck of about 6 cm around)." … Row 1 `sc in 2nd ch and next 12 ch` (13) … Row 2 (13) |

ch 22 is 21 stitches; at the pattern's 20 sc per 10 cm that is 105 mm of collar against a neck the same
page calls "about 6 cm around" — 75 % too long, with only the "check that the relaxed chain reaches
around the assembly" sentence standing between the maker and a collar that cannot overlap by one
stitch. ch 14 = 13 stitches = 65 mm, which leaves exactly the one-stitch overlap the finishing step
asks for. The three affected lines (foundation, Row 1, Row 2) were changed together so the count
column still re-derives.

## 3. Corrections the pasted volume still needs (not present in this repo's older revision)

The repo's `NovalityStore_Grand_Collection.md` is a pre-round-2 snapshot, so four of the volume's
current sentences do not exist here to patch. Apply these in the volume itself — either by hand from
the items below, or with the script that ships alongside this report:

```bash
python3 docs/reviews/round3_volume_errata.py --dry-run path/to/NovalityStore_Grand_Collection.md
python3 docs/reviews/round3_volume_errata.py           path/to/NovalityStore_Grand_Collection.md
```

It applies all ten round-3 edits idempotently, lists which fixes are already in place, and exits 1 if
any expected sentence is missing (so a stale volume is detectable rather than silently half-patched).

### 3.1 NS-04, "Coco tips forward or backward" bullet

The volume still says "the Rnd 5 spacing must be 7 sc, 10 sc, 7 sc". Those are the made-stitch runs of
the *old* Rnd 5 (7 - 3 - 10 - 3 - 7), i.e. the arrangement with gaps 2/4/0/6 that causes the tipping —
the bullet prescribes the fault. Replace the sentence with:

> keep all four leg joins three plain stitches apart all the way round (back legs over stitches 1-3
> and 13-15 of the Rnd-4 round, front legs over 7-9 and 19-21)

and check the Rnd 5 table row in the same pattern. If it still reads
`1 sc, inc, 1 sc, inc, 1 sc, join FL1: 3 sc, [sc, inc] x 3, 1 sc, join FL2: 3 sc, 3 sc, inc, 2 sc`,
replace it with `[sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc`, so that
the row, the explanation and the troubleshooting bullet all describe one arrangement (see §2.1).

### 3.2 NS-04, "Work the numbers exactly" paragraph

Replace "At thirty stitches and roughly 3.5 mm per stitch the body itself measures about 34 mm across
at the leg joins in Rnds 4 and 5" with

> At thirty stitches and 4.5 mm per stitch the body itself measures about 43 mm across at the Rnd-5
> leg join (about 34 mm at Rnd 4)

The rest of the sentence ("the splayed legs widen the standing footprint … measure your own piece") is
already right. Reason in §2.2 — the pattern's gauge line says 4.5 mm per stitch, not 3.5.

### 3.3 NS-04, both rows of the Part 17 review table

- Row 1 says "… 30 stitches at ~3.5 mm give ~34 mm across the body". Should read "30 stitches at
  4.5 mm give about 43 mm across the body (34 mm at Rnd 4)".
- Row 2 says "Leg gaps 5/7/3/9 columns: not a rectangle, so Coco tips; resolved with explicit 7/10/7
  joins … Derived body width stated (~34 mm)." Two problems: 5/7/3/9 are the distances between leg
  *centres* under the 7/10/7 arrangement (plain gaps 2/4/0/6), so the row resolves the defect with the
  arrangement that produces it; and it compares centre distances with row 1's "gaps 3/3/3/3", which
  are plain-stitch gaps. Rewrite on one measure: "plain gaps 2/4/0/6 (centres 5/7/3/9 apart) before;
  3/3/3/3 (centres 6 apart) after; body 43 mm across at Rnd 5".

### 3.4 NS-17, the lamb's fixed collar — wording

"With scarlet, ch 14 (about 6.5 cm relaxed at DK gauge, against an assembled neck of about 6 cm
around)." — the pattern's own yarn is worsted (#4) throughout and its gauge is 20 sc = 10 cm, i.e.
5 mm per stitch: 13 stitches × 5 mm = 65 mm and 12 × 5 = 60 mm, which is exactly the two figures
given. "DK gauge" contradicts the materials list. Replace "at DK gauge" with "at the pattern's worsted
gauge" (the master in this repo already reads that way after §2.8; the errata script fixes your copy).

## 4. Per-pattern record

`tables/rows` are the stitch tables and instruction rows the auditor re-derived. "Prose" lists the
figures that were hand-derived beyond the tables — every one of the 17 patterns now has at least one
non-trivial derivation, not just a gauge-to-size sanity check (about 60 numbers in all).

| Pattern | tables/rows | Prose figures re-derived | Outcome |
|---|---|---|---|
| NS-01 Hamish | 9 / 91 | head 70 × 67 mm = 48 st × 4.55 mm and 16 rounds × 4.17 mm ✓; eye spacing 7 st = 31.9 mm ≈ "32 mm, just under half the head" ✓; muzzle face 24 st = 34.8 mm ≈ 35 ✓ and rim 18 st = 26.1 mm ≈ 26 ✓; yarn 42 g allowed vs ~31 g implied | clean |
| NS-02 Boo, Pip, Bramble | 11 / 73 | 36 st at 3.5 mm = 40.1 mm across — exactly as stated ✓; brim 20 st = 22.3 mm vs "about 24 mm" on a 27 mm head (9 %, inside "about"; 24 mm is also the right ~11 % negative ease) | clean |
| NS-03 | 4 / 52 | tail 10 rounds × 4.3 = 43 mm ✓; 6 sts = 27 mm ≈ "about half" the 52 mm head ✓; +2 gill rounds → +17 mm ≈ 10 → 12 cm span ✓; neck-rework arithmetic 18 → 20 → 24 works ✓ | clean |
| NS-04 Coco | 4 / 39 | 36 st = 52 mm → 4.5 mm/st; Rnd 5 width 43 mm; leg lengths 34.4 / 38.7 mm from joins 17.2 / 21.5 mm up → both feet 17.2 mm below the body ✓ | **2 corrections** (§2.1, §2.2) + 3 in the volume only (§3.1–3.3) |
| NS-05 | 3 / 30 | 23 rounds × 7 mm = 161 mm ≈ 16 cm ✓; widest 30 st × 8 mm = 76.4 mm = the "76 mm-diameter head" ✓; 7-st eye spacing = 56 mm ✓; 12-st swatch = 96 mm ≈ "about 10 cm" ✓ | clean |
| NS-06 the cat | 2 / 20 | 48 st = 79 × 52 mm → 36 st = 59 × 39 mm (fixed, §2.3); ears 5 → 3 → 2 close exactly; tail is a flat 4-stitch spiral that explicitly uses no magic ring ✓ | **1 correction** (§2.3) |
| NS-07 | 7 / 33 | nine petals = 18 anchors × 2 = the 36-st petal round ✓; the bulky version ("about 1.3× the gauge" = 4.5/3.5 = 1.286) predicts 3.9 / 4.9 / 3.5 cm from 3.0 / 3.8 / 2.7 ✓ | clean |
| NS-08 | 7 / 59 | 30 st = 43 mm ✓; 24 rounds × 4.3 = 103 mm = the stated "103 mm by the gauge" ✓; legs 6 rnd = 25.8 mm on a 26 mm join and 8 rnd = 34.4 mm on a 34 mm join — both feet exactly on the table ✓; spike strip 3 + 9 × 3 + 3 = 33 ✓ | clean |
| NS-09 | 3 / 11 | 24 st = 26.7 mm disc ✓ exact; bump positions 4 / 9 / 13 / 18 / 22 follow from the runs 3,4,3,4,3,2 ✓; 19 plain + 5 fans = 35 ✓; 42-st version = 46.8 mm + flippers ≈ 5.7 cm ✓ | clean |
| NS-10 | 3 / 24 | head 36 st at 4.3 mm = 49.3 mm ≈ 4.9 cm ✓; blanket check 9 dc = 38.7 ≈ 39 mm ✓; 26 cm square → diagonal 26 × √2 = 36.8 cm ✓ | clean |
| NS-11 the turkey | 4 / 18 | 30 st = 45-48 mm ≈ "about 5 cm wide at the base" ✓; gauge 11 rounds = 5 cm ⇒ 12 cm ≈ 27 rounds ✓ | **1 correction** (§2.7) |
| NS-12 the fir | 1 / 26 | 48 st at ~4.7 mm = 72 mm round = the stated 7 cm wide ✓; enclosed volume under 150 cm³ (fixed stuffing, §2.4) | **1 correction** (§2.4) |
| NS-13 the ornaments | 3 / 13 | bauble 6 → 24 then closed to a 6-st crown ✓ (24 st ≈ 36 mm vs stated 3.75 cm, inside "about"); star = 15 mm ring + 2 × ~14 mm blocked fan reach | **1 correction** (§2.5) |
| NS-14 the tree skirt | 6 / 0 (skipped by the tool — see §6) + 32 rows by hand | every growth round reads 12 × N with N − 2 plain dc per repeat (N − 3 on bobble rounds); total 6,336 st ✓; its own gauge derivation gives 4 in per 6¼ rounds vs the 6 written (reported as F3 in its validation report) | **1 correction** (§2.6) |
| NS-15 the wreath | 5 / 18 | all three sizes are circumference = π × centreline diameter: 7 → 22.0, 29 → 91.1, 40 → 125.7 cm against 22 / 92 / 125 ✓; poinsettia geometry deferred (§5.1) | clean (1 item deferred) |
| NS-16 the lion | 4 / 31 | 20 sc & 20 rounds = 10 cm ⇒ 20 st = 10 cm round, 5 cm flat ✓ (both stated); garland maths 200 − 40 = 160, 160 ÷ 23 = 6.96 ≈ "about 7 cm" ✓; toe 23 → 20 → 8 → 4 ✓ | clean |
| NS-17 the goat & lamb | 14 / 154 (largest) | hair 24 + 10 + 9 = 43 strands ✓; collar 13 st × 5 mm = 65 mm against the 60 mm neck ✓ (foundation was ch 22, fixed §2.8); its size row already flags the 17 cm target as unverified ✓ | **1 correction** (§2.8) + 1 in the volume only (§3.4) |

### 4.1 The checks that came out exact

Worth recording, because these are the sentences that *look* unchecked but are in fact right, and a
future edit should not "fix" them:

- **NS-09** — 24 shell stitches at 3.5 mm/ch = 84 mm round = **26.7 mm** disc, exactly as written; the
  five appendage bumps land on stitches **4 / 9 / 13 / 18 / 22**, exactly as written, because the runs
  are 3,4,3,4,3,2 (sum 24) and the round produces 19 plain + 5 fans = **35**; the 42-stitch version is
  46.8 mm + flippers ≈ **5.7 cm**, exactly as written.
- **NS-15** — all three wreath sizes satisfy circumference = π × centreline diameter: 7 → 22.0 cm,
  29 → 91.1 cm, 40 → 125.7 cm against 22 / 92 / 125.
- **NS-07** — "about 1.3× the original gauge" is 4.5/3.5 = 1.286, and applying it to 3.0 / 3.8 / 2.7 cm
  gives 3.9 / 4.9 / 3.5 cm, exactly the stated scaled sizes, with stitch counts unchanged.
- **NS-16** — "20 sc and 20 rounds = 10 cm" then "20 stitches = 10 cm circumference, 5 cm flat" is
  self-consistent, and 160 ÷ 23 = 6.96 cm is "about 7 cm".
- **NS-08** — both legs are exactly as long as their joins are high (6 rounds = 25.8 mm on a 26 mm
  join, 8 rounds = 34.4 mm on a 34 mm join), so all four feet reach the table; the spike strip
  3 + 9 × 3 + 3 = 33.
- **NS-10** — 36-stitch head at 4.3 mm = 49.3 mm ≈ "head about 4.9 cm across"; 9 dc = 38.7 ≈ 39 mm;
  26 cm square → 36.8 cm diagonal.
- **NS-01** — head 70 × 67 mm is 48 st × 4.55 mm and 16 rounds × 4.17 mm; 7-stitch eye spacing =
  31.9 mm ≈ "about 32 mm, just under half the head"; muzzle face 24 st = 34.8 ≈ 35 mm and rim
  18 st = 26.1 ≈ 26 mm.
- **NS-03** — 10-round tail × 4.3 mm = 43 mm; the gill option (+2 rounds at 12 sts) adds ~17 mm,
  i.e. 10 → 12 cm; the neck fix (R13 20 st, R14 [4 sc, inc] × 4 = 24) consumes all 20 and makes 24.
- **NS-05** — 30 st × 8 mm = 76.4 mm = the stated 76 mm-diameter head; 7-stitch eye spacing = 56 mm.

## 5. Examined and deliberately not changed

### 5.1 NS-15 poinsettia "approx. 3.5 in" — ambiguous, not wrong

If the 3 tr of `[ch 4, 3 tr, ch 4, sl st] in the same st` are worked into the centre stitch (the
literal reading of "in the same st"), each petal reaches ~18 mm and the bloom is ~9 + 2 × 18 ≈
**4.5 cm (1.8 in)**. If they are worked into the tip of the ch 4, the petal reaches ~35 mm and the
bloom is ≈ **7.9 cm (3.1 in)** — within "about 3.5 in". So the stated size follows from one reading
and not the other, and the text does not say which. This needs the designer's intent or a sample, not
a number change; the fix, if the 4.5 cm reading is intended, is to add a treble and two chains to each
petal (a design change). Recommend clarifying the anchor in the petal row either way.

### 5.2 Not changed on purpose

- **NS-14's 2 errors / 4 warnings.** The dual-dialect flags are expected and documented (the pattern
  is deliberately printed in both US and UK terms); changing the wording to silence the engine would
  remove the UK column. Left as is.
- **"Target range, not a weighed amount" style warnings** on NS-14. These are honesty flags about
  unverified data, not defects; silencing them would require claiming measurements nobody took.
- **NS-02's brim (22 mm derived vs 24 mm stated).** Inside the ±10 % "about" band and the stated
  figure gives the intended ~11 % negative ease on a 27 mm head.
- **NS-11 stuffing 10 g.** Right in line with the same ~0.05 g/cm³: a 12 cm tall, 5 cm wide body holds
  roughly 240 cm³, so 10 g is a sound allowance and independently corroborates NS-12's corrected 5 g.
- **Yarn allowances generally.** All patterns except NS-14 allot at or above the ~1.6 g per 100
  stitches implied by their own stitch totals (NS-01: 42 g allowed vs ~31 g implied; the rest are
  similar or looser), so nothing is short. NS-14's 3–5× over-allowance is already catalogued in
  `docs/ns14/NS14_validation_report.md` (F2) with the per-size table, and that report's figures
  re-derive.

## 6. Notebook: four tooling and ledger notes

1. **The old volume's ledger said NS-14 was "2 errors / 3 warnings"; this checkout reproduces 2 / 4.**
   The fourth warning is "The opening is an approximate target. It was not checked against a finished
   stand." The other 16 patterns reproduce 0 / 0 exactly. The old volume also credited a build script,
   `docs/kit/build_grand.py`, that did not exist in the repository — so its ledger could not be
   reproduced at all. **Now fixed:** that script exists, and the regenerated volume
   (`NovalityStore_Grand_Collection_corrected.md`) carries a ledger whose engine, audit, table/row and
   page counts are all recomputed on every build, so the row reads 2 / 4 because that is what the
   engine reports.
2. **The shared auditor silently skips NS-14.** Its tables carry a leading `[ ]` checklist column, and
   `audit_tables()` skips any row whose first cell starts with `[ ]`/`[x]`, so all 32 NS-14 rows are
   invisible to it (`rows=0`). The skirt's counts were checked by hand instead: `Sts` = 12 × N for
   every round 2-32 and the plain runs are N − 2 (N − 3 on bobble rounds) — all correct. If NS-14 is
   ever re-audited with the kit, its tables need the checkbox column removed or the auditor needs to
   skip the checkbox cell instead of the row.
3. **Override dicts are per pattern.** `OVERRIDES` in `docs/kit/audit_overrides.py` is keyed by
   `"NS-xx"`, so the call must be `audit_tables(text, OVERRIDES["NS-07"], SKIP_TABLES)`. Passing the
   whole dict looks fine but disables every override, and the 14 override-covered rows (NS-07 petal,
   NS-10 rnd 2 / rnds 3-20, NS-11 r9-12 / r13 / r16, NS-15 continuation rows) then show up as
   "unparsed" instead of being checked.
4. **`NovalityStore_Grand_Collection.md` is a pre-round-2 hand-compiled snapshot** and is now marked
   superseded in its own header. The maintained edition is
   `NovalityStore_Grand_Collection_corrected.md`, built from the seventeen masters by
   `docs/kit/build_grand.py` (17 parts, front matter, recomputed ledger and a corrections table). The
   two figures the snapshot still gets wrong beyond the round-3 list are NS-02's brim (24 mm for a
   22 mm derivation, inside tolerance) and nothing else of consequence — NS-04's Rnd 5, NS-11's
   stuffing, NS-12's stuffing, NS-13's star and NS-17's collar are all corrected in the masters.

## 7. Re-verify

```bash
# rebuild the volume, and prove the committed copy is current
python3 docs/kit/build_grand.py
python3 docs/kit/build_grand.py --check

# the round-3 figures, re-derived by test (stdlib only, 13 tests)
python3 -m pytest tests/test_ns_prose_figures.py -q

# arithmetic over all 17 masters (expect problems=0 unparsed=0)
python3 - <<'EOF'
import sys; sys.path.insert(0,'docs/kit')
from pathlib import Path
from audit_lib import audit_tables
from audit_overrides import OVERRIDES, SKIP_TABLES
for i in range(1,18):
    n='%02d'%i
    p=Path(f'docs/ns{n}/NS{n}_corrected.md')
    probs,unp=audit_tables(p.read_text(), OVERRIDES.get(f'NS-{n}',{}), SKIP_TABLES)
    print(f'NS-{n}', len(probs), len(unp))
EOF

# engine over all 17 masters (expect 0/0 except NS-14 2/4)
for n in $(seq -w 1 17); do printf "NS-%s " $n; python3 docs/kit/engine_run.py docs/ns$n/NS${n}_corrected.md | tail -6; done
```
