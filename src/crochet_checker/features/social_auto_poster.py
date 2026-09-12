"""
Crochet Social Auto-Poster - Generate and schedule social media content for your patterns
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


class SocialAutoPoster:
    """Generate social media content for crochet patterns"""
    
    def __init__(self, data_file: str = "social_posts.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
    
    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"posts": [], "templates": {}}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def generate_instagram_post(self, pattern_name: str, description: str = "") -> Dict:
        """Generate Instagram post content"""
        hashtags = [
            "#crochet", "#crochetpattern", "#handmade", "#yarnlove",
            "#crochetaddict", "#crafty", "#diy", "#patterns",
            "#crochetersofinstagram", "#instacrochet"
        ]
        
        caption = f"""
✨ NEW PATTERN RELEASE ✨

{pattern_name}

{description or 'Beautiful handmade crochet pattern available now!'}

🧶 Perfect for all skill levels
📏 Detailed instructions included
💝 Made with love

Link in bio to get your copy!

{' '.join(hashtags)}
""".strip()
        
        return {
            "platform": "instagram",
            "caption": caption,
            "hashtags": hashtags,
            "image_suggestion": "High-quality photo of finished item with yarn and hook",
            "best_time": "Tuesday-Thursday, 6-9 PM",
        }
    
    def generate_pinterest_pin(self, pattern_name: str, description: str = "") -> Dict:
        """Generate Pinterest pin content"""
        return {
            "platform": "pinterest",
            "title": f"{pattern_name} - Free Crochet Pattern",
            "description": description or f"Beautiful {pattern_name} crochet pattern. Perfect for beginners and advanced crocheters alike. Get the pattern now!",
            "keywords": ["crochet pattern", "free pattern", "handmade", "yarn craft"],
            "image_size": "1000x1500px (vertical)",
        }
    
    def generate_facebook_post(self, pattern_name: str, description: str = "") -> Dict:
        """Generate Facebook post content"""
        post = f"""
🧶 Just released: {pattern_name}! 🧶

{description or 'Check out this beautiful new crochet pattern!'}

✨ What's included:
• Detailed step-by-step instructions
• Photos for every step
• Multiple sizes (if applicable)
• Support from the designer

📥 Download now: [YOUR LINK]

Question: What's your next project going to be? Let me know in the comments! 👇

#CrochetPattern #HandmadeWithLove #CrochetCommunity
""".strip()
        
        return {
            "platform": "facebook",
            "post": post,
            "engagement_question": "What's your next project going to be?",
        }
    
    def generate_twitter_post(self, pattern_name: str) -> Dict:
        """Generate Twitter/X post content"""
        tweets = [
            f"✨ New pattern alert! {pattern_name} is now available! 🧶 Get it here: [LINK] #crochet #pattern",
            f"🧶 Just dropped: {pattern_name}! Beautiful design, easy to follow. Link in bio! #crochetpattern #handmade",
            f"Who's ready for their next crochet project? {pattern_name} is here! 🧵✨ #crochetcommunity #diy",
        ]
        
        return {
            "platform": "twitter",
            "tweets": tweets,
            "hashtags": ["#crochet", "#pattern", "#handmade", "#diy"],
            "character_limit": 280,
        }
    
    def generate_content_calendar(self, pattern_name: str, days: int = 7) -> List[Dict]:
        """Generate a week's worth of social media content"""
        calendar = []
        platforms = ["instagram", "pinterest", "facebook", "twitter"]
        
        for day in range(days):
            date = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")
            platform = platforms[day % len(platforms)]
            
            post = {
                "date": date,
                "platform": platform,
                "content_type": "pattern_promotion",
                "status": "scheduled"
            }
            
            if platform == "instagram":
                post.update(self.generate_instagram_post(pattern_name))
            elif platform == "pinterest":
                post.update(self.generate_pinterest_pin(pattern_name))
            elif platform == "facebook":
                post.update(self.generate_facebook_post(pattern_name))
            elif platform == "twitter":
                post.update(self.generate_twitter_post(pattern_name))
            
            calendar.append(post)
        
        return calendar
    
    def save_content_calendar(self, calendar: List[Dict]):
        """Save content calendar"""
        self.data["posts"].extend(calendar)
        self.save_data()


if __name__ == "__main__":
    print("📱 Crochet Social Auto-Poster")
    print("=" * 50)
    
    poster = SocialAutoPoster()
    
    pattern_name = "Cozy Granny Square Blanket"
    
    print("\n📸 Instagram Post:")
    ig = poster.generate_instagram_post(pattern_name, "Warm and cozy blanket perfect for winter!")
    print(ig["caption"][:200] + "...")
    
    print("\n📌 Pinterest Pin:")
    pin = poster.generate_pinterest_pin(pattern_name)
    print(f"  Title: {pin['title']}")
    print(f"  Description: {pin['description'][:100]}...")
    
    print("\n📘 Facebook Post:")
    fb = poster.generate_facebook_post(pattern_name)
    print(fb["post"][:200] + "...")
    
    print("\n🐦 Twitter Posts:")
    tw = poster.generate_twitter_post(pattern_name)
    for i, tweet in enumerate(tw["tweets"], 1):
        print(f"  {i}. {tweet}")
    
    print("\n📅 Content Calendar (7 days):")
    calendar = poster.generate_content_calendar(pattern_name, 7)
    for post in calendar:
        print(f"  {post['date']} - {post['platform']:10s} - {post['status']}")
    
    print("\n✅ Social Auto-Poster ready!")
