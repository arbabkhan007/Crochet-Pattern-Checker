"""Monte Carlo geometry and tolerance simulation."""

from __future__ import annotations

import random
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class SimulationResult:
    simulations: int
    expected_width_cm: float
    minimum_width_cm: float
    maximum_width_cm: float
    expected_height_cm: float
    minimum_height_cm: float
    maximum_height_cm: float
    pass_probability: float
    tolerance_percent: float
    seed: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        import json

        return json.dumps(self.to_dict(), indent=2)


class MonteCarloSimulator:
    """
    Estimate dimensional variation caused by gauge and tension changes.

    This is a risk estimate, not a replacement for material calibration.
    """

    def __init__(
        self,
        simulations: int = 10_000,
        seed: int = 42,
    ):
        if simulations < 100:
            raise ValueError("simulations must be at least 100")

        self.simulations = simulations
        self.seed = seed

    def simulate(
        self,
        pattern,
        *,
        gauge_stitches_per_10cm: float,
        gauge_rows_per_10cm: float,
        tolerance_percent: float = 5.0,
        tension_variation_percent: float = 3.0,
    ) -> SimulationResult:
        if gauge_stitches_per_10cm <= 0:
            raise ValueError("gauge_stitches_per_10cm must be positive")

        if gauge_rows_per_10cm <= 0:
            raise ValueError("gauge_rows_per_10cm must be positive")

        items = getattr(pattern, "rounds", []) or getattr(pattern, "rows", [])

        if not items:
            raise ValueError("pattern has no rows or rounds")

        max_stitches = max(
            int(getattr(item, "computed_stitch_count", 0))
            for item in items
        )

        round_count = len(items)

        # Base dimensions from gauge.
        base_width = max_stitches / gauge_stitches_per_10cm * 10.0
        base_height = round_count / gauge_rows_per_10cm * 10.0

        rng = random.Random(self.seed)
        widths: list[float] = []
        heights: list[float] = []
        passed = 0

        for _ in range(self.simulations):
            tension = rng.uniform(
                1.0 - tension_variation_percent / 100.0,
                1.0 + tension_variation_percent / 100.0,
            )

            width = base_width * tension
            height = base_height * tension

            widths.append(width)
            heights.append(height)

            width_error = abs(width - base_width) / base_width * 100
            height_error = abs(height - base_height) / base_height * 100

            if (
                width_error <= tolerance_percent
                and height_error <= tolerance_percent
            ):
                passed += 1

        return SimulationResult(
            simulations=self.simulations,
            expected_width_cm=round(sum(widths) / len(widths), 3),
            minimum_width_cm=round(min(widths), 3),
            maximum_width_cm=round(max(widths), 3),
            expected_height_cm=round(sum(heights) / len(heights), 3),
            minimum_height_cm=round(min(heights), 3),
            maximum_height_cm=round(max(heights), 3),
            pass_probability=round(
                passed / self.simulations,
                4,
            ),
            tolerance_percent=tolerance_percent,
            seed=self.seed,
        )
