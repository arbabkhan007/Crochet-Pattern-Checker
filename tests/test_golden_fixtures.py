"""Lock a small provisional golden set to explicit rule and source identities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from crochet_checker.validation.validator import RULESET_ID, validate_pattern

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "golden_fixtures"
MANIFEST = FIXTURES / "manifest.json"
FINDING_KEYS = (
    "rule_id",
    "severity",
    "location",
    "expected",
    "actual",
    "source_line",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_golden_manifest_locks_ruleset_and_fixture_source_identity():
    manifest = _manifest()
    assert manifest["schema_version"] == 1
    assert manifest["ruleset_id"] == RULESET_ID
    assert manifest["review_status"] == "provisional"

    for item in manifest["ruleset_sources"]:
        source = (ROOT / item["path"]).resolve()
        assert source.is_relative_to(ROOT.resolve()), item["path"]
        assert source.is_file(), item["path"]
        assert _sha256(source) == item["sha256"], (
            f"Ruleset source changed: {item['path']}; review findings and update "
            "the manifest hash deliberately."
        )

    fixture_names = {item["file"] for item in manifest["cases"]}
    actual_names = {path.name for path in FIXTURES.glob("*.txt")}
    assert actual_names == fixture_names


def test_golden_fixtures_match_exact_status_and_finding_contract():
    manifest = _manifest()
    for case in manifest["cases"]:
        fixture = (FIXTURES / case["file"]).resolve()
        assert fixture.is_relative_to(FIXTURES.resolve()), case["id"]
        assert _sha256(fixture) == case["sha256"], (
            f"Fixture text changed: {case['id']}; review the expected findings."
        )

        report = validate_pattern(fixture.read_text(encoding="utf-8"))
        assert report.overall_status == case["expected_status"], case["id"]
        payload = report.to_dict()
        assert payload["ruleset_id"] == manifest["ruleset_id"], case["id"]
        actual_findings = [
            {key: finding.get(key) for key in FINDING_KEYS}
            for finding in payload["findings"]
        ]
        assert actual_findings == case["expected_findings"], (
            f"Unexpected/missing findings for {case['id']}: "
            f"expected={case['expected_findings']!r}, actual={actual_findings!r}"
        )
