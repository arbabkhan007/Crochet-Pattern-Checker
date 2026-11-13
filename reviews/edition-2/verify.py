"""Edition-2 table audit. Exact-text manual cases fail closed on edits.
Run from repository root. Written arithmetic only, not shape/fit validation.
"""
from pathlib import Path
import sys,re,json
ROOT = Path(__file__).resolve().parent
TOOLS = ROOT / 'tools' if (ROOT / 'tools').exists() else ROOT.parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
from pattern_release_audit import Audit, canonical_math, MANUAL, norm, translate_us_to_uk

def rows(text):
 header=None;tab=0
 for ln,line in enumerate(text.splitlines(),1):
  if not line.startswith('|'):header=None;continue
  cells=[s.strip() for s in line.strip('|').split('|')]
  if header is None:header=[s.lower() for s in cells];tab+=1;continue
  if all(re.fullmatch(':?-{3,}:?',x) for x in cells):continue
  if not ('sts' in header or 'count' in header):continue
  ui=next((header.index(h) for h in ['us terms','instruction','instruction (us)','exact instruction'] if h in header),None)
  if ui is None:continue
  ci=header.index('sts') if 'sts' in header else header.index('count')
  yield ln,tab,header,cells,ui,ci

def verify(folder):
 a=Audit();ledger=[];scope=[]
 paths=sorted(folder.glob('NS??_edition2.md'))
 a.equal(len(paths),17,'file inventory')
 cases={(x['file'],norm(x['instruction'])):x for x in json.loads((folder/'cases.json').read_text())}
 for p in paths:
  prev=None;tab=None
  for ln,nt,h,c,ui,ci in rows(p.read_text()):
   loc=f'{p.name}:{ln}';a.equal(len(c),len(h),loc+' columns')
   inst=c[ui];s=norm(inst);label=c[ui-1];value=c[ci]
   if 'uk terms' in h or 'uk equivalent' in h:
    ki=h.index('uk terms') if 'uk terms' in h else h.index('uk equivalent')
    a.equal(norm(c[ki]).replace('half treble','htr'),norm(translate_us_to_uk(inst)),loc+' US/UK')
   if nt!=tab:
    cont=p.name[:4] in ('NS11','NS14') or (p.name[:4]=='NS16' and label in ('Row 1','Foot R1','Toe R1')) or (p.name[:4]=='NS09' and label=='R5')
    if not cont:prev=None
    tab=nt
   m=re.fullmatch(r'\(?(\d+)(?: each)?\)?',value)
   case=cases.get((p.name,s))
   if case:
    a.equal(value,case['stated'],loc+' manual stated')
    if 'previous' in case:a.equal(prev,case['previous'],loc+' manual input')
    for eq in case.get('arithmetic',[]):a.equal(sum(eq['terms']),eq['expected'],loc+' '+eq['label'])
    if 'produced' in case:
     if m:a.equal(case['produced'],int(m[1]),loc+' manual output')
     prev=case['produced'];ledger.append(dict(file=p.name,line=ln,instruction=inst,produced=prev,method='exact-text manual'))
    else:scope.append(dict(file=p.name,line=ln,instruction=inst,scope=case['method']))
    continue
   if s.startswith('ch ') and re.fullmatch('ch [0-9]+',s):
    prev=int(s.split()[1])-1;continue
   if not m:a.check(False,loc+' UNCOUNTED '+inst);continue
   rng=re.fullmatch(r'R(?:nds?\s*)?(\d+)[–-]R?(\d+)',label,re.I)
   numbers=range(int(rng[1]),int(rng[2])+1) if rng else [label]
   suffix=re.search(r'\((\d+) rnd\)$',s)
   if suffix and rng:a.equal(int(suffix[1]),len(numbers),loc+' range')
   clean=re.sub(r' \(\d+ rnd\)$','',inst).replace('sc around each round','sc in each st around')
   if clean=='inc around':clean='inc in each st around'
   for num in numbers:
    result=canonical_math(clean,prev) or MANUAL.get(s)
    a.check(result is not None,loc+' UNHANDLED '+inst)
    if result is None:continue
    used,made=result;a.equal(made,int(m[1]),loc+' output')
    if used not in (None,0) and prev is not None:a.equal(used,prev,loc+' input')
    ledger.append(dict(file=p.name,line=ln,round=num,instruction=inst,consumed=used,produced=made));prev=made
 # Body text, closures, variants and spatial assertions have separate explicit coverage.
 for case in json.loads((folder/'prose-checks.json').read_text()):
  a.check(case['instruction'] in (folder/case['file']).read_text(),case['name']+' changed/missing')
  for eq in case['arithmetic']:a.equal(sum(eq['terms']),eq['expected'],case['name']+' '+eq['label'])
 return a,ledger,scope
if __name__=='__main__':
 folder=Path(__file__).resolve().parent;a,l,s=verify(folder)
 (folder/'stitch-ledger.json').write_text(json.dumps(dict(counted=l,explicit_scope=s),indent=2)+'\n')
 print(f'{len(l)} counted records; {len(s)} explicit scoped records; {a.checks} assertions; {len(a.errors)} errors')
 for e in a.errors:print(e)
 sys.exit(bool(a.errors))
