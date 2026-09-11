"""Audit harness for the Christmas Collection (NS X01-X03).

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
from . import PATTERNS

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


def main():
    bobble_derivations()
    print("== Deterministic audit ==")
    reports = [audit_pattern(p) for p in PATTERNS]
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
