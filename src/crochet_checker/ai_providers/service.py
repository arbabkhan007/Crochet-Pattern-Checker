"""Run lifecycle, history persistence, and explicit revalidated draft revisions."""

from __future__ import annotations

import difflib
import hashlib
import uuid
from typing import Any, Iterable

from .history import ConsensusHistoryStore
from .orchestrator import ConsensusRunner
from .provider_adapters import ProviderCatalog
from .settings import ConsensusSettings


class RevisionLimitError(ValueError):
    """A requested draft exceeds the configured revalidation limit."""


class ConsensusService:
    def __init__(
        self,
        *,
        store: ConsensusHistoryStore | None = None,
        catalog: ProviderCatalog | None = None,
        settings: ConsensusSettings | None = None,
        runner: ConsensusRunner | None = None,
    ):
        self.settings = settings or ConsensusSettings.from_env()
        self.catalog = catalog or ProviderCatalog.from_env()
        self.store = store or ConsensusHistoryStore()
        self.runner = runner or ConsensusRunner(
            catalog=self.catalog, settings=self.settings
        )

    def create_run(
        self,
        pattern_text: str,
        *,
        parent_run_id: str | None = None,
        revision_number: int = 0,
        revision_changes: Iterable[dict[str, Any]] = (),
    ) -> str:
        run_id = str(uuid.uuid4())
        self.store.create_run(
            run_id,
            pattern_text,
            parent_run_id=parent_run_id,
            revision_number=revision_number,
            revision_changes=revision_changes,
        )
        return run_id

    async def execute(self, run_id: str) -> dict[str, Any] | None:
        record = self.store.get_run(run_id)
        if record is None:
            return None
        try:
            text = self.store.get_pattern_text(run_id)
            revision = self._revision_metadata(record, text)
            self.store.set_running(run_id)

            def progress(update: dict[str, Any]) -> None:
                self.store.update_progress(run_id, update)

            report = await self.runner.run(
                text, run_id=run_id, revision=revision, progress=progress
            )
            self.store.save_report(run_id, report)
        except Exception:
            self.store.mark_failed(
                run_id, "Validation run failed; no approval was issued."
            )
        return self.store.get_run(run_id)

    async def run_now(self, pattern_text: str) -> dict[str, Any]:
        run_id = self.create_run(pattern_text)
        return await self.execute(run_id) or {
            "run_id": run_id,
            "status": "failed",
            "report": None,
        }

    def create_revision(
        self, parent_run_id: str, changes: list[dict[str, Any]]
    ) -> tuple[str, dict[str, Any]]:
        if not changes:
            raise ValueError("At least one explicit change with a reason is required")
        parent = self.store.get_run(parent_run_id)
        if parent is None:
            raise KeyError(parent_run_id)
        if parent["status"] != "completed":
            raise ValueError("A draft can only be based on a completed validation run")
        revision_number = int(parent["revision_number"]) + 1
        if revision_number > self.settings.max_revisions:
            raise RevisionLimitError(
                f"Configured revision limit ({self.settings.max_revisions}) reached"
            )
        original = self.store.get_pattern_text(parent_run_id)
        root_id = parent.get("root_run_id") or parent_run_id
        root_record = self.store.get_run(root_id)
        root_pattern_hash = (
            root_record["pattern_hash"] if root_record else parent["pattern_hash"]
        )
        draft = original
        applied: list[dict[str, str]] = []
        for index, item in enumerate(changes, 1):
            source, replacement, reason = (
                item.get("from_text"),
                item.get("to_text"),
                item.get("reason"),
            )
            if not isinstance(source, str) or not source:
                raise ValueError(f"Change {index} requires nonempty from_text")
            if not isinstance(replacement, str):
                raise ValueError(f"Change {index} requires to_text as text")
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError(f"Change {index} requires a reason")
            if source == replacement:
                raise ValueError(f"Change {index} is a no-op")
            count = draft.count(source)
            if count != 1:
                raise ValueError(
                    f"Change {index} source must match exactly once; found {count}"
                )
            draft = draft.replace(source, replacement, 1)
            applied.append(
                {"from_text": source, "to_text": replacement, "reason": reason.strip()}
            )
        if not draft.strip():
            raise ValueError("Draft cannot be empty")
        child_id = self.create_run(
            draft,
            parent_run_id=parent_run_id,
            revision_number=revision_number,
            revision_changes=applied,
        )
        diff = "\n".join(
            difflib.unified_diff(
                original.splitlines(),
                draft.splitlines(),
                fromfile=f"run:{parent_run_id}",
                tofile=f"draft:{child_id}",
                lineterm="",
            )
        )
        metadata = {
            "run_id": child_id,
            "parent_run_id": parent_run_id,
            "root_run_id": root_id,
            "revision_number": revision_number,
            "max_revisions": self.settings.max_revisions,
            "original_pattern_hash": root_pattern_hash,
            "draft_pattern_hash": hashlib.sha256(draft.encode("utf-8")).hexdigest(),
            "changes": applied,
            "diff": diff,
            "original_preserved": True,
            "status": "queued_for_full_revalidation",
        }
        return child_id, metadata

    def _revision_metadata(self, record: dict[str, Any], text: str) -> dict[str, Any]:
        parent_id = record.get("parent_run_id")
        if not parent_id:
            return {
                "parent_run_id": None,
                "root_run_id": record.get("root_run_id") or record["run_id"],
                "revision_number": 0,
                "max_revisions": self.settings.max_revisions,
                "original_pattern_hash": record["pattern_hash"],
                "changes": [],
                "diff": "",
                "original_preserved": True,
            }
        parent_text = self.store.get_pattern_text(parent_id)
        root_id = record.get("root_run_id") or parent_id
        root = self.store.get_run(root_id)
        return {
            "parent_run_id": parent_id,
            "root_run_id": root_id,
            "revision_number": int(record["revision_number"]),
            "max_revisions": self.settings.max_revisions,
            "original_pattern_hash": root["pattern_hash"] if root else None,
            "changes": record.get("revision_changes", []),
            "diff": "\n".join(
                difflib.unified_diff(
                    parent_text.splitlines(),
                    text.splitlines(),
                    fromfile=f"run:{parent_id}",
                    tofile=f"draft:{record['run_id']}",
                    lineterm="",
                )
            ),
            "original_preserved": True,
        }
