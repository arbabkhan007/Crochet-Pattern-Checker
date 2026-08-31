"""Tests for utilities."""
from crochet_checker.parser import CrochetParser
from crochet_checker.utils import estimate_yarn, track_progress

PATTERN = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: inc x 6 (12)" + chr(10) + "Round 3: (sc, inc) x 6 (18)"

class TestYarnCalc:
    def test_estimate(self):
        est = estimate_yarn(CrochetParser().parse(PATTERN))
        assert est.total_yards > 0 and est.confidence in ["low","medium","high"]
    def test_weights(self):
        p = CrochetParser().parse(PATTERN)
        assert estimate_yarn(p, yarn_weight="bulky").total_yards > estimate_yarn(p, yarn_weight="worsted").total_yards
    def test_skeins(self):
        assert estimate_yarn(CrochetParser().parse(PATTERN)).skeins_needed > 0

class TestProgress:
    def test_create(self):
        t = track_progress(CrochetParser().parse(PATTERN))
        assert t.total_rounds == 3 and t.get_percentage() == 0
    def test_complete(self):
        t = track_progress(CrochetParser().parse(PATTERN))
        assert t.complete_round(1) and t.get_percentage() > 0 and t.get_current_round() == 2
    def test_uncomplete(self):
        t = track_progress(CrochetParser().parse(PATTERN))
        t.complete_round(1)
        assert t.uncomplete_round(1) and t.get_percentage() == 0
    def test_note(self):
        t = track_progress(CrochetParser().parse(PATTERN))
        t.add_note("Test")
        assert len(t.notes) == 1
    def test_summary(self):
        t = track_progress(CrochetParser().parse(PATTERN))
        t.complete_round(1)
        assert "1/3" in t.get_summary()
