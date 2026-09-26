from .parser import CrochetParser, ParseError, parse_pattern

"""
Parser package - AST-based pattern parsing and unrolling

Pipeline (per 4-pattern audit):
  1. MarkdownFrontmatterSanitizer  -> strips non-instructional markdown
  2. GlossaryPrePassExtractor      -> symbol table before instruction parsing
  3. MultiPieceASTBuilder          -> isolated PieceNode scopes
  4. RecursiveLoopUnroller         -> flat array of atomic operations
"""

from .ast_builder import (
    ASTBuilder,
    ConstructionMode,
    MultiPieceASTBuilder,
    PatternNode,
    PieceNode,
    RoundNode,
    StitchInstruction,
)
from .glossary import GlossaryEntry, GlossaryPrePassExtractor
from .lexer import Lexer, Section
from .sanitizer import MarkdownFrontmatterSanitizer
from .unroller import AtomicOperation, RecursiveLoopUnroller, RepeatNode, Unroller

__all__ = [
    "CrochetParser",
    "ParseError",
    "parse_pattern",
    # Lexer
    "Lexer",
    "Section",
    # Sanitizer
    "MarkdownFrontmatterSanitizer",
    # Glossary
    "GlossaryPrePassExtractor",
    "GlossaryEntry",
    # AST Builder
    "ASTBuilder",
    "MultiPieceASTBuilder",
    "PatternNode",
    "PieceNode",
    "RoundNode",
    "StitchInstruction",
    "ConstructionMode",
    # Unroller
    "Unroller",
    "RepeatNode",
    "RecursiveLoopUnroller",
    "AtomicOperation",
]
