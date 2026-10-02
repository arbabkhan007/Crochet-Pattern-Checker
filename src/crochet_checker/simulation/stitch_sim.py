"""Place one point for each written stitch.

The coordinates are a geometric model of the written order. They are not a
measured size and not a photo. A join is recorded only when the written stitch
consumes a stitch in the previous round and that stitch was placed. A missing
join is not guessed.
"""

from __future__ import annotations

import math
import re

from pydantic import BaseModel, Field

from ..model.stitch import STITCH_CONSUMPTION, STITCH_PRODUCTION, StitchType

HONESTY = (
    "Each point is one written stitch. The position is a geometric model, "
    "not a measured size and not a photo. A line is drawn only when that "
    "stitch consumes a previous stitch and the counts fit. A missing join "
    "is not guessed."
)

_EACH = {"each_stitch_around", "each_stitch_across", "remaining"}
_SKIP_TYPES = {
    StitchType.MAGIC_RING,
    StitchType.SKIP,
    StitchType.FASTEN_OFF,
    StitchType.SEW,
}
_MAX_STITCHES = 50000


class MappedStitch(BaseModel):
    piece: str
    copy_index: int
    round_number: int
    index: int
    stitch_type: str
    x: float
    y: float
    z: float
    parents: list[int] = Field(default_factory=list)
    is_join_target: bool = True
    color_label: str = ""
    color_hex: str = ""


class StitchSimulation(BaseModel):
    stitches: list[MappedStitch] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @property
    def stitch_count(self) -> int:
        return len(self.stitches)

    @property
    def join_count(self) -> int:
        return sum(len(item.parents) for item in self.stitches)


def simulate_stitches(pattern) -> StitchSimulation:
    """Map every written stitch to a model coordinate."""
    notes = [HONESTY]
    stitches: list[MappedStitch] = []
    unmatched = False
    stated_mismatch = False
    chain_placed = False
    join_skipped = False
    stopped = False
    made_copies = False
    color_split = False
    color_unknown = False
    color_labeled = False
    color_missing = False
    pattern_text = getattr(pattern, "source_text", "") or ""

    sections = _sections(pattern)
    origin_x = 0.0
    for name, copies, units, is_round in sections:
        if copies > 1:
            made_copies = True
        span = _piece_span(units, is_round)
        piece_max = origin_x
        for copy in range(copies):
            placed, flags = _place_piece(
                name,
                copy,
                units,
                is_round,
                origin_x + copy * span,
                pattern_text,
            )
            if len(stitches) + len(placed) > _MAX_STITCHES:
                room = _MAX_STITCHES - len(stitches)
                stitches.extend(placed[: max(room, 0)])
                stopped = True
                break
            stitches.extend(placed)
            unmatched = unmatched or flags["unmatched"]
            stated_mismatch = stated_mismatch or flags["stated_mismatch"]
            chain_placed = chain_placed or flags["chain_placed"]
            join_skipped = join_skipped or flags["join_skipped"]
            color_split = color_split or flags["color_split"]
            color_unknown = color_unknown or flags["color_unknown"]
            color_labeled = color_labeled or flags["color_labeled"]
            color_missing = color_missing or flags["color_missing"]
            if placed:
                piece_max = max(piece_max, max(item.x for item in placed))
        if stopped:
            break
        origin_x = piece_max + 8.0

    if chain_placed:
        notes.append(
            "A written chain is placed. The checker's round count does not "
            "treat that chain as a produced body stitch."
        )
    if join_skipped:
        notes.append("A join slip stitch was not added as a new stitch.")
    if unmatched:
        notes.append(
            "Some written stitches had no previous stitch left to join. "
            "The missing join was not guessed."
        )
    if stated_mismatch:
        notes.append(
            "A stated count does not match the stitches placed from the "
            "instructions. The stated number was not substituted."
        )
    if made_copies:
        notes.append(
            "Copies follow the written make count. They were not made or measured."
        )
    if stopped:
        notes.append(
            "Stopped after 50000 written stitches. No further stitch was invented."
        )
    if color_split:
        notes.append(
            "A round names more than one color. The split was not guessed."
        )
    if color_unknown:
        notes.append(
            "A written color name has no sheet swatch. A dye was not invented."
        )
    if color_labeled:
        notes.append("A color letter is a label, not a measured dye.")
    if color_missing and stitches:
        notes.append("Some stitches have no written color. No color was invented.")
    if not stitches:
        notes.append("No written stitch was placed.")
    return StitchSimulation(stitches=stitches, notes=notes)


def stitch_map_svg(simulation: StitchSimulation, title: str = "Stitch map") -> str:
    """Two-view SVG of the stitch model. Not a photo."""
    width, height = 920, 1040
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="24" y="32" font-family="sans-serif" font-size="18" '
        f'fill="#243042">{_xml(title)}</text>',
    ]
    note = " ".join(simulation.notes)
    parts.append(
        f'<text x="24" y="54" font-family="sans-serif" font-size="11" fill="#5c6b7a">'
        f"{_xml(note[:220])}</text>"
    )
    parts.append(_panel(simulation, 24, 78, 872, 430, "top"))
    parts.append(_panel(simulation, 24, 530, 872, 430, "side"))
    parts.append(
        f'<text x="24" y="990" font-family="sans-serif" font-size="12" fill="#243042">'
        f"{simulation.stitch_count} written stitches, {simulation.join_count} joins drawn. "
        f"Not a measured size.</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def stitch_model_obj(simulation: StitchSimulation) -> str:
    """OBJ points and join lines. Not a measured mesh."""
    lines = [
        "# Crochet stitch model",
        "# " + HONESTY,
        f"# stitches {simulation.stitch_count}",
    ]
    for stitch in simulation.stitches:
        lines.append(
            f"v {stitch.x:.4f} {stitch.y:.4f} {stitch.z:.4f}"
        )
    by_key: dict[tuple[str, int, int], list[int]] = {}
    for index, stitch in enumerate(simulation.stitches):
        by_key.setdefault((stitch.piece, stitch.copy_index, stitch.round_number), []).append(index)
    rounds: dict[tuple[str, int], list[int]] = {}
    for stitch in simulation.stitches:
        rounds.setdefault((stitch.piece, stitch.copy_index), [])
        if stitch.round_number not in rounds[(stitch.piece, stitch.copy_index)]:
            rounds[(stitch.piece, stitch.copy_index)].append(stitch.round_number)
    for (piece, copy_index), numbers in rounds.items():
        order = {number: position for position, number in enumerate(numbers)}
        for stitch_index, stitch in enumerate(simulation.stitches):
            if stitch.piece != piece or stitch.copy_index != copy_index or not stitch.parents:
                continue
            position = order.get(stitch.round_number)
            if position is None or position == 0:
                continue
            previous = numbers[position - 1]
            targets = [
                index
                for index in by_key.get((piece, copy_index, previous), [])
                if simulation.stitches[index].is_join_target
            ]
            for parent in stitch.parents:
                if 0 <= parent < len(targets):
                    lines.append(f"l {targets[parent] + 1} {stitch_index + 1}")
    return "\n".join(lines) + "\n"


def _sections(pattern):
    if getattr(pattern, "pieces", None):
        for piece in pattern.pieces:
            copies = piece.make_count if piece.make_count is not None else 1
            if copies < 1:
                continue
            if piece.rounds:
                yield piece.name or "piece", copies, piece.rounds, True
            elif piece.rows:
                yield piece.name or "piece", copies, piece.rows, False
        return
    if getattr(pattern, "rounds", None):
        yield "pattern", 1, pattern.rounds, True
    elif getattr(pattern, "rows", None):
        yield "pattern", 1, pattern.rows, False


def _piece_span(units, is_round) -> float:
    widest = 1
    previous = 0
    for unit in units:
        count = _body_count(unit, previous)
        widest = max(widest, count, previous)
        previous = count or previous
    if is_round:
        return (widest / math.pi) + 6.0
    return widest + 4.0


def _body_count(unit, previous: int) -> int:
    return len(_expand(unit, previous, "piece", 0)[0])


def _place_piece(name, copy_index, units, is_round, origin_x, pattern_text=""):
    flags = {
        "unmatched": False,
        "stated_mismatch": False,
        "chain_placed": False,
        "join_skipped": False,
        "color_split": False,
        "color_unknown": False,
        "color_labeled": False,
        "color_missing": False,
    }
    placed: list[MappedStitch] = []
    previous_targets: list[MappedStitch] = []
    for layer, unit in enumerate(units):
        raw, local_flags = _expand(unit, len(previous_targets), name, copy_index)
        label, hex_color, kind = _color_for_unit(unit, pattern_text)
        for item in raw:
            item.color_label = label
            item.color_hex = hex_color
        local_flags["color_split"] = kind == "split"
        local_flags["color_unknown"] = kind == "unknown"
        local_flags["color_labeled"] = kind == "labeled"
        local_flags["color_missing"] = kind == "missing"
        for key in flags:
            flags[key] = flags[key] or local_flags[key]
        targets = [item for item in raw if item.is_join_target]
        count = max(len(targets), 1)
        for index, item in enumerate(targets):
            if is_round:
                theta = (2 * math.pi * index / count) - (math.pi / 2)
                radius = count / (2 * math.pi)
                item.x = origin_x + radius * math.cos(theta)
                item.y = radius * math.sin(theta)
                item.z = float(layer)
            else:
                item.x = origin_x + float(index)
                item.y = 0.0
                item.z = float(layer)
        for index, item in enumerate(raw):
            if item.is_join_target:
                continue
            item.x = origin_x - 1.0
            item.y = -1.0 - (index * 0.15)
            item.z = float(layer)
        _resolve_parents(raw, previous_targets)
        placed.extend(raw)
        if targets:
            previous_targets = targets
        elif raw:
            previous_targets = [item for item in raw if item.stitch_type == "chain"]
        else:
            previous_targets = []
    return placed, flags


def _resolve_parents(raw, previous_targets):
    for item in raw:
        kept = []
        for parent in item.parents:
            if 0 <= parent < len(previous_targets):
                kept.append(parent)
        item.parents = kept


def _expand(unit, previous_count: int, piece: str, copy_index: int):
    flags = {
        "unmatched": False,
        "stated_mismatch": False,
        "chain_placed": False,
        "join_skipped": False,
    }
    raw: list[MappedStitch] = []
    cursor = 0
    number = getattr(unit, "round_number", None)
    if number is None:
        number = getattr(unit, "row_number", 0)

    def add(kind: str, parents: list[int], target: bool) -> None:
        raw.append(
            MappedStitch(
                piece=piece,
                copy_index=copy_index,
                round_number=number,
                index=len(raw),
                stitch_type=kind,
                x=0.0,
                y=0.0,
                z=0.0,
                parents=list(parents),
                is_join_target=target,
            )
        )

    for instruction in getattr(unit, "instructions", []) or []:
        groups = []
        if instruction.is_repeat_block and instruction.repeat_unit and instruction.repeat_count:
            groups.extend([instruction.repeat_unit] * instruction.repeat_count)
        elif instruction.operations:
            groups.append(instruction.operations)
        for group in groups:
            for op in group:
                kind = op.stitch_type
                into = op.into_stitch or ""
                if into == "join":
                    flags["join_skipped"] = True
                    continue
                if kind in _SKIP_TYPES:
                    if kind == StitchType.SKIP:
                        step = STITCH_CONSUMPTION.get(kind, 1) * max(op.count, 0)
                        if cursor + step > previous_count:
                            flags["unmatched"] = True
                        cursor += step
                    continue
                if into in _EACH:
                    remaining = max(previous_count - cursor, 0)
                    per = STITCH_PRODUCTION.get(kind, 1)
                    if per <= 0:
                        per = 1 if kind == StitchType.CHAIN else 0
                    if remaining == 0 or per == 0:
                        flags["unmatched"] = True
                        cursor = previous_count
                        continue
                    for index in range(remaining):
                        parent = cursor + index
                        parents = [parent] if parent < previous_count else []
                        if not parents:
                            flags["unmatched"] = True
                        produced = per
                        for _ in range(produced):
                            add(kind.value, parents, kind != StitchType.CHAIN)
                    cursor = previous_count
                    continue
                if kind == StitchType.CHAIN:
                    for _ in range(max(op.count, 0)):
                        add("chain", [], False)
                        flags["chain_placed"] = True
                    continue
                per = STITCH_PRODUCTION.get(kind, 1)
                cons = STITCH_CONSUMPTION.get(kind, 1)
                if per <= 0:
                    continue
                for _ in range(max(op.count, 0)):
                    parents = []
                    for _consumed in range(max(cons, 0)):
                        if cursor < previous_count:
                            parents.append(cursor)
                        else:
                            flags["unmatched"] = True
                        cursor += 1
                    for _produced in range(per):
                        add(kind.value, parents, True)

    targets = [item for item in raw if item.stitch_type != "chain"]
    if targets:
        for item in raw:
            item.is_join_target = item.stitch_type != "chain"
    else:
        for item in raw:
            item.is_join_target = True
    stated = _stated_count(unit)
    comparable = len(targets) if targets else len(raw)
    if stated is not None and stated != comparable:
        flags["stated_mismatch"] = True
    return raw, flags


def _stated_count(unit) -> int | None:
    for instruction in getattr(unit, "instructions", []) or []:
        if instruction.stated_stitch_count is not None:
            return instruction.stated_stitch_count
    expected = getattr(unit, "expected_ending_stitch_count", None)
    return expected


def _panel(simulation, left, top, width, height, mode: str) -> str:
    label = "Top view" if mode == "top" else "Side view"
    parts = [
        f'<text x="{left}" y="{top + 16}" font-family="sans-serif" font-size="13" '
        f'fill="#243042">{label}</text>'
    ]
    if not simulation.stitches:
        parts.append(
            f'<text x="{left}" y="{top + 40}" font-family="sans-serif" font-size="12" '
            f'fill="#5c6b7a">No written stitch was placed.</text>'
        )
        return "\n".join(parts)
    xs, ys = [], []
    for stitch in simulation.stitches:
        xs.append(stitch.x)
        ys.append(stitch.y if mode == "top" else stitch.z)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(max_x - min_x, 1.0)
    span_y = max(max_y - min_y, 1.0)
    plot_left, plot_top = left + 12, top + 28
    plot_w, plot_h = width - 24, height - 40
    scale = min(plot_w / span_x, plot_h / span_y)

    def project(stitch):
        px = plot_left + (stitch.x - min_x) * scale
        source = stitch.y if mode == "top" else stitch.z
        py = plot_top + plot_h - (source - min_y) * scale
        return px, py

    if mode == "top":
        lookup = {
            (item.piece, item.copy_index, item.round_number, item.index): item
            for item in simulation.stitches
        }
        by_round: dict[tuple[str, int], list[int]] = {}
        for item in simulation.stitches:
            by_round.setdefault((item.piece, item.copy_index), [])
            if item.round_number not in by_round[(item.piece, item.copy_index)]:
                by_round[(item.piece, item.copy_index)].append(item.round_number)
        for stitch in simulation.stitches:
            numbers = by_round.get((stitch.piece, stitch.copy_index), [])
            if stitch.round_number not in numbers:
                continue
            position = numbers.index(stitch.round_number)
            if position == 0:
                continue
            previous_number = numbers[position - 1]
            targets = [
                item
                for item in simulation.stitches
                if item.piece == stitch.piece
                and item.copy_index == stitch.copy_index
                and item.round_number == previous_number
                and item.is_join_target
            ]
            x2, y2 = project(stitch)
            for parent in stitch.parents:
                if parent < 0 or parent >= len(targets):
                    continue
                x1, y1 = project(targets[parent])
                parts.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="#d5dde6" stroke-width="0.6"/>'
                )
        del lookup
    for stitch in simulation.stitches:
        px, py = project(stitch)
        color = stitch.color_hex or _color(stitch.stitch_type)
        parts.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.2" fill="{color}"/>'
        )
    return "\n".join(parts)


def stitch_table_csv(simulation: StitchSimulation) -> str:
    """One row per written stitch. An empty color was not invented."""
    lines = [
        "# Coordinates are a model, not a measurement. An empty color was not invented.",
        "piece,copy,round,index,stitch_type,color,parents,x,y,z",
    ]
    for stitch in simulation.stitches:
        parents = ";".join(str(parent) for parent in stitch.parents)
        lines.append(
            ",".join(
                [
                    _csv(stitch.piece),
                    str(stitch.copy_index),
                    str(stitch.round_number),
                    str(stitch.index),
                    _csv(stitch.stitch_type),
                    _csv(stitch.color_label),
                    _csv(parents),
                    f"{stitch.x:.4f}",
                    f"{stitch.y:.4f}",
                    f"{stitch.z:.4f}",
                ]
            )
        )
    return "\n".join(lines) + "\n"


def _csv(value: str) -> str:
    if any(mark in value for mark in ",\"\n"):
        return '"' + value.replace('"', '""') + '"'
    return value


_SWATCHES = {
    "brown": "#8B5A2B",
    "indigo": "#3F51B5",
    "gold": "#C9A227",
    "white": "#F4F1EA",
    "black": "#222222",
    "red": "#C0392B",
    "blue": "#2471A3",
    "green": "#1E8449",
    "pink": "#D4738E",
    "yellow": "#F4D03F",
    "orange": "#E67E22",
    "purple": "#7D3C98",
    "grey": "#7F8C8D",
    "gray": "#7F8C8D",
    "cream": "#F6E7C1",
    "navy": "#1A365D",
    "teal": "#148F77",
}
_LABEL_HEX = {
    "A": "#3d7ea6",
    "B": "#c9a227",
    "C": "#1e8449",
    "D": "#c0392b",
    "E": "#7d3c98",
}


def _color_for_unit(unit, pattern_text: str) -> tuple[str, str, str]:
    line = getattr(unit, "source_text", "") or ""
    letters = re.findall(r"\bColor\s+([A-Z])\b", line)
    letters = list(dict.fromkeys(letters))
    if len(letters) > 1:
        return "", "", "split"
    if not letters:
        return "", "", "missing"
    letter = letters[0]
    names = re.findall(
        rf"\bColor\s+{letter}\s*:\s*([A-Za-z]+)",
        pattern_text,
    )
    if names and names[0].lower() in _SWATCHES:
        return f"{letter} {names[0]}", _SWATCHES[names[0].lower()], "swatch"
    if names:
        return letter, _LABEL_HEX.get(letter, "#5c6b7a"), "unknown"
    return letter, _LABEL_HEX.get(letter, "#5c6b7a"), "labeled"


def _color(kind: str) -> str:
    return {
        "single_crochet": "#3d7ea6",
        "half_double_crochet": "#3f8f6b",
        "double_crochet": "#6d5bd0",
        "treble_crochet": "#d17a32",
        "increase": "#2e9e62",
        "decrease": "#c4524a",
        "chain": "#8b97a3",
        "slip_stitch": "#5c6b7a",
    }.get(kind, "#243042")


def _xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
