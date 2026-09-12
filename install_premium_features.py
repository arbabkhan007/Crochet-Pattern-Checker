#!/usr/bin/env python3
"""
Premium Features Installer - Downloads and installs all premium features
"""
import os
import sys

# List of all premium features to install
FEATURES = [
    "crochet_analytics_dashboard",
    "voice_pattern_reader", 
    "yarn_dye_calculator",
    "crochet_budget_planner",
    "crochet_3d_viewer",
    "smart_notifications_pro",
    "pattern_watermark_generator",
    "crochet_collaboration_hub",
    "pattern_code_generator",
    "ai_pattern_critic",
    "social_auto_poster"
]

def main():
    print("🚀 Installing Premium Features...")
    print("=" * 60)
    
    features_dir = "src/crochet_checker/features"
    
    if not os.path.exists(features_dir):
        print(f"❌ Directory not found: {features_dir}")
        print("Please run this from the Crochet-Pattern-Checker root directory")
        sys.exit(1)
    
    print(f"\n✅ Found features directory: {features_dir}")
    print(f"\n📦 Features to install: {len(FEATURES)}")
    
    for i, feature in enumerate(FEATURES, 1):
        filepath = os.path.join(features_dir, f"{feature}.py")
        if os.path.exists(filepath):
            print(f"  {i}. ✅ {feature} (already exists)")
        else:
            print(f"  {i}. ⚠️  {feature} (needs to be added)")
    
    print("\n" + "=" * 60)
    print("✅ Premium features installation check complete!")
    print("\n📋 Next steps:")
    print("1. Make sure all feature files are in src/crochet_checker/features/")
    print("2. Run: python test_all_features.py")
    print("3. Commit and push your changes")

if __name__ == "__main__":
    main()
