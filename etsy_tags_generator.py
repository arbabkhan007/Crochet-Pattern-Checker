"""
Etsy Tags Generator - Generate optimized Etsy tags for patterns
"""

class EtsyTagsGenerator:
    def __init__(self):
        self.tag_categories = {
            "item_type": ["crochet pattern", "amigurumi", "blanket", "hat"],
            "skill_level": ["beginner crochet", "easy pattern", "advanced"],
            "recipient": ["baby gift", "gift for her", "kids toy"],
        }
    
    def generate_tags(self, pattern_info: dict) -> list:
        tags = []
        item_type = pattern_info.get("type", "crochet pattern")
        tags.append(item_type)
        tags.append("pdf pattern")
        tags.append("digital download")
        tags.append("handmade")
        tags.append("diy crochet")
        return tags[:13]
    
    def generate_listing_title(self, pattern_name: str, tags: list) -> str:
        title = f"{pattern_name} Crochet Pattern"
        if "pdf" in " ".join(tags).lower():
            title += " - PDF Digital Download"
        return title

if __name__ == "__main__":
    print("🏷️ Etsy Tags Generator")
    print("=" * 60)
    generator = EtsyTagsGenerator()
    tags = generator.generate_tags({"type": "amigurumi pattern"})
    print(f"\nGenerated {len(tags)} tags:")
    for tag in tags:
        print(f"  • {tag}")
    title = generator.generate_listing_title("Cute Bunny", tags)
    print(f"\nListing Title: {title}")
    print("\n✨ Etsy Tags Generator complete!")
