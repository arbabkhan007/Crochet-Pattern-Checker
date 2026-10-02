"""A stitch color is shown only when one color letter is written."""

from crochet_checker.parser.parser import parse_pattern
from crochet_checker.simulation.stitch_sim import simulate_stitches, stitch_model_obj, stitch_table_csv
from crochet_checker.validation.validator import validate_pattern


def test_one_written_color_is_kept_and_a_split_is_not_guessed():
    text = (
        "Color A: Brown\n"
        "Color B: Gold\n"
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: With Color A, inc x 6 (12)\n"
        "Round 3: With Color A and Color B, sc in each st around (12)\n"
    )
    before = validate_pattern(text)
    simulation = simulate_stitches(parse_pattern(text))
    after = validate_pattern(text)
    assert before.overall_status == after.overall_status
    first = [stitch for stitch in simulation.stitches if stitch.round_number == 1]
    second = [stitch for stitch in simulation.stitches if stitch.round_number == 2]
    third = [stitch for stitch in simulation.stitches if stitch.round_number == 3]
    assert first and all(stitch.color_label == "" for stitch in first)
    assert second and all(stitch.color_label == "A Brown" for stitch in second)
    assert all(stitch.color_hex == "#8B5A2B" for stitch in second)
    assert third and all(stitch.color_label == "" for stitch in third)
    assert any("split was not guessed" in note for note in simulation.notes)
    assert any("No color was invented" in note for note in simulation.notes)
    table = stitch_table_csv(simulation)
    assert "A Brown" in table
    assert "not a measurement" in table


def test_unknown_color_name_does_not_invent_a_dye():
    text = (
        "Color A: Chartreuse\n"
        "Round 1: With Color A, 6 sc into magic ring (6)\n"
    )
    simulation = simulate_stitches(parse_pattern(text))
    assert simulation.stitches
    assert all(stitch.color_label == "A" for stitch in simulation.stitches)
    assert all(stitch.color_hex != "" for stitch in simulation.stitches)
    assert all("chartreuse" not in stitch.color_hex.lower() for stitch in simulation.stitches)
    assert any("dye was not invented" in note for note in simulation.notes)


def test_obj_keeps_a_written_color_label():
    text = (
        "Color A: Brown\n"
        "Round 1: 6 sc into magic ring (6)\n"
        "Round 2: With Color A, inc x 6 (12)\n"
    )
    simulation = simulate_stitches(parse_pattern(text))
    obj = stitch_model_obj(simulation)
    assert obj.count("\nv ") == len(simulation.stitches)
    assert "# color A Brown" in obj
    assert "A dye was not invented" not in obj
    unlabeled = [stitch for stitch in simulation.stitches if stitch.round_number == 1]
    assert unlabeled and all(stitch.color_label == "" for stitch in unlabeled)
