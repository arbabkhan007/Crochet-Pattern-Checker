"""
Subscription Box Planner - Plan and manage monthly crochet subscription boxes
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class BoxItem:
    """An item in a subscription box"""
    name: str
    type: str  # pattern, yarn, tool, notion, extra
    quantity: int = 1
    unit_cost: float = 0
    description: str = ""
    supplier: str = ""
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @property
    def total_cost(self) -> float:
        return self.unit_cost * self.quantity


@dataclass
class SubscriptionBox:
    """A subscription box"""
    id: str
    month: str
    theme: str = ""
    items: List[Dict] = field(default_factory=list)
    target_cost: float = 0
    actual_cost: float = 0
    subscriber_count: int = 0
    status: str = "planning"  # planning, sourcing, packed, shipped, delivered
    shipping_date: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SubscriptionBoxPlanner:
    """
    Plan and manage monthly crochet subscription boxes
    
    Features:
    - Monthly box planning
    - Theme selection
    - Item sourcing
    - Cost management
    - Subscriber tracking
    - Shipping logistics
    - Revenue projection
    """
    
    THEMES = {
        "cozy_winter": {
            "name": "Cozy Winter",
            "emoji": "❄️",
            "season": "winter",
            "suggested_items": ["Chunky yarn", "Warm hat pattern", "Stitch markers (snowflake)", "Hot cocoa packet"],
        },
        "spring_garden": {
            "name": "Spring Garden",
            "emoji": "🌸",
            "season": "spring",
            "suggested_items": ["Floral yarn", "Flower pattern", "Floral stitch markers", "Seed packet"],
        },
        "summer_beach": {
            "name": "Summer Beach",
            "emoji": "🏖️",
            "season": "summer",
            "suggested_items": ["Cotton yarn", "Beach bag pattern", "Shell stitch markers", "Sunscreen"],
        },
        "autumn_harvest": {
            "name": "Autumn Harvest",
            "emoji": "🍂",
            "season": "fall",
            "suggested_items": ["Warm-toned yarn", "Pumpkin pattern", "Leaf markers", "Spiced tea"],
        },
        "amigurumi_party": {
            "name": "Amigurumi Party",
            "emoji": "🧸",
            "season": "any",
            "suggested_items": ["Safety eyes", "Stuffing", "Amigurumi pattern", "Embroidery thread"],
        },
        "beginner_basics": {
            "name": "Beginner Basics",
            "emoji": "🌟",
            "season": "any",
            "suggested_items": ["Starter yarn", "Basic hook", "Beginner pattern", "Stitch guide"],
        },
        "luxury_luxe": {
            "name": "Luxury Luxe",
            "emoji": "💎",
            "season": "any",
            "suggested_items": ["Merino yarn", "Bamboo hook", "Designer pattern", "Project bag"],
        },
        "holiday_cheer": {
            "name": "Holiday Cheer",
            "emoji": "🎄",
            "season": "winter",
            "suggested_items": ["Red/green yarn", "Ornament pattern", "Gift tag markers", "Candy cane"],
        },
    }
    
    MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    
    def __init__(self, storage_path: str = "subscription_boxes.json"):
        self.storage_path = Path(storage_path)
        self.boxes: Dict[str, SubscriptionBox] = {}
        self.subscribers: List[Dict] = []
        self._next_id = 1
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for k, v in data.get("boxes", {}).items():
                    self.boxes[k] = SubscriptionBox(**v)
                self.subscribers = data.get("subscribers", [])
                self._next_id = data.get("next_id", 1)
            except Exception:
                pass
    
    def save(self):
        data = {
            "boxes": {k: v.to_dict() for k, v in self.boxes.items()},
            "subscribers": self.subscribers,
            "next_id": self._next_id,
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def create_box(self, month: str, theme: str = "", target_cost: float = 25) -> str:
        """Create a new monthly box"""
        box_id = f"BOX{self._next_id:04d}"
        self._next_id += 1
        
        box = SubscriptionBox(
            id=box_id,
            month=month,
            theme=theme,
            target_cost=target_cost,
        )
        
        self.boxes[box_id] = box
        self.save()
        return box_id
    
    def add_item(self, box_id: str, name: str, item_type: str = "extra",
                quantity: int = 1, unit_cost: float = 0, **kwargs) -> Dict:
        """Add an item to a box"""
        box = self.boxes.get(box_id)
        if not box:
            return {"error": "Box not found"}
        
        item = BoxItem(name=name, type=item_type, quantity=quantity,
                      unit_cost=unit_cost, **kwargs)
        box.items.append(item.to_dict())
        box.actual_cost += item.total_cost
        
        self.save()
        return {"item": item.to_dict(), "running_cost": box.actual_cost}
    
    def plan_monthly_box(self, month: str, theme_key: str = None,
                        subscriber_tier: str = "standard") -> Dict:
        """Plan a complete monthly box"""
        theme = self.THEMES.get(theme_key, self.THEMES["cozy_winter"])
        
        # Pricing tiers
        tiers = {
            "basic": {"price": 19.99, "item_count": 3, "yarn_yards": 100},
            "standard": {"price": 29.99, "item_count": 5, "yarn_yards": 200},
            "premium": {"price": 44.99, "item_count": 7, "yarn_yards": 350},
        }
        tier = tiers.get(subscriber_tier, tiers["standard"])
        
        # Generate box plan
        items = []
        for suggested in theme["suggested_items"]:
            items.append({
                "name": suggested,
                "type": "suggested",
                "estimated_cost": round(tier["price"] / tier["item_count"] * 0.4, 2),
            })
        
        # Cost breakdown
        estimated_item_cost = sum(i["estimated_cost"] for i in items)
        packaging_cost = 3.00
        shipping_cost = 5.00
        total_cost = estimated_item_cost + packaging_cost + shipping_cost
        profit = tier["price"] - total_cost
        
        return {
            "month": month,
            "theme": theme["name"],
            "theme_emoji": theme["emoji"],
            "tier": subscriber_tier,
            "subscriber_price": tier["price"],
            "items": items,
            "cost_breakdown": {
                "items": round(estimated_item_cost, 2),
                "packaging": packaging_cost,
                "shipping": shipping_cost,
                "total": round(total_cost, 2),
            },
            "profit_per_box": round(profit, 2),
            "profit_margin_pct": round(profit / tier["price"] * 100, 1),
        }
    
    def add_subscriber(self, name: str, email: str = "", tier: str = "standard",
                      start_month: str = None) -> Dict:
        """Add a subscriber"""
        subscriber = {
            "name": name,
            "email": email,
            "tier": tier,
            "start_month": start_month or datetime.now().strftime("%B %Y"),
            "status": "active",
            "boxes_received": 0,
        }
        self.subscribers.append(subscriber)
        self.save()
        return subscriber
    
    def get_business_projections(self, subscriber_count: int = None,
                                tier: str = "standard",
                                months: int = 12) -> Dict:
        """Project business revenue"""
        tiers = {
            "basic": 19.99,
            "standard": 29.99,
            "premium": 44.99,
        }
        price = tiers.get(tier, 29.99)
        count = subscriber_count or len([s for s in self.subscribers if s["status"] == "active"])
        
        monthly_revenue = price * count
        monthly_costs = 15 * count  # Average cost per box
        monthly_profit = monthly_revenue - monthly_costs
        
        # Growth assumptions
        growth_rate = 0.10  # 10% monthly growth
        
        projections = []
        cumulative = 0
        subscribers = count
        for m in range(1, months + 1):
            revenue = price * subscribers
            costs = 15 * subscribers
            profit = revenue - costs
            cumulative += profit
            
            projections.append({
                "month": m,
                "subscribers": subscribers,
                "revenue": round(revenue, 2),
                "costs": round(costs, 2),
                "profit": round(profit, 2),
                "cumulative_profit": round(cumulative, 2),
            })
            
            subscribers = int(subscribers * (1 + growth_rate))
        
        return {
            "starting_subscribers": count,
            "tier": tier,
            "price_per_box": price,
            "monthly_revenue": round(monthly_revenue, 2),
            "monthly_profit": round(monthly_profit, 2),
            "yearly_revenue": round(sum(p["revenue"] for p in projections), 2),
            "yearly_profit": round(sum(p["profit"] for p in projections), 2),
            "projections": projections,
        }
    
    def get_box_planning_dashboard(self) -> Dict:
        """Get box planning dashboard"""
        boxes = list(self.boxes.values())
        active_subs = len([s for s in self.subscribers if s["status"] == "active"])
        
        # Upcoming boxes
        now = datetime.now()
        upcoming_months = []
        for i in range(1, 7):
            month_date = now + timedelta(days=30*i)
            month_name = self.MONTH_NAMES[month_date.month - 1]
            year = month_date.year
            upcoming_months.append(f"{month_name} {year}")
        
        # Planned boxes
        planned = [b for b in boxes if b.status == "planning"]
        shipped = [b for b in boxes if b.status in ("shipped", "delivered")]
        
        return {
            "total_boxes": len(boxes),
            "active_subscribers": active_subs,
            "planned_boxes": len(planned),
            "shipped_boxes": len(shipped),
            "upcoming_months": upcoming_months,
            "revenue_per_month": round(active_subs * 29.99, 2),
        }
    
    def suggest_box_contents(self, month: str, budget: float = 25) -> Dict:
        """Suggest box contents for a month"""
        month_num = None
        for i, name in enumerate(self.MONTH_NAMES, 1):
            if name.lower() in month.lower():
                month_num = i
                break
        
        # Match season
        if month_num in (12, 1, 2):
            season = "winter"
        elif month_num in (3, 4, 5):
            season = "spring"
        elif month_num in (6, 7, 8):
            season = "summer"
        else:
            season = "fall"
        
        matching_themes = [t for t, info in self.THEMES.items() if info["season"] == season]
        if not matching_themes:
            matching_themes = list(self.THEMES.keys())
        
        suggestions = []
        for theme_key in matching_themes[:2]:
            theme = self.THEMES[theme_key]
            plan = self.plan_monthly_box(month, theme_key)
            suggestions.append({
                "theme": theme["name"],
                "emoji": theme["emoji"],
                "items": theme["suggested_items"],
                "estimated_cost": plan["cost_breakdown"]["total"],
            })
        
        return {
            "month": month,
            "season": season,
            "budget": budget,
            "suggestions": suggestions,
        }


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  SUBSCRIPTION BOX PLANNER - DEMONSTRATION")
    print("=" * 60)
    
    planner = SubscriptionBoxPlanner(storage_path="/tmp/demo_boxes.json")
    
    # Show themes
    print(f"\n📦 Available Themes:")
    for key, theme in planner.THEMES.items():
        print(f"  {theme['emoji']} {theme['name']} ({theme['season']})")
    
    # Plan a box
    print(f"\n🗓️  Planning January Box:")
    plan = planner.plan_monthly_box("January 2026", "cozy_winter", "standard")
    print(f"  Theme: {plan['theme_emoji']} {plan['theme']}")
    print(f"  Subscriber Price: ${plan['subscriber_price']}")
    print(f"  Items:")
    for item in plan["items"]:
        print(f"    • {item['name']} (${item['estimated_cost']})")
    print(f"  Total Cost: ${plan['cost_breakdown']['total']}")
    print(f"  Profit/Box: ${plan['profit_per_box']} ({plan['profit_margin_pct']}%)")
    
    # Add items to box
    box_id = planner.create_box("January 2026", "Cozy Winter")
    planner.add_item(box_id, "Merino Wool Yarn", "yarn", unit_cost=8.00)
    planner.add_item(box_id, "Chunky Beanie Pattern", "pattern", unit_cost=0)
    planner.add_item(box_id, "Wooden Stitch Markers", "notion", unit_cost=3.50)
    planner.add_item(box_id, "Hot Cocoa Mix", "extra", unit_cost=2.00)
    print(f"\n✅ Created box with 4 items")
    
    # Add subscribers
    for name in ["Alice", "Bob", "Carol", "Dave", "Eve"]:
        planner.add_subscriber(name, tier="standard")
    print(f"✅ Added 5 subscribers")
    
    # Business projections
    print(f"\n💰 Business Projections (12 months):")
    proj = planner.get_business_projections(subscriber_count=50, months=6)
    print(f"  Starting: {proj['starting_subscribers']} subscribers")
    print(f"  Price: ${proj['price_per_box']}/box")
    print(f"  Monthly Revenue: ${proj['monthly_revenue']}")
    print(f"  Monthly Profit: ${proj['monthly_profit']}")
    print(f"  6-Month Revenue: ${proj['yearly_revenue']}")
    print(f"  6-Month Profit: ${proj['yearly_profit']}")
    
    # Growth projections
    print(f"\n📈 Growth:")
    for p in proj["projections"][:4]:
        print(f"  Month {p['month']}: {p['subscribers']} subs → ${p['revenue']} rev → ${p['profit']} profit")
    
    # Suggestions
    print(f"\n🎁 Box Suggestions for March:")
    suggestions = planner.suggest_box_contents("March", budget=25)
    print(f"  Season: {suggestions['season']}")
    for s in suggestions["suggestions"]:
        print(f"  {s['emoji']} {s['theme']}: {', '.join(s['items'][:3])}...")
    
    # Dashboard
    print(f"\n📊 Dashboard:")
    dash = planner.get_box_planning_dashboard()
    print(f"  Active Subscribers: {dash['active_subscribers']}")
    print(f"  Revenue/Month: ${dash['revenue_per_month']}")
    print(f"  Boxes Planned: {dash['planned_boxes']}")
    
    # Cleanup
    if os.path.exists("/tmp/demo_boxes.json"):
        os.remove("/tmp/demo_boxes.json")
    
    print(f"\n  Subscription Box Planner Complete! 📦")
