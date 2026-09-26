from crochet_checker.ai_providers.quality import AIQualityChecker
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


def test_offline_quality_check():
    text = (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: (sc, inc) x 6 (18)"
    )

    pattern = parse_pattern(text)
    compiler_report = validate_pattern(pattern)
    result = AIQualityChecker(mode="offline").check(
        pattern,
        compiler_report,
    )

    assert result.compiler_valid is True
    assert result.claims
    assert result.confidence >= 0
    assert result.to_dict()["pattern_hash"]


def test_invalid_pattern_is_reported():
    text = (
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: (sc, inc) x 7 (18)"
    )

    pattern = parse_pattern(text)
    compiler_report = validate_pattern(pattern)
    result = AIQualityChecker(mode="offline").check(
        pattern,
        compiler_report,
    )

    assert result.compiler_valid is True or result.compiler_errors
    assert result.to_json()
