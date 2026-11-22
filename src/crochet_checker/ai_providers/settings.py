"""Configuration for multi-provider review and fail-closed delivery gating."""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from math import ceil
from typing import Mapping

CORE_REQUIRED_ROLES = ("stitch_arithmetic", "construction_assembly")


def _bool_value(value: str | None, default: bool) -> bool:
    if value is None or not value.strip():
        return default
    return value.strip().casefold() in {"1", "true", "yes", "on"}


def _int_value(value: str | None, default: int, minimum: int = 0) -> int:
    try:
        return max(minimum, int(value)) if value is not None else default
    except (TypeError, ValueError):
        return default


def _float_value(
    value: str | None, default: float, minimum: float, maximum: float
) -> float:
    try:
        result = float(value) if value is not None else default
    except (TypeError, ValueError):
        return default
    if not math.isfinite(result):
        return default
    return min(maximum, max(minimum, result))


@dataclass(frozen=True)
class ConsensusSettings:
    min_participating_models: int = 2
    min_participation_ratio: float = 1.0
    consensus_threshold: float = 0.67
    max_concurrency: int = 8
    enable_cross_examination: bool = True
    enable_adversarial_review: bool = True
    strict_required_participation: bool = True
    max_revisions: int = 3
    required_roles: tuple[str, ...] = ("stitch_arithmetic", "construction_assembly")

    def __post_init__(self) -> None:
        if not 1 <= self.min_participating_models <= 32:
            raise ValueError("min_participating_models must be between 1 and 32")
        if (
            not math.isfinite(self.min_participation_ratio)
            or not 0.0 <= self.min_participation_ratio <= 1.0
        ):
            raise ValueError("min_participation_ratio must be between 0 and 1")
        if (
            not math.isfinite(self.consensus_threshold)
            or not 0.5 <= self.consensus_threshold <= 1.0
        ):
            raise ValueError("consensus_threshold must be between 0.5 and 1")
        if not 1 <= self.max_concurrency <= 32:
            raise ValueError("max_concurrency must be between 1 and 32")
        if not 0 <= self.max_revisions <= 10:
            raise ValueError("max_revisions must be between 0 and 10")
        if any(not role.strip() for role in self.required_roles):
            raise ValueError("required_roles must not contain blank values")
        if not set(CORE_REQUIRED_ROLES).issubset(self.required_roles):
            raise ValueError(
                "required_roles must include stitch_arithmetic and construction_assembly"
            )
        if not self.strict_required_participation:
            raise ValueError(
                "strict required-provider participation cannot be disabled"
            )

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "ConsensusSettings":
        source = os.environ if env is None else env
        roles_raw = source.get(
            "CROCHET_REQUIRED_REVIEW_ROLES",
            "stitch_arithmetic,construction_assembly",
        )
        roles = tuple(item.strip() for item in roles_raw.split(",") if item.strip())
        return cls(
            min_participating_models=min(
                32, _int_value(source.get("CROCHET_CONSENSUS_MIN_MODELS"), 2, 1)
            ),
            min_participation_ratio=_float_value(
                source.get("CROCHET_CONSENSUS_MIN_PARTICIPATION_RATIO"), 1.0, 0.0, 1.0
            ),
            consensus_threshold=_float_value(
                source.get("CROCHET_CONSENSUS_THRESHOLD"), 0.67, 0.5, 1.0
            ),
            max_concurrency=min(
                32, _int_value(source.get("CROCHET_CONSENSUS_MAX_CONCURRENCY"), 8, 1)
            ),
            enable_cross_examination=_bool_value(
                source.get("CROCHET_CONSENSUS_CROSS_EXAMINATION"), True
            ),
            enable_adversarial_review=_bool_value(
                source.get("CROCHET_CONSENSUS_ADVERSARIAL_REVIEW"), True
            ),
            strict_required_participation=_bool_value(
                source.get("CROCHET_CONSENSUS_STRICT_PARTICIPATION"), True
            ),
            max_revisions=min(
                10, _int_value(source.get("CROCHET_CONSENSUS_MAX_REVISIONS"), 3)
            ),
            required_roles=roles,
        )

    def required_participant_target(self, required_model_count: int) -> int:
        return max(
            self.min_participating_models,
            ceil(required_model_count * self.min_participation_ratio),
        )
