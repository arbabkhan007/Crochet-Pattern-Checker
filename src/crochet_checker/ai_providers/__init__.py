"""Advisory AI helpers plus the optional hosted multi-provider review platform."""

from .provider import AIConfig, AIProvider
from .consensus import AIConsensusChecker, ConsensusReport
from .quality import AIClaim, AIQualityChecker, AIQualityReport, RepairProposal, quality_check
from .history import ConsensusHistoryStore
from .orchestrator import ConsensusRunner
from .provider_adapters import AnthropicAdapter, GoogleAdapter, OpenAICompatibleAdapter, ProviderAdapter, ProviderAvailability, ProviderCatalog, ProviderConfig, ProviderRequestError, ProviderResponse, create_adapter, supported_provider_ids
from .service import ConsensusService, RevisionLimitError
from .settings import ConsensusSettings

__all__ = [
    "AIClaim", "AIConfig", "AIConsensusChecker", "AIProvider", "AIQualityChecker", "AIQualityReport",
    "AnthropicAdapter", "ConsensusHistoryStore", "ConsensusReport", "ConsensusRunner", "ConsensusService",
    "ConsensusSettings", "GoogleAdapter", "OpenAICompatibleAdapter", "ProviderAdapter", "ProviderAvailability",
    "ProviderCatalog", "ProviderConfig", "ProviderRequestError", "ProviderResponse", "RepairProposal",
    "RevisionLimitError", "create_adapter", "quality_check", "supported_provider_ids",
]
