"""Advanced Features for Crochet Pattern Checker"""

from .error_correction import auto_correct_pattern, format_corrections
from .gauge_calculator import calculate_gauge, format_gauge_info
from .pattern_diff import diff_patterns, format_diff_result
from .pattern_search import PatternSearchEngine, format_search_results
from .pattern_translator import detect_term_system, translate_pattern
from .size_scaler import format_scale_info, scale_pattern
from .yarn_calculator import estimate_yarn, format_yarn_estimate

__all__ = [
    "PatternSearchEngine",
    "auto_correct_pattern",
    "calculate_gauge",
    "detect_term_system",
    "diff_patterns",
    "estimate_yarn",
    "format_corrections",
    "format_diff_result",
    "format_gauge_info",
    "format_scale_info",
    "format_search_results",
    "format_yarn_estimate",
    "scale_pattern",
    "translate_pattern",
]

# Bulk management features
from .bulk_importer import BulkPatternImporter, format_import_results
from .pattern_collection import (
    PatternCollection,
    PatternCollectionManager,
    format_collections,
)
from .pattern_library_manager import (
    EnhancedPatternLibrary,
    Pattern,
    format_library_stats,
    format_pattern_list,
)
from .pattern_splitter import PatternSplitter, format_split_results, split_pattern_file

__all__.extend(
    [
        "BulkPatternImporter",
        "EnhancedPatternLibrary",
        "Pattern",
        "PatternCollection",
        "PatternCollectionManager",
        "PatternSplitter",
        "format_collections",
        "format_import_results",
        "format_library_stats",
        "format_pattern_list",
        "format_split_results",
        "split_pattern_file",
    ]
)


# Additional advanced features
from .pattern_analytics import (
    PatternAnalyticsEngine,
    format_analytics,
    generate_analytics_report,
)
from .pattern_comparison import PatternComparator, compare_patterns, format_comparison
from .pattern_export import PatternExporter, export_pattern_to_file
from .pattern_templates import PatternTemplateLibrary, format_template_list
from .pattern_version_control import PatternVersionControl, format_version_history

__all__.extend(
    [
        "PatternAnalyticsEngine",
        "PatternComparator",
        "PatternExporter",
        "PatternTemplateLibrary",
        "PatternVersionControl",
        "compare_patterns",
        "export_pattern_to_file",
        "format_analytics",
        "format_comparison",
        "format_template_list",
        "format_version_history",
        "generate_analytics_report",
    ]
)


# Blender and Browser features
from .blender_integration import (
    BlenderPatternGenerator,
    BlenderPatternVisualizer,
    generate_3d_from_pattern,
    visualize_stitches,
)
from .browser_viewer import (
    BrowserImageViewer,
    BrowserPDFViewer,
    view_image_in_browser,
    view_pdf_in_browser,
)
from .html_generator import HTMLPatternGenerator, generate_interactive_pattern

__all__.extend(
    [
        "BlenderPatternGenerator",
        "BlenderPatternVisualizer",
        "BrowserImageViewer",
        "BrowserPDFViewer",
        "HTMLPatternGenerator",
        "generate_3d_from_pattern",
        "generate_interactive_pattern",
        "view_image_in_browser",
        "view_pdf_in_browser",
        "visualize_stitches",
    ]
)
