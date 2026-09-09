"""
Crochet Meditation - Guided mindful crochet sessions combining mindfulness with crafting
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class MeditationSession:
    """A meditation session"""
    id: str
    date: str
    duration_minutes: int = 0
    type: str = ""  # mindful, breathing, gratitude, body_scan
    mood_before: int = 3
    mood_after: int = 3
    notes: str = ""
    completed: bool = False
    
    def to_dict(self) -> Dict:
        return vars(self)


class CrochetMeditation:
    """
    Mindful crochet and meditation guide
    
    Features:
    - Guided crochet meditation sessions
    - Breathing exercises synced with stitch counting
    - Body scan meditation
    - Gratitude journaling
    - Stress tracking
    - Mindfulness streaks
    - Session history
    """
    
    BREATHING_PATTERNS = {
        "calm": {"inhale": 4, "hold": 4, "exhale": 4, "hold_after": 4, "name": "Box Breathing"},
        "relaxing": {"inhale": 4, "hold": 7, "exhale": 8, "hold_after": 0, "name": "4-7-8 Breathing"},
        "energizing": {"inhale": 6, "hold": 0, "exhale": 2, "hold_after": 0, "name": "Energizing Breath"},
        "stitch_sync": {"inhale": 3, "hold": 0, "exhale": 3, "hold_after": 0, "name": "Stitch-Sync Breathing"},
    }
    
    GUIDED_SESSIONS = {
        "mindful_stitching": {
            "name": "Mindful Stitching",
            "duration": 10,
            "steps": [
                {"time": 0, "instruction": "Close your eyes. Take 3 deep breaths."},
                {"time": 30, "instruction": "Notice the texture of the yarn in your hands."},
                {"time": 60, "instruction": "Feel the weight of your hook. Is your grip relaxed?"},
                {"time": 120, "instruction": "Watch each stitch form. Don't rush. Be present."},
                {"time": 180, "instruction": "Notice your breathing. Sync it with your movements."},
                {"time": 300, "instruction": "Appreciate the rhythm. You are creating something beautiful."},
                {"time": 420, "instruction": "Take a moment to feel grateful for this time."},
                {"time": 540, "instruction": "Complete the session with a deep breath. Well done!"},
            ],
        },
        "body_scan": {
            "name": "Crochet Body Scan",
            "duration": 15,
            "steps": [
                {"time": 0, "instruction": "Put down your hook. Sit comfortably."},
                {"time": 30, "instruction": "Focus on your feet. Any tension? Release it."},
                {"time": 90, "instruction": "Move to your legs. Notice any sensations."},
                {"time": 180, "instruction": "Scan your hands and wrists. These work hard! Relax them."},
                {"time": 270, "instruction": "Check your shoulders. Drop them. Let them relax."},
                {"time": 360, "instruction": "Softify your face. Unclench your jaw. Blink slowly."},
                {"time": 450, "instruction": "Take a deep breath. Feel calm throughout your body."},
                {"time": 540, "instruction": "Pick up your hook with fresh, relaxed hands."},
            ],
        },
        "gratitude": {
            "name": "Gratitude Crochet",
            "duration": 10,
            "steps": [
                {"time": 0, "instruction": "Think of one thing you're grateful for today."},
                {"time": 60, "instruction": "As you crochet each stitch, think of a positive moment."},
                {"time": 120, "instruction": "Who are you thankful for? Send them good thoughts."},
                {"time": 180, "instruction": "What did you learn today? Appreciate your growth."},
                {"time": 300, "instruction": "This handmade item carries your love and gratitude."},
                {"time": 420, "instruction": "Feel the warmth of creating something with intention."},
                {"time": 540, "instruction": "Complete your session feeling thankful. 🙏"},
            ],
        },
        "stress_release": {
            "name": "Stress Release Stitching",
            "duration": 15,
            "steps": [
                {"time": 0, "instruction": "Identify what's stressing you. Name it."},
                {"time": 60, "instruction": "With each stitch, imagine releasing that tension."},
                {"time": 120, "instruction": "Let your hands move rhythmically. No rush."},
                {"time": 180, "instruction": "Breathe in calm. Breathe out stress."},
                {"time": 300, "instruction": "Notice how crochet anchors you in the present moment."},
                {"time": 420, "instruction": "The stress dissolves with each beautiful stitch."},
                {"time": 540, "instruction": "You've created beauty from stress. Well done."},
                {"time": 660, "instruction": "Take one final deep breath. Feel the calm."},
            ],
        },
    }
    
    AFFIRMATIONS = [
        "I am creating something beautiful with my own hands.",
        "Each stitch I make is a moment of mindfulness.",
        "I am patient with myself and my craft.",
        "My hands know what to do. I trust my skills.",
        "I deserve this time for myself.",
        "Creating with intention brings me peace.",
        "I am grateful for the gift of making.",
        "Every row brings me closer to something wonderful.",
        "I am calm, focused, and present.",
        "My crochet is my meditation.",
        "I release tension with every stitch.",
        "I am proud of what I create.",
        "This moment is mine. I am at peace.",
        "Slow and steady creates beauty.",
    ]
    
    def __init__(self, storage_path: str = "crochet_meditation.json"):
        self.storage_path = Path(storage_path)
        self.data = {
            "sessions": [],
            "total_minutes": 0,
            "streak": 0,
            "last_session": None,
            "mood_history": [],
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
    
    def start_session(self, session_type: str = "mindful_stitching") -> Dict:
        """Start a guided meditation session"""
        session = self.GUIDED_SESSIONS.get(session_type, self.GUIDED_SESSIONS["mindful_stitching"])
        
        return {
            "session_type": session_type,
            "name": session["name"],
            "duration_minutes": session["duration"],
            "steps": session["steps"],
            "affirmation": self.get_affirmation(),
            "breathing_pattern": self.BREATHING_PATTERNS["stitch_sync"],
        }
    
    def complete_session(self, session_type: str, duration: int,
                        mood_before: int = 3, mood_after: int = None,
                        notes: str = "") -> Dict:
        """Complete and log a session"""
        session_id = f"MS{len(self.data['sessions']) + 1:04d}"
        
        if mood_after is None:
            mood_after = min(5, mood_before + 1)  # Assume slight improvement
        
        session = {
            "id": session_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "type": session_type,
            "duration_minutes": duration,
            "mood_before": mood_before,
            "mood_after": mood_after,
            "notes": notes,
            "completed": True,
        }
        
        self.data["sessions"].append(session)
        self.data["total_minutes"] += duration
        self.data["mood_history"].append({
            "date": session["date"],
            "before": mood_before,
            "after": mood_after,
            "improvement": mood_after - mood_before,
        })
        
        # Update streak
        today = datetime.now().strftime("%Y-%m-%d")
        if self.data["last_session"]:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            if self.data["last_session"] == yesterday:
                self.data["streak"] += 1
            elif self.data["last_session"] != today:
                self.data["streak"] = 1
        else:
            self.data["streak"] = 1
        self.data["last_session"] = today
        
        self.save()
        
        improvement = mood_after - mood_before
        return {
            "session_id": session_id,
            "duration": duration,
            "mood_change": improvement,
            "mood_before": mood_before,
            "mood_after": mood_after,
            "streak": self.data["streak"],
            "total_minutes": self.data["total_minutes"],
            "affirmation": self.get_affirmation(),
        }
    
    def get_breathing_exercise(self, pattern: str = "calm") -> Dict:
        """Get a breathing exercise"""
        p = self.BREATHING_PATTERNS.get(pattern, self.BREATHING_PATTERNS["calm"])
        
        total_cycle = p["inhale"] + p["hold"] + p["exhale"] + p["hold_after"]
        
        return {
            "name": p["name"],
            "pattern": p,
            "total_cycle_seconds": total_cycle,
            "instructions": [
                f"Breathe in for {p['inhale']} seconds",
                f"Hold for {p['hold']} seconds" if p["hold"] > 0 else None,
                f"Breathe out for {p['exhale']} seconds",
                f"Hold for {p['hold_after']} seconds" if p["hold_after"] > 0 else None,
            ],
            "cycle": f"{p['inhale']}-{p['hold']}-{p['exhale']}-{p['hold_after']}" if p["hold_after"] else f"{p['inhale']}-{p['hold']}-{p['exhale']}",
        }
    
    def get_affirmation(self) -> str:
        """Get a random affirmation"""
        import random
        return random.choice(self.AFFIRMATIONS)
    
    def get_mood_impact_report(self) -> Dict:
        """Analyze mood impact of meditation"""
        history = self.data.get("mood_history", [])
        
        if not history:
            return {"message": "No sessions recorded yet"}
        
        avg_before = sum(h["before"] for h in history) / len(history)
        avg_after = sum(h["after"] for h in history) / len(history)
        avg_improvement = avg_after - avg_before
        
        total_sessions = len(history)
        positive_sessions = sum(1 for h in history if h["after"] > h["before"])
        
        # Recent trend
        recent = history[-7:] if len(history) >= 7 else history
        recent_avg_before = sum(h["before"] for h in recent) / len(recent)
        recent_avg_after = sum(h["after"] for h in recent) / len(recent)
        
        return {
            "total_sessions": total_sessions,
            "total_minutes": self.data["total_minutes"],
            "total_hours": round(self.data["total_minutes"] / 60, 1),
            "streak": self.data["streak"],
            "avg_mood_before": round(avg_before, 1),
            "avg_mood_after": round(avg_after, 1),
            "avg_improvement": round(avg_improvement, 1),
            "positive_sessions_pct": round(positive_sessions / max(1, total_sessions) * 100, 1),
            "recent_avg_improvement": round(recent_avg_after - recent_avg_before, 1),
            "recommendation": self._get_recommendation(avg_improvement),
        }
    
    def _get_recommendation(self, improvement: float) -> str:
        if improvement >= 1.5:
            return "✨ Meditation is having a major positive impact on your mood!"
        elif improvement >= 0.5:
            return "😊 Consistent practice is improving your wellbeing."
        else:
            return "🧘 Try longer sessions or different meditation types for deeper relaxation."
    
    def generate_session_html(self, session_type: str = "mindful_stitching") -> str:
        """Generate interactive meditation session HTML"""
        session = self.GUIDED_SESSIONS.get(session_type, self.GUIDED_SESSIONS["mindful_stitching"])
        
        steps_json = json.dumps(session["steps"])
        
        return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Mindful Crochet</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }}
.container {{ text-align: center; max-width: 500px; }}
h1 {{ font-size: 2em; margin-bottom: 20px; }}
.step {{ font-size: 1.5em; margin: 30px 0; min-height: 80px; transition: opacity 0.5s; }}
.timer {{ font-size: 3em; margin: 20px 0; }}
.progress {{ width: 100%; height: 8px; background: rgba(255,255,255,0.2); border-radius: 4px; overflow: hidden; margin: 20px 0; }}
.progress-bar {{ height: 100%; background: white; transition: width 1s linear; }}
button {{ padding: 15px 30px; font-size: 1.2em; border: none; border-radius: 25px; cursor: pointer;
    background: white; color: #764ba2; font-weight: bold; margin: 10px; }}
.affirmation {{ font-style: italic; margin: 20px 0; opacity: 0.8; }}
</style></head>
<body>
<div class="container">
    <h1>🧘 {session['name']}</h1>
    <div class="progress"><div class="progress-bar" id="progress"></div></div>
    <div class="timer" id="timer">0:00</div>
    <div class="step" id="step">Press Start to begin your mindful session</div>
    <div class="affirmation" id="affirmation"></div>
    <div>
        <button onclick="startSession()" id="startBtn">▶️ Start</button>
        <button onclick="stopSession()" id="stopBtn" style="display:none">⏹️ End</button>
    </div>
</div>
<script>
const steps = {steps_json};
let timer = null;
let seconds = 0;
let currentStep = 0;
const totalSeconds = {session['duration']} * 60;
const affirmations = {json.dumps(self.AFFIRMATIONS)};

function startSession() {{
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-block';
    currentStep = 0;
    showStep();
    
    timer = setInterval(() => {{
        seconds++;
        const min = Math.floor(seconds / 60);
        const sec = seconds % 60;
        document.getElementById('timer').textContent = min + ':' + (sec < 10 ? '0' : '') + sec;
        
        const pct = (seconds / totalSeconds) * 100;
        document.getElementById('progress').style.width = pct + '%';
        
        if (currentStep < steps.length && seconds >= steps[currentStep].time) {{
            showStep();
            currentStep++;
        }}
        
        if (seconds % 60 === 0) {{
            document.getElementById('affirmation').textContent = 
                '"' + affirmations[Math.floor(Math.random() * affirmations.length)] + '"';
        }}
        
        if (seconds >= totalSeconds) {{
            stopSession();
            document.getElementById('step').textContent = '🎉 Session complete! Well done! 🙏';
        }}
    }}, 1000);
}}

function showStep() {{
    if (currentStep < steps.length) {{
        document.getElementById('step').style.opacity = 0;
        setTimeout(() => {{
            document.getElementById('step').textContent = steps[currentStep].instruction;
            document.getElementById('step').style.opacity = 1;
        }}, 300);
    }}
}}

function stopSession() {{
    clearInterval(timer);
    document.getElementById('startBtn').style.display = 'inline-block';
    document.getElementById('stopBtn').style.display = 'none';
}}
</script>
</body></html>'''


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  CROCHET MEDITATION - DEMONSTRATION")
    print("=" * 60)
    
    med = CrochetMeditation(storage_path="/tmp/demo_meditation.json")
    
    # Get sessions
    print(f"\n🧘 Available Sessions:")
    for key, session in med.GUIDED_SESSIONS.items():
        print(f"  • {session['name']} ({session['duration']} min)")
    
    # Start a session
    print(f"\n▶️  Starting Mindful Stitching session...")
    s = med.start_session("mindful_stitching")
    print(f"  Name: {s['name']}")
    print(f"  Duration: {s['duration_minutes']} min")
    print(f"  Steps: {len(s['steps'])}")
    print(f"  Affirmation: \"{s['affirmation']}\"")
    
    # Breathing exercise
    print(f"\n🌬️  Breathing Exercise:")
    breath = med.get_breathing_exercise("relaxing")
    print(f"  {breath['name']}: {breath['cycle']}")
    for inst in breath['instructions']:
        if inst:
            print(f"    → {inst}")
    
    # Complete sessions
    print(f"\n📝 Logging sessions...")
    for mood_b in [2, 3, 2, 4, 3]:
        result = med.complete_session("mindful_stitching", 10, mood_before=mood_b)
    
    print(f"  Completed 5 sessions")
    
    # Mood report
    report = med.get_mood_impact_report()
    print(f"\n📊 Mood Impact Report:")
    print(f"  Total Sessions: {report['total_sessions']}")
    print(f"  Total Time: {report['total_hours']} hours")
    print(f"  Streak: {report['streak']} days")
    print(f"  Avg Mood Before: {report['avg_mood_before']}/5")
    print(f"  Avg Mood After: {report['avg_mood_after']}/5")
    print(f"  Avg Improvement: +{report['avg_improvement']}")
    print(f"  Positive Sessions: {report['positive_sessions_pct']}%")
    print(f"  {report['recommendation']}")
    
    # Interactive HTML
    html = med.generate_session_html("mindful_stitching")
    print(f"\n✅ Interactive meditation player: {len(html)} chars")
    
    # Cleanup
    if os.path.exists("/tmp/demo_meditation.json"):
        os.remove("/tmp/demo_meditation.json")
    
    print(f"\n  Crochet Meditation Complete! 🧘")
