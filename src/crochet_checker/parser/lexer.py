from __future__ import annotations
from enum import Enum, auto
from typing import Optional
from pydantic import BaseModel

class TokenType(Enum):
    NUMBER=auto(); STITCH_ABBREV=auto(); COMMA=auto(); LPAREN=auto(); RPAREN=auto()
    TIMES=auto(); INTO=auto(); EACH=auto(); AROUND=auto(); NEXT=auto(); STITCH=auto()
    REMAINING=auto(); MAGIC_RING=auto(); TEXT=auto(); EOF=auto()

class Token(BaseModel):
    type: TokenType; value: str; position: int = 0

STITCH_ABBS = {"ch","sl st","slst","sc","hdc","dc","tr","inc","dec","sc2tog","dc2tog","fpdc","bpdc"}

class Lexer:
    def __init__(self, text): self.text = text; self.pos = 0; self.tokens = []
    def tokenize(self):
        self.pos = 0; self.tokens = []
        while self.pos < len(self.text):
            self._skip_ws()
            if self.pos >= len(self.text): break
            t = self._next(); 
            if t: self.tokens.append(t)
        self.tokens.append(Token(type=TokenType.EOF, value="", position=self.pos))
        return self.tokens
    def _skip_ws(self):
        while self.pos < len(self.text) and self.text[self.pos] in " \t\n\r": self.pos += 1
    def _next(self):
        if self.pos >= len(self.text): return None
        ch = self.text[self.pos]
        if ch == ",": self.pos += 1; return Token(type=TokenType.COMMA, value=",", position=self.pos-1)
        if ch == "(": self.pos += 1; return Token(type=TokenType.LPAREN, value="(", position=self.pos-1)
        if ch == ")": self.pos += 1; return Token(type=TokenType.RPAREN, value=")", position=self.pos-1)
        if ch.isdigit(): return self._num()
        if ch in "×*": self.pos += 1; return Token(type=TokenType.TIMES, value=ch, position=self.pos-1)
        if ch.isalpha(): return self._word()
        self.pos += 1; return None
    def _num(self):
        s = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isdigit(): self.pos += 1
        return Token(type=TokenType.NUMBER, value=self.text[s:self.pos], position=s)
    def _word(self):
        s = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalpha() or self.text[self.pos]=="'"): self.pos += 1
        w = self.text[s:self.pos].lower()
        rest = self.text[self.pos:].lstrip()
        if w=="sl" and rest.startswith("st"):
            self.pos += len(self.text[self.pos:]) - len(self.text[self.pos:].lstrip()); self.pos += 2
            return Token(type=TokenType.STITCH_ABBREV, value="sl st", position=s)
        if w=="magic" and rest.startswith("ring"):
            self.pos += len(self.text[self.pos:]) - len(self.text[self.pos:].lstrip()); self.pos += 4
            return Token(type=TokenType.MAGIC_RING, value="magic ring", position=s)
        kw = {"in":TokenType.INTO,"into":TokenType.INTO,"each":TokenType.EACH,"around":TokenType.AROUND,
              "next":TokenType.NEXT,"st":TokenType.STITCH,"sts":TokenType.STITCH,
              "rem":TokenType.REMAINING,"remaining":TokenType.REMAINING,"x":TokenType.TIMES}
        if w in kw: return Token(type=kw[w], value=w, position=s)
        if w in STITCH_ABBS or w == "mr":
            if w == "mr": return Token(type=TokenType.MAGIC_RING, value="MR", position=s)
            return Token(type=TokenType.STITCH_ABBREV, value=w, position=s)
        return Token(type=TokenType.TEXT, value=w, position=s)

def tokenize(text): return Lexer(text).tokenize()
