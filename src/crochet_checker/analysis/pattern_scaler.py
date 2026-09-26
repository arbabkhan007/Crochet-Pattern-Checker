"""Pattern Scaler"""

from dataclasses import dataclass


@dataclass
class ScaleResult:
    scale_factor: float
    adjusted_stitches: int
    adjustments: list[str]


class PatternScaler:
    def scale(
        self,
        pattern_text: str,
        original_size: tuple[int, int],
        target_size: tuple[int, int],
    ) -> ScaleResult:
        scale_factor = target_size[0] / original_size[0]
        stitch_count = pattern_text.lower().count("sc") + pattern_text.lower().count(
            "dc"
        )
        return ScaleResult(
            scale_factor=scale_factor,
            adjusted_stitches=int(stitch_count * scale_factor),
            adjustments=[f"Scale factor: {scale_factor:.2f}x"],
        )
