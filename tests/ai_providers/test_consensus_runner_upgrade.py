import asyncio
import json
from types import SimpleNamespace

import pytest

from crochet_checker.ai_providers.orchestrator import ConsensusRunner
from crochet_checker.ai_providers.provider_adapters import (
    ProviderCatalog,
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


def test_independent_specialist_reviews_are_concurrent_and_roles_are_distinct():
    providers = configs(2)
    active_calls = [0]
    max_active_calls = [0]

    class TrackingAdapter(FakeAdapter):
        async def generate(self, system_prompt, user_prompt):
            active_calls[0] += 1
            max_active_calls[0] = max(max_active_calls[0], active_calls[0])
            try:
                await asyncio.sleep(0.01)
                return await super().generate(system_prompt, user_prompt)
            finally:
                active_calls[0] -= 1

    adapters = {
        item.provider_id: TrackingAdapter(item.provider_id, findings=[])
        for item in providers
    }
    report = asyncio.run(
        runner_for(adapters, provider_configs=providers).run(PATTERN)
    )

    roles = {item["provider_id"]: item["role"] for item in report["models"]["states"]}
    assert roles == {
        "provider_a": "stitch_arithmetic",
        "provider_b": "construction_assembly",
    }
    assert max_active_calls[0] >= 2
    assert report["ai_consensus"]["policy"]["met"] is True


def test_consensus_is_not_claimed_when_a_required_provider_misses_the_policy():
    providers = configs(3)
    adapters = {
        providers[0].provider_id: FakeAdapter(
            providers[0].provider_id, findings=[_finding()]
        ),
        providers[1].provider_id: FakeAdapter(
            providers[1].provider_id, findings=[_finding()]
        ),
        providers[2].provider_id: FakeAdapter(
            providers[2].provider_id,
            failure=ProviderRequestError(
                "Provider service error persisted",
                attempts=2,
                latency_ms=5,
                status_code=503,
            ),
        ),
    }
    report = asyncio.run(
        runner_for(
            adapters,
            provider_configs=providers,
            settings=ConsensusSettings(consensus_threshold=0.6),
        ).run(PATTERN)
    )

    issue = report["ai_consensus"]["issues"][0]
    assert issue["support_threshold_met"] is True
    assert issue["consensus_reached"] is False
    assert report["ai_consensus"]["status"] == "CONSENSUS_POLICY_NOT_MET"
    assert report["ai_consensus"]["policy"]["met"] is False
    assert report["ai_consensus"]["policy"]["checks"][
        "required_provider_slots_met"
    ] is False
    assert any("provider_c" in reason for reason in report["ai_consensus"]["policy"]["reasons"])
    assert "consensus" in report["ai_consensus"]["reason_consensus_not_reached"].casefold()


def test_low_support_info_finding_blocks_consensus_and_delivery_gate():
    low_severity_finding = _finding()
    low_severity_finding["severity"] = "info"
    providers = configs(2)
    adapters = {
        providers[0].provider_id: FakeAdapter(
            providers[0].provider_id, findings=[low_severity_finding]
        ),
        providers[1].provider_id: FakeAdapter(providers[1].provider_id, findings=[]),
    }
    report = asyncio.run(
        runner_for(adapters, provider_configs=providers).run(PATTERN)
    )

    assert report["ai_consensus"]["issues"][0]["support_threshold_met"] is False
    assert report["ai_consensus"]["status"] == "CONSENSUS_POLICY_NOT_MET"
    assert report["gate"]["approved"] is False
    assert report["gate"]["consensus_policy_satisfied"] is False
    assert any(
        item["code"] == "consensus_policy_not_met"
        for item in report["gate"]["blockers"]
    )


def test_selected_but_unconfigured_optional_provider_is_reported_with_assigned_role():
    catalog = ProviderCatalog.from_env(
        {
            "CROCHET_CONSENSUS_PROVIDERS": "openai,anthropic",
            "CROCHET_REQUIRED_PROVIDERS": "openai",
            "OPENAI_MODEL": "configured-test-model",
            "OPENAI_API_KEY": "test-only-key",
            "ANTHROPIC_MODEL": "missing-key-test-model",
        }
    )
    runner = ConsensusRunner(
        catalog=catalog,
        adapters={"openai": FakeAdapter("openai", findings=[])},
        settings=ConsensusSettings(),
        validator=lambda _text: _valid_report(),
        unverified_steps=lambda _text: [],
    )
    report = asyncio.run(runner.run(PATTERN))

    anthropic = next(
        item for item in report["models"]["states"] if item["provider_id"] == "anthropic"
    )
    assert anthropic["status"] == "not_configured"
    assert anthropic["role"] == "construction_assembly"
    assert anthropic["independent_participated"] is False
    assert anthropic["missing_configuration"] == ["API key"]
    assert report["models"]["participation"]["selected_provider_count"] == 2
    assert report["models"]["participation"][
        "selected_independent_participation_ratio"
    ] == 0.5
    assert report["ai_consensus"]["status"] == "CONSENSUS_POLICY_NOT_MET"
    assert report["ai_consensus"]["reason_consensus_not_reached"]


def test_progress_callback_failure_does_not_discard_a_structured_review_report():
    providers = configs(2)
    adapters = {
        item.provider_id: FakeAdapter(item.provider_id, findings=[])
        for item in providers
    }

    async def broken_progress(_update):
        raise RuntimeError("progress database unavailable")

    report = asyncio.run(
        runner_for(adapters, provider_configs=providers).run(
            PATTERN, progress=broken_progress
        )
    )

    assert report["execution_status"] == "completed"
    assert report["report_schema_version"] == 1
    assert len(report["rounds"]["provider_calls"]) == 6
    assert report["rounds"]["provider_call_records_complete"] is True


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


def test_configured_fallback_not_needed_is_not_reported_as_a_failure_or_participant():
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
        "provider_a": FakeAdapter("provider_a", findings=[]),
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

    fallback_state = next(
        item
        for item in report["models"]["states"]
        if item["provider_id"] == "provider_fallback"
    )
    assert fallback_state["status"] == "not_attempted"
    assert fallback_state["is_fallback"] is True
    assert "provider_fallback" not in {
        item["provider_id"] for item in report["models"]["participating"]
    }
    assert all(
        item["provider_id"] != "provider_fallback"
        for item in report["models"]["failed"]
    )
    assert not any(
        item["provider_id"] == "provider_fallback"
        for item in report["rounds"]["provider_calls"]
    )
    assert report["gate"]["approved"] is True


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
