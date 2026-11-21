"""Modern single-page UI for the Crochet Pattern Checker.

Tabs: Check Â· Visualize Â· Gauge Â· Convert Â· Report.
Dark-mode aware, responsive, no external assets.
"""

from __future__ import annotations

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Crochet Pattern Checker â€” validate, visualize, publish</title>
<style>
:root{--bg:#f8fafc;--card:#ffffff;--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--accent:#7c3aed;--accent2:#db2777;--ok:#16a34a;--warn:#ca8a04;--err:#dc2626;--radius:14px}
@media(prefers-color-scheme:dark){:root{--bg:#0b1120;--card:#111827;--ink:#e5e7eb;--muted:#94a3b8;--line:#1f2937}}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5}
header{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;padding:2.2rem 1rem 1.6rem;text-align:center}
header h1{font-size:clamp(1.6rem,4vw,2.4rem);font-weight:800;letter-spacing:-.02em}
header p{opacity:.9;margin-top:.4rem}
header a{color:#fff;font-weight:600}
.wrap{max-width:1080px;margin:0 auto;padding:1rem}
.tabs{display:flex;gap:.4rem;flex-wrap:wrap;margin:1rem 0}
.tabs button{border:1px solid var(--line);background:var(--card);color:var(--ink);padding:.55rem 1rem;border-radius:999px;cursor:pointer;font-weight:600}
.tabs button[aria-selected="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
@media(max-width:820px){.grid{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:1.1rem}
.card h2{font-size:1.05rem;margin-bottom:.7rem}
textarea,input,select{width:100%;padding:.6rem;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);font:inherit}
textarea{min-height:220px;resize:vertical;font-family:ui-monospace,Menlo,monospace;font-size:.9rem}
label{font-size:.85rem;color:var(--muted);display:block;margin:.5rem 0 .2rem}
.btn{background:var(--accent);color:#fff;border:0;padding:.6rem 1.1rem;border-radius:10px;font-weight:700;cursor:pointer;margin:.4rem .3rem 0 0}
.btn.secondary{background:transparent;color:var(--accent);border:1px solid var(--accent)}
.btn:hover{opacity:.9}
.badge{display:inline-block;padding:.3rem .8rem;border-radius:999px;font-weight:800;font-size:.85rem}
.badge.pass{background:#dcfce7;color:#166534}.badge.warn{background:#fef9c3;color:#854d0e}.badge.err{background:#fee2e2;color:#991b1b}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:.6rem;margin:.8rem 0}
.stat{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:.6rem;text-align:center}
.stat b{font-size:1.25rem;display:block}
.stat span{font-size:.75rem;color:var(--muted)}
.errs{background:#fef2f2;border-radius:10px;padding:.8rem 1.2rem;margin-top:.6rem;color:#991b1b}
.warns{background:#fefce8;border-radius:10px;padding:.8rem 1.2rem;margin-top:.6rem;color:#854d0e}
@media(prefers-color-scheme:dark){.errs{background:#450a0a;color:#fecaca}.warns{background:#422006;color:#fde68a}}
.bar-row{display:flex;align-items:center;gap:.5rem;margin:.25rem 0}
.bar-label{width:3rem;text-align:right;font-size:.8rem;color:var(--muted)}
.bar-track{flex:1;background:var(--line);border-radius:4px;height:.9rem;overflow:hidden}
.bar-fill{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2))}
.bar-value{width:3rem;font-size:.85rem;font-weight:700}
.svg-box{overflow:auto;text-align:center}
.svg-box svg{max-width:100%;height:auto}
.drop{border:2px dashed var(--line);border-radius:10px;padding:1rem;text-align:center;cursor:pointer;color:var(--muted);margin-bottom:.6rem}
.drop.over{border-color:var(--accent);color:var(--accent)}
.muted{color:var(--muted);font-size:.85rem}
footer{text-align:center;color:var(--muted);padding:2rem 1rem;font-size:.85rem}
code{background:var(--bg);padding:.1rem .35rem;border-radius:6px}
</style></head>
<body>
<header>
<h1>ðŸ§¶ Crochet Pattern Checker</h1>
<p>Validate stitch counts, visualize, and publish â€” deterministic, no AI guesswork.</p>
<p><a href="/consensus">Multi-AI written review dashboard</a> Â· <a href="/docs">API docs</a> Â· <a href="/api/health">Health</a></p>
</header>
<div class="wrap">
<nav class="tabs" role="tablist">
<button role="tab" aria-selected="true" data-tab="check">âœ“ Check</button>
<button role="tab" aria-selected="false" data-tab="viz">ðŸ“Š Visualize</button>
<button role="tab" aria-selected="false" data-tab="gauge">ðŸ“ Gauge &amp; Yarn</button>
<button role="tab" aria-selected="false" data-tab="convert">ðŸ”€ US â†” UK</button>
<button role="tab" aria-selected="false" data-tab="report">ðŸ“„ Report</button>
</nav>

<section id="tab-check">
<div class="grid">
<div class="card">
<h2>Enter your pattern</h2>
<div class="drop" id="drop">ðŸ“ Drop a .txt file or click to upload<input type="file" id="file" accept=".txt" hidden></div>
<textarea id="pattern" placeholder="Round 1: 6 sc into magic ring (6)&#10;Round 2: inc x 6 (12)&#10;Round 3: (sc, inc) x 6 (18)&#10;Round 4: (2 sc, inc) x 6 (24)"></textarea>
<div>
<button class="btn" onclick="checkPattern()">Check pattern</button>
<button class="btn secondary" onclick="loadExample()">Load example</button>
<button class="btn secondary" onclick="copyPattern()">Copy</button>
</div>
<p class="muted">Paste US rounds/rows. The checker counts stitches and reports contradictions â€” it does not guess from photos.</p>
</div>
<div class="card"><h2>Results</h2><div id="results"><p class="muted">Enter a pattern and click â€œCheck patternâ€.</p></div></div>
</div>
</section>

<section id="tab-viz" hidden>
<div class="card">
<h2>Pattern diagram</h2>
<div>
<button class="btn" onclick="renderPattern()">Render diagram</button>
<button class="btn secondary" onclick="simulatePattern()">3D simulate</button>
</div>
<div class="svg-box" id="vizOut"><p class="muted">Diagrams appear here.</p></div>
</div>
</section>

<section id="tab-gauge" hidden>
<div class="grid">
<div class="card">
<h2>Gauge â†’ finished size</h2>
<label>Stitches in piece</label><input id="gSt" type="number" value="40" min="1">
<label>Rows in piece</label><input id="gRows" type="number" value="40" min="1">
<label>Stitches per 4 in (swatch)</label><input id="gSts" type="number" value="20" min="1">
<label>Rows per 4 in (swatch)</label><input id="gRows4" type="number" value="20" min="1">
<button class="btn" onclick="calcGauge()">Calculate size</button>
<div id="gaugeOut" style="margin-top:.8rem"></div>
</div>
<div class="card">
<h2>Yarn &amp; hook</h2>
<label>Total stitches</label><input id="ySt" type="number" value="1000" min="0">
<label>Stitch</label><select id="yStitch"><option>sc</option><option>hdc</option><option>dc</option><option>tr</option></select>
<button class="btn" onclick="calcYarn()">Estimate yarn</button>
<label>Yarn weight (0â€“7 or name)</label><input id="hWeight" value="worsted">
<button class="btn secondary" onclick="calcHook()">Recommend hook</button>
<div id="yarnOut" style="margin-top:.8rem"></div>
</div>
</div>
</section>

<section id="tab-convert" hidden>
<div class="card">
<h2>US â†” UK terminology</h2>
<label>Direction</label>
<select id="convDir"><option value="us-to-uk">US â†’ UK</option><option value="uk-to-us">UK â†’ US</option></select>
<label>Pattern text</label>
<textarea id="convIn" placeholder="Round 1: 6 sc into magic ring (6)"></textarea>
<button class="btn" onclick="convertTerms()">Convert</button>
<button class="btn secondary" onclick="copyConverted()">Copy result</button>
<pre id="convOut" class="muted" style="white-space:pre-wrap;margin-top:.8rem"></pre>
</div>
</section>

<section id="tab-report" hidden>
<div class="card">
<h2>Shareable report</h2>
<p class="muted">Self-contained HTML: verdict, stitch-count ladder, findings. Written counts only.</p>
<button class="btn" onclick="makeReport()">Generate report</button>
<button class="btn secondary" onclick="makePdf()">Printable sheet (HTML)</button>
<div id="reportOut" style="margin-top:.8rem"></div>
</div>
</section>
</div>
<footer>Crochet Pattern Checker Â· deterministic written-pattern checks Â· <code>crochet-check serve</code> to run locally</footer>
<script>
const $=id=>document.getElementById(id);
const esc=value=>String(value??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('\"','&quot;').replaceAll("'",'&#39;');
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{
document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected','false'));
b.setAttribute('aria-selected','true');
['check','viz','gauge','convert','report'].forEach(t=>$('tab-'+t).hidden=t!==b.dataset.tab);
});
const drop=$('drop'),file=$('file');
drop.onclick=()=>file.click();
file.onchange=e=>{if(e.target.files[0])read(e.target.files[0])};
drop.ondragover=e=>{e.preventDefault();drop.classList.add('over')};
drop.ondragleave=()=>drop.classList.remove('over');
drop.ondrop=e=>{e.preventDefault();drop.classList.remove('over');if(e.dataTransfer.files[0])read(e.dataTransfer.files[0])};
function read(f){const r=new FileReader();r.onload=e=>$('pattern').value=e.target.result;r.readAsText(f)}
function loadExample(){$('pattern').value="Round 1: 6 sc into magic ring (6)\nRound 2: inc x 6 (12)\nRound 3: (sc, inc) x 6 (18)\nRound 4: (2 sc, inc) x 6 (24)\nRound 5: (3 sc, inc) x 6 (30)\nRound 6: (4 sc, inc) x 6 (36)\nRound 7-12: sc in each st around (36)\nRound 13: (4 sc, dec) x 6 (30)\nRound 14: (3 sc, dec) x 6 (24)\nRound 15: (2 sc, dec) x 6 (18)\nRound 16: (sc, dec) x 6 (12)\nRound 17: dec x 6 (6)"}
function copyPattern(){navigator.clipboard.writeText($('pattern').value)}
async function post(path,body){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Request failed');return d}
function badge(s){s=String(s);const c=s.includes('PASS')&&!s.includes('WARN')?'pass':s.includes('WARN')?'warn':'err';return `<span class="badge ${c}">${esc(s)}</span>`}
async function checkPattern(){const t=$('pattern').value;if(!t.trim())return alert('Enter a pattern');const out=$('results');out.innerHTML='<p class="muted">Checkingâ€¦</p>';
try{const d=await post('/api/check',{pattern_text:t});
let h=`<div style="text-align:center">${badge(d.status)}<div style="font-size:2rem;font-weight:800">${d.score}/100</div></div>
<div class="stats"><div class="stat"><b>${d.rounds}</b><span>Rounds</span></div><div class="stat"><b>${d.max_stitches}</b><span>Max stitches</span></div>
<div class="stat"><b>${d.max_diameter_inches}"</b><span>Est. diameter*</span></div><div class="stat"><b>${d.total_height_inches}"</b><span>Est. height*</span></div></div>
<p class="muted">*Estimate from written counts, not a measurement.</p>`;
if(d.errors?.length)h+=`<div class="errs"><b>Errors (${d.errors.length})</b><ul>${d.errors.map(e=>`<li>[${esc(e.location)}] ${esc(e.message)}</li>`).join('')}</ul></div>`;
if(d.warnings?.length)h+=`<div class="warns"><b>Warnings (${d.warnings.length})</b><ul>${d.warnings.map(w=>`<li>[${esc(w.location)}] ${esc(w.message)}</li>`).join('')}</ul></div>`;
out.innerHTML=h}catch(e){out.innerHTML=`<div class="errs">${esc(e.message)}</div>`}}
async function renderPattern(){const t=$('pattern').value;if(!t.trim())return alert('Enter a pattern');const out=$('vizOut');out.innerHTML='<p class="muted">Renderingâ€¦</p>';
try{const d=await post('/api/render',{pattern_text:t});out.innerHTML=d.svg+(d.stitch_svg?`<p class="muted">Stitch map: ${d.stitches} written stitches.</p>${d.stitch_svg}`:'')+(d.geometry_svg?`<p class="muted">Geometry map. ${esc(d.geometry_note||'')}</p>${d.geometry_svg}`:'')}catch(e){out.innerHTML=`<div class="errs">${esc(e.message)}</div>`}}
async function simulatePattern(){const t=$('pattern').value;if(!t.trim())return alert('Enter a pattern');const out=$('vizOut');out.innerHTML='<p class="muted">Simulatingâ€¦</p>';
try{const d=await post('/api/simulate',{pattern_text:t});out.innerHTML=`<div class="stats"><div class="stat"><b>${esc(d.shape)}</b><span>Shape</span></div><div class="stat"><b>${Math.round(d.confidence*100)}%</b><span>Confidence</span></div><div class="stat"><b>${d.vertices}</b><span>Vertices</span></div><div class="stat"><b>${d.faces}</b><span>Faces</span></div></div><p class="muted">${esc(d.note||'')}</p>`+(d.assembly_svg||'')}catch(e){out.innerHTML=`<div class="errs">${esc(e.message)}</div>`}}
async function calcGauge(){try{const d=await post('/api/gauge',{stitches:+$('gSt').value,rows:+$('gRows').value,sts_per_4in:+$('gSts').value,rows_per_4in:+$('gRows4').value});
$('gaugeOut').innerHTML=`<div class="stats"><div class="stat"><b>${d.width_in}"</b><span>Width (${d.width_cm} cm)</span></div><div class="stat"><b>${d.height_in}"</b><span>Height (${d.height_cm} cm)</span></div></div><p class="muted">${esc(d.note)}</p>`}catch(e){$('gaugeOut').innerHTML=`<div class="errs">${esc(e.message)}</div>`}}
async function calcYarn(){try{const d=await post('/api/yarn',{total_stitches:+$('ySt').value,stitch:$('yStitch').value});
$('yarnOut').innerHTML=`<div class="stats"><div class="stat"><b>${d.yards} yd</b><span>Yardage (${d.metres} m)</span></div><div class="stat"><b>${d.balls_100g}</b><span>100 g balls</span></div></div><p class="muted">${esc(d.note)}</p>`}catch(e){$('yarnOut').innerHTML=`<div class="errs">${esc(e.message)}</div>`}}
async function calcHook(){try{const r=await fetch('/api/hooks?weight='+encodeURIComponent($('hWeight').value));const d=await r.json();if(!r.ok)throw new Error(d.detail);
$('yarnOut').innerHTML=`<div class="stats"><div class="stat"><b>${d.hook_mm_low}â€“${d.hook_mm_high} mm</b><span>Hook (${esc(d.hook_us)})</span></div><div class="stat"><b>${d.gauge_sts_per_4in?.join('â€“')||'â€”'}</b><span>Sts / 4 in</span></div></div><p class="muted">Weight ${d.weight_number} Â· ${esc(d.weight_name)}. ${esc(d.source)}</p>`}catch(e){$('yarnOut').innerHTML=`<div class="errs">${esc(e.message)}</div>`}}
async function convertTerms(){const t=$('convIn').value;if(!t.trim())return alert('Enter pattern text');
try{const d=await post('/api/convert',{pattern_text:t,direction:$('convDir').value});$('convOut').textContent=d.converted;$('convOut').dataset.text=d.converted}catch(e){$('convOut').textContent=e.message}}
function copyConverted(){navigator.clipboard.writeText($('convOut').dataset.text||'')}
function download(html,name){const b=new Blob([html],{type:'text/html'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;a.click()}
async function makeReport(){const t=$('pattern').value;if(!t.trim())return alert('Enter a pattern');
try{const d=await post('/api/report',{pattern_text:t});download(d.html,'pattern-report.html');
$('reportOut').innerHTML=`<div class="stats"><div class="stat"><b>${esc(d.status)}</b><span>Status</span></div><div class="stat"><b>${d.score}/100</b><span>Score</span></div></div><p class="muted">Report downloaded. Stitch-count ladder included.</p>`}catch(e){$('reportOut').innerHTML=`<div class="errs">${esc(e.message)}</div>`}}
async function makePdf(){const t=$('pattern').value;if(!t.trim())return alert('Enter a pattern');
try{const d=await post('/api/pdf',{pattern_text:t,template:'craft'});download(d.html,'pattern-sheet.html');$('reportOut').innerHTML='<p class="muted">Printable sheet downloaded (HTML â€” open and print).</p>'}catch(e){$('reportOut').innerHTML=`<div class="errs">${esc(e.message)}</div>`}}
</script>
</body>
</html>
"""


def frontend_html() -> str:
    return HTML
