"""
Terminology validation - detects US vs UK term mix-ups.
"""

from typing import Optional


class TerminologyValidator:
    """Validates crochet terminology consistency (US vs UK)."""
    
    # US to UK term mappings
    US_TO_UK = {
        'sc': 'dc',           # single crochet -> double crochet
        'hdc': 'htr',         # half double crochet -> half treble
        'dc': 'tr',           # double crochet -> treble
        'tr': 'dtr',          # treble -> double treble
        'dtr': 'trtr',        # double treble -> triple treble
        'sl st': 'ss',        # slip stitch -> slip stitch (same)
        'inc': 'inc',         # increase (same)
        'dec': 'dec',         # decrease (same)
        'sc2tog': 'dc2tog',   # single crochet 2 together -> dc 2 together
        'hdc2tog': 'htr2tog', # half double crochet 2 together -> htr 2 together
        'dc2tog': 'tr2tog',   # double crochet 2 together -> tr 2 together
    }
    
    # UK to US term mappings (reverse)
    UK_TO_US = {v: k for k, v in US_TO_UK.items() if k != v}
    
    # US-specific terms (not used in UK)
    US_ONLY_TERMS = {'sc', 'hdc', 'dc2tog', 'hdc2tog', 'sc2tog'}
    
    # UK-specific terms (not used in US)
    UK_ONLY_TERMS = {'dc', 'htr', 'tr2tog', 'htr2tog', 'dc2tog'}
    
    def __init__(self, declared_system: Optional[str] = None):
        """
        Initialize validator.
        
        Args:
            declared_system: 'US', 'UK', or None (auto-detect)
        """
        self.declared_system = declared_system
        self.detected_system = None
        self.warnings = []
        self.errors = []
        self.us_count = 0
        self.uk_count = 0
    
    def validate_pattern(self, pattern) -> list[dict]:
        """
        Validate terminology consistency across entire pattern.
        
        Returns list of issues found.
        """
        issues = []
        
        # Auto-detect system if not declared
        if not self.declared_system:
            self.detected_system = self._detect_system(pattern)
        else:
            self.detected_system = self.declared_system.upper()
        
        # Check each round/row
        items = pattern.rounds or pattern.rows
        for item in items:
            round_num = item.round_number if hasattr(item, 'round_number') else item.row_number
            
            for instruction in item.instructions:
                if hasattr(instruction, 'source_text'):
                    round_issues = self._validate_instruction(
                        instruction.source_text,
                        round_num
                    )
                    issues.extend(round_issues)
        
        # Add system detection warning if mixed
        if self.us_count > 0 and self.uk_count > 0:
            issues.append({
                'type': 'mixed_terminology',
                'severity': 'error',
                'message': f'Pattern uses both US terms ({self.us_count}) and UK terms ({self.uk_count})',
                'suggestion': 'Use only US or UK terminology consistently'
            })
        
        return issues
    
    def _detect_system(self, pattern) -> str:
        """Auto-detect whether pattern uses US or UK terms."""
        items = pattern.rounds or pattern.rows
        
        for item in items:
            for instruction in item.instructions:
                if hasattr(instruction, 'source_text'):
                    text = instruction.source_text.lower()
                    
                    # Check for US-specific terms
                    for term in self.US_ONLY_TERMS:
                        if term in text:
                            self.us_count += 1
                    
                    # Check for UK-specific terms
                    for term in self.UK_ONLY_TERMS:
                        if term in text:
                            self.uk_count += 1
        
        # Determine system based on counts
        if self.us_count > self.uk_count:
            return 'US'
        elif self.uk_count > self.us_count:
            return 'UK'
        else:
            return 'US'  # Default to US
    
    def _validate_instruction(self, text: str, round_number: int) -> list[dict]:
        """Validate terminology in a single instruction."""
        issues = []
        text_lower = text.lower()
        
        # Check for US terms when UK is declared
        if self.detected_system == 'UK':
            for us_term in self.US_ONLY_TERMS:
                if us_term in text_lower:
                    uk_equivalent = self.US_TO_UK.get(us_term, us_term)
                    issues.append({
                        'type': 'terminology_mismatch',
                        'round': round_number,
                        'severity': 'warning',
                        'message': f"US term '{us_term}' found in UK pattern",
                        'suggestion': f"Use '{uk_equivalent}' instead (UK term)"
                    })
        
        # Check for UK terms when US is declared
        elif self.detected_system == 'US':
            for uk_term in self.UK_ONLY_TERMS:
                if uk_term in text_lower:
                    # Avoid false positives (e.g., "dc" in "sc2tog")
                    if self._is_actual_term(text_lower, uk_term):
                        us_equivalent = self.UK_TO_US.get(uk_term, uk_term)
                        issues.append({
                            'type': 'terminology_mismatch',
                            'round': round_number,
                            'severity': 'warning',
                            'message': f"UK term '{uk_term}' found in US pattern",
                            'suggestion': f"Use '{us_equivalent}' instead (US term)"
                        })
        
        return issues
    
    def _is_actual_term(self, text: str, term: str) -> bool:
        """Check if term is actually used (not part of another word)."""
        import re
        # Use word boundaries to avoid false positives
        pattern = r'\b' + re.escape(term) + r'\b'
        return bool(re.search(pattern, text))
    
    def get_system_info(self) -> dict:
        """Get information about detected terminology system."""
        return {
            'declared': self.declared_system,
            'detected': self.detected_system,
            'us_terms': self.us_count,
            'uk_terms': self.uk_count,
            'consistent': self.us_count == 0 or self.uk_count == 0
        }


def validate_terminology(pattern) -> list[dict]:
    """
    Validate terminology consistency in a pattern.
    
    Args:
        pattern: Pattern object to validate
    
    Returns:
        List of issues found
    """
    # Check if pattern declares terminology system
    declared_system = None
    if hasattr(pattern, 'metadata') and hasattr(pattern.metadata, 'notes'):
        for note in pattern.metadata.notes:
            note_lower = note.lower()
            if 'us terms' in note_lower or 'us terminology' in note_lower:
                declared_system = 'US'
                break
            elif 'uk terms' in note_lower or 'uk terminology' in note_lower:
                declared_system = 'UK'
                break
    
    validator = TerminologyValidator(declared_system)
    return validator.validate_pattern(pattern)
