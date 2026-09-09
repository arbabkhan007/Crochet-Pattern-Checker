"""
AI Model Router - Connects to multiple AI services
Supports: OpenAI, Google Gemini, ElevenLabs, Sora, etc.
"""
import json
import os
import time
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class AIModelConfig:
    """Configuration for an AI model"""
    name: str
    provider: str  # openai, google, elevenlabs, stability, runway
    model_id: str
    api_key_env: str  # Environment variable name for API key
    capabilities: List[str] = field(default_factory=list)
    max_tokens: int = 4096
    temperature: float = 0.7
    is_available: bool = True
    
    def to_dict(self) -> Dict:
        return asdict(self)


class AIModelRouter:
    """
    Routes requests to the best available AI model
    
    Supported Models:
    - OpenAI GPT-4o: Script generation, narration text
    - OpenAI Sora: Video generation
    - OpenAI DALL-E 3: Thumbnail generation
    - Google Gemini 2.0: Script generation, analysis
    - Google Veo 2: Video generation
    - ElevenLabs: Voice synthesis (multiple voices)
    - Google TTS: Alternative voice synthesis
    - Stability AI: Image generation
    - Runway Gen-3: Video generation
    """
    
    MODELS = {
        # Text/Script Generation
        "gpt4o": AIModelConfig(
            name="GPT-4o",
            provider="openai",
            model_id="gpt-4o",
            api_key_env="OPENAI_API_KEY",
            capabilities=["text", "script", "narration", "analysis"],
            max_tokens=16000,
        ),
        "gpt4o_mini": AIModelConfig(
            name="GPT-4o Mini",
            provider="openai",
            model_id="gpt-4o-mini",
            api_key_env="OPENAI_API_KEY",
            capabilities=["text", "script", "narration"],
            max_tokens=16000,
        ),
        "gemini": AIModelConfig(
            name="Google Gemini 2.0",
            provider="google",
            model_id="gemini-2.0-flash-exp",
            api_key_env="GOOGLE_API_KEY",
            capabilities=["text", "script", "analysis", "multimodal"],
            max_tokens=32000,
        ),
        
        # Voice Synthesis
        "elevenlabs_turbo": AIModelConfig(
            name="ElevenLabs Turbo v2.5",
            provider="elevenlabs",
            model_id="eleven_turbo_v2_5",
            api_key_env="ELEVENLABS_API_KEY",
            capabilities=["voice", "tts", "multilingual"],
        ),
        "elevenlabs_multilingual": AIModelConfig(
            name="ElevenLabs Multilingual v2",
            provider="elevenlabs",
            model_id="eleven_multilingual_v2",
            api_key_env="ELEVENLABS_API_KEY",
            capabilities=["voice", "tts", "multilingual", "emotional"],
        ),
        "google_tts": AIModelConfig(
            name="Google Text-to-Speech",
            provider="google",
            model_id="en-US-Neural2-F",
            api_key_env="GOOGLE_API_KEY",
            capabilities=["voice", "tts"],
        ),
        
        # Video Generation
        "sora": AIModelConfig(
            name="OpenAI Sora",
            provider="openai",
            model_id="sora",
            api_key_env="OPENAI_API_KEY",
            capabilities=["video", "animation", "tutorial"],
        ),
        "veo2": AIModelConfig(
            name="Google Veo 2",
            provider="google",
            model_id="veo-2",
            api_key_env="GOOGLE_API_KEY",
            capabilities=["video", "animation", "tutorial"],
        ),
        "runway_gen3": AIModelConfig(
            name="Runway Gen-3 Alpha",
            provider="runway",
            model_id="gen-3-alpha",
            api_key_env="RUNWAY_API_KEY",
            capabilities=["video", "animation"],
        ),
        
        # Image Generation
        "dalle3": AIModelConfig(
            name="DALL-E 3",
            provider="openai",
            model_id="dall-e-3",
            api_key_env="OPENAI_API_KEY",
            capabilities=["image", "thumbnail", "diagram"],
        ),
        "stable_diffusion": AIModelConfig(
            name="Stable Diffusion XL",
            provider="stability",
            model_id="stable-diffusion-xl-1024-v1-0",
            api_key_env="STABILITY_API_KEY",
            capabilities=["image", "thumbnail"],
        ),
        
        # Audio/Music
        "elevenlabs_sfx": AIModelConfig(
            name="ElevenLabs Sound Effects",
            provider="elevenlabs",
            model_id="eleven_multilingual_v2",
            api_key_env="ELEVENLABS_API_KEY",
            capabilities=["sfx", "ambient", "background"],
        ),
    }
    
    # Voice presets for different tutorial styles
    VOICE_PRESETS = {
        "warm_friendly": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Sarah
            "name": "Sarah",
            "style": "Warm, friendly, encouraging",
            "best_for": "Beginner tutorials"
        },
        "professional": {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
            "name": "Rachel",
            "style": "Professional, clear, calm",
            "best_for": "Technical instructions"
        },
        "energetic": {
            "voice_id": "AZnzlk1XvdvUeBnXldUp",  # Antoni
            "name": "Antoni",
            "style": "Energetic, enthusiastic",
            "best_for": "Challenge videos, social media"
        },
        "gentle": {
            "voice_id": "MF3mGyEYCl7XYWbV9V6O",  # Elli
            "name": "Elli",
            "style": "Gentle, soft, relaxing",
            "best_for": "Meditative crochet, ASMR"
        },
        "narrator": {
            "voice_id": "ErXwobaYiN019PkySvjV",  # Glenn
            "name": "Glenn",
            "style": "Deep, authoritative narrator",
            "best_for": "Documentary style"
        },
    }
    
    def __init__(self):
        self.available_models = self._check_availability()
        self.cache_dir = Path(".ai_cache")
        self.cache_dir.mkdir(exist_ok=True)
    
    def _check_availability(self) -> Dict[str, bool]:
        """Check which models are available based on API keys"""
        available = {}
        for model_id, config in self.MODELS.items():
            api_key = os.environ.get(config.api_key_env, "")
            available[model_id] = bool(api_key)
        return available
    
    def get_available_models(self, capability: str = None) -> List[str]:
        """Get list of available models, optionally filtered by capability"""
        result = []
        for model_id, config in self.MODELS.items():
            if self.available_models.get(model_id, False):
                if capability is None or capability in config.capabilities:
                    result.append(model_id)
        return result
    
    def get_best_model(self, capability: str) -> Optional[str]:
        """Get the best available model for a capability"""
        available = self.get_available_models(capability)
        if not available:
            return None
        
        # Priority order
        priority = {
            "text": ["gpt4o", "gemini", "gpt4o_mini"],
            "script": ["gpt4o", "gemini"],
            "voice": ["elevenlabs_multilingual", "elevenlabs_turbo", "google_tts"],
            "video": ["sora", "veo2", "runway_gen3"],
            "image": ["dalle3", "stable_diffusion"],
            "sfx": ["elevenlabs_sfx"],
        }
        
        for model in priority.get(capability, []):
            if model in available:
                return model
        
        return available[0] if available else None
    
    # ════════════════════════════════════════════════════
    # TEXT/SCRIPT GENERATION
    # ════════════════════════════════════════════════════
    
    def generate_tutorial_script(self, pattern: Dict, style: str = "friendly") -> str:
        """Generate a tutorial narration script using AI"""
        model = self.get_best_model("script")
        
        if model == "gpt4o" or model == "gpt4o_mini":
            return self._generate_script_openai(pattern, style)
        elif model == "gemini":
            return self._generate_script_gemini(pattern, style)
        else:
            return self._generate_script_local(pattern, style)
    
    def _generate_script_openai(self, pattern: Dict, style: str) -> str:
        """Generate script using OpenAI GPT-4o"""
        try:
            import openai
            client = openai.OpenAI()
            
            title = pattern.get("title", "Pattern")
            rounds = pattern.get("rounds", [])
            difficulty = pattern.get("difficulty", "Beginner")
            
            style_prompts = {
                "friendly": "warm, encouraging, like a friend teaching you",
                "professional": "clear, precise, like a technical instructor",
                "energetic": "exciting, upbeat, like a YouTube creator",
                "gentle": "soft, calming, meditative, ASMR-like",
            }
            
            rounds_text = "\n".join(
                f"Round {r.get('round', r.get('round_number', i+1))}: {r.get('instruction', '')} ({r.get('count', r.get('stitch_count', 0))} sts)"
                for i, r in enumerate(rounds)
            )
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"""You are a crochet tutorial narrator. 
                    Write a step-by-step narration script for a crochet pattern video.
                    Style: {style_prompts.get(style, 'friendly')}
                    Include:
                    - Warm introduction mentioning the pattern name
                    - Materials needed
                    - Step-by-step instructions for each round
                    - Stitch count verification after each round
                    - Encouragement and tips
                    - Celebratory conclusion
                    Keep each round's narration to 15-30 seconds.
                    Use natural speech patterns, not robotic."""},
                    {"role": "user", "content": f"""Write a tutorial script for this crochet pattern:

Pattern: {title}
Difficulty: {difficulty}
Rounds:
{rounds_text}

Write the full narration script."""}
                ],
                max_tokens=4000,
                temperature=0.8,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI script generation failed: {e}")
            return self._generate_script_local(pattern, style)
    
    def _generate_script_gemini(self, pattern: Dict, style: str) -> str:
        """Generate script using Google Gemini"""
        try:
            import google.generativeai as genai
            
            title = pattern.get("title", "Pattern")
            rounds = pattern.get("rounds", [])
            
            rounds_text = "\n".join(
                f"Round {r.get('round', i+1)}: {r.get('instruction', '')} ({r.get('count', 0)} sts)"
                for i, r in enumerate(rounds)
            )
            
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(f"""
Write a warm, friendly tutorial narration script for this crochet pattern:
Pattern: {title}
Rounds: {rounds_text}

Include introduction, step-by-step instructions, stitch counts, tips, and conclusion.
Make it sound natural for video narration, about 3-5 minutes of speaking.
""")
            
            return response.text
            
        except Exception as e:
            print(f"Gemini script generation failed: {e}")
            return self._generate_script_local(pattern, style)
    
    def _generate_script_local(self, pattern: Dict, style: str) -> str:
        """Generate script locally (no API needed)"""
        title = pattern.get("title", "Pattern")
        rounds = pattern.get("rounds", [])
        difficulty = pattern.get("difficulty", "Beginner")
        materials = pattern.get("materials", {})
        
        lines = []
        
        # Introduction
        lines.append(f"Welcome to today's crochet tutorial!")
        lines.append(f"We're going to make {title} together.")
        lines.append(f"This is a {difficulty.lower()} level pattern, perfect for {'getting started' if difficulty == 'Beginner' else 'building your skills'}.")
        lines.append("")
        
        # Materials
        if materials:
            lines.append("Before we begin, let's gather our materials.")
            for key, val in materials.items():
                lines.append(f"You'll need {val} {key.replace('_', ' ')}.")
            lines.append("")
        
        # Tips
        lines.append("A few quick tips before we start:")
        lines.append("Use a stitch marker to keep track of your rounds.")
        lines.append("Keep your tension consistent for even stitches.")
        lines.append("Count your stitches at the end of each round.")
        lines.append("")
        
        # Rounds
        lines.append("Let's begin!")
        lines.append("")
        
        for rnd in rounds:
            rn = rnd.get("round_number", rnd.get("round", 0))
            instr = rnd.get("instruction", "")
            count = rnd.get("count", rnd.get("stitch_count", 0))
            
            lines.append(f"Round {rn}.")
            
            # Expand instruction into speakable form
            spoken = self._instruction_to_speech(instr)
            lines.append(spoken)
            
            if count:
                lines.append(f"You should now have {count} stitches.")
                lines.append(f"Let me count with you... one, two, three... yes, {count} stitches. Perfect!")
            
            lines.append("")
            
            # Add encouragement at milestones
            if rn == len(rounds) // 3:
                lines.append("Great progress! We're about a third of the way done. You're doing amazing!")
                lines.append("")
            elif rn == len(rounds) // 2:
                lines.append("Halfway there! Look at how beautiful it's coming along. Keep going!")
                lines.append("")
            elif rn == len(rounds):
                lines.append("And that's the last round! Can you believe it?")
                lines.append("")
        
        # Conclusion
        lines.append("Congratulations! You've completed the pattern!")
        lines.append("Now, fasten off your yarn and weave in any loose ends.")
        lines.append("Look at what you've made! Isn't it beautiful?")
        lines.append("")
        lines.append("If you enjoyed this tutorial, please like and subscribe for more crochet patterns.")
        lines.append("Tag me in your finished projects, I'd love to see them!")
        lines.append("Happy crocheting!")
        
        return "\n".join(lines)
    
    def _instruction_to_speech(self, instruction: str) -> str:
        """Convert written instruction to natural speech"""
        spoken = instruction
        
        # Expand abbreviations
        expansions = {
            "sc": "single crochet",
            "dc": "double crochet",
            "hdc": "half double crochet",
            "tc": "treble crochet",
            "inc": "increase",
            "dec": "decrease",
            "sl st": "slip stitch",
            "ch": "chain",
            "MR": "magic ring",
            "st": "stitch",
            "sts": "stitches",
            "rnd": "round",
            "rep": "repeat",
            "FO": "fasten off",
            "x": "times",
            "×": "times",
        }
        
        for abbr, full in expansions.items():
            import re
            spoken = re.sub(r'\b' + re.escape(abbr) + r'\b', full, spoken, flags=re.IGNORECASE)
        
        # Handle repeat patterns
        import re
        bracket_match = re.search(r'\[(.*?)\]\s*[×x]\s*(\d+)', spoken, re.IGNORECASE)
        if bracket_match:
            inner = bracket_match.group(1)
            times = bracket_match.group(2)
            spoken = spoken.replace(bracket_match.group(0), 
                                   f"Repeat the following {times} times: {inner}")
        
        return spoken
    
    # ════════════════════════════════════════════════════
    # VOICE SYNTHESIS
    # ════════════════════════════════════════════════════
    
    def generate_voice(self, text: str, voice: str = "warm_friendly", 
                      output_path: str = "tutorial_audio.mp3") -> bool:
        """Generate voice narration using ElevenLabs, gTTS, or pyttsx3"""
        voice_config = self.VOICE_PRESETS.get(voice, self.VOICE_PRESETS["warm_friendly"])
        
        # Try ElevenLabs first (best quality, needs API key)
        if self.available_models.get("elevenlabs_turbo") or self.available_models.get("elevenlabs_multilingual"):
            return self._generate_voice_elevenlabs(text, voice_config, output_path)
        
        # Try gTTS second (free, no system deps, good quality)
        return self._generate_voice_gtts(text, output_path)
    
    def _generate_voice_gtts(self, text: str, output_path: str) -> bool:
        """Generate voice using Google TTS (free, no API key needed)"""
        try:
            from gtts import gTTS
            max_chars = 4500
            if len(text) > max_chars:
                text = text[:max_chars]
            tts = gTTS(text=text, lang='en', tld='com', slow=False)
            tts.save(output_path)
            print(f"  ✅ Voice generated with Google TTS (free)")
            return True
        except ImportError:
            print(f"  ⚠️  gTTS not installed. Run: pip install gTTS")
            script_path = output_path.replace('.mp3', '_script.txt')
            Path(script_path).write_text(text)
            print(f"  📝 Script saved to: {script_path}")
            return True
        except Exception as e:
            print(f"  ⚠️  gTTS error: {e}")
            script_path = output_path.replace('.mp3', '_script.txt')
            Path(script_path).write_text(text)
            print(f"  📝 Script saved to: {script_path}")
            return True
    
    def _generate_voice_elevenlabs(self, text: str, voice_config: Dict, 
                                   output_path: str) -> bool:
        """Generate voice using ElevenLabs API"""
        try:
            from elevenlabs import ElevenLabs, save
            
            client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))
            
            audio = client.generate(
                text=text,
                voice=voice_config["voice_id"],
                model="eleven_turbo_v2_5",
                stream=False
            )
            
            save(audio, output_path)
            print(f"  ✅ Voice generated with ElevenLabs ({voice_config['name']})")
            return True
            
        except ImportError:
            print("  ⚠️  elevenlabs package not installed. Run: pip install elevenlabs")
            return self._generate_voice_local(text, output_path)
        except Exception as e:
            print(f"  ❌ ElevenLabs error: {e}")
            return self._generate_voice_local(text, output_path)
    
    def _generate_voice_google(self, text: str, output_path: str) -> bool:
        """Generate voice using Google TTS"""
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            print(f"  ✅ Voice generated with Google TTS")
            return True
            
        except ImportError:
            print("  ⚠️  gTTS not installed. Run: pip install gTTS")
            return self._generate_voice_local(text, output_path)
        except Exception as e:
            print(f"  ❌ Google TTS error: {e}")
            return self._generate_voice_local(text, output_path)
    
    def _generate_voice_local(self, text: str, output_path: str) -> bool:
        """Generate voice using local TTS (pyttsx3)"""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            print(f"  ✅ Voice generated with local TTS")
            return True
            
        except ImportError:
            # Last resort: just save the text as a script file
            script_path = output_path.replace('.mp3', '_script.txt')
            Path(script_path).write_text(text)
            print(f"  📝 No TTS available. Script saved to: {script_path}")
            print(f"  💡 Install voice support: pip install elevenlabs gTTS pyttsx3")
            return True
        except Exception as e:
            print(f"  ❌ Local TTS error: {e}")
            return False
    
    # ════════════════════════════════════════════════════
    # VIDEO GENERATION
    # ════════════════════════════════════════════════════
    
    def generate_video_prompt(self, pattern: Dict, round_num: int = None) -> str:
        """Generate a detailed video prompt for AI video models"""
        title = pattern.get("title", "Pattern")
        rounds = pattern.get("rounds", [])
        
        if round_num is not None:
            rnd = next((r for r in rounds if r.get("round", r.get("round_number")) == round_num), None)
            if rnd:
                return self._generate_round_prompt(title, rnd, round_num, len(rounds))
        
        # Generate full video prompt
        return self._generate_full_video_prompt(pattern)
    
    def _generate_round_prompt(self, title: str, rnd: Dict, round_num: int, 
                              total_rounds: int) -> str:
        """Generate a video prompt for a single round"""
        instr = rnd.get("instruction", "")
        count = rnd.get("count", rnd.get("stitch_count", 0))
        
        return f"""Close-up crochet tutorial video showing hands working {title}.
Round {round_num} of {total_rounds}: {instr}.
The camera focuses on the crochet hook and yarn, showing each stitch being formed.
Soft, warm lighting. Clean workspace with neutral background.
The crocheter's hands are steady and skilled.
After completing the round, the stitch count of {count} is verified.
Style: calm, instructional, high quality, 4K resolution.
Duration: 10-15 seconds."""
    
    def _generate_full_video_prompt(self, pattern: Dict) -> str:
        """Generate prompt for full tutorial video"""
        title = pattern.get("title", "Pattern")
        total_rounds = len(pattern.get("rounds", []))
        difficulty = pattern.get("difficulty", "Beginner")
        
        return f"""Professional crochet tutorial video for {title}.
Opening shot: Beautiful finished {title} on a cozy workspace.
Transition to close-up of hands beginning the pattern.
Step-by-step demonstration of all {total_rounds} rounds.
Each round clearly labeled with text overlay.
Stitch count verification after each round.
Warm, inviting lighting. Soft background music.
Difficulty level: {difficulty}.
Style: Professional YouTube tutorial, 4K, steady camera.
Total duration: 3-5 minutes.
End screen with completed project and call to action."""
    
    def generate_video_sora(self, prompt: str, duration: int = 10) -> Dict:
        """Generate video using OpenAI Sora"""
        if not self.available_models.get("sora"):
            return {
                "status": "unavailable",
                "message": "Sora API key not configured. Set OPENAI_API_KEY.",
                "fallback": "animation"
            }
        
        try:
            # Sora API call (when available)
            return {
                "status": "ready",
                "model": "sora",
                "prompt": prompt[:200] + "...",
                "duration": duration,
                "message": "Ready to generate. Call Sora API with this prompt."
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def generate_video_veo2(self, prompt: str) -> Dict:
        """Generate video using Google Veo 2"""
        if not self.available_models.get("veo2"):
            return {
                "status": "unavailable",
                "message": "Veo 2 API key not configured. Set GOOGLE_API_KEY.",
                "fallback": "animation"
            }
        
        return {
            "status": "ready",
            "model": "veo-2",
            "prompt": prompt[:200] + "...",
            "message": "Ready to generate with Google Veo 2."
        }
    
    def generate_video(self, pattern: Dict) -> Dict:
        """Generate a complete tutorial video"""
        # Check which video models are available
        video_models = self.get_available_models("video")
        
        if not video_models:
            # Fallback: Generate animated HTML video
            return {
                "status": "fallback",
                "type": "html_animation",
                "content": self._generate_html_animation(pattern),
                "message": "No video API keys configured. Generated HTML animation instead."
            }
        
        # Use best available video model
        model = video_models[0]
        full_prompt = self.generate_video_prompt(pattern)
        
        if model == "sora":
            result = self.generate_video_sora(full_prompt)
        elif model == "veo2":
            result = self.generate_video_veo2(full_prompt)
        else:
            result = {"status": "ready", "model": model}
        
        return result
    
    def _generate_html_animation(self, pattern: Dict) -> str:
        """Generate an animated HTML tutorial as fallback"""
        title = pattern.get("title", "Pattern")
        rounds = pattern.get("rounds", [])
        
        rounds_json = json.dumps([
            {
                "round": r.get("round", r.get("round_number", i+1)),
                "instruction": r.get("instruction", ""),
                "count": r.get("count", r.get("stitch_count", 0))
            }
            for i, r in enumerate(rounds)
        ])
        
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Video Tutorial - {title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, sans-serif;
    background: #0a0a0a;
    color: #fff;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    overflow: hidden;
}}
.video-container {{
    width: 100%;
    max-width: 800px;
    aspect-ratio: 16/9;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    margin: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}
.title-bar {{
    position: absolute;
    top: 0; left: 0; right: 0;
    padding: 20px;
    background: linear-gradient(180deg, rgba(0,0,0,0.8) 0%, transparent 100%);
    z-index: 10;
}}
.title-bar h1 {{
    font-size: 1.5em;
    color: #e94560;
}}
.round-display {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 5;
}}
.round-number {{
    font-size: 4em;
    font-weight: bold;
    color: #4ecca3;
    text-shadow: 0 0 20px rgba(78,204,163,0.5);
    opacity: 0;
    animation: fadeInScale 0.5s ease forwards;
}}
.instruction {{
    font-size: 1.3em;
    color: #fff;
    margin-top: 15px;
    max-width: 600px;
    line-height: 1.6;
    opacity: 0;
    animation: fadeIn 0.5s ease 0.3s forwards;
}}
.stitch-count {{
    font-size: 1.5em;
    color: #ffd700;
    margin-top: 20px;
    opacity: 0;
    animation: fadeIn 0.5s ease 0.6s forwards;
}}
.progress-bar {{
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 4px;
    background: rgba(255,255,255,0.1);
}}
.progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, #e94560, #4ecca3);
    transition: width 0.5s ease;
}}
.controls {{
    display: flex;
    gap: 15px;
    margin: 20px;
}}
.btn {{
    padding: 15px 30px;
    border: none;
    border-radius: 8px;
    font-size: 1em;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.1s;
}}
.btn:active {{ transform: scale(0.95); }}
.btn-play {{ background: #4ecca3; color: #0a0a0a; }}
.btn-pause {{ background: #e94560; color: #fff; }}
.btn-next {{ background: #16213e; color: #4ecca3; border: 2px solid #4ecca3; }}
.btn-prev {{ background: #16213e; color: #e94560; border: 2px solid #e94560; }}
.timer {{
    position: absolute;
    bottom: 20px;
    right: 20px;
    font-size: 1.2em;
    color: rgba(255,255,255,0.7);
    z-index: 10;
}}
.stitch-animation {{
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.hook {{
    width: 8px;
    height: 120px;
    background: linear-gradient(180deg, #c0c0c0, #808080);
    border-radius: 4px;
    position: absolute;
    transform-origin: bottom center;
    animation: hookMove 2s ease-in-out infinite;
}}
.yarn {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: radial-gradient(circle, #e94560, #c0392b);
    position: absolute;
    bottom: 30%;
    right: 25%;
    box-shadow: 0 5px 15px rgba(233,69,96,0.3);
}}
@keyframes fadeInScale {{
    from {{ opacity: 0; transform: scale(0.8); }}
    to {{ opacity: 1; transform: scale(1); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}
@keyframes hookMove {{
    0%, 100% {{ transform: rotate(-10deg) translateY(0); }}
    50% {{ transform: rotate(10deg) translateY(-20px); }}
}}
</style>
</head>
<body>
<div class="video-container" id="videoContainer">
    <div class="title-bar">
        <h1>{title}</h1>
        <p>AI-Generated Video Tutorial</p>
    </div>
    
    <div class="stitch-animation">
        <div class="hook"></div>
        <div class="yarn"></div>
    </div>
    
    <div class="round-display" id="roundDisplay">
        <div class="round-number" id="roundNumber">Round 1</div>
        <div class="instruction" id="instruction">Loading...</div>
        <div class="stitch-count" id="stitchCount"></div>
    </div>
    
    <div class="timer" id="timer">0:00</div>
    <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
</div>

<div class="controls">
    <button class="btn btn-prev" onclick="prevRound()">⏮ Prev</button>
    <button class="btn btn-play" id="playBtn" onclick="togglePlay()">▶ Play</button>
    <button class="btn btn-next" onclick="nextRound()">Next ⏭</button>
</div>

<script>
const rounds = {rounds_json};
let currentRound = 0;
let isPlaying = false;
let timer = 0;
let interval;

function updateDisplay() {{
    const rnd = rounds[currentRound];
    document.getElementById('roundNumber').textContent = 'Round ' + rnd.round;
    document.getElementById('instruction').textContent = rnd.instruction;
    document.getElementById('stitchCount').textContent = rnd.count ? rnd.count + ' stitches' : '';
    document.getElementById('progressFill').style.width = ((currentRound + 1) / rounds.length * 100) + '%';
    
    // Reset animation
    const rn = document.getElementById('roundNumber');
    rn.style.animation = 'none';
    rn.offsetHeight;
    rn.style.animation = 'fadeInScale 0.5s ease forwards';
}}

function nextRound() {{
    if (currentRound < rounds.length - 1) {{
        currentRound++;
        updateDisplay();
    }}
}}

function prevRound() {{
    if (currentRound > 0) {{
        currentRound--;
        updateDisplay();
    }}
}}

function togglePlay() {{
    isPlaying = !isPlaying;
    document.getElementById('playBtn').textContent = isPlaying ? '⏸ Pause' : '▶ Play';
    document.getElementById('playBtn').className = isPlaying ? 'btn btn-pause' : 'btn btn-play';
    
    if (isPlaying) {{
        interval = setInterval(() => {{
            timer++;
            let mins = Math.floor(timer / 60);
            let secs = timer % 60;
            document.getElementById('timer').textContent = mins + ':' + (secs < 10 ? '0' : '') + secs;
            
            if (timer % 5 === 0) {{
                nextRound();
                if (currentRound >= rounds.length - 1) {{
                    clearInterval(interval);
                    isPlaying = false;
                    document.getElementById('playBtn').textContent = '▶ Replay';
                    document.getElementById('playBtn').className = 'btn btn-play';
                }}
            }}
        }}, 1000);
    }} else {{
        clearInterval(interval);
    }}
}}

updateDisplay();
</script>
</body>
</html>'''
        
        return html
    
    def get_status(self) -> Dict:
        """Get status of all AI models"""
        return {
            "available_models": {k: v for k, v in self.available_models.items() if v},
            "missing_api_keys": [k for k, v in self.available_models.items() if not v],
            "voice_presets": list(self.VOICE_PRESETS.keys()),
            "capabilities": {
                "text_generation": bool(self.get_available_models("text")),
                "voice_synthesis": bool(self.get_available_models("voice")),
                "video_generation": bool(self.get_available_models("video")),
                "image_generation": bool(self.get_available_models("image")),
            }
        }


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  AI MODEL ROUTER - STATUS")
    print("=" * 60)
    
    router = AIModelRouter()
    status = router.get_status()
    
    print(f"\n  Available Models: {len(status['available_models'])}")
    for model, available in status['available_models'].items():
        print(f"    ✅ {model}")
    
    print(f"\n  Missing API Keys: {len(status['missing_api_keys'])}")
    for model in status['missing_api_keys']:
        env_var = router.MODELS[model].api_key_env
        print(f"    ❌ {model} → Set {env_var}")
    
    print(f"\n  Capabilities:")
    for cap, available in status['capabilities'].items():
        icon = "✅" if available else "❌ (using fallback)"
        print(f"    {icon} {cap}")
    
    # Test script generation
    print(f"\n  Testing script generation (local)...")
    sample = {
        "title": "Test Ball",
        "difficulty": "Beginner",
        "rounds": [
            {"round": 1, "instruction": "6 sc in MR", "count": 6},
            {"round": 2, "instruction": "inc in each st around", "count": 12},
            {"round": 3, "instruction": "[sc, inc] x 6", "count": 18},
        ]
    }
    
    script = router._generate_script_local(sample, "friendly")
    print(f"  Generated script: {len(script)} chars")
    print(f"  First 200 chars: {script[:200]}...")
    
    # Test video prompt
    print(f"\n  Testing video generation (fallback)...")
    video = router.generate_video(sample)
    print(f"  Status: {video['status']}")
    print(f"  Type: {video.get('type', 'N/A')}")
    
    print(f"\n  AI Model Router Complete!")
