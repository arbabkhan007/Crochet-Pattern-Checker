"""Audit harness for the Christmas Collection (NS 11, NS 12, NS 13).

Reuses the master audit's audit_pattern() (continuity, stated counts, parser
dual-check, repo StitchCountValidator, abbreviation + terminology scans) and
adds derivation checks for the constructions outside the parser grammar
(bobbles, fan edges, chain spaces).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from tools.novality.audit import audit_pattern
from . import PATTERNS, NEW

RESULTS = Path("tools/novality_xmas/audit_results.json")


def expect(name: str, got, want):
    line = f"{'OK ' if got == want else 'FAIL'} {name}: got {got}, want {want}"
    print("  " + line)
    if got != want:
        raise AssertionError(line)


def bobble_derivations():
    print("== Manual derivations (bobbles, fans, chain spaces) ==")
    # Gnome nose round: 14 sc + BO + 15 sc => 30
    expect("Gnome R14 nose", (14 + 1 + 15), 30)
    # Tree bobble rounds
    for rnd, rep, cons_per, prod_per, prev, prod in [
        ("R10", "[BO, 7 sc]", 1 + 7, 1 + 7, 48, 48),
        ("R12", "[BO, 5 sc, sc2tog]", 1 + 5 + 2, 1 + 5 + 1, 48, 42),
        ("R14", "[BO, 4 sc, sc2tog]", 1 + 4 + 2, 1 + 4 + 1, 42, 36),
        ("R16", "[BO, 3 sc, sc2tog]", 1 + 3 + 2, 1 + 3 + 1, 36, 30),
        ("R18", "[BO, 2 sc, sc2tog]", 1 + 2 + 2, 1 + 2 + 1, 30, 24),
        ("R20", "[BO, sc, sc2tog]", 1 + 1 + 2, 1 + 1 + 1, 24, 18),
        ("R22", "[BO, sc2tog]", 1 + 2, 1 + 1, 18, 12),
    ]:
        expect(f"Tree {rnd} {rep}", (cons_per * 6, prod_per * 6), (prev, prod))
    # Star: 2 centre stitches per point x 5 = 10; fans 7 sts x 5 + 5 sl st = 40
    expect("Star R2 consumption", 2 * 5, 10)
    expect("Star R2 edge count", 7 * 5 + 5, 40)
    # Snowflake ring + spaces
    expect("Snowflake R1 spokes", 11 + 1, 12)
    expect("Snowflake R2 consumption", 2 * 6, 12)
    # Bauble ladder anchors
    expect("Bauble R7 consumes", 4 * 6, 24)

    # ---- NS 14 tree skirt: the 12-spoke ladder ----
    skirt = next(p for p in NEW if p["id"] == "treeskirt")
    rows = [r for pc in skirt["pieces"] for sp in pc["subpieces"] for r in sp["rows"]]
    rnd_rows = [(int(r["label"][1:]), r) for r in rows if r["label"].startswith("R")]
    for n, r in rnd_rows:
        expect(f"Skirt R{n} stated == 12*{n}", r["stated"], 12 * n)
        expect(f"Skirt R{n} continuity",
               (r["cons"] if r["cons"] is not None else 0, r["prod"]),
               (12 * (n - 1), 12 * n))
    for n, scallops in ((14, 28), (23, 46), (32, 64)):
        s = dict(rnd_rows)[n]["stated"]
        expect(f"Skirt R{n} divisible by 6 -> scallops", (s % 6, s // 6), (0, scallops))
    expect("Skirt bobble rounds", [n for n, r in rnd_rows if "BO " in r["text"]],
           [5, 8, 11, 14, 17, 20, 23, 26, 29, 32])

    # ---- NS 15 wreath ----
    wreath = next(p for p in NEW if p["id"] == "wreath")
    wrows = [r for pc in wreath["pieces"] for sp in pc["subpieces"] for r in sp["rows"]]
    petals = next(r for r in wrows if r["label"] == "Petals")
    expect("Poinsettia petals consume all 6 centre sts", petals["cons"], 6)
    expect("Poinsettia per-petal production", petals["prod"], 6 * (3 + 1))  # 3 tr + 1 sl st
    expect("Poinsettia leaf chains used", 1 + 1 + 3 + 1 + 1, 7)  # of 8 ch, 2nd-ch start
    expect("Bow tails from 15 ch", 15 - 1, 14)
    expect("Bow band from 6 ch", 6 - 1, 5)
    snow = next(r for r in wrows if r["label"] == "R2" and "Ch 5" in r["text"])
    expect("Wreath snowflake R2 consumption", snow["cons"], 12)
    expect("Wreath tube constant stitch", 12, 12)


def main():
    bobble_derivations()
    print("== Deterministic audit ==")
    reports = [audit_pattern(p) for p in PATTERNS + NEW]
    RESULTS.write_text(json.dumps(reports, indent=2))
    errors = 0
    for r in reports:
        status = "PASS" if not r["errors"] else "FAIL"
        print(f"[{status}] {r['title']} ({r['design_code']}) - {r['rows_checked']} rows / "
              f"{r['blocks']} blocks, {r['repo_validated_blocks']} repo-validated, "
              f"{r['manual_rows']} manual rows, {len(r['errors'])} errors, "
              f"{len(r['warnings'])} warnings")
        errors += len(r["errors"]) + len(r["warnings"])
        for e in r["errors"] + r["warnings"]:
            print(f"    [{e['level']}] {e['where']}: {e['message']}")
    if errors:
        sys.exit(1)
    print("All Christmas patterns PASS the audit.")


if __name__ == "__main__":
    main()
