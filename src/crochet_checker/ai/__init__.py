"""AI Assistance package."""
from .explainer import PatternExplainer, explain_pattern, ExplanationResult
from .terminology import TerminologyTranslator, translate_pattern, US_TO_UK, UK_TO_US
from .suggestions import SuggestionEngine, generate_suggestions, Suggestion
from .description import DescriptionGenerator, generate_description, PatternDescription
