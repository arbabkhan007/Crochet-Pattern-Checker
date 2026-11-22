#!/usr/bin/env python3
"""Validate a private JSON response/manifest against one of the public eval schemas."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class ValidationError(ValueError):
    """Raised for unreadable JSON, invalid schemas, or schema violations."""


def _load(path: str) -> Any:
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read JSON file {path!r}: {exc}") from exc


def validate(instance_path: str, schema_path: str) -> None:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        raise ValidationError("install eval dependencies with: python3 -m pip install -r evals/requirements.txt") from exc

    schema = _load(schema_path)
    instance = _load(instance_path)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema exception subclasses
        raise ValidationError(f"invalid schema {schema_path!r}: {exc}") from exc
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: (list(map(str, error.absolute_path)), error.message))
    if errors:
        details = []
        for error in errors[:20]:
            path = ".".join(str(part) for part in error.absolute_path) or "$"
            details.append(f"{path}: {error.message}")
        if len(errors) > 20:
            details.append(f"... and {len(errors) - 20} more validation error(s)")
        raise ValidationError("\n".join(details))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True, help="public JSON Schema path")
    parser.add_argument("--input", required=True, help="private JSON instance path")
    args = parser.parse_args(argv)
    try:
        validate(args.input, args.schema)
    except ValidationError as exc:
        print(f"validate.py: {exc}", file=sys.stderr)
        return 2
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
