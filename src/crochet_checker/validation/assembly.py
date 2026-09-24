"""
AssemblyGraphValidator
Models joined modules (e.g., Join-As-You-Go petals) as a directed graph to verify 
that N modular pieces contain the required N neighbor-to-neighbor and N core joins 
before ring closure.
"""
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field

class AssemblyError(Exception):
    """Raised when assembly validation fails"""
    pass

@dataclass
class JoinNode:
    """Represents a join point between pieces"""
    join_id: str
    piece_a: str
    piece_b: str
    join_type: str  # "neighbor" or "core"
    round_number: int
    is_complete: bool = False

@dataclass
class PieceNode:
    """Represents a modular piece"""
    piece_id: str
    piece_type: str  # e.g., "petal", "leaf", "motif"
    joins: List[str] = field(default_factory=list)  # join_ids
    is_closed: bool = False

class AssemblyGraphValidator:
    """
    Validates assembly of modular pieces using directed graph.
    Ensures proper joins before ring closure.
    """
    
    def __init__(self):
        self.pieces: Dict[str, PieceNode] = {}
        self.joins: Dict[str, JoinNode] = {}
        self.adjacency: Dict[str, Set[str]] = {}
        self.join_counter: int = 0
    
    def add_piece(self, piece_id: str, piece_type: str = "motif") -> PieceNode:
        """Add a modular piece to the assembly"""
        if piece_id not in self.pieces:
            piece = PieceNode(piece_id=piece_id, piece_type=piece_type)
            self.pieces[piece_id] = piece
            self.adjacency[piece_id] = set()
        return self.pieces[piece_id]
    
    def add_join(self, piece_a: str, piece_b: str, join_type: str = "neighbor",
                round_number: int = 1) -> JoinNode:
        """Add a join between two pieces"""
        if piece_a not in self.pieces:
            self.add_piece(piece_a)
        if piece_b not in self.pieces:
            self.add_piece(piece_b)
        
        join = JoinNode(
            join_id=f"join_{self.join_counter}",
            piece_a=piece_a,
            piece_b=piece_b,
            join_type=join_type,
            round_number=round_number
        )
        
        self.joins[join.join_id] = join
        self.pieces[piece_a].joins.append(join.join_id)
        self.pieces[piece_b].joins.append(join.join_id)
        
        # Update adjacency
        self.adjacency[piece_a].add(piece_b)
        self.adjacency[piece_b].add(piece_a)
        
        self.join_counter += 1
        return join
    
    def complete_join(self, join_id: str) -> bool:
        """Mark a join as complete"""
        if join_id in self.joins:
            self.joins[join_id].is_complete = True
            return True
        return False
    
    def close_ring(self, piece_id: str) -> bool:
        """Close a ring of pieces"""
        if piece_id in self.pieces:
            self.pieces[piece_id].is_closed = True
            return True
        return False
    
    def validate_assembly(self) -> Dict:
        """
        Validate the complete assembly.
        Checks that N modular pieces have N neighbor joins and N core joins.
        Hub pieces (joined only via 'core' joins, e.g. a center ring) are
        excluded from the modular count.
        """
        # Classify pieces: modular (ring members) vs hubs (core-only recipients)
        neighbor_participants = set()
        core_participants = set()
        for join in self.joins.values():
            if join.join_type == "neighbor":
                neighbor_participants.add(join.piece_a)
                neighbor_participants.add(join.piece_b)
            else:
                core_participants.add(join.piece_a)
                core_participants.add(join.piece_b)
        
        hub_pieces = {pid for pid in core_participants if pid not in neighbor_participants}
        modular_pieces = neighbor_participants | {
            pid for pid in self.pieces if pid not in hub_pieces
        }
        n_modular = len(modular_pieces)
        
        # Count joins by type
        neighbor_joins = [j for j in self.joins.values() if j.join_type == "neighbor"]
        core_joins = [j for j in self.joins.values() if j.join_type == "core"]
        
        # N modular pieces need N neighbor joins (ring) and N core joins (center)
        expected_neighbor_joins = n_modular
        expected_core_joins = n_modular if hub_pieces else 0
        
        errors = []
        warnings = []
        
        # Check number of neighbor joins
        if len(neighbor_joins) < expected_neighbor_joins:
            missing = expected_neighbor_joins - len(neighbor_joins)
            errors.append(
                f"Missing {missing} neighbor-to-neighbor join(s). "
                f"Have {len(neighbor_joins)}, need {expected_neighbor_joins}"
            )
        
        # Check number of core joins
        if len(core_joins) < expected_core_joins:
            missing = expected_core_joins - len(core_joins)
            errors.append(
                f"Missing {missing} core join(s). "
                f"Have {len(core_joins)}, need {expected_core_joins}"
            )
        
        # Check that all pieces are connected
        disconnected = self._find_disconnected_pieces()
        if disconnected:
            warnings.append(f"Disconnected pieces: {disconnected}")
        
        # Check incomplete joins
        incomplete = [j.join_id for j in self.joins.values() if not j.is_complete]
        if incomplete:
            warnings.append(f"Incomplete joins: {incomplete}")
        
        # Ring degree check: each modular piece needs 2 neighbor joins
        neighbor_degree = {pid: 0 for pid in modular_pieces}
        for join in neighbor_joins:
            neighbor_degree[join.piece_a] = neighbor_degree.get(join.piece_a, 0) + 1
            neighbor_degree[join.piece_b] = neighbor_degree.get(join.piece_b, 0) + 1
        for pid, degree in neighbor_degree.items():
            if degree != 2:
                warnings.append(
                    f"Piece '{pid}' has {degree} neighbor join(s); a ring member needs 2"
                )
        
        # Check ring closure
        unclosed = [p.piece_id for p in self.pieces.values() if not p.is_closed]
        if unclosed and len(unclosed) == len(self.pieces):
            warnings.append("No pieces have been closed into a ring")
        
        return {
            "total_pieces": len(self.pieces),
            "modular_pieces": n_modular,
            "hub_pieces": sorted(hub_pieces),
            "neighbor_joins": len(neighbor_joins),
            "core_joins": len(core_joins),
            "expected_neighbor_joins": expected_neighbor_joins,
            "expected_core_joins": expected_core_joins,
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _find_disconnected_pieces(self) -> List[str]:
        """Find pieces that are not connected to the main assembly"""
        if not self.pieces:
            return []
        
        # BFS from first piece
        visited = set()
        queue = [next(iter(self.pieces))]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            for neighbor in self.adjacency.get(current, set()):
                if neighbor not in visited:
                    queue.append(neighbor)
        
        # Pieces not visited are disconnected
        return [pid for pid in self.pieces if pid not in visited]
    
    def validate_join_as_you_go(self) -> Dict:
        """
        Specialized validation for Join-As-You-Go (JAYG) patterns.
        JAYG requires each piece to join to its neighbors in order.
        """
        if not self.pieces:
            return {"is_valid": False, "errors": ["No pieces defined"]}
        
        errors = []
        warnings = []
        
        # Get pieces in creation order
        piece_ids = list(self.pieces.keys())
        
        # Check sequential joins
        for i in range(1, len(piece_ids)):
            current = piece_ids[i]
            previous = piece_ids[i - 1]
            
            # Each piece should join to the previous piece
            has_join = False
            for join in self.joins.values():
                if (join.piece_a == current and join.piece_b == previous) or \
                   (join.piece_a == previous and join.piece_b == current):
                    has_join = True
                    break
            
            if not has_join:
                warnings.append(
                    f"Piece '{current}' is not joined to previous piece '{previous}'"
                )
        
        # Check ring closure (last piece joins back to first)
        if len(piece_ids) >= 2:
            first = piece_ids[0]
            last = piece_ids[-1]
            
            has_closure = False
            for join in self.joins.values():
                if (join.piece_a == first and join.piece_b == last) or \
                   (join.piece_a == last and join.piece_b == first):
                    has_closure = True
                    break
            
            if not has_closure:
                errors.append(
                    f"Ring not closed: piece '{last}' is not joined back to '{first}'"
                )
        
        # Check core joins
        core_join_count = sum(1 for j in self.joins.values() if j.join_type == "core")
        if core_join_count < len(piece_ids):
            warnings.append(
                f"Expected {len(piece_ids)} core joins, found {core_join_count}"
            )
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_assembly_summary(self) -> Dict:
        """Get summary of the assembly"""
        piece_join_counts = {
            pid: len(piece.joins) for pid, piece in self.pieces.items()
        }
        
        join_types = {}
        for join in self.joins.values():
            join_types[join.join_type] = join_types.get(join.join_type, 0) + 1
        
        return {
            "total_pieces": len(self.pieces),
            "total_joins": len(self.joins),
            "join_types": join_types,
            "pieces": piece_join_counts,
            "adjacency": {pid: sorted(list(adj)) for pid, adj in self.adjacency.items()}
        }
    
    def reset(self) -> None:
        """Reset the validator"""
        self.pieces.clear()
        self.joins.clear()
        self.adjacency.clear()
        self.join_counter = 0

# Example usage
if __name__ == "__main__":
    validator = AssemblyGraphValidator()
    
    # Simulate 6 petals in a ring
    print("Creating 6 petals with JAYG assembly")
    for i in range(1, 7):
        validator.add_piece(f"petal_{i}", "petal")
    
    # Add neighbor joins (petal 1->2, 2->3, ..., 5->6, 6->1)
    for i in range(1, 7):
        next_petal = f"petal_{i % 6 + 1}"
        join = validator.add_join(f"petal_{i}", next_petal, "neighbor")
        validator.complete_join(join.join_id)
    
    # Add core joins
    for i in range(1, 7):
        join = validator.add_join(f"petal_{i}", "center", "core")
        validator.complete_join(join.join_id)
    
    # Close ring
    for i in range(1, 7):
        validator.close_ring(f"petal_{i}")
    
    # Validate
    result = validator.validate_assembly()
    print(f"✅ Valid: {result['is_valid']}")
    print(f"   Neighbor joins: {result['neighbor_joins']}/{result['expected_neighbor_joins']}")
    print(f"   Core joins: {result['core_joins']}/{result['expected_core_joins']}")
    
    if result['warnings']:
        print("Warnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")
    
    # Test incomplete assembly
    print("\nTesting incomplete assembly (missing joins)")
    validator.reset()
    
    for i in range(1, 5):
        validator.add_piece(f"petal_{i}", "petal")
    
    # Only add 3 neighbor joins (missing 1) and no core joins
    for i in range(1, 4):
        validator.add_join(f"petal_{i}", f"petal_{i+1}", "neighbor")
    
    result = validator.validate_assembly()
    print(f"Valid: {result['is_valid']}")
    print(f"Errors: {result['errors']}")
    
    # Test JAYG validation
    print("\nTesting JAYG validation")
    jayg_result = validator.validate_join_as_you_go()
    print(f"JAYG Valid: {jayg_result['is_valid']}")
    if jayg_result['errors']:
        print(f"JAYG Errors: {jayg_result['errors']}")
    if jayg_result['warnings']:
        print(f"JAYG Warnings: {jayg_result['warnings']}")
