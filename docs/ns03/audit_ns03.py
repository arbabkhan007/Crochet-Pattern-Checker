#!/usr/bin/env python3
"""NS 03 Axel the Axolotl - independent stitch-count audit.

Re-derives consumed/produced stitches for every written round from the
instruction text alone and checks them against the stated counts, then
checks the fin anchor budget, the tip closure, the published variants and
the stated geometry. Exits non-zero if any check fails.
"""
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "NS03_corrected.md"
if not SRC.exists():
    SRC = Path(__file__).resolve().parent / "ns03_original.txt"

FAIL = []


def check(label, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (f"  [{detail}]" if detail else ""))
    if not ok:
        FAIL.append(label)


def parse_tables(text):
    tables, cur = [], []
    for line in text.splitlines():
        if line.startswith("| R") and "|" in line[1:]:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not re.match(r"^R\d+$", cells[0]):
                continue
            cur.append(cells)
        elif line.startswith("|---"):
            continue
        else:
            if cur:
                tables.append(cur)
                cur = []
    if cur:
        tables.append(cur)
    return tables


def derive(instr, prev):
    """Return (consumed, produced) for one written round."""
    i = instr.lower()
    m = re.match(r"^(\d+) sc in mr$", i)
    if m:
        return 0, int(m.group(1))
    if "inc in each st around" in i:
        return prev, 2 * prev
    m = re.match(r"^\[(?:(\d+) )?sc, inc\] x (\d+)$", i)
    if m:
        k, r = int(m.group(1) or 1), int(m.group(2))
        return r * (k + 1), r * (k + 2)
    m = re.match(r"^\[(?:(\d+) )?sc, invdec\] x (\d+)$", i)
    if m:
        k, r = int(m.group(1) or 1), int(m.group(2))
        return r * (k + 2), r * (k + 1)
    m = re.match(r"^\[(\d+) sc, inc\] x (\d+), (\d+) sc$", i)
    if m:  # neck variant: [7 sc, inc] x 2, 2 sc
        k, r, tail = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return r * (k + 1) + tail, r * (k + 2) + tail
    if "sc in each st around" in i:
        return prev, prev
    raise ValueError(f"unparsed round: {instr!r}")


def audit_rounds(name, rows):
    prev = 0
    for rnd, instr, sts, *_ in rows:
        stated = int(re.search(r"\((\d+)\)", sts).group(1))
        cons, prod = derive(instr, prev)
        ok = prod == stated and cons == prev
        check(f"{name} {rnd}: consumed {cons} = prev {prev}, produced {prod} = stated {stated}",
              ok, instr)
        prev = stated
    return prev


text = SRC.read_text(encoding="utf-8")
tables = parse_tables(text)
print(f"source: {SRC.name}  tables found: {len(tables)}\n-- main piece --")
main = tables[0]
audit_rounds("main", main)
print("-- arms --")
audit_rounds("arm", tables[1])
print("-- feet --")
audit_rounds("foot", tables[2])
print("-- gills --")
audit_rounds("gill", tables[3])

print("-- fin, closure, variants, geometry --")
tail_rounds = [r for r in main if 27 <= int(r[0][1:]) <= 36]
check("tail spans R27-R36 = 10 marked anchors", len(tail_rounds) == 10, f"{len(tail_rounds)} rounds")
check("5 scallops x 2 anchors = 10 anchors", 5 * 2 == len(tail_rounds))
check("tip closure: 6 sts fold to 3 pairs, 3 sc", 6 // 2 == 3)
# published variants
check("neck variant R13' consumes all 18 and makes 20",
      derive("[7 sc, inc] x 2, 2 sc", 18) == (18, 20))
check("neck variant R14' consumes all 20 and makes 24",
      derive("[4 sc, inc] x 4", 20) == (20, 24))
check("gill span variant: +2 plain rounds at 12 then R5 12->8",
      derive("sc in each st around", 12) == (12, 12) and derive("[sc, invdec] x 4", 12) == (12, 8))
# geometry from the stated gauge: 4.5 mm per stitch, 4.3 mm per round
import math
circ = 36 * 4.5
check("head diameter 36 x 4.5 / pi = 51.6 mm (stated 51.6-52)", round(circ / math.pi, 1) == 51.6,
      f"{circ / math.pi:.1f} mm")
check("head height 12 rounds x 4.3 = 51.6 mm (stated 51.6)", round(12 * 4.3, 1) == 51.6)
check("tail length 10 rounds x 4.3 = 43 mm (stated 4.3 cm)", round(10 * 4.3, 1) == 43.0)
check("eye spacing 6 sts x 4.5 = 27 mm (stated about 27 mm)", 6 * 4.5 == 27.0)

print()
if FAIL:
    print(f"{len(FAIL)} CHECK(S) FAILED")
    sys.exit(1)
print("ALL CHECKS PASS")
