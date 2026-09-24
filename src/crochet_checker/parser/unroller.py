"""
Unroller - Recursively expands nested brackets and multipliers
"""
import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class RepeatNode:
    """Represents a repeat block"""
    count: int
    content: str
    children: List['RepeatNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class Unroller:
    """Recursively expands nested brackets and multipliers"""
    
    def __init__(self):
        self.bracket_pattern = re.compile(r'\*([^*]+)\*(?:\s*(?:repeat|rep)\s*(\d+)?\s*times?|\s*around)?', re.IGNORECASE)
        self.multiplier_pattern = re.compile(r'(\d+)\s*times?', re.IGNORECASE)
        self.paren_pattern = re.compile(r'\(([^()]+)\)')
    
    def unroll(self, instruction_text: str, repeat_count: Optional[int] = None) -> str:
        """Unroll all repeat blocks in instruction text"""
        result = instruction_text
        
        # Keep unrolling until no more repeats found
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            new_result = self._unroll_single_level(result, repeat_count)
            if new_result == result:
                break
            result = new_result
            iteration += 1
        
        return result
    
    def _unroll_single_level(self, text: str, default_repeat: Optional[int] = None) -> str:
        """Unroll one level of repeats"""
        result = text
        
        # Find repeat blocks
        for match in self.bracket_pattern.finditer(text):
            repeat_content = match.group(1).strip()
            
            # Determine repeat count
            if match.group(2):
                count = int(match.group(2))
            elif 'around' in match.group(0).lower():
                count = default_repeat or 6  # Default for "around"
            else:
                count = 1
            
            # Recursively unroll nested repeats
            unrolled_content = self._unroll_single_level(repeat_content, count)
            
            # Expand the repeat
            expanded = ' '.join([unrolled_content] * count)
            
            # Replace in result
            result = result.replace(match.group(0), expanded)
        
        return result
    
    def parse_repeat_tree(self, instruction_text: str) -> List[RepeatNode]:
        """Parse instruction text into repeat tree structure"""
        nodes = []
        
        # Find all repeat blocks
        for match in self.bracket_pattern.finditer(instruction_text):
            content = match.group(1).strip()
            
            # Determine count
            if match.group(2):
                count = int(match.group(2))
            elif 'around' in match.group(0).lower():
                count = 6
            else:
                count = 1
            
            # Parse nested repeats
            children = self.parse_repeat_tree(content)
            
            nodes.append(RepeatNode(
                count=count,
                content=content,
                children=children
            ))
        
        return nodes
    
    def validate_corners(self, instruction_text: str, canvas_queue: List[str]) -> List[str]:
        """Validate corner spaces match between instruction and canvas"""
        errors = []
        
        # Extract corner expectations from instruction
        corner_pattern = re.compile(r'ch-(\d+)\s*sp', re.IGNORECASE)
        instruction_corners = corner_pattern.findall(instruction_text)
        
        # Extract corner spaces from canvas
        canvas_corners = []
        for item in canvas_queue:
            match = re.match(r'ch_sp_(\d+)', item)
            if match:
                canvas_corners.append(int(match.group(1)))
        
        # Validate matches
        for i, expected in enumerate(instruction_corners):
            expected_size = int(expected)
            if i >= len(canvas_corners):
                errors.append(f"Expected ch-{expected_size} sp at position {i}, but canvas ended")
            elif canvas_corners[i] != expected_size:
                errors.append(
                    f"CornerMismatchError: Expected ch-{expected_size} sp, "
                    f"but found ch-{canvas_corners[i]} sp at position {i}"
                )
        
        return errors
    
    def calculate_stitch_count(self, instruction_text: str, glossary: dict = None) -> int:
        """Calculate total stitch count from unrolled instruction"""
        unrolled = self.unroll(instruction_text)
        
        # Count stitches
        stitch_pattern = re.compile(r'(\d+)\s*(sc|dc|hdc|tr|sl\s*st|ch)', re.IGNORECASE)
        total = 0
        
        for match in stitch_pattern.finditer(unrolled):
            count = int(match.group(1))
            stitch_type = match.group(2).lower()
            
            # Check glossary for special stitches
            if glossary and match.group(0) in glossary:
                # Special stitch might have different count
                pass
            
            total += count
        
        return total


if __name__ == "__main__":
    print("🔄 Unroller Test")
    unroller = Unroller()
    
    # Test simple repeat
    test1 = "*1 sc, 2 sc in next st* repeat 3 times"
    result1 = unroller.unroll(test1)
    print(f"Input: {test1}")
    print(f"Output: {result1}")
    print(f"Stitch count: {unroller.calculate_stitch_count(test1)}")
    
    # Test nested repeat
    test2 = "*(*1 sc, 2 sc in next st*) repeat 2 times, 1 sc* repeat around"
    result2 = unroller.unroll(test2, repeat_count=6)
    print(f"\nInput: {test2}")
    print(f"Output: {result2}")
    
    # Test corner validation
    instruction = "1 sc in ch-2 sp, 1 sc in ch-3 sp"
    canvas = ["st_1", "ch_sp_2", "st_2", "ch_sp_3", "st_3"]
    errors = unroller.validate_corners(instruction, canvas)
    print(f"\nCorner validation errors: {errors}")


# ============================================================================
# RecursiveLoopUnroller - Unrolls nested bracket multipliers
# (*[(...) ... (...)]* and "twice" / "N times") into a flat, sequential array
# of atomic operations before validation.
# (Added per 4-pattern audit)
# ============================================================================

@dataclass
class AtomicOperation:
    """Represents a single atomic stitch operation after unrolling."""
    operation: str
    count: int = 1
    original_text: str = ""
    nesting_level: int = 0


class RecursiveLoopUnroller:
    """Recursively unrolls nested repeats into a flat array of atomic operations."""
    
    def __init__(self):
        self.max_recursion_depth = 10
        # All repeat forms share one multiplier suffix:
        #   repeat N times | N times | twice | thrice
        self._multiplier = r'\s*(?:repeat\s*(\d+)\s*times?|(\d+)\s*times?|(twice)|(thrice))?'
        self.repeat_pattern = re.compile(
            r'\*\s*(.*?)\s*\*' + self._multiplier,
            re.IGNORECASE | re.DOTALL
        )
        self.bracket_pattern = re.compile(
            r'\[\s*(.*?)\s*\]' + self._multiplier,
            re.IGNORECASE | re.DOTALL
        )
        self.paren_repeat_pattern = re.compile(
            r'\(\s*(.*?)\s*\)' + self._multiplier,
            re.IGNORECASE | re.DOTALL
        )
        self.atomic_pattern = re.compile(
            r'(\d+)\s+(sc|dc|hdc|tr|sl\s*st|ch)|'
            r'(sc|dc|hdc|tr|sl\s*st|ch)\s+(\d+)|'
            r'(sc|dc|hdc|tr|sl\s*st|ch)',
            re.IGNORECASE
        )
    
    def unroll(self, pattern_text: str) -> List[AtomicOperation]:
        """Unroll all nested repeats into atomic operations."""
        operations: List[AtomicOperation] = []
        self._unroll_recursive(pattern_text, operations, 0)
        return operations
    
    def _unroll_recursive(self, text: str, operations: List[AtomicOperation], depth: int) -> None:
        if depth > self.max_recursion_depth:
            raise RecursionError(f"Maximum recursion depth ({self.max_recursion_depth}) exceeded")
        
        # Try star-repeat, square-bracket, and paren-repeat in priority order
        for pattern in (self.repeat_pattern, self.bracket_pattern, self.paren_repeat_pattern):
            match = pattern.search(text)
            if not match:
                continue
            
            repeat_content = match.group(1)
            repeat_count = self._multiplier_count(match)
            
            before = text[:match.start()]
            after = text[match.end():]
            
            if before.strip():
                self._parse_atomics(before, operations, depth)
            for _ in range(repeat_count):
                self._unroll_recursive(repeat_content, operations, depth + 1)
            if after.strip():
                self._unroll_recursive(after, operations, depth)
            return
        
        # No repeats left -> parse atomics directly
        self._parse_atomics(text, operations, depth)
    
    @staticmethod
    def _multiplier_count(match: re.Match) -> int:
        """Unified multiplier extraction: 'repeat N times' | 'N times' | twice | thrice."""
        if match.group(2):
            return int(match.group(2))
        if match.group(3):
            return int(match.group(3))
        if match.group(4):
            return 2
        if match.group(5):
            return 3
        return 1
    
    def _parse_atomics(self, text: str, operations: List[AtomicOperation], depth: int) -> None:
        segments = re.split(r'[,;]|\s+and\s+', text)
        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue
            
            # "twice"/"thrice"/"N times" multiplier
            times_match = re.search(r'(\d+)\s*times?|twice|thrice', segment, re.IGNORECASE)
            multiplier = 1
            if times_match:
                if 'twice' in segment.lower():
                    multiplier = 2
                elif 'thrice' in segment.lower():
                    multiplier = 3
                else:
                    multiplier = int(times_match.group(1))
                segment = segment[:times_match.start()].strip()
            
            atomics = list(self.atomic_pattern.finditer(segment))
            if not atomics:
                # Unparseable segment -> keep as generic op
                operations.append(AtomicOperation(
                    operation=segment, count=1, original_text=segment, nesting_level=depth
                ))
                continue
            
            for _ in range(multiplier):
                for m in atomics:
                    if m.group(1) and m.group(2):
                        count, st = int(m.group(1)), m.group(2).lower()
                    elif m.group(3) and m.group(4):
                        count, st = int(m.group(4)), m.group(3).lower()
                    else:
                        count, st = 1, m.group(5).lower()
                    operations.append(AtomicOperation(
                        operation=st, count=count, original_text=segment, nesting_level=depth
                    ))
    
    def to_flat_string(self, operations: List[AtomicOperation]) -> str:
        """Convert operations back to a flat instruction string."""
        parts = []
        for op in operations:
            parts.append(f"{op.count} {op.operation}" if op.count > 1 else op.operation)
        return ', '.join(parts)
    
    def count_total_stitches(self, operations: List[AtomicOperation]) -> int:
        """Count total working stitches (chains/slips/skips and noise excluded)."""
        known_stitch = re.compile(r'(?:sc|dc|hdc|tr|dtr)', re.IGNORECASE)
        total = 0
        for op in operations:
            name = op.operation.strip()
            if name.lower() in ('ch', 'sl st', 'skip'):
                continue
            if known_stitch.fullmatch(name):
                total += op.count
        return total
    
    def validate_unrolling(self, original: str, operations: List[AtomicOperation]) -> List[str]:
        """Validate that unrolling preserved the pattern structure."""
        warnings = []
        if not operations:
            warnings.append("No operations found after unrolling")
        if operations:
            max_depth = max(op.nesting_level for op in operations)
            if max_depth > 5:
                warnings.append(f"Deep nesting detected (level {max_depth})")
        for op in operations:
            if op.count > 10:
                warnings.append(f"Large repeat count: {op.count} {op.operation}")
        return warnings


if __name__ == "__main__":
    print("🔄 Unroller Test")
    unroller = Unroller()
    
    test1 = "*1 sc, 2 sc in next st* repeat 3 times"
    result1 = unroller.unroll(test1)
    print(f"Input: {test1}")
    print(f"Output: {result1}")
    print(f"Stitch count: {unroller.calculate_stitch_count(test1)}")
    
    test2 = "*(*1 sc, 2 sc in next st*) repeat 2 times, 1 sc* repeat around"
    result2 = unroller.unroll(test2, repeat_count=6)
    print(f"\nInput: {test2}")
    print(f"Output: {result2}")
    
    instruction = "1 sc in ch-2 sp, 1 sc in ch-3 sp"
    canvas = ["st_1", "ch_sp_2", "st_2", "ch_sp_3", "st_3"]
    errors = unroller.validate_corners(instruction, canvas)
    print(f"\nCorner validation errors: {errors}")
    
    # RecursiveLoopUnroller demo
    print("\n\n🔁 RecursiveLoopUnroller Test")
    ru = RecursiveLoopUnroller()
    ops = ru.unroll("*[sc, 2 dc in next st] repeat 3 times, sc* twice")
    print(f"Atomic operations: {len(ops)}")
    print(f"Flat: {ru.to_flat_string(ops[:12])}")
    print(f"Stitch count: {ru.count_total_stitches(ops)}")
    print(f"Warnings: {ru.validate_unrolling('*[sc, 2 dc] x3, sc* twice', ops)}")
