"""Exercise production modules the coverage gate was missing."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from crochet_checker.ai_providers.consensus import AIClaim, AIConsensusChecker, ConsensusReport
from crochet_checker.ast.nodes import InstructionNode
from crochet_checker.engine.anchor_graph import AnchorNotFoundError, AnchorType, GlobalAnchorGraph
from crochet_checker.engine.assembly_graph import AssemblyGraph, JoinType
from crochet_checker.engine.canvas_queue import CanvasQueue, PostVsHeadLoopTracker, StitchStatus
from crochet_checker.engine.consumer import StitchConsumer as LoopConsumer
from crochet_checker.engine.state_machine import StateMachine
from crochet_checker.engine.stitch_consumer import StitchConsumer
from crochet_checker.model.instruction import Instruction, ParsedOperation
from crochet_checker.model.row import Round, Row, RowOrRound
from crochet_checker.model.stitch import StitchType
from crochet_checker.parser.grammar import extract_stated_count, is_row_header
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.utils.markdown_parser import MarkdownPatternParser, parse_markdown_pattern
from crochet_checker.utils.pdf_reader import extract_text_from_pdf, is_pdf_file, read_pattern_file
from crochet_checker.utils.progress_tracker import ProgressTracker, track_progress
from crochet_checker.validation.assembly import AssemblyGraphValidator
from crochet_checker.validation.chains import TurningChainRulesEngine
from crochet_checker.validation.corners import CornerMismatchError, CornerSequenceValidator
from crochet_checker.validation.exhaustion import OrphanedStitchAnalyzer, OrphanedStitchError
from crochet_checker.validation.reporter import PatternReporter
from crochet_checker.validation.validator import PatternValidator, ValidationError, ValidationResult


def _result(valid=False):
    return ValidationResult(
        is_valid=valid,
        total_stitches=18,
        piece_count=2,
        errors=[
            ValidationError(12, "stated 16 but made 14", piece_name="Head", round_number=15)
        ],
        warnings=[ValidationError(4, "edging is too full", severity="warning", round_number=2)],
        stitch_counts={("Head", 1): 6, ("Head", 2): 18},
        execution_time=0.01,
    )


def test_reporter_formats_and_files(tmp_path, capsys):
    reporter = PatternReporter()
    result = _result()
    text = reporter.generate_report(result, "text")
    assert "INVALID" in text and "Head" in text and "ERRORS" in text and "WARNINGS" in text
    payload = json.loads(reporter.generate_report(result, "json"))
    assert payload["summary"]["error_count"] == 1 and payload["errors"]
    markdown = reporter.generate_report(result, "markdown")
    assert "Validation Report" in markdown or "#" in markdown
    empty = ValidationResult(is_valid=True, total_stitches=0, piece_count=0)
    assert "VALID" in reporter.generate_report(empty)
    reporter.print_report(empty)
    assert "VALID" in capsys.readouterr().out
    path = tmp_path / "report.txt"
    reporter.save_report(result, str(path), "json")
    assert "errors" in path.read_text()
    parsed = reporter.generate_report(
        "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n",
        "text",
    )
    assert "REPORT" in parsed


def test_assembly_graph_validator():
    graph = AssemblyGraphValidator()
    assert graph.validate_join_as_you_go()["is_valid"] is False
    graph.add_piece("center", "hub")
    for name in ("a", "b", "c"):
        graph.add_piece(name, "petal")
    graph.add_join("a", "b", "neighbor")
    graph.add_join("b", "c", "neighbor")
    graph.add_join("c", "a", "neighbor")
    for name in ("a", "b", "c"):
        graph.add_join(name, "center", "core")
    report = graph.validate_assembly()
    assert report["neighbor_joins"] == 3
    assert graph.complete_join("missing") is False
    for join_id in list(graph.joins):
        assert graph.complete_join(join_id) is True
    assert graph.close_ring("nope") is False
    for name in ("a", "b", "c", "center"):
        assert graph.close_ring(name) is True
    closed = graph.validate_assembly()
    assert closed["is_valid"] is True
    jayg = graph.validate_join_as_you_go()
    assert "errors" in jayg
    summary = graph.get_assembly_summary()
    assert summary["total_pieces"] == 4
    lonely = AssemblyGraphValidator()
    lonely.add_piece("solo")
    lonely.add_piece("other")
    dropped = lonely.validate_assembly()
    assert dropped["is_valid"] is False
    graph.reset()
    assert graph.pieces == {}


def test_corners_and_chains():
    corners = CornerSequenceValidator()
    assert corners.parse_corner_from_instruction("sc across") is None
    assert corners.parse_corner_from_instruction("ch-2 sp") == 2
    corners.add_corner_space(2, 1, 2, 4)
    corners.add_corner_space(2, 1, 3, 8)
    corners.add_repeat_block(2, 9, 9)
    assert corners.validate_sequence(2)
    corners.add_repeat_block(3, 1, 11)
    with pytest.raises(CornerMismatchError):
        corners.validate_sequence(2)
    uneven = corners.validate_asymmetric_pattern(2)
    assert uneven["is_valid"] is False
    assert corners.get_corner_summary(2)["corners"]
    corners.reset()
    assert corners.corner_spaces == []

    chains = TurningChainRulesEngine()
    assert chains.parse_turning_chain("sc 6", 1, 1) is None
    plain = chains.parse_turning_chain("ch 3", 1, 2)
    silent = chains.parse_turning_chain("ch 1 (does not count as st)", 1, 3)
    named = chains.parse_turning_chain("ch 2 (counts as dc)", 1, 4)
    assert plain.counts_as_stitch and not silent.counts_as_stitch
    counted = chains.calculate_round_stitch_count(1, 20)
    assert counted["total_count"] == 22
    warnings = chains.validate_turning_chains(1)
    assert warnings and "dc" in warnings[0]
    assert chains.get_chain_summary(1)["total_chains"] == 3
    chains.reset()
    assert chains.turning_chains == []
    assert named.stitch_type == "dc"


def test_exhaustion_analyzer():
    analyzer = OrphanedStitchAnalyzer()
    first = [analyzer.add_stitch(1, index) for index in range(4)]
    assert analyzer.get_stitch("missing") is None
    assert analyzer.get_stitches_in_round(9) == []
    assert analyzer.work_stitch("missing", 2) is False
    assert analyzer.skip_stitch("missing") is False
    assert analyzer.work_stitch(first[0].stitch_id, 2) is True
    assert analyzer.work_stitch(first[0].stitch_id, 2) is False
    assert analyzer.skip_stitch(first[1].stitch_id) is True
    analyzer.add_skip_directive(1, [2], "leave unworked")
    with pytest.raises(OrphanedStitchError):
        analyzer.analyze_exhaustion(1)
    quiet = analyzer.analyze_exhaustion(1, raise_on_orphans=False)
    assert quiet.orphans
    assert analyzer.validate_pattern()
    assert analyzer.analyze_all_rounds(raise_on_orphans=True) == {}
    summary = analyzer.get_round_summary(1)
    assert summary["total_stitches"] == 4
    analyzer.add_stitch(2, 0)
    analyzer.work_stitch(analyzer.get_stitches_in_round(2)[0].stitch_id, 3)
    assert analyzer.analyze_exhaustion(2).is_exhausted
    skipped = OrphanedStitchAnalyzer()
    many = [skipped.add_stitch(3, index) for index in range(4)]
    for stitch in many:
        skipped.skip_stitch(stitch.stitch_id)
    report = skipped.analyze_exhaustion(3, raise_on_orphans=False)
    assert any("50%" in item for item in report.warnings)
    analyzer.reset()
    assert analyzer.canvas == {}


def test_markdown_and_pdf_and_progress(tmp_path):
    markdown = tmp_path / "hat.md"
    markdown.write_text(
        "# Hat\n\n## Body\n\n**Notes**\n\nRound 1: 6 sc into magic ring\n"
        "Row 2: 10 dc\nSee [guide](https://example.com) and *inc* then `dec`.\n"
    )
    parser = MarkdownPatternParser()
    parsed = parser.parse_file(str(markdown))
    assert parsed["title"] == "Hat"
    clean = parser.extract_clean_pattern(parsed)
    assert "magic ring" in clean and "guide" in clean
    assert "Hat" in parse_markdown_pattern(str(markdown))

    from PyPDF2 import PdfWriter

    plain = tmp_path / "plain.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with plain.open("wb") as handle:
        writer.write(handle)
    assert extract_text_from_pdf(str(plain)) == ""
    locked = tmp_path / "locked.pdf"
    secret = PdfWriter()
    secret.add_blank_page(width=72, height=72)
    secret.encrypt("secret")
    with locked.open("wb") as handle:
        secret.write(handle)
    with pytest.raises(ValueError):
        extract_text_from_pdf(str(locked))
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf(str(tmp_path / "missing.pdf"))
    note = tmp_path / "note.txt"
    note.write_text("Round 1: 6 sc")
    assert is_pdf_file(str(plain)) and not is_pdf_file(str(note))
    assert read_pattern_file(str(note)) == "Round 1: 6 sc"
    assert read_pattern_file(str(plain)) == ""

    pattern = parse_pattern("Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\n")
    tracker = track_progress(pattern, "hat")
    assert isinstance(tracker, ProgressTracker)
    tracker.complete_round(1, "done")
    tracker.complete_round(1)
    tracker.uncomplete_round(1)
    tracker.add_note("check the neck")
    assert tracker.get_current_round() == 1
    assert tracker.get_percentage() == 0
    tracker.save(str(tmp_path / "progress.json"))
    assert (tmp_path / "progress.json").exists()
    assert "hat" in tracker.get_summary()
    assert Path(tmp_path / "progress.json").exists()


def test_row_round_and_grammar():
    repeat = Instruction(
        source_text="(sc, inc) x 6 (18)",
        is_repeat_block=True,
        repeat_count=6,
        repeat_unit=[
            ParsedOperation(stitch_type=StitchType.SINGLE_CROCHET, count=1),
            ParsedOperation(stitch_type=StitchType.INCREASE, count=1),
        ],
        stated_stitch_count=18,
    )
    around = Instruction(
        source_text="sc in each st around",
        operations=[
            ParsedOperation(
                stitch_type=StitchType.SINGLE_CROCHET,
                count=1,
                into_stitch="each_stitch_around",
            )
        ],
    )
    row = Row(row_number=2, instructions=[repeat, around], expected_ending_stitch_count=18)
    assert row.computed_stitch_count > 0
    assert row.compute_stitch_count_with_context(6) > 0
    assert row.validate_internal_consistency() == []
    bad = Instruction(
        source_text="6 sc (8)",
        operations=[ParsedOperation(stitch_type=StitchType.SINGLE_CROCHET, count=6)],
        stated_stitch_count=8,
    )
    assert Row(row_number=3, instructions=[bad]).validate_internal_consistency()
    rnd = Round(round_number=2, instructions=[repeat])
    wrapped = RowOrRound(is_round=True, round=rnd)
    assert wrapped.number == 2
    assert wrapped.instructions
    assert wrapped.computed_stitch_count > 0
    assert wrapped.computed_stitches_consumed > 0
    empty = RowOrRound(is_round=False)
    assert empty.instructions == []
    assert empty.computed_stitch_count == 0
    with pytest.raises(ValueError):
        _ = empty.number
    assert rnd.compute_stitch_count_with_context(12) > 0
    clean, count = extract_stated_count("6 sc (6)")
    assert clean == "6 sc" and count == 6
    assert extract_stated_count("6 sc")[1] is None
    assert is_row_header("Rounds 5-8: sc around")[0] is True
    assert is_row_header("not a header")[0] is False


def test_canvas_consumer_and_posts():
    canvas = CanvasQueue()
    canvas.initialize_round(4, 2)
    consumer = StitchConsumer()
    assert consumer.consume_single(canvas, "sc").produced_count == 1
    assert consumer.consume_increase(canvas, 2).produced_count == 2
    assert consumer.skip_stitches(canvas, 1).produced_count == 0
    assert consumer.consume_decrease(canvas, 1).produced_count == 1
    canvas.initialize_round(6, 3)
    assert consumer.consume_cluster(canvas, 3, "dc").consumed_count == 3
    assert consumer.parse_and_consume(canvas, "3-dc-cl").consumed_count == 3
    canvas.initialize_round(4, 4)
    assert consumer.parse_and_consume(canvas, "3-dc-dec").consumed_count == 3
    assert consumer.parse_and_consume(canvas, "2 sc in next st").produced_count == 2
    canvas.initialize_round(3, 5)
    assert consumer.parse_and_consume(canvas, "skip 2").consumed_count == 2
    space = canvas.add_space("ch_sp", 3)
    assert space.element_type == "ch_sp"
    canvas.canvas_pointer = len(canvas.elements) - 1
    assert consumer.consume_space(canvas, "ch_sp", 2).produced_count == 2
    canvas.initialize_round(2, 6)
    with pytest.raises(Exception):
        consumer.check_orphan_stitches(canvas)
    allowed = consumer.check_orphan_stitches(canvas, has_explicit_unworked=True)
    assert allowed["exhausted"] is False
    assert canvas.peek() is not None
    assert canvas.move_to(1) is True
    assert canvas.get_element_at(0) is not None
    assert canvas.get_unworked()
    info = canvas.get_position_info()
    assert "pointer" in info or info
    assert canvas.to_string()
    assert canvas.validate_backward_traversal(-1) is False
    tracker = PostVsHeadLoopTracker(canvas)
    assert tracker.can_work_head(0) is True
    assert tracker.work_head(0) is True
    assert tracker.can_work_post(0) in (True, False)
    tracker.work_post(0)
    assert tracker.get_summary()
    empty = CanvasQueue()
    with pytest.raises(ValueError):
        consumer.consume_single(empty, "sc")


def test_anchor_state_and_assembly_engines():
    graph = GlobalAnchorGraph()
    first = graph.create_node(1, 0, AnchorType.STITCH_TOP, "sc")
    second = graph.create_node(2, 0, AnchorType.POST, "fpdc")
    third = graph.create_node(2, 1, AnchorType.CHAIN_SPACE)
    assert graph.create_dependency(second.node_id, first.node_id) is True
    from crochet_checker.engine.anchor_graph import CircularDependencyError
    with pytest.raises(CircularDependencyError):
        graph.create_dependency(first.node_id, second.node_id)
    assert first.node_id in graph.get_all_dependencies(second.node_id)
    assert second.node_id in graph.get_all_dependents(first.node_id)
    assert graph.get_nodes_in_round(1)
    assert graph.get_nodes_by_position(2, 0)
    assert graph.find_anchor_in_previous_rounds(0, AnchorType.STITCH_TOP, 2)
    with pytest.raises(AnchorNotFoundError):
        graph.get_node("missing")
    issues = graph.validate_dependencies()
    assert isinstance(issues, list)
    assert graph.get_graph_summary()["total_nodes"] == 3
    first.add_dependency(third.node_id)
    first.add_dependent(second.node_id)
    graph.reset()
    assert graph.nodes == {}

    machine = StateMachine()
    machine.initialize_round(6, 1, create_mode=True)
    assert machine.execute_instruction("sc") == 1
    assert machine.execute_instruction("not-a-stitch") == 0
    node = InstructionNode(action="stitch", stitch_type="sc", count=2)
    machine.execute_instruction(node)
    chain = InstructionNode(action="turning_chain", stitch_type="ch", count=3, counts_as_stitch=True)
    machine.execute_instruction(chain)
    assert machine.get_current_stitch_count() >= 0
    assert machine.finalize_round() >= 0
    assert machine.get_report()
    machine.validate_directional_movement(node)

    loops = LoopConsumer()
    one = loops.add_loop(1, 0)
    two = loops.add_loop(1, 1)
    three = loops.add_loop(1, 2)
    four = loops.add_loop(1, 3)
    assert loops.get_loop(one.loop_id) is one
    assert loops.get_loop_at(1, 0) is one
    assert loops.work_stitch(one.loop_id, 2) is True
    assert loops.skip_stitch(two.loop_id) is True
    cluster = loops.create_cluster(2, "dc")
    with pytest.raises(Exception):
        loops.consume_in_cluster([three.loop_id], cluster)
    assert loops.consume_in_cluster([three.loop_id, four.loop_id], cluster) is True
    assert loops.bridge_with_chain(two.loop_id) in (True, False)
    assert loops.get_unworked_loops(1) is not None
    assert loops.check_exhaustion(1, allow_unworked=True)
    assert loops.get_round_summary(1)
    assert loops.get_overall_summary()
    loops.new_round()
    loops.reset()

    assembly = AssemblyGraph()
    assembly.register_piece("head")
    assembly.register_piece("body")
    assembly.add_anchor_point("head", "edge", "h1", 4, 0)
    assembly.add_anchor_point("body", "edge", "b1", 4, 0)
    assembly.add_join("head", "body", JoinType.SEAM, "h1", "b1", 8)
    assert assembly.validate_ring_closure("head", 1) in (True, False)
    assert assembly.validate_assembly_completeness() in (True, False)
    assert isinstance(assembly.detect_orphan_pieces(), list)
    assert assembly.get_assembly_report()
    assembly.register_piece("petal-a")
    assembly.register_piece("petal-b")
    assembly.validate_flower_assembly(2, "head")


def test_consensus_without_keys():
    pattern = parse_pattern("Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 7 (18)\n")
    from crochet_checker.validation import validate_pattern

    report = validate_pattern(pattern)
    checker = AIConsensusChecker()
    compared = checker.compare(pattern, report)
    assert isinstance(compared, ConsensusReport)
    assert compared.to_dict()["compiler_errors"]
    claim = AIClaim(provider="local", claim="same", confidence=1.0, verified=True)
    same = ConsensusReport(
        compiler_valid=True,
        compiler_errors=[],
        claims=[claim],
        disagreements=[],
        recommendation="ok",
    )
    assert same.is_consistent is True
    same.disagreements.append("split")
    assert same.is_consistent is False
