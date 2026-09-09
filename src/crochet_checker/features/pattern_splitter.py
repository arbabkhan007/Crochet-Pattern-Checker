"""Pattern Splitter - Detect and split multiple patterns from one file"""

import re
from typing import List
from dataclasses import dataclass

@dataclass
class SplitPattern:
    pattern_id: str
    title: str
    content: str
    start_line: int
    end_line: int
    confidence: float

class PatternSplitter:
    """Detect and split multiple patterns from a single file"""
    
    def __init__(self):
        self.pattern_markers = [
            r'^#{1,3}\s+\d+\.',
            r'^#{1,3}\s+[A-Z][a-z]+',
            r'^Pattern\s+\d+:',
            r'^\*{2}Pattern\s+\d+',
        ]
    
    def split_patterns(self, content: str) -> List[SplitPattern]:
        """Split content into multiple patterns"""
        lines = content.split('\n')
        patterns = []
        current_pattern_lines = []
        current_title = ""
        start_line = 0
        
        for i, line in enumerate(lines):
            is_new_pattern = self._is_pattern_start(line)
            
            if is_new_pattern and current_pattern_lines:
                if len(current_pattern_lines) > 5:
                    patterns.append(SplitPattern(
                        pattern_id=f"pattern_{len(patterns) + 1}",
                        title=current_title or f"Pattern {len(patterns) + 1}",
                        content='\n'.join(current_pattern_lines),
                        start_line=start_line,
                        end_line=i - 1,
                        confidence=self._calculate_confidence(current_pattern_lines)
                    ))
                
                current_pattern_lines = [line]
                current_title = self._extract_title(line)
                start_line = i
            else:
                current_pattern_lines.append(line)
                if not current_title and i < 10:
                    current_title = self._extract_title(line)
        
        if current_pattern_lines and len(current_pattern_lines) > 5:
            patterns.append(SplitPattern(
                pattern_id=f"pattern_{len(patterns) + 1}",
                title=current_title or f"Pattern {len(patterns) + 1}",
                content='\n'.join(current_pattern_lines),
                start_line=start_line,
                end_line=len(lines) - 1,
                confidence=self._calculate_confidence(current_pattern_lines)
            ))
        
        return patterns
    
    def _is_pattern_start(self, line: str) -> bool:
        """Check if a line marks the start of a new pattern"""
        line_stripped = line.strip()
        for marker in self.pattern_markers:
            if re.match(marker, line_stripped):
                return True
        if re.match(r'^\d+\.\s+[A-Z]', line_stripped):
            return True
        return False
    
    def _extract_title(self, line: str) -> str:
        """Extract pattern title from a line"""
        title = re.sub(r'^#+\s*', '', line)
        title = re.sub(r'^\*+\s*', '', title)
        title = re.sub(r'^\d+\.\s*', '', title)
        return title.strip()
    
    def _calculate_confidence(self, lines: List[str]) -> float:
        """Calculate confidence that this is a valid pattern"""
        content = '\n'.join(lines)
        score = 0.0
        
        if re.search(r'round\s+\d+|rnd\s+\d+|r\s+\d+', content.lower()):
            score += 0.3
        if re.search(r'\d+\s+sc|\d+\s+dc|\d+\s+hdc', content.lower()):
            score += 0.3
        if 'magic ring' in content.lower() or 'mr' in content.lower():
            score += 0.2
        if len(lines) > 20:
            score += 0.2
        
        return min(1.0, score)

def split_pattern_file(content: str) -> List[SplitPattern]:
    """Split a pattern file into multiple patterns"""
    splitter = PatternSplitter()
    return splitter.split_patterns(content)

def format_split_results(patterns: List[SplitPattern]) -> str:
    """Format split results for display"""
    if not patterns:
        return "No patterns detected."
    
    output = [
        f"🔍 Pattern Splitter Results",
        "=" * 40,
        f"Detected {len(patterns)} pattern(s)\n"
    ]
    
    for i, pattern in enumerate(patterns, 1):
        output.append(f"{i}. {pattern.title}")
        output.append(f"   Lines: {pattern.start_line}-{pattern.end_line}")
        output.append(f"   Confidence: {pattern.confidence*100:.0f}%")
        output.append(f"   Length: {len(pattern.content.split(chr(10)))} lines")
        output.append("")
    
    return "\n".join(output)
