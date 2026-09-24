"""
Parser for crochet pattern instructions.

Converts human-readable crochet pattern text into structured Pattern objects.
This is the most critical component - it must handle the wide variety of
ways crochet patterns are written while preserving the original text.
"""

from __future__ import annotations

import re
from typing import Optional

from ..model.instruction import Instruction, ParsedOperation
from ..model.pattern import ConstructionType, Pattern, PatternMetadata
from ..model.row import Row, Round
from ..model.stitch import ABBREVIATION_MAP, StitchType
from .grammar import (
    EACH_AROUND,
    MAGIC_RING_START,
    NEXT_N,
    REPEAT_BLOCK,
    REMAINING,
    STATED_COUNT,
    is_row_header,
)


class ParseError(Exception):
    """Error during pattern parsing."""

    def __init__(self, message: str, source_text: str = "", position: int = 0):
        self.source_text = source_text
        self.position = position
        super().__init__(message)


class CrochetParser:
    """
    Parses crochet pattern text into structured Pattern objects.

    The parser works in three stages:
    1. Split the pattern into lines and identify row/round headers
    2. Parse each instruction into structured operations
    3. Assemble the complete Pattern object
    """

    def __init__(self) -> None:
        self.abbreviations: dict[str, StitchType] = dict(
            ABBREVIATION_MAP.get_all_abbreviations()
        )
        self.warnings: list[str] = []

    def parse(self, text: str) -> Pattern:
        """
        Parse a complete crochet pattern from text.

        Args:
            text: The full pattern text

        Returns:
            A structured Pattern object
        """
        self.warnings = []
        lines = self._split_into_lines(text)
        metadata, yarn, hook, gauge, lines = self._extract_metadata(lines)

        # Determine if pattern uses rows or rounds
        construction = self._detect_construction(lines)

        # Parse each row/round
        pattern = Pattern(
            metadata=metadata,
            source_text=text,
            construction=construction,
            yarn=yarn,
            hook=hook,
            gauge=gauge,
        )

        if construction == ConstructionType.IN_THE_ROUND or construction == ConstructionType.JOINED_ROUNDS:
            pattern.rounds = self._parse_rounds(lines)
        else:
            pattern.rows = self._parse_rows(lines)

        # Set notes and finishing from metadata extraction
        pattern.notes = getattr(self, '_parsed_notes', [])
        pattern.finishing = getattr(self, '_parsed_finishing', [])

        # Detect and populate pieces for multi-piece patterns
        from .parser import detect_pattern_pieces
        piece_boundaries = detect_pattern_pieces(text)
        if piece_boundaries and len(piece_boundaries) > 1:
            # Multi-piece pattern detected
            from ..model.pattern import PatternPiece
            
            # Parse each piece separately
            text_lines = text.split('\n')
            
            for piece_info in piece_boundaries:
                # Extract lines for this piece
                start_line = piece_info['start_line']
                end_line = piece_info['end_line']
                piece_lines = text_lines[start_line:end_line]
                
                # Filter to only content lines (rounds/rows)
                piece_content_lines = []
                for line in piece_lines:
                    is_header, _, _, _, _ = is_row_header(line)
                    if is_header or self._looks_like_instruction(line):
                        piece_content_lines.append(line)
                
                # Parse rounds/rows for this piece
                if construction == ConstructionType.IN_THE_ROUND or construction == ConstructionType.JOINED_ROUNDS:
                    piece_rounds = self._parse_rounds(piece_content_lines)
                    piece = PatternPiece(
                        name=piece_info['name'],
                        make_count=piece_info['make_count'],
                        rounds=piece_rounds,
                    )
                else:
                    piece_rows = self._parse_rows(piece_content_lines)
                    piece = PatternPiece(
                        name=piece_info['name'],
                        make_count=piece_info['make_count'],
                        rows=piece_rows,
                    )
                
                pattern.pieces.append(piece)

        return pattern

    def _split_into_lines(self, text: str) -> list[str]:
        """Split pattern text into non-empty lines."""
        lines = []
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped:
                lines.append(stripped)
        return lines

    def _extract_metadata(self, lines: list[str]) -> tuple[PatternMetadata, Optional[Yarn], Optional[Hook], Optional[Gauge], list[str]]:
        """Extract and remove metadata lines (title, materials, etc.)."""
        from ..model.yarn import Yarn, Hook, Gauge
        
        metadata = PatternMetadata()
        yarn: Optional[Yarn] = None
        hook: Optional[Hook] = None
        gauge: Optional[Gauge] = None
        content_lines: list[str] = []
        notes: list[str] = []
        finishing: list[str] = []
        
        # Track if we've seen any round/row instructions yet
        seen_instruction = False
        in_notes = False
        in_finishing = False
        
        for i, line in enumerate(lines):
            lower = line.lower().strip()
            
            # Check if this is a round/row header
            is_header, _, _, _, _ = is_row_header(line)
            
            if is_header:
                seen_instruction = True
                content_lines.append(line)
                continue
            
            # After instructions start, collect notes/finishing
            if seen_instruction:
                if lower.startswith("finish") or lower.startswith("assembly") or lower.startswith("sew"):
                    in_finishing = True
                    in_notes = False
                if in_finishing:
                    finishing.append(line)
                elif lower.startswith("note"):
                    in_notes = True
                    in_finishing = False
                elif in_notes:
                    notes.append(line)
                else:
                    content_lines.append(line)
                continue
            
            # Before instructions - parse metadata
            # Title - first non-metadata line
            if i == 0 and not self._is_metadata_line(line):
                metadata.title = line.strip()
                continue
            
            # Difficulty
            if lower.startswith("difficulty:"):
                metadata.difficulty = line.split(":", 1)[1].strip()
                continue
            
            # Category
            if lower.startswith("category:"):
                metadata.category = line.split(":", 1)[1].strip()
                continue
            
            # Yarn
            if lower.startswith("yarn:"):
                yarn_text = line.split(":", 1)[1].strip()
                yarn = self._parse_yarn(yarn_text)
                continue
            
            # Hook
            if lower.startswith("hook:"):
                hook_text = line.split(":", 1)[1].strip()
                hook = self._parse_hook(hook_text)
                continue
            
            # Gauge
            if lower.startswith("gauge:"):
                gauge_text = line.split(":", 1)[1].strip()
                gauge = self._parse_gauge(gauge_text)
                continue
            
            # Designer
            if lower.startswith("designer:") or lower.startswith("design:"):
                metadata.designer = line.split(":", 1)[1].strip()
                continue
            
            # Description - line after title that isn't metadata
            if metadata.title and not metadata.description and not self._is_metadata_line(line):
                if not is_header and not self._looks_like_instruction(line):
                    metadata.description = line.strip()
                    continue
            
            # If nothing matched, add as content
            if self._looks_like_instruction(line) or is_header:
                content_lines.append(line)
        
        metadata_dict = metadata.model_dump()
        metadata_dict["notes"] = notes
        final_metadata = PatternMetadata(**{k: v for k, v in metadata_dict.items() if k in PatternMetadata.model_fields})
        # Set source_text
        final_metadata = metadata  # Keep the original with all parsed fields
        
        # Detect section headers (HEAD, BODY, EARS, etc.)
        section_headers = []
        for i, line in enumerate(content_lines):
            # Match patterns like "HEAD (make 1)", "BODY:", "EARS (make 2)"
            if re.match(r'^[A-Z][A-Z\s]+\s*(\(make\s+\d+\))?\s*:?$', line.strip()):
                section_headers.append((i, line.strip()))
        
        # Store for validator use
        self._section_headers = section_headers
        
        # Store notes/finishing for later
        self._parsed_notes = notes
        self._parsed_finishing = finishing
        
        return metadata, yarn, hook, gauge, content_lines
    
    def _is_metadata_line(self, line: str) -> bool:
        """Check if a line is a metadata line (not a pattern instruction)."""
        lower = line.lower().strip()
        metadata_prefixes = [
            "difficulty:", "category:", "yarn:", "hook:", "gauge:",
            "designer:", "design:", "size:", "finished size:",
            "materials:", "notes:", "abbreviation",
        ]
        return any(lower.startswith(p) for p in metadata_prefixes)
    
    def _parse_yarn(self, text: str) -> Yarn:
        """Parse yarn information from text."""
        from ..model.yarn import Yarn
        yarn = Yarn()
        text_lower = text.lower()
        
        # Try to extract weight
        weight_patterns = {
            "lace": "lace", "fingering": "fingering", "sock": "fingering",
            "sport": "sport", "dk": "dk", "double knit": "dk",
            "worsted": "worsted", "aran": "worsted", "afghan": "aran",
            "bulky": "bulky", "chunky": "bulky",
            "super bulky": "super_bulky", "super bulky": "super_bulky",
            "jumbo": "jumbo",
            "#0": "lace", "#1": "fingering", "#2": "sport", "#3": "dk",
            "#4": "worsted", "#5": "bulky", "#6": "super_bulky", "#7": "jumbo",
        }
        for pattern, weight in weight_patterns.items():
            if pattern in text_lower:
                yarn.weight = weight
                break
        
        # Extract hook size if mentioned in yarn line
        hook_match = re.search(r'(\d+\.?\d*)\s*mm', text)
        if hook_match:
            yarn.hook_size_mm = float(hook_match.group(1))
        
        # Use full text as name if no weight found
        if not yarn.weight:
            yarn.name = text.strip()
        else:
            yarn.name = text.strip()
        
        return yarn
    
    def _parse_hook(self, text: str) -> Hook:
        """Parse hook information from text."""
        from ..model.yarn import Hook
        hook = Hook()
        
        # Extract mm size
        mm_match = re.search(r'(\d+\.?\d*)\s*mm', text)
        if mm_match:
            hook.size_mm = float(mm_match.group(1))
        
        # Extract US size
        us_match = re.search(r'US\s+([A-G]-?\d+|\d+)', text, re.IGNORECASE)
        if us_match:
            hook.us_size = us_match.group(1)
        
        return hook
    
    def _parse_gauge(self, text: str) -> Gauge:
        """Parse gauge information from text."""
        from ..model.yarn import Gauge
        gauge = Gauge()
        
        # Try "N sts x N rows = X in/cm"
        match = re.search(r'(\d+)\s*sts?\s*[x×]\s*(\d+)\s*rows?\s*=\s*(\d+\.?\d*)\s*(in|cm|inch)', text, re.IGNORECASE)
        if match:
            gauge.stitches_per_unit = int(match.group(1))
            gauge.rows_per_unit = int(match.group(2))
            gauge.unit_size = float(match.group(3))
            gauge.unit = match.group(4).lower()
            if gauge.unit in ("in", "inch"):
                gauge.unit = "in"
            return gauge
        
        # Try "N sts = X in/cm"
        match = re.search(r'(\d+)\s*sts?\s*(?:around)?\s*(?:measures)?\s*(?:about)?\s*(\d+\.?\d*)\s*(mm|in|cm)', text, re.IGNORECASE)
        if match:
            gauge.stitches_per_unit = int(match.group(1))
            gauge.unit_size = float(match.group(2))
            gauge.unit = match.group(3).lower()
            gauge.rows_per_unit = 1
            return gauge
        
        return gauge

    def _detect_construction(self, lines: list[str]) -> ConstructionType:
        """Detect whether the pattern uses rows or rounds."""
        round_indicators = 0
        row_indicators = 0

        for line in lines:
            lower = line.lower()
            is_header, header_type, _, _, _ = is_row_header(line)
            if is_header:
                if header_type.lower() in ("round", "rnd"):
                    round_indicators += 1
                elif header_type.lower() == "row":
                    row_indicators += 1
            if "magic ring" in lower or "mr" in lower.lower().split():
                round_indicators += 2
            if "around" in lower:
                round_indicators += 1
            if "turn" in lower:
                row_indicators += 1

        if round_indicators > row_indicators:
            return ConstructionType.IN_THE_ROUND
        return ConstructionType.FLAT

    def _parse_rounds(self, lines: list[str]) -> list[Round]:
        """Parse pattern lines into Round objects."""
        rounds: list[Round] = []
        current_round: Optional[Round] = None

        for line in lines:
            is_header, header_type, number, rest, end_number = is_row_header(line)

            if is_header and header_type.lower() in ("round", "rnd", "r"):
                if current_round is not None:
                    rounds.append(current_round)

                # Handle range notation (e.g., "Round 11-18: sc in each st around")
                if end_number > number:
                    # Create copies for each round in the range
                    for n in range(number, end_number + 1):
                        instructions = self._parse_instruction_text(rest, line)
                        rounds.append(Round(
                            round_number=n,
                            instructions=instructions,
                            source_text=line,
                        ))
                    current_round = None
                else:
                    instructions = self._parse_instruction_text(rest, line)
                    current_round = Round(
                        round_number=number,
                        instructions=instructions,
                        source_text=line,
                    )
            elif current_round is not None:
                # Continuation of current round
                additional = self._parse_instruction_text(line, line)
                current_round.instructions.extend(additional)
            else:
                # Try to parse as instruction anyway (first round might not have header)
                if self._looks_like_instruction(line):
                    instructions = self._parse_instruction_text(line, line)
                    if instructions:
                        current_round = Round(
                            round_number=1,
                            instructions=instructions,
                            source_text=line,
                        )

        if current_round is not None:
            rounds.append(current_round)

        return rounds

    def _parse_rows(self, lines: list[str]) -> list[Row]:
        """Parse pattern lines into Row objects."""
        rows: list[Row] = []
        current_row: Optional[Row] = None

        for line in lines:
            is_header, header_type, number, rest, end_number = is_row_header(line)

            if is_header and header_type.lower() == "row":
                if current_row is not None:
                    rows.append(current_row)

                # Handle range notation
                if end_number > number:
                    for n in range(number, end_number + 1):
                        instructions = self._parse_instruction_text(rest, line)
                        rows.append(Row(
                            row_number=n,
                            instructions=instructions,
                            source_text=line,
                        ))
                    current_row = None
                else:
                    instructions = self._parse_instruction_text(rest, line)
                    current_row = Row(
                        row_number=number,
                        instructions=instructions,
                        source_text=line,
                    )
            elif current_row is not None:
                additional = self._parse_instruction_text(line, line)
                current_row.instructions.extend(additional)
            else:
                if self._looks_like_instruction(line):
                    instructions = self._parse_instruction_text(line, line)
                    if instructions:
                        current_row = Row(
                            row_number=1,
                            instructions=instructions,
                            source_text=line,
                        )

        if current_row is not None:
            rows.append(current_row)

        return rows

    def _looks_like_instruction(self, line: str) -> bool:
        """Check if a line looks like a crochet instruction."""
        lower = line.lower()
        # Skip metadata-like lines
        if any(lower.startswith(x) for x in [
            "materials:", "yarn:", "hook:", "gauge:", "difficulty:", "size:",
            "notes:", "finished", "this pattern",
        ]):
            return False
        # Skip lines that look like titles (no stitch abbreviations and no row/round prefix)
        if not re.match(r'^(row|round|rnd)\s+\d', lower):
            # If it doesn't start with a row/round header, check for stitch abbreviations
            # Use word boundaries to avoid matching "ch" in "crochet" etc.
            abbrev_patterns = [
                r'\bsc\b', r'\bdc\b', r'\bhdc\b', r'\btr\b', r'\bch\s+\d',
                r'\binc\b', r'\bdec\b', r'\bsl\s+st\b', r'\bmr\b',
                r'\bmagic\s+ring\b', r'\bmagic\s+circle\b',
            ]
            has_abbrev = any(re.search(p, lower) for p in abbrev_patterns)
            if not has_abbrev:
                return False
            return True
        return True

    def _parse_instruction_text(self, text: str, source_line: str) -> list[Instruction]:
        """Parse a piece of instruction text into Instruction objects."""
        text = text.strip()
        if not text:
            return []

        # Split on sentence boundaries (periods followed by space and new instruction)
        parts = self._split_instruction_parts(text)
        instructions: list[Instruction] = []

        for part in parts:
            part = part.strip()
            if not part:
                continue
            inst = self._parse_single_instruction(part)
            if inst:
                instructions.append(inst)

        return instructions

    def _split_instruction_parts(self, text: str) -> list[str]:
        """
        Split an instruction text into separate parts.

        Handles semicolons, periods between instructions, and "then" connections.
        """
        # Remove trailing period
        text = text.rstrip(".")

        # Split on period followed by space and what looks like a new instruction
        parts = re.split(r'\.\s+(?=\d|\(|sc|dc|hdc|tr|ch|inc|dec|sl|skip|join|fasten)', text, flags=re.IGNORECASE)

        if len(parts) == 1:
            # Try splitting on semicolons
            parts = re.split(r'\s*;\s*', text)

        return [p.strip() for p in parts if p.strip()]

    def _parse_single_instruction(self, text: str) -> Optional[Instruction]:
        """Parse a single instruction string into an Instruction object."""
        text = text.strip()
        if not text:
            return None

        # Extract stated count if present
        clean_text, stated_count = self._extract_stated_count(text)

        instruction = Instruction(
            source_text=text,
            normalized_text=clean_text,
            stated_stitch_count=stated_count,
        )

        # Try different parsing strategies in order of specificity

        # Strategy 1: Magic ring start - "6 sc into magic ring"
        if self._try_parse_magic_ring(clean_text, instruction):
            return instruction

        # Strategy 2: Repeat block - "(sc, inc) x 6"
        if self._try_parse_repeat_block(clean_text, instruction):
            return instruction

        # Strategy 3: "sc in each st around"
        if self._try_parse_each_around(clean_text, instruction):
            return instruction

        # Strategy 4: "sc in next N sts"
        if self._try_parse_next_n(clean_text, instruction):
            return instruction

        # Strategy 5: Generic count + stitch - "3 dc", "2 sc"
        if self._try_parse_count_stitch(clean_text, instruction):
            return instruction

        # Strategy 6: Chain - "ch 5"
        if self._try_parse_chain(clean_text, instruction):
            return instruction

        # Strategy 7: Remaining stitches - "sc in each remaining st"
        if self._try_parse_remaining(clean_text, instruction):
            return instruction

        # Strategy 8: Stitch x count - "dec x 6", "inc x 3"
        if self._try_parse_stitch_times_count(clean_text, instruction):
            return instruction

        # Strategy 9: Generic parsing - try to find any recognizable operations
        if self._try_parse_generic(clean_text, instruction):
            return instruction

        # If nothing worked, mark as ambiguous
        instruction.is_ambiguous = True
        instruction.parse_warnings.append(f"Could not parse: '{text}'")
        instruction.confidence = 0.0
        return instruction

    def _extract_stated_count(self, text: str) -> tuple[str, Optional[int]]:
        """Extract stated stitch count from end of instruction."""
        match = STATED_COUNT.search(text.strip())
        if match:
            count = int(match.group(1))
            clean = text[:match.start()].strip().rstrip(",")
            return clean, count
        return text, None

    def _try_parse_magic_ring(self, text: str, instruction: Instruction) -> bool:
        """Try to parse 'N sc into magic ring' style instructions."""
        match = MAGIC_RING_START.match(text)
        if not match:
            # Also try just "N sc in MR"
            match2 = re.match(
                r"(\d+)\s+(sc|hdc|dc|tr)\s+(?:in|into)\s+MR",
                text, re.IGNORECASE,
            )
            if not match2:
                return False
            match = match2

        count = int(match.group(1))
        stitch = self._resolve_stitch(match.group(2))

        instruction.operations = [
            ParsedOperation(stitch_type=StitchType.MAGIC_RING, count=1),
            ParsedOperation(stitch_type=stitch, count=count),
        ]
        instruction.confidence = 0.95
        return True

    def _try_parse_repeat_block(self, text: str, instruction: Instruction) -> bool:
        """Try to parse '(stuff) x N' style instructions."""
        match = REPEAT_BLOCK.search(text)
        if not match:
            return False

        repeat_text = match.group(1)
        repeat_count = int(match.group(2))

        # Parse the repeat unit
        unit_ops = self._parse_operation_sequence(repeat_text)
        if not unit_ops:
            return False

        instruction.is_repeat_block = True
        instruction.repeat_unit = unit_ops
        instruction.repeat_count = repeat_count

        # Also store expanded operations
        instruction.operations = []
        for _ in range(repeat_count):
            for op in unit_ops:
                instruction.operations.append(
                    op.model_copy(update={"is_part_of_repeat": True, "repeat_count": repeat_count})
                )

        instruction.confidence = 0.9
        return True

    def _try_parse_each_around(self, text: str, instruction: Instruction) -> bool:
        """Try to parse 'sc in each st around' style instructions."""
        match = EACH_AROUND.match(text)
        if not match:
            return False

        stitch = self._resolve_stitch(match.group(1))

        # "each st around" means we don't know the exact count from the text
        # The count depends on the previous round's stitch count
        instruction.operations = [
            ParsedOperation(
                stitch_type=stitch,
                count=1,  # Will be expanded based on context
                into_stitch="each_stitch_around",
            )
        ]
        instruction.confidence = 0.85
        return True

    def _try_parse_next_n(self, text: str, instruction: Instruction) -> bool:
        """Try to parse 'sc in next N sts' style instructions."""
        match = NEXT_N.match(text)
        if not match:
            return False

        stitch = self._resolve_stitch(match.group(1))
        count = int(match.group(2))

        instruction.operations = [
            ParsedOperation(stitch_type=stitch, count=count, into_stitch="next")
        ]
        instruction.confidence = 0.9
        return True

    def _try_parse_count_stitch(self, text: str, instruction: Instruction) -> bool:
        """Try to parse 'N stitch' style instructions."""
        match = re.match(
            r"(\d+)\s+(ch|sl\s*st|sc|hdc|dc|tr|inc|dec|sc2tog|dc2tog)",
            text, re.IGNORECASE,
        )
        if not match:
            return False

        count = int(match.group(1))
        stitch = self._resolve_stitch(match.group(2))

        instruction.operations = [
            ParsedOperation(stitch_type=stitch, count=count)
        ]
        instruction.confidence = 0.9
        return True

    def _try_parse_chain(self, text: str, instruction: Instruction) -> bool:
        """Try to parse 'ch N' style instructions."""
        match = re.match(r"ch\s+(\d+)", text, re.IGNORECASE)
        if not match:
            return False

        count = int(match.group(1))
        instruction.operations = [
            ParsedOperation(stitch_type=StitchType.CHAIN, count=count)
        ]
        instruction.confidence = 0.95
        return True

    def _try_parse_remaining(self, text: str, instruction: Instruction) -> bool:
        """Try to parse 'stitch in remaining sts' style instructions."""
        match = REMAINING.match(text)
        if not match:
            return False

        stitch = self._resolve_stitch(match.group(1))
        instruction.operations = [
            ParsedOperation(
                stitch_type=stitch,
                count=1,  # Will be resolved based on context
                into_stitch="remaining",
            )
        ]
        instruction.confidence = 0.8
        return True

    def _try_parse_stitch_times_count(self, text: str, instruction: Instruction) -> bool:
        """Try to parse 'stitch x N' style instructions like 'dec x 6'."""
        match = re.match(
            r"(ch|sl\s*st|sc|hdc|dc|tr|inc|dec|sc2tog|dc2tog)\s*[x×]\s*(\d+)",
            text, re.IGNORECASE,
        )
        if not match:
            return False

        stitch = self._resolve_stitch(match.group(1))
        count = int(match.group(2))

        instruction.operations = [
            ParsedOperation(stitch_type=stitch, count=count)
        ]
        instruction.confidence = 0.9
        return True

    def _try_parse_generic(self, text: str, instruction: Instruction) -> bool:
        """Generic fallback parser - find any recognizable operations."""
        ops: list[ParsedOperation] = []

        # Try to find any stitch abbreviations with optional counts
        pattern = re.compile(
            r"(\d+)?\s*(ch|sl\s*st|sc|hdc|dc|tr|inc|dec|sc2tog|dc2tog)",
            re.IGNORECASE,
        )

        for match in pattern.finditer(text):
            count = int(match.group(1)) if match.group(1) else 1
            stitch = self._resolve_stitch(match.group(2))
            ops.append(ParsedOperation(stitch_type=stitch, count=count))

        if ops:
            instruction.operations = ops
            instruction.confidence = 0.6
            instruction.parse_warnings.append("Parsed with generic fallback - may be incomplete")
            return True

        return False

    def _parse_operation_sequence(self, text: str) -> list[ParsedOperation]:
        """Parse a sequence of operations (typically from within parentheses)."""
        ops: list[ParsedOperation] = []

        # Split on commas
        parts = [p.strip() for p in text.split(",")]

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Try "N stitch" pattern
            match = re.match(r"(\d+)\s+(.+)", part)
            if match:
                count = int(match.group(1))
                rest = match.group(2).strip()
                stitch = self._resolve_stitch_from_text(rest)
                if stitch:
                    ops.append(ParsedOperation(stitch_type=stitch, count=count))
                    continue

            # Try just a stitch abbreviation
            stitch = self._resolve_stitch_from_text(part)
            if stitch:
                ops.append(ParsedOperation(stitch_type=stitch, count=1))

        return ops

    def _resolve_stitch(self, abbrev: str) -> StitchType:
        """Resolve an abbreviation string to a StitchType."""
        normalized = abbrev.lower().strip()

        # Direct mapping
        direct = {
            "ch": StitchType.CHAIN,
            "sl st": StitchType.SLIP_STITCH,
            "slst": StitchType.SLIP_STITCH,
            "sc": StitchType.SINGLE_CROCHET,
            "hdc": StitchType.HALF_DOUBLE_CROCHET,
            "dc": StitchType.DOUBLE_CROCHET,
            "tr": StitchType.TREBLE_CROCHET,
            "inc": StitchType.INCREASE,
            "2sc": StitchType.INCREASE,
            "dec": StitchType.DECREASE,
            "sc2tog": StitchType.DECREASE,
            "dc2tog": StitchType.DECREASE,
        }

        if normalized in direct:
            return direct[normalized]

        result = ABBREVIATION_MAP.lookup(normalized)
        if result:
            return result

        self.warnings.append(f"Unknown stitch abbreviation: '{abbrev}'")
        return StitchType.UNKNOWN

    def _resolve_stitch_from_text(self, text: str) -> Optional[StitchType]:
        """Try to resolve a stitch type from arbitrary text."""
        text = text.lower().strip()

        # Direct abbreviation match
        abbrevs = {
            "ch": StitchType.CHAIN,
            "sl st": StitchType.SLIP_STITCH,
            "sc": StitchType.SINGLE_CROCHET,
            "hdc": StitchType.HALF_DOUBLE_CROCHET,
            "dc": StitchType.DOUBLE_CROCHET,
            "tr": StitchType.TREBLE_CROCHET,
            "inc": StitchType.INCREASE,
            "dec": StitchType.DECREASE,
        }

        if text in abbrevs:
            return abbrevs[text]

        # Try partial match
        for abbrev, stitch_type in abbrevs.items():
            if abbrev in text:
                return stitch_type

        return None


def parse_pattern(text: str) -> Pattern:
    """Convenience function to parse a pattern from text."""
    parser = CrochetParser()
    return parser.parse(text)


def parse_instruction(text: str) -> Instruction:
    """Parse a single instruction."""
    parser = CrochetParser()
    result = parser._parse_single_instruction(text)
    if result is None:
        return Instruction(
            source_text=text,
            is_ambiguous=True,
            parse_warnings=["Could not parse instruction"],
            confidence=0.0,
        )
    return result


def detect_pattern_pieces(text: str) -> list[dict]:
    """
    Detect piece boundaries in multi-piece patterns.
    
    Returns list of dicts with:
    - name: piece name (e.g., "HEAD", "ARMS")
    - make_count: how many to make (e.g., 2)
    - start_line: line index where piece starts
    - end_line: line index where piece ends
    """
    import re
    
    lines = text.split('\n')
    pieces = []
    current_piece = None
    
    # Words that should NOT be treated as piece names
    non_piece_words = {'FO', 'FINISH', 'ASSEMBLY', 'NOTES', 'MATERIALS'}
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Match patterns like "HEAD (make 1)", "ARMS (make 2)", "BODY:"
        match = re.match(r'^([A-Z][A-Z\s,/&]+?)\s*(?:\(make\s+(\d+)\))?\s*:?\s*$', line_stripped)
        
        if match:
            name = match.group(1).strip()
            
            # Skip if this is not a real piece name
            if name in non_piece_words or len(name) < 2:
                continue
            
            # Save previous piece
            if current_piece:
                current_piece['end_line'] = i
                pieces.append(current_piece)
            
            # Start new piece
            make_count = int(match.group(2)) if match.group(2) else 1
            current_piece = {
                'name': name,
                'make_count': make_count,
                'start_line': i + 1,  # +1 to skip the header line
                'end_line': len(lines)  # Default to end
            }
    
    # Add last piece
    if current_piece:
        pieces.append(current_piece)
    
    return pieces
