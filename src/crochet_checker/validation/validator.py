"""
Validator - Main entry point for pattern validation
Implements the multi-pass compiler design for comprehensive pattern validation
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from ..lexer.markdown_parser import MarkdownParser
from ..lexer.glossary_extractor import GlossaryExtractor
from ..ast.nodes import PatternNode, PieceNode, InstructionNode
from ..ast.unroller import ASTUnroller
from ..engine.state_machine import StateMachine
from ..engine.assembly_graph import AssemblyGraph


@dataclass
class ValidationError:
    """Represents a validation error"""
    line_number: int
    message: str
    severity: str = "error"  # 'error', 'warning', 'info'
    piece_name: str = ""
    round_number: int = 0


@dataclass
class ValidationResult:
    """Result of pattern validation"""
    is_valid: bool
    total_stitches: int
    piece_count: int
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    info: List[ValidationError] = field(default_factory=list)
    stitch_counts: Dict[int, int] = field(default_factory=dict)
    execution_time: float = 0.0


class PatternValidator:
    """Main validator implementing multi-pass compiler design"""
    
    def __init__(self):
        self.parser = MarkdownParser()
        self.glossary_extractor = GlossaryExtractor()
        self.unroller = ASTUnroller()
        self.state_machine = StateMachine()
        self.assembly_graph = AssemblyGraph()
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
    
    def validate(self, pattern_text: str) -> ValidationResult:
        """
        Validate a crochet pattern using multi-pass compiler design
        
        Pass 1: Extract frontmatter and glossary
        Pass 2: Build AST and unroll loops
        Pass 3: Validate and check topology
        """
        import time
        start_time = time.time()
        
        # Pass 1: Parse and extract glossary
        pattern_ast = self._pass1_extract_and_parse(pattern_text)
        
        # Pass 2: Build AST and unroll
        unrolled_instructions = self._pass2_build_and_unroll(pattern_ast)
        
        # Pass 3: Validate with state machine
        validation_result = self._pass3_validate(unrolled_instructions, pattern_ast)
        
        execution_time = time.time() - start_time
        validation_result.execution_time = execution_time
        
        return validation_result
    
    def _pass1_extract_and_parse(self, pattern_text: str) -> PatternNode:
        """Pass 1: Extract glossary and parse markdown structure"""
        # Extract glossary
        extracted_glossary = self.glossary_extractor.extract_from_text(pattern_text)
        
        # Parse markdown into AST
        pattern_ast = self.parser.parse(pattern_text)
        
        # Merge glossaries
        pattern_ast.glossary.update(extracted_glossary)
        
        return pattern_ast
    
    def _pass2_build_and_unroll(self, pattern_ast: PatternNode) -> Dict[str, List[List[InstructionNode]]]:
        """Pass 2: Unroll all loops and repeats into atomic instructions"""
        unrolled = {}
        
        for piece in pattern_ast.pieces:
            piece_instructions = []
            prev_stitch_count = 0
            
            for round_node in piece.rounds:
                # Unroll the round instructions
                instructions = self.unroller.unroll_round(
                    round_node.raw_text,
                    round_node.line_number,
                    prev_stitch_count
                )
                
                piece_instructions.append(instructions)
                
                # Calculate expected stitch count for next round
                prev_stitch_count = self.unroller.calculate_round_stitch_count(
                    instructions, prev_stitch_count
                )
            
            unrolled[piece.name] = piece_instructions
        
        return unrolled
    
    def _pass3_validate(self, unrolled_instructions: Dict[str, List[List[InstructionNode]]],
                       pattern_ast: PatternNode) -> ValidationResult:
        """Pass 3: Validate using state machine and check topology"""
        total_stitches = 0
        stitch_counts = {}
        
        # Validate each piece
        for piece_name, piece_rounds in unrolled_instructions.items():
            piece = pattern_ast.get_piece(piece_name)
            if not piece:
                continue
            
            prev_count = 0
            
            for round_idx, instructions in enumerate(piece_rounds, 1):
                # Initialize state machine for this round
                if round_idx == 1:
                    # Foundation round: works into a magic ring / chain,
                    # stitches are created fresh (no previous canvas to consume)
                    self.state_machine.initialize_round(0, round_idx, create_mode=True)
                else:
                    self.state_machine.initialize_round(prev_count, round_idx)
                
                # Execute each instruction
                round_stitches = 0
                for instr in instructions:
                    # Validate directional movement
                    self.state_machine.validate_directional_movement(instr)
                    
                    # Execute instruction
                    produced = self.state_machine.execute_instruction(instr)
                    round_stitches += produced
                    
                    # Check for errors
                    if self.state_machine.errors:
                        for error in self.state_machine.errors:
                            self.errors.append(ValidationError(
                                line_number=instr.line_number,
                                message=error,
                                severity="error",
                                piece_name=piece_name,
                                round_number=round_idx
                            ))
                        self.state_machine.errors.clear()
                    
                    # Check for warnings
                    if self.state_machine.warnings:
                        for warning in self.state_machine.warnings:
                            self.warnings.append(ValidationError(
                                line_number=instr.line_number,
                                message=warning,
                                severity="warning",
                                piece_name=piece_name,
                                round_number=round_idx
                            ))
                        self.state_machine.warnings.clear()
                
                # Finalize round
                final_count = self.state_machine.finalize_round()
                stitch_counts[(piece_name, round_idx)] = final_count
                total_stitches += final_count
                prev_count = final_count
        
        # Validate assembly (if multiple pieces)
        if len(pattern_ast.pieces) > 1:
            self._validate_assembly(pattern_ast)
        
        is_valid = len(self.errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            total_stitches=total_stitches,
            piece_count=len(pattern_ast.pieces),
            errors=self.errors.copy(),
            warnings=self.warnings.copy(),
            stitch_counts=stitch_counts
        )
    
    def _validate_assembly(self, pattern_ast: PatternNode):
        """Validate assembly connections between pieces"""
        # Register all pieces
        for piece in pattern_ast.pieces:
            self.assembly_graph.register_piece(piece.name, {
                'construction_type': piece.construction_type.value,
                'round_count': len(piece.rounds)
            })
        
        # Check for assembly instructions in pattern text
        # This would need to be enhanced to detect join instructions
        # For now, just validate completeness
        orphans = self.assembly_graph.detect_orphan_pieces()
        
        if orphans and len(pattern_ast.pieces) > 1:
            self.warnings.append(ValidationError(
                line_number=0,
                message=f"Pieces without joins detected: {', '.join(orphans)}",
                severity="warning"
            ))


if __name__ == "__main__":
    print("✅ Pattern Validator")
    print("=" * 60)
    
    validator = PatternValidator()
    
    test_pattern = """
# Simple Amigurumi Ball

## Body (worked in rounds)
Round 1: 6 sc in magic ring (6)
Round 2: inc in each st around (12)
Round 3: *sc 1, inc* rep around (18)
Round 4: sc in each st around (18)
Round 5: *sc 2, dec* rep around (12)
Round 6: dec around (6)

## Glossary
sc - single crochet
inc - increase
dec - decrease
rep - repeat
"""
    
    result = validator.validate(test_pattern)
    
    print(f"\nValidation Result:")
    print(f"  Valid: {result.is_valid}")
    print(f"  Total Stitches: {result.total_stitches}")
    print(f"  Pieces: {result.piece_count}")
    print(f"  Execution Time: {result.execution_time:.3f}s")
    
    print(f"\nStitch Counts:")
    for (piece, round_num), count in sorted(result.stitch_counts.items()):
        print(f"  {piece} Round {round_num}: {count} stitches")
    
    if result.errors:
        print(f"\n❌ Errors ({len(result.errors)}):")
        for error in result.errors[:5]:
            print(f"  Line {error.line_number}: {error.message}")
    
    if result.warnings:
        print(f"\n⚠️ Warnings ({len(result.warnings)}):")
        for warning in result.warnings[:5]:
            print(f"  Line {warning.line_number}: {warning.message}")
    
    print("\n✅ Pattern Validator working!")


# ============================================================================
# Compatibility exports (used by test_all_features.py and legacy callers)
# ============================================================================

from enum import Enum as _Enum


class Severity(_Enum):
    """Severity levels for validation findings."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationReport:
    """Legacy-style validation report container."""
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stitch_count: int = 0


def validate_pattern(pattern_text: str):
    """
    Convenience function for one-shot validation.
    Returns a plain dict compatible with legacy callers.
    """
    validator = PatternValidator()
    result = validator.validate(pattern_text)
    return {
        'valid': result.is_valid,
        'errors': [e.message for e in result.errors],
        'warnings': [w.message for w in result.warnings],
        'stitch_count': result.total_stitches,
    }
