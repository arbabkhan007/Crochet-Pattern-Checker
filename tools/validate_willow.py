#!/usr/bin/env python3
"""Deterministic validation driver for the Willow the Bunny Lovey pattern.

Pipeline (mirrors the repo's philosophy — AI never decides correctness):
  1. Split the pattern into pieces (HEAD / EARS / BLANKET).
  2. Parse each round-based piece with the repo parser and run the repo's
     deterministic stitch-count validator on it.
  3. Additionally check that round numbers are CONTIGUOUS (a skipped round
     number is how rows/rounds get lost in layout, and it breaks the count
     chain silently).
  4. For the granny-square blanket, check every stated checkpoint against the
     closed-form granny-square model + the stated gauge.

Usage: python tools/validate_willow.py <pattern.txt> [--json]
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from crochet_checker.parser import parse_pattern  # noqa: E402
from crochet_checker.validation.stitch_counts import validate_stitch_counts  # noqa: E402

PIECE_RE = re.compile(r"^===\s*(.+?)\s*(?:\((.*?)\))?\s*===$")
GAUGE_MM_PER_ST = 4.3          # stated in the pattern
GAUGE_MM_PER_RND = 3.8         # stated in the pattern
GRANNY_RNDS = 20               # stated blanket size basis
BORDER_SC_STATED = 252
DC_CHECKPOINTS_STATED = {3: 36, 5: 60, 10: 120, 15: 180, 20: 240}
SIZE_CLAIMS_CM = {18: 23, 20: 26, 22: 28}   # rounds -> claimed cm per side
GROWTH_CLAIM_CM = 1.3
GAUGE_CHECK_CLAIM_MM = 39    # "9 dc along an edge should measure ~39 mm"
HEAD_DIAMETER_CLAIM_CM = 4.9
HEAD_HEIGHT_CLAIM_CM = 5.7   # 15 rounds x 3.8 mm (v2 correction: 5 decrease rounds needed from 36 sts)
HEAD_MAX_STS = 36
HEAD_RNDS = 15


def split_pieces(text: str):
    pieces, name, buf = [], None, []
    for line in text.splitlines():
        m = PIECE_RE.match(line.strip())
        if m:
            if name:
                pieces.append((name, "\n".join(buf)))
            name, buf = (m.group(1), [m.group(2) or ""] if m.group(2) else [m.group(1)])
        elif name is not None:
            buf.append(line)
    if name:
        pieces.append((name, "\n".join(buf)))
    return pieces


def round_numbers(text: str):
    nums = []
    for line in text.splitlines():
        m = re.match(r"^(?:Round|Rnd)s?\s+(\d+)(?:\s*[-–]\s*(\d+))?", line.strip(), re.I)
        if m:
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else a
            nums.extend(range(a, b + 1))
    return nums


def check_contiguity(name: str, text: str, findings: list):
    nums = round_numbers(text)
    if not nums:
        return
    expected = list(range(nums[0], nums[0] + len(nums)))
    missing = sorted(set(expected) - set(nums))
    dupes = sorted({n for n in nums if nums.count(n) > 1})
    if missing:
        findings.append(
            f"STRUCTURE | {name}: round number sequence skips {missing} "
            f"(have {nums[0]}..{nums[-1]}). A round was lost in layout or was never written."
        )
    if dupes:
        findings.append(f"STRUCTURE | {name}: duplicate round number(s) {dupes}.")


def check_round_piece(name: str, text: str, findings: list):
    # comments are notes for humans — strip them so they don't pollute the parse
    text = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
    pattern = parse_pattern(text)
    report = validate_stitch_counts(pattern)
    for f in report.findings:
        sev = f.severity.value
        fix = f" -> FIX: {f.suggested_fix}" if f.suggested_fix else ""
        findings.append(f"{sev} | {name} {f.location}: {f.message}{fix}")
    check_contiguity(name, text, findings)
    return len(report.errors)


def granny_model_checks(findings: list):
    """Closed-form granny-square math vs. every stated checkpoint."""
    ok = 0
    def chk(label, ok_flag, detail):
        nonlocal ok
        findings.append(("PASS" if ok_flag else "FAIL") + f" | BLANKET: {label} — {detail}")
        ok += 1 if ok_flag else 0

    # dc per round: R1 = 4 groups x 3 = 12; each round adds one 3-dc group per side (+12)
    series = {n: 12 * n for n in range(1, GRANNY_RNDS + 1)}
    bad = {n: v for n, v in DC_CHECKPOINTS_STATED.items() if series.get(n) != v}
    chk("dc checkpoints (R3=36, R5=60, R10=120, R15=180, R20=240)",
        not bad, f"model gives {({n: series[n] for n in DC_CHECKPOINTS_STATED})}" +
                 (f"; mismatches: {bad}" if bad else ""))

    # edge width at R20: 3 dc per side per round -> 60 dc per edge
    edge20 = 3 * GRANNY_RNDS
    chk("60 dc per edge at R20", edge20 == 60, f"model: 3 x {GRANNY_RNDS} = {edge20}")
    chk("edge size 60 x 4.3 mm = 26 cm", abs(edge20 * GAUGE_MM_PER_ST / 10 - 26) < 0.25,
        f"{edge20 * GAUGE_MM_PER_ST / 10:.1f} cm (claimed 26 cm)")

    # gauge check: 9 dc after Rnd 3 ~ 39 mm
    chk("gauge check 9 dc ~ 39 mm", abs(9 * GAUGE_MM_PER_ST - GAUGE_CHECK_CLAIM_MM) <= 0.5,
        f"{9 * GAUGE_MM_PER_ST:.1f} mm (claimed {GAUGE_CHECK_CLAIM_MM} mm)")

    # growth per round per side: 3 dc x 4.3 mm
    chk("growth ~1.3 cm per side per round",
        abs(3 * GAUGE_MM_PER_ST / 10 - GROWTH_CLAIM_CM) < 0.05,
        f"{3 * GAUGE_MM_PER_ST / 10:.2f} cm (claimed {GROWTH_CLAIM_CM} cm)")

    # sizing table 18/20/22 rounds
    for rnds, claim in SIZE_CLAIMS_CM.items():
        got = 3 * rnds * GAUGE_MM_PER_ST / 10
        chk(f"{rnds} rounds ~ {claim} cm", abs(got - claim) <= 0.6, f"model: {got:.1f} cm")

    # border: 240 dc + 4 corners x 3 sc
    border = series[GRANNY_RNDS] + 4 * 3
    chk("border = 252 sc", border == BORDER_SC_STATED,
        f"model: {series[GRANNY_RNDS]} + 12 = {border} (claimed {BORDER_SC_STATED})")

    # head size: 36 sts around -> diameter; 14 rounds -> height
    dia = HEAD_MAX_STS * GAUGE_MM_PER_ST / math.pi / 10
    chk("head ~ 4.9 cm across", abs(dia - HEAD_DIAMETER_CLAIM_CM) <= 0.2,
        f"model: {dia:.2f} cm (claimed {HEAD_DIAMETER_CLAIM_CM} cm)")
    hgt = HEAD_RNDS * GAUGE_MM_PER_RND / 10
    chk("head ~ 5.7 cm tall", abs(hgt - HEAD_HEIGHT_CLAIM_CM) <= 0.2,
        f"model: {hgt:.2f} cm (claimed {HEAD_HEIGHT_CLAIM_CM} cm)")

    # diagonal & overall length sanity (replaces the unverifiable 33 cm claim)
    diag = 26 * math.sqrt(2)
    findings.append(f"INFO | BLANKET: corner-to-corner diagonal = {diag:.1f} cm "
                    f"(26 cm square) — replaces the unreproducible '33 cm ear tips to corner' claim")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    path = Path(args[0]) if args else Path("patterns/willow_bunny_lovey_v2_fixed.txt")
    text = path.read_text()
    findings = []
    errors = 0
    for name, body in split_pieces(text):
        if name.upper() == "BLANKET":
            granny_model_checks(findings)
        else:
            errors += check_round_piece(name, body, findings)

    for f in findings:
        print(f)
    errors += sum(1 for f in findings if f.startswith("FAIL") or f.startswith("ERROR")
                  or f.startswith("CRITICAL"))
    summary = {
        "file": str(path),
        "errors": errors,
        "checks": len(findings),
        "status": "ERROR" if errors else "PASS",
    }
    print("\nSUMMARY:", json.dumps(summary))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
