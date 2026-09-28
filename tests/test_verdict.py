from crochet_checker.verification import verify_pattern


def test_verdict_uses_the_real_checker_and_names_the_gaps():
    bad = "Round 1: (sc, dec) x 6 (12)\nRound 2: inc x 12 (24)\n"
    verdict = verify_pattern(bad)
    assert verdict.status == "ERROR"
    assert any("12 stitches jump to 24" in item for item in verdict.errors)
    assert "text checker" in verdict.engines_ran
    assert "chart text" in verdict.engines_ran
    assert "chart image detector" in verdict.engines_skipped
    assert "photo stitch classifier" in verdict.engines_skipped
    assert "hosted language model" in verdict.engines_skipped

    good = (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: inc x 6 (12)\n"
        "Round 3: (sc, inc) x 6 (18)\n"
    )
    passed = verify_pattern(good)
    assert passed.status == "PASS"
    assert passed.engines_skipped == verdict.engines_skipped
