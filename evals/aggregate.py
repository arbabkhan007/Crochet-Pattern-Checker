#!/usr/bin/env python3
"""Aggregate complete per-fixture replicate scores without best-of-N selection."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

TAXONOMY_CATEGORIES = ("math", "coherence", "finishing", "absurdity", "format")


class EvaluationError(ValueError):
    """Raised when an aggregate input is incomplete or inconsistent."""


def _need(condition: bool, message: str) -> None:
    if not condition:
        raise EvaluationError(message)


def _is_number(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def summarize(
    payload: Any,
    *,
    min_macro: float = 92.0,
    min_fixture: float = 85.0,
    required_clean_batches: int = 3,
) -> dict[str, Any]:
    _need(isinstance(payload, dict), "input must be a JSON object")
    _need(_is_number(min_macro) and 0 <= min_macro <= 100, "min_macro must be a finite number from 0 to 100")
    _need(_is_number(min_fixture) and 0 <= min_fixture <= 100, "min_fixture must be a finite number from 0 to 100")
    _need(type(required_clean_batches) is int and required_clean_batches >= 1, "required_clean_batches must be a positive integer")
    split = payload.get("split")
    _need(isinstance(split, str) and split in {"development", "holdout"}, "split must be 'development' or 'holdout'")
    fixtures = payload.get("fixtures")
    _need(isinstance(fixtures, list) and bool(fixtures), "fixtures must be a non-empty array")
    _need(all(isinstance(item, str) and item.strip() for item in fixtures), "fixture IDs must be non-empty strings")
    _need(len(set(fixtures)) == len(fixtures), "fixture IDs must be unique")
    replicates_per_fixture = payload.get("replicates_per_fixture")
    _need(type(replicates_per_fixture) is int and replicates_per_fixture >= 1, "replicates_per_fixture must be a positive integer")
    batches = payload.get("batches")
    _need(isinstance(batches, list) and bool(batches), "batches must be a non-empty array")
    batch_ids: set[str] = set()
    all_runs: list[dict[str, Any]] = []
    batch_refuted: list[dict[str, Any]] = []
    reference_replicate_ids: set[str] | None = None

    for batch_index, batch in enumerate(batches):
        prefix = f"batches[{batch_index}]"
        _need(isinstance(batch, dict), f"{prefix} must be an object")
        batch_id = batch.get("id")
        _need(isinstance(batch_id, str) and batch_id.strip(), f"{prefix}.id must be a non-empty string")
        _need(batch_id not in batch_ids, f"duplicate batch id {batch_id!r}")
        batch_ids.add(batch_id)
        runs = batch.get("runs")
        _need(isinstance(runs, list), f"{prefix}.runs must be an array")
        _need(len(runs) == len(fixtures) * replicates_per_fixture, f"{prefix} must contain exactly fixtures × replicates_per_fixture runs")
        observed: set[tuple[str, str]] = set()
        replicates_by_fixture: dict[str, set[str]] = {fixture: set() for fixture in fixtures}
        refuted_total = 0
        for run_index, run in enumerate(runs):
            run_prefix = f"{prefix}.runs[{run_index}]"
            _need(isinstance(run, dict), f"{run_prefix} must be an object")
            fixture = run.get("fixture")
            replicate = run.get("replicate")
            _need(fixture in fixtures, f"{run_prefix} references unexpected fixture {fixture!r}")
            _need(isinstance(replicate, str) and replicate.strip(), f"{run_prefix}.replicate must be a non-empty string")
            key = (fixture, replicate)
            _need(key not in observed, f"duplicate fixture/replicate pair {key!r} in batch {batch_id!r}")
            observed.add(key)
            replicates_by_fixture[fixture].add(replicate)
            score = run.get("score")
            _need(_is_number(score) and 0 <= score <= 100, f"{run_prefix}.score must be a finite number from 0 to 100")
            refuted_count = run.get("refuted_count")
            _need(type(refuted_count) is int and refuted_count >= 0, f"{run_prefix}.refuted_count must be a non-negative integer")
            taxonomy = run.get("failure_taxonomy")
            _need(isinstance(taxonomy, dict) and set(taxonomy) == set(TAXONOMY_CATEGORIES), f"{run_prefix}.failure_taxonomy must contain exactly {', '.join(TAXONOMY_CATEGORIES)}")
            for category, count in taxonomy.items():
                _need(type(count) is int and count >= 0, f"{run_prefix}.failure_taxonomy.{category} must be a non-negative integer")
            _need(taxonomy["format"] <= 1, f"{run_prefix}.failure_taxonomy.format must be 0 or 1")
            if taxonomy["format"] == 1:
                _need(score == 0 and refuted_count == 0, f"{run_prefix}: a format failure must score 0 and have no adjudicated refuted claims")
            refuted_total += refuted_count
            all_runs.append({"batch": batch_id, "fixture": fixture, "replicate": replicate, "score": float(score), "refuted_count": refuted_count, "failure_taxonomy": dict(taxonomy)})
        expected_replicate_ids: set[str] | None = None
        for fixture in fixtures:
            ids = replicates_by_fixture[fixture]
            _need(len(ids) == replicates_per_fixture, f"{prefix} has the wrong replicate count for fixture {fixture!r}")
            if expected_replicate_ids is None:
                expected_replicate_ids = ids
            else:
                _need(ids == expected_replicate_ids, f"{prefix} must use the same predeclared replicate IDs for every fixture")
        assert expected_replicate_ids is not None
        if reference_replicate_ids is None:
            reference_replicate_ids = expected_replicate_ids
        else:
            _need(expected_replicate_ids == reference_replicate_ids, f"{prefix} uses a different replicate matrix from earlier batches")
        batch_refuted.append({"id": batch_id, "refuted_count": refuted_total})

    per_fixture: dict[str, float] = {}
    for fixture in fixtures:
        values = [run["score"] for run in all_runs if run["fixture"] == fixture]
        per_fixture[fixture] = sum(values) / len(values)
    macro = sum(per_fixture.values()) / len(per_fixture)
    taxonomy_totals = {
        category: sum(run["failure_taxonomy"][category] for run in all_runs)
        for category in TAXONOMY_CATEGORIES
    }
    result: dict[str, Any] = {
        "split": split,
        "batch_count": len(batches),
        "replicates_per_fixture_per_batch": replicates_per_fixture,
        "scored_responses": len(all_runs),
        "fixture_means": per_fixture,
        "macro_average": macro,
        "failure_taxonomy": taxonomy_totals,
        "batch_refuted_counts": batch_refuted,
        "thresholds": {"macro_minimum": min_macro, "fixture_minimum": min_fixture, "clean_final_batches": required_clean_batches},
    }

    if split == "development":
        result["status"] = "DEVELOPMENT_SCORED"
        return result
    if len(batches) < required_clean_batches:
        result["status"] = "INCOMPLETE"
        result["reasons"] = [f"need at least {required_clean_batches} complete holdout batches to evaluate the consecutive-clean-batch gate"]
        return result

    final_batches = batch_refuted[-required_clean_batches:]
    no_refuted = all(batch["refuted_count"] == 0 for batch in final_batches)
    macro_ok = macro >= min_macro
    fixture_ok = all(value >= min_fixture for value in per_fixture.values())
    result["final_gate"] = {"macro_ok": macro_ok, "every_fixture_ok": fixture_ok, "consecutive_clean_batches_ok": no_refuted}
    result["status"] = "PASS" if macro_ok and fixture_ok and no_refuted else "FAIL"
    return result


def assess_development_change(
    candidate: dict[str, Any],
    baseline: dict[str, Any],
    *,
    minimum_macro_gain: float = 1.0,
    maximum_fixture_drop: float = 5.0,
) -> dict[str, Any]:
    _need(isinstance(candidate, dict) and isinstance(baseline, dict), "candidate and baseline must be summary objects")
    _need(candidate.get("split") == "development" and baseline.get("split") == "development", "tuning comparisons must use development summaries")
    _need(_is_number(minimum_macro_gain) and minimum_macro_gain >= 0, "minimum_macro_gain must be a non-negative finite number")
    _need(_is_number(maximum_fixture_drop) and maximum_fixture_drop >= 0, "maximum_fixture_drop must be a non-negative finite number")
    candidate_means = candidate.get("fixture_means")
    baseline_means = baseline.get("fixture_means")
    _need(isinstance(candidate_means, dict) and isinstance(baseline_means, dict), "summaries must contain fixture_means objects")
    _need(set(candidate_means) == set(baseline_means) and bool(candidate_means), "candidate and baseline must have the same fixture IDs")
    for fixture in candidate_means:
        _need(_is_number(candidate_means[fixture]) and _is_number(baseline_means[fixture]), f"fixture mean for {fixture!r} must be finite numeric")
        _need(0 <= candidate_means[fixture] <= 100 and 0 <= baseline_means[fixture] <= 100, f"fixture mean for {fixture!r} must be in [0, 100]")
    candidate_macro = candidate.get("macro_average")
    baseline_macro = baseline.get("macro_average")
    _need(_is_number(candidate_macro) and _is_number(baseline_macro), "summaries must contain finite numeric macro_average values")
    deltas = {fixture: candidate_means[fixture] - baseline_means[fixture] for fixture in candidate_means}
    macro_delta = candidate_macro - baseline_macro
    accepted = macro_delta >= minimum_macro_gain and all(delta >= -maximum_fixture_drop for delta in deltas.values())
    return {
        "accepted": accepted,
        "macro_delta": macro_delta,
        "fixture_deltas": deltas,
        "minimum_macro_gain": minimum_macro_gain,
        "maximum_fixture_drop": maximum_fixture_drop,
    }


def _read_json(path: str) -> Any:
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"cannot read JSON file {path!r}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="private aggregate input JSON path")
    parser.add_argument("--baseline", help="prior development aggregate summary JSON path")
    parser.add_argument("--min-macro", type=float, default=92.0)
    parser.add_argument("--min-fixture", type=float, default=85.0)
    parser.add_argument("--clean-batches", type=int, default=3)
    parser.add_argument("--min-gain", type=float, default=1.0)
    parser.add_argument("--max-drop", type=float, default=5.0)
    args = parser.parse_args(argv)
    try:
        result = summarize(_read_json(args.input), min_macro=args.min_macro, min_fixture=args.min_fixture, required_clean_batches=args.clean_batches)
        if args.baseline:
            result["tuning_comparison"] = assess_development_change(result, _read_json(args.baseline), minimum_macro_gain=args.min_gain, maximum_fixture_drop=args.max_drop)
    except EvaluationError as exc:
        print(f"aggregate.py: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] == "FAIL":
        return 1
    if result["status"] == "INCOMPLETE":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
