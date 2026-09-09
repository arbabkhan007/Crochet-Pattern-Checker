"""
AI Tutorial Generator - Creates audio and video tutorials from any pattern
Combines: AI script writing, ElevenLabs voice, Sora/Veo video, simulation
"""
import json
import os
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

# Import the model router
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from .ai_model_router import AIModelRouter
except (ImportError, SystemError):
    try:
        from ai_model_router import AIModelRouter
    except ImportError:
        # Running from different directory
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "ai_model_router",
            os.path.join(os.path.dirname(__file__), "ai_model_router.py")
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        AIModelRouter = mod.AIModelRouter


@dataclass
class TutorialStep:
    """A single step in the tutorial"""
    round_number: int
    instruction: str
    stitch_count: int
    narration: str
    visual_prompt: str
    duration_seconds: float = 5.0
    tips: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class GeneratedTutorial:
    """A complete generated tutorial"""
    pattern_name: str
    total_steps: int
    total_duration_seconds: float
    script: str
    audio_path: str = ""
    video_path: str = ""
    html_path: str = ""
    steps: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return asdict(self)


class AITutorialGenerator:
    """
    Generates complete audio and video tutorials from crochet patterns
    
    Pipeline:
    1. Parse pattern → Extract rounds, stitches, counts
    2. Generate script → AI writes narration (GPT-4o/Gemini)
    3. Simulate rounds → Create visual descriptions for each step
    4. Generate audio → ElevenLabs voice synthesis
    5. Generate video → Sora/Veo2 for real video, HTML animation as fallback
    6. Combine → Sync audio + video with round transitions
    7. Export → MP4, MP3, HTML package
    
    AI Models Used:
    - OpenAI GPT-4o: Script generation, narration writing
    - Google Gemini: Alternative script generation
    - ElevenLabs: Voice synthesis (multiple voice options)
    - Google TTS: Free voice alternative
    - OpenAI Sora: Video generation (when available)
    - Google Veo 2: Video generation (when available)
    - Runway Gen-3: Video generation (when available)
    - DALL-E 3: Thumbnail generation
    """
    
    def __init__(self, output_dir: str = "tutorials"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.router = AIModelRouter()
    
    def generate_tutorial(self, pattern: Dict, 
                         voice: str = "warm_friendly",
                         video_style: str = "friendly",
                         generate_audio: bool = True,
                         generate_video: bool = True) -> GeneratedTutorial:
        """
        Generate a complete tutorial from a pattern
        
        Args:
            pattern: The crochet pattern data
            voice: Voice preset name
            video_style: Tutorial style (friendly, professional, energetic)
            generate_audio: Whether to generate audio narration
            generate_video: Whether to generate video
            
        Returns:
            GeneratedTutorial with all outputs
        """
        title = pattern.get("title", pattern.get("name", "Untitled"))
        print(f"\n  Generating tutorial for: {title}")
        print(f"  " + "=" * 50)
        
        # Step 1: Create tutorial steps
        print(f"\n  [1/5] Creating tutorial steps...")
        steps = self._create_steps(pattern, video_style)
        print(f"  ✅ Created {len(steps)} steps")
        
        # Step 2: Generate narration script
        print(f"\n  [2/5] Generating narration script...")
        script = self.router.generate_tutorial_script(pattern, video_style)
        print(f"  ✅ Script: {len(script)} chars")
        
        # Step 3: Generate audio
        audio_path = ""
        if generate_audio:
            print(f"\n  [3/5] Generating audio narration...")
            audio_path = self._generate_audio(script, title, voice)
        else:
            print(f"\n  [3/5] Audio skipped")
        
        # Step 4: Generate video
        video_path = ""
        html_path = ""
        if generate_video:
            print(f"\n  [4/5] Generating video tutorial...")
            video_result = self.router.generate_video(pattern)
            
            if video_result.get("status") == "fallback":
                # Generate HTML animation
                html_path = self._save_html_animation(video_result["content"], title)
                print(f"  ✅ HTML animation generated")
            else:
                print(f"  ✅ Video model: {video_result.get('model', 'N/A')}")
                video_path = video_result.get("path", "")
        else:
            print(f"\n  [4/5] Video skipped")
        
        # Step 5: Create metadata package
        print(f"\n  [5/5] Creating tutorial package...")
        
        # Calculate total duration
        total_duration = sum(s.duration_seconds for s in steps)
        
        tutorial = GeneratedTutorial(
            pattern_name=title,
            total_steps=len(steps),
            total_duration_seconds=total_duration,
            script=script,
            audio_path=audio_path,
            video_path=video_path,
            html_path=html_path,
            steps=[s.to_dict() for s in steps],
            metadata={
                "voice": voice,
                "style": video_style,
                "ai_models_used": self._get_models_used(generate_audio, generate_video),
                "pattern_difficulty": pattern.get("difficulty", "Unknown"),
                "total_rounds": len(pattern.get("rounds", [])),
            }
        )
        
        # Save tutorial package
        package_path = self._save_package(tutorial, title)
        print(f"  ✅ Package saved: {package_path}")
        
        print(f"\n  " + "=" * 50)
        print(f"  TUTORIAL COMPLETE!")
        print(f"  Steps: {len(steps)} | Duration: {total_duration:.0f}s")
        print(f"  Audio: {'✅' if audio_path else '❌'} | Video: {'✅' if video_path or html_path else '❌'}")
        
        return tutorial
    
    def _create_steps(self, pattern: Dict, style: str) -> List[TutorialStep]:
        """Create detailed tutorial steps from pattern"""
        steps = []
        rounds = pattern.get("rounds", [])
        title = pattern.get("title", "Pattern")
        
        for rnd in rounds:
            rn = rnd.get("round_number", rnd.get("round", 0))
            instr = rnd.get("instruction", "")
            count = rnd.get("count", rnd.get("stitch_count", 0))
            
            # Generate narration for this round
            narration = self._round_narration(rn, instr, count, len(rounds))
            
            # Generate visual prompt for video
            visual_prompt = self.router._generate_round_prompt(title, rnd, rn, len(rounds))
            
            # Estimate duration
            word_count = len(narration.split())
            duration = max(3.0, word_count * 0.3)  # ~3 words per second
            
            # Generate tips
            tips = self._generate_tips(rn, instr, count, len(rounds))
            
            step = TutorialStep(
                round_number=rn,
                instruction=instr,
                stitch_count=count,
                narration=narration,
                visual_prompt=visual_prompt,
                duration_seconds=round(duration, 1),
                tips=tips
            )
            steps.append(step)
        
        return steps
    
    def _round_narration(self, round_num: int, instruction: str, 
                        count: int, total_rounds: int) -> str:
        """Generate narration for a single round"""
        spoken = self.router._instruction_to_speech(instruction)
        
        lines = [f"Now for round {round_num}."]
        lines.append(spoken + ".")
        
        if count:
            lines.append(f"You should have {count} stitches.")
        
        # Add tips based on round position
        if round_num == 1:
            lines.append("Make sure to pull that magic ring nice and tight.")
        elif round_num == total_rounds:
            lines.append("That's the last round! Beautiful work!")
        elif round_num == total_rounds // 2:
            lines.append("We're halfway there! Keep up the great work.")
        
        return " ".join(lines)
    
    def _generate_tips(self, round_num: int, instruction: str, 
                      count: int, total_rounds: int) -> List[str]:
        """Generate contextual tips for a round"""
        tips = []
        instr_lower = instruction.lower()
        
        if "mr" in instr_lower or "magic ring" in instr_lower:
            tips.append("Pull the tail tight to close the center hole")
        
        if "inc" in instr_lower and "each" in instr_lower:
            tips.append("Work both stitches into the same stitch from the previous round")
        
        if "dec" in instr_lower:
            tips.append("Insert hook into both stitches, yarn over, pull through both")
        
        if count > 30:
            tips.append("Use a stitch marker to track your starting point")
        
        if round_num == 1:
            tips.append("This is the foundation round - take your time")
        
        return tips
    
    def _generate_audio(self, script: str, title: str, voice: str) -> str:
        """Generate audio narration"""
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)
        audio_path = str(self.output_dir / f"{safe_title}_audio.mp3")
        
        success = self.router.generate_voice(script, voice, audio_path)
        
        if success and os.path.exists(audio_path):
            return audio_path
        
        return ""
    
    def _save_html_animation(self, html_content: str, title: str) -> str:
        """Save HTML animation to file"""
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)
        html_path = str(self.output_dir / f"{safe_title}_video.html")
        Path(html_path).write_text(html_content)
        return html_path
    
    def _save_package(self, tutorial: GeneratedTutorial, title: str) -> str:
        """Save the complete tutorial package"""
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)
        package_path = self.output_dir / f"{safe_title}_package.json"
        package_path.write_text(json.dumps(tutorial.to_dict(), indent=2))
        return str(package_path)
    
    def _get_models_used(self, audio: bool, video: bool) -> List[str]:
        """Get list of AI models used"""
        models = []
        
        script_model = self.router.get_best_model("script")
        if script_model:
            models.append(f"Script: {script_model}")
        
        if audio:
            voice_model = self.router.get_best_model("voice")
            if voice_model:
                models.append(f"Voice: {voice_model}")
            else:
                models.append("Voice: local TTS fallback")
        
        if video:
            video_model = self.router.get_best_model("video")
            if video_model:
                models.append(f"Video: {video_model}")
            else:
                models.append("Video: HTML animation fallback")
        
        return models
    
    # ════════════════════════════════════════════════════
    # BATCH GENERATION
    # ════════════════════════════════════════════════════
    
    def generate_for_library(self, patterns: List[Dict]) -> List[GeneratedTutorial]:
        """Generate tutorials for multiple patterns"""
        results = []
        for i, pattern in enumerate(patterns, 1):
            print(f"\n{'=' * 50}")
            print(f"  Generating tutorial {i}/{len(patterns)}")
            tutorial = self.generate_tutorial(pattern)
            results.append(tutorial)
        return results
    
    # ════════════════════════════════════════════════════
    # REAL-TIME SIMULATION
    # ════════════════════════════════════════════════════
    
    def simulate_round(self, pattern: Dict, round_num: int) -> Dict:
        """
        Simulate a single round with full visual + audio description
        This is used for step-by-step tutorial playback
        """
        rounds = pattern.get("rounds", [])
        rnd = next((r for r in rounds 
                   if r.get("round", r.get("round_number")) == round_num), None)
        
        if not rnd:
            return {"error": f"Round {round_num} not found"}
        
        title = pattern.get("title", "Pattern")
        instruction = rnd.get("instruction", "")
        count = rnd.get("count", rnd.get("stitch_count", 0))
        
        # Generate visual description
        visual = self.router._generate_round_prompt(title, rnd, round_num, len(rounds))
        
        # Generate narration
        narration = self._round_narration(round_num, instruction, count, len(rounds))
        
        # Calculate estimated stitch positions for visualization
        prev_round = next((r for r in rounds 
                         if r.get("round", r.get("round_number")) == round_num - 1), None)
        prev_count = prev_round.get("count", prev_round.get("stitch_count", 0)) if prev_round else 0
        
        simulation = {
            "round_number": round_num,
            "total_rounds": len(rounds),
            "instruction": instruction,
            "stitch_count": count,
            "previous_count": prev_count,
            "stitches_added": count - prev_count if prev_count > 0 else count,
            "narration": narration,
            "visual_prompt": visual,
            "audio_clip_needed": True,
            "animation_frames": self._estimate_frames(instruction, count),
            "difficulty_note": self._get_difficulty_note(instruction),
        }
        
        return simulation
    
    def _estimate_frames(self, instruction: str, count: int) -> int:
        """Estimate number of animation frames needed"""
        # Each stitch needs about 3-5 frames to show formation
        return max(30, count * 3)
    
    def _get_difficulty_note(self, instruction: str) -> str:
        """Get a difficulty note for the instruction"""
        instr_lower = instruction.lower()
        
        if any(s in instr_lower for s in ["cable", "broomstick", "hairpin"]):
            return "Advanced technique - take it slow"
        elif any(s in instr_lower for s in ["popcorn", "bobble", "shell"]):
            return "Intermediate technique"
        elif "dec" in instr_lower and "inc" in instr_lower:
            return "Watch your stitch count carefully"
        elif "each st" in instr_lower:
            return "Steady rounds - maintain even tension"
        else:
            return ""


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║  🎬 AI TUTORIAL GENERATOR - DEMONSTRATION               ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    generator = AITutorialGenerator(output_dir="/tmp/demo_tutorials")
    
    sample = {
        "title": "Cute Bunny Amigurumi",
        "difficulty": "Beginner",
        "materials": {"Hook": "3.5mm", "Yarn": "DK cotton, white + pink"},
        "rounds": [
            {"round": 1, "instruction": "6 sc in MR", "count": 6},
            {"round": 2, "instruction": "inc in each st around", "count": 12},
            {"round": 3, "instruction": "[sc, inc] x 6", "count": 18},
            {"round": 4, "instruction": "[2 sc, inc] x 6", "count": 24},
            {"round": 5, "instruction": "[3 sc, inc] x 6", "count": 30},
            {"round": 6, "instruction": "[4 sc, inc] x 6", "count": 36},
            {"round": 7, "instruction": "sc in each st around", "count": 36},
            {"round": 8, "instruction": "sc in each st around", "count": 36},
            {"round": 9, "instruction": "[4 sc, dec] x 6", "count": 30},
            {"round": 10, "instruction": "[3 sc, dec] x 6", "count": 24},
            {"round": 11, "instruction": "[2 sc, dec] x 6", "count": 18},
            {"round": 12, "instruction": "[sc, dec] x 6", "count": 12},
            {"round": 13, "instruction": "dec x 6", "count": 6},
        ]
    }
    
    # Generate tutorial
    tutorial = generator.generate_tutorial(
        sample,
        voice="warm_friendly",
        video_style="friendly",
        generate_audio=True,
        generate_video=True
    )
    
    # Simulate a single round
    print(f"\n\n  Simulating Round 3...")
    sim = generator.simulate_round(sample, 3)
    print(f"  Round: {sim['round_number']}/{sim['total_rounds']}")
    print(f"  Instruction: {sim['instruction']}")
    print(f"  Count: {sim['stitch_count']}")
    print(f"  Narration: {sim['narration'][:100]}...")
    print(f"  Animation frames: {sim['animation_frames']}")
    
    # Cleanup
    import shutil
    if os.path.exists("/tmp/demo_tutorials"):
        shutil.rmtree("/tmp/demo_tutorials")
    
    print(f"\n  AI Tutorial Generator Complete! 🎬")
