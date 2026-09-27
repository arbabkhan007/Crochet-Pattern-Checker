"""Yarn profiles and material-substitution analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class YarnProfile:
    name: str
    fiber: str
    elasticity: float
    shrinkage_percent: float
    drape: float
    stitch_definition: float
    confidence: float = 0.8

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SubstitutionResult:
    original: YarnProfile
    replacement: YarnProfile
    width_change_percent: float
    height_change_percent: float
    risk_score: float
    sample_required: bool
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["original"] = self.original.to_dict()
        result["replacement"] = self.replacement.to_dict()
        return result


DEFAULT_YARNS: dict[str, YarnProfile] = {
    "cotton": YarnProfile(
        name="cotton",
        fiber="cotton",
        elasticity=0.15,
        shrinkage_percent=3.0,
        drape=0.45,
        stitch_definition=0.95,
        confidence=0.9,
    ),
    "acrylic": YarnProfile(
        name="acrylic",
        fiber="acrylic",
        elasticity=0.35,
        shrinkage_percent=1.0,
        drape=0.60,
        stitch_definition=0.80,
        confidence=0.9,
    ),
    "wool": YarnProfile(
        name="wool",
        fiber="wool",
        elasticity=0.70,
        shrinkage_percent=8.0,
        drape=0.75,
        stitch_definition=0.75,
        confidence=0.85,
    ),
    "linen": YarnProfile(
        name="linen",
        fiber="linen",
        elasticity=0.10,
        shrinkage_percent=4.0,
        drape=0.35,
        stitch_definition=0.90,
        confidence=0.75,
    ),
    "bamboo": YarnProfile(
        name="bamboo",
        fiber="bamboo",
        elasticity=0.25,
        shrinkage_percent=5.0,
        drape=0.90,
        stitch_definition=0.65,
        confidence=0.75,
    ),
}


class YarnDatabase:
    def __init__(self):
        self.profiles = dict(DEFAULT_YARNS)

    def add(self, profile: YarnProfile) -> None:
        self.profiles[profile.name.lower()] = profile

    def get(self, name: str) -> YarnProfile:
        key = name.lower().strip()

        if key not in self.profiles:
            raise KeyError(
                f"Unknown yarn profile: {name}. "
                f"Available: {', '.join(sorted(self.profiles))}"
            )

        return self.profiles[key]

    def all(self) -> list[YarnProfile]:
        return list(self.profiles.values())


class YarnSubstitutionAnalyzer:
    def __init__(
        self,
        database: YarnDatabase | None = None,
        maximum_safe_change_percent: float = 5.0,
    ):
        self.database = database or YarnDatabase()
        self.maximum_safe_change_percent = maximum_safe_change_percent

    def compare(
        self,
        original: str | YarnProfile,
        replacement: str | YarnProfile,
    ) -> SubstitutionResult:
        original_profile = (
            self.database.get(original)
            if isinstance(original, str)
            else original
        )
        replacement_profile = (
            self.database.get(replacement)
            if isinstance(replacement, str)
            else replacement
        )

        elasticity_delta = (
            replacement_profile.elasticity
            - original_profile.elasticity
        )

        shrinkage_delta = (
            replacement_profile.shrinkage_percent
            - original_profile.shrinkage_percent
        )

        drape_delta = (
            replacement_profile.drape
            - original_profile.drape
        )

        definition_delta = (
            replacement_profile.stitch_definition
            - original_profile.stitch_definition
        )

        width_change = elasticity_delta * 10
        height_change = (
            shrinkage_delta * 0.5
            + drape_delta * 2
        )

        risk = (
            abs(width_change) * 0.35
            + abs(height_change) * 0.25
            + abs(definition_delta) * 20
            + abs(shrinkage_delta) * 0.20
        )

        reasons: list[str] = []

        if abs(elasticity_delta) > 0.20:
            reasons.append(
                "Elasticity differs significantly."
            )

        if abs(shrinkage_delta) > 3:
            reasons.append(
                "Expected shrinkage differs significantly."
            )

        if abs(drape_delta) > 0.25:
            reasons.append(
                "Fabric drape differs significantly."
            )

        if abs(definition_delta) > 0.20:
            reasons.append(
                "Stitch definition differs significantly."
            )

        if not reasons:
            reasons.append(
                "Material properties are within the configured risk range."
            )

        return SubstitutionResult(
            original=original_profile,
            replacement=replacement_profile,
            width_change_percent=round(width_change, 3),
            height_change_percent=round(height_change, 3),
            risk_score=round(min(100.0, risk), 3),
            sample_required=risk > self.maximum_safe_change_percent,
            reasons=reasons,
        )
