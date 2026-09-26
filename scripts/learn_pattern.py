#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.learning import LearningStore
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a pattern and save safe learning feedback."
    )
    parser.add_argument(
        "pattern_file",
        nargs="?",
        help="Text file containing the crochet pattern.",
    )
    parser.add_argument(
        "--confirmed",
        action="store_true",
        help="Mark the result as user-confirmed.",
    )
    parser.add_argument(
        "--corrected-file",
        help="Optional corrected pattern text file.",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show learning statistics.",
    )
    parser.add_argument(
        "--export-regressions",
        action="store_true",
        help="Export confirmed cases as regression JSON files.",
    )

    args = parser.parse_args()
    store = LearningStore()

    if args.stats:
        print(json.dumps(store.statistics(), indent=2))

    if args.export_regressions:
        count = store.export_regression_tests()
        print(f"Exported regression cases: {count}")

    if not args.pattern_file:
        return 0

    pattern_text = Path(args.pattern_file).read_text(
        encoding="utf-8"
    )

    pattern = parse_pattern(pattern_text)
    report = validate_pattern(pattern)

    print("Valid:", report.valid)
    print("Score:", report.score)
    print("Status:", report.overall_status)

    print("\nErrors:")
    for error in report.errors:
        print("-", getattr(error, "message", str(error)))

    print("\nWarnings:")
    for warning in report.warnings:
        print("-", getattr(warning, "message", str(warning)))

    corrected_text = None

    if args.corrected_file:
        corrected_text = Path(args.corrected_file).read_text(
            encoding="utf-8"
        )

    case = store.record(
        pattern_text=pattern_text,
        report=report,
        corrected_text=corrected_text,
        confirmed=args.confirmed,
    )

    print("\nSaved learning case:", case.case_id)

    if args.confirmed:
        print("Confirmed regression case exported.")
    else:
        print(
            "Recorded as unconfirmed. "
            "Use --confirmed only after human review."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
