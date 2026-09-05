"""Gauge Calculator"""

from dataclasses import dataclass

@dataclass
class GaugeInfo:
    stitches_per_inch: float
    rows_per_inch: float
    stitch_size_mm: float
    row_size_mm: float
    recommended_hook: str
    tension: str

def calculate_gauge(stitch_count: int, row_count: int, width_inches: float, height_inches: float) -> GaugeInfo:
    sts_per_inch = stitch_count / width_inches
    rows_per_inch = row_count / height_inches
    stitch_size_mm = 25.4 / sts_per_inch
    row_size_mm = 25.4 / rows_per_inch
    
    hook_sizes = [(2.0, "2.0 mm"), (3.5, "3.5 mm (E-4)"), (5.0, "5.0 mm (H-8)"), (6.0, "6.0 mm (J-10)")]
    recommended_hook = min(hook_sizes, key=lambda x: abs(x[0] - stitch_size_mm))[1]
    
    tension = 'tight' if stitch_size_mm < 4.0 else 'loose' if stitch_size_mm > 6.0 else 'normal'
    
    return GaugeInfo(
        stitches_per_inch=round(sts_per_inch, 2),
        rows_per_inch=round(rows_per_inch, 2),
        stitch_size_mm=round(stitch_size_mm, 2),
        row_size_mm=round(row_size_mm, 2),
        recommended_hook=recommended_hook,
        tension=tension
    )

def format_gauge_info(gauge: GaugeInfo) -> str:
    return f"""📐 Gauge Information
{'=' * 40}
Stitches per inch: {gauge.stitches_per_inch}
Rows per inch: {gauge.rows_per_inch}
Stitch size: {gauge.stitch_size_mm} mm
Recommended hook: {gauge.recommended_hook}
Tension: {gauge.tension}"""
