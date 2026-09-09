"""
Timelapse Video Maker - Create progress videos from photos
Turn your crochet journey into a beautiful timelapse video
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class TimelapseFrame:
    """A single frame in the timelapse"""
    photo_path: str = ""
    round_number: int = 0
    timestamp: str = ""
    caption: str = ""
    transition: str = "fade"  # fade, slide, zoom, none
    duration_seconds: float = 2.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TimelapseProject:
    """A timelapse video project"""
    name: str
    frames: List[Dict] = field(default_factory=list)
    music: str = ""
    background: str = "dark"
    title_card: str = ""
    end_card: str = ""
    fps: int = 30
    frame_duration: float = 2.0
    transition_type: str = "fade"
    output_format: str = "html"  # html, gif, mp4
    width: int = 1080
    height: int = 1080
    
    def to_dict(self) -> Dict:
        return asdict(self)


class TimelapseMaker:
    """
    Create timelapse videos from crochet progress photos
    
    Features:
    - Combine progress photos into video
    - Add transitions (fade, slide, zoom)
    - Background music selection
    - Title/end cards
    - Multiple output formats (HTML, GIF guide, MP4 guide)
    - Round-by-round annotation
    - Progress overlay
    """
    
    TRANSITIONS = {
        "fade": "Smooth fade between frames",
        "slide_left": "Slide from right to left",
        "slide_up": "Slide from bottom to top",
        "zoom_in": "Zoom into next frame",
        "zoom_out": "Zoom out from next frame",
        "flip": "3D flip transition",
        "none": "No transition (cut)",
    }
    
    THEMES = {
        "dark": {"bg": "#0a0a0a", "text": "#ffffff", "accent": "#4ECCA3"},
        "light": {"bg": "#f5f5f5", "text": "#333333", "accent": "#E94560"},
        "cozy": {"bg": "#2C1810", "text": "#F5DEB3", "accent": "#DAA520"},
        "pastel": {"bg": "#FFF0F5", "text": "#4A4A4A", "accent": "#FFB6C1"},
        "ocean": {"bg": "#0C2340", "text": "#E0F7FA", "accent": "#00BCD4"},
        "forest": {"bg": "#1B3A2D", "text": "#C8E6C9", "accent": "#66BB6A"},
    }
    
    MUSIC_SUGGESTIONS = [
        {"name": "Relaxing Piano", "mood": "calm", "bpm": 60},
        {"name": "Upbeat Acoustic", "mood": "happy", "bpm": 120},
        {"name": "Lo-fi Beats", "mood": "chill", "bpm": 90},
        {"name": "Cinematic", "mood": "epic", "bpm": 80},
        {"name": "Nature Sounds", "mood": "peaceful", "bpm": 0},
    ]
    
    def __init__(self):
        self.projects: Dict[str, TimelapseProject] = {}
    
    def create_project(self, name: str, theme: str = "dark",
                      fps: int = 30, frame_duration: float = 2.0) -> str:
        """Create a new timelapse project"""
        project = TimelapseProject(
            name=name,
            background=theme,
            fps=fps,
            frame_duration=frame_duration,
        )
        self.projects[name] = project
        return name
    
    def add_frame(self, project_name: str, photo_path: str = "",
                 round_number: int = 0, caption: str = "",
                 transition: str = "fade") -> bool:
        """Add a frame to the timelapse"""
        if project_name not in self.projects:
            return False
        
        frame = TimelapseFrame(
            photo_path=photo_path,
            round_number=round_number,
            timestamp=datetime.now().isoformat(),
            caption=caption,
            transition=transition,
            duration_seconds=self.projects[project_name].frame_duration,
        )
        
        self.projects[project_name].frames.append(frame.to_dict())
        return True
    
    def add_demo_frames(self, project_name: str, total_rounds: int = 10):
        """Add demo frames for testing"""
        for i in range(1, total_rounds + 1):
            captions = [
                f"Starting round {i}",
                f"Round {i} in progress",
                f"Round {i} complete!",
            ]
            self.add_frame(
                project_name,
                round_number=i,
                caption=captions[i % len(captions)]
            )
    
    def generate_html_timelapse(self, project_name: str) -> str:
        """Generate an interactive HTML timelapse"""
        if project_name not in self.projects:
            return "<p>Project not found</p>"
        
        proj = self.projects[project_name]
        theme = self.THEMES.get(proj.background, self.THEMES["dark"])
        
        frames_json = json.dumps(proj.frames)
        
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Timelapse - {proj.name}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, sans-serif;
    background: {theme['bg']};
    color: {theme['text']};
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}}
h1 {{
    color: {theme['accent']};
    margin: 20px 0;
    font-size: 2em;
}}
.player {{
    width: {proj.width}px;
    height: {proj.height}px;
    max-width: 90vw;
    max-height: 60vh;
    background: rgba(0,0,0,0.3);
    border-radius: 12px;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}
.frame {{
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    opacity: 0;
    transition: opacity 0.8s ease;
    padding: 40px;
    text-align: center;
}}
.frame.active {{ opacity: 1; }}
.frame .round-num {{
    font-size: 5em;
    font-weight: bold;
    color: {theme['accent']};
    text-shadow: 0 0 30px rgba(78,204,163,0.3);
    margin-bottom: 20px;
}}
.frame .caption {{
    font-size: 1.5em;
    color: {theme['text']};
    opacity: 0.8;
    max-width: 80%;
}}
.frame .photo-area {{
    width: 70%;
    height: 70%;
    border: 3px dashed rgba(255,255,255,0.2);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4em;
    margin-bottom: 20px;
}}
.progress {{
    width: {proj.width}px;
    max-width: 90vw;
    height: 6px;
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    margin: 20px 0;
    overflow: hidden;
}}
.progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, {theme['accent']}, {theme['text']});
    transition: width 0.5s ease;
    border-radius: 3px;
}}
.controls {{
    display: flex;
    gap: 15px;
    margin: 20px;
    align-items: center;
}}
.btn {{
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1em;
    font-weight: bold;
    transition: transform 0.1s;
}}
.btn:active {{ transform: scale(0.95); }}
.btn-play {{ background: {theme['accent']}; color: {theme['bg']}; }}
.btn-stop {{ background: #e94560; color: white; }}
.btn-step {{ background: rgba(255,255,255,0.1); color: {theme['text']}; }}
.info {{
    color: rgba(255,255,255,0.5);
    margin: 10px;
    font-size: 0.9em;
}}
.speed-control {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 10px;
}}
.speed-control input {{
    width: 100px;
}}
</style>
</head>
<body>
<h1>{proj.name}</h1>
<p class="info">Crochet Progress Timelapse</p>

<div class="player" id="player">
    <!-- Frames will be injected here -->
</div>

<div class="progress">
    <div class="progress-fill" id="progressFill" style="width: 0%"></div>
</div>

<div class="controls">
    <button class="btn btn-step" onclick="prevFrame()">⏮</button>
    <button class="btn btn-play" id="playBtn" onclick="togglePlay()">▶ Play</button>
    <button class="btn btn-step" onclick="nextFrame()">⏭</button>
    <button class="btn btn-stop" onclick="resetTimelapse()">↺ Reset</button>
</div>

<div class="speed-control">
    <span>Speed:</span>
    <input type="range" min="0.5" max="5" step="0.5" value="{proj.frame_duration}" 
           onchange="changeSpeed(this.value)" id="speedSlider">
    <span id="speedLabel">{proj.frame_duration}s</span>
</div>

<p class="info" id="frameInfo">Frame 0 / 0</p>

<script>
const frames = {frames_json};
let currentFrame = -1;
let isPlaying = false;
let interval;
let frameDuration = {proj.frame_duration} * 1000;

// Build frames
const player = document.getElementById('player');
frames.forEach((frame, i) => {{
    const div = document.createElement('div');
    div.className = 'frame';
    div.id = 'frame-' + i;
    div.innerHTML = `
        <div class="photo-area">🧶</div>
        <div class="round-num">Round ${{frame.round_number || i + 1}}</div>
        <div class="caption">${{frame.caption || ''}}</div>
    `;
    player.appendChild(div);
}});

function showFrame(idx) {{
    document.querySelectorAll('.frame').forEach(f => f.classList.remove('active'));
    if (idx >= 0 && idx < frames.length) {{
        document.getElementById('frame-' + idx).classList.add('active');
        currentFrame = idx;
        document.getElementById('progressFill').style.width = ((idx + 1) / frames.length * 100) + '%';
        document.getElementById('frameInfo').textContent = `Frame ${{idx + 1}} / ${{frames.length}}`;
    }}
}}

function nextFrame() {{
    if (currentFrame < frames.length - 1) {{
        showFrame(currentFrame + 1);
    }} else if (isPlaying) {{
        togglePlay();
    }}
}}

function prevFrame() {{
    if (currentFrame > 0) showFrame(currentFrame - 1);
}}

function togglePlay() {{
    isPlaying = !isPlaying;
    document.getElementById('playBtn').textContent = isPlaying ? '⏸ Pause' : '▶ Play';
    document.getElementById('playBtn').className = isPlaying ? 'btn btn-stop' : 'btn btn-play';
    
    if (isPlaying) {{
        if (currentFrame >= frames.length - 1) showFrame(-1);
        interval = setInterval(nextFrame, frameDuration);
    }} else {{
        clearInterval(interval);
    }}
}}

function resetTimelapse() {{
    clearInterval(interval);
    isPlaying = false;
    document.getElementById('playBtn').textContent = '▶ Play';
    document.getElementById('playBtn').className = 'btn btn-play';
    showFrame(0);
}}

function changeSpeed(val) {{
    frameDuration = val * 1000;
    document.getElementById('speedLabel').textContent = val + 's';
    if (isPlaying) {{
        clearInterval(interval);
        interval = setInterval(nextFrame, frameDuration);
    }}
}}

// Start at first frame
showFrame(0);
</script>
</body>
</html>'''
        
        return html
    
    def get_project_info(self, project_name: str) -> Dict:
        """Get project information"""
        if project_name not in self.projects:
            return {}
        
        proj = self.projects[project_name]
        total_duration = sum(f.get("duration_seconds", 2) for f in proj.frames)
        
        return {
            "name": proj.name,
            "total_frames": len(proj.frames),
            "total_duration_seconds": round(total_duration, 1),
            "total_duration_string": f"{int(total_duration // 60)}m {int(total_duration % 60)}s" if total_duration >= 60 else f"{int(total_duration)}s",
            "theme": proj.background,
            "fps": proj.fps,
            "transitions_used": list(set(f.get("transition", "fade") for f in proj.frames)),
        }
    
    def export_for_external_tool(self, project_name: str) -> Dict:
        """Export project data for external video tools"""
        if project_name not in self.projects:
            return {}
        
        proj = self.projects[project_name]
        
        return {
            "ffmpeg_command": self._generate_ffmpeg_command(proj),
            "frames_list": proj.frames,
            "total_frames": len(proj.frames),
            "suggested_tools": [
                "FFmpeg (command line video)",
                "CapCut (free mobile/desktop)",
                "DaVinci Resolve (free professional)",
                "Canva Video (easy online)",
                "InShot (mobile)",
            ]
        }
    
    def _generate_ffmpeg_command(self, proj: TimelapseProject) -> str:
        """Generate FFmpeg command for video creation"""
        return (
            f"ffmpeg -framerate 1/{proj.frame_duration} "
            f"-i frame_%04d.jpg "
            f"-c:v libx264 -pix_fmt yuv420p "
            f"-r 30 {proj.name.replace(' ', '_')}_timelapse.mp4"
        )


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  TIMELAPSE VIDEO MAKER - DEMONSTRATION")
    print("=" * 60)
    
    maker = TimelapseMaker()
    
    # Create project
    proj = maker.create_project("Bunny Timelapse", theme="cozy", frame_duration=2.0)
    print(f"\n✅ Created project: {proj}")
    
    # Add demo frames
    maker.add_demo_frames(proj, total_rounds=13)
    print(f"✅ Added 13 frames")
    
    # Get info
    info = maker.get_project_info(proj)
    print(f"\n📊 Project Info:")
    for key, val in info.items():
        print(f"  {key}: {val}")
    
    # Generate HTML
    html = maker.generate_html_timelapse(proj)
    print(f"\n✅ HTML timelapse: {len(html)} chars")
    
    # Export for external tools
    export = maker.export_for_external_tool(proj)
    print(f"\n🎬 FFmpeg command:")
    print(f"  {export['ffmpeg_command']}")
    print(f"\n📱 Suggested tools:")
    for tool in export['suggested_tools']:
        print(f"  • {tool}")
    
    # Themes
    print(f"\n🎨 Available Themes:")
    for name, colors in maker.THEMES.items():
        print(f"  • {name}: bg={colors['bg']} accent={colors['accent']}")
    
    # Music
    print(f"\n🎵 Music Suggestions:")
    for m in maker.MUSIC_SUGGESTIONS:
        print(f"  • {m['name']} ({m['mood']}, {m['bpm']} BPM)")
    
    print(f"\n  Timelapse Maker Complete! 🎬")
