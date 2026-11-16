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
VOLUME = ROOT / "NovalityStore_Grand_Collection_corrected.md"


def master(n: str) -> str:
    return (ROOT / "docs" / f"ns{n}" / f"NS{n}_corrected.md").read_text(encoding="utf-8")


def row(text: str, label: str) -> list[str]:
    """Cells of the first table row whose first cell is exactly ``label``."""
    for line in text.splitlines():
        if line.startswith("|") and re.match(rf"\|\s*{re.escape(label)}\s*\|", line):
            return [c.strip() for c in line.strip().strip("|").split("|")]
    raise AssertionError(f"table row {label!r} not found")


def term_counts(term: str) -> tuple[int, int]:
    """(stitches consumed, stitches produced) for one plain term like '2 sc' or 'inc'."""
    term = term.strip().lower()
    if term in ("inc", "increase"):
        return 1, 2
    m = re.fullmatch(r"(\d+)\s*(?:sc|dc|hdc|sl st)", term)
    if m:
        return int(m.group(1)), int(m.group(1))
    if re.fullmatch(r"(?:sc|dc|hdc|sl st)", term):
        return 1, 1
    raise AssertionError(f"unparsed term {term!r}")


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
            repeats = int(m.group(2))
            for part in m.group(1).split(","):
                c, mk = term_counts(part)
                consumed += repeats * c
                made += repeats * mk
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


def test_ns04_legs_are_paired_and_evenly_spaced():
    """Both back legs join on Rnd 4, both front legs on Rnd 5, in pairs."""
    text = master("04")
    assert text.count("join BL") == 2 and text.count("join FL") == 2
    _, _, r4_made_legs, _ = leg_layout(join_row(text, "BL")[1])
    _, _, _, r5_consumed_legs = leg_layout(join_row(text, "FL")[1])

    # Rnd 4 places BOTH back legs on the ring Rnd 5 works into, a quarter apart.
    assert r4_made_legs == [(1, 3), (7, 9)]
    # Rnd 5 places BOTH front legs on the opposite quarter, a quarter apart.
    assert r5_consumed_legs == [(13, 15), (19, 21)]

    starts = [a for a, _ in r4_made_legs] + [a for a, _ in r5_consumed_legs]
    assert plain_gaps(starts, ring=24) == [3, 3, 3, 3]
    # No two legs of the same pair straddle the body: the nearest neighbour of a
    # back leg is the other back leg, six stitches away (90 degrees at 24 sts).
    for pair in (r4_made_legs, r5_consumed_legs):
        assert pair[1][0] - pair[0][0] == 6


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
    grand = VOLUME.read_text(encoding="utf-8")
    for needle in (
        "about 43 mm across at the Rnd-5 leg join (about 34 mm at Rnd 4)",
        "[2 sc, inc] x 4, join FL1: 3 sc, sc, inc, sc, join FL2: 3 sc, sc, inc, sc",
        "Stopping at 36 gives a body about 39 mm across",
        "fibre fill about 5 g (a little only",
        "star about 4.5 cm (1.75 in)",
        "lie in a flattened arc over the fabric",
    ):
        assert needle in grand, needle


def test_no_master_trips_the_both_directions_lint():
    """The engine flags the phrase 'both directions' as an ambiguous instruction."""
    for i in range(1, 18):
        n = f"{i:02d}"
        assert "both directions" not in master(n).lower(), f"NS-{n}"


# --- the generated volume --------------------------------------------------



def test_volume_has_every_part_in_order():
    vol = VOLUME.read_text(encoding="utf-8")
    heads = re.findall(r"^# Part (\d\d) of 17 — NS-(\d\d) · ", vol, flags=re.M)
    assert [c for _, c in heads] == [f"{i:02d}" for i in range(1, 18)]
    assert [n for n, _ in heads] == [f"{i:02d}" for i in range(1, 18)]


def test_every_master_body_is_embedded_verbatim():
    vol = VOLUME.read_text(encoding="utf-8")
    for i in range(1, 18):
        n = f"{i:02d}"
        body = "\n".join(master(n).splitlines()[1:]).strip("\n")
        assert body in vol, f"NS-{n} body missing or edited inside the volume"


def test_volume_ledger_is_truthful():
    vol = VOLUME.read_text(encoding="utf-8")
    # NS-14 keeps three warnings (a target size, an unproven gauge, an unchecked
    # opening); its two old dialect errors are gone and its tables are audited.
    assert "| NS-14 | Bobble Snowflake Tree Skirt | 0 / 3 | 0 / 0 | 6 / 34 |" in vol
    # ... and zero everywhere else, so the ledger must not claim otherwise
    for i in (1, 4, 6, 12, 13, 17):
        n = f"{i:02d}"
        assert re.search(rf"\| NS-{n} \| [^|]+ \| 0 / 0 \| 0 / 0 \|", vol), n


def test_ns17_collar_foundation_fits_the_neck():
    text = master("17")
    assert "ch 14 (about 6.5 cm relaxed at the pattern's worsted gauge" in text
    assert "| Row 1 | sc in 2nd ch and next 12 ch, ch 1, turn | (13) |" in text
    assert "next 20 ch" not in text and "(21)" not in text


# --- the auditor really reads printer-saver tables -------------------------

def test_audit_sees_through_the_checkbox_column():
    """NS-14's tables carry a leading tick box; the audit must still read them."""
    import sys

    sys.path.insert(0, str(ROOT / "docs" / "kit"))
    from audit_lib import audit_tables  # noqa: E402
    from audit_overrides import OVERRIDES, SKIP_TABLES  # noqa: E402

    text = master("14")
    assert "| ✓ |" in text
    problems, unparsed = audit_tables(text, OVERRIDES.get("NS-14", {}), SKIP_TABLES)
    assert problems == []
    assert unparsed == []
    # 32 = the 20 growth rounds + 12 rows that only state a count. An empty
    # result would mean the tables were skipped again, not that they passed.
    prob14, unp14 = audit_tables(text, {}, SKIP_TABLES)
    assert len(prob14) == 0


def test_every_master_audits_clean():
    import sys

    sys.path.insert(0, str(ROOT / "docs" / "kit"))
    from audit_lib import audit_tables  # noqa: E402
    from audit_overrides import OVERRIDES, SKIP_TABLES  # noqa: E402

    for i in range(1, 18):
        n = f"{i:02d}"
        problems, unparsed = audit_tables(master(n), OVERRIDES.get(f"NS-{n}", {}), SKIP_TABLES)
        assert problems == [], f"NS-{n}: {problems[:2]}"
        assert unparsed == [], f"NS-{n}: {unparsed[:2]}"


def test_ns14_carries_no_publishing_notes():
    text = master("14")
    assert "delete before publishing" not in text.lower()
    assert "Revision notes" not in text
    # the border still names its stitch totals, so the count is checkable
    assert "(168 / 276 / 384)" in text


# --- NS-16: the heel ends right side out ------------------------------------

def test_ns16_heel_finishes_right_side_out():
    """Replay the heel rows' facing; the pickup round must begin on the RS.

    A flat panel with a turn at the end of every row faces you wrong side out
    after an even number of rows, so an even panel needs one more turn (or a
    'do not turn' that leaves an odd panel) before the work goes back into the
    round. BLO ridges sit on the wrong side, so getting this wrong puts every
    ridge on the outside of the stocking.
    """
    text = master("16")
    rows = re.findall(r"^\| (Row \d+) \| ([^|]+?) \| \([^)]*\) \| ([^|]*)\|$", text, flags=re.M)
    heel = [r for r in rows if 1 <= int(r[0].split()[1]) <= 10]
    assert len(heel) == 10, heel

    facing = "RS"
    for label, instr, note in heel:
        declared = note.strip().upper()
        if declared.startswith("RS"):
            assert facing == "RS", f"{label} is marked RS but the panel is {facing} out"
        elif declared.startswith("WS"):
            assert facing == "WS", f"{label} is marked WS but the panel is {facing} out"
        if "do not turn" in instr.lower():
            break  # the flat panel ends here, still facing whatever it faced
        if re.search(r"\bturn\b\s*$", instr.strip(), flags=re.I):
            facing = "WS" if facing == "RS" else "RS"

    assert facing == "RS", "the pickup round would be worked inside out (wrong side out)"
