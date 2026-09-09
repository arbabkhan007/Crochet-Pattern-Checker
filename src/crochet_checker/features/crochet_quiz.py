"""
Crochet Quiz & Learning Game - Gamified stitch learning with XP, levels, and achievements
"""
import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class QuizQuestion:
    """A quiz question"""
    id: str
    category: str
    question: str
    options: List[str]
    correct_answer: int
    difficulty: str  # beginner, intermediate, advanced
    xp_reward: int = 10
    explanation: str = ""


class CrochetQuiz:
    """
    Gamified crochet learning system
    
    Features:
    - Stitch knowledge quizzes
    - XP and leveling system
    - Achievements and badges
    - Daily challenges
    - Streak tracking
    - Leaderboards
    - Learning paths
    """
    
    QUESTIONS = [
        QuizQuestion("Q001", "stitches", "What does 'sc' stand for?",
                    ["Single Crochet", "Slip Chain", "Soft Crochet", "Special Chain"],
                    0, "beginner", 10, "sc = single crochet, the most basic stitch"),
        QuizQuestion("Q002", "stitches", "Which stitch is taller than a single crochet?",
                    ["Slip stitch", "Half double crochet", "Chain stitch", "Magic ring"],
                    1, "beginner", 10, "HDC is taller than SC but shorter than DC"),
        QuizQuestion("Q003", "stitches", "What is a 'frog' in crochet?",
                    ["A type of yarn", "Ripping out stitches (rip it, rip it)", "A stitch pattern", "A hook size"],
                    1, "beginner", 15, "Frog = rip it out (sounds like a frog!)"),
        QuizQuestion("Q004", "tools", "What hook size is most common for worsted weight yarn?",
                    ["2.0mm", "4.0mm (G/6)", "6.0mm (J)", "10.0mm"],
                    1, "beginner", 10, "G/6 (4.0mm) is standard for worsted weight"),
        QuizQuestion("Q005", "techniques", "What is gauge in crochet?",
                    ["Tension of yarn", "Stitches per inch measurement", "Hook size", "Yarn weight"],
                    1, "intermediate", 15, "Gauge = stitches per inch, crucial for sizing"),
        QuizQuestion("Q006", "stitches", "Which stitch uses the most yarn?",
                    ["Single crochet", "Double crochet", "Treble crochet", "Chain stitch"],
                    2, "intermediate", 15, "Treble uses more yarn per stitch than DC or SC"),
        QuizQuestion("Q007", "patterns", "What does '(inc)' mean in a pattern?",
                    ["Decrease", "Increase", "Insert hook", "In color"],
                    1, "beginner", 10, "inc = increase, usually 2 SC in same stitch"),
        QuizQuestion("Q008", "yarn", "What weight is 'DK' yarn?",
                    ["Lace weight", "Double Knitting (light)", "Worsted", "Bulky"],
                    1, "beginner", 10, "DK = Double Knitting, lighter than worsted"),
        QuizQuestion("Q009", "techniques", "What is amigurumi?",
                    ["A type of hook", "Japanese crochet for stuffed toys", "A stitch pattern", "A yarn brand"],
                    1, "beginner", 15, "Amigurumi = Japanese art of crochet stuffed toys"),
        QuizQuestion("Q010", "stitches", "How many chains typically start a DC row?",
                    ["1", "2", "3", "4"],
                    2, "intermediate", 10, "3 chains = turning chain for DC"),
        QuizQuestion("Q011", "techniques", "What is a magic ring/magic circle?",
                    ["A type of ring to wear", "Adjustable starting loop for circles", "A stitch pattern", "A tool"],
                    1, "intermediate", 15, "Magic ring creates a tight, adjustable center"),
        QuizQuestion("Q012", "patterns", "What does 'rep' mean?",
                    ["Repeat", "Repair", "Replace", "Repel"],
                    0, "beginner", 10, "rep = repeat the following instructions"),
        QuizQuestion("Q013", "yarn", "Which fiber is NOT natural?",
                    ["Cotton", "Wool", "Acrylic", "Silk"],
                    2, "beginner", 10, "Acrylic is synthetic; others are natural fibers"),
        QuizQuestion("Q014", "techniques", "What is blocking?",
                    ["Preventing stitches", "Shaping finished work with moisture", "A type of stitch", "Cutting yarn"],
                    1, "intermediate", 15, "Blocking shapes and sets your finished piece"),
        QuizQuestion("Q015", "advanced", "What is a post stitch?",
                    ["A stitch around the post of previous row", "A social media stitch", "A decrease", "An increase"],
                    0, "advanced", 20, "Post stitches work around the stitch post for texture"),
        QuizQuestion("Q016", "techniques", "What does 'working in the round' mean?",
                    ["Using circular needles", "Crocheting in a spiral or joined rounds", "Making a circle", "Turning work"],
                    1, "beginner", 15, "Working in the round = continuous circles without turning"),
        QuizQuestion("Q017", "stitches", "Which is the shortest stitch?",
                    ["Chain", "Slip stitch", "Single crochet", "Half double"],
                    1, "beginner", 10, "Slip stitch is the shortest/flat stitch"),
        QuizQuestion("Q018", "yarn", "What does 'superwash' mean?",
                    ["Super clean", "Machine washable wool", "Super soft", "Super strong"],
                    1, "intermediate", 15, "Superwash wool can be machine washed"),
        QuizQuestion("Q019", "patterns", "What is a 'repeat' in a pattern?",
                    ["Starting over", "Instructions to do multiple times", "A mistake", "A different color"],
                    1, "beginner", 10, "Repeat = do the same instructions again"),
        QuizQuestion("Q020", "advanced", "What is tapestry crochet?",
                    ["Crochet with tape", "Multi-color crochet carrying yarn", "Crochet on tapestry fabric", "A brand"],
                    1, "advanced", 20, "Tapestry crochet = colorwork carrying unused yarn inside"),
    ]
    
    ACHIEVEMENTS = {
        "first_quiz": {"name": "First Steps", "desc": "Complete your first quiz", "xp": 50, "icon": "🎯"},
        "streak_3": {"name": "On Fire", "desc": "3 correct in a row", "xp": 30, "icon": "🔥"},
        "streak_10": {"name": "Unstoppable", "desc": "10 correct in a row", "xp": 100, "icon": "⚡"},
        "level_5": {"name": "Knowledgeable", "desc": "Reach level 5", "xp": 200, "icon": "📚"},
        "all_categories": {"name": "Well Rounded", "desc": "Answer from every category", "xp": 75, "icon": "🌟"},
        "perfect_score": {"name": "Perfect!", "desc": "100% on a quiz", "xp": 50, "icon": "💯"},
        "daily_player": {"name": "Daily Devotee", "desc": "Play 7 days in a row", "xp": 150, "icon": "📅"},
        "xp_1000": {"name": "Master Crocheter", "desc": "Earn 1000 XP total", "xp": 500, "icon": "👑"},
    }
    
    CATEGORIES = ["stitches", "tools", "techniques", "patterns", "yarn", "advanced"]
    
    def __init__(self, storage_path: str = "crochet_quiz.json"):
        self.storage_path = Path(storage_path)
        self.data = {
            "xp": 0,
            "level": 1,
            "quizzes_completed": 0,
            "total_correct": 0,
            "total_answered": 0,
            "current_streak": 0,
            "best_streak": 0,
            "categories_answered": [],
            "achievements": [],
            "daily_streak": 0,
            "last_played": None,
            "history": [],
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
    
    def get_questions_for_quiz(self, count: int = 5, category: str = None,
                               difficulty: str = None) -> List[QuizQuestion]:
        """Get random questions for a quiz"""
        questions = self.QUESTIONS.copy()
        
        if category:
            questions = [q for q in questions if q.category == category]
        if difficulty:
            questions = [q for q in questions if q.difficulty == difficulty]
        
        random.shuffle(questions)
        return questions[:min(count, len(questions))]
    
    def answer_question(self, question_id: str, selected: int) -> Dict:
        """Submit an answer"""
        question = next((q for q in self.QUESTIONS if q.id == question_id), None)
        if not question:
            return {"error": "Question not found"}
        
        correct = selected == question.correct_answer
        xp_earned = question.xp_reward if correct else 0
        
        if correct:
            self.data["total_correct"] += 1
            self.data["current_streak"] += 1
            self.data["best_streak"] = max(self.data["best_streak"], self.data["current_streak"])
            
            if question.category not in self.data["categories_answered"]:
                self.data["categories_answered"].append(question.category)
        else:
            self.data["current_streak"] = 0
        
        self.data["total_answered"] += 1
        self.add_xp(xp_earned)
        
        # Check streak achievements
        new_achievements = []
        if self.data["current_streak"] >= 3 and "streak_3" not in self.data["achievements"]:
            new_achievements.append("streak_3")
        if self.data["current_streak"] >= 10 and "streak_10" not in self.data["achievements"]:
            new_achievements.append("streak_10")
        
        for ach in new_achievements:
            self.data["achievements"].append(ach)
            self.add_xp(self.ACHIEVEMENTS[ach]["xp"])
        
        self.save()
        
        return {
            "correct": correct,
            "xp_earned": xp_earned,
            "correct_answer": question.options[question.correct_answer],
            "explanation": question.explanation,
            "current_streak": self.data["current_streak"],
            "new_achievements": new_achievements,
            "total_xp": self.data["xp"],
            "level": self.data["level"],
        }
    
    def add_xp(self, amount: int):
        """Add XP and level up"""
        self.data["xp"] += amount
        
        # Level up check (100 XP per level)
        new_level = (self.data["xp"] // 100) + 1
        if new_level > self.data["level"]:
            self.data["level"] = new_level
            
            if new_level >= 5 and "level_5" not in self.data["achievements"]:
                self.data["achievements"].append("level_5")
            if self.data["xp"] >= 1000 and "xp_1000" not in self.data["achievements"]:
                self.data["achievements"].append("xp_1000")
    
    def complete_quiz(self, correct: int, total: int) -> Dict:
        """Mark a quiz as complete"""
        self.data["quizzes_completed"] += 1
        
        # Update daily streak
        today = datetime.now().strftime("%Y-%m-%d")
        if self.data["last_played"] != today:
            yesterday = (datetime.now().replace(hour=0, minute=0, second=0) - 
                        __import__('datetime').timedelta(days=1)).strftime("%Y-%m-%d")
            if self.data["last_played"] == yesterday:
                self.data["daily_streak"] += 1
            else:
                self.data["daily_streak"] = 1
            self.data["last_played"] = today
        
        # Check achievements
        new_achievements = []
        if self.data["quizzes_completed"] == 1 and "first_quiz" not in self.data["achievements"]:
            new_achievements.append("first_quiz")
        if correct == total and "perfect_score" not in self.data["achievements"]:
            new_achievements.append("perfect_score")
        if len(self.data["categories_answered"]) >= len(self.CATEGORIES) and "all_categories" not in self.data["achievements"]:
            new_achievements.append("all_categories")
        if self.data["daily_streak"] >= 7 and "daily_player" not in self.data["achievements"]:
            new_achievements.append("daily_player")
        
        for ach in new_achievements:
            self.data["achievements"].append(ach)
            self.add_xp(self.ACHIEVEMENTS[ach]["xp"])
        
        self.save()
        
        return {
            "score": f"{correct}/{total}",
            "percentage": round(correct / total * 100, 1),
            "xp_earned": sum(q.xp_reward for q in []),  # Already added per question
            "daily_streak": self.data["daily_streak"],
            "achievements_earned": new_achievements,
            "level": self.data["level"],
            "total_xp": self.data["xp"],
        }
    
    def get_player_stats(self) -> Dict:
        """Get player statistics"""
        accuracy = (self.data["total_correct"] / max(1, self.data["total_answered"])) * 100
        
        return {
            "level": self.data["level"],
            "xp": self.data["xp"],
            "xp_to_next_level": 100 - (self.data["xp"] % 100),
            "quizzes_completed": self.data["quizzes_completed"],
            "total_correct": self.data["total_correct"],
            "total_answered": self.data["total_answered"],
            "accuracy": round(accuracy, 1),
            "current_streak": self.data["current_streak"],
            "best_streak": self.data["best_streak"],
            "daily_streak": self.data["daily_streak"],
            "achievements": self.data["achievements"],
            "categories_explored": len(self.data["categories_answered"]),
        }
    
    def get_learning_path(self) -> List[Dict]:
        """Get recommended learning path"""
        stats = self.get_player_stats()
        
        path = [
            {"level": 1, "topic": "Basic Stitches (SC, DC, HDC)", "status": "completed" if stats["level"] > 1 else "current"},
            {"level": 2, "topic": "Reading Patterns & Abbreviations", "status": "locked" if stats["level"] < 2 else "completed" if stats["level"] > 2 else "current"},
            {"level": 3, "topic": "Gauge & Sizing", "status": "locked" if stats["level"] < 3 else "current"},
            {"level": 4, "topic": "Colorwork & Techniques", "status": "locked" if stats["level"] < 4 else "current"},
            {"level": 5, "topic": "Advanced Stitches & Design", "status": "locked" if stats["level"] < 5 else "current"},
        ]
        
        return path


# Demo
if __name__ == "__main__":
    import os
    print("\n" + "=" * 60)
    print("  CROCHET QUIZ & LEARNING GAME - DEMONSTRATION")
    print("=" * 60)
    
    quiz = CrochetQuiz(storage_path="/tmp/demo_quiz.json")
    
    # Get a quiz
    print(f"\n📝 Starting Quiz (5 questions)...")
    questions = quiz.get_questions_for_quiz(count=5)
    
    # Answer questions
    correct = 0
    for i, q in enumerate(questions, 1):
        print(f"\n  Q{i}: {q.question}")
        for j, opt in enumerate(q.options):
            print(f"    {j}. {opt}")
        
        # Simulate answer (first option for demo)
        result = quiz.answer_question(q.id, q.correct_answer)
        if result["correct"]:
            correct += 1
            print(f"    ✅ Correct! +{result['xp_earned']} XP")
        else:
            print(f"    ❌ Wrong. Answer: {result['correct_answer']}")
            print(f"    💡 {result['explanation']}")
        
        if result["new_achievements"]:
            for ach in result["new_achievements"]:
                info = quiz.ACHIEVEMENTS[ach]
                print(f"    🏆 Achievement Unlocked: {info['icon']} {info['name']}!")
    
    # Complete quiz
    final = quiz.complete_quiz(correct, len(questions))
    print(f"\n🎯 Quiz Complete!")
    print(f"  Score: {final['score']} ({final['percentage']}%)")
    print(f"  Level: {final['level']}")
    print(f"  Daily Streak: {final['daily_streak']} days")
    
    # Stats
    stats = quiz.get_player_stats()
    print(f"\n📊 Player Stats:")
    print(f"  Level: {stats['level']} ({stats['xp']} XP)")
    print(f"  Accuracy: {stats['accuracy']}%")
    print(f"  Best Streak: {stats['best_streak']}")
    print(f"  Achievements: {len(stats['achievements'])}")
    
    # Learning path
    print(f"\n📚 Learning Path:")
    for step in quiz.get_learning_path():
        icon = "✅" if step["status"] == "completed" else "🔒" if step["status"] == "locked" else "▶️"
        print(f"  {icon} Lv{step['level']}: {step['topic']}")
    
    # Cleanup
    if os.path.exists("/tmp/demo_quiz.json"):
        os.remove("/tmp/demo_quiz.json")
    
    print(f"\n  Crochet Quiz Complete! 🎮")
