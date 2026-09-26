"""AI Assistance package."""

from .description import DescriptionGenerator, PatternDescription, generate_description
from .explainer import ExplanationResult, PatternExplainer, explain_pattern
from .suggestions import Suggestion, SuggestionEngine, generate_suggestions
from .terminology import UK_TO_US, US_TO_UK, TerminologyTranslator, translate_pattern
