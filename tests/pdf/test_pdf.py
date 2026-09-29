"""Tests for PDF generation."""

from crochet_checker.parser.parser import parse_pattern
from crochet_checker.pdf import PDFConfig, PDFGenerator, generate_pdf_html
from crochet_checker.validation import validate_pattern

T = (
    "Round 1: 6 sc into magic ring (6)"
    + chr(10)
    + "Round 2: (sc, inc) x 6 (18)"
    + chr(10)
    + "Round 3: (2 sc, inc) x 6 (24)"
)


class TestPDF:
    def test_generates_html(self):
        html = generate_pdf_html(parse_pattern(T))
        assert html.startswith("<!DOCTYPE html>") and "</html>" in html

    def test_contains_rounds(self):
        html = generate_pdf_html(parse_pattern(T))
        assert "Round 1" in html and "Round 2" in html and "Round 3" in html

    def test_stitch_counts(self):
        html = generate_pdf_html(parse_pattern(T))
        assert "(6 sts)" in html and "(18 sts)" in html

    def test_abbreviations(self):
        html = generate_pdf_html(parse_pattern(T))
        assert "Abbreviations" in html and "Single Crochet" in html

    def test_materials(self):
        html = generate_pdf_html(parse_pattern(T))
        assert "Materials" in html

    def test_measurements(self):
        html = generate_pdf_html(parse_pattern(T))
        assert "Finished Measurements" in html

    def test_validation(self):
        p = parse_pattern(T)
        r = validate_pattern(p)
        html = generate_pdf_html(p, validation_report=r)
        assert "Validation Report" in html

    def test_designer(self):
        html = generate_pdf_html(
            parse_pattern(T), config=PDFConfig(designer_name="Jane")
        )
        assert "Jane" in html

    def test_save(self):
        import os
        import tempfile

        p = parse_pattern(T)
        gen = PDFGenerator()
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
            fp = f.name
        try:
            gen.save(fp, p)
            assert "<!DOCTYPE html>" in open(fp).read()
        finally:
            os.unlink(fp)


def test_sheet_options_do_not_change_a_check():
    text = "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\n"
    before = validate_pattern(text)
    html = generate_pdf_html(parse_pattern(text), config=PDFConfig(template="craft", page_size="Letter"), validation_report=before)
    after = validate_pattern(text)
    assert before.overall_status == after.overall_status == "PASS"
    assert "Letter" in html and "#5B4A69" in html
    assert "Charts" in html and "<svg" in html and "Worked" in html
    assert "counter(page)" in html and "not a reading of a chart image" in html

def test_color_key_uses_only_written_names():
    named = generate_pdf_html(parse_pattern("Color A: Brown\nRound 1: 6 sc into magic ring (6)\n"))
    plain = generate_pdf_html(parse_pattern("Round 1: 6 sc into magic ring (6)\n"))
    unknown = generate_pdf_html(parse_pattern("Color A: Chartreuse\nRound 1: 6 sc into magic ring (6)\n"))
    assert "Color key" in named and "#8B5A2B" in named
    assert "Color key" not in plain and "Color key" not in unknown

def test_sections_can_be_left_out():
    html = generate_pdf_html(parse_pattern(T), config=PDFConfig(include_materials=False, include_charts=False, include_checklist=False, copyright_text="Mine"))
    assert "Materials" not in html and "Charts" not in html and "Worked" not in html and "Mine" in html
