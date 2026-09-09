"""
Custom Sizing Calculator - Input body measurements, get perfect-fit pattern adjustments
"""
import json
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


class CustomSizingCalculator:
    """
    Calculate custom sizing for crochet garments
    
    Features:
    - Body measurement input
    - Gauge-based sizing
    - Pattern adjustments
    - Ease calculations
    - Standard size charts
    - Fit recommendations
    """
    
    STANDARD_SIZES = {
        "XS": {"bust": 32, "waist": 24, "hip": 34, "sleeve": 23},
        "S":  {"bust": 34, "waist": 26, "hip": 36, "sleeve": 23.5},
        "M":  {"bust": 36, "waist": 28, "hip": 38, "sleeve": 24},
        "L":  {"bust": 38, "waist": 30, "hip": 40, "sleeve": 24.5},
        "XL": {"bust": 40, "waist": 32, "hip": 42, "sleeve": 25},
        "2XL": {"bust": 44, "waist": 36, "hip": 46, "sleeve": 25.5},
        "3XL": {"bust": 48, "waist": 40, "hip": 50, "sleeve": 26},
        "4XL": {"bust": 52, "waist": 44, "hip": 54, "sleeve": 26.5},
        "5XL": {"bust": 56, "waist": 48, "hip": 58, "sleeve": 27},
    }
    
    EASE_TYPES = {
        "fitted": {"bust": 2, "waist": 1, "hip": 2},
        "semi_fitted": {"bust": 4, "waist": 3, "hip": 4},
        "relaxed": {"bust": 6, "waist": 5, "hip": 6},
        "oversized": {"bust": 10, "waist": 8, "hip": 10},
    }
    
    GARMENT_TYPES = {
        "sweater": {"areas": ["bust", "waist", "hip", "sleeve", "length"]},
        "cardigan": {"areas": ["bust", "waist", "hip", "sleeve", "length"]},
        "tank_top": {"areas": ["bust", "waist", "hip", "length"]},
        "hat": {"areas": ["head_circumference", "depth"]},
        "sock": {"areas": ["foot_circumference", "foot_length", "calf"]},
        "mittens": {"areas": ["hand_circumference", "hand_length"]},
        "scarf": {"areas": ["width", "length"]},
        "blanket": {"areas": ["width", "length"]},
    }
    
    def calculate_gauge(self, swatch_stitches: int, swatch_inches: float,
                       swatch_rows: int = None, swatch_rows_inches: float = None) -> Dict:
        """Calculate gauge from a swatch"""
        sts_per_inch = swatch_stitches / swatch_inches
        rows_per_inch = None
        if swatch_rows and swatch_rows_inches:
            rows_per_inch = swatch_rows / swatch_rows_inches
        
        return {
            "sts_per_inch": round(sts_per_inch, 2),
            "rows_per_inch": round(rows_per_inch, 2) if rows_per_inch else None,
            "sts_per_4_inches": round(sts_per_inch * 4, 1),
            "rows_per_4_inches": round(rows_per_inch * 4, 1) if rows_per_inch else None,
        }
    
    def match_standard_size(self, bust: float = None, waist: float = None,
                           hip: float = None) -> Dict:
        """Find the closest standard size"""
        if not any([bust, waist, hip]):
            return {"error": "Please provide at least one measurement"}
        
        matches = {}
        for size, measurements in self.STANDARD_SIZES.items():
            diffs = []
            if bust:
                diffs.append(abs(measurements["bust"] - bust))
            if waist:
                diffs.append(abs(measurements["waist"] - waist))
            if hip:
                diffs.append(abs(measurements["hip"] - hip))
            matches[size] = round(sum(diffs) / len(diffs), 1)
        
        best = min(matches.items(), key=lambda x: x[1])
        
        return {
            "recommended_size": best[0],
            "avg_difference": best[1],
            "all_sizes": matches,
            "your_measurements": {"bust": bust, "waist": waist, "hip": hip},
        }
    
    def calculate_custom_sizing(self, body_measurement: float, gauge_sts_per_inch: float,
                               ease: float = 2, garment_part: str = "bust") -> Dict:
        """Calculate stitches needed for custom sizing"""
        total_inches = body_measurement + ease
        total_stitches = math.ceil(total_inches * gauge_sts_per_inch)
        
        return {
            "body_measurement": body_measurement,
            "ease": ease,
            "finished_measurement": round(total_inches, 1),
            "gauge_sts_per_inch": gauge_sts_per_inch,
            "total_stitches": total_stitches,
            "garment_part": garment_part,
        }
    
    def adjust_pattern(self, original_gauge: Dict, new_gauge: Dict,
                      original_size: str = "M", target_measurements: Dict = None) -> Dict:
        """Adjust pattern for different gauge or size"""
        orig_sts = original_gauge["sts_per_inch"]
        new_sts = new_gauge["sts_per_inch"]
        
        ratio = orig_sts / new_sts if new_sts > 0 else 1
        
        size_info = self.STANDARD_SIZES.get(original_size, {})
        
        if target_measurements:
            adjustments = {}
            for part, measurement in target_measurements.items():
                original = size_info.get(part, measurement)
                scale = measurement / original if original > 0 else 1
                adjustments[part] = {
                    "original": original,
                    "target": measurement,
                    "scale_factor": round(scale, 2),
                    "adjustment_pct": round((scale - 1) * 100, 1),
                }
        else:
            adjustments = {}
        
        return {
            "original_gauge": orig_sts,
            "new_gauge": new_sts,
            "gauge_ratio": round(ratio, 2),
            "adjustments": adjustments,
            "recommendation": self._get_recommendation(ratio),
        }
    
    def _get_recommendation(self, ratio: float) -> str:
        if ratio < 0.85:
            return "⚠️ Significantly different gauge - consider changing hook size"
        elif ratio < 0.95:
            return "Slightly different gauge - minor adjustments needed"
        elif ratio <= 1.05:
            return "✅ Gauge matches well - minimal adjustments needed"
        elif ratio <= 1.15:
            return "Slightly different gauge - minor adjustments needed"
        else:
            return "⚠️ Significantly different gauge - consider changing hook size"
    
    def full_sizing_plan(self, measurements: Dict, gauge: Dict,
                        garment_type: str = "sweater", fit: str = "semi_fitted") -> Dict:
        """Complete sizing plan for a garment"""
        ease = self.EASE_TYPES.get(fit, self.EASE_TYPES["semi_fitted"])
        garment = self.GARMENT_TYPES.get(garment_type, self.GARMENT_TYPES["sweater"])
        
        plan = {}
        for area in garment["areas"]:
            body = measurements.get(area, 0)
            if body == 0:
                continue
            
            ease_amount = ease.get(area, 2)
            total_inches = body + ease_amount
            sts_needed = math.ceil(total_inches * gauge["sts_per_inch"])
            
            plan[area] = {
                "body": body,
                "ease": ease_amount,
                "finished": round(total_inches, 1),
                "stitches": sts_needed,
                "rows": math.ceil(total_inches * gauge.get("rows_per_inch", 5)) if gauge.get("rows_per_inch") else None,
            }
        
        return {
            "garment": garment_type,
            "fit": fit,
            "gauge": gauge,
            "measurements": measurements,
            "plan": plan,
        }
    
    def generate_size_chart_html(self, pattern_stitches: Dict = None) -> str:
        """Generate HTML size chart"""
        rows = ""
        for size, m in self.STANDARD_SIZES.items():
            row = f"<tr><td><strong>{size}</strong></td>"
            row += f"<td>{m['bust']}</td><td>{m['waist']}</td><td>{m['hip']}</td><td>{m['sleeve']}</td>"
            if pattern_stitches and size in pattern_stitches:
                row += f"<td>{pattern_stitches[size]}</td>"
            row += "</tr>"
            rows += row
        
        extra_header = "<th>Pattern Sts</th>" if pattern_stitches else ""
        
        return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Size Chart</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
table {{ margin: 20px auto; border-collapse: collapse; }}
th, td {{ padding: 10px 16px; border: 1px solid #0f3460; text-align: center; }}
th {{ background: #16213e; }}
h1 {{ text-align: center; }}
.note {{ text-align: center; color: #888; max-width: 600px; margin: 0 auto; }}
</style></head>
<body>
<h1>📐 Garment Size Chart</h1>
<p class="note">All measurements in inches. Measure yourself and add ease for desired fit.</p>
<table>
<tr><th>Size</th><th>Bust</th><th>Waist</th><th>Hip</th><th>Sleeve</th>{extra_header}</tr>
{rows}
</table>
</body></html>'''


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  CUSTOM SIZING CALCULATOR - DEMONSTRATION")
    print("=" * 60)
    
    calc = CustomSizingCalculator()
    
    # Gauge
    print(f"\n📏 Calculating Gauge:")
    gauge = calc.calculate_gauge(swatch_stitches=16, swatch_inches=4, swatch_rows=12, swatch_rows_inches=4)
    print(f"  16 sts / 4 inches = {gauge['sts_per_inch']} sts/inch")
    print(f"  12 rows / 4 inches = {gauge['rows_per_inch']} rows/inch")
    
    # Match standard size
    print(f"\n👤 Finding Best Size:")
    match = calc.match_standard_size(bust=37, waist=29, hip=39)
    print(f"  Your measurements: Bust {37}, Waist {29}, Hip {39}")
    print(f"  Recommended: {match['recommended_size']} (avg diff: {match['avg_difference']}\")")
    
    # Custom sizing
    print(f"\n🧮 Custom Sizing (Bust = 37\", ease = 4\"):")
    sizing = calc.calculate_custom_sizing(37, gauge['sts_per_inch'], ease=4, garment_part="bust")
    print(f"  Body: {sizing['body_measurement']}\"")
    print(f"  + Ease: {sizing['ease']}\"")
    print(f"  = Finished: {sizing['finished_measurement']}\"")
    print(f"  → Need {sizing['total_stitches']} stitches")
    
    # Full sizing plan
    print(f"\n📋 Full Sweater Sizing Plan:")
    measurements = {"bust": 37, "waist": 29, "hip": 39, "sleeve": 24, "length": 22}
    plan = calc.full_sizing_plan(measurements, gauge, "sweater", "semi_fitted")
    for area, data in plan['plan'].items():
        print(f"  {area}: Body {data['body']}\" + Ease {data['ease']}\" = {data['finished']}\" → {data['stitches']} sts")
    
    # Pattern adjustment
    print(f"\n🔄 Pattern Adjustment:")
    adj = calc.adjust_pattern(
        original_gauge={"sts_per_inch": 4},
        new_gauge={"sts_per_inch": 4.5},
        original_size="M",
        target_measurements={"bust": 40}
    )
    print(f"  Original gauge: {adj['original_gauge']} sts/in")
    print(f"  New gauge: {adj['new_gauge']} sts/in")
    print(f"  Ratio: {adj['gauge_ratio']}")
    print(f"  {adj['recommendation']}")
    
    # Size chart HTML
    html = calc.generate_size_chart_html()
    print(f"\n✅ Size chart HTML: {len(html)} chars")
    
    print(f"\n  Custom Sizing Calculator Complete! 📐")
