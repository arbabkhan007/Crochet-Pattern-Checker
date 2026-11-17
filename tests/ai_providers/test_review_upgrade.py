import json

import pytest

from crochet_checker.ai_providers.review import parse_review_response

PATTERN = "Round 1: 6 sc into magic ring (6)"


def payload(**overrides):
    value = {
        "summary": "Reviewed the written instruction.",
        "coverage": [
            {
                "scope": "stitch arithmetic",
                "status": "reviewed",
                "reason": "The line states six stitches.",
                "evidence_quote": PATTERN,
            }
        ],
        "findings": [],
        "assessments": [],
        "open_questions": [],
    }
    value.update(overrides)
    return json.dumps(value)


def parse(text):
    return parse_review_response(
        text,
        provider_id="provider-a",
        model="test-model",
        phase="independent",
        role="stitch_arithmetic",
        reviewer_alias="Reviewer A",
        pattern_text=PATTERN,
    )


def test_requires_nonempty_source_grounded_review_coverage():
    review = parse(payload())
    assert review.coverage[0].evidence_status == "grounded_text"
    assert review.findings == []

    with pytest.raises(ValueError, match="coverage"):
        parse(payload(coverage=[]))
    with pytest.raises(ValueError, match="not grounded"):
        parse(
            payload(
                coverage=[
                    {
                        "scope": "arithmetic",
                        "status": "reviewed",
                        "reason": "check",
                        "evidence_quote": "Round 4: invented",
                    }
                ]
            )
        )


def test_grounding_rejects_fabricated_finding_even_with_plausible_claim():
    finding = {
        "location": "Round 1",
        "line_number": 1,
        "source_instruction": "Round 1: 6 sc into magic ring (6)",
        "category": "arithmetic",
        "issue_code": "wrong_total",
        "issue": "Count mismatch",
        "expected_count": 6,
        "actual_count": 9,
        "severity": "major",
        "explanation": "The written count differs.",
        "proposed_correction": "(6)",
        "confidence": 0.99,
        "evidence_quote": "Round 1: 6 sc into magic ring (6)",
    }
    review = parse(payload(findings=[finding]))
    assert review.findings[0].evidence_status == "grounded_text"
    assert review.findings[0].matched_line_number == 1

    finding["evidence_quote"] = "Round 1: nine stitches (9)"
    review = parse(payload(findings=[finding]))
    assert review.findings[0].evidence_status == "not_found"

    second_line = "Round 2: (sc, inc) x 6 (18)"
    finding["source_instruction"] = second_line
    finding["evidence_quote"] = PATTERN
    mismatch = parse_review_response(
        payload(findings=[finding]),
        provider_id="provider-a",
        model="test-model",
        phase="independent",
        role="stitch_arithmetic",
        reviewer_alias="Reviewer A",
        pattern_text=PATTERN + "\n" + second_line,
    )
    assert mismatch.findings[0].evidence_status == "source_instruction_mismatch"


def test_finding_schema_and_confidence_are_strict():
    with pytest.raises(ValueError, match="missing required"):
        parse(payload(findings=[{"location": "Round 1"}]))
    with pytest.raises(ValueError, match="confidence"):
        finding = {
            "location": "Round 1",
            "source_instruction": PATTERN,
            "expected_count": None,
            "actual_count": None,
            "severity": "major",
            "explanation": "text",
            "proposed_correction": "",
            "confidence": float("nan"),
            "evidence_quote": PATTERN,
        }
        parse(payload(findings=[finding]))


def test_assessment_requires_source_quote_and_allowed_position():
    data = {
        "finding_id": "Reviewer B-F1",
        "position": "agree",
        "reason": "The line supports the text.",
        "evidence_quote": PATTERN,
    }
    review = parse(payload(assessments=[data]))
    assert review.assessments[0].evidence_status == "grounded_text"
    with pytest.raises(ValueError, match="assessment"):
        parse(payload(assessments=[{**data, "position": "maybe"}]))
    with pytest.raises(ValueError, match="not grounded"):
        parse(payload(assessments=[{**data, "evidence_quote": "not in source"}]))


def test_rejects_unstructured_and_oversized_payloads():
    with pytest.raises(ValueError, match="structured JSON"):
        parse("not JSON")
    with pytest.raises(ValueError, match="item limit"):
        parse(payload(open_questions=["q"] * 101))
