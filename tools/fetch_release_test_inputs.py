#!/usr/bin/env python3
"""Fetch checksum-pinned NS01 images and release PDFs into an external cache.

The checkout stays free of the reviewed media removals. Collection archives are
built separately from these PDFs and the current Markdown masters by
run_tests_with_release_inputs.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from urllib.request import Request, urlopen

EXPECTED_REPOSITORY = "arbabkhan007/Crochet-Pattern-Checker"
EXPECTED_COMMIT = "9dbdfab5cf05e68a2136897f9739a0d81cc54114"
MANIFEST_PATH = Path(__file__).with_name("release-test-inputs-manifest.json")
DEFAULT_CACHE = (
    Path.home()
    / ".cache"
    / "crochet-pattern-checker"
    / "release-test-inputs"
    / EXPECTED_COMMIT
)
CHUNK_SIZE = 1024 * 1024


def sha256_and_size(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while True:
            block = stream.read(CHUNK_SIZE)
            if not block:
                break
            digest.update(block)
            size += len(block)
    return digest.hexdigest(), size


def safe_relative_path(value: str) -> PurePosixPath:
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or "\x00" in value
        or any(part in ("", ".", "..") for part in value.split("/"))
    ):
        raise ValueError(f"unsafe manifest path: {value!r}")
    return PurePosixPath(value)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def validate_external_cache(cache_root: Path) -> Path:
    root = cache_root.expanduser().resolve()
    repo = repository_root().resolve()
    try:
        root.relative_to(repo)
    except ValueError:
        return root
    raise ValueError(
        f"cache must be outside the repository checkout ({repo}); got {root}"
    )


def load_manifest() -> tuple[dict, str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    source = manifest.get("source", {})
    expected_base = (
        f"https://raw.githubusercontent.com/{EXPECTED_REPOSITORY}/"
        f"{EXPECTED_COMMIT}/"
    )
    if (
        source.get("repository") != EXPECTED_REPOSITORY
        or source.get("commit") != EXPECTED_COMMIT
        or source.get("raw_base") != expected_base
    ):
        raise ValueError("input manifest is not pinned to the reviewed source commit")
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported input manifest schema")
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ValueError("input manifest files must be a list")
    groups = manifest.get("groups", {})
    if groups.get("ns01-images", {}).get("count") != 2:
        raise ValueError("expected exactly two NS01 image inputs")
    if groups.get("release-pdfs", {}).get("count") != 34:
        raise ValueError("expected exactly 34 release PDF inputs")
    if len(files) != 36:
        raise ValueError(f"expected 36 pinned inputs, found {len(files)}")
    return manifest, expected_base


def resolve_target(cache_root: Path, relative: PurePosixPath) -> Path:
    root = cache_root.resolve()
    target = root.joinpath(*relative.parts)
    resolved = target.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"manifest path escapes the external cache: {relative.as_posix()}"
        ) from exc
    return resolved


def verify_file(path: Path, item: dict) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    digest, size = sha256_and_size(path)
    return digest == item["sha256"] and size == item["size_bytes"]


def fetch_item(
    item: dict, raw_base: str, cache_root: Path, dry_run: bool
) -> tuple[str, int]:
    relative = safe_relative_path(item["path"])
    target = resolve_target(cache_root, relative)
    expected_sha = item.get("sha256", "")
    expected_size = item.get("size_bytes")
    if (
        not re.fullmatch(r"[0-9a-f]{64}", expected_sha)
        or not isinstance(expected_size, int)
        or isinstance(expected_size, bool)
        or expected_size < 0
    ):
        raise ValueError(f"invalid size/hash metadata for {relative.as_posix()}")

    if target.exists() or target.is_symlink():
        if verify_file(target, item):
            print(f"[ok]      {relative.as_posix()}")
            return "ok", 0
        raise RuntimeError(
            f"cached file exists but does not match the pinned SHA-256/size: {target}\n"
            "Move or remove that cache entry, then rerun; it will not be overwritten silently."
        )

    if dry_run:
        print(f"[missing] {relative.as_posix()} ({expected_size} bytes)")
        return "missing", expected_size

    target.parent.mkdir(parents=True, exist_ok=True)
    url = raw_base + quote(relative.as_posix(), safe="/")
    request = Request(
        url,
        headers={"User-Agent": "Crochet-Pattern-Checker-release-input-fetcher/1"},
    )
    temp_path: Path | None = None
    digest = hashlib.sha256()
    received = 0
    try:
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".part", dir=target.parent
        )
        temp_path = Path(temp_name)
        with os.fdopen(fd, "wb") as output, urlopen(request, timeout=90) as response:
            while True:
                block = response.read(CHUNK_SIZE)
                if not block:
                    break
                output.write(block)
                digest.update(block)
                received += len(block)
        if received != expected_size or digest.hexdigest() != expected_sha:
            raise RuntimeError(
                f"download verification failed for {relative.as_posix()}: "
                f"got {received} bytes / {digest.hexdigest()}, expected "
                f"{expected_size} bytes / {expected_sha}"
            )
        os.chmod(temp_path, 0o644)
        os.replace(temp_path, target)
        temp_path = None
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass

    print(f"[fetched] {relative.as_posix()} ({received} bytes)")
    return "fetched", received


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--group",
        choices=("ns01-images", "release-pdfs", "all"),
        default="all",
        help="which input group to fetch (default: all)",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help=(
            "external cache root (default: CROCHET_RELEASE_INPUT_CACHE or "
            "~/.cache/crochet-pattern-checker/release-test-inputs/<commit>)"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report missing or mismatched inputs without downloading",
    )
    args = parser.parse_args()

    try:
        manifest, raw_base = load_manifest()
        requested_cache = args.cache_dir or Path(
            os.environ.get("CROCHET_RELEASE_INPUT_CACHE", DEFAULT_CACHE)
        )
        cache_root = validate_external_cache(requested_cache)
        selected_groups = (
            {"ns01-images", "release-pdfs"}
            if args.group == "all"
            else {args.group}
        )
        selected = [
            item
            for item in manifest["files"]
            if selected_groups.intersection(item.get("groups", []))
        ]
        expected_count = sum(
            manifest["groups"][group]["count"] for group in selected_groups
        )
        if len(selected) != expected_count:
            raise ValueError(
                f"manifest group count mismatch: expected {expected_count}, "
                f"found {len(selected)}"
            )

        print(f"Pinned source: {EXPECTED_REPOSITORY} at {EXPECTED_COMMIT}")
        print(f"Cache root: {cache_root}")
        print(f"Group(s): {', '.join(sorted(selected_groups))}; files: {len(selected)}")
        totals = {"ok": 0, "missing": 0, "fetched": 0, "bytes": 0}
        for item in selected:
            status, size = fetch_item(item, raw_base, cache_root, args.dry_run)
            totals[status] += 1
            totals["bytes"] += size
        print(
            f"Summary: {totals['ok']} verified, {totals['fetched']} fetched, "
            f"{totals['missing']} missing; {totals['bytes']} bytes downloaded "
            "or needed"
        )
        if args.dry_run and totals["missing"]:
            print("DRY RUN ONLY; no files downloaded.")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
