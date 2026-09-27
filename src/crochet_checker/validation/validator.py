"""
Validator - Main entry point for pattern validation
Implements the multi-pass compiler design for comprehensive pattern validation
"""

from dataclasses import dataclass, field

from ..ast.nodes import InstructionNode, PatternNode
from ..ast.unroller import ASTUnroller
from ..engine.assembly_graph import AssemblyGraph
from ..engine.state_machine import StateMachine
from ..lexer.glossary_extractor import GlossaryExtractor
from ..lexer.markdown_parser import MarkdownParser


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
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)
    info: list[ValidationError] = field(default_factory=list)
    stitch_counts: dict[int, int] = field(default_factory=dict)
    execution_time: float = 0.0


class PatternValidator:
    """Main validator implementing multi-pass compiler design"""

    def __init__(self):
        self.parser = MarkdownParser()
        self.glossary_extractor = GlossaryExtractor()
        self.unroller = ASTUnroller()
        self.state_machine = StateMachine()
        self.assembly_graph = AssemblyGraph()
        self.errors: list[ValidationError] = []
        self.warnings: list[ValidationError] = []

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

    def _pass2_build_and_unroll(
        self, pattern_ast: PatternNode
    ) -> dict[str, list[list[InstructionNode]]]:
        """Pass 2: Unroll all loops and repeats into atomic instructions"""
        unrolled = {}

        for piece in pattern_ast.pieces:
            piece_instructions = []
            prev_stitch_count = 0

            for round_node in piece.rounds:
                # Unroll the round instructions
                instructions = self.unroller.unroll_round(
                    round_node.raw_text, round_node.line_number, prev_stitch_count
                )

                piece_instructions.append(instructions)

                # Calculate expected stitch count for next round
                prev_stitch_count = self.unroller.calculate_round_stitch_count(
                    instructions, prev_stitch_count
                )

            unrolled[piece.name] = piece_instructions

        return unrolled

    def _pass3_validate(
        self,
        unrolled_instructions: dict[str, list[list[InstructionNode]]],
        pattern_ast: PatternNode,
    ) -> ValidationResult:
        """Pass 3: Validate using state machine and check topology"""
        total_stitches = 0
        stitch_counts = {}

        # Validate each piece
        for piece_name, piece_rounds in unrolled_instructions.items():
            piece = pattern_ast.get_piece(piece_name)
            if not piece:
                continue

            prev_count = 0
            previous_loops = None
            foundation_chain = None
            last_number = None
            round_nodes = piece.rounds

            for round_idx, instructions in enumerate(piece_rounds, 1):
                raw_text = ""
                line_number = 0
                number = None
                if round_idx - 1 < len(round_nodes):
                    raw_text = round_nodes[round_idx - 1].raw_text
                    line_number = round_nodes[round_idx - 1].line_number
                    number = round_nodes[round_idx - 1].number
                # A repeated "Round 1" is a new piece when headings were not split.
                if number is not None and last_number is not None and number <= last_number:
                    previous_loops = None
                    foundation_chain = None
                if number is not None:
                    last_number = number
                parsed = self._parsed_round_instructions(raw_text)
                if parsed is not None:
                    message = self._continuity_message(
                        raw_text, line_number, previous_loops, foundation_chain
                    )
                    if message:
                        self.errors.append(
                            ValidationError(
                                line_number=line_number,
                                message=message,
                                severity="error",
                                piece_name=piece_name,
                                round_number=round_idx,
                            )
                        )
                    counted = self._loops_after_round(raw_text, previous_loops)
                    ops = [op for inst in parsed for op in inst.operations]
                    if ops and all(
                        getattr(op.stitch_type, "value", "") == "chain" for op in ops
                    ):
                        foundation_chain = counted
                    else:
                        foundation_chain = None
                    previous_loops = counted
                    stitch_counts[(piece_name, round_idx)] = counted
                    total_stitches += counted
                    prev_count = counted
                    continue
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
                            self.errors.append(
                                ValidationError(
                                    line_number=instr.line_number,
                                    message=error,
                                    severity="error",
                                    piece_name=piece_name,
                                    round_number=round_idx,
                                )
                            )
                        self.state_machine.errors.clear()

                    # Check for warnings
                    if self.state_machine.warnings:
                        for warning in self.state_machine.warnings:
                            self.warnings.append(
                                ValidationError(
                                    line_number=instr.line_number,
                                    message=warning,
                                    severity="warning",
                                    piece_name=piece_name,
                                    round_number=round_idx,
                                )
                            )
                        self.state_machine.warnings.clear()

                # Finalize round. This path is only for text the live parser
                # could not read. Parsed rounds are checked above.
                final_count = self.state_machine.finalize_round()
                previous_loops = None
                foundation_chain = None
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
            stitch_counts=stitch_counts,
        )

    def _parsed_round_instructions(self, raw_text: str):
        """Parse one round with the live instruction parser, not the unroller."""
        from ..parser.grammar import is_row_header
        from ..parser.parser import CrochetParser

        # Bold and code markers hide headers. A single asterisk is a repeat
        # marker, as in "*sc, inc* 6 times", and must not be deleted.
        from ..parser.normalizer import sanitize_pattern_text

        cleaned = sanitize_pattern_text(raw_text or "").strip()
        if not cleaned:
            return None
        header, _header_type, _number, rest, _end = is_row_header(cleaned)
        text = rest if header else cleaned
        return CrochetParser()._parse_instruction_text(text, cleaned)

    def _context_consumed(self, instructions, previous) -> int:
        """Loops a round works into, expanding 'each st around'."""
        context = {"each_stitch_around", "each_stitch_across", "remaining"}
        skip = {"join", "foundation", "foundation_chain"}
        from ..model.stitch import STITCH_CONSUMPTION

        total = 0
        for instruction in instructions:
            for op in instruction.operations:
                value = getattr(op.stitch_type, "value", "")
                target = getattr(op, "into_stitch", None)
                if value in ("chain", "magic_ring") or target in skip:
                    continue
                if target in context:
                    total += 0 if previous is None else previous
                    continue
                total += STITCH_CONSUMPTION.get(op.stitch_type, 1) * int(op.count)
        return total

    def _continuity_message(self, raw_text, line_number, previous, foundation_chain):
        """Flag a count change that the stitches do not explain.

        '(sc, inc) x 6' after 6 stitches is an increase, so it is not a loop
        error. '9 sc' after '10 sc' is. A starting chain is the base for the
        next row, and one turning-chain row may use one less stitch.
        """
        instructions = self._parsed_round_instructions(raw_text) or []
        ops = [op for instruction in instructions for op in instruction.operations]
        if not ops or previous is None:
            return None
        if all(getattr(op.stitch_type, "value", "") == "chain" for op in ops):
            return None
        values = {getattr(op.stitch_type, "value", "") for op in ops}
        produced = self._loops_after_round(raw_text, previous)
        consumed = self._context_consumed(instructions, previous)
        if consumed > previous and "increase" not in values:
            return (
                f"Line {line_number}: Attempted to work stitch beyond available loops. "
                f"Position: {previous}, Available: {previous}"
            )
        if produced < previous and "decrease" not in values:
            if foundation_chain and produced == foundation_chain - 1:
                return None
            noun = "stitch" if produced == 1 else "stitches"
            return (
                f"Line {line_number}: worked {produced} {noun} into {previous} "
                f"without a decrease."
            )
        return None

    def _loops_after_round(self, raw_text: str, previous) -> int:
        """Stitches the next round can work into."""
        instructions = self._parsed_round_instructions(raw_text) or []
        ops = [op for instruction in instructions for op in instruction.operations]
        if ops and all(
            getattr(op.stitch_type, "value", "") == "chain" for op in ops
        ):
            return sum(int(op.count) for op in ops)
        total = 0
        available = previous
        for instruction in instructions:
            total += _produced_with_context(instruction, available)
            if _needs_previous_round(instruction):
                available = 0
            elif available is not None:
                available -= instruction.total_stitches_consumed
        return total

    def _validate_assembly(self, pattern_ast: PatternNode):
        """Validate assembly connections between pieces"""
        # Register all pieces
        for piece in pattern_ast.pieces:
            self.assembly_graph.register_piece(
                piece.name,
                {
                    "construction_type": piece.construction_type.value,
                    "round_count": len(piece.rounds),
                },
            )

        # Check for assembly instructions in pattern text
        # This would need to be enhanced to detect join instructions
        # For now, just validate completeness
        orphans = self.assembly_graph.detect_orphan_pieces()
        recorded_joins = bool(getattr(self.assembly_graph, "edges", None))

        # With no recorded joins, every piece looks orphaned. That is not
        # evidence of a bad pattern, and a heading used to swallow later
        # rounds into the piece name.
        if orphans and recorded_joins:
            names = [name.splitlines()[0].strip() for name in orphans]
            self.warnings.append(
                ValidationError(
                    line_number=0,
                    message=f"Pieces without joins detected: {', '.join(names)}",
                    severity="warning",
                )
            )


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

    print("\nValidation Result:")
    print(f"  Valid: {result.is_valid}")
    print(f"  Total Stitches: {result.total_stitches}")
    print(f"  Pieces: {result.piece_count}")
    print(f"  Execution Time: {result.execution_time:.3f}s")

    print("\nStitch Counts:")
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
# ============================================================================
# Compatibility exports
# ============================================================================

from enum import Enum as _Enum


class Severity(_Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
@dataclass
class _CompatFinding:
    """Legacy finding object used by AI and suggestion consumers."""

    message: str
    severity: str = "error"
    location: str = ""

    def __str__(self) -> str:
        return self.message


@dataclass
class ValidationReport:
    """
    Compatibility report shared by the validator, AI, visualization, PDF,
    and web layers.
    """

    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stitch_count: int = 0
    score: int = 100
    overall_status: str = "PASS"
    stitch_counts: dict[int, int] = field(default_factory=dict)
    row_transitions: list[dict] = field(default_factory=list)
    consistency: bool = True

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def is_valid(self) -> bool:
        return self.valid

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "errors": [getattr(item, "message", str(item)) for item in self.errors],
            "warnings": [getattr(item, "message", str(item)) for item in self.warnings],
            "stitch_count": self.stitch_count,
            "score": self.score,
            "overall_status": self.overall_status,
            "stitch_counts": self.stitch_counts,
            "row_transitions": self.row_transitions,
            "consistency": self.consistency,
        }



_CONTEXT_TARGETS = ("each_stitch_around", "each_stitch_across", "remaining")


def _needs_previous_round(instruction) -> bool:
    """True when the instruction count depends on the previous round."""
    return any(
        getattr(op, "into_stitch", None) in _CONTEXT_TARGETS
        for op in getattr(instruction, "operations", []) or []
    )


def _produced_with_context(instruction, previous: int | None) -> int:
    """Count stitches produced, expanding context-dependent operations.

    'inc in each st around' is stored as one increase. Without the previous
    round that is 2, not 12. A joined foundation chain ('ch 40, sl st to
    join') counts as the chain length. A turning chain does not.
    """
    ops = getattr(instruction, "operations", []) or []
    targets = {getattr(op, "into_stitch", None) for op in ops}
    has_foundation = "foundation" in targets
    needs_context = bool(targets & set(_CONTEXT_TARGETS))
    if not has_foundation and not needs_context and not targets & {"join", "foundation_chain"}:
        return instruction.total_stitches_produced
    if needs_context and previous is None and not has_foundation:
        return instruction.total_stitches_produced

    from ..model.stitch import STITCH_CONSUMPTION, STITCH_PRODUCTION

    remaining = 0 if previous is None else previous
    total = 0
    for op in ops:
        target = getattr(op, "into_stitch", None)
        if target == "foundation":
            total += op.count
            remaining = op.count
            continue
        if target in ("join", "foundation_chain"):
            continue
        if target in _CONTEXT_TARGETS:
            per = STITCH_PRODUCTION.get(op.stitch_type, 1)
            total += remaining * per
            remaining = 0
            continue
        per = STITCH_PRODUCTION.get(op.stitch_type, 1)
        cons = STITCH_CONSUMPTION.get(op.stitch_type, 1)
        total += op.count * per
        remaining -= op.count * cons
    return total


def validate_pattern(pattern_input, strict=False):
    """
    Validate raw pattern text or a parsed Pattern object and return the
    compatibility ValidationReport expected by legacy callers.
    """

    if isinstance(pattern_input, str):
        pattern_text = pattern_input
    else:
        pattern_text = getattr(pattern_input, "source_text", None)

    if not isinstance(pattern_text, str):
        raise TypeError(
            "validate_pattern expects pattern text or a parsed Pattern with source_text"
        )

    result = PatternValidator().validate(pattern_text)

    errors = [item.message for item in result.errors]
    warnings = [item.message for item in result.warnings]

    # Compatibility check for stated stitch counts.
    # The compiler pipeline validates spatial consumption, while the legacy
    # suite also expects internal counts such as "(sc, inc) x 7 (18)" to fail
    # because the operations produce 21 stitches, not 18.
    # "each st around" / "remaining" are resolved from the previous round
    # instead of the placeholder count stored on the operation.
    try:
        from ..parser.parser import parse_pattern

        parsed = (
            pattern_input
            if not isinstance(pattern_input, str)
            else parse_pattern(pattern_text)
        )
        if parsed.pieces and len(parsed.pieces) > 1:
            groups = [
                piece.rounds or piece.rows
                for piece in parsed.pieces
                if piece.rounds or piece.rows
            ]
        else:
            groups = [parsed.rounds or parsed.rows]

        for rows_or_rounds in groups:
            previous = None

            for item in rows_or_rounds:
                produced_this_round = 0
                available = previous
                for instruction in item.instructions:
                    computed = _produced_with_context(instruction, available)
                    produced_this_round += computed
                    if _needs_previous_round(instruction):
                        available = 0
                    elif available is not None:
                        available -= instruction.total_stitches_consumed

                    stated = getattr(instruction, "stated_stitch_count", None)
                    if stated is None:
                        continue
                    if computed != stated:
                        number = getattr(item, "round_number", getattr(item, "row_number", "?"))
                        plain = (
                            _needs_previous_round(instruction)
                            and previous is not None
                            and not any(
                                getattr(getattr(op, "stitch_type", None), "value", "")
                                in ("increase", "decrease")
                                for op in instruction.operations
                            )
                        )
                        if plain:
                            message = (
                                f"Round/row {number}: plain round received {previous} stitches "
                                f"and has no increase or decrease, but states {stated}."
                            )
                        else:
                            message = (
                                f"Round/row {number}: "
                                f"stated {stated} stitches but operations produce {computed}"
                            )
                        if message not in errors:
                            errors.append(message)
                previous = produced_this_round
    except Exception:
        # The compiler result remains authoritative if legacy parsing is
        # unavailable for an unusual input.
        pass

    try:
        from .joins import join_interface_errors

        for message in join_interface_errors(pattern_text):
            if message not in errors:
                errors.append(message)
    except Exception:
        pass

    try:
        from .audit_rules import audit_findings

        audit_errors, audit_warnings = audit_findings(pattern_text)
        for message in audit_errors:
            if message not in errors:
                errors.append(message)
        for message in audit_warnings:
            if message not in warnings:
                warnings.append(message)
    except Exception:
        pass

    # Keep the score useful for legacy callers.
    if errors:
        score = max(0, 100 - min(100, len(errors) * 25))
        status = "ERROR"
    elif warnings:
        score = 90
        status = "PASS_WITH_WARNINGS"
    else:
        score = 100
        status = "PASS"

    # AI and suggestion consumers expect error.message, not plain strings.
    error_objects = [
        item if hasattr(item, "message") else _CompatFinding(str(item))
        for item in errors
    ]
    warning_objects = [
        item if hasattr(item, "message") else _CompatFinding(str(item), "warning")
        for item in warnings
    ]

    report = ValidationReport(
        valid=bool(result.is_valid) and not errors,
        errors=error_objects,
        warnings=warning_objects,
        stitch_count=result.total_stitches,
        score=score,
        overall_status=status,
        stitch_counts=dict(result.stitch_counts),
        consistency=not bool(errors),
    )

    return report
