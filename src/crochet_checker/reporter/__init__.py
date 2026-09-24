"""
Reporter package - Reporting & diagnostic tools

Per 4-pattern audit:
- UnsupportedSyntaxFallback -> explicit warnings instead of silent fallbacks
- DiffPatchGenerator        -> minimal pattern rewrite suggestions
"""

from .fallback import (
    UnsupportedSyntaxFallback,
    CountResult,
    FallbackWarning,
    TrustLevel,
)
from .patcher import DiffPatchGenerator, Patch, PatchReport

__all__ = [
    'UnsupportedSyntaxFallback',
    'CountResult',
    'FallbackWarning',
    'TrustLevel',
    'DiffPatchGenerator',
    'Patch',
    'PatchReport',
]
