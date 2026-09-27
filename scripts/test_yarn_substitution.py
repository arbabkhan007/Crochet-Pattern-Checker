#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.enterprise import YarnSubstitutionAnalyzer


analyzer = YarnSubstitutionAnalyzer()

safe = analyzer.compare("cotton", "linen")
risky = analyzer.compare("cotton", "wool")

print("Cotton to linen:")
print(safe.to_dict())

print("\nCotton to wool:")
print(risky.to_dict())

assert safe.risk_score >= 0
assert risky.risk_score >= safe.risk_score
assert risky.sample_required is True

print("\nYarn substitution analysis: PASS")
