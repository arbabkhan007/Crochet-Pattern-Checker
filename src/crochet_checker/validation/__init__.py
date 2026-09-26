"""
Compiler-Grade Validation Package

Provides multi-pass compiler-based validation for crochet patterns:
- Multi-piece & Module AST parsing
- Multi-pass compiler design
- State-machine loop & anchor tracking
- Graph-based assembly validation
- Intermediate representation & syntax warnings

Rules engine (per 4-pattern audit):
- OrphanedStitchAnalyzer    -> exhaustion check per round
- CornerSequenceValidator   -> corner-space queue matching
- TurningChainRulesEngine   -> turning chain count allocation
- AssemblyGraphValidator    -> N neighbor joins + N core joins before closure
"""

from .assembly import AssemblyError, AssemblyGraphValidator
from .chains import ChainAllocation, TurningChainRulesEngine
from .corners import CornerMismatchError, CornerSequenceValidator
from .exhaustion import ExhaustionReport, OrphanedStitchAnalyzer, OrphanedStitchError
from .reporter import PatternReporter
from .validator import PatternValidator, ValidationError, ValidationResult

__all__ = [
    # Core pipeline
    "PatternValidator",
    "ValidationResult",
    "ValidationError",
    "PatternReporter",
    # Exhaustion
    "OrphanedStitchAnalyzer",
    "ExhaustionReport",
    "OrphanedStitchError",
    # Corners
    "CornerSequenceValidator",
    "CornerMismatchError",
    # Chains
    "TurningChainRulesEngine",
    "ChainAllocation",
    # Assembly
    "AssemblyGraphValidator",
    "AssemblyError",
]


# Legacy compatibility exports used by the original test suite.
from enum import Enum as _Enum

from .validator import (
    Severity as CompilerSeverity,
)
from .validator import (
    ValidationReport,
    validate_pattern,
)

try:
    from .stitch_counts import (
        StitchCountReport,
        validate_stitch_counts,
    )
except ImportError:
    validate_stitch_counts = None
    StitchCountReport = None


class OverallStatus(_Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    ERROR = "error"


__all__.extend(
    [
        "CompilerSeverity",
        "OverallStatus",
        "StitchCountReport",
        "ValidationReport",
        "validate_pattern",
        "validate_stitch_counts",
    ]
)

from .stitch_counts import ValidationFinding

__all__.append("ValidationFinding")
