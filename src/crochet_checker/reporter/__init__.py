"""
Reporter package - Reporting & diagnostic tools

Per 4-pattern audit:
- UnsupportedSyntaxFallback -> explicit warnings instead of silent fallbacks
- DiffPatchGenerator        -> minimal pattern rewrite suggestions
"""

from .fallback import (
    CountResult,
    FallbackWarning,
    TrustLevel,
    UnsupportedSyntaxFallback,
)
from .patcher import DiffPatchGenerator, Patch, PatchReport

__all__ = [
    "CountResult",
    "DiffPatchGenerator",
    "FallbackWarning",
    "Patch",
    "PatchReport",
    "TrustLevel",
    "UnsupportedSyntaxFallback",
]
