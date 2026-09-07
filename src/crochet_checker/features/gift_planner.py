"""
Gift Planner - Plan handmade gifts with deadlines, ideas, and tracking
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class GiftIdea:
    """A gift idea"""
    name: str
    category: str  # baby, home, wearable, accessory, toy, blanket
    difficulty: str
    estimated_hours: float
    estimated_cost: float
    pattern_name: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class GiftProject:
    """A planned gift"""
    id: str
    recipient: str
    occasion: str
    item_name: str
    deadline: str
    status: str = "planned"  # planned, started, in_progress, finished, wrapped, given
    pattern: str = ""
    colors: List[str] = field(default_factory=list)
    estimated_hours: float = 0
    actual_hours: float = 0
    materials_cost: float = 0
    notes: str = ""
    is_secret: bool = False
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @property
    def days_until_deadline(self) -> Optional[int]:
        if not self.deadline:
            return None
        dl = datetime.strptime(self.deadline, "%Y-%m-%d")
        return (dl - datetime.now()).days


class GiftPlanner:
    """
    Plan and track handmade gifts
    
    Features:
    - Gift idea database
    - Recipient tracking
    - Deadline management
    - Occasion calendar (birthdays, holidays)
    - Budget tracking
    - Secret gift mode
    - Gift history
    """
    
    GIFT_IDEAS = [
        GiftIdea("Amigurumi Bunny", "toy", "Beginner", 4, 8, tags=["baby", "cute"]),
        GiftIdea("Baby Blanket", "baby", "Intermediate", 15, 25, tags=["baby", "shower"]),
        GiftIdea("Cozy Scarf", "wearable", "Beginner", 6, 12, tags=["winter", "unisex"]),
        GiftIdea("Granny Square Bag", "accessory", "Intermediate", 8, 15, tags=["fashion", "colorful"]),
        GiftIdea("Dishcloth Set", "home", "Beginner", 3, 5, tags=["kitchen", "practical"]),
        GiftIdea("Beanie Hat", "wearable", "Beginner", 3, 8, tags=["winter", "quick"]),
        GiftIdea("Lovie/Comforter", "baby", "Advanced Beginner", 5, 12, tags=["baby", "gift"]),
        GiftIdea("Phone Cozy", "accessory", "Beginner", 2, 4, tags=["quick", "practical"]),
        GiftIdea("Table Runner", "home", "Intermediate", 10, 20, tags=["home_decor", "elegant"]),
        GiftIdea("Stuffed Heart", "toy", "Beginner", 2, 3, tags=["valentine", "romantic"]),
        GiftIdea("Market Bag", "accessory", "Intermediate", 6, 10, tags=["eco", "practical"]),
        GiftIdea("Washcloth Set", "home", "Beginner", 4, 6, tags=["kitchen", "spa"]),
    ]
    
    OCCASIONS = {
        "christmas": {"month": 12, "day": 25, "emoji": "🎄"},
        "valentines": {"month": 2, "day": 14, "emoji": "💕"},
        "mothers_day": {"month": 5, "day": None, "emoji": "👩"},  # 2nd Sunday
        "fathers_day": {"month": 6, "day": None, "emoji": "👨"},  # 3rd Sunday
        "birthday": {"month": None, "day": None, "emoji": "🎂"},
        "baby_shower": {"month": None, "day": None, "emoji": "👶"},
        "wedding": {"month": None, "day": None, "emoji": "💒"},
        "housewarming": {"month": None, "day": None, "emoji": "🏠"},
        "graduation": {"month": None, "day": None, "emoji": "🎓"},
        "thank_you": {"month": None, "day": None, "emoji": "🙏"},
    }
    
    def __init__(self, storage_path: str = "gift_planner.json"):
        self.storage_path = Path(storage_path)
        self.gifts: Dict[str, GiftProject] = {}
        self.recipients: Dict[str, Dict] = {}
        self._next_id = 1
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for k, v in data.get("gifts", {}).items():
                    self.gifts[k] = GiftProject(**v)
                self.recipients = data.get("recipients", {})
                self._next_id = data.get("next_id", 1)
            except Exception:
                pass
    
    def save(self):
        data = {
            "gifts": {k: v.to_dict() for k, v in self.gifts.items()},
            "recipients": self.recipients,
            "next_id": self._next_id,
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def add_recipient(self, name: str, relationship: str = "",
                     birthday: str = "", preferences: str = "") -> str:
        """Add a gift recipient"""
        self.recipients[name] = {
            "name": name,
            "relationship": relationship,
            "birthday": birthday,
            "preferences": preferences,
            "gifts_given": 0,
        }
        self.save()
        return name
    
    def plan_gift(self, recipient: str, occasion: str, item_name: str,
                 deadline: str, estimated_hours: float = 0,
                 pattern: str = "", **kwargs) -> str:
        """Plan a new gift"""
        gid = f"GIFT{self._next_id:04d}"
        self._next_id += 1
        
        gift = GiftProject(
            id=gid,
            recipient=recipient,
            occasion=occasion,
            item_name=item_name,
            deadline=deadline,
            estimated_hours=estimated_hours,
            pattern=pattern,
            **kwargs
        )
        
        self.gifts[gid] = gift
        self.save()
        return gid
    
    def get_gift_ideas(self, category: str = "", difficulty: str = "",
                      max_hours: float = None, max_cost: float = None) -> List[GiftIdea]:
        """Get gift ideas filtered by criteria"""
        ideas = self.GIFT_IDEAS.copy()
        
        if category:
            ideas = [i for i in ideas if i.category == category]
        if difficulty:
            ideas = [i for i in ideas if i.difficulty == difficulty]
        if max_hours:
            ideas = [i for i in ideas if i.estimated_hours <= max_hours]
        if max_cost:
            ideas = [i for i in ideas if i.estimated_cost <= max_cost]
        
        return ideas
    
    def get_upcoming_occasions(self, days_ahead: int = 60) -> List[Dict]:
        """Get upcoming occasions"""
        now = datetime.now()
        upcoming = []
        
        # Check fixed dates
        for name, info in self.OCCASIONS.items():
            if info["month"] and info["day"]:
                try:
                    occasion_date = datetime(now.year, info["month"], info["day"])
                    if occasion_date < now:
                        occasion_date = datetime(now.year + 1, info["month"], info["day"])
                    days = (occasion_date - now).days
                    if days <= days_ahead:
                        upcoming.append({
                            "occasion": name,
                            "date": occasion_date.strftime("%Y-%m-%d"),
                            "days_away": days,
                            "emoji": info["emoji"],
                        })
                except ValueError:
                    pass
        
        # Check birthdays
        for name, info in self.recipients.items():
            if info.get("birthday"):
                try:
                    bday = datetime.strptime(info["birthday"], "%m-%d")
                    bday = datetime(now.year, bday.month, bday.day)
                    if bday < now:
                        bday = datetime(now.year + 1, bday.month, bday.day)
                    days = (bday - now).days
                    if days <= days_ahead:
                        upcoming.append({
                            "occasion": f"{name}'s Birthday",
                            "date": bday.strftime("%Y-%m-%d"),
                            "days_away": days,
                            "emoji": "🎂",
                            "recipient": name,
                        })
                except ValueError:
                    pass
        
        return sorted(upcoming, key=lambda x: x["days_away"])
    
    def get_urgent_gifts(self) -> List[Dict]:
        """Get gifts with approaching deadlines"""
        urgent = []
        for gift in self.gifts.values():
            if gift.status in ("given",):
                continue
            days = gift.days_until_deadline
            if days is not None and days <= 14:
                urgent.append({
                    "id": gift.id,
                    "recipient": gift.recipient,
                    "item": gift.item_name,
                    "occasion": gift.occasion,
                    "deadline": gift.deadline,
                    "days_left": days,
                    "status": gift.status,
                    "urgency": "🔴" if days <= 3 else "🟡" if days <= 7 else "🟢",
                })
        return sorted(urgent, key=lambda x: x["days_left"])
    
    def calculate_work_plan(self, gift_id: str, hours_per_day: float = 1.0) -> Dict:
        """Calculate a work plan to finish on time"""
        gift = self.gifts.get(gift_id)
        if not gift:
            return {}
        
        days = gift.days_until_deadline
        if days is None or days <= 0:
            return {"error": "No deadline or deadline passed"}
        
        remaining_hours = gift.estimated_hours - gift.actual_hours
        
        if remaining_hours <= 0:
            return {"status": "complete", "message": "Already done!"}
        
        hours_per_day_needed = remaining_hours / days
        is_feasible = hours_per_day_needed <= hours_per_day * 1.5
        
        # Suggest schedule
        schedule = []
        hours_left = remaining_hours
        for i in range(1, days + 1):
            day_hours = min(hours_per_day, hours_left)
            hours_left -= day_hours
            if day_hours > 0:
                schedule.append({"day": i, "hours": round(day_hours, 1)})
            if hours_left <= 0:
                break
        
        return {
            "days_available": days,
            "hours_remaining": round(remaining_hours, 1),
            "hours_per_day_needed": round(hours_per_day_needed, 1),
            "is_feasible": is_feasible,
            "suggested_daily_hours": round(min(hours_per_day, hours_per_day_needed * 1.2), 1),
            "schedule": schedule[:10],
        }
    
    def get_budget_summary(self) -> Dict:
        """Get gift budget summary"""
        total_cost = sum(g.materials_cost for g in self.gifts.values())
        total_hours = sum(g.actual_hours for g in self.gifts.values())
        completed = sum(1 for g in self.gifts.values() if g.status == "given")
        planned = sum(1 for g in self.gifts.values() if g.status == "planned")
        
        return {
            "total_gifts": len(self.gifts),
            "completed": completed,
            "planned": planned,
            "total_materials_cost": round(total_cost, 2),
            "total_hours": round(total_hours, 1),
            "avg_cost_per_gift": round(total_cost / max(1, len(self.gifts)), 2),
        }
    
    def display_dashboard(self):
        """Display gift planning dashboard"""
        budget = self.get_budget_summary()
        urgent = self.get_urgent_gifts()
        upcoming = self.get_upcoming_occasions(30)
        
        print(f"\n{'=' * 60}")
        print(f"  🎁 GIFT PLANNER DASHBOARD")
        print(f"{'=' * 60}")
        
        print(f"\n  📊 OVERVIEW")
        print(f"  {'─' * 40}")
        print(f"  Total Gifts:    {budget['total_gifts']}")
        print(f"  Completed:      {budget['completed']}")
        print(f"  Planned:        {budget['planned']}")
        print(f"  Materials Cost: ${budget['total_materials_cost']:.2f}")
        print(f"  Total Hours:    {budget['total_hours']}h")
        
        if upcoming:
            print(f"\n  📅 UPCOMING OCCASIONS (30 days)")
            print(f"  {'─' * 40}")
            for occ in upcoming[:5]:
                print(f"  {occ['emoji']} {occ['occasion']:20s} {occ['days_away']} days ({occ['date']})")
        
        if urgent:
            print(f"\n  ⚠️  URGENT GIFTS")
            print(f"  {'─' * 40}")
            for g in urgent:
                print(f"  {g['urgency']} {g['item']} for {g['recipient']} - {g['days_left']} days left")
        
        # Gift ideas
        print(f"\n  💡 QUICK GIFT IDEAS")
        print(f"  {'─' * 40}")
        quick_gifts = [i for i in self.GIFT_IDEAS if i.estimated_hours <= 4]
        for idea in quick_gifts[:5]:
            print(f"  • {idea.name} ({idea.difficulty}, {idea.estimated_hours}h, ${idea.estimated_cost})")


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  GIFT PLANNER - DEMONSTRATION")
    print("=" * 60)
    
    planner = GiftPlanner(storage_path="/tmp/demo_gifts.json")
    
    # Add recipients
    planner.add_recipient("Mom", "mother", "03-15", "Likes pink and flowers")
    planner.add_recipient("Best Friend", "friend", "07-22", "Loves cats")
    print(f"✅ Added 2 recipients")
    
    # Plan gifts
    g1 = planner.plan_gift("Mom", "Birthday", "Granny Square Blanket",
                          (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d"),
                          estimated_hours=15)
    
    g2 = planner.plan_gift("Best Friend", "Christmas", "Cat Amigurumi",
                          (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                          estimated_hours=4)
    
    g3 = planner.plan_gift("Mom", "Christmas", "Cozy Scarf",
                          (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
                          estimated_hours=6)
    
    print(f"✅ Planned 3 gifts")
    
    # Gift ideas
    print(f"\n💡 Gift ideas under 5 hours:")
    for idea in planner.get_gift_ideas(max_hours=5):
        print(f"  • {idea.name} ({idea.difficulty}, {idea.estimated_hours}h)")
    
    # Urgent gifts
    urgent = planner.get_urgent_gifts()
    print(f"\n⚠️  Urgent gifts:")
    for g in urgent:
        print(f"  {g['urgency']} {g['item']} for {g['recipient']} - {g['days_left']} days")
    
    # Work plan
    plan = planner.calculate_work_plan(g1, hours_per_day=1.5)
    print(f"\n📋 Work plan for {g1}:")
    print(f"  Days available: {plan.get('days_available', 0)}")
    print(f"  Hours remaining: {plan.get('hours_remaining', 0)}")
    print(f"  Hours/day needed: {plan.get('hours_per_day_needed', 0)}")
    print(f"  Feasible: {'✅ Yes' if plan.get('is_feasible') else '❌ Tight'}")
    
    # Dashboard
    planner.display_dashboard()
    
    # Cleanup
    if os.path.exists("/tmp/demo_gifts.json"):
        os.remove("/tmp/demo_gifts.json")
    
    print(f"\n  Gift Planner Complete! 🎁")
