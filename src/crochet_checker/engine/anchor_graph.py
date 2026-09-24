"""
GlobalAnchorGraph (Multi-Depth Lookups)
Tracks stitch nodes across all previous rounds (N-1, N-2, ...) so multi-level 
stitches (like Split-tr2tog anchored into Round 1) can register dependencies 
without breaking the active round pointer.
"""
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class AnchorType(Enum):
    """Type of anchor point"""
    STITCH_TOP = "stitch_top"
    POST = "post"
    CHAIN_SPACE = "chain_space"
    SIDE_BAR = "side_bar"

@dataclass
class AnchorNode:
    """Represents an anchorable point in the pattern"""
    node_id: str
    round_number: int
    position: int
    anchor_type: AnchorType
    stitch_type: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)  # node_ids that depend on this
    dependents: List[str] = field(default_factory=list)    # node_ids this depends on
    metadata: Dict = field(default_factory=dict)
    
    def add_dependency(self, node_id: str) -> None:
        """Add a dependency (another node that depends on this)"""
        if node_id not in self.dependencies:
            self.dependencies.append(node_id)
    
    def add_dependent(self, node_id: str) -> None:
        """Add a dependent (node this depends on)"""
        if node_id not in self.dependents:
            self.dependents.append(node_id)

class CircularDependencyError(Exception):
    """Raised when a circular dependency is detected"""
    pass

class AnchorNotFoundError(Exception):
    """Raised when trying to access a non-existent anchor"""
    pass

class GlobalAnchorGraph:
    """
    Tracks stitch nodes across all previous rounds for multi-depth lookups.
    Allows multi-level stitches to register dependencies without breaking
    the active round pointer.
    """
    
    def __init__(self):
        self.nodes: Dict[str, AnchorNode] = {}
        self.round_nodes: Dict[int, List[str]] = {}  # round_number -> [node_ids]
        self.node_counter: int = 0
        
    def create_node(self, round_number: int, position: int, 
                   anchor_type: AnchorType, stitch_type: Optional[str] = None,
                   metadata: Optional[Dict] = None) -> AnchorNode:
        """Create a new anchor node"""
        node_id = f"r{round_number}_p{position}_{anchor_type.value}_{self.node_counter}"
        
        node = AnchorNode(
            node_id=node_id,
            round_number=round_number,
            position=position,
            anchor_type=anchor_type,
            stitch_type=stitch_type,
            metadata=metadata or {}
        )
        
        self.nodes[node_id] = node
        
        # Index by round
        if round_number not in self.round_nodes:
            self.round_nodes[round_number] = []
        self.round_nodes[round_number].append(node_id)
        
        self.node_counter += 1
        return node
    
    def get_node(self, node_id: str) -> AnchorNode:
        """Get a node by ID"""
        if node_id not in self.nodes:
            raise AnchorNotFoundError(f"Anchor node '{node_id}' not found")
        return self.nodes[node_id]
    
    def get_nodes_in_round(self, round_number: int) -> List[AnchorNode]:
        """Get all nodes in a specific round"""
        if round_number not in self.round_nodes:
            return []
        return [self.nodes[nid] for nid in self.round_nodes[round_number]]
    
    def get_nodes_by_position(self, round_number: int, position: int) -> List[AnchorNode]:
        """Get nodes at a specific position in a round"""
        return [
            node for node in self.get_nodes_in_round(round_number)
            if node.position == position
        ]
    
    def create_dependency(self, from_node_id: str, to_node_id: str) -> bool:
        """
        Create a dependency: from_node depends on to_node.
        Returns True if successful, False if circular dependency detected.
        """
        from_node = self.get_node(from_node_id)
        to_node = self.get_node(to_node_id)
        
        # Check for circular dependency
        if self._would_create_cycle(from_node_id, to_node_id):
            raise CircularDependencyError(
                f"Creating dependency from {from_node_id} to {to_node_id} "
                "would create a circular dependency"
            )
        
        from_node.add_dependent(to_node_id)
        to_node.add_dependency(from_node_id)
        
        return True
    
    def _would_create_cycle(self, from_id: str, to_id: str) -> bool:
        """Check if creating a dependency would create a cycle"""
        visited = set()
        
        def dfs(node_id: str) -> bool:
            if node_id == from_id:
                return True  # Found a cycle
            if node_id in visited:
                return False
            visited.add(node_id)
            
            node = self.nodes.get(node_id)
            if not node:
                return False
            
            for dep_id in node.dependents:
                if dfs(dep_id):
                    return True
            
            return False
        
        return dfs(to_id)
    
    def get_all_dependencies(self, node_id: str, depth: int = -1) -> Set[str]:
        """
        Get all dependencies recursively.
        depth: -1 for all depths, 0 for direct only, N for N levels deep
        """
        dependencies = set()
        visited = set()
        
        def collect_deps(nid: str, current_depth: int):
            if nid in visited:
                return
            if depth >= 0 and current_depth > depth:
                return
            
            visited.add(nid)
            node = self.nodes.get(nid)
            if not node:
                return
            
            for dep_id in node.dependents:
                dependencies.add(dep_id)
                collect_deps(dep_id, current_depth + 1)
        
        collect_deps(node_id, 0)
        return dependencies
    
    def get_all_dependents(self, node_id: str, depth: int = -1) -> Set[str]:
        """
        Get all dependents recursively.
        depth: -1 for all depths, 0 for direct only, N for N levels deep
        """
        dependents = set()
        visited = set()
        
        def collect_dependents(nid: str, current_depth: int):
            if nid in visited:
                return
            if depth >= 0 and current_depth > depth:
                return
            
            visited.add(nid)
            node = self.nodes.get(nid)
            if not node:
                return
            
            for dep_id in node.dependencies:
                dependents.add(dep_id)
                collect_dependents(dep_id, current_depth + 1)
        
        collect_dependents(node_id, 0)
        return dependents
    
    def find_anchor_in_previous_rounds(self, position: int, anchor_type: AnchorType,
                                      max_depth: int = -1) -> List[AnchorNode]:
        """
        Find anchor nodes at a position in previous rounds.
        max_depth: -1 for all previous rounds, N for last N rounds
        """
        results = []
        
        if max_depth < 0:
            # Search all previous rounds
            rounds_to_search = sorted(self.round_nodes.keys(), reverse=True)
        else:
            # Search last N rounds
            all_rounds = sorted(self.round_nodes.keys(), reverse=True)
            rounds_to_search = all_rounds[:max_depth]
        
        for round_num in rounds_to_search:
            nodes = self.get_nodes_by_position(round_num, position)
            for node in nodes:
                if node.anchor_type == anchor_type:
                    results.append(node)
        
        return results
    
    def validate_dependencies(self) -> List[str]:
        """
        Validate all dependencies in the graph.
        Returns list of validation errors.
        """
        errors = []
        
        for node_id, node in self.nodes.items():
            # Check that all dependencies exist
            for dep_id in node.dependents:
                if dep_id not in self.nodes:
                    errors.append(f"Node {node_id} depends on non-existent node {dep_id}")
            
            for dep_id in node.dependencies:
                if dep_id not in self.nodes:
                    errors.append(f"Node {node_id} has non-existent dependent {dep_id}")
            
            # Check for dependencies on future rounds
            for dep_id in node.dependents:
                dep_node = self.nodes.get(dep_id)
                if dep_node and dep_node.round_number > node.round_number:
                    errors.append(
                        f"Node {node_id} (round {node.round_number}) depends on "
                        f"future node {dep_id} (round {dep_node.round_number})"
                    )
        
        return errors
    
    def get_graph_summary(self) -> Dict:
        """Get summary of the anchor graph"""
        total_nodes = len(self.nodes)
        total_dependencies = sum(len(node.dependents) for node in self.nodes.values())
        rounds = sorted(self.round_nodes.keys())
        
        return {
            "total_nodes": total_nodes,
            "total_dependencies": total_dependencies,
            "rounds": len(rounds),
            "round_range": (min(rounds) if rounds else 0, max(rounds) if rounds else 0),
            "nodes_per_round": {r: len(nodes) for r, nodes in self.round_nodes.items()}
        }
    
    def reset(self) -> None:
        """Reset the graph"""
        self.nodes.clear()
        self.round_nodes.clear()
        self.node_counter = 0

# Example usage
if __name__ == "__main__":
    graph = GlobalAnchorGraph()
    
    # Simulate Round 1: 6 sc
    print("Creating Round 1 anchors")
    for i in range(6):
        graph.create_node(1, i, AnchorType.STITCH_TOP, "sc")
    
    # Simulate Round 2: Working into Round 1
    print("Creating Round 2 anchors")
    for i in range(6):
        node = graph.create_node(2, i, AnchorType.STITCH_TOP, "sc")
        # Create dependency on Round 1
        r1_nodes = graph.get_nodes_by_position(1, i)
        if r1_nodes:
            graph.create_dependency(node.node_id, r1_nodes[0].node_id)
    
    # Simulate a complex stitch that anchors back to Round 1
    print("\nCreating complex stitch anchored to Round 1")
    complex_node = graph.create_node(3, 0, AnchorType.POST, "Split-tr2tog")
    r1_node = graph.get_nodes_by_position(1, 0)[0]
    graph.create_dependency(complex_node.node_id, r1_node.node_id)
    
    print(f"Complex stitch dependencies: {complex_node.dependents}")
    
    # Find all dependencies
    all_deps = graph.get_all_dependencies(complex_node.node_id)
    print(f"All dependencies (recursive): {all_deps}")
    
    # Validate
    errors = graph.validate_dependencies()
    if errors:
        print("\nValidation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✅ All dependencies valid")
    
    # Get summary
    summary = graph.get_graph_summary()
    print(f"\nGraph summary: {summary}")
