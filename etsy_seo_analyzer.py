"""Does not grade a listing."""

class EtsySEOAnalyzer:
    def __init__(self):
        self.seo_factors = {}

    def analyze_seo(self, listing_data: dict) -> dict:
        return {
            "scores": {},
            "overall_score": None,
            "grade": None,
            "note": "No SEO score was invented. This is not a grade.",
        }

if __name__ == "__main__":
    result = EtsySEOAnalyzer().analyze_seo({"title": "Cute Bunny Pattern PDF", "tags": ["crochet"]})
    print(result["note"])
