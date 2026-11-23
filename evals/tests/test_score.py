import sys
import unittest
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVALS_DIR))
from score import EvaluationError, score_format_failure, score_run  # noqa: E402


CATEGORIES = {"math": 40, "coherence": 35, "finishing": 15, "absurdity": 10}


def make_rubric():
    return {
        "fixture": "synthetic-fixture",
        "version": "synthetic-v1",
        "category_weights": dict(CATEGORIES),
        "false_positive_penalty": {"per_refuted_claim": 2, "cap": 10},
        "items": [
            {
                "id": "math-item",
                "category": "math",
                "location": "synthetic R1",
                "expected_claim": "synthetic arithmetic issue",
                "required_evidence": "quote and recomputation",
                "points": 40,
                "acceptable_variants": [],
                "partial_credit": [{"key": "correct-location-only", "points": 20, "criteria": "location is right but arithmetic is incomplete"}],
            },
            {
                "id": "coherence-item",
                "category": "coherence",
                "location": "synthetic notes",
                "expected_claim": "synthetic cross-reference issue",
                "required_evidence": "quote both conflicting statements",
                "points": 35,
                "acceptable_variants": [],
                "partial_credit": [],
            },
            {
                "id": "finishing-item",
                "category": "finishing",
                "location": "synthetic finish",
                "expected_claim": "synthetic finishing issue",
                "required_evidence": "quote the directive",
                "points": 15,
                "acceptable_variants": [],
                "partial_credit": [],
            },
            {
                "id": "absurdity-item",
                "category": "absurdity",
                "location": "synthetic directive",
                "expected_claim": "synthetic impossible directive",
                "required_evidence": "quote and explain contradiction",
                "points": 10,
                "acceptable_variants": [],
                "partial_credit": [],
            },
        ],
    }


def make_solver():
    return {"fixture": "synthetic-fixture", "defects": [{"id": "D1"}, {"id": "D2"}]}


def make_adjudication():
    return {
        "fixture": "synthetic-fixture",
        "human_approved": True,
        "reviewer": "test-reviewer",
        "claims": [
            {"claim_id": "D1", "rubric_item_id": "math-item", "judgment": "full", "partial_credit_key": None},
            {"claim_id": "D2", "rubric_item_id": None, "judgment": "refuted", "partial_credit_key": None},
        ],
    }


class ScoreRunTests(unittest.TestCase):
    def test_full_credit_and_capped_false_positive_penalty(self):
        result = score_run(make_rubric(), make_solver(), make_adjudication())
        self.assertEqual(result["raw_points"], 40)
        self.assertEqual(result["false_positive_penalty"], 2)
        self.assertEqual(result["score"], 38)
        self.assertEqual(result["refuted_claim_count"], 1)
        self.assertEqual(result["failure_taxonomy"], {"math": 0, "coherence": 1, "finishing": 1, "absurdity": 1, "format": 0})
        self.assertEqual(result["missed_item_ids"], ["coherence-item", "finishing-item", "absurdity-item"])

    def test_partial_credit_uses_rubric_value(self):
        adjudication = make_adjudication()
        adjudication["claims"][0].update({"judgment": "partial", "partial_credit_key": "correct-location-only"})
        result = score_run(make_rubric(), make_solver(), adjudication)
        self.assertEqual(result["raw_points"], 20)
        self.assertEqual(result["score"], 18)
        self.assertIn("math-item", result["undercredited_item_ids"])

    def test_format_failure_is_zero_and_counts_all_items_as_uncredited(self):
        result = score_format_failure(make_rubric())
        self.assertEqual(result["score"], 0)
        self.assertTrue(result["format_failure"])
        self.assertEqual(result["failure_taxonomy"], {"math": 1, "coherence": 1, "finishing": 1, "absurdity": 1, "format": 1})

    def test_unreviewed_adjudication_is_rejected(self):
        adjudication = make_adjudication()
        adjudication["human_approved"] = False
        with self.assertRaisesRegex(EvaluationError, "human-approved"):
            score_run(make_rubric(), make_solver(), adjudication)

    def test_claim_ids_must_match_solver(self):
        adjudication = make_adjudication()
        adjudication["claims"].pop()
        with self.assertRaisesRegex(EvaluationError, "exactly match"):
            score_run(make_rubric(), make_solver(), adjudication)

    def test_one_rubric_item_cannot_be_double_credited(self):
        solver = {"fixture": "synthetic-fixture", "defects": [{"id": "D1"}, {"id": "D2"}]}
        adjudication = make_adjudication()
        adjudication["claims"][1].update({"rubric_item_id": "math-item", "judgment": "full"})
        with self.assertRaisesRegex(EvaluationError, "mapped more than once"):
            score_run(make_rubric(), solver, adjudication)

    def test_item_and_category_points_must_sum_to_one_hundred(self):
        rubric = make_rubric()
        rubric["items"][0]["points"] = 39
        with self.assertRaisesRegex(EvaluationError, "sum to 100"):
            score_run(rubric, make_solver(), make_adjudication())

    def test_penalty_is_capped(self):
        solver = {"fixture": "synthetic-fixture", "defects": [{"id": f"D{i}"} for i in range(1, 8)]}
        adjudication = {
            "fixture": "synthetic-fixture",
            "human_approved": True,
            "reviewer": "test-reviewer",
            "claims": [
                {"claim_id": f"D{i}", "rubric_item_id": None, "judgment": "refuted", "partial_credit_key": None}
                for i in range(1, 8)
            ],
        }
        result = score_run(make_rubric(), solver, adjudication)
        self.assertEqual(result["false_positive_penalty"], 10)
        self.assertEqual(result["score"], 0)


if __name__ == "__main__":
    unittest.main()
