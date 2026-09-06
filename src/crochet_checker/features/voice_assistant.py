"""
Voice Assistant - Read patterns aloud, voice commands, hands-free crochet help
"""
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class VoiceCommand:
    command: str
    action: str
    aliases: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class ReadingSession:
    pattern_name: str
    current_round: int = 1
    total_rounds: int = 0
    reading_speed: str = "normal"  # slow, normal, fast
    auto_advance: bool = False
    repeat_count: int = 0
    notes: List[str] = field(default_factory=list)
    started_at: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class VoiceAssistant:
    """
    Voice assistant for hands-free crochet help
    
    Features:
    - Read patterns aloud round by round
    - Voice commands (next round, repeat, pause)
    - Speed control
    - Auto-advance mode
    - Text-to-speech output
    - Voice command recognition
    - Pattern bookmarking
    """
    
    COMMANDS = [
        VoiceCommand("next", "next_round", ["n", "next round", "continue"], "Go to next round"),
        VoiceCommand("previous", "prev_round", ["p", "prev", "back", "go back"], "Go to previous round"),
        VoiceCommand("repeat", "repeat_round", ["again", "say again", "one more time"], "Repeat current round"),
        VoiceCommand("pause", "pause", ["stop", "wait", "hold on"], "Pause reading"),
        VoiceCommand("resume", "resume", ["go", "continue reading"], "Resume reading"),
        VoiceCommand("speed up", "faster", ["faster", "quicker"], "Increase reading speed"),
        VoiceCommand("slow down", "slower", ["slower", "slow down"], "Decrease reading speed"),
        VoiceCommand("round", "jump_round", ["go to round", "jump to"], "Jump to specific round"),
        VoiceCommand("status", "status", ["where am i", "progress", "how far"], "Show current position"),
        VoiceCommand("count", "count_stitches", ["how many", "stitch count"], "Show stitch count"),
        VoiceCommand("help", "help", ["commands", "what can you do"], "Show available commands"),
        VoiceCommand("stop", "stop_session", ["exit", "quit", "done"], "End reading session"),
        VoiceCommand("note", "add_note", ["remember", "make a note"], "Add a note for current round"),
        VoiceCommand("bookmark", "bookmark", ["save place", "mark"], "Bookmark current position"),
    ]
    
    SPEED_SETTINGS = {
        "slow": {"wpm": 100, "pause_between_rounds": 3.0},
        "normal": {"wpm": 150, "pause_between_rounds": 2.0},
        "fast": {"wpm": 200, "pause_between_rounds": 1.0},
    }
    
    def __init__(self):
        self.session: Optional[ReadingSession] = None
        self.pattern_data: Dict = {}
        self.rounds: List[Dict] = []
        self.is_paused = False
        self.bookmarks: Dict[str, int] = {}
        self.history: List[Dict] = []
    
    def load_pattern(self, pattern: Dict) -> str:
        """Load a pattern for reading"""
        self.pattern_data = pattern
        self.rounds = pattern.get("rounds", [])
        title = pattern.get("title", pattern.get("name", "Untitled Pattern"))
        
        self.session = ReadingSession(
            pattern_name=title,
            total_rounds=len(self.rounds),
            started_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return self._format_announcement(
            f"Loaded: {title}. {len(self.rounds)} rounds. "
            f"Starting from Round 1. Say 'next' to continue."
        )
    
    def get_current_round_text(self) -> str:
        """Get the text for the current round"""
        if not self.session or not self.rounds:
            return "No pattern loaded."
        
        idx = self.session.current_round - 1
        if 0 <= idx < len(self.rounds):
            rnd = self.rounds[idx]
            rn = rnd.get("round_number", rnd.get("round", self.session.current_round))
            instr = rnd.get("instruction", "")
            count = rnd.get("stitch_count", rnd.get("count", 0))
            
            text = f"Round {rn}. {instr}"
            if count:
                text += f". That gives you {count} stitches."
            
            return text
        
        return "No more rounds."
    
    def next_round(self) -> str:
        """Move to next round"""
        if not self.session:
            return "No pattern loaded. Say 'load pattern' first."
        
        if self.session.current_round >= self.session.total_rounds:
            return self._format_announcement(
                f"Congratulations! You've completed all {self.session.total_rounds} rounds "
                f"of {self.session.pattern_name}!"
            )
        
        self.session.current_round += 1
        self.history.append({
            "action": "next",
            "round": self.session.current_round,
            "timestamp": time.strftime("%H:%M:%S")
        })
        
        text = self.get_current_round_text()
        
        if self.session.current_round == self.session.total_rounds:
            text += " This is the final round!"
        
        return self._format_announcement(text)
    
    def previous_round(self) -> str:
        """Go back to previous round"""
        if not self.session:
            return "No pattern loaded."
        
        if self.session.current_round <= 1:
            return "Already at Round 1."
        
        self.session.current_round -= 1
        return self._format_announcement(self.get_current_round_text())
    
    def repeat_round(self) -> str:
        """Repeat current round"""
        if not self.session:
            return "No pattern loaded."
        
        self.session.repeat_count += 1
        return self._format_announcement(f"Repeating: {self.get_current_round_text()}")
    
    def jump_to_round(self, round_num: int) -> str:
        """Jump to a specific round"""
        if not self.session:
            return "No pattern loaded."
        
        if 1 <= round_num <= self.session.total_rounds:
            self.session.current_round = round_num
            return self._format_announcement(
                f"Jumped to Round {round_num}. {self.get_current_round_text()}"
            )
        
        return f"Invalid round. Pattern has {self.session.total_rounds} rounds."
    
    def get_status(self) -> str:
        """Get current reading status"""
        if not self.session:
            return "No pattern loaded."
        
        progress = (self.session.current_round / self.session.total_rounds * 100) 
        return self._format_announcement(
            f"Reading: {self.session.pattern_name}. "
            f"Round {self.session.current_round} of {self.session.total_rounds}. "
            f"Progress: {progress:.0f}%. "
            f"Speed: {self.session.reading_speed}."
        )
    
    def get_stitch_count(self) -> str:
        """Get current stitch count"""
        if not self.session or not self.rounds:
            return "No pattern loaded."
        
        idx = self.session.current_round - 1
        if 0 <= idx < len(self.rounds):
            rnd = self.rounds[idx]
            count = rnd.get("stitch_count", rnd.get("count", 0))
            rn = rnd.get("round_number", rnd.get("round", self.session.current_round))
            return self._format_announcement(
                f"Round {rn} has {count} stitches."
            )
        return "No round data available."
    
    def change_speed(self, direction: str) -> str:
        """Change reading speed"""
        if not self.session:
            return "No pattern loaded."
        
        speeds = ["slow", "normal", "fast"]
        current_idx = speeds.index(self.session.reading_speed)
        
        if direction == "faster" and current_idx < 2:
            self.session.reading_speed = speeds[current_idx + 1]
        elif direction == "slower" and current_idx > 0:
            self.session.reading_speed = speeds[current_idx - 1]
        
        return self._format_announcement(f"Speed set to {self.session.reading_speed}.")
    
    def add_note(self, note: str) -> str:
        """Add a note for the current round"""
        if not self.session:
            return "No pattern loaded."
        
        self.session.notes.append(
            f"Round {self.session.current_round}: {note}"
        )
        return self._format_announcement(f"Note saved for Round {self.session.current_round}.")
    
    def set_bookmark(self, name: str = "") -> str:
        """Bookmark current position"""
        if not self.session:
            return "No pattern loaded."
        
        bookmark_name = name or f"bookmark_{len(self.bookmarks) + 1}"
        self.bookmarks[bookmark_name] = self.session.current_round
        return self._format_announcement(
            f"Bookmarked Round {self.session.current_round} as '{bookmark_name}'."
        )
    
    def goto_bookmark(self, name: str) -> str:
        """Jump to a bookmark"""
        if name in self.bookmarks:
            self.session.current_round = self.bookmarks[name]
            return self._format_announcement(
                f"Jumped to bookmark '{name}' at Round {self.session.current_round}."
            )
        return f"Bookmark '{name}' not found."
    
    def get_help(self) -> str:
        """Get list of available commands"""
        lines = ["Available voice commands:"]
        for cmd in self.COMMANDS:
            aliases = ", ".join(cmd.aliases[:3])
            lines.append(f"  - {cmd.command} ({aliases}): {cmd.description}")
        return self._format_announcement("\n".join(lines))
    
    def process_command(self, command: str) -> str:
        """Process a voice command"""
        cmd_lower = command.lower().strip()
        
        for vc in self.COMMANDS:
            if cmd_lower == vc.command.lower() or cmd_lower in [a.lower() for a in vc.aliases]:
                action = vc.action
                
                if action == "next_round":
                    return self.next_round()
                elif action == "prev_round":
                    return self.previous_round()
                elif action == "repeat_round":
                    return self.repeat_round()
                elif action == "pause":
                    self.is_paused = True
                    return "Paused. Say 'resume' to continue."
                elif action == "resume":
                    self.is_paused = False
                    return "Resumed."
                elif action == "faster":
                    return self.change_speed("faster")
                elif action == "slower":
                    return self.change_speed("slower")
                elif action == "status":
                    return self.get_status()
                elif action == "count_stitches":
                    return self.get_stitch_count()
                elif action == "help":
                    return self.get_help()
                elif action == "stop_session":
                    return self._end_session()
                elif action == "bookmark":
                    return self.set_bookmark()
        
        return f"I didn't understand '{command}'. Say 'help' for commands."
    
    def _format_announcement(self, text: str) -> str:
        """Format text for speech output"""
        return text
    
    def _end_session(self) -> str:
        """End the reading session"""
        if not self.session:
            return "No active session."
        
        summary = (
            f"Session complete. You worked on {self.session.pattern_name}, "
            f"reached Round {self.session.current_round} of {self.session.total_rounds}. "
            f"Repeat requests: {self.session.repeat_count}."
        )
        
        if self.session.notes:
            summary += f" You left {len(self.session.notes)} notes."
        
        self.session = None
        return summary
    
    def generate_reading_script(self, pattern: Dict) -> str:
        """Generate a complete reading script for TTS"""
        lines = []
        title = pattern.get("title", "Pattern")
        rounds = pattern.get("rounds", [])
        
        lines.append(f"Welcome to {title}.")
        lines.append(f"This pattern has {len(rounds)} rounds.")
        lines.append("")
        
        # Materials
        materials = pattern.get("materials", {})
        if materials:
            lines.append("Materials needed:")
            for k, v in materials.items():
                lines.append(f"  {k.replace('_', ' ')}: {v}")
            lines.append("")
        
        # Rounds
        lines.append("Let's begin!")
        lines.append("")
        
        for rnd in rounds:
            rn = rnd.get("round_number", rnd.get("round", 0))
            instr = rnd.get("instruction", "")
            count = rnd.get("stitch_count", rnd.get("count", 0))
            
            lines.append(f"Round {rn}.")
            lines.append(f"{instr}.")
            if count:
                lines.append(f"You should have {count} stitches.")
            lines.append("")
            lines.append("Pause here. Say 'next' when ready.")
            lines.append("")
        
        lines.append("Congratulations! You've completed the pattern!")
        
        return "\n".join(lines)


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  VOICE ASSISTANT - DEMONSTRATION")
    print("=" * 60)
    
    assistant = VoiceAssistant()
    
    sample = {
        "title": "Simple Amigurumi Ball",
        "rounds": [
            {"round": 1, "instruction": "6 sc in magic ring", "count": 6},
            {"round": 2, "instruction": "increase in each stitch around", "count": 12},
            {"round": 3, "instruction": "single crochet, increase repeat around", "count": 18},
            {"round": 4, "instruction": "2 single crochet, increase repeat around", "count": 24},
            {"round": 5, "instruction": "single crochet in each stitch around", "count": 24},
            {"round": 6, "instruction": "single crochet, decrease repeat around", "count": 18},
            {"round": 7, "instruction": "2 single crochet, decrease repeat around", "count": 12},
            {"round": 8, "instruction": "decrease repeat around", "count": 6},
        ]
    }
    
    # Load pattern
    print(f"\n{assistant.load_pattern(sample)}")
    
    # Simulate voice commands
    commands = ["next", "next", "status", "count", "next", "repeat", 
                "slow down", "next", "note: stuff firmly here", "next", "next", "next"]
    
    print(f"\n--- Simulating Voice Commands ---")
    for cmd in commands:
        response = assistant.process_command(cmd)
        print(f"\n  User: \"{cmd}\"")
        print(f"  Assistant: {response}")
    
    # Generate full reading script
    print(f"\n--- Reading Script (for TTS) ---")
    script = assistant.generate_reading_script(sample)
    print(script[:500])
    
    print(f"\n  Voice Assistant Complete!")
