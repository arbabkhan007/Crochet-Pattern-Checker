"""3D mesh data structure and OBJ export."""
from __future__ import annotations
import math
from pydantic import BaseModel, Field

class Vec3(BaseModel):
    x: float = 0.0; y: float = 0.0; z: float = 0.0
    def __add__(self, o): return Vec3(x=self.x+o.x, y=self.y+o.y, z=self.z+o.z)
    def __sub__(self, o): return Vec3(x=self.x-o.x, y=self.y-o.y, z=self.z-o.z)
    def __mul__(self, s): return Vec3(x=self.x*s, y=self.y*s, z=self.z*s)
    def length(self): return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def normalized(self):
        l = self.length()
        return Vec3(x=self.x/l, y=self.y/l, z=self.z/l) if l > 0 else Vec3()

class Mesh(BaseModel):
    vertices: list[Vec3] = Field(default_factory=list)
    faces: list[tuple] = Field(default_factory=list)
    name: str = "crochet_mesh"
    @property
    def vertex_count(self): return len(self.vertices)
    @property
    def face_count(self): return len(self.faces)
    def add_vertex(self, x, y, z):
        self.vertices.append(Vec3(x=x, y=y, z=z)); return len(self.vertices)-1
    def add_face(self, v1, v2, v3): self.faces.append((v1, v2, v3))
    def add_quad(self, v1, v2, v3, v4):
        self.faces.append((v1, v2, v3)); self.faces.append((v1, v3, v4))
    def bounding_box(self):
        if not self.vertices: return Vec3(), Vec3()
        mn = Vec3(x=float("inf"), y=float("inf"), z=float("inf"))
        mx = Vec3(x=float("-inf"), y=float("-inf"), z=float("-inf"))
        for v in self.vertices:
            mn.x=min(mn.x,v.x); mn.y=min(mn.y,v.y); mn.z=min(mn.z,v.z)
            mx.x=max(mx.x,v.x); mx.y=max(mx.y,v.y); mx.z=max(mx.z,v.z)
        return mn, mx
    def to_obj(self):
        lines = [f"# Crochet Pattern Checker 3D Mesh", f"# Object: {self.name}", ""]
        for v in self.vertices: lines.append(f"v {v.x:.6f} {v.y:.6f} {v.z:.6f}")
        lines.append("")
        for f in self.faces: lines.append(f"f {f[0]+1} {f[1]+1} {f[2]+1}")
        return chr(10).join(lines)
    def save_obj(self, filepath):
        from pathlib import Path; Path(filepath).write_text(self.to_obj())

def generate_sphere_mesh(radius, segments=24, rings=12, center=None):
    if center is None: center = Vec3()
    mesh = Mesh(name="sphere")
    top_idx = mesh.add_vertex(center.x, center.y+radius, center.z)
    ring_indices = []
    for j in range(1, rings):
        phi = math.pi*j/rings; rr = radius*math.sin(phi); ry = center.y+radius*math.cos(phi)
        cr = []
        for i in range(segments):
            theta = (2*math.pi*i)/segments
            cr.append(mesh.add_vertex(center.x+rr*math.cos(theta), ry, center.z+rr*math.sin(theta)))
        ring_indices.append(cr)
    bot_idx = mesh.add_vertex(center.x, center.y-radius, center.z)
    for i in range(segments):
        mesh.add_face(top_idx, ring_indices[0][(i+1)%segments], ring_indices[0][i])
    for j in range(len(ring_indices)-1):
        for i in range(segments):
            ni=(i+1)%segments
            mesh.add_quad(ring_indices[j][i], ring_indices[j][ni], ring_indices[j+1][ni], ring_indices[j+1][i])
    lr = ring_indices[-1]
    for i in range(segments):
        mesh.add_face(bot_idx, lr[i], lr[(i+1)%segments])
    return mesh

def generate_tube_mesh(bottom_radius, top_radius, height, segments=24, center=None):
    if center is None: center = Vec3()
    mesh = Mesh(name="tube")
    bi = []
    for i in range(segments):
        a = (2*math.pi*i)/segments
        bi.append(mesh.add_vertex(center.x+bottom_radius*math.cos(a), center.y, center.z+bottom_radius*math.sin(a)))
    ti = []
    for i in range(segments):
        a = (2*math.pi*i)/segments
        ti.append(mesh.add_vertex(center.x+top_radius*math.cos(a), center.y+height, center.z+top_radius*math.sin(a)))
    for i in range(segments):
        ni=(i+1)%segments; mesh.add_quad(bi[i], bi[ni], ti[ni], ti[i])
    bc = mesh.add_vertex(center.x, center.y, center.z)
    for i in range(segments): mesh.add_face(bc, bi[(i+1)%segments], bi[i])
    tc = mesh.add_vertex(center.x, center.y+height, center.z)
    for i in range(segments): mesh.add_face(tc, ti[i], ti[(i+1)%segments])
    return mesh

def generate_flat_circle_mesh(radius, segments=36, center=None):
    if center is None: center = Vec3()
    mesh = Mesh(name="flat_circle")
    ci = mesh.add_vertex(center.x, center.y, center.z)
    ri = []
    for i in range(segments):
        a = (2*math.pi*i)/segments
        ri.append(mesh.add_vertex(center.x+radius*math.cos(a), center.y, center.z+radius*math.sin(a)))
    for i in range(segments): mesh.add_face(ci, ri[i], ri[(i+1)%segments])
    return mesh

def generate_hat_mesh(crown_radius, brim_radius, crown_height, brim_height=2.0, segments=36, center=None):
    if center is None: center = Vec3()
    mesh = Mesh(name="hat")
    cc = Vec3(x=center.x, y=center.y+brim_height, z=center.z)
    crown = generate_sphere_mesh(crown_radius, segments, segments//2, cc)
    for v in crown.vertices: mesh.add_vertex(v.x, v.y, v.z)
    for f in crown.faces: mesh.add_face(f[0], f[1], f[2])
    ir, orr = [], []
    by = center.y + brim_height
    for i in range(segments):
        a = (2*math.pi*i)/segments
        ir.append(mesh.add_vertex(center.x+crown_radius*math.cos(a), by, center.z+crown_radius*math.sin(a)))
        orr.append(mesh.add_vertex(center.x+brim_radius*math.cos(a), by, center.z+brim_radius*math.sin(a)))
    for i in range(segments):
        ni=(i+1)%segments; mesh.add_quad(ir[i], ir[ni], orr[ni], orr[i])
    return mesh
