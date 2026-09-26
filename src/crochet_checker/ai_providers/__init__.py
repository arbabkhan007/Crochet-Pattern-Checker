"""Multi-provider AI assistance."""

from .provider import AIConfig, AIProvider

from .consensus import AIClaim, AIConsensusChecker, ConsensusReport

__all__ = [
    "AIClaim",
    "AIConsensusChecker",
    "ConsensusReport",
]

from .quality import (
    AIClaim,
    AIQualityChecker,
    AIQualityReport,
    RepairProposal,
    quality_check,
)
