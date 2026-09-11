"""Integration and mutation tests for the commercial pattern release gate."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path("tools/pattern_release_audit.py")


def run_audit(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(AUDIT)],
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
    )


def copy_release_tree(destination: Path) -> Path:
    shutil.copytree(ROOT / "patterns", destination / "patterns")
    (destination / "tools").mkdir()
    shutil.copy2(ROOT / AUDIT, destination / AUDIT)
    return destination


def test_current_commercial_pattern_collection_passes_release_gate():
    result = run_audit(ROOT)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "count rows checked: 517" in result.stdout
    assert "assertions: 2523" in result.stdout
    assert "PASS - all release-gate checks succeeded" in result.stdout


@pytest.mark.parametrize(
    ("filename", "original", "mutation", "expected_finding"),
    [
        (
            "01_Hamish_the_Highland_Cow.md",
            "| R8 | [6 sc, inc] x 6 | (48) | fringe row 1 / ears |",
            "| R8 | [6 sc, inc] x 6 | (47) | fringe row 1 / ears |",
            "got 48, expected 47",
        ),
        (
            "11_No-Sew_Christmas_Gnome.md",
            "| R1 | 6 sc in MR | 6 dc in MR | (6) | - |",
            "| R1 | 6 sc in MR | 6 tr in MR | (6) | - |",
            "US/UK parity",
        ),
        (
            "10_Willow_the_Bunny_Lovey.md",
            "18 marked Rnd-12 stitches",
            "the marked base stitches",
            "missing release safeguard '18 marked Rnd-12 stitches'",
        ),
        (
            "01_Hamish_the_Highland_Cow.md",
            "Start each leg 25 degrees forward from vertical",
            "Angle each front leg forward",
            "missing release safeguard 'Start each leg 25 degrees forward from vertical'",
        ),
        (
            "01_Hamish_the_Highland_Cow.md",
            "\n## Care\n",
            "\n## Cleaning notes\n",
            "missing care section",
        ),
        (
            "05_Little_Duck_Plushie.md",
            "\n## Colorways\n",
            "\n## Palette notes\n",
            "missing section '## Colorways'",
        ),
    ],
    ids=[
        "count",
        "terminology",
        "structural-safeguard",
        "front-leg-safeguard",
        "required-care-section",
        "required-colourway-section",
    ],
)
def test_release_gate_rejects_mutations(
    tmp_path: Path,
    filename: str,
    original: str,
    mutation: str,
    expected_finding: str,
):
    root = copy_release_tree(tmp_path / "release")
    pattern = root / "patterns" / filename
    text = pattern.read_text(encoding="utf-8")
    assert text.count(original) == 1
    pattern.write_text(text.replace(original, mutation, 1), encoding="utf-8")

    result = run_audit(root)

    assert result.returncode != 0
    assert "FAIL" in result.stdout
    assert expected_finding in result.stdout
