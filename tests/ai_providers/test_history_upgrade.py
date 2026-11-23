import asyncio

import pytest

from crochet_checker.ai_providers.history import ConsensusHistoryStore
from crochet_checker.ai_providers.provider_adapters import ProviderCatalog
from crochet_checker.ai_providers.service import ConsensusService, RevisionLimitError
from crochet_checker.ai_providers.settings import ConsensusSettings

ORIGINAL = "Round 1: 6 sc into magic ring (6)\n"


class StubRunner:
    def __init__(self, result=None, failure=None):
        self.result = result or {
            "approved": False,
            "approval_status": "NOT APPROVED – HUMAN REVIEW REQUIRED",
            "gate": {"blockers": [{"code": "test", "message": "Test only"}]},
        }
        self.failure = failure
        self.calls = []

    async def run(self, pattern_text, *, run_id=None, revision=None, progress=None):
        self.calls.append((pattern_text, run_id, revision))
        if progress:
            progress(
                {
                    "stage": "test",
                    "current": 1,
                    "total": 5,
                    "message": "mocked test progress",
                }
            )
        if self.failure:
            raise self.failure
        return {
            **self.result,
            "run_id": run_id,
            "pattern_hash": "test-hash",
            "revision": revision,
        }


def completed_parent(store):
    store.create_run("parent", ORIGINAL)
    store.save_report(
        "parent",
        {
            "approved": False,
            "approval_status": "NOT APPROVED – HUMAN REVIEW REQUIRED",
            "scoring": {"weighted_score": 42},
            "models": {"configured": [], "participating": [], "failed": []},
        },
    )


def service_for(store, runner, *, max_revisions=3):
    return ConsensusService(
        store=store,
        catalog=ProviderCatalog.from_env({}),
        settings=ConsensusSettings(max_revisions=max_revisions),
        runner=runner,
    )


def test_sqlite_history_persists_runs_report_progress_and_summary():
    store = ConsensusHistoryStore(":memory:")
    store.create_run("run-1", ORIGINAL)
    store.update_progress(
        "run-1",
        {
            "stage": "cross_examination",
            "current": 2,
            "total": 5,
            "message": "reviewing",
        },
    )
    report = {
        "approved": False,
        "approval_status": "NOT APPROVED – HUMAN REVIEW REQUIRED",
        "scoring": {"weighted_score": 20},
        "models": {
            "configured": [{"provider_id": "x"}],
            "participating": [],
            "failed": [{"provider_id": "x"}],
        },
    }
    store.save_report("run-1", report)

    run = store.get_run("run-1")
    assert run["status"] == "completed"
    assert run["report"] == report
    assert run["pattern_hash"]
    listing = store.list_runs(1)[0]
    assert listing["approval_status"] == report["approval_status"]
    assert listing["weighted_score"] == 20
    assert listing["configured_model_count"] == 1
    assert listing["failed_model_count"] == 1
    assert "report" not in listing


def test_explicit_revision_is_a_new_immutable_child_with_diff_and_revalidation():
    store = ConsensusHistoryStore(":memory:")
    completed_parent(store)
    runner = StubRunner()
    service = service_for(store, runner)
    child_id, metadata = service.create_revision(
        "parent",
        [
            {
                "from_text": "6 sc",
                "to_text": "5 sc",
                "reason": "A reviewer proposed clarifying the starting count.",
            }
        ],
    )

    assert metadata["parent_run_id"] == "parent"
    assert metadata["revision_number"] == 1
    assert metadata["original_preserved"] is True
    assert "-Round 1: 6 sc" in metadata["diff"]
    assert "+Round 1: 5 sc" in metadata["diff"]
    assert store.get_pattern_text("parent") == ORIGINAL
    assert store.get_pattern_text(child_id) == "Round 1: 5 sc into magic ring (6)\n"

    child = asyncio.run(service.execute(child_id))
    assert child["status"] == "completed"
    assert runner.calls[0][0] == store.get_pattern_text(child_id)
    assert runner.calls[0][2]["parent_run_id"] == "parent"
    assert runner.calls[0][2]["revision_number"] == 1
    assert child["report"]["revision"]["parent_run_id"] == "parent"
    assert store.get_pattern_text("parent") == ORIGINAL


def test_revision_requires_one_exact_match_reason_and_available_revision_budget():
    store = ConsensusHistoryStore(":memory:")
    completed_parent(store)
    service = service_for(store, StubRunner(), max_revisions=1)
    with pytest.raises(ValueError, match="exactly once"):
        service.create_revision(
            "parent", [{"from_text": "6", "to_text": "7", "reason": "clarify"}]
        )
    with pytest.raises(ValueError, match="reason"):
        service.create_revision(
            "parent", [{"from_text": "6 sc", "to_text": "7 sc", "reason": " "}]
        )
    with pytest.raises(ValueError, match="no-op"):
        service.create_revision(
            "parent", [{"from_text": "6 sc", "to_text": "6 sc", "reason": "same"}]
        )
    child_id, _ = service.create_revision(
        "parent", [{"from_text": "6 sc", "to_text": "7 sc", "reason": "explicit test"}]
    )
    store.save_report(child_id, {"approved": False})
    with pytest.raises(RevisionLimitError):
        service.create_revision(
            child_id,
            [
                {
                    "from_text": "7 sc",
                    "to_text": "8 sc",
                    "reason": "second revision not allowed",
                }
            ],
        )


def test_nested_revision_tracks_the_original_root_hash_and_parent_link():
    store = ConsensusHistoryStore(":memory:")
    completed_parent(store)
    service = service_for(store, StubRunner(), max_revisions=2)
    root_hash = store.get_run("parent")["pattern_hash"]
    first_id, _ = service.create_revision(
        "parent", [{"from_text": "6 sc", "to_text": "5 sc", "reason": "First draft"}]
    )
    store.save_report(first_id, {"approved": False})
    second_id, metadata = service.create_revision(
        first_id, [{"from_text": "5 sc", "to_text": "4 sc", "reason": "Second draft"}]
    )
    assert metadata["parent_run_id"] == first_id
    assert metadata["root_run_id"] == "parent"
    assert metadata["original_pattern_hash"] == root_hash
    assert store.get_run(second_id)["root_run_id"] == "parent"
    assert store.get_pattern_text("parent") == ORIGINAL


def test_failed_execution_records_no_approval_and_never_persists_exception_secret():
    store = ConsensusHistoryStore(":memory:")
    runner = StubRunner(failure=RuntimeError("token=very-secret provider detail"))
    service = service_for(store, runner)
    run_id = service.create_run(ORIGINAL)
    run = asyncio.run(service.execute(run_id))

    assert run["status"] == "failed"
    assert run["report"] is not None
    assert run["report"]["execution_status"] == "failed"
    assert run["report"]["approved"] is False
    assert run["report"]["ai_consensus"]["status"] == (
        "NOT_EVALUATED_DUE_TO_ORCHESTRATION_FAILURE"
    )
    assert run["report"]["ai_consensus"]["reason_consensus_not_reached"]
    assert run["report"]["rounds"]["provider_call_records_complete"] is False
    assert "very-secret" not in run["error"]
    assert run["progress"]["stage"] == "failed"


def test_orchestration_failure_names_configured_models_and_marks_participation_unknown():
    store = ConsensusHistoryStore(":memory:")
    catalog = ProviderCatalog.from_env(
        {
            "CROCHET_CONSENSUS_PROVIDERS": "openai",
            "OPENAI_MODEL": "explicit-test-model",
            "OPENAI_API_KEY": "secret-for-test-only",
        }
    )
    runner = StubRunner(failure=RuntimeError("provider response included secret"))
    service = ConsensusService(
        store=store,
        catalog=catalog,
        settings=ConsensusSettings(),
        runner=runner,
    )
    run_id = service.create_run(ORIGINAL)
    run = asyncio.run(service.execute(run_id))

    report = run["report"]
    assert run["status"] == "failed"
    assert report["models"]["selected_provider_ids"] == ["openai"]
    assert report["models"]["participating"] == []
    assert report["models"]["unknown"][0]["provider_id"] == "openai"
    assert report["models"]["unknown"][0]["role"] == "stitch_arithmetic"
    assert report["models"]["unknown"][0]["independent_participated"] is None
    assert "secret-for-test-only" not in str(report)
    listing = store.list_runs(1)[0]
    assert listing["unknown_model_count"] == 1


def test_only_completed_parent_can_be_revised_and_missing_parent_is_not_silenced():
    store = ConsensusHistoryStore(":memory:")
    service = service_for(store, StubRunner())
    store.create_run("queued", ORIGINAL)
    with pytest.raises(ValueError, match="completed"):
        service.create_revision(
            "queued", [{"from_text": "6 sc", "to_text": "7 sc", "reason": "explicit"}]
        )
    with pytest.raises(KeyError):
        service.create_revision(
            "missing", [{"from_text": "6 sc", "to_text": "7 sc", "reason": "explicit"}]
        )
