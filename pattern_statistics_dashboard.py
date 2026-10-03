"""
Pattern Statistics Dashboard - Track statistics
"""

class PatternStatisticsDashboard:
    def __init__(self):
        self.statistics = {
            "total_patterns": 0,
            "by_category": {},
            "by_difficulty": {},
            "total_yardage": 0,
        }
    
    def add_pattern_stats(self, pattern_data: dict) -> dict:
        self.statistics["total_patterns"] += 1
        category = pattern_data.get("category", "general")
        self.statistics["by_category"][category] = self.statistics["by_category"].get(category, 0) + 1
        return self.statistics
    
    def get_summary(self) -> dict:
        return {
            "total_patterns": self.statistics["total_patterns"],
            "categories": len(self.statistics["by_category"]),
        }

if __name__ == "__main__":
    print("📊 Pattern Statistics Dashboard")
    print("=" * 60)
    dashboard = PatternStatisticsDashboard()
    dashboard.add_pattern_stats({"category": "amigurumi"})
    dashboard.add_pattern_stats({"category": "blanket"})
    summary = dashboard.get_summary()
    print(f"\nTotal Patterns: {summary['total_patterns']}")
    print(f"Categories: {summary['categories']}")
    print("\n✨ Pattern Statistics Dashboard complete!")
