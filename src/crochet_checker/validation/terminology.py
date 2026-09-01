"""Terminology validation - detects US vs UK term mix-ups."""
from typing import Optional

class TerminologyValidator:
    US_TO_UK = {'sc': 'dc', 'hdc': 'htr', 'dc': 'tr', 'tr': 'dtr'}
    UK_TO_US = {v: k for k, v in US_TO_UK.items() if k != v}
    US_ONLY_TERMS = {'sc', 'hdc'}
    UK_ONLY_TERMS = {'dc', 'htr'}
    
    def __init__(self, declared_system: Optional[str] = None):
        self.declared_system = declared_system
        self.detected_system = None
        self.us_count = 0
        self.uk_count = 0
    
    def validate_pattern(self, pattern) -> list[dict]:
        issues = []
        if not self.declared_system:
            self.detected_system = self._detect_system(pattern)
        else:
            self.detected_system = self.declared_system.upper()
        
        items = pattern.rounds or pattern.rows
        for item in items:
            round_num = item.round_number if hasattr(item, 'round_number') else item.row_number
            for instruction in item.instructions:
                if hasattr(instruction, 'source_text'):
                    text_lower = instruction.source_text.lower()
                    if self.detected_system == 'US':
                        for uk_term in self.UK_ONLY_TERMS:
                            if uk_term in text_lower:
                                self.uk_count += 1
                                us_equiv = self.UK_TO_US.get(uk_term, uk_term)
                                issues.append({
                                    'type': 'terminology_mismatch',
                                    'round': round_num,
                                    'severity': 'warning',
                                    'message': f"UK term '{uk_term}' found in US pattern",
                                    'suggestion': f"Use '{us_equiv}' instead (US term)"
                                })
        return issues
    
    def _detect_system(self, pattern) -> str:
        items = pattern.rounds or pattern.rows
        for item in items:
            for instruction in item.instructions:
                if hasattr(instruction, 'source_text'):
                    text = instruction.source_text.lower()
                    for term in self.US_ONLY_TERMS:
                        if term in text:
                            self.us_count += 1
                    for term in self.UK_ONLY_TERMS:
                        if term in text:
                            self.uk_count += 1
        return 'US' if self.us_count >= self.uk_count else 'UK'

def validate_terminology(pattern) -> list[dict]:
    validator = TerminologyValidator()
    return validator.validate_pattern(pattern)
