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
    assert "table rows: 728" in result.stdout
    assert "dual rows: 111" in result.stdout
    assert "count rows checked: 700" in result.stdout
    assert "assertions: 3247" in result.stdout
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
            "11_No-Sew_Christmas_Gnome.md",
            "One complete plain skin-tone round—Rnd 15—sits between the nose round and the change to hat colour for Rnd 16",
            "The nose sits on the round immediately before the hat-colour change",
            "missing release safeguard 'One complete plain skin-tone round",
        ),
        (
            "12_Bobble_Christmas_Tree.md",
            "The low decrease anchors the bobble",
            "The following decrease sits beside the bobble",
            "missing release safeguard 'The low decrease anchors the bobble'",
        ),
        (
            "12_Bobble_Christmas_Tree.md",
            "| R22 | [BO, sc2tog] x 6 | [BO, dc2tog] x 6 | (12) | 18 to 12; push each BO outward before the adjacent decrease |",
            "| R22 | [BO, sc2tog] x 6 | [BO, dc2tog] x 6 | (13) | 18 to 13; push each BO outward before the adjacent decrease |",
            "got 12, expected 13",
        ),
        (
            "12_Bobble_Christmas_Tree.md",
            "[sc, sc2tog] x 6 (12)",
            "[sc, sc2tog] x 5 (10)",
            "missing release safeguard '[sc, sc2tog] x 6 (12)'",
        ),
        (
            "13_Christmas_Ornament_Bundle.md",
            "sl st = sl st - slip stitch in both US and UK terms",
            "sl st - slip stitch",
            "missing release safeguard 'sl st = sl st - slip stitch in both US and UK terms'",
        ),
        (
            "13_Christmas_Ornament_Bundle.md",
            "3 tr, ch 3, sl st) in each of the 6 ch-5 spaces",
            "4 tr, ch 3, sl st) in each of the 6 ch-5 spaces",
            "missing release safeguard '3 tr, ch 3, sl st) in each of the 6 ch-5 spaces'",
        ),
        (
            "13_Christmas_Ornament_Bundle.md",
            "3 dtr, ch 3, sl st) in each of the 6 ch-5 spaces",
            "3 tr, ch 3, sl st) in each of the 6 ch-5 spaces",
            "missing release safeguard '3 dtr, ch 3, sl st) in each of the 6 ch-5 spaces'",
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
        (
            "14_Bobble_Snowflake_Tree_Skirt.md",
            "Each spoke needs its own centre join and outer-edge fasten-off",
            "Work all surface spokes as one continuous route",
            "missing release safeguard 'Each spoke needs its own centre join and outer-edge fasten-off'",
        ),
        (
            "14_Bobble_Snowflake_Tree_Skirt.md",
            "| R12 | Ch 2, [dc in next 10 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 10 sts, 2 tr in next st] x 12, sl st to first tr | (144) | 10 plain + 1 increase anchor consumes 11 and makes 12 |",
            "| R12 | Ch 2, [dc in next 9 sts, 2 dc in next st] x 12, sl st to first dc | Ch 2, [tr in next 9 sts, 2 tr in next st] x 12, sl st to first tr | (144) | 10 plain + 1 increase anchor consumes 11 and makes 12 |",
            "got 132, expected 144",
        ),
        (
            "16_Crochet_Mini_Stocking_Advent_Garland.md",
            "Row 6 | BLO sc in each st across, ch 1, turn",
            "Row 6 | BLO sc in each st across; do not turn",
            "missing release safeguard 'Row 6 | BLO sc in each st across, ch 1, turn'",
        ),
        (
            "17_Year_of_the_Fire_Goat_2027_Plushie_Set.md",
            "| R13 | [sc, dec] x 4 | (8) | corrected even opening; FO with sewing tail |",
            "| R13 | [sc, dec] x 4 | (9) | corrected even opening; FO with sewing tail |",
            "got 8, expected 9",
        ),
    ],
    ids=[
        "count",
        "terminology",
        "ns11-nose-round-order",
        "ns12-r22-shape-safeguard",
        "ns12-r22-count",
        "ns12-smooth-tip-fallback-count",
        "ns13-slip-stitch-terminology",
        "ns13-us-tall-arm-load",
        "ns13-uk-tall-arm-translation",
        "structural-safeguard",
        "front-leg-safeguard",
        "required-care-section",
        "required-colourway-section",
        "ns14-separate-spokes-safeguard",
        "ns14-r12-plain-count",
        "ns16-heel-turn-safeguard",
        "ns17-even-leg-opening",
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
