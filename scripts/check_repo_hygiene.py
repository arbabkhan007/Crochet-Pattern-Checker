"""Fail CI if machine-local environments or generated caches are tracked."""

from __future__ import annotations

import subprocess
import sys

FORBIDDEN_DIRECTORY_NAMES = {
    ".venv",
    "venv",
    "ENV",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


def main() -> int:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    tracked = [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]
    offenders = [
        path
        for path in tracked
        if any(part in FORBIDDEN_DIRECTORY_NAMES for part in path.split("/"))
        or path.endswith(tuple(FORBIDDEN_SUFFIXES))
    ]

    if offenders:
        print("Tracked local environments or generated files found:", file=sys.stderr)
        for path in offenders:
            print(f"  {path}", file=sys.stderr)
        return 1

    print("Repository hygiene check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
