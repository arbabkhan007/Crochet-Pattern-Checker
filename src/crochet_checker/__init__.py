"""Crochet Pattern Checker - Verification, Visualization & PDF Publishing Engine."""
__version__ = "0.1.0"

# Priority 1 Enhancements
from .library import PatternLibrary, SavedPattern
from .marketplace import EtsyListingGenerator, RavelryExportGenerator
from .ai_enhanced import analyze_difficulty

# Priority 2 Enhancements
from .testing import PatternTestingSystem, Tester, TestCall, Feedback
from .yarn import YarnSubstitutionEngine, YarnProperties
from .pricing import CostCalculator, PricingStrategy
