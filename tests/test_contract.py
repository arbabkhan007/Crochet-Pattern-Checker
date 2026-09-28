"""Lock the public contract: example statuses, known benchmark findings, and unread lines."""

from pathlib import Path

from crochet_checker.validation.validator import validate_pattern
from crochet_checker.verification.limits import unread_notes
from crochet_checker.verification.verdict import verify_pattern

ROOT = Path(__file__).resolve().parents[1]

EXAMPLES = {
    "amigurumi.txt": ("PASS", 0, 0),
    "amigurumi_bunny.txt": ("PASS", 0, 0),
    "basket.txt": ("PASS", 0, 0),
    "flat_coaster.txt": ("PASS", 0, 0),
    "gradual_bowl.txt": ("PASS", 0, 0),
    "scarf.txt": ("PASS", 0, 0),
    "simple_hat.txt": ("PASS", 0, 0),
    "tube_cowl.txt": ("PASS", 0, 0),
    "baby_booties.txt": ("ERROR", 4, 0),
    "intentionally_broken_pattern.txt": ("ERROR", 3, 0),
    "mini_sphere.txt": ("ERROR", 4, 1),
}


def _messages(report):
    return [str(getattr(item, "message", item)) for item in list(report.errors) + list(report.warnings)]


def test_example_statuses_stay_locked():
    for name, expected in EXAMPLES.items():
        report = validate_pattern((ROOT / "examples" / name).read_text(encoding="utf-8"))
        assert (report.overall_status, len(report.errors), len(report.warnings)) == expected, name


def test_benchmark_findings_are_in_the_source():
    gemini = validate_pattern((ROOT / "docs" / "gemini_corrected.md").read_text(encoding="utf-8"))
    chatgpt = validate_pattern((ROOT / "docs" / "chatgpt_corrected.md").read_text(encoding="utf-8"))
    assert gemini.overall_status == "PASS_WITH_WARNINGS"
    assert len(gemini.errors) == 0 and len(gemini.warnings) == 1
    assert "row-end" in _messages(gemini)[0]
    assert chatgpt.overall_status == "ERROR"
    assert len(chatgpt.errors) == 1 and len(chatgpt.warnings) == 0
    assert "3 stitches cannot close 4" in _messages(chatgpt)[0]


def test_six_to_eighteen_is_not_a_valid_sphere():
    bad = validate_pattern(
        "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n"
    )
    good = validate_pattern(
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: inc x 6 (12)\n"
        "Round 3: (sc, inc) x 6 (18)\n"
    )
    assert bad.overall_status == "ERROR"
    assert any("6 to 18" in message for message in _messages(bad))
    assert good.overall_status == "PASS"


def test_unread_lines_are_disclosed_and_not_errors():
    text = "Round 1: 6 sc into magic ring (6)\nCinch shut.\nsew head to body.\n"
    report = validate_pattern(text)
    notes = unread_notes(text)
    verdict = verify_pattern(text)
    assert report.overall_status == "PASS"
    assert any("cinch" in note.lower() for note in notes)
    assert any("lowercase sew" in note.lower() for note in notes)
    assert verdict.not_checked == notes
    assert "photo stitch classifier" in verdict.engines_skipped


def test_a_zero_hook_is_an_error_in_any_sentence():
    bad = validate_pattern("Use a hook of 0 mm.\nRound 1: 6 sc into magic ring (6)\n")
    exact = validate_pattern("Hook: 0 mm.\n")
    banned = validate_pattern("Do not use a 0 mm hook.\nRound 1: 6 sc into magic ring (6)\n")
    sized = validate_pattern("Hook: 3.0 mm\nRound 1: 6 sc into magic ring (6)\n")
    eyes = validate_pattern("10 mm safety eyes (x2)\nRound 1: 6 sc into magic ring (6)\n")
    quoted = validate_pattern("> Hook: 0 mm is impossible.\nRound 1: 6 sc into magic ring (6)\n")
    assert bad.overall_status == "ERROR"
    assert any("0 mm cannot make a stitch" in message for message in _messages(bad))
    assert exact.overall_status == "ERROR"
    assert len(exact.errors) == 1
    assert banned.overall_status == "PASS"
    assert sized.overall_status == "PASS"
    assert eyes.overall_status == "PASS"
    assert quoted.overall_status == "PASS"


def test_an_uncounted_instruction_is_named_and_not_an_error():
    text = (
        "Next, make a round of single crochet increases "
        "until the piece measures 18 stitches.\n"
    )
    report = validate_pattern(text)
    notes = unread_notes(text)
    assert report.overall_status == "PASS"
    assert not report.errors and not report.warnings
    assert any(note.startswith("Not counted:") for note in notes)
    sphere = (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: inc x 6 (12)\n"
        "Round 3: (sc, inc) x 6 (18)\n"
    )
    assert unread_notes(sphere) == []
    assert validate_pattern(sphere).overall_status == "PASS"


def test_zero_work_paraphrases_are_errors():
    chain = validate_pattern('Make a chain of 0 before the first stitch.\n')
    work = validate_pattern('Work zero stitches in this round.\n')
    skip = validate_pattern('Skip zero stitches, then sc.\n')
    repeat = validate_pattern('Repeat this zero times.\n')
    hook = validate_pattern('The hook is 5 cm.\n')
    safe = validate_pattern('Do not make a chain of 0.\nch 10, then sc in the next stitch.\nWork 6 stitches.\nSkip 2 stitches.\nRound 1: 6 sc into magic ring (6)\n')
    gauge = validate_pattern('Gauge: 20 sts and 22 rnds = 4 inches (10 cm) in sc with a 3.5 mm hook.\nRound 1: 6 sc into magic ring (6)\n')
    assert chain.overall_status == "ERROR"
    assert any("makes no chain" in message for message in _messages(chain))
    assert any("does no work" in message for message in _messages(work))
    assert any("does not move the hook" in message for message in _messages(skip))
    assert any("repeat of zero" in message for message in _messages(repeat))
    assert any("centimeters" in message for message in _messages(hook))
    assert len(validate_pattern('Hook: 5 cm.\n').errors) == 1
    assert safe.overall_status == "PASS"
    assert gauge.overall_status == "PASS"
    assert "centimeters" not in " ".join(_messages(gauge))


def test_large_hook_and_zero_words_are_not_one_sentence():
    huge = validate_pattern('Use a 40 mm hook for this piece.\n')
    exact = validate_pattern('Hook: 40 mm.\n')
    small = validate_pattern('Use a 3.5 mm hook.\nRound 1: 6 sc into magic ring (6)\n')
    chain = validate_pattern('Chain zero, then single crochet.\n')
    work = validate_pattern('Work 0 in the next round.\n')
    cm = validate_pattern('The hook measures 5 centimeters.\n')
    banned = validate_pattern('Do not use a 5 centimeter hook.\nRound 1: 6 sc into magic ring (6)\n')
    quoted = validate_pattern('> Use a 40 mm hook.\nRound 1: 6 sc into magic ring (6)\n')
    assert huge.overall_status == "PASS_WITH_WARNINGS"
    assert any("40 mm or more" in message for message in _messages(huge))
    assert len(exact.warnings) == 1
    assert small.overall_status == "PASS"
    assert any("makes no chain" in message for message in _messages(chain))
    assert any("does no work" in message for message in _messages(work))
    assert any("centimeters" in message for message in _messages(cm))
    assert banned.overall_status == "PASS"
    assert quoted.overall_status == "PASS"


def test_spoken_zero_and_one_are_the_same_defects():
    dec = validate_pattern('Decrease five times across eleven stitches.\n')
    ok = validate_pattern('Decrease six times across twelve stitches.\n')
    round_zero = validate_pattern('The piece starts at Round zero.\n')
    shell = validate_pattern('Work a shell of one.\n')
    make = validate_pattern('Ears (make zero).\n')
    yo = validate_pattern('yo zero, then pull through.\n')
    small = validate_pattern('Use a 3.5 mm hook.\nRound 1: 6 sc into magic ring (6)\n')
    bad = validate_pattern('Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n')
    quoted = validate_pattern('> Work a shell of one.\nRound 1: 6 sc into magic ring (6)\n')
    banned = validate_pattern('Do not chain zero.\nRound 1: 6 sc into magic ring (6)\n')
    assert any("uses 10 stitches, not 11" in message for message in _messages(dec))
    assert ok.overall_status == "PASS"
    assert any("Round 0 is not a round" in message for message in _messages(round_zero))
    assert any("not a shell" in message for message in _messages(shell))
    assert any("Make 0" in message for message in _messages(make))
    assert any("yo 0" in message for message in _messages(yo))
    assert small.overall_status == "PASS"
    assert bad.overall_status == "ERROR"
    assert any("6 to 18" in message for message in _messages(bad))
    assert quoted.overall_status == "PASS"
    assert banned.overall_status == "PASS"


def test_spoken_counts_match_the_digit_checks():
    inc = validate_pattern('Increase from twelve to six.\n')
    ok_inc = validate_pattern('Increase from six to twelve.\n')
    mid = validate_pattern('Then increase from 10 to 4.\n')
    mult = validate_pattern('Use a multiple of six, nineteen stitches.\n')
    ok_mult = validate_pattern('Multiple of six, eighteen stitches.\n')
    apart = validate_pattern('Place the eyes twelve stitches apart on a six-stitch round.\n')
    skipped = validate_pattern('Skip none of the stitches.\n')
    hook = validate_pattern('Use hook H/8 (2.25 mm).\n')
    ok_hook = validate_pattern('Use hook H/8 (5 mm).\n')
    small = validate_pattern('Use a 3.5 mm hook.\n')
    gauge = validate_pattern('Gauge: 14 sc = 4 inches (10 cm).\nHook: 5 mm.\n')
    turn = validate_pattern('ch one, turn, tr in the next stitch.\n')
    ok_turn = validate_pattern('ch 1, turn, sc in the next stitch.\n')
    quoted = validate_pattern('> Increase from twelve to six.\n')
    banned = validate_pattern('Do not increase from twelve to six.\n')
    bad = validate_pattern('Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n')
    huge = validate_pattern('Use a forty mm hook.\n')
    assert any("does not rise" in message for message in _messages(inc))
    assert ok_inc.overall_status == "PASS"
    assert any("10 to 4" in message for message in _messages(mid))
    assert any("not divisible" in message for message in _messages(mult))
    assert ok_mult.overall_status == "PASS"
    assert any("do not fit" in message for message in _messages(apart))
    assert skipped.overall_status == "PASS"
    assert any("more than 1.5 mm" in message for message in _messages(hook))
    assert ok_hook.overall_status == "PASS"
    assert small.overall_status == "PASS"
    assert gauge.overall_status == "PASS"
    assert any("too short to turn" in message for message in _messages(turn))
    assert ok_turn.overall_status == "PASS"
    assert quoted.overall_status == "PASS"
    assert banned.overall_status == "PASS"
    assert bad.overall_status == "ERROR"
    assert any("6 to 18" in message for message in _messages(bad))
    assert huge.overall_status == "PASS_WITH_WARNINGS"
    assert len(huge.errors) == 0 and len(huge.warnings) == 1
