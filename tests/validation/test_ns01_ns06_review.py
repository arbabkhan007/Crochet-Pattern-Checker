"""Checks the attached-pattern review without changing the master collection."""
import importlib.util
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / 'reviews/ns01-ns06'
spec = importlib.util.spec_from_file_location('ns_review', FOLDER / 'verify.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_all_reviewed_tables():
    audit, ledger = module.verify(FOLDER)
    assert not audit.errors, audit.errors
    assert len(ledger) == 299
    assert len({r['file'] for r in ledger}) == 6

def test_wrong_count_is_rejected(tmp_path):
    for p in FOLDER.glob('NS??_reviewed.md'):
        shutil.copy(p, tmp_path / p.name)
    p = tmp_path / 'NS01_reviewed.md'
    p.write_text(p.read_text().replace('| (48) | fringe row 1 / ears |', '| (47) | fringe row 1 / ears |'))
    audit, _ = module.verify(tmp_path)
    assert any('output' in e for e in audit.errors)

def test_unknown_instruction_is_not_passed(tmp_path):
    p = tmp_path / 'NS01_reviewed.md'
    p.write_text((FOLDER / p.name).read_text().replace('[6 sc, inc] x 6', 'invented stitch sequence'))
    audit, _ = module.verify(tmp_path)
    assert any('unhandled' in e for e in audit.errors)
