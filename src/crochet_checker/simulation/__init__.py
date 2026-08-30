"""Simulation package."""
from .mesh import Mesh, Vec3, generate_sphere_mesh, generate_tube_mesh, generate_flat_circle_mesh, generate_hat_mesh
from .surface import SurfaceSimulator, DetectedShape, ShapeAnalysis, simulate_surface, analyze_pattern_shape
