"""Tests for visualization."""
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern
from crochet_checker.visualization import generate_circle_diagram, generate_stitch_count_chart, generate_crochet_chart, render_2d_preview, measure_pattern
T = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (18)" + chr(10) + "Round 3: (2 sc, inc) x 6 (24)"

class TestCircleDiagram:
    def test_valid_svg(self):
        svg = generate_circle_diagram(parse_pattern(T))
        assert svg.startswith("<svg"); assert svg.strip().endswith("</svg>")
    def test_has_labels(self):
        svg = generate_circle_diagram(parse_pattern(T))
        assert "R1" in svg; assert "R2" in svg

class TestStitchCountChart:
    def test_valid_svg(self):
        svg = generate_stitch_count_chart(parse_pattern(T))
        assert svg.startswith("<svg")
    def test_has_counts(self):
        svg = generate_stitch_count_chart(parse_pattern(T))
        assert ">6<" in svg; assert ">18<" in svg

class TestCrochetChart:
    def test_valid_svg(self):
        svg = generate_crochet_chart(parse_pattern(T))
        assert svg.startswith("<svg")
    def test_has_legend(self):
        svg = generate_crochet_chart(parse_pattern(T))
        assert "sc" in svg; assert "inc" in svg

class TestRender2D:
    def test_preview(self):
        p = parse_pattern(T); r = validate_pattern(p)
        svg = render_2d_preview(p, r)
        assert svg.startswith("<svg"); assert "Pattern Instructions" in svg
    def test_without_report(self):
        svg = render_2d_preview(parse_pattern(T)); assert svg.startswith("<svg")

class TestMeasure:
    def test_measurements(self):
        m = measure_pattern(parse_pattern(T))
        assert m.total_rounds == 3; assert m.max_stitch_count == 24
