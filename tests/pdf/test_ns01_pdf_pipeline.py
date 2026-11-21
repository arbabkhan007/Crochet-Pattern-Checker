"""Regression tests for the NS 01 structured PDF build and asset QA."""

from __future__ import annotations

import copy
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from pypdf import PdfReader
from reportlab.lib.units import mm

from tools.build_ns01_etsy_pdf import (
    GaugeRulerFlowable,
    assembly_steps,
    build_pdf,
    build_printer_pdf,
    check_pdf_text_bounds,
    expected_progress_box_count,
    export_placement_svg,
    postflight_pdf,
    postflight_printer_pdf,
)
from tools.ns01_pdf_asset_qa import audit_assets, format_report
from tools.ns01_pdf_model import (
    SOURCE,
    compile_ns01_pdf_model,
    insert_exceeds_crochet_threshold,
    validate_ns01_pdf_model,
)

ROOT = Path(__file__).resolve().parents[2]


def test_compiled_model_matches_canonical_ns01_master() -> None:
    model = compile_ns01_pdf_model()
    pattern = model["pattern"]
    head = model["components"]["head"]
    body = model["components"]["body"]

    assert pattern["design_code"] == "NS 01"
    assert pattern["finished_size_cm"] == 15
    assert pattern["hook_mm"] == 3.5
    assert pattern["hook_us"] == "E-4"
    assert pattern["gauge"] == {
        "stitches": 11,
        "stitch_type": "sc",
        "rounds": 12,
        "measure_cm": 5.0,
    }
    assert [(yarn["id"], yarn["grams"]) for yarn in pattern["yarns"]] == [
        ("A", 25),
        ("B", 12),
        ("C", 5),
        ("D", 6),
    ]
    assert head["closure"] == {"round": 16, "stitches": 6, "closed": True}
    assert head["neck_join"] == {"round": 14, "stitches": 18}
    assert head["features"]["eyes"] == {
        "diameter_mm": 12,
        "round_start": 9,
        "round_end": 10,
        "spacing_stitches": 7,
    }
    assert head["features"]["muzzle"] == {
        "round_start": 10,
        "lower_edge_round_start": 15,
        "lower_edge_round_end": 16,
    }
    assert body["ending"] == {"round": 19, "stitches": 18, "open": True}
    assert body["features"]["front_legs"]["gap_stitches"] == 8


def test_insert_fit_threshold_is_one_sided_at_1_15() -> None:
    assert not insert_exceeds_crochet_threshold(11.5, 10.0)
    assert insert_exceeds_crochet_threshold(11.5001, 10.0)
    assert not insert_exceeds_crochet_threshold(8.5, 10.0)
    with pytest.raises(ValueError, match="positive finite"):
        insert_exceeds_crochet_threshold(0.0, 10.0)


def test_model_validation_rejects_inconsistent_join_or_direction() -> None:
    model = compile_ns01_pdf_model()

    wrong_join = copy.deepcopy(model)
    wrong_join["components"]["body"]["ending"]["stitches"] = 24
    wrong_join["components"]["body"]["rounds"][-1]["stitches"] = 24
    with pytest.raises(
        ValueError, match="join count and open body neck count do not match"
    ):
        validate_ns01_pdf_model(wrong_join)

    wrong_closure = copy.deepcopy(model)
    wrong_closure["components"]["head"]["closure"]["stitches"] = 5
    with pytest.raises(ValueError, match="Head closure disagrees"):
        validate_ns01_pdf_model(wrong_closure)

    wrong_rounds = copy.deepcopy(model)
    wrong_rounds["components"]["head"]["rounds"][0]["start"] = 2
    with pytest.raises(ValueError, match="Non-contiguous head round table"):
        validate_ns01_pdf_model(wrong_rounds)

    wrong_direction = copy.deepcopy(model)
    wrong_direction["components"]["head"]["direction"] = "BOTTOM_UP"
    with pytest.raises(ValueError, match="JSON Schema validation"):
        validate_ns01_pdf_model(wrong_direction)


def test_source_tables_drive_checkbox_count_and_print_scale() -> None:
    model = compile_ns01_pdf_model()
    assert expected_progress_box_count(SOURCE.read_text(encoding="utf-8")) == 81
    assert model["pattern"]["gauge"]["measure_cm"] == 5
    assert GaugeRulerFlowable.side == pytest.approx(50 * mm)


def test_vector_placement_svg_uses_current_rounds(tmp_path: Path) -> None:
    model = compile_ns01_pdf_model()
    svg_path = tmp_path / "ns01-placement.svg"
    export_placement_svg(model, svg_path)

    root = ET.parse(svg_path).getroot()
    svg_text = " ".join(root.itertext())
    assert "R14" in svg_text and "R19" in svg_text
    assert "Eyes 12 mm" in svg_text
    assert "R15" in svg_text and "R16" in svg_text
    assert "not to scale" in svg_text.lower()
    assert root.tag.endswith("svg")


def test_assembly_overview_callouts_follow_compiled_rounds_and_join() -> None:
    model = compile_ns01_pdf_model()
    steps = {label: note for _number, label, note in assembly_steps(model)}

    assert "Rnd 16" in steps["MUZZLE + FACE"]
    assert "Rnds 5–7" in steps["HORNS"]
    assert "R8–R9" in steps["EARS"]
    assert "Rnds 6–8" in steps["FRINGE"]
    assert "18 body R19 sts to 18 head R14 sts" in steps["HEAD → BODY"]
    assert "Rnds 3–6" in steps["BACK LEGS"]
    assert "Rnds 8–9" in steps["FRONT LEGS"]
    assert "3 rounds above base" in steps["BELLY PATCH"]


def test_photo_qa_reports_resolution_and_human_review_hold() -> None:
    assets, pending = audit_assets()
    report = format_report(assets, pending)

    assert len(assets) == 2
    assert assets[0].pixel_width == 864
    assert assets[0].dpi_x == pytest.approx(205, abs=1)
    assert assets[1].dpi_x == pytest.approx(287, abs=1)
    assert all(not asset.meets_resolution_target for asset in assets)
    assert len(pending) >= 5
    assert "Photo-asset release status: HOLD" in report
    assert "not a photograph of a verified sample" in report

    strict = subprocess.run(
        [sys.executable, "tools/ns01_pdf_asset_qa.py", "--strict"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    assert strict.returncode == 1
    assert "Photo-asset release status: HOLD" in strict.stdout


def test_both_ns01_pdf_editions_pass_generated_output_regression(
    tmp_path: Path,
) -> None:
    model = compile_ns01_pdf_model()
    full_colour = tmp_path / "NS01-review.pdf"
    printer_saver = tmp_path / "NS01-printer-review.pdf"

    build_pdf(full_colour, model)
    postflight_pdf(full_colour)
    build_printer_pdf(printer_saver, model)
    postflight_printer_pdf(printer_saver)

    full_text = "\n".join(
        page.extract_text() or "" for page in PdfReader(full_colour).pages
    )
    printer_text = "\n".join(
        page.extract_text() or "" for page in PdfReader(printer_saver).pages
    )
    assert "50 mm × 50 mm" in full_text
    assert "Round-referenced placement schematic" in full_text
    assert "Open neck: R19 · 18 sts" in full_text
    assert "Eyes 12 mm" in full_text
    assert "Round-referenced placement schematic" in printer_text
    assert check_pdf_text_bounds(full_colour) > 0
    assert check_pdf_text_bounds(printer_saver) > 0
