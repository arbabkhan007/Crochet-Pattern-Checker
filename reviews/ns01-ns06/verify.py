"""Table arithmetic audit; exact-text manual cases fail closed on edits.
Run: python reviews/ns01-ns06/verify.py
Not a physical construction or safety test.
"""
from pathlib import Path
import sys, re, json
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from pattern_release_audit import Audit, parse_rows, canonical_math, MANUAL, norm

EXTRA = {
 norm('ch 2, turn, hdc across'): (60,60),
 norm('BLO sc around in Yarn C'): (18,18),
 norm('ch 1, turn; 6 sc, inc in each of next 3, 2 sc (last 3 sts of R1 stay unworked)'): (11,14),
 norm('[sc, inc] x 3, join FL1: 3 sc, [sc, inc] x 3, 3 sc, join FL2: 3 sc, 3 sc'): (24,30),
}
def verify(folder):
 audit=Audit(); ledger=[]
 for path in sorted(folder.glob('NS??_reviewed.md')):
  rows=parse_rows(path,audit); prev=None; table=None
  for row in rows:
   if table != row.table: prev=None; table=row.table
   s=norm(row.instruction)
   if row.stated is None:
    if s == 'back legs: [sc, invdec] x 3; front legs: sc in each st around':
     audit.equal(prev,9,'Coco branch input'); audit.equal(row.stated_text,'(6 back / 9 front)','Coco branch counts')
     ledger.append(dict(file=path.name,line=row.line,instruction=row.instruction,consumed=9,produced='6 back / 9 front',method='explicit branch'))
     prev=9 # only front legs continue
    elif re.fullmatch(r'ch \d+',s): prev=int(s.split()[1])-1
    else: audit.check(False,f'{path.name}:{row.line}: unhandled uncounted instruction {s}')
    continue
   math=EXTRA.get(s) or canonical_math(row.instruction,prev) or MANUAL.get(s)
   audit.check(math is not None,f'{path.name}:{row.line}: unhandled {s}')
   if math is None: continue
   used,made=math
   audit.equal(made,row.stated,f'{path.name}:{row.line} output')
   partial='last 3 sts of r1 stay unworked' in s
   if prev is not None and used not in (None,0):
    audit.equal(used+(3 if partial else 0),prev,f'{path.name}:{row.line} input')
   ledger.append(dict(file=path.name,line=row.line,instruction=row.instruction,consumed=used,produced=made,method='explicit' if s in EXTRA or canonical_math(row.instruction,prev) is None else 'canonical'))
   prev=made
 return audit,ledger
if __name__=='__main__':
 folder=Path(__file__).resolve().parent
 audit,ledger=verify(folder)
 (folder/'stitch-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
 print(f'{len(ledger)} table instructions; {audit.checks} assertions; {len(audit.errors)} errors')
 for error in audit.errors: print(error)
 sys.exit(bool(audit.errors))
