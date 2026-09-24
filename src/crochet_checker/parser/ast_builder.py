import re
"""
AST Builder - Builds PatternNode -> PieceNode -> Round/RowNode hierarchy
"""
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum

try:
    from .lexer import Lexer, Section
except ImportError:  # pragma: no cover - run as __main__ demo
    import importlib.util
    from pathlib import Path
    _spec = importlib.util.spec_from_file_location(
        "lexer", Path(__file__).resolve().parent / "lexer.py")
    _lexer_mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_lexer_mod)
    Lexer, Section = _lexer_mod.Lexer, _lexer_mod.Section


class ConstructionMode(Enum):
    ROUNDS = "ROUNDS"
    ROWS = "ROWS"


@dataclass
class StitchInstruction:
    """Represents a single stitch instruction"""
    stitch_type: str
    count: int = 1
    target: Optional[str] = None  # e.g., "next st", "ch-sp"
    line_number: int = 0


@dataclass
class RoundNode:
    """Represents a single round or row"""
    number: int
    instructions: List[StitchInstruction] = field(default_factory=list)
    raw_text: str = ""
    line_number: int = 0
    stitch_count: Optional[int] = None


@dataclass
class PieceNode:
    """Represents a piece/module of the pattern"""
    name: str
    construction_mode: ConstructionMode = ConstructionMode.ROUNDS
    rounds: List[RoundNode] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def add_round(self, round_node: RoundNode):
        self.rounds.append(round_node)
    
    def get_round(self, number: int) -> Optional[RoundNode]:
        for r in self.rounds:
            if r.number == number:
                return r
        return None


@dataclass
class PatternNode:
    """Root node of the pattern AST"""
    title: str = ""
    pieces: List[PieceNode] = field(default_factory=list)
    glossary: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def add_piece(self, piece: PieceNode):
        self.pieces.append(piece)
    
    def get_piece(self, name: str) -> Optional[PieceNode]:
        for p in self.pieces:
            if p.name.lower() == name.lower():
                return p
        return None


class ASTBuilder:
    """Builds AST from tokenized sections"""
    
    def __init__(self):
        self.lexer = Lexer()
        self.stitch_pattern = re.compile(r'(\d+)\s*(sc|dc|hdc|tr|sl\s*st|ch|skip|inc|dec)', re.IGNORECASE)
    
    def build(self, markdown_text: str) -> PatternNode:
        """Build complete AST from markdown"""
        pattern = PatternNode()
        
        # Tokenize into sections
        sections = self.lexer.tokenize(markdown_text)
        
        # Extract glossary
        pattern.glossary = self.lexer.isolate_glossary(sections)
        
        # Extract instructions and build pieces
        current_piece = None
        
        for section in sections:
            if section.section_type == 'instructions':
                # Parse instruction lines
                lines = section.content.split('\n')
                
                for i, line in enumerate(lines):
                    line_num = section.line_number + i
                    cleaned = self.lexer.strip_markdown(line)
                    
                    # Check for piece header
                    if self._is_piece_header(cleaned):
                        piece_name = self._extract_piece_name(cleaned)
                        construction_mode = self._detect_construction_mode(cleaned)
                        
                        current_piece = PieceNode(
                            name=piece_name,
                            construction_mode=construction_mode
                        )
                        pattern.add_piece(current_piece)
                    
                    # Check for round/row
                    round_num = self.lexer.extract_round_number(cleaned)
                    if round_num and current_piece:
                        round_node = self._parse_round(cleaned, round_num, line_num)
                        current_piece.add_round(round_node)
        
        # If no pieces found, create default piece
        if not pattern.pieces:
            default_piece = PieceNode(name="Main")
            instructions = self.lexer.isolate_instructions(sections)
            
            for line_num, line in instructions:
                round_num = self.lexer.extract_round_number(line)
                if round_num:
                    round_node = self._parse_round(line, round_num, line_num)
                    default_piece.add_round(round_node)
            
            pattern.add_piece(default_piece)
        
        return pattern
    
    def _is_piece_header(self, line: str) -> bool:
        """Check if line is a piece header"""
        return bool(re.search(r'(piece|module|part|section)\s+\d+', line, re.IGNORECASE))
    
    def _extract_piece_name(self, line: str) -> str:
        """Extract piece name from header"""
        match = re.search(r'(piece|module|part|section)\s+(\d+|\w+)', line, re.IGNORECASE)
        if match:
            return match.group(0)
        return "Unknown Piece"
    
    def _detect_construction_mode(self, line: str) -> ConstructionMode:
        """Detect if piece uses ROUNDS or ROWS"""
        if re.search(r'\brows?\b', line, re.IGNORECASE):
            return ConstructionMode.ROWS
        return ConstructionMode.ROUNDS
    
    def _parse_round(self, line: str, round_num: int, line_num: int) -> RoundNode:
        """Parse a round/row line into RoundNode"""
        round_node = RoundNode(
            number=round_num,
            raw_text=line,
            line_number=line_num
        )
        
        # Extract stitch count if present: "(6)", "(12 sts)", "(12 stitches)"
        count_match = re.search(r'\((\d+)\s*(?:sts?|stitches?)?\)', line)
        if count_match:
            round_node.stitch_count = int(count_match.group(1))
        
        # Parse instructions
        instructions = self._parse_instructions(line, line_num)
        round_node.instructions = instructions
        
        return round_node
    
    def _parse_instructions(self, line: str, line_num: int) -> List[StitchInstruction]:
        """Parse instruction line into StitchInstructions"""
        instructions = []
        
        # Find all stitch patterns
        for match in self.stitch_pattern.finditer(line):
            count = int(match.group(1))
            stitch_type = match.group(2).lower()
            
            # Look for target after stitch
            target = None
            rest_of_line = line[match.end():]
            target_match = re.match(r'\s+(in|into)\s+(.+?)(?:,|$)', rest_of_line)
            if target_match:
                target = target_match.group(2).strip()
            
            instructions.append(StitchInstruction(
                stitch_type=stitch_type,
                count=count,
                target=target,
                line_number=line_num
            ))
        
        return instructions


if __name__ == "__main__":
    print("🏗️ AST Builder Test")
    builder = ASTBuilder()
    
    test_pattern = """
# Test Pattern

## Glossary
sc: single crochet
dc: double crochet

## Instructions
Round 1: 6 sc in magic ring (6)
Round 2: 2 sc in each st around (12)
Round 3: *1 sc, 2 sc in next st* repeat around (18)
"""
    
    ast = builder.build(test_pattern)
    print(f"Title: {ast.title}")
    print(f"Pieces: {len(ast.pieces)}")
    print(f"Glossary: {ast.glossary}")
    
    for piece in ast.pieces:
        print(f"\nPiece: {piece.name}")
        print(f"Mode: {piece.construction_mode.value}")
        print(f"Rounds: {len(piece.rounds)}")
        for r in piece.rounds:
            print(f"  Round {r.number}: {len(r.instructions)} instructions, count={r.stitch_count}")


# ============================================================================
# MultiPieceASTBuilder - Splits markdown into isolated PieceNode scopes.
# Ensures yarn pointers, construction types (ROWS vs ROUNDS), and stitch state
# reset completely between independent modules or petals.
# (Added per 4-pattern audit: Chrono-Mandala, Astral Lattice, Asymmetric
#  Pentagon, Hyper-Geometric Polyhedron)
# ============================================================================

class MultiPieceASTBuilder:
    """Splits sanitized markdown into isolated PieceNode scopes with full state reset."""
    
    def __init__(self):
        self.lexer = Lexer()
        self.stitch_pattern = re.compile(r'(\d+)\s*(sc|dc|hdc|tr|sl\s*st|ch|skip|inc|dec)', re.IGNORECASE)
        # Piece headers: "Petal 1", "Body 2", or a bare name on its own line ("Body", "Head")
        self._piece_keywords = r'(?:piece|module|part|section|component|petal|leaf|body|head|arm|leg|ear|tail)s?'
        self.piece_numbered_pattern = re.compile(
            rf'(?i)^{self._piece_keywords}\s+\d+'
        )
        self.piece_bare_pattern = re.compile(
            rf'(?i)^{self._piece_keywords}\s*$'
        )
    
    def build(self, markdown_text: str) -> PatternNode:
        """Build a multi-piece AST by scanning the raw text line by line.

        The lexer's section tokenizer can swallow piece headers (e.g. '## Petal 1'),
        so this builder works on raw markdown to guarantee piece isolation.
        """
        pattern = PatternNode()
        
        # Glossary pre-pass: definitions must not be tallied as stitches
        sections = self.lexer.tokenize(markdown_text)
        pattern.glossary = self.lexer.isolate_glossary(sections)
        
        current_piece = None
        piece_counter = 0
        in_glossary_section = False
        
        for line_num, raw_line in enumerate(markdown_text.split('\n'), 1):
            line = self.lexer.strip_markdown(raw_line)
            if not line.strip():
                continue
            
            # Skip glossary/abbreviation sections entirely
            if re.match(r'(?i)^#*\s*(glossary|abbreviations|stitch\s+definitions)\s*$', line):
                in_glossary_section = True
                continue
            if in_glossary_section:
                if line.startswith('#'):
                    in_glossary_section = False
                else:
                    continue  # glossary definition lines -> never instructions
            
            # Detect piece header -> new isolated scope
            if self._is_piece_header(line):
                piece_counter += 1
                piece_name = self._extract_piece_name(line)
                detected_mode = self._detect_construction_mode(line)
                
                current_piece = PieceNode(
                    name=piece_name,
                    construction_mode=detected_mode or ConstructionMode.ROUNDS
                )
                current_piece.metadata['scope_id'] = piece_counter
                current_piece.metadata['yarn_pointer'] = 0  # yarn pointer resets per piece
                current_piece.metadata['mode_explicit'] = detected_mode is not None
                pattern.add_piece(current_piece)
                continue
            
            # Round/row within current piece scope
            round_num = self.lexer.extract_round_number(line)
            if round_num and current_piece:
                round_node = self._parse_round(line, round_num, line_num)
                current_piece.add_round(round_node)
        
        # Post-pass: infer ROWS vs ROUNDS from content when the header didn't say
        for piece in pattern.pieces:
            if not piece.metadata.get('mode_explicit') and piece.rounds:
                first_raw = piece.rounds[0].raw_text
                if re.search(r'\brow\b', first_raw, re.IGNORECASE):
                    piece.construction_mode = ConstructionMode.ROWS
                elif re.search(r'\bround\b', first_raw, re.IGNORECASE):
                    piece.construction_mode = ConstructionMode.ROUNDS
        
        # Fallback: no explicit pieces -> single default piece
        if not pattern.pieces:
            default_piece = PieceNode(name="Main")
            default_piece.metadata['scope_id'] = 1
            default_piece.metadata['yarn_pointer'] = 0
            instructions = self.lexer.isolate_instructions(sections)
            for line_num, line in instructions:
                round_num = self.lexer.extract_round_number(line)
                if round_num:
                    round_node = self._parse_round(line, round_num, line_num)
                    default_piece.add_round(round_node)
            pattern.add_piece(default_piece)
        
        return pattern
    
    def _is_piece_header(self, line: str) -> bool:
        """Check if line starts a new independent piece/module."""
        return bool(self.piece_numbered_pattern.match(line) or self.piece_bare_pattern.match(line))
    
    def _extract_piece_name(self, line: str) -> str:
        """Extract the piece name from a header line."""
        numbered = self.piece_numbered_pattern.match(line)
        if numbered:
            return numbered.group(0)
        bare = self.piece_bare_pattern.match(line)
        if bare:
            return bare.group(0)
        return "Unknown Piece"
    
    def _detect_construction_mode(self, line: str) -> Optional[ConstructionMode]:
        """Detect ROWS vs ROUNDS from the header line. Returns None if unspecified."""
        if re.search(r'\brows?\b', line, re.IGNORECASE):
            return ConstructionMode.ROWS
        if re.search(r'\brounds?\b', line, re.IGNORECASE):
            return ConstructionMode.ROUNDS
        return None
    
    def _parse_round(self, line: str, round_num: int, line_num: int) -> RoundNode:
        """Parse a round line into a RoundNode."""
        round_node = RoundNode(
            number=round_num,
            raw_text=line,
            line_number=line_num
        )
        # Accept "(6)", "(12 sts)", "(12 stitches)"
        count_match = re.search(r'\((\d+)\s*(?:sts?|stitches?)?\)', line)
        if count_match:
            round_node.stitch_count = int(count_match.group(1))
        
        for match in self.stitch_pattern.finditer(line):
            round_node.instructions.append(StitchInstruction(
                stitch_type=match.group(2).lower(),
                count=int(match.group(1)),
                line_number=line_num
            ))
        return round_node
    
    def validate_piece_boundaries(self, pattern: PatternNode) -> List[str]:
        """
        Validate that pieces are properly isolated.
        Returns a list of boundary errors (empty = valid).
        """
        errors = []
        for piece in pattern.pieces:
            if not piece.rounds:
                errors.append(f"Piece '{piece.name}' has no rounds")
            round_numbers = [r.number for r in piece.rounds]
            for i in range(1, len(round_numbers)):
                if round_numbers[i] != round_numbers[i - 1] + 1:
                    errors.append(
                        f"Piece '{piece.name}': missing round {round_numbers[i-1] + 1}"
                    )
            if piece.construction_mode == ConstructionMode.ROUNDS and \
               any('row' in r.raw_text.lower() for r in piece.rounds):
                errors.append(
                    f"Piece '{piece.name}': ROWS content inside ROUNDS piece scope"
                )
        return errors


if __name__ == "__main__":
    print("🏗️ AST Builder Test")
    builder = ASTBuilder()
    
    test_pattern = """
# Test Pattern

## Glossary
sc: single crochet
dc: double crochet

## Instructions
Round 1: 6 sc in magic ring (6)
Round 2: 2 sc in each st around (12)
Round 3: *1 sc, 2 sc in next st* repeat around (18)
"""
    
    ast = builder.build(test_pattern)
    print(f"Title: {ast.title}")
    print(f"Pieces: {len(ast.pieces)}")
    print(f"Glossary: {ast.glossary}")
    
    for piece in ast.pieces:
        print(f"\nPiece: {piece.name}")
        print(f"Mode: {piece.construction_mode.value}")
        print(f"Rounds: {len(piece.rounds)}")
        for r in piece.rounds:
            print(f"  Round {r.number}: {len(r.instructions)} instructions, count={r.stitch_count}")
    
    # Multi-piece test
    print("\n\n🧩 MultiPieceASTBuilder Test")
    multi = MultiPieceASTBuilder()
    multi_pattern = """
## Petal 1
Round 1: 6 sc in magic ring (6)
Round 2: 2 sc in each st (12)

## Petal 2
Round 1: 6 sc in magic ring (6)
Round 2: 2 sc in each st (12)
"""
    mast = multi.build(multi_pattern)
    print(f"Pieces found: {len(mast.pieces)}")
    for p in mast.pieces:
        print(f"  {p.name}: {len(p.rounds)} rounds, scope={p.metadata.get('scope_id')}")
    boundary_errors = multi.validate_piece_boundaries(mast)
    print(f"Boundary errors: {boundary_errors}")
