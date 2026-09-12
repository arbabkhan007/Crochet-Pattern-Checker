"""
Crochet Analytics Dashboard - Beautiful charts and insights about your crochet journey
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path


class CrochetAnalytics:
    """Generate beautiful analytics dashboards for crochet projects"""
    
    def __init__(self, data_file: str = "crochet_analytics.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
    
    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {
            "projects": [],
            "yarn_usage": [],
            "time_spent": [],
            "skills_learned": []
        }
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_project(self, name: str, category: str, hours: float, yarn_yards: float, 
                    difficulty: str, completed_date: str = None):
        """Add a completed project"""
        project = {
            "name": name,
            "category": category,
            "hours": hours,
            "yarn_yards": yarn_yards,
            "difficulty": difficulty,
            "completed_date": completed_date or datetime.now().strftime("%Y-%m-%d")
        }
        self.data["projects"].append(project)
        self.save_data()
    
    def add_yarn_purchase(self, brand: str, color: str, yards: float, cost: float, date: str = None):
        """Track yarn purchases"""
        purchase = {
            "brand": brand,
            "color": color,
            "yards": yards,
            "cost": cost,
            "date": date or datetime.now().strftime("%Y-%m-%d")
        }
        self.data["yarn_usage"].append(purchase)
        self.save_data()
    
    def add_skill(self, skill_name: str, proficiency: int, date: str = None):
        """Track skills learned (proficiency 1-10)"""
        skill = {
            "name": skill_name,
            "proficiency": proficiency,
            "date": date or datetime.now().strftime("%Y-%m-%d")
        }
        self.data["skills_learned"].append(skill)
        self.save_data()
    
    def generate_dashboard_html(self, output_file: str = "crochet_dashboard.html"):
        """Generate beautiful HTML dashboard with charts"""
        
        # Calculate statistics
        total_projects = len(self.data["projects"])
        total_hours = sum(p["hours"] for p in self.data["projects"])
        total_yarn = sum(p["yarn_yards"] for p in self.data["projects"])
        total_yarn_cost = sum(y["cost"] for y in self.data["yarn_usage"])
        total_skills = len(self.data["skills_learned"])
        
        # Category breakdown
        categories = {}
        for p in self.data["projects"]:
            cat = p["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        # Monthly progress
        monthly = {}
        for p in self.data["projects"]:
            month = p["completed_date"][:7]  # YYYY-MM
            monthly[month] = monthly.get(month, 0) + 1
        
        # Difficulty distribution
        difficulties = {}
        for p in self.data["projects"]:
            diff = p["difficulty"]
            difficulties[diff] = difficulties.get(diff, 0) + 1
        
        # Top yarn brands
        yarn_brands = {}
        for y in self.data["yarn_usage"]:
            brand = y["brand"]
            yarn_brands[brand] = yarn_brands.get(brand, 0) + y["yards"]
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crochet Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .stat-label {{
            color: #666;
            font-size: 1.1em;
            margin-top: 5px;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .chart-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .chart-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }}
        canvas {{ max-height: 300px; }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧶 Crochet Analytics Dashboard</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_projects}</div>
                <div class="stat-label">Projects Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_hours:.1f}</div>
                <div class="stat-label">Hours Spent</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_yarn:.0f}</div>
                <div class="stat-label">Yards of Yarn Used</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${total_yarn_cost:.2f}</div>
                <div class="stat-label">Total Yarn Investment</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_skills}</div>
                <div class="stat-label">Skills Mastered</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-title">📊 Projects by Category</div>
                <canvas id="categoryChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">📈 Monthly Progress</div>
                <canvas id="monthlyChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">🎯 Difficulty Distribution</div>
                <canvas id="difficultyChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">🧶 Top Yarn Brands (by yards)</div>
                <canvas id="yarnChart"></canvas>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
    </div>
    
    <script>
        // Category Chart
        new Chart(document.getElementById('categoryChart'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(list(categories.keys()))},
                datasets: [{{
                    data: {json.dumps(list(categories.values()))},
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a']
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});
        
        // Monthly Chart
        new Chart(document.getElementById('monthlyChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(list(monthly.keys()))},
                datasets: [{{
                    label: 'Projects',
                    data: {json.dumps(list(monthly.values()))},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
        }});
        
        // Difficulty Chart
        new Chart(document.getElementById('difficultyChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(difficulties.keys()))},
                datasets: [{{
                    label: 'Projects',
                    data: {json.dumps(list(difficulties.values()))},
                    backgroundColor: ['#43e97b', '#4facfe', '#fa709a']
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
        }});
        
        // Yarn Brands Chart
        new Chart(document.getElementById('yarnChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(yarn_brands.keys())[:5])},
                datasets: [{{
                    label: 'Yards Used',
                    data: {json.dumps(list(yarn_brands.values())[:5])},
                    backgroundColor: '#764ba2'
                }}]
            }},
            options: {{ responsive: true, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
        }});
    </script>
</body>
</html>"""
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        return output_file


if __name__ == "__main__":
    print("🎨 Crochet Analytics Dashboard")
    print("=" * 50)
    
    analytics = CrochetAnalytics()
    
    # Add sample data
    print("\n📝 Adding sample projects...")
    analytics.add_project("Granny Square Blanket", "Blankets", 45.5, 2500, "Intermediate")
    analytics.add_project("Amigurumi Bunny", "Toys", 8.0, 150, "Beginner")
    analytics.add_project("Lace Shawl", "Accessories", 32.0, 1200, "Advanced")
    analytics.add_project("Baby Booties", "Baby", 4.5, 80, "Beginner")
    analytics.add_project("Cable Sweater", "Garments", 60.0, 1800, "Advanced")
    
    print("🧶 Adding yarn purchases...")
    analytics.add_yarn_purchase("Red Heart", "Various", 5000, 125.00)
    analytics.add_yarn_purchase("Lily Sugar'n Cream", "Natural", 1200, 45.00)
    analytics.add_yarn_purchase("Malabrigo", "Purple", 800, 95.00)
    
    print("🎯 Adding skills...")
    analytics.add_skill("Single Crochet", 10)
    analytics.add_skill("Double Crochet", 10)
    analytics.add_skill("Cable Stitch", 7)
    analytics.add_skill("Lace Work", 5)
    analytics.add_skill("Amigurumi", 8)
    
    print("\n📊 Generating dashboard...")
    output = analytics.generate_dashboard_html()
    print(f"✅ Dashboard saved to: {output}")
    print("\nOpen this file in your browser to see beautiful charts!")
