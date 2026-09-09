"""
Pattern Tester Manager - Manage pattern testers, feedback, and testing workflows
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class Tester:
    """A pattern tester"""
    id: str
    name: str
    email: str = ""
    skill_level: str = "intermediate"  # beginner, intermediate, advanced
    specialties: List[str] = field(default_factory=list)  # amigurumi, garments, blankets
    yarn_stash_sizes: List[str] = field(default_factory=list)  # small, medium, large
    hook_sizes: List[str] = field(default_factory=list)
    notes: str = ""
    tests_completed: int = 0
    avg_feedback_quality: float = 0
    active: bool = True
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PatternTest:
    """A pattern testing assignment"""
    id: str
    pattern_name: str
    tester_id: str
    status: str = "assigned"  # assigned, in_progress, submitted, reviewed, completed
    assigned_date: str = ""
    due_date: str = ""
    completed_date: str = ""
    feedback: Dict = field(default_factory=dict)
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class PatternTesterManager:
    """
    Manage pattern testers and testing workflow
    
    Features:
    - Tester database
    - Test assignment
    - Feedback collection
    - Testing workflow tracking
    - Tester matching
    - Review system
    """
    
    FEEDBACK_TEMPLATE = {
        "clarity": {"rating": 0, "comments": ""},
        "accuracy": {"rating": 0, "comments": ""},
        "difficulty_match": {"rating": 0, "comments": ""},
        "enjoyment": {"rating": 0, "comments": ""},
        "would_make_again": None,
        "errors_found": [],
        "suggestions": "",
        "photos": [],
        "yarn_used": "",
        "hook_used": "",
        "gauge_match": None,
        "total_time_hours": 0,
    }
    
    SKILL_LEVELS = {
        "beginner": {"weight": 1, "desc": "New to crochet, basic stitches"},
        "intermediate": {"weight": 2, "desc": "Comfortable with patterns, multiple stitch types"},
        "advanced": {"weight": 3, "desc": "Complex patterns, design, colorwork"},
    }
    
    def __init__(self, storage_path: str = "pattern_testers.json"):
        self.storage_path = Path(storage_path)
        self.testers: Dict[str, Tester] = {}
        self.tests: Dict[str, PatternTest] = {}
        self._next_tester_id = 1
        self._next_test_id = 1
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for k, v in data.get("testers", {}).items():
                    self.testers[k] = Tester(**v)
                for k, v in data.get("tests", {}).items():
                    self.tests[k] = PatternTest(**v)
                self._next_tester_id = data.get("next_tester_id", 1)
                self._next_test_id = data.get("next_test_id", 1)
            except Exception:
                pass
    
    def save(self):
        data = {
            "testers": {k: v.to_dict() for k, v in self.testers.items()},
            "tests": {k: v.to_dict() for k, v in self.tests.items()},
            "next_tester_id": self._next_tester_id,
            "next_test_id": self._next_test_id,
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def add_tester(self, name: str, email: str = "", skill_level: str = "intermediate",
                  specialties: List[str] = None, **kwargs) -> str:
        """Add a new pattern tester"""
        tid = f"T{self._next_tester_id:04d}"
        self._next_tester_id += 1
        
        tester = Tester(
            id=tid, name=name, email=email,
            skill_level=skill_level,
            specialties=specialties or [],
            **kwargs
        )
        self.testers[tid] = tester
        self.save()
        return tid
    
    def assign_test(self, pattern_name: str, tester_id: str,
                   due_days: int = 14) -> str:
        """Assign a pattern test to a tester"""
        test_id = f"TEST{self._next_test_id:04d}"
        self._next_test_id += 1
        
        today = datetime.now()
        test = PatternTest(
            id=test_id,
            pattern_name=pattern_name,
            tester_id=tester_id,
            assigned_date=today.strftime("%Y-%m-%d"),
            due_date=(today + timedelta(days=due_days)).strftime("%Y-%m-%d"),
        )
        
        self.tests[test_id] = test
        self.save()
        return test_id
    
    def submit_feedback(self, test_id: str, feedback: Dict) -> Dict:
        """Submit tester feedback"""
        test = self.tests.get(test_id)
        if not test:
            return {"error": "Test not found"}
        
        test.feedback = feedback
        test.status = "submitted"
        test.completed_date = datetime.now().strftime("%Y-%m-%d")
        
        # Update tester stats
        tester = self.testers.get(test.tester_id)
        if tester:
            tester.tests_completed += 1
            quality = sum(feedback.get(k, {}).get("rating", 0) for k in ["clarity", "accuracy", "difficulty_match", "enjoyment"]) / 4
            if tester.avg_feedback_quality == 0:
                tester.avg_feedback_quality = quality
            else:
                tester.avg_feedback_quality = (tester.avg_feedback_quality + quality) / 2
        
        self.save()
        return {"status": "submitted", "test_id": test_id}
    
    def find_best_testers(self, skill_level: str = None,
                         specialty: str = None,
                         max_active_tests: int = 2) -> List[Dict]:
        """Find suitable testers for a pattern"""
        # Count active tests per tester
        active_counts = {}
        for test in self.tests.values():
            if test.status in ("assigned", "in_progress"):
                active_counts[test.tester_id] = active_counts.get(test.tester_id, 0) + 1
        
        candidates = []
        for tester in self.testers.values():
            if not tester.active:
                continue
            if tester.id in active_counts and active_counts[tester.id] >= max_active_tests:
                continue
            if skill_level and tester.skill_level != skill_level:
                continue
            if specialty and specialty not in tester.specialties:
                continue
            
            candidates.append({
                "id": tester.id,
                "name": tester.name,
                "skill_level": tester.skill_level,
                "specialties": tester.specialties,
                "tests_completed": tester.tests_completed,
                "active_tests": active_counts.get(tester.id, 0),
                "avg_quality": round(tester.avg_feedback_quality, 1),
            })
        
        return sorted(candidates, key=lambda x: x["tests_completed"], reverse=True)
    
    def get_testing_dashboard(self) -> Dict:
        """Get testing dashboard overview"""
        all_tests = list(self.tests.values())
        
        by_status = {}
        for test in all_tests:
            by_status[test.status] = by_status.get(test.status, 0) + 1
        
        # Overdue tests
        today = datetime.now().strftime("%Y-%m-%d")
        overdue = [t for t in all_tests if t.status in ("assigned", "in_progress") and t.due_date < today]
        
        # Tester stats
        active_testers = len([t for t in self.testers.values() if t.active])
        total_completed = sum(t.tests_completed for t in self.testers.values())
        
        # Recent feedback
        recent = sorted(all_tests, key=lambda t: t.completed_date or "", reverse=True)
        recent_feedback = [
            {"pattern": t.pattern_name, "tester": self.testers.get(t.tester_id, Tester("", "")).name,
             "status": t.status, "date": t.completed_date}
            for t in recent[:5] if t.status == "submitted"
        ]
        
        return {
            "total_testers": len(self.testers),
            "active_testers": active_testers,
            "total_tests": len(all_tests),
            "by_status": by_status,
            "overdue_count": len(overdue),
            "overdue": [{"id": t.id, "pattern": t.pattern_name, "due": t.due_date} for t in overdue],
            "total_completed_tests": total_completed,
            "recent_feedback": recent_feedback,
        }
    
    def generate_feedback_form_html(self, test_id: str = "TEST0001") -> str:
        """Generate feedback form HTML"""
        return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Pattern Test Feedback</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: #f5f5f5; padding: 20px; max-width: 600px; margin: 0 auto; }}
h1 {{ color: #333; }}
.section {{ background: white; border-radius: 8px; padding: 16px; margin: 16px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
label {{ display: block; margin: 8px 0 4px; font-weight: bold; }}
input, textarea, select {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 8px; }}
.stars {{ font-size: 1.5em; cursor: pointer; }}
.stars span {{ color: #ddd; }}
.stars span.active {{ color: #FFD700; }}
button {{ background: #4ECCA3; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 1em; cursor: pointer; }}
button:hover {{ background: #3db891; }}
</style></head>
<body>
<h1>📝 Pattern Test Feedback</h1>
<p>Test ID: {test_id}</p>

<div class="section">
    <h3>📖 Clarity</h3>
    <p>How clear were the pattern instructions?</p>
    <div class="stars" onclick="rate(this, 'clarity')">
        <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
    </div>
    <label>Comments</label>
    <textarea rows="3" placeholder="Any clarity issues..."></textarea>
</div>

<div class="section">
    <h3>✅ Accuracy</h3>
    <p>Were the stitch counts and instructions accurate?</p>
    <div class="stars" onclick="rate(this, 'accuracy')">
        <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
    </div>
    <label>Errors Found</label>
    <textarea rows="3" placeholder="List any errors..."></textarea>
</div>

<div class="section">
    <h3>📊 Difficulty Match</h3>
    <p>Did the difficulty match the stated level?</p>
    <div class="stars" onclick="rate(this, 'difficulty')">
        <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
    </div>
</div>

<div class="section">
    <h3>💖 Overall Enjoyment</h3>
    <p>How much did you enjoy making this?</p>
    <div class="stars" onclick="rate(this, 'enjoyment')">
        <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
    </div>
</div>

<div class="section">
    <h3>🧶 Details</h3>
    <label>Yarn Used</label>
    <input type="text" placeholder="Brand, weight, color">
    <label>Hook Size</label>
    <input type="text" placeholder="e.g., 4.0mm (G/6)">
    <label>Gauge Match?</label>
    <select><option>Yes, perfect</option><option>Slightly off</option><option>No</option></select>
    <label>Time to Complete (hours)</label>
    <input type="number" placeholder="e.g., 5">
    <label>Would you make this again?</label>
    <select><option>Yes!</option><option>Maybe</option><option>No</option></select>
</div>

<div class="section">
    <h3>💡 Suggestions</h3>
    <textarea rows="4" placeholder="Any improvement suggestions..."></textarea>
</div>

<button onclick="alert('Feedback submitted! Thank you!')">Submit Feedback 🎉</button>

<script>
function rate(el, category) {{
    const stars = el.querySelectorAll('span');
    stars.forEach(s => s.classList.remove('active'));
    event.target.classList.add('active');
    let prev = event.target;
    while (prev.previousElementSibling) {{
        prev = prev.previousElementSibling;
        prev.classList.add('active');
    }}
}}
</script>
</body></html>'''


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  PATTERN TESTER MANAGER - DEMONSTRATION")
    print("=" * 60)
    
    mgr = PatternTesterManager(storage_path="/tmp/demo_testers.json")
    
    # Add testers
    t1 = mgr.add_tester("Alice", "alice@example.com", "intermediate",
                        specialties=["amigurumi", "accessories"])
    t2 = mgr.add_tester("Bob", "bob@example.com", "advanced",
                        specialties=["garments", "colorwork"])
    t3 = mgr.add_tester("Carol", "carol@example.com", "beginner",
                        specialties=["blankets", "home"])
    print(f"✅ Added 3 testers")
    
    # Assign tests
    test1 = mgr.assign_test("Bunny Amigurumi v2", t1, due_days=14)
    test2 = mgr.assign_test("Granny Square Cardigan", t2, due_days=21)
    test3 = mgr.assign_test("Cozy Blanket", t3, due_days=30)
    print(f"✅ Assigned 3 tests")
    
    # Submit feedback
    feedback = {
        "clarity": {"rating": 5, "comments": "Very clear instructions"},
        "accuracy": {"rating": 4, "comments": "Stitch counts correct"},
        "difficulty_match": {"rating": 5, "comments": "Perfect for intermediate"},
        "enjoyment": {"rating": 5, "comments": "So fun to make!"},
        "would_make_again": True,
        "yarn_used": "Red Heart Super Saver",
        "hook_used": "4.0mm (G/6)",
        "gauge_match": True,
        "total_time_hours": 4,
    }
    mgr.submit_feedback(test1, feedback)
    print(f"✅ Submitted feedback for test 1")
    
    # Find testers
    print(f"\n🔍 Best testers for 'amigurumi':")
    candidates = mgr.find_best_testers(specialty="amigurumi")
    for c in candidates:
        print(f"  • {c['name']} ({c['skill_level']}, {c['tests_completed']} tests done)")
    
    # Dashboard
    print(f"\n📊 Testing Dashboard:")
    dash = mgr.get_testing_dashboard()
    print(f"  Total Testers: {dash['total_testers']}")
    print(f"  Active: {dash['active_testers']}")
    print(f"  Total Tests: {dash['total_tests']}")
    print(f"  By Status: {dash['by_status']}")
    print(f"  Overdue: {dash['overdue_count']}")
    
    if dash['recent_feedback']:
        print(f"\n📝 Recent Feedback:")
        for f in dash['recent_feedback']:
            print(f"  • {f['pattern']} by {f['tester']} ({f['status']})")
    
    # Feedback form HTML
    html = mgr.generate_feedback_form_html(test2)
    print(f"\n✅ Feedback form HTML: {len(html)} chars")
    
    # Cleanup
    if os.path.exists("/tmp/demo_testers.json"):
        os.remove("/tmp/demo_testers.json")
    
    print(f"\n  Pattern Tester Manager Complete! 🧪")
