#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from crochet_checker.ai_providers.quality import AIQualityChecker
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern

text = """\
Round 1: 6 sc into magic ring (6)
Round 2: (sc, inc) x 6 (18)
Round 3: (2 sc, inc) x 6 (24)
"""

pattern = parse_pattern(text)
compiler_report = validate_pattern(pattern)

report = AIQualityChecker(mode="offline").check(
    pattern,
    compiler_report,
)

assert report.compiler_valid is True
assert report.confidence >= 0.0
assert report.to_dict()["pattern_hash"]
assert "compiler" in [claim.provider for claim in report.claims]

print("AI quality layer: PASS")
print(report.to_json())
