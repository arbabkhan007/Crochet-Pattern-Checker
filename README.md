# Crochet Pattern Checker

**Validate, visualize, simulate, and publish crochet patterns — all from the command line.**


> Turn raw crochet pattern text into validated documents, 2D diagrams, 3D meshes, professional PDFs, and AI-powered explanations automatically.

---

## Features

### Parse and Validate
- Parses any US crochet pattern format (magic ring, sc/hdc/dc/tr, increases, decreases, repeats)
- Deterministic mathematical validation catches stitch count errors before you crochet
- Confidence levels: PASS, PASS WITH WARNINGS, NEEDS REVIEW, ERROR

### 2D Visualization
- Circle diagrams, stitch count charts, crochet charts, combined preview

### 3D Simulation
- Automatic shape detection (sphere, hat, tube, cone, flat circle, bowl)
- Export to .obj files — open in Blender, MeshLab, or any 3D viewer

### PDF Publishing
- Professional pattern documents with cover page, materials, abbreviations
- Real PDF output via WeasyPrint — no browser needed

### AI Assistance
- Plain English pattern explanations
- Fix suggestions for validation errors
- US to UK terminology translation (sc to dc, hdc to htr, etc.)
- Marketing-ready pattern descriptions with tags

### Web Interface
- Beautiful drag-and-drop web UI
- Real-time validation, rendering, and 3D simulation
- REST API for integration

---

## Quick Start

**Install:**
```bash
git clone https://github.com/arbabkhan007/Crochet-Pattern-Checker.git
cd Crochet-Pattern-Checker
pip install -e ".[dev]"
pip install weasyprint
```

**Validate:**
```bash
crochet-check check examples/amigurumi.txt
```

**Generate 2D diagrams:**
```bash
crochet-check render examples/simple_hat.txt -o output/
```

**Generate 3D mesh:**
```bash
crochet-check render-3d examples/amigurumi.txt
```

**Generate PDF:**
```bash
crochet-check pdf examples/amigurumi.txt --designer "Your Name" -o pattern.pdf
```

**AI explanation:**
```bash
crochet-check explain examples/amigurumi.txt
```

**Start web UI:**
```bash
crochet-check serve --port 8000
```

---

## All Commands

| Command | Description |
|---------|-------------|
| `crochet-check check pattern.txt` | Validate stitch counts |
| `crochet-check render pattern.txt -o output/` | Generate 2D SVG diagrams |
| `crochet-check measure pattern.txt` | Show measurements |
| `crochet-check render-3d pattern.txt` | Generate 3D mesh (OBJ) |
| `crochet-check pdf pattern.txt -o out.pdf` | Generate professional PDF |
| `crochet-check explain pattern.txt` | AI explanation + suggestions |
| `crochet-check serve --port 8000` | Start web UI |

---

## Example Patterns

| File | Shape | Rounds | Description |
|------|-------|--------|-------------|
| amigurumi.txt | Sphere | 17 | Classic amigurumi ball |
| simple_hat.txt | Hat | 10 | Beanie with crown shaping |
| flat_coaster.txt | Flat Circle | 8 | Simple round coaster |
| tube_cowl.txt | Tube | 12 | Infinity cowl/scarf |
| gradual_bowl.txt | Bowl | 10 | Decorative bowl shape |
| mini_sphere.txt | Sphere | 10 | Small amigurumi sphere |

---

## Architecture

```
Pattern Text -> Parser -> Validators -> Report -> AI Explanation
                                                      |
                                         2D SVGs | 3D Mesh | PDF
```

Key principle: AI never decides mathematical correctness. All validation is deterministic code.

---

## US to UK Translation

| US Term | UK Term |
|---------|---------|
| Single Crochet (sc) | Double Crochet (dc) |
| Half Double Crochet (hdc) | Half Treble (htr) |
| Double Crochet (dc) | Treble (tr) |

---

## Testing

```bash
pytest tests/ -v    # 129 tests
```

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Write tests
4. Make sure pytest passes
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE)

---

Built with love for the crochet community.

Parse -> Validate -> Visualize -> Simulate -> Publish -> Explain
