"""
Ergonomic Assistant - Stretch reminders, posture tips, hand care for crocheters
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class StretchExercise:
    """A stretch exercise"""
    name: str
    target: str  # hands, wrists, neck, shoulders, back
    duration_seconds: int = 30
    description: str = ""
    difficulty: str = "easy"
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ErgonomicAssistant:
    """
    Ergonomic health assistant for crocheters
    
    Features:
    - Stretch reminders based on session length
    - Hand and wrist exercises
    - Posture checks
    - Pain tracking
    - Break scheduling
    - Ergonomic tips
    - Session timer with alerts
    """
    
    STRETCHES = [
        StretchExercise("Finger Spread", "hands", 15,
            "Spread fingers wide, hold 5 seconds, make fist, repeat 5 times"),
        StretchExercise("Wrist Flexor", "wrists", 20,
            "Extend arm, palm up. Pull fingers back gently with other hand. Hold 15s each hand"),
        StretchExercise("Wrist Extensor", "wrists", 20,
            "Extend arm, palm down. Press hand down gently. Hold 15s each hand"),
        StretchExercise("Thumb Circle", "hands", 15,
            "Circle thumb in both directions, 10 times each"),
        StretchExercise("Prayer Stretch", "wrists", 20,
            "Press palms together at chest, lower hands until stretch. Hold 15s"),
        StretchExercise("Neck Roll", "neck", 30,
            "Slowly roll head in circles, 5 each direction"),
        StretchExercise("Shoulder Shrug", "shoulders", 15,
            "Raise shoulders to ears, hold 5s, release. Repeat 5 times"),
        StretchExercise("Cat-Cow", "back", 30,
            "On hands and knees, alternate arching and rounding back 10 times"),
        StretchExercise("Eye Rest", "eyes", 20,
            "Look at something 20 feet away for 20 seconds (20-20-20 rule)"),
        StretchExercise("Hand Massage", "hands", 30,
            "Massage each finger and palm with thumb of other hand"),
        StretchExercise("Wrist Circles", "wrists", 15,
            "Rotate wrists in circles, 10 each direction"),
        StretchExercise("Finger Taps", "hands", 15,
            "Tap each finger to thumb rapidly, 10 times each hand"),
    ]
    
    POSTURE_CHECKS = [
        {"check": "Feet flat on floor", "area": "posture"},
        {"check": "Back supported by chair", "area": "posture"},
        {"check": "Shoulders relaxed, not hunched", "area": "shoulders"},
        {"check": "Elbows at 90 degrees", "area": "arms"},
        {"check": "Work at eye level", "area": "neck"},
        {"check": "Wrists straight, not bent", "area": "wrists"},
        {"check": "Good lighting on work", "area": "eyes"},
    ]
    
    TIPS = [
        "Take a 5-minute break every 30 minutes",
        "Use a larger hook size to reduce hand strain",
        "Keep your yarn at a comfortable height",
        "Alternate crochet with other hobbies",
        "Use ergonomic crochet hooks with padded grips",
        "Warm up hands before starting a session",
        "Keep tension relaxed - tight gripping causes strain",
        "Try a yarn bowl to reduce wrist movement",
        "Stretch before and after crocheting",
        "Stay hydrated - dehydrated muscles cramp easier",
        "Use good lighting to avoid eye strain",
        "Vary your projects to use different hand motions",
        "Consider a wrist brace for support during long sessions",
        "Ice hands if they feel inflamed after crocheting",
    ]
    
    PAIN_AREAS = ["thumb", "index_finger", "wrist", "forearm", "shoulder", "neck", "upper_back", "eyes"]
    
    BREAK_SCHEDULE = {
        "light": {"work_minutes": 45, "break_minutes": 5, "stretches": 2},
        "moderate": {"work_minutes": 30, "break_minutes": 5, "stretches": 3},
        "intensive": {"work_minutes": 20, "break_minutes": 5, "stretches": 4},
    }
    
    def __init__(self, storage_path: str = "ergonomic.json"):
        self.storage_path = Path(storage_path)
        self.data = {
            "session_start": None,
            "breaks_taken": 0,
            "total_stretches": 0,
            "pain_log": [],
            "daily_sessions": [],
            "intensity": "moderate",
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
    
    def start_session(self, intensity: str = "moderate"):
        """Start a crochet session with tracking"""
        self.data["session_start"] = datetime.now().isoformat()
        self.data["breaks_taken"] = 0
        self.data["intensity"] = intensity
        self.save()
        return f"Session started! Intensity: {intensity}"
    
    def check_break_needed(self) -> Dict:
        """Check if a break is needed based on session time"""
        if not self.data.get("session_start"):
            return {"needed": False, "message": "No active session"}
        
        start = datetime.fromisoformat(self.data["session_start"])
        elapsed = (datetime.now() - start).total_seconds() / 60  # minutes
        
        schedule = self.BREAK_SCHEDULE.get(self.data["intensity"], self.BREAK_SCHEDULE["moderate"])
        time_since_break = elapsed - (self.data["breaks_taken"] * (schedule["work_minutes"] + schedule["break_minutes"]))
        
        needed = time_since_break >= schedule["work_minutes"]
        
        return {
            "needed": needed,
            "minutes_elapsed": round(elapsed, 1),
            "breaks_taken": self.data["breaks_taken"],
            "next_break_in": round(schedule["work_minutes"] - time_since_break, 1) if not needed else 0,
            "schedule": schedule,
            "message": "Time for a break! 🧘" if needed else f"Next break in {round(schedule['work_minutes'] - time_since_break, 1)} min"
        }
    
    def take_break(self) -> Dict:
        """Take a scheduled break"""
        self.data["breaks_taken"] += 1
        
        schedule = self.BREAK_SCHEDULE.get(self.data["intensity"], self.BREAK_SCHEDULE["moderate"])
        num_stretches = schedule["stretches"]
        
        import random
        selected = random.sample(self.STRETCHES, min(num_stretches, len(self.STRETCHES)))
        
        self.save()
        
        return {
            "break_number": self.data["breaks_taken"],
            "duration_minutes": schedule["break_minutes"],
            "stretches": [{"name": s.name, "target": s.target, "duration": f"{s.duration_seconds}s", "description": s.description} for s in selected],
            "tip": random.choice(self.TIPS),
        }
    
    def log_pain(self, area: str, severity: int, notes: str = "") -> Dict:
        """Log pain or discomfort"""
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "area": area,
            "severity": min(10, max(1, severity)),
            "notes": notes,
        }
        self.data["pain_log"].append(entry)
        self.save()
        
        # Analyze patterns
        recent = [p for p in self.data["pain_log"] if p["area"] == area]
        avg_severity = sum(p["severity"] for p in recent[-5:]) / min(5, len(recent))
        
        advice = self._get_pain_advice(area, severity)
        
        return {
            "logged": True,
            "area": area,
            "severity": severity,
            "advice": advice,
            "pattern": f"This is the {len(recent)}th time you've logged {area} pain" if len(recent) > 2 else "",
            "avg_severity": round(avg_severity, 1),
        }
    
    def _get_pain_advice(self, area: str, severity: int) -> List[str]:
        """Get advice based on pain area and severity"""
        advice = []
        
        if severity >= 7:
            advice.append("⚠️ High pain level - consider stopping and resting")
            advice.append("Apply ice for 15 minutes")
            if area in ("wrist", "thumb"):
                advice.append("Consider seeing a doctor if pain persists")
        
        area_advice = {
            "thumb": ["Try a larger hook grip", "Use your other hand more", "Thumb splint at night"],
            "wrist": ["Check your wrist angle", "Use ergonomic hooks", "Wrist exercises 3x daily"],
            "forearm": ["Massage forearm muscles", "Check tension - relax your grip", "Take more breaks"],
            "shoulder": ["Check your seating position", "Do shoulder rolls every 15 min", "Support your arms"],
            "neck": ["Raise your work to eye level", "Take posture breaks", "Gentle neck stretches"],
            "eyes": ["Follow 20-20-20 rule", "Improve lighting", "Get eyes checked"],
        }
        
        advice.extend(area_advice.get(area, ["Take a break", "Stretch gently"]))
        return advice
    
    def get_posture_check(self) -> List[Dict]:
        """Get a posture checklist"""
        return [
            {"check": pc["check"], "area": pc["area"], "status": "unchecked"}
            for pc in self.POSTURE_CHECKS
        ]
    
    def get_daily_routine(self) -> List[Dict]:
        """Get a daily stretch routine"""
        import random
        routine = random.sample(self.STRETCHES, min(6, len(self.STRETCHES)))
        return [s.to_dict() for s in routine]
    
    def get_health_report(self) -> Dict:
        """Get ergonomic health report"""
        pain_entries = self.data.get("pain_log", [])
        
        by_area = {}
        for p in pain_entries:
            area = p["area"]
            if area not in by_area:
                by_area[area] = {"count": 0, "avg_severity": 0, "entries": []}
            by_area[area]["count"] += 1
            by_area[area]["entries"].append(p)
        
        for area, data in by_area.items():
            data["avg_severity"] = round(sum(e["severity"] for e in data["entries"]) / data["count"], 1)
        
        worst_area = max(by_area.items(), key=lambda x: x[1]["count"]) if by_area else (None, {})
        
        return {
            "total_sessions": len(self.data.get("daily_sessions", [])),
            "total_breaks": self.data.get("breaks_taken", 0),
            "total_pain_entries": len(pain_entries),
            "pain_by_area": {k: v["count"] for k, v in by_area.items()},
            "worst_area": worst_area[0],
            "worst_area_count": worst_area[1].get("count", 0) if worst_area[0] else 0,
            "intensity": self.data.get("intensity", "moderate"),
        }


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  ERGONOMIC ASSISTANT - DEMONSTRATION")
    print("=" * 60)
    
    erg = ErgonomicAssistant(storage_path="/tmp/demo_ergo.json")
    
    # Start session
    print(f"\n{erg.start_session('moderate')}")
    
    # Check break
    check = erg.check_break_needed()
    print(f"\n⏰ Break check: {check['message']}")
    
    # Take a break
    break_info = erg.take_break()
    print(f"\n🧘 Taking Break #{break_info['break_number']}:")
    for s in break_info["stretches"]:
        print(f"  • {s['name']} ({s['target']}, {s['duration']}): {s['description'][:60]}...")
    print(f"  💡 Tip: {break_info['tip']}")
    
    # Log pain
    print(f"\n🤕 Logging wrist pain...")
    pain_result = erg.log_pain("wrist", 4, "After long session")
    print(f"  Advice: {pain_result['advice'][:2]}")
    
    # Posture check
    print(f"\n🪑 Posture Checklist:")
    for check in erg.get_posture_check():
        print(f"  □ {check['check']}")
    
    # Daily routine
    print(f"\n🧘 Daily Stretch Routine:")
    for s in erg.get_daily_routine():
        print(f"  • {s['name']} ({s['duration_seconds']}s) - {s['target']}")
    
    # Health report
    report = erg.get_health_report()
    print(f"\n📊 Health Report:")
    print(f"  Pain entries: {report['total_pain_entries']}")
    if report['worst_area']:
        print(f"  Worst area: {report['worst_area']} ({report['worst_area_count']} times)")
    
    # Cleanup
    if os.path.exists("/tmp/demo_ergo.json"):
        os.remove("/tmp/demo_ergo.json")
    
    print(f"\n  Ergonomic Assistant Complete! 🧘")
