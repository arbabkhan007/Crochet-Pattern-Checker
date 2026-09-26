from pathlib import Path

from crochet_checker.learning import LearningStore
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


def test_learning_store_records_case(tmp_path: Path):
    store = LearningStore(str(tmp_path / "learning"))

    pattern = parse_pattern(
        "Round 1: 6 sc into magic ring (6)"
    )
    report = validate_pattern(pattern)

    case = store.record(
        pattern_text=pattern.source_text,
        report=report,
        confirmed=True,
    )

    assert case.case_id
    assert case.confirmed is True
    assert store.statistics()["total_cases"] == 1
    assert store.statistics()["confirmed_cases"] == 1
