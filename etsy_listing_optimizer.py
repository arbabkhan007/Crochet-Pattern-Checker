"""Does not score a listing."""

class EtsyListingOptimizer:
    def __init__(self):
        self.seo_keywords = {}

    def analyze_listing(self, title: str, description: str, tags: list) -> dict:
        return {
            "title_length": len(title),
            "description_length": len(description),
            "tags_count": len(tags),
            "seo_score": None,
            "note": "No listing score was invented.",
        }

    def generate_optimized_title(self, original_title: str, keywords: list) -> str:
        return original_title

if __name__ == "__main__":
    result = EtsyListingOptimizer().analyze_listing("Bunny Pattern", "Adorable bunny", ["crochet"])
    print(result["note"])
