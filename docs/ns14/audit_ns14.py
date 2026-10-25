"""Independent audit of the NS 14 growth ladder.

Extracts the US-terms column from the pasted construction table and checks it
against the pattern's own stated rule:

    Round N consumes N-1 old stitches and produces N new stitches in each of
    12 repeats -> the round ends with exactly 12 x N stitches.

It also re-derives the border scallop counts and the gauge/diameter arithmetic.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/ns14_original.txt")
text = SRC.read_text(encoding="utf-8")

# PDF text extraction glued some tokens together ("2 dcin next st", "slst",
# "x12", "against thestand"). Re-open the joins that matter for counting.
for a, b in (
    ("dcin", "dc in"), ("trin", "tr in"), ("slst", "sl st"), ("sl stto", "sl st to"),
    ("BOin", "BO in"), ("scin", "sc in"), ("innext", "in next"),
    ("nextst", "next st"), ("eachst", "each st"), ("inst", "in st"),
):
    text = re.sub(rf"\b{a}\b", b, text, flags=re.IGNORECASE)
text = re.sub(r"([a-z])(\bx\s*\d+\b)", r"\1 \2", text, flags=re.IGNORECASE)
text = re.sub(r"\bx\s*(\d+)\b", r"x \1", text, flags=re.IGNORECASE)

# ---------------------------------------------------------------- extraction
# Table rows look like:
#   [ ] R12  Ch 2, [dc in next 10 sts, 2 dc in next st] x12, sl st to first dc
#            Ch 2, [tr in next 10 sts, ...] (144)  <note>
ROW = re.compile(r"\[\s*\]\s*R(\d+)(.+)", re.IGNORECASE)

rows: dict[int, dict] = {}
for line in text.splitlines():
    m = ROW.search(line)
    if not m:
        continue
    n = int(m.group(1))
    rest = m.group(2)
    # US column = everything before the second "Ch 2"
    parts = re.split(r"Ch\s*2\s*,", rest, flags=re.IGNORECASE)
    us = parts[1] if len(parts) > 1 else rest
    # cut the US column where the UK column starts (it uses "tr in")
    us = re.split(r"Ch\s*2\s*,\s*\[?\s*(?:BO in next st,\s*)?tr\b", us, flags=re.IGNORECASE)[0]
    us = re.sub(r"\s+", " ", us).strip()
    stated = re.search(r"\((\d+)\)", rest)
    rows[n] = {
        "us": us,
        "stated": int(stated.group(1)) if stated else None,
        "raw": re.sub(r"\s+", " ", line).strip(),
    }

# ------------------------------------------------------- per-repeat analysis
BOBBLE = re.compile(r"BO\s+in\s+next\s+st", re.IGNORECASE)
PLAIN = re.compile(r"(?<!2 )\bdc\s+in\s+next\s+(\d+)\s+sts?", re.IGNORECASE)
PLAIN_ONE = re.compile(r"(?<!2 )\bdc\s+in\s+next\s+st\b(?!\s*s)", re.IGNORECASE)
INC = re.compile(r"2\s+dc\s+in\s+next\s+st", re.IGNORECASE)
REPEATS = re.compile(r"[x×]\s*(\d+)", re.IGNORECASE)

print(f"Source: {SRC}")
print(f"Rows extracted: {len(rows)}  (R{min(rows)}-R{max(rows)})\n")
print(f"{'Rnd':>4} {'bob':>3} {'plain':>5} {'inc':>3} {'reps':>4} "
      f"{'consumed':>8} {'produced':>8} {'x reps':>7} {'stated':>7}  verdict")
print("-" * 96)

problems: list[str] = []
for n in sorted(rows):
    us = rows[n]["us"]
    stated = rows[n]["stated"]
    reps = int(REPEATS.search(us).group(1)) if REPEATS.search(us) else None

    if n == 1:
        # "12 dc in ring"
        consumed, produced = 0, 12
        bob, plain, inc = 0, 0, 0
        detail = "12 dc into the ring; no old stitches"
        ok = (stated == 12)
        print(f"{n:>4} {bob:>3} {plain:>5} {inc:>3} {reps or '-':>4} "
              f"{consumed:>8} {produced:>8} {produced:>7} {stated:>7}  "
              f"{'OK' if ok else 'MISMATCH'}  ({detail})")
        if not ok:
            problems.append(f"R{n}: stated {stated}, ring round should make 12")
        continue

    if n == 2:
        bob, plain, inc = 0, 0, 0
        consumed, produced = 1, 2          # 2 dc in each st
        ok = (stated == 24)
        print(f"{n:>4} {bob:>3} {'each':>5} {inc:>3} {'12':>4} "
              f"{consumed:>8} {produced:>8} {24:>7} {stated:>7}  "
              f"{'OK' if ok else 'MISMATCH'}  (2 dc in each of 12 sts)")
        if not ok:
            problems.append(f"R{n}: stated {stated}, doubling 12 gives 24")
        continue

    bob = 1 if BOBBLE.search(us) else 0
    pm = PLAIN.search(us)
    if pm:
        plain = int(pm.group(1))
    elif PLAIN_ONE.search(us):
        plain = 1          # "dc in next st" = one plain dc
    else:
        plain = None
    inc = 1 if INC.search(us) else 0

    if plain is None:
        problems.append(f"R{n}: could not read a plain-dc count from '{us}'")
        print(f"{n:>4} {bob:>3} {'?':>5} {inc:>3} {reps or '-':>4}  UNREADABLE: {us}")
        continue

    # per repeat: BO consumes 1 makes 1; each plain dc consumes 1 makes 1;
    # the increase anchor consumes 1 makes 2
    consumed = bob + plain + inc
    produced = bob + plain + 2 * inc
    total = produced * (reps or 12)
    old_total = (rows[n - 1]["stated"] or 0) if n - 1 in rows else None

    expected_consumed = n - 1
    expected_produced = n
    ok = True
    notes = []
    if reps != 12:
        ok = False
        notes.append(f"repeat count is {reps}, rule says 12")
    if consumed != expected_consumed:
        ok = False
        notes.append(f"consumes {consumed} old sts/repeat, rule says {expected_consumed}")
    if produced != expected_produced:
        ok = False
        notes.append(f"produces {produced} new sts/repeat, rule says {expected_produced}")
    if old_total is not None and consumed * (reps or 12) != old_total:
        ok = False
        notes.append(f"consumes {consumed * (reps or 12)} of {old_total} available sts "
                     f"-> {old_total - consumed * (reps or 12)} left unworked")
    if stated != total:
        ok = False
        notes.append(f"stated ({stated}) != computed {total}")

    print(f"{n:>4} {bob:>3} {plain:>5} {inc:>3} {reps:>4} "
          f"{consumed:>8} {produced:>8} {total:>7} {stated:>7}  "
          f"{'OK' if ok else 'ERROR'}" + ("" if ok else "  <- " + "; ".join(notes)))
    if not ok:
        problems.append(f"R{n}: " + "; ".join(notes))

# --------------------------------------------------- bobble-round cadence
bobble_rounds = sorted(n for n in rows if n > 2 and BOBBLE.search(rows[n]["us"]))
print(f"\nBobble rounds found: {bobble_rounds}")
print(f"Gaps: {[b - a for a, b in zip(bobble_rounds, bobble_rounds[1:])]}")
print(f"Covered by 'every third round from R5': {list(range(5, 33, 3))}")
if bobble_rounds != list(range(5, 33, 3)):
    problems.append(f"bobble cadence {bobble_rounds} != every 3rd round from R5")

# ------------------------------------------------------------- size stops
for stop, want in ((14, 168), (23, 276), (32, 384)):
    got = rows.get(stop, {}).get("stated")
    scallops = (got / 6) if got else None
    ok = got == want and scallops == int(scallops)
    print(f"Size stop R{stop}: stated {got} (target {want}), scallops {scallops} "
          f"-> {'OK' if ok else 'ERROR'}")
    if not ok:
        problems.append(f"R{stop} size stop: stated {got}, expected {want}, divisible by 6")

# ------------------------------------------------------- gauge / diameter
print("\nGauge-derived diameters (12 sts = 4 in -> 3 sts/in):")
for stop in (14, 23, 32):
    sts = rows[stop]["stated"]
    circ = sts / 3
    diam_in = circ / 3.141592653589793
    print(f"  R{stop}: {sts} sts -> {circ:.0f} in circumference -> "
          f"{diam_in:.1f} in / {diam_in * 2.54:.0f} cm diameter")

print("\n" + "=" * 96)
if problems:
    print(f"{len(problems)} PROBLEM(S) FOUND")
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("No arithmetic problems found.")
