"""Geometry is a written count, not a millimetre measurement."""

import math
from pathlib import Path

from crochet_checker.parser.parser import parse_pattern
from crochet_checker.simulation.geometry_map import geometry_map_svg, geometry_table_csv, written_geometry
from crochet_checker.simulation.written_views import write_written_views
from crochet_checker.validation.validator import validate_pattern

ROOT = Path(__file__).resolve().parents[2]


def test_round_radius_is_count_over_two_pi_and_not_a_millimetre():
    text = "Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\n"
    before = validate_pattern(text)
    geometry = written_geometry(parse_pattern(text))
    after = validate_pattern(text)
    assert before.overall_status == after.overall_status
    assert len(geometry.layers) == 2
    assert geometry.layers[0].stitch_count == 6
    assert geometry.layers[0].radius == 6 / (2 * math.pi)
    assert geometry.layers[0].z == 0
    assert geometry.layers[1].stitch_count == 12
    assert geometry.layers[1].z == 1
    assert geometry.layers[0].width == 0
    svg = geometry_map_svg(geometry)
    table = geometry_table_csv(geometry)
    assert "Not a millimetre measurement." in svg
    assert "Not a millimetre measurement" in table
    assert "mm" not in table.splitlines()[1]


def test_row_width_is_the_written_count():
    text = (ROOT / "examples" / "scarf.txt").read_text(encoding="utf-8")
    geometry = written_geometry(parse_pattern(text))
    assert geometry.layers
    assert all(not layer.is_round for layer in geometry.layers)
    assert geometry.layers[0].width == 19
    assert geometry.layers[0].radius == 0
    assert "made" not in " ".join(geometry.notes).lower()


def test_views_write_every_file_without_changing_status(tmp_path):
    text = (ROOT / "examples" / "amigurumi.txt").read_text(encoding="utf-8")
    pattern = parse_pattern(text)
    before = validate_pattern(text)
    views = write_written_views(pattern, tmp_path, "amigurumi")
    after = validate_pattern(text)
    assert before.overall_status == after.overall_status == "PASS"
    for name in (
        "stitch_map.svg",
        "stitch_sim.obj",
        "stitch_map.csv",
        "assembly_map.svg",
        "geometry_map.svg",
        "geometry_map.csv",
        "shape_mesh.obj",
    ):
        assert (tmp_path / name).is_file(), name
    assert "does not track each loop" in (tmp_path / "shape_mesh.obj").read_text(encoding="utf-8")
    assert views["stitch_sim"].stitch_count == 432


def test_every_picture_command_writes_the_same_views(tmp_path):
    from click.testing import CliRunner

    from crochet_checker.cli import cli

    pattern = ROOT / "examples" / "scarf.txt"
    runner = CliRunner()
    for command in ("render", "render-3d", "simulate"):
        result = runner.invoke(cli, [command, str(pattern), "-o", str(tmp_path / command)])
        assert result.exit_code == 0, result.output
        folder = tmp_path / command / "scarf"
        for name in ("stitch_map.svg", "stitch_sim.obj", "geometry_map.svg", "shape_mesh.obj"):
            assert (folder / name).is_file(), (command, name)
        assert "Not a millimetre measurement." in (folder / "geometry_map.svg").read_text(encoding="utf-8")
    measured = runner.invoke(cli, ["measure", str(pattern)])
    assert measured.exit_code == 0, measured.output
    assert "Not a measured swatch" in measured.output
