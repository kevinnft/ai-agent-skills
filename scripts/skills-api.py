#!/usr/bin/env python3
"""
Skills Manager API - Lightweight REST API for ai-agent-skills

Features:
- Browse all skills
- Search & filter
- Get skill details
- One-click install
- Usage statistics
- RESTful API
- Lightweight (<50MB RAM, <10MB disk)
- Production-ready

API Endpoints:
    GET  /api/skills              - List all skills
    GET  /api/skills/:name        - Get skill details
    POST /api/skills/:name/install - Install skill
    GET  /api/skills/search?q=web - Search skills
    GET  /api/categories          - List categories
    GET  /api/stats               - Usage statistics
    GET  /health                  - Health check

Usage:
    ./scripts/skills-api.py                    # Start API server
    ./scripts/skills-api.py --port 8000        # Custom port
    ./scripts/skills-api.py --host 0.0.0.0     # Bind to all interfaces
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

try:
    from flask import Flask, jsonify, request, send_file
    from flask_cors import CORS
except ImportError:
    print("❌ Flask not installed. Install with: pip install flask flask-cors")
    sys.exit(1)

app = Flask(__name__)
CORS(app)  # Enable CORS for web access

# Configuration
SKILLS_DIR = Path.home() / '.hermes' / 'skills'
REPO_DIR = Path.cwd()
STATS_FILE = REPO_DIR / '.skills-stats.json'

@dataclass
class Skill:
    name: str
    category: str
    description: str
    path: str
    size_kb: int
    files: List[str]
    installed: bool

@dataclass
class Stats:
    total_installs: int
    popular_skills: Dict[str, int]
    last_updated: str

class SkillsManager:
    def __init__(self):
        self.repo_dir = REPO_DIR
        self.skills_dir = SKILLS_DIR
        self.stats = self.load_stats()
    
    def load_stats(self) -> Stats:
        """Load usage statistics"""
        if STATS_FILE.exists():
            try:
                with open(STATS_FILE, 'r') as f:
                    data = json.load(f)
                return Stats(**data)
            except:
                pass
        
        return Stats(
            total_installs=0,
            popular_skills={},
            last_updated=datetime.now().isoformat()
        )
    
    def save_stats(self):
        """Save usage statistics"""
        with open(STATS_FILE, 'w') as f:
            json.dump(asdict(self.stats), f, indent=2)
    
    def get_all_skills(self) -> List[Skill]:
        """Get all available skills"""
        skills = []
        skills_path = self.repo_dir / 'skills'
        
        if not skills_path.exists():
            return skills
        
        # Iterate through categories
        for category_dir in skills_path.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('.'):
                continue
            
            category = category_dir.name
            
            # Iterate through skills in category
            for skill_dir in category_dir.iterdir():
                if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                    continue
                
                skill_name = skill_dir.name
                skill_file = skill_dir / 'SKILL.md'
                
                if not skill_file.exists():
                    continue
                
                # Read description from SKILL.md
                description = self.extract_description(skill_file)
                
                # Get files
                files = [f.name for f in skill_dir.rglob('*') if f.is_file()]
                
                # Calculate size
                size_kb = sum(f.stat().st_size for f in skill_dir.rglob('*') if f.is_file()) // 1024
                
                # Check if installed
                installed = (self.skills_dir / category / skill_name).exists()
                
                skills.append(Skill(
                    name=skill_name,
                    category=category,
                    description=description,
                    path=str(skill_dir.relative_to(self.repo_dir)),
                    size_kb=size_kb,
                    files=files,
                    installed=installed
                ))
        
        return skills
    
    def extract_description(self, skill_file: Path) -> str:
        """Extract description from SKILL.md"""
        try:
            with open(skill_file, 'r') as f:
                content = f.read()
            
            # Try to find description in frontmatter
            match = re.search(r'description:\s*["\']?([^"\'\n]+)["\']?', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            
            # Try to find first paragraph
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('---'):
                    return line[:200]
            
            return "No description available"
        except:
            return "No description available"
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """Get skill by name"""
        skills = self.get_all_skills()
        for skill in skills:
            if skill.name == name:
                return skill
        return None
    
    def get_skill_content(self, name: str) -> Optional[str]:
        """Get skill content"""
        skill = self.get_skill(name)
        if not skill:
            return None
        
        skill_file = self.repo_dir / skill.path / 'SKILL.md'
        if not skill_file.exists():
            return None
        
        with open(skill_file, 'r') as f:
            return f.read()
    
    def search_skills(self, query: str) -> List[Skill]:
        """Search skills by name or description"""
        query = query.lower()
        skills = self.get_all_skills()
        
        results = []
        for skill in skills:
            if query in skill.name.lower() or query in skill.description.lower() or query in skill.category.lower():
                results.append(skill)
        
        return results
    
    def get_categories(self) -> List[Dict[str, any]]:
        """Get all categories with skill counts"""
        skills = self.get_all_skills()
        categories = {}
        
        for skill in skills:
            if skill.category not in categories:
                categories[skill.category] = 0
            categories[skill.category] += 1
        
        return [
            {'name': cat, 'count': count}
            for cat, count in sorted(categories.items())
        ]
    
    def install_skill(self, name: str) -> bool:
        """Install skill to ~/.hermes/skills/"""
        skill = self.get_skill(name)
        if not skill:
            return False
        
        # Create target directory
        target_dir = self.skills_dir / skill.category / skill.name
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy skill
        source_dir = self.repo_dir / skill.path
        
        try:
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(source_dir, target_dir)
            
            # Update stats
            self.stats.total_installs += 1
            if skill.name not in self.stats.popular_skills:
                self.stats.popular_skills[skill.name] = 0
            self.stats.popular_skills[skill.name] += 1
            self.stats.last_updated = datetime.now().isoformat()
            self.save_stats()
            
            return True
        except Exception as e:
            print(f"Error installing skill: {e}")
            return False

# Initialize manager
manager = SkillsManager()

# API Routes

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/skills', methods=['GET'])
def list_skills():
    """List all skills"""
    skills = manager.get_all_skills()
    
    # Optional filters
    category = request.args.get('category')
    installed = request.args.get('installed')
    
    if category:
        skills = [s for s in skills if s.category == category]
    
    if installed is not None:
        installed_bool = installed.lower() == 'true'
        skills = [s for s in skills if s.installed == installed_bool]
    
    return jsonify({
        'total': len(skills),
        'skills': [asdict(s) for s in skills]
    })

@app.route('/api/skills/<name>', methods=['GET'])
def get_skill(name: str):
    """Get skill details"""
    skill = manager.get_skill(name)
    
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    content = manager.get_skill_content(name)
    
    return jsonify({
        'skill': asdict(skill),
        'content': content
    })

@app.route('/api/skills/<name>/install', methods=['POST'])
def install_skill(name: str):
    """Install skill"""
    skill = manager.get_skill(name)
    
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    success = manager.install_skill(name)
    
    if success:
        return jsonify({
            'status': 'installed',
            'skill': name,
            'path': str(manager.skills_dir / skill.category / skill.name)
        })
    else:
        return jsonify({'error': 'Installation failed'}), 500

@app.route('/api/skills/search', methods=['GET'])
def search_skills():
    """Search skills"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
    results = manager.search_skills(query)
    
    return jsonify({
        'query': query,
        'total': len(results),
        'results': [asdict(s) for s in results]
    })

@app.route('/api/categories', methods=['GET'])
def list_categories():
    """List all categories"""
    categories = manager.get_categories()
    
    return jsonify({
        'total': len(categories),
        'categories': categories
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get usage statistics"""
    stats = manager.stats
    
    # Get top 10 popular skills
    popular = sorted(
        stats.popular_skills.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    return jsonify({
        'total_installs': stats.total_installs,
        'total_skills': len(manager.get_all_skills()),
        'total_categories': len(manager.get_categories()),
        'popular_skills': [
            {'name': name, 'installs': count}
            for name, count in popular
        ],
        'last_updated': stats.last_updated
    })

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'name': 'Skills Manager API',
        'version': '1.0.0',
        'description': 'Lightweight REST API for ai-agent-skills',
        'endpoints': {
            'GET /health': 'Health check',
            'GET /api/skills': 'List all skills',
            'GET /api/skills/:name': 'Get skill details',
            'POST /api/skills/:name/install': 'Install skill',
            'GET /api/skills/search?q=query': 'Search skills',
            'GET /api/categories': 'List categories',
            'GET /api/stats': 'Usage statistics'
        },
        'repository': 'https://github.com/kevinnft/ai-agent-skills',
        'documentation': 'https://github.com/kevinnft/ai-agent-skills/blob/main/docs/skills-api.md'
    })

def main():
    parser = argparse.ArgumentParser(
        description='Skills Manager API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  Skills Manager API v1.0.0                   ║
╚══════════════════════════════════════════════════════════════╝

🚀 Starting server...
📍 Host: {args.host}
🔌 Port: {args.port}
🌐 URL: http://{args.host}:{args.port}

📚 API Endpoints:
   GET  /health                      - Health check
   GET  /api/skills                  - List all skills
   GET  /api/skills/:name            - Get skill details
   POST /api/skills/:name/install    - Install skill
   GET  /api/skills/search?q=query   - Search skills
   GET  /api/categories              - List categories
   GET  /api/stats                   - Usage statistics

Press Ctrl+C to stop
""")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
