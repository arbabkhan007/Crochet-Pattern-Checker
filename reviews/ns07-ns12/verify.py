"""Fail-closed table arithmetic and selected prose-construction checks.
Run from the repo root: python reviews/ns07-ns12/verify.py
Uses the repository's exact-text manual arithmetic for noncanonical rows.
This is not a test-crochet, dimensional measurement or safety test.
"""
from pathlib import Path
import sys
import re
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from pattern_release_audit import Audit, parse_rows, canonical_math, MANUAL, norm, translate_us_to_uk

GRANNY = 'sl st in next 2 dc and into the next corner ch-2 space; ch 3 (counts as first dc), 2 dc, ch 2, 3 dc in that same corner. Work 3 dc in every GAP between adjacent 3-dc groups along each side (these are not chain spaces), and (3 dc, ch 2, 3 dc) in each remaining corner; sl st to top of ch-3. Each round adds one 3-dc group to every side (+12 dc per round)'

def verify(folder):
    audit = Audit()
    ledger = []
    paths = sorted(folder.glob('NS??_reviewed.md'))
    audit.equal([p.name for p in paths], [f'NS{i:02}_reviewed.md' for i in range(7,13)], 'file inventory')
    for path in paths:
        text = path.read_text()
        rows = parse_rows(path, audit)
        prev = None
        table = None
        for row in rows:
            loc = f'{path.name}:{row.line}'
            # The reader recognizes "UK terms", whereas these uploads use
            # "UK equivalent". Read the actual fourth-column count/third-column UK text.
            if path.name.startswith(('NS11', 'NS12')):
                cells = text.splitlines()[row.line - 1].strip('|').split('|')
                audit.equal(norm(cells[2]), norm(translate_us_to_uk(row.instruction)), loc + ' US/UK parity')
            s = norm(row.instruction)
            if table != row.table:
                # Only these tables intentionally continue an existing piece.
                continuation = path.name.startswith('NS11') or (path.name.startswith('NS09') and row.label == 'R5')
                if not continuation: prev = None
                table = row.table
            if re.fullmatch(r'ch \d+', s) and row.stated is None:
                prev = int(s.split()[1]) - 1
                continue
            if row.stated is None:
                audit.equal(row.instruction, GRANNY, loc + ' unknown uncounted instruction')
                audit.equal(row.label, 'Rnds 3-20', loc + ' granny range')
                audit.equal(prev, 24, loc + ' granny start')
                if row.instruction == GRANNY:
                    for n in range(3,21):
                        # 4 corners each make 6 dc; each side has n-2 intergroup gaps.
                        made = 4 * 6 + 4 * (n-2) * 3
                        audit.equal(made, 12*n, loc + f' granny R{n}')
                        ledger.append(dict(file=path.name,line=row.line,round=n,consumed_groups=4*(n-2),corners=4,produced=made,method='explicit granny spaces'))
                    prev = 240
                continue
            range_match = re.fullmatch(r'R(?:nds?\s*)?(\d+)-(\d+)', row.label, re.I)
            rounds = range(int(range_match[1]), int(range_match[2])+1) if range_match else [row.label]
            suffix = re.search(r'\((\d+) rnd\)$', s)
            if range_match:
                audit.equal(int(suffix[1]) if suffix else None, len(rounds), loc + ' range length')
            clean = re.sub(r' \(\d+ rnd\)$','',row.instruction)
            for number in rounds:
                math = canonical_math(clean, prev) or MANUAL.get(s)
                audit.check(math is not None, loc + ' unhandled ' + s)
                if math is None: continue
                used, made = math
                audit.equal(made, row.stated, loc + ' output')
                if prev is not None and used not in (None, 0):
                    audit.equal(used, prev, loc + ' input')
                ledger.append(dict(file=path.name,line=row.line,round=number,instruction=row.instruction,consumed=used,produced=made,method='canonical or exact-text arithmetic'))
                prev = made
    # Selected prose instructions must match reviewed text, not just cached totals.
    for item in json.loads((folder/'prose-checks.json').read_text()):
        text = (folder/item['file']).read_text()
        audit.check(item['instruction'] in text, item['file'] + ' changed/missing prose: ' + item['name'])
        for counts in item['arithmetic']:
            audit.equal(sum(counts['terms']), counts['expected'], item['name'] + ': ' + counts['label'])
    return audit, ledger

if __name__ == '__main__':
    folder = Path(__file__).resolve().parent
    audit, ledger = verify(folder)
    (folder/'stitch-ledger.json').write_text(json.dumps(ledger, indent=2)+'\n')
    print(f'{len(ledger)} expanded round/row records; {audit.checks} assertions; {len(audit.errors)} errors')
    for e in audit.errors: print(e)
    sys.exit(bool(audit.errors))
