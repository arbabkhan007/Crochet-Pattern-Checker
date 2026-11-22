"""Crochet Pattern Checker - Validate and generate crochet patterns."""

__version__ = "1.0.0"

# Only import core features that definitely work
try:
    from .parser import CrochetParser, parse_pattern

    PARSER_OK = True
except Exception as e:
    print(f"Warning: Parser import failed: {e}")
    PARSER_OK = False

try:
    from .validation import validate_pattern

    VALIDATION_OK = True
except Exception as e:
    print(f"Warning: Validation import failed: {e}")
    VALIDATION_OK = False

try:
    from .pdf import generate_pdf

    PDF_OK = True
except Exception as e:
    print(f"Warning: PDF import failed: {e}")
    PDF_OK = False

try:
    from .utils import read_pattern_file

    UTILS_OK = True
except Exception as e:
    print(f"Warning: Utils import failed: {e}")
    UTILS_OK = False

# Build __all__ dynamically based on what imported successfully
__all__ = []
if PARSER_OK:
    __all__.extend(["CrochetParser", "parse_pattern"])
if VALIDATION_OK:
    __all__.extend(["validate_pattern"])
if PDF_OK:
    __all__.extend(["generate_pdf"])
if UTILS_OK:
    __all__.extend(["read_pattern_file"])

try:
    from .calculators import (
        convert_length,
        convert_terminology,
        estimate_yarn,
        gauge_to_size,
        nearest_hook,
        recommend_hook,
        shape_from_counts,
        stitch_count_chart,
        stitches_for_size,
        wpi_to_weight,
    )
    from .report import build_report, write_report

    CALCULATORS_OK = True
except Exception as e:
    print(f"Warning: Calculator/report import failed: {e}")
    CALCULATORS_OK = False

if CALCULATORS_OK:
    __all__.extend(
        [
            "gauge_to_size",
            "stitches_for_size",
            "estimate_yarn",
            "recommend_hook",
            "nearest_hook",
            "wpi_to_weight",
            "convert_terminology",
            "convert_length",
            "stitch_count_chart",
            "shape_from_counts",
            "build_report",
            "write_report",
        ]
    )
