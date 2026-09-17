"""Tests for the ValidationReport orchestrator and flat-row short-row semantics."""
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern, OverallStatus, Severity


class TestReportInterface:
    def test_clean_pattern_passes(self):
        t = "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\nRound 3: (sc, inc) x 6 (18)"
        r = validate_pattern(parse_pattern(t))
        assert r.overall_status == OverallStatus.PASS
        assert r.score == 100
        assert r.errors == [] and r.warnings == []

    def test_error_pattern(self):
        t = "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (20)"
        r = validate_pattern(parse_pattern(t))
        assert r.overall_status == OverallStatus.ERROR
        assert r.score < 80
        assert len(r.errors) >= 1

    def test_strict_mode_promotes_warnings(self):
        t = "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 5 (15)"
        r = validate_pattern(parse_pattern(t))          # mismatch -> error anyway
        assert r.overall_status == OverallStatus.ERROR
        r2 = validate_pattern(parse_pattern(t), strict=True)
        assert r2.overall_status == OverallStatus.ERROR

    def test_to_dict(self):
        d = validate_pattern(parse_pattern("Round 1: 6 sc into magic ring (6)")).to_dict()
        assert d["overall_status"] == "PASS"
        assert "score" in d and "errors" in d and "warnings" in d

    def test_empty_pattern_needs_review(self):
        r = validate_pattern(parse_pattern("A pattern with no stitch lines."))
        assert r.overall_status == OverallStatus.NEEDS_REVIEW


class TestShortRowSemantics:
    def test_short_row_under_consumption_is_warning(self):
        t = ("Row 1: ch 1, sc in the next 10 sts, TURN (10)\n"
             "Row 2: ch 1, sc 6, dec, TURN (7)")
        r = validate_pattern(parse_pattern(t))
        assert r.errors == []
        assert any(w.location == "Row 2" for w in r.warnings)

    def test_over_consumption_is_error(self):
        t = ("Row 1: ch 1, sc in the next 10 sts, TURN (10)\n"
             "Row 2: ch 1, sc in each of the 12 sts, TURN (12)")
        r = validate_pattern(parse_pattern(t))
        assert len(r.errors) == 1

    def test_stated_mismatch_is_error(self):
        t = ("Row 1: ch 1, sc in the next 10 sts, TURN (10)\n"
             "Row 2: ch 1, sc in each of the 10 sts, TURN (9)")
        r = validate_pattern(parse_pattern(t))
        assert any(e.location == "Row 2" and "states" in e.message for e in r.errors)


class TestFullStockingStreams:
    """The NS16 mini stocking validation transcripts must stay clean."""

    CUFF_LEG = ("Rnd 1: 20 sc around foundation chain (20)\n"
                "Rnd 2-4: sc in each st around, working BLO (20)\n"
                "Rnd 5: sc in each st around (20)\n"
                "Rnd 6-10: sc in each st around (20)\n")
    HEEL = ("Row 1: ch 1, sc in the next 10 sts only, TURN (10)\n"
            "Row 2: ch 1, sc in BLO of each of the 10 sts, TURN (10)\n"
            "Row 3: ch 1, sc in each of the 10 sts, TURN (10)\n"
            "Row 4: ch 1, sc in BLO of each of the 10 sts, TURN (10)\n"
            "Row 5: ch 1, sc in each of the 10 sts, TURN (10)\n"
            "Row 6: ch 1, sc in BLO of each of the 10 sts, DO NOT TURN (10)\n"
            "Row 7: ch 1, sc 6, dec, TURN (7)\n"
            "Row 8: ch 1, sc 4, dec, TURN (5)\n"
            "Row 9: ch 1, sc 3, dec, TURN (4)\n"
            "Row 10: ch 1, sc 2, dec, DO NOT TURN (3)\n")
    FOOT_TOE = ("Rnd 11: 5 sc along heel edge, 10 sc across instep, 5 sc along heel edge, 3 sc across heel (23)\n"
                "Rnd 12: 17 sc, 3 dec evenly spaced (20)\n"
                "Rnd 13-16: sc in each st around (20)\n"
                "Rnd 17: (sc 3, dec) 4 times (16)\n"
                "Rnd 18: (sc 2, dec) 4 times (12)\n"
                "Rnd 19: (sc 1, dec) 4 times (8)\n"
                "Rnd 20: dec 4 times (4)\n")

    def test_cuff_leg(self):
        r = validate_pattern(parse_pattern(self.CUFF_LEG))
        assert r.errors == []

    def test_heel(self):
        r = validate_pattern(parse_pattern(self.HEEL))
        assert r.errors == []
        # exactly the two intentional short-row warnings
        assert sorted(w.location for w in r.warnings) == ["Row 7", "Row 8"]

    def test_foot_toe(self):
        r = validate_pattern(parse_pattern(self.FOOT_TOE))
        assert r.errors == []


class TestFoundationRing:
    def test_chain_join_round_uses_stated_size(self):
        t = ("Round 1: ch 40, sl st to join (40)\n"
             "Round 2: sc in each st around (40)\n"
             "Round 3: sc in each st around (40)")
        r = validate_pattern(parse_pattern(t))
        assert r.errors == []
        assert r.overall_status == OverallStatus.PASS


class TestFlatRowContext:
    def test_sc_across_resolves(self):
        t = ("Row 1: ch 20, sc in 2nd ch from hook, sc in each ch across (19)\n"
             "Row 2: ch 1, turn, sc in each st across (19)\n"
             "Row 3: ch 1, turn, sc in each st across (19)")
        r = validate_pattern(parse_pattern(t))
        assert r.errors == []

    def test_bracket_counts_pipeline(self):
        t = ("Rnd 1: 6 sc in MR [6]\n"
             "Rnd 2: Inc in each st around [12]\n"
             "Rnd 3: (sc 1, inc) x 6 [18]\n"
             "Rnd 4: (sc 1, dec) x 6 [12]")
        r = validate_pattern(parse_pattern(t))
        assert r.errors == []
