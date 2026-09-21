"""
Advanced Tension Analyzer - Analyze and predict tension issues
"""

class AdvancedTensionAnalyzer:
    def __init__(self):
        self.tension_profiles = {
            "tight": {"gauge_multiplier": 1.2, "fabric_stiffness": 0.8},
            "normal": {"gauge_multiplier": 1.0, "fabric_stiffness": 0.5},
            "loose": {"gauge_multiplier": 0.8, "fabric_stiffness": 0.3},
        }
    
    def analyze_tension(self, pattern_text: str, crocheter_profile: str = "normal") -> dict:
        """Analyze tension characteristics"""
        profile = self.tension_profiles.get(crocheter_profile, self.tension_profiles["normal"])
        
        lines = pattern_text.strip().split('\n')
        stitch_counts = []
        
        for line in lines:
            count = line.lower().count("sc") + line.lower().count("dc") + line.lower().count("hdc")
            if count > 0:
                stitch_counts.append(count)
        
        avg_stitches = sum(stitch_counts) / len(stitch_counts) if stitch_counts else 0
        consistency = self._calculate_consistency(stitch_counts)
        
        issues = []
        if consistency < 0.7:
            issues.append("Inconsistent stitch count - tension may vary")
        
        if crocheter_profile == "tight":
            issues.append("Tight tension - consider larger hook")
        elif crocheter_profile == "loose":
            issues.append("Loose tension - consider smaller hook")
        
        return {
            "avg_stitches_per_row": avg_stitches,
            "consistency_score": consistency,
            "tension_profile": crocheter_profile,
            "gauge_multiplier": profile["gauge_multiplier"],
            "fabric_stiffness": profile["fabric_stiffness"],
            "issues": issues,
            "recommendations": self._get_recommendations(crocheter_profile, consistency)
        }
    
    def _calculate_consistency(self, stitch_counts: list) -> float:
        """Calculate stitch count consistency"""
        if len(stitch_counts) < 2:
            return 1.0
        
        avg = sum(stitch_counts) / len(stitch_counts)
        variance = sum((x - avg) ** 2 for x in stitch_counts) / len(stitch_counts)
        std_dev = variance ** 0.5
        
        consistency = 1.0 - (std_dev / avg) if avg > 0 else 1.0
        return max(0, min(1, consistency))
    
    def _get_recommendations(self, profile: str, consistency: float) -> list:
        """Get tension recommendations"""
        recommendations = []
        
        if profile == "tight":
            recommendations.append("Use hook 0.5mm larger than recommended")
            recommendations.append("Relax your grip on yarn")
        elif profile == "loose":
            recommendations.append("Use hook 0.5mm smaller than recommended")
            recommendations.append("Maintain firmer yarn tension")
        
        if consistency < 0.8:
            recommendations.append("Practice consistent tension")
            recommendations.append("Use stitch markers to track progress")
        
        return recommendations

if __name__ == "__main__":
    print("🎯 Advanced Tension Analyzer")
    print("=" * 60)
    
    analyzer = AdvancedTensionAnalyzer()
    
    pattern = """Row 1: 10 sc
Row 2: 12 sc
Row 3: 11 sc
Row 4: 10 sc"""
    
    print("\n📊 Analyzing tension...")
    result = analyzer.analyze_tension(pattern, "normal")
    
    print(f"\nAverage stitches per row: {result['avg_stitches_per_row']:.1f}")
    print(f"Consistency score: {result['consistency_score']:.2f}")
    print(f"Tension profile: {result['tension_profile']}")
    print(f"Gauge multiplier: {result['gauge_multiplier']}")
    
    if result['issues']:
        print("\n⚠️ Issues detected:")
        for issue in result['issues']:
            print(f"  • {issue}")
    
    print("\n💡 Recommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
    
    print("\n✨ Analysis complete!")
