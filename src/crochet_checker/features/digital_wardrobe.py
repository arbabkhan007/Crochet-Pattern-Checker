"""
Digital Wardrobe - Catalog and manage your handmade crochet clothing & accessories
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class WardrobeItem:
    """A handmade wardrobe item"""
    id: str
    name: str
    category: str  # top, bottom, dress, accessory, hat, scarf, bag, blanket, other
    color: str = ""
    yarn_used: str = ""
    yarn_amount: str = ""
    hook_size: str = ""
    pattern_name: str = ""
    date_completed: str = ""
    photo: str = ""
    notes: str = ""
    times_worn: int = 0
    cost: float = 0
    hours_made: float = 0
    rating: int = 0  # 1-5
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @property
    def cost_per_wear(self) -> Optional[float]:
        if self.times_worn > 0:
            return round(self.cost / self.times_worn, 2)
        return None


class DigitalWardrobe:
    """
    Catalog and manage handmade wardrobe items
    
    Features:
    - Item catalog with photos
    - Cost per wear calculator
    - Outfit planning
    - Seasonal organization
    - Wear tracking
    - Yarn usage statistics
    - Wardrobe value calculator
    """
    
    CATEGORIES = {
        "top": {"emoji": "👕", "name": "Tops & Sweaters"},
        "bottom": {"emoji": "👖", "name": "Bottoms & Skirts"},
        "dress": {"emoji": "👗", "name": "Dresses"},
        "hat": {"emoji": "🧢", "name": "Hats & Beanies"},
        "scarf": {"emoji": "🧣", "name": "Scarves & Cowls"},
        "bag": {"emoji": "👜", "name": "Bags & Purses"},
        "blanket": {"emoji": "🛏️", "name": "Blankets & Throws"},
        "accessory": {"emoji": "💍", "name": "Accessories"},
        "amigurumi": {"emoji": "🧸", "name": "Amigurumi & Toys"},
        "home": {"emoji": "🏠", "name": "Home Items"},
        "other": {"emoji": "✨", "name": "Other"},
    }
    
    SEASONS = ["spring", "summer", "fall", "winter", "all-season"]
    
    def __init__(self, storage_path: str = "digital_wardrobe.json"):
        self.storage_path = Path(storage_path)
        self.items: Dict[str, WardrobeItem] = {}
        self._next_id = 1
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for k, v in data.get("items", {}).items():
                    self.items[k] = WardrobeItem(**v)
                self._next_id = data.get("next_id", 1)
            except Exception:
                pass
    
    def save(self):
        data = {
            "items": {k: v.to_dict() for k, v in self.items.items()},
            "next_id": self._next_id,
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def add_item(self, name: str, category: str, **kwargs) -> str:
        """Add a new wardrobe item"""
        item_id = f"WD{self._next_id:04d}"
        self._next_id += 1
        
        item = WardrobeItem(id=item_id, name=name, category=category, **kwargs)
        self.items[item_id] = item
        self.save()
        return item_id
    
    def log_wear(self, item_id: str) -> Dict:
        """Log wearing an item"""
        item = self.items.get(item_id)
        if not item:
            return {"error": "Item not found"}
        
        item.times_worn += 1
        self.save()
        
        cpw = item.cost_per_wear
        return {
            "item": item.name,
            "times_worn": item.times_worn,
            "cost_per_wear": f"${cpw}" if cpw else "N/A",
            "message": f"Wore {item.name}! ({item.times_worn}x total)"
        }
    
    def get_wardrobe_stats(self) -> Dict:
        """Get wardrobe statistics"""
        items = list(self.items.values())
        
        total_items = len(items)
        total_cost = sum(i.cost for i in items)
        total_hours = sum(i.hours_made for i in items)
        total_wears = sum(i.times_worn for i in items)
        
        # By category
        by_category = {}
        for item in items:
            cat = item.category
            if cat not in by_category:
                by_category[cat] = {"count": 0, "cost": 0, "wears": 0}
            by_category[cat]["count"] += 1
            by_category[cat]["cost"] += item.cost
            by_category[cat]["wears"] += item.times_worn
        
        # Most worn
        most_worn = sorted(items, key=lambda i: i.times_worn, reverse=True)[:5]
        
        # Best value (lowest cost per wear)
        worn_items = [i for i in items if i.times_worn > 0]
        best_value = sorted(worn_items, key=lambda i: i.cost / i.times_worn if i.times_worn > 0 else 999)[:5]
        
        # Average ratings
        rated_items = [i for i in items if i.rating > 0]
        avg_rating = sum(i.rating for i in rated_items) / max(1, len(rated_items))
        
        return {
            "total_items": total_items,
            "total_value": round(total_cost, 2),
            "total_hours": round(total_hours, 1),
            "total_wears": total_wears,
            "avg_cost_per_item": round(total_cost / max(1, total_items), 2),
            "by_category": by_category,
            "most_worn": [{"name": i.name, "wears": i.times_worn, "cpw": i.cost_per_wear} for i in most_worn],
            "best_value": [{"name": i.name, "cpw": i.cost_per_wear, "cost": i.cost} for i in best_value],
            "avg_rating": round(avg_rating, 1) if rated_items else 0,
            "items_by_season": {s: len([i for i in items if s in i.tags]) for s in self.SEASONS},
        }
    
    def plan_outfit(self, occasion: str = "", weather: str = "") -> Dict:
        """Suggest outfit combinations"""
        items = list(self.items.values())
        
        # Filter by occasion
        if occasion:
            occasion_map = {
                "casual": ["top", "bottom", "accessory"],
                "formal": ["dress", "top", "accessory"],
                "outdoor": ["hat", "scarf", "accessory"],
                "cozy": ["blanket", "scarf", "hat"],
            }
            relevant_cats = occasion_map.get(occasion, [])
            items = [i for i in items if i.category in relevant_cats]
        
        # Sort by most worn (proven favorites)
        suggestions = sorted(items, key=lambda i: i.times_worn, reverse=True)
        
        return {
            "occasion": occasion,
            "weather": weather,
            "suggestions": [
                {"name": i.name, "category": i.category, "color": i.color, "wears": i.times_worn}
                for i in suggestions[:5]
            ],
        }
    
    def get_yarn_usage(self) -> Dict:
        """Analyze yarn usage"""
        yarn_stats = {}
        
        for item in self.items.values():
            if item.yarn_used:
                yarn = item.yarn_used
                if yarn not in yarn_stats:
                    yarn_stats[yarn] = {"items": 0, "total_amount": "", "categories": set()}
                yarn_stats[yarn]["items"] += 1
                yarn_stats[yarn]["categories"].add(item.category)
        
        return {
            "yarns_used": len(yarn_stats),
            "details": {k: {"items": v["items"], "categories": list(v["categories"])} for k, v in yarn_stats.items()},
            "most_used_yarn": max(yarn_stats.items(), key=lambda x: x[1]["items"])[0] if yarn_stats else "None",
        }
    
    def generate_catalog_html(self) -> str:
        """Generate a visual HTML catalog"""
        items = list(self.items.values())
        
        cards = ""
        for item in items:
            cat_info = self.CATEGORIES.get(item.category, self.CATEGORIES["other"])
            cards += f"""
            <div class="card">
                <div class="cat-icon">{cat_info['emoji']}</div>
                <h3>{item.name}</h3>
                <p class="cat">{cat_info['name']}</p>
                <p class="color" style="background:{item.color or '#ccc'}">{'&nbsp;' if item.color else ''}</p>
                <div class="stats">
                    <span>👁 {item.times_worn}x worn</span>
                    <span>💰 ${item.cost:.0f}</span>
                    {'<span>⭐ ' + str(item.rating) + '/5</span>' if item.rating else ''}
                </div>
            </div>"""
        
        return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Digital Wardrobe</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
h1 {{ text-align: center; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; max-width: 1000px; margin: 20px auto; }}
.card {{ background: #16213e; border-radius: 12px; padding: 16px; text-align: center; border: 1px solid #0f3460; }}
.cat-icon {{ font-size: 2.5em; }}
h3 {{ margin: 8px 0 4px; }}
.cat {{ color: #888; font-size: 0.85em; }}
.color {{ width: 30px; height: 30px; border-radius: 50%; margin: 8px auto; border: 2px solid #333; }}
.stats {{ display: flex; justify-content: center; gap: 12px; font-size: 0.8em; margin-top: 10px; }}
</style></head>
<body>
<h1>👗 My Digital Wardrobe</h1>
<p style="text-align:center">{len(items)} handmade items</p>
<div class="grid">{cards}</div>
</body></html>'''


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  DIGITAL WARDROBE - DEMONSTRATION")
    print("=" * 60)
    
    wardrobe = DigitalWardrobe(storage_path="/tmp/demo_wardrobe.json")
    
    # Add items
    wardrobe.add_item("Granny Square Sweater", "top",
                     color="#FF6347", yarn_used="Red Heart Super Saver",
                     cost=25, hours_made=20, times_worn=15, rating=5)
    
    wardrobe.add_item("Cozy Beanie", "hat",
                     color="#4169E1", yarn_used="Wool Blend",
                     cost=8, hours_made=3, times_worn=30, rating=4)
    
    wardrobe.add_item("Market Bag", "bag",
                     color="#228B22", yarn_used="Cotton Yarn",
                     cost=5, hours_made=4, times_worn=50, rating=5)
    
    wardrobe.add_item("Infinity Scarf", "scarf",
                     color="#DDA0DD", yarn_used="Chunky Acrylic",
                     cost=12, hours_made=6, times_worn=20, rating=4)
    
    print(f"✅ Added 4 wardrobe items")
    
    # Log wear
    result = wardrobe.log_wear("WD0003")  # Market Bag
    print(f"\n{result['message']}")
    print(f"  Cost per wear: {result['cost_per_wear']}")
    
    # Stats
    stats = wardrobe.get_wardrobe_stats()
    print(f"\n📊 Wardrobe Stats:")
    print(f"  Total Items: {stats['total_items']}")
    print(f"  Total Value: ${stats['total_value']}")
    print(f"  Total Hours: {stats['total_hours']}h")
    print(f"  Total Wears: {stats['total_wears']}")
    print(f"  Avg Rating: {stats['avg_rating']}/5")
    
    print(f"\n👑 Most Worn:")
    for item in stats['most_worn'][:3]:
        print(f"  • {item['name']} - {item['wears']}x worn (${item['cpw']}/wear)")
    
    print(f"\n💰 Best Value (lowest cost per wear):")
    for item in stats['best_value'][:3]:
        print(f"  • {item['name']} - ${item['cpw']}/wear")
    
    # Yarn usage
    yarn = wardrobe.get_yarn_usage()
    print(f"\n🧶 Yarn Usage: {yarn['yarns_used']} different yarns")
    print(f"  Most used: {yarn['most_used_yarn']}")
    
    # Outfit planning
    outfit = wardrobe.plan_outfit(occasion="casual")
    print(f"\n👗 Casual Outfit Suggestions:")
    for s in outfit['suggestions'][:3]:
        print(f"  • {s['name']} ({s['category']})")
    
    # HTML catalog
    html = wardrobe.generate_catalog_html()
    print(f"\n✅ Visual catalog: {len(html)} chars")
    
    # Cleanup
    if os.path.exists("/tmp/demo_wardrobe.json"):
        os.remove("/tmp/demo_wardrobe.json")
    
    print(f"\n  Digital Wardrobe Complete! 👗")
