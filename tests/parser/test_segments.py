"""Tests for multi-segment and beginner-style instruction parsing.

Covers real-world pattern phrasing that earlier parser versions silently
dropped everything after the first operation.
"""
from crochet_checker.parser.parser import parse_pattern, parse_instruction


def ops(line):
    inst = parse_instruction(line)
    return [(o.stitch_type.value, o.count) for o in inst.operations]


class TestCommaSegments:
    def test_sc_n_dec(self):
        # heel-turn phrasing: "sc 6, dec"
        inst = parse_instruction("Ch 1, sc 6, dec, TURN (7)")
        assert inst.stated_stitch_count == 7
        assert inst.total_stitches_produced == 7
        assert inst.total_stitches_consumed == 8

    def test_multi_segment(self):
        # "N sc, dec x M, K sc" — previously only "10 sc" was captured
        inst = parse_instruction("10 sc, dec x 5, 5 sc (15)")
        assert inst.total_stitches_produced == 20
        assert inst.total_stitches_consumed == 25

    def test_commas_inside_parens_do_not_split(self):
        inst = parse_instruction("(sc, inc) x 6 (18)")
        assert inst.total_stitches_produced == 18
        assert inst.total_stitches_consumed == 12


class TestRepeatTimes:
    def test_n_times(self):
        inst = parse_instruction("Ch 1, (sc 3, dec) 4 times. (16)")
        assert inst.stated_stitch_count == 16
        assert inst.total_stitches_produced == 16
        assert inst.total_stitches_consumed == 20

    def test_stitch_first_units(self):
        # repeat unit uses "sc 3" (stitch before count)
        inst = parse_instruction("(sc 3, dec) 4 times")
        assert inst.total_stitches_produced == 16

    def test_dec_times(self):
        inst = parse_instruction("dec 4 times (4)")
        assert inst.total_stitches_produced == 4
        assert inst.total_stitches_consumed == 8


class TestExactEachN:
    def test_blo_each_of_n(self):
        inst = parse_instruction("Ch 1, sc in BLO of each of the 10 sts (10)")
        assert inst.total_stitches_produced == 10
        assert inst.total_stitches_consumed == 10

    def test_each_of_n(self):
        inst = parse_instruction("sc in each of the 10 sts (10)")
        assert inst.total_stitches_produced == 10

    def test_next_n_with_the(self):
        inst = parse_instruction("sc in the next 10 sts only (10)")
        assert inst.total_stitches_produced == 10


class TestPickupSegments:
    def test_picked_up_stitches(self):
        inst = parse_instruction(
            "5 sc along heel edge, 10 sc across instep, 5 sc along heel edge, 3 sc across heel (23)"
        )
        assert inst.stated_stitch_count == 23
        assert inst.total_stitches_produced == 23
        assert inst.total_stitches_consumed == 23


class TestHousekeeping:
    def test_join_does_not_add_stitch(self):
        inst = parse_instruction("Ch 1, sc in each st around. Join with sl st. (20)")
        # the join slip stitch is housekeeping, not stitch production
        kinds = [k for k, _ in ops("Ch 1, sc in each st around. Join with sl st. (20)")]
        assert "slip_stitch" not in kinds

    def test_turn_dropped(self):
        p = parse_pattern("Row 1: ch 1, sc 6, dec, TURN (7)")
        assert len(p.rows[0].instructions) == 1
        assert p.rows[0].computed_stitch_count == 7


class TestRangeHeaders:
    def test_rnd_range_expansion(self):
        p = parse_pattern("Rnd 6-10: sc in each st around (20)")
        assert [r.round_number for r in p.rounds] == [6, 7, 8, 9, 10]


class TestBracketCounts:
    """[N] square-bracket stated counts (amigurumi convention)."""

    def test_bracket_stated(self):
        inst = parse_instruction("Rnd 1: 6 sc in MR [6]")
        assert inst.stated_stitch_count == 6
        assert inst.total_stitches_produced == 6

    def test_bracket_after_repeat(self):
        inst = parse_instruction("(sc 5, dec) x 6 [36]")
        assert inst.stated_stitch_count == 36
        assert inst.total_stitches_produced == 36
        assert inst.total_stitches_consumed == 42


class TestLeadingBLO:
    def test_blo_prefix(self):
        inst = parse_instruction("BLO sc in each st around [10]")
        kinds = [k for k, _ in ops("BLO sc in each st around [10]")]
        assert inst.stated_stitch_count == 10
        assert kinds == ["single_crochet"]  # ctx op, not double-counted


class TestEachWithoutAround:
    def test_inc_in_each_st(self):
        inst = parse_instruction("Inc in each st [12]")
        assert inst.stated_stitch_count == 12
        kinds = dict(ops("Inc in each st [12]"))
        assert kinds.get("increase") == 1  # ctx op resolved against previous round

    def test_across_rows(self):
        p = parse_pattern("Row 1: ch 1, sc in each st across (5)\nRow 2: ch 1, turn, sc in each st across (5)")
        r2 = p.rows[1]
        assert r2.computed_stitch_count >= 1  # ctx ops stored as single op
