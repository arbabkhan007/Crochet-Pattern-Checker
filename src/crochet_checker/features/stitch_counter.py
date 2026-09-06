"""
Stitch Counter - Interactive click counter with progress tracking
"""
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class CounterSession:
    pattern_name: str
    current_round: int = 1
    current_stitch: int = 0
    target_stitches: int = 0
    total_rounds: int = 0
    round_counts: Dict[int, int] = field(default_factory=dict)
    started_at: str = ""
    last_tap_time: float = 0
    taps_per_minute: float = 0
    is_running: bool = False
    
    def to_dict(self) -> Dict:
        return asdict(self)


class StitchCounter:
    """
    Interactive stitch counter for real-time crochet tracking
    
    Features:
    - Tap to count stitches
    - Auto-detect round completion
    - Haptic feedback zones (visual)
    - Speed tracking (stitches per minute)
    - Undo last tap
    - Jump to round
    - Multiple pattern support
    - Session history
    """
    
    def __init__(self, storage_path: str = ".stitch_counter.json"):
        self.storage_path = Path(storage_path)
        self.session: Optional[CounterSession] = None
        self.sessions_history: List[Dict] = []
        self.load()
    
    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                self.sessions_history = data.get("history", [])
            except Exception:
                pass
    
    def save(self):
        data = {"history": self.sessions_history}
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def start_session(self, pattern_name: str, rounds: List[Dict] = None,
                     total_rounds: int = 0) -> str:
        """Start a new counting session"""
        self.session = CounterSession(
            pattern_name=pattern_name,
            total_rounds=total_rounds or (len(rounds) if rounds else 0),
            started_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            is_running=True
        )
        
        if rounds:
            self.session.target_stitches = rounds[0].get("count", rounds[0].get("stitch_count", 0))
        
        return f"Started counting: {pattern_name}. Round 1, target: {self.session.target_stitches} stitches."
    
    def tap(self) -> Dict:
        """Register a stitch tap"""
        if not self.session or not self.session.is_running:
            return {"error": "No active session", "message": "Start a session first"}
        
        now = time.time()
        self.session.current_stitch += 1
        
        # Calculate taps per minute
        if self.session.last_tap_time > 0:
            elapsed = now - self.session.last_tap_time
            if elapsed > 0:
                instant_spm = 60.0 / elapsed
                self.session.taps_per_minute = (
                    self.session.taps_per_minute * 0.7 + instant_spm * 0.3
                )
        
        self.session.last_tap_time = now
        
        result = {
            "stitch": self.session.current_stitch,
            "target": self.session.target_stitches,
            "round": self.session.current_round,
            "progress": round(self.session.current_stitch / max(1, self.session.target_stitches) * 100, 1),
            "spm": round(self.session.taps_per_minute, 1),
            "round_complete": self.session.current_stitch >= self.session.target_stitches > 0,
        }
        
        if result["round_complete"]:
            result["message"] = f"Round {self.session.current_round} complete! ({self.session.target_stitches} stitches)"
            result["next_action"] = "Call next_round() to advance"
        else:
            remaining = self.session.target_stitches - self.session.current_stitch
            result["message"] = f"{remaining} stitches remaining in round {self.session.current_round}"
        
        return result
    
    def undo(self) -> Dict:
        """Undo last tap"""
        if not self.session or self.session.current_stitch <= 0:
            return {"message": "Nothing to undo", "stitch": 0, "target": 0, "round": 0}
        
        self.session.current_stitch -= 1
        return {
            "stitch": self.session.current_stitch,
            "target": self.session.target_stitches,
            "round": self.session.current_round,
            "message": f"Undone. Now at stitch {self.session.current_stitch}"
        }
    
    def next_round(self, target_stitches: int = 0) -> Dict:
        """Advance to next round"""
        if not self.session:
            return {"error": "No active session"}
        
        # Save current round count
        self.session.round_counts[self.session.current_round] = self.session.current_stitch
        
        self.session.current_round += 1
        self.session.current_stitch = 0
        
        if target_stitches > 0:
            self.session.target_stitches = target_stitches
        
        is_final = self.session.current_round > self.session.total_rounds > 0
        
        result = {
            "round": self.session.current_round,
            "target": self.session.target_stitches,
            "message": f"Round {self.session.current_round}"
        }
        
        if is_final:
            result["message"] = "All rounds complete! Pattern finished!"
            result["pattern_complete"] = True
            self._end_session()
        else:
            result["message"] += f". Target: {self.session.target_stitches} stitches"
        
        return result
    
    def jump_to_round(self, round_num: int, target_stitches: int = 0) -> Dict:
        """Jump to a specific round"""
        if not self.session:
            return {"error": "No active session"}
        
        self.session.current_round = round_num
        self.session.current_stitch = 0
        if target_stitches > 0:
            self.session.target_stitches = target_stitches
        
        return {
            "round": self.session.current_round,
            "target": self.session.target_stitches,
            "message": f"Jumped to Round {self.session.current_round}"
        }
    
    def get_display(self) -> str:
        """Get visual display of current state"""
        if not self.session:
            return "No active session"
        
        # Progress bar for current round
        if self.session.target_stitches > 0:
            progress = self.session.current_stitch / self.session.target_stitches
            bar_width = 30
            filled = int(bar_width * progress)
            bar = "#" * filled + "-" * (bar_width - filled)
        else:
            bar = "?" * 30
        
        # Round progress
        if self.session.total_rounds > 0:
            round_progress = f"Round {self.session.current_round}/{self.session.total_rounds}"
        else:
            round_progress = f"Round {self.session.current_round}"
        
        lines = [
            f"  {self.session.pattern_name}",
            f"  {round_progress}",
            f"  [{bar}]",
            f"  {self.session.current_stitch}/{self.session.target_stitches} stitches",
            f"  Speed: {self.session.taps_per_minute:.0f} spm",
        ]
        
        return "\n".join(lines)
    
    def _end_session(self):
        """End and save session"""
        if self.session:
            self.session.is_running = False
            self.sessions_history.append(self.session.to_dict())
            self.save()
    
    def get_history(self) -> List[Dict]:
        return self.sessions_history
    
    def generate_html_counter(self, pattern: Dict = None) -> str:
        """Generate an interactive HTML stitch counter"""
        pattern_name = pattern.get("title", "Pattern") if pattern else "Counter"
        rounds = pattern.get("rounds", []) if pattern else []
        
        round_targets = json.dumps([r.get("count", r.get("stitch_count", 0)) for r in rounds])
        
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Stitch Counter - {pattern_name}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ 
    font-family: -apple-system, sans-serif; 
    background: #1a1a2e; color: #eee;
    display: flex; flex-direction: column; align-items: center;
    min-height: 100vh; padding: 20px;
    user-select: none; -webkit-user-select: none;
}}
h1 {{ color: #e94560; margin: 20px 0; font-size: 1.5em; }}
.round-info {{ font-size: 1.2em; margin: 10px; color: #a8d8ea; }}
.counter-display {{
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, #16213e, #0f3460);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    margin: 20px; cursor: pointer;
    border: 4px solid #e94560;
    transition: transform 0.1s;
    box-shadow: 0 0 30px rgba(233,69,96,0.3);
}}
.counter-display:active {{ transform: scale(0.95); }}
.counter-display.complete {{ border-color: #4ecca3; box-shadow: 0 0 30px rgba(78,204,163,0.3); }}
.stitch-count {{ font-size: 3em; font-weight: bold; }}
.target {{ font-size: 1em; color: #888; }}
.progress-bar {{
    width: 80%; max-width: 300px; height: 10px;
    background: #16213e; border-radius: 5px; margin: 15px;
    overflow: hidden;
}}
.progress-fill {{
    height: 100%; background: linear-gradient(90deg, #e94560, #4ecca3);
    transition: width 0.3s; border-radius: 5px;
}}
.controls {{ display: flex; gap: 10px; margin: 15px; flex-wrap: wrap; justify-content: center; }}
.btn {{
    padding: 12px 24px; border: none; border-radius: 8px;
    font-size: 1em; cursor: pointer; font-weight: bold;
    transition: transform 0.1s;
}}
.btn:active {{ transform: scale(0.95); }}
.btn-primary {{ background: #e94560; color: white; }}
.btn-secondary {{ background: #16213e; color: #a8d8ea; border: 1px solid #a8d8ea; }}
.btn-success {{ background: #4ecca3; color: #1a1a2e; }}
.speed {{ font-size: 0.9em; color: #888; margin: 5px; }}
.round-tabs {{
    display: flex; flex-wrap: wrap; gap: 5px; margin: 15px;
    justify-content: center; max-width: 400px;
}}
.round-tab {{
    padding: 5px 10px; border-radius: 4px; font-size: 0.8em;
    background: #16213e; color: #888; cursor: pointer;
}}
.round-tab.active {{ background: #e94560; color: white; }}
.round-tab.done {{ background: #4ecca3; color: #1a1a2e; }}
</style>
</head>
<body>
<h1>{pattern_name}</h1>
<div class="round-info" id="roundInfo">Round 1</div>

<div class="counter-display" id="counterBtn" onclick="tap()">
    <div class="stitch-count" id="stitchCount">0</div>
    <div class="target" id="targetCount">/ 0</div>
</div>

<div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>

<div class="speed" id="speedDisplay">0 stitches/min</div>

<div class="controls">
    <button class="btn btn-secondary" onclick="undo()">Undo</button>
    <button class="btn btn-primary" onclick="nextRound()">Next Round</button>
    <button class="btn btn-secondary" onclick="reset()">Reset</button>
</div>

<div class="round-tabs" id="roundTabs"></div>

<script>
let currentRound = 0;
let currentStitch = 0;
let roundTargets = {round_targets};
let lastTap = 0;
let completedRounds = new Set();

function updateDisplay() {{
    document.getElementById('stitchCount').textContent = currentStitch;
    let target = roundTargets[currentRound] || 0;
    document.getElementById('targetCount').textContent = '/ ' + target;
    document.getElementById('roundInfo').textContent = 'Round ' + (currentRound + 1) + ' of ' + roundTargets.length;
    
    let progress = target > 0 ? (currentStitch / target * 100) : 0;
    document.getElementById('progressFill').style.width = Math.min(100, progress) + '%';
    
    let btn = document.getElementById('counterBtn');
    btn.classList.toggle('complete', currentStitch >= target && target > 0);
    
    updateTabs();
}}

function tap() {{
    currentStitch++;
    let now = Date.now();
    if (lastTap > 0) {{
        let elapsed = (now - lastTap) / 1000;
        let spm = Math.round(60 / elapsed);
        document.getElementById('speedDisplay').textContent = spm + ' stitches/min';
    }}
    lastTap = now;
    
    let target = roundTargets[currentRound] || 0;
    if (currentStitch >= target && target > 0) {{
        completedRounds.add(currentRound);
    }}
    
    updateDisplay();
    if (navigator.vibrate) navigator.vibrate(30);
}}

function undo() {{
    if (currentStitch > 0) {{
        currentStitch--;
        updateDisplay();
    }}
}}

function nextRound() {{
    if (currentRound < roundTargets.length - 1) {{
        completedRounds.add(currentRound);
        currentRound++;
        currentStitch = 0;
        updateDisplay();
    }}
}}

function jumpToRound(idx) {{
    currentRound = idx;
    currentStitch = 0;
    updateDisplay();
}}

function reset() {{
    currentRound = 0;
    currentStitch = 0;
    completedRounds.clear();
    updateDisplay();
}}

function updateTabs() {{
    let html = '';
    for (let i = 0; i < roundTargets.length; i++) {{
        let cls = 'round-tab';
        if (i === currentRound) cls += ' active';
        else if (completedRounds.has(i)) cls += ' done';
        html += '<div class="' + cls + '" onclick="jumpToRound(' + i + ')">R' + (i+1) + '</div>';
    }}
    document.getElementById('roundTabs').innerHTML = html;
}}

updateDisplay();
</script>
</body>
</html>'''
        return html


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  STITCH COUNTER - DEMONSTRATION")
    print("=" * 60)
    
    counter = StitchCounter(storage_path="/tmp/demo_counter.json")
    
    # Start session
    rounds = [
        {"round": 1, "count": 6},
        {"round": 2, "count": 12},
        {"round": 3, "count": 18},
        {"round": 4, "count": 24},
        {"round": 5, "count": 24},
    ]
    
    print(f"\n{counter.start_session('Demo Ball', rounds=rounds, total_rounds=5)}")
    
    # Simulate tapping
    print(f"\n--- Simulating Stitches ---")
    for i in range(6):
        result = counter.tap()
        print(f"  Tap {i+1}: {result['message']}")
    
    # Round complete
    print(f"\n{counter.next_round(target_stitches=12)['message']}")
    
    # Tap through round 2
    for i in range(12):
        counter.tap()
    print(f"Round 2 complete!")
    
    print(f"\n{counter.next_round(target_stitches=18)['message']}")
    
    # Display
    print(f"\n--- Current Display ---")
    print(counter.get_display())
    
    # Undo
    print(f"\n{counter.undo()['message']}")
    print(counter.get_display())
    
    # Generate HTML
    html = counter.generate_html_counter({
        "title": "Demo Ball",
        "rounds": rounds
    })
    print(f"\nHTML counter generated: {len(html)} chars")
    
    # Cleanup
    import os
    if os.path.exists("/tmp/demo_counter.json"):
        os.remove("/tmp/demo_counter.json")
    
    print(f"\n  Stitch Counter Complete!")
