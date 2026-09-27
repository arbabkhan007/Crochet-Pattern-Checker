"""Tamper-evident enterprise certification audit trail."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditTrail:
    """Append-only hash-chained audit storage."""

    def __init__(self, path: str = ".crochet_learning/audit.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _hash(data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def _last_hash(self) -> str:
        if not self.path.exists():
            return "GENESIS"

        lines = self.path.read_text(encoding="utf-8").splitlines()
        if not lines:
            return "GENESIS"

        try:
            return json.loads(lines[-1])["record_hash"]
        except (KeyError, json.JSONDecodeError):
            return "CORRUPTED"

    def append(
        self,
        *,
        pattern_hash: str,
        certification,
        operator: str = "system",
        action: str = "CERTIFICATION",
    ) -> dict[str, Any]:
        previous_hash = self._last_hash()

        record: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operator": operator,
            "action": action,
            "pattern_hash": pattern_hash,
            "previous_hash": previous_hash,
            "certification": certification.to_dict(),
        }

        canonical = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
        )

        record["record_hash"] = self._hash(canonical)

        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

        return record

    def records(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        result = []

        for line in self.path.read_text(
            encoding="utf-8"
        ).splitlines():
            if line.strip():
                result.append(json.loads(line))

        return result

    def verify(self) -> tuple[bool, list[str]]:
        records = self.records()
        errors: list[str] = []
        previous_hash = "GENESIS"

        for index, record in enumerate(records):
            if record.get("previous_hash") != previous_hash:
                errors.append(
                    f"Record {index}: previous hash does not match."
                )

            stored_hash = record.get("record_hash")
            unsigned = dict(record)
            unsigned.pop("record_hash", None)

            canonical = json.dumps(
                unsigned,
                sort_keys=True,
                separators=(",", ":"),
            )
            calculated_hash = self._hash(canonical)

            if stored_hash != calculated_hash:
                errors.append(
                    f"Record {index}: record hash is invalid."
                )

            previous_hash = stored_hash or "CORRUPTED"

        return not errors, errors

    def export(self, output: str) -> Path:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.records(), indent=2),
            encoding="utf-8",
        )
        return destination
