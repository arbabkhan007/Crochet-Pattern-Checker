"""Automatic Error Correction"""

import re
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Correction:
    line_number: int
    original: str
    corrected: str
    error_type: str
    confidence: float
    explanation: str

def detect_common_errors(pattern_text: str) -> List[Correction]:
    corrections = []
    lines = pattern_text.splitlines()
    
    typos = {'magick': 'magic', 'singel': 'single', 'doulbe': 'double'}
    
    for i, line in enumerate(lines, 1):
        for typo, correct in typos.items():
            if typo in line.lower():
                corrected_line = re.sub(re.escape(typo), correct, line, flags=re.IGNORECASE)
                corrections.append(Correction(
                    line_number=i,
                    original=line,
                    corrected=corrected_line,
                    error_type='typo',
                    confidence=0.9,
                    explanation=f"Typo: '{typo}' should be '{correct}'"
                ))
        
        if line.count('(') != line.count(')'):
            if line.count('(') > line.count(')'):
                corrections.append(Correction(
                    line_number=i,
                    original=line,
                    corrected=line + ')' * (line.count('(') - line.count(')')),
                    error_type='parentheses',
                    confidence=0.7,
                    explanation=f"Missing {line.count('(') - line.count(')')} closing parenthesis"
                ))
    
    return corrections

def auto_correct_pattern(pattern_text: str) -> Tuple[str, List[Correction]]:
    corrections = detect_common_errors(pattern_text)
    corrections.sort(key=lambda c: c.line_number, reverse=True)
    
    lines = pattern_text.splitlines()
    for correction in corrections:
        if correction.confidence >= 0.8:
            lines[correction.line_number - 1] = correction.corrected
    
    return '\n'.join(lines), corrections

def format_corrections(corrections: List[Correction]) -> str:
    if not corrections:
        return "✅ No errors detected!"
    
    output = [f"🔧 Found {len(corrections)} potential error(s)\n{'=' * 40}\n"]
    
    for i, correction in enumerate(corrections, 1):
        output.append(f"{i}. Line {correction.line_number} ({correction.error_type})")
        output.append(f"   Original: {correction.original}")
        output.append(f"   Corrected: {correction.corrected}")
        output.append(f"   Confidence: {correction.confidence*100:.0f}%")
        output.append(f"   {correction.explanation}\n")
    
    return "\n".join(output)
