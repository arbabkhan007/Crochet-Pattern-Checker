# 🧶 Crochet Pattern Checker — Grand Capability Test Prompt

Use this prompt to test EVERY feature of your repo. Copy and paste into a new AI session.

---

## PROMPT START

I have a complete open-source **Crochet Pattern Checker** at `https://github.com/arbabkhan007/Crochet-Pattern-Checker`.

It has 6 phases: Parser, Validator, 2D Visualization, 3D Simulation, PDF Publishing, Web UI, and AI Assistance.

**Test every single capability of this tool.** Run the following tests in order and show me the results:

---

### TEST 1: Parser — Can it parse different pattern formats?

```bash
# Test basic circle pattern
cat << 'EOF' > /tmp/test_circle.txt
Round 1: 6 sc into magic ring (6)
Round 2: (sc, inc) x 6 (12)
Round 3: (2 sc, inc) x 6 (18)
Round 4: (3 sc, inc) x 6 (24)
Round 5: (4 sc, inc) x 6 (30)
EOF

crochet-check check /tmp/test_circle.txt

# Test amigurumi with increases AND decreases
cat << 'EOF' > /tmp/test_amigurumi.txt
Round 1: 6 sc into magic ring (6)
Round 2: inc x 6 (12)
Round 3: (sc, inc) x 6 (18)
Round 4: (2 sc, inc) x 6 (24)
Round 5: (3 sc, inc) x 6 (30)
Round 6: (4 sc, inc) x 6 (36)
Round 7-11: sc around (36)
Round 12: (4 sc, dec) x 6 (30)
Round 13: (3 sc, dec) x 6 (24)
Round 14: (2 sc, dec) x 6 (18)
Round 15: (sc, dec) x 6 (12)
Round 16: dec x 6 (6)
EOF

crochet-check check /tmp/test_amigurumi.txt
```

**Expected:** Both should parse and validate. Show PASS or PASS WITH WARNINGS.

---

### TEST 2: Validator — Can it catch errors?

```bash
# Test with WRONG stitch count (should fail)
cat << 'EOF' > /tmp/test_wrong.txt
Round 1: 6 sc into magic ring (6)
Round 2: (sc, inc) x 6 (13)
Round 3: (2 sc, inc) x 6 (24)
EOF

crochet-check check /tmp/test_wrong.txt
```

**Expected:** Should detect ERROR — Round 2 should be (18) not (13). Show the error message.

---

### TEST 3: 2D Visualization — Can it generate SVG diagrams?

```bash
crochet-check render /tmp/test_circle.txt -o /tmp/output_2d/
ls -la /tmp/output_2d/
```

**Expected:** Should create `diagram.svg`, `stitch_counts.svg`, `crochet_chart.svg`, `preview.svg`.
Show that all 4 files exist and are valid SVGs (contain `<svg` tag).

---

### TEST 4: Measurements — Can it calculate real-world dimensions?

```bash
crochet-check measure /tmp/test_circle.txt
```

**Expected:** Should show total rounds, max stitches, diameter in inches, height in inches.
Verify the math: 30 stitches in last round should give ~9.5 inches diameter.

---

### TEST 5: 3D Simulation — Can it detect shapes and generate meshes?

```bash
crochet-check render-3d /tmp/test_amigurumi.txt
ls -la output/
```

**Expected:**
- Should detect shape as "sphere" or "hat" (confidence > 70%)
- Should generate OBJ file with vertices and faces
- OBJ file should exist and be non-empty

---

### TEST 6: PDF Publishing — Can it generate professional documents?

```bash
crochet-check pdf /tmp/test_circle.txt --designer "Test Designer" -o /tmp/output_pdf/pattern.html
ls -la /tmp/output_pdf/
```

**Expected:**
- Should generate HTML file
- File should contain: cover page, materials section, abbreviations, instructions, measurements
- Open in browser → print to PDF should work

---

### TEST 7: AI Assistance — Can it explain patterns?

```bash
crochet-check explain /tmp/test_amigurumi.txt
```

**Expected output should include:**
- ✅ Summary (number of rounds, validation status)
- ✅ Shape guess (should say "sphere" or "amigurumi")
- ✅ Difficulty assessment
- ✅ Highlights (starts with 6, ends with 6, 16 rounds)
- ✅ Recommendations (add gauge, add yarn info, uses magic ring)
- ✅ Marketing description with title, skill level, tags

---

### TEST 8: US↔UK Translation — Can it translate terminology?

```bash
python3 << 'PYEOF'
from crochet_checker.ai import translate_pattern

us_pattern = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (12)" + chr(10) + "Round 3: 4 dc (4)"

result = translate_pattern(us_pattern, "US", "UK")
print("US:", us_pattern)
print("UK:", result.translated_text)
print("Changes:", result.changes_made)
PYEOF
```

**Expected:**
- `sc` → `dc` (single crochet becomes double crochet)
- `dc` → `tr` (double crochet becomes treble)
- Changes should be tracked and displayed

---

### TEST 9: Web UI — Can it serve a web interface?

```bash
# Start server in background
crochet-check serve --port 8000 &
sleep 3

# Test API endpoints
curl -X POST http://localhost:8000/api/check \
  -H "Content-Type: application/json" \
  -d '{"pattern_text": "Round 1: 6 sc into magic ring (6)\nRound 2: (sc, inc) x 6 (12)"}'

curl http://localhost:8000/api/health

# Test file upload
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/tmp/test_circle.txt"
```

**Expected:**
- Server starts on port 8000
- `/api/health` returns `{"status": "ok"}`
- `/api/check` returns validation result with status, score, errors, warnings
- `/api/upload` accepts file and returns validation

---

### TEST 10: Fix Suggestions — Can it suggest corrections?

```bash
python3 << 'PYEOF'
from crochet_checker.parser.parser import parse_pattern
from crochet_checker.validation import validate_pattern
from crochet_checker.ai import generate_suggestions

bad_pattern = "Round 1: 6 sc into magic ring (6)" + chr(10) + "Round 2: (sc, inc) x 6 (13)"

p = parse_pattern(bad_pattern)
r = validate_pattern(p)
suggestions = generate_suggestions(p, r)

print(f"Errors found: {len(r.errors)}")
print(f"Suggestions generated: {len(suggestions)}")
for s in suggestions:
    print(f"  [{s.confidence}] {s.error_location}: {s.suggestion}")
    if s.explanation:
        print(f"       {s.explanation}")
PYEOF
```

**Expected:**
- Should detect stitch count mismatch
- Should generate suggestion with confidence level
- Suggestion should explain what's wrong

---

### TEST 11: Edge Cases — Can it handle weird patterns?

```bash
# Empty pattern
echo "" > /tmp/test_empty.txt
crochet-check check /tmp/test_empty.txt

# Single round
echo "Round 1: 10 sc into magic ring (10)" > /tmp/test_single.txt
crochet-check check /tmp/test_single.txt

# Very long pattern (50 rounds)
python3 -c "
for i in range(1, 51):
    print(f'Round {i}: sc around ({6 + i})')
" > /tmp/test_long.txt
crochet-check check /tmp/test_long.txt
```

**Expected:**
- Empty: Should handle gracefully (no crash)
- Single round: Should validate
- Long pattern: Should validate without performance issues

---

### TEST 12: Run Full Test Suite

```bash
python -m pytest tests/ -v --tb=short
```

**Expected:** All tests should pass (75+ tests in Codespaces, 128 in sandbox).

---

## Scoring Rubric

For each test, score:
- ✅ **PASS** — Works as expected
- ⚠️ **PARTIAL** — Works but with warnings/limitations
- ❌ **FAIL** — Doesn't work or crashes

**Final Score: ___/12**

If all 12 tests pass, your Crochet Pattern Checker is **production-ready**!

---

## What to Look For

1. **Robustness** — Does it crash on bad input?
2. **Accuracy** — Are the calculations correct?
3. **Completeness** — Does every feature work?
4. **Usability** — Are error messages helpful?
5. **Performance** — Does it handle large patterns?

---

## PROMPT END

---

### Quick Test Command (Run All at Once):

```bash
cd /home/user/crochet-pattern-checker

# Create test patterns
cat << 'EOF' > /tmp/test_circle.txt
Round 1: 6 sc into magic ring (6)
Round 2: (sc, inc) x 6 (12)
Round 3: (2 sc, inc) x 6 (18)
Round 4: (3 sc, inc) x 6 (24)
Round 5: (4 sc, inc) x 6 (30)
EOF

cat << 'EOF' > /tmp/test_amigurumi.txt
Round 1: 6 sc into magic ring (6)
Round 2: inc x 6 (12)
Round 3: (sc, inc) x 6 (18)
Round 4: (2 sc, inc) x 6 (24)
Round 5: (3 sc, inc) x 6 (30)
Round 6: (4 sc, inc) x 6 (36)
Round 7-11: sc around (36)
Round 12: (4 sc, dec) x 6 (30)
Round 13: (3 sc, dec) x 6 (24)
Round 14: (2 sc, dec) x 6 (18)
Round 15: (sc, dec) x 6 (12)
Round 16: dec x 6 (6)
EOF

# Run all commands
echo "=== TEST 1: Parser ===" && crochet-check check /tmp/test_circle.txt
echo -e "\n=== TEST 2: Validator ===" && crochet-check check /tmp/test_amigurumi.txt
echo -e "\n=== TEST 3: 2D Visualization ===" && crochet-check render /tmp/test_circle.txt -o /tmp/test_out/ && ls /tmp/test_out/
echo -e "\n=== TEST 4: Measurements ===" && crochet-check measure /tmp/test_circle.txt
echo -e "\n=== TEST 5: 3D Simulation ===" && crochet-check render-3d /tmp/test_amigurumi.txt
echo -e "\n=== TEST 6: PDF ===" && crochet-check pdf /tmp/test_circle.txt --designer "Tester" -o /tmp/test_out/pattern.html && ls /tmp/test_out/*.html
echo -e "\n=== TEST 7: AI Explanation ===" && crochet-check explain /tmp/test_amigurumi.txt
echo -e "\n=== TEST 8: Run Tests ===" && python -m pytest tests/ -v --tb=short | tail -5
```

This will test everything in ~30 seconds! 🚀
