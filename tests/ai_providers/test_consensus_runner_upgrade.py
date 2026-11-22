import asyncio
import json
from types import SimpleNamespace

import pytest

from crochet_checker.ai_providers.orchestrator import ConsensusRunner
from crochet_checker.ai_providers.provider_adapters import (
    ProviderConfig,
    ProviderRequestError,
    ProviderResponse,
)
from crochet_checker.ai_providers.settings import ConsensusSettings

PATTERN = "Round 1: 6 sc into magic ring (6)"


def configs(count=2):
    values = [
        ProviderConfig(
            "provider_a",
            "openai_compatible",
            "unit-test-model-a",
            "https://unit.invalid/v1",
            api_key="test-secret-a",
        ),
        ProviderConfig(
            "provider_b",
            "anthropic",
            "unit-test-model-b",
            "https://unit.invalid",
            api_key="test-secret-b",
        ),
        ProviderConfig(
            "provider_c",
            "google",
            "unit-test-model-c",
            "https://unit.invalid/v1beta",
            api_key="test-secret-c",
        ),
    ]
    return values[:count]


def _finding(expected=6, actual=9):
    return {
        "location": "Round 1",
        "line_number": 1,
        "source_instruction": PATTERN,
        "category": "arithmetic",
        "issue_code": "count_mismatch",
        "issue": "The stated count is inconsistent.",
        "expected_count": expected,
        "actual_count": actual,
        "severity": "major",
        "explanation": "This is a test-only, source-cited concern.",
        "proposed_correction": "(6)",
        "confidence": 0.8,
        "evidence_quote": PATTERN,
    }


class FakeAdapter:
    def __init__(
        self,
        provider_id,
        *,
        findings=None,
        position="agree",
        failure=None,
        coverage_quote=PATTERN,
    ):
        self.provider_id = provider_id
        self.findings = findings
        self.position = position
        self.failure = failure
        self.coverage_quote = coverage_quote
        self.prompts = []

    async def generate(self, system_prompt, user_prompt):
        self.prompts.append((system_prompt, user_prompt))
        if self.failure:
            raise self.failure
        request = json.loads(user_prompt)
        peer_findings = [
            finding
            for reviewer in request.get("anonymized_peer_reviews", {}).get(
                "reviewers", []
            )
            for finding in reviewer.get("findings", [])
        ]
        assessments = [
            {
                "finding_id": item["finding_id"],
                "position": self.position,
                "reason": "Test reviewer assessed the exact cited instruction.",
                "evidence_quote": PATTERN,
            }
            for item in peer_findings
        ]
        findings = (
            self.findings(request.get("phase"), self.provider_id)
            if callable(self.findings)
            else self.findings
        )
        if findings is None:
            findings = [_finding()]
        payload = {
            "summary": "Test-only mocked structured review.",
            "coverage": [
                {
                    "scope": request["role"],
                    "status": "reviewed",
                    "reason": "Test adapter cites a literal source line.",
                    "evidence_quote": self.coverage_quote,
                }
            ],
            "findings": findings,
            "assessments": assessments,
            "open_questions": [],
        }
        return ProviderResponse(
            json.dumps(payload),
            input_tokens=100,
            output_tokens=50,
            reported_model="test-reported-model",
            latency_ms=3,
            attempts=1,
            estimated_cost_usd=0.0001,
        )


def _valid_report():
    return SimpleNamespace(
        valid=True,
        overall_status="PASS",
        score=100,
        errors=[],
        warnings=[],
        stitch_count=6,
        stitch_counts={1: 6},
        execution_time=0.001,
    )


def runner_for(
    adapters, *, provider_configs=None, settings=None, validator=None, notes=None
):
    provider_configs = provider_configs or configs(len(adapters))
    return ConsensusRunner(
        providers=provider_configs,
        required_provider_ids=[item.provider_id for item in provider_configs],
        adapters=adapters,
        settings=settings or ConsensusSettings(),
        validator=validator or (lambda _text: _valid_report()),
        unverified_steps=notes or (lambda _text: []),
    )


def test_parallel_provider_phases_and_written_only_scoped_approval():
    adapters = {
        item.provider_id: FakeAdapter(item.provider_id, findings=[])
        for item in configs(2)
    }
    runner = runner_for(adapters)
    report = asyncio.run(runner.run(PATTERN, run_id="test-run"))

    assert report["approved"] is True
    assert report["approval_status"] == "APPROVED FOR WRITTEN-TEXT CHECKS ONLY"
    assert report["gate"]["physical_construction_verified"] is False
    assert report["gate"]["physical_verification_required_but_missing"] is False
    assert len(report["rounds"]["independent"]) == 2
    assert len(report["rounds"]["cross_examination"]) == 2
    assert len(report["rounds"]["adversarial_review"]) == 2
    assert report["models"]["participation"]["fully_completed_count"] == 2
    assert report["telemetry"]["successful_provider_calls"] == 6
    assert report["telemetry"]["estimated_cost_usd"] == pytest.approx(0.0006)
    assert all(
        "test-secret" not in json.dumps(item) for item in report["models"]["configured"]
    )
    for adapter in adapters.values():
        assert len(adapter.prompts) == 3


def test_deterministic_failure_cannot_be_overruled_by_mocked_ai():
    adapters = {
        item.provider_id: FakeAdapter(item.provider_id, findings=[])
        for item in configs(2)
    }
    invalid = SimpleNamespace(
        valid=False,
        overall_status="FAIL",
        score=0,
        errors=["round count mismatch"],
        warnings=[],
        stitch_count=0,
        stitch_counts={},
    )
    report = asyncio.run(
        runner_for(adapters, validator=lambda _text: invalid).run(PATTERN)
    )

    assert report["deterministic"]["valid"] is False
    assert report["gate"]["approved"] is False
    assert report["approval_status"] == "NOT APPROVED – HUMAN REVIEW REQUIRED"
    assert any(
        item["code"] == "deterministic_validation_failed"
        for item in report["gate"]["blockers"]
    )


def test_grounded_actionable_findings_are_not_auto_approved():
    adapters = {
        item.provider_id: FakeAdapter(item.provider_id, findings=[_finding()])
        for item in configs(2)
    }
    report = asyncio.run(runner_for(adapters).run(PATTERN))

    assert len(report["ai_consensus"]["issues"]) == 1
    issue = report["ai_consensus"]["issues"][0]
    assert issue["independent_support_count"] == 2
    assert issue["consensus_reached"] is True
    assert report["gate"]["approved"] is False
    assert any(
        item["code"] == "unresolved_actionable_ai_findings"
        for item in report["gate"]["blockers"]
    )
    assert report["correction_proposals"][0]["status"].startswith("PROPOSAL ONLY")


def test_unresolved_conflicting_count_claims_block_gate_and_are_reported():
    def different_claims(_phase, provider_id):
        return [_finding(expected=6 if provider_id == "provider_a" else 9, actual=12)]

    adapters = {
        item.provider_id: FakeAdapter(item.provider_id, findings=different_claims)
        for item in configs(2)
    }
    report = asyncio.run(runner_for(adapters).run(PATTERN))

    assert any(
        item["type"] == "conflicting_count_claims"
        for item in report["ai_consensus"]["disagreements"]
    )
    assert any(
        item["code"] == "unresolved_model_disagreement"
        for item in report["gate"]["blockers"]
    )
    assert report["deterministic"]["valid"] is True


def test_provider_failure_is_visible_and_never_reported_as_a_review():
    provider_list = configs(2)
    adapters = {
        provider_list[0].provider_id: FakeAdapter(
            provider_list[0].provider_id,
            failure=ProviderRequestError(
                "Provider service error persisted",
                attempts=3,
                latency_ms=5,
                status_code=503,
            ),
        ),
        provider_list[1].provider_id: FakeAdapter(
            provider_list[1].provider_id, findings=[]
        ),
    }
    settings = ConsensusSettings(
        min_participating_models=1,
        enable_cross_examination=False,
        enable_adversarial_review=False,
    )
    report = asyncio.run(
        runner_for(adapters, provider_configs=provider_list, settings=settings).run(
            PATTERN
        )
    )

    failed = [
        item
        for item in report["rounds"]["provider_calls"]
        if item["provider_id"] == provider_list[0].provider_id
    ]
    assert failed and failed[0]["status"] == "failed"
    assert failed[0]["attempts"] == 3
    assert failed[0]["error"] == "HTTP 503: Provider service error persisted"
    assert all(
        item["provider_id"] != provider_list[0].provider_id
        for item in report["rounds"]["independent"]
    )
    assert report["gate"]["approved"] is False
    assert any(
        item["code"] == "required_model_missing" for item in report["gate"]["blockers"]
    )


def test_configured_fallback_is_reported_as_the_required_slot_substitute():
    selected = configs(2)
    fallback = ProviderConfig(
        "provider_fallback",
        "openai_compatible",
        "explicit-fallback-model",
        "https://unit.invalid/v1",
        api_key="fallback-secret",
        required=False,
    )
    adapters = {
        "provider_a": FakeAdapter(
            "provider_a",
            failure=ProviderRequestError(
                "primary unavailable", attempts=2, latency_ms=10, status_code=503
            ),
        ),
        "provider_b": FakeAdapter("provider_b", findings=[]),
        "provider_fallback": FakeAdapter("provider_fallback", findings=[]),
    }
    runner = ConsensusRunner(
        providers=selected,
        required_provider_ids=["provider_a", "provider_b"],
        fallbacks={"provider_a": fallback},
        adapters=adapters,
        settings=ConsensusSettings(),
        validator=lambda _text: _valid_report(),
        unverified_steps=lambda _text: [],
    )
    report = asyncio.run(runner.run(PATTERN))

    fallback_call = next(
        item
        for item in report["rounds"]["provider_calls"]
        if item["provider_id"] == "provider_fallback" and item["phase"] == "independent"
    )
    assert fallback_call["status"] == "succeeded"
    assert fallback_call["is_fallback"] is True
    assert "provider_fallback" in {
        item["provider_id"] for item in report["models"]["participating"]
    }
    assert "provider_a" not in {
        item["provider_id"] for item in report["rounds"]["independent"]
    }
    assert report["gate"]["approved"] is True
    slot = next(
        item
        for item in report["models"]["states"]
        if item["provider_id"] == "provider_a"
    )
    assert slot["status"] == "failed"
    assert slot["required_slot_satisfied_by"] == "provider_fallback"
    assert report["models"]["participation"]["required_slots_satisfied"] is True


def test_missing_or_ungrounded_review_coverage_fails_closed():
    adapters = {
        item.provider_id: FakeAdapter(
            item.provider_id, findings=[], coverage_quote="invented source quote"
        )
        for item in configs(2)
    }
    report = asyncio.run(runner_for(adapters).run(PATTERN))

    assert report["models"]["participation"]["independent_success_count"] == 0
    assert report["gate"]["approved"] is False
    assert report["telemetry"]["failed_provider_calls"] >= 2
    assert all(
        item["error"] == "Provider returned an invalid structured review"
        for item in report["rounds"]["provider_calls"]
        if item["phase"] == "independent"
    )


def test_disabled_phases_are_explicit_and_not_falsely_reported_as_calls():
    providers = configs(2)
    adapters = {
        item.provider_id: FakeAdapter(item.provider_id, findings=[])
        for item in providers
    }
    settings = ConsensusSettings(
        enable_cross_examination=False, enable_adversarial_review=False
    )
    report = asyncio.run(
        runner_for(adapters, provider_configs=providers, settings=settings).run(PATTERN)
    )
    assert report["rounds"]["phases"]["cross_examination"]["status"] == "disabled"
    assert report["rounds"]["phases"]["adversarial_review"]["status"] == "disabled"
    assert report["telemetry"]["successful_provider_calls"] == 2
    assert all(len(adapter.prompts) == 1 for adapter in adapters.values())
    assert report["gate"]["approved"] is False
    assert (
        sum(
            item["code"] == "required_review_phase_disabled"
            for item in report["gate"]["blockers"]
        )
        == 2
    )


def test_anonymized_cross_examination_prompt_does_not_disclose_provider_names():
    providers = configs(2)
    adapters = {
        item.provider_id: FakeAdapter(item.provider_id, findings=[_finding()])
        for item in providers
    }
    report = asyncio.run(runner_for(adapters).run(PATTERN))
    cross_prompt = json.loads(adapters["provider_a"].prompts[1][1])
    packet = cross_prompt["anonymized_peer_reviews"]
    serialized = json.dumps(packet)
    assert "provider_id" not in serialized
    assert "unit-test-model" not in serialized
    assert "Reviewer B" in serialized
    assert report["rounds"]["cross_examination"]
