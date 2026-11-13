"""Batch-two arithmetic, translation and prose mutation checks."""
import importlib.util
from pathlib import Path
import shutil
import pytest
ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / 'reviews/ns07-ns12'
spec = importlib.util.spec_from_file_location('batch_two', FOLDER / 'verify.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_reviewed_batch():
    audit, ledger = module.verify(FOLDER)
    assert not audit.errors, audit.errors
    assert len(ledger) == 201
    assert len({r['file'] for r in ledger}) == 6

@pytest.mark.parametrize('file,old,new,diagnostic', [
    ('NS08_reviewed.md', '| (36) | head at full width |', '| (35) | head at full width |', 'output'),
    ('NS12_reviewed.md', '[BO, 5 dc, dc2tog] x 6', '[BO, 4 dc, dc2tog] x 6', 'US/UK parity'),
    ('NS07_reviewed.md', 'R4-6 | sc in each st around (3 rnd)', 'R4-7 | sc in each st around (3 rnd)', 'range length'),
    ('NS09_reviewed.md', '= 53 stitches, consuming all 42', '= 54 stitches, consuming all 42', 'changed/missing prose'),
    ('NS08_reviewed.md', '[4 sc, dec] x 6', 'unknown stitch sequence', 'unhandled'),
    ('NS10_reviewed.md', '252 sc', '250 sc', 'changed/missing prose'),
])
def test_mutations_fail(tmp_path, file, old, new, diagnostic):
    for p in FOLDER.glob('NS??_reviewed.md'):
        shutil.copy(p, tmp_path / p.name)
    shutil.copy(FOLDER / 'prose-checks.json', tmp_path / 'prose-checks.json')
    p = tmp_path / file
    assert old in p.read_text()
    p.write_text(p.read_text().replace(old, new))
    audit, _ = module.verify(tmp_path)
    assert any(diagnostic in e for e in audit.errors), audit.errors
