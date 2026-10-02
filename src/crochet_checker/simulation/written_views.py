"""Write every written view. None of these files is a measured size or a photo."""

from __future__ import annotations

from pathlib import Path

from .assembly_map import assembly_map_svg, written_assembly
from .geometry_map import geometry_map_svg, geometry_table_csv, written_geometry
from .stitch_sim import simulate_stitches, stitch_map_svg, stitch_model_obj, stitch_table_csv
from .surface import simulate_surface

SHAPE_NOTE = (
    "The shape mesh does not track each loop. It is not a measured size and not a photo."
)


def write_written_views(pattern, out_dir, stem: str) -> dict:
    """Save the 2D map, 3D points, table, piece map, geometry, and shape mesh."""
    folder = Path(out_dir)
    folder.mkdir(parents=True, exist_ok=True)
    stitch_sim = simulate_stitches(pattern)
    assembly = written_assembly(pattern)
    geometry = written_geometry(pattern, stitch_sim)
    mesh = simulate_surface(pattern)
    files = {
        "stitch_map.svg": stitch_map_svg(stitch_sim, stem),
        "stitch_sim.obj": stitch_model_obj(stitch_sim),
        "stitch_map.csv": stitch_table_csv(stitch_sim),
        "assembly_map.svg": assembly_map_svg(assembly, stem),
        "geometry_map.svg": geometry_map_svg(geometry, stem),
        "geometry_map.csv": geometry_table_csv(geometry),
        "shape_mesh.obj": "# " + SHAPE_NOTE + "\n" + mesh.to_obj(),
    }
    for name, body in files.items():
        (folder / name).write_text(body)
    return {
        "stitch_sim": stitch_sim,
        "assembly": assembly,
        "geometry": geometry,
        "mesh": mesh,
        "files": files,
    }
