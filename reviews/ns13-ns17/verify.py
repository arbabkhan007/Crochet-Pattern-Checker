"""Written-table audit for batch three. Run from repository root.
Unknown instructions fail closed; variable-length rounds are representative,
not a claimed fixed number of rounds. No physical/safety certification.
"""
from pathlib import Path
import sys, re, json
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from pattern_release_audit import Audit, canonical_math, MANUAL, norm, translate_us_to_uk

EXTRA = {
 'sc in 2nd ch and next 12 ch, ch 1, turn': (13,13),
 'with mc, sc in each st around': (20,20),
}

def tables(text):
    header=None; table=0; section=''
    for number,line in enumerate(text.splitlines(),1):
        if line.startswith('#'): section=line.lstrip('#').strip()
        if not line.startswith('|'): header=None; continue
        cells=[c.strip() for c in line.strip('|').split('|')]
        if header is None:
            header=[c.lower() for c in cells]; table+=1; continue
        if all(re.fullmatch(':?-{3,}:?',c) for c in cells): continue
        if 'sts' not in header: continue
        yield number,table,section,header,cells

def verify(folder):
    audit=Audit(); ledger=[]; uncounted=[]
    paths=sorted(folder.glob('NS??_reviewed.md'))
    audit.equal([p.name for p in paths],[f'NS{i}_reviewed.md' for i in range(13,18)],'inventory')
    special=json.loads((folder/'special-cases.json').read_text())
    cases={(x['file'],norm(x['instruction'])):x for x in special}
    for path in paths:
        prev=None; oldtable=None
        for line,table,section,header,cells in tables(path.read_text()):
            loc=f'{path.name}:{line}'
            audit.equal(len(cells),len(header),loc+' table width')
            if len(cells)!=len(header): continue
            ui=header.index('us terms') if 'us terms' in header else header.index('instruction')
            label=cells[ui-1]; instruction=cells[ui]; s=norm(instruction)
            if 'uk terms' in header or 'uk equivalent' in header:
                ki=header.index('uk terms') if 'uk terms' in header else header.index('uk equivalent')
                audit.equal(norm(cells[ki]).replace("half treble", "htr"),norm(translate_us_to_uk(instruction)),loc+' US/UK parity')
            if table!=oldtable:
                continuation=path.name.startswith('NS14') or (path.name.startswith('NS16') and label in ('Row 1','Foot R1','Toe R1'))
                if not continuation: prev=None
                oldtable=table
            count=re.fullmatch(r'\((\d+)(?: each)?\)',cells[header.index('sts')])
            if count is None and re.fullmatch(r'ch \d+',s):
                prev=int(s.split()[1])-1;continue
            case=cases.get((path.name,s))
            if case:
                audit.equal(cells[header.index('sts')],case['stated'],loc+' special stated count')
                for arithmetic in case.get('arithmetic',[]):
                    audit.equal(sum(arithmetic['terms']),arithmetic['expected'],loc+' '+arithmetic['label'])
                if 'previous' in case: audit.equal(prev,case['previous'],loc+' special previous')
                if 'produced' in case:
                    if count: audit.equal(case['produced'],int(count[1]),loc+' output')
                    ledger.append(dict(file=path.name,line=line,label=label,instruction=instruction,produced=case['produced'],method=case['method']))
                    prev=case['produced']
                else:
                    uncounted.append(dict(file=path.name,line=line,label=label,instruction=instruction,reason=case['method']))
                continue
            if not count:
                audit.check(False,loc+' UNHANDLED UNCOUNTED '+instruction);continue
            rng=re.fullmatch(r'R(?:nds?\s*)?(\d+)[–-](\d+)',label,re.I)
            nums=range(int(rng[1]),int(rng[2])+1) if rng else [label]
            suffix=re.search(r'\((\d+) rnd\)$',s)
            if rng: audit.equal(int(suffix[1]) if suffix else None,len(nums),loc+' range length')
            clean=re.sub(r' \(\d+ rnd\)$','',instruction)
            for n in nums:
                result=EXTRA.get(s) or canonical_math(clean,prev) or MANUAL.get(s)
                audit.check(result is not None,loc+' UNHANDLED '+instruction)
                if result is None:continue
                used,made=result
                audit.equal(made,int(count[1]),loc+' output')
                if used not in (None,0) and prev is not None: audit.equal(used,prev,loc+' input')
                ledger.append(dict(file=path.name,line=line,label=n,instruction=instruction,consumed=used,produced=made,method='canonical/exact text'))
                prev=made
    for case in json.loads((folder/'prose-checks.json').read_text()):
        audit.check(case['instruction'] in (folder/case['file']).read_text(),case['file']+' changed/missing prose: '+case['name'])
        for x in case['arithmetic']:audit.equal(sum(x['terms']),x['expected'],case['name']+' '+x['label'])
    return audit,ledger,uncounted

if __name__=='__main__':
    folder=Path(__file__).resolve().parent
    audit,ledger,uncounted=verify(folder)
    (folder/'stitch-ledger.json').write_text(json.dumps({'counted':ledger,'explicit_noncount_cases':uncounted},indent=2)+'\n')
    print(f'{len(ledger)} counted row/round records; {len(uncounted)} explicit noncount cases; {audit.checks} assertions; {len(audit.errors)} errors')
    for e in audit.errors:print(e)
    sys.exit(bool(audit.errors))
