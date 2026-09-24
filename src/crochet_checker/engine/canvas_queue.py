"""
Canvas Queue - Tracks stitch tops, corner spaces, and spatial pointer
"""
from typing import List, Optional, Dict
from dataclasses import dataclass
from enum import Enum


class StitchStatus(Enum):
    UNTOUCHED = "UNTOUCHED"
    WORKED_INTO = "WORKED_INTO"
    CONSUMED_IN_CLUSTER = "CONSUMED_IN_CLUSTER"
    SKIPPED = "SKIPPED"


@dataclass
class CanvasElement:
    """Represents an element on the canvas (stitch top or space)"""
    element_type: str  # 'st', 'ch_sp'
    index: int
    capacity: int = 1  # For spaces: how many stitches can go in
    status: StitchStatus = StitchStatus.UNTOUCHED
    round_created: int = 0
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def is_workable(self) -> bool:
        """Check if element can be worked into"""
        return self.status == StitchStatus.UNTOUCHED
    
    def consume(self):
        """Mark element as worked into"""
        if self.is_workable():
            self.status = StitchStatus.WORKED_INTO
        else:
            raise ValueError(f"Cannot work into {self.status.value} element")


class CanvasQueue:
    """Sequential ring buffer representing the previous round"""
    
    def __init__(self):
        self.elements: List[CanvasElement] = []
        self.canvas_pointer: int = 0
        self.current_round: int = 0
    
    def initialize_round(self, stitch_count: int, round_number: int = 1):
        """Initialize canvas for a new round"""
        self.elements = []
        self.canvas_pointer = 0
        self.current_round = round_number
        
        # Create stitch elements
        for i in range(stitch_count):
            self.elements.append(CanvasElement(
                element_type='st',
                index=i,
                capacity=1,
                round_created=round_number - 1
            ))
    
    def peek(self) -> Optional[CanvasElement]:
        """Peek at current element without advancing pointer"""
        if self.canvas_pointer < len(self.elements):
            return self.elements[self.canvas_pointer]
        return None
    
    def advance(self, steps: int = 1) -> List[CanvasElement]:
        """Advance pointer and return elements passed"""
        passed = []
        
        for _ in range(steps):
            if self.canvas_pointer < len(self.elements):
                passed.append(self.elements[self.canvas_pointer])
                self.canvas_pointer += 1
            else:
                break
        
        return passed
    
    def move_to(self, position: int) -> bool:
        """Move pointer to specific position"""
        if 0 <= position < len(self.elements):
            self.canvas_pointer = position
            return True
        return False
    
    def get_element_at(self, index: int) -> Optional[CanvasElement]:
        """Get element at specific index"""
        if 0 <= index < len(self.elements):
            return self.elements[index]
        return None
    
    def add_space(self, space_type: str, capacity: int) -> CanvasElement:
        """Add a space element (ch-sp, corner space, etc.)"""
        element = CanvasElement(
            element_type=space_type,
            index=len(self.elements),
            capacity=capacity,
            round_created=self.current_round
        )
        self.elements.append(element)
        return element
    
    def get_unworked(self) -> List[CanvasElement]:
        """Get all unworked elements"""
        return [e for e in self.elements if e.status == StitchStatus.UNTOUCHED]
    
    def check_exhaustion(self) -> Dict:
        """Check if all elements have been worked"""
        unworked = self.get_unworked()
        
        return {
            'exhausted': len(unworked) == 0,
            'unworked_count': len(unworked),
            'unworked_indices': [e.index for e in unworked],
            'total_elements': len(self.elements),
            'worked_count': len(self.elements) - len(unworked)
        }
    
    def validate_backward_traversal(self, target_index: int) -> bool:
        """Validate backward traversal is allowed"""
        if target_index < self.canvas_pointer:
            # Backward traversal requires explicit directive
            return False
        return True
    
    def get_position_info(self) -> Dict:
        """Get current position information"""
        return {
            'pointer': self.canvas_pointer,
            'total_elements': len(self.elements),
            'remaining': len(self.elements) - self.canvas_pointer,
            'current_element': self.peek()
        }
    
    def to_string(self) -> str:
        """String representation of canvas"""
        parts = []
        for i, elem in enumerate(self.elements):
            marker = " <--" if i == self.canvas_pointer else ""
            status_char = {
                StitchStatus.UNTOUCHED: "○",
                StitchStatus.WORKED_INTO: "●",
                StitchStatus.CONSUMED_IN_CLUSTER: "◉",
                StitchStatus.SKIPPED: "○"
            }[elem.status]
            
            parts.append(f"{status_char}{elem.index}{marker}")
        
        return " ".join(parts)


class BackwardTraversalError(Exception):
    """Raised when backward traversal is attempted without explicit directive"""
    pass


class OrphanedStitchError(Exception):
    """Raised when stitches are left unworked at end of round"""
    pass


if __name__ == "__main__":
    print("🎨 Canvas Queue Test")
    canvas = CanvasQueue()
    
    # Initialize with 6 stitches
    canvas.initialize_round(6, round_number=1)
    print(f"Initial canvas: {canvas.to_string()}")
    
    # Work first 2 stitches
    worked = canvas.advance(2)
    for elem in worked:
        elem.consume()
    print(f"After working 2: {canvas.to_string()}")
    
    # Add a corner space
    canvas.add_space('ch_sp', capacity=2)
    print(f"After adding space: {canvas.to_string()}")
    
    # Check exhaustion
    exhaustion = canvas.check_exhaustion()
    print(f"Exhaustion check: {exhaustion}")
    
    # Position info
    print(f"Position: {canvas.get_position_info()}")


# ============================================================================
# PostVsHeadLoopTracker - Distinguishes working around a post (BPtr/FPtr)
# from consuming the head loop of a stitch, ensuring post stitches don't
# prematurely mark top loops as consumed.
# (Added per 4-pattern audit)
# ============================================================================

class PostVsHeadLoopTracker:
    """
    Tracks post-work vs head-loop-work separately for every canvas element.
    A BPtr/FPtr stitch works AROUND the post and must not consume the head loop.
    """
    
    def __init__(self, canvas: 'CanvasQueue'):
        self.canvas = canvas
        self.post_worked_indices = set()
        self.head_worked_indices = set()
    
    def work_post(self, element_index: int) -> bool:
        """Work around the post of an element. Does NOT consume the head loop."""
        elem = self.canvas.get_element_at(element_index)
        if not elem:
            return False
        if elem.metadata.get('post_worked'):
            return False
        elem.metadata['post_worked'] = True
        self.post_worked_indices.add(element_index)
        return True
    
    def work_head(self, element_index: int) -> bool:
        """Work into the head loop. Consumes the element (marks WORKED_INTO)."""
        elem = self.canvas.get_element_at(element_index)
        if not elem:
            return False
        if elem.metadata.get('head_worked') or not elem.is_workable():
            return False
        elem.metadata['head_worked'] = True
        elem.consume()
        self.head_worked_indices.add(element_index)
        return True
    
    def can_work_post(self, element_index: int) -> bool:
        """Check if the post of an element is still available."""
        elem = self.canvas.get_element_at(element_index)
        return bool(elem and not elem.metadata.get('post_worked'))
    
    def can_work_head(self, element_index: int) -> bool:
        """Check if the head loop of an element is still available."""
        elem = self.canvas.get_element_at(element_index)
        return bool(elem and elem.is_workable() and not elem.metadata.get('head_worked'))
    
    def get_unconsumed_heads(self) -> List[CanvasElement]:
        """Get elements whose head loops remain unconsumed (post may be worked)."""
        return [e for e in self.canvas.elements
                if e.is_workable() and not e.metadata.get('head_worked')]
    
    def get_summary(self) -> Dict:
        """Summary of post vs head loop tracking."""
        return {
            'post_worked': len(self.post_worked_indices),
            'head_worked': len(self.head_worked_indices),
            'total_elements': len(self.canvas.elements),
            'unconsumed_heads': len(self.get_unconsumed_heads()),
        }


if __name__ == "__main__":
    print("🎨 Canvas Queue Test")
    canvas = CanvasQueue()
    
    canvas.initialize_round(6, round_number=1)
    print(f"Initial canvas: {canvas.to_string()}")
    
    worked = canvas.advance(2)
    for elem in worked:
        elem.consume()
    print(f"After working 2: {canvas.to_string()}")
    
    canvas.add_space('ch_sp', capacity=2)
    print(f"After adding space: {canvas.to_string()}")
    
    exhaustion = canvas.check_exhaustion()
    print(f"Exhaustion check: {exhaustion}")
    
    print(f"Position: {canvas.get_position_info()}")
    
    # PostVsHeadLoopTracker demo
    print("\n\n🎯 PostVsHeadLoopTracker Test")
    tracker = PostVsHeadLoopTracker(canvas)
    print(f"Work post of element 0: {tracker.work_post(0)}")
    print(f"Head of element 0 still available: {tracker.can_work_head(0)}")
    print(f"Work head of element 0: {tracker.work_head(0)}")
    print(f"Head of element 0 now available: {tracker.can_work_head(0)}")
    print(f"Summary: {tracker.get_summary()}")
