#!/usr/bin/env python3
"""
Comprehensive Test Suite for ALL Crochet Pattern Checker Features
Tests: Basic features, Spatial Compiler, and Advanced Tools
"""
import sys
import os
import time

# Add src to path
sys.path.insert(0, '/workspaces/crochet-pattern-checker/src')

print("=" * 80)
print("🧪 COMPREHENSIVE TEST SUITE - ALL FEATURES")
print("=" * 80)

test_results = {
    'passed': 0,
    'failed': 0,
    'total': 0,
    'categories': {}
}

def test_feature(name, test_func, category="General"):
    """Test a single feature"""
    test_results['total'] += 1
    if category not in test_results['categories']:
        test_results['categories'][category] = {'passed': 0, 'failed': 0}
    
    try:
        start = time.time()
        result = test_func()
        elapsed = time.time() - start
        
        if result:
            print(f"✅ {name} ({elapsed:.3f}s)")
            test_results['passed'] += 1
            test_results['categories'][category]['passed'] += 1
            return True
        else:
            print(f"❌ {name} - Test returned False")
            test_results['failed'] += 1
            test_results['categories'][category]['failed'] += 1
            return False
    except Exception as e:
        print(f"❌ {name} - {str(e)}")
        test_results['failed'] += 1
        test_results['categories'][category]['failed'] += 1
        return False

# ============================================================================
# CATEGORY 1: SPATIAL COMPILER FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("🏗️ TESTING SPATIAL COMPILER FEATURES")
print("=" * 80)

def test_lexer():
    from crochet_checker.lexer.markdown_parser import MarkdownParser
    parser = MarkdownParser()
    result = parser.parse("# Test\nRound 1: 6 sc")
    return result is not None

def test_glossary_extractor():
    from crochet_checker.lexer.glossary_extractor import GlossaryExtractor
    extractor = GlossaryExtractor()
    glossary = extractor.extract_glossary("sc - single crochet\ndc - double crochet")
    return len(glossary) > 0

def test_ast_builder():
    from crochet_checker.ast.ast_builder import ASTBuilder
    builder = ASTBuilder()
    ast = builder.build("Round 1: 6 sc\nRound 2: 12 sc")
    return ast is not None and len(ast.pieces) > 0

def test_unroller():
    from crochet_checker.ast.unroller import Unroller
    unroller = Unroller()
    result = unroller.unroll("*sc 2* repeat 3 times")
    return "sc" in result

def test_canvas_queue():
    from crochet_checker.engine.canvas_queue import CanvasQueue
    queue = CanvasQueue()
    queue.initialize_round(6)
    return queue.current_stitch_count == 6

def test_stitch_consumer():
    from crochet_checker.engine.stitch_consumer import StitchConsumer
    consumer = StitchConsumer()
    result = consumer.consume("sc", 1)
    return result is not None

def test_state_machine():
    from crochet_checker.engine.state_machine import StateMachine
    machine = StateMachine()
    machine.execute_instruction("sc", 6)
    return machine.state is not None

def test_assembly_graph():
    from crochet_checker.engine.assembly_graph import AssemblyGraph
    graph = AssemblyGraph()
    graph.add_piece("piece1")
    return len(graph.pieces) > 0

# Run spatial compiler tests
test_feature("Markdown Parser", test_lexer, "Spatial Compiler")
test_feature("Glossary Extractor", test_glossary_extractor, "Spatial Compiler")
test_feature("AST Builder", test_ast_builder, "Spatial Compiler")
test_feature("Repeat Unroller", test_unroller, "Spatial Compiler")
test_feature("Canvas Queue", test_canvas_queue, "Spatial Compiler")
test_feature("Stitch Consumer", test_stitch_consumer, "Spatial Compiler")
test_feature("State Machine", test_state_machine, "Spatial Compiler")
test_feature("Assembly Graph", test_assembly_graph, "Spatial Compiler")

# ============================================================================
# CATEGORY 2: OPTIMIZATION FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("🔧 TESTING OPTIMIZATION FEATURES")
print("=" * 80)

def test_pattern_optimizer():
    from crochet_checker.optimization.pattern_optimizer import PatternOptimizer
    optimizer = PatternOptimizer()
    optimizations = optimizer.optimize("Round 1: ch 1, sc in each st")
    return isinstance(optimizations, list)

test_feature("Pattern Optimizer", test_pattern_optimizer, "Optimization")

# ============================================================================
# CATEGORY 3: VISUALIZATION FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("🎨 TESTING VISUALIZATION FEATURES")
print("=" * 80)

def test_pattern_debugger():
    from crochet_checker.visualization.pattern_debugger import PatternDebugger
    debugger = PatternDebugger()
    debugger.set_breakpoint(5)
    return len(debugger.breakpoints) > 0

test_feature("Pattern Debugger", test_pattern_debugger, "Visualization")

# ============================================================================
# CATEGORY 4: INTERACTIVE FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("🎮 TESTING INTERACTIVE FEATURES")
print("=" * 80)

def test_stitch_counter():
    from crochet_checker.interactive.stitch_counter import InteractiveStitchCounter
    counter = InteractiveStitchCounter()
    counter.complete_stitch("sc")
    progress = counter.get_progress()
    return progress['total_stitches'] == 1

test_feature("Interactive Stitch Counter", test_stitch_counter, "Interactive")

# ============================================================================
# CATEGORY 5: ANALYSIS FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("📊 TESTING ANALYSIS FEATURES")
print("=" * 80)

def test_complexity_analyzer():
    from crochet_checker.analysis.complexity_analyzer import ComplexityAnalyzer
    analyzer = ComplexityAnalyzer()
    result = analyzer.analyze("Round 1: 6 sc")
    return result.overall_score >= 0

def test_time_estimator():
    from crochet_checker.analysis.time_estimator import TimeEstimator
    estimator = TimeEstimator()
    result = estimator.estimate("Round 1: 6 sc")
    return result.total_hours >= 0

def test_yarn_calculator():
    from crochet_checker.analysis.yarn_calculator import AdvancedYarnCalculator
    calc = AdvancedYarnCalculator()
    result = calc.calculate("Round 1: 6 sc", "worsted")
    return result.total_yards > 0

def test_pattern_scaler():
    from crochet_checker.analysis.pattern_scaler import PatternScaler
    scaler = PatternScaler()
    result = scaler.scale("Round 1: 6 sc", (10, 10), (15, 15))
    return result.scale_factor > 0

def test_gauge_calculator():
    from crochet_checker.analysis.gauge_calculator import GaugeCalculator
    calc = GaugeCalculator()
    result = calc.calculate_from_swatches(17, 4.0, "5.0mm", "worsted")
    return result.stitches_per_4_inches > 0

test_feature("Complexity Analyzer", test_complexity_analyzer, "Analysis")
test_feature("Time Estimator", test_time_estimator, "Analysis")
test_feature("Yarn Calculator", test_yarn_calculator, "Analysis")
test_feature("Pattern Scaler", test_pattern_scaler, "Analysis")
test_feature("Gauge Calculator", test_gauge_calculator, "Analysis")

# ============================================================================
# CATEGORY 6: VALIDATION FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("✅ TESTING VALIDATION FEATURES")
print("=" * 80)

def test_validator():
    from crochet_checker.validation.validator import PatternValidator
    validator = PatternValidator()
    result = validator.validate("Round 1: 6 sc")
    return result is not None

def test_reporter():
    from crochet_checker.validation.reporter import PatternReporter
    reporter = PatternReporter()
    report = reporter.generate_report("Round 1: 6 sc")
    return len(report) > 0

test_feature("Pattern Validator", test_validator, "Validation")
test_feature("Pattern Reporter", test_reporter, "Validation")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)

success_rate = (test_results['passed'] / test_results['total'] * 100) if test_results['total'] > 0 else 0

print(f"\nTotal Tests: {test_results['total']}")
print(f"✅ Passed: {test_results['passed']}")
print(f"❌ Failed: {test_results['failed']}")
print(f"📈 Success Rate: {success_rate:.1f}%")

print("\n📋 Results by Category:")
for category, results in test_results['categories'].items():
    total = results['passed'] + results['failed']
    rate = (results['passed'] / total * 100) if total > 0 else 0
    print(f"  {category:20s}: {results['passed']}/{total} ({rate:.0f}%)")

print("\n" + "=" * 80)
if test_results['failed'] == 0:
    print("🎉 ALL TESTS PASSED! Your crochet pattern checker is ready!")
else:
    print(f"⚠️  {test_results['failed']} test(s) failed. Check the output above.")
print("=" * 80)

sys.exit(0 if test_results['failed'] == 0 else 1)
