#!/usr/bin/env python3
"""Deterministically score one Solver response from a private rubric and approved adjudication.

This tool performs arithmetic only. It does not decide whether a claim is correct; a human must
review the adjudication before setting human_approved=true.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CATEGORIES = ("math", "coherence", "finishing", "absurdity")
JUDGMENTS = {"full", "partial", "refuted", "unverifiable"}


class EvaluationError(ValueError):
    """Raised when an input is inconsistent with the scoring contract."""


def _need(condition: bool, message: str) -> None:
    if not condition:
        raise EvaluationError(message)


def _is_int(value: Any) -> bool:
    return type(value) is int


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_rubric(rubric: Any) -> dict[str, dict[str, Any]]:
    _need(isinstance(rubric, dict), "rubric must be a JSON object")
    _need(_nonempty_string(rubric.get("fixture")), "rubric.fixture must be a non-empty string")
    _need(_nonempty_string(rubric.get("version")), "rubric.version must be a non-empty string")

    weights = rubric.get("category_weights")
    _need(isinstance(weights, dict), "rubric.category_weights must be an object")
    _need(set(weights) == set(CATEGORIES), f"category_weights must contain exactly {', '.join(CATEGORIES)}")
    for category, value in weights.items():
        _need(_is_int(value) and value >= 0, f"category weight for {category} must be a non-negative integer")
    _need(sum(weights.values()) == 100, "category weights must sum to 100")

    penalty = rubric.get("false_positive_penalty")
    _need(isinstance(penalty, dict), "rubric.false_positive_penalty must be an object")
    per_claim = penalty.get("per_refuted_claim")
    cap = penalty.get("cap")
    _need(_is_int(per_claim) and per_claim >= 0, "per_refuted_claim must be a non-negative integer")
    _need(_is_int(cap) and 0 <= cap <= 100, "false-positive cap must be an integer from 0 to 100")

    raw_items = rubric.get("items")
    _need(isinstance(raw_items, list) and bool(raw_items), "rubric.items must be a non-empty array")
    items: dict[str, dict[str, Any]] = {}
    category_points = {category: 0 for category in CATEGORIES}
    for index, item in enumerate(raw_items):
        prefix = f"rubric.items[{index}]"
        _need(isinstance(item, dict), f"{prefix} must be an object")
        item_id = item.get("id")
        _need(_nonempty_string(item_id), f"{prefix}.id must be a non-empty string")
        _need(item_id not in items, f"duplicate rubric item id: {item_id}")
        category = item.get("category")
        _need(category in CATEGORIES, f"{prefix}.category must be one of {', '.join(CATEGORIES)}")
        points = item.get("points")
        _need(_is_int(points) and 1 <= points <= 100, f"{prefix}.points must be an integer from 1 to 100")
        _need(_nonempty_string(item.get("location")), f"{prefix}.location must be a non-empty string")
        _need(_nonempty_string(item.get("expected_claim")), f"{prefix}.expected_claim must be a non-empty string")
        _need(_nonempty_string(item.get("required_evidence")), f"{prefix}.required_evidence must be a non-empty string")

        partials = item.get("partial_credit")
        _need(isinstance(partials, list), f"{prefix}.partial_credit must be an array")
        partial_by_key: dict[str, int] = {}
        for part_index, part in enumerate(partials):
            part_prefix = f"{prefix}.partial_credit[{part_index}]"
            _need(isinstance(part, dict), f"{part_prefix} must be an object")
            key = part.get("key")
            part_points = part.get("points")
            _need(_nonempty_string(key), f"{part_prefix}.key must be a non-empty string")
            _need(key not in partial_by_key, f"duplicate partial-credit key {key!r} in item {item_id}")
            _need(_is_int(part_points) and 0 <= part_points <= points, f"{part_prefix}.points must be between 0 and the item's points")
            _need(_nonempty_string(part.get("criteria")), f"{part_prefix}.criteria must be a non-empty string")
            partial_by_key[key] = part_points

        clean_item = dict(item)
        clean_item["_partial_by_key"] = partial_by_key
        items[item_id] = clean_item
        category_points[category] += points

    _need(sum(item["points"] for item in items.values()) == 100, "rubric item points must sum to 100")
    _need(category_points == weights, "item point totals must equal the configured category weights")
    return items


def score_run(rubric: Any, solver: Any, adjudication: Any) -> dict[str, Any]:
    items = validate_rubric(rubric)
    _need(isinstance(solver, dict), "solver report must be a JSON object")
    fixture = rubric["fixture"]
    _need(solver.get("fixture") == fixture, "solver fixture does not match rubric fixture")
    defects = solver.get("defects")
    _need(isinstance(defects, list), "solver.defects must be an array")
    solver_ids: list[str] = []
    for index, defect in enumerate(defects):
        _need(isinstance(defect, dict), f"solver.defects[{index}] must be an object")
        claim_id = defect.get("id")
        _need(_nonempty_string(claim_id), f"solver.defects[{index}].id must be a non-empty string")
        _need(claim_id not in solver_ids, f"duplicate Solver claim id: {claim_id}")
        solver_ids.append(claim_id)

    _need(isinstance(adjudication, dict), "adjudication must be a JSON object")
    _need(adjudication.get("fixture") == fixture, "adjudication fixture does not match rubric fixture")
    _need(adjudication.get("human_approved") is True, "adjudication must be explicitly human-approved before scoring")
    _need(_nonempty_string(adjudication.get("reviewer")) and adjudication.get("reviewer") != "unreviewed", "approved adjudication must name its human reviewer")
    claims = adjudication.get("claims")
    _need(isinstance(claims, list), "adjudication.claims must be an array")

    adjudicated_ids: list[str] = []
    mapped_items: set[str] = set()
    earned_by_category = {category: 0 for category in CATEGORIES}
    awarded_by_item: dict[str, int] = {item_id: 0 for item_id in items}
    refuted_claim_ids: list[str] = []
    unverifiable_claim_ids: list[str] = []

    for index, claim in enumerate(claims):
        prefix = f"adjudication.claims[{index}]"
        _need(isinstance(claim, dict), f"{prefix} must be an object")
        claim_id = claim.get("claim_id")
        _need(_nonempty_string(claim_id), f"{prefix}.claim_id must be a non-empty string")
        _need(claim_id not in adjudicated_ids, f"duplicate adjudication for Solver claim {claim_id}")
        adjudicated_ids.append(claim_id)
        judgment = claim.get("judgment")
        _need(judgment in JUDGMENTS, f"{prefix}.judgment must be one of {', '.join(sorted(JUDGMENTS))}")
        item_id = claim.get("rubric_item_id")
        partial_key = claim.get("partial_credit_key")
        _need(item_id is None or _nonempty_string(item_id), f"{prefix}.rubric_item_id must be a string or null")
        _need(partial_key is None or _nonempty_string(partial_key), f"{prefix}.partial_credit_key must be a string or null")
        if item_id is not None:
            _need(item_id in items, f"{prefix} references unknown rubric item {item_id!r}")
            _need(item_id not in mapped_items, f"rubric item {item_id!r} is mapped more than once; resolve duplicate claims first")
            mapped_items.add(item_id)

        if judgment == "full":
            _need(item_id is not None, f"{prefix}: full judgment requires a rubric_item_id")
            _need(partial_key is None, f"{prefix}: full judgment cannot use a partial_credit_key")
            item = items[item_id]
            earned_by_category[item["category"]] += item["points"]
            awarded_by_item[item_id] = item["points"]
        elif judgment == "partial":
            _need(item_id is not None, f"{prefix}: partial judgment requires a rubric_item_id")
            _need(partial_key is not None, f"{prefix}: partial judgment requires a partial_credit_key")
            item = items[item_id]
            _need(partial_key in item["_partial_by_key"], f"{prefix}: unknown partial-credit key {partial_key!r} for item {item_id!r}")
            earned_by_category[item["category"]] += item["_partial_by_key"][partial_key]
            awarded_by_item[item_id] = item["_partial_by_key"][partial_key]
        else:
            _need(partial_key is None, f"{prefix}: {judgment} judgment cannot use a partial_credit_key")
            if judgment == "refuted":
                refuted_claim_ids.append(claim_id)
            else:
                unverifiable_claim_ids.append(claim_id)

    _need(set(adjudicated_ids) == set(solver_ids), "adjudication claim IDs must exactly match Solver defect IDs")

    raw_points = sum(earned_by_category.values())
    penalty_config = rubric["false_positive_penalty"]
    penalty = min(penalty_config["per_refuted_claim"] * len(refuted_claim_ids), penalty_config["cap"])
    final_score = max(0, min(100, raw_points - penalty))
    undercredited = [item_id for item_id, item in items.items() if awarded_by_item[item_id] < item["points"]]
    missed = [item_id for item_id in items if item_id not in mapped_items]
    uncredited_by_category = {category: 0 for category in CATEGORIES}
    missed_by_category = {category: 0 for category in CATEGORIES}
    for item_id in undercredited:
        uncredited_by_category[items[item_id]["category"]] += 1
    for item_id in missed:
        missed_by_category[items[item_id]["category"]] += 1

    return {
        "fixture": fixture,
        "rubric_version": rubric["version"],
        "raw_points": raw_points,
        "false_positive_penalty": penalty,
        "score": final_score,
        "format_failure": False,
        "refuted_claim_count": len(refuted_claim_ids),
        "refuted_claim_ids": refuted_claim_ids,
        "unverifiable_claim_count": len(unverifiable_claim_ids),
        "unverifiable_claim_ids": unverifiable_claim_ids,
        "per_category": {
            category: {
                "earned": earned_by_category[category],
                "possible": rubric["category_weights"][category],
                "uncredited_item_count": uncredited_by_category[category],
                "missed_item_count": missed_by_category[category],
            }
            for category in CATEGORIES
        },
        "failure_taxonomy": {**uncredited_by_category, "format": 0},
        "missed_item_ids": missed,
        "undercredited_item_ids": undercredited,
    }


def score_format_failure(rubric: Any) -> dict[str, Any]:
    """Return the predeclared zero score for a refusal, truncation, or invalid Solver response."""
    items = validate_rubric(rubric)
    uncredited_by_category = {category: 0 for category in CATEGORIES}
    for item in items.values():
        uncredited_by_category[item["category"]] += 1
    return {
        "fixture": rubric["fixture"],
        "rubric_version": rubric["version"],
        "raw_points": 0,
        "false_positive_penalty": 0,
        "score": 0,
        "format_failure": True,
        "refuted_claim_count": 0,
        "refuted_claim_ids": [],
        "unverifiable_claim_count": 0,
        "unverifiable_claim_ids": [],
        "per_category": {
            category: {
                "earned": 0,
                "possible": rubric["category_weights"][category],
                "uncredited_item_count": uncredited_by_category[category],
                "missed_item_count": uncredited_by_category[category],
            }
            for category in CATEGORIES
        },
        "failure_taxonomy": {**uncredited_by_category, "format": 1},
        "missed_item_ids": list(items),
        "undercredited_item_ids": list(items),
    }


def _read_json(path: str) -> Any:
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"cannot read JSON file {path!r}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rubric", required=True, help="private rubric JSON path")
    parser.add_argument("--solver", help="Solver JSON path")
    parser.add_argument("--adjudication", help="human-approved adjudication JSON path")
    parser.add_argument("--format-failure", action="store_true", help="record a refusal, truncation, or invalid Solver response as zero without adjudication")
    args = parser.parse_args(argv)
    if args.format_failure and (args.solver or args.adjudication):
        parser.error("--format-failure cannot be combined with --solver or --adjudication")
    if not args.format_failure and (not args.solver or not args.adjudication):
        parser.error("provide both --solver and --adjudication, or use --format-failure")
    try:
        rubric = _read_json(args.rubric)
        result = score_format_failure(rubric) if args.format_failure else score_run(rubric, _read_json(args.solver), _read_json(args.adjudication))
    except EvaluationError as exc:
        print(f"score.py: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
