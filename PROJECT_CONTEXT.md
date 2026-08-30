# Crochet Pattern Checker — Complete Project Context Prompt

Use this prompt to continue development or provide context in a new AI session.
Copy everything between "PROMPT START" and "PROMPT END" below.

---

## PROMPT START

I built an open-source **Crochet Pattern Checker** — a production-ready Python tool that parses, validates, simulates, visualizes, and publishes crochet patterns. All 6 phases are complete and pushed to GitHub at `https://github.com/arbabkhan007/Crochet-Pattern-Checker`.

### What This Tool Does (End-to-End Pipeline):
1. **Parse** — reads raw crochet pattern text and builds structured data
2. **Validate** — mathematically verifies stitch counts, catches errors deterministically
3. **Visualize** — generates 2D SVG diagrams, stitch count charts, crochet charts
4. **Simulate** — detects shape (sphere/hat/tube/etc.), generates 3D mesh, exports OBJ
5. **Publish** — creates professional HTML/PDF documents for selling patterns
6. **Explain** — AI-powered explanations, fix suggestions, US↔UK translation, marketing descriptions
7. **Web UI** — FastAPI server with beautiful frontend

### Architecture & Hard Constraints:
- **AI must NOT decide mathematical correctness** — deterministic code does ALL validation
- Architecture: AI interpretation → Structured pattern → Deterministic validators → Simulation → Validation report → AI explanation
- Never silently modify the original pattern
- Confidence levels: PASS, PASS WITH WARNINGS, NEEDS REVIEW, ERROR, UNABLE TO VERIFY
- US terminology first, UK terminology mapping implemented
- Every pattern has versioning
- Real, maintainable code — not pseudo-code

### Project Structure:
```
src/crochet_checker/
├── __init__.py              # Package exports, version = "0.6.0"
├── cli.py                   # Click CLI with 7 subcommands:
│                            #   check, render, measure, render-3d, pdf, explain, serve
├── model/
│   ├── __init__.py
│   └── pattern.py           # Pydantic models:
│                            #   Pattern (fields: metadata, source_text, construction, yarn, hook, gauge, rows, rounds)
│                            #   PatternMetadata, Yarn, Hook, Gauge, Round, Row, Instruction
│                            #   ConstructionType enum (flat, in_the_round)
│                            #   Instruction has: operations (list of ParsedOperation), stated_stitch_count, repeat_count
│                            #   ParsedOperation has: stitch_type (StitchType enum), count
│                            #   StitchType values: single_crochet, double_crochet, half_double_crochet,
│                            #     treble, increase, decrease, chain, slip_stitch, magic_ring, etc.
│                            #   IMPORTANT: Pattern does NOT have 'notes' or 'finishing' fields
├── parser/
│   ├── __init__.py
│   └── parser.py            # Lexer + recursive descent Parser
│                            #   CrochetParser class, parse_pattern() function
│                            #   Parses: magic ring/MR, sc/hdc/dc/tr, inc/dec, repeat blocks (x N), stitch counts (N)
│                            #   Round has: round_number, instructions, source_text, computed_stitch_count
│                            #   Round.compute_stitch_count_with_context(prev_count) for context-dependent math
├── validation/
│   ├── __init__.py
│   └── stitch_counts.py     # validate_pattern(), ValidationReport, ValidationFinding
│                            #   ValidationFinding fields: validator, severity, location, message,
│                            #     original_instruction, expected, actual, suggested_fix, confidence
│                            #   ValidationReport has: errors, warnings, infos, all_findings, overall_status, score
│                            #   Validates: stitch count consistency, increase/decrease math, row transitions
├── visualization/
│   ├── __init__.py          # Exports: render_2d_preview, measure_pattern, StitchDimensions, PatternMeasurements
│   ├── measurements.py      # StitchDimensions, PatternMeasurements (Pydantic model)
│   │                        #   IMPORTANT: Uses @computed_field + @property for computed properties
│   │                        #   (total_height_inches, max_diameter_inches, max_circumference_inches, etc.)
│   │                        #   This is REQUIRED for Pydantic v2 — plain @property doesn't work
│   │                        #   measure_pattern(), MeasurementEngine
│   ├── stitch_diagram.py    # SVGDiagram, generate_circle_diagram(), generate_stitch_count_chart()
│   ├── render_2d.py         # render_2d_preview()
│   └── crochet_chart.py     # generate_crochet_chart()
├── simulation/
│   ├── __init__.py          # Exports: simulate_surface, Vec3, Mesh, DetectedShape, ShapeAnalysis
│   ├── mesh.py              # Vec3 (3D vector), Mesh (vertices + faces), OBJ export
│   │                        #   Mesh generators: generate_sphere_mesh, generate_tube_mesh,
│   │                        #     generate_flat_circle_mesh, generate_hat_mesh
│   └── surface.py           # SurfaceSimulator, DetectedShape enum (sphere/hat/flat_circle/tube/cone/bowl)
│                            #   ShapeAnalysis, analyze_pattern_shape(), simulate_surface()
├── pdf/
│   ├── __init__.py          # Exports: PDFConfig, PDFGenerator, generate_pdf_html
│   └── generator.py         # PDFConfig, PDFGenerator - generates professional HTML (print to PDF)
│                            #   Sections: cover, materials, abbreviations, instructions, measurements, validation
│                            #   IMPORTANT: No notes/finishing fields on Pattern - don't reference them
│                            #   Uses @computed_field PatternMeasurements for inch values
├── web/
│   ├── __init__.py          # Exports: app
│   └── app.py               # FastAPI app with endpoints:
│                            #   GET / (embedded HTML+CSS+JS frontend)
│                            #   POST /api/check, /api/upload, /api/render, /api/simulate, /api/pdf
│                            #   GET /api/health
├── ai/
│   ├── __init__.py          # Exports: PatternExplainer, TerminologyTranslator, SuggestionEngine, DescriptionGenerator
│   ├── explainer.py         # PatternExplainer - generates plain English explanations
│   │                        #   ExplanationResult: summary, explanation, highlights, recommendations, shape_guess
│   │                        #   Uses op.stitch_type.value (not inst.stitch_type!) to check operations
│   ├── terminology.py       # TerminologyTranslator - US↔UK translation
│   │                        #   Single-pass replacement to avoid cascading (sc→dc then dc→tr)
│   │                        #   Uses regex word boundaries for abbreviations
│   ├── suggestions.py       # SuggestionEngine - fix suggestions for validation errors
│   │                        #   Suggestion: error_location, error_message, suggestion, confidence, explanation
│   └── description.py       # DescriptionGenerator - marketing-ready descriptions
│                            #   PatternDescription: title, short/full description, materials, skill, size, tags, features
tests/
├── parser/test_parser.py              # ~32 tests
├── validation/test_stitch_counts.py   # ~10 tests
├── geometry/test_measurements.py      # 8 tests
├── visualization/test_visualization.py # ~16 tests
├── simulation/test_simulation.py      # 16 tests
├── pdf/test_pdf.py                    # ~11 tests
├── web/test_web.py                    # 12 tests
└── ai/test_ai.py                      # 25 tests
```

### Dependencies (pyproject.toml):
```
Core: pydantic>=2.0, click>=8.0, rich>=13.0
API: fastapi>=0.100, uvicorn>=0.23, python-multipart>=0.0.6
Dev: pytest>=7.4, pytest-cov>=4.1, httpx>=0.24, fastapi>=0.100, uvicorn>=0.23
```

### CLI Commands:
```bash
crochet-check check pattern.txt                        # Validate pattern
crochet-check render pattern.txt -o output/            # Generate 2D SVG diagrams
crochet-check measure pattern.txt                      # Show measurements
crochet-check render-3d pattern.txt                    # Generate 3D OBJ mesh
crochet-check pdf pattern.txt --designer "Name" -o f   # Generate PDF-ready HTML
crochet-check explain pattern.txt                      # AI explanation + suggestions
crochet-check serve --port 8000                        # Start web UI
```

### Known Issues & Gotchas:
1. **Pydantic v2**: PatternMeasurements MUST use `@computed_field` + `@property` for computed properties
2. **measurements.py** exists in `visualization/measurements.py` — both locations must have the file
3. **Pattern model**: Only has metadata, source_text, construction, yarn, hook, gauge, rows, rounds — NO notes or finishing
4. **Instruction model**: No `stitch_type` field — use `inst.operations[i].stitch_type.value` instead
5. **ParsedOperation**: Not directly importable from model.pattern — access via instruction.operations
6. **ValidationFinding** (not ValidationIssue): That's the error/warning class name
7. **Parser doesn't throw on invalid input** — returns empty/minimal patterns gracefully
8. **Terminology translator**: Must use single-pass regex to avoid cascading replacements
9. **Web UI**: Single-file HTML embedded in app.py — no external CSS/JS dependencies

### Test Status:
- Sandbox: 128 tests passing across 8 test files
- Codespaces: 75 tests passing (some test files not synced)

### What's Working:
- ✅ Parsing any US crochet pattern format
- ✅ Mathematical validation of stitch counts
- ✅ 2D SVG diagram generation (circle, chart, stitch count chart)
- ✅ 3D shape detection (sphere, hat, tube, cone, flat circle, bowl)
- ✅ OBJ mesh export (opens in Blender, MeshLab, 3D viewers)
- ✅ Professional PDF/HTML generation with cover page, materials, instructions
- ✅ FastAPI web server with drag-and-drop upload, real-time validation
- ✅ AI explanations in plain English
- ✅ Fix suggestions for common errors
- ✅ US↔UK terminology translation (single crochet ↔ double crochet, etc.)
- ✅ Marketing description generation with tags, skill level, size

### What Could Be Added Next:
- UK terminology as primary (currently US-first)
- LLM provider integration (OpenAI/Anthropic) for richer explanations
- Direct PDF generation (currently HTML → print to PDF)
- Pattern gallery / community sharing
- Yarn quantity estimator
- Row-by-row progress tracker in web UI
- Mobile-responsive improvements
- More stitch type support (post stitches, bobble, etc.)
- Integration with Ravelry/Etsy APIs

### My Request:
[Describe what you want to do next — continue development, fix bugs, add features, etc.]

## PROMPT END

---

## Quick Reference — Commands to Copy-Paste

### Start working:
```bash
cd /home/user/crochet-pattern-checker
pip install -e ".[dev]"
python -m pytest tests/ -v
```

### Run everything:
```bash
crochet-check check examples/amigurumi.txt
crochet-check render examples/amigurumi.txt -o output/
crochet-check render-3d examples/amigurumi.txt
crochet-check pdf examples/amigurumi.txt --designer "Your Name"
crochet-check explain examples/amigurumi.txt
crochet-check serve --port 8000
```

### Push changes:
```bash
git add -A
git commit -m "Description of changes"
git push
```

---

*All 6 phases complete. Version 0.6.0. 128 tests passing.*
*Generated for https://github.com/arbabkhan007/Crochet-Pattern-Checker*
