from __future__ import annotations
import re
from typing import Optional
from ..model.instruction import Instruction, ParsedOperation
from ..model.pattern import ConstructionType, Pattern, PatternMetadata
from ..model.row import Row, Round
from ..model.stitch import ABBREVIATION_MAP, StitchType
from .grammar import EACH_AROUND, MAGIC_RING_START, NEXT_N, REPEAT_BLOCK, REMAINING, STATED_COUNT, is_row_header

class CrochetParser:
    def parse(self, text):
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        con = self._detect(lines)
        p = Pattern(metadata=PatternMetadata(), source_text=text, construction=con)
        if con in (ConstructionType.IN_THE_ROUND, ConstructionType.JOINED_ROUNDS):
            p.rounds = self._parse_rounds(lines)
        else:
            p.rows = self._parse_rows(lines)
        return p
    def _detect(self, lines):
        ri, rwi = 0, 0
        for l in lines:
            lo = l.lower()
            ih, ht, _, _, _ = is_row_header(l)
            if ih:
                if ht.lower() in ("round","rnd"): ri += 1
                elif ht.lower() == "row": rwi += 1
            if "magic ring" in lo: ri += 2
            if "around" in lo: ri += 1
            if "turn" in lo: rwi += 1
        return ConstructionType.IN_THE_ROUND if ri > rwi else ConstructionType.FLAT
    def _parse_rounds(self, lines):
        rounds, cur = [], None
        for l in lines:
            ih, ht, num, rest, end = is_row_header(l)
            if ih and ht.lower() in ("round","rnd"):
                if cur: rounds.append(cur)
                if end > num:
                    for n in range(num, end+1):
                        rounds.append(Round(round_number=n, instructions=self._parse_inst(rest), source_text=l))
                    cur = None
                else:
                    cur = Round(round_number=num, instructions=self._parse_inst(rest), source_text=l)
            elif cur: cur.instructions.extend(self._parse_inst(l))
            elif self._looks(l):
                inst = self._parse_inst(l)
                if inst: cur = Round(round_number=1, instructions=inst, source_text=l)
        if cur: rounds.append(cur)
        return rounds
    def _parse_rows(self, lines):
        rows, cur = [], None
        for l in lines:
            ih, ht, num, rest, end = is_row_header(l)
            if ih and ht.lower() == "row":
                if cur: rows.append(cur)
                if end > num:
                    for n in range(num, end+1):
                        rows.append(Row(row_number=n, instructions=self._parse_inst(rest), source_text=l))
                    cur = None
                else:
                    cur = Row(row_number=num, instructions=self._parse_inst(rest), source_text=l)
            elif cur: cur.instructions.extend(self._parse_inst(l))
            elif self._looks(l):
                inst = self._parse_inst(l)
                if inst: cur = Row(row_number=1, instructions=inst, source_text=l)
        if cur: rows.append(cur)
        return rows
    def _looks(self, line):
        lo = line.lower()
        if any(lo.startswith(x) for x in ["materials:","yarn:","hook:","gauge:","difficulty:","notes:"]): return False
        if not re.match(r'^(row|round|rnd)\s+\d', lo):
            return any(re.search(p, lo) for p in [r'\bsc\b',r'\bdc\b',r'\bhdc\b',r'\btr\b',r'\bch\s+\d',r'\binc\b',r'\bdec\b',r'\bsl\s+st\b',r'\bmagic\s+ring\b'])
        return True
    def _parse_inst(self, text):
        text = text.strip()
        if not text: return []
        parts = re.split(r'\.\s+(?=\d|\(|sc|dc|hdc|tr|ch|inc|dec)', text.rstrip("."), flags=re.IGNORECASE)
        if len(parts) == 1: parts = re.split(r'\s*;\s*', text)
        result = []
        for p in parts:
            p = p.strip()
            if not p: continue
            i = self._one(p)
            if i: result.append(i)
        return result
    def _one(self, text):
        text = text.strip()
        if not text: return None
        ct, stated = self._stated(text)
        inst = Instruction(source_text=text, normalized_text=ct, stated_stitch_count=stated)
        if self._magic(ct, inst): return inst
        if self._repeat(ct, inst): return inst
        if self._each(ct, inst): return inst
        if self._nextn(ct, inst): return inst
        if self._countst(ct, inst): return inst
        if self._chain(ct, inst): return inst
        if self._remain(ct, inst): return inst
        if self._stimes(ct, inst): return inst
        if self._generic(ct, inst): return inst
        inst.is_ambiguous = True; inst.confidence = 0.0
        return inst
    def _stated(self, text):
        m = STATED_COUNT.search(text.strip())
        if m: return text[:m.start()].strip().rstrip(","), int(m.group(1))
        return text, None
    def _magic(self, text, inst):
        m = MAGIC_RING_START.match(text)
        if not m:
            m = re.match(r"(\d+)\s+(sc|hdc|dc|tr)\s+(?:in|into)\s+MR", text, re.IGNORECASE)
            if not m: return False
        c, st = int(m.group(1)), self._resolve(m.group(2))
        inst.operations = [ParsedOperation(stitch_type=StitchType.MAGIC_RING, count=1), ParsedOperation(stitch_type=st, count=c)]
        inst.confidence = 0.95; return True
    def _repeat(self, text, inst):
        m = REPEAT_BLOCK.search(text)
        if not m: return False
        rt, rc = m.group(1), int(m.group(2))
        unit = self._ops(rt)
        if not unit: return False
        inst.is_repeat_block = True; inst.repeat_unit = unit; inst.repeat_count = rc
        inst.operations = []
        for _ in range(rc):
            for op in unit: inst.operations.append(op.model_copy(update={"is_part_of_repeat":True,"repeat_count":rc}))
        inst.confidence = 0.9; return True
    def _each(self, text, inst):
        m = EACH_AROUND.match(text)
        if not m: return False
        inst.operations = [ParsedOperation(stitch_type=self._resolve(m.group(1)), count=1, into_stitch="each_stitch_around")]
        inst.confidence = 0.85; return True
    def _nextn(self, text, inst):
        m = NEXT_N.match(text)
        if not m: return False
        inst.operations = [ParsedOperation(stitch_type=self._resolve(m.group(1)), count=int(m.group(2)), into_stitch="next")]
        inst.confidence = 0.9; return True
    def _countst(self, text, inst):
        m = re.match(r"(\d+)\s+(ch|sl\s*st|sc|hdc|dc|tr|inc|dec|sc2tog|dc2tog)", text, re.IGNORECASE)
        if not m: return False
        inst.operations = [ParsedOperation(stitch_type=self._resolve(m.group(2)), count=int(m.group(1)))]
        inst.confidence = 0.9; return True
    def _chain(self, text, inst):
        m = re.match(r"ch\s+(\d+)", text, re.IGNORECASE)
        if not m: return False
        inst.operations = [ParsedOperation(stitch_type=StitchType.CHAIN, count=int(m.group(1)))]
        inst.confidence = 0.95; return True
    def _remain(self, text, inst):
        m = REMAINING.match(text)
        if not m: return False
        inst.operations = [ParsedOperation(stitch_type=self._resolve(m.group(1)), count=1, into_stitch="remaining")]
        inst.confidence = 0.8; return True
    def _stimes(self, text, inst):
        m = re.match(r"(ch|sl\s*st|sc|hdc|dc|tr|inc|dec|sc2tog|dc2tog)\s*[x×]\s*(\d+)", text, re.IGNORECASE)
        if not m: return False
        inst.operations = [ParsedOperation(stitch_type=self._resolve(m.group(1)), count=int(m.group(2)))]
        inst.confidence = 0.9; return True
    def _generic(self, text, inst):
        ops, pat = [], re.compile(r"(\d+)?\s*(ch|sl\s*st|sc|hdc|dc|tr|inc|dec|sc2tog|dc2tog)", re.IGNORECASE)
        for m in pat.finditer(text):
            c = int(m.group(1)) if m.group(1) else 1
            ops.append(ParsedOperation(stitch_type=self._resolve(m.group(2)), count=c))
        if ops: inst.operations = ops; inst.confidence = 0.6; return True
        return False
    def _ops(self, text):
        ops = []
        for p in [x.strip() for x in text.split(",")]:
            if not p: continue
            m = re.match(r"(\d+)\s+(.+)", p)
            if m:
                st = self._resolve2(m.group(2).strip())
                if st: ops.append(ParsedOperation(stitch_type=st, count=int(m.group(1)))); continue
            st = self._resolve2(p)
            if st: ops.append(ParsedOperation(stitch_type=st, count=1))
        return ops
    def _resolve(self, a):
        d = {"ch":StitchType.CHAIN,"sl st":StitchType.SLIP_STITCH,"slst":StitchType.SLIP_STITCH,
             "sc":StitchType.SINGLE_CROCHET,"hdc":StitchType.HALF_DOUBLE_CROCHET,"dc":StitchType.DOUBLE_CROCHET,
             "tr":StitchType.TREBLE_CROCHET,"inc":StitchType.INCREASE,"2sc":StitchType.INCREASE,
             "dec":StitchType.DECREASE,"sc2tog":StitchType.DECREASE}
        r = ABBREVIATION_MAP.lookup(a.lower().strip())
        return d.get(a.lower().strip(), r or StitchType.UNKNOWN)
    def _resolve2(self, t):
        a = {"ch":StitchType.CHAIN,"sc":StitchType.SINGLE_CROCHET,"hdc":StitchType.HALF_DOUBLE_CROCHET,
             "dc":StitchType.DOUBLE_CROCHET,"tr":StitchType.TREBLE_CROCHET,"inc":StitchType.INCREASE,"dec":StitchType.DECREASE}
        if t.lower() in a: return a[t.lower()]
        for k,v in a.items():
            if k in t.lower(): return v
        return None

def parse_pattern(text): return CrochetParser().parse(text)
def parse_instruction(text):
    r = CrochetParser()._one(text)
    return r or Instruction(source_text=text, is_ambiguous=True, confidence=0.0)
