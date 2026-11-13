"""Regression tests for the third uploaded-pattern batch."""
import importlib.util
from pathlib import Path
import shutil
import pytest
ROOT=Path(__file__).resolve().parents[2]
FOLDER=ROOT/'reviews/ns13-ns17'
spec=importlib.util.spec_from_file_location('batch_three',FOLDER/'verify.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_reviewed_batch():
    audit,ledger,noncount=module.verify(FOLDER)
    assert not audit.errors,audit.errors
    assert len(ledger)==235
    assert len(noncount)==16
    assert len({r['file'] for r in ledger})==5

@pytest.mark.parametrize('file,old,new,diagnostic',[
 ('NS14_reviewed.md','dc in next 7 sts, 2 dc in next st','dc in next 6 sts, 2 dc in next st','output'),
 ('NS13_reviewed.md','[2 dc, dc2tog] x 6','[3 dc, dc2tog] x 6','US/UK parity'),
 ('NS16_reviewed.md','(7) | consumes 8 of 10','(8) | consumes 8 of 10','special stated count'),
 ('NS17_reviewed.md','[5 sc, inc] x 6','invented stitch sequence','UNHANDLED'),
 ('NS13_reviewed.md','R5-6 | sc in each st around (2 rnd)','R5-7 | sc in each st around (2 rnd)','range length'),
 ('NS17_reviewed.md','13 peaks require ch 39','13 peaks require ch 40','changed/missing prose'),
 ('NS14_reviewed.md','168 ÷ 6 = 28 scallops','168 ÷ 6 = 29 scallops','changed/missing prose'),
 ('NS16_reviewed.md','change from AC back to MC for Foot R1','continue AC for Foot R1','changed/missing prose'),
])
def test_mutations_rejected(tmp_path,file,old,new,diagnostic):
    for p in FOLDER.glob('NS??_reviewed.md'):shutil.copy(p,tmp_path/p.name)
    for name in ('special-cases.json','prose-checks.json'):shutil.copy(FOLDER/name,tmp_path/name)
    p=tmp_path/file
    assert old in p.read_text()
    p.write_text(p.read_text().replace(old,new))
    audit,_,_=module.verify(tmp_path)
    assert any(diagnostic in e for e in audit.errors),audit.errors
