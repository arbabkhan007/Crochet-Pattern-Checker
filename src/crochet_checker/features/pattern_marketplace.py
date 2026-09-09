"""
Pattern Marketplace - Buy, sell, and discover crochet patterns
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class MarketplaceListing:
    """A pattern listing on the marketplace"""
    id: str
    title: str
    designer: str
    description: str = ""
    category: str = "amigurumi"
    difficulty: str = "Beginner"
    price: float = 0  # 0 = free
    currency: str = "USD"
    
    # Pattern details
    yarn_weight: str = "Worsted"
    hook_size: str = "5.0mm"
    yardage: int = 0
    finished_size: str = ""
    pattern_format: str = "PDF"
    page_count: int = 0
    
    # Media
    images: List[str] = field(default_factory=list)
    video_url: str = ""
    
    # Stats
    downloads: int = 0
    favorites: int = 0
    reviews: List[Dict] = field(default_factory=list)
    rating: float = 0
    rating_count: int = 0
    
    # Status
    is_published: bool = False
    is_free: bool = True
    created_at: str = ""
    updated_at: str = ""
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.is_free = self.price <= 0
    
    @property
    def average_rating(self) -> float:
        if not self.reviews:
            return 0
        return sum(r.get("rating", 0) for r in self.reviews) / len(self.reviews)
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data["average_rating"] = self.average_rating
        return data


class PatternMarketplace:
    """
    Pattern marketplace for buying and selling patterns
    
    Features:
    - List patterns for sale or free
    - Search and discover patterns
    - Rating and review system
    - Category browsing
    - Trending patterns
    - Designer profiles
    - Revenue tracking
    """
    
    CATEGORIES = [
        "amigurumi", "blankets", "hats", "scarves", "clothing",
        "bags", "home_decor", "baby", "toys", "accessories",
        "holiday", "flowers", "food", "granny_squares", "other"
    ]
    
    DIFFICULTY_LEVELS = ["Beginner", "Advanced Beginner", "Intermediate", "Advanced", "Expert"]
    
    TRENDING_TAGS = [
        "cottagecore", "sustainable", "modern", "vintage", 
        "kawaii", "boho", "minimalist", "colorwork", "texture",
        "quick_make", "scrappy", "gift_idea", "baby_shower"
    ]
    
    def __init__(self, storage_path: str = "marketplace.json"):
        self.storage_path = Path(storage_path)
        self.listings: Dict[str, MarketplaceListing] = {}
        self._next_id = 1
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for k, v in data.get("listings", {}).items():
                    self.listings[k] = MarketplaceListing(**v)
                self._next_id = data.get("next_id", 1)
            except Exception:
                pass
    
    def save(self):
        data = {
            "listings": {k: v.to_dict() for k, v in self.listings.items()},
            "next_id": self._next_id,
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def create_listing(self, title: str, designer: str, 
                      price: float = 0, category: str = "amigurumi",
                      **kwargs) -> str:
        """Create a new marketplace listing"""
        lid = f"PAT{self._next_id:05d}"
        self._next_id += 1
        
        listing = MarketplaceListing(
            id=lid,
            title=title,
            designer=designer,
            price=price,
            category=category,
            **kwargs
        )
        self.listings[lid] = listing
        self.save()
        return lid
    
    def search(self, query: str = "", category: str = "", 
              difficulty: str = "", max_price: float = None,
              is_free: bool = None, sort_by: str = "popular") -> List[MarketplaceListing]:
        """Search marketplace"""
        results = []
        query_lower = query.lower()
        
        for listing in self.listings.values():
            if not listing.is_published:
                continue
            
            if query and query_lower not in f"{listing.title} {listing.description} {' '.join(listing.tags)}".lower():
                continue
            
            if category and listing.category != category:
                continue
            
            if difficulty and listing.difficulty != difficulty:
                continue
            
            if max_price is not None and listing.price > max_price:
                continue
            
            if is_free is not None and listing.is_free != is_free:
                continue
            
            results.append(listing)
        
        # Sort
        if sort_by == "popular":
            results.sort(key=lambda l: l.downloads + l.favorites, reverse=True)
        elif sort_by == "newest":
            results.sort(key=lambda l: l.created_at, reverse=True)
        elif sort_by == "rating":
            results.sort(key=lambda l: l.average_rating, reverse=True)
        elif sort_by == "price_low":
            results.sort(key=lambda l: l.price)
        elif sort_by == "price_high":
            results.sort(key=lambda l: l.price, reverse=True)
        
        return results
    
    def get_trending(self, limit: int = 10) -> List[MarketplaceListing]:
        """Get trending patterns"""
        published = [l for l in self.listings.values() if l.is_published]
        
        # Score by recent activity
        scored = []
        for l in published:
            score = l.downloads * 3 + l.favorites * 2 + l.rating_count * 5
            scored.append((l, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [l for l, _ in scored[:limit]]
    
    def add_review(self, listing_id: str, reviewer: str, 
                  rating: int, text: str = "") -> bool:
        """Add a review to a listing"""
        if listing_id not in self.listings:
            return False
        
        review = {
            "reviewer": reviewer,
            "rating": rating,
            "text": text,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        
        self.listings[listing_id].reviews.append(review)
        self.listings[listing_id].rating_count += 1
        self.listings[listing_id].rating = self.listings[listing_id].average_rating
        self.save()
        return True
    
    def record_download(self, listing_id: str) -> bool:
        """Record a pattern download"""
        if listing_id not in self.listings:
            return False
        self.listings[listing_id].downloads += 1
        self.save()
        return True
    
    def get_designer_catalog(self, designer: str) -> List[MarketplaceListing]:
        """Get all patterns by a designer"""
        return [l for l in self.listings.values() 
                if l.designer == designer and l.is_published]
    
    def get_revenue_report(self, designer: str) -> Dict:
        """Get revenue report for a designer"""
        patterns = self.get_designer_catalog(designer)
        
        total_revenue = sum(l.price * l.downloads for l in patterns)
        total_downloads = sum(l.downloads for l in patterns)
        free_downloads = sum(l.downloads for l in patterns if l.is_free)
        paid_downloads = sum(l.downloads for l in patterns if not l.is_free)
        
        return {
            "designer": designer,
            "total_patterns": len(patterns),
            "total_revenue": round(total_revenue, 2),
            "total_downloads": total_downloads,
            "free_downloads": free_downloads,
            "paid_downloads": paid_downloads,
            "avg_rating": round(sum(l.average_rating for l in patterns) / max(1, len(patterns)), 1),
            "top_pattern": max(patterns, key=lambda l: l.downloads).title if patterns else "N/A",
        }
    
    def generate_storefront_html(self, designer: str = None) -> str:
        """Generate a storefront HTML page"""
        if designer:
            listings = self.get_designer_catalog(designer)
            title = f"{designer}'s Pattern Shop"
        else:
            listings = [l for l in self.listings.values() if l.is_published]
            title = "Crochet Pattern Marketplace"
        
        listings_html = ""
        for l in listings:
            price_display = "FREE" if l.is_free else f"${l.price:.2f}"
            stars = "⭐" * int(l.average_rating) if l.average_rating > 0 else ""
            
            listings_html += f'''
            <div class="listing">
                <div class="listing-image">🧶</div>
                <div class="listing-info">
                    <h3>{l.title}</h3>
                    <p class="designer">by {l.designer}</p>
                    <p class="details">{l.difficulty} | {l.category.replace('_', ' ').title()} | {l.yarn_weight}</p>
                    <div class="stats">
                        <span>{stars} {l.average_rating:.1f}</span>
                        <span>⬇ {l.downloads}</span>
                        <span>❤ {l.favorites}</span>
                    </div>
                    <div class="price">{price_display}</div>
                </div>
            </div>'''
        
        return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; max-width: 1200px; margin: 0 auto; }}
h1 {{ color: #4ECCA3; text-align: center; margin: 30px 0; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
.listing {{ background: #16213e; border-radius: 12px; overflow: hidden; transition: transform 0.2s; cursor: pointer; }}
.listing:hover {{ transform: translateY(-5px); }}
.listing-image {{ height: 200px; background: linear-gradient(135deg, #0f3460, #1a1a2e); display: flex; align-items: center; justify-content: center; font-size: 4em; }}
.listing-info {{ padding: 15px; }}
.listing-info h3 {{ color: #4ECCA3; margin: 0 0 5px; }}
.designer {{ color: #888; font-size: 0.9em; margin: 5px 0; }}
.details {{ color: #aaa; font-size: 0.85em; }}
.stats {{ display: flex; gap: 15px; margin: 10px 0; color: #888; font-size: 0.85em; }}
.price {{ font-size: 1.3em; font-weight: bold; color: #4ECCA3; }}
.filters {{ text-align: center; margin: 20px 0; }}
.filter-btn {{ padding: 8px 16px; margin: 5px; border: 1px solid #4ECCA3; border-radius: 20px; background: transparent; color: #4ECCA3; cursor: pointer; }}
.filter-btn:hover, .filter-btn.active {{ background: #4ECCA3; color: #1a1a2e; }}
</style></head>
<body>
<h1>{title}</h1>
<div class="filters">
    <button class="filter-btn active">All</button>
    <button class="filter-btn">Free</button>
    <button class="filter-btn">Beginner</button>
    <button class="filter-btn">Amigurumi</button>
    <button class="filter-btn">Blankets</button>
    <button class="filter-btn">Trending</button>
</div>
<div class="grid">{listings_html}</div>
</body></html>'''


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  PATTERN MARKETPLACE - DEMONSTRATION")
    print("=" * 60)
    
    market = PatternMarketplace(storage_path="/tmp/demo_market.json")
    
    # Create listings
    l1 = market.create_listing("Cute Bunny Amigurumi", "CozyStitches", 
                              price=4.99, category="amigurumi",
                              difficulty="Beginner", yarn_weight="DK",
                              tags=["cute", "baby", "gift_idea"])
    market.listings[l1].is_published = True
    market.listings[l1].downloads = 150
    market.listings[l1].favorites = 45
    
    l2 = market.create_listing("Granny Square Blanket", "CozyStitches",
                              price=0, category="blankets",
                              difficulty="Beginner", tags=["classic", "quick_make"])
    market.listings[l2].is_published = True
    market.listings[l2].downloads = 500
    market.listings[l2].favorites = 120
    
    l3 = market.create_listing("Cable Knit Hat", "YarnMaster",
                              price=3.99, category="hats",
                              difficulty="Intermediate", tags=["winter", "texture"])
    market.listings[l3].is_published = True
    market.listings[l3].downloads = 75
    
    # Add reviews
    market.add_review(l1, "Sarah_K", 5, "Adorable pattern! So easy to follow!")
    market.add_review(l1, "CrochetFan", 4, "Love it! Made 3 already.")
    market.add_review(l2, "GrannyQueen", 5, "Classic and beautiful!")
    
    # Search
    print("\n🔍 Search: 'amigurumi'")
    results = market.search(query="amigurumi")
    for r in results:
        print(f"  • {r.title} by {r.designer} - {'FREE' if r.is_free else '$' + str(r.price)} ({r.downloads} downloads)")
    
    # Trending
    print("\n🔥 Trending:")
    for t in market.get_trending(3):
        print(f"  • {t.title} - ⬇{t.downloads} ❤{t.favorites}")
    
    # Revenue
    print("\n💰 Revenue Report (CozyStitches):")
    rev = market.get_revenue_report("CozyStitches")
    for key, val in rev.items():
        print(f"  {key}: {val}")
    
    # Storefront
    html = market.generate_storefront_html()
    print(f"\n✅ Storefront HTML: {len(html)} chars")
    
    # Cleanup
    if os.path.exists("/tmp/demo_market.json"):
        os.remove("/tmp/demo_market.json")
    
    print(f"\n  Pattern Marketplace Complete! 🛒")
