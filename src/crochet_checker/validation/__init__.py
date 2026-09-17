"""Validation system for crochet patterns."""
from .validator import (
    validate_pattern,
    ValidationReport,
    Severity,
    ValidationFinding,
    OverallStatus,
)
from .multipiece import MultiPieceDetector, detect_and_validate_multipiece

# Try to import abbreviations (may have issues)
try:
    from .abbreviations import AbbreviationValidator, validate_abbreviations
except:
    pass

__all__ = [
    "validate_pattern",
    "OverallStatus",
    "ValidationReport",
    "Severity",
    "ValidationFinding",
    "MultiPieceDetector",
    "detect_and_validate_multipiece",
]
