#!/usr/bin/env python3

import sys
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.enterprise import (
    CertificationReportWriter,
    EnterpriseCertifier,
)
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern


pattern = parse_pattern(
    "Round 1: 6 sc into magic ring (6)\n"
    "Round 2: (sc, inc) x 6 (18)"
)

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
    output = Path(directory) / "certificate.html"
    CertificationReportWriter().write(
        certificate,
        str(output),
        title="Enterprise Crochet Certification",
    )

    content = output.read_text(encoding="utf-8")

    assert "<!doctype html>" in content
    assert certificate.pattern_hash in content
    assert certificate.level.value in content
    assert "Compiler valid" in content

print("Commercial certification report: PASS")
