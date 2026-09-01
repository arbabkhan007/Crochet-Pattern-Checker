"""Abbreviation validation - detects invalid stitch abbreviations."""
from typing import Optional
from ..model.stitch import STITCH_PRODUCTION, ABBREVIATION_MAP

class AbbreviationValidator:
    VALID_ABBREVIATIONS = {
        'ch', 'sl st', 'sc', 'hdc', 'dc', 'tr', 'dtr',
        'inc', 'dec', 'invdec', 'sc2tog', 'dc2tog', 'hdc2tog',
        'mr', 'magic ring', 'sk', 'sp', 'sts', 'st',
        'yo', 'yr', 'turn', 'beg', 'end', 'rep',
    }
    VALID_ABBREVIATIONS.update(STITCH_PRODUCTION.keys())
    VALID_ABBREVIATIONS.update(ABBREVIATION_MAP.keys())
    
    def validate_instruction_text(self, text: str, round_number: int) -> list[dict]:
        issues = []
        import re
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        skip_words = {'in', 'each', 'around', 'next', 'first', 'last', 'same', 'skip', 'space', 'stitch', 'stitches', 'make', 'times', 'repeat', 'from', 'to'}
        
        for word in words:
            word_lower = word.lower().strip('.,()[]')
            if word_lower.isdigit() or word_lower in skip_words:
                continue
            if word_lower not in self.VALID_ABBREVIATIONS:
                issues.append({
                    'type': 'invalid_abbreviation',
                    'round': round_number,
                    'abbreviation': word,
                    'message': f"Unknown abbreviation '{word}'",
                    'severity': 'error'
                })
        return issues

def validate_abbreviations(pattern) -> list[dict]:
    validator = AbbreviationValidator()
    all_issues = []
    items = pattern.rounds or pattern.rows
    for item in items:
        round_num = item.round_number if hasattr(item, 'round_number') else item.row_number
        for instruction in item.instructions:
            if hasattr(instruction, 'source_text'):
                issues = validator.validate_instruction_text(instruction.source_text, round_num)
                all_issues.extend(issues)
    return all_issues
