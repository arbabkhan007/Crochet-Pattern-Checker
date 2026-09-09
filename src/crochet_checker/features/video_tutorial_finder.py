"""
Video Tutorial Finder - Auto-find video tutorials for stitches and techniques
"""
import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Tutorial:
    title: str
    url: str
    platform: str
    duration: str
    difficulty: str
    topic: str
    channel: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class VideoTutorialFinder:
    """
    Find video tutorials for crochet stitches and techniques
    
    Features:
    - Auto-detect stitches needing tutorials
    - Search by stitch type
    - Difficulty-appropriate recommendations
    - Playlist generation
    - Technique breakdown
    """
    
    TUTORIAL_DATABASE = {
        # Basic stitches
        "magic ring": [
            {"title": "Magic Ring Tutorial - Beginner Friendly", "url": "https://youtube.com/results?search_query=magic+ring+crochet+tutorial", "duration": "3:30", "difficulty": "Beginner", "channel": "Crochet School"},
            {"title": "Magic Ring vs Chain Ring", "url": "https://youtube.com/results?search_query=magic+ring+vs+chain+ring", "duration": "5:00", "difficulty": "Beginner", "channel": "Hooked on Happiness"},
        ],
        "sc": [
            {"title": "Single Crochet for Absolute Beginners", "url": "https://youtube.com/results?search_query=single+crochet+tutorial+beginner", "duration": "4:15", "difficulty": "Beginner", "channel": "Bella Coco"},
        ],
        "dc": [
            {"title": "Double Crochet Stitch Tutorial", "url": "https://youtube.com/results?search_query=double+crochet+tutorial", "duration": "4:45", "difficulty": "Beginner", "channel": "Bella Coco"},
        ],
        "hdc": [
            {"title": "Half Double Crochet Tutorial", "url": "https://youtube.com/results?search_query=half+double+crochet+tutorial", "duration": "3:50", "difficulty": "Beginner", "channel": "TL Yarn Crafts"},
        ],
        "inc": [
            {"title": "How to Increase in Crochet", "url": "https://youtube.com/results?search_query=crochet+increase+tutorial", "duration": "2:30", "difficulty": "Beginner", "channel": "Crochet Ever After"},
        ],
        "dec": [
            {"title": "Invisible Decrease for Amigurumi", "url": "https://youtube.com/results?search_query=invisible+decrease+amigurumi", "duration": "3:15", "difficulty": "Beginner", "channel": "Snappy Tots"},
        ],
        "sl st": [
            {"title": "Slip Stitch Tutorial", "url": "https://youtube.com/results?search_query=slip+stitch+crochet+tutorial", "duration": "2:45", "difficulty": "Beginner", "channel": "Bella Coco"},
        ],
        # Intermediate
        "granny square": [
            {"title": "Classic Granny Square Tutorial", "url": "https://youtube.com/results?search_query=granny+square+tutorial+step+by+step", "duration": "12:00", "difficulty": "Beginner", "channel": "Bella Coco"},
            {"title": "Joining Granny Squares", "url": "https://youtube.com/results?search_query=join+granny+squares+crochet", "duration": "8:30", "difficulty": "Intermediate", "channel": "Crochet Kim"},
        ],
        "amigurumi": [
            {"title": "Amigurumi Basics - Complete Guide", "url": "https://youtube.com/results?search_query=amigurumi+basics+complete+guide", "duration": "25:00", "difficulty": "Beginner", "channel": "Snappy Tots"},
            {"title": "Amigurumi Shaping Techniques", "url": "https://youtube.com/results?search_query=amigurumi+shaping+techniques", "duration": "15:00", "difficulty": "Intermediate", "channel": "Stella's Crochet"},
        ],
        "spiral": [
            {"title": "Working in Spiral vs Joined Rounds", "url": "https://youtube.com/results?search_query=spiral+vs+joined+rounds+crochet", "duration": "6:00", "difficulty": "Beginner", "channel": "Crochet Ever After"},
        ],
        # Advanced
        "cable": [
            {"title": "Crochet Cable Stitch Tutorial", "url": "https://youtube.com/results?search_query=crochet+cable+stitch+tutorial", "duration": "15:00", "difficulty": "Advanced", "channel": "TL Yarn Crafts"},
        ],
        "popcorn": [
            {"title": "Popcorn Stitch Tutorial", "url": "https://youtube.com/results?search_query=popcorn+stitch+crochet+tutorial", "duration": "7:00", "difficulty": "Intermediate", "channel": "Bella Coco"},
        ],
        "bobble": [
            {"title": "Bobble Stitch Made Easy", "url": "https://youtube.com/results?search_query=bobble+stitch+crochet+easy", "duration": "6:30", "difficulty": "Intermediate", "channel": "Hooked on Happiness"},
        ],
        "shell": [
            {"title": "Shell Stitch Tutorial", "url": "https://youtube.com/results?search_query=shell+stitch+crochet+tutorial", "duration": "8:00", "difficulty": "Intermediate", "channel": "Bella Coco"},
        ],
        "color change": [
            {"title": "Clean Color Changes in Crochet", "url": "https://youtube.com/results?search_query=clean+color+change+crochet", "duration": "7:30", "difficulty": "Intermediate", "channel": "TL Yarn Crafts"},
        ],
        "joining": [
            {"title": "Invisible Join Tutorial", "url": "https://youtube.com/results?search_query=invisible+join+crochet", "duration": "4:00", "difficulty": "Intermediate", "channel": "Crochet Ever After"},
        ],
        "weaving ends": [
            {"title": "How to Weave in Ends - 3 Methods", "url": "https://youtube.com/results?search_query=weave+in+ends+crochet+methods", "duration": "8:00", "difficulty": "Beginner", "channel": "Bella Coco"},
        ],
        "blocking": [
            {"title": "How to Block Crochet", "url": "https://youtube.com/results?search_query=how+to+block+crochet+tutorial", "duration": "10:00", "difficulty": "Beginner", "channel": "TL Yarn Crafts"},
        ],
        "gauge": [
            {"title": "Understanding Gauge in Crochet", "url": "https://youtube.com/results?search_query=crochet+gauge+tutorial", "duration": "12:00", "difficulty": "Beginner", "channel": "Bella Coco"},
        ],
    }
    
    def __init__(self):
        self.recommended: List[Dict] = []
    
    def find_tutorials_for_pattern(self, pattern: Dict) -> List[Dict]:
        """Find all tutorials needed for a pattern"""
        tutorials = []
        rounds = pattern.get("rounds", [])
        
        # Extract all stitch types from pattern
        all_text = " ".join(r.get("instruction", "") for r in rounds).lower()
        
        # Check for each known stitch/technique
        found_topics = set()
        
        for topic, topic_tutorials in self.TUTORIAL_DATABASE.items():
            if topic in all_text:
                found_topics.add(topic)
                # Get the most relevant tutorial
                for t in topic_tutorials:
                    difficulty = pattern.get("difficulty", "Beginner")
                    if self._difficulty_match(t["difficulty"], difficulty):
                        tutorials.append({**t, "topic": topic, "reason": f"Used in this pattern"})
                        break
        
        # Check for construction types
        full_text = json.dumps(pattern).lower()
        if "spiral" in full_text and "spiral" not in found_topics:
            tutorials.extend([{**t, "topic": "spiral", "reason": "Pattern uses spiral rounds"} 
                            for t in self.TUTORIAL_DATABASE.get("spiral", [])[:1]])
        
        if "granny" in full_text and "granny square" not in found_topics:
            tutorials.extend([{**t, "topic": "granny square", "reason": "Pattern uses granny square"} 
                            for t in self.TUTORIAL_DATABASE.get("granny square", [])[:1]])
        
        if "amigurumi" in full_text or ("stuff" in full_text and "mr" in all_text):
            tutorials.extend([{**t, "topic": "amigurumi", "reason": "Amigurumi technique needed"} 
                            for t in self.TUTORIAL_DATABASE.get("amigurumi", [])[:1]])
        
        return tutorials
    
    def find_by_stitch(self, stitch: str) -> List[Dict]:
        """Find tutorials for a specific stitch"""
        stitch_lower = stitch.lower()
        results = []
        
        for topic, tutorials in self.TUTORIAL_DATABASE.items():
            if stitch_lower in topic or topic in stitch_lower:
                results.extend([{**t, "topic": topic} for t in tutorials])
        
        if not results:
            # Generate search URL
            results.append({
                "title": f"Search: {stitch} tutorial",
                "url": f"https://youtube.com/results?search_query={stitch.replace(' ', '+')}+crochet+tutorial",
                "platform": "YouTube",
                "duration": "varies",
                "difficulty": "varies",
                "topic": stitch,
                "channel": "search"
            })
        
        return results
    
    def generate_playlist(self, pattern: Dict, difficulty_filter: str = "all") -> Dict:
        """Generate a learning playlist for a pattern"""
        tutorials = self.find_tutorials_for_pattern(pattern)
        
        if difficulty_filter != "all":
            tutorials = [t for t in tutorials if t["difficulty"].lower() == difficulty_filter.lower()]
        
        # Sort by difficulty then duration
        diff_order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
        tutorials.sort(key=lambda t: (diff_order.get(t["difficulty"], 1), t["duration"]))
        
        total_duration = self._parse_total_duration(tutorials)
        
        return {
            "name": f"Learn: {pattern.get('title', 'Pattern')}",
            "tutorials": tutorials,
            "total_tutorials": len(tutorials),
            "estimated_total_duration": total_duration,
            "difficulty_range": self._get_difficulty_range(tutorials),
        }
    
    def get_stitch_glossary(self) -> Dict[str, List[Dict]]:
        """Get full stitch glossary with tutorials"""
        return self.TUTORIAL_DATABASE
    
    def _difficulty_match(self, tutorial_diff: str, pattern_diff: str) -> bool:
        """Check if tutorial difficulty is appropriate"""
        levels = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
        t_level = levels.get(tutorial_diff, 0)
        p_level = levels.get(pattern_diff, 0)
        return t_level <= p_level + 1  # Allow one level above
    
    def _parse_total_duration(self, tutorials: List[Dict]) -> str:
        """Calculate total duration"""
        total_minutes = 0
        for t in tutorials:
            dur = t.get("duration", "0:00")
            parts = dur.split(":")
            if len(parts) == 2:
                try:
                    total_minutes += int(parts[0]) + int(parts[1]) / 60
                except ValueError:
                    pass
        
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
    
    def _get_difficulty_range(self, tutorials: List[Dict]) -> str:
        """Get range of difficulties"""
        diffs = set(t["difficulty"] for t in tutorials)
        return " - ".join(sorted(diffs))


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  VIDEO TUTORIAL FINDER - DEMONSTRATION")
    print("=" * 60)
    
    finder = VideoTutorialFinder()
    
    sample = {
        "title": "Amigurumi Bunny",
        "difficulty": "Beginner",
        "rounds": [
            {"round": 1, "instruction": "6 sc in magic ring"},
            {"round": 2, "instruction": "inc in each st around"},
            {"round": 3, "instruction": "[sc, inc] x 6"},
            {"round": 7, "instruction": "sc in each st around"},
            {"round": 10, "instruction": "[4 sc, dec] x 6"},
            {"round": 15, "instruction": "sl st to join"},
        ]
    }
    
    # Find tutorials
    tutorials = finder.find_tutorials_for_pattern(sample)
    print(f"\n  Tutorials for '{sample['title']}':")
    for t in tutorials:
        print(f"    [{t['difficulty']}] {t['title']} ({t['duration']})")
        print(f"      Topic: {t['topic']} | {t.get('reason', '')}")
    
    # Generate playlist
    playlist = finder.generate_playlist(sample)
    print(f"\n  Learning Playlist: {playlist['name']}")
    print(f"  {playlist['total_tutorials']} tutorials | {playlist['estimated_total_duration']}")
    print(f"  Difficulty: {playlist['difficulty_range']}")
    
    # Search specific stitch
    print(f"\n  Tutorials for 'popcorn' stitch:")
    for t in finder.find_by_stitch("popcorn"):
        print(f"    {t['title']} ({t['duration']})")
    
    print(f"\n  Video Tutorial Finder Complete!")
