#!/usr/bin/env python3
"""
Test Audit Features - 13 features from the 4-pattern audit
(The Chrono-Mandala, The Astral Lattice, The Asymmetric Pentagon,
 The Hyper-Geometric Polyhedron)

Layers tested:
  1. Parser  - MarkdownFrontmatterSanitizer, GlossaryPrePassExtractor,
               MultiPieceASTBuilder, RecursiveLoopUnroller
  2. Engine  - CanvasQueue (Ring & Linear Buffer), PostVsHeadLoopTracker,
               GlobalAnchorGraph, StitchConsumer (Loop State Allocator)
  3. Validation - OrphanedStitchAnalyzer, CornerSequenceValidator,
                  TurningChainRulesEngine, AssemblyGraphValidator
  4. Reporter  - UnsupportedSyntaxFallback, DiffPatchGenerator
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

TESTS = []


def test(name):
    def decorator(fn):
        TESTS.append((name, fn))
        return fn
    return decorator


# ============================================================================
# 1. PARSING & AST PIPELINE
# ============================================================================

@test("MarkdownFrontmatterSanitizer")
def _():
    from crochet_checker.parser.sanitizer import MarkdownFrontmatterSanitizer
    s = MarkdownFrontmatterSanitizer()
    text = """# My Pattern\n## Notes\nRemember tension!\nRound 1: Ch 4, sl st to join\n- Yarn: wool\nRound 2: Ch 3, 11 dc in ring"""
    sanitized, removed = s.sanitize(text)
    assert 'Round 1' in sanitized, "Round 1 lost"
    assert 'Round 2' in sanitized, "Round 2 lost"
    assert 'Remember' not in sanitized, "Note leaked into instructions"
    assert len(removed) > 0, "No removed sections recorded"


@test("GlossaryPrePassExtractor")
def _():
    from crochet_checker.parser.glossary import GlossaryPrePassExtractor
    g = GlossaryPrePassExtractor()
    text = """## Glossary\nsc: single crochet\n3-tr-cl: 3 Treble Cluster\nBPtr: Back Post Treble"""
    glossary = g.extract(text)
    assert 'sc' in glossary, "sc not extracted"
    assert '3-tr-cl' in glossary, "complex stitch not extracted"
    assert 'BPtr' in glossary, "post stitch not extracted"
    assert glossary['3-tr-cl'].is_complex, "complex flag not set"
    assert g.is_defined('sc')
    assert not g.is_defined('xyzzy')
    assert glossary['3-tr-cl'].stitch_count > 0, "stitch count not computed"


@test("MultiPieceASTBuilder")
def _():
    from crochet_checker.parser.ast_builder import MultiPieceASTBuilder, ConstructionMode
    b = MultiPieceASTBuilder()
    text = """## Petal 1\nRound 1: 6 sc in magic ring (6)\nRound 2: 2 sc in each st (12)\n\n## Petal 2\nRound 1: 6 sc in magic ring (6)\nRound 2: 2 sc in each st (12)"""
    ast = b.build(text)
    assert len(ast.pieces) == 2, f"Expected 2 pieces, got {len(ast.pieces)}"
    for p in ast.pieces:
        assert len(p.rounds) == 2, f"Piece {p.name} has {len(p.rounds)} rounds"
        assert p.rounds[0].stitch_count == 6, "Round 1 count wrong"
        assert p.rounds[1].stitch_count == 12, "Round 2 count wrong"
        assert p.metadata.get('scope_id') is not None, "scope isolation missing"
    errors = b.validate_piece_boundaries(ast)
    assert errors == [], f"Boundary errors: {errors}"
    # Rows vs rounds detection
    text_rows = "## Body\nRow 1: ch 5\nRow 2: sc across"
    ast2 = b.build(text_rows)
    assert ast2.pieces[0].construction_mode == ConstructionMode.ROWS


@test("RecursiveLoopUnroller")
def _():
    from crochet_checker.parser.unroller import RecursiveLoopUnroller
    u = RecursiveLoopUnroller()
    ops = u.unroll("*[sc, 2 dc in next st] repeat 3 times, sc* twice")
    assert len(ops) > 0, "No operations unrolled"
    # [sc, 2 dc] = 3 stitches, x3 = 9, +sc = 10, x2 = 20 stitches
    total = u.count_total_stitches(ops)
    assert total == 20, f"Expected 20 stitches, got {total}"
    flat = u.to_flat_string(ops[:3])
    assert 'sc' in flat
    warnings = u.validate_unrolling("*[sc, 2 dc] x3, sc* twice", ops)
    assert isinstance(warnings, list)
    # Deeply nested
    nested = u.unroll("*[*(sc, dc) twice* repeat 3 times] repeat 2 times*")
    assert len(nested) > 0


# ============================================================================
# 2. SPATIAL ENGINE & STATE MACHINE
# ============================================================================

@test("CanvasQueue Ring & Linear Buffer")
def _():
    from crochet_checker.engine import CanvasQueue, BackwardTraversalError
    c = CanvasQueue()
    c.initialize_round(6, round_number=1)
    assert len(c.elements) == 6
    # Forward traversal
    worked = c.advance(3)
    for e in worked:
        e.consume()
    assert c.canvas_pointer == 3
    # Backward traversal rejected
    assert not c.validate_backward_traversal(0), "Backward traversal should be rejected"
    # Exhaustion not complete
    ex = c.check_exhaustion()
    assert not ex['exhausted']
    assert ex['unworked_count'] == 3
    # Finish round
    for e in c.advance(3):
        e.consume()
    assert c.check_exhaustion()['exhausted']


@test("PostVsHeadLoopTracker")
def _():
    from crochet_checker.engine import CanvasQueue, PostVsHeadLoopTracker
    c = CanvasQueue()
    c.initialize_round(6, round_number=1)
    t = PostVsHeadLoopTracker(c)
    # BPtr works around post, head stays available
    assert t.work_post(0), "Post work failed"
    assert t.can_work_head(0), "Head loop prematurely consumed by post stitch"
    assert not t.can_work_post(0), "Post still available after being worked"
    # Head consumption
    assert t.work_head(0), "Head work failed"
    assert not t.can_work_head(0), "Head loop still available after consumption"
    summary = t.get_summary()
    assert summary['post_worked'] == 1
    assert summary['head_worked'] == 1
    assert summary['unconsumed_heads'] == 5


@test("GlobalAnchorGraph Multi-Depth Lookups")
def _():
    from crochet_checker.engine import GlobalAnchorGraph, AnchorType
    g = GlobalAnchorGraph()
    # Round 1: 6 anchors
    for i in range(6):
        g.create_node(1, i, AnchorType.STITCH_TOP, "sc")
    # Round 2 depends on Round 1
    for i in range(6):
        node = g.create_node(2, i, AnchorType.STITCH_TOP, "sc")
        r1 = g.get_nodes_by_position(1, i)[0]
        g.create_dependency(node.node_id, r1.node_id)
    # Split-tr2tog anchored into Round 1 from Round 3
    split = g.create_node(3, 0, AnchorType.POST, "Split-tr2tog")
    g.create_dependency(split.node_id, g.get_nodes_by_position(1, 0)[0].node_id)
    deps = g.get_all_dependencies(split.node_id)
    assert g.get_nodes_by_position(1, 0)[0].node_id in deps
    errors = g.validate_dependencies()
    assert errors == [], f"Anchor graph errors: {errors}"
    summary = g.get_graph_summary()
    assert summary['total_nodes'] == 13
    assert summary['rounds'] == 3


@test("StitchConsumer Loop State Allocator")
def _():
    from crochet_checker.engine import LoopStateAllocator
    from crochet_checker.engine.consumer import LoopLifecycleState
    c = LoopStateAllocator()
    loops = [c.add_loop(1, i).loop_id for i in range(6)]
    # Cluster consumes 3
    cluster_id = c.create_cluster(3, "tr")
    assert c.consume_in_cluster(loops[:3], cluster_id)
    # Work remaining 3 individually
    for lid in loops[3:]:
        assert c.work_stitch(lid, 1)
    result = c.check_exhaustion(1)
    assert result['exhausted'], f"Not exhausted: {result}"
    # State transitions
    c2 = LoopStateAllocator()
    l2 = c2.add_loop(1, 0)
    assert l2.state == LoopLifecycleState.UNTOUCHED
    assert c2.skip_stitch(l2.loop_id)
    assert l2.state == LoopLifecycleState.SKIPPED
    l3 = c2.add_loop(1, 1)
    assert c2.bridge_with_chain(l3.loop_id)
    assert l3.state == LoopLifecycleState.BRIDGED_BY_CHAIN


# ============================================================================
# 3. VALIDATION & RULES ENGINE
# ============================================================================

@test("OrphanedStitchAnalyzer Exhaustion Check")
def _():
    from crochet_checker.validation import OrphanedStitchAnalyzer, OrphanedStitchError
    a = OrphanedStitchAnalyzer()
    stitches = [a.add_stitch(1, i).stitch_id for i in range(6)]
    for sid in stitches:
        assert a.work_stitch(sid, 1)
    report = a.analyze_exhaustion(1, raise_on_orphans=False)
    assert report.is_exhausted, "Round should be exhausted"
    # Orphan case
    a2 = OrphanedStitchAnalyzer()
    stitches2 = [a2.add_stitch(2, i).stitch_id for i in range(6)]
    for sid in stitches2[:4]:
        a2.work_stitch(sid, 2)
    raised = False
    try:
        a2.analyze_exhaustion(2, raise_on_orphans=True)
    except OrphanedStitchError as e:
        raised = True
        assert hasattr(e, 'orphans') and len(e.orphans) == 2
    assert raised, "OrphanedStitchError not raised"
    # Skip directive prevents orphan error
    a3 = OrphanedStitchAnalyzer()
    stitches3 = [a3.add_stitch(3, i).stitch_id for i in range(6)]
    a3.add_skip_directive(3, [4, 5], "skip 2 sts")
    for sid in stitches3[:4]:
        a3.work_stitch(sid, 3)
    report3 = a3.analyze_exhaustion(3, raise_on_orphans=False)
    assert report3.is_exhausted, "Skip directive should prevent orphans"


@test("CornerSequenceValidator")
def _():
    from crochet_checker.validation import CornerSequenceValidator, CornerMismatchError
    v = CornerSequenceValidator()
    for i in range(4):
        v.add_corner_space(1, i, 2, i * 5)
    for i in range(4):
        v.add_repeat_block(2, i, line_number=10 + i)
    errors = v.validate_sequence(1)
    assert errors == [], f"Unexpected errors: {errors}"
    # Mismatch: expecting ch-3, found ch-2
    v2 = CornerSequenceValidator()
    v2.add_corner_space(1, 0, 2, 0)
    v2.add_repeat_block(3, 0, line_number=10)
    raised = False
    try:
        v2.validate_sequence(1)
    except CornerMismatchError as e:
        raised = True
        assert 'ch-3' in str(e) and 'ch-2' in str(e)
    assert raised, "CornerMismatchError not raised"
    # Asymmetric validation
    v3 = CornerSequenceValidator()
    v3.add_corner_space(1, 0, 2, 0)
    v3.add_corner_space(1, 1, 3, 5)
    v3.add_corner_space(1, 1, 2, 10)  # inconsistent
    report = v3.validate_asymmetric_pattern(1)
    assert not report['is_valid']
    assert len(report['inconsistencies']) == 1


@test("TurningChainRulesEngine")
def _():
    from crochet_checker.validation import TurningChainRulesEngine
    e = TurningChainRulesEngine()
    # Explicit counts-as
    e.parse_turning_chain("ch 3 (counts as dc)", 1, 5)
    result = e.calculate_round_stitch_count(1, 10)
    assert result['total_count'] == 11, f"Expected 11, got {result['total_count']}"
    assert result['turning_chain_addition'] == 1
    # Explicit does-not-count
    e2 = TurningChainRulesEngine()
    e2.parse_turning_chain("ch 1 (does not count as st)", 2, 10)
    result2 = e2.calculate_round_stitch_count(2, 12)
    assert result2['total_count'] == 12, "ch-1 should add 0"
    # Default: ch-3 counts as dc
    e3 = TurningChainRulesEngine()
    e3.parse_turning_chain("ch 3", 3, 15)
    result3 = e3.calculate_round_stitch_count(3, 15)
    assert result3['total_count'] == 16, "ch-3 should count by default"
    # Mismatch warning: ch-2 claims to count as dc
    e4 = TurningChainRulesEngine()
    e4.parse_turning_chain("ch 2 (counts as dc)", 4, 20)
    warnings = e4.validate_turning_chains(4)
    assert len(warnings) == 1, f"Expected 1 warning, got {len(warnings)}"


@test("AssemblyGraphValidator")
def _():
    from crochet_checker.validation import AssemblyGraphValidator
    v = AssemblyGraphValidator()
    for i in range(1, 7):
        v.add_piece(f"petal_{i}", "petal")
    # 6 neighbor joins forming a ring
    for i in range(1, 7):
        join = v.add_join(f"petal_{i}", f"petal_{i % 6 + 1}", "neighbor")
        v.complete_join(join.join_id)
    # 6 core joins
    for i in range(1, 7):
        join = v.add_join(f"petal_{i}", "center", "core")
        v.complete_join(join.join_id)
    for i in range(1, 7):
        v.close_ring(f"petal_{i}")
    result = v.validate_assembly()
    assert result['is_valid'], f"Assembly invalid: {result['errors']}"
    assert result['neighbor_joins'] == 6
    assert result['core_joins'] == 6
    # JAYG validation
    jayg = v.validate_join_as_you_go()
    assert jayg['is_valid'], f"JAYG invalid: {jayg['errors']}"
    # Incomplete assembly (missing ring closure join, no hub)
    v2 = AssemblyGraphValidator()
    for i in range(1, 5):
        v2.add_piece(f"petal_{i}", "petal")
    for i in range(1, 4):
        v2.add_join(f"petal_{i}", f"petal_{i+1}", "neighbor")
    result2 = v2.validate_assembly()
    assert not result2['is_valid']
    assert any('neighbor' in err.lower() for err in result2['errors'])
    # Missing core joins when a hub exists
    v3 = AssemblyGraphValidator()
    for i in range(1, 5):
        v3.add_piece(f"petal_{i}", "petal")
    for i in range(1, 5):
        v3.add_join(f"petal_{i}", f"petal_{i % 4 + 1}", "neighbor")
    v3.add_join("petal_1", "center", "core")  # only 1 of 4 core joins
    result3 = v3.validate_assembly()
    assert not result3['is_valid']
    assert any('core' in err.lower() for err in result3['errors'])


# ============================================================================
# 4. REPORTING & DIAGNOSTICS
# ============================================================================

@test("UnsupportedSyntaxFallback")
def _():
    from crochet_checker.reporter import UnsupportedSyntaxFallback, TrustLevel
    f = UnsupportedSyntaxFallback()
    # Normal parse -> TRUSTED
    r1 = f.parse_with_fallback("Round 3: 2 dc in each st around (24 sts)", 3)
    assert r1.trust_level == TrustLevel.TRUSTED
    assert r1.count == 24
    # Unsupported spatial phrasing -> not TRUSTED, warning recorded
    r2 = f.parse_with_fallback("work backward through the space to the first stitch", 5)
    assert r2.trust_level != TrustLevel.TRUSTED, "Unsupported syntax must not be TRUSTED"
    assert f.has_warnings(), "Warning not recorded"
    untrusted = f.get_untrusted_counts()
    assert len(untrusted) >= 1
    # Vague instruction
    f2 = UnsupportedSyntaxFallback()
    r3 = f2.parse_with_fallback("sc in several stitches around", 7)
    assert r3.trust_level == TrustLevel.UNTRUSTED
    assert len(f2.get_warnings()) >= 1


@test("DiffPatchGenerator")
def _():
    from crochet_checker.reporter import DiffPatchGenerator
    g = DiffPatchGenerator()
    # Count mismatch: 10 dc but expected 12
    report = g.analyze_round(1, ["ch 3, 10 dc in ring"], 12, [5])
    assert report.total_issues >= 1
    count_patches = [p for p in report.patches if 'stitch_count' in p.issue_type]
    assert len(count_patches) == 1, f"Expected 1 count patch, got {len(count_patches)}"
    assert count_patches[0].confidence > 0.5
    diff = count_patches[0].to_diff()
    assert 'round_1_original' in diff and 'round_1_corrected' in diff
    # Turning chain mismatch: ch-2 with dc
    report2 = g.analyze_round(2, ["ch 2, dc in each st around"], 20, [10])
    chain_patches = [p for p in report2.patches if 'turning_chain' in p.issue_type]
    assert len(chain_patches) == 1
    assert 'ch 3' in chain_patches[0].corrected_text  # preserves user's notation style
    assert 'ch 2' not in chain_patches[0].corrected_text
    # Full pattern patch report
    full = g.generate_full_patch_report(
        "Round 1: ch 4, sl st to join\nRound 2: ch 3, 10 dc in ring (12 sts)\n"
        "Round 3: ch 2, 2 dc in each st around (24 sts)"
    )
    assert full['total_patches'] >= 1
    assert all('diff' in p for p in full['patches'])


# ============================================================================
# RUNNER
# ============================================================================

def main():
    print("=" * 70)
    print("🧪 TEST AUDIT FEATURES - 13 features from 4-pattern audit")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for name, fn in TESTS:
        try:
            fn()
            print(f"✅ {name}")
            passed += 1
        except Exception as e:
            print(f"❌ {name} - {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"Total Tests: {len(TESTS)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed / len(TESTS) * 100:.1f}%")
    print("=" * 70)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
