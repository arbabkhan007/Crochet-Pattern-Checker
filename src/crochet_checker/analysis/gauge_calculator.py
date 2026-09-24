"""Gauge Calculator"""
from dataclasses import dataclass

@dataclass
class GaugeInfo:
    stitches_per_4_inches: float
    matches_pattern: bool

class GaugeCalculator:
    def calculate_from_swatches(self, swatch_stitches: int, swatch_width_inches: float, hook_size: str, yarn_weight: str) -> GaugeInfo:
        sts_per_4 = (swatch_stitches / swatch_width_inches) * 4
        standard = {'worsted': 17, 'dk': 22, 'bulky': 14}.get(yarn_weight, 17)
        return GaugeInfo(stitches_per_4_inches=sts_per_4, matches_pattern=abs(sts_per_4 - standard) <= 2)
