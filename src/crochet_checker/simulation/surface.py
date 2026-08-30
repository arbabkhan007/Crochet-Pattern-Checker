"""Surface simulation - converts crochet patterns to 3D surfaces."""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from ..model.pattern import Pattern
from ..visualization.measurements import MeasurementEngine, StitchDimensions, measure_pattern
from .mesh import Mesh, Vec3, generate_sphere_mesh, generate_tube_mesh, generate_flat_circle_mesh, generate_hat_mesh

class DetectedShape(str, Enum):
    FLAT_CIRCLE = "flat_circle"; SPHERE = "sphere"; HAT = "hat"
    TUBE = "tube"; CONE = "cone"; BOWL = "bowl"; UNKNOWN = "unknown"

class ShapeAnalysis(BaseModel):
    detected_shape: DetectedShape = DetectedShape.UNKNOWN
    confidence: float = 0.0
    max_radius_mm: float = 0.0
    height_mm: float = 0.0
    has_increases: bool = False
    has_decreases: bool = False
    increase_rounds: int = 0
    decrease_rounds: int = 0
    constant_rounds: int = 0
    explanation: str = ""

class SurfaceSimulator:
    def __init__(self, stitch_dims=None):
        self.dims = stitch_dims or StitchDimensions.for_worsted()
    def analyze_shape(self, pattern):
        a = ShapeAnalysis()
        if not pattern.rounds:
            a.explanation = "Pattern uses rows not rounds."; return a
        counts, prev = [], 0
        for r in pattern.rounds:
            sc = r.computed_stitch_count
            if sc == 0: sc = r.compute_stitch_count_with_context(prev)
            counts.append(sc); prev = sc if sc > 0 else prev
        if not counts: return a
        for i in range(1, len(counts)):
            if counts[i] > counts[i-1]: a.increase_rounds += 1; a.has_increases = True
            elif counts[i] < counts[i-1]: a.decrease_rounds += 1; a.has_decreases = True
            else: a.constant_rounds += 1
        m = measure_pattern(pattern, self.dims)
        a.max_radius_mm = m.max_radius_mm; a.height_mm = m.total_height_mm
        fc, lc = counts[0], counts[-1]
        if a.has_increases and not a.has_decreases:
            if a.constant_rounds > a.increase_rounds:
                a.detected_shape = DetectedShape.HAT; a.confidence = 0.8
                a.explanation = "Increases then constant - hat."
            elif lc > fc * 5:
                a.detected_shape = DetectedShape.FLAT_CIRCLE; a.confidence = 0.7
                a.explanation = "Steady increases - flat circle."
            else:
                a.detected_shape = DetectedShape.BOWL; a.confidence = 0.5
                a.explanation = "Increases - bowl or circle."
        elif a.has_increases and a.has_decreases:
            if lc < fc * 2 and lc <= 12:
                a.detected_shape = DetectedShape.SPHERE; a.confidence = 0.9
                a.explanation = "Increases then decreases to small count - sphere."
            elif a.constant_rounds > 0:
                a.detected_shape = DetectedShape.HAT; a.confidence = 0.85
                a.explanation = "Increases, constant, decreases - hat."
            else:
                a.detected_shape = DetectedShape.SPHERE; a.confidence = 0.7
                a.explanation = "Increases and decreases - sphere."
        elif a.has_decreases and not a.has_increases:
            a.detected_shape = DetectedShape.CONE; a.confidence = 0.6
            a.explanation = "Only decreases - cone."
        else:
            if a.constant_rounds >= len(counts) * 0.7:
                a.detected_shape = DetectedShape.TUBE; a.confidence = 0.8
                a.explanation = "Constant count - tube."
            else:
                a.detected_shape = DetectedShape.UNKNOWN; a.confidence = 0.3
                a.explanation = "Unknown shape."
        return a
    def generate_mesh(self, pattern):
        a = self.analyze_shape(pattern)
        m = measure_pattern(pattern, self.dims)
        radius = m.max_radius_mm / 10; height = m.total_height_mm / 10
        if radius <= 0: radius = 5.0
        if height <= 0: height = 5.0
        seg = 32
        s = a.detected_shape
        if s == DetectedShape.SPHERE: return generate_sphere_mesh(radius, seg, seg//2)
        elif s == DetectedShape.HAT: return generate_hat_mesh(radius, radius*1.3, height*0.7, height*0.05, seg)
        elif s == DetectedShape.FLAT_CIRCLE: return generate_flat_circle_mesh(radius, seg)
        elif s == DetectedShape.TUBE: return generate_tube_mesh(radius, radius, height, seg)
        elif s == DetectedShape.CONE: return generate_tube_mesh(radius, radius*0.3, height, seg)
        elif s == DetectedShape.BOWL: return generate_sphere_mesh(radius, seg, seg//4)
        else: return generate_sphere_mesh(radius, seg)

def simulate_surface(pattern, stitch_dims=None):
    return SurfaceSimulator(stitch_dims).generate_mesh(pattern)
def analyze_pattern_shape(pattern, stitch_dims=None):
    return SurfaceSimulator(stitch_dims).analyze_shape(pattern)
