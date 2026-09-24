"""
Markdown Parser - Strips formatting, extracts modules & rounds
Parses markdown headers into a multi-level AST before evaluating stitches
"""
import re
from typing import List, Tuple, Dict
from ..ast.nodes import PatternNode, PieceNode, RoundNode, ConstructionType


class MarkdownParser:
    """Parses markdown-formatted crochet patterns into AST"""
    
    def __init__(self):
        self.header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.round_pattern = re.compile(r'(?:round|row)\s+(\d+)[\s:]*', re.IGNORECASE)
        self.construction_pattern = re.compile(r'(?:worked\s+in\s+)?(rounds?|rows?)', re.IGNORECASE)
    
    def parse(self, markdown_text: str) -> PatternNode:
        """Parse markdown text into PatternNode AST"""
        pattern = PatternNode()
        
        # Split into sections by headers
        sections = self._split_by_headers(markdown_text)
        
        current_piece = None
        line_number = 0
        
        for section_type, section_content in sections:
            line_number += section_content.count('\n') + 1
            
            if section_type == 'title':
                pattern.title = section_content.strip()
            
            elif section_type == 'piece':
                # New piece/module
                piece_name = section_content.strip()
                construction_type = self._detect_construction_type(section_content)
                
                current_piece = PieceNode(
                    name=piece_name,
                    construction_type=construction_type
                )
                pattern.add_piece(current_piece)
            
            elif section_type == 'content' and current_piece:
                # Parse rounds/rows within current piece
                rounds = self._parse_rounds(section_content, line_number)
                for round_node in rounds:
                    current_piece.add_round(round_node)
            
            elif section_type == 'glossary':
                # Extract glossary/abbreviations
                glossary = self._parse_glossary(section_content)
                pattern.glossary.update(glossary)
            
            elif section_type == 'notes':
                # Extract notes
                notes = [line.strip() for line in section_content.split('\n') if line.strip()]
                pattern.notes.extend(notes)
        
        # If no pieces found, create a default piece
        if not pattern.pieces:
            default_piece = PieceNode(
                name="Main",
                construction_type=ConstructionType.ROUNDS
            )
            rounds = self._parse_rounds(markdown_text, 1)
            for round_node in rounds:
                default_piece.add_round(round_node)
            pattern.add_piece(default_piece)
        
        return pattern
    
    def _split_by_headers(self, text: str) -> List[Tuple[str, str]]:
        """Split text into sections based on markdown headers"""
        sections = []
        lines = text.split('\n')
        current_section = []
        current_type = 'content'
        
        for line in lines:
            header_match = self.header_pattern.match(line)
            
            if header_match:
                # Save previous section
                if current_section:
                    sections.append((current_type, '\n'.join(current_section)))
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                # Determine section type
                if level == 1:
                    current_type = 'title'
                elif any(kw in title.lower() for kw in ['glossary', 'abbreviation', 'terms']):
                    current_type = 'glossary'
                elif any(kw in title.lower() for kw in ['note', 'instruction', 'special']):
                    current_type = 'notes'
                else:
                    current_type = 'piece'
                
                current_section = [title]
            else:
                current_section.append(line)
        
        # Save last section
        if current_section:
            sections.append((current_type, '\n'.join(current_section)))
        
        return sections
    
    def _detect_construction_type(self, text: str) -> ConstructionType:
        """Detect if piece is worked in rounds or rows"""
        if re.search(r'\brounds?\b', text, re.IGNORECASE):
            return ConstructionType.ROUNDS
        elif re.search(r'\brows?\b', text, re.IGNORECASE):
            return ConstructionType.ROWS
        else:
            return ConstructionType.ROUNDS  # Default to rounds
    
    def _parse_rounds(self, text: str, start_line: int) -> List[RoundNode]:
        """Parse rounds/rows from text"""
        rounds = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines, start_line):
            line = line.strip()
            if not line:
                continue
            
            round_match = self.round_pattern.match(line)
            if round_match:
                round_num = int(round_match.group(1))
                round_node = RoundNode(
                    number=round_num,
                    line_number=i,
                    raw_text=line
                )
                rounds.append(round_node)
        
        return rounds
    
    def _parse_glossary(self, text: str) -> Dict[str, str]:
        """Parse glossary/abbreviation definitions"""
        glossary = {}
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Parse "abbreviation - definition" or "abbreviation: definition"
            match = re.match(r'([a-z\s]+)\s*[-:]\s*(.+)', line, re.IGNORECASE)
            if match:
                abbrev = match.group(1).strip()
                definition = match.group(2).strip()
                glossary[abbrev.lower()] = definition
        
        return glossary


if __name__ == "__main__":
    print("📄 Markdown Parser")
    print("=" * 60)
    
    parser = MarkdownParser()
    
    test_markdown = """# Amigurumi Bear

## Materials
- Worsted weight yarn
- 4mm hook

## Body (worked in rounds)
Round 1: 6 sc in magic ring (6)
Round 2: inc in each st around (12)
Round 3: *sc 1, inc* rep around (18)

## Head (worked in rounds)
Round 1: 6 sc in magic ring (6)
Round 2: inc in each st around (12)

## Glossary
sc - single crochet
inc - increase (2 sc in same st)
rep - repeat
"""
    
    pattern = parser.parse(test_markdown)
    
    print(f"\nPattern Title: {pattern.title}")
    print(f"Pieces Found: {len(pattern.pieces)}")
    
    for piece in pattern.pieces:
        print(f"\n  Piece: {piece.name}")
        print(f"  Type: {piece.construction_type.value}")
        print(f"  Rounds: {len(piece.rounds)}")
        for r in piece.rounds:
            print(f"    Round {r.number}: {r.raw_text[:50]}...")
    
    print(f"\nGlossary: {len(pattern.glossary)} terms")
    for term, defn in list(pattern.glossary.items())[:3]:
        print(f"  {term}: {defn}")
    
    print("\n✅ Markdown Parser working!")
