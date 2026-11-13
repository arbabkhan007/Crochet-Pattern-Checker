"""Self-contained regression tests: python reviews/edition-2/check_tests.py."""
from pathlib import Path
import tempfile, shutil, unittest, importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('edition2_verify',HERE/'verify.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class EditionTwoTests(unittest.TestCase):
    def test_all_patterns(self):
        a,l,s=v.verify(HERE)
        self.assertEqual(a.errors,[])
        self.assertEqual(len(l),710)
        self.assertEqual(len(s),15)
        self.assertEqual(len({r['file'] for r in l}),17)

    def test_mutations_fail(self):
        mutations=[
          ('NS01','| R20 | [2 sc, dec] x 6 | 18 |','| R20 | [2 sc, dec] x 6 | 17 |','output'),
          ('NS02','| (23) | counted sts','| (24) | counted sts','output'),
          ('NS04','[sc, inc] x 1, join BL2','[sc, inc] x 2, join BL2','UNHANDLED'),
          ('NS09','| (35) | head & flippers','| (34) | head & flippers','manual stated'),
          ('NS12','[BO, 5 dc, dc2tog] x 6','[BO, 4 dc, dc2tog] x 6','US/UK'),
          ('NS16','2 sc, dec; ch 1, turn','2 sc, dec; do not turn','manual input'),
          ('NS16','so the RS/outside faces you','so the WS/inside faces you','changed/missing'),
          ('NS17','near Body Rnds 8–10 at the lower centre back','near Body Rnds 19–20 at the upper back','changed/missing'),
        ]
        for code,old,new,expected in mutations:
            with self.subTest(code=code,change=old), tempfile.TemporaryDirectory() as d:
                dst=Path(d)
                for p in HERE.glob('NS??_edition2.md'):shutil.copy(p,dst/p.name)
                for name in ['cases.json','prose-checks.json']:shutil.copy(HERE/name,dst/name)
                p=dst/f'{code}_edition2.md';self.assertIn(old,p.read_text());p.write_text(p.read_text().replace(old,new))
                a,_,_=v.verify(dst)
                self.assertTrue(a.errors,'Mutation was silently accepted')
                # Every scenario must fail; some trigger more than one downstream rule.

    def test_coco_reference_map(self):
        # Trace the corrected join instructions block-by-block, not physical angles.
        r4=[('BL1',3,3),('plain',2,3),('BL2',3,3),('plain',10,15)]
        r5=[('plain',12,16),('FL1',3,3),('plain',3,4),('FL2',3,3),('plain',3,4)]
        back={};front={};old=new=1
        for name,used,made in r4:
            if name.startswith('BL'):back[name]=set(range(new,new+made))
            old+=used;new+=made
        self.assertEqual((old-1,new-1),(18,24))
        old=new=1
        for name,used,made in r5:
            if name.startswith('FL'):front[name]=set(range(old,old+used))
            old+=used;new+=made
        self.assertEqual((old-1,new-1),(24,30))
        self.assertEqual([sorted(x) for x in [*back.values(),*front.values()]],[[1,2,3],[7,8,9],[13,14,15],[19,20,21]])
        allsets=[*back.values(),*front.values()]
        self.assertEqual(len(set.union(*allsets)),12)

    def test_turtle_symmetry(self):
        for total,head,flippers in [(24,4,[9,13,19,23]),(42,8,[16,24,34,42])]:
            offsets={(p-head)%total for p in flippers}
            self.assertEqual(offsets,{(-x)%total for x in offsets})

    def test_star_wrap(self):
        anchors=[(2+k-1)%10+1 for k in range(10)]
        self.assertEqual(anchors,[2,3,4,5,6,7,8,9,10,1])
        self.assertEqual(len(set(anchors)),10)

    def test_sash_modules(self):
        for peaks in range(2,25):
            row=3*peaks-1
            positions=[1+3*k for k in range(peaks)]
            self.assertEqual(positions[-1],row-1)
            self.assertEqual(1+3*(peaks-1)+1,row)
if __name__=='__main__':unittest.main(verbosity=2)
