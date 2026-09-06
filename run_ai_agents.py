#!/usr/bin/env python3
"""
🤖 Quick launcher for AI Agent Swarm
Usage:
  python run_ai_agents.py validate <pattern_file>
  python run_ai_agents.py generate <description> [type] [size]
  python run_ai_agents.py search <query> [type]
  python run_ai_agents.py dashboard
  python run_ai_agents.py learn
"""
import sys
import json
sys.path.insert(0, 'src')

from crochet_checker.agents.orchestrator import Orchestrator, AgentType

def main():
    if len(sys.argv) < 2:
        print("""
🤖 AI AGENT SWARM - Crochet Pattern Checker
═══════════════════════════════════════════

Usage:
  python run_ai_agents.py validate <pattern.json>    Validate a pattern
  python run_ai_agents.py generate <description>     Generate a new pattern
  python run_ai_agents.py search <query> [type]      Search for patterns
  python run_ai_agents.py dashboard                  Show agent dashboard
  python run_ai_agents.py learn                      Show AI learning status

Examples:
  python run_ai_agents.py validate my_pattern.json
  python run_ai_agents.py generate "cute bunny" sphere small
  python run_ai_agents.py search amigurumi animals patterns
  python run_ai_agents.py dashboard
  python run_ai_agents.py learn
""")
        return
    
    command = sys.argv[1].lower()
    orch = Orchestrator()
    
    if command == 'validate':
        if len(sys.argv) < 3:
            print("❌ Need a pattern file. Usage: python run_ai_agents.py validate <file.json>")
            return
        
        with open(sys.argv[2]) as f:
            pattern = json.load(f)
        
        print("\n🤖 Running FULL PIPELINE...")
        results = orch.run_pipeline(pattern, pipeline='full')
        
        # Save PDF if generated
        if results.get('pdf', {}).get('file_content'):
            pdf_name = sys.argv[2].replace('.json', '_output.md')
            with open(pdf_name, 'w') as f:
                f.write(results['pdf']['file_content'])
            print(f"\n📄 PDF content saved to: {pdf_name}")
    
    elif command == 'generate':
        desc = sys.argv[2] if len(sys.argv) > 2 else "amigurumi ball"
        ptype = sys.argv[3] if len(sys.argv) > 3 else "sphere"
        size = sys.argv[4] if len(sys.argv) > 4 else "medium"
        
        results = orch.run_pipeline(
            {'description': desc, 'type': ptype, 'size': size},
            pipeline='generate'
        )
        
        gen = results.get('generation', {})
        if gen.get('pattern'):
            pattern = gen['pattern']
            output_file = f"generated_{ptype}_{size}.json"
            with open(output_file, 'w') as f:
                json.dump(pattern, f, indent=2)
            print(f"\n💾 Pattern saved to: {output_file}")
    
    elif command == 'search':
        query = sys.argv[2] if len(sys.argv) > 2 else "amigurumi"
        stype = sys.argv[3] if len(sys.argv) > 3 else "patterns"
        
        results = orch.run_pipeline(
            {'query': query, 'search_type': stype},
            pipeline='search'
        )
        
        search = results.get('search', {})
        print(f"\n🔍 Search results for '{query}':")
        for r in search.get('results', []):
            print(f"  • {r.get('name', '')} ({r.get('difficulty', 'N/A')})")
    
    elif command == 'dashboard':
        orch.print_dashboard()
    
    elif command == 'learn':
        results = orch.run_pipeline({}, pipeline='learn')
        insights = results.get('learning', [])
        if isinstance(insights, list):
            for i in insights:
                print(f"  💡 {i.get('message', '')}")
        else:
            print(f"  📊 {json.dumps(results.get('learning', {}), indent=2)}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("   Try: validate, generate, search, dashboard, learn")

if __name__ == "__main__":
    main()
