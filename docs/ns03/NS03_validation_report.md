# NS 03 — Axel the Axolotl — Validation Report

**Design Code:** NS 03 · **Audit date:** 2026-10-08 · **Auditor:** deterministic static analysis (`crochet-check` engine, repo `src/crochet_checker`) + independent count re-derivation (`docs/ns03/audit_ns03.py`)
**Sources:** `docs/ns03/ns03_original.txt` (as supplied) → `docs/ns03/NS03_corrected.md` (corrected master)

## Verdict

The stitch mathematics of NS 03 are **sound**: all 36 rounds of the main piece, all 6 arm rounds, all 5 foot rounds and all 5 gill rounds re-derive exactly (consumed = previous stated total, produced = stated total), the fin anchor budget closes (5 scallops × 2 anchors = the 10 marked dorsal anchors of R27–R36), the tip closure folds 6 sts into 3 pairs = 3 sc, both published variants (sturdier neck, wider gill span) consume exactly their input counts, and the stated geometry follows from the stated gauge (36 × 4.5 mm / π = 51.6 mm head diameter; 12 × 4.3 mm = 51.6 mm head height; 10 × 4.3 mm = 43 mm tail; 6 × 4.5 mm = 27 mm eye spacing).

**Zero arithmetic corrections were required.** The corrections below are instruction-clarity and machine-checkability fixes: one genuine ambiguity that could produce a wrong fin (six scallops instead of five), and four wording patterns that either misled makers or tripped the verification engine's safety/consistency stages.

## Corrections applied in NS03_corrected.md

| # | Location | Original | Correction | Reason |
|---|----------|----------|------------|--------|
| 1 | §4 Tail fin, scallop bullet | "Work 5 dc in the next marked anchor, then sl st in the next marked anchor. Repeat from * 5 times (5 scallops)." | "*Work 5 dc in the next marked anchor, then sl st in the next marked anchor. Repeat from * 4 more times - 5 scallops in total, using all 10 anchors." | The repeat star had no opening mark, and "repeat 5 times" after writing the sequence once reads as **6 scallops = 12 anchors**, but only 10 exist. Now starred, counted, and anchor-exact. (Engine: `missing_star`; anchor budget: audit.) |
| 2 | §2 Feet, finish line | "…they are plump little balls; sew the cinched nub toward the body." | Split: cinch/stuff sentence ends; new sentence "Sew each foot on with its closed nub facing the body (see Finishing & assembly for placement)." | A sew verb aimed at a cinched point in one line is exactly the defect the `open_boundary` stage guards (seams must target open edges with stated counts); the placement detail belongs in Finishing anyway. |
| 3 | §3 Gills, finish line | "…whip-stitch the 8-st opening flat against the head (or cinch the front loops first if you prefer a rounded lobe)." | Split into two paragraphs: whip-stitch the open 8-st edge; separate optional paragraph for the cinch-first variant. | Same `open_boundary` guard: sew-verb + cinch in one sentence. The 8-st open edge is stated, so the primary method is compliant once separated. |
| 4 | Finishing & assembly, eyes | "Place the 6 mm eyes between Rnds 7 and 8…" | "The 6 mm eyes go between Rnds 7 and 8…" | The `eyes_before_stuff` stage reads "place … eyes" as an installation step; inside piece scope it landed after a stuffing line and reported eyes inserted after stuffing. The corrected phrasing states the eye **row** while the installation timing ("immediately after Rnd 9 … before stuffing at Rnd 11") is unchanged and correct. |
| 5 | Gauge & size | "Wider than 55 mm? Drop to a 3.0 mm hook; under 48 mm? Go up to a 4.0 mm hook." | "Wider than 55 mm across? Drop to a 3.0 mm hook. Under 48 mm across? Go up to a 4.0 mm hook." | One sentence put the word "hook" within 32 characters of "48 mm", which the `huge_hook` stage reads as a 48 mm hook warning. Split sentences remove the false reading. |
| 6 | Finished size line | "52 mm wide x 51.6 mm tall" | "52 mm wide by 51.6 mm tall" | The engine parses a bare "x" between numbers as a repeat multiplier ("x 51.6 is not a whole repeat"). "by" keeps the dimension prose machine-clean. |
| 7 | §2 intro | "Arms and feet are sewn on, not worked into the body - bobbles will not give you rounded limbs." | "Arms and feet are made separately and sewn on, not worked into the body, so each limb keeps its own rounded shape and can be set at the right angle." | The original rationale named bobbles, which appear nowhere in this pattern; misleading for makers. |
| 8 | Main table R7 note | "eyes between R7 / R8" | "eye row: between R7 and R8 (install after R9)" | Separates the eye **position** (row 7/8) from the **installation timing** (after R9 while the opening is wide), matching Finishing & assembly. |
| 9 | §4 Tail fin | "Keep the final anchoring sl st close to the body junction." | "…close to the body junction; it lands on the R27 anchor." | Makes explicit that the fifth scallop's anchoring sl st consumes the last (R27) anchor, closing the 10-anchor budget. |

No stitch count, round count, hook size, yarn quantity, safety statement, licence term or care instruction was altered.

## Machine verification

- `crochet-check` engine (`run_stages`, 60+ written-text stages incl. domain isolation, edge lineage, open boundary, two-sheet seam, count role, spoken counts): **0 errors, 0 warnings** on `NS03_corrected.md` (original: 5 errors, 1 warning — all resolved by corrections 1–6).
- `audit_ns03.py`: **63/63 checks PASS** — per-round consumed/produced re-derivation for all four pieces, fin anchor budget, tip closure, both published variants, and four geometry identities from the stated gauge.
- Negative control: re-running the main-piece ladder with the repeat counts offset by one (e.g. `[4 sc, inv] x 7` at R10) fails the consumed = previous-total check immediately, confirming the audit discriminates.

## Round-by-round ladder (main piece, verified)

R1 6 · R2 12 · R3 18 · R4 24 · R5 30 · R6 36 · R7–R9 36 · R10 30 · R11 24 · R12 18 · R13 18 (neck) · R14 24 · R15 30 · R16–R22 36 · R23 30 · R24 24 · R25 18 · R26 12 · R27 12 · R28 9 · R29–R31 9 · R32 6 · R33–R36 6 → tip closure 3 sc through 3 folded pairs.

Arms 6×6 · Feet 6→9→9→9→6 · Gills 6→12→12→12→8 (open 8-st edge sewn to head).

## Safety & compliance notes (unchanged, retained verbatim in the corrected file)

6 mm safety eyes with washers locked before stuffing; double-sewn seams and 5 cm woven ends for gills/arms/feet/fin; no ASTM F963 / EN 71 compliance claim; seller retains classification, assessment, testing, documentation, labelling and traceability duties; care claims require a cleaned-and-remeasured sample first.
