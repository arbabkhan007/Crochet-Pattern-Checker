"""
Voice-Controlled Pattern Reader - Hands-free pattern reading while crocheting
"""
import json
from typing import List, Dict
from pathlib import Path


class VoicePatternReader:
    """Read crochet patterns aloud with voice control"""
    
    def __init__(self):
        self.patterns = []
        self.current_position = 0
        self.speed = "normal"  # slow, normal, fast
        self.voice_enabled = True
    
    def load_pattern(self, pattern_text: str) -> List[str]:
        """Parse pattern into readable steps"""
        lines = []
        for line in pattern_text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Clean up for voice reading
                line = line.replace('sc', 'single crochet')
                line = line.replace('dc', 'double crochet')
                line = line.replace('hdc', 'half double crochet')
                line = line.replace('ch', 'chain')
                line = line.replace('sl st', 'slip stitch')
                line = line.replace('st', 'stitch')
                line = line.replace('sts', 'stitches')
                line = line.replace('rep', 'repeat')
                line = line.replace('inc', 'increase')
                line = line.replace('dec', 'decrease')
                lines.append(line)
        self.patterns = lines
        self.current_position = 0
        return lines
    
    def get_current_step(self) -> str:
        """Get current step to read"""
        if self.current_position < len(self.patterns):
            return self.patterns[self.current_position]
        return "Pattern complete! Great job!"
    
    def next_step(self) -> str:
        """Move to next step"""
        self.current_position += 1
        return self.get_current_step()
    
    def previous_step(self) -> str:
        """Go back one step"""
        if self.current_position > 0:
            self.current_position -= 1
        return self.get_current_step()
    
    def repeat_current(self) -> str:
        """Repeat current step"""
        return self.get_current_step()
    
    def jump_to_row(self, row_number: int) -> str:
        """Jump to specific row"""
        for i, line in enumerate(self.patterns):
            if f"row {row_number}" in line.lower() or f"round {row_number}" in line.lower():
                self.current_position = i
                return self.get_current_step()
        return f"Row {row_number} not found"
    
    def get_progress(self) -> Dict:
        """Get current progress"""
        total = len(self.patterns)
        current = self.current_position
        return {
            "current": current + 1,
            "total": total,
            "percent": (current / total * 100) if total > 0 else 0,
            "remaining": total - current
        }
    
    def generate_audio_script(self) -> str:
        """Generate script for text-to-speech"""
        script = "Welcome to your crochet pattern! I'll read each step for you.\n\n"
        for i, step in enumerate(self.patterns, 1):
            script += f"Step {i}: {step}\n\n"
        script += "Pattern complete! You did an amazing job!"
        return script
    
    def create_tts_commands(self) -> List[str]:
        """Generate say commands for macOS or espeak for Linux"""
        commands = []
        for step in self.patterns:
            # Clean text for TTS
            clean = step.replace('"', '').replace("'", "")
            commands.append(f'say "{clean}"')  # macOS
            # For Linux: commands.append(f'espeak "{clean}"')
        return commands


if __name__ == "__main__":
    print("🎙️ Voice-Controlled Pattern Reader")
    print("=" * 50)
    
    reader = VoicePatternReader()
    
    # Sample pattern
    pattern = """
    Row 1: Ch 20, sc in 2nd ch from hook and each ch across
    Row 2: Ch 1, turn, sc in each st across
    Row 3: Ch 1, turn, hdc in each st across
    Row 4: Ch 3, turn, dc in each st across
    Row 5: Ch 1, turn, sc in each st across
    """
    
    print("\n📖 Loading pattern...")
    steps = reader.load_pattern(pattern)
    print(f"Loaded {len(steps)} steps")
    
    print("\n🎯 First step:")
    print(reader.get_current_step())
    
    print("\n▶️ Next step:")
    print(reader.next_step())
    
    print("\n🔁 Repeat:")
    print(reader.repeat_current())
    
    print("\n⏭️ Next:")
    print(reader.next_step())
    
    print("\n📊 Progress:")
    progress = reader.get_progress()
    print(f"Step {progress['current']} of {progress['total']} ({progress['percent']:.1f}%)")
    
    print("\n🔊 TTS Commands (first 3):")
    commands = reader.create_tts_commands()
    for cmd in commands[:3]:
        print(f"  {cmd}")
    
    print("\n✅ Voice Pattern Reader ready!")
