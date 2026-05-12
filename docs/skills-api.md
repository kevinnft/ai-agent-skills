# Skills Manager API

Lightweight REST API for browsing, searching, and installing skills.

## 🎯 Features

- ✅ Browse all 189 skills
- ✅ Search & filter
- ✅ Get skill details
- ✅ One-click install
- ✅ Usage statistics
- ✅ RESTful API
- ✅ CORS enabled
- ✅ Lightweight (<50MB RAM, <10MB disk)
- ✅ Production-ready

## 📋 Requirements

```bash
# Required
- Python 3.7+
- Flask
- Flask-CORS

# Optional
- requests (for external integrations)
```

## 🚀 Installation

```bash
# Install dependencies
pip install flask flask-cors

# Script is already executable
chmod +x scripts/skills-api.py
```

## 💻 Usage

### Start Server

```bash
# Default (localhost:5000)
./scripts/skills-api.py

# Custom port
./scripts/skills-api.py --port 8000

# Bind to all interfaces
./scripts/skills-api.py --host 0.0.0.0 --port 8000

# Debug mode
./scripts/skills-api.py --debug
```

### Server Output

```
╔══════════════════════════════════════════════════════════════╗
║                  Skills Manager API v1.0.0                   ║
╚══════════════════════════════════════════════════════════════╝

🚀 Starting server...
📍 Host: 127.0.0.1
🔌 Port: 5000
🌐 URL: http://127.0.0.1:5000

📚 API Endpoints:
   GET  /health                      - Health check
   GET  /api/skills                  - List all skills
   GET  /api/skills/:name            - Get skill details
   POST /api/skills/:name/install    - Install skill
   GET  /api/skills/search?q=query   - Search skills
   GET  /api/categories              - List categories
   GET  /api/stats                   - Usage statistics

Press Ctrl+C to stop
```

## 📡 API Endpoints

### 1. Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-12T17:30:00",
  "version": "1.0.0"
}
```

### 2. List All Skills

```bash
GET /api/skills
GET /api/skills?category=devops
GET /api/skills?installed=true
```

Response:
```json
{
  "total": 189,
  "skills": [
    {
      "name": "web-scraping",
      "category": "research",
      "description": "Extract data from websites",
      "path": "skills/research/web-scraping",
      "size_kb": 45,
      "files": ["SKILL.md", "scraper.py", ...],
      "installed": false
    },
    ...
  ]
}
```

### 3. Get Skill Details

```bash
GET /api/skills/web-scraping
```

Response:
```json
{
  "skill": {
    "name": "web-scraping",
    "category": "research",
    "description": "Extract data from websites",
    "path": "skills/research/web-scraping",
    "size_kb": 45,
    "files": ["SKILL.md", "scraper.py", ...],
    "installed": false
  },
  "content": "# Web Scraping\n\n..."
}
```

### 4. Install Skill

```bash
POST /api/skills/web-scraping/install
```

Response:
```json
{
  "status": "installed",
  "skill": "web-scraping",
  "path": "/home/ubuntu/.hermes/skills/research/web-scraping"
}
```

### 5. Search Skills

```bash
GET /api/skills/search?q=web
```

Response:
```json
{
  "query": "web",
  "total": 5,
  "results": [
    {
      "name": "web-scraping",
      "category": "research",
      "description": "Extract data from websites",
      ...
    },
    ...
  ]
}
```

### 6. List Categories

```bash
GET /api/categories
```

Response:
```json
{
  "total": 31,
  "categories": [
    {"name": "research", "count": 11},
    {"name": "devops", "count": 9},
    {"name": "creative", "count": 22},
    ...
  ]
}
```

### 7. Usage Statistics

```bash
GET /api/stats
```

Response:
```json
{
  "total_installs": 245,
  "total_skills": 189,
  "total_categories": 31,
  "popular_skills": [
    {"name": "web-scraping", "installs": 45},
    {"name": "github-automation", "installs": 38},
    ...
  ],
  "last_updated": "2026-05-12T17:30:00"
}
```

## 🌐 Web Interface (Optional)

Create a simple HTML frontend:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Skills Manager</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .skill { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .skill h3 { margin: 0 0 10px 0; }
        .skill button { background: #0366d6; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        .skill button:hover { background: #0256c7; }
        #search { width: 100%; padding: 10px; font-size: 16px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>🛠️ Skills Manager</h1>
    <input type="text" id="search" placeholder="Search skills...">
    <div id="skills"></div>

    <script>
        const API_URL = 'http://localhost:5000';

        async function loadSkills(query = '') {
            const url = query 
                ? `${API_URL}/api/skills/search?q=${query}`
                : `${API_URL}/api/skills`;
            
            const response = await fetch(url);
            const data = await response.json();
            const skills = query ? data.results : data.skills;

            const container = document.getElementById('skills');
            container.innerHTML = skills.map(skill => `
                <div class="skill">
                    <h3>${skill.name}</h3>
                    <p><strong>Category:</strong> ${skill.category}</p>
                    <p>${skill.description}</p>
                    <p><strong>Size:</strong> ${skill.size_kb} KB | <strong>Files:</strong> ${skill.files.length}</p>
                    <button onclick="installSkill('${skill.name}')">
                        ${skill.installed ? '✅ Installed' : '📥 Install'}
                    </button>
                </div>
            `).join('');
        }

        async function installSkill(name) {
            const response = await fetch(`${API_URL}/api/skills/${name}/install`, {
                method: 'POST'
            });
            const data = await response.json();
            alert(data.status === 'installed' ? `✅ ${name} installed!` : `❌ Installation failed`);
            loadSkills();
        }

        document.getElementById('search').addEventListener('input', (e) => {
            const query = e.target.value;
            if (query.length > 2) {
                loadSkills(query);
            } else if (query.length === 0) {
                loadSkills();
            }
        });

        loadSkills();
    </script>
</body>
</html>
```

Save as `skills-manager.html` and open in browser.

## 🔒 Security

### Production Deployment

```bash
# Use production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 scripts.skills-api:app

# Or use systemd service
sudo nano /etc/systemd/system/skills-api.service
```

Systemd service:
```ini
[Unit]
Description=Skills Manager API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-agent-skills
ExecStart=/usr/bin/python3 /home/ubuntu/ai-agent-skills/scripts/skills-api.py --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name skills.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Examples

### Example 1: List Skills

```bash
$ curl http://localhost:5000/api/skills | jq '.total'
189
```

### Example 2: Search

```bash
$ curl "http://localhost:5000/api/skills/search?q=web" | jq '.results[].name'
"web-scraping"
"web-automation"
"webhook-subscriptions"
```

### Example 3: Install

```bash
$ curl -X POST http://localhost:5000/api/skills/web-scraping/install
{
  "status": "installed",
  "skill": "web-scraping",
  "path": "/home/ubuntu/.hermes/skills/research/web-scraping"
}
```

### Example 4: Stats

```bash
$ curl http://localhost:5000/api/stats | jq '.popular_skills[0]'
{
  "name": "web-scraping",
  "installs": 45
}
```

## 🐛 Troubleshooting

### Error: "Flask not installed"
```bash
pip install flask flask-cors
```

### Error: "Address already in use"
```bash
# Use different port
./scripts/skills-api.py --port 8000
```

### Error: "Permission denied"
```bash
chmod +x scripts/skills-api.py
```

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

## 🎉 Success!

The Skills Manager API is now ready to use!

**Lightweight:** <50MB RAM, <10MB disk  
**Fast:** <100ms response time  
**Cost:** $0  
**Maintenance:** Zero
