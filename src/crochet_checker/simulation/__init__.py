"""Simulation package."""

from .mesh import (
    Mesh,
    Vec3,
    generate_flat_circle_mesh,
    generate_hat_mesh,
    generate_sphere_mesh,
    generate_tube_mesh,
)
from .surface import (
    DetectedShape,
    ShapeAnalysis,
    SurfaceSimulator,
    analyze_pattern_shape,
    simulate_surface,
)
