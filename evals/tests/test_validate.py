import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

EVALS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVALS_DIR))
from validate import ValidationError, validate  # noqa: E402


class ValidateTests(unittest.TestCase):
    def test_all_schemas_are_valid_draft_2020_12(self):
        for schema_path in (EVALS_DIR / "schemas").glob("*.json"):
            with self.subTest(schema=schema_path.name):
                Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding="utf-8")))

    def test_solver_schema_accepts_minimal_well_formed_report(self):
        report = {
            "fixture": "opaque-id",
            "defects": [],
            "coverage": [{"area": "stitch_counts", "status": "checked", "reason": "all rows reviewed"}],
            "untestable_reasons": [],
            "summary": "No supported defects found.",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "solver.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            validate(str(path), str(EVALS_DIR / "schemas" / "solver.schema.json"))

    def test_aggregate_input_schema_accepts_synthetic_complete_batch(self):
        aggregate = {
            "split": "development",
            "fixtures": ["synthetic-a"],
            "replicates_per_fixture": 1,
            "batches": [{
                "id": "batch-1",
                "runs": [{
                    "fixture": "synthetic-a",
                    "replicate": "r1",
                    "score": 0,
                    "refuted_count": 0,
                    "failure_taxonomy": {"math": 0, "coherence": 0, "finishing": 0, "absurdity": 0, "format": 1},
                }],
            }],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "aggregate.json"
            path.write_text(json.dumps(aggregate), encoding="utf-8")
            validate(str(path), str(EVALS_DIR / "schemas" / "aggregate-input.schema.json"))

    def test_solver_schema_rejects_extra_keys(self):
        report = {
            "fixture": "opaque-id",
            "defects": [],
            "coverage": [],
            "untestable_reasons": [],
            "summary": "",
            "rubric_answer": "must not appear",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "solver.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "rubric_answer"):
                validate(str(path), str(EVALS_DIR / "schemas" / "solver.schema.json"))


if __name__ == "__main__":
    unittest.main()
