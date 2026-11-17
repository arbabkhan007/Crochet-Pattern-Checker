"""SQLite persistence for consensus runs, report history, and draft ancestry."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ConsensusHistoryStore:
    """Local store; revisions create child rows and never mutate parent text."""

    def __init__(self, database_path: str | Path | None = None):
        if database_path is None:
            database_path = os.environ.get(
                "CROCHET_CONSENSUS_DATABASE", ".crochet_consensus/history.sqlite3"
            )
        self._memory = str(database_path) == ":memory:"
        self._keeper: sqlite3.Connection | None = None
        if self._memory:
            self.database_path = (
                f"file:crochet_consensus_{uuid.uuid4().hex}?mode=memory&cache=shared"
            )
            self._keeper = sqlite3.connect(
                self.database_path, uri=True, check_same_thread=False
            )
        else:
            self.database_path = str(Path(database_path).expanduser())
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(
            self.database_path, timeout=15, uri=self._memory, check_same_thread=False
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=15000")
        try:
            yield connection
        except BaseException:
            connection.rollback()
            raise
        else:
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connect() as db:
            if not self._memory:
                db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS consensus_runs (
                    run_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    pattern_hash TEXT NOT NULL,
                    pattern_text TEXT NOT NULL,
                    parent_run_id TEXT REFERENCES consensus_runs(run_id),
                    root_run_id TEXT,
                    revision_number INTEGER NOT NULL DEFAULT 0,
                    revision_changes_json TEXT NOT NULL DEFAULT '[]',
                    report_json TEXT,
                    progress_json TEXT NOT NULL DEFAULT '{}',
                    error TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_consensus_created ON consensus_runs(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_consensus_parent ON consensus_runs(parent_run_id, revision_number);
            """)

    def create_run(
        self,
        run_id: str,
        pattern_text: str,
        *,
        parent_run_id: str | None = None,
        revision_number: int = 0,
        revision_changes: Iterable[dict[str, Any]] = (),
    ) -> dict[str, Any]:
        now = _now()
        pattern_hash = hashlib.sha256(pattern_text.encode("utf-8")).hexdigest()
        progress = {
            "stage": "queued",
            "current": 0,
            "total": 5,
            "message": "Waiting to start validation",
            "updated_at": now,
        }
        with self._connect() as db:
            if parent_run_id:
                parent = db.execute(
                    "SELECT root_run_id FROM consensus_runs WHERE run_id=?",
                    (parent_run_id,),
                ).fetchone()
                if parent is None:
                    raise KeyError(parent_run_id)
                root_id = parent["root_run_id"] or parent_run_id
            else:
                root_id = run_id
            db.execute(
                """INSERT INTO consensus_runs
                (run_id,created_at,updated_at,status,pattern_hash,pattern_text,parent_run_id,root_run_id,revision_number,revision_changes_json,report_json,progress_json,error)
                VALUES (?,?,?,'queued',?,?,?,?,?,?,NULL,?,NULL)""",
                (
                    run_id,
                    now,
                    now,
                    pattern_hash,
                    pattern_text,
                    parent_run_id,
                    root_id,
                    revision_number,
                    json.dumps(list(revision_changes), ensure_ascii=False),
                    json.dumps(progress),
                ),
            )
        return self.get_run(run_id) or {}

    def update_progress(self, run_id: str, progress: dict[str, Any]) -> None:
        with self._connect() as db:
            db.execute(
                "UPDATE consensus_runs SET updated_at=?,status='running',progress_json=? WHERE run_id=?",
                (_now(), json.dumps(progress, ensure_ascii=False), run_id),
            )

    def set_running(self, run_id: str) -> None:
        with self._connect() as db:
            db.execute(
                "UPDATE consensus_runs SET updated_at=?,status='running' WHERE run_id=?",
                (_now(), run_id),
            )

    def save_report(self, run_id: str, report: dict[str, Any]) -> None:
        progress = {
            "stage": "completed",
            "current": 5,
            "total": 5,
            "message": "Validation report saved",
            "updated_at": _now(),
        }
        with self._connect() as db:
            cursor = db.execute(
                "UPDATE consensus_runs SET updated_at=?,status='completed',report_json=?,progress_json=?,error=NULL WHERE run_id=?",
                (
                    _now(),
                    json.dumps(report, ensure_ascii=False, separators=(",", ":")),
                    json.dumps(progress),
                    run_id,
                ),
            )
            if cursor.rowcount == 0:
                raise KeyError(run_id)

    def mark_failed(self, run_id: str, safe_error: str) -> None:
        progress = {
            "stage": "failed",
            "current": 0,
            "total": 5,
            "message": "Run failed; no approval issued",
            "updated_at": _now(),
        }
        with self._connect() as db:
            db.execute(
                "UPDATE consensus_runs SET updated_at=?,status='failed',error=?,progress_json=? WHERE run_id=?",
                (_now(), safe_error[:400], json.dumps(progress), run_id),
            )

    def get_pattern_text(self, run_id: str) -> str:
        with self._connect() as db:
            row = db.execute(
                "SELECT pattern_text FROM consensus_runs WHERE run_id=?", (run_id,)
            ).fetchone()
        if row is None:
            raise KeyError(run_id)
        return str(row["pattern_text"])

    def revision_number(self, run_id: str) -> int:
        with self._connect() as db:
            row = db.execute(
                "SELECT revision_number FROM consensus_runs WHERE run_id=?", (run_id,)
            ).fetchone()
        if row is None:
            raise KeyError(run_id)
        return int(row["revision_number"])

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute(
                "SELECT * FROM consensus_runs WHERE run_id=?", (run_id,)
            ).fetchone()
        return self._row(row) if row else None

    def list_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 200))
        with self._connect() as db:
            rows = db.execute(
                "SELECT * FROM consensus_runs ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        result = []
        for row in rows:
            item = self._row(row) or {}
            report = item.pop("report", None)
            item["approval_status"] = report.get("approval_status") if report else None
            item["approved"] = bool(report.get("approved")) if report else False
            item["weighted_score"] = (
                report.get("scoring", {}).get("weighted_score") if report else None
            )
            models = report.get("models", {}) if report else {}
            item["configured_model_count"] = len(models.get("configured", []))
            item["participating_model_count"] = len(models.get("participating", []))
            item["failed_model_count"] = len(models.get("failed", []))
            result.append(item)
        return result

    @staticmethod
    def _row(row: sqlite3.Row) -> dict[str, Any]:
        def decode(name: str, fallback: Any):
            try:
                return json.loads(row[name]) if row[name] else fallback
            except (TypeError, json.JSONDecodeError):
                return fallback

        return {
            "run_id": row["run_id"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "status": row["status"],
            "pattern_hash": row["pattern_hash"],
            "parent_run_id": row["parent_run_id"],
            "root_run_id": row["root_run_id"],
            "revision_number": row["revision_number"],
            "revision_changes": decode("revision_changes_json", []),
            "report": decode("report_json", None),
            "progress": decode("progress_json", {}),
            "error": row["error"],
        }
