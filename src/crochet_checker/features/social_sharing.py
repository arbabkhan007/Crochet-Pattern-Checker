"""
Social Sharing - Share patterns to Ravelry, Instagram, Pinterest, Etsy
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class SharePost:
    platform: str
    title: str
    description: str
    hashtags: List[str] = field(default_factory=list)
    image_url: str = ""
    pattern_url: str = ""
    price: float = 0
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SocialSharing:
    """
    Generate share-ready content for multiple platforms
    
    Features:
    - Ravelry pattern listing generator
    - Instagram post captions + hashtags
    - Pinterest pin descriptions
    - Etsy listing generator
    - Twitter/X posts
    - Facebook posts
    - Hashtag generator
    - SEO optimization
    """
    
    HASHTAG_DATABASE = {
        "amigurumi": ["#amigurumi", "#crochet", "#handmade", "#stuffed", "#cute",
                     "#crochetlove", "#amigurumipattern", "#handmadewithlove"],
        "blanket": ["#crochetblanket", "#grannysquare", "#blanket", "#cozy",
                   "#crochetblanket", "#homemade", "#handmadething"],
        "hat": ["#crochethat", "#beanie", "#hatpattern", "#wintercrochet",
               "#handmadehat", "#crochetfashion"],
        "baby": ["#babycrochet", "#crochetbaby", "#newborn", "#babygift",
                "#safetoy", "#handmadeforbaby"],
        "flower": ["#crochetflower", "#crochetrose", "#flowerpattern",
                  "#botanical", "#crochetgarden"],
        "food": ["#crochetfood", "#amigurumifood", "#crochetcute",
                "#foodie", "#kawaiicrochet"],
        "beginner": ["#beginnercrochet", "#easypattern", "#crochettutorial",
                    "#learntocrochet", "#crochetforbeginners"],
        "modern": ["#moderncrochet", "#crochetdesign", "#contemporary",
                  "#minimalist", "#scandi"],
        "vintage": ["#vintagecrochet", "#retrocrochet", "#heirloom",
                   "#classiccrochet", "#nostalgia"],
        "sustainable": ["#sustainablefashion", "#ecocrochet", "#slowfashion",
                       "#handmadesustainable", "#ethicalfashion"],
    }
    
    def __init__(self):
        self.posts: List[SharePost] = []
    
    def generate_ravelry_listing(self, pattern: Dict) -> Dict:
        """Generate Ravelry pattern listing"""
        title = pattern.get("title", pattern.get("name", "Untitled"))
        rounds = pattern.get("rounds", [])
        
        return {
            "platform": "Ravelry",
            "pattern_name": title,
            "designer": pattern.get("designer", "Independent Designer"),
            "category": self._detect_category(pattern),
            "craft": "Crochet",
            "weight": pattern.get("yarn_weight", "Worsted (4)"),
            "hook_size": pattern.get("hook_size", "5.0 mm"),
            "yardage": sum(r.get("count", 0) for r in rounds) * 12 // 100,
            "difficulty": pattern.get("difficulty", "Easy"),
            "availability": "Free" if not pattern.get("price") else f"${pattern.get('price', 0)}",
            "description": self._generate_description(pattern, "ravelry"),
            "tags": self._generate_tags(pattern),
            "photo_tips": [
                "Flat lay on neutral background",
                "Close-up of stitch detail",
                "Finished item being used/worn",
                "Size reference with common object"
            ],
            "generated_at": datetime.now().isoformat(),
        }
    
    def generate_instagram_post(self, pattern: Dict, style: str = "casual") -> Dict:
        """Generate Instagram caption and hashtags"""
        title = pattern.get("title", "My latest crochet")
        category = self._detect_category(pattern)
        
        # Generate caption based on style
        if style == "casual":
            caption = f"Just finished: {title}! What do you think?"
        elif style == "story":
            caption = f"Behind the design of {title}..."
        elif style == "tutorial":
            caption = f"How I made {title} - step by step!"
        elif style == "sales":
            caption = f"Now available: {title} pattern! Link in bio."
        else:
            caption = f"{title}"
        
        hashtags = self.get_hashtags(category, count=20)
        
        return {
            "platform": "Instagram",
            "caption": caption,
            "hashtags": hashtags,
            "full_post": f"{caption}\n\n{' '.join(hashtags)}",
            "best_times": ["Tuesday 7pm", "Thursday 6pm", "Sunday 10am"],
            "image_tips": [
                "Square format (1080x1080)",
                "Bright, natural lighting",
                "Clean background",
                "Show texture close-up"
            ]
        }
    
    def generate_pinterest_pin(self, pattern: Dict) -> Dict:
        """Generate Pinterest pin content"""
        title = pattern.get("title", "Crochet Pattern")
        category = self._detect_category(pattern)
        
        return {
            "platform": "Pinterest",
            "title": f"{title} - Free Crochet Pattern",
            "description": self._generate_description(pattern, "pinterest"),
            "board_suggestions": [
                f"Crochet {category.title()} Patterns",
                "Handmade Gifts",
                "Crochet Ideas",
                "DIY Projects"
            ],
            "pin_tips": [
                "Vertical image (1000x1500px)",
                "Clear text overlay",
                "Bright colors",
                "Show finished item"
            ],
            "keywords": self._generate_seo_keywords(pattern),
        }
    
    def generate_etsy_listing(self, pattern: Dict, price: float = 5.99) -> Dict:
        """Generate Etsy listing"""
        title = pattern.get("title", "Crochet Pattern PDF")
        
        return {
            "platform": "Etsy",
            "title": f"{title} | Crochet Pattern PDF | Instant Download | Beginner Friendly",
            "description": self._generate_description(pattern, "etsy"),
            "price": f"${price:.2f}",
            "category": "Craft Supplies & Tools > Patterns > Crochet Patterns",
            "tags": [
                "crochet pattern",
                "pdf pattern",
                "instant download",
                self._detect_category(pattern),
                "digital pattern",
                "printable pattern",
                "handmade",
                "gift idea",
                "crochet tutorial",
                "DIY project",
                "beginner friendly",
                "step by step",
                "US terms",
            ],
            "seo_title": f"{title} Crochet Pattern PDF Download",
            "listing_tips": [
                "Include mockup photos",
                "Add preview pages",
                "Set as digital download",
                "Include size chart"
            ],
        }
    
    def generate_twitter_post(self, pattern: Dict) -> Dict:
        """Generate Twitter/X post"""
        title = pattern.get("title", "New pattern")
        hashtags = self.get_hashtags(self._detect_category(pattern), count=3)
        
        return {
            "platform": "Twitter/X",
            "text": f"New pattern alert! {title} {' '.join(hashtags)}",
            "thread_ideas": [
                f"1/ Just published: {title}",
                "2/ Here's what you'll need...",
                "3/ The trickiest part was...",
                "4/ Pattern link in bio!"
            ],
            "character_count": len(f"New pattern alert! {title} {' '.join(hashtags)}"),
        }
    
    def generate_facebook_post(self, pattern: Dict) -> Dict:
        """Generate Facebook post"""
        title = pattern.get("title", "My crochet pattern")
        category = self._detect_category(pattern)
        
        return {
            "platform": "Facebook",
            "text": f"I just finished designing: {title}! "
                   f"It's a {category} pattern perfect for "
                   f"{'beginners' if pattern.get('difficulty', '').lower() in ['beginner', 'easy'] else 'experienced crocheters'}. "
                   f"What do you think? Drop a comment!",
            "group_suggestions": [
                "Crochet Patterns Free",
                f"Crochet {category.title()} Lovers",
                "Amigurumi Addicts" if category == "amigurumi" else "Crochet Community",
            ],
            "hashtags": self.get_hashtags(category, count=5),
        }
    
    def get_hashtags(self, category: str, count: int = 15) -> List[str]:
        """Get relevant hashtags for a category"""
        hashtags = set()
        
        # Category-specific
        if category in self.HASHTAG_DATABASE:
            hashtags.update(self.HASHTAG_DATABASE[category])
        
        # Always add general
        hashtags.update(["#crochet", "#handmade", "#crochetpattern"])
        
        return sorted(list(hashtags))[:count]
    
    def generate_all_platforms(self, pattern: Dict) -> Dict:
        """Generate content for all platforms at once"""
        return {
            "ravelry": self.generate_ravelry_listing(pattern),
            "instagram": self.generate_instagram_post(pattern),
            "pinterest": self.generate_pinterest_pin(pattern),
            "etsy": self.generate_etsy_listing(pattern),
            "twitter": self.generate_twitter_post(pattern),
            "facebook": self.generate_facebook_post(pattern),
        }
    
    def _detect_category(self, pattern: Dict) -> str:
        """Detect pattern category"""
        text = json.dumps(pattern).lower()
        if "amigurumi" in text or "stuffed" in text or "ball" in text:
            return "amigurumi"
        elif "blanket" in text or "afghan" in text or "granny" in text:
            return "blanket"
        elif "hat" in text or "beanie" in text:
            return "hat"
        elif "baby" in text or "infant" in text:
            return "baby"
        elif "flower" in text or "rose" in text:
            return "flower"
        elif "food" in text or "fruit" in text:
            return "food"
        return "general"
    
    def _generate_description(self, pattern: Dict, platform: str) -> str:
        """Generate platform-specific description"""
        title = pattern.get("title", "Pattern")
        difficulty = pattern.get("difficulty", "Intermediate")
        rounds = pattern.get("rounds", [])
        
        if platform == "ravelry":
            return (
                f"{title} is a {difficulty.lower()} crochet pattern worked in the round. "
                f"It consists of {len(rounds)} rounds and is perfect for crocheters looking "
                f"for a satisfying project. Pattern includes step-by-step instructions with "
                f"stitch counts for every round. US terms."
            )
        elif platform == "pinterest":
            return (
                f"Free {title} crochet pattern! Easy to follow instructions, "
                f"perfect for {difficulty.lower()} crocheters. "
                f"Save this pin for your next project! #crochet #pattern"
            )
        elif platform == "etsy":
            return (
                f"WHAT YOU GET:\n"
                f"- Instant PDF download of {title}\n"
                f"- {len(rounds)} rounds of detailed instructions\n"
                f"- Stitch counts for every round\n"
                f"- US crochet terms\n"
                f"- Difficulty: {difficulty}\n\n"
                f"MATERIALS NEEDED:\n"
                f"- Worsted weight yarn\n"
                f"- Appropriate hook size\n"
                f"- Stitch marker\n\n"
                f"This is a digital pattern, not a finished item."
            )
        return f"{title} - a beautiful crochet pattern."
    
    def _generate_tags(self, pattern: Dict) -> List[str]:
        category = self._detect_category(pattern)
        return [
            "crochet", "pattern", category, "handmade",
            pattern.get("difficulty", "intermediate").lower(),
            "US-terms", "PDF", "download"
        ]
    
    def _generate_seo_keywords(self, pattern: Dict) -> List[str]:
        title = pattern.get("title", "")
        category = self._detect_category(pattern)
        return [
            f"{title} pattern",
            f"{category} crochet pattern",
            f"free {category} pattern",
            f"easy crochet {category}",
            "crochet pattern PDF",
            "downloadable crochet pattern",
        ]


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  SOCIAL SHARING - DEMONSTRATION")
    print("=" * 60)
    
    sharing = SocialSharing()
    
    sample = {
        "title": "Cute Bunny Amigurumi",
        "difficulty": "Beginner",
        "rounds": [{"round": i, "count": 6*i} for i in range(1, 13)],
        "yarn_weight": "DK",
        "hook_size": "3.5mm",
    }
    
    # Generate for all platforms
    print("\n--- All Platforms ---")
    all_posts = sharing.generate_all_platforms(sample)
    
    for platform, post in all_posts.items():
        print(f"\n  [{platform.upper()}]")
        if platform == "instagram":
            print(f"  Caption: {post['caption']}")
            print(f"  Hashtags: {' '.join(post['hashtags'][:8])}")
        elif platform == "twitter":
            print(f"  Tweet: {post['text']}")
        elif platform == "pinterest":
            print(f"  Title: {post['title']}")
            print(f"  Desc: {post['description'][:100]}...")
        elif platform == "etsy":
            print(f"  Title: {post['title'][:80]}...")
            print(f"  Price: {post['price']}")
        elif platform == "ravelry":
            print(f"  Name: {post['pattern_name']}")
            print(f"  Difficulty: {post['difficulty']}")
        elif platform == "facebook":
            print(f"  Post: {post['text'][:100]}...")
    
    print("\n  Social Sharing Complete!")
