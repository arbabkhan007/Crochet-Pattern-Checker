"""Tests for the calculators module (gauge, yarn, hooks, conversion)."""

import pytest

from crochet_checker.calculators import (
    convert_length,
    convert_terminology,
    estimate_yarn,
    gauge_to_size,
    nearest_hook,
    recommend_hook,
    shape_from_counts,
    stitches_for_size,
    stitch_count_chart,
    wpi_to_weight,
)


def test_gauge_to_size():
    result = gauge_to_size(40, 40, 20, 20)
    assert result.width_in == 8.0
    assert result.height_in == 8.0
    assert result.width_cm == 20.3


def test_gauge_rejects_bad_input():
    with pytest.raises(ValueError):
        gauge_to_size(0, 10, 20, 20)
    with pytest.raises(ValueError):
        gauge_to_size(10, 10, 0, 20)


def test_stitches_for_size():
    assert stitches_for_size(8, 20) == 40
    assert stitches_for_size(8, 20, round_to=6) == 42
    with pytest.raises(ValueError):
        stitches_for_size(8, 20, round_to=0)


def test_estimate_yarn():
    est = estimate_yarn(1000, "sc")
    assert est.yards > 0
    assert est.metres > 0
    assert est.balls_100g > 0
    with pytest.raises(ValueError):
        estimate_yarn(100, "unknown")
    with pytest.raises(ValueError):
        estimate_yarn(100, "sc", yards_per_100g=0)


def test_recommend_hook_by_number_and_name():
    by_number = recommend_hook(4)
    by_name = recommend_hook("worsted")
    assert by_number.weight_number == 4
    assert by_name.weight_number == 4
    assert by_number.hook_mm_low == 5.5


def test_recommend_hook_unknown():
    with pytest.raises(ValueError):
        recommend_hook("not-a-weight")


def test_nearest_hook():
    mm, label = nearest_hook(5.0)
    assert mm == 5.0
    assert label == "H-8"


def test_wpi_to_weight():
    assert wpi_to_weight(10) == 4
    assert wpi_to_weight(35) == 0
    assert wpi_to_weight(3) == 7


def test_convert_terminology_us_to_uk():
    out = convert_terminology("Round 1: 6 sc, 2 hdc, 1 dc (9)", "us-to-uk")
    assert "6 dc" in out
    assert "2 htr" in out
    assert "1 tr" in out


def test_convert_terminology_uk_to_us():
    out = convert_terminology("6 dc, 2 htr", "uk-to-us")
    assert "6 sc" in out
    assert "2 hdc" in out


def test_convert_terminology_word_boundaries():
    # "sc" inside other words must not be replaced.
    out = convert_terminology("scale the sc", "us-to-uk")
    assert "scale" in out
    assert "dc" in out


def test_convert_length():
    assert convert_length(4, "in", "cm") == 10.16
    assert convert_length(100, "cm", "in") == 39.37


def test_stitch_count_chart():
    chart = stitch_count_chart([6, 12, 18])
    assert chart[0]["pct_of_max"] == pytest.approx(33.3, abs=0.1)
    assert chart[-1]["pct_of_max"] == 100.0


def test_shape_from_counts():
    assert shape_from_counts([36] * 5) == "tube"
    assert shape_from_counts([36, 30, 24, 18]) == "cone"
    assert shape_from_counts([6, 12, 18, 24]) == "bowl"
