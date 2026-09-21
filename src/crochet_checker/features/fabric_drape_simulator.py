"""
Fabric Drape Simulator - Simulate how fabric will drape
"""

class FabricDrapeSimulator:
    def __init__(self):
        self.drape_properties = {
            "sc": {"stiffness": 0.7, "drape": 0.3},
            "dc": {"stiffness": 0.4, "drape": 0.6},
            "hdc": {"stiffness": 0.5, "drape": 0.5},
            "tr": {"stiffness": 0.3, "drape": 0.7},
        }
    
    def simulate_drape(self, stitch_pattern: list) -> dict:
        """Simulate fabric drape characteristics"""
        total_stiffness = 0
        total_drape = 0
        count = len(stitch_pattern)
        
        for stitch in stitch_pattern:
            props = self.drape_properties.get(stitch, {"stiffness": 0.5, "drape": 0.5})
            total_stiffness += props["stiffness"]
            total_drape += props["drape"]
        
        avg_stiffness = total_stiffness / count if count > 0 else 0.5
        avg_drape = total_drape / count if count > 0 else 0.5
        
        if avg_drape > 0.6:
            drape_quality = "excellent"
        elif avg_drape > 0.4:
            drape_quality = "good"
        else:
            drape_quality = "stiff"
        
        return {
            "stiffness_score": avg_stiffness,
            "drape_score": avg_drape,
            "drape_quality": drape_quality,
            "best_for": self._recommend_use(avg_drape),
            "fabric_behavior": "fluid" if avg_drape > 0.6 else "structured" if avg_drape < 0.4 else "balanced"
        }
    
    def _recommend_use(self, drape_score: float) -> str:
        """Recommend best use based on drape"""
        if drape_score > 0.6:
            return "Scarves, shawls, flowing garments"
        elif drape_score > 0.4:
            return "Sweaters, blankets, bags"
        else:
            return "Amigurumi, hats, structured items"

if __name__ == "__main__":
    print("🧣 Fabric Drape Simulator")
    print("=" * 60)
    
    simulator = FabricDrapeSimulator()
    
    stitch_pattern = ["dc", "dc", "dc", "sc", "dc", "dc"]
    
    print(f"\nAnalyzing stitch pattern: {stitch_pattern}")
    result = simulator.simulate_drape(stitch_pattern)
    
    print(f"\nDrape characteristics:")
    print(f"  Stiffness: {result['stiffness_score']:.2f}")
    print(f"  Drape: {result['drape_score']:.2f}")
    print(f"  Quality: {result['drape_quality']}")
    print(f"  Behavior: {result['fabric_behavior']}")
    print(f"  Best for: {result['best_for']}")
    
    print("\n✨ Simulation complete!")
