"""Multi-provider AI assistance: OpenAI, Claude, Gemini, Ollama."""
from __future__ import annotations
import os
from typing import Optional, Literal
from pydantic import BaseModel
from ..model.pattern import Pattern
from ..validation import ValidationReport

class AIConfig(BaseModel):
    provider: Literal["rule_based", "openai", "anthropic", "gemini", "ollama"] = "rule_based"
    api_key: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000

class AIProvider:
    def __init__(self, config=None):
        self.config = config or AIConfig()
        self._api_key = self.config.api_key or self._get_key()
    def _get_key(self):
        keys = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "gemini": "GOOGLE_API_KEY"}
        env = keys.get(self.config.provider)
        return os.environ.get(env) if env else None
    def explain_pattern(self, pattern, report, context=""):
        if self.config.provider == "rule_based" or not self._api_key:
            return self._rule_explain(pattern, report)
        if self.config.provider == "openai": return self._openai(pattern, report, context)
        if self.config.provider == "anthropic": return self._anthropic(pattern, report, context)
        if self.config.provider == "gemini": return self._gemini(pattern, report, context)
        if self.config.provider == "ollama": return self._ollama(pattern, report, context)
        return self._rule_explain(pattern, report)
    def suggest_fixes(self, pattern, report):
        from ..ai.suggestions import SuggestionEngine
        return [{"error": s.error_message, "suggestion": s.suggestion, "explanation": s.explanation} for s in SuggestionEngine().generate_suggestions(pattern, report)]
    def translate_terminology(self, text, from_t="US", to_t="UK"):
        from ..ai.terminology import translate_pattern
        return translate_pattern(text, from_t, to_t).translated_text
    def _rule_explain(self, p, r):
        from ..ai.explainer import PatternExplainer
        result = PatternExplainer().explain(p, r)
        parts = [result.summary, "", result.explanation]
        if result.highlights: parts.append("\nKey Points:"); [parts.append(f"  * {h}") for h in result.highlights]
        if result.recommendations: parts.append("\nRecommendations:"); [parts.append(f"  + {r}") for r in result.recommendations]
        return "\n".join(parts)
    def _prompt(self, p, r, ctx):
        items = p.rounds or p.rows; n = len(items) if items else 0
        prompt = f"Explain this crochet pattern:\nTitle: {p.metadata.title or 'Untitled'}\nRounds: {n}\nStatus: {r.overall_status}\nScore: {r.score}/100\n"
        if r.errors: prompt += f"\nErrors ({len(r.errors)}):\n" + "\n".join(f"  - {e.message}" for e in r.errors[:3])
        if r.warnings: prompt += f"\nWarnings ({len(r.warnings)}):\n" + "\n".join(f"  - {w.message}" for w in r.warnings[:3])
        prompt += "\n\nProvide: 1) Summary 2) Difficulty 3) Key techniques 4) Tips 5) Issues and fixes"
        return prompt
    def _openai(self, p, r, ctx):
        try:
            import openai
            c = openai.OpenAI(api_key=self._api_key)
            return c.chat.completions.create(model=self.config.model or "gpt-4-turbo-preview", messages=[{"role":"system","content":"You are a crochet pattern expert."},{"role":"user","content":self._prompt(p,r,ctx)}], temperature=self.config.temperature, max_tokens=self.config.max_tokens).choices[0].message.content
        except Exception as e: print(f"OpenAI failed: {e}"); return self._rule_explain(p, r)
    def _anthropic(self, p, r, ctx):
        try:
            import anthropic
            c = anthropic.Anthropic(api_key=self._api_key)
            return c.messages.create(model=self.config.model or "claude-3-sonnet-20240229", max_tokens=self.config.max_tokens, messages=[{"role":"user","content":self._prompt(p,r,ctx)}]).content[0].text
        except Exception as e: print(f"Claude failed: {e}"); return self._rule_explain(p, r)
    def _gemini(self, p, r, ctx):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self._api_key)
            return genai.GenerativeModel(self.config.model or "gemini-pro").generate_content(self._prompt(p,r,ctx)).text
        except Exception as e: print(f"Gemini failed: {e}"); return self._rule_explain(p, r)
    def _ollama(self, p, r, ctx):
        try:
            import ollama
            return ollama.chat(model=self.config.model or "llama2", messages=[{"role":"user","content":self._prompt(p,r,ctx)}])["message"]["content"]
        except Exception as e: print(f"Ollama failed: {e}"); return self._rule_explain(p, r)
