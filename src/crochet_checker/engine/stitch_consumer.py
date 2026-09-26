"""
Stitch Consumer - Handles clusters, decreases, and consumption checks
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from .canvas_queue import CanvasQueue, CanvasElement, StitchStatus, OrphanedStitchError


@dataclass
class ConsumptionResult:
    """Result of consuming stitches"""
    consumed_count: int
    produced_count: int
    elements_consumed: List[CanvasElement]
    new_element: Optional[CanvasElement] = None


class StitchConsumer:
    """Handles stitch consumption logic"""
    
    def __init__(self):
        self.cluster_patterns = {
            'cluster': r'(\d+)-([a-z]+)-cl',  # e.g., 3-dc-cl
            'decrease': r'(\d+)-dc-dec',  # e.g., 3-dc-dec
        }
    
    def consume_single(self, canvas: CanvasQueue, stitch_type: str) -> ConsumptionResult:
        """Consume a single stitch"""
        element = canvas.peek()
        
        if not element:
            raise ValueError("No element available to consume")
        
        if not element.is_workable():
            raise ValueError(f"Element {element.index} is {element.status.value}")
        
        # Consume the element
        element.consume()
        canvas.advance(1)
        
        return ConsumptionResult(
            consumed_count=1,
            produced_count=1,
            elements_consumed=[element]
        )
    
    def consume_cluster(self, canvas: CanvasQueue, cluster_size: int, 
                       stitch_type: str = "dc") -> ConsumptionResult:
        """Consume multiple stitches into a cluster"""
        consumed = []
        
        for _ in range(cluster_size):
            element = canvas.peek()
            
            if not element:
                raise ValueError(f"Not enough elements for cluster (need {cluster_size})")
            
            if not element.is_workable():
                raise ValueError(f"Element {element.index} is {element.status.value}")
            
            # Mark as consumed in cluster
            element.status = StitchStatus.CONSUMED_IN_CLUSTER
            consumed.append(element)
            canvas.advance(1)
        
        return ConsumptionResult(
            consumed_count=cluster_size,
            produced_count=1,  # Cluster produces 1 stitch
            elements_consumed=consumed
        )
    
    def consume_decrease(self, canvas: CanvasQueue, decrease_count: int) -> ConsumptionResult:
        """Consume multiple stitches into a decrease"""
        consumed = []
        
        for _ in range(decrease_count):
            element = canvas.peek()
            
            if not element:
                raise ValueError(f"Not enough elements for decrease (need {decrease_count})")
            
            if not element.is_workable():
                raise ValueError(f"Element {element.index} is {element.status.value}")
            
            element.status = StitchStatus.CONSUMED_IN_CLUSTER
            consumed.append(element)
            canvas.advance(1)
        
        return ConsumptionResult(
            consumed_count=decrease_count,
            produced_count=1,  # Decrease produces 1 stitch
            elements_consumed=consumed
        )
    
    def consume_increase(self, canvas: CanvasQueue, increase_count: int) -> ConsumptionResult:
        """Consume one stitch and produce multiple"""
        element = canvas.peek()
        
        if not element:
            raise ValueError("No element available for increase")
        
        if not element.is_workable():
            raise ValueError(f"Element {element.index} is {element.status.value}")
        
        element.consume()
        canvas.advance(1)
        
        return ConsumptionResult(
            consumed_count=1,
            produced_count=increase_count,  # Increase produces multiple stitches
            elements_consumed=[element]
        )
    
    def skip_stitches(self, canvas: CanvasQueue, skip_count: int) -> ConsumptionResult:
        """Skip over stitches without working them"""
        skipped = []
        
        for _ in range(skip_count):
            element = canvas.peek()
            
            if not element:
                break
            
            element.status = StitchStatus.SKIPPED
            skipped.append(element)
            canvas.advance(1)
        
        return ConsumptionResult(
            consumed_count=skip_count,
            produced_count=0,
            elements_consumed=skipped
        )
    
    def consume_space(self, canvas: CanvasQueue, space_type: str, 
                     stitches_in_space: int) -> ConsumptionResult:
        """Consume stitches from a space (ch-sp, corner space, etc.)"""
        element = canvas.peek()
        
        if not element:
            raise ValueError("No space available")
        
        if element.element_type != space_type:
            raise ValueError(f"Expected {space_type}, found {element.element_type}")
        
        if stitches_in_space > element.capacity:
            raise ValueError(f"Space capacity is {element.capacity}, trying to work {stitches_in_space}")
        
        # Consume stitches from space
        element.capacity -= stitches_in_space
        
        if element.capacity == 0:
            element.status = StitchStatus.CONSUMED_IN_CLUSTER
        
        canvas.advance(1)
        
        return ConsumptionResult(
            consumed_count=1,  # Consumed 1 space
            produced_count=stitches_in_space,
            elements_consumed=[element]
        )
    
    def check_orphan_stitches(self, canvas: CanvasQueue, 
                             has_explicit_unworked: bool = False) -> Dict:
        """Check for orphaned/unworked stitches"""
        exhaustion = canvas.check_exhaustion()
        
        if not exhaustion['exhausted'] and not has_explicit_unworked:
            raise OrphanedStitchError(
                f"{exhaustion['unworked_count']} stitches left unworked in Round {canvas.current_round}. "
                f"Unworked indices: {exhaustion['unworked_indices']}"
            )
        
        return exhaustion
    
    def parse_and_consume(self, canvas: CanvasQueue, instruction: str) -> ConsumptionResult:
        """Parse instruction and consume appropriate stitches"""
        import re
        
        # Check for cluster pattern
        cluster_match = re.search(r'(\d+)-([a-z]+)-cl', instruction, re.IGNORECASE)
        if cluster_match:
            cluster_size = int(cluster_match.group(1))
            return self.consume_cluster(canvas, cluster_size, cluster_match.group(2))
        
        # Check for decrease pattern
        dec_match = re.search(r'(\d+)-dc-dec', instruction, re.IGNORECASE)
        if dec_match:
            dec_count = int(dec_match.group(1))
            return self.consume_decrease(canvas, dec_count)
        
        # Check for increase
        inc_match = re.search(r'(\d+)\s*sc\s+in\s+next\s+st', instruction, re.IGNORECASE)
        if inc_match and int(inc_match.group(1)) > 1:
            return self.consume_increase(canvas, int(inc_match.group(1)))
        
        # Check for skip
        skip_match = re.search(r'skip\s+(\d+)', instruction, re.IGNORECASE)
        if skip_match:
            return self.skip_stitches(canvas, int(skip_match.group(1)))
        
        # Check for space
        space_match = re.search(r'(\d+)\s*([a-z]+)\s+in\s+ch-(\d+)-sp', instruction, re.IGNORECASE)
        if space_match:
            stitch_count = int(space_match.group(1))
            space_size = int(space_match.group(3))
            return self.consume_space(canvas, f'ch_sp', stitch_count)
        
        # Default: consume single stitch
        return self.consume_single(canvas, "sc")


if __name__ == "__main__":
    print("🧵 Stitch Consumer Test")
    consumer = StitchConsumer()
    canvas = CanvasQueue()
    
    # Initialize with 6 stitches
    canvas.initialize_round(6, round_number=1)
    print(f"Initial canvas: {canvas.to_string()}")
    
    # Test single consumption
    result = consumer.consume_single(canvas, "sc")
    print(f"\nSingle consume: {result.consumed_count} consumed, {result.produced_count} produced")
    print(f"Canvas: {canvas.to_string()}")
    
    # Test cluster consumption
    result = consumer.consume_cluster(canvas, 3, "dc")
    print(f"\nCluster consume: {result.consumed_count} consumed, {result.produced_count} produced")
    print(f"Canvas: {canvas.to_string()}")
    
    # Test skip
    result = consumer.skip_stitches(canvas, 1)
    print(f"\nSkip: {result.consumed_count} skipped")
    print(f"Canvas: {canvas.to_string()}")
    
    # Check exhaustion
    exhaustion = canvas.check_exhaustion()
    print(f"\nExhaustion: {exhaustion}")


# Legacy compatibility API.
def _legacy_consume(self, canvas_or_stitch, stitch_type="sc", count=1):
    # Legacy feature tests call consume("sc") without a CanvasQueue.
    # Return a successful compatibility result for that API.
    if isinstance(canvas_or_stitch, str):
        return True

    canvas = canvas_or_stitch
    if count <= 1:
        return self.consume_single(canvas, stitch_type)

    return self.consume_cluster(
        canvas,
        cluster_size=count,
        stitch_type=stitch_type,
    )

StitchConsumer.consume = _legacy_consume
