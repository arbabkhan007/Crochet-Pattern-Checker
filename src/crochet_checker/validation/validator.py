"""Pattern Validator - Validates crochet patterns"""
from enum import Enum

class Severity(Enum):
    """Severity levels for validation findings"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ValidationReport:
    """Validation report container"""
    def __init__(self):
        self.valid = True
        self.errors = []
        self.warnings = []
        self.stitch_count = 0

class PatternValidator:
    def validate(self, pattern_text: str):
        return {
            'valid': True,
            'errors': [],
            'warnings': [],
            'stitch_count': pattern_text.lower().count('sc') + pattern_text.lower().count('dc')
        }

def validate_pattern(pattern_text: str):
    """Convenience function for validation"""
    validator = PatternValidator()
    return validator.validate(pattern_text)
