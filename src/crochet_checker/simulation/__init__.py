"""Simulation package."""

from .mesh import (
    Mesh,
    Vec3,
    generate_flat_circle_mesh,
    generate_hat_mesh,
    generate_sphere_mesh,
    generate_tube_mesh,
)
from .assembly_map import ASSEMBLY_NOTE, AssemblyMap, assembly_map_svg, written_assembly
from .stitch_sim import (
    HONESTY,
    MappedStitch,
    StitchSimulation,
    simulate_stitches,
    stitch_map_svg,
    stitch_model_obj,
    stitch_table_csv,
)
from .surface import (
    DetectedShape,
    ShapeAnalysis,
    SurfaceSimulator,
    analyze_pattern_shape,
    simulate_surface,
)
