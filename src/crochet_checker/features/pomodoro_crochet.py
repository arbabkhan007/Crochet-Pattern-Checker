"""
Pomodoro Crochet Timer - Productive timed crochet sessions with breaks
"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path


class PomodoroCrochetTimer:
    """
    Pomodoro timer optimized for crochet sessions
    
    Features:
    - Customizable work/break intervals
    - Session tracking
    - Daily/weekly totals
    - Streak tracking
    - Goal integration
    - Break activity suggestions
    """
    
    PRESETS = {
        "standard": {"work": 25, "short_break": 5, "long_break": 15, "cycles": 4},
        "relaxed": {"work": 20, "short_break": 5, "long_break": 10, "cycles": 3},
        "focused": {"work": 45, "short_break": 10, "long_break": 20, "cycles": 4},
        "beginner": {"work": 15, "short_break": 5, "long_break": 10, "cycles": 3},
        "marathon": {"work": 50, "short_break": 10, "long_break": 30, "cycles": 6},
    }
    
    BREAK_ACTIVITIES = [
        "Stand up and stretch your arms overhead",
        "Roll your shoulders 10 times each direction",
        "Do wrist circles - 10 each direction",
        "Walk around the room for 2 minutes",
        "Get a glass of water and hydrate",
        "Do the 20-20-20 rule: look 20 feet away for 20 seconds",
        "Massage your hands and fingers",
        "Take 5 deep breaths",
        "Do neck rolls - 5 each direction",
        "Check your posture - sit up straight!",
        "Look out a window and rest your eyes",
        "Do finger spreads - open wide, make fist, repeat 10x",
    ]
    
    def __init__(self, storage_path: str = "pomodoro_crochet.json"):
        self.storage_path = Path(storage_path)
        self.data = {
            "sessions": [],
            "total_work_minutes": 0,
            "total_break_minutes": 0,
            "total_pomodoros": 0,
            "daily_log": {},
            "streak": 0,
            "last_session_date": None,
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
    
    def create_session(self, preset: str = "standard", custom_minutes: int = None) -> Dict:
        """Create a pomodoro session plan"""
        config = self.PRESETS.get(preset, self.PRESETS["standard"])
        
        if custom_minutes:
            config = {**config, "work": custom_minutes}
        
        # Build timeline
        timeline = []
        total_minutes = 0
        
        for cycle in range(1, config["cycles"] + 1):
            # Work phase
            timeline.append({
                "type": "work",
                "duration": config["work"],
                "label": f"Work #{cycle}",
                "instruction": f"Focus on your crochet for {config['work']} minutes",
            })
            total_minutes += config["work"]
            
            # Break phase
            if cycle < config["cycles"]:
                break_time = config["short_break"]
                break_type = "short"
            else:
                break_time = config["long_break"]
                break_type = "long"
            
            timeline.append({
                "type": "break",
                "duration": break_time,
                "label": f"{break_type.title()} Break",
                "instruction": f"Rest for {break_time} minutes. {self.get_break_activity()}",
                "activity": self.get_break_activity(),
            })
            total_minutes += break_time
        
        return {
            "preset": preset,
            "config": config,
            "timeline": timeline,
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 1),
            "pomodoros": config["cycles"],
        }
    
    def complete_session(self, preset: str = "standard", pomodoros_completed: int = 0) -> Dict:
        """Log a completed session"""
        config = self.PRESETS.get(preset, self.PRESETS["standard"])
        
        work_minutes = pomodoros_completed * config["work"]
        break_minutes = (pomodoros_completed - 1) * config["short_break"]
        if pomodoros_completed == config["cycles"]:
            break_minutes += config["long_break"] - config["short_break"]
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Update streak
        if self.data["last_session_date"] != today:
            if self.data["last_session_date"]:
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                if self.data["last_session_date"] == yesterday:
                    self.data["streak"] += 1
                else:
                    self.data["streak"] = 1
            else:
                self.data["streak"] = 1
            self.data["last_session_date"] = today
        
        # Update daily log
        if today not in self.data["daily_log"]:
            self.data["daily_log"][today] = {"work_minutes": 0, "pomodoros": 0}
        
        self.data["daily_log"][today]["work_minutes"] += work_minutes
        self.data["daily_log"][today]["pomodoros"] += pomodoros_completed
        
        self.data["total_work_minutes"] += work_minutes
        self.data["total_break_minutes"] += break_minutes
        self.data["total_pomodoros"] += pomodoros_completed
        
        self.data["sessions"].append({
            "date": today,
            "time": datetime.now().strftime("%H:%M"),
            "preset": preset,
            "pomodoros": pomodoros_completed,
            "work_minutes": work_minutes,
        })
        
        self.save()
        
        return {
            "pomodoros_completed": pomodoros_completed,
            "work_minutes": work_minutes,
            "total_hours": round(self.data["total_work_minutes"] / 60, 1),
            "streak": self.data["streak"],
            "today_minutes": self.data["daily_log"][today]["work_minutes"],
        }
    
    def get_break_activity(self) -> str:
        """Get a random break activity"""
        import random
        return random.choice(self.BREAK_ACTIVITIES)
    
    def get_stats(self) -> Dict:
        """Get pomodoro statistics"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_data = self.data["daily_log"].get(today, {"work_minutes": 0, "pomodoros": 0})
        
        # This week
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        week_minutes = 0
        week_pomodoros = 0
        for i in range(7):
            day = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            day_data = self.data["daily_log"].get(day, {"work_minutes": 0, "pomodoros": 0})
            week_minutes += day_data["work_minutes"]
            week_pomodoros += day_data["pomodoros"]
        
        # Best day
        best_day = max(self.data["daily_log"].items(), key=lambda x: x[1]["work_minutes"]) if self.data["daily_log"] else (None, {"work_minutes": 0})
        
        return {
            "total_pomodoros": self.data["total_pomodoros"],
            "total_work_hours": round(self.data["total_work_minutes"] / 60, 1),
            "total_sessions": len(self.data["sessions"]),
            "streak": self.data["streak"],
            "today": {
                "minutes": today_data["work_minutes"],
                "pomodoros": today_data["pomodoros"],
            },
            "this_week": {
                "minutes": week_minutes,
                "pomodoros": week_pomodoros,
                "hours": round(week_minutes / 60, 1),
            },
            "best_day": {
                "date": best_day[0],
                "minutes": best_day[1]["work_minutes"],
            },
            "avg_per_session": round(self.data["total_work_minutes"] / max(1, len(self.data["sessions"])), 0),
        }
    
    def generate_timer_html(self, preset: str = "standard") -> str:
        """Generate interactive timer HTML"""
        config = self.PRESETS.get(preset, self.PRESETS["standard"])
        
        return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Pomodoro Crochet Timer</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2);
    color: white; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.timer {{ font-size: 5em; font-weight: bold; margin: 20px; }}
.label {{ font-size: 1.5em; margin: 10px; opacity: 0.8; }}
.cycle {{ font-size: 1.2em; opacity: 0.6; margin: 10px; }}
.activity {{ font-size: 1.1em; margin: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; max-width: 400px; text-align: center; }}
button {{ padding: 15px 40px; font-size: 1.3em; border: none; border-radius: 30px; cursor: pointer;
    margin: 10px; font-weight: bold; }}
.start {{ background: #4ECCA3; color: white; }}
.reset {{ background: rgba(255,255,255,0.2); color: white; }}
.work {{ background: #E94560; color: white; }}
.break {{ background: #4ECCA3; color: white; }}
</style></head>
<body>
<div class="label" id="label">Ready to Focus!</div>
<div class="timer" id="timer">25:00</div>
<div class="cycle" id="cycle">Pomodoro 1 of {config['cycles']}</div>
<div class="activity" id="activity">🧶 Focus on your crochet project</div>
<div>
    <button class="start" onclick="toggleTimer()" id="toggleBtn">▶️ Start</button>
    <button class="reset" onclick="resetTimer()">🔄 Reset</button>
</div>
<script>
const workMin = {config['work']};
const shortBreak = {config['short_break']};
const longBreak = {config['long_break']};
const cycles = {config['cycles']};
const activities = {json.dumps(self.BREAK_ACTIVITIES)};

let seconds = workMin * 60;
let currentCycle = 1;
let isWork = true;
let timer = null;
let running = false;

function updateDisplay() {{
    const min = Math.floor(seconds / 60);
    const sec = seconds % 60;
    document.getElementById('timer').textContent = 
        (min < 10 ? '0' : '') + min + ':' + (sec < 10 ? '0' : '') + sec;
}}

function toggleTimer() {{
    if (running) {{
        clearInterval(timer);
        running = false;
        document.getElementById('toggleBtn').textContent = '▶️ Resume';
    }} else {{
        running = true;
        document.getElementById('toggleBtn').textContent = '⏸️ Pause';
        timer = setInterval(() => {{
            seconds--;
            if (seconds <= 0) {{
                switchPhase();
            }} else {{
                updateDisplay();
            }}
        }}, 1000);
    }}
}}

function switchPhase() {{
    if (isWork) {{
        // Switch to break
        isWork = false;
        if (currentCycle === cycles) {{
            seconds = longBreak * 60;
            document.getElementById('label').textContent = '🎉 Long Break - You did it!';
        }} else {{
            seconds = shortBreak * 60;
            document.getElementById('label').textContent = '☕ Short Break';
        }}
        document.getElementById('timer').className = 'timer break';
        document.getElementById('activity').textContent = 
            '💡 ' + activities[Math.floor(Math.random() * activities.length)];
    }} else {{
        // Switch to work
        isWork = true;
        currentCycle++;
        if (currentCycle > cycles) {{
            document.getElementById('label').textContent = '🏆 Session Complete!';
            document.getElementById('timer').textContent = '00:00';
            document.getElementById('activity').textContent = 'Amazing work! Take a well-deserved rest.';
            clearInterval(timer);
            running = false;
            document.getElementById('toggleBtn').textContent = '▶️ Start';
            return;
        }}
        seconds = workMin * 60;
        document.getElementById('label').textContent = '🧶 Focus Time!';
        document.getElementById('timer').className = 'timer work';
        document.getElementById('activity').textContent = '🧶 Focus on your crochet project';
    }}
    document.getElementById('cycle').textContent = 
        'Pomodoro ' + currentCycle + ' of ' + cycles;
    updateDisplay();
}}

function resetTimer() {{
    clearInterval(timer);
    running = false;
    currentCycle = 1;
    isWork = true;
    seconds = workMin * 60;
    document.getElementById('timer').className = 'timer';
    document.getElementById('label').textContent = 'Ready to Focus!';
    document.getElementById('cycle').textContent = 'Pomodoro 1 of ' + cycles;
    document.getElementById('activity').textContent = '🧶 Focus on your crochet project';
    document.getElementById('toggleBtn').textContent = '▶️ Start';
    updateDisplay();
}}

updateDisplay();
</script>
</body></html>'''


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  POMODORO CROCHET TIMER - DEMONSTRATION")
    print("=" * 60)
    
    timer = PomodoroCrochetTimer(storage_path="/tmp/demo_pomo.json")
    
    # Show presets
    print(f"\n⏱️  Available Presets:")
    for name, config in timer.PRESETS.items():
        total = config["work"] * config["cycles"]
        print(f"  • {name}: {config['work']}min work × {config['cycles']} = {total}min")
    
    # Create session
    print(f"\n📋 Standard Session Plan:")
    session = timer.create_session("standard")
    print(f"  Total: {session['total_minutes']}min ({session['total_hours']}h)")
    print(f"  Pomodoros: {session['pomodoros']}")
    for item in session["timeline"][:4]:
        icon = "🧶" if item["type"] == "work" else "☕"
        print(f"  {icon} {item['label']}: {item['duration']}min")
    
    # Complete sessions
    print(f"\n✅ Completing sessions...")
    for _ in range(3):
        result = timer.complete_session("standard", pomodoros_completed=4)
    
    print(f"  Total hours: {result['total_hours']}")
    print(f"  Streak: {result['streak']} days")
    
    # Stats
    print(f"\n📊 Pomodoro Stats:")
    stats = timer.get_stats()
    print(f"  Total Pomodoros: {stats['total_pomodoros']}")
    print(f"  Total Work: {stats['total_work_hours']} hours")
    print(f"  Sessions: {stats['total_sessions']}")
    print(f"  Streak: {stats['streak']} days")
    print(f"  Today: {stats['today']['minutes']}min")
    print(f"  This Week: {stats['this_week']['hours']}h")
    
    # Break activities
    print(f"\n💡 Break Activities:")
    for _ in range(3):
        print(f"  • {timer.get_break_activity()}")
    
    # HTML timer
    html = timer.generate_timer_html("standard")
    print(f"\n✅ Interactive timer: {len(html)} chars")
    
    # Cleanup
    if os.path.exists("/tmp/demo_pomo.json"):
        os.remove("/tmp/demo_pomo.json")
    
    print(f"\n  Pomodoro Crochet Timer Complete! ⏱️")
