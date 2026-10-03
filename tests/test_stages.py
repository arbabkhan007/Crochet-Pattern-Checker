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
        "chain-short": (
            "Row 1: ch 10, sc in 2nd ch from hook, sc in each ch across (12)\n",
            "Row 1: ch 10, sc in 2nd ch from hook, sc in each ch across (9)\n",
            "cannot hold",
        ),
        "paren": (
            "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\nRound 3: (sc, inc x 6 (18)\n",
            "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\nRound 3: (sc, inc) x 6 (18)\n",
            "unclosed",
        ),
        "star": (
            "Rep from * around.\n",
            "*sc, inc* rep from * around.\n",
            "opening star",
        ),
        "dec-cover": (
            "dec x 5 on 11 stitches.\n",
            "dec x 5 on 10 stitches.\n",
            "Decrease cover",
        ),
        "double": (
            "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n",
            "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\nRound 3: (sc, inc) x 6 (18)\n",
            "More than doubling",
        ),
        "written-as": (
            "Graft a 30-stitch partition into a round written as 38.\n",
            "Graft a 30-stitch partition into a round written as 30.\n",
            "Written count",
        ),
        "eye-count": (
            "10 mm safety eyes (x2)\nMount 4 safety eyes between rounds 6 and 7.\n",
            "10 mm safety eyes (x2)\nMount 2 safety eyes between rounds 6 and 7.\n",
            "Eye count",
        ),
        "future": (
            "Round 1: 6 sc into magic ring (6)\nRound 2: sc in each st around to Round 5 (6)\nRound 5: sc in each st around (6)\n",
            "Round 1: 6 sc into magic ring (6)\nRound 2: sc in each st around (6)\nRound 3: sc in each st around (6)\nRound 4: sc in each st around (6)\nRound 5: sc in each st around (6)\nRound 6: sc in each st around to Round 5 (6)\n",
            "has not been made",
        ),
        "make-count": (
            "Ears (make 2)\nRound 1: 6 sc into magic ring (6)\nSew 3 ears to the head.\n",
            "Ears (make 2)\nRound 1: 6 sc into magic ring (6)\nSew 2 ears to the head.\n",
            "Make count",
        ),
        "zero": (
            "Repeat x 0.\n",
            "Repeat x 6.\n",
            "repeat of zero",
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


def test_written_seam_rules_do_not_invent_a_join():
    leaked = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\n"
        "BODY\nRound 1: sc in each st of the HEAD (6)\n"
    )
    isolated = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\n"
        "BODY\nRound 1: 6 sc into magic ring (6)\n"
    )
    missing_edge = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\nSew 9 stitches of the head to the body.\n"
    )
    stated_edge = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\nSew 6 stitches of the head to the body.\n"
    )
    closed = "Round 1: 6 sc into magic ring (6)\nSew the ears to the magic ring.\n"
    open_edge = "Round 1: 6 sc into magic ring (6)\nSew the ears to the head.\n"
    branch = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\n"
        "BODY\nRound 1: 6 sc into magic ring (6)\n"
        "EARS\nRound 1: 6 sc into magic ring (6)\n"
        "Sew head, body, and ears together.\n"
    )
    pair = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\n"
        "BODY\nRound 1: 6 sc into magic ring (6)\n"
        "EARS\nRound 1: 6 sc into magic ring (6)\n"
        "Sew the ears to the head.\n"
    )
    quoted = "> Sew the ears to the magic ring.\nRound 1: 6 sc into magic ring (6)\n"
    assert "outside this round" in " ".join(_messages(validate_pattern(leaked)))
    assert "outside this round" not in " ".join(_messages(validate_pattern(isolated)))
    assert "edge was not invented" in " ".join(_messages(validate_pattern(missing_edge)))
    assert "edge was not invented" not in " ".join(_messages(validate_pattern(stated_edge)))
    assert "closed magic ring" in " ".join(_messages(validate_pattern(closed)))
    assert "closed magic ring" not in " ".join(_messages(validate_pattern(open_edge)))
    assert "Y-branch was not drawn" in " ".join(_messages(validate_pattern(branch)))
    assert "Y-branch was not drawn" not in " ".join(_messages(validate_pattern(pair)))
    assert validate_pattern(quoted).overall_status == "PASS"


def test_a_piece_does_not_continue_after_it_ends():
    continued = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\n"
        "Fasten off.\nRound 2: sc in each st around (6)\n"
    )
    restarted = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\nFasten off.\n"
        "EAR\nRound 1: 6 sc into magic ring (6)\n"
    )
    kept = (
        "Rounds 1-12, leg 1: 12 sc around. Fasten off leg 1. "
        "Keep the working yarn on leg 2.\n"
        "Round 13: sc 12 around leg 2 (12)\n"
    )
    other_part = (
        "Rounds 1-12, Leg 1: 12 sc around. Fasten off, leaving a tail.\n"
        "Rounds 1-12, Leg 2: 12 sc around. (12)\n"
    )
    self_join = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\nSew the head to the head.\n"
    )
    other_join = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\n"
        "BODY\nRound 1: 6 sc into magic ring (6)\nSew the head to the body.\n"
    )
    turned = "Round 2: sc in each st around, turn (6)\n"
    row_turn = "Row 2: sc in each st across, turn (6)\n"
    quoted = "> Fasten off.\n> Round 2: sc in each st around, turn (6)\nRound 1: 6 sc into magic ring (6)\n"
    assert "ended this yarn" in " ".join(_messages(validate_pattern(continued)))
    assert "ended this yarn" not in " ".join(_messages(validate_pattern(restarted)))
    assert "ended this yarn" not in " ".join(_messages(validate_pattern(kept)))
    assert "ended this yarn" not in " ".join(_messages(validate_pattern(other_part)))
    assert "piece to itself" in " ".join(_messages(validate_pattern(self_join)))
    assert "piece to itself" not in " ".join(_messages(validate_pattern(other_join)))
    assert "does not turn" in " ".join(_messages(validate_pattern(turned)))
    assert "does not turn" not in " ".join(_messages(validate_pattern(row_turn)))
    assert "ended this yarn" not in " ".join(_messages(validate_pattern(quoted)))
    assert "does not turn" not in " ".join(_messages(validate_pattern(quoted)))


def test_a_closed_piece_is_not_worked_again():
    stuffed = (
        "Round 1: 6 sc into magic ring (6)\nCinch shut.\nStuff the head.\n"
    )
    eyed = (
        "Round 1: 6 sc into magic ring (6)\nCinch shut.\n"
        "Insert safety eyes between rounds 4 and 5.\n"
    )
    continued = (
        "Round 1: 6 sc into magic ring (6)\nCinch shut.\n"
        "Round 2: sc in each st around (6)\n"
    )
    before = (
        "Round 1: 6 sc into magic ring (6)\nStuff the head.\n"
        "Insert safety eyes between rounds 4 and 5.\nCinch shut.\n"
    )
    restarted = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\nCinch shut.\n"
        "EAR\nRound 1: 6 sc into magic ring (6)\nStuff the ear lightly.\n"
    )
    joined = "Cinch 6 held stitches to 6 body stitches.\nMount 2 safety eyes on the body.\n"
    twice = (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: 6 sc into magic ring (6)\n"
    )
    two_pieces = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\n"
        "EAR\nRound 1: 6 sc into magic ring (6)\n"
    )
    both_counts = "ch 3 counts as a dc and does not count as a dc.\n"
    one_count = "ch 3 counts as a dc.\n"
    both_endings = "Fasten off and do not fasten off.\n"
    one_ending = "Do not fasten off.\nRound 1: 6 sc into magic ring (6)\n"
    quoted = "> Cinch shut.\n> Stuff the head.\nRound 1: 6 sc into magic ring (6)\n"
    blob = lambda text: " ".join(_messages(validate_pattern(text)))
    assert "closed this piece" in blob(stuffed)
    assert "closed this piece" in blob(eyed)
    assert "closed this piece" in blob(continued)
    assert "closed this piece" not in blob(before)
    assert "closed this piece" not in blob(restarted)
    assert "closed this piece" not in blob(joined)
    assert "second magic ring" in blob(twice)
    assert "second magic ring" not in blob(two_pieces)
    assert "does not count" in blob(both_counts)
    assert "does not count" not in blob(one_count)
    assert "does not fasten off" in blob(both_endings)
    assert "does not fasten off" not in blob(one_ending)
    assert "closed this piece" not in blob(quoted)


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


def test_fifty_phrase_rules():
    from crochet_checker.verification.batch import RULES

    assert len(RULES) == 50
    for rule in RULES:
        bad = validate_pattern(rule.wrong)
        good = validate_pattern(rule.corrected)
        blob = " ".join(_messages(bad))
        assert bad.overall_status != "PASS", rule.slug
        assert rule.needle in blob, rule.slug
        assert good.overall_status == "PASS", (rule.slug, _messages(good))
