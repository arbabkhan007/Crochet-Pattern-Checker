"""Convert a US-terms pattern dict to a UK-terms variant.

Only instructional / descriptive strings are converted; machine fields
(cons / prod / stated / check / codes) are untouched because stitch COUNTS do
not change between terminologies.

Mapping (per the supplied conversion table):
  sc -> dc, hdc -> htr, dc -> tr, tr -> dtr, sc2tog -> dc2tog,
  5-dc bobble -> 5-tr bobble (handled by the dc rule), sl st / ch unchanged.
"""
from __future__ import annotations

import copy
import re

# longer/specific tokens first; placeholders stop cascading replacements
_SUBS = [
    (re.compile(r"\bsc2tog\b"), "\x00K1\x00"),   # -> dc2tog
    (re.compile(r"\bhdc\b"), "\x00K2\x00"),      # -> htr
    (re.compile(r"\bdc\b"), "\x00K3\x00"),       # -> tr
    (re.compile(r"\btr\b"), "\x00K4\x00"),       # -> dtr
    (re.compile(r"\bsc\b"), "\x00K5\x00"),       # -> dc
    (re.compile(r"US terms"), "\x00K6\x00"),     # -> UK terms
    (re.compile(r"US Terms"), "\x00K6\x00"),
]
_FILL = {
    "\x00K1\x00": "dc2tog",
    "\x00K2\x00": "htr",
    "\x00K3\x00": "tr",
    "\x00K4\x00": "dtr",
    "\x00K5\x00": "dc",
    "\x00K6\x00": "UK terms",
}

# keys whose values must NOT be converted
_SKIP_KEYS = {
    "id", "number", "design_code", "hashtag", "check", "cons", "prod",
    "stated", "skip_check", "allow_gap", "kind", "type", "file_slug",
    "assets_key",
}


def _conv(value, key):
    if isinstance(value, str):
        if key in _SKIP_KEYS:
            return value
        out = value
        for rx, repl in _SUBS:
            out = rx.sub(repl, out)
        for ph, txt in _FILL.items():
            out = out.replace(ph, txt)
        return out
    if isinstance(value, list):
        return [_conv(v, key) for v in value]
    if isinstance(value, tuple):
        return tuple(_conv(v, key) for v in value)
    if isinstance(value, dict):
        return {k: _conv(v, k) for k, v in value.items()}
    return value


def to_uk(p: dict) -> dict:
    """Return a UK-terminology deep-copied pattern dict."""
    uk = _conv(copy.deepcopy(p), None)
    if uk.get("abbreviations_uk"):
        uk["abbreviations"] = uk["abbreviations_uk"]
    # UK marker in the meta row so both versions are visibly distinct
    return uk
