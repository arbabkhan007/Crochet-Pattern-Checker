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

# Bulk management features
from .bulk_importer import BulkPatternImporter, format_import_results
from .pattern_splitter import PatternSplitter, split_pattern_file, format_split_results
from .pattern_collection import PatternCollectionManager, PatternCollection, format_collections
from .pattern_library_manager import EnhancedPatternLibrary, Pattern, format_pattern_list, format_library_stats

__all__.extend([
    'BulkPatternImporter', 'format_import_results',
    'PatternSplitter', 'split_pattern_file', 'format_split_results',
    'PatternCollectionManager', 'PatternCollection', 'format_collections',
    'EnhancedPatternLibrary', 'Pattern', 'format_pattern_list', 'format_library_stats',
])


# Additional advanced features
from .pattern_analytics import PatternAnalyticsEngine, generate_analytics_report, format_analytics
from .pattern_version_control import PatternVersionControl, format_version_history
from .pattern_templates import PatternTemplateLibrary, format_template_list
from .pattern_export import PatternExporter, export_pattern_to_file
from .pattern_comparison import PatternComparator, compare_patterns, format_comparison

__all__.extend([
    'PatternAnalyticsEngine', 'generate_analytics_report', 'format_analytics',
    'PatternVersionControl', 'format_version_history',
    'PatternTemplateLibrary', 'format_template_list',
    'PatternExporter', 'export_pattern_to_file',
    'PatternComparator', 'compare_patterns', 'format_comparison',
])
