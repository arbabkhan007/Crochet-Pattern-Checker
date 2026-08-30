"""Tests for 3D simulation."""
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.simulation.mesh import Mesh, Vec3, generate_sphere_mesh, generate_tube_mesh, generate_flat_circle_mesh, generate_hat_mesh
from crochet_checker.simulation.surface import simulate_surface, analyze_pattern_shape, DetectedShape

class TestVec3:
    def test_add(self):
        v = Vec3(x=1,y=2,z=3) + Vec3(x=4,y=5,z=6)
        assert v.x==5 and v.y==7 and v.z==9
    def test_length(self):
        assert abs(Vec3(x=3,y=4,z=0).length() - 5.0) < 0.01
    def test_normalized(self):
        assert abs(Vec3(x=0,y=0,z=5).normalized().z - 1.0) < 0.01

class TestMesh:
    def test_vertex(self):
        m = Mesh(); idx = m.add_vertex(1,2,3)
        assert idx==0 and m.vertex_count==1
    def test_face(self):
        m = Mesh(); m.add_vertex(0,0,0); m.add_vertex(1,0,0); m.add_vertex(0,1,0); m.add_face(0,1,2)
        assert m.face_count==1
    def test_obj(self):
        m = Mesh(); m.add_vertex(0,0,0); m.add_vertex(1,0,0); m.add_vertex(0,1,0); m.add_face(0,1,2)
        obj = m.to_obj(); assert "v 0" in obj and "f 1 2 3" in obj

class TestMeshGen:
    def test_sphere(self):
        m = generate_sphere_mesh(5.0, 16, 8); assert m.vertex_count > 0 and m.face_count > 0
    def test_tube(self):
        m = generate_tube_mesh(3,3,10,16); assert m.vertex_count > 0
    def test_circle(self):
        m = generate_flat_circle_mesh(5.0, 24); assert m.face_count == 24
    def test_hat(self):
        m = generate_hat_mesh(5,7,8,segments=24); assert m.vertex_count > 0

class TestShapeAnalysis:
    def test_sphere(self):
        t = chr(10).join(["Round 1: 6 sc into magic ring (6)","Round 2: (sc, inc) x 6 (18)","Round 3: (2 sc, inc) x 6 (24)","Round 4: (sc, dec) x 6 (18)","Round 5: dec x 6 (6)"])
        a = analyze_pattern_shape(parse_pattern(t))
        assert a.detected_shape in (DetectedShape.SPHERE, DetectedShape.HAT)
    def test_flat_circle(self):
        t = chr(10).join(["Round 1: 6 sc into magic ring (6)","Round 2: (sc, inc) x 6 (18)","Round 3: (2 sc, inc) x 6 (24)","Round 4: (3 sc, inc) x 6 (30)","Round 5: (4 sc, inc) x 6 (36)"])
        a = analyze_pattern_shape(parse_pattern(t))
        assert a.detected_shape in (DetectedShape.FLAT_CIRCLE, DetectedShape.BOWL)

class TestSurface:
    def test_generates_mesh(self):
        t = chr(10).join(["Round 1: 6 sc into magic ring (6)","Round 2: (sc, inc) x 6 (18)","Round 3: (2 sc, inc) x 6 (24)"])
        m = simulate_surface(parse_pattern(t)); assert m.vertex_count > 0
    def test_obj_export(self):
        t = chr(10).join(["Round 1: 6 sc into magic ring (6)","Round 2: (sc, inc) x 6 (18)"])
        m = simulate_surface(parse_pattern(t)); obj = m.to_obj()
        assert obj.startswith("#") and "v " in obj and "f " in obj
