"""
Crochet Event Planner - Plan meetups, workshops, and craft events
"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path


class CrochetEventPlanner:
    """
    Plan crochet meetups, workshops, and events
    
    Features:
    - Event creation and scheduling
    - RSVP tracking
    - Supply lists
    - Budget planning
    - Venue management
    - Event templates
    """
    
    EVENT_TYPES = {
        "meetup": {
            "name": "Crochet Meetup",
            "emoji": "🧶",
            "typical_size": "5-15",
            "duration": "2-3 hours",
        },
        "workshop": {
            "name": "Workshop/Class",
            "emoji": "📚",
            "typical_size": "8-20",
            "duration": "3-4 hours",
        },
        "stitch_n_sip": {
            "name": "Stitch & Sip",
            "emoji": "🍷",
            "typical_size": "10-25",
            "duration": "2-3 hours",
        },
        "craft_fair": {
            "name": "Craft Fair/Market",
            "emoji": "🏪",
            "typical_size": "50-200",
            "duration": "Full day",
        },
        "charity": {
            "name": "Charity Crochet-Along",
            "emoji": "❤️",
            "typical_size": "10-50",
            "duration": "Varies",
        },
        "retreat": {
            "name": "Crochet Retreat",
            "emoji": "🏕️",
            "typical_size": "15-40",
            "duration": "Weekend",
        },
    }
    
    SUPPLY_TEMPLATES = {
        "meetup": [
            "Yarn samples for show & tell",
            "Name tags",
            "Sign-in sheet",
            "Pattern copies (optional)",
            "Snacks & drinks",
        ],
        "workshop": [
            "Yarn for each participant",
            "Hooks (various sizes)",
            " printed patterns",
            "Scissors",
            "Stitch markers",
            "Whiteboard/markers",
            "Sample finished items",
        ],
        "stitch_n_sip": [
            "Beverages (wine, tea, coffee)",
            "Snacks/cheese board",
            "Starter yarn kits",
            "Simple patterns",
            "Music playlist",
            "Ambient lighting",
        ],
        "craft_fair": [
            "Display table & cloth",
            "Pricing tags",
            "Business cards",
            "Payment processing (Square/Venmo)",
            "Packaging supplies",
            "Change/cash box",
            "Signage",
            "Inventory list",
        ],
    }
    
    def __init__(self, storage_path: str = "crochet_events.json"):
        self.storage_path = Path(storage_path)
        self.data = {
            "events": [],
            "venues": [],
            "templates": [],
        }
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                self.data.update(json.loads(self.storage_path.read_text()))
            except Exception:
                pass
    
    def save(self):
        self.storage_path.write_text(json.dumps(self.data, indent=2))
    
    def create_event(self, name: str, event_type: str, date: str,
                    time: str = "", location: str = "", capacity: int = 20,
                    price: float = 0) -> Dict:
        """Create a new event"""
        event = {
            "id": f"EVT{len(self.data['events']) + 1:04d}",
            "name": name,
            "type": event_type,
            "date": date,
            "time": time,
            "location": location,
            "capacity": capacity,
            "price": price,
            "status": "planning",
            "rsvps": [],
            "supply_list": self.SUPPLY_TEMPLATES.get(event_type, []),
            "budget": {"income": 0, "expenses": 0},
            "notes": "",
        }
        
        self.data["events"].append(event)
        self.save()
        return event
    
    def add_rsvp(self, event_id: str, name: str, email: str = "",
                attending: bool = True) -> Dict:
        """Add an RSVP"""
        event = next((e for e in self.data["events"] if e["id"] == event_id), None)
        if not event:
            return {"error": "Event not found"}
        
        rsvp = {
            "name": name,
            "email": email,
            "attending": attending,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        
        event["rsvps"].append(rsvp)
        
        attending_count = len([r for r in event["rsvps"] if r["attending"]])
        
        self.save()
        
        return {
            "event": event["name"],
            "rsvp_added": name,
            "total_attending": attending_count,
            "capacity": event["capacity"],
            "spots_remaining": event["capacity"] - attending_count,
        }
    
    def add_venue(self, name: str, location: str = "", capacity: int = 0,
                 cost: float = 0, notes: str = "") -> Dict:
        """Add a venue"""
        venue = {
            "id": f"V{len(self.data['venues']) + 1:04d}",
            "name": name,
            "location": location,
            "capacity": capacity,
            "cost": cost,
            "notes": notes,
            "bookings": 0,
        }
        self.data["venues"].append(venue)
        self.save()
        return venue
    
    def calculate_budget(self, event_id: str, ticket_price: float = 0,
                        venue_cost: float = 0, supply_cost: float = 0,
                        expected_attendees: int = 10) -> Dict:
        """Calculate event budget"""
        event = next((e for e in self.data["events"] if e["id"] == event_id), None)
        if not event:
            return {"error": "Event not found"}
        
        price = ticket_price or event.get("price", 0)
        
        income = price * expected_attendees
        expenses = venue_cost + (supply_cost * expected_attendees)
        profit = income - expenses
        
        break_even = 0
        if price > 0 and supply_cost > 0:
            break_even = round(venue_cost / (price - supply_cost)) if price > supply_cost else expected_attendees
        
        return {
            "event": event["name"],
            "income": {
                "ticket_price": price,
                "expected_attendees": expected_attendees,
                "total_income": round(income, 2),
            },
            "expenses": {
                "venue": venue_cost,
                "supplies_per_person": supply_cost,
                "total_supplies": round(supply_cost * expected_attendees, 2),
                "total_expenses": round(expenses, 2),
            },
            "profit": round(profit, 2),
            "break_even_attendees": break_even,
            "profit_per_person": round(profit / max(1, expected_attendees), 2),
        }
    
    def get_upcoming_events(self) -> List[Dict]:
        """Get upcoming events"""
        today = datetime.now().strftime("%Y-%m-%d")
        upcoming = []
        
        for event in self.data["events"]:
            if event["date"] >= today:
                attending = len([r for r in event["rsvps"] if r["attending"]])
                upcoming.append({
                    **event,
                    "attending": attending,
                    "spots_remaining": event["capacity"] - attending,
                })
        
        return sorted(upcoming, key=lambda e: e["date"])
    
    def get_event_checklist(self, event_id: str) -> Dict:
        """Get event planning checklist"""
        event = next((e for e in self.data["events"] if e["id"] == event_id), None)
        if not event:
            return {"error": "Event not found"}
        
        checklist = {
            "4_weeks_before": [
                "Set date and time",
                "Book venue",
                "Create event listing",
                "Start promotion",
            ],
            "2_weeks_before": [
                "Order supplies",
                "Confirm RSVPs",
                "Prepare patterns/materials",
                "Send reminders",
            ],
            "1_week_before": [
                "Final supply check",
                "Confirm venue details",
                "Prepare name tags",
                "Set up payment processing",
            ],
            "day_of": [
                "Arrive 30 min early",
                "Set up displays",
                "Prepare refreshments",
                "Have sign-in sheet ready",
                "Bring extra hooks/yarn for forgetful attendees",
            ],
            "after_event": [
                "Send thank you notes",
                "Share photos (with permission)",
                "Collect feedback",
                "Calculate final budget",
                "Plan next event!",
            ],
        }
        
        return {
            "event": event["name"],
            "type": event["type"],
            "checklist": checklist,
            "supplies_needed": event.get("supply_list", []),
        }
    
    def get_dashboard(self) -> Dict:
        """Get events dashboard"""
        upcoming = self.get_upcoming_events()
        total_events = len(self.data["events"])
        total_rsvps = sum(len(e["rsvps"]) for e in self.data["events"])
        
        return {
            "total_events": total_events,
            "upcoming_count": len(upcoming),
            "total_rsvps": total_rsvps,
            "venues_saved": len(self.data["venues"]),
            "upcoming": upcoming[:5],
            "event_types": {k: v["name"] for k, v in self.EVENT_TYPES.items()},
        }


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  CROCHET EVENT PLANNER - DEMONSTRATION")
    print("=" * 60)
    
    planner = CrochetEventPlanner(storage_path="/tmp/demo_events.json")
    
    # Show event types
    print(f"\n📅 Event Types:")
    for key, info in planner.EVENT_TYPES.items():
        print(f"  {info['emoji']} {info['name']} ({info['typical_size']}, {info['duration']})")
    
    # Create events
    e1 = planner.create_event("Beginner Crochet Workshop", "workshop",
                             (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
                             "2:00 PM", "Community Center", capacity=15, price=25)
    
    e2 = planner.create_event("Stitch & Sip Evening", "stitch_n_sip",
                             (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d"),
                             "7:00 PM", "Local Cafe", capacity=20, price=15)
    
    print(f"\n✅ Created 2 events")
    
    # Add RSVPs
    for name in ["Alice", "Bob", "Carol", "Dave"]:
        planner.add_rsvp(e1["id"], name, f"{name.lower()}@email.com")
    
    for name in ["Eve", "Frank"]:
        planner.add_rsvp(e2["id"], name)
    
    print(f"✅ Added RSVPs")
    
    # Add venue
    venue = planner.add_venue("Community Center", "123 Main St", capacity=30, cost=50)
    print(f"✅ Added venue: {venue['name']}")
    
    # Budget
    print(f"\n💰 Budget for Workshop:")
    budget = planner.calculate_budget(e1["id"], ticket_price=25, venue_cost=50,
                                      supply_cost=5, expected_attendees=15)
    print(f"  Income: ${budget['income']['total_income']}")
    print(f"  Expenses: ${budget['expenses']['total_expenses']}")
    print(f"  Profit: ${budget['profit']}")
    print(f"  Break-even: {budget['break_even_attendees']} attendees")
    
    # Upcoming
    print(f"\n📅 Upcoming Events:")
    upcoming = planner.get_upcoming_events()
    for e in upcoming:
        info = planner.EVENT_TYPES.get(e["type"], {})
        print(f"  {info.get('emoji', '📅')} {e['name']} - {e['date']} ({e['attending']}/{e['capacity']})")
    
    # Checklist
    print(f"\n📋 Event Checklist:")
    check = planner.get_event_checklist(e1["id"])
    for period, tasks in list(check["checklist"].items())[:2]:
        print(f"  {period.replace('_', ' ').title()}:")
        for task in tasks[:3]:
            print(f"    □ {task}")
    
    # Dashboard
    print(f"\n📊 Dashboard:")
    dash = planner.get_dashboard()
    print(f"  Total Events: {dash['total_events']}")
    print(f"  Upcoming: {dash['upcoming_count']}")
    print(f"  Total RSVPs: {dash['total_rsvps']}")
    
    # Cleanup
    if os.path.exists("/tmp/demo_events.json"):
        os.remove("/tmp/demo_events.json")
    
    print(f"\n  Crochet Event Planner Complete! 📅")
