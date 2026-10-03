"""
Etsy SEO Analyzer - Analyze Etsy listing SEO
"""

class EtsySEOAnalyzer:
    def __init__(self):
        self.seo_factors = {
            "title": {"weight": 30, "optimal_length": (50, 140)},
            "tags": {"weight": 25, "optimal_count": 13},
            "description": {"weight": 20, "optimal_length": (500, 2000)},
        }
    
    def analyze_seo(self, listing_data: dict) -> dict:
        scores = {}
        title = listing_data.get("title", "")
        scores["title"] = 100 if 50 <= len(title) <= 140 else 50
        
        tags = listing_data.get("tags", [])
        scores["tags"] = min(100, (len(tags) / 13) * 100)
        
        overall = sum(scores.values()) / len(scores)
        return {
            "scores": scores,
            "overall_score": round(overall, 1),
            "grade": "A+" if overall >= 90 else "B" if overall >= 70 else "C"
        }

if __name__ == "__main__":
    print("🔍 Etsy SEO Analyzer")
    print("=" * 60)
    analyzer = EtsySEOAnalyzer()
    listing = {"title": "Cute Bunny Pattern PDF", "tags": ["crochet"] * 13}
    analysis = analyzer.analyze_seo(listing)
    print(f"\nOverall Score: {analysis['overall_score']}/100")
    print(f"Grade: {analysis['grade']}")
    print("\n✨ Etsy SEO Analyzer complete!")
