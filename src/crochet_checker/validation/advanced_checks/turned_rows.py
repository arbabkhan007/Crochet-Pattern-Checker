"""Turn, face parity, height-profile reversal, and WS-only stitch checks."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .common import AdvancedFinding, ROUND_HEADER, ROW_HEADER, split_sections

_HEIGHT = {"sl st": 0, "sc": 1, "hdc": 2, "dc": 3, "tr": 4, "dtr": 5}
_REQUIRED_TURN_CHAIN = {"sc": 1, "hdc": 2, "dc": 3, "tr": 4, "dtr": 5}
_ROW = re.compile(
    r"^\s*row\.?\s*(\d+)\b\s*(?:\((RS|WS)\)|[, ]+\b(RS|WS)\b)?\s*[:.)-]?\s*(.*)$",
    re.IGNORECASE,
)
_STITCH = re.compile(
    r"(?:(?P<before>\d+)\s*(?:[x×]\s*)?)?"
    r"(?P<stitch>dtr|tr|dc|hdc|sc|sl\s*st)\b"
    r"(?:\s*[x×]?\s*(?P<after>\d+))?",
    re.IGNORECASE,
)
_FACE = re.compile(r"\b(RS|WS|right\s+side|wrong\s+side)\b", re.IGNORECASE)


@dataclass(frozen=True)
class RowProfile:
    number: int
    source: str
    body: str
    explicit_face: str | None
    heights: tuple[int, ...]
    stitch_types: tuple[str, ...]
    turn_at_start: bool
    turn_at_end: bool
    turning_chain: int | None
    line_number: int


@dataclass(frozen=True)
class RowOrientation:
    number: int
    face: str | None
    reverse_stitch_array: bool
    traversal_reversed: bool


def _is_positive_turn(body: str, match: re.Match[str]) -> bool:
    before = body[max(0, match.start() - 20) : match.start()]
    return not re.search(r"(?:do\s+not|don't|should\s+not)\s*$", before, re.IGNORECASE)


def _profile(line: str, line_number: int) -> RowProfile | None:
    match = _ROW.match(line.strip())
    if not match:
        return None
    number = int(match.group(1))
    explicit = (match.group(2) or match.group(3) or "").upper() or None
    body = match.group(4)
    if explicit is None:
        side = _FACE.search(body)
        if side:
            token = side.group(1).upper()
            explicit = "RS" if token == "RS" or token.startswith("RIGHT") else "WS"

    tokens = list(_STITCH.finditer(body))
    heights: list[int] = []
    stitch_types: list[str] = []
    token_counts = [
        int(token.group("before") or token.group("after") or 1) for token in tokens
    ]
    if sum(token_counts) <= 10_000:
        for token, count in zip(tokens, token_counts, strict=True):
            name = re.sub(r"\s+", " ", token.group("stitch").lower())
            heights.extend([_HEIGHT[name]] * count)
            stitch_types.extend([name] * count)

    turns = [
        m
        for m in re.finditer(r"\bturn\b", body, re.IGNORECASE)
        if _is_positive_turn(body, m)
    ]
    first_start = tokens[0].start() if tokens else len(body)
    last_end = tokens[-1].end() if tokens else 0
    turn_at_start = any(item.start() < first_start for item in turns)
    turn_at_end = any(item.start() > last_end for item in turns)

    chain = None
    for chain_match in re.finditer(r"\b(?:ch|chain)\s+(\d+)\b", body, re.IGNORECASE):
        following_turn = re.search(
            r"\bturn\b", body[chain_match.end() : chain_match.end() + 20], re.IGNORECASE
        )
        preceding_turn = re.search(
            r"\bturn\b",
            body[max(0, chain_match.start() - 20) : chain_match.start()],
            re.IGNORECASE,
        )
        if following_turn or preceding_turn:
            chain = int(chain_match.group(1))
            break

    return RowProfile(
        number,
        line.strip(),
        body,
        explicit,
        tuple(heights),
        tuple(stitch_types),
        turn_at_start,
        turn_at_end,
        chain,
        line_number,
    )


def annotate_row_turns(rows: list[RowProfile]) -> list[RowOrientation]:
    """Infer only turn parity; an unknown starting face stays unknown."""
    result: list[RowOrientation] = []
    face: str | None = None
    traversal_reversed = False
    previous_number: int | None = None
    pending_turn = False
    for row in rows:
        if previous_number is not None and row.number != previous_number + 1:
            face = None
            traversal_reversed = False
            pending_turn = False
        turn_before = pending_turn or row.turn_at_start
        if turn_before:
            traversal_reversed = not traversal_reversed
            # A trailing turn was already applied to the face after the prior
            # row. A leading turn is applied here only when no pending turn did it.
            if row.turn_at_start and not pending_turn and face is not None:
                face = "WS" if face == "RS" else "RS"
        if row.explicit_face is not None:
            face = row.explicit_face
        result.append(
            RowOrientation(
                row.number,
                face,
                reverse_stitch_array=turn_before,
                traversal_reversed=traversal_reversed,
            )
        )
        if face is not None and row.turn_at_end:
            face = "WS" if face == "RS" else "RS"
        pending_turn = row.turn_at_end
        previous_number = row.number
    return result


def _slope(values: tuple[int, ...]) -> int:
    if len(values) < 2:
        return 0
    return (values[-1] > values[0]) - (values[-1] < values[0])


def _row_groups(text: str) -> list[tuple[list[RowProfile], str, int, str]]:
    result = []
    for heading, body, start_line in split_sections(text):
        rows = []
        body_start = start_line + (1 if heading else 0)
        for number, line in enumerate(body.splitlines(), start=body_start):
            parsed = _profile(line, number)
            if parsed:
                rows.append(parsed)
        if rows:
            result.append((rows, body, start_line, heading))
    return result


def turned_row_findings(text: str) -> list[AdvancedFinding]:
    findings: list[AdvancedFinding] = []
    glossary_dec_flo = bool(
        re.search(
            r"\bdec\s*[-:]\s*[^\n]*(?:front[- ]loops?|\bFLO\b)[^\n]*(?:invisible\s+)?decrease",
            text,
            re.IGNORECASE,
        )
    )
    glossary_bobble_push = bool(
        re.search(
            r"\b(?:bo|bobble)\s*[-:]\s*[^\n]*(?:push|pushed)\s+(?:the\s+)?bobble\s+toward\s+you",
            text,
            re.IGNORECASE,
        )
    )

    for rows, body, _start_line, heading in _row_groups(text):
        orientation = annotate_row_turns(rows)
        for index, row in enumerate(rows):
            if index and row.number == rows[index - 1].number + 1:
                previous = rows[index - 1]
                prev_state = orientation[index - 1]
                state = orientation[index]
                if (
                    row.explicit_face
                    and prev_state.face
                    and (previous.turn_at_end or row.turn_at_start)
                ):
                    expected = (
                        ("WS" if prev_state.face == "RS" else "RS")
                        if state.reverse_stitch_array
                        else prev_state.face
                    )
                    if row.explicit_face != expected:
                        findings.append(
                            AdvancedFinding(
                                "RowFaceParityConflict",
                                f"Row {row.number} is marked {row.explicit_face}, but the written turn sequence predicts {expected}.",
                                "error",
                                row.line_number,
                            )
                        )

                if previous.turn_at_end or row.turn_at_start:
                    under = tuple(reversed(previous.heights))
                    if (
                        len(under) == len(row.heights)
                        and _slope(under) < 0
                        and _slope(row.heights) > 0
                        and len(under) >= 3
                    ):
                        findings.append(
                            AdvancedFinding(
                                "TurnedRowTaperInversion",
                                f"Row {row.number} reverses a rising stitch-height profile; its written profile also rises, so short stitches would stack over taller stitches. Review the taper direction.",
                                "warning",
                                row.line_number,
                            )
                        )

                if (
                    previous.turn_at_end
                    and previous.turning_chain is not None
                    and row.stitch_types
                ):
                    required = _REQUIRED_TURN_CHAIN.get(row.stitch_types[0])
                    if required is not None and previous.turning_chain < required:
                        findings.append(
                            AdvancedFinding(
                                "TurningChainHeightMismatch",
                                f"Row {previous.number} turns with ch {previous.turning_chain}, but Row {row.number} begins with {row.stitch_types[0]} (commonly ch {required} is used for that height).",
                                "warning",
                                previous.line_number,
                            )
                        )

            state = orientation[index]
            if (
                state.face == "WS"
                and glossary_dec_flo
                and re.search(r"\bdec\b", row.body, re.IGNORECASE)
            ):
                findings.append(
                    AdvancedFinding(
                        "WrongSideInvisibleDecrease",
                        f"Row {row.number} is WS and uses a glossary-defined front-loop invisible decrease; consider a both-loop decrease or verify the intended visible side.",
                        "warning",
                        row.line_number,
                    )
                )
            if (
                state.face == "WS"
                and glossary_bobble_push
                and re.search(r"\b(?:bo|bobble)\b", row.body, re.IGNORECASE)
            ):
                findings.append(
                    AdvancedFinding(
                        "WrongSideBobbleExtrusion",
                        f"Row {row.number} is WS and uses a bobble definition that pushes the bobble toward the worker; verify which fabric face should show it.",
                        "warning",
                        row.line_number,
                    )
                )

        if re.search(r"\bshort[- ]rows?\b", f"{heading}\n{body}", re.IGNORECASE):
            last = rows[-1]
            last_face = orientation[-1].face
            face_after = (
                ("WS" if last_face == "RS" else "RS") if last.turn_at_end else last_face
            )
            body_lines = body.splitlines()
            row_positions = [
                index
                for index, line in enumerate(body_lines)
                if _ROW.match(line.strip())
            ]
            last_row_position = (
                row_positions[-1] if row_positions else len(body_lines) - 1
            )
            resume_index = next(
                (
                    index
                    for index, line in enumerate(
                        body_lines[last_row_position + 1 :], start=last_row_position + 1
                    )
                    if ROUND_HEADER.match(line.strip())
                ),
                None,
            )
            reorientation = False
            if resume_index is not None:
                between = "\n".join(body_lines[last_row_position + 1 : resume_index])
                reorientation = bool(
                    re.search(
                        r"\b(?:reorient\w*|flip(?:ped|ping)?|turn\s+(?:the\s+)?work|turn\s+to\s+(?:RS|right\s+side)|right[- ]side[- ]out)\b",
                        between,
                        re.IGNORECASE,
                    )
                )
            if face_after == "WS" and resume_index is not None and not reorientation:
                findings.append(
                    AdvancedFinding(
                        "InsideOutTopologyInversion",
                        "Short rows leave the WS facing before continuous rounds resume. State an explicit reorientation or turn before continuing in the round.",
                        "warning",
                        last.line_number,
                    )
                )
    return findings
