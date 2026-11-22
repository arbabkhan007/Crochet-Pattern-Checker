from crochet_checker.validation.advanced_checks import (
    ConstructionMode,
    FeatureBounds,
    RoundLoopState,
    assembly_findings,
    build_loop_states,
    check_anatomical_attachment,
    check_flat_curvature,
    check_folded_tube_closure,
    check_insert_diameter,
    check_surface_loop_join,
    classify_construction_mode,
    color_crease_findings,
    curvature_findings,
    find_spatial_collisions,
    find_advanced_findings,
    normalized_anatomical_height,
    oval_findings,
    parse_numbered_assembly_steps,
    quadruped_compass_findings,
    quadruped_findings_from_text,
    seam_stretch_mismatch,
    stitch_to_angle,
    validate_oval_foundation,
)
from crochet_checker.validation.advanced_checks.loop_occupancy import (
    loop_occupancy_findings,
)
from crochet_checker.validation.advanced_checks.turned_rows import turned_row_findings


def test_oval_foundation_counts_chain_consumption_not_stitches_produced():
    errors, produced = validate_oval_foundation(
        6,
        2,
        [(1, 2), (3, 3), (1, 3)],
        [(3, 3), (1, 2)],
    )
    assert errors == []
    assert produced == 13

    errors, produced = validate_oval_foundation(
        6,
        2,
        [(1, 2), (3, 3), (1, 3)],
        [(4, 4), (1, 2)],
    )
    assert produced == 14
    assert any("return pass consumes 5 chains" in error.lower() for error in errors)


def test_oval_text_adapter_requires_explicit_top_and_return_pass_evidence():
    good = (
        "Oval: ch 6; 2 sc in 2nd ch from hook, sc in next 3 ch, "
        "3 sc in last ch, working on opposite side, sc in next 3 ch, 2 sc in first ch."
    )
    bad = good.replace(
        "sc in next 3 ch, 2 sc in first ch", "sc in next 4 ch, 2 sc in first ch"
    )
    assert oval_findings(good) == []
    assert any(item.code == "OvalFoundationAccounting" for item in oval_findings(bad))
    invalid_start = good.replace("2nd ch from hook", "7th ch from hook")
    assert any(
        item.code == "OvalFoundationAccounting" for item in oval_findings(invalid_start)
    )
    undercount = good.replace(
        "sc in next 3 ch, 2 sc in first ch", "sc in next 2 ch, 2 sc in first ch"
    )
    assert any(
        item.code == "OvalReturnUnaccountedChains" for item in oval_findings(undercount)
    )
    assert oval_findings("Oval: work around the chain as written.") == []


def test_loop_banks_reflect_the_next_round_and_unknown_stays_unknown():
    states = build_loop_states({1: "UNKNOWN", 2: "BLO", 3: "FLO"})
    assert states[1].flo_free is True
    assert states[1].blo_free is False
    assert states[2].flo_free is False
    assert states[2].blo_free is True
    assert states[3].flo_free is None
    assert check_surface_loop_join(1, "FLO", states) is None
    assert "already consumed" in check_surface_loop_join(1, "BLO", states)

    text = (
        "## Body\n"
        "Round 1: 6 sc in magic ring (6)\n"
        "Round 2: sc in BLO of each st around (6)\n"
        "Round 3: sc in FLO of each st around (6)\n"
        "Attach a tab to the FLO of Round 2.\n"
    )
    findings = loop_occupancy_findings(text)
    assert any(item.code == "LoopOccupancyCollision" for item in findings)


def test_hoof_crease_requires_explicit_color_change_and_blo_round():
    text = (
        "At Round 4, change color from shoe to leg.\n"
        "Work BLO in Round 3 to form the hoof crease.\n"
    )
    findings = color_crease_findings(text)
    assert len(findings) == 1
    assert findings[0].code == "ColorChangeCreaseMisalignment"


def test_turns_reverse_profiles_check_face_parity_and_ws_glossary_rules():
    taper = (
        "## Short Rows\nRow 1 (RS): 4 sc, 4 hdc, turn\nRow 2 (WS): 4 sc, 4 hdc, turn\n"
    )
    findings = turned_row_findings(taper)
    assert any(item.code == "TurnedRowTaperInversion" for item in findings)
    assert not any(item.code == "RowFaceParityConflict" for item in findings)

    wrong_face = "## Short Rows\nRow 1 (RS): 4 sc\nRow 2 (RS): turn, 4 sc\n"
    assert any(
        item.code == "RowFaceParityConflict" for item in turned_row_findings(wrong_face)
    )

    glossary = (
        "## Glossary\ndec - front-loop-only invisible decrease\n"
        "## Short Rows\nRow 1 (WS): 3 dec, do not turn\n"
    )
    assert any(
        item.code == "WrongSideInvisibleDecrease"
        for item in turned_row_findings(glossary)
    )


def test_ws_short_row_before_rounds_is_reported_only_when_explicit():
    text = (
        "## Heel\n"
        "Short rows shape the heel.\n"
        "Row 1 (WS): 4 sc, do not turn\n"
        "Round 1: 12 sc around the heel (12)\n"
    )
    assert any(
        item.code == "InsideOutTopologyInversion" for item in turned_row_findings(text)
    )
    assert not any(
        item.code == "InsideOutTopologyInversion"
        for item in turned_row_findings("Row 1 (WS): 4 sc, do not turn")
    )
    oriented = (
        "## Heel\n"
        "Short rows shape the heel.\n"
        "Row 1 (WS): 4 sc, do not turn\n"
        "Reorient the work to RS.\n"
        "Round 1: 12 sc around the heel (12)\n"
    )
    assert not any(
        item.code == "InsideOutTopologyInversion"
        for item in turned_row_findings(oriented)
    )
    skipped = "## Rows\nRow 1 (RS): 4 sc, turn\nRow 3 (WS): 4 sc\n"
    assert not any(
        item.code == "RowFaceParityConflict" for item in turned_row_findings(skipped)
    )


def test_explicit_spatial_boxes_collide_but_partial_coordinates_do_not():
    text = (
        "Attach safety eyes to the head, rounds 11-12, stitch 17-25.\n"
        "Sew the muzzle onto the head, rounds 11-12, stitch 20-23.\n"
        "Attach ears to the top of the head around rounds 8-10.\n"
    )
    from crochet_checker.validation.advanced_checks.spatial import (
        attachment_bounds_from_text,
    )

    boxes = attachment_bounds_from_text(text)
    findings = find_spatial_collisions(boxes)
    assert len(findings) == 1
    assert findings[0].code == "SpatialBoundingBoxCollision"

    unknown = [
        FeatureBounds("eyes", "head", 4, 5, None, None, None, "eyes around rounds 4-5"),
        FeatureBounds("muzzle", "head", 4, 5, 3, 6, "stitch", "muzzle at stitches 3-6"),
    ]
    assert find_spatial_collisions(unknown) == []

    reversed_interval = (
        "Attach eyes to the head, round 4, stitches 30-4.\n"
        "Attach muzzle to the head, round 4, stitches 1-6.\n"
    )
    assert find_spatial_collisions(attachment_bounds_from_text(reversed_interval)) == []


def test_polar_positions_and_seam_stretch_require_explicit_inputs():
    assert stitch_to_angle(1, 4) == 45
    assert seam_stretch_mismatch(8, 8, 2, 4) is not None
    assert seam_stretch_mismatch(8, 8, 2, 4, threshold=2.0) is None
    explicit_seam = "Gauge: 28 sts and 28 rows = 10 cm.\nSeam: 14 sts over 2 rounds.\n"
    assert any(
        item.code == "SeamStretchMismatch"
        for item in find_advanced_findings(explicit_seam)
    )

    crowded = {
        "foreleg 1": (7, 1, 36),
        "foreleg 2": (7, 3, 36),
        "hind leg 1": (7, 5, 36),
        "hind leg 2": (7, 7, 36),
    }
    findings = quadruped_compass_findings(crowded)
    assert any(item.code == "QuadrupedHemisphereClustering" for item in findings)
    spaced = {
        "foreleg 1": (7, 34, 36),
        "foreleg 2": (7, 4, 36),
        "hind leg 1": (7, 16, 36),
        "hind leg 2": (7, 22, 36),
    }
    assert quadruped_compass_findings(spaced) == []

    positions = (
        "## JAYG limbs\nStitch 1 is at the center front of the torso.\n"
        "Foreleg 1 joins as you go at Round 7, Stitch 1 of 36.\n"
        "Foreleg 2 joins as you go at Round 7, Stitch 3 of 36.\n"
        "Hind leg 1 joins as you go at Round 7, Stitch 5 of 36.\n"
        "Hind leg 2 joins as you go at Round 7, Stitch 7 of 36.\n"
    )
    assert any(
        item.code == "QuadrupedHemisphereClustering"
        for item in quadruped_findings_from_text(positions)
    )
    assert (
        quadruped_findings_from_text(positions.replace("JAYG limbs", "Limb positions"))
        == []
    )
    assert (
        quadruped_findings_from_text(
            positions.replace(
                "Stitch 1 is at the center front of the torso.",
                "Stitch 1 begins the round.",
            )
        )
        == []
    )


def test_spiral_colorwork_warns_only_for_four_identical_unshifted_rounds():
    text = (
        "## Body\nWork in a continuous unjoined spiral.\n"
        "Round 1: 14 A, 8 B, 14 A (36)\n"
        "Round 2: 14 A, 8 B, 14 A (36)\n"
        "Round 3: 14 A, 8 B, 14 A (36)\n"
        "Round 4: 14 A, 8 B, 14 A (36)\n"
    )
    findings = find_advanced_findings(text)
    assert any(item.code == "SpiralColorworkDrift" for item in findings)
    shifted = text + "Shift the start by one stitch each round.\n"
    assert not any(
        item.code == "SpiralColorworkDrift" for item in find_advanced_findings(shifted)
    )
    local_shift = text + "Shift the start one stitch in Round 2.\n"
    assert any(
        item.code == "SpiralColorworkDrift"
        for item in find_advanced_findings(local_shift)
    )
    quoted_example = "## Body\n```text\n" + text.split("## Body\n", 1)[1] + "```\n"
    assert not any(
        item.code == "SpiralColorworkDrift"
        for item in find_advanced_findings(quoted_example)
    )


def test_anatomical_axis_uses_explicit_direction_and_rounds():
    assert normalized_anatomical_height(3, 33, "BOTTOM_UP") == 2 / 32
    assert normalized_anatomical_height(3, 33, "TOP_DOWN") == 30 / 32
    findings = check_anatomical_attachment("wings", 2, 3, 33, "BOTTOM_UP")
    assert findings and findings[0].code == "AnatomicalZAxisInversion"
    assert not check_anatomical_attachment("wings", 2, 3, 33, "TOP_DOWN")

    text = (
        "## Torso\nWorked bottom-up from base to neck.\n"
        "Round 1: 8 sc in magic ring (8)\n"
        "Round 2: 16 sc (16)\n"
        "Round 3: 24 sc (24)\n"
        "Round 4: 32 sc (32)\n"
        "Round 33: 32 sc (32)\n"
        "Attach wings to the torso, rounds 2-3.\n"
    )
    findings = find_advanced_findings(text)
    assert any(item.code == "AnatomicalZAxisInversion" for item in findings)


def test_flat_disc_curvature_detects_only_explicit_centered_flat_sc_counts():
    findings = check_flat_curvature(
        [(1, 8), (2, 16), (3, 32), (4, 64)],
        flat_intent=True,
        center_start=True,
        single_crochet=True,
    )
    assert [item.code for item in findings] == [
        "HyperbolicCurvatureOverflow",
        "HyperbolicCurvatureOverflow",
    ]
    assert all(item.severity == "warning" for item in findings)
    assert (
        check_flat_curvature(
            [(1, 8), (2, 16), (3, 24), (4, 32)],
            flat_intent=True,
            center_start=True,
            single_crochet=True,
        )
        == []
    )
    assert (
        check_flat_curvature(
            [(1, 8), (2, 16), (3, 24)],
            flat_intent=False,
            center_start=True,
            single_crochet=True,
        )
        == []
    )

    text = (
        "## Flat coaster\nStart with a magic ring.\n"
        "Round 1: 8 sc in ring (8)\n"
        "Round 2: 16 sc around (16)\n"
        "Round 3: 32 sc around (32)\n"
        "Round 4: 64 sc around (64)\n"
    )
    assert any(
        item.code == "HyperbolicCurvatureOverflow" for item in curvature_findings(text)
    )


def test_insert_diameter_and_folded_tube_closure_need_written_counts():
    overflow = check_insert_diameter(3.5, 14, 2.8)
    assert overflow and overflow.code == "InsertDiameterOverflow"
    assert check_insert_diameter(1.7, 14, 2.8) is not None
    closure = check_folded_tube_closure(14, 5)
    assert closure and closure[0].code == "PartialTubeClosure"
    assert check_folded_tube_closure(14, 7) == []
    assert check_folded_tube_closure(5, 3) == []

    text = (
        "Gauge: 28 sts and 28 rows = 10 cm.\n"
        "A 3.5 cm dowel fits inside an opening of 14 stitches.\n"
        "## Leg\nRound 3: 14 sc (14)\nFlatten and close with 5 sc.\n"
    )
    findings = find_advanced_findings(text)
    assert any(item.code == "InsertDiameterOverflow" for item in findings)
    assert any(item.code == "PartialTubeClosure" for item in findings)

    ambiguous_gauge = (
        "Gauge: 28 sts and 28 rows = 10 cm.\n"
        "Alternate gauge: 20 sts and 24 rows = 10 cm.\n"
        "A 3.5 cm dowel fits inside an opening of 14 stitches.\n"
    )
    assert not any(
        item.code == "InsertDiameterOverflow"
        for item in find_advanced_findings(ambiguous_gauge)
    )


def test_assembly_ingests_all_numbered_steps_and_skips_in_crochet_attachments():
    text = (
        "## Head (make separately)\nRounds 1-3: work in rounds.\n"
        "## Tail (make 1)\nRounds 1-2: work in rounds.\n"
        "## Tapestry Chest Crest\nWorked inline as part of the torso colorwork.\n"
        "## Forelegs\nJoin as you go (JAYG) to the torso.\n"
        "## Waist Peplum\nSlip stitch directly to the torso.\n"
        "## Final Assembly\n"
        "### Steps\n"
        "1. Sew the head to the body at rounds 9-10.\n"
        "2. Attach the tail to the body at round 12.\n"
        "3. Add the eyes to the head at round 4.\n"
    )
    steps = parse_numbered_assembly_steps(text)
    assert [step.number for step in steps] == [1, 2, 3]
    assert steps[0].piece_name == "Head"
    assert steps[0].target_round_min == 9
    assert steps[0].target_round_max == 10
    assert (
        classify_construction_mode(
            "Tapestry Chest Crest", "Worked inline as part of the torso colorwork"
        )
        == ConstructionMode.INLINE_COLORWORK
    )
    assert (
        classify_construction_mode("Forelegs", "Join as you go (JAYG)")
        == ConstructionMode.JAYG_ATTACHED
    )
    assert (
        classify_construction_mode("Waist", "Slip stitch directly to the torso")
        == ConstructionMode.DIRECT_SURFACE_JOIN
    )
    assert (
        classify_construction_mode("Tail (make 1)", "Work in rounds")
        == ConstructionMode.UNKNOWN
    )
    assert assembly_findings(text) == []

    missing = (
        "## Head (make separately)\nRound 1: 6 sc in magic ring (6)\n"
        "Final Assembly:\n"
        "1. Add the eyes to the head.\n"
    )
    missing_findings = assembly_findings(missing)
    assert len(missing_findings) == 1
    assert missing_findings[0].code == "MissingSeparatePieceAssemblyStep"
    assert missing_findings[0].line_number == 1


def test_advanced_findings_are_attached_to_the_primary_validator_report():
    from crochet_checker.validation.validator import PatternValidator

    text = (
        "# Flat coaster\nStart with a magic ring.\n"
        "Round 1: 8 sc in ring (8)\n"
        "Round 2: 16 sc around (16)\n"
        "Round 3: 32 sc around (32)\n"
    )
    report = PatternValidator().validate(text)
    assert any(
        "HyperbolicCurvatureOverflow" in item.message for item in report.warnings
    )
