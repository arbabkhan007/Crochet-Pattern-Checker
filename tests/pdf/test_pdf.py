"""Tests for PDF generation."""
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern
from crochet_checker.pdf import PDFConfig, PDFGenerator, generate_pdf_html
T = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (18)" + chr(10) + "Round 3: (2 sc, inc) x 6 (24)"

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
        p = parse_pattern(T); r = validate_pattern(p)
        html = generate_pdf_html(p, validation_report=r)
        assert "Validation Report" in html
    def test_designer(self):
        html = generate_pdf_html(parse_pattern(T), config=PDFConfig(designer_name="Jane"))
        assert "Jane" in html
    def test_save(self):
        import tempfile, os
        p = parse_pattern(T); gen = PDFGenerator()
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f: fp = f.name
        try:
            gen.save(fp, p)
            assert "<!DOCTYPE html>" in open(fp).read()
        finally: os.unlink(fp)
