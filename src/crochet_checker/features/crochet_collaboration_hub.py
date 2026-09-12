"""
Pattern Collaboration Hub - Real-time pattern editing and version tracking for teams
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class CollaborationHub:
    """Manage collaborative pattern editing"""
    
    def __init__(self, data_file: str = "collaboration.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
    
    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"projects": {}, "users": {}}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def create_project(self, name: str, owner: str, description: str = ""):
        """Create a collaborative project"""
        project_id = f"proj_{len(self.data['projects']) + 1}"
        self.data["projects"][project_id] = {
            "name": name,
            "owner": owner,
            "description": description,
            "collaborators": [owner],
            "versions": [{
                "content": "",
                "author": owner,
                "timestamp": datetime.now().isoformat(),
                "comment": "Initial version"
            }],
            "comments": [],
            "created": datetime.now().isoformat()
        }
        self.save_data()
        return project_id
    
    def add_collaborator(self, project_id: str, username: str) -> bool:
        """Add a collaborator to a project"""
        if project_id not in self.data["projects"]:
            return False
        
        project = self.data["projects"][project_id]
        if username not in project["collaborators"]:
            project["collaborators"].append(username)
            self.save_data()
        return True
    
    def add_version(self, project_id: str, content: str, author: str, comment: str = ""):
        """Add a new version of the pattern"""
        if project_id not in self.data["projects"]:
            return False
        
        version = {
            "content": content,
            "author": author,
            "timestamp": datetime.now().isoformat(),
            "comment": comment
        }
        self.data["projects"][project_id]["versions"].append(version)
        self.save_data()
        return True
    
    def add_comment(self, project_id: str, author: str, text: str):
        """Add a comment to the project"""
        if project_id not in self.data["projects"]:
            return False
        
        comment = {
            "author": author,
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        self.data["projects"][project_id]["comments"].append(comment)
        self.save_data()
        return True
    
    def get_project_history(self, project_id: str) -> Dict:
        """Get full project history"""
        if project_id not in self.data["projects"]:
            return {}
        
        project = self.data["projects"][project_id]
        return {
            "name": project["name"],
            "owner": project["owner"],
            "collaborators": project["collaborators"],
            "total_versions": len(project["versions"]),
            "total_comments": len(project["comments"]),
            "versions": project["versions"][-5:],  # Last 5 versions
            "recent_comments": project["comments"][-5:]  # Last 5 comments
        }
    
    def generate_collaboration_report(self, project_id: str) -> str:
        """Generate a collaboration report"""
        history = self.get_project_history(project_id)
        if not history:
            return "Project not found"
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║         🤝 COLLABORATION REPORT                           ║
║         {history['name']}                                 ║
╚══════════════════════════════════════════════════════════╝

📋 PROJECT INFO
═══════════════════════════════════════════════════════════
  Owner: {history['owner']}
  Collaborators: {', '.join(history['collaborators'])}
  Total Versions: {history['total_versions']}
  Total Comments: {history['total_comments']}

📝 RECENT CHANGES
═══════════════════════════════════════════════════════════
"""
        for version in history['versions']:
            report += f"  • {version['author']} - {version['comment'] or 'No comment'}\n"
            report += f"    {version['timestamp'][:16]}\n"
        
        if history['recent_comments']:
            report += "\n💬 RECENT COMMENTS\n"
            report += "═" * 59 + "\n"
            for comment in history['recent_comments']:
                report += f"  {comment['author']}: {comment['text']}\n"
                report += f"    {comment['timestamp'][:16]}\n"
        
        return report


if __name__ == "__main__":
    print("🤝 Pattern Collaboration Hub")
    print("=" * 50)
    
    hub = CollaborationHub()
    
    print("\n📁 Creating collaborative project...")
    project_id = hub.create_project(
        "Granny Square Blanket",
        "alice_designer",
        "Modern granny square blanket pattern"
    )
    print(f"✅ Created project: {project_id}")
    
    print("\n👥 Adding collaborators...")
    hub.add_collaborator(project_id, "bob_tester")
    hub.add_collaborator(project_id, "carol_editor")
    
    print("\n📝 Adding versions...")
    hub.add_version(project_id, "Row 1: Ch 20, sc across", "alice_designer", "Initial pattern")
    hub.add_version(project_id, "Row 1: Ch 25, sc across\nRow 2: Ch 1, turn, sc across", 
                   "bob_tester", "Added row 2")
    
    print("\n💬 Adding comments...")
    hub.add_comment(project_id, "carol_editor", "Love the pattern! Maybe add a border?")
    hub.add_comment(project_id, "alice_designer", "Good idea! Working on it.")
    
    print("\n📊 Collaboration Report:")
    print(hub.generate_collaboration_report(project_id))
    
    print("\n✅ Collaboration Hub ready!")
