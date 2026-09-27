#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.enterprise import (
    CertificationLevel,
    EnterpriseCertifier,
)
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


TEXT = """\
Round 1: 6 sc into magic ring (6)
Round 2: (sc, inc) x 6 (18)
Round 3: (2 sc, inc) x 6 (24)
"""

pattern = parse_pattern(TEXT)
compiler_report = validate_pattern(pattern)

certifier = EnterpriseCertifier(
    tolerance_percent=5.0,
    minimum_confidence=0.90,
    require_gauge=True,
    require_yarn_profile=True,
)

report = certifier.certify(
    pattern,
    compiler_report,
    gauge_verified=True,
    yarn_profile_known=True,
    geometry_verified=True,
    ai_conflicts=False,
    safety_passed=True,
    tolerance_passed=True,
)

assert report.compiler_valid is True
assert report.sample_required is False
assert report.level == CertificationLevel.CERTIFIED
assert report.confidence >= 0.90
assert report.to_json()

print("Enterprise certification: PASS")
print(report.to_json())
