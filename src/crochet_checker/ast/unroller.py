"""
AST Unroller - Expands nested repeat brackets and 'N times' loops
Converts compact pattern notation into flat sequence of atomic actions
"""
import re
from typing import List, Tuple
from .nodes import InstructionNode, StitchNode


class ASTUnroller:
    """Expands pattern repeats and loops into atomic instructions"""
    
    def __init__(self):
        self.repeat_pattern = re.compile(r'\*([^*]+)\*(?:\s*rep(?:eat)?(?:\s+from\s+\*)?(?:\s+(\d+)\s+times)?|\s+around)?', re.IGNORECASE)
        self.n_times_pattern = re.compile(r'(\d+)\s+times', re.IGNORECASE)
        self.repeat_around_pattern = re.compile(r'rep(?:eat)?\s+around', re.IGNORECASE)
    
    def unroll_round(self, round_text: str, line_number: int = 0, prev_stitch_count: int = 0) -> List[InstructionNode]:
        """Unroll a single round/row into atomic instructions"""
        instructions = []
        
        # Handle nested repeats
        expanded_text = self._expand_nested_repeats(round_text)
        
        # Parse individual instructions
        raw_instructions = self._split_instructions(expanded_text)
        
        for instr_text in raw_instructions:
            instr_text = instr_text.strip()
            if not instr_text:
                continue
            
            # Parse stitch instruction
            stitch_nodes = self._parse_stitch_instruction(instr_text, line_number, prev_stitch_count)
            instructions.extend(stitch_nodes)
        
        return instructions
    
    def _expand_nested_repeats(self, text: str) -> str:
        """Expand all repeat patterns in text"""
        # Keep expanding until no more repeats found
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            expanded = self._expand_single_repeat(text)
            if expanded == text:
                break
            text = expanded
            iteration += 1
        
        return text
    
    def _expand_single_repeat(self, text: str) -> str:
        """Expand a single repeat pattern"""
        match = self.repeat_pattern.search(text)
        if not match:
            return text
        
        repeat_content = match.group(1).strip()
        times_match = self.n_times_pattern.search(text[match.end():])
        
        if times_match:
            times = int(times_match.group(1))
        elif self.repeat_around_pattern.search(text[match.end():]):
            times = 6  # Default for "around" (can be adjusted based on context)
        else:
            times = 1
        
        # Expand the repeat
        expanded = ' '.join([repeat_content] * times)
        
        # Replace in original text
        full_match_end = match.end()
        if times_match:
            full_match_end = match.end() + times_match.end()
        
        result = text[:match.start()] + expanded + text[full_match_end:]
        return result.strip()
    
    def _split_instructions(self, text: str) -> List[str]:
        """Split text into individual instruction segments"""
        # Split by commas, but keep parenthetical groups together
        segments = []
        current = []
        paren_depth = 0
        
        for char in text:
            if char == '(':
                paren_depth += 1
                current.append(char)
            elif char == ')':
                paren_depth -= 1
                current.append(char)
            elif char == ',' and paren_depth == 0:
                segments.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
        
        if current:
            segments.append(''.join(current).strip())
        
        return [s for s in segments if s]
    
    def _parse_stitch_instruction(self, text: str, line_number: int, prev_stitch_count: int) -> List[InstructionNode]:
        """Parse a single stitch instruction into InstructionNode(s)"""
        instructions = []
        text = text.strip()
        
        # Check for turning chain
        turning_chain_match = re.match(r'ch\s+(\d+)\s*(?:\(([^)]+)\))?', text, re.IGNORECASE)
        if turning_chain_match:
            ch_count = int(turning_chain_match.group(1))
            counts_text = turning_chain_match.group(2) or ""
            counts_as = 'counts as' in counts_text.lower()
            
            instructions.append(InstructionNode(
                action="turning_chain",
                stitch_type="ch",
                count=ch_count,
                is_turning_chain=True,
                counts_as_stitch=counts_as,
                line_number=line_number
            ))
            return instructions
        
        # Parse standard stitch instructions
        stitch_pattern = re.compile(
            r'(?:(\d+)\s+)?(sc|dc|hdc|tr|dtr|sl\s*st|ch|picot|skip|sp|st|inc|dec)\s*(?:(?:in|into)\s+(?:next\s+)?(\d+)\s*(?:st|sts|ch|ch\-?sp|space|spaces)?)?',
            re.IGNORECASE
        )
        
        for match in stitch_pattern.finditer(text):
            count = int(match.group(1)) if match.group(1) else 1
            stitch_type = match.group(2).strip().lower()
            target_pos = int(match.group(3)) if match.group(3) else None
            
            instructions.append(InstructionNode(
                action="stitch",
                stitch_type=stitch_type,
                count=count,
                target_position=target_pos,
                line_number=line_number
            ))
        
        # If no stitches parsed, create a generic instruction
        if not instructions and text:
            instructions.append(InstructionNode(
                action="unknown",
                stitch_type="unknown",
                count=1,
                line_number=line_number
            ))
        
        return instructions
    
    def calculate_round_stitch_count(self, instructions: List[InstructionNode], prev_count: int) -> int:
        """Calculate the expected stitch count after executing instructions"""
        count = prev_count
        
        for instr in instructions:
            if instr.action == "stitch":
                if instr.stitch_type in ['inc', 'increase']:
                    count += instr.count
                elif instr.stitch_type in ['dec', 'decrease']:
                    count -= instr.count
                elif instr.stitch_type not in ['skip', 'sl st', 'ch']:
                    # Regular stitches don't change count unless they're increases/decreases
                    pass
            elif instr.action == "turning_chain" and instr.counts_as_stitch:
                count += instr.count
        
        return count


if __name__ == "__main__":
    print("🔄 AST Unroller")
    print("=" * 60)
    
    unroller = ASTUnroller()
    
    # Test repeat expansion
    test_round = "*sc 2, inc* rep 3 times"
    expanded = unroller.unroll_round(test_round, line_number=1, prev_stitch_count=10)
    
    print(f"\nInput: {test_round}")
    print(f"Expanded instructions: {len(expanded)}")
    for i, instr in enumerate(expanded, 1):
        print(f"  {i}. {instr.stitch_type} x{instr.count}")
    
    print("\n✅ AST Unroller working!")

# Legacy compatibility alias.
try:
    Unroller
except NameError:
    Unroller = ASTUnroller


# Legacy compatibility API.
def _legacy_unroll(self, text, *args, **kwargs):
    """
    Legacy text-based unroller.

    Example:
        *sc 2* repeat 3 times
    becomes:
        sc sc sc sc sc sc
    """
    import re

    value = str(text).strip()

    repeat_match = re.search(
        r"\*(.*?)\*\s*repeat\s+(\d+)\s+times",
        value,
        flags=re.IGNORECASE,
    )

    if repeat_match:
        body = repeat_match.group(1).strip()
        count = int(repeat_match.group(2))
        return " ".join([body] * count)

    twice_match = re.search(
        r"\*(.*?)\*\s*(twice|thrice)",
        value,
        flags=re.IGNORECASE,
    )

    if twice_match:
        body = twice_match.group(1).strip()
        count = 2 if twice_match.group(2).lower() == "twice" else 3
        return " ".join([body] * count)

    return value


ASTUnroller.unroll = _legacy_unroll

# Legacy class name.
Unroller = ASTUnroller
