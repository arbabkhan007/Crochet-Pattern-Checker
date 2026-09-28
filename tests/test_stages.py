from crochet_checker.validation.validator import validate_pattern
from crochet_checker.verification import inspect_photo, read_chart_image, run_stages


def _messages(report):
    return [str(getattr(item, "message", item)) for item in report.errors + report.warnings]


def test_each_stage_fails_wrong_and_passes_corrected():
    cases = {
        "dialect": (
            "Head\nTerms: UK\nRound 1: 6 sc into magic ring (6)\n",
            "Head\nTerms: US\nRound 1: 6 sc into magic ring (6)\n",
            "marked UK",
        ),
        "termination": (
            "Round 1: 6 sc into magic ring (6)\nRepeat until the piece is long enough.\n",
            "Round 1: 6 sc into magic ring (6)\nRepeat until 18 sts.\n",
            "does not terminate",
        ),
        "reach": (
            "Round 1: 6 sc into magic ring (6)\nRound 2: sc in the 9th st (1)\n",
            "Round 1: 6 sc into magic ring (6)\nRound 2: sc in each st around (6)\n",
            "not reachable",
        ),
        "free loop": (
            "Round 1: 6 sc into magic ring (6)\nRound 2: sc in each st around (6)\nUse the unused loop of Round 1.\n",
            "Round 1: 6 sc BLO into magic ring (6)\nRound 2: sc in each st around (6)\nUse the unused loop of Round 1.\n",
            "unused loop of Round 1",
        ),
        "reference": (
            "Round 1: 6 sc into magic ring (6)\nJoin to Round 9.\n",
            "Round 1: 6 sc into magic ring (6)\nJoin to Round 1.\n",
            "Round 9 is named",
        ),
        "piece": (
            "Head\nRound 1: 6 sc into magic ring (6)\nSew the Ear to the Head.\n",
            "Head\nRound 1: 6 sc into magic ring (6)\nEar\nRound 1: 6 sc into magic ring (6)\nSew the Ear to the Head.\n",
            "Piece 'Ear'",
        ),
        "chart": (
            "Chart legend: X = sc, V = dc\nChart row 1: X V X (4)\n",
            "Chart legend: X = sc, V = dc\nChart row 1: X V X V (4)\n",
            "symbols produce 3",
        ),
        "ambiguity": (
            "Round 1: 6 sc into magic ring (6)\nRound 2: sc in next st\n",
            "Round 1: 6 sc into magic ring (6)\nRound 2: sc in each st around (6)\n",
            "does not say how many",
        ),
        "short-row": (
            "Short rows 11a-11c worked over 12 sts.\nThe next round works 28 of 34 perimeter positions.\n",
            "Short rows 11a-11c worked over 12 sts, leaving 6 row-ends.\nThe next round works 28 of 34 perimeter positions.\n",
            "Short-row gap",
        ),
        "closed": (
            "Join 3 stitches of a closed tentacle.\n",
            "Join 3 stitches of an open tentacle edge.\n",
            "closed tentacle",
        ),
        "flat-cap": (
            "Cinch the last round shut and sew it flat to the body.\n",
            "Leave the last round open and sew it flat to the body.\n",
            "sealed cap",
        ),
        "underside": (
            "Join: sc 12, ch 3, sc 12, sc 3 across ch (30)\n",
            "Join: sc 12, ch 3, sc 12, sc 3 across the chain, sc 3 across the underside of the chain (30)\n",
            "Chain underside",
        ),
        "dropped": (
            "Work 21 body stitches from a 24-stitch body.\n",
            "Work 21 body stitches from a 24-stitch body and skip 3.\n",
            "Dropped body",
        ),
        "post": (
            "Switch to gold in FLO, (5 sc, bpdc) x 7\n",
            "Switch to gold in FLO, (5 sc, fpdc) x 7\n",
            "back post",
        ),
        "stuff": (
            "Round 1: 6 sc into magic ring (6)\nStuff the head.\nInsert safety eyes between rounds 6 and 7.\n",
            "Round 1: 6 sc into magic ring (6)\nInsert safety eyes between rounds 6 and 7.\nStuff the head.\n",
            "after stuffing",
        ),
        "row-end": (
            "5 stitches in each row end.\n",
            "sc in each row end.\n",
            "Row-end density",
        ),
        "incoming": (
            "(5 sc, dec) x 6 (36) on 44 stitches.\n",
            "(5 sc, dec) x 6 (36) on 42 stitches.\n",
            "Incoming cover",
        ),
        "color": (
            "Yarn: Color A brown.\nSwitch to Color B for the edging.\n",
            "Yarn: Color A brown and Color B gold.\nSwitch to Color B for the edging.\n",
            "Color B is used",
        ),
        "order": (
            "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\nRound 2: sc in each st around (12)\n",
            "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\nRound 3: sc in each st around (12)\n",
            "repeats or goes backwards",
        ),
        "every": (
            "5 stitches worked into every base stitch.\n",
            "1 stitch worked into every base stitch.\n",
            "worked 5 times",
        ),
        "eyes": (
            "Mount 2 safety eyes on the frill.\n",
            "Mount safety eyes on a solid sc round, not on the frill.\n",
            "mounted on the frill",
        ),
        "frill": (
            "756 stitches worked into 108 base stitches.\n",
            "108 stitches worked into 108 base stitches.\n",
            "Prose frill",
        ),
        "gauge": (
            "Yarn: worsted weight\nGauge: 40 sc = 4 inches\nRound 1: 6 sc into magic ring (6)\n",
            "Yarn: worsted weight\nGauge: 12 sc = 4 inches\nRound 1: 6 sc into magic ring (6)\n",
            "Craft Yarn Council",
        ),
    }
    for name, (wrong, fixed, needle) in cases.items():
        bad = validate_pattern(wrong)
        good = validate_pattern(fixed)
        assert bad.overall_status != "PASS", name
        assert needle in " ".join(_messages(bad)), name
        assert good.overall_status == "PASS", (name, _messages(good))
        assert not good.errors and not good.warnings, name


def test_a_leading_dialect_covers_pieces_that_do_not_redeclare():
    text = "Terms: UK\nHead\nRound 1: 6 sc into magic ring (6)\n"
    report = validate_pattern(text)
    assert any("marked UK" in str(getattr(item, "message", item)) for item in report.errors)


def test_pieces_may_use_different_dialects():
    text = (
        "Head\nTerms: US\nRound 1: 6 sc into magic ring (6)\n\n"
        "Brim\nTerms: UK\nNote: the brim is htr.\n"
    )
    assert run_stages(text).errors == []


def test_photo_and_chart_image_do_not_invent_counts():
    photo = inspect_photo()
    assert photo["automatic_detection"] is False
    assert photo["counts"] is None
    confirmed = inspect_photo(confirmed_stitches=16, confirmed_rows=16)
    assert confirmed["counts"] == {"stitches": 16, "rows": 16}
    assert confirmed["automatic_detection"] is False
    assert read_chart_image()["read"] is False


def test_skipped_engines_stay_named():
    report = run_stages("Round 1: 6 sc into magic ring (6)\n")
    assert report.status == "PASS"
    assert "photo stitch classifier" in report.engines_skipped
    assert "process cluster" in report.engines_skipped
    assert "stitch reachability" in report.engines_ran


def test_lowercase_assembly_words_are_not_missing_pieces():
    text = (
        "Attach the tentacle externally with a sewing seam.\n"
        "Instructions: attach the safety eyes.\n"
        "Round 1: 6 sc into magic ring (6)\n"
    )
    report = validate_pattern(text)
    messages = " ".join(_messages(report))
    assert "Piece" not in messages
