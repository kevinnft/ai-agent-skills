# Quality Dashboard

Real-time monitoring of repository health, metrics, and quality scores.

## 🎯 Features

- ✅ Repository metrics (stars, forks, issues, PRs)
- ✅ Health checks (README, LICENSE, CI, broken links)
- ✅ Code quality analysis
- ✅ Contributor statistics
- ✅ Quality score calculation (0-100, heuristic — see `scripts/quality-dashboard.py`)
- ✅ Badge generation
- ✅ JSON export
- ✅ Automated alerts
- ✅ Telegram notifications

## 📋 Requirements

```bash
# Required
- Python 3.7+
- PyGithub
- GitHub token

# Optional
- requests (for Telegram notifications)
```

## 🚀 Installation

```bash
# Install dependencies
pip install PyGithub requests

# Set GitHub token
export GITHUB_TOKEN="your_github_token"

# Or add to ~/.bashrc
echo 'export GITHUB_TOKEN="your_github_token"' >> ~/.bashrc
```

## 💻 Usage

### Basic Usage

```bash
# Run dashboard
./scripts/quality-dashboard.py

# Specific repository
./scripts/quality-dashboard.py --repo owner/repo

# JSON output
./scripts/quality-dashboard.py --json

# Generate badge only
./scripts/quality-dashboard.py --badge

# Check and alert
./scripts/quality-dashboard.py --alert
```

## 📊 Dashboard Output

```
======================================================================
📊 QUALITY DASHBOARD: kevinnft/ai-agent-skills
======================================================================

Overall Quality Score: 92/100   # heuristic — see scripts/quality-dashboard.py

📈 Repository Metrics:
  ⭐ Stars: 5
  🍴 Forks: 12
  👀 Watchers: 8
  📋 Open Issues: 3
  🔀 Open PRs: 1
  👥 Contributors: 5
  📝 Commits (7d): 12
  📝 Commits (30d): 45
  🕐 Last Commit: 2026-05-12 17:30
  💾 Size: 25600 KB

🏥 Health Checks:
  ✅ README.md: README.md present
  ✅ LICENSE: LICENSE present
  ✅ CONTRIBUTING.md: CONTRIBUTING.md present
  ✅ CODE_OF_CONDUCT.md: CODE_OF_CONDUCT.md present
  ✅ CI/CD: 2 workflow(s) configured
  ✅ Broken Links: No broken links detected
  ✅ SECURITY.md: SECURITY.md present

🎯 Quality Breakdown:
  Health: 100/100
  Activity: 85/100
  Community: 75/100
  Documentation: 100/100
  Code Quality: 100/100

🏷️  Quality Badge:
  Markdown: ![Quality](https://img.shields.io/badge/quality-92%25%20excellent-brightgreen)
  URL: https://img.shields.io/badge/quality-92%25%20excellent-brightgreen

======================================================================
```

## 📈 Quality Score Calculation

### Overall Score (0-100)
Weighted average of:
- Health: 25%
- Activity: 20%
- Community: 15%
- Documentation: 20%
- Code Quality: 20%

### Health Score
Based on health checks:
- README.md present
- LICENSE present
- CONTRIBUTING.md present
- CODE_OF_CONDUCT.md present
- SECURITY.md present
- CI/CD configured
- No broken links

### Activity Score
Based on:
- Commits this week (max 50 points)
- Commits this month (max 30 points)
- Recent commit (20 points)

### Community Score
Based on:
- Stars (max 40 points)
- Forks (max 30 points)
- Contributors (max 30 points)

### Documentation Score
Based on documentation files present:
- README.md
- LICENSE
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- SECURITY.md

### Code Quality Score
Based on:
- No broken links (+20)
- CI/CD configured (+30)
- Other quality checks (+50)

## 🏷️ Quality Badge

Add to your README.md:

```markdown
![Quality](https://img.shields.io/badge/quality-92%25%20excellent-brightgreen)
```

Badge colors:
- 90-100: `brightgreen` (excellent)
- 75-89: `green` (good)
- 60-74: `yellow` (fair)
- 0-59: `red` (needs improvement)

## 🔔 Automated Alerts

Enable alerts for:
- Overall score < 60
- Critical health checks failed
- Warning health checks failed

### Telegram Alerts

```bash
# Set environment variables
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# Run with alerts
./scripts/quality-dashboard.py --alert
```

## 📤 JSON Export

```bash
# Export as JSON
./scripts/quality-dashboard.py --json > quality-report.json
```

JSON structure:
```json
{
  "repository": "kevinnft/ai-agent-skills",
  "timestamp": "2026-05-12T17:30:00",
  "metrics": {
    "stars": 45,
    "forks": 12,
    ...
  },
  "health_checks": [
    {
      "name": "README.md",
      "status": true,
      "message": "README.md present",
      "severity": "info"
    },
    ...
  ],
  "quality_score": {
    "overall": 92,
    "health": 100,
    "activity": 85,
    "community": 75,
    "documentation": 100,
    "code_quality": 100
  },
  "badge_url": "https://img.shields.io/badge/quality-92%25%20excellent-brightgreen"
}
```

## 🤖 Automation

### Cron Job (Daily Check)

```bash
# Add to crontab
crontab -e

# Run daily at 9 AM
0 9 * * * cd ~/ai-agent-skills && ./scripts/quality-dashboard.py --alert
```

### GitHub Actions (Weekly Report)

```yaml
name: Quality Report

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install PyGithub requests
      
      - name: Run Quality Dashboard
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: ./scripts/quality-dashboard.py --alert
```

## 📊 Examples

### Example 1: Basic Dashboard

```bash
$ ./scripts/quality-dashboard.py

📊 Analyzing repository...

======================================================================
📊 QUALITY DASHBOARD: kevinnft/ai-agent-skills
======================================================================

Overall Quality Score: 92/100   # heuristic — see scripts/quality-dashboard.py

[... full dashboard output ...]
```

### Example 2: JSON Export

```bash
$ ./scripts/quality-dashboard.py --json

{
  "repository": "kevinnft/ai-agent-skills",
  "timestamp": "2026-05-12T17:30:00",
  "metrics": { ... },
  "health_checks": [ ... ],
  "quality_score": { ... }
}
```

### Example 3: Alerts

```bash
$ ./scripts/quality-dashboard.py --alert

📊 Analyzing repository...

🚨 ALERTS:
  ⚠️  Overall quality score is low: 58/100
  ❌ Critical: README.md missing
  ⚠️  Warning: LICENSE missing
```

## 🐛 Troubleshooting

### Error: "PyGithub not installed"
```bash
pip install PyGithub
```

### Error: "GitHub token not found"
```bash
export GITHUB_TOKEN="your_token"
```

### Error: "Rate limit exceeded"
```bash
# Wait for rate limit reset
# Or use authenticated requests (already done)
```

## 📚 Resources

- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [Shields.io Badges](https://shields.io/)

## 🎉 Success!

The Quality Dashboard is now ready to use!

**Monitoring:** 24/7 automated  
**Alerts:** Real-time  
**Cost:** $0  
**Maintenance:** Zero
