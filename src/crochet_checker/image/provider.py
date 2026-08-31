"""Multi-provider image generation for crochet patterns."""
from __future__ import annotations
import os, base64, hashlib
from typing import Optional, Literal
from pydantic import BaseModel

class ImageConfig(BaseModel):
    provider: Literal["placeholder", "dalle", "gemini", "stable_diffusion"] = "placeholder"
    api_key: Optional[str] = None
    style: str = "watercolor"
    size: str = "1024x1024"

class ImageProvider:
    def __init__(self, config=None):
        self.config = config or ImageConfig()
        self._api_key = self.config.api_key or self._get_api_key()
    def _get_api_key(self):
        keys = {"dalle": "OPENAI_API_KEY", "gemini": "GOOGLE_API_KEY", "stable_diffusion": "REPLICATE_API_TOKEN"}
        env = keys.get(self.config.provider)
        return os.environ.get(env) if env else None
    def generate_cover_image(self, title, category=""):
        if self.config.provider == "placeholder" or not self._api_key:
            return self._placeholder(title, category)
        if self.config.provider == "dalle": return self._dalle(title, category)
        if self.config.provider == "gemini": return self._gemini(title, category)
        if self.config.provider == "stable_diffusion": return self._sd(title, category)
        return self._placeholder(title, category)
    def _placeholder(self, title, category):
        h = hashlib.md5(title.encode()).hexdigest()
        h1, h2 = int(h[:3], 16) % 360, (int(h[:3], 16) + 60) % 360
        icon = self._icon(category)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
<defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:hsl({h1},70%,85%)"/><stop offset="100%" style="stop-color:hsl({h2},70%,75%)"/>
</linearGradient></defs>
<rect width="400" height="400" fill="url(#bg)" rx="20"/>
<g transform="translate(200,200)"><circle r="120" fill="white" opacity="0.9"/>{icon}</g>
<text x="200" y="360" text-anchor="middle" font-family="Georgia" font-size="16" fill="hsl({h1},40%,30%)">{title[:30]}</text>
</svg>"""
    def _icon(self, cat):
        c = cat.lower() if cat else ""
        if "hat" in c: return '<path d="M-40,-30 Q0,-60 40,-30 L40,20 Q0,30 -40,20 Z" fill="hsl(200,60%,50%)"/>'
        if "scarf" in c: return '<rect x="-60" y="-10" width="120" height="20" rx="5" fill="hsl(0,60%,60%)"/>'
        if "amigurumi" in c or "sphere" in c: return '<circle r="50" fill="hsl(120,60%,60%)"/><circle cx="-15" cy="-15" r="8" fill="white"/><circle cx="15" cy="-15" r="8" fill="white"/>'
        if "blanket" in c: return '<rect x="-50" y="-50" width="100" height="100" fill="hsl(280,60%,70%)" rx="5"/>'
        return '<circle r="45" fill="hsl(340,60%,65%)"/><path d="M-30,-20 Q0,-40 30,-20 Q40,0 30,20 Q0,40 -30,20 Q-40,0 -30,-20" stroke="hsl(340,60%,55%)" fill="none" stroke-width="2"/>'
    def _dalle(self, title, cat):
        try:
            import openai
            c = openai.OpenAI(api_key=self._api_key)
            r = c.images.generate(model="dall-e-3", prompt=f"crochet {cat}: {title}. {self.config.style} illustration.", size=self.config.size, n=1, response_format="b64_json")
            return r.data[0].b64_json
        except: return self._placeholder(title, cat)
    def _gemini(self, title, cat):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self._api_key)
            m = genai.GenerativeModel("gemini-2.0-flash-exp")
            r = m.generate_content(f"Generate image: crochet {cat}: {title}. {self.config.style}.", generation_config={"response_mime_type": "image/png"})
            if r.parts and r.parts[0].inline_data: return base64.b64encode(r.parts[0].inline_data.data).decode()
            return self._placeholder(title, cat)
        except: return self._placeholder(title, cat)
    def _sd(self, title, cat):
        try:
            import replicate, requests
            r = replicate.run("stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf", input={"prompt": f"crochet {cat}: {title}. {self.config.style}."})
            return base64.b64encode(requests.get(r[0]).content).decode()
        except: return self._placeholder(title, cat)

def generate_pattern_image(title, category="", provider="placeholder", api_key=None, style="watercolor"):
    return ImageProvider(ImageConfig(provider=provider, api_key=api_key, style=style)).generate_cover_image(title, category)
