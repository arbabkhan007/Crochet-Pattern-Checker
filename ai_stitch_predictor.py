"""Does not predict a stitch that was not written."""

class AIStitchPredictor:
    def __init__(self):
        self.pattern_rules = {
            "increases": ["inc", "2 sc in next st"],
            "decreases": ["dec", "sc 2 together"],
        }

    def predict_next_stitch(self, current_row: str, pattern_history: list) -> dict:
        return {
            "prediction": None,
            "confidence": None,
            "note": "The next stitch was not predicted. No confidence was invented.",
        }

if __name__ == "__main__":
    result = AIStitchPredictor().predict_next_stitch("sc in next 5 sts", [])
    print(result["note"])
