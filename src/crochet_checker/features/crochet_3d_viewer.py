"""
3D Pattern Viewer - Generate interactive 3D visualizations of crochet patterns using WebGL
"""
from typing import Dict, List
import json


class Crochet3DViewer:
    """Generate 3D visualizations of crochet patterns"""
    
    def __init__(self):
        self.pattern_data = None
    
    def parse_pattern_to_3d(self, pattern_text: str) -> Dict:
        """Parse pattern into 3D coordinates"""
        # Simplified: create basic shapes based on pattern type
        if "blanket" in pattern_text.lower() or "square" in pattern_text.lower():
            return self._generate_flat_grid(10, 10)
        elif "hat" in pattern_text.lower() or "beanie" in pattern_text.lower():
            return self._generate_cylinder(8, 10)
        elif "amigurumi" in pattern_text.lower() or "ball" in pattern_text.lower():
            return self._generate_sphere(8)
        else:
            return self._generate_flat_grid(8, 8)
    
    def _generate_flat_grid(self, width: int, height: int) -> Dict:
        """Generate flat grid (for blankets, scarves)"""
        vertices = []
        faces = []
        
        for y in range(height):
            for x in range(width):
                vertices.append([x, y, 0])
                
                if x < width - 1 and y < height - 1:
                    v = y * width + x
                    faces.append([v, v + 1, v + width + 1, v + width])
        
        return {"vertices": vertices, "faces": faces, "type": "flat"}
    
    def _generate_cylinder(self, radius: int, height: int) -> Dict:
        """Generate cylinder (for hats)"""
        import math
        vertices = []
        faces = []
        
        # Generate points around circumference for each height level
        segments = 20
        for h in range(height):
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                x = radius * math.cos(angle)
                y = h
                z = radius * math.sin(angle)
                vertices.append([x, y, z])
        
        # Connect faces
        for h in range(height - 1):
            for i in range(segments):
                v1 = h * segments + i
                v2 = h * segments + (i + 1) % segments
                v3 = (h + 1) * segments + (i + 1) % segments
                v4 = (h + 1) * segments + i
                faces.append([v1, v2, v3, v4])
        
        return {"vertices": vertices, "faces": faces, "type": "cylinder"}
    
    def _generate_sphere(self, radius: int) -> Dict:
        """Generate sphere (for amigurumi)"""
        import math
        vertices = []
        faces = []
        
        # Generate points on sphere using spherical coordinates
        rings = 10
        segments = 20
        
        for i in range(rings + 1):
            phi = math.pi * i / rings
            for j in range(segments):
                theta = 2 * math.pi * j / segments
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.cos(phi)
                z = radius * math.sin(phi) * math.sin(theta)
                vertices.append([x, y, z])
        
        # Connect faces
        for i in range(rings):
            for j in range(segments):
                v1 = i * segments + j
                v2 = i * segments + (j + 1) % segments
                v3 = (i + 1) * segments + (j + 1) % segments
                v4 = (i + 1) * segments + j
                faces.append([v1, v2, v3, v4])
        
        return {"vertices": vertices, "faces": faces, "type": "sphere"}
    
    def generate_3d_html(self, pattern_data: Dict, output_file: str = "crochet_3d_viewer.html") -> str:
        """Generate interactive 3D viewer HTML"""
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>3D Crochet Pattern Viewer</title>
    <style>
        body {{
            margin: 0;
            overflow: hidden;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: Arial, sans-serif;
        }}
        #canvas {{
            display: block;
            width: 100vw;
            height: 100vh;
        }}
        .controls {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .controls h2 {{ margin: 0 0 10px 0; color: #667eea; }}
        .info {{ margin: 5px 0; color: #666; }}
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <div class="controls">
        <h2>🧶 3D Pattern Viewer</h2>
        <div class="info">Shape: {pattern_data['type'].title()}</div>
        <div class="info">Vertices: {len(pattern_data['vertices'])}</div>
        <div class="info">Faces: {len(pattern_data['faces'])}</div>
        <div class="info" style="margin-top: 10px; font-size: 0.9em;">
            🖱️ Drag to rotate<br>
            🔄 Scroll to zoom
        </div>
    </div>
    
    <script>
        const canvas = document.getElementById('canvas');
        const gl = canvas.getContext('webgl');
        
        // Resize canvas
        function resize() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            gl.viewport(0, 0, canvas.width, canvas.height);
        }}
        window.addEventListener('resize', resize);
        resize();
        
        // Vertex shader
        const vsSource = `
            attribute vec4 aPosition;
            uniform mat4 uModelView;
            uniform mat4 uProjection;
            void main() {{
                gl_Position = uProjection * uModelView * aPosition;
            }}
        `;
        
        // Fragment shader
        const fsSource = `
            precision mediump float;
            void main() {{
                gl_FragColor = vec4(0.4, 0.5, 0.9, 1.0);
            }}
        `;
        
        // Compile shader
        function compileShader(type, source) {{
            const shader = gl.createShader(type);
            gl.shaderSource(shader, source);
            gl.compileShader(shader);
            return shader;
        }}
        
        const vs = compileShader(gl.VERTEX_SHADER, vsSource);
        const fs = compileShader(gl.FRAGMENT_SHADER, fsSource);
        
        const program = gl.createProgram();
        gl.attachShader(program, vs);
        gl.attachShader(program, fs);
        gl.linkProgram(program);
        gl.useProgram(program);
        
        // Create vertex buffer
        const vertices = new Float32Array({json.dumps(pattern_data['vertices'])}.flat());
        const buffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
        
        const posLoc = gl.getAttribLocation(program, 'aPosition');
        gl.enableVertexAttribArray(posLoc);
        gl.vertexAttribPointer(posLoc, 3, gl.FLOAT, false, 0, 0);
        
        // Create index buffer
        const indices = new Uint16Array({json.dumps(pattern_data['faces'])}.flat());
        const indexBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);
        
        // Matrices
        const modelViewLoc = gl.getUniformLocation(program, 'uModelView');
        const projectionLoc = gl.getUniformLocation(program, 'uProjection');
        
        // Simple perspective projection
        function perspective(fov, aspect, near, far) {{
            const f = 1.0 / Math.tan(fov / 2);
            return new Float32Array([
                f / aspect, 0, 0, 0,
                0, f, 0, 0,
                0, 0, (far + near) / (near - far), -1,
                0, 0, (2 * far * near) / (near - far), 0
            ]);
        }}
        
        // Rotation matrix
        function rotateY(angle) {{
            const c = Math.cos(angle);
            const s = Math.sin(angle);
            return new Float32Array([
                c, 0, s, 0,
                0, 1, 0, 0,
                -s, 0, c, 0,
                0, 0, 0, 1
            ]);
        }}
        
        function translate(x, y, z) {{
            return new Float32Array([
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                x, y, z, 1
            ]);
        }}
        
        // Mouse interaction
        let rotation = 0;
        let isDragging = false;
        let lastX = 0;
        
        canvas.addEventListener('mousedown', (e) => {{
            isDragging = true;
            lastX = e.clientX;
        }});
        
        canvas.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                rotation += (e.clientX - lastX) * 0.01;
                lastX = e.clientX;
            }}
        }});
        
        canvas.addEventListener('mouseup', () => isDragging = false);
        
        // Render loop
        function render() {{
            gl.clearColor(0.1, 0.1, 0.2, 1.0);
            gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
            gl.enable(gl.DEPTH_TEST);
            
            const projection = perspective(Math.PI / 4, canvas.width / canvas.height, 0.1, 100.0);
            gl.uniformMatrix4fv(projectionLoc, false, projection);
            
            const modelView = translate(0, 0, -30);
            gl.uniformMatrix4fv(modelViewLoc, false, modelView);
            
            gl.drawElements(gl.LINE_LOOP, indices.length, gl.UNSIGNED_SHORT, 0);
            
            requestAnimationFrame(render);
        }}
        
        render();
    </script>
</body>
</html>"""
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        return output_file


if __name__ == "__main__":
    print("🎨 3D Crochet Pattern Viewer")
    print("=" * 50)
    
    viewer = Crochet3DViewer()
    
    print("\n📦 Generating 3D shapes...")
    
    # Test different shapes
    shapes = [
        ("Blanket", "blanket pattern"),
        ("Hat", "hat pattern"),
        ("Amigurumi", "amigurumi ball")
    ]
    
    for name, pattern in shapes:
        data = viewer.parse_pattern_to_3d(pattern)
        print(f"\n{name}:")
        print(f"  Type: {data['type']}")
        print(f"  Vertices: {len(data['vertices'])}")
        print(f"  Faces: {len(data['faces'])}")
    
    # Generate viewer
    print("\n🌐 Generating 3D viewer...")
    data = viewer.parse_pattern_to_3d("blanket pattern")
    output = viewer.generate_3d_html(data)
    print(f"✅ 3D viewer saved to: {output}")
    print("\nOpen in browser to see interactive 3D visualization!")
