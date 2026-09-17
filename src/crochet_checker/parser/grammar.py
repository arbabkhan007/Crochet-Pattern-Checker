import re
REPEAT_BLOCK = re.compile(r"[\(\[]([^)\]]+)[\)\]]\s*(?:[x×*]\s*(\d+)|(\d+)\s*times?\b)", re.IGNORECASE)
EACH_AROUND = re.compile(r"(sc|hdc|dc|tr|sl\s*st|inc)\s+in\s+each\s+(sts|stitches|stitch|st|ch|sp)(?:\s+(?:around|across))?", re.IGNORECASE)
STATED_COUNT = re.compile(r"[\(\[](\d+)[\)\]]\s*$", re.IGNORECASE)
EXACT_EACH_N = re.compile(r"(sc|hdc|dc|tr|inc|dec)\s+(?:in\s+)?(?:BLO\s+(?:of\s+)?|blo\s+(?:of\s+)?|front\s+loops?\s+(?:of\s+)?|back\s+loops?\s+(?:of\s+)?)?(?:each\s+of\s+(?:the\s+)?)?(\d+)\s+sts?(?:\s+only)?\s*$", re.IGNORECASE)
MAGIC_RING_START = re.compile(r"(\d+)\s+(sc|hdc|dc|tr)\s+(?:in|into)\s+(?:magic\s+ring|MR|magic\s+circle)", re.IGNORECASE)
REMAINING = re.compile(r"(sc|hdc|dc|tr|inc|dec)\s+in\s+(?:each\s+)?(?:remaining|rem)\s+(?:sts?)", re.IGNORECASE)
NEXT_N = re.compile(r"(sc|hdc|dc|tr|inc|dec)\s+in\s+(?:the\s+)?(?:each\s+)?(?:the\s+)?(?:next\s+)?(\d+)\s+(sts?)", re.IGNORECASE)
ROW_HEADER = re.compile(r"^(Row|Rnd|Round)s?\s+(\d+)(?:\s*[-–]\s*(\d+))?\s*[:\.]?\s*(.*)", re.IGNORECASE)

def is_row_header(line):
    m = ROW_HEADER.match(line.strip())
    if m:
        s = int(m.group(2)); e = int(m.group(3)) if m.group(3) else 0
        return True, m.group(1), s, m.group(4), e
    return False, "", 0, "", 0
