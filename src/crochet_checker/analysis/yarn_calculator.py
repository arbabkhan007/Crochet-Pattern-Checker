"""Yarn Calculator"""

from dataclasses import dataclass


@dataclass
class YarnRequirement:
    total_yards: float
    skeins_needed: int


class AdvancedYarnCalculator:
    def calculate(
        self, pattern_text: str, yarn_weight: str = "worsted"
    ) -> YarnRequirement:
        stitch_count = pattern_text.lower().count("sc") + pattern_text.lower().count(
            "dc"
        )
        yards_per_stitch = {"lace": 0.8, "worsted": 1.5, "bulky": 2.0}.get(
            yarn_weight, 1.5
        )
        total_yards = stitch_count * yards_per_stitch * 1.1
        return YarnRequirement(
            total_yards=total_yards, skeins_needed=int(total_yards / 200) + 1
        )
