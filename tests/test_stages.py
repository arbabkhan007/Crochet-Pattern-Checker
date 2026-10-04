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


def test_a_line_cannot_state_two_endings():
    blob = lambda text: " ".join(_messages(validate_pattern(text)))
    two = "Round 2: sc in each st around (12 sts) (18 sts)\n"
    same = "Round 2: sc in each st around (12 sts) (12 sts)\n"
    shut = "Round 1: 6 sc into magic ring (6)\nCinch shut and leave the opening open.\n"
    held = "Cinch 6 held stitches to 6 body stitches.\n"
    endings = "Finish with an invisible join and sl st to join.\n"
    one_end = "Finish with an invisible join.\n"
    spiral = "Work in a continuous spiral and join every round.\n"
    no_join = "Work in a continuous spiral and do not join.\n"
    later = (
        "Work in a continuous spiral.\n"
        "Join with a slip stitch at the end of each round.\n"
    )
    banned = (
        "HEAD\nRound 1: 6 sc into magic ring (6)\nDo not stuff.\nStuff the head firmly.\n"
    )
    allowed = (
        "EAR\nRound 1: 6 sc into magic ring (6)\nDo not stuff.\n"
        "HEAD\nRound 1: 6 sc into magic ring (6)\nStuff the head.\n"
    )
    copies = "Ears (make 2)\nEars (make 3)\nRound 1: 6 sc into magic ring (6)\n"
    once = "Ears (make 2)\nRound 1: 6 sc into magic ring (6)\n"
    quoted = "> Round 2: sc around (12 sts) (18 sts)\nRound 1: 6 sc into magic ring (6)\n"
    assert "more than one stitch count" in blob(two)
    assert "more than one stitch count" not in blob(same)
    assert "leaves it open" in blob(shut)
    assert "leaves it open" not in blob(held)
    assert "two endings" in blob(endings)
    assert "two endings" not in blob(one_end)
    assert "does not join every round" in blob(spiral)
    assert "does not join every round" not in blob(no_join)
    assert "does not join every round" in blob(later)
    assert "not to stuff, then stuffs" in blob(banned)
    assert "not to stuff, then stuffs" not in blob(allowed)
    assert "make 2 and make 3" in blob(copies)
    assert "make 2 and make 3" not in blob(once)
    assert "more than one stitch count" not in blob(quoted)


def test_a_contradiction_is_caught_in_any_sentence():
    blob = lambda text: " ".join(_messages(validate_pattern(text)))
    assert "different counts" in blob("Repeat six (5) times.\n")
    assert "different counts" not in blob("Repeat six (6) times.\n")
    assert "different counts" not in blob("Round one (6)\nRound 1: 6 sc into magic ring (6)\n")
    assert "same stitch" in blob("Work the next stitch in FLO and BLO.\n")
    assert "same stitch" not in blob("Round 2: sc in BLO, sc in FLO (12)\n")
    assert "both directions" in blob("Work the round in both directions.\n")
    assert "both directions" not in blob("Work left to right or right to left.\n")
    assert "cannot both face" in blob("Keep the right side and the wrong side facing.\n")
    assert "cannot both face" not in blob("With the right side facing.\n")
    assert "yarn under" in blob("Yarn over and yarn under the same stitch.\n")
    assert "yarn under" not in blob("Work yarn over for the same stitch.\n")
    assert "not forward" in blob("Reverse single crochet worked forward.\n")
    assert "not forward" not in blob("Reverse sc worked backward.\n")
    assert "separate instructions" in blob("Work this row right-handed and left-handed.\n")
    assert "separate instructions" not in blob("Written for right-handed work.\n")
    assert "two seams" in blob("Sew with a whipstitch and a mattress stitch.\n")
    assert "two seams" not in blob("Seam with mattress stitch.\n")
    assert "chain ring" in blob("Begin with a magic ring and a chain ring.\n")
    assert "chain ring" not in blob("Round 1: 6 sc into magic ring (6)\n")
    assert "two fabrics" in blob("Work in the round and back and forth.\n")
    assert "Rows are worked across" in blob("Row 4: sc in each stitch around.\n")
    assert "Rows are worked across" not in blob("Round 4: sc in each st around (12)\n")
    assert "negative measure" in blob("The piece is 8 inches long and -8 inches long.\n")
    assert "negative measure" not in blob("The cuff is 1-2 inches.\n")
    assert "not converted" in blob("The edge is 4 inches, which is 4 cm.\n")
    assert "not converted" not in blob("Gauge: 20 sts = 4 inches (10 cm).\n")
    assert "does not stuff" in blob("Stuff the head and do not stuff the head.\n")
    assert "does not stuff" not in blob("Do not stuff.\n")
    assert "does not turn" in blob("Turn the row and do not turn the row.\n")
    quoted = "> Work the round in both directions.\nRound 1: 6 sc into magic ring (6)\n"
    assert "both directions" not in blob(quoted)


def test_nearby_wording_uses_the_same_rule():
    blob = lambda text: " ".join(_messages(validate_pattern(text)))
    assert "more than 1.5 mm" in blob("Use an H/8 (2.25 mm) hook.\n")
    assert "more than 1.5 mm" not in blob("Use an H/8 (5 mm) hook.\n")
    assert "more than 1.5 mm" not in blob("Use a 3.5 mm hook.\n")
    assert "category 4, not 1" in blob("Yarn: worsted weight (1).\n")
    assert "category 4, not 1" not in blob("Yarn: worsted weight (4).\n")
    assert "not a UK treble" in blob("A US sc is a UK treble.\n")
    assert "not a UK treble" not in blob("A US sc is a UK double.\n")
    assert "smaller, not larger" in blob("Steel hook 14 is larger than steel hook 1.\n")
    assert "smaller, not larger" not in blob("Steel hook 14 is smaller than steel hook 1.\n")
    assert "must be even" in blob("The count must be even: 7 stitches.\n")
    assert "must be even" not in blob("The count must be even (8 stitches).\n")
    assert "past a 6-stitch" in blob("Work stitch 12 of the 6-stitch round.\n")
    assert "past a" not in blob("Work stitch 4 of the 24-stitch round.\n")
    assert "do not fit" in blob("The eyes are 10 stitches apart on an 8-stitch round.\n")
    assert "does not fit" in blob("Skip 8 stitches on a 6-stitch row.\n")
    assert "too short to turn for a dc" in blob("ch 2, turn, dc in the next stitch.\n")
    assert "too short to turn for a dc" not in blob("ch 3, turn, dc in the next stitch.\n")
    assert "too short to turn" not in blob("Row 2: ch 1, turn, sc in each st across (19)\n")
    assert "not a stitch" in blob("The slip knot counts as stitch 1.\n")
    assert "not a color change" in blob("Switch to Color B, then switch to Color B.\n")
    assert "not a color change" not in blob("Switch to Color B, then switch to Color A.\n")
    assert "does not terminate" in blob("Keep going until it looks long enough.\n")
    assert "does not terminate" not in blob("Repeat until the piece is 8 inches long.\n")
    assert "not a UK treble" not in blob("> A US sc is a UK treble.\nRound 1: 6 sc into magic ring (6)\n")


def test_remaining_copied_rules_apply_in_any_sentence():
    blob = lambda text: " ".join(_messages(validate_pattern(text)))
    assert "plus 2" in blob("It needs a multiple of 6 plus 2, and the count is 21 stitches.\n")
    assert "plus 2" not in blob("Multiple of 6 plus 2, 20 stitches.\n")
    assert "same stitch" in blob("Increase and decrease in every stitch.\n")
    assert "added two times" in blob("The chain is counted twice in the total.\n")
    assert "added two times" not in blob("The turning chain counts once.\n")
    assert "0 inches is not" in blob("The finished width is 0 inches.\n")
    assert "not a whole stitch" in blob("sc 1.5 in the next stitch.\n")
    assert "not a whole stitch" not in blob("Use a 3.5 mm hook.\n")
    assert "not a whole repeat" in blob("Repeat the shell 1.5 times.\n")
    assert "not a whole repeat" not in blob("The wing is about 2.1 times the socket.\n")
    assert "negative repeat" in blob("Repeat the row -2 times.\n")
    assert "negative repeat" not in blob("Repeat 1-2 times.\n")
    assert "not a usable round" in blob("Round 400: sc around.\n")
    assert "not a usable round" not in blob("Round 29: sc around (6)\n")
    assert "both loops" in blob("Work BLO only and through both loops of that stitch.\n")
    assert "both loops" not in blob("Work BLO or both loops.\n")
    assert "no post" in blob("Work a front post around the chain.\n")
    assert "not a chain stitch" in blob("Count the slip knot as the first stitch.\n")
    assert "not continued" in blob("Fasten off, then continue in that same yarn.\n")
    assert "replaces the starting chain" in blob("Use foundation single crochet and also a starting chain for this row.\n")
    assert "replaces the starting chain" not in blob("Use foundation single crochet or a starting chain.\n")
    assert "does not join every round" in blob("This spiral also slip stitches the round closed.\n")
    assert "past a 6-stitch" in blob("The marker goes in stitch 9 of 6.\n")
    assert "do not fit" in blob("Place the eyes 10 stitches apart on a round of 6 stitches.\n")
    assert "does not fit" in blob("Skip 8 on a row of 6 stitches.\n")
    assert "must be even" in blob("Keep an even count of 7 stitches.\n")
    assert "must be odd" in blob("Keep an odd count of 8 stitches.\n")
    assert "more than 1.5 mm" in blob("Hook H 8 is 2.25 mm.\n")
    assert "more than 1.5 mm" not in blob("Hook H 8 is 5 mm.\n")
    assert "category 4, not 1" in blob("This is a category 1 worsted yarn.\n")
    assert "category 4, not 1" not in blob("This is a category 4 worsted yarn.\n")
    assert "written in centimeters" in blob("Use a five centimeter hook.\n")
    assert "not a fabric" in blob("Gauge is zero sc per 4 inches.\n")
    assert "not a UK treble" in blob("A US hdc is a UK treble.\n")
    assert "not a shell" in blob("Work a shell of 2 dc.\n")
    assert "not a shell" not in blob("Work a shell of 5.\n")
    assert "no chains to work into" in blob("sc in the chain 0 space.\n")
    assert "plus 2" not in blob("> It needs a multiple of 6 plus 2, and the count is 21 stitches.\n")


def test_zero_and_word_gaps_are_named():
    blob = lambda text: " ".join(_messages(validate_pattern(text)))
    assert "does not terminate" in blob("Repeat until done.\n")
    assert "does not terminate" not in blob("Repeat until 6 stitches.\n")
    assert "does not cross" in blob("Cross a cable of 0 stitches.\n")
    assert "does not cross" not in blob("Cable over 2 stitches.\n")
    assert "no cord" in blob("Make an icord of 0 stitches.\n")
    assert "no cord" not in blob("I-cord of 4 stitches.\n")
    assert "does not leave" in blob("Work a spike down 0 rows.\n")
    assert "does not leave" not in blob("Spike stitch down 2 rows.\n")
    assert "draws no line" in blob("Surface crochet 0 stitches.\n")
    assert "draws no line" not in blob("Surface crochet of 12 chains.\n")
    assert "nothing to tie" in blob("Make a pompom of 0 wraps.\n")
    assert "nothing to tie" not in blob("Pom-pom of 40 wraps.\n")
    assert "does not fill" in blob("Stuff with 0 ounces.\n")
    assert "not a piece" in blob("Ears (make -1).\n")
    assert "not a piece" not in blob("Ears (make 2).\n")
    assert "Start at 1" in blob("Row -1: sc across (6).\n")
    assert "Start at 1" not in blob("Row 1: sc across (6).\n")
    assert "not a shell" in blob("Work a shell of zero.\n")
    assert "no post" in blob("fpdc around ch 4.\n")
    assert "no post" not in blob("fpdc around the dc.\n")
    assert "same stitch" in blob("Work FLO only and both loops of that stitch.\n")
    assert "same stitch" not in blob("Work FLO or both loops.\n")
    assert "The join was not added" in blob("Work continuous rounds and join each round with a slip stitch.\n")
    assert "The join was not added" not in blob("Worked in continuous rounds.\n")
    assert "two fabrics" in blob("Work this piece in the round and in rows.\n")
    assert "two fabrics" not in blob("Work this piece in the round or in rows.\n")
    assert "not continued" in blob("Fasten off and keep working the next round.\n")
    assert "stitch 1" in blob("Place the marker at stitch zero.\n")
    assert "does not fit" in blob("Skip twelve on a row of six stitches.\n")
    assert "does not fit" not in blob("Skip two on a row of six stitches.\n")
    assert "do not fit" in blob("Place the eyes twelve stitches apart on a round of six stitches.\n")
    assert "leaves the piece empty" in blob("Stuff the head and leave the head empty.\n")
    assert "does not terminate" not in blob("> Repeat until done.\nRound 1: 6 sc into magic ring (6)\n")


def test_other_wording_uses_the_same_rule():
    blob = lambda text: " ".join(_messages(validate_pattern(text)))
    assert "more than 1.5 mm" in blob("Hook H/8 is 2.25 mm.\n")
    assert "more than 1.5 mm" not in blob("Hook H/8 is 5 mm.\n")
    assert "too short to turn" in blob("Ch 1, turn for dc.\n")
    assert "too short to turn" not in blob("ch 3, turn for dc.\n")
    assert "cannot count as a dc" in blob("ch 1 counts as dc.\n")
    assert "cannot count as a dc" not in blob("ch 3 counts as a dc.\n")
    assert "not a V-stitch" in blob("A V-stitch of one.\n")
    assert "not a V-stitch" not in blob("Work a V-stitch of 2 dc.\n")
    assert "not a fan" in blob("Fan of 1.\n")
    assert "not a fan" not in blob("Work a fan of 5.\n")
    assert "cannot make a star" in blob("A star stitch of one.\n")
    assert "not a cluster" in blob("A cluster of one dc.\n")
    assert "not a cluster" not in blob("Work a cluster of 3.\n")
    assert "no loop" in blob("A loop of zero.\n")
    assert "no loop" not in blob("Work a loop stitch of 1.\n")
    assert "0 chains" in blob("Start the oval with zero chains.\n")
    assert "0 chains" not in blob("Oval start with 8 chains.\n")
    assert "0 rows" in blob("The rectangle is zero rows.\n")
    assert "0 rows" not in blob("Rectangle of 12 rows.\n")
    assert "double and single" in blob("Hold the yarn doubled and single.\n")
    assert "double and single" not in blob("Work yarn double or single.\n")
    assert "do not fit" in blob("Eyes twelve apart on a round of six stitches.\n")
    assert "do not fit" not in blob("Eyes two apart on a round of six stitches.\n")
    assert "starting chain" in blob("Foundation sc and also chain 20 to start.\n")
    assert "starting chain" not in blob("Start with foundation sc.\n")
    assert "not a fringe" in blob("Make a fringe using no strands.\n")
    assert "more than 1.5 mm" not in blob("> Hook H/8 is 2.25 mm.\n")


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


def test_none_and_made_of_use_the_same_rule():
    errors = [
        "Work no stitches.",
        "Round none.",
        "Corner made of zero chains.",
        "ch one, turn for dc.",
        "Rounds 8 to 5.",
        "Steel hook 7 is bigger than steel 1.",
    ]
    for line in errors:
        result = validate_pattern(line + "\n")
        assert result.errors, line
    for line in (
        "No stitches are left unworked.",
        "Rounds 1 to 8.",
        "ch three, turn for dc.",
        "Back loop only or both loops.",
        "> Work no stitches.",
    ):
        assert validate_pattern(line + "\n").errors == [], line

def test_abbreviations_use_the_same_rule():
    errors = [
        "Inc from 12 to 6.",
        "Rnd 8 to rnd 5.",
        "Change from colour C to colour C.",
        "The ch-1 counts as dc.",
        "Magic circle and a chain ring.",
        "H/8 measures 2.25 mm.",
    ]
    for line in errors:
        result = validate_pattern(line + "\n")
        assert result.errors, line
    for line in (
        "Increase 6 to 12.",
        "Rounds 1 to 8.",
        "Change from colour C to colour D.",
        "The ch-3 counts as dc.",
        "Magic ring or a chain ring.",
        "H-8 measures 5.0 mm.",
        "> Inc from 12 to 6.",
    ):
        assert validate_pattern(line + "\n").errors == [], line

def test_glued_forms_use_the_same_rule():
    errors = [
        "ch1, turn for dc.",
        "8in = 8cm.",
        "H/8 = 2.25mm.",
        "Decrease from 6 up to 12.",
        "Eyes placed 8 sts apart on a 6-st round.",
    ]
    for line in errors:
        result = validate_pattern(line + "\n")
        assert result.errors, line
    for line in (
        "ch 3, turn, dc.",
        "4 inches = 10.16 cm.",
        "H-8 = 5.0mm.",
        "Increase from 6 up to 12.",
        "Eyes placed 2 sts apart on a 6-st round.",
        "Turn inside out.",
        "> ch1, turn for dc.",
    ):
        assert validate_pattern(line + "\n").errors == [], line
