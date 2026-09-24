"""
Assembly Graph - Validates inter-piece joins and ring closures
Treats joins as a Directed Graph to catch missing joins and incomplete assemblies
"""
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class JoinType(Enum):
    SLIP_STITCH = "sl st"
    SEAM = "seam"
    JOIN_AS_YOU_GO = "jaygo"
    WHIP_STITCH = "whip stitch"
    MATTRESS_STITCH = "mattress stitch"


@dataclass
class AnchorPoint:
    """Represents a joinable point on a piece"""
    piece_name: str
    point_id: str
    point_type: str  # 'picot', 'chain_space', 'stitch_top', 'edge'
    round_number: Optional[int] = None
    stitch_index: Optional[int] = None


@dataclass
class JoinEdge:
    """Represents a join between two anchor points"""
    source: AnchorPoint
    target: AnchorPoint
    join_type: JoinType
    line_number: int = 0
    verified: bool = False


class AssemblyGraph:
    """Graph-based assembly validator for crochet pieces"""
    
    def __init__(self):
        self.pieces: Dict[str, Dict] = {}
        self.anchor_points: List[AnchorPoint] = []
        self.edges: List[JoinEdge] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []
    
    def register_piece(self, piece_name: str, metadata: Dict = None):
        """Register a piece in the assembly"""
        self.pieces[piece_name] = {
            'name': piece_name,
            'metadata': metadata or {},
            'anchor_points': [],
            'joined_to': set()
        }
    
    def add_anchor_point(self, piece_name: str, point_type: str, 
                        point_id: str = None, round_number: int = None,
                        stitch_index: int = None) -> AnchorPoint:
        """Add an anchor point to a piece"""
        if piece_name not in self.pieces:
            self.register_piece(piece_name)
        
        if point_id is None:
            point_id = f"{piece_name}_{point_type}_{len(self.anchor_points)}"
        
        anchor = AnchorPoint(
            piece_name=piece_name,
            point_id=point_id,
            point_type=point_type,
            round_number=round_number,
            stitch_index=stitch_index
        )
        
        self.anchor_points.append(anchor)
        self.pieces[piece_name]['anchor_points'].append(anchor)
        
        return anchor
    
    def add_join(self, source_piece: str, target_piece: str, 
                join_type: JoinType = JoinType.SLIP_STITCH,
                source_point: str = None, target_point: str = None,
                line_number: int = 0) -> JoinEdge:
        """Add a join between two pieces"""
        # Find or create anchor points
        if source_point:
            source_anchor = self._find_anchor(source_piece, source_point)
        else:
            source_anchor = self.add_anchor_point(source_piece, 'edge')
        
        if target_point:
            target_anchor = self._find_anchor(target_piece, target_point)
        else:
            target_anchor = self.add_anchor_point(target_piece, 'edge')
        
        edge = JoinEdge(
            source=source_anchor,
            target=target_anchor,
            join_type=join_type,
            line_number=line_number
        )
        
        self.edges.append(edge)
        
        # Update piece join tracking
        self.pieces[source_piece]['joined_to'].add(target_piece)
        self.pieces[target_piece]['joined_to'].add(source_piece)
        
        return edge
    
    def _find_anchor(self, piece_name: str, point_id: str) -> Optional[AnchorPoint]:
        """Find an anchor point by ID"""
        for anchor in self.anchor_points:
            if anchor.piece_name == piece_name and anchor.point_id == point_id:
                return anchor
        return None
    
    def validate_ring_closure(self, piece_name: str, expected_joins: int) -> bool:
        """Validate that a piece forms a complete ring"""
        piece_joins = [e for e in self.edges 
                      if e.source.piece_name == piece_name or e.target.piece_name == piece_name]
        
        if len(piece_joins) < expected_joins:
            self.errors.append(
                f"IncompleteAssemblyError: Piece '{piece_name}' has {len(piece_joins)} joins, "
                f"but {expected_joins} are required for ring closure"
            )
            return False
        
        return True
    
    def validate_assembly_completeness(self) -> bool:
        """Validate that all pieces are properly joined"""
        unjoined_pieces = []
        
        for piece_name, piece_data in self.pieces.items():
            if not piece_data['joined_to']:
                unjoined_pieces.append(piece_name)
        
        if unjoined_pieces:
            self.warnings.append(
                f"Unjoined pieces detected: {', '.join(unjoined_pieces)}"
            )
            return False
        
        return True
    
    def detect_orphan_pieces(self) -> List[str]:
        """Detect pieces that are not connected to the main assembly"""
        if not self.pieces:
            return []
        
        # Build adjacency graph
        visited = set()
        start_piece = list(self.pieces.keys())[0]
        
        def dfs(piece_name):
            if piece_name in visited:
                return
            visited.add(piece_name)
            for joined_piece in self.pieces[piece_name]['joined_to']:
                dfs(joined_piece)
        
        dfs(start_piece)
        
        orphans = [p for p in self.pieces.keys() if p not in visited]
        return orphans
    
    def validate_flower_assembly(self, petal_count: int, center_piece: str = None) -> bool:
        """Validate a flower assembly with petals around a center"""
        # Find all petal pieces
        petals = [name for name in self.pieces.keys() 
                 if 'petal' in name.lower()]
        
        if len(petals) != petal_count:
            self.errors.append(
                f"Expected {petal_count} petals, found {len(petals)}"
            )
            return False
        
        # Each petal should join to center and to adjacent petals
        expected_joins_per_petal = 2 if center_piece else 2
        
        for petal in petals:
            petal_edges = [e for e in self.edges 
                          if e.source.piece_name == petal or e.target.piece_name == petal]
            
            if len(petal_edges) < expected_joins_per_petal:
                self.errors.append(
                    f"Petal '{petal}' has {len(petal_edges)} joins, "
                    f"expected {expected_joins_per_petal}"
                )
                return False
        
        return True
    
    def get_assembly_report(self) -> Dict:
        """Generate assembly validation report"""
        orphans = self.detect_orphan_pieces()
        
        return {
            'total_pieces': len(self.pieces),
            'total_joins': len(self.edges),
            'pieces': list(self.pieces.keys()),
            'orphan_pieces': orphans,
            'assembly_complete': self.validate_assembly_completeness(),
            'warnings': self.warnings,
            'errors': self.errors,
            'join_summary': self._summarize_joins()
        }
    
    def _summarize_joins(self) -> Dict[str, int]:
        """Summarize joins by type"""
        summary = {}
        for edge in self.edges:
            join_type = edge.join_type.value
            summary[join_type] = summary.get(join_type, 0) + 1
        return summary


if __name__ == "__main__":
    print("🔗 Assembly Graph Validator")
    print("=" * 60)
    
    graph = AssemblyGraph()
    
    # Register pieces
    graph.register_piece("center")
    graph.register_piece("petal_1")
    graph.register_piece("petal_2")
    graph.register_piece("petal_3")
    
    # Add joins (flower with 3 petals)
    graph.add_join("petal_1", "center", JoinType.SLIP_STITCH, line_number=10)
    graph.add_join("petal_2", "center", JoinType.SLIP_STITCH, line_number=15)
    graph.add_join("petal_3", "center", JoinType.SLIP_STITCH, line_number=20)
    
    # Validate
    is_valid = graph.validate_flower_assembly(3, "center")
    
    print(f"\nFlower Assembly Validation: {is_valid}")
    print(f"Total Pieces: {len(graph.pieces)}")
    print(f"Total Joins: {len(graph.edges)}")
    
    # Get report
    report = graph.get_assembly_report()
    print(f"\nAssembly Report:")
    print(f"  Complete: {report['assembly_complete']}")
    print(f"  Orphans: {report['orphan_pieces']}")
    print(f"  Join Summary: {report['join_summary']}")
    
    if report['warnings']:
        print(f"\nWarnings:")
        for warning in report['warnings']:
            print(f"  ⚠️ {warning}")
    
    if report['errors']:
        print(f"\nErrors:")
        for error in report['errors']:
            print(f"  ❌ {error}")
    
    print("\n✅ Assembly Graph Validator working!")
