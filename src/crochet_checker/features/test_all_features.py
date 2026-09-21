#!/usr/bin/env python3
"""
Complete Test Suite for All Crochet Pattern Checker Features
"""
import os
import sys
import importlib.util

def test_feature(file_path):
    """Test a single feature file"""
    try:
        spec = importlib.util.spec_from_file_location("module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    """Run all tests"""
    features_dir = os.path.dirname(os.path.abspath(__file__))
    feature_files = [f for f in os.listdir(features_dir) 
                     if f.endswith('.py') and f != '__init__.py' and f != 'test_all_features.py']
    
    print("🧪 CROCHET PATTERN CHECKER - COMPLETE TEST SUITE")
    print("=" * 70)
    print(f"\n📊 Testing {len(feature_files)} features...\n")
    
    passed = 0
    failed = 0
    errors = []
    
    for feature_file in sorted(feature_files):
        file_path = os.path.join(features_dir, feature_file)
        success, error = test_feature(file_path)
        
        if success:
            print(f"✅ {feature_file}")
            passed += 1
        else:
            print(f"❌ {feature_file}")
            failed += 1
            errors.append((feature_file, error))
    
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Total: {passed + failed}")
    
    if passed + failed > 0:
        success_rate = (passed / (passed + failed)) * 100
        print(f"🎉 Success Rate: {success_rate:.1f}%")
    
    if errors:
        print("\n❌ FAILED FEATURES:")
        for feature, error in errors:
            print(f"  • {feature}: {error[:100]}")
    
    print("\n" + "=" * 70)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
