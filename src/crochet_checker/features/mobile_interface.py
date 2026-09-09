
from pathlib import Path
import webbrowser
import tempfile

class MobilePatternInterface:
    """Mobile-responsive pattern interface"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def generate_mobile_interface(self, pattern_text: str, title: str = "Crochet Pattern") -> str:
        """Generate mobile-responsive interface"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Mobile</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 10px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        .progress-container {{
            background: rgba(255,255,255,0.2);
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
        }}
        .progress-bar {{
            background: rgba(255,255,255,0.3);
            height: 15px;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }}
        .progress-fill {{
            background: #4CAF50;
            height: 100%;
            width: 0%;
            transition: width 0.3s ease;
        }}
        .controls {{
            padding: 15px;
            background: #f8f9fa;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            border-bottom: 1px solid #dee2e6;
        }}
        button {{
            flex: 1;
            min-width: 80px;
            background: #667eea;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }}
        button:active {{
            transform: scale(0.95);
        }}
        .round {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 10px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        .round.completed {{
            background: #d4edda;
            border-left-color: #28a745;
            opacity: 0.7;
        }}
        .round-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .round-number {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
        }}
        .check-btn {{
            background: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 18px;
        }}
        .round.completed .check-btn {{
            background: #6c757d;
        }}
        .round-instruction {{
            color: #495057;
            line-height: 1.6;
            font-size: 0.95em;
        }}
        .timer {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
        }}
        .timer-display {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .timer-controls {{
            display: flex;
            gap: 10px;
            justify-content: center;
        }}
        .timer-btn {{
            padding: 10px 20px;
            font-size: 16px;
        }}
        @media (max-width: 480px) {{
            .header h1 {{
                font-size: 1.2em;
            }}
            .round {{
                margin: 8px;
                padding: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧶 {title}</h1>
            <div class="progress-container">
                <div>Progress: <span id="progressText">0%</span></div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <button onclick="resetProgress()">↺ Reset</button>
            <button onclick="saveProgress()">💾 Save</button>
            <button onclick="toggleTimer()">⏱️ Timer</button>
        </div>
        
        <div id="roundsContainer"></div>
        
        <div class="timer" id="timerSection" style="display: none;">
            <div>Timer</div>
            <div class="timer-display" id="timerDisplay">00:00:00</div>
            <div class="timer-controls">
                <button class="timer-btn" onclick="startTimer()">▶️ Start</button>
                <button class="timer-btn" onclick="pauseTimer()">⏸️ Pause</button>
                <button class="timer-btn" onclick="resetTimer()">↺ Reset</button>
            </div>
        </div>
    </div>
    
    <script>
        const patternText = `{pattern_text}`;
        const rounds = parsePattern(patternText);
        let completedRounds = new Set();
        let timerInterval = null;
        let timerSeconds = 0;
        
        function parsePattern(text) {{
            const lines = text.split('\n');
            const rounds = [];
            let currentRound = null;
            
            for (let line of lines) {{
                const match = line.match(/(?:round|rnd|r)\s+(\d+):?\s*(.*)/i);
                if (match) {{
                    if (currentRound) rounds.push(currentRound);
                    const countMatch = line.match(/\((\d+)\)/);
                    currentRound = {{
                        number: parseInt(match[1]),
                        instruction: match[2],
                        stitchCount: countMatch ? parseInt(countMatch[1]) : null
                    }};
                }} else if (currentRound && line.trim()) {{
                    currentRound.instruction += ' ' + line.trim();
                }}
            }}
            if (currentRound) rounds.push(currentRound);
            return rounds;
        }}
        
        function renderRounds() {{
            const container = document.getElementById('roundsContainer');
            container.innerHTML = rounds.map(round => `
                <div class="round" data-round="${{round.number}}">
                    <div class="round-header">
                        <span class="round-number">Round ${{round.number}}</span>
                        ${{round.stitchCount ? `<span>(${{round.stitchCount}} sts)</span>` : ''}}
                        <button class="check-btn" onclick="toggleRound(${{round.number}})">✓</button>
                    </div>
                    <div class="round-instruction">${{round.instruction}}</div>
                </div>
            `).join('');
        }}
        
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
            const total = rounds.length;
            const completed = completedRounds.size;
            const percentage = Math.round((completed / total) * 100);
            
            document.getElementById('progressText').textContent = percentage + '%';
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
                timer: timerSeconds,
                timestamp: new Date().toISOString()
            }};
            localStorage.setItem('crochet_mobile_progress', JSON.stringify(data));
            alert('Progress saved!');
        }}
        
        function toggleTimer() {{
            const timerSection = document.getElementById('timerSection');
            timerSection.style.display = timerSection.style.display === 'none' ? 'block' : 'none';
        }}
        
        function startTimer() {{
            if (!timerInterval) {{
                timerInterval = setInterval(() => {{
                    timerSeconds++;
                    updateTimerDisplay();
                }}, 1000);
            }}
        }}
        
        function pauseTimer() {{
            if (timerInterval) {{
                clearInterval(timerInterval);
                timerInterval = null;
            }}
        }}
        
        function resetTimer() {{
            pauseTimer();
            timerSeconds = 0;
            updateTimerDisplay();
        }}
        
        function updateTimerDisplay() {{
            const hours = Math.floor(timerSeconds / 3600);
            const minutes = Math.floor((timerSeconds % 3600) / 60);
            const seconds = timerSeconds % 60;
            document.getElementById('timerDisplay').textContent = 
                `${{String(hours).padStart(2, '0')}}:${{String(minutes).padStart(2, '0')}}:${{String(seconds).padStart(2, '0')}}`;
        }}
        
        // Load saved progress
        const savedData = localStorage.getItem('crochet_mobile_progress');
        if (savedData) {{
            const data = JSON.parse(savedData);
            completedRounds = new Set(data.completed);
            timerSeconds = data.timer || 0;
            updateTimerDisplay();
        }}
        
        renderRounds();
        updateProgress();
    </script>
</body>
</html>
"""
        
        html_path = Path(self.temp_dir) / f"{title.replace(' ', '_')}_mobile.html"
        with open(html_path, 'w') as f:
            f.write(html)
        
        webbrowser.open(f'file://{html_path.absolute()}')
        return str(html_path)

def generate_mobile_interface(pattern_text: str, title: str = "Crochet Pattern") -> str:
    """Convenience function for mobile interface"""
    interface = MobilePatternInterface()
    return interface.generate_mobile_interface(pattern_text, title)
