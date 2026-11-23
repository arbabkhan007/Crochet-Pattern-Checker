import sys
import unittest
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVALS_DIR))
from aggregate import EvaluationError, assess_development_change, summarize  # noqa: E402


def make_payload(split="holdout", batch_count=3, score_a=93, score_b=91, refuted=0):
    batches = []
    for batch_index in range(batch_count):
        runs = []
        for fixture, score in (("opaque-a", score_a), ("opaque-b", score_b)):
            for replicate in ("r1", "r2"):
                runs.append({
                    "fixture": fixture,
                    "replicate": replicate,
                    "score": score,
                    "refuted_count": refuted if batch_index == 0 else 0,
                    "failure_taxonomy": {"math": 0, "coherence": 0, "finishing": 0, "absurdity": 0, "format": 0},
                })
        batches.append({"id": f"batch-{batch_index + 1}", "runs": runs})
    return {"split": split, "fixtures": ["opaque-a", "opaque-b"], "replicates_per_fixture": 2, "batches": batches}


class AggregateTests(unittest.TestCase):
    def test_holdout_pass_uses_macro_fixture_means(self):
        result = summarize(make_payload())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["macro_average"], 92.0)
        self.assertEqual(result["fixture_means"], {"opaque-a": 93.0, "opaque-b": 91.0})

    def test_holdout_below_fixture_floor_fails(self):
        result = summarize(make_payload(score_a=99, score_b=84))
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["final_gate"]["every_fixture_ok"])

    def test_any_refuted_claim_in_final_three_batches_fails_clean_gate(self):
        result = summarize(make_payload(refuted=1))
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["final_gate"]["consecutive_clean_batches_ok"])

    def test_fewer_than_three_holdout_batches_is_incomplete(self):
        result = summarize(make_payload(batch_count=2))
        self.assertEqual(result["status"], "INCOMPLETE")

    def test_failure_taxonomy_is_aggregated(self):
        payload = make_payload()
        payload["batches"][0]["runs"][0]["failure_taxonomy"].update({"math": 2, "format": 1})
        payload["batches"][0]["runs"][0]["score"] = 0
        result = summarize(payload)
        self.assertEqual(result["failure_taxonomy"]["math"], 2)
        self.assertEqual(result["failure_taxonomy"]["format"], 1)

    def test_development_results_do_not_claim_final_pass(self):
        result = summarize(make_payload(split="development"))
        self.assertEqual(result["status"], "DEVELOPMENT_SCORED")

    def test_incomplete_batch_matrix_is_rejected(self):
        payload = make_payload()
        payload["batches"][0]["runs"].pop()
        with self.assertRaisesRegex(EvaluationError, "exactly fixtures"):
            summarize(payload)

    def test_tuning_requires_gain_and_limits_fixture_regression(self):
        baseline = {"split": "development", "macro_average": 80.0, "fixture_means": {"a": 78.0, "b": 82.0}}
        candidate = {"split": "development", "macro_average": 82.0, "fixture_means": {"a": 80.0, "b": 84.0}}
        self.assertTrue(assess_development_change(candidate, baseline)["accepted"])
        regressing = {"split": "development", "macro_average": 82.0, "fixture_means": {"a": 72.0, "b": 92.0}}
        self.assertFalse(assess_development_change(regressing, baseline)["accepted"])


if __name__ == "__main__":
    unittest.main()
