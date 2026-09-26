#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.ai_providers.quality import AIQualityChecker
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


TEXT = """\
Round 1: 6 sc into magic ring (6)
Round 2: (sc, inc) x 6 (18)
Round 3: (2 sc, inc) x 6 (24)
"""


pattern = parse_pattern(TEXT)
compiler_report = validate_pattern(pattern)
quality_report = AIQualityChecker(mode="offline").check(
    pattern,
    compiler_report,
)

assert quality_report.compiler_valid is True
assert quality_report.pattern_hash
assert quality_report.claims
assert quality_report.to_dict()
assert quality_report.to_json()

print("AI quality layer: PASS")
print("Compiler valid:", quality_report.compiler_valid)
print("Confidence:", quality_report.confidence)
print(quality_report.to_json())
