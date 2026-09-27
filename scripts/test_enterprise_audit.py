#!/usr/bin/env python3

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.enterprise import (
    AuditTrail,
    EnterpriseCertifier,
)
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


text = (
    "Round 1: 6 sc into magic ring (6)\n"
    "Round 2: (sc, inc) x 6 (18)"
)

pattern = parse_pattern(text)
compiler_report = validate_pattern(pattern)

certificate = EnterpriseCertifier().certify(
    pattern,
    compiler_report,
    gauge_verified=True,
    yarn_profile_known=True,
    geometry_verified=True,
    ai_conflicts=False,
    safety_passed=True,
    tolerance_passed=True,
)

with tempfile.TemporaryDirectory() as directory:
    trail = AuditTrail(
        str(Path(directory) / "audit.jsonl")
    )

    first = trail.append(
        pattern_hash=certificate.pattern_hash,
        certification=certificate,
        operator="test-user",
    )

    second = trail.append(
        pattern_hash=certificate.pattern_hash,
        certification=certificate,
        operator="test-user",
        action="REVIEW",
    )

    valid, errors = trail.verify()

    assert first["previous_hash"] == "GENESIS"
    assert second["previous_hash"] == first["record_hash"]
    assert valid is True
    assert errors == []
    assert len(trail.records()) == 2

print("Enterprise audit trail: PASS")
