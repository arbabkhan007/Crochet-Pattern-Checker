"""Tests for measurements."""
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.visualization.measurements import StitchDimensions, measure_pattern

class TestStitchDimensions:
    def test_default(self):
        d = StitchDimensions(); assert d.width_mm > 0; assert d.height_mm > 0
    def test_from_gauge(self):
        d = StitchDimensions.from_gauge(16, 16); assert abs(d.width_mm - 6.35) < 0.1
    def test_worsted(self):
        assert StitchDimensions.for_worsted().width_mm == 6.0

class TestMeasureEngine:
    def test_measure_circle(self):
        t = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (18)" + chr(10) + "Round 3: (2 sc, inc) x 6 (24)"
        m = measure_pattern(parse_pattern(t))
        assert m.total_rounds == 3; assert m.max_stitch_count == 24; assert m.max_radius_mm > 0
    def test_radius_increases(self):
        t = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (18)" + chr(10) + "Round 3: (2 sc, inc) x 6 (24)"
        m = measure_pattern(parse_pattern(t))
        radii = [rm.radius_mm for rm in m.round_measurements]
        assert radii[0] < radii[1] < radii[2]
    def test_inches(self):
        t = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (18)"
        m = measure_pattern(parse_pattern(t))
        assert m.max_radius_inches > 0
