
from pathlib import Path
from typing import List, Dict
import webbrowser
import tempfile

class HTMLPatternGenerator:
    """Generate interactive HTML patterns"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def generate_interactive_pattern(self, pattern_text: str, title: str = "Crochet Pattern") -> str:
        """Generate interactive HTML pattern"""
        # Parse pattern
        rounds = self._parse_rounds(pattern_text)
        
        # Generate HTML
        html = self._generate_html(rounds, title, pattern_text)
        
        # Save file
        html_path = Path(self.temp_dir) / f"{title.replace(' ', '_')}_interactive.html"
        with open(html_path, 'w') as f:
            f.write(html)
        
        # Open in browser
        webbrowser.open(f'file://{html_path.absolute()}')
        
        return str(html_path)
    
    def _parse_rounds(self, pattern_text: str) -> List[Dict]:
        """Parse pattern into rounds"""
        import re
        rounds = []
        
        # Extract rounds
        lines = pattern_text.split('\n')
        current_round = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts a new round
            round_match = re.match(r'(?:round|rnd|r)\s+(\d+):?\s*(.*)', line, re.IGNORECASE)
            if round_match:
                if current_round:
                    rounds.append(current_round)
                current_round = {
                    'number': int(round_match.group(1)),
                    'instruction': round_match.group(2),
                    'stitches': []
                }
                
                # Extract stitch count
                count_match = re.search(r'\((\d+)\)', line)
                if count_match:
                    current_round['stitch_count'] = int(count_match.group(1))
            elif current_round:
                # Continue previous round
                current_round['instruction'] += ' ' + line
        
        if current_round:
            rounds.append(current_round)
        
        return rounds
    
    def _generate_html(self, rounds: List[Dict], title: str, original_text: str) -> str:
        """Generate interactive HTML"""
        rounds_html = ""
        for rnd in rounds:
            stitch_count = rnd.get('stitch_count', '?')
            rounds_html += f"""
            <div class="round" data-round="{rnd['number']}">
                <div class="round-header">
                    <span class="round-number">Round {rnd['number']}</span>
                    <span class="stitch-count">({stitch_count} sts)</span>
                    <button class="check-btn" onclick="toggleRound({rnd['number']})">✓</button>
                </div>
                <div class="round-instruction">{rnd['instruction']}</div>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title} - Interactive Pattern</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .progress {{
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .progress-bar {{
            background: rgba(255,255,255,0.3);
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }}
        .progress-fill {{
            background: #4CAF50;
            height: 100%;
            width: 0%;
            transition: width 0.3s ease;
        }}
        .controls {{
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }}
        button:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .rounds-container {{
            padding: 20px;
            max-height: 600px;
            overflow-y: auto;
        }}
        .round {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 6px;
            transition: all 0.3s ease;
        }}
        .round.completed {{
            background: #d4edda;
            border-left-color: #28a745;
            opacity: 0.7;
        }}
        .round-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }}
        .round-number {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
        }}
        .stitch-count {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        .check-btn {{
            margin-left: auto;
            background: #28a745;
            padding: 5px 15px;
            font-size: 16px;
        }}
        .check-btn:hover {{
            background: #218838;
        }}
        .round.completed .check-btn {{
            background: #6c757d;
        }}
        .round-instruction {{
            color: #495057;
            line-height: 1.6;
        }}
        .stats {{
            padding: 20px;
            background: #f8f9fa;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        .stat-box {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧶 {title}</h1>
            <div class="progress">
                <div>Progress: <span id="progressText">0 / {len(rounds)} rounds</span></div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <button onclick="resetProgress()">↺ Reset Progress</button>
            <button onclick="saveProgress()">💾 Save Progress</button>
            <button onclick="loadProgress()">📂 Load Progress</button>
            <button onclick="printPattern()">🖨️ Print Pattern</button>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value" id="totalRounds">{len(rounds)}</div>
                <div class="stat-label">Total Rounds</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="completedRounds">0</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="remainingRounds">{len(rounds)}</div>
                <div class="stat-label">Remaining</div>
            </div>
        </div>
        
        <div class="rounds-container">
            {rounds_html}
        </div>
    </div>
    
    <script>
        let completedRounds = new Set();
        
        function toggleRound(roundNum) {{
            const round = document.querySelector(`[data-round="${{roundNum}}"]`);
            const btn = round.querySelector('.check-btn');
            
            if (completedRounds.has(roundNum)) {{
                completedRounds.delete(roundNum);
                round.classList.remove('completed');
                btn.textContent = '✓';
            }} else {{
                completedRounds.add(roundNum);
                round.classList.add('completed');
                btn.textContent = '✓ Done';
            }}
            
            updateProgress();
        }}
        
        function updateProgress() {{
            const total = {len(rounds)};
            const completed = completedRounds.size;
            const remaining = total - completed;
            const percentage = (completed / total) * 100;
            
            document.getElementById('completedRounds').textContent = completed;
            document.getElementById('remainingRounds').textContent = remaining;
            document.getElementById('progressText').textContent = `${{completed}} / ${{total}} rounds`;
            document.getElementById('progressFill').style.width = percentage + '%';
        }}
        
        function resetProgress() {{
            if (confirm('Reset all progress?')) {{
                completedRounds.clear();
                document.querySelectorAll('.round').forEach(round => {{
                    round.classList.remove('completed');
                    round.querySelector('.check-btn').textContent = '✓';
                }});
                updateProgress();
            }}
        }}
        
        function saveProgress() {{
            const data = {{
                completed: Array.from(completedRounds),
                timestamp: new Date().toISOString()
            }};
            localStorage.setItem('crochet_progress', JSON.stringify(data));
            alert('Progress saved!');
        }}
        
        function loadProgress() {{
            const data = localStorage.getItem('crochet_progress');
            if (data) {{
                const parsed = JSON.parse(data);
                completedRounds = new Set(parsed.completed);
                document.querySelectorAll('.round').forEach(round => {{
                    const roundNum = parseInt(round.dataset.round);
                    if (completedRounds.has(roundNum)) {{
                        round.classList.add('completed');
                        round.querySelector('.check-btn').textContent = '✓ Done';
                    }}
                }});
                updateProgress();
                alert('Progress loaded!');
            }} else {{
                alert('No saved progress found.');
            }}
        }}
        
        function printPattern() {{
            window.print();
        }}
    </script>
</body>
</html>
"""
        return html

def generate_interactive_pattern(pattern_text: str, title: str = "Crochet Pattern") -> str:
    """Convenience function to generate interactive pattern"""
    generator = HTMLPatternGenerator()
    return generator.generate_interactive_pattern(pattern_text, title)
