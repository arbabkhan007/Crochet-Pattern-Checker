"""Multi-model AI consensus checking for crochet patterns."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
    Record the compiler result. A hosted chat is not called.
    """

    def __init__(
        self,
        openai_config: object | None = None,
        gemini_config: object | None = None,
    ):
        del openai_config, gemini_config

    def compare(self, pattern, report) -> ConsensusReport:
        del pattern
        compiler_errors = [
            getattr(error, "message", str(error))
            for error in getattr(report, "errors", [])
        ]
        disagreements = [
            "Hosted chat was not called. The compiler result stands."
        ]
        if compiler_errors:
            recommendation = (
                "Resolve deterministic compiler errors first. "
                "A chat model was not called and cannot override the stitch count."
            )
        else:
            recommendation = (
                "The compiler result stands. A chat model was not called."
            )
        return ConsensusReport(
            compiler_valid=not compiler_errors,
            compiler_errors=compiler_errors,
            claims=[],
            disagreements=disagreements,
            recommendation=recommendation,
        )
