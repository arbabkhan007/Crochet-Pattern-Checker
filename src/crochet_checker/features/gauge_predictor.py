"""
Gauge Predictor - Predict gauge based on yarn and hook
"""

class GaugePredictor:
    def __init__(self):
        self.gauge_data = {
            ("worsted", "5.0mm", "sc"): {"stitches_per_4in": 14, "rows_per_4in": 16},
            ("worsted", "5.0mm", "dc"): {"stitches_per_4in": 12, "rows_per_4in": 14},
            ("dk", "4.0mm", "sc"): {"stitches_per_4in": 18, "rows_per_4in": 20},
            ("bulky", "6.5mm", "sc"): {"stitches_per_4in": 10, "rows_per_4in": 12},
        }
    
    def predict_gauge(self, yarn_weight: str, hook_size: str, stitch_type: str) -> dict:
        """Predict gauge for given parameters"""
        key = (yarn_weight.lower(), hook_size, stitch_type.lower())
        gauge = self.gauge_data.get(key, {"stitches_per_4in": 14, "rows_per_4in": 16})
        
        return {
            "stitches_per_4_inches": gauge["stitches_per_4in"],
            "rows_per_4_inches": gauge["rows_per_4in"],
            "stitches_per_cm": gauge["stitches_per_4in"] / 10.16,
            "rows_per_cm": gauge["rows_per_4in"] / 10.16,
            "yarn_weight": yarn_weight,
            "hook_size": hook_size,
            "stitch_type": stitch_type
        }
    
    def calculate_project_size(self, gauge: dict, stitch_count: int, row_count: int) -> dict:
        """Calculate final project size"""
        width_inches = (stitch_count / gauge["stitches_per_4_inches"]) * 4
        height_inches = (row_count / gauge["rows_per_4_inches"]) * 4
        
        return {
            "width_inches": width_inches,
            "height_inches": height_inches,
            "width_cm": width_inches * 2.54,
            "height_cm": height_inches * 2.54
        }

if __name__ == "__main__":
    print("📏 Gauge Predictor")
    print("=" * 60)
    
    predictor = GaugePredictor()
    
    print("\n📊 Predicting gauge...")
    gauge = predictor.predict_gauge("worsted", "5.0mm", "sc")
    
    print(f"\nPredicted gauge:")
    print(f"  {gauge['stitches_per_4_inches']} stitches x {gauge['rows_per_4_inches']} rows = 4 inches")
    print(f"  {gauge['stitches_per_cm']:.1f} stitches/cm x {gauge['rows_per_cm']:.1f} rows/cm")
    
    size = predictor.calculate_project_size(gauge, 40, 30)
    print(f"\nFor 40 stitches x 30 rows:")
    print(f"  Size: {size['width_inches']:.1f} x {size['height_inches']:.1f} inches")
    print(f"  Size: {size['width_cm']:.1f} x {size['height_cm']:.1f} cm")
    
    print("\n✨ Prediction complete!")
