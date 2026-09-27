#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.enterprise import MonteCarloSimulator
from crochet_checker.parser.parser import parse_pattern


pattern = parse_pattern(
    "Round 1: 6 sc into magic ring (6)\n"
    "Round 2: (sc, inc) x 6 (18)\n"
    "Round 3: (2 sc, inc) x 6 (24)\n"
)

result = MonteCarloSimulator(
    simulations=1000,
    seed=42,
).simulate(
    pattern,
    gauge_stitches_per_10cm=18,
    gauge_rows_per_10cm=20,
    tolerance_percent=5,
    tension_variation_percent=3,
)

assert result.simulations == 1000
assert result.minimum_width_cm <= result.expected_width_cm
assert result.expected_width_cm <= result.maximum_width_cm
assert 0 <= result.pass_probability <= 1
assert result.to_json()

print("Monte Carlo simulation: PASS")
print(result.to_json())
