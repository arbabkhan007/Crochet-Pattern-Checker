"""Lock the round-3 prose and geometry corrections in the 17 NS masters.

Stdlib only, so these run without the engine's pydantic/PDF stack:

    python3 -m pytest tests/test_ns_prose_figures.py -q

Each assertion re-derives the figure it guards. The derivations themselves are
written out in docs/reviews/GRAND_COLLECTION_ROUND_3_REVIEW.md.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAND = ROOT / "NovalityStore_Grand_Collection.md"


def master(n: str) -> str:
    return (ROOT / "docs" / f"ns{n}" / f"NS{n}_corrected.md").read_text(encoding="utf-8")


def row(text: str, label: str) -> list[str]:
    """Cells of the first table row whose first cell is exactly ``label``."""
    for line in text.splitlines():
        if line.startswith("|") and re.match(rf"\|\s*{re.escape(label)}\s*\|", line):
            return [c.strip() for c in line.strip().strip("|").split("|")]
    raise AssertionError(f"table row {label!r} not found")


def join_row(text: str, which: str) -> list[str]:
    """Cells of the row that joins the back or front legs (NS-04 has several R4 rows)."""
    for line in text.splitlines():
        if line.startswith("|") and f"join {which}" in line:
            return [c.strip() for c in line.strip().strip("|").split("|")]
    raise AssertionError(f"no row joining {which}")


def split_terms(instr: str) -> list[str]:
    """Split on commas that are not inside [] so '[sc, inc] x 3' stays one term."""
    terms, depth, buf = [], 0, ""
    for ch in instr:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            terms.append(buf)
            buf = ""
        else:
            buf += ch
    terms.append(buf)
    return [t.strip() for t in terms if t.strip()]


def leg_layout(instr: str) -> tuple[int, int, list[tuple[int, int]], list[tuple[int, int]]]:
    """Replay a leg-join row.

    Returns (consumed, made, legs_by_made_position, legs_by_consumed_position) where
    each leg is the half-open ``(first, last)`` stitch range it is worked over.
    """
    consumed = made = 0
    made_legs: list[tuple[int, int]] = []
    consumed_legs: list[tuple[int, int]] = []
    for raw in split_terms(instr):
        term = raw.lower()
        if not term:
            continue
        m = re.fullmatch(r"join\s+(?:bl|fl)\d*\s*:\s*(\d+)\s*sc", term)
        if m:
            n = int(m.group(1))
            consumed_legs.append((consumed + 1, consumed + n))
            made_legs.append((made + 1, made + n))
            consumed += n
            made += n
            continue
        m = re.fullmatch(r"\[(.+?)\]\s*x\s*(\d+)", term)
        if m:
            body = [t.strip() for t in m.group(1).split(",")]
            repeats = int(m.group(2))
            consumed += repeats * sum(1 for _ in body)
            made += repeats * sum(2 if t.startswith("inc") else 1 for t in body)
            continue
        m = re.fullmatch(r"inc\s*x\s*(\d+)", term)
        if m:
            consumed += int(m.group(1))
            made += 2 * int(m.group(1))
            continue
        if term.startswith("inc"):
            consumed += 1
            made += 2
            continue
        m = re.fullmatch(r"(\d+)\s*sc", term)
        if m:
            consumed += int(m.group(1))
            made += int(m.group(1))
            continue
        if term == "sc":
            consumed += 1
            made += 1
            continue
        raise AssertionError(f"unparsed term {raw!r} in {instr!r}")
    return consumed, made, made_legs, consumed_legs


def plain_gaps(leg_starts: list[int], ring: int, leg_width: int = 3) -> list[int]:
    """Plain stitches between each neighbouring pair of legs around the ring."""
    starts = sorted(leg_starts)
    gaps = []
    for i, start in enumerate(starts):
        nxt = starts[(i + 1) % len(starts)]
        span = (nxt - start) % ring or ring
        gaps.append(span - leg_width)
    return gaps


# --- NS-04: the leg geometry ------------------------------------------------


def test_ns04_join_rows_still_add_up():
    text = master("04")
    assert leg_layout(join_row(text, "BL")[1])[:2] == (18, 24)
    assert leg_layout(join_row(text, "FL")[1])[:2] == (24, 30)


def test_ns04_four_legs_form_a_square():
    text = master("04")
    _, _, r4_made_legs, _ = leg_layout(join_row(text, "BL")[1])
    _, _, _, r5_consumed_legs = leg_layout(join_row(text, "FL")[1])

    # Rnd 4 places the back legs on the ring Rnd 5 works into.
    assert r4_made_legs == [(1, 3), (13, 15)]
    # Rnd 5 places the front legs half a body apart from them.
    assert r5_consumed_legs == [(7, 9), (19, 21)]

    starts = [a for a, _ in r4_made_legs] + [a for a, _ in r5_consumed_legs]
    assert plain_gaps(starts, ring=24) == [3, 3, 3, 3]


def test_ns04_width_follows_from_its_own_gauge():
    text = master("04")
    assert "4.5 mm per stitch" in text  # the gauge line says 36 sc = 52 mm
    assert "about 43 mm across at the Rnd-5 leg join (about 34 mm at Rnd 4)" in text
    assert "65 mm across and 29 mm front to back" not in text


# --- the other corrected prose figures -------------------------------------


def test_ns06_base_width():
    text = master("06")
    assert "Stopping at 36 gives a body about 39 mm across" in text
    assert "about 34 mm across" not in text


def test_ns12_stuffing_matches_a_little_only():
    text = master("12")
    assert "fibre fill about 5 g (a little only" in text
    assert "about 25 g" not in text


def test_ns13_star_size():
    text = master("13")
    assert "star about 4.5 cm (1.75 in)" in text
    assert "9 cm (3.5 in)" not in text
    # snowflake claim is achievable and must stay
    assert "snowflake about 10 cm (4 in)" in text


def test_ns14_cover_brand_matches_the_others():
    first = master("14").splitlines()[0]
    assert first == "# NOVALITY STORE — PRINTER-SAVER EDITION"
    # the studio stays credited as the designer
    assert "Novality Crochet Studio" in master("14")


# --- the compiled volume stays in sync -------------------------------------


def test_grand_collection_carries_the_corrections():
    grand = GRAND.read_text(encoding="utf-8")
    for needle in (
        "about 43 mm across at the Rnd-5 leg join (about 34 mm at Rnd 4)",
        "[sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc",
        "Stopping at 36 gives a body about 39 mm across",
        "fibre fill about 5 g (a little only",
        "star about 4.5 cm (1.75 in)",
        "# NOVALITY STORE — PRINTER-SAVER EDITION",
    ):
        assert needle in grand, needle


def test_no_master_trips_the_both_directions_lint():
    """The engine flags the phrase 'both directions' as an ambiguous instruction."""
    for i in range(1, 18):
        n = f"{i:02d}"
        assert "both directions" not in master(n).lower(), f"NS-{n}"
