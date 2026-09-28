"""Prove the family checks and the 5,000-sentence case list."""

from crochet_checker.validation.validator import validate_pattern
from crochet_checker.verification.span import PHRASES, proof_cases


def _messages(report):
    return [
        str(getattr(item, "message", item))
        for item in list(report.errors) + list(report.warnings)
    ]


def test_phrase_and_family_lessons_are_proved():
    assert len(PHRASES) == 51
    for item in PHRASES:
        bad = validate_pattern(item.wrong)
        good = validate_pattern(item.corrected)
        assert bad.overall_status != "PASS", item.slug
        assert item.needle in " ".join(_messages(bad)), item.slug
        assert good.overall_status == "PASS", (item.slug, _messages(good))


def test_five_thousand_cases_are_proved():
    cases = proof_cases()
    assert len(cases) == 5000
    for name, wrong, corrected, needle in cases:
        bad = validate_pattern(wrong + "\n")
        good = validate_pattern(corrected + "\n")
        assert bad.overall_status != "PASS", (name, wrong)
        assert needle in " ".join(_messages(bad)), (name, wrong)
        assert good.overall_status == "PASS", (name, corrected, _messages(good))
