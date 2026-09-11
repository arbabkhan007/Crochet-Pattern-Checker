"""
MASTER TEST SCRIPT - Test ALL 70 features in one command
Run: python test_all_features.py
"""
import os
import sys
import subprocess
import time
from datetime import datetime

FEATURES_DIR = "src/crochet_checker/features"
TIMEOUT = 30

SLOW_FILES = {
    "ai_tutorial_generator": 120,
    "photo_studio": 60,
}

SLOW_FILES = {"ai_tutorial_generator": 120, "photo_studio": 60}  # seconds per test

# Files that need extra time
SLOW_FILES = {
    "ai_tutorial_generator": 60,  # Downloads audio
    "photo_studio": 45,
}

# Skip these (utility files, not standalone features)
SKIP_FILES = ["__init__.py", "_pdf_utils.py", "robust_cli.py"]

def test_feature(filepath, project_root=".", filename=""):
    """Test a single feature file"""
    timeout = SLOW_FILES.get(filename, TIMEOUT)
    try:
        abs_path = os.path.abspath(filepath)
        result = subprocess.run(
            [sys.executable, abs_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=project_root
        )
        
        if result.returncode == 0:
            # Get the last meaningful line
            lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
            last_line = lines[-1] if lines else "OK"
            return True, last_line
        else:
            error_lines = [l.strip() for l in result.stderr.strip().split("\n") if l.strip()]
            error = error_lines[-1] if error_lines else f"Exit code {result.returncode}"
            return False, error[:80]
    
    except subprocess.TimeoutExpired:
        return False, f"Timeout ({timeout}s)"
    except Exception as e:
        return False, str(e)[:80]


def main():
    start_time = time.time()
    
    print()
    print("=" * 70)
    print("  🧶 CROCHET PATTERN CHECKER - MASTER TEST SUITE")
    print(f"  📅 {datetime.now().strftime('%B %d, %Y %I:%M %p')}")
    print("=" * 70)
    print()
    
    # Find all feature files
    if not os.path.exists(FEATURES_DIR):
        print(f"  ❌ Features directory not found: {FEATURES_DIR}")
        print(f"  💡 Run this from the project root!")
        sys.exit(1)
    
    feature_files = sorted([
        f for f in os.listdir(FEATURES_DIR)
        if f.endswith(".py") and f not in SKIP_FILES and not f.startswith("_")
    ])
    
    total = len(feature_files)
    print(f"  📦 Found {total} features to test")
    print(f"  ⏱️  Timeout per test: {TIMEOUT}s")
    print()
    print("-" * 70)
    print(f"  {'#':<4} {'FEATURE':<35} {'STATUS':<8} {'DETAIL'}")
    print("-" * 70)
    
    passed = 0
    failed = 0
    failed_list = []
    
    # Get project root
    project_root = os.path.abspath(".")
    
    for i, filename in enumerate(feature_files, 1):
        filepath = os.path.join(FEATURES_DIR, filename)
        name = filename.replace(".py", "")
        
        # Progress indicator
        status, detail = test_feature(filepath, project_root, filename)
        
        if status:
            passed += 1
            symbol = "✅"
            status_text = "PASS"
        else:
            failed += 1
            failed_list.append((name, detail))
            symbol = "❌"
            status_text = "FAIL"
        
        # Truncate detail for display
        detail_short = detail[:30] if len(detail) > 30 else detail
        print(f"  {symbol} {i:<3} {name:<35} {status_text:<8} {detail_short}")
    
    elapsed = time.time() - start_time
    
    print("-" * 70)
    print()
    
    # Summary
    pct = round((passed / total) * 100, 1) if total > 0 else 0
    
    print(f"  {'═' * 50}")
    print(f"  📊 RESULTS")
    print(f"  {'═' * 50}")
    print(f"  Total Features:  {total}")
    print(f"  ✅ Passed:       {passed}")
    print(f"  ❌ Failed:       {failed}")
    print(f"  Success Rate:    {pct}%")
    print(f"  Time Taken:      {elapsed:.1f}s")
    
    if failed_list:
        print()
        print(f"  ❌ FAILED FEATURES:")
        print(f"  {'─' * 50}")
        for name, error in failed_list:
            print(f"    • {name}")
            print(f"      Error: {error}")
    
    print()
    if failed == 0:
        print(f"  🎉 ALL {total} FEATURES PASS! Your repo is ready to push!")
    elif pct >= 90:
        print(f"  👍 {pct}% passing - almost perfect!")
    elif pct >= 70:
        print(f"  📝 {pct}% passing - some fixes needed")
    else:
        print(f"  ⚠️  {pct}% passing - multiple issues to fix")
    
    print(f"  {'═' * 50}")
    print()
    
    # Return exit code
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
