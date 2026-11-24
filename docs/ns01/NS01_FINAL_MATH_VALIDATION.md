# NS01 Hamish the Highland Cow — Updated Mathematical Validation Report

**Date:** 2026-11-24 (UTC)  
**Source:** `patterns/01_Hamish_the_Highland_Cow.md` (post-correction)  
**Method:** Manual arithmetic recheck + `docs/kit/audit_lib.py` + `docs/kit/engine_run.py` + builder postflight. No stitch counts were changed.

## Summary

| Check | Result |
|---|---|
| Independent audit (`audit_lib.py`) | **0 problems, 0 unparsed rows** |
| Deterministic engine (`engine_run.py`) | **0 errors, 0 warnings** |
| Stitch-count changes made in this pass | **None** |
| Construction clarifications made | Head finishing, standard leg finishing, head-body join, opening retention, scarf turning chain |

## Component validation

### 1. Head (Yarn A, R1–R16)
| Rnd | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| R1 | MR 6 | 6 | (6) | PASS |
| R2 | inc x 6 | 12 | (12) | PASS |
| R3 | (sc 1, inc) x 6 | 18 | (18) | PASS |
| R4 | (sc 2, inc) x 6 | 24 | (24) | PASS |
| R5 | (sc 3, inc) x 6 | 30 | (30) | PASS |
| R6 | (sc 4, inc) x 6 | 36 | (36) | PASS |
| R7–R11 | sc around | 36 | (36) | PASS |
| R12 | (sc 4, dec) x 6 | 30 | (30) | PASS |
| R13 | (sc 3, dec) x 6 | 24 | (24) | PASS |
| R14 | (sc 2, dec) x 6 | 18 | (18) | PASS |
| R15 | (sc 1, dec) x 6 | 12 | (12) | PASS |
| R16 | dec x 6 | 6 | (6) | PASS |

**Head finishing:** Added explicit closing instruction after R16 (FLO through remaining 6, pull tight, knot, weave in). No count impact.

### 2. Muzzle (Yarn B)
| Rnd | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| R1 | MR 6 | 6 | (6) | PASS |
| R2 | inc x 6 | 12 | (12) | PASS |
| R3 | (sc 1, inc) x 6 | 18 | (18) | PASS |
| R4 | sc around | 18 | (18) | PASS |

FO, leave long tail for sewing; lightly stuffed; not closed. Unchanged.

### 3. Body (Yarn A)
| Rnd | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| R1 | MR 6 | 6 | (6) | PASS |
| R2 | inc x 6 | 12 | (12) | PASS |
| R3 | (sc 1, inc) x 6 | 18 | (18) | PASS |
| R4 | (sc 2, inc) x 6 | 24 | (24) | PASS |
| R5 | (sc 3, inc) x 6 | 30 | (30) | PASS |
| R6 | (sc 4, inc) x 6 | 36 | (36) | PASS |
| R7–R12 | sc around | 36 | (36) | PASS |
| R13 | (sc 4, dec) x 6 | 30 | (30) | PASS |
| R14 | sc around | 30 | (30) | PASS |
| R15 | (sc 3, dec) x 6 | 24 | (24) | PASS |
| R16 | sc around | 24 | (24) | PASS |
| R17 | (sc 2, dec) x 6 | 18 | (18) | PASS |
| R18 | sc around | 18 | (18) | PASS |
| R19 | (sc 1, dec) x 6 | 12 | (12) | PASS |

Body remains open at R19 with 18-st attachment context clarified in assembly (R19 ring used as neck opening/attachment ring; R14 head ring has 18 sts for one-for-one match). No count changes.

### 4. Belly Patch (Yarn B, rows)
| Row | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| Foundation | ch 9 | 9 | - | PASS |
| R1 | sc in 2nd ch from hook and across, ch 1, turn | 8 | (8) | PASS |
| R2–R6 | sc across, ch 1, turn | 8 | (8) | PASS |
| R7 | sc across | 8 | (8) | PASS |

Terminology corrected to `Foundation:`; counts unchanged.

### 5. Legs (Yarn B/C, make 4)
| Rnd | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| R1 | MR 6 | 6 | (6) | PASS |
| R2 | inc x 6 | 12 | (12) | PASS |
| R3 | BLO sc around | 12 | (12) | PASS |
| R4 | sc around (C) | 12 | (12) | PASS |
| R5 | (sc 4, dec) x 2 | 10 | (10) | PASS |
| R6–R8 | sc around | 10 | (10) | PASS |
| R9 | (sc 3, dec) x 2 | 8 | (8) | PASS |
| R10–R15 | sc around | 8 | (8) | PASS |
| R16 | sc in each st around | 9 | (9) | PASS (as written) |

**R16 note:** Instruction states `sc in each st around (9)`. Count progression 8→9 implies one increase in the round. This is unchanged from original pattern and not altered in this pass (no silent count change). Added finishing clarification: leave 9-stitch opening open, 30–40 cm tail, no closing/flattening.

### 6. Shortened Front Legs (optional)
| Rnd | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| R1–R9 | same as standard | 6,12,12,12,10,10,10,10,8 | match | PASS |
| R10 | sc around | 8 | (8) | PASS |

FO with 40 cm tail, do not close/flatten; 12-st top-opening measurement preserved as written in assembly note (legacy measurement note retained; not a stitch-count row). No stitch-count rows changed.

### 7. Ears (Yarn A, make 2)
| Rnd | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| R1 | MR 4 | 4 | (4) | PASS |
| R2 | (sc 1, inc) x 2 | 6 | (6) | PASS |
| R3 | (sc 2, inc) x 2 | 8 | (8) | PASS |
| R4 | (sc 3, inc) x 2 | 10 | (10) | PASS |
| R5 | (sc 4, inc) x 2 | 12 | (12) | PASS |
| R6 | sc around | 12 | (12) | PASS |

### 8. Horns (Yarn D, make 2)
| Rnd | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| R1 | MR 4 | 4 | (4) | PASS |
| R2 | (sc 1, inc) x 2 | 6 | (6) | PASS |
| R3–R4 | sc around | 6 | (6) | PASS |

### 9. Scarf (Yarn C)
| Row | Instruction | Math | Stated | Check |
|---:|---|---:|---:|:---:|
| Foundation | ch 61 | 61 | - | PASS |
| R1 | hdc in 2nd ch from hook and across | 60 | (60) | PASS |
| R2 | ch 2, turn, hdc across (turning ch does not count) | 60 | (60) | PASS |

**Correction:** R2 turning chain changed from `ch 1` to `ch 2` for hdc; stitch count remains 60.

## Construction / placement checks

| Check | Status | Notes |
|---|---|---|
| Head closure at R16 (6 sts) | PASS | Explicit FLO closure added. |
| Body neck/open attachment ring R19 (18 sts) | PASS | Clarified in assembly. |
| Head attachment ring R14 (18 sts) | PASS | Explicitly stated as attachment ring; 1:1 to Body R19. |
| Head R16 6-st closure not used as 18-st seam target | PASS | Explicitly warned against. |
| Standard leg top remains open (9 sts) | PASS | Explicit do-not-close instruction added. |
| Shortened front legs not closed/flattened | PASS | Explicit in finishing/placement text. |
| Three-size claims qualified | PASS | Estimated/untested; no physical sample claimed. |

## Tooling results

```text
audit_lib.py: NS01 Hamish — 0 problems, 0 unparsed
engine_run.py: ERRORS (0), WARNINGS (0)
build_ns01_etsy_pdf.py postflight:
  Color: PASS — 14 A4 pages, 4.91 MiB, 3 distinct images, 81 progress boxes, 837 text spans in bounds
  Printer-saver: PASS — 13 A4 pages, 0.13 MiB, 88 progress boxes, 833 text spans in bounds, no raster images
```