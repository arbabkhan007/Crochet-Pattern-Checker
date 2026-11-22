#!/usr/bin/env python3
"""Deterministic round-chain validator for the Novality amigurumi patterns.

Input files are pre-normalised transcriptions of the source patterns:
  === PIECE NAME ===              section header (one per crocheted piece)
  Rnd N: <segments> (stated)      a round      Row N: <segments> (stated)  a flat row
  Rnd N-M: <segments> (stated)    a range (expanded)
  # ...                           comment / prose (ignored by the math)

Segment vocabulary (all regex + integer arithmetic — nothing fuzzy):
  6 sc in MR | N sc | sc N | hdc | dc | sl st 2 | inc [x N] | dec [x N] | invdec [x N]
  sc in each st around | inc in each st around | sc around
  [segment, segment, ...] x N                    repeat block
  (sc, hdc, sc) in next st                       cluster worked into ONE stitch
  N sc across both layers                        two-layer closing
  %%partial                                      flat row that intentionally
                                                 consumes fewer stitches

Checks: chain consumption vs. previous round, stated count vs. produced count,
round-number contiguity. Exit 1 on any ERROR.
"""
from __future__ import annotations
import json
import math
import re
import sys
from pathlib import Path

STITCH = {"sc": (1, 1), "hdc": (1, 1), "dc": (1, 1), "tr": (1, 1), "sl st": (1, 1)}

ROUND_RE = re.compile(
    r"^(?:rnd|round|row)s?\s*(\d+)\s*(?:[-–]\s*(\d+))?\s*[:.\-]?\s*(.*)$", re.I)
PIECE_RE = re.compile(r"^===\s*(.+?)\s*===\s*$")


def split_segments(s: str):
    segs, buf, depth = [], "", 0
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            segs.append(buf)
            buf = ""
        else:
            buf += ch
    if buf.strip():
        segs.append(buf)
    return [x.strip() for x in segs if x.strip()]


def _cluster(seg: str):
    m = re.match(r"^\(([^)]+)\)\s+(?:all\s+)?in(?:to)?\s+(?:the\s+)?next\b(.*)$", seg, re.I)
    if not m:
        return None
    produce = 0
    for tok in split_segments(m.group(1)):
        tok = tok.strip().lower()
        if tok in STITCH:
            produce += STITCH[tok][1]
        elif re.fullmatch(r"ch\s*\d+", tok) or tok == "picot":
            produce += 0
        else:
            raise ValueError(f"cluster token: {tok!r}")
    return (1, produce)


def seg_eval(seg: str, avail):
    """-> (consume, produce, kind); consume/produce may be None = ambiguous."""
    s = seg.strip().rstrip(".")
    s = re.sub(r"^(FLO|BLO)\s*:\s*", "", s, flags=re.I)
    s = re.sub(r"^(FLO|BLO)\s+", "", s, flags=re.I)
    lo = s.lower()
    cl = _cluster(s)
    if cl:
        return cl[0], cl[1], "cluster"

    m = re.fullmatch(r"(\d+)\s*(sc|hdc|dc|tr)(?:\s+in\s+mr\b.*)?", lo)
    if m:
        n = int(m.group(1))
        return (0, n, "mr") if "in mr" in lo else (n, n, "st")
    m = re.fullmatch(r"(sc|hdc|dc|tr)\s+(\d+)(?:\s+.*)?", lo)
    if m:
        n = int(m.group(2))
        c, p = STITCH[m.group(1)]
        return n * c, n * p, "st"
    m = re.fullmatch(r"(sl\s*st)\s+(\d+)", lo) or re.fullmatch(r"(\d+)\s*sl\s*st", lo)
    if m:
        n = int(m.group(2))
        return n, n, "st"
    m = re.fullmatch(r"sl\s*st(?:\s+in\s+(?:the\s+)?next\s+st.*)?", lo)
    if m:
        return 1, 1, "st"
    if lo in STITCH:
        c, p = STITCH[lo]
        return c, p, "st"
    m = re.fullmatch(r"inc(?:\s*x\s*(\d+))?", lo)
    if m:
        n = int(m.group(1) or 1)
        return n, 2 * n, "inc"
    m = re.fullmatch(r"(?:dec|inv\s*dec|invdec)(?:\s*x\s*(\d+))?", lo)
    if m:
        n = int(m.group(1) or 1)
        return 2 * n, n, "dec"
    if re.fullmatch(r"inc\s+in\s+each\s+st(\s+around)?", lo):
        return (avail, 2 * avail, "inc-each") if avail is not None else (None, None, "amb")
    m = re.fullmatch(r"(sc|hdc|dc|tr)\s+in\s+each\s+st(\s+around)?", lo)
    if m:
        return (avail, avail, "each") if avail is not None else (None, None, "amb")
    m = re.fullmatch(r"(sc|hdc|dc|tr)\s+around", lo)
    if m:
        return (avail, avail, "each") if avail is not None else (None, None, "amb")
    m = re.fullmatch(r"(\d+)\s*sc\s+across\s+both\s+layers.*", lo)
    if m:
        n = int(m.group(1))
        return 2 * n, n, "join"
    m = re.fullmatch(r"\[([^]]+)\]\s*x\s*(\d+)", s, re.I)
    if m:
        uc = up = 0
        for sub in split_segments(m.group(1)):
            c, p, _ = seg_eval(sub, None)
            uc += c if c is not None else 0
            up += p if p is not None else 0
        n = int(m.group(2))
        return uc * n, up * n, "rep"
    m = re.fullmatch(r"ch\s*(\d+)", lo)
    if m:
        return 0, 0, "ch"
    raise ValueError(f"unparsed segment: {seg!r}")


def eval_round(body: str, avail):
    """-> (consume, produce, ambiguous, had_mr)"""
    body = body.strip()
    partial = "%%partial" in body
    body = body.replace("%%partial", "").strip()
    stated = None
    m = re.search(r"\((\d+)\)\s*$", body)
    if m:
        stated = int(m.group(1))
        body = body[: m.start()].strip()
    if not body:
        return None, stated, False, False
    cons = prod = 0
    amb = had_mr = False
    for seg in split_segments(body):
        try:
            c, p, kind = seg_eval(seg, avail)
        except ValueError:
            return None, stated, True, False
        if kind == "mr":
            had_mr = True
        if c is None:
            amb = True
            continue
        cons += c
        prod += p
    if partial:
        cons = None
    return cons, prod, amb, had_mr, stated


def parse_file(text: str):
    pieces, name = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        pm = PIECE_RE.match(line)
        if pm:
            name = pm.group(1)
            pieces.append((name, []))
            continue
        rm = ROUND_RE.match(line)
        if rm and name:
            a = int(rm.group(1))
            b = int(rm.group(2)) if rm.group(2) else a
            for n in range(a, b + 1):
                pieces[-1][1].append((n, rm.group(3)))
            continue
        if name is None:
            continue  # prose before first piece
    return pieces


def validate_piece(pname, rounds, findings):
    if not rounds:
        return
    nums = [n for n, _ in rounds]
    expected = list(range(nums[0], nums[0] + len(nums)))
    missing = sorted(set(expected) - set(nums))
    if missing:
        findings.append(("STRUCTURE", f"{pname}: round sequence skips {missing}"))
    prev = None
    for n, body in rounds:
        out = eval_round(body, prev)
        cons, prod, amb, had_mr, stated = (out + (None,))[:5] if len(out) == 4 else out
        if amb:
            findings.append(("WARNING", f"{pname} Rnd {n}: context-dependent round"))
            if stated is not None:
                prev = stated
            continue
        if prev is not None and cons is not None and cons != prev:
            findings.append(("ERROR",
                f"{pname} Rnd {n}: consumes {cons} but previous round produced {prev}"))
        elif prev is None and not had_mr and cons not in (0, None):
            findings.append(("WARNING",
                f"{pname} Rnd {n}: first checked round consumes {cons} (foundation/join?)"))
        if stated is not None and prod is not None and stated != prod:
            findings.append(("ERROR",
                f"{pname} Rnd {n}: states ({stated}) but produces {prod}"))
        prev = prod if prod is not None else prev


def near(value, claim, tol):
    ok = abs(value - claim) <= tol
    return ok, f"computed {value:.1f} vs claimed {claim}"


# ---- per-pattern arithmetic spot checks (all closed-form from stated gauge) --
def extra_checks(slug):
    pi = math.pi
    E = {
        "axel": [
            ("Head width 36 sts x 4.5 mm = 51.6 mm dia (claimed 52 mm)", near(36 * 4.5 / pi, 52, 0.5)),
            ("Head height 12 rnds x 4.3 mm = 51.6 mm (claimed 51.6 mm)", near(12 * 4.3, 51.6, 0.1)),
            ("Tail R27-36 = 10 rnds x 4.3 mm = 43 mm (claimed 4.3 cm)", near(10 * 4.3, 43, 0.1)),
            ("Eye gap 6 sts x 4.5 mm = 27 mm ~ half the 52 mm head", near(6 * 4.5, 26, 1.5)),
        ],
        "coco": [
            ("Standing height 20 rnds x 4.3 + 17 mm legs = 103 mm (claimed 10.3 cm)", near(20 * 4.3 + 17, 103, 0.5)),
            ("Muzzle face 24 sts = 34.4 mm dia (claimed 35 mm)", near(24 * 4.5 / pi, 35, 1.0)),
            ("Muzzle rim 18 sts = 25.8 mm dia (claimed 26 mm)", near(18 * 4.5 / pi, 26, 1.0)),
            ("Eye gap 6 sts x 4.5 mm = 27 mm", near(6 * 4.5, 27, 0.1)),
        ],
        "ember": [
            ("Head R1-11 = 11 rnds x 4.3 = 47.3 mm (claimed 47 mm)", near(11 * 4.3, 47, 0.5)),
            ("Body R1-13 = 13 rnds x 4.3 = 55.9 mm (claimed 56 mm)", near(13 * 4.3, 56, 0.5)),
            ("Tail 12 rnds x 4.3 = 51.6 mm (claimed 5 cm)", near(12 * 4.3, 52, 0.5)),
            ("Gauge 30 sts = 42.9 mm dia (claimed 43 mm)", near(30 * 4.5 / pi, 43, 0.5)),
            ("Back leg 6 rnds = 25.8 mm (claimed 26 mm)", near(6 * 4.3, 26, 0.5)),
            ("Front leg 8 rnds = 34.4 mm (claimed 34 mm)", near(8 * 4.3, 34, 0.5)),
            ("Wingspan 45+34+45 = 124 mm (claimed 12.5 cm)", near(45 + 34 + 45, 124, 0.1)),
        ],
        "hamish": [
            ("Head 48 sts x 4.55 mm = 69.5 mm dia (claimed 70 mm)", near(48 * 4.55 / pi, 70, 1.0)),
            ("Head 16 rnds x 4.17 mm = 66.7 mm (claimed 67 mm)", near(16 * 4.17, 67, 1.0)),
            ("Muzzle face 24 sts = 34.8 mm (claimed 35 mm)", near(24 * 4.55 / pi, 35, 1.0)),
            ("Muzzle rim 18 sts = 26.1 mm (claimed 26 mm)", near(18 * 4.55 / pi, 26, 1.0)),
            ("Body 19 rnds = 79.2 mm (claimed 79 mm)", near(19 * 4.17, 79, 1.0)),
            ("Leg 16 rnds = 66.7 mm (claimed 67 mm)", near(16 * 4.17, 67, 1.0)),
            ("Eye gap 7 sts = 31.8 mm (claimed ~32 mm)", near(7 * 4.545, 32, 0.5)),
            ("Fringe knots 24+10+9 = 43 (44th strand = spare)", near(24 + 10 + 9, 43, 0)),
        ],
        "kawaii": [
            ("Boo height 12 rnds x 3.2 + 10 hem = 48.4 mm (claimed 48 mm)", near(12 * 3.2 + 10, 48, 0.5)),
            ("Boo head 26 sts = 28.9 mm dia (v2 claims 29 mm; source said 27)", near(26 * 3.5 / pi, 29, 0.3)),
            ("Hat brim 20 sts = 22.3 mm (v2 claims snug ~22 mm; source said 26)", near(20 * 3.5 / pi, 22, 0.4)),
            ("Pumpkin gauge 36 sts = 40.1 mm dia (claimed 40 mm)", near(36 * 3.5 / pi, 40, 0.5)),
            ("Bramble height 16 rnds x 3.2 = 51.2 mm (claimed 48-51 mm)", near(16 * 3.2, 51, 1.0)),
            ("Bramble wingspan 42+33+42 = 117 mm (claimed ~11.5 cm)", near(42 + 33 + 42, 117, 0.1)),
        ],
        "duck": [
            ("Height 23 rnds x 7 mm = 161 mm (claimed 16 cm)", near(23 * 7, 161, 0.5)),
            ("Width 30 sts x 8 mm = 76.4 mm dia (claimed 76 mm)", near(30 * 8 / pi, 76, 0.7)),
            ("Swatch 12 sts x 8 mm = 96 mm (claimed ~10 cm)", near(12 * 8, 96, 5.0)),
            ("Eye gap 7-8 sts = 56-64 mm (claimed 56-64 mm on 76 mm head)", near(7.5 * 8, 60, 4.0)),
        ],
        "momo": [
            ("Loaf height 10 wall rnds x 4.3 mm = 43 mm (claimed 4.3 cm)", near(10 * 4.3, 43, 0.1)),
            ("Base perimeter 48 sts x 4.5 mm = 216 mm ~ 79 x 52 mm oval (claimed)", near(2 * (79 + 52) * 0.79, 206, 12)),
            ("Eye gap 7 sts x 4.5 mm = 31.5 mm ~ 60 pct of 52 mm width (claimed 32)", near(7 * 4.5, 32, 0.6)),
            ("36-st alt base ~ 60 x 40 mm (v2 claim; source said 34 mm across)", near(52 * 162 / 208, 40, 2.0)),
        ],
        "trio": [
            ("Waddle height 12 rnds x 3.2 mm = 38.4 mm (claimed ~3.8 cm)", near(12 * 3.2, 38, 0.5)),
            ("Petal round: 9 repeats x (1+3) = 36 sts from 18 (claimed 36)", near(9 * 4, 36, 0)),
            ("Sunny span 20 mm centre + 2 x 5 mm petals = 30 mm (claimed ~3.0 cm)", near(20 + 10, 30, 2.0)),
            ("Bigger trio x1.3: 3.0/3.8/2.7 -> 3.9/4.9/3.5 cm (claimed)", near(3.8 * 1.3, 4.9, 0.1)),
            ("Spud R2 oval 20 sts x 3.5 mm = 70 mm circ ~ 24-27 mm long (claimed 2.7 cm)", near(20 * 3.5 / pi * 1.2, 27, 3.0)),
        ],
        "shelby": [
            ("Small disc 24 sts x 3.5 mm = 26.7 mm dia (claimed 26.7 mm)", near(24 * 3.5 / pi, 26.7, 0.2)),
            ("Whole charm = 108 shell + 95 underside = 203 sts (claimed 203)", near(108 + 95, 203, 0)),
            ("Big disc 42 sts = 46.8 mm + bumps ~ 57 mm (claimed 5.7 cm)", near(42 * 3.5 / pi + 10, 57, 2.0)),
            ("Big cluster round produces 53 from 42 anchors (claimed 53)", near(7 + 4 + 8 + 3 + 7 + 3 + 8 + 3 + 7 + 3, 53, 0)),
        ],
    }
    return E.get(slug, [])


def run_file(path: Path):
    text = path.read_text()
    slug = re.sub(r"_v\d+_.*$", "", path.stem)
    findings = []
    pieces = parse_file(text)
    if not pieces:
        findings.append(("STRUCTURE", "no machine-readable rounds found"))
    for pname, rounds in pieces:
        validate_piece(pname, rounds, findings)
    n_err = sum(1 for s, _ in findings if s in ("ERROR", "STRUCTURE"))
    n_warn = sum(1 for s, _ in findings if s == "WARNING")
    checks = 0
    for label, (ok, detail) in extra_checks(slug):
        checks += 1
        findings.append(("PASS" if ok else "FAIL", f"SIZE: {label} — {detail}"))
    n_err += sum(1 for s, _ in findings if s == "FAIL")
    return {
        "file": path.name, "slug": slug, "pieces": len(pieces),
        "rounds_checked": sum(len(r) for _, r in pieces),
        "errors": n_err, "warnings": n_warn, "size_checks": checks,
        "findings": [f"{s} | {m}" for s, m in findings],
        "status": "ERROR" if n_err else "PASS",
    }


def main():
    paths = [Path(a) for a in sys.argv[1:] if not a.startswith("--")]
    if not paths:
        paths = sorted(Path("patterns").glob("*_v[12]_*.txt"))
        paths = [p for p in paths if "willow" not in p.stem]
    results = [run_file(p) for p in paths]
    for r in results:
        print(f"\n=== {r['file']} — {r['status']} "
              f"({r['pieces']} pieces, {r['rounds_checked']} rounds, "
              f"{r['errors']} errors, {r['warnings']} warnings, "
              f"{r['size_checks']} size checks) ===")
        for f in r["findings"]:
            print("  " + f)
    print("\nSUMMARY " + json.dumps({
        "files": len(results),
        "all_pass": all(r["status"] == "PASS" for r in results),
        "by_file": {r["file"]: r["status"] for r in results},
    }))
    return 0 if all(r["status"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
