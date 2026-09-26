"""Safe feedback and regression-learning store."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class LearningCase:
    case_id: str
    pattern_text: str
    corrected_text: str | None = None
    compiler_valid: bool = False
    score: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    source: str = "user"
    confirmed: bool = False
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LearningStore:
    """
    Stores feedback locally.

    No API calls are made. No rule is changed automatically.
    Confirmed cases can be exported as regression tests.
    """

    def __init__(
        self,
        root: str = ".crochet_learning",
    ):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.cases_file = self.root / "cases.jsonl"
        self.regression_dir = self.root / "regression"
        self.regression_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def make_id(pattern_text: str) -> str:
        digest = hashlib.sha256(
            pattern_text.strip().encode("utf-8")
        ).hexdigest()
        return digest[:20]

    @staticmethod
    def _messages(items) -> list[str]:
        return [
            getattr(item, "message", str(item))
            for item in items
        ]

    def record(
        self,
        pattern_text: str,
        report,
        corrected_text: str | None = None,
        confirmed: bool = False,
        source: str = "user",
    ) -> LearningCase:
        case = LearningCase(
            case_id=self.make_id(pattern_text),
            pattern_text=pattern_text,
            corrected_text=corrected_text,
            compiler_valid=bool(getattr(report, "valid", False)),
            score=int(getattr(report, "score", 0)),
            errors=self._messages(getattr(report, "errors", [])),
            warnings=self._messages(getattr(report, "warnings", [])),
            source=source,
            confirmed=confirmed,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        with self.cases_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(case.to_dict()) + "\n")

        if confirmed:
            self.export_regression(case)

        return case

    def export_regression(self, case: LearningCase) -> Path:
        path = self.regression_dir / f"{case.case_id}.json"
        path.write_text(
            json.dumps(case.to_dict(), indent=2),
            encoding="utf-8",
        )
        return path

    def cases(self) -> list[LearningCase]:
        if not self.cases_file.exists():
            return []

        result = []

        for line in self.cases_file.read_text(
            encoding="utf-8"
        ).splitlines():
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                result.append(LearningCase(**data))
            except (json.JSONDecodeError, TypeError):
                continue

        return result

    def statistics(self) -> dict[str, Any]:
        cases = self.cases()
        errors: dict[str, int] = {}

        for case in cases:
            for error in case.errors:
                key = re.sub(
                    r"\d+",
                    "<number>",
                    error.lower(),
                )
                errors[key] = errors.get(key, 0) + 1

        return {
            "total_cases": len(cases),
            "confirmed_cases": sum(
                1 for case in cases if case.confirmed
            ),
            "valid_cases": sum(
                1 for case in cases if case.compiler_valid
            ),
            "top_errors": sorted(
                errors.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:20],
        }

    def export_regression_tests(
        self,
        output_dir: str = "tests/regression",
    ) -> int:
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        count = 0

        for case in self.cases():
            if not case.confirmed:
                continue

            path = output / f"{case.case_id}.json"
            path.write_text(
                json.dumps(case.to_dict(), indent=2),
                encoding="utf-8",
            )
            count += 1

        return count
