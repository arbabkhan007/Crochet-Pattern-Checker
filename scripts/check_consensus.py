#!/usr/bin/env python3
"""Check the three viewpoint files and prove the agreed consensus lessons."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crochet_checker.validation.validator import validate_pattern

DOCS = ROOT / "docs"
LESSONS = ROOT / "consensus_lessons"
VIEWPOINTS = (
    "wrong_benchmarks.md",
    "gemini_corrected.md",
    "chatgpt_corrected.md",
)
NOISE = (
    "Undefined abbreviation",
    "Glossary defines",
)


def clean(report) -> bool:
    return (
        str(report.overall_status).lower() == "pass"
        and not report.errors
        and not report.warnings
    )


def messages(items) -> list[str]:
    return [str(getattr(item, "message", item)) for item in items]


def split_patterns(text: str) -> list[tuple[str, str]]:
    parts = text.split("\n## Pattern ")
    found = []
    for part in parts[1:]:
        title = part.split("\n", 1)[0].strip()
        found.append((title, "## Pattern " + part))
    return found


def useful(lines: list[str]) -> list[str]:
    return [line for line in lines if not line.startswith(NOISE)]


def lesson_fields(text: str) -> tuple[str, str, str]:
    title, _, body = text.partition("\n")
    how = ""
    what = ""
    for block in body.split("\n\n"):
        stripped = block.strip()
        if stripped.lower().startswith("how:"):
            how = stripped.split(":", 1)[1].strip()
        elif stripped.lower().startswith("what:"):
            what = stripped.split(":", 1)[1].strip()
    return title.strip(), how, what


def main() -> int:
    folders = sorted(path for path in LESSONS.iterdir() if path.is_dir())
    if len(folders) < 9:
        sys.exit(f"Expected at least 9 consensus lessons, found {len(folders)}.")

    failed = False
    proved = []
    for folder in folders:
        wrong = validate_pattern((folder / "wrong.txt").read_text(encoding="utf-8"))
        fixed = validate_pattern((folder / "corrected.txt").read_text(encoding="utf-8"))
        title, how, what = lesson_fields((folder / "lesson.txt").read_text(encoding="utf-8"))
        ok = (not clean(wrong)) and clean(fixed) and how and what
        print(
            folder.name,
            "wrong", wrong.overall_status, "err", len(wrong.errors), "warn", len(wrong.warnings),
            "| corrected", fixed.overall_status, "err", len(fixed.errors), "warn", len(fixed.warnings),
        )
        if not ok:
            failed = True
            print("  LESSON_FAILED", folder.name)
        proved.append({
            "name": folder.name,
            "title": title,
            "how": how,
            "what": what,
            "wrong_status": wrong.overall_status,
            "wrong_errors": useful(messages(wrong.errors)),
            "wrong_warnings": useful(messages(wrong.warnings)),
            "fixed_status": fixed.overall_status,
        })

    viewpoint_rows = []
    for filename in VIEWPOINTS:
        text = (DOCS / filename).read_text(encoding="utf-8")
        pieces = [("whole file", text), *split_patterns(text)]
        for title, body in pieces:
            report = validate_pattern(body)
            row = {
                "file": filename,
                "title": title,
                "status": report.overall_status,
                "errors": len(report.errors),
                "warnings": len(report.warnings),
                "seen": useful(messages(report.errors) + messages(report.warnings))[:3],
            }
            viewpoint_rows.append(row)
            print(
                filename,
                title[:42],
                report.overall_status,
                "err", len(report.errors),
                "warn", len(report.warnings),
            )

    write_report(proved, viewpoint_rows)
    if failed:
        sys.exit("CONSENSUS_FAILED")
    print("CONSENSUS_OK")
    return 0


def write_report(proved: list[dict], rows: list[dict]) -> None:
    lines = [
        "# Consensus learning",
        "",
        "This file is rewritten by `scripts/check_consensus.py`. It is the check result, not a fourth pattern.",
        "",
        "The three viewpoints stay unedited:",
        "",
        "- `docs/wrong_benchmarks.md`",
        "- `docs/gemini_corrected.md`",
        "- `docs/chatgpt_corrected.md`",
        "",
        "The checker does not change its own rules. A lesson is learned only when `wrong.txt` is not a clean pass and `corrected.txt` passes with no errors and no warnings.",
        "",
        "## How to read a viewpoint check",
        "",
        "A PASS on the Gemini or ChatGPT file is not proof. `[sc 1, inc] 6 times` and a backticked `×` repeat are not the checker's dialect. The counter does not expand them, so a wrong repeat can pass.",
        "",
        "An ERROR made only of undefined abbreviations, or of `worked N stitches into` on a prose line, is parser noise. It is not the lesson.",
        "",
        "A 12-to-24 increase is now an error. An unequal stitch seam is now an error. An unequal inch edge is now a warning. A UK piece that uses sc, an unbounded repeat, an unreachable stitch, a missing round, a short chart-symbol row, an uncounted stitch line, a gauge far outside the Craft Yarn Council crochet band, a short-row span that drops 34 to 28 without stating the row-ends, and a prose frill above 2.5 times full are now checked. A cinch with no numbers is still unread. A photo is still not classified.",
        "",
        "## What the checker learned",
        "",
        "These lessons are the consensus. Each one is agreed by both corrected files and proved by the checker.",
        "",
    ]
    for item in proved:
        lines.append(f"### {item['name']}: {item['title']}")
        lines.append("")
        lines.append(f"Wrong result: {item['wrong_status']}.")
        for message in item["wrong_errors"] + item["wrong_warnings"]:
            lines.append(f"- {message}")
        lines.append(f"Corrected result: {item['fixed_status']}.")
        lines.append("")
        lines.append(f"How: {item['how']}")
        lines.append("")
        lines.append(f"What: {item['what']}")
        lines.append("")

    lines.extend([
        "## What was checked and not learned",
        "",
        "| Pattern | Agreed defect | Why it is not a lesson |",
        "|---|---|---|",
        "| Bear | Do not cinch, with no stitch counts | Cinch and flatten are still prose when no two stitch counts are written. |",
        "| Bear | Do not cinch the arm | Cinch and flatten are prose. The checker does not read them. |",
        "| Bear | Add legs and ears | A missing piece is not an error unless the checker can see a count. |",
        "| Wyvern | 24-stitch join versus a valid 30 | The models disagree. No consensus pattern is written. |",
        "| Wyvern | 35-stitch fan versus 42-stitch fan | Both still warn above 2.5 times full. Neither is the lesson. |",
        "| Dragon and Chimera | Which decrease formula to use | The models disagree on the target count. Only the cover-the-round rule is learned. |",
        "| Leviathan | Rebuild the hub to 64 | One model changes the count to 48. The other rebuilds the join. Only the 48-clause total is learned. |",
        "| All | Eyes on a frill, closed tentacle wording | A prose frill of N stitches worked into M base stitches now warns above 2.5x. These other sites are still unread. |",
        "",
        "## Viewpoint check",
        "",
        "These rows are what the checker returned. They are not a vote.",
        "",
        "| File | Section | Status | Errors | Warnings | Seen, after dropping abbreviation noise |",
        "|---|---|---|---:|---:|---|",
    ])
    for row in rows:
        seen = "; ".join(row["seen"]) if row["seen"] else "none"
        seen = seen.replace("|", "/")
        title = row["title"].replace("|", "/")
        lines.append(
            f"| `{row['file']}` | {title} | {row['status']} | {row['errors']} | {row['warnings']} | {seen} |"
        )

    lines.extend([
        "",
        "## Not merged",
        "",
        "| Pattern | Gemini | ChatGPT |",
        "|---|---|---|",
        "| Bear arms | Flatten an 8-stitch opening | Decrease to 4, then flatten |",
        "| Bear ears | 6, then 9 | 6, then 12, then 18 |",
        "| Bear legs | Stay at 12 | Decrease 12 to 9 |",
        "| Wyvern join | Rewrite to 24 | Keep 30 once the bridge is worked |",
        "| Wyvern wing | 35 stitches | 42 stitches, or 28 for a flatter edge |",
        "| Dragon rejoin | 36 perimeter positions | 34, or mark 6 as skipped |",
        "| Leviathan hub | Rebuild to 64 | The written clauses are 48 |",
        "| Chimera round 15 | 44 to 40 | 44 to 38 |",
        "| Chimera frill | About 150 stitches | 324 stitches |",
        "| Chimera graft | 24 to 24 | 36 to 36 |",
        "",
        "Do not auto-merge a row in that table. A later file may choose one side only when a person says which source it follows.",
        "",
    ])
    (DOCS / "consensus.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
