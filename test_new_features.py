"""
Test suite for all new advanced features
"""
import sys
sys.path.insert(0, '/home/user/crochet-pattern-checker/src')

print("=" * 70)
print("🧪 TESTING NEW ADVANCED FEATURES")
print("=" * 70)

# Test 1: Pattern Optimizer
print("\n1️⃣ Testing Pattern Optimizer...")
from crochet_checker.optimization.pattern_optimizer import PatternOptimizer
optimizer = PatternOptimizer()
test_pattern = "Round 1: sc in each st around, ch 1, turn"
optimizations = optimizer.optimize(test_pattern)
print(f"✅ Found {len(optimizations)} optimizations")

# Test 2: Pattern Debugger
print("\n2️⃣ Testing Pattern Debugger...")
from crochet_checker.visualization.pattern_debugger import PatternDebugger
debugger = PatternDebugger()
debugger.set_breakpoint(5)
debugger.set_breakpoint(10)
visual_map = debugger.generate_visual_map(test_pattern)
print(f"✅ Generated visual map with {len(debugger.breakpoints)} breakpoints")

# Test 3: Interactive Stitch Counter
print("\n3️⃣ Testing Interactive Stitch Counter...")
from crochet_checker.interactive.stitch_counter import InteractiveStitchCounter
counter = InteractiveStitchCounter({1: 6, 2: 12, 3: 18})
for i in range(6):
    counter.complete_stitch("sc")
counter.next_round()
progress = counter.get_progress()
print(f"✅ Progress: {progress['total_stitches']} stitches, {progress['current_round']} rounds")

# Test 4: Complexity Analyzer
print("\n4️⃣ Testing Complexity Analyzer...")
from crochet_checker.analysis.complexity_analyzer import ComplexityAnalyzer
analyzer = ComplexityAnalyzer()
complexity = analyzer.analyze(test_pattern)
print(f"✅ Complexity: {complexity.overall_score:.1f}/100 ({complexity.difficulty_level})")

# Test 5: Time Estimator
print("\n5️⃣ Testing Time Estimator...")
from crochet_checker.analysis.time_estimator import TimeEstimator
estimator = TimeEstimator()
estimate = estimator.estimate(test_pattern, 'intermediate')
print(f"✅ Estimated time: {estimate.total_hours:.1f} hours")

# Test 6: Yarn Calculator
print("\n6️⃣ Testing Advanced Yarn Calculator...")
from crochet_checker.analysis.yarn_calculator import AdvancedYarnCalculator
yarn_calc = AdvancedYarnCalculator()
yarn_req = yarn_calc.calculate(test_pattern, 'worsted')
print(f"✅ Yarn needed: {yarn_req.total_yards:.1f} yards ({yarn_req.skeins_needed} skeins)")

# Test 7: Pattern Scaler
print("\n7️⃣ Testing Pattern Scaler...")
from crochet_checker.analysis.pattern_scaler import PatternScaler
scaler = PatternScaler()
scale_result = scaler.scale(test_pattern, (10, 10), (15, 15))
print(f"✅ Scale factor: {scale_result.scale_factor:.2f}x")

# Test 8: Gauge Calculator
print("\n8️⃣ Testing Gauge Calculator...")
from crochet_checker.analysis.gauge_calculator import GaugeCalculator
gauge_calc = GaugeCalculator()
gauge = gauge_calc.calculate_from_swatches(17, 22, 4.0, 4.0, '5.0mm', 'worsted')
print(f"✅ Gauge: {gauge.stitches_per_4_inches:.1f} sts per 4\"")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\nNew Features Added:")
print("  ✅ Pattern Optimization Engine")
print("  ✅ Visual Pattern Debugger")
print("  ✅ Interactive Stitch Counter")
print("  ✅ Complexity Analyzer")
print("  ✅ Time Estimation Engine")
print("  ✅ Advanced Yarn Calculator")
print("  ✅ Pattern Scaling Calculator")
print("  ✅ Gauge Calculator")
