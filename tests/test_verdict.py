from crochet_checker.verification import verify_pattern


def test_verdict_uses_the_real_checker_and_names_the_gaps():
    bad = "Round 1: (sc, dec) x 6 (12)\nRound 2: inc x 12 (24)\n"
    verdict = verify_pattern(bad)
    assert verdict.status == "PASS_WITH_WARNINGS"
    assert verdict.errors == []
    assert any("12 to 24 stitches doubles the count" in item for item in verdict.warnings)
    assert "text checker" in verdict.engines_ran
    assert "chart text" in verdict.engines_ran
    assert "chart image detector" in verdict.engines_skipped
    assert "photo stitch classifier" in verdict.engines_skipped
    assert "hosted language model" in verdict.engines_skipped
    assert verdict.to_dict()["ruleset_id"] == "CPC-RULESET-1"
    assert any(
        finding["rule_id"] == "CPC.SHAPE.LARGE_STEP_REVIEW"
        for finding in verdict.findings
    )

    good = (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: inc x 6 (12)\n"
        "Round 3: (sc, inc) x 6 (18)\n"
    )
    passed = verify_pattern(good)
    assert passed.status == "PASS"
    assert passed.engines_skipped == verdict.engines_skipped


def test_unparsed_row_requires_review_instead_of_a_clean_pass():
    from crochet_checker.validation.validator import validate_pattern

    text = (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: puff stitch in each st around\n"
    )
    report = validate_pattern(text)
    assert report.overall_status == "NEEDS_REVIEW"
    assert report.errors == []
    assert len(report.not_checked) == 1
    assert "puff stitch" in report.not_checked[0]
    assert report.findings[0].rule_id == "CPC.PARSER.ROW_UNPARSED"


def test_repeat_suffix_is_reviewed_without_counting_the_parsed_prefix():
    from crochet_checker.validation.validator import validate_pattern

    text = (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: (sc, inc) x 6 (18) or (sc, inc) x 3 (9)\n"
    )
    report = validate_pattern(text)
    assert report.overall_status == "NEEDS_REVIEW"
    assert report.errors == []
    assert len(report.not_checked) == 1
    assert "text after the repeat may be unparsed" in report.not_checked[0]
    finding = report.findings[0].to_dict()
    assert finding["rule_id"] == "CPC.PARSER.REPEAT_SUFFIX_UNPARSED"
    assert finding["severity"] == "review"
    assert finding["location"] == "Line 2"
