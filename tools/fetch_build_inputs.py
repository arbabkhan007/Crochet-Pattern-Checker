#!/usr/bin/env python3
"""Fetch the checksum-pinned source assets needed by the optional PDF/Etsy builders.

Files are stored in an external cache, never in the repository working tree.
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
EXPECTED_COMMIT = "49d69daeb8d7a2462d5e5bef5394a4ff5d170a3b"
MANIFEST_PATH = Path(__file__).with_name("build-inputs-manifest.json")
DEFAULT_CACHE = Path.home() / ".cache" / "crochet-pattern-checker" / EXPECTED_COMMIT
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
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"unsafe manifest path: {value!r}")
    if "\\" in value or "\x00" in value:
        raise ValueError(f"unsafe manifest path: {value!r}")
    return path


def load_manifest() -> tuple[dict, str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    source = manifest.get("source", {})
    if source.get("repository") != EXPECTED_REPOSITORY or source.get("commit") != EXPECTED_COMMIT:
        raise ValueError("build-input manifest is not pinned to the reviewed repository commit")
    raw_base = f"https://raw.githubusercontent.com/{EXPECTED_REPOSITORY}/{EXPECTED_COMMIT}/"
    if source.get("raw_base") != raw_base:
        raise ValueError("build-input manifest has an unexpected source URL")
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("files"), list):
        raise ValueError("unsupported build-input manifest schema")
    return manifest, raw_base


def resolve_target(cache_root: Path, relative: PurePosixPath) -> Path:
    root = cache_root.expanduser().resolve()
    target = root.joinpath(*relative.parts)
    resolved = target.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"manifest path escapes cache root: {relative.as_posix()}") from exc
    return resolved


def verify_file(path: Path, item: dict) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    digest, size = sha256_and_size(path)
    return digest == item["sha256"] and size == item["size_bytes"]


def fetch_item(item: dict, raw_base: str, cache_root: Path, dry_run: bool) -> tuple[str, int]:
    relative = safe_relative_path(item["path"])
    target = resolve_target(cache_root, relative)
    expected_sha = item.get("sha256", "")
    expected_size = item.get("size_bytes")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha) or not isinstance(expected_size, int) or expected_size < 0:
        raise ValueError(f"invalid size/hash metadata for {relative.as_posix()}")

    if target.exists():
        if verify_file(target, item):
            print(f"[ok]      {relative.as_posix()}")
            return "ok", 0
        raise RuntimeError(
            f"cached file is present but does not match the pinned hash: {target}\n"
            "Move or remove that cache file, then rerun; the fetcher will not overwrite it silently."
        )

    if dry_run:
        print(f"[missing] {relative.as_posix()} ({expected_size} bytes)")
        return "missing", expected_size

    target.parent.mkdir(parents=True, exist_ok=True)
    url = raw_base + quote(relative.as_posix(), safe="/")
    request = Request(url, headers={"User-Agent": "Crochet-Pattern-Checker-build-input-fetcher/1"})
    temp_path: Path | None = None
    digest = hashlib.sha256()
    received = 0
    try:
        fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".part", dir=target.parent)
        temp_path = Path(temp_name)
        with os.fdopen(fd, "wb") as output, urlopen(request, timeout=60) as response:
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
                f"got {received} bytes / {digest.hexdigest()}, expected {expected_size} / {expected_sha}"
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
    parser.add_argument("--group", choices=("novality", "publish", "all"), default="all",
                        help="which builder inputs to fetch (default: all)")
    parser.add_argument("--cache-dir", type=Path, default=None,
                        help="external cache root (default: CROCHET_BUILD_CACHE or ~/.cache/crochet-pattern-checker/<commit>)")
    parser.add_argument("--dry-run", action="store_true", help="report missing/hash-mismatched inputs without downloading")
    args = parser.parse_args()

    try:
        manifest, raw_base = load_manifest()
        cache_root = (args.cache_dir or Path(os.environ.get("CROCHET_BUILD_CACHE", DEFAULT_CACHE))).expanduser().resolve()
        groups = {"novality", "publish"} if args.group == "all" else {args.group}
        selected = [item for item in manifest["files"] if groups.intersection(item.get("groups", []))]
        if not selected:
            raise ValueError(f"no build inputs listed for group {args.group!r}")
        print(f"Pinned source: {EXPECTED_REPOSITORY} at {EXPECTED_COMMIT}")
        print(f"Cache root: {cache_root}")
        print(f"Group(s): {', '.join(sorted(groups))}; files: {len(selected)}")

        totals = {"ok": 0, "missing": 0, "fetched": 0, "bytes": 0}
        for item in selected:
            status, size = fetch_item(item, raw_base, cache_root, args.dry_run)
            totals[status] += 1
            totals["bytes"] += size
        print(f"Summary: {totals['ok']} verified, {totals['fetched']} fetched, {totals['missing']} missing; "
              f"{totals['bytes']} bytes downloaded or needed")
        if args.dry_run and totals["missing"]:
            print("DRY RUN ONLY; no files downloaded.")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
