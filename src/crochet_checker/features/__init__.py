"""Advanced Features for Crochet Pattern Checker"""

from .pattern_translator import translate_pattern, detect_term_system
from .yarn_calculator import estimate_yarn, format_yarn_estimate
from .size_scaler import scale_pattern, format_scale_info
from .gauge_calculator import calculate_gauge, format_gauge_info
from .pattern_diff import diff_patterns, format_diff_result
from .pattern_search import PatternSearchEngine, format_search_results
from .error_correction import auto_correct_pattern, format_corrections

__all__ = [
    'translate_pattern', 'detect_term_system',
    'estimate_yarn', 'format_yarn_estimate',
    'scale_pattern', 'format_scale_info',
    'calculate_gauge', 'format_gauge_info',
    'diff_patterns', 'format_diff_result',
    'PatternSearchEngine', 'format_search_results',
    'auto_correct_pattern', 'format_corrections',
]
