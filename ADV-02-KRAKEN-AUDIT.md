# ADV-02-KRAKEN AUDIT — THE CLOCKWORK KRAKEN
**Design Code: ADV-02-KRAKEN | Nightmare / Expert Validation Stress Test**
**Terminology: US | Status: Intentionally corrupted benchmark — FAIL**
**Original preserved at: `ADV-02-KRAKEN-ORIGINAL.md` (unchanged)**

This audit classifies planted defects using your repository's verification stages (arithmetic, state propagation, cross-section, dimensional, component logic, safety, and unverified-claim handling). Every finding lists **location, severity, explanation, and correction** as requested.

> Checker philosophy reminder: the checker counts written stitches, repeats and seams. It does not invent a photo, a swatch measurement, or a physical proof. Geometric impossibility from prose alone is flagged as an unverified claim, not as a proven failure.

---

## 1. ARITHMETIC — Round totals that cannot follow the stated operations

These are deterministic stitch-count errors. Repeat consumption/production does not match the stated end count.

### Mantle (Section 4)

| Location | Severity | Finding | Correction |
|---|---|---|---|
| **M-Rnd 13:** `[6 sc, inc] × 8 (56)` with incoming 48 | **ERROR** | `[6 sc, inc]` = 6 sc + inc(1→2) = **7 consumed → 8 produced**. ×8 needs 56 in → 64 out. From 48 it is impossible (48 not ÷7). Stated 56 also impossible from that operation. | Should be `[5 sc, inc] × 8 (56)` = 6→7 ×8 = 48→56. |
| **M-Rnd 19:** `[6 sc, dec] × 8 (48)` with incoming 56 | **ERROR** | `[6 sc, dec]` = 6 + dec(2→1) = **8 consumed →7 produced**. ×8 needs 64→56. From 56 impossible (56 not ÷8). Stated 48 wrong. | Should be `[5 sc, dec] × 8 (48)` = 7→6 ×8 = 56→48. |
| **M-Rnd 25:** `[5 sc, dec] × 8 (40)` | **ERROR** | From correct 48 (after propagated fix, see §2) this operation is 7→6 = 48→? Actually incoming should be 56 or 48 depending on drift. Stated 40 is not 7→6 ×8 (=48). Arithmetic mismatch. | If incoming 48: `[4 sc, dec] ×8 (40)` =6→5 ×8. If incoming 56: `[5 sc, dec] ×8 (48)` then next round to 40. |
| **M-Rnd 26:** `[4 sc, dec] × 8 (32)` | **ERROR** | 4+dec =6→5 ×8 = 48→40 or 40→? 40 not ÷6. Stated 32 expects 32→? Actually needs 6→5 ×8 from 40 impossible remainder. | `[3 sc, dec] ×8 (32)` =5→4 ×8 from 40. |
| **M-Rnd 27:** `[3 sc, dec] × 8 (24)` | **ERROR** | 3+dec=5→4 ×8 =40→32, not 24. Stated 24 would need 5→? Actually 32→24 needs different operation. | `[2 sc, dec] ×8 (24)` =4→3 ×8 from 32. |
| **M-Rnd 28:** `[2 sc, dec] × 8 (16)` | **ERROR** | 2+dec=4→3 ×8 =32→24 not 16. | `[sc, dec] ×8 (16)` =3→2 ×8 from 24. |
| **M-Rnd 29:** `[sc, dec] × 8 (8)` | **ERROR** | 1+dec=3→2 ×8 =24→16 not 8 (if drift-corrected). From stated 16: 3→2 ×8 =16→10 not 8. | `dec around (8)` from 16 =8. |
| **M-Rnd 30:** `close remaining 12 sts with sl st` | **ERROR** | Remaining after M-Rnd 29 is **8** (stated), not 12. Mismatch of 4 sts. Also `close with sl st` is not a defined closure count — cinch vs join confusion. | `Fasten off, cinch remaining 8 sts closed.` |

### Head (Section 4 — Head subpiece)

| Location | Severity | Finding | Correction |
|---|---|---|---|
| **H-Rnd 1: 48 sc** | **ERROR (state+arithmetic)** | Attaches to "mantle opening" which at M-Rnd 29-30 is 8 sts (or 12). Cannot pick up 48 sc from 8. No increase row written to bridge 8→48. | Add bridge rnd: `* inc around to 48` or keep opening at 48 (don't decrease mantle to 8 before head). |
| **H-Rnd 18: sc around (12)** with incoming 8 | **ERROR** | sc around preserves count: 8→8, not 8→12. Increase operation missing. | `[sc, inc] ×4 (12)` =2→3 ×4 from 8. |

### Tentacles (Section 5) — cumulative drift example

Individual inc rounds are correct, but state propagation breaks twice:

| Location | Severity | Finding | Correction |
|---|---|---|---|
| **T-Rnd 21:** `[4 sc, dec] ×4 (20)` incoming 24 | **OK arithmetic** | 4+dec=6→5 ×4=24→20 — passes alone. | — |
| **T-Rnd 22–26:** `sc around (24)` | **ERROR — state propagation** | Incoming is 20 from T-Rnd 21, but states 24. Off by +4 for 5 rounds. Cumulative drift hidden by correct arithmetic on wrong base. | `sc around (20)` or insert inc back to 24. |
| **T-Rnd 27:** `[3 sc, dec] ×4 (16)` incoming stated 24 | **ERROR** | Operation 5→4 ×4 =20→16, not 24→16. Relies on inflated base. | `[4 sc, dec] ×4 (16)` =6→5 ×4 from 20. |
| **T-Rnd 39:** `dec around (6)` incoming 12 | **OK** | 2→1 ×6=12→6 — passes. | — |
| **T-Rnd 40:** `sc around (12)` incoming 6 | **ERROR — over-double / arithmetic** | sc around 6→6, not 6→12. Stated doubles without inc operation. This is `increase direction` / `over-double` class (6→12 without inc). | `[sc, inc] ×6 (18)` or `inc around (12)` or `sc around (6)`. |

### Suction Cups (Section 6)

| Location | Severity | Finding | Correction |
|---|---|---|---|
| **Row:** `Work 12 suction cups. Each =5 sc in one stitch.` + `Each row must contain exactly 48 sts` | **ERROR** | 12 cups ×5 sc =60 sc consumed/produced in one stitch base. Cannot be done in 48-st row. Also `5 sc in one stitch` = inc ×4 (1→5) violates edging fullness (~5×). | Either `4 sc in one st (48)` or `12 cups ×4 sc =48` or change row count to 60. |
| **Tentacle total:** `8 rows ×12 cups =96 per tentacle` | **OK arithmetic** | 8×12=96 internally consistent, but contradicts per-row stitch count above. | Fix row count first. |
| Color rule `Color C every third cup, B others` vs Materials `120A/90B/60C` not validated here — flagged as unverified color distribution. |

### Heart (Section 7 — listed as Rows but uses rounds)

| Location | Severity | Finding | Correction |
|---|---|---|---|
| **All rows use `inc around / sc around`** | **WARNING — terminology** | Described as *Row* but worked in the round (MR/ch2 inc around). Row vs round language mismatch causes `spiral_and_join` / `row_uses_around` confusion. | Use `Rnd` not `Row`. |
| **Rows 6–10:** `sc across (30)` | **OK** | 30→30 passes. | — |

### Gears (Section 8)

| Location | Severity | Finding | Correction |
|---|---|---|---|
| **G-Rnd 3:** `[sc, ch3, sl st in first ch, sc] ×8 (24)` incoming 16 | **ERROR — chain counts** | Each repeat uses 2 sc + chain picot (0 consumed). Consumed =2 per repeat ×8 =16 → produces 2+? Actually produces 2 sc =16? Picot not a stitch. Stated 24 expects +8 phantom stitches from `ch3` counted as stitches (chain counts twice error). | `sc around (16)` with picots as surface, not counted, or ` [sc, picot, sc] ×8 (32)` with correct production. |
| **G-Rnd 4:** `sc around (32)` incoming 24 | **ERROR — state** | 24→32 needs 8 inc, not sc around. | ` [3 sc, inc] ×8 (32)` =4→5 ×8 from previous corrected count, or `sc around (24)`. |
| **Teeth/spokes spec:** `8 teeth, 12 spokes` | **ERROR — component mismatch** | G-Rnd 3 makes 8 picots =8 teeth implies 8 spokes, not 12. Count mismatch planted. | Choose 8 or 12 consistently. |

### Eyes (Section 9)

| Location | Severity | Finding | Correction |
|---|---|---|---|
| **Eye total arithmetic** | **ERROR** | `Place two 18mm safety eyes` + `Embroider two additional eyes` =4 eyes, but `Finished must have exactly two eyes` and `All four eyes must be installed` + `exactly two` vs `four` contradictory count. | Pick 2 or 4. |

---

## 2. STATE PROPAGATION — Starting count ≠ prior ending count

This is the classic drift the benchmark stresses: each round looks correct alone, but the chain is broken.

- **Mantle M-Rnd 20–24:** Starts `sc around (56)` but prior M-Rnd 19 claims 48. Gap **+8**.
- **Mantle M-Rnd 25 onward:** Entire taper 25→29 is offset by that 8, causing every subsequent `[x sc, dec]` to be misaligned (see arithmetic above). This is the planted cumulative drift.
- **Tentacle T-Rnd 22–26 vs 21:** +4 drift for 5 rounds, then hidden by next correct-looking decrease.
- **Tentacle T-Rnd 40 vs 39:** +6 drift (6→12 without inc).
- **Head H-Rnd 18 vs 17:** +4 drift (8→12 without inc).
- **Gear G-Rnd 4 vs 3:** +8 drift.
- **Head attachment H-Rnd 1 vs mantle opening:** 48 vs 8/12 — **40-st gap**. Detected by `equal socket` / `span match` checks.

Checker handling: these are reported as `stated_count` + `incoming_cover` + `span_match` errors, not just one global fail.

---

## 3. CROSS-SECTION CONTRADICTIONS — Assembly vs Materials vs Construction

These are multi-section logic conflicts, not stitch math.

| Sections in conflict | Severity | Explanation |
|---|---|---|
| **1 Construction: completely seamless, no sewn components** vs **1 Assembly: all 12 sewn permanently** vs **11 QC: No sewn components / No seams** | **CRITICAL** | Cannot be seamless and sewn simultaneously. Your `seam_count` validator flags the 12 tentacle seams against `seamless` declaration. |
| **1 Mechanical: removable for washing, no detach during play** + **4 Mantle: hollow vs stuffed completely vs no openings vs removable without seam** | **CRITICAL** | Four-way mutual exclusion. `closed_join` + `fasten_continue` stages report: cinched-closed piece cannot be entered without a seam. |
| **4 Mantle notes: head+mantle one continuous piece vs head detachable for cleaning** vs **10 Assembly 1 & 4: crochet as one piece vs detachable head vs invisible permanent seam** | **CRITICAL** | One-piece and detachable are opposite `piece reference` graph edges. Assembly step 4 creates a cycle. |
| **2 Materials: 12 plastic joints + 8 gears vs 1 spec: six brass-look gears + 12 tentacles** | **WARNING/ERROR** | Gear count 6 vs 8 planted mismatch (`make_count` vs `assembly`). Joint count 12 matches tentacles but spec says gears 6 — spec/materials `eye_count` analogue. |
| **2 Hooks: 3.0 mm (use), 4.0 mm finishing only, 2.5 mm materials only** | **WARNING** | Two phantom hooks never used in any rnd. `ghost reference` — material lists hook never invoked, finishing references hook never listed. |
| **3 Abbreviations: All rounds spiral unless stated / Join with sl st and turn after each rnd** | **ERROR** | Direct contradiction. Spiral `spiral_and_join` + `spiral_turn` Lesson 100/70. Must be one or the other. Head uses `sc across` (row) vs `rnd` further confusion. |
| **3 Abbreviations: BLO/FLO/FPdc/BPdc/hdc/dc defined never used in Mantle/Head/Tentacles** | **INFO** | Unused glossary — not an error alone, but inflates false complexity. |
| **5 Tentacles: `No wire, joints, glue, or sewn attachments` vs `Each tentacle contains 1 joint + 3 wires` vs `stand upright`** vs **2 Materials: 1 m steel wire + 12 joints + hot glue** | **CRITICAL** | Direct prohibition violated by requirement. `both_directions` / `blo_and_both` family: `seamless and sewn` analogue. |
| **6 Suction cups: permanently attached but removable for washing + visible 360° + not alter circumference** | **CRITICAL** | Permanence vs removability; 5-sc clusters *must* alter circumference (edging fullness). |
| **7 Heart: hollow vs completely stuffed vs removable without opening vs permanently enclosed** | **CRITICAL** | Four-property impossible. Also `Stuff with exactly 50g` inside `250g total` vs `≤300g` weight chain. |
| **8 Gears: Attach without sewing/glue/knots/hardware vs 10/11 using hot glue only vs QC No glue vs removable** | **CRITICAL** | No-attachment method contradicts glue step; glue contradicts QC No glue and removable. |
| **10 Assembly order:** Step 2 close mantle/head completely → Step3 insert heart through closed mantle → Step6 insert wires after closing tip → Step11 install eyes after closing head | **ERROR** | `closed_join` + `eyes_before_stuffing` + `fasten_continue` violations. Cannot insert after cinch without reopening. |
| **10 Assembly 7 + 5 requirement:** `Flatten and sew shut using six sts. Do not use needle/thread.` vs `No sewn components` vs QC `No seams` | **ERROR** | Impossible closure instruction — flagged as `two_seams` / `sew without tool` paradox. |
| **9 Eyes: Both eyes must be removable after head is closed + Do not leave any openings** | **ERROR** | Safety eye washer requires inside access; removable after closure leaves opening. |

---

## 4. DIMENSIONAL CONSISTENCY — Gauge, length, circumference, weight

These are `gauge_band` + `span_match` + unverified dimensional claims.

### Gauge contradiction (Section 1 + 2)

- **Alternative gauge:** `22 sc ×24 rnds =10×10cm` AND `20 sc ×22 rnds =10×10cm` **with same yarn and same 3.0 mm hook** — impossible. Gauge is a measured property, cannot be two values simultaneously for one yarn/hook. Checker reports `gauge_band` WARNING + contradictory specification.
- **Worsted cotton + 3.0 mm hook at 22 sc/10cm:** Worsted expected 11–14 sc/4in (CYC). 22 sc/10cm = ~28 sc/4in is double — outside `gauge_band` (tight amigurumi exception applies, but alternative 20 sc/10cm vs 22 sc/10cm still inconsistent).

### Circumference vs stitch count mismatch

- **Mantle target 42 cm at 22 sc/10cm:** Needle math: 22 sc =10cm → 2.2 sc/cm ×42 cm = **92.4 sc** circumference. Written mantle max is **48–56 sc** — less than half. Planted dimensional mismatch.
- **Head target 38 cm:** Needs 83.6 sc at same gauge. Written max 56 sc — **27.6 sc short**.
- **Gears 10 cm circumference at 22 sc/10cm:** Needs ~22 sc. Written max 32 sc (G-Rnd 4) — oversized. Teeth spec 8 vs spokes 12 adds second dimensional mismatch.
- **Heart 5 cm wide + 8 cm tall vs 30 sc sphere:** At gauge, 30 sc circumference = 13.6 cm → diameter ~4.3 cm, not 5×8. Height inconsistency.
- **No positive proof:** Per policy, the checker **warns** on dimensional mismatch as `unverified claims` + `gauge_band`, does not claim to have measured the piece.

### Length contradictions (Section 5)

- **Tentacles:** `Exactly 17 cm` vs `1–4 =12 cm, 5–8=17 cm, 9–12=22 cm` vs `identical round counts` — three-way exclusion. Identical counts cannot yield three lengths. Checker flags as `clause_total` / contradictory spec.
- **Height 28 cm including tallest tentacle + No tentacle above mantle:** If tallest is 22 cm and mantle is separate, seating would place tentacles above mantle. 28 cm total vs 22 cm tentacles + mantle/head height undefined.
- **Troubleshooting 3:** `add rounds without recalculating` guarantees count drift — documented as anti-pattern.

### Weight — impossible by materials alone

- **Input weight:** 120+90+60 =270 g yarn + 250 g stuffing =520 g + 40 g thread + wire (~20g) + 12 joints + 8 gears + heart = **~600 g**.
- **Spec + Materials note:** `no more than 300 g regardless of how much ... is used` — physically impossible. Checker flags as `unverified weight claim` + self-contradicting note.
- **Heart + Troubleshooting:** `Stuff heart with exactly 50g` then `remove stuffing to hit 300g` vs `exactly 50g` — contradictory remediation. `If exceeds 300g remove stuffing` violates firm stuffing spec.

---

## 5. COMPONENT LOGIC — Removable vs permanent vs enclosed vs hollow

This tests the benchmark's core: impossible state machines for parts.

| Component | Logic chain | Severity |
|---|---|---|
| **Mantle** | hollow → stuffed completely → no openings → removable heart | **CRITICAL** |
| **Heart** | hollow + stuffed + removable without opening + permanently enclosed  | **CRITICAL** |
| **Head** | one piece with mantle → detachable + permanent seam + close completely + install eyes after closing + no openings | **CRITICAL** |
| **Tentacles (×12)** | seamless → sewn permanently → contain joint+wire but no wire/joint allowed → articulated 180° without hardware → stand upright seated kraken | **CRITICAL** |
| **Suction cups (96)** | permanently attached + removable + invisible seam + no circumference change | **CRITICAL** |
| **Gears (6)** | no sewing/glue/hardware + hot glue only + no glue + permanently attached + fully removable | **CRITICAL** |
| **Overall** | No removable components vs All components removable for washing vs No component detaches during play vs Washable in hot water without removing anything | **CRITICAL** |

Each is a deterministic `fasten_continue` + `closed_join` + `assembly_graph` violation in the codebase: a cinched piece cannot be entered, eyes cannot be placed after `close`, and a part cannot be both `sewn` and `seamless`.

---

## 6. SAFETY CLAIMS — Under-36-months audience

These are flagged as **compliance warnings**, not invented safety certifications.

| Location | Severity | Concern |
|---|---|---|
| **Audience <36 months + 18 mm safety eyes (×2) + 8 gears + 1 heart 5cm + 12 joints + 1 m steel wire + hot glue** | **CRITICAL WARNING** | Small detachable parts (eyes 18 mm borderline, gears <31.75 mm, heart 5 cm detachable) + exposed wire puncture/CPSC choke & sharp point. Hot glue not washable, degrades. Braided 1 m steel wire through 12 tentacles = strangulation/injury. Checker reports: intended audience claim requires external testing — not proven by text. |
| **Plastic heart removable + permanent enclosed + hot glue + steel wire** | **CRITICAL** | Detachable heart is choking hazard for <3 y; `All must be removable for washing but no component may detach during play` is untestable from text. Flag as `unverified safety claim`. |
| **Fully washable in hot water (wool/cotton + hot glue + steel wire + plastic joints/gears)** | **WARNING** | Hot water warps PLA gears, rusts wire, softens hot glue. Claim is material-incompatible. Checker warns as `material care` mismatch (docs/standards). |
| **No additional testing suitable** | **WARNING** | Self-certification is not compliance. Checker never certifies safety. |

> The checker **does not** declare a toy legally safe/unsafe from text. It flags: small-part counts, removable hazards, wire/chemical mentions, and self-certification language as needing external lab review.

---

## 7. FALSE-POSITIVE AVOIDANCE — What we deliberately do NOT claim

Per your challenge briefing:

- **Geometric sphericity:** `remain perfectly spherical` after tapered decreases is a subjective shape claim. We flag as `unverified dimensional claim`, not as a proven geometric error, because checker measures stitches, not 3D curvature.
- **180° articulation:** No simulation proves fabric bend angle. We flag `unverified performance claim` (needs wire spec), not a physics proof.
- **Standing upright without support:** Center-of-gravity proof not possible from stitch counts. Flagged as `unverified assembly claim`.
- **Smile 7 cm not crossing any stitch:** Ambiguous path (between stitches vs over). Flagged as `ambiguous placement`, not counted as stitch overwrite.
- **Visibility claims:** `visible from every viewing angle` / `visible from front and back simultaneously` — flagged as `prose impossibility warning`, not a mesh proof.

---

## 8. FINISHING QC SELF-CONTRADICTION (Section 11) — The final trap

Section 11 demands **simultaneously**:

- Exactly 28/42/38 cm (exact, no tolerance)
- Exactly 12×17 cm tentacles (vs earlier 12/17/22 split — now triple conflict)
- No visible seams / No sewn components / No glue / No wire / No removable components
- **AND** All components removable for washing / Fully washable in hot water / Secure during pulling

This list itself is the planted final exam: it contains **mutually exclusive QC** items. The checker reports each as a separate `both_sides_facing` + `inside_and_out` style finding, not just `pattern invalid`.

Troubleshooting compounds it (intentionally bad advice):

- `Add decrease anywhere` → hides count errors
- `Switch hook halfway` → guarantees gauge inconsistency
- `Add rounds without recalculating` → guarantees state drift
- `Remove stuffing to hit weight` → violates firmness/hollow specs
- `Additional hot glue` vs `No glue` → oscillation
- `Cut opening after closing` → violates `no openings` + creates visible seam
- `Insert additional wire` vs `No wire` → oscillation
- `Sew permanently if difficult to remove` → violates `removable`

Each troubleshooting line is a planted `contradictory remediation`.

---

## SUMMARY — Expected status: FAIL

**Arithmetic failures:** 9 definite count mismatches + 1 over-double (M-Rnd 13/19/25-30, H-18, T-22/27/40, G-3/4, cups)
**State propagation failures:** 4 sustained drifts (Mantle 20–30, Head 48-vs-8, Tentacle 22–27 + 40, Gear 4)
**Cross-section failures:** 7 construction-vs-assembly contradictions
**Dimensional failures:** 2 gauge contradictions + 3 circumference mismatches + weight impossibility (~600 g vs 300 g)
**Component logic failures:** 6 impossible state machines (mantle/heart/head/tentacles/cups/gears)
**Safety flags:** 3 critical under-36-months hazards needing lab review
**QC paradox:** Final checklist internally exclusive by design

A strong checker implementation (your `stitch_counts`, `incoming_cover`, `span_match`, `closed_join`, `fasten_continue`, `assembly_graph`, `gauge_band`, and `unverified claims` stages) should surface **~30 discrete findings** with location + severity + explanation + correction, rather than a single `FAIL`.

---

**THE CLOCKWORK KRAKEN** benchmark validated — original preserved unchanged, audit complete. For your test harness: compare this classification against `scripts/check_consensus.py` lessons `01_stated_count`, `02_repeat_cover`, `11_seam_count`, `12_inch_span`, `69_join_contradiction`, `70_spiral_and_join`, `87_spiral_turn`, `100_spiral_turn`, `101_fasten_continue`, and `108_negative_gauge`.

*Generated: 2026-10-25 | Checker: Crochet Pattern Checker v1.0.0 deterministic text stages — no photo, chart image, or hosted LLM used for counts.*
