"""Stitch geometry is a model of the written stitches, not a measurement."""

from pathlib import Path

from crochet_checker.parser.parser import parse_pattern
from crochet_checker.simulation.stitch_sim import (
    HONESTY,
    simulate_stitches,
    stitch_map_svg,
    stitch_model_obj,
)

ROOT = Path(__file__).resolve().parents[2]


def _pattern(name: str):
    return parse_pattern((ROOT / "examples" / name).read_text(encoding="utf-8"))


def test_amigurumi_places_every_written_round():
    simulation = simulate_stitches(_pattern("amigurumi.txt"))
    counts = {}
    for stitch in simulation.stitches:
        counts[stitch.round_number] = counts.get(stitch.round_number, 0) + 1
    assert counts[1] == 6
    assert counts[2] == 12
    assert counts[7] == 36
    assert counts[17] == 6
    assert simulation.stitch_count == 432
    assert HONESTY in simulation.notes[0]
    assert "not a photo" in stitch_map_svg(simulation)
    assert stitch_model_obj(simulation).count("\nv ") == 432


def test_increase_join_is_not_guessed_past_the_previous_round():
    simulation = simulate_stitches(_pattern("amigurumi.txt"))
    second = [stitch for stitch in simulation.stitches if stitch.round_number == 2]
    assert all(stitch.parents == [index // 2] for index, stitch in enumerate(second))


def test_chain_round_is_placed_and_the_join_is_not_a_new_stitch():
    simulation = simulate_stitches(_pattern("tube_cowl.txt"))
    first = [stitch for stitch in simulation.stitches if stitch.round_number == 1]
    second = [stitch for stitch in simulation.stitches if stitch.round_number == 2]
    assert len(first) == 40
    assert all(stitch.stitch_type == "chain" for stitch in first)
    assert len(second) == 40
    assert any("join slip stitch" in note for note in simulation.notes)


def test_row_each_across_uses_the_previous_written_count():
    simulation = simulate_stitches(_pattern("scarf.txt"))
    second = [
        stitch
        for stitch in simulation.stitches
        if stitch.round_number == 2 and stitch.stitch_type == "single_crochet"
    ]
    assert len(second) == 19
    assert all(len(stitch.parents) == 1 for stitch in second)


def test_make_count_copies_are_not_called_a_made_sample():
    simulation = simulate_stitches(_pattern("amigurumi_bunny.txt"))
    copies = {stitch.copy_index for stitch in simulation.stitches if stitch.piece == "EARS"}
    assert copies == {0, 1}
    assert any("were not made or measured" in note for note in simulation.notes)


def test_empty_pattern_invents_no_stitch():
    simulation = simulate_stitches(parse_pattern("This note has no rounds.\n"))
    assert simulation.stitches == []
    assert any("No written stitch was placed." in note for note in simulation.notes)
