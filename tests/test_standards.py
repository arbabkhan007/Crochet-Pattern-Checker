"""The published reference is complete and does not invent a Size 8 band."""

from crochet_checker.standards.reference import (
    ABBREVIATIONS,
    CROCHET_HOOKS,
    KNITTING_NEEDLES,
    REPEAT_MARKS,
    STEEL_HOOKS,
    TUNISIAN,
    US_UK,
    YARN_WEIGHTS,
    hook_label,
    render_markdown,
    steel_rows_for_label,
    yarn_by_name,
    yarn_by_number,
)


def test_yarn_weights_are_the_published_zero_to_seven():
    assert [item["number"] for item in YARN_WEIGHTS] == list(range(8))
    assert yarn_by_number(8) is None
    worsted = yarn_by_name("worsted")
    assert worsted["number"] == 4
    assert worsted["crochet_gauge"] == (11, 14)
    lace = yarn_by_number(0)
    assert lace["crochet_gauge_stitch"] == "double crochet"
    assert lace["knit_gauge"] == (33, 40)
    assert lace["hook_mm"] is None
    assert lace["steel_hook_mm"] == (1.4, 1.6)
    assert lace["regular_hook_mm"] == 2.25
    assert lace["banded"] is False
    assert yarn_by_name("super fine")["number"] == 1
    assert yarn_by_name("super bulky")["number"] == 6


def test_hook_and_needle_charts_keep_the_council_labels():
    assert hook_label(5.0) == "H-8"
    assert hook_label(6.5) == "K-10 1/2"
    assert hook_label(2.5) is None
    assert len(CROCHET_HOOKS) == 28
    assert len(KNITTING_NEEDLES) == 29
    assert steel_rows_for_label("00") == ((3.5, "00"), (2.7, "00"))
    assert steel_rows_for_label("2") == ((2.25, "2"), (2.20, "2"))
    assert steel_rows_for_label("8/7/2") == ((1.5, "8/7/2"),)
    assert len({label for _, label in STEEL_HOOKS}) < len(STEEL_HOOKS)


def test_terms_include_the_council_lists():
    assert ABBREVIATIONS["sc"] == "single crochet"
    assert ABBREVIATIONS["hdc"] == "half double crochet"
    assert ABBREVIATIONS["trtr"] == "triple treble crochet"
    assert TUNISIAN["tss"] == "Tunisian simple stitch"
    assert US_UK[1] == ("single crochet (sc)", "double crochet (dc)")
    assert "slst" not in ABBREVIATIONS
    assert ABBREVIATIONS["m"] == "marker"
    assert REPEAT_MARKS[0][0] == "*"
    page = render_markdown()
    assert "No Size 8 numbers are stored." in page
    assert "| 8 | " not in page.split("## Crochet hooks")[0]
    assert "H-8" in page
