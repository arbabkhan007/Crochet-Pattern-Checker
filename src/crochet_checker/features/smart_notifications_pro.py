"""
Smart Notifications Pro - Advanced reminder system for WIPs, deadlines, and yarn sales
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


class SmartNotificationsPro:
    """Advanced notification system for crochet projects"""
    
    def __init__(self, data_file: str = "notifications.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
    
    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"notifications": [], "preferences": {"email": False, "desktop": True}}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_wip_reminder(self, project_name: str, last_worked: str, reminder_days: int = 7):
        """Set reminder for work-in-progress"""
        notification = {
            "type": "wip_reminder",
            "project": project_name,
            "last_worked": last_worked,
            "reminder_date": (datetime.strptime(last_worked, "%Y-%m-%d") + 
                            timedelta(days=reminder_days)).strftime("%Y-%m-%d"),
            "message": f"Time to work on {project_name}!",
            "status": "active"
        }
        self.data["notifications"].append(notification)
        self.save_data()
    
    def add_deadline(self, project_name: str, deadline: str, advance_notice: int = 3):
        """Set deadline reminder"""
        notification = {
            "type": "deadline",
            "project": project_name,
            "deadline": deadline,
            "notice_date": (datetime.strptime(deadline, "%Y-%m-%d") - 
                          timedelta(days=advance_notice)).strftime("%Y-%m-%d"),
            "message": f"{project_name} is due in {advance_notice} days!",
            "status": "active"
        }
        self.data["notifications"].append(notification)
        self.save_data()
    
    def add_custom_reminder(self, message: str, date: str, category: str = "general"):
        """Add custom reminder"""
        notification = {
            "type": "custom",
            "category": category,
            "date": date,
            "message": message,
            "status": "active"
        }
        self.data["notifications"].append(notification)
        self.save_data()
    
    def get_upcoming_notifications(self, days_ahead: int = 7) -> List[Dict]:
        """Get notifications for next X days"""
        today = datetime.now()
        future = today + timedelta(days=days_ahead)
        
        upcoming = []
        for notif in self.data["notifications"]:
            if notif["status"] != "active":
                continue
            
            date_str = notif.get("reminder_date") or notif.get("notice_date") or notif.get("date")
            if not date_str:
                continue
            
            notif_date = datetime.strptime(date_str, "%Y-%m-%d")
            if today <= notif_date <= future:
                upcoming.append({
                    **notif,
                    "days_away": (notif_date - today).days
                })
        
        return sorted(upcoming, key=lambda x: x["days_away"])
    
    def check_overdue_wips(self) -> List[Dict]:
        """Find WIPs that haven't been worked on recently"""
        today = datetime.now()
        overdue = []
        
        for notif in self.data["notifications"]:
            if notif["type"] != "wip_reminder" or notif["status"] != "active":
                continue
            
            last_worked = datetime.strptime(notif["last_worked"], "%Y-%m-%d")
            days_since = (today - last_worked).days
            
            if days_since > 14:  # 2 weeks without progress
                overdue.append({
                    "project": notif["project"],
                    "days_since": days_since,
                    "message": f"{notif['project']} hasn't been touched in {days_since} days"
                })
        
        return overdue
    
    def generate_daily_briefing(self) -> str:
        """Generate daily notification summary"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        upcoming = self.get_upcoming_notifications(1)
        overdue = self.check_overdue_wips()
        
        briefing = f"""
╔══════════════════════════════════════════════════════════╗
║         📅 DAILY CROCHET BRIEFING                         ║
║         {today}                                           ║
╚══════════════════════════════════════════════════════════╝
"""
        if upcoming:
            briefing += "\n🔔 TODAY'S NOTIFICATIONS\n"
            briefing += "═" * 59 + "\n"
            for notif in upcoming:
                if notif["days_away"] == 0:
                    briefing += f"  ⚠️  {notif['message']}\n"
                else:
                    briefing += f"  📌 {notif['message']} (in {notif['days_away']} day(s))\n"
        else:
            briefing += "\n✅ No notifications for today!\n"
        
        if overdue:
            briefing += "\n⏰ OVERDUE PROJECTS\n"
            briefing += "═" * 59 + "\n"
            for item in overdue:
                briefing += f"  ❗ {item['message']}\n"
        
        return briefing


if __name__ == "__main__":
    print("🔔 Smart Notifications Pro")
    print("=" * 50)
    
    notifier = SmartNotificationsPro()
    
    # Add sample notifications
    print("\n📝 Adding notifications...")
    today = datetime.now()
    
    notifier.add_wip_reminder("Granny Square Blanket", 
                             (today - timedelta(days=5)).strftime("%Y-%m-%d"), 7)
    notifier.add_deadline("Birthday Gift Scarf", 
                         (today + timedelta(days=10)).strftime("%Y-%m-%d"), 3)
    notifier.add_custom_reminder("Yarn sale at Joann's!", 
                                (today + timedelta(days=2)).strftime("%Y-%m-%d"), "sales")
    
    # Show upcoming
    print("\n📅 Upcoming notifications (7 days):")
    upcoming = notifier.get_upcoming_notifications(7)
    for notif in upcoming:
        print(f"  Day {notif['days_away']}: {notif['message']}")
    
    # Check overdue
    print("\n⏰ Checking for overdue WIPs...")
    overdue = notifier.check_overdue_wips()
    if overdue:
        for item in overdue:
            print(f"  ⚠️  {item['message']}")
    else:
        print("  ✅ All WIPs are current!")
    
    # Daily briefing
    print("\n📋 Daily Briefing:")
    print(notifier.generate_daily_briefing())
    
    print("\n✅ Smart Notifications ready!")
