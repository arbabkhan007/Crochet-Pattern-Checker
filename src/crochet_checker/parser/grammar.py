import re
REPEAT_BLOCK = re.compile(r"[\(\[]([^)\]]+)[\)\]]\s*[x×]\s*(\d+)", re.IGNORECASE)
EACH_AROUND = re.compile(r"(sc|hdc|dc|tr|sl\s*st|inc|dec)\s+in\s+each\s+(st|sts)\s+around", re.IGNORECASE)
EACH_ACROSS = re.compile(r"(sc|hdc|dc|tr|sl\s*st|inc|dec)\s+in\s+each\s+(st|sts|ch)\s+across", re.IGNORECASE)
STATED_COUNT = re.compile(r"\((\d+)\)\s*$", re.IGNORECASE)
MAGIC_RING_START = re.compile(r"(\d+)\s+(sc|hdc|dc|tr)\s+(?:in|into)\s+(?:magic\s+ring|MR|magic\s+circle)", re.IGNORECASE)
REMAINING = re.compile(r"(sc|hdc|dc|tr|inc|dec)\s+in\s+(?:each\s+)?(?:remaining|rem)\s+(?:sts?)", re.IGNORECASE)
NEXT_N = re.compile(r"(sc|hdc|dc|tr|inc|dec)\s+in\s+(?:each\s+)?(?:next\s+)?(\d+)\s+(sts?)", re.IGNORECASE)
SECOND_CHAIN = re.compile(r"(sc|hdc|dc|tr|sl\s*st|inc|dec)\s+in\s+(?:the\s+)?(?:2nd|second)\s+(?:ch|st)\s+from\s+hook", re.IGNORECASE)
CHAIN_RING = re.compile(r"^ch\s+(\d+)\b.*\b(?:join|joined|form\s+(?:a\s+)?(?:ring|circle))\b", re.IGNORECASE)
STITCH_ABBR = re.compile(r"\b(ch|sl\s*st|sc|hdc|dc|tr|inc|dec|sc2tog|dc2tog)\b", re.IGNORECASE)
ROW_HEADER = re.compile(r"^(Row|Rnd|Round)s?\s+(\d+)(?:\s*[-–]\s*(\d+))?\s*[:\.]?\s*(.*)", re.IGNORECASE)

def is_row_header(line):
    m = ROW_HEADER.match(line.strip())
    if m:
        s = int(m.group(2)); e = int(m.group(3)) if m.group(3) else 0
        return True, m.group(1), s, m.group(4), e
    return False, "", 0, "", 0
