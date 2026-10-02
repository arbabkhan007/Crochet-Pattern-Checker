"""Map written stitch order to a model radius and layer.

A round radius is the stitch count divided by 2 pi. A row width is the stitch
count. z is the layer index. None of these is a millimetre.
"""

from __future__ import annotations

import html
import math

from pydantic import BaseModel, Field

GEOMETRY_NOTE = (
    "Geometry uses the written stitch order. For a round, radius is the stitch "
    "count divided by 2 pi. For a row, width is the stitch count. z is the layer "
    "index. None of these is a millimetre, a photo, or a measured size."
)
_COPY_NOTE = (
    "A copy index is a written make count, not a made piece and not a measurement."
)
_SVG_LIMIT = 40


class GeometryLayer(BaseModel):
    piece: str
    copy_index: int
    round_number: int
    stitch_count: int
    is_round: bool
    radius: float
    width: float
    z: int


class GeometryMap(BaseModel):
    layers: list[GeometryLayer] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


def written_geometry(pattern, simulation=None) -> GeometryMap:
    """Read placement geometry from written join targets. Do not invent a size."""
    from .stitch_sim import simulate_stitches

    if simulation is None:
        simulation = simulate_stitches(pattern)
    grouped: dict[tuple, list] = {}
    for stitch in simulation.stitches:
        if not stitch.is_join_target:
            continue
        key = (stitch.piece, stitch.copy_index, stitch.round_number, int(stitch.z))
        grouped.setdefault(key, []).append(stitch)
    layers: list[GeometryLayer] = []
    for (piece, copy_index, number, layer), stitches in grouped.items():
        count = len(stitches)
        is_round = bool(stitches[0].is_round)
        if is_round:
            radius = count / (2 * math.pi) if count else 0.0
            width = 0.0
        else:
            radius = 0.0
            width = float(count)
        layers.append(
            GeometryLayer(
                piece=piece or "piece",
                copy_index=copy_index,
                round_number=int(number),
                stitch_count=count,
                is_round=is_round,
                radius=radius,
                width=width,
                z=layer,
            )
        )
    notes = [GEOMETRY_NOTE]
    if not layers:
        notes.append("No written stitch was placed, so no size was invented.")
    if any(layer.copy_index > 0 for layer in layers):
        notes.append(_COPY_NOTE)
    return GeometryMap(layers=layers, notes=notes)


def geometry_map_svg(geometry: GeometryMap, title: str = "Geometry map") -> str:
    """A table of written layers. Not a measured diagram."""
    width, height = 760, 220 + 18 * min(len(geometry.layers), _SVG_LIMIT)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="24" y="32" font-family="sans-serif" font-size="18" fill="#243042">'
        f"{_xml(title)}</text>",
        '<text x="24" y="54" font-family="sans-serif" font-size="11" fill="#5c6b7a">'
        "Not a millimetre measurement.</text>",
    ]
    if not geometry.layers:
        parts.append(
            '<text x="24" y="92" font-family="sans-serif" font-size="13" fill="#5c6b7a">'
            "No written stitch was placed.</text></svg>"
        )
        return "\n".join(parts)
    y = 84
    parts.append(
        f'<text x="24" y="{y}" font-family="sans-serif" font-size="11" fill="#243042">'
        "piece  copy  round  count  model  z</text>"
    )
    y += 18
    for layer in geometry.layers[:_SVG_LIMIT]:
        if layer.is_round:
            model = f"radius {layer.radius:.3f}"
        else:
            model = f"width {layer.width:.0f}"
        label = (
            f"{layer.piece}  {layer.copy_index}  {layer.round_number}  "
            f"{layer.stitch_count}  {model}  {layer.z}"
        )
        parts.append(
            f'<text x="24" y="{y}" font-family="sans-serif" font-size="11" fill="#243042">'
            f"{_xml(label)}</text>"
        )
        y += 16
    if len(geometry.layers) > _SVG_LIMIT:
        parts.append(
            f'<text x="24" y="{y}" font-family="sans-serif" font-size="11" fill="#5c6b7a">'
            f"The first {_SVG_LIMIT} layers are drawn. The CSV has every layer.</text>"
        )
    parts.append("</svg>")
    return "\n".join(parts)


def geometry_table_csv(geometry: GeometryMap) -> str:
    """One row per written layer. Not a millimetre measurement."""
    lines = [
        "# Radius is stitch count / 2 pi for a round. Width is the stitch count for a row. "
        "z is the layer index. Not a millimetre measurement.",
        "piece,copy,round,stitch_count,kind,radius,width,z",
    ]
    for layer in geometry.layers:
        kind = "round" if layer.is_round else "row"
        lines.append(
            ",".join(
                [
                    _csv(layer.piece),
                    str(layer.copy_index),
                    str(layer.round_number),
                    str(layer.stitch_count),
                    kind,
                    f"{layer.radius:.6f}",
                    f"{layer.width:.0f}",
                    str(layer.z),
                ]
            )
        )
    return "\n".join(lines) + "\n"


def _xml(text: str) -> str:
    return html.escape(text, quote=True)


def _csv(text: str) -> str:
    if any(character in text for character in ",\"\n"):
        return '"' + text.replace('"', '""') + '"'
    return text
