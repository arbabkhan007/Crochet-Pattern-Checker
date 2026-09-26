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

from .validator import PatternValidator, ValidationResult, ValidationError
from .reporter import PatternReporter
from .exhaustion import OrphanedStitchAnalyzer, ExhaustionReport, OrphanedStitchError
from .corners import CornerSequenceValidator, CornerMismatchError
from .chains import TurningChainRulesEngine, ChainAllocation
from .assembly import AssemblyGraphValidator, AssemblyError

__all__ = [
    # Core pipeline
    'PatternValidator',
    'ValidationResult',
    'ValidationError',
    'PatternReporter',
    # Exhaustion
    'OrphanedStitchAnalyzer',
    'ExhaustionReport',
    'OrphanedStitchError',
    # Corners
    'CornerSequenceValidator',
    'CornerMismatchError',
    # Chains
    'TurningChainRulesEngine',
    'ChainAllocation',
    # Assembly
    'AssemblyGraphValidator',
    'AssemblyError',
]


# Legacy compatibility exports used by the original test suite.
from enum import Enum as _Enum

from .validator import (
    validate_pattern,
    ValidationReport,
    Severity as CompilerSeverity,
)

try:
    from .stitch_counts import (
        validate_stitch_counts,
        StitchCountReport,
    )
except ImportError:
    validate_stitch_counts = None
    StitchCountReport = None


class OverallStatus(_Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    ERROR = "error"


__all__.extend([
    "validate_pattern",
    "ValidationReport",
    "CompilerSeverity",
    "OverallStatus",
    "validate_stitch_counts",
    "StitchCountReport",
])

from .stitch_counts import ValidationFinding

__all__.append("ValidationFinding")
