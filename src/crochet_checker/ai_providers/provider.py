"""Rule-based wording. A hosted chat is not called."""

from __future__ import annotations

import os
from typing import Literal

from pydantic import BaseModel


class AIConfig(BaseModel):
    provider: Literal["rule_based", "openai", "anthropic", "gemini", "ollama"] = (
        "rule_based"
    )
    api_key: str | None = None
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1000


class AIProvider:
    def __init__(self, config=None):
        self.config = config or AIConfig()
        self._api_key = self.config.api_key or self._get_key()

    def _get_key(self):
        keys = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "gemini": "GOOGLE_API_KEY",
        }
        env = keys.get(self.config.provider)
        return os.environ.get(env) if env else None

    def explain_pattern(self, pattern, report, context=""):
        del context
        return (
            self._rule_explain(pattern, report)
            + "\nHosted chat was not called."
        )

    def suggest_fixes(self, pattern, report):
        from ..ai.suggestions import SuggestionEngine

        return [
            {
                "error": s.error_message,
                "suggestion": s.suggestion,
                "explanation": s.explanation,
            }
            for s in SuggestionEngine().generate_suggestions(pattern, report)
        ]

    def translate_terminology(self, text, from_t="US", to_t="UK"):
        from ..ai.terminology import translate_pattern

        return translate_pattern(text, from_t, to_t).translated_text

    def _rule_explain(self, p, r):
        from ..ai.explainer import PatternExplainer

        result = PatternExplainer().explain(p, r)
        parts = [result.summary, "", result.explanation]
        if result.highlights:
            parts.append("\nKey Points:")
            [parts.append(f"  * {h}") for h in result.highlights]
        if result.recommendations:
            parts.append("\nRecommendations:")
            [parts.append(f"  + {rc}") for rc in result.recommendations]
        return "\n".join(parts)
