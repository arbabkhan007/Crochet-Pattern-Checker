"""Does not invent listing tags."""

class EtsyTagsGenerator:
    def __init__(self):
        self.tag_categories = {}

    def generate_tags(self, pattern_info: dict) -> list:
        given = pattern_info.get("tags") or []
        return list(given)

    def generate_listing_title(self, pattern_name: str, tags: list) -> str:
        return pattern_name

if __name__ == "__main__":
    tags = EtsyTagsGenerator().generate_tags({"type": "amigurumi pattern", "tags": []})
    print("No tags were invented." if not tags else "Used only the given tags.")
