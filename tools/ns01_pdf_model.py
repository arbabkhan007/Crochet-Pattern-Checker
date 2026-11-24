"""Compile PDF-only structured facts from the canonical NS01 Markdown master.

The Markdown file remains the single authoring source. This module deliberately
extracts only facts needed by the PDF layout and placement figure; it does not
copy the pattern instructions into a second editable JSON document.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "patterns/01_Hamish_the_Highland_Cow.md"
SCHEMA = ROOT / "schemas/ns01_pdf_render_model.schema.json"
SOURCE_LABEL = "patterns/01_Hamish_the_Highland_Cow.md"
# Optional external cache keeps reviewed image inputs out of the checkout.
RELEASE_INPUT_CACHE = os.environ.get("CROCHET_RELEASE_INPUT_CACHE")
ASSET_ROOT = (
    Path(RELEASE_INPUT_CACHE).expanduser().resolve()
    if RELEASE_INPUT_CACHE
    else ROOT
)
HERO_ASSET = ASSET_ROOT / "assets/patterns/ns01/hamish_cover_concept.png"
MATERIALS_ASSET = ASSET_ROOT / "assets/patterns/ns01/hamish_materials_concept.png"
COVER_IMAGE_BOX_MM = (107.0, 195.0)
MATERIALS_IMAGE_BOX_MM = (160.0, 68.0)
MIN_PRINT_DPI = 300.0
INSERT_FIT_UPPER_RATIO = 1.15


def insert_exceeds_crochet_threshold(
    insert_diameter_mm: float, crochet_diameter_mm: float
) -> bool:
    """Flag only inserts larger than 1.15 times a measured crochet diameter.

    Both measurements must use the same unit. This one-sided numerical check is
    not a physical fit test; it intentionally has no lower threshold or fit band.
    """

    diameters = (insert_diameter_mm, crochet_diameter_mm)
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
        for value in diameters
    ):
        raise ValueError("Insert and crochet diameters must be positive finite numbers")
    return insert_diameter_mm > INSERT_FIT_UPPER_RATIO * crochet_diameter_mm


def _match(
    pattern: str, text: str, label: str, flags: int = re.IGNORECASE
) -> re.Match[str]:
    match = re.search(pattern, text, flags)
    if match is None:
        raise ValueError(
            f"Could not derive {label} from the canonical NS01 Markdown master"
        )
    return match


def _section(text: str, heading_pattern: str) -> str:
    """Return a Markdown heading section up to the next heading of equal level."""

    match = re.search(
        rf"^#{{2,}}\s+{heading_pattern}[^\n]*\n", text, re.MULTILINE | re.IGNORECASE
    )
    if match is None:
        raise ValueError(
            f"Could not find canonical NS01 section matching {heading_pattern!r}"
        )
    level = len(re.match(r"^#+", match.group(0)).group(0))  # type: ignore[union-attr]
    rest = text[match.end() :]
    next_heading = re.search(rf"^#{{1,{level}}}\s+", rest, re.MULTILINE)
    return rest[: next_heading.start()] if next_heading else rest


def _round_rows(section: str, label: str) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() in {"rnd", "round", "row"}:
            continue
        round_match = re.fullmatch(
            r"R\s*(\d+)(?:\s*[–-]\s*R?\s*(\d+))?", cells[0], re.IGNORECASE
        )
        stitch_match = re.fullmatch(r"\(?\s*(\d+)\s*\)?", cells[2])
        if round_match is None or stitch_match is None:
            continue
        start = int(round_match.group(1))
        end = int(round_match.group(2) or start)
        if end < start:
            raise ValueError(
                f"Invalid round range in canonical {label} table: {cells[0]!r}"
            )
        rows.append(
            {"start": start, "end": end, "stitches": int(stitch_match.group(1))}
        )

    if not rows:
        raise ValueError(f"No numbered round rows found in canonical {label} table")
    rows.sort(key=lambda row: (row["start"], row["end"]))
    expected_next = 1
    for row in rows:
        if row["start"] != expected_next:
            raise ValueError(
                f"Non-contiguous {label} rounds in canonical master: expected R{expected_next}, "
                f"found R{row['start']}"
            )
        expected_next = row["end"] + 1
    return rows


def _stitches_at(
    round_rows: list[dict[str, int]], round_number: int, label: str
) -> int:
    for row in round_rows:
        if row["start"] <= round_number <= row["end"]:
            return row["stitches"]
    raise ValueError(
        f"{label} R{round_number} is not represented in its canonical round table"
    )


def _pair(match: re.Match[str], start_index: int = 1) -> dict[str, int]:
    return {
        "round_start": int(match.group(start_index)),
        "round_end": int(match.group(start_index + 1)),
    }


def _round_table_total(component_name: str, component: dict[str, Any]) -> int:
    """Require a sorted, contiguous one-based round table and return its end."""

    expected_next = 1
    for row in component["rounds"]:
        if row["end"] < row["start"] or row["start"] != expected_next:
            raise ValueError(
                f"Non-contiguous {component_name} round table at R{expected_next}"
            )
        expected_next = row["end"] + 1
    return expected_next - 1


def _validate_model(model: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(model),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        detail = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(
            f"Compiled NS01 PDF model failed JSON Schema validation: {detail}"
        )

    pattern = model["pattern"]
    if pattern["time_hours"]["maximum"] < pattern["time_hours"]["minimum"]:
        raise ValueError("Estimated maximum time is below the minimum time")
    yarn_ids = [yarn["id"] for yarn in pattern["yarns"]]
    if sorted(yarn_ids) != ["A", "B", "C", "D"]:
        raise ValueError("NS01 render model must contain one each of yarns A through D")

    head = model["components"]["head"]
    body = model["components"]["body"]
    head_total = _round_table_total("head", head)
    body_total = _round_table_total("body", body)
    for component_name, component, total in (
        ("head", head, head_total),
        ("body", body, body_total),
    ):
        for feature_name, feature in component["features"].items():
            round_fields = (
                "round_start",
                "round_end",
                "lower_edge_round_start",
                "lower_edge_round_end",
            )
            for field in round_fields:
                if field in feature and feature[field] > total:
                    raise ValueError(
                        f"{component_name} {feature_name} references a round beyond its table"
                    )
            if (
                "round_start" in feature
                and "round_end" in feature
                and feature["round_start"] > feature["round_end"]
            ):
                raise ValueError(
                    f"{component_name} {feature_name} has a reversed round range"
                )
            if (
                "lower_edge_round_start" in feature
                and feature["lower_edge_round_start"] > feature["lower_edge_round_end"]
            ):
                raise ValueError(
                    f"{component_name} {feature_name} has a reversed lower-edge range"
                )
    fringe_rounds = head["features"]["fringe"]["rounds"]
    if any(round_number > head_total for round_number in fringe_rounds):
        raise ValueError("Head fringe references a round beyond the head table")
    if len(set(fringe_rounds)) != len(fringe_rounds):
        raise ValueError("Head fringe references a round more than once")

    closure = head["closure"]
    if closure["round"] != head_total or closure["stitches"] != _stitches_at(
        head["rounds"], closure["round"], "head"
    ):
        raise ValueError("Head closure disagrees with the final head round table row")
    body_ending = body["ending"]
    if body_ending["round"] != body_total or body_ending["stitches"] != _stitches_at(
        body["rounds"], body_ending["round"], "body"
    ):
        raise ValueError("Open body neck disagrees with the final body round table row")

    join = head["neck_join"]
    if join["stitches"] != _stitches_at(head["rounds"], join["round"], "head"):
        raise ValueError("Head join count disagrees with its round table row")
    if join["stitches"] != body_ending["stitches"]:
        raise ValueError("Head join count and open body neck count do not match")


def validate_ns01_pdf_model(model: dict[str, Any]) -> None:
    """Validate a compiled model against the JSON Schema and cross-field rules."""

    _validate_model(model)


def compile_ns01_pdf_model(source_path: Path = SOURCE) -> dict[str, Any]:
    """Compile and validate the layout model from the current NS01 master."""

    source_path = Path(source_path)
    raw = source_path.read_bytes()
    text = raw.decode("utf-8")
    try:
        source_label = source_path.resolve().relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise ValueError("NS01 PDF model source must be inside the repository") from exc
    if source_label != SOURCE_LABEL:
        raise ValueError(f"Unexpected NS01 canonical source path: {source_label}")

    title_match = _match(
        r"^#\s+(.+?)\s+the\s+(.+)$", text, "pattern title", re.MULTILINE
    )
    code_match = _match(r"Design Code\s+(NS\s*0?1)\b", text, "design code")
    level_match = _match(
        r"^>\s*\*\*US terms\s*·\s*([^·]+?)\s*·\s*(\d+)\s*-\s*(\d+)\s*hours",
        text,
        "skill level and estimated time",
        re.MULTILINE,
    )
    size_match = _match(
        r"\*\*FINISHED SIZE\*\*\s+About\s+(\d+(?:\.\d+)?)\s*cm", text, "finished size"
    )
    hook_match = _match(
        r"Hook:\s*(\d+(?:\.\d+)?)\s*mm\s*\(US\s+([^)]+)\)", text, "hook size"
    )
    yarn_weight_match = _match(
        r"^-\s*Yarn\s+A\s+-\s*[^:]+:\s*([^,\n]+)",
        text,
        "primary yarn weight",
        re.MULTILINE | re.IGNORECASE,
    )
    gauge_match = _match(
        r"Gauge:\s*(\d+)\s+sc\s*x\s*(\d+)\s+rounds\s*=\s*(\d+(?:\.\d+)?)\s*cm",
        text,
        "gauge",
    )

    yarns: list[dict[str, Any]] = []
    for line in text.splitlines():
        yarn_match = re.match(
            r"\s*-\s*Yarn\s+([A-D])\s+-\s*([^:]+):.*?about\s+(\d+(?:\.\d+)?)\s*g\b",
            line,
            re.IGNORECASE,
        )
        if yarn_match:
            yarns.append(
                {
                    "id": yarn_match.group(1).upper(),
                    "name": yarn_match.group(2).strip(),
                    "grams": float(yarn_match.group(3)),
                }
            )
    yarns.sort(key=lambda item: item["id"])
    if [item["id"] for item in yarns] != ["A", "B", "C", "D"]:
        raise ValueError(
            "Canonical NS01 source must specify Yarn A through Yarn D quantities"
        )

    head_section = _section(text, r"1\.\s+Head\b")
    body_section = _section(text, r"3\.\s+Body\b")
    head_rounds = _round_rows(head_section, "head")
    body_rounds = _round_rows(body_section, "body")

    eyes_match = _match(
        r"(?:Place|Insert|the)\s+(?:the\s+)?(\d+(?:\.\d+)?)\s*mm eyes (?:go in )?between Rnds\s+(\d+)\s+and\s+(\d+),\s*(\d+)\s+stitches apart",
        text,
        "eye placement",
    )
    muzzle_match = _match(
        r"Pin the top edge.*?at Rnd\s+(\d+)\s+and let the lower edge fall at Rnd\s+(\d+)\s*[-–]\s*(\d+)",
        text,
        "muzzle placement",
    )
    horns_match = _match(
        r"2\.\s*Horns between Rnds\s+(\d+)\s+and\s+(\d+),\s*(\d+)\s+stitches apart",
        text,
        "horn placement",
    )
    ears_match = _match(
        r"3\.\s*Ears[^\n]*?centred on Rnds\s+(\d+)\s*[-–]\s*(\d+)",
        text,
        "ear placement",
    )
    fringe_section = _section(text, r"9\.\s+Fringe\b")
    fringe_match = _match(
        r"three rows across the front of the head:.*?Rnd\s+(\d+).*?Rnd\s+(\d+).*?Rnd\s+(\d+)",
        fringe_section,
        "fringe row placement",
    )
    front_legs_match = _match(
        r"7\.\s*Front legs:\s*FRONT across Rnds\s+(\d+)\s*[-–]\s*(\d+),\s*about\s+(\d+)\s+sts apart",
        text,
        "front-leg placement",
    )
    back_legs_match = _match(
        r"6\.\s*Back legs:\s*lower sides across Rnds\s+(\d+)\s*[-–]\s*(\d+)",
        text,
        "back-leg placement",
    )
    belly_section = _section(text, r"4\.\s+Belly patch\b")
    belly_match = _match(
        r"lower edge about\s+(\d+)\s+rounds up from the base",
        belly_section,
        "belly-patch placement",
    )
    tail_section = _section(text, r"8\.\s+Tail\b")
    tail_match = _match(
        r"at the (centre-back[^.]+last increase round)", tail_section, "tail anchor"
    )
    join_match = _match(
        r"Match the\s+(\d+)\s+body Rnd-(\d+) stitches one-for-one to the\s+(\d+)\s+head stitches of Rnd\s+(\d+)",
        text,
        "head/body seam counts",
    )

    body_join_count, body_join_round, head_join_count, head_join_round = map(
        int, join_match.groups()
    )
    if body_join_count != _stitches_at(body_rounds, body_join_round, "body"):
        raise ValueError(
            "The written body/head seam count disagrees with the body round table"
        )
    if head_join_count != _stitches_at(head_rounds, head_join_round, "head"):
        raise ValueError(
            "The written body/head seam count disagrees with the head round table"
        )
    head_last_round = max(row["end"] for row in head_rounds)
    body_last_round = max(row["end"] for row in body_rounds)
    head_last_stitches = _stitches_at(head_rounds, head_last_round, "head")
    body_last_stitches = _stitches_at(body_rounds, body_last_round, "body")
    if not re.search(r"close the hole", head_section, re.IGNORECASE):
        raise ValueError("The canonical head table no longer declares a closed ending")
    if not re.search(r"leave neck\s+OPEN", body_section, re.IGNORECASE):
        raise ValueError("The canonical body table no longer declares its open neck")

    model: dict[str, Any] = {
        "schema_version": 1,
        "source": {"path": source_label, "sha256": hashlib.sha256(raw).hexdigest()},
        "pattern": {
            "design_code": re.sub(r"\s+", " ", code_match.group(1)).upper(),
            "title": title_match.group(1).strip(),
            "subtitle": f"the {title_match.group(2).strip()}",
            "skill_level": level_match.group(1).strip(),
            "terminology": "US",
            "time_hours": {
                "minimum": int(level_match.group(2)),
                "maximum": int(level_match.group(3)),
            },
            "finished_size_cm": float(size_match.group(1)),
            "finished_size_approximate": True,
            "hook_mm": float(hook_match.group(1)),
            "hook_us": hook_match.group(2).strip(),
            "yarn_weight": yarn_weight_match.group(1).strip(),
            "gauge": {
                "stitches": int(gauge_match.group(1)),
                "stitch_type": "sc",
                "rounds": int(gauge_match.group(2)),
                "measure_cm": float(gauge_match.group(3)),
            },
            "yarns": yarns,
        },
        "components": {
            "head": {
                "direction": "TOP_DOWN",
                "rounds": head_rounds,
                "closure": {
                    "round": head_last_round,
                    "stitches": head_last_stitches,
                    "closed": True,
                },
                "neck_join": {"round": head_join_round, "stitches": head_join_count},
                "features": {
                    "eyes": {
                        "diameter_mm": float(eyes_match.group(1)),
                        "round_start": int(eyes_match.group(2)),
                        "round_end": int(eyes_match.group(3)),
                        "spacing_stitches": int(eyes_match.group(4)),
                    },
                    "muzzle": {
                        "round_start": int(muzzle_match.group(1)),
                        "lower_edge_round_start": int(muzzle_match.group(2)),
                        "lower_edge_round_end": int(muzzle_match.group(3)),
                    },
                    "horns": {
                        "round_start": int(horns_match.group(1)),
                        "round_end": int(horns_match.group(2)),
                        "spacing_stitches": int(horns_match.group(3)),
                    },
                    "ears": _pair(ears_match),
                    "fringe": {
                        "rounds": [int(value) for value in fringe_match.groups()]
                    },
                },
            },
            "body": {
                "direction": "BOTTOM_UP",
                "rounds": body_rounds,
                "ending": {
                    "round": body_last_round,
                    "stitches": body_last_stitches,
                    "open": True,
                },
                "features": {
                    "front_legs": {
                        "round_start": int(front_legs_match.group(1)),
                        "round_end": int(front_legs_match.group(2)),
                        "gap_stitches": int(front_legs_match.group(3)),
                    },
                    "back_legs": _pair(back_legs_match),
                    "belly_patch": {
                        "optional": True,
                        "lower_edge_offset_from_base_rounds": int(belly_match.group(1)),
                    },
                    "tail": {
                        "anchor_note": re.sub(r"\s+", " ", tail_match.group(1)).strip()
                    },
                },
            },
        },
    }
    validate_ns01_pdf_model(model)
    return model


def main() -> int:
    model = compile_ns01_pdf_model()
    print(json.dumps(model, indent=2, ensure_ascii=False))
    print(f"\nNS01 render model: PASS ({model['source']['sha256']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
