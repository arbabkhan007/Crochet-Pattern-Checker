import re
REPEAT_BLOCK = re.compile(r"\(([^)]+)\)\s*[x×]\s*(\d+)", re.IGNORECASE)
EACH_AROUND = re.compile(r"(sc|hdc|dc|tr|sl\s*st|inc)\s+in\s+each\s+(st|sts)\s+around", re.IGNORECASE)
STATED_COUNT = re.compile(r"\((\d+)\)\s*$", re.IGNORECASE)
MAGIC_RING_START = re.compile(r"(\d+)\s+(sc|hdc|dc|tr)\s+(?:in|into)\s+(?:magic\s+ring|MR|magic\s+circle)", re.IGNORECASE)
REMAINING = re.compile(r"(sc|hdc|dc|tr|inc|dec)\s+in\s+(?:each\s+)?(?:remaining|rem)\s+(?:sts?)", re.IGNORECASE)
NEXT_N = re.compile(r"(sc|hdc|dc|tr|inc|dec)\s+in\s+(?:each\s+)?(?:next\s+)?(\d+)\s+(sts?)", re.IGNORECASE)
ROW_HEADER = re.compile(r"^(Row|Rnd|Round)s?\s+(\d+)(?:\s*[-–]\s*(\d+))?\s*[:\.]?\s*(.*)", re.IGNORECASE)

def is_row_header(line):
    m = ROW_HEADER.match(line.strip())
    if m:
        s = int(m.group(2)); e = int(m.group(3)) if m.group(3) else 0
        return True, m.group(1), s, m.group(4), e
    return False, "", 0, "", 0
