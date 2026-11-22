"""Regression tests for four targeted NS102 validator refinements."""

from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation.advanced_checks import (
    attachment_bounds_from_text,
    find_advanced_findings,
    find_spatial_collisions,
    validate_bom_and_stuffing_sanity,
)
from crochet_checker.validation.advanced_checks.loop_occupancy import (
    loop_occupancy_findings,
)
from crochet_checker.validation.advanced_checks.turned_rows import turned_row_findings
from crochet_checker.validation.stitch_counts import validate_stitch_counts
from crochet_checker.validation.validator import PatternValidator


def test_repeat_trailing_clause_is_not_included_in_multiplier():
    text = (
        "Rnd 9: [sc, inc] x 4, sc (14)\n"
        "Rnd 10: [2 sc, inc] x 4, 2 sc (18)"
    )
    pattern = parse_pattern(text)
    rnd9, rnd10 = pattern.rounds

    assert rnd9.instructions[0].total_stitches_consumed == 9
    assert rnd9.instructions[0].total_stitches_produced == 13
    assert rnd10.instructions[0].total_stitches_consumed == 14
    assert rnd10.instructions[0].total_stitches_produced == 18
    assert all(op.is_part_of_repeat for op in rnd10.instructions[0].operations[:-1])
    assert rnd10.instructions[0].operations[-1].count == 2
    assert not rnd10.instructions[0].operations[-1].is_part_of_repeat

    report = validate_stitch_counts(pattern)
    rnd9_data, rnd10_data = report.row_by_row
    assert rnd9_data["stitches_consumed"] == 9
    assert rnd9_data["stitches_produced"] == 13
    assert rnd10_data["stitches_consumed"] == 14
    assert rnd10_data["stitches_produced"] == 18
    assert any(
        finding.location == "Round 9"
        and "states 14" in finding.message
        and "produce 13" in finding.message
        for finding in report.errors
    )
    assert any(
        finding.location == "Round 10"
        and "consumes 14" in finding.message
        and "Round 9 produced 13" in finding.message
        for finding in report.errors
    )

    live_report = PatternValidator().validate(text)
    assert live_report.stitch_counts[("Main", 1)] == 13
    assert live_report.stitch_counts[("Main", 2)] == 18
    assert any(
        "consumes 14" in finding.message
        and "only 13 are available" in finding.message
        and "1 extra stitch" in finding.message
        for finding in live_report.errors
    )


def test_loop_ownership_tracks_prior_rounds_across_sections_and_multiple_targets():
    text = """\
## Thoracic Mantle
Rnd 12: 48 sc around (48)
Rnd 13: Working in FLO around, [6 sc, inc] x 6. (48)
Rnd 14: Working in BLO around, 48 sc. (48)
Rnd 15-17: 48 sc around (3 rounds total). (48)

## Section 10: Barnacle Skirt
Join Yarn C into the unworked back loops of Rnd 13 and the unworked front loops of Rnd 14 simultaneously.
Attach the trim to the free FLO of Rnd 13.
"""
    findings = [
        item for item in loop_occupancy_findings(text)
        if item.code == "LoopOccupancyCollision"
    ]

    assert len(findings) == 2
    assert any("Round 13 BLO" in item.message and "Round 14" in item.message for item in findings)
    assert any("Round 14 FLO" in item.message and "Round 15" in item.message for item in findings)
    assert not any("Round 13 FLO" in item.message for item in findings)


def test_turned_row_detects_descending_profile_reuse_and_dtr_chain_deficit():
    inverted = """\
## Fin Rows
Row 3 (RS): 3 dtr, 4 tr, 4 dc, 3 sc, ch 1, turn
Row 4 (WS): 3 dtr, 4 tr, 4 dc, 3 sc, turn
"""
    findings = turned_row_findings(inverted)
    codes = {item.code for item in findings}

    assert "TurnedRowTaperInversion" in codes
    assert "TurningChainHeightMismatch" in codes
    elevation_finding = next(item for item in findings if item.code == "TurningChainHeightMismatch")
    assert elevation_finding.severity == "warning"
    assert "typically ch 4 or ch 5" in elevation_finding.message

    mirrored = """\
## Fin Rows
Row 3 (RS): 3 dtr, 4 tr, 4 dc, 3 sc, ch 1, turn
Row 4 (WS): 3 sc, 4 dc, 4 tr, 3 dtr, ch 1, turn
"""
    mirrored_findings = turned_row_findings(mirrored)
    assert not any(item.code == "TurnedRowTaperInversion" for item in mirrored_findings)
    assert not any(item.code == "TurningChainHeightMismatch" for item in mirrored_findings)


def test_bom_sections_stuffing_and_explicit_assembly_overlap_are_reported():
    text = """\
Finished size: 75 cm tall

## Materials
- Yarn A — Ocean Blue, 150 g
- Yarn E — Radioactive Chartreuse, 85 g
- Polyester fiberfill — 4,500 g
- 1x Brass Pressure Gauge Bezel (worked in Section 14)

## Section 1: Cephalic Dome
Use Yarn A for the dome.

## Section 10: Gill Frills
Work the frills separately.

## Section 12: Barnacle Skirt
Work the skirt as written.

## Final Assembly
3. Attach the Gill Frills to the Cephalic Dome, Rnds 7–9, Sts 4–7.
4. Sew the Kraken Rostrum Spikes onto the Cephalic Dome, Rnds 8–10, Sts 6–9.
"""
    findings = find_advanced_findings(text)
    codes = {item.code for item in findings}

    assert "OrphanedYarn" in codes
    assert "DanglingSectionReference" in codes
    assert "ImplausibleStuffingMass" in codes
    assert "SpatialBoundingBoxCollision" in codes
    assert any("Yarn E" in item.message for item in findings if item.code == "OrphanedYarn")
    assert any("Section 14" in item.message for item in findings if item.code == "DanglingSectionReference")
    assert any("4,500" in item.message and "75 cm" in item.message for item in findings if item.code == "ImplausibleStuffingMass")

    live_messages = [item.message for item in PatternValidator().validate(text).warnings]
    for code in ("OrphanedYarn", "DanglingSectionReference", "ImplausibleStuffingMass", "SpatialBoundingBoxCollision"):
        assert any(f"[{code}]" in message for message in live_messages)


def test_multiple_features_and_disjoint_ranges_are_not_cartesian_product_collisions():
    text = (
        "Attach Gill Frills and Kraken Rostrum Spikes to the Cephalic Dome, "
        "Rounds 7–9, Sts 4–7 & 25–28."
    )
    boxes = attachment_bounds_from_text(text)
    assert boxes
    assert all(box.horizontal_min is None for box in boxes)
    assert find_spatial_collisions(boxes) == []


def test_bom_stuffing_helper_is_case_insensitive_and_skips_plausible_mass():
    warnings = validate_bom_and_stuffing_sanity(
        ["Yarn E — Radioactive Chartreuse, 85 g"],
        ["yarn A"],
        list(range(1, 13)),
        [14],
        75,
        4500,
    )
    assert any(item.startswith("ORPHANED YARN IN BOM:") for item in warnings)
    assert any(item.startswith("DANGLING SECTION REFERENCE:") for item in warnings)
    assert any(item.startswith("IMPLAUSIBLE STUFFING MASS:") for item in warnings)

    plausible = validate_bom_and_stuffing_sanity([], [], [1], [], 75, 600)
    assert plausible == []
