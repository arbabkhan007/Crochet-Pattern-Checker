"""Written diff and export stay inside the existing views."""

from crochet_checker.written_diff import diff_counts
from crochet_checker.written_export import REFUSED, export_text
import pytest

LEFT = "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\n"
RIGHT = "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n"


def test_diff_names_a_written_count_change():
    lines, changed = diff_counts(LEFT, RIGHT)
    assert changed
    assert any("2: 12 to 18" in line for line in lines)
    text = "\n".join(lines).lower()
    assert "not a measured shape" in text
    assert "cone" in text and "disk" in text


def test_diff_match_is_not_a_shape():
    lines, changed = diff_counts(LEFT, LEFT)
    assert not changed
    assert any("match" in line for line in lines)


def test_export_reuses_existing_views(tmp_path):
    obj = export_text(LEFT, "obj")
    assert obj.startswith("# Crochet stitch model")
    assert "not a measured size" in obj
    gltf = export_text(LEFT, "gltf")
    assert '"version": "2.0"' in gltf
    assert "not millimetres" in gltf
    assert "<svg" in export_text(LEFT, "svg")
    assert export_text(LEFT, "html").startswith("<!DOCTYPE html>")


def test_indd_is_refused():
    with pytest.raises(ValueError, match="not a format"):
        export_text(LEFT, "indd")
    assert "print-shop" in REFUSED
