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


def test_print_setup_is_on_the_sheet_only():
    text = "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\n"
    before = validate_pattern(text)
    html = generate_pdf_html(
        parse_pattern(text),
        config=PDFConfig(template="craft", page_size="Letter", large_print=True, ink_saver=True, landscape=True, binding="left", compact=True),
        validation_report=before,
    )
    after = validate_pattern(text)
    assert before.overall_status == after.overall_status == "PASS"
    assert "large-print" in html and "ink-saver" in html and "Letter landscape" in html and "2.8cm" in html
    assert "Crochet pattern sheet" in html and "does not certify the pattern" in html
    assert "+6" in html and "Round marks" in html and "Change" in html and "not a measured length" in html

def test_new_print_parts_do_not_restore_hidden_sections():
    html = generate_pdf_html(
        parse_pattern(T),
        config=PDFConfig(
            include_materials=False,
            include_charts=False,
            include_checklist=False,
            copyright_text="Mine",
            large_print=True,
            include_marks=True,
            include_change=True,
            include_ruled_notes=True,
            include_used_stitches=True,
        ),
    )
    assert "Materials" not in html and "Charts" not in html and "Worked" not in html and "Mine" in html
    assert "Round marks" in html and "Write-in notes" in html

def test_optional_print_parts_can_be_left_out():
    html = generate_pdf_html(
        parse_pattern(T),
        config=PDFConfig(include_marks=False, include_change=False, include_ruled_notes=False, include_used_stitches=False, include_index=False),
    )
    assert "Round marks" not in html and "Write-in notes" not in html and "<th>Change</th>" not in html and "Stitches used" not in html

def test_written_color_tints_only_a_known_name():
    named = generate_pdf_html(parse_pattern("Color A: Brown\nRound 1: 6 sc in brown (6)\n"))
    unknown = generate_pdf_html(parse_pattern("Color A: Chartreuse\nRound 1: 6 sc in Chartreuse (6)\n"))
    assert "background:#8B5A2B22" in named
    assert 'style="background:' not in unknown

def test_a_flagged_round_stays_an_error():
    text = "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n"
    report = validate_pattern(text)
    html = generate_pdf_html(parse_pattern(text), validation_report=report)
    again = validate_pattern(text)
    assert report.overall_status == again.overall_status == "ERROR"
    assert "6 to 18" in html


def test_advanced_print_does_not_change_a_check():
    text = "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\nRound 3: sc in each st around (12)\nRound 4: sc in each st around (12)\nRound 5: sc in each st around (12)\n"
    before = validate_pattern(text)
    html = generate_pdf_html(
        parse_pattern(text),
        config=PDFConfig(duplex=True, binding="left", cards=True, crop_marks=True),
        validation_report=before,
    )
    after = validate_pattern(text)
    assert before.overall_status == after.overall_status == "PASS"
    assert "counter(pages)" in html and "bookmark-level" in html and "target-counter" in html
    assert "marks: crop cross" in html and "page: cover" in html and "string-set: piece-title" in html
    assert "Count ladder" in html and "Count sequence:" in html and "hold 12" in html
    assert "not a finished size" in html and "Text id" in html and "Not a certification." in html
    assert "Parsed: MR, 6 sc" in html and "Check status: PASS" in html
    assert "Maker ________" in html and "@page :left" in html and "cards" in html
    again = generate_pdf_html(parse_pattern(text))
    assert html.split("Text id ")[1][:8] == again.split("Text id ")[1][:8]

def test_a_flagged_round_is_outlined_on_the_ladder():
    text = "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n"
    report = validate_pattern(text)
    html = generate_pdf_html(parse_pattern(text), validation_report=report)
    again = validate_pattern(text)
    assert report.overall_status == again.overall_status == "ERROR"
    assert 'stroke="#C0392B"' in html and "Check status: ERROR" in html
    assert "6 to 18" in html

def test_advanced_parts_do_not_restore_hidden_words():
    html = generate_pdf_html(
        parse_pattern(T),
        config=PDFConfig(
            include_materials=False,
            include_charts=False,
            include_checklist=False,
            copyright_text="Mine",
            duplex=True,
            cards=True,
            crop_marks=True,
        ),
    )
    assert "Materials" not in html and "Charts" not in html and "Worked" not in html and "Mine" in html
    assert "Count ladder" in html and "Text id" in html

def test_advanced_parts_can_be_left_out():
    html = generate_pdf_html(
        parse_pattern(T),
        config=PDFConfig(include_ladder=False, include_parse=False, include_maker=False, include_map=False),
    )
    assert "Count ladder" not in html and "Parsed:" not in html and "Maker ________" not in html and "Make order" not in html

def test_piece_links_follow_written_pieces():
    from pathlib import Path

    text = (Path(__file__).resolve().parents[2] / "examples" / "amigurumi_bunny.txt").read_text(encoding="utf-8")
    html = generate_pdf_html(parse_pattern(text))
    assert 'href="#piece-1"' in html and 'id="piece-1"' in html and "Make order" in html and "HEAD" in html
