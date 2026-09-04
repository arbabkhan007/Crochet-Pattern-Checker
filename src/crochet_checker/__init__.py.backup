"""Crochet Pattern Checker - Validate and generate crochet patterns."""

__version__ = "1.0.0"

# Core
from .parser import CrochetParser, parse_pattern
from .validation import validate_pattern
from .pdf import generate_pdf
from .utils import read_pattern_file

# Priority 1
from .library import PatternLibrary, SavedPattern
from .marketplace import EtsyListingGenerator, RavelryExportGenerator
from .ai_enhanced import DifficultyAnalyzer

# Priority 2
from .testing import PatternTestingSystem, Tester, TestCall, Feedback
from .yarn import YarnSubstitutionEngine, YarnProperties
from .pricing import CostCalculator, CostBreakdown, PricingRecommendation

# Priority 3
from .batch import BatchProcessor
from .generator import PatternGenerator
from .api import app

__all__ = [
    # Core
    "CrochetParser", "parse_pattern", "validate_pattern", "generate_pdf", "read_pattern_file",
    # Priority 1
    "PatternLibrary", "SavedPattern",
    "EtsyListingGenerator", "RavelryExportGenerator",
    "DifficultyAnalyzer",
    # Priority 2
    "PatternTestingSystem", "Tester", "TestCall", "Feedback",
    "YarnSubstitutionEngine", "YarnProperties",
    "CostCalculator", "CostBreakdown", "PricingRecommendation",
    # Priority 3
    "BatchProcessor",
    "PatternGenerator",
    "app",
]
