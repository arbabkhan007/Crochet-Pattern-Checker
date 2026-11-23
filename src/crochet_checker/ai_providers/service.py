"""Run lifecycle, history persistence, and explicit revalidated draft revisions."""

from __future__ import annotations

import difflib
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Iterable

from .history import ConsensusHistoryStore
from .orchestrator import ConsensusRunner, DEFAULT_REVIEW_ROLES
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
        report: Any = None
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
            safe_error = "Consensus run failed before a complete, safely persisted result was available."
            try:
                failure_record = self.store.get_run(run_id) or record
            except Exception:
                failure_record = record
            failure_report = (
                self._persistence_failure_report(report, run_id)
                if isinstance(report, dict)
                else self._execution_failure_report(run_id, failure_record)
            )
            try:
                self.store.save_failure_report(run_id, failure_report, safe_error)
            except Exception:
                # If persistence itself is unavailable, retain the existing minimal
                # failure status as a last resort; never expose exception contents.
                self.store.mark_failed(run_id, safe_error)
        return self.store.get_run(run_id)

    def _execution_failure_report(
        self, run_id: str, record: dict[str, Any]
    ) -> dict[str, Any]:
        providers = list(getattr(self.runner, "providers", self.catalog.providers))
        fallbacks = dict(getattr(self.runner, "fallbacks", self.catalog.fallbacks))
        selected_ids = tuple(
            getattr(self.runner, "selected_ids", self.catalog.selected_ids)
        )
        required_ids = tuple(
            getattr(self.runner, "required_provider_ids", self.catalog.required_ids)
        )
        issues = list(
            getattr(self.runner, "configuration_issues", self.catalog.configuration_issues)
        )
        availability = list(
            getattr(
                self.runner,
                "availability",
                [item.to_dict() for item in self.catalog.availability],
            )
        )
        roles = dict(getattr(self.runner, "roles", {}))
        provider_by_id = {item.provider_id: item for item in providers}
        availability_by_id = {item.get("provider_id"): item for item in availability}
        for index, provider_id in enumerate(selected_ids):
            provider = provider_by_id.get(provider_id)
            available = availability_by_id.get(provider_id, {})
            roles.setdefault(
                provider_id,
                (provider.role if provider else None)
                or available.get("role")
                or DEFAULT_REVIEW_ROLES[index % len(DEFAULT_REVIEW_ROLES)],
            )
        for primary, fallback in fallbacks.items():
            roles.setdefault(fallback.provider_id, roles.get(primary, fallback.role))
        for detail in availability:
            for primary in detail.get("fallback_for", []):
                provider_id = detail.get("provider_id")
                if provider_id:
                    roles.setdefault(
                        provider_id,
                        roles.get(primary)
                        or detail.get("role")
                        or "stitch_arithmetic",
                    )
        configs = {item.provider_id: item for item in providers}
        configs.update({item.provider_id: item for item in fallbacks.values()})
        states = []
        phases = ("independent", "cross_examination", "adversarial_review")
        for provider_id, config in configs.items():
            states.append(
                {
                    **config.public_dict(),
                    "required": provider_id in required_ids,
                    "role": roles.get(provider_id) or config.role,
                    "status": "outcome_unknown_after_orchestration_failure",
                    "participation_status": "unknown",
                    "independent_participated": None,
                    "fully_completed": None,
                    "required_slot_satisfied": None,
                    "required_slot_satisfied_by": None,
                    "phase_status": {phase: "unknown" for phase in phases},
                    "phase_errors": {},
                    "attempt_count": None,
                    "is_fallback": provider_id not in selected_ids,
                    "failure_reason": "The run ended before a complete provider-call record was returned.",
                }
            )
        for provider_id in selected_ids:
            if provider_id in configs:
                continue
            detail = availability_by_id.get(provider_id, {})
            issue = next(
                (
                    item
                    for item in issues
                    if f"{provider_id} is selected but not configured" in item
                ),
                "Selected provider is not configured for this run.",
            )
            states.append(
                {
                    "provider_id": provider_id,
                    "model": detail.get("model"),
                    "family": detail.get("family"),
                    "required": provider_id in required_ids,
                    "role": roles.get(provider_id) or detail.get("role"),
                    "status": "not_configured",
                    "required_slot_satisfied": False
                    if provider_id in required_ids
                    else None,
                    "required_slot_satisfied_by": None,
                    "participation_status": "not_attempted",
                    "independent_participated": False,
                    "fully_completed": False,
                    "phase_status": {phase: "not_run" for phase in phases},
                    "phase_errors": {},
                    "configuration_error": issue,
                    "missing_configuration": list(
                        detail.get("missing_configuration", [])
                    ),
                    "attempt_count": 0,
                    "is_fallback": False,
                }
            )
        for detail in availability:
            provider_id = detail.get("provider_id")
            fallback_for = list(detail.get("fallback_for", []))
            if not fallback_for or provider_id in configs or provider_id in selected_ids:
                continue
            states.append(
                {
                    "provider_id": provider_id,
                    "model": detail.get("model"),
                    "family": detail.get("family"),
                    "required": False,
                    "role": roles.get(provider_id) or detail.get("role"),
                    "status": "not_configured",
                    "participation_status": "not_attempted",
                    "independent_participated": False,
                    "fully_completed": False,
                    "phase_status": {phase: "not_run" for phase in phases},
                    "phase_errors": {},
                    "configuration_error": next(
                        (
                            item
                            for item in issues
                            if f"Fallback {provider_id} " in item
                        ),
                        "Configured fallback is not available for this run.",
                    ),
                    "missing_configuration": list(
                        detail.get("missing_configuration", [])
                    ),
                    "attempt_count": 0,
                    "is_fallback": True,
                    "fallback_for": fallback_for,
                }
            )
        configured_models = [item.public_dict() for item in providers]
        unknown_states = [
            item
            for item in states
            if item["status"] == "outcome_unknown_after_orchestration_failure"
        ]
        deterministic = {
            "valid": None,
            "status": "RESULT_UNAVAILABLE",
            "score": None,
            "errors": None,
            "warnings": None,
            "stitch_count": None,
            "stitch_counts": None,
            "execution_time_seconds": None,
            "result_note": "The run did not return a final deterministic-check record.",
        }
        policy_reason = (
            "The orchestrator did not return enough information to verify participation, "
            "review phases, evidence, or agreement; consensus was not evaluated."
        )
        return {
            "report_schema_version": 1,
            "execution_status": "failed",
            "run_id": run_id,
            "created_at": record.get("created_at")
            or datetime.now(timezone.utc).isoformat(),
            "pattern_hash": record.get("pattern_hash"),
            "revision": {
                "parent_run_id": record.get("parent_run_id"),
                "root_run_id": record.get("root_run_id") or run_id,
                "revision_number": int(record.get("revision_number", 0)),
                "max_revisions": self.settings.max_revisions,
                "original_pattern_hash": record.get("pattern_hash")
                if not record.get("parent_run_id")
                else None,
                "changes": record.get("revision_changes", []),
                "diff": None,
                "original_preserved": True,
            },
            "review_mode": "multi_provider_consensus",
            "authority_note": "Deterministic written-text checks remain authoritative for checked rules. AI findings cannot override arithmetic.",
            "execution_failure": {
                "code": "orchestration_failure",
                "message": "The review orchestrator failed before a complete report could be returned.",
                "last_known_stage": (record.get("progress") or {}).get("stage"),
                "participation_and_call_records": "unknown; no provider is represented as a confirmed participant",
            },
            "deterministic": deterministic,
            "models": {
                "configured": configured_models,
                "fallbacks": {
                    primary: config.public_dict()
                    for primary, config in fallbacks.items()
                },
                "selected_provider_ids": list(selected_ids),
                "required_provider_ids": list(required_ids),
                "configuration_issues": issues,
                "participating": [],
                "failed": [
                    item for item in states if item["status"] == "not_configured"
                ],
                "unknown": unknown_states,
                "states": states,
                "availability": availability,
                "participation": {
                    "selected_provider_count": len(selected_ids),
                    "selected_independent_success_count": None,
                    "selected_independent_participation_ratio": None,
                    "independent_success_count": None,
                    "fully_completed_count": None,
                    "minimum_independent_models": self.settings.min_participating_models,
                    "required_provider_count": len(required_ids),
                    "required_target": self.settings.required_participant_target(
                        len(required_ids)
                    ),
                    "minimum_participation_ratio": self.settings.min_participation_ratio,
                    "strict_required_participation": self.settings.strict_required_participation,
                    "required_slots_satisfied": None,
                    "required_slots": [
                        {
                            "required_provider_id": provider_id,
                            "satisfied": None,
                            "satisfied_by_provider_id": None,
                        }
                        for provider_id in required_ids
                    ],
                    "required_roles": list(self.settings.required_roles),
                    "completed_roles": None,
                    "missing_roles": None,
                    "roles_status": "unknown_due_to_orchestration_failure",
                    "result_note": "Provider participation cannot be confirmed from the failed orchestration result.",
                },
            },
            "rounds": {
                "independent": [],
                "cross_examination": [],
                "adversarial_review": [],
                "phases": {
                    phase: {
                        "status": "unknown",
                        "reason": "The orchestrator returned no complete phase record.",
                    }
                    for phase in phases
                },
                "provider_calls": [],
                "provider_call_records_complete": False,
                "provider_calls_may_have_occurred": True,
            },
            "findings": [],
            "findings_status": "unknown_due_to_orchestration_failure",
            "findings_records_complete": False,
            "review_coverage": [],
            "ai_consensus": {
                "status": "NOT_EVALUATED_DUE_TO_ORCHESTRATION_FAILURE",
                "threshold": self.settings.consensus_threshold,
                "policy": {
                    "status": "not_satisfied",
                    "met": False,
                    "checks": {},
                    "reasons": [policy_reason],
                },
                "issues": [],
                "issues_status": "not_evaluated",
                "disagreements": [],
                "disagreement_records_complete": False,
                "dissent_status": "not_evaluated",
                "open_questions": [],
                "open_questions_status": "not_evaluated",
                "grounded_findings": 0,
                "ungrounded_findings": 0,
                "reason_consensus_not_reached": policy_reason,
            },
            "correction_proposals": [],
            "scoring": {
                "weighted_score": None,
                "max_score": 100,
                "interpretation": "Unavailable because orchestration failed; not a correctness score.",
            },
            "telemetry": {
                "provider_call_count": None,
                "successful_provider_calls": None,
                "failed_provider_calls": None,
                "call_records_complete": False,
                "total_latency_ms": None,
                "estimated_cost_usd": None,
            },
            "construction_verification": {
                "written_unverified_steps": [],
                "written_gap_scan": "result_unavailable",
                "written_steps_all_parsed": None,
                "physical_sample_tested": False,
                "physical_verification_note": "No physical build or test was performed.",
            },
            "gate": {
                "approved": False,
                "status": "NOT APPROVED – HUMAN REVIEW REQUIRED",
                "approval_scope": "No approval is issued when orchestration fails before a complete report is produced.",
                "blockers": [
                    {
                        "code": "orchestration_failure",
                        "message": "A complete deterministic and provider report was not returned.",
                    }
                ],
                "blocker_count": 1,
                "required_model_participation_satisfied": False,
                "consensus_policy_satisfied": False,
                "deterministic_validation_satisfied": False,
                "human_review_required": True,
                "physical_construction_verified": False,
                "physical_verification_required_but_missing": False,
                "delivery_authorized": False,
            },
            "approval_status": "NOT APPROVED – HUMAN REVIEW REQUIRED",
            "approved": False,
        }

    @staticmethod
    def _persistence_failure_report(
        report: dict[str, Any], run_id: str
    ) -> dict[str, Any]:
        failed = dict(report)
        failure = {
            "code": "report_persistence_failure",
            "message": "The completed report could not be saved normally; no approval is issued from this run record.",
        }
        failed["execution_status"] = "failed_to_persist_completed_report"
        failed["execution_failure"] = failure
        failed["approved"] = False
        failed["approval_status"] = "NOT APPROVED – HUMAN REVIEW REQUIRED"
        gate = dict(failed.get("gate") or {})
        blockers = list(gate.get("blockers") or [])
        blockers.append(
            {
                "code": "report_persistence_failure",
                "message": failure["message"],
            }
        )
        gate.update(
            {
                "approved": False,
                "status": "NOT APPROVED – HUMAN REVIEW REQUIRED",
                "blockers": blockers,
                "blocker_count": len(blockers),
                "human_review_required": True,
                "delivery_authorized": False,
            }
        )
        failed["gate"] = gate
        failed["run_id"] = run_id
        return failed

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
