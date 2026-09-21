"""
Virtual Fit Simulator - Simulate how garments will fit
"""

class VirtualFitSimulator:
    def __init__(self):
        self.body_measurements = {
            "small": {"bust": 86, "waist": 68, "hips": 91},
            "medium": {"bust": 96, "waist": 78, "hips": 101},
            "large": {"bust": 106, "waist": 88, "hips": 111},
        }
    
    def simulate_fit(self, pattern_dimensions: dict, body_size: str = "medium") -> dict:
        """Simulate garment fit"""
        body = self.body_measurements.get(body_size, self.body_measurements["medium"])
        
        bust_fit = self._calculate_fit(pattern_dimensions.get("bust", 0), body["bust"])
        waist_fit = self._calculate_fit(pattern_dimensions.get("waist", 0), body["waist"])
        hips_fit = self._calculate_fit(pattern_dimensions.get("hips", 0), body["hips"])
        
        overall_fit = (bust_fit["score"] + waist_fit["score"] + hips_fit["score"]) / 3
        
        return {
            "body_size": body_size,
            "bust_fit": bust_fit,
            "waist_fit": waist_fit,
            "hips_fit": hips_fit,
            "overall_fit_score": overall_fit,
            "fit_rating": self._get_fit_rating(overall_fit),
            "recommendations": self._get_fit_recommendations(overall_fit, bust_fit, waist_fit, hips_fit)
        }
    
    def _calculate_fit(self, garment_measurement: float, body_measurement: float) -> dict:
        """Calculate fit for specific measurement"""
        if garment_measurement == 0:
            return {"score": 50, "ease": 0, "status": "no_data"}
        
        ease = garment_measurement - body_measurement
        ease_percent = (ease / body_measurement) * 100
        
        if -2 <= ease <= 5:
            score = 100
            status = "perfect_fit"
        elif ease > 5:
            score = max(50, 100 - (ease - 5) * 5)
            status = "loose"
        else:
            score = max(50, 100 - abs(ease) * 10)
            status = "tight"
        
        return {
            "score": score,
            "ease_cm": ease,
            "ease_percent": ease_percent,
            "status": status
        }
    
    def _get_fit_rating(self, score: float) -> str:
        """Get overall fit rating"""
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Fair"
        else:
            return "Poor"
    
    def _get_fit_recommendations(self, overall: float, bust: dict, waist: dict, hips: dict) -> list:
        """Get fit recommendations"""
        recommendations = []
        
        if overall < 70:
            recommendations.append("Consider adjusting pattern for better fit")
        
        if bust["status"] == "tight":
            recommendations.append("Add width at bust area")
        elif bust["status"] == "loose":
            recommendations.append("Reduce width at bust or add darts")
        
        if waist["status"] == "tight":
            recommendations.append("Add ease at waist")
        
        return recommendations

if __name__ == "__main__":
    print("👗 Virtual Fit Simulator")
    print("=" * 60)
    
    simulator = VirtualFitSimulator()
    
    garment = {"bust": 98, "waist": 80, "hips": 103}
    
    print("\n📊 Simulating fit for medium body...")
    result = simulator.simulate_fit(garment, "medium")
    
    print(f"\nBody Size: {result['body_size']}")
    print(f"Overall Fit Score: {result['overall_fit_score']:.0f}/100")
    print(f"Fit Rating: {result['fit_rating']}")
    
    print(f"\nDetailed Fit:")
    print(f"  Bust: {result['bust_fit']['status']} ({result['bust_fit']['ease_cm']:+.1f} cm ease)")
    print(f"  Waist: {result['waist_fit']['status']} ({result['waist_fit']['ease_cm']:+.1f} cm ease)")
    print(f"  Hips: {result['hips_fit']['status']} ({result['hips_fit']['ease_cm']:+.1f} cm ease)")
    
    if result['recommendations']:
        print("\n💡 Recommendations:")
        for rec in result['recommendations']:
            print(f"  • {rec}")
    
    print("\n✨ Simulation complete!")
