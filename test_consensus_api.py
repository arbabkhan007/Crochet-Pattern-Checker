"""API/dashboard smoke tests run with an isolated SQLite file and no providers."""

from __future__ import annotations

import importlib

from fastapi.testclient import TestClient

from crochet_checker.ai_providers.history import ConsensusHistoryStore
from crochet_checker.ai_providers.orchestrator import ConsensusRunner
from crochet_checker.ai_providers.provider_adapters import ProviderCatalog
from crochet_checker.ai_providers.service import ConsensusService
from crochet_checker.ai_providers.settings import ConsensusSettings


PATTERN = "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)"


def isolated_client(tmp_path, monkeypatch):
    module = importlib.import_module("crochet_checker.web.app")
    catalog = ProviderCatalog.from_env({})
    settings = ConsensusSettings(
        min_participating_models=1,
        min_participation_ratio=1.0,
        consensus_threshold=0.67,
        max_concurrency=2,
        enable_cross_examination=True,
        enable_adversarial_review=True,
        strict_required_participation=True,
        max_revisions=2,
        required_roles=(),
    )
    store = ConsensusHistoryStore(tmp_path / "api-history.sqlite3")
    runner = ConsensusRunner(catalog=catalog, settings=settings)
    service = ConsensusService(store=store, catalog=catalog, settings=settings, runner=runner)
    monkeypatch.setattr(module, "_CONSENSUS_SERVICE", service)
    return module, TestClient(module.app), service


def test_consensus_dashboard_and_provider_status_disclose_scope_not_keys(tmp_path, monkeypatch):
    _module, client, _service = isolated_client(tmp_path, monkeypatch)
    page = client.get("/consensus")
    providers = client.get("/api/consensus/providers")
    assert page.status_code == 200
    assert "Start multi-round validation" in page.text
    assert "NOT APPROVED – HUMAN REVIEW REQUIRED" in page.text
    assert providers.status_code == 200
    body = providers.json()
    assert body["credential_values_exposed"] is False
    assert body["settings"]["physical_verification_required"] is True
    assert all("api_key" not in item for item in body["providers"])


def test_consensus_validate_endpoint_persists_report_and_history(tmp_path, monkeypatch):
    _module, client, service = isolated_client(tmp_path, monkeypatch)
    response = client.post("/api/consensus/validate", json={"pattern_text": PATTERN})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["report"]["deterministic"]["valid"] is True
    assert body["report"]["approved"] is False
    assert body["report"]["approval_status"] == "NOT APPROVED – HUMAN REVIEW REQUIRED"
    assert service.store.get_pattern_text(body["run_id"]) == PATTERN

    detail = client.get(f"/api/consensus/runs/{body['run_id']}")
    history = client.get("/api/consensus/runs")
    assert detail.status_code == 200 and detail.json()["report"]["run_id"] == body["run_id"]
    assert history.status_code == 200 and history.json()["runs"][0]["run_id"] == body["run_id"]


def test_queued_job_and_revision_routes_preserve_parent_pattern(tmp_path, monkeypatch):
    _module, client, service = isolated_client(tmp_path, monkeypatch)
    started = client.post("/api/consensus", json={"pattern_text": PATTERN})
    assert started.status_code == 202
    parent_id = started.json()["run_id"]
    parent = client.get(f"/api/consensus/runs/{parent_id}").json()
    assert parent["status"] == "completed"

    revised = client.post(
        f"/api/consensus/runs/{parent_id}/revisions",
        json={
            "changes": [
                {
                    "from_text": "Round 2: inc x 6 (12)",
                    "to_text": "Round 2: inc x 6 (12)\nFasten off.",
                    "reason": "The designer explicitly chose this separate finishing note.",
                }
            ]
        },
    )
    assert revised.status_code == 202
    child_id = revised.json()["run_id"]
    assert service.store.get_pattern_text(parent_id) == PATTERN
    assert service.store.get_pattern_text(child_id).endswith("Fasten off.")
    child = client.get(f"/api/consensus/runs/{child_id}").json()
    assert child["status"] == "completed"
    assert child["report"]["revision"]["parent_run_id"] == parent_id
    draft = client.get(f"/api/consensus/runs/{child_id}/draft")
    assert draft.status_code == 200
    assert draft.headers["cache-control"] == "no-store"
    assert draft.json()["draft_text"].endswith("Fasten off.")
    assert draft.json()["revalidation_complete"] is True
    assert draft.json()["original_pattern_hash"] == parent["pattern_hash"]


def test_revision_route_requires_a_reason_and_unique_source(tmp_path, monkeypatch):
    _module, client, _service = isolated_client(tmp_path, monkeypatch)
    parent = client.post("/api/consensus/validate", json={"pattern_text": PATTERN}).json()
    run_id = parent["run_id"]
    missing_reason = client.post(
        f"/api/consensus/runs/{run_id}/revisions",
        json={"changes": [{"from_text": "Round 2", "to_text": "Round 3", "reason": ""}]},
    )
    assert missing_reason.status_code == 422
    repeated_source = client.post(
        f"/api/consensus/runs/{run_id}/revisions",
        json={"changes": [{"from_text": "Round", "to_text": "Rnd", "reason": "Test change."}]},
    )
    assert repeated_source.status_code == 422
