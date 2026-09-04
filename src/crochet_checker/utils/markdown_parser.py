"""Enhanced markdown parser for crochet patterns."""
import re
from pathlib import Path
from typing import List, Dict

class MarkdownPatternParser:
    """Parse markdown files to extract crochet patterns."""
    
    def __init__(self):
        self.sections = {}
        self.pattern_text = []
    
    def parse_file(self, file_path: str) -> Dict:
        """Parse a markdown file."""
        content = Path(file_path).read_text()
        return self.parse_content(content)
    
    def parse_content(self, content: str) -> Dict:
        """Parse markdown content."""
        lines = content.split('\n')
        
        result = {
            'title': '',
            'sections': {},
            'pattern_text': [],
            'metadata': {}
        }
        
        current_section = 'main'
        result['sections'][current_section] = []
        
        for line in lines:
            # Detect headers
            if line.startswith('# '):
                result['title'] = line[2:].strip()
                current_section = 'title'
            elif line.startswith('## '):
                current_section = line[3:].strip()
                result['sections'][current_section] = []
            elif line.startswith('### '):
                current_section = line[4:].strip()
                result['sections'][current_section] = []
            elif line.startswith('**') and line.endswith('**'):
                current_section = line.strip('*').strip()
                result['sections'][current_section] = []
            else:
                if line.strip():
                    result['sections'].setdefault(current_section, []).append(line)
                    if self._is_pattern_instruction(line):
                        result['pattern_text'].append(line)
        
        return result
    
    def _is_pattern_instruction(self, line: str) -> bool:
        """Check if a line looks like a pattern instruction."""
        patterns = [
            r'round \d+',
            r'row \d+',
            r'r\d+',
            r'\d+ sc',
            r'\d+ dc',
            r'magic ring',
            r'mr',
            r'inc',
            r'dec',
        ]
        
        line_lower = line.lower()
        return any(re.search(p, line_lower) for p in patterns)
    
    def extract_clean_pattern(self, parsed: Dict) -> str:
        """Extract clean pattern text from parsed markdown."""
        lines = []
        
        if parsed['title']:
            lines.append(parsed['title'])
            lines.append('')
        
        for instruction in parsed['pattern_text']:
            clean = instruction.strip()
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)
            clean = re.sub(r'\*([^*]+)\*', r'\1', clean)
            clean = re.sub(r'`([^`]+)`', r'\1', clean)
            clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
            
            if clean:
                lines.append(clean)
        
        return '\n'.join(lines)

def parse_markdown_pattern(file_path: str) -> str:
    """Parse a markdown pattern file and return clean text."""
    parser = MarkdownPatternParser()
    parsed = parser.parse_file(file_path)
    return parser.extract_clean_pattern(parsed)
