"""An assembly line is a written piece pair, not a guessed stitch join."""

from pathlib import Path

from crochet_checker.parser.parser import parse_pattern
from crochet_checker.simulation.assembly_map import assembly_map_svg, written_assembly
from crochet_checker.validation.validator import validate_pattern

ROOT = Path(__file__).resolve().parents[2]


def _pattern(name: str):
    return parse_pattern((ROOT / "examples" / name).read_text(encoding="utf-8"))


def _pairs(assembly):
    return {tuple(sorted((edge.left, edge.right))) for edge in assembly.edges}


def test_bunny_draws_only_two_named_pieces():
    pattern = _pattern("amigurumi_bunny.txt")
    before = validate_pattern(pattern.source_text)
    assembly = written_assembly(pattern)
    after = validate_pattern(pattern.source_text)
    assert before.overall_status == after.overall_status
    assert _pairs(assembly) == {
        ("BODY", "HEAD"),
        ("EARS", "HEAD"),
        ("ARMS", "BODY"),
    }
    assert all("legs" not in edge.left.lower() and "legs" not in edge.right.lower() for edge in assembly.edges)
    assert any("legs" in line.lower() for line in assembly.unnamed)
    assert "not a stitch join" in assembly_map_svg(assembly)
    assert any("not guessed" in note for note in assembly.notes)


def test_three_named_pieces_are_not_guessed():
    text = "HEAD\nRound 1: 6 sc into magic ring (6)\nBODY\nRound 1: 6 sc into magic ring (6)\nEARS (make 2)\nRound 1: 6 sc into magic ring (6)\nSew head, body, and ears together.\n"
    assembly = written_assembly(parse_pattern(text))
    assert assembly.edges == []
    assert any("not guessed" in note for note in assembly.notes)


def test_no_piece_list_draws_no_join():
    text = "Sew head to body.\nRound 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\n"
    assembly = written_assembly(parse_pattern(text))
    assert assembly.edges == []
    assert any("No piece list" in note for note in assembly.notes)


def test_numberless_sew_does_not_invent_a_count():
    text = "EARS (make 2)\nRound 1: 6 sc into magic ring (6)\nHEAD\nRound 1: 6 sc into magic ring (6)\nSew the ears to the head.\n"
    assembly = written_assembly(parse_pattern(text))
    assert _pairs(assembly) == {("EARS", "HEAD")}
    assert len(assembly.edges) == 1
    assert "2" not in " ".join(assembly.edges[0].sources)


def test_render_3d_writes_the_assembly_map(tmp_path):
    from click.testing import CliRunner

    from crochet_checker.cli import cli

    result = CliRunner().invoke(
        cli,
        ["render-3d", str(ROOT / "examples" / "amigurumi_bunny.txt"), "-o", str(tmp_path)],
    )
    assert result.exit_code == 0, result.output
    assert "Piece joins: 3" in result.output
    svg = (tmp_path / "amigurumi_bunny" / "assembly_map.svg").read_text(encoding="utf-8")
    assert "Not drawn" in svg
    assert "not a stitch join" in svg
