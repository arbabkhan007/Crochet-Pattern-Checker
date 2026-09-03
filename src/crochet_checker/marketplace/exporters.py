"""Marketplace listing generators."""
from typing import Optional
from pydantic import BaseModel

class MarketplaceListing(BaseModel):
    """A marketplace listing."""
    title: str = ""
    description: str = ""
    tags: list[str] = []
    price: float = 0.0
    category: str = ""

class EtsyListingGenerator:
    """Generate Etsy listings."""
    
    def generate_listing(self, pattern) -> MarketplaceListing:
        """Generate an Etsy listing from a pattern."""
        title = f"Amigurumi - {pattern.metadata.title or 'Pattern'}"
        description = f"Beautiful crochet pattern for {pattern.metadata.title or 'amigurumi'}."
        tags = ["amigurumi", "crochet", "pattern", "pdf", "download"]
        price = 5.99
        
        return MarketplaceListing(
            title=title[:140],
            description=description,
            tags=tags[:13],
            price=price,
            category="Craft Supplies & Tools"
        )

class RavelryExportGenerator:
    """Generate Ravelry exports."""
    
    def generate_export(self, pattern) -> dict:
        """Generate a Ravelry export from a pattern."""
        return {
            "pattern_name": pattern.metadata.title or "Pattern",
            "pattern_author": "Designer",
            "category": "Toys and Amigurumi",
            "yarn_weight": "Worsted (9 wpi)",
            "hook_size": "3.5 mm",
        }
