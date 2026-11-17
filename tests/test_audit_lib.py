"""Regression tests for docs/kit/audit_lib.py.

The important case is the printable tick-box column: NS-14's construction table
starts every row with `[ ]`, and the auditor used to skip those rows entirely,
which made a 34-row ladder look audited when only 4 rows had been read.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "docs" / "kit"))
sys.path.insert(0, str(ROOT / "docs" / "kit"))

import audit_lib  # noqa: E402

TABLE_HEAD = (
    "| ✓ | Rnd | US terms | UK terms | Sts | Note |\n"
    "|---|---|---|---|---|---|\n"
)


def _ns14_rows(last_count="(36)"):
    # rows copied verbatim from NS-14, tick-box column included
    return TABLE_HEAD + (
        "| [ ] | Ring | Ch 20, check the relaxed ring against the stand, then sl st to first ch without twisting | Ch 20, check the relaxed ring against the stand, then sl st to first ch without twisting | – | |\n"
        "| [ ] | R1 | Ch 2, 12 dc in ring, sl st to first dc | Ch 2, 12 tr in ring, sl st to first tr | (12) | |\n"
        "| [ ] | R2 | Ch 2, 2 dc in each st around, sl st to first dc | Ch 2, 2 tr in each st around, sl st to first tr | (24) | |\n"
        f"| [ ] | R3 | Ch 2, [dc in next st, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next st, 2 tr in next st] x 12, sl st to first tr | {last_count} | |\n"
    )


def test_checkbox_column_is_read_past():
    problems, unparsed = audit_lib.audit_tables(_ns14_rows())
    assert problems == []
    # the ring is the only count-free row; R1-R3 must have been read
    assert [u[0] for u in unparsed] == ["Ring"]


def test_checkbox_column_still_catches_a_wrong_count():
    problems, _ = audit_lib.audit_tables(_ns14_rows("(37)"))
    assert problems, "a wrong stated count must be reported"


@pytest.mark.parametrize(
    "seq,prev,expected",
    [
        ("Ch 2, 2 dc in each st around, sl st to first dc", 12, (24, 12)),
        ("Ch 2, [dc, inc] x 6, sl st to first dc", 12, (18, 12)),
        ("Ch 2, 12 dc in each st around", None, (None, None)),
    ],
)
def test_repeat_ladder(seq, prev, expected):
    made, required = audit_lib._sim_repeat_ladder(seq, prev)
    assert (made, required) == expected


def test_border_repeat_divides_or_refuses():
    border = ("join cc in any st; ch 1, [sc in next st, skip 2 sts, 5 dc in next st, "
              "skip 2 sts] around, sl st to first sc, fo")
    assert audit_lib._sim_repeat_ladder(border, 168) == (168, 168)
    # 170 is not divisible by the 6-stitch repeat: the ladder declines, so the
    # row is reported as unparsed rather than silently accepted
    assert audit_lib._sim_repeat_ladder(border, 170) is None


def test_ns14_ladder_is_fully_audited():
    master = (ROOT / "docs" / "ns14" / "NS14_corrected.md").read_text(encoding="utf-8")
    problems, unparsed = audit_lib.audit_tables(master, None, ())
    assert problems == []
    labels = [u[0] for u in unparsed]
    # the foundation ring and the "around" border carry no countable input
    assert labels == ["Ring", "Border"], labels
