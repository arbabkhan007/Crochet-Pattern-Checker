"""Regression test for the NS 14 Bobble Snowflake Tree Skirt pattern.

Runs the stitch-level simulator over the published pattern. Stdlib only, so it
does not depend on the crochet_checker package importing cleanly.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PATTERN_DIR = Path(__file__).resolve().parents[1] / "patterns" / "ns14-bobble-snowflake-tree-skirt"
VERIFY = PATTERN_DIR / "verify.py"


def run(target: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VERIFY), target],
        cwd=PATTERN_DIR,
        capture_output=True,
        text=True,
    )


@pytest.mark.skipif(not VERIFY.exists(), reason="pattern verifier not present")
def test_corrected_pattern_passes_cleanly():
    result = run("corrected.md")
    assert result.returncode == 0, result.stdout
    assert "PASS" in result.stdout
    assert "ERROR(S)" not in result.stdout
    assert "WARNING(S)" not in result.stdout


@pytest.mark.skipif(not VERIFY.exists(), reason="pattern verifier not present")
def test_corrected_pattern_columns_are_radial():
    """The 12 increase columns must not drift - counts alone cannot catch this."""
    out = run("corrected.md").stdout
    assert "cumulative column rotation: 0.0 degrees" in out
    assert "straddle two parent repeats: 0" in out


@pytest.mark.skipif(not VERIFY.exists(), reason="pattern verifier not present")
def test_every_round_hits_the_12n_ladder():
    out = run("corrected.md").stdout
    assert "US/UK stream mismatches: 0" in out
    for n in range(1, 33):
        assert f"R{n} " in out or f"R{n}  " in out


@pytest.mark.skipif(not (PATTERN_DIR / "original.md").exists(), reason="baseline absent")
def test_original_pattern_is_still_detected_as_broken():
    """Guards the detector itself: the pre-fix pattern must still fail."""
    result = run("original.md")
    assert result.returncode == 1
    assert "Round-start anchor contradiction" in result.stdout


CROSSCHECK = PATTERN_DIR / "crosscheck.py"


def run_cc(target: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CROSSCHECK), target],
        cwd=PATTERN_DIR,
        capture_output=True,
        text=True,
    )


@pytest.mark.skipif(not CROSSCHECK.exists(), reason="cross-checker not present")
def test_independent_crosscheck_agrees():
    """A second implementation, sharing no code, must reach the same verdict."""
    result = run_cc("corrected.md")
    assert result.returncode == 0, result.stdout
    assert "CROSS-CHECK PASSED" in result.stdout
    assert "rounds with a slipped col: 0" in result.stdout


@pytest.mark.skipif(not CROSSCHECK.exists(), reason="cross-checker not present")
def test_independent_crosscheck_catches_the_original():
    result = run_cc("original.md")
    assert result.returncode == 1
    assert "increases off-column     : 360 of 360" in result.stdout
