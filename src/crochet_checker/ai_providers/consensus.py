"""Multi-model AI consensus checking for crochet patterns."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .provider import AIConfig, AIProvider


@dataclass
class AIClaim:
    provider: str
    claim: str
    confidence: float = 0.0
    verified: bool = False


@dataclass
class ConsensusReport:
    compiler_valid: bool
    compiler_errors: list[str] = field(default_factory=list)
    claims: list[AIClaim] = field(default_factory=list)
    disagreements: list[str] = field(default_factory=list)
    recommendation: str = ""

    @property
    def is_consistent(self) -> bool:
        return not self.disagreements

    def to_dict(self) -> dict[str, Any]:
        return {
            "compiler_valid": self.compiler_valid,
            "compiler_errors": self.compiler_errors,
            "claims": [
                {
                    "provider": claim.provider,
                    "claim": claim.claim,
                    "confidence": claim.confidence,
                    "verified": claim.verified,
                }
                for claim in self.claims
            ],
            "disagreements": self.disagreements,
            "recommendation": self.recommendation,
        }


class AIConsensusChecker:
    """
    Compare independent AI opinions against deterministic validation.

    The compiler remains authoritative. AI output is advisory only.
    """

    def __init__(
        self,
        openai_config: AIConfig | None = None,
        gemini_config: AIConfig | None = None,
    ):
        self.openai = AIProvider(
            openai_config
            or AIConfig(provider="openai", model="gpt-4o-mini")
        )
        self.gemini = AIProvider(
            gemini_config
            or AIConfig(provider="gemini", model="gemini-1.5-flash")
        )

    def compare(self, pattern, report) -> ConsensusReport:
        compiler_errors = [
            getattr(error, "message", str(error))
            for error in getattr(report, "errors", [])
        ]

        claims: list[AIClaim] = []
        disagreements: list[str] = []

        provider_results = []

        for name, provider in (
            ("openai", self.openai),
            ("gemini", self.gemini),
        ):
            try:
                response = provider.explain_pattern(pattern, report)
                claim = AIClaim(
                    provider=name,
                    claim=response,
                    confidence=0.5,
                    verified=False,
                )
                claims.append(claim)
                provider_results.append((name, response))
            except Exception as exc:
                disagreements.append(
                    f"{name} provider unavailable: {type(exc).__name__}: {exc}"
                )

        if len(provider_results) == 2:
            left = provider_results[0][1].strip()
            right = provider_results[1][1].strip()

            if left != right:
                disagreements.append(
                    "ChatGPT and Gemini returned different explanations. "
                    "Use compiler findings as the authoritative result."
                )

        if compiler_errors:
            recommendation = (
                "Resolve deterministic compiler errors first. "
                "AI explanations are advisory and must not override "
                "compiler stitch counts."
            )
        elif disagreements:
            recommendation = (
                "The pattern passed deterministic validation, but AI opinions "
                "differ. Review the exact round counts manually."
            )
        else:
            recommendation = (
                "The pattern passed deterministic validation and AI responses "
                "did not produce a detected disagreement."
            )

        return ConsensusReport(
            compiler_valid=getattr(report, "valid", False),
            compiler_errors=compiler_errors,
            claims=claims,
            disagreements=disagreements,
            recommendation=recommendation,
        )
