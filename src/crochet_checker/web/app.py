"""FastAPI web application for crochet pattern checker."""
from __future__ import annotations
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from ..parser.parser import CrochetParser
from ..validation import validate_pattern
from ..visualization import render_2d_preview, measure_pattern
from ..simulation import simulate_surface
from ..pdf import PDFConfig, PDFGenerator

app = FastAPI(title="Crochet Pattern Checker", version="0.5.0")

class CheckRequest(BaseModel):
    pattern_text: str

@app.get("/", response_class=HTMLResponse)
async def index():
    return get_frontend_html()

@app.post("/api/check")
async def check_pattern(request: CheckRequest):
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        report = validate_pattern(pattern)
        m = measure_pattern(pattern)
        return {"status": report.overall_status, "score": report.score,
                "errors": [{"message": e.message, "location": e.location} for e in report.errors],
                "warnings": [{"message": w.message, "location": w.location} for w in report.warnings],
                "rounds": m.total_rounds, "max_stitches": m.max_stitch_count,
                "max_diameter_inches": round(m.max_diameter_inches, 2),
                "total_height_inches": round(m.total_height_inches, 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/upload")
async def upload_pattern(file: UploadFile = File(...)):
    try:
        text = (await file.read()).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read file")
    try:
        pattern = CrochetParser().parse(text)
        report = validate_pattern(pattern)
        m = measure_pattern(pattern)
        return {"status": report.overall_status, "score": report.score,
                "errors": [{"message": e.message, "location": e.location} for e in report.errors],
                "warnings": [{"message": w.message, "location": w.location} for w in report.warnings],
                "rounds": m.total_rounds, "max_stitches": m.max_stitch_count,
                "max_diameter_inches": round(m.max_diameter_inches, 2),
                "total_height_inches": round(m.total_height_inches, 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/render")
async def render_pattern(request: CheckRequest):
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        report = validate_pattern(pattern)
        svg = render_2d_preview(pattern, report)
        return {"svg": svg, "status": report.overall_status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/simulate")
async def simulate_pattern(request: CheckRequest):
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        result = simulate_surface(pattern)
        return {"shape": result.detected_shape.value, "confidence": round(result.confidence, 2),
                "vertices": len(result.mesh.vertices), "faces": len(result.mesh.faces), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/pdf")
async def generate_pdf(request: CheckRequest, designer: Optional[str] = None):
    try:
        pattern = CrochetParser().parse(request.pattern_text)
        report = validate_pattern(pattern)
        config = PDFConfig(designer_name=designer or "")
        html = PDFGenerator(config).generate(pattern, report)
        return {"html": html, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.5.0"}


def get_frontend_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Crochet Pattern Checker</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}
.container{max-width:1200px;margin:0 auto}
header{text-align:center;color:white;padding:40px 0}
header h1{font-size:2.5em;margin-bottom:10px}
header p{font-size:1.2em;opacity:.9}
.main-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}
.panel{background:white;border-radius:12px;padding:25px;box-shadow:0 10px 40px rgba(0,0,0,.2)}
.panel h2{color:#333;margin-bottom:15px;font-size:1.3em}
textarea{width:100%;height:300px;border:2px solid #e0e0e0;border-radius:8px;padding:15px;font-family:monospace;font-size:14px;resize:vertical}
textarea:focus{outline:none;border-color:#667eea}
.btn{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;padding:12px 30px;border-radius:8px;font-size:16px;cursor:pointer;margin:10px 5px 10px 0}
.btn:hover{opacity:.9}
.result-box{margin-top:20px;padding:20px;border-radius:8px;background:#f8f9fa}
.status-pass{background:#d4edda;color:#155724;border:1px solid #c3e6cb}
.status-warn{background:#fff3cd;color:#856404;border:1px solid #ffeaa7}
.status-error{background:#f8d7da;color:#721c24;border:1px solid #f5c6cb}
.status-badge{display:inline-block;padding:5px 15px;border-radius:20px;font-weight:bold;font-size:14px}
.score{font-size:48px;font-weight:bold;text-align:center;margin:20px 0}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:15px}
.stat-card{background:white;padding:15px;border-radius:8px;text-align:center}
.stat-value{font-size:24px;font-weight:bold;color:#667eea}
.stat-label{font-size:12px;color:#666;margin-top:5px}
.errors-list{margin-top:15px;padding:15px;border-radius:8px;background:#f8d7da}
.warnings-list{margin-top:15px;padding:15px;border-radius:8px;background:#fff3cd}
.errors-list li{color:#721c24;margin:5px 0}
.warnings-list li{color:#856404;margin:5px 0}
.svg-container{margin-top:20px;background:white;padding:20px;border-radius:8px;text-align:center}
.svg-container svg{max-width:100%;height:auto}
.upload-zone{border:2px dashed #ccc;border-radius:8px;padding:30px;text-align:center;cursor:pointer;margin-bottom:15px}
.upload-zone:hover,.upload-zone.dragover{border-color:#667eea;background:#f0f4ff}
footer{text-align:center;color:white;padding:40px 0 20px;opacity:.8}
</style>
</head>
<body>
<div class="container">
<header><h1>\xf0\x9f\xa7\xb6 Crochet Pattern Checker</h1><p>Validate, visualize, and publish your crochet patterns</p></header>
<div class="main-grid">
<div class="panel"><h2>\xf0\x9f\x93\x9d Enter Your Pattern</h2>
<div class="upload-zone" id="dropZone"><p>\xf0\x9f\x93\x81 Drop a .txt file here or click to upload</p><input type="file" id="fileInput" accept=".txt" style="display:none"></div>
<textarea id="patternInput" placeholder="Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (18)\nRound 3: (2 sc, inc) x 6 (24)..."></textarea>
<button class="btn" onclick="checkPattern()">Check Pattern</button>
<button class="btn" onclick="renderPattern()">Render</button>
<button class="btn" onclick="simulatePattern()">3D Simulate</button>
</div>
<div class="panel"><h2>\xf0\x9f\x93\x8a Results</h2><div id="results"><p style="color:#999;text-align:center;padding:50px 0">Enter a pattern and click "Check Pattern" to see results</p></div></div>
</div>
<div class="panel" style="margin-top:20px" id="diagramPanel" hidden><h2>Pattern Diagram</h2><div class="svg-container" id="svgContainer"></div></div>
<footer><p>Crochet Pattern Checker v0.5.0 | Built with FastAPI</p></footer>
</div>
<script>
const dropZone=document.getElementById('dropZone'),fileInput=document.getElementById('fileInput'),patternInput=document.getElementById('patternInput');
dropZone.addEventListener('click',()=>fileInput.click());
dropZone.addEventListener('dragover',e=>{e.preventDefault();dropZone.classList.add('dragover')});
dropZone.addEventListener('dragleave',()=>dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop',e=>{e.preventDefault();dropZone.classList.remove('dragover');if(e.dataTransfer.files[0])readFile(e.dataTransfer.files[0])});
fileInput.addEventListener('change',e=>{if(e.target.files[0])readFile(e.target.files[0])});
function readFile(f){const r=new FileReader();r.onload=e=>patternInput.value=e.target.result;r.readAsText(f)}
async function checkPattern(){const t=patternInput.value;if(!t.trim())return alert('Enter a pattern');const res=document.getElementById('results');res.innerHTML='<p style="text-align:center;padding:20px">Checking...</p>';try{const r=await fetch('/api/check',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pattern_text:t})});const d=await r.json();if(!r.ok){res.innerHTML='<div class="result-box status-error"><b>Error:</b> '+d.detail+'</div>';return}const c=d.status.includes('PASS')&&!d.status.includes('WARNING')?'status-pass':d.status.includes('WARNING')?'status-warn':'status-error';let h='<div class="result-box '+c+'"><div style="text-align:center"><span class="status-badge">'+d.status+'</span><div class="score">'+d.score+'/100</div></div><div class="stats"><div class="stat-card"><div class="stat-value">'+d.rounds+'</div><div class="stat-label">Rounds</div></div><div class="stat-card"><div class="stat-value">'+d.max_stitches+'</div><div class="stat-label">Max Stitches</div></div><div class="stat-card"><div class="stat-value">'+d.max_diameter_inches+'"\'</div><div class="stat-label">Diameter</div></div><div class="stat-card"><div class="stat-value">'+d.total_height_inches+'"\'</div><div class="stat-label">Height</div></div></div></div>';if(d.errors&&d.errors.length>0){h+='<div class="errors-list"><b>Errors:</b><ul>';d.errors.forEach(e=>h+='<li>['+e.location+'] '+e.message+'</li>');h+='</ul></div>'}if(d.warnings&&d.warnings.length>0){h+='<div class="warnings-list"><b>Warnings:</b><ul>';d.warnings.forEach(w=>h+='<li>['+w.location+'] '+w.message+'</li>');h+='</ul></div>'}res.innerHTML=h}catch(e){res.innerHTML='<div class="result-box status-error"><b>Error:</b> '+e.message+'</div>'}}
async function renderPattern(){const t=patternInput.value;if(!t.trim())return alert('Enter a pattern');const p=document.getElementById('diagramPanel'),c=document.getElementById('svgContainer');p.hidden=false;c.innerHTML='<p style="text-align:center;padding:20px">Generating...</p>';try{const r=await fetch('/api/render',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pattern_text:t})});const d=await r.json();c.innerHTML=d.svg}catch(e){c.innerHTML='<p style="color:red">Error: '+e.message+'</p>'}}
async function simulatePattern(){const t=patternInput.value;if(!t.trim())return alert('Enter a pattern');const res=document.getElementById('results');res.innerHTML='<p style="text-align:center;padding:20px">Simulating...</p>';try{const r=await fetch('/api/simulate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pattern_text:t})});const d=await r.json();if(!r.ok){res.innerHTML='<div class="result-box status-error"><b>Error:</b> '+d.detail+'</div>';return}res.innerHTML='<div class="result-box status-pass"><h3 style="text-align:center;margin-bottom:15px">3D Simulation</h3><div class="stats"><div class="stat-card"><div class="stat-value">'+d.shape+'</div><div class="stat-label">Detected Shape</div></div><div class="stat-card"><div class="stat-value">'+(d.confidence*100).toFixed(0)+'%</div><div class="stat-label">Confidence</div></div><div class="stat-card"><div class="stat-value">'+d.vertices+'</div><div class="stat-label">Vertices</div></div><div class="stat-card"><div class="stat-value">'+d.faces+'</div><div class="stat-label">Faces</div></div></div></div>'}catch(e){res.innerHTML='<div class="result-box status-error"><b>Error:</b> '+e.message+'</div>'}}
</script>
</body>
</html>"""
