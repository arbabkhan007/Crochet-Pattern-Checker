"""
StitchConsumer (Loop State Allocator)
Tracks individual loop lifecycle states (UNTOUCHED, WORKED_INTO, CONSUMED_IN_CLUSTER, 
SKIPPED, BRIDGED_BY_CHAIN).
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class LoopLifecycleState(Enum):
    """Lifecycle state of a loop"""
    UNTOUCHED = "untouched"
    WORKED_INTO = "worked_into"
    CONSUMED_IN_CLUSTER = "consumed_in_cluster"
    SKIPPED = "skipped"
    BRIDGED_BY_CHAIN = "bridged_by_chain"

@dataclass
class LoopState:
    """Tracks the state of a single loop"""
    loop_id: str
    round_number: int
    position: int
    state: LoopLifecycleState = LoopLifecycleState.UNTOUCHED
    worked_by_round: Optional[int] = None
    cluster_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    def work(self, round_number: int, cluster_id: Optional[str] = None) -> bool:
        """Mark loop as worked"""
        if self.state == LoopLifecycleState.UNTOUCHED:
            self.state = LoopLifecycleState.WORKED_INTO
            self.worked_by_round = round_number
            self.cluster_id = cluster_id
            return True
        return False
    
    def skip(self) -> bool:
        """Mark loop as skipped"""
        if self.state == LoopLifecycleState.UNTOUCHED:
            self.state = LoopLifecycleState.SKIPPED
            return True
        return False
    
    def consume_in_cluster(self, cluster_id: str) -> bool:
        """Mark loop as consumed in a cluster"""
        if self.state == LoopLifecycleState.UNTOUCHED:
            self.state = LoopLifecycleState.CONSUMED_IN_CLUSTER
            self.cluster_id = cluster_id
            return True
        return False
    
    def bridge_by_chain(self) -> bool:
        """Mark loop as bridged by chain"""
        if self.state == LoopLifecycleState.UNTOUCHED:
            self.state = LoopLifecycleState.BRIDGED_BY_CHAIN
            return True
        return False
    
    def is_available(self) -> bool:
        """Check if loop is available to be worked"""
        return self.state == LoopLifecycleState.UNTOUCHED

class ClusterDefinition:
    """Defines a cluster of stitches"""
    def __init__(self, cluster_id: str, stitch_count: int, stitch_type: str):
        self.cluster_id = cluster_id
        self.stitch_count = stitch_count
        self.stitch_type = stitch_type
        self.consumed_loops: List[str] = []  # instance-level, set per cluster

try:
    from .canvas_queue import OrphanedStitchError  # shared engine exception
except ImportError:  # pragma: no cover - run as __main__ demo
    from canvas_queue import OrphanedStitchError

class InvalidOperationError(Exception):
    """Raised when an invalid operation is attempted"""
    pass

class StitchConsumer:
    """
    Tracks individual loop lifecycle states and manages stitch consumption.
    Ensures all base stitches are properly accounted for.
    """
    
    def __init__(self):
        self.loops: Dict[str, LoopState] = {}
        self.clusters: Dict[str, ClusterDefinition] = {}
        self.round_number: int = 0
        self.loop_counter: int = 0
        self.cluster_counter: int = 0
        self.stitches_worked: int = 0
        self.stitches_skipped: int = 0
        
    def add_loop(self, round_number: int, position: int) -> LoopState:
        """Add a new loop to track"""
        loop_id = f"r{round_number}_p{position}_{self.loop_counter}"
        
        loop = LoopState(
            loop_id=loop_id,
            round_number=round_number,
            position=position
        )
        
        self.loops[loop_id] = loop
        self.loop_counter += 1
        return loop
    
    def get_loop(self, loop_id: str) -> Optional[LoopState]:
        """Get a loop by ID"""
        return self.loops.get(loop_id)
    
    def get_loop_at(self, round_number: int, position: int) -> Optional[LoopState]:
        """Get loop at specific round and position"""
        for loop in self.loops.values():
            if loop.round_number == round_number and loop.position == position:
                return loop
        return None
    
    def work_stitch(self, loop_id: str, round_number: int) -> bool:
        """Work a single stitch into a loop"""
        loop = self.get_loop(loop_id)
        if not loop:
            raise InvalidOperationError(f"Loop {loop_id} not found")
        
        if loop.work(round_number):
            self.stitches_worked += 1
            return True
        return False
    
    def skip_stitch(self, loop_id: str) -> bool:
        """Skip a stitch"""
        loop = self.get_loop(loop_id)
        if not loop:
            raise InvalidOperationError(f"Loop {loop_id} not found")
        
        if loop.skip():
            self.stitches_skipped += 1
            return True
        return False
    
    def create_cluster(self, stitch_count: int, stitch_type: str) -> str:
        """Create a new cluster definition"""
        cluster_id = f"cluster_{self.cluster_counter}"
        cluster = ClusterDefinition(cluster_id, stitch_count, stitch_type)
        self.clusters[cluster_id] = cluster
        self.cluster_counter += 1
        return cluster_id
    
    def consume_in_cluster(self, loop_ids: List[str], cluster_id: str) -> bool:
        """Consume multiple loops in a cluster"""
        cluster = self.clusters.get(cluster_id)
        if not cluster:
            raise InvalidOperationError(f"Cluster {cluster_id} not found")
        
        if len(loop_ids) != cluster.stitch_count:
            raise InvalidOperationError(
                f"Cluster requires {cluster.stitch_count} loops, got {len(loop_ids)}"
            )
        
        for loop_id in loop_ids:
            loop = self.get_loop(loop_id)
            if not loop:
                raise InvalidOperationError(f"Loop {loop_id} not found")
            
            if not loop.consume_in_cluster(cluster_id):
                raise InvalidOperationError(f"Loop {loop_id} is not available")
            
            cluster.consumed_loops.append(loop_id)
            self.stitches_worked += 1
        
        return True
    
    def bridge_with_chain(self, loop_id: str) -> bool:
        """Bridge a loop with a chain"""
        loop = self.get_loop(loop_id)
        if not loop:
            raise InvalidOperationError(f"Loop {loop_id} not found")
        
        return loop.bridge_by_chain()
    
    def get_unworked_loops(self, round_number: Optional[int] = None) -> List[LoopState]:
        """Get all unworked loops, optionally filtered by round"""
        unworked = []
        for loop in self.loops.values():
            if loop.is_available():
                if round_number is None or loop.round_number == round_number:
                    unworked.append(loop)
        return unworked
    
    def check_exhaustion(self, round_number: int, allow_unworked: bool = False) -> Dict:
        """
        Check if all loops in a round have been worked.
        Raises OrphanedStitchError if unworked loops found and not allowed.
        """
        unworked = self.get_unworked_loops(round_number)
        
        result = {
            "round": round_number,
            "total_loops": len([l for l in self.loops.values() if l.round_number == round_number]),
            "unworked_count": len(unworked),
            "unworked_loops": [l.loop_id for l in unworked],
            "exhausted": len(unworked) == 0
        }
        
        if not allow_unworked and not result["exhausted"]:
            raise OrphanedStitchError(
                f"Round {round_number} has {result['unworked_count']} unworked loops: "
                f"{result['unworked_loops']}"
            )
        
        return result
    
    def get_round_summary(self, round_number: int) -> Dict:
        """Get summary of a specific round"""
        round_loops = [l for l in self.loops.values() if l.round_number == round_number]
        
        state_counts = {}
        for state in LoopLifecycleState:
            count = len([l for l in round_loops if l.state == state])
            state_counts[state.value] = count
        
        return {
            "round": round_number,
            "total_loops": len(round_loops),
            "state_counts": state_counts,
            "worked": state_counts.get("worked_into", 0) + state_counts.get("consumed_in_cluster", 0),
            "skipped": state_counts.get("skipped", 0),
            "unworked": state_counts.get("untouched", 0)
        }
    
    def get_overall_summary(self) -> Dict:
        """Get overall summary of all loops"""
        state_counts = {}
        for state in LoopLifecycleState:
            count = len([l for l in self.loops.values() if l.state == state])
            state_counts[state.value] = count
        
        return {
            "total_loops": len(self.loops),
            "total_clusters": len(self.clusters),
            "state_counts": state_counts,
            "stitches_worked": self.stitches_worked,
            "stitches_skipped": self.stitches_skipped
        }
    
    def new_round(self) -> None:
        """Start a new round"""
        self.round_number += 1
    
    def reset(self) -> None:
        """Reset the consumer"""
        self.loops.clear()
        self.clusters.clear()
        self.round_number = 0
        self.loop_counter = 0
        self.cluster_counter = 0
        self.stitches_worked = 0
        self.stitches_skipped = 0

# Example usage
if __name__ == "__main__":
    consumer = StitchConsumer()
    
    # Simulate Round 1: 6 sc
    print("Round 1: 6 sc")
    round1_loops = []
    for i in range(6):
        loop = consumer.add_loop(1, i)
        round1_loops.append(loop.loop_id)
    
    print(f"Created {len(round1_loops)} loops")
    
    # Work all stitches in Round 1
    for loop_id in round1_loops:
        consumer.work_stitch(loop_id, 1)
    
    # Check exhaustion
    try:
        result = consumer.check_exhaustion(1)
        print(f"✅ Round 1 exhausted: {result['exhausted']}")
    except OrphanedStitchError as e:
        print(f"❌ {e}")
    
    # Simulate Round 2 with a cluster
    print("\nRound 2: Working with cluster")
    consumer.new_round()
    
    # Add loops for Round 2
    round2_loops = []
    for i in range(6):
        loop = consumer.add_loop(2, i)
        round2_loops.append(loop.loop_id)
    
    # Create a cluster that consumes 3 loops
    cluster_id = consumer.create_cluster(3, "tr")
    print(f"Created cluster: {cluster_id}")
    
    # Consume first 3 loops in cluster
    consumer.consume_in_cluster(round2_loops[:3], cluster_id)
    print(f"Consumed 3 loops in cluster")
    
    # Work remaining 3 loops individually
    for loop_id in round2_loops[3:]:
        consumer.work_stitch(loop_id, 2)
    
    # Check exhaustion
    try:
        result = consumer.check_exhaustion(2)
        print(f"✅ Round 2 exhausted: {result['exhausted']}")
    except OrphanedStitchError as e:
        print(f"❌ {e}")
    
    # Get summaries
    print(f"\nRound 1 summary: {consumer.get_round_summary(1)}")
    print(f"Round 2 summary: {consumer.get_round_summary(2)}")
    print(f"\nOverall summary: {consumer.get_overall_summary()}")


# Legacy compatibility method.
def _legacy_consume(self, *args, **kwargs):
    if args:
        loop_id = args[0]
        round_number = args[1] if len(args) > 1 else kwargs.get("round_number", 1)
        return self.work_stitch(loop_id, round_number)
    return True

StitchConsumer.consume = _legacy_consume
