import asyncio
import hashlib

import pytest
from fastapi.testclient import TestClient

from crochet_checker.ai_providers.history import ConsensusHistoryStore
from crochet_checker.ai_providers.provider_adapters import (
    ProviderCatalog,
    ProviderConfig,
)
from crochet_checker.ai_providers.service import ConsensusService
from crochet_checker.ai_providers.settings import ConsensusSettings
from crochet_checker.web.app import app

PATTERN = "Round 1: 6 sc into magic ring (6)"


class ApiRunner:
    async def run(self, pattern_text, *, run_id=None, revision=None, progress=None):
        if progress:
            progress(
                {
                    "stage": "completed",
                    "current": 5,
                    "total": 5,
                    "message": "test completed",
                }
            )
        return {
            "run_id": run_id,
            "approved": False,
            "approval_status": "NOT APPROVED – HUMAN REVIEW REQUIRED",
            "pattern_hash": hashlib.sha256(pattern_text.encode()).hexdigest(),
            "revision": revision,
            "gate": {
                "approved": False,
                "status": "NOT APPROVED – HUMAN REVIEW REQUIRED",
                "blockers": [{"code": "mock", "message": "Test adapter only"}],
            },
            "models": {"configured": [], "participating": [], "failed": []},
            "scoring": {"weighted_score": 0},
        }


@pytest.fixture
def client_and_service():
    old = getattr(app.state, "consensus_service", None)
    catalog = ProviderCatalog.from_env(
        {
            "CROCHET_CONSENSUS_PROVIDERS": "openai",
            "OPENAI_MODEL": "explicit-test-model",
            "OPENAI_API_KEY": "api-secret-must-not-be-returned",
        }
    )
    service = ConsensusService(
        store=ConsensusHistoryStore(":memory:"),
        catalog=catalog,
        settings=ConsensusSettings(),
        runner=ApiRunner(),
    )
    app.state.consensus_service = service
    try:
        with TestClient(app) as client:
            yield client, service
    finally:
        if old is None:
            delattr(app.state, "consensus_service")
        else:
            app.state.consensus_service = old


def test_provider_status_and_dashboard_never_expose_credentials(client_and_service):
    client, _service = client_and_service
    response = client.get("/api/consensus/providers")
    assert response.status_code == 200
    assert "api-secret-must-not-be-returned" not in response.text
    assert response.json()["status"]["selected_provider_ids"] == ["openai"]
    assert response.json()["status"]["providers"][0]["ready"] is True

    dashboard = client.get("/consensus")
    assert dashboard.status_code == 200
    assert "written-text" in dashboard.text
    assert "correction draft" in dashboard.text


def test_history_run_and_revalidated_draft_routes(client_and_service):
    client, service = client_and_service
    response = client.post("/api/consensus/runs", json={"pattern_text": PATTERN})
    assert response.status_code == 202
    run_id = response.json()["run_id"]
    assert response.json()["status"] == "queued"

    run = client.get(f"/api/consensus/runs/{run_id}")
    assert run.status_code == 200
    assert run.json()["status"] == "completed"
    assert run.json()["report"]["approved"] is False

    draft = client.post(
        f"/api/consensus/runs/{run_id}/drafts",
        json={
            "changes": [
                {
                    "from_text": "6 sc",
                    "to_text": "5 sc",
                    "reason": "Test-only correction rationale",
                }
            ]
        },
    )
    assert draft.status_code == 202
    data = draft.json()["draft"]
    child_id = data["run_id"]
    assert data["parent_run_id"] == run_id
    assert data["original_preserved"] is True
    assert service.store.get_pattern_text(run_id) == PATTERN
    assert (
        service.store.get_pattern_text(child_id) == "Round 1: 5 sc into magic ring (6)"
    )
    assert client.get(f"/api/consensus/runs/{child_id}").json()["status"] == "completed"
    listed = client.get("/api/consensus/runs?limit=10").json()["runs"]
    assert len(listed) == 2


def test_blank_pattern_bad_revision_and_unknown_history_are_rejected(
    client_and_service,
):
    client, _service = client_and_service
    assert (
        client.post("/api/consensus/runs", json={"pattern_text": "  "}).status_code
        == 422
    )
    assert client.get("/api/consensus/runs/not-a-run").status_code == 404

    parent = client.post("/api/consensus/runs", json={"pattern_text": PATTERN}).json()[
        "run_id"
    ]
    invalid = client.post(
        f"/api/consensus/runs/{parent}/drafts",
        json={
            "changes": [
                {
                    "from_text": "not present",
                    "to_text": "new",
                    "reason": "A test reason",
                }
            ]
        },
    )
    assert invalid.status_code == 409
    assert "match exactly once" in invalid.json()["detail"]
