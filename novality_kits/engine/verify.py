"""Deterministic stitch-count verification of every rounds table in every pattern data file.

Run:  python engine/verify.py            (all patterns)
      python engine/verify.py coco ember (subset)
Exit code 1 if any round fails. Run before every build / publish.

Arithmetic: sc/hdc/dc/sl st 1->1, inc 1->2, dec/invdec 2->1, (k sts) in next st 1->k, [..] x N multiplies both,
"sc in each st around" consumes and produces the previous count. Every round must consume exactly the previous
round's count and produce exactly the stated count.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import SLUGS, load_pattern  # noqa: E402


def _split_top(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "[(": depth += 1
        if ch in "])": depth -= 1
        if ch == "," and depth == 0: out.append(cur); cur = ""
        else: cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def _shell(s):
    return sum(1 for t in re.split(r"[,\s]+", s.strip()) if t)


def ev(seg, prev):
    s = seg.strip().lower().rstrip("*").strip()
    s = re.sub(r"\s*\(\d+ rnds?\)$", "", s)
    if m := re.fullmatch(r"(\d+) sc in mr", s): return (0, int(m[1]))
    if s == "inc in each st around": return (prev or 0, 2 * (prev or 0))
    if s in ("sc in each st around", "sc around", "sc in each st around, then fo"): return (prev or 0, prev or 0)
    if m := re.fullmatch(r"\[(.*)\]\s*x\s*(\d+)", s):
        c = p = 0
        for sub in _split_top(m[1]):
            cc, pp = ev(sub, None); c += cc; p += pp
        return (c * int(m[2]), p * int(m[2]))
    if m := re.fullmatch(r"\((.*)\)\s*(?:all )?in (?:the )?next(?: st)?", s): return (1, _shell(m[1]))
    if m := re.fullmatch(r"(\d+)\s*sc in (?:the )?last(?: ch| loop)?", s): return (1, int(m[1]))
    if s == "sc in 2nd ch": return (1, 1)
    if m := re.fullmatch(r"(sc|hdc|dc|sl st) in (?:the )?(?:next|first|last)?\s*(\d+)", s): return (int(m[2]), int(m[2]))
    if m := re.fullmatch(r"(\d+)\s*(sc|hdc|dc|sl st)(\*)?", s): return (int(m[1]), int(m[1]))
    if m := re.fullmatch(r"(sc|hdc|dc|sl st)\s*(\d+)", s): return (int(m[2]), int(m[2]))
    if s in ("sc", "hdc", "dc", "sl st", "sl st in next st"): return (1, 1)
    if m := re.fullmatch(r"inc\s*x\s*(\d+)", s): return (int(m[1]), 2 * int(m[1]))
    if s == "inc": return (1, 2)
    if m := re.fullmatch(r"(dec|invdec)\s*x\s*(\d+)", s): return (2 * int(m[2]), int(m[2]))
    if s in ("dec", "invdec"): return (2, 1)
    if s.startswith("other side:"): return ev(s.split(":", 1)[1], prev)
    if s.startswith("then "): return ev(s[5:], prev)
    raise ValueError(f"cannot evaluate {seg!r}")


def eval_instr(instr, prev):
    s = instr.strip()
    s = re.sub(r"^(FLO|BLO)\s*:?\s*", "", s, flags=re.I)
    s = re.sub(r"^join [a-z]+ with a sl st into any st of rnd \d+, then\s*", "", s, flags=re.I)
    s = s.replace("; other side:", ",")
    s = re.sub(r",\s*then FO$", "", s, flags=re.I)
    c = p = 0
    for seg in _split_top(s):
        cc, pp = ev(seg, prev); c += cc; p += pp
    return c, p


SPECIAL_START = {"Petal": 18}   # Sunny's petal row is worked into Rnd 3 (18)
FRESH = ("R1", "Row 1", "Petal")


def check_table(tbl, out, carry=None):
    prev, ok, n = carry, True, 0
    for label, instr, cnt, note in tbl["rounds"]:
        if label.lower().startswith("found"):
            prev = ("chain", instr); continue
        if isinstance(cnt, str) or tbl["heading"].startswith("Total dc"):
            prev = cnt if isinstance(cnt, int) else prev; continue
        n += 1
        start = SPECIAL_START.get(label, prev)
        try:
            c, p = eval_instr(instr, None if isinstance(start, tuple) else start)
        except ValueError as e:
            out.append(f"    ?? {label:6} {instr!r}: {e}"); ok = False; prev = cnt; continue
        problems = []
        if isinstance(start, tuple):
            pass                                   # first round on a foundation chain: production check only
        elif start is not None and c != start:
            problems.append(f"consumes {c} but previous round has {start}")
        if p != cnt: problems.append(f"produces {p} but table states {cnt}")
        if problems:
            ok = False; out.append(f"    !! {label:6} {instr:60} {'; '.join(problems)}")
        prev = cnt
    return ok, n


def verify(slug, quiet=False):
    P = load_pattern(slug); lines = []; rounds_here = 0; bad = 0; last = None
    for sec in P["sections"]:
        for tbl in sec.get("tables", []):
            first = tbl["rounds"][0][0]
            carry = last if (first not in FRESH and not first.lower().startswith("found")) else None
            ok, n = check_table(tbl, lines, carry); rounds_here += n
            if not ok: bad += 1
            last = next((r[2] for r in reversed(tbl["rounds"]) if isinstance(r[2], int)), last)
    if not quiet:
        print(f"[{'OK ' if not lines else 'ERR'}] {P['title']:34} {rounds_here:3} rounds")
        for l in lines: print(l)
    return rounds_here, bad


def main(slugs):
    total, bad = 0, 0
    for slug in slugs:
        r, b = verify(slug); total += r; bad += b
    print(f"\n{total} rounds checked across {len(slugs)} patterns; tables with problems: {bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or SLUGS))
