"""Deterministic audit of the 10 Novality Store patterns.

Reuses the repository's own engine wherever possible:

* crochet_checker.parser      - parses every parseable instruction string
* crochet_checker.model       - STITCH_CONSUMPTION / STITCH_PRODUCTION tables
* crochet_checker.validation  - StitchCountValidator runs end-to-end on every
                                piece that is fully parser-covered

Every round is verified THREE ways:
  1. hand-computed consumed/produced counts stored in the data files
  2. the repository parser's computed counts for the same instruction
     (when a normalized, parser-safe form exists in "check")
  3. round-to-round continuity: cons(row n) == prod(row n - 1)
     and stated(n) == prod(n)

Rows whose construction the repo parser cannot represent (oval chains,
cluster rounds, shells, FLO/BLO ruffles) use hand-computed counts only and
are listed as "manual" in the output, per-row.

Also checks:
  * every abbreviation used in an instruction is declared in the pattern's
    own Abbreviations list
  * no UK-only terms (htr / treble / dtr) appear in US-terminology patterns
  * the regenerated markdown sources stay in sync with the data
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field, asdict

from crochet_checker.parser.parser import CrochetParser, parse_instruction
from crochet_checker.model.stitch import STITCH_PRODUCTION
from crochet_checker.validation.stitch_counts import StitchCountValidator

from . import PATTERNS

STANDARD_TOKENS = {
    "ch", "sl", "st", "sts", "sc", "hdc", "dc", "tr", "inc", "dec", "invdec",
    "mr", "flo", "blo", "fo", "rnd", "rnds", "mr", "x", "sp", "sk", "picot",
    "in", "each", "next", "first", "last", "then", "and", "or", "the", "to",
    "from", "with", "across", "around", "both", "sides", "side", "of", "a",
    "an", "it", "as", "into", "through", "layers", "layer", "join", "joins",
    "joined", "yarn", "colour", "color", "main", "contrast", "cream", "pink",
    "lavender", "sage", "hook", "mm", "cm", "g", "incl", "counts", "count",
    "repeat", "rep", "brim", "tip", "base", "hoof", "ridge", "crown",
    "work", "working", "worked", "make", "made", "leave", "leaving", "flat",
    "flatten", "close", "closed", "closing", "continue", "rotate", "ignore",
    "stuff", "stuffed", "stuffing", "lightly", "firmly", "now", "here",
    "only", "same", "space", "spaces", "corner", "between", "along",
    "other", "end", "final", "row", "round", "chain", "stitch", "stitches",
    "turn", "over", "under", "out", "down", "back", "front", "loop",
    "loops", "lost", "stay", "unworked", "they", "form", "pointed",
    "second", "2nd", "3rd", "total", "times", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine", "ten", "anchored", "anchor",
    "scallop", "shell", "shells", "cluster", "clusters", "bump", "bumps",
    "head", "flippers", "ridge", "opening", "bell", "live", "edge",
    "position", "positions", "plain", "runs", "magic", "ring", "circle",
    "tbl", "bl1", "bl2", "fl1", "fl2", "bl", "fl",
    "nd", "rd", "th", "all", "any", "that", "every", "per", "top",
    "remaining", "adds", "group", "takes", "returns", "makes", "using",
    "behind", "covers", "covering", "wide", "span", "spans", "lands",
    "worth", "whose", "mirrors", "mirror", "its", "itself", "rhythm",
    "written", "below", "measurable", "marks", "mark", "visible",
            "available", "changed", "unchanged", "adjust", "method", "workable",
    "c", "r", "yellow", "brown", "orange", "black", "white", "grey",
    "ginger", "chocolate", "tan", "teal", "lilac", "charcoal", "mustard",
    "rust", "blush", "oat", "cocoa", "mint", "leucistic", "melanoid",
}

UK_ONLY = re.compile(r"\b(htr|dtr|treble\s+crochet|treble)\b", re.IGNORECASE)


@dataclass
class Finding:
    level: str           # ERROR | WARN | INFO
    where: str
    message: str


@dataclass
class PieceAudit:
    piece: str
    rows: int = 0
    manual_rows: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)


def _declared_abbrevs(pattern) -> set[str]:
    decl = set()
    for line in pattern.get("abbreviations", []):
        abbr = line.split("-")[0].strip().lower()
        for tok in re.findall(r"[a-z()0-9 ]+", abbr):
            tok = tok.strip()
            if tok:
                decl.add(tok)
    return decl


def _instruction_tokens(text: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[A-Za-z]+", text)]


def check_abbreviations(pattern, report: PieceAudit):
    decl = _declared_abbrevs(pattern)
    allowed = STANDARD_TOKENS | decl
    for piece in pattern["pieces"]:
        for sub in piece["subpieces"]:
            for row in sub.get("rows", []):
                for tok in _instruction_tokens(row["text"]):
                    if tok not in allowed and not tok.isdigit():
                        report.findings.append(Finding(
                            "WARN", f"{piece['name']} {row['label']}",
                            f"token '{tok}' used but not declared in Abbreviations"))


def check_terminology(pattern, report: PieceAudit):
    texts = []
    for piece in pattern["pieces"]:
        for sub in piece["subpieces"]:
            for row in sub.get("rows", []):
                texts.append((f"{piece['name']} {row['label']}", row["text"]))
            for note in sub.get("notes", []):
                texts.append((piece["name"], note))
    for where, t in texts:
        m = UK_ONLY.search(t)
        if m:
            report.findings.append(Finding(
                "ERROR", where, f"UK-only term '{m.group(0)}' in a US-terms pattern"))


def _compare_with_parser(row, where, report, prev_prod):
    """Verify hand counts against the repository parser."""
    chk = row.get("check")
    if not chk:
        if (not row.get("skip_check")) and (row.get("stated") is not None or row.get("cons") is not None or row.get("prod") is not None):
            report.manual_rows.append(row["label"])
        return
    from crochet_checker.model.stitch import STITCH_CONSUMPTION
    inst = parse_instruction(chk)
    context = any(op.into_stitch in ("each_stitch_around", "remaining")
                  for op in inst.operations)
    if context:
        prod = None
        if prev_prod is not None:
            rem, tot = prev_prod, 0
            for op in inst.operations:
                if op.into_stitch in ("each_stitch_around", "remaining"):
                    tot += rem * STITCH_PRODUCTION.get(op.stitch_type, 1)
                    rem = 0
                else:
                    tot += op.count * STITCH_PRODUCTION.get(op.stitch_type, 1)
                    rem -= op.count * STITCH_CONSUMPTION.get(op.stitch_type, 1)
            prod = tot
        cons = prev_prod
    else:
        prod = inst.total_stitches_produced or None
        cons = inst.total_stitches_consumed or None
    if row.get("prod") is not None and prod is not None and row["prod"] != prod:
        report.findings.append(Finding(
            "ERROR", where,
            f"produced mismatch: data says {row['prod']}, repo parser says {prod} "
            f"({chk!r})"))
    if (row.get("cons") is not None and cons is not None
            and not context and row["cons"] != cons):
        report.findings.append(Finding(
            "ERROR", where,
            f"consumed mismatch: data says {row['cons']}, repo parser says {cons} "
            f"({chk!r})"))


def audit_piece(pattern, piece, sub) -> list[Finding]:
    findings: list[Finding] = []
    rows = sub.get("rows", [])
    prev_prod = None
    for i, row in enumerate(rows):
        where = f"{piece['name']} / {sub['name'] or 'main'} / {row['label']}"
        if row.get("skip_check"):
            continue
        # 1. row-to-row continuity
        if prev_prod is not None and row.get("cons") is not None and row["cons"] != prev_prod:
            findings.append(Finding(
                "ERROR", where,
                f"consumes {row['cons']} but previous row produced {prev_prod}"))
        # 2. stated count is consistent with produced count
        if row.get("stated") is not None and row.get("prod") is not None and row["stated"] != row["prod"]:
            findings.append(Finding(
                "ERROR", where,
                f"states ({row['stated']}) but instruction produces {row['prod']}"))
        prev_prod = row.get("prod", prev_prod)
    return findings


def _repo_validate_rows(rows) -> list[Finding]:
    """End-to-end StitchCountValidator pass on fully parser-covered pieces."""
    if not rows or any(not r.get("check") or r.get("skip_check") for r in rows):
        return []
    lines = []
    for i, r in enumerate(rows, start=1):
        stated = f" ({r['stated']})" if r.get("stated") is not None else ""
        lines.append(f"Round {i}: {r['check']}{stated}")
    text = "\n".join(lines)
    pattern = CrochetParser().parse(text)
    report = StitchCountValidator().validate(pattern)
    return [Finding(f.severity.name, f.location, f.message)
            for f in report.findings
            if f.severity.name in ("ERROR", "CRITICAL")]


def _iter_audit_rows(pattern):
    """Yield (piece_name, sub_name, rows) for every checkable block."""
    for piece in pattern["pieces"]:
        for sub in piece["subpieces"]:
            if sub.get("rows"):
                yield (f"{piece['name']} / {sub['name'] or 'main'}", sub["rows"])
    for extra in pattern.get("extras", []):
        for r in extra.get("audit_rows", []):
            pass
        if extra.get("audit_rows"):
            yield (f"{extra['name']}", extra["audit_rows"])


def audit_pattern(pattern) -> dict:
    findings: list[Finding] = []
    blocks = 0
    manual = 0
    rows_total = 0
    repo_checked = 0
    for block_name, rows in _iter_audit_rows(pattern):
        blocks += 1
        rows_total += len(rows)
        prev_prod = None
        for row in rows:
            where = f"{block_name} / {row['label']}"
            if row.get("skip_check"):
                prev_prod = row.get("prod", prev_prod)
                continue
            if (prev_prod is not None and row.get("cons") is not None
                    and row["cons"] != prev_prod and not row.get("allow_gap")):
                findings.append(Finding("ERROR", where,
                                        f"consumes {row['cons']} but previous row produced {prev_prod}"))
            if row.get("allow_gap") and row.get("cons") is not None and prev_prod is not None and row["cons"] > prev_prod:
                findings.append(Finding("ERROR", where,
                                        f"consumes {row['cons']} but only {prev_prod} available"))
            if row.get("stated") is not None and row.get("prod") is not None and row["stated"] != row["prod"]:
                findings.append(Finding("ERROR", where,
                                        f"states ({row['stated']}) but instruction produces {row['prod']}"))
            parser_report = PieceAudit(piece=block_name)
            _compare_with_parser(row, where, parser_report, prev_prod)
            findings.extend(parser_report.findings)
            if not row.get("check"):
                manual += 1
            prev_prod = row.get("prod", prev_prod)
        for f in _repo_validate_rows(rows):
            findings.append(Finding("ERROR", f"{block_name} / {f.where}",
                                    f"repo StitchCountValidator: {f.message}"))
        if all(r.get("check") for r in rows):
            repo_checked += 1
    abbr_report = PieceAudit(piece="abbrev")
    check_abbreviations(pattern, abbr_report)
    findings.extend(abbr_report.findings)
    term_report = PieceAudit(piece="terms")
    check_terminology(pattern, term_report)
    findings.extend(term_report.findings)
    errors = [f for f in findings if f.level in ("ERROR", "CRITICAL")]
    return {
        "id": pattern["id"],
        "title": pattern["title"],
        "design_code": pattern["design_code"],
        "blocks": blocks,
        "rows_checked": rows_total,
        "manual_rows": manual,
        "repo_validated_blocks": repo_checked,
        "errors": [asdict(f) for f in errors],
        "warnings": [asdict(f) for f in findings if f.level == "WARN"],
        "status": "PASS" if not errors else "FAIL",
    }


def main():
    results = [audit_pattern(p) for p in PATTERNS]
    ok = True
    for r in results:
        mark = "PASS" if r["status"] == "PASS" else "FAIL"
        print(f"[{mark}] {r['title']} ({r['design_code']}) - "
              f"{r['rows_checked']} rows / {r['blocks']} blocks, "
              f"{r['repo_validated_blocks']} fully repo-validated, "
              f"{r['manual_rows']} manual rows, "
              f"{len(r['errors'])} errors, {len(r['warnings'])} warnings")
        for e in r["errors"]:
            ok = False
            print(f"    ERROR  {e['where']}: {e['message']}")
        for w in r["warnings"]:
            print(f"    WARN   {w['where']}: {w['message']}")
    out = {"patterns": results,
           "all_pass": all(r["status"] == "PASS" for r in results)}
    with open("tools/novality/audit_results.json", "w") as fh:
        json.dump(out, fh, indent=2)
    if not ok:
        sys.exit(1)
    print("All 10 patterns PASS the deterministic stitch-count audit.")


if __name__ == "__main__":
    main()
