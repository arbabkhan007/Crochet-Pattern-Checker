"""US/UK terminology translator."""
from __future__ import annotations
import re
from pydantic import BaseModel, Field

US_TO_UK = {"single crochet":"double crochet","sc":"dc","half double crochet":"half treble crochet","hdc":"htr","double crochet":"treble crochet","dc":"tr","treble crochet":"double treble crochet","tr":"dtr","sc2tog":"dc2tog"}
UK_TO_US = {"double crochet":"single crochet","dc":"sc","half treble crochet":"half double crochet","htr":"hdc","treble crochet":"double crochet","tr":"dc","double treble crochet":"treble crochet","dtr":"tr","dc2tog":"sc2tog"}

class TranslationResult(BaseModel):
    translated_text: str = ""
    from_terms: str = ""
    to_terms: str = ""
    changes_made: list[str] = Field(default_factory=list)
    num_changes: int = 0

class TerminologyTranslator:
    def translate_us_to_uk(self, text): return self._translate(text, US_TO_UK, "US", "UK")
    def translate_uk_to_us(self, text): return self._translate(text, UK_TO_US, "UK", "US")
    def translate(self, text, f, t):
        f,t = f.upper(),t.upper()
        if f=="US" and t=="UK": return self.translate_us_to_uk(text)
        elif f=="UK" and t=="US": return self.translate_uk_to_us(text)
        raise ValueError(f"Unknown: {f} -> {t}")
    def _translate(self, text, mapping, ft, tt):
        changes = []; sorted_terms = sorted(mapping.keys(), key=len, reverse=True)
        patterns = []
        for term in sorted_terms:
            if len(term) <= 3: patterns.append(r"\b" + re.escape(term) + r"\b")
            else: patterns.append(re.escape(term))
        regex = re.compile("|".join(f"({p})" for p in patterns), re.IGNORECASE)
        def repl(match):
            orig = match.group(0)
            for term in sorted_terms:
                if re.match(re.escape(term), orig, re.IGNORECASE):
                    rep = mapping[term]; tr = self._case(orig, rep)
                    changes.append(f"{orig} -> {tr}"); return tr
            return orig
        result = regex.sub(repl, text)
        return TranslationResult(translated_text=result, from_terms=ft, to_terms=tt, changes_made=changes, num_changes=len(changes))
    def _case(self, o, r):
        if o.isupper(): return r.upper()
        if o.islower(): return r.lower()
        if o[0].isupper(): return r[0].upper() + r[1:]
        return r

def translate_pattern(text, f="US", t="UK"):
    return TerminologyTranslator().translate(text, f, t)
