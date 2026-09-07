"""Validation system for crochet patterns."""
from .validator import (
    OverallStatus,
    Severity,
    StitchCountReport,
    StitchCountValidator,
    ValidationFinding,
    ValidationPipeline,
    ValidationReport,
    validate_pattern,
    validate_stitch_counts,
)
from .multipiece import MultiPieceDetector, detect_and_validate_multipiece

# Try to import abbreviations (may have issues)
try:
    from .abbreviations import AbbreviationValidator, validate_abbreviations
except Exception:  # pragma: no cover - optional validator
    pass

__all__ = [
    "validate_pattern",
    "ValidationReport",
    "ValidationFinding",
    "ValidationPipeline",
    "StitchCountReport",
    "StitchCountValidator",
    "validate_stitch_counts",
    "OverallStatus",
    "Severity",
    "MultiPieceDetector",
    "detect_and_validate_multipiece",
]
