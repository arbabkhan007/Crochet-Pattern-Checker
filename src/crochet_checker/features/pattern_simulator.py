"""
Pattern Simulator - Visual simulation of crochet patterns before making them
"""
import json
import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class StitchType(Enum):
    CH = "ch"
    SC = "sc"
    HDC = "hdc"
    DC = "dc"
    TC = "tc"
    SL = "sl"
    INC = "inc"
    DEC = "dec"
    FO = "fo"
    MR = "mr"


@dataclass
class SimulatedStitch:
    """A single stitch in the simulation"""
    x: float
    y: float
    z: float
    stitch_type: StitchType
    round_number: int
    stitch_index: int
    color: str = "#FF6B6B"
    tension: float = 1.0  # 0.5=loose, 1.0=normal, 1.5=tight
    rotation: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'position': (self.x, self.y, self.z),
            'type': self.stitch_type.value,
            'round': self.round_number,
            'index': self.stitch_index,
            'color': self.color,
            'tension': self.tension
        }


@dataclass
class SimulationConfig:
    """Configuration for the simulation"""
    stitch_width: float = 5.0  # mm
    stitch_height: float = 4.0  # mm
    stitch_depth: float = 3.0  # mm
    gauge_stitches: int = 15  # per 10cm
    gauge_rows: int = 16  # per 10cm
    yarn_weight: str = "worsted"
    hook_size: float = 5.0  # mm
    tension: float = 1.0
    show_grid: bool = True
    show_rounds: bool = True
    show_dimensions: bool = True
    animation_speed: float = 1.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


class PatternSimulator:
    """
    Simulates crochet patterns to preview the final result
    
    Features:
    - Visual stitch-by-stitch simulation
    - 3D mesh generation
    - Color pattern visualization
    - Tension analysis
    - Size prediction
    - Animation support
    """
    
    STITCH_DIMENSIONS = {
        StitchType.CH: (3.0, 2.0, 1.0),
        StitchType.SC: (5.0, 4.0, 3.0),
        StitchType.HDC: (5.0, 5.5, 3.0),
        StitchType.DC: (5.0, 7.0, 3.0),
        StitchType.TC: (5.0, 9.0, 3.0),
        StitchType.SL: (3.0, 1.5, 1.0),
    }
    
    def __init__(self, config: SimulationConfig = None):
        self.config = config or SimulationConfig()
        self.stitches: List[SimulatedStitch] = []
        self.rounds: Dict[int, List[SimulatedStitch]] = {}
        self.dimensions: Optional[Tuple[float, float, float]] = None
        self.warnings: List[str] = []
    
    def simulate_from_pattern(self, pattern_data: Dict) -> Dict:
        """
        Simulate a pattern and return preview data
        
        Args:
            pattern_data: Parsed pattern data
            
        Returns:
            Simulation results with mesh, dimensions, preview
        """
        self.stitches = []
        self.rounds = {}
        self.warnings = []
        
        rounds = pattern_data.get('rounds', [])
        
        if not rounds:
            return {'error': 'No rounds found in pattern', 'stitches': []}
        
        for round_data in rounds:
            round_num = round_data.get('round_number', 0)
            instructions = round_data.get('instructions', '')
            
            self._simulate_round(round_num, instructions)
        
        self._calculate_dimensions()
        
        return {
            'total_stitches': len(self.stitches),
            'total_rounds': len(self.rounds),
            'dimensions': self.dimensions,
            'stitches_by_type': self._count_stitches_by_type(),
            'tension_analysis': self._analyze_tension(),
            'warnings': self.warnings,
            'mesh_data': self._generate_mesh_data(),
            'preview_svg': self._generate_preview_svg(),
            'estimated_yarn': self._estimate_yarn_usage(),
            'estimated_time': self._estimate_time()
        }
    
    def _simulate_round(self, round_num: int, instructions: str):
        """Simulate a single round of stitches"""
        round_stitches = []
        
        stitch_count = self._parse_stitch_count(instructions)
        prev_count = len(self.rounds.get(round_num - 1, [])) if round_num > 1 else 0
        
        if round_num == 1:
            # First round - circular start
            angle_step = 360.0 / stitch_count if stitch_count > 0 else 60
            for i in range(stitch_count):
                angle = math.radians(i * angle_step)
                radius = self.config.stitch_width * 0.5
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                z = 0
                
                stitch = SimulatedStitch(
                    x=x, y=y, z=z,
                    stitch_type=StitchType.SC,
                    round_number=round_num,
                    stitch_index=i,
                    tension=self.config.tension
                )
                round_stitches.append(stitch)
        else:
            # Subsequent rounds - expand outward
            prev_radius = self._get_round_radius(round_num - 1)
            new_radius = prev_radius + self.config.stitch_height * 0.7
            
            angle_step = 360.0 / stitch_count if stitch_count > 0 else 30
            for i in range(stitch_count):
                angle = math.radians(i * angle_step)
                x = new_radius * math.cos(angle)
                y = new_radius * math.sin(angle)
                z = self.config.stitch_depth * (round_num - 1) * 0.3
                
                stitch = SimulatedStitch(
                    x=x, y=y, z=z,
                    stitch_type=StitchType.SC,
                    round_number=round_num,
                    stitch_index=i,
                    tension=self.config.tension
                )
                round_stitches.append(stitch)
            
            # Check for issues
            if prev_count > 0:
                change = stitch_count - prev_count
                if change > prev_count * 0.5:
                    self.warnings.append(
                        f"Round {round_num}: Large increase ({change} stitches). "
                        "May cause ruffling."
                    )
                elif change < -prev_count * 0.3:
                    self.warnings.append(
                        f"Round {round_num}: Large decrease ({abs(change)} stitches). "
                        "May cause puckering."
                    )
        
        self.stitches.extend(round_stitches)
        self.rounds[round_num] = round_stitches
    
    def _parse_stitch_count(self, instructions: str) -> int:
        """Extract stitch count from instructions"""
        # Try to find count in parentheses at end
        import re
        match = re.search(r'\((\d+)\)\s*$', instructions)
        if match:
            return int(match.group(1))
        
        # Estimate from instructions
        count = 0
        parts = instructions.lower().split()
        for i, part in enumerate(parts):
            if part in ('sc', 'hdc', 'dc', 'tc', 'ch', 'sl'):
                count += 1
            elif part == 'inc':
                count += 2
            elif part == 'dec':
                count += 1
            elif part == 'repeat' and i > 0:
                try:
                    repeat_count = int(parts[i-1]) if parts[i-1].isdigit() else 1
                    count *= repeat_count
                except:
                    pass
        
        return max(count, 6)  # Minimum 6 stitches for a circle
    
    def _get_round_radius(self, round_num: int) -> float:
        """Get the radius of a specific round"""
        if round_num not in self.rounds:
            return 0
        
        stitches = self.rounds[round_num]
        if not stitches:
            return 0
        
        return max(math.sqrt(s.x**2 + s.y**2) for s in stitches)
    
    def _calculate_dimensions(self):
        """Calculate overall dimensions of the simulated piece"""
        if not self.stitches:
            self.dimensions = (0, 0, 0)
            return
        
        xs = [s.x for s in self.stitches]
        ys = [s.y for s in self.stitches]
        zs = [s.z for s in self.stitches]
        
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        depth = max(zs) - min(zs)
        
        self.dimensions = (
            round(width, 1),
            round(height, 1),
            round(depth, 1)
        )
    
    def _count_stitches_by_type(self) -> Dict[str, int]:
        """Count stitches by type"""
        counts = {}
        for s in self.stitches:
            name = s.stitch_type.value
            counts[name] = counts.get(name, 0) + 1
        return counts
    
    def _analyze_tension(self) -> Dict:
        """Analyze tension consistency"""
        if not self.stitches:
            return {'consistent': True, 'score': 100}
        
        tensions = [s.tension for s in self.stitches]
        avg = sum(tensions) / len(tensions)
        variance = sum((t - avg) ** 2 for t in tensions) / len(tensions)
        std_dev = math.sqrt(variance)
        
        score = max(0, 100 - std_dev * 50)
        consistent = std_dev < 0.1
        
        return {
            'consistent': consistent,
            'score': round(score, 1),
            'average_tension': round(avg, 2),
            'std_deviation': round(std_dev, 3),
            'min_tension': round(min(tensions), 2),
            'max_tension': round(max(tensions), 2)
        }
    
    def _generate_mesh_data(self) -> Dict:
        """Generate mesh data for 3D rendering"""
        vertices = []
        faces = []
        
        for i, stitch in enumerate(self.stitches):
            dims = self.STITCH_DIMENSIONS.get(stitch.stitch_type, (5, 4, 3))
            w, h, d = dims
            
            # Create a box for each stitch
            base_idx = len(vertices)
            vertices.extend([
                (stitch.x - w/2, stitch.y - h/2, stitch.z),
                (stitch.x + w/2, stitch.y - h/2, stitch.z),
                (stitch.x + w/2, stitch.y + h/2, stitch.z),
                (stitch.x - w/2, stitch.y + h/2, stitch.z),
                (stitch.x - w/2, stitch.y - h/2, stitch.z + d),
                (stitch.x + w/2, stitch.y - h/2, stitch.z + d),
                (stitch.x + w/2, stitch.y + h/2, stitch.z + d),
                (stitch.x - w/2, stitch.y + h/2, stitch.z + d),
            ])
            
            faces.extend([
                (base_idx, base_idx+1, base_idx+2, base_idx+3),
                (base_idx+4, base_idx+5, base_idx+6, base_idx+7),
                (base_idx, base_idx+1, base_idx+5, base_idx+4),
                (base_idx+2, base_idx+3, base_idx+7, base_idx+6),
                (base_idx, base_idx+3, base_idx+7, base_idx+4),
                (base_idx+1, base_idx+2, base_idx+6, base_idx+5),
            ])
        
        return {
            'vertices': vertices,
            'faces': faces,
            'vertex_count': len(vertices),
            'face_count': len(faces)
        }
    
    def _generate_preview_svg(self) -> str:
        """Generate SVG preview of the pattern"""
        if not self.stitches:
            return "<svg></svg>"
        
        xs = [s.x for s in self.stitches]
        ys = [s.y for s in self.stitches]
        
        padding = 20
        min_x = min(xs) - padding
        min_y = min(ys) - padding
        max_x = max(xs) + padding
        max_y = max(ys) + padding
        width = max_x - min_x
        height = max_y - min_y
        
        scale = min(400 / width, 400 / height) if width > 0 and height > 0 else 1
        
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" '
            f'viewBox="{min_x} {min_y} {width} {height}">'
        ]
        
        # Background
        svg_parts.append(
            f'<rect x="{min_x}" y="{min_y}" width="{width}" height="{height}" '
            f'fill="#f5f5f5"/>'
        )
        
        # Draw stitches
        for stitch in self.stitches:
            r = self.config.stitch_width * 0.3
            svg_parts.append(
                f'<circle cx="{stitch.x}" cy="{stitch.y}" r="{r}" '
                f'fill="{stitch.color}" stroke="#333" stroke-width="0.5" '
                f'opacity="0.8"/>'
            )
        
        # Draw round labels
        for round_num, round_stitches in self.rounds.items():
            if round_stitches:
                s = round_stitches[0]
                svg_parts.append(
                    f'<text x="{s.x + 10}" y="{s.y}" font-size="5" '
                    f'fill="#666">R{round_num}</text>'
                )
        
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)
    
    def _estimate_yarn_usage(self) -> Dict:
        """Estimate yarn usage in meters/grams"""
        stitch_length = {
            StitchType.CH: 8,
            StitchType.SC: 12,
            StitchType.HDC: 16,
            StitchType.DC: 20,
            StitchType.TC: 24,
            StitchType.SL: 5,
        }
        
        total_mm = 0
        for s in self.stitches:
            length = stitch_length.get(s.stitch_type, 12)
            total_mm += length * s.tension
        
        meters = total_mm / 1000
        grams = meters * 0.3  # Approximate for worsted weight
        
        return {
            'total_meters': round(meters, 1),
            'total_yards': round(meters * 1.094, 1),
            'estimated_grams': round(grams, 0),
            'skeins_needed': max(1, math.ceil(grams / 50))  # 50g per skein
        }
    
    def _estimate_time(self) -> Dict:
        """Estimate time to complete"""
        stitch_time_minutes = {
            StitchType.CH: 0.05,
            StitchType.SC: 0.1,
            StitchType.HDC: 0.12,
            StitchType.DC: 0.15,
            StitchType.TC: 0.18,
            StitchType.SL: 0.03,
        }
        
        total_minutes = 0
        for s in self.stitches:
            time = stitch_time_minutes.get(s.stitch_type, 0.1)
            total_minutes += time
        
        hours = total_minutes / 60
        
        if hours < 1:
            time_str = f"{int(total_minutes)} minutes"
        elif hours < 24:
            time_str = f"{hours:.1f} hours"
        else:
            days = hours / 24
            time_str = f"{days:.1f} days"
        
        return {
            'total_minutes': round(total_minutes, 0),
            'total_hours': round(hours, 1),
            'estimated_string': time_str,
            'skill_level': 'Beginner' if total_minutes < 60 else
                          'Intermediate' if total_minutes < 300 else
                          'Advanced'
        }
    
    def export_simulation(self, format: str = "json") -> str:
        """Export simulation results"""
        result = {
            'total_stitches': len(self.stitches),
            'total_rounds': len(self.rounds),
            'dimensions': self.dimensions,
            'config': self.config.to_dict(),
            'mesh_data': self._generate_mesh_data(),
            'preview_svg': self._generate_preview_svg(),
            'yarn_estimate': self._estimate_yarn_usage(),
            'time_estimate': self._estimate_time()
        }
        
        if format == "json":
            return json.dumps(result, indent=2)
        elif format == "svg":
            return self._generate_preview_svg()
        
        return json.dumps(result)


# ===========================================================
# DEMO
# ===========================================================

if __name__ == "__main__":
    print("""
+==========================================================+
|     [crystal] PATTERN SIMULATOR - DEMONSTRATION                |
+==========================================================+
    """)
    
    simulator = PatternSimulator()
    
    sample = {
        'rounds': [
            {'round_number': 1, 'instructions': '6 sc in magic ring (6)'},
            {'round_number': 2, 'instructions': 'inc in each st around (12)'},
            {'round_number': 3, 'instructions': '(sc, inc) repeat around (18)'},
            {'round_number': 4, 'instructions': '(2 sc, inc) repeat around (24)'},
            {'round_number': 5, 'instructions': '(3 sc, inc) repeat around (30)'},
            {'round_number': 6, 'instructions': 'sc in each st around (30)'},
            {'round_number': 7, 'instructions': '(4 sc, inc) repeat around (36)'},
            {'round_number': 8, 'instructions': 'sc in each st around (36)'},
        ]
    }
    
    print("[crystal] Simulating pattern...")
    result = simulator.simulate_from_pattern(sample)
    
    print(f"\n[CHART] SIMULATION RESULTS")
    print("=" * 50)
    print(f"  Total Stitches:    {result['total_stitches']}")
    print(f"  Total Rounds:      {result['total_rounds']}")
    print(f"  Dimensions:        {result['dimensions']} mm (WxHxD)")
    
    print(f"\n[yarn] STITCH BREAKDOWN:")
    for stype, count in result['stitches_by_type'].items():
        print(f"  {stype}: {count}")
    
    print(f"\n TENSION ANALYSIS:")
    tension = result['tension_analysis']
    print(f"  Consistent: {'[OK] Yes' if tension['consistent'] else '[!] No'}")
    print(f"  Score: {tension['score']}/100")
    print(f"  Average: {tension['average_tension']}")
    
    print(f"\n[YARN] YARN ESTIMATE:")
    yarn = result['estimated_yarn']
    print(f"  Total: {yarn['total_meters']}m ({yarn['total_yards']} yards)")
    print(f"  Weight: ~{int(yarn['estimated_grams'])}g")
    print(f"  Skeins: {yarn['skeins_needed']}")
    
    print(f"\n? TIME ESTIMATE:")
    time = result['estimated_time']
    print(f"  Duration: {time['estimated_string']}")
    print(f"  Skill Level: {time['skill_level']}")
    
    if result['warnings']:
        print(f"\n[!] WARNINGS:")
        for w in result['warnings']:
            print(f"  - {w}")
    
    print(f"\n[COLOR] SVG Preview generated ({len(result['preview_svg'])} chars)")
    print(f" Mesh data: {result['mesh_data']['vertex_count']} vertices, "
          f"{result['mesh_data']['face_count']} faces")
    
    print("\n[OK] Pattern Simulator Complete! ")
