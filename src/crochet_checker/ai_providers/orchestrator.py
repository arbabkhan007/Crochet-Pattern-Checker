"""Parallel multi-round provider review, evidence aggregation, and hard delivery gate."""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
import math
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from ..validation.validator import validate_pattern
from ..verification.limits import unread_notes
from .provider_adapters import (
    ProviderCatalog,
    ProviderConfig,
    ProviderRequestError,
    ProviderResponse,
    create_adapter,
)
from .review import (
    ParsedReview,
    ReviewFinding,
    SEVERITY_RANK,
    anonymized_peer_packet,
    build_system_prompt,
    build_user_prompt,
    deterministic_context_dict,
    parse_review_response,
)
from .settings import ConsensusSettings

DEFAULT_REVIEW_ROLES = (
    "stitch_arithmetic",
    "construction_assembly",
    "instruction_clarity",
    "materials_completeness",
    "adversarial_counterexample",
)
ProgressCallback = Callable[[dict[str, Any]], Any]


@dataclass
class CallOutcome:
    config: ProviderConfig
    alias: str
    role: str
    phase: str
    review: ParsedReview | None
    call_record: dict[str, Any]

    @property
    def succeeded(self) -> bool:
        return self.review is not None and self.call_record.get("status") == "succeeded"


class ConsensusRunner:
    """Run deterministic checks plus independent, cross-examination, and adversarial AI rounds."""

    def __init__(
        self,
        *,
        catalog: ProviderCatalog | None = None,
        providers: Sequence[ProviderConfig] | None = None,
        required_provider_ids: Sequence[str] | None = None,
        fallbacks: Mapping[str, ProviderConfig] | None = None,
        configuration_issues: Sequence[str] = (),
        settings: ConsensusSettings | None = None,
        adapter_factory: Callable[[ProviderConfig], Any] = create_adapter,
        adapters: Mapping[str, Any] | None = None,
        validator: Callable[[str], Any] = validate_pattern,
        unverified_steps: Callable[[str], list[str]] = unread_notes,
    ):
        self.catalog = catalog
        self.settings = settings or ConsensusSettings.from_env()
        if catalog:
            self.providers = list(catalog.providers)
            self.required_provider_ids = tuple(catalog.required_ids)
            self.fallbacks = dict(catalog.fallbacks)
            self.configuration_issues = list(catalog.configuration_issues)
            self.selected_ids = tuple(catalog.selected_ids)
            self.availability = [item.to_dict() for item in catalog.availability]
        else:
            self.providers = list(providers or [])
            self.required_provider_ids = tuple(
                required_provider_ids
                if required_provider_ids is not None
                else [item.provider_id for item in self.providers if item.required]
            )
            self.fallbacks = dict(fallbacks or {})
            self.configuration_issues = list(configuration_issues)
            self.selected_ids = tuple(item.provider_id for item in self.providers)
            self.availability = []
        self.validator = validator
        self.unverified_steps = unverified_steps
        injected = dict(adapters or {})
        self.adapters: dict[str, Any] = {}
        for config in [*self.providers, *self.fallbacks.values()]:
            self.adapters[config.provider_id] = injected.get(
                config.provider_id
            ) or adapter_factory(config)
        self.roles = self._assign_roles()

    def _assign_roles(self) -> dict[str, str]:
        configs = {config.provider_id: config for config in self.providers}
        availability = {
            item.get("provider_id"): item for item in self.availability
        }
        roles: dict[str, str] = {}
        for index, provider_id in enumerate(self.selected_ids):
            config = configs.get(provider_id)
            available = availability.get(provider_id, {})
            configured_role = (
                config.role if config is not None else available.get("role")
            )
            roles[provider_id] = configured_role or DEFAULT_REVIEW_ROLES[
                index % len(DEFAULT_REVIEW_ROLES)
            ]
        for primary, fallback in self.fallbacks.items():
            roles[fallback.provider_id] = roles.get(
                primary, fallback.role or "stitch_arithmetic"
            )
        for item in self.availability:
            for primary in item.get("fallback_for", []):
                provider_id = item.get("provider_id")
                if provider_id:
                    roles[provider_id] = roles.get(primary) or item.get(
                        "role"
                    ) or "stitch_arithmetic"
        return roles

    def _semaphore(self) -> asyncio.Semaphore:
        loop = asyncio.get_running_loop()
        cache_name = "_crochet_consensus_semaphores"
        cache = getattr(loop, cache_name, None)
        if cache is None:
            cache = {}
            try:
                setattr(loop, cache_name, cache)
            except (AttributeError, TypeError):
                return asyncio.Semaphore(self.settings.max_concurrency)
        return cache.setdefault(
            self.settings.max_concurrency,
            asyncio.Semaphore(self.settings.max_concurrency),
        )

    async def run(
        self,
        pattern_text: str,
        *,
        run_id: str | None = None,
        revision: dict[str, Any] | None = None,
        progress: ProgressCallback | None = None,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        semaphore = self._semaphore()
        created_at = datetime.now(timezone.utc).isoformat()
        pattern_hash = hashlib.sha256(pattern_text.encode("utf-8")).hexdigest()
        await _notify(
            progress,
            "deterministic_validation",
            0,
            "Running independent written-text checks",
        )
        validator_error = None
        deterministic_report = None
        try:
            deterministic_report = self.validator(pattern_text)
        except Exception:
            validator_error = "Deterministic validator execution failed"
        try:
            notes = list(self.unverified_steps(pattern_text))
        except Exception:
            notes = ["Written construction coverage could not be determined."]
        deterministic = _serialize_deterministic(
            deterministic_report, validator_error, notes
        )
        if deterministic_report is None:
            deterministic_context = {
                "authority": "Independent written-text checker; AI cannot override checked counts.",
                "valid": False,
                "status": "CHECK_FAILED",
                "errors": [validator_error or "Deterministic validation failed"],
                "warnings": [],
                "unparsed_or_unverified_written_steps": notes,
                "physical_construction_verified": False,
            }
        else:
            deterministic_context = deterministic_context_dict(
                deterministic_report, notes
            )

        aliases = {
            config.provider_id: _reviewer_alias(i)
            for i, config in enumerate(self.providers)
        }
        call_records: list[dict[str, Any]] = []
        reviews: list[dict[str, Any]] = []
        active: dict[str, tuple[ProviderConfig, str, str, ParsedReview]] = {}
        first = await asyncio.gather(
            *[
                self._call(
                    config,
                    semaphore,
                    aliases[config.provider_id],
                    self.roles[config.provider_id],
                    "independent",
                    pattern_text,
                    None,
                    None,
                )
                for config in self.providers
            ]
        )
        primary_outcomes = {item.config.provider_id: item for item in first}
        for item in first:
            call_records.append(item.call_record)
            if item.succeeded:
                active[item.config.provider_id] = (
                    item.config,
                    item.alias,
                    item.role,
                    item.review,
                )
                reviews.append(_review_dict(item))
        fallback_requests = [
            (primary, result, self.fallbacks[primary])
            for primary, result in primary_outcomes.items()
            if not result.succeeded and primary in self.fallbacks
        ]
        fallbacks = await asyncio.gather(
            *[
                self._call(
                    config,
                    semaphore,
                    result.alias,
                    self.roles.get(primary, "stitch_arithmetic"),
                    "independent",
                    pattern_text,
                    None,
                    None,
                )
                for primary, result, config in fallback_requests
            ]
        )
        for (primary, _result, config), outcome in zip(
            fallback_requests, fallbacks, strict=True
        ):
            outcome.call_record.update({"is_fallback": True, "fallback_for": primary})
            call_records.append(outcome.call_record)
            if outcome.succeeded:
                active[config.provider_id] = (
                    config,
                    outcome.alias,
                    outcome.role,
                    outcome.review,
                )
                reviews.append(_review_dict(outcome))
        await _notify(
            progress,
            "independent_review",
            2,
            f"Independent structured reviewers: {len(active)}",
        )

        phase_status: dict[str, dict[str, Any]] = {
            "independent": _phase_summary(
                [*first, *fallbacks], succeeded_override=len(active)
            ),
        }
        phase_reviews: dict[str, dict[str, ParsedReview]] = {
            "independent": {pid: item[3] for pid, item in active.items()}
        }
        active_groups = [(value[1], value[3]) for value in active.values()]

        cross: list[CallOutcome] = []
        if self.settings.enable_cross_examination:
            if len(active) < 2:
                phase_status["cross_examination"] = {
                    "status": "skipped",
                    "reason": "At least two successful independent reviewers are required.",
                    "succeeded": 0,
                    "failed": 0,
                    "expected": len(active),
                }
            else:
                await _notify(
                    progress,
                    "cross_examination",
                    2,
                    "Cross-examining anonymized peer findings",
                )
                cross = await asyncio.gather(
                    *[
                        self._call(
                            config,
                            semaphore,
                            alias,
                            role,
                            "cross_examination",
                            pattern_text,
                            deterministic_context,
                            anonymized_peer_packet(
                                [peer for peer in active_groups if peer[0] != alias]
                            ),
                        )
                        for config, alias, role, _review in active.values()
                    ]
                )
                for item in cross:
                    call_records.append(item.call_record)
                    if item.succeeded:
                        reviews.append(_review_dict(item))
                phase_status["cross_examination"] = _phase_summary(cross)
                phase_reviews["cross_examination"] = {
                    item.config.provider_id: item.review
                    for item in cross
                    if item.succeeded
                }
        else:
            phase_status["cross_examination"] = {
                "status": "disabled",
                "reason": "Disabled by configuration.",
                "succeeded": 0,
                "failed": 0,
                "expected": 0,
            }

        adv: list[CallOutcome] = []
        if self.settings.enable_adversarial_review:
            if active:
                await _notify(
                    progress, "adversarial_review", 3, "Running adversarial review"
                )
                aliases_by_id = {pid: value[1] for pid, value in active.items()}
                adv = await asyncio.gather(
                    *[
                        self._call(
                            config,
                            semaphore,
                            alias,
                            role,
                            "adversarial_review",
                            pattern_text,
                            deterministic_context,
                            anonymized_peer_packet(
                                _peer_reviews_for(pid, aliases_by_id, phase_reviews)
                            ),
                        )
                        for pid, (config, alias, role, _review) in active.items()
                    ]
                )
                for item in adv:
                    call_records.append(item.call_record)
                    if item.succeeded:
                        reviews.append(_review_dict(item))
                phase_status["adversarial_review"] = _phase_summary(adv)
                phase_reviews["adversarial_review"] = {
                    item.config.provider_id: item.review
                    for item in adv
                    if item.succeeded
                }
            else:
                phase_status["adversarial_review"] = {
                    "status": "skipped",
                    "reason": "No structured independent review succeeded.",
                    "succeeded": 0,
                    "failed": 0,
                    "expected": 0,
                }
        else:
            phase_status["adversarial_review"] = {
                "status": "disabled",
                "reason": "Disabled by configuration.",
                "succeeded": 0,
                "failed": 0,
                "expected": 0,
            }

        await _notify(
            progress,
            "evidence_consensus",
            4,
            "Grounding evidence and evaluating fail-closed gate",
        )
        findings = [finding for review in reviews for finding in review["findings"]]
        assessments = [
            {
                "provider_id": review["provider_id"],
                "model": review["model"],
                "phase": review["phase"],
                **assessment,
            }
            for review in reviews
            for assessment in review["assessments"]
        ]
        open_questions = [
            {
                "provider_id": review["provider_id"],
                "model": review["model"],
                "phase": review["phase"],
                "question": question,
            }
            for review in reviews
            for question in review["open_questions"]
        ]
        clusters = _build_issue_clusters(
            findings,
            pattern_text,
            set(active),
            self.settings.consensus_threshold,
            expected_participant_count=len(self.selected_ids),
        )
        disagreements = _build_disagreements(assessments, clusters)
        corrections = _correction_proposals(findings)
        states = _model_states(
            self.providers,
            self.fallbacks,
            self.required_provider_ids,
            call_records,
            active,
            phase_status,
            self.configuration_issues,
            selected_ids=self.selected_ids,
            availability=self.availability,
            roles=self.roles,
        )
        completed_count = sum(bool(item["fully_completed"]) for item in states)
        consensus_policy = _build_consensus_policy(
            states=states,
            selected_ids=self.selected_ids,
            required_ids=self.required_provider_ids,
            phase_status=phase_status,
            clusters=clusters,
            disagreements=disagreements,
            open_questions=open_questions,
            findings=findings,
            configuration_issues=self.configuration_issues,
            settings=self.settings,
        )
        for cluster in clusters:
            cluster["consensus_reached"] = bool(
                consensus_policy["met"] and cluster["support_threshold_met"]
            )
            cluster["consensus_blockers"] = (
                [] if cluster["consensus_reached"] else list(consensus_policy["reasons"])
            )
        gate = _build_gate(
            deterministic,
            notes,
            findings,
            disagreements,
            open_questions,
            self.selected_ids,
            self.required_provider_ids,
            states,
            self.configuration_issues,
            consensus_policy,
            self.settings,
        )
        scoring = _build_score(
            deterministic.get("score", 0),
            findings,
            clusters,
            len(active),
            completed_count,
            self.settings,
            len(self.required_provider_ids),
        )
        telemetry = _telemetry(
            call_records, int((time.perf_counter() - started) * 1000)
        )
        required_roles = list(self.settings.required_roles)
        complete_roles = sorted(
            {
                self.roles.get(pid, "")
                for pid, state in ((item["provider_id"], item) for item in states)
                if state["fully_completed"] and self.roles.get(pid, "")
            }
        )
        consensus_status = _consensus_status(
            len(active), clusters, disagreements, consensus_policy
        )
        if consensus_status == "GROUNDED_FINDINGS_AGREED":
            consensus_reason = None
        elif consensus_policy["reasons"]:
            consensus_reason = (
                "Consensus was not reached because "
                + "; ".join(consensus_policy["reasons"])
            )
        elif consensus_status == "NO_GROUNDED_FINDINGS_REPORTED":
            consensus_reason = (
                "No grounded findings were reported; no issue-level consensus claim is made."
            )
        else:
            consensus_reason = "No independent model review was confirmed."
        dissent_status = (
            "unresolved"
            if disagreements
            else "none_reported_in_completed_protocol"
            if consensus_policy["participation_protocol_met"]
            else "not_fully_evaluated"
        )
        selected_states = [
            item for item in states if item["provider_id"] in self.selected_ids
        ]
        selected_independent = sum(
            bool(item.get("independent_participated")) for item in selected_states
        )
        selected_participation_ratio = (
            round(selected_independent / len(self.selected_ids), 4)
            if self.selected_ids
            else 0.0
        )
        report = {
            "report_schema_version": 1,
            "execution_status": "completed",
            "run_id": run_id,
            "created_at": created_at,
            "pattern_hash": pattern_hash,
            "revision": revision or {"parent_run_id": None, "revision_number": 0},
            "review_mode": "multi_provider_consensus",
            "authority_note": "Deterministic written-text checks remain authoritative for checked rules. AI findings are advisory and never override arithmetic.",
            "deterministic": deterministic,
            "models": {
                "configured": [
                    {
                        **item.public_dict(),
                        "required": item.provider_id in self.required_provider_ids,
                    }
                    for item in self.providers
                ],
                "fallbacks": {
                    primary: item.public_dict()
                    for primary, item in self.fallbacks.items()
                },
                "selected_provider_ids": list(self.selected_ids),
                "required_provider_ids": list(self.required_provider_ids),
                "configuration_issues": list(self.configuration_issues),
                "participating": [
                    {
                        "provider_id": config.provider_id,
                        "model": config.model,
                        "role": role,
                        "required": config.provider_id in self.required_provider_ids,
                        "is_fallback": config.provider_id not in self.selected_ids,
                        "phases_succeeded": [
                            phase
                            for phase, group in phase_reviews.items()
                            if config.provider_id in group
                        ],
                    }
                    for config, _alias, role, _review in active.values()
                ],
                "failed": [
                    item
                    for item in states
                    if item["status"] in {"failed", "incomplete", "not_configured"}
                ],
                "states": states,
                "availability": self.availability,
                "participation": {
                    "selected_provider_count": len(self.selected_ids),
                    "selected_independent_success_count": selected_independent,
                    "selected_independent_participation_ratio": selected_participation_ratio,
                    "independent_success_count": len(active),
                    "fully_completed_count": completed_count,
                    "minimum_independent_models": self.settings.min_participating_models,
                    "required_provider_count": len(self.required_provider_ids),
                    "required_target": self.settings.required_participant_target(
                        len(self.required_provider_ids)
                    ),
                    "minimum_participation_ratio": self.settings.min_participation_ratio,
                    "strict_required_participation": self.settings.strict_required_participation,
                    "required_slots_satisfied": consensus_policy["checks"][
                        "required_provider_slots_met"
                    ],
                    "required_slots": [
                        {
                            "required_provider_id": item["provider_id"],
                            "satisfied": item.get(
                                "required_slot_satisfied",
                                item.get("fully_completed", False),
                            ),
                            "satisfied_by_provider_id": item.get(
                                "required_slot_satisfied_by"
                            ),
                        }
                        for item in states
                        if item.get("required")
                    ],
                    "required_roles": required_roles,
                    "completed_roles": complete_roles,
                    "missing_roles": [
                        role for role in required_roles if role not in complete_roles
                    ],
                },
            },
            "rounds": {
                "independent": [r for r in reviews if r["phase"] == "independent"],
                "cross_examination": [
                    r for r in reviews if r["phase"] == "cross_examination"
                ],
                "adversarial_review": [
                    r for r in reviews if r["phase"] == "adversarial_review"
                ],
                "phases": phase_status,
                "provider_calls": call_records,
                "provider_call_records_complete": True,
                "provider_calls_may_have_occurred": bool(call_records),
            },
            "findings": findings,
            "findings_status": "complete_for_recorded_successful_reviews",
            "findings_records_complete": True,
            "review_coverage": [
                {
                    "provider_id": review["provider_id"],
                    "model": review["model"],
                    "phase": review["phase"],
                    "role": review["role"],
                    **coverage,
                }
                for review in reviews
                for coverage in review["coverage"]
            ],
            "ai_consensus": {
                "status": consensus_status,
                "reason_consensus_not_reached": consensus_reason,
                "threshold": self.settings.consensus_threshold,
                "policy": consensus_policy,
                "agreement_method": "Grounded issue clusters; one independent contribution per explicitly selected provider slot (a configured fallback may substitute); support ratios use all selected slots and confidence is not a vote weight. Consensus is reported only when the configured participation, role, phase, evidence, dissent, question, and issue-support policy is satisfied.",
                "issues": clusters,
                "issues_status": "evaluated_for_recorded_successful_reviews",
                "disagreements": disagreements,
                "disagreement_records_complete": True,
                "dissent_status": dissent_status,
                "open_questions": open_questions,
                "open_questions_status": "reported_for_recorded_successful_reviews",
                "grounded_findings": sum(
                    item["evidence_status"] == "grounded_text" for item in findings
                ),
                "ungrounded_findings": sum(
                    item["evidence_status"] != "grounded_text" for item in findings
                ),
            },
            "correction_proposals": corrections,
            "scoring": scoring,
            "telemetry": telemetry,
            "construction_verification": {
                "written_unverified_steps": notes,
                "written_gap_scan": "gaps_flagged"
                if notes
                else "no_known_gaps_flagged",
                "written_steps_all_parsed": None,
                "physical_sample_tested": False,
                "physical_verification_note": "No physical crochet build, fit, gauge swatch, fabric, durability, or finishing test was performed. A gap scan that flags no known issue is not proof that every instruction was interpreted.",
            },
            "gate": gate,
            "approval_status": gate["status"],
            "approved": gate["approved"],
        }
        await _notify(progress, "completed", 5, "Consensus report ready")
        return report

    async def _call(
        self,
        config: ProviderConfig,
        semaphore: asyncio.Semaphore,
        alias: str,
        role: str,
        phase: str,
        pattern: str,
        deterministic: dict[str, Any] | None,
        peer: dict[str, Any] | None,
    ) -> CallOutcome:
        adapter = self.adapters.get(config.provider_id)
        if adapter is None:
            return CallOutcome(
                config,
                alias,
                role,
                phase,
                None,
                _failure(
                    config, phase, role, "Provider adapter is not configured", 0, 0
                ),
            )
        prefix = alias.split()[-1]
        reviewer = {
            "independent": prefix,
            "cross_examination": prefix + "-X",
            "adversarial_review": prefix + "-A",
        }.get(phase, prefix)
        system = build_system_prompt(phase, role)
        user = build_user_prompt(
            phase,
            role,
            pattern,
            anonymized_context=peer,
            deterministic_context=deterministic,
        )
        budget = (
            config.timeout_seconds * (config.max_retries + 1)
            + 15 * config.max_retries
            + 2
        )
        start = time.perf_counter()
        try:
            async with semaphore:
                response = await asyncio.wait_for(
                    adapter.generate(system, user), timeout=budget
                )
            if not isinstance(response, ProviderResponse):
                raise ValueError("unsupported adapter response")
            review = parse_review_response(
                response.text,
                provider_id=config.provider_id,
                model=config.model,
                phase=phase,
                role=role,
                reviewer_alias=reviewer,
                pattern_text=pattern,
            )
            if phase in {"cross_examination", "adversarial_review"}:
                _validate_peer_coverage(review, peer)
            record = {
                "provider_id": config.provider_id,
                "model": config.model,
                "reported_model": response.reported_model,
                "phase": phase,
                "role": role,
                "status": "succeeded",
                "attempts": response.attempts,
                "latency_ms": response.latency_ms,
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
                "estimated_cost_usd": response.estimated_cost_usd,
                "error": None,
            }
            return CallOutcome(config, alias, role, phase, review, record)
        except asyncio.TimeoutError:
            message, attempts, latency = (
                "Provider call timed out",
                1,
                int((time.perf_counter() - start) * 1000),
            )
        except ProviderRequestError as exc:
            message, attempts, latency = (
                _safe_provider_error(exc),
                exc.attempts,
                exc.latency_ms,
            )
        except ValueError as exc:
            safe = str(exc)
            allowed = {
                "provider response was not structured JSON",
                "provider response was not valid structured JSON",
                "provider response must be a JSON object",
            }
            message = (
                safe
                if safe in allowed
                else "Provider returned an invalid structured review"
            )
            attempts, latency = 1, int((time.perf_counter() - start) * 1000)
        except Exception:
            message, attempts, latency = (
                "Provider adapter failed unexpectedly",
                1,
                int((time.perf_counter() - start) * 1000),
            )
        return CallOutcome(
            config,
            alias,
            role,
            phase,
            None,
            _failure(config, phase, role, message, attempts, latency),
        )


def _validate_peer_coverage(review: ParsedReview, peer: dict[str, Any] | None) -> None:
    expected = {
        finding.get("finding_id")
        for reviewer in (peer or {}).get("reviewers", [])
        for finding in reviewer.get("findings", [])
        if finding.get("finding_id")
    }
    submitted = [item.finding_id for item in review.assessments]
    if len(submitted) != len(set(submitted)) or set(submitted) != expected:
        raise ValueError("Peer assessment coverage is incomplete")


def _serialize_deterministic(
    report: Any, error: str | None, notes: list[str]
) -> dict[str, Any]:
    if report is None:
        return {
            "valid": False,
            "status": "CHECK_FAILED",
            "score": 0,
            "errors": [error or "Deterministic validation failed"],
            "warnings": [],
            "stitch_count": 0,
            "stitch_counts": {},
            "execution_time_seconds": None,
            "unverified_written_steps": list(notes),
        }
    return {
        "valid": bool(getattr(report, "valid", False)),
        "status": str(getattr(report, "overall_status", "UNKNOWN")),
        "score": int(getattr(report, "score", 0) or 0),
        "errors": [
            _issue_dict(item, "error") for item in getattr(report, "errors", []) or []
        ],
        "warnings": [
            _issue_dict(item, "warning")
            for item in getattr(report, "warnings", []) or []
        ],
        "stitch_count": int(getattr(report, "stitch_count", 0) or 0),
        "stitch_counts": _json_safe(getattr(report, "stitch_counts", {}) or {}),
        "execution_time_seconds": getattr(report, "execution_time", None),
        "unverified_written_steps": list(notes),
    }


def _issue_dict(item: Any, default: str) -> dict[str, str]:
    return {
        "message": str(getattr(item, "message", item)),
        "location": str(getattr(item, "location", "")),
        "severity": str(getattr(item, "severity", default)),
    }


def _phase_summary(
    outcomes: Sequence[CallOutcome], succeeded_override: int | None = None
) -> dict[str, Any]:
    successes = sum(item.succeeded for item in outcomes)
    failures = len(outcomes) - successes
    count = successes if succeeded_override is None else succeeded_override
    status = "completed" if failures == 0 else "partial" if count else "failed"
    return {
        "status": status,
        "succeeded": count,
        "failed": failures,
        "expected": len(outcomes),
    }


def _review_dict(outcome: CallOutcome) -> dict[str, Any]:
    assert outcome.review is not None
    return {
        "provider_id": outcome.config.provider_id,
        "model": outcome.config.model,
        "phase": outcome.phase,
        "reviewer_alias": outcome.alias,
        "role": outcome.role,
        "summary": outcome.review.summary,
        "coverage": [item.to_dict() for item in outcome.review.coverage],
        "findings": [item.to_dict() for item in outcome.review.findings],
        "assessments": [item.to_dict() for item in outcome.review.assessments],
        "open_questions": list(outcome.review.open_questions),
    }


def _safe_provider_error(error: ProviderRequestError) -> str:
    allowed = {
        "Provider request timed out",
        "Provider transport failed",
        "Provider rate limit persisted",
        "Provider service error persisted",
        "Provider rejected the request",
        "Provider returned invalid JSON",
        "Provider returned an unexpected response shape",
        "Provider response contained no chat content",
        "Provider response contained no message content",
        "Provider response contained no generated content",
    }
    raw_message = str(error)
    message = raw_message if raw_message in allowed else "Provider request failed"
    status = error.status_code
    return (
        f"HTTP {status}: {message}"
        if isinstance(status, int) and 100 <= status <= 599
        else message
    )


def _failure(
    config: ProviderConfig,
    phase: str,
    role: str,
    error: str,
    attempts: int,
    latency: int,
) -> dict[str, Any]:
    return {
        "provider_id": config.provider_id,
        "model": config.model,
        "reported_model": None,
        "phase": phase,
        "role": role,
        "status": "failed",
        "attempts": attempts,
        "latency_ms": latency,
        "input_tokens": None,
        "output_tokens": None,
        "estimated_cost_usd": None,
        "error": error[:300],
    }


def _build_issue_clusters(
    findings: list[dict[str, Any]],
    pattern_text: str,
    independent_ids: set[str],
    threshold: float,
    *,
    expected_participant_count: int,
) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for item in findings:
        if item.get("evidence_status") != "grounded_text":
            continue
        groups[_cluster_key(item, pattern_text)].append(item)
    clusters = []
    lines = pattern_text.splitlines()
    for index, (_key, observations) in enumerate(
        sorted(groups.items(), key=lambda item: str(item[0])), 1
    ):
        models = sorted(
            {
                str(item["provider_id"])
                for item in observations
                if item.get("phase") == "independent"
            }
        )
        observed = sorted({str(item["provider_id"]) for item in observations})
        ratio = (
            len(models) / expected_participant_count
            if expected_participant_count
            else 0.0
        )
        first = observations[0]
        line = first.get("matched_line_number")
        severity = max(
            (str(item.get("severity", "major")) for item in observations),
            key=lambda value: SEVERITY_RANK.get(value, 2),
        )
        clusters.append(
            {
                "cluster_id": f"issue-{index}",
                "category": first.get("category", "other"),
                "issue_code": first.get("issue_code", ""),
                "issue": first.get("issue", ""),
                "location": first.get("location", ""),
                "line_number": line,
                "source_instruction": first.get("source_instruction", ""),
                "evidence_quote": first.get("evidence_quote", ""),
                "source_line": lines[line - 1]
                if isinstance(line, int) and 1 <= line <= len(lines)
                else None,
                "expected_count": first.get("expected_count"),
                "actual_count": first.get("actual_count"),
                "severity": severity,
                "explanations": _distinct(
                    item.get("explanation", "") for item in observations
                ),
                "independent_support_count": len(models),
                "independent_participant_count": len(independent_ids),
                "expected_independent_provider_count": expected_participant_count,
                "support_basis": "Explicitly selected provider slots; configured fallbacks may substitute for a selected primary.",
                "support_ratio": round(ratio, 4),
                "support_threshold_met": expected_participant_count >= 2
                and len(models) >= 2
                and len(models) > expected_participant_count / 2
                and ratio >= threshold,
                "consensus_reached": False,
                "supporting_models": models,
                "observed_models": observed,
                "reported_in_phases": sorted(
                    {str(item.get("phase", "")) for item in observations}
                ),
                "observation_count": len(observations),
                "finding_ids": [
                    str(item.get("finding_id", "")) for item in observations
                ],
            }
        )
    return clusters


def _cluster_key(item: dict[str, Any], pattern_text: str) -> tuple[Any, ...]:
    line = item.get("matched_line_number")
    lines = pattern_text.splitlines()
    source = (
        _normalize(lines[line - 1])
        if isinstance(line, int) and 1 <= line <= len(lines)
        else _normalize(str(item.get("evidence_quote", "")))
    )
    expected, actual = (
        _count(item.get("expected_count")),
        _count(item.get("actual_count")),
    )
    code = str(item.get("issue_code") or "").casefold()
    claim = (
        f"{code}|{expected}|{actual}"
        if code
        else f"{_normalize(str(item.get('issue') or item.get('explanation') or ''))}|{expected}|{actual}"
    )
    return str(item.get("category", "other")), source, claim


def _build_disagreements(
    assessments: list[dict[str, Any]], clusters: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    result = []
    known = {fid for cluster in clusters for fid in cluster["finding_ids"]}
    for item in assessments:
        if item.get("position") in {"disagree", "uncertain"}:
            fid = str(item.get("finding_id", ""))
            result.append(
                {
                    "type": "reviewer_disagreement"
                    if item["position"] == "disagree"
                    else "reviewer_uncertainty",
                    "finding_id": fid,
                    "target_found_in_consensus": fid in known,
                    "provider_id": item.get("provider_id"),
                    "model": item.get("model"),
                    "phase": item.get("phase"),
                    "position": item.get("position"),
                    "reason": item.get("reason", ""),
                    "evidence_quote": item.get("evidence_quote", ""),
                    "evidence_status": item.get("evidence_status", "not_provided"),
                    "resolution": "Unresolved; model opinion is not deterministic proof.",
                }
            )
    for i, left in enumerate(clusters):
        for right in clusters[i + 1 :]:
            if (
                left.get("category") != right.get("category")
                or left.get("line_number") is None
                or left.get("line_number") != right.get("line_number")
            ):
                continue
            conflict = any(
                left.get(field) is not None
                and right.get(field) is not None
                and _count(left.get(field)) != _count(right.get(field))
                for field in ("expected_count", "actual_count")
            )
            if conflict:
                result.append(
                    {
                        "type": "conflicting_count_claims",
                        "line_number": left.get("line_number"),
                        "category": left.get("category"),
                        "finding_ids": left.get("finding_ids", [])
                        + right.get("finding_ids", []),
                        "claims": [
                            {
                                "expected_count": left.get("expected_count"),
                                "actual_count": left.get("actual_count"),
                                "supporting_models": left.get("supporting_models", []),
                            },
                            {
                                "expected_count": right.get("expected_count"),
                                "actual_count": right.get("actual_count"),
                                "supporting_models": right.get("supporting_models", []),
                            },
                        ],
                        "resolution": "Unresolved conflicting model claims; deterministic checks remain authoritative.",
                    }
                )
    return result


def _correction_proposals(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result, seen = [], set()
    for item in findings:
        correction = str(item.get("proposed_correction", "")).strip()
        key = (
            item.get("provider_id"),
            item.get("finding_id"),
            item.get("evidence_quote"),
            correction,
        )
        if not correction or key in seen:
            continue
        seen.add(key)
        result.append(
            {
                "proposal_id": f"draft-proposal-{len(result) + 1}",
                "provider_id": item.get("provider_id"),
                "model": item.get("model"),
                "phase": item.get("phase"),
                "finding_id": item.get("finding_id"),
                "original_excerpt": item.get("evidence_quote", ""),
                "proposed_correction_snippet": correction,
                "reason": item.get("explanation") or item.get("issue", ""),
                "confidence": item.get("confidence", 0.0),
                "status": "PROPOSAL ONLY — NOT APPLIED OR VALIDATED",
            }
        )
    return result


def _model_states(
    providers: list[ProviderConfig],
    fallbacks: Mapping[str, ProviderConfig],
    required_ids: Sequence[str],
    calls: list[dict[str, Any]],
    active: Mapping[str, Any],
    phase_status: Mapping[str, Any],
    config_issues: Sequence[str],
    *,
    selected_ids: Sequence[str],
    availability: Sequence[Mapping[str, Any]],
    roles: Mapping[str, str],
) -> list[dict[str, Any]]:
    configs = {item.provider_id: item for item in providers}
    configs.update({item.provider_id: item for item in fallbacks.values()})
    availability_by_id = {item.get("provider_id"): item for item in availability}
    logs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for call in calls:
        logs[call["provider_id"]].append(call)
    states = []
    required = set(required_ids)
    selected = set(selected_ids)
    phases = ("independent", "cross_examination", "adversarial_review")
    for pid, config in configs.items():
        records = logs.get(pid, [])
        phase_map = {
            phase: any(
                item.get("phase") == phase and item.get("status") == "succeeded"
                for item in records
            )
            for phase in phases
        }
        enabled = ["independent"]
        if phase_status.get("cross_examination", {}).get("status") != "disabled":
            enabled.append("cross_examination")
        if phase_status.get("adversarial_review", {}).get("status") != "disabled":
            enabled.append("adversarial_review")
        complete = pid in active and all(
            phase_map.get(phase, False) for phase in enabled
        )
        failed = any(item.get("status") == "failed" for item in records)
        is_fallback = pid not in selected
        status = (
            "not_attempted"
            if is_fallback and not records
            else "completed"
            if complete
            else "incomplete"
            if pid in active or failed
            else "not_configured"
        )
        if failed and pid not in active:
            status = "failed"
        active_role = next(
            (value[2] for value in active.values() if value[0].provider_id == pid),
            None,
        )
        role = active_role or roles.get(pid) or config.role
        errors = defaultdict(list)
        for item in records:
            if item.get("status") == "failed":
                errors[item["phase"]].append(item.get("error", "Provider call failed"))
        states.append(
            {
                **config.public_dict(),
                "required": pid in required,
                "role": role,
                "status": status,
                "independent_participated": phase_map["independent"],
                "fully_completed": complete,
                "phase_status": phase_map,
                "phase_errors": dict(errors),
                "attempt_count": sum(
                    int(item.get("attempts") or 0) for item in records
                ),
                "is_fallback": is_fallback,
            }
        )

    for pid in selected_ids:
        if pid in configs:
            continue
        detail = availability_by_id.get(pid, {})
        issue = next(
            (
                item
                for item in config_issues
                if f"{pid} is selected but not configured" in item
            ),
            "Selected provider is not configured for this run.",
        )
        states.append(
            {
                "provider_id": pid,
                "model": detail.get("model"),
                "family": detail.get("family"),
                "required": pid in required,
                "role": roles.get(pid) or detail.get("role"),
                "status": "not_configured",
                "independent_participated": False,
                "fully_completed": False,
                "phase_status": {phase: False for phase in phases},
                "phase_errors": {},
                "configuration_error": issue,
                "missing_configuration": list(detail.get("missing_configuration", [])),
                "attempt_count": 0,
                "is_fallback": False,
            }
        )

    for detail in availability:
        pid = detail.get("provider_id")
        fallback_for = list(detail.get("fallback_for", []))
        if not fallback_for or pid in configs or pid in selected:
            continue
        issue = next(
            (
                item
                for item in config_issues
                if f"Fallback {pid} " in item
            ),
            "Configured fallback is not available for this run.",
        )
        states.append(
            {
                "provider_id": pid,
                "model": detail.get("model"),
                "family": detail.get("family"),
                "required": False,
                "role": roles.get(str(pid)) or detail.get("role"),
                "status": "not_configured",
                "independent_participated": False,
                "fully_completed": False,
                "phase_status": {phase: False for phase in phases},
                "phase_errors": {},
                "configuration_error": issue,
                "missing_configuration": list(detail.get("missing_configuration", [])),
                "attempt_count": 0,
                "is_fallback": True,
                "fallback_for": fallback_for,
            }
        )

    fallback_by_primary = {
        primary: config.provider_id for primary, config in fallbacks.items()
    }
    for detail in availability:
        for primary in detail.get("fallback_for", []):
            fallback_by_primary.setdefault(primary, detail.get("provider_id"))
    states_by_id = {item["provider_id"]: item for item in states}
    for state in states:
        if not state.get("required"):
            continue
        state["required_slot_satisfied"] = bool(state.get("fully_completed"))
        state["required_slot_satisfied_by"] = (
            state["provider_id"] if state.get("fully_completed") else None
        )
        if state.get("fully_completed"):
            continue
        fallback_id = fallback_by_primary.get(state["provider_id"])
        fallback_state = states_by_id.get(fallback_id) if fallback_id else None
        if fallback_state and fallback_state.get("fully_completed"):
            state["required_slot_satisfied"] = True
            state["required_slot_satisfied_by"] = fallback_id
    return states


def _build_consensus_policy(
    *,
    states: list[dict[str, Any]],
    selected_ids: Sequence[str],
    required_ids: Sequence[str],
    phase_status: Mapping[str, Mapping[str, Any]],
    clusters: list[dict[str, Any]],
    disagreements: list[dict[str, Any]],
    open_questions: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    configuration_issues: Sequence[str],
    settings: ConsensusSettings,
) -> dict[str, Any]:
    state_by_id = {item["provider_id"]: item for item in states}
    required = set(required_ids)
    missing_required = [
        provider_id
        for provider_id in sorted(required)
        if provider_id not in state_by_id
        or not state_by_id[provider_id].get(
            "required_slot_satisfied",
            state_by_id[provider_id].get("fully_completed", False),
        )
    ]
    independent_count = sum(
        bool(item.get("independent_participated")) for item in states
    )
    completed_count = sum(bool(item.get("fully_completed")) for item in states)
    target = settings.required_participant_target(len(required))
    completed_roles = {
        str(item.get("role"))
        for item in states
        if item.get("fully_completed") and item.get("role")
    }
    missing_roles = [
        role for role in settings.required_roles if role not in completed_roles
    ]
    checks = {
        "minimum_independent_participation_met": independent_count
        >= settings.min_participating_models,
        "complete_round_participation_met": completed_count >= target,
        "required_provider_slots_met": not missing_required,
        "required_roles_met": not missing_roles,
        "cross_examination_completed": settings.enable_cross_examination
        and phase_status.get("cross_examination", {}).get("status") == "completed",
        "adversarial_review_completed": settings.enable_adversarial_review
        and phase_status.get("adversarial_review", {}).get("status") == "completed",
        "provider_configuration_clean": not configuration_issues,
        "issue_support_thresholds_met": all(
            item.get("support_threshold_met", False) for item in clusters
        ),
        "all_findings_source_grounded": all(
            item.get("evidence_status") == "grounded_text" for item in findings
        ),
        "no_unresolved_disagreements": not disagreements,
        "no_open_questions": not open_questions,
    }
    participation_keys = (
        "minimum_independent_participation_met",
        "complete_round_participation_met",
        "required_provider_slots_met",
        "required_roles_met",
        "cross_examination_completed",
        "adversarial_review_completed",
        "provider_configuration_clean",
    )
    agreement_keys = (
        "issue_support_thresholds_met",
        "all_findings_source_grounded",
        "no_unresolved_disagreements",
        "no_open_questions",
    )
    reasons = []
    if not checks["minimum_independent_participation_met"]:
        reasons.append(
            f"Only {independent_count} independent reviewers participated; at least {settings.min_participating_models} are required."
        )
    if not checks["complete_round_participation_met"]:
        reasons.append(
            f"Only {completed_count} reviewers completed the enabled rounds; the configured target is {target}."
        )
    if missing_required:
        reasons.append(
            "Required provider slot(s) are incomplete: "
            + ", ".join(missing_required)
            + "."
        )
    if missing_roles:
        reasons.append(
            "Required review role(s) are incomplete: "
            + ", ".join(missing_roles)
            + "."
        )
    if not checks["cross_examination_completed"]:
        reasons.append("The required cross-examination phase did not complete.")
    if not checks["adversarial_review_completed"]:
        reasons.append("The required adversarial-review phase did not complete.")
    if configuration_issues:
        reasons.append(
            "Provider configuration issues remain: "
            + "; ".join(configuration_issues)
            + "."
        )
    if not checks["issue_support_thresholds_met"]:
        reasons.append(
            "One or more grounded issue clusters did not meet the configured independent-support threshold."
        )
    if not checks["all_findings_source_grounded"]:
        reasons.append("One or more model findings are not grounded in the source text.")
    if disagreements:
        reasons.append(f"{len(disagreements)} reviewer disagreement(s) remain unresolved.")
    if open_questions:
        reasons.append(f"{len(open_questions)} open review question(s) remain.")
    met = all(checks.values())
    selected = set(selected_ids)
    selected_states = [item for item in states if item["provider_id"] in selected]
    selected_independent = sum(
        bool(item.get("independent_participated")) for item in selected_states
    )
    return {
        "status": "satisfied" if met else "not_satisfied",
        "met": met,
        "participation_protocol_met": all(checks[key] for key in participation_keys),
        "issue_agreement_policy_met": all(checks[key] for key in agreement_keys),
        "requirements": {
            "minimum_independent_participants": settings.min_participating_models,
            "minimum_participation_ratio": settings.min_participation_ratio,
            "required_completed_participants": target,
            "strict_required_provider_ids": sorted(required),
            "required_roles": list(settings.required_roles),
            "cross_examination_required": True,
            "adversarial_review_required": True,
            "independent_issue_support_threshold": settings.consensus_threshold,
        },
        "checks": checks,
        "observed": {
            "selected_provider_count": len(selected),
            "selected_independent_participant_count": selected_independent,
            "independent_participant_count": independent_count,
            "fully_completed_participant_count": completed_count,
            "required_provider_slots_satisfied": not missing_required,
            "missing_required_provider_ids": missing_required,
            "completed_roles": sorted(completed_roles),
            "missing_roles": missing_roles,
            "cross_examination_status": phase_status.get(
                "cross_examination", {}
            ).get("status", "not_run"),
            "adversarial_review_status": phase_status.get(
                "adversarial_review", {}
            ).get("status", "not_run"),
            "grounded_issue_count": len(clusters),
            "disagreement_count": len(disagreements),
            "open_question_count": len(open_questions),
        },
        "reasons": reasons,
    }


def _build_gate(
    deterministic: dict[str, Any],
    notes: list[str],
    findings: list[dict[str, Any]],
    disagreements: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    selected: Sequence[str],
    required_ids: Sequence[str],
    states: list[dict[str, Any]],
    issues: Sequence[str],
    consensus_policy: Mapping[str, Any],
    settings: ConsensusSettings,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []

    def add(code: str, message: str) -> None:
        if not any(
            item["code"] == code and item["message"] == message for item in blockers
        ):
            blockers.append({"code": code, "message": message})

    if not selected:
        add("no_models_selected", "No hosted providers were explicitly selected.")
    for issue in issues:
        add("provider_configuration", issue)
    if not consensus_policy.get("met", False):
        reasons = consensus_policy.get("reasons", [])
        detail = "; ".join(str(item) for item in reasons) or "Required criteria were not satisfied."
        add(
            "consensus_policy_not_met",
            "AI consensus policy was not satisfied: " + detail,
        )
    if not settings.enable_cross_examination:
        add(
            "required_review_phase_disabled",
            "Cross-examination is disabled; the required review protocol did not run.",
        )
    if not settings.enable_adversarial_review:
        add(
            "required_review_phase_disabled",
            "Adversarial review is disabled; the required review protocol did not run.",
        )
    if not deterministic.get("valid", False):
        add(
            "deterministic_validation_failed",
            "Deterministic written-text checks did not pass.",
        )
    if deterministic.get("status") == "CHECK_FAILED":
        add(
            "deterministic_checker_unavailable",
            "The deterministic checker could not complete.",
        )
    independent = sum(item.get("independent_participated", False) for item in states)
    complete = sum(item.get("fully_completed", False) for item in states)
    target = settings.required_participant_target(len(required_ids))
    if independent < settings.min_participating_models:
        add(
            "minimum_model_participation",
            f"Only {independent} structured independent reviews; at least {settings.min_participating_models} required.",
        )
    if complete < target:
        add(
            "complete_round_participation",
            f"Only {complete} models completed enabled rounds; target is {target}.",
        )
    missing = [
        item["provider_id"]
        for item in states
        if item.get("required")
        and not item.get("required_slot_satisfied", item.get("fully_completed"))
    ]
    if settings.strict_required_participation and missing:
        add(
            "required_model_missing",
            "Required model participation is incomplete: "
            + ", ".join(sorted(set(missing)))
            + ".",
        )
    completed_roles = {
        item.get("role")
        for item in states
        if item.get("fully_completed") and item.get("role")
    }
    missing_roles = [
        role for role in settings.required_roles if role not in completed_roles
    ]
    if missing_roles:
        add(
            "review_role_coverage",
            "Required review role(s) did not complete: "
            + ", ".join(missing_roles)
            + ".",
        )
    actionable = [
        item
        for item in findings
        if SEVERITY_RANK.get(str(item.get("severity", "major")), 2)
        > SEVERITY_RANK["info"]
    ]
    if actionable:
        add(
            "unresolved_actionable_ai_findings",
            f"{len(actionable)} source-cited AI finding(s) require human resolution or a separately revalidated draft.",
        )
    if disagreements:
        add(
            "unresolved_model_disagreement",
            f"{len(disagreements)} disagreement(s) remain unresolved.",
        )
    if questions:
        add(
            "unresolved_review_questions",
            f"{len(questions)} open review question(s) remain.",
        )
    if any(item.get("evidence_status") != "grounded_text" for item in findings):
        add(
            "ungrounded_ai_claim",
            "One or more AI findings lack source-grounded evidence.",
        )
    if notes:
        add(
            "unverified_written_construction",
            f"{len(notes)} written instruction/assembly item(s) remain unparsed or unverified.",
        )
    approved = not blockers
    return {
        "approved": approved,
        "status": "APPROVED FOR WRITTEN-TEXT CHECKS ONLY"
        if approved
        else "NOT APPROVED – HUMAN REVIEW REQUIRED",
        "approval_scope": "Written-text checker plus configured, successful, source-grounded review phases only; not an assessment of a physical sample.",
        "blockers": blockers,
        "blocker_count": len(blockers),
        "required_model_participation_satisfied": not missing and complete >= target,
        "consensus_policy_satisfied": bool(consensus_policy.get("met", False)),
        "deterministic_validation_satisfied": bool(deterministic.get("valid")),
        "human_review_required": bool(blockers),
        "physical_construction_verified": False,
        "physical_verification_required_but_missing": False,
        "physical_verification_note": "No physical crochet build, gauge swatch, fit, fabric, durability, or finishing review was performed. Written-text approval must not be represented as physical verification or safety certification.",
        "delivery_authorized": approved,
    }


def _build_score(
    deterministic_score: Any,
    findings: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    independent: int,
    completed: int,
    settings: ConsensusSettings,
    required_count: int,
) -> dict[str, Any]:
    try:
        raw = float(deterministic_score)
        deterministic = max(0.0, min(100.0, raw)) if math.isfinite(raw) else 0.0
    except (TypeError, ValueError):
        deterministic = 0.0
    target = settings.required_participant_target(required_count)
    participation = min(1.0, completed / target) if target else 0.0
    grounding = (
        sum(item.get("evidence_status") == "grounded_text" for item in findings)
        / len(findings)
        if findings
        else 0.0
    )
    agreement = (
        sum(float(item.get("support_ratio", 0)) for item in clusters) / len(clusters)
        if clusters
        else 0.0
    )
    weights = {
        "deterministic_text_checks": 50,
        "complete_model_participation": 20,
        "source_evidence_grounding": 15,
        "independent_model_agreement": 15,
    }
    components = {
        "deterministic_text_checks": round(deterministic * 0.5, 2),
        "complete_model_participation": round(participation * 20, 2),
        "source_evidence_grounding": round(grounding * 15, 2),
        "independent_model_agreement": round(agreement * 15, 2),
    }
    return {
        "weighted_score": round(sum(components.values()), 2),
        "max_score": 100,
        "weights": weights,
        "components": components,
        "observed_ratios": {
            "deterministic_score_percent": round(deterministic, 2),
            "fully_completed_model_participation_ratio": round(participation, 4),
            "evidence_grounding_ratio": round(grounding, 4),
            "mean_independent_issue_agreement_ratio": round(agreement, 4),
        },
        "independent_participant_count": independent,
        "fully_completed_participant_count": completed,
        "required_participant_target": target,
        "interpretation": "Process completeness only—not correctness probability, physical verification, safety certification, or an approval override.",
    }


def _telemetry(calls: list[dict[str, Any]], total_latency: int) -> dict[str, Any]:
    successful = sum(item.get("status") == "succeeded" for item in calls)
    costs = [
        item["estimated_cost_usd"]
        for item in calls
        if isinstance(item.get("estimated_cost_usd"), (int, float))
        and math.isfinite(item["estimated_cost_usd"])
    ]
    inputs = [
        item["input_tokens"]
        for item in calls
        if isinstance(item.get("input_tokens"), int)
    ]
    outputs = [
        item["output_tokens"]
        for item in calls
        if isinstance(item.get("output_tokens"), int)
    ]
    cost = round(sum(costs), 8) if len(costs) == successful and successful else None
    return {
        "provider_call_count": len(calls),
        "successful_provider_calls": successful,
        "failed_provider_calls": len(calls) - successful,
        "total_latency_ms": total_latency,
        "provider_latency_ms": sum(int(item.get("latency_ms") or 0) for item in calls),
        "reported_input_tokens": sum(inputs) if inputs else None,
        "reported_output_tokens": sum(outputs) if outputs else None,
        "calls_with_token_usage": sum(
            item.get("input_tokens") is not None
            or item.get("output_tokens") is not None
            for item in calls
        ),
        "estimated_cost_usd": cost,
        "calls_with_cost_estimate": len(costs),
        "cost_note": "Costs are estimated only when usage and configured rates are available; unknown prices are not assumed.",
    }


def _consensus_status(
    independent: int,
    clusters: list[dict[str, Any]],
    disagreements: list[dict[str, Any]],
    policy: Mapping[str, Any],
) -> str:
    if independent == 0:
        return "NO_INDEPENDENT_MODEL_PARTICIPATION"
    if disagreements:
        return "DISPUTED_OR_UNRESOLVED"
    if not policy.get("met", False):
        return "CONSENSUS_POLICY_NOT_MET"
    if not clusters:
        return "NO_GROUNDED_FINDINGS_REPORTED"
    return (
        "GROUNDED_FINDINGS_AGREED"
        if all(item.get("consensus_reached", False) for item in clusters)
        else "PARTIAL_OR_NO_CONSENSUS"
    )


def _reviewer_alias(index: int) -> str:
    letters = ""
    while True:
        letters = chr(ord("A") + index % 26) + letters
        index = index // 26 - 1
        if index < 0:
            return f"Reviewer {letters}"


def _peer_reviews_for(
    current: str,
    aliases: Mapping[str, str],
    groups: Mapping[str, Mapping[str, ParsedReview]],
) -> list[tuple[str, ParsedReview]]:
    provider_ids = (
        set().union(*(set(items) for items in groups.values())) if groups else set()
    )
    result = []
    for pid in sorted(provider_ids):
        if pid == current or pid not in aliases:
            continue
        for phase, reviews in groups.items():
            review = reviews.get(pid)
            if review:
                alias = (
                    aliases[pid]
                    if phase == "independent"
                    else f"{aliases[pid]} {phase}"
                )
                result.append((alias, review))
    return result


def _count(value: Any) -> str:
    return "" if value is None else str(value).strip().casefold()


def _normalize(value: str) -> str:
    value = value.casefold().replace("–", "-").replace("—", "-").replace("−", "-")
    value = re.sub(r"[*_`]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def _distinct(values: Any) -> list[str]:
    result = []
    for value in values:
        value = str(value).strip()
        if value and value not in result:
            result.append(value)
    return result


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


async def _notify(
    callback: ProgressCallback | None, stage: str, current: int, message: str
) -> None:
    if callback is None:
        return
    try:
        value = callback(
            {
                "stage": stage,
                "current": current,
                "total": 5,
                "message": message,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        if inspect.isawaitable(value):
            await value
    except Exception:
        # Progress reporting is best-effort and must not discard a valid review.
        return
