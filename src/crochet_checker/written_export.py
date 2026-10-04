"""Write an existing written view in another file type."""

from __future__ import annotations

import base64
import json
import struct

from .parser import CrochetParser
from .pdf.generator import generate_pdf_html
from .simulation.stitch_sim import HONESTY, simulate_stitches, stitch_map_svg, stitch_model_obj

FORMATS = ("obj", "gltf", "svg", "html")
REFUSED = "indd is not a format. This does not write a print-shop file."


def export_text(pattern_text: str, fmt: str) -> str:
    if fmt == "indd":
        raise ValueError(REFUSED)
    if fmt not in FORMATS:
        raise ValueError(f"{fmt} is not a format. Use obj, gltf, svg, or html.")
    pattern = CrochetParser().parse(pattern_text)
    if fmt == "html":
        return generate_pdf_html(pattern)
    simulation = simulate_stitches(pattern)
    if fmt == "obj":
        return stitch_model_obj(simulation)
    if fmt == "svg":
        return stitch_map_svg(simulation)
    return _points_gltf(simulation)


def _points_gltf(simulation) -> str:
    note = HONESTY + " These coordinates are not millimetres."
    points = [(stitch.x, stitch.y, stitch.z) for stitch in simulation.stitches]
    if not points:
        return json.dumps(
            {
                "asset": {"version": "2.0", "extras": {"note": note}},
                "scenes": [{"nodes": []}],
                "nodes": [],
            },
            indent=2,
        ) + "\n"
    blob = b"".join(struct.pack("<fff", x, y, z) for x, y, z in points)
    document = {
        "asset": {"version": "2.0", "extras": {"note": note}},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "mode": 0}]}],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,
                "count": len(points),
                "type": "VEC3",
                "min": [min(p[0] for p in points), min(p[1] for p in points), min(p[2] for p in points)],
                "max": [max(p[0] for p in points), max(p[1] for p in points), max(p[2] for p in points)],
            }
        ],
        "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": len(blob)}],
        "buffers": [
            {
                "uri": "data:application/octet-stream;base64," + base64.b64encode(blob).decode("ascii"),
                "byteLength": len(blob),
            }
        ],
    }
    return json.dumps(document, indent=2) + "\n"
