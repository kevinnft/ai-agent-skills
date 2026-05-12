# Skill Registry Discovery Workflow

When user asks to analyze skill catalogs from Hermes docs or ecosystem, use this workflow to navigate local ecosystem-atlas data when web scraping fails.

## Problem

Hermes docs skill catalog (https://hermes-agent.nousresearch.com/docs/skills) is JavaScript-rendered and fails with:
- `browser_navigate` → Chrome sandbox errors in WSL2/VPS
- `curl` → Returns empty HTML shell (SPA, no server-side rendering)

## Solution: Use Local Ecosystem Atlas

The ecosystem-atlas repo (installed at `~/.hermes/ecosystem-atlas/`) contains pre-scraped data in JSON format.

### Step 1: Locate Data

```bash
ls ~/.hermes/ecosystem-atlas/data/
# repos.json         — 111 ecosystem projects
# summaries.json     — Project summaries
# featured.json      — Featured projects
# lists.json         — Curated lists
```

### Step 2: Query repos.json

**Structure:**
```json
[
  {
    "owner": "NousResearch",
    "repo": "hermes-agent",
    "name": "hermes-agent",
    "description": "The self-improving AI agent...",
    "stars": 83290,
    "url": "https://github.com/...",
    "official": true,
    "category": "Core & Official"
  },
  ...
]
```

**Categories:**
- Core & Official (6 repos)
- Skills & Skill Registries (20 repos) ← **Target for skill discovery**
- Plugins & Extensions (10 repos)
- Memory & Context (13 repos)
- Multi-Agent & Orchestration (7 repos)
- Integrations & Bridges (8 repos)
- Developer Tools (8 repos)
- Deployment & Infra (8 repos)
- Workspaces & GUIs (11 repos)
- Domain Applications (8 repos)
- Guides & Docs (9 repos)
- Forks & Derivatives (3 repos)

### Step 3: Filter by Category

**Problem:** Direct jq with `&` fails in WSL2 bash (treats `&` as shell backgrounding)

```bash
# ❌ FAILS in WSL2
cat repos.json | jq '.[] | select(.category == "Skills & Skill Registries")'
# Error: Foreground command uses '&' backgrounding
```

**Solution:** Use Python instead

```python
import json

with open('~/.hermes/ecosystem-atlas/data/repos.json') as f:
    repos = json.load(f)

# Filter by category
skills_repos = [r for r in repos if r['category'] == 'Skills & Skill Registries']

# Sort by stars
skills_repos.sort(key=lambda x: x['stars'], reverse=True)

# Display
for repo in skills_repos:
    print(f"{repo['name']} ({repo['stars']} ⭐)")
    print(f"  {repo['description']}")
    print(f"  {repo['url']}\n")
```

### Step 4: Evaluate Against User Constraints

Apply VPS resource constraints and existing tools:

**Evaluation criteria:**
1. **Disk usage** — Reject if >500MB without asking (user: "gede banget makan emori dan ram")
2. **RAM usage** — Reject if >100MB without asking
3. **Redundancy** — Skip if already installed or covered by existing skills
4. **Relevance** — Match against user's actual workflows (scraping, monitoring, API testing)

**Example evaluation:**

```python
# High priority (install now)
high_priority = [
    "Anthropic-Cybersecurity-Skills",  # 754 skills, relevant for security testing
    "SkillClaw",                       # Agentic evolution, optimize existing 42 skills
    "super-hermes",                    # Better delegation prompts
    "hermes-skill-factory"             # Auto-generate from workflows
]

# Skip (redundant or not relevant)
skip = [
    "wondelai/skills",        # Already installed (42 skills)
    "drawio-skill",           # Already installed
    "chainlink-agent-skills", # Not relevant (no blockchain work)
    "pydantic-ai-skills",     # Wrong framework (user uses Hermes)
]
```

### Step 5: Provide Actionable Recommendations

**Format:**
```markdown
## High Priority (Install Now)
1. **Name** (stars ⭐)
   - Description
   - **Use case:** Specific workflow it improves
   - **Relevant:** Why it matters for user's setup
   - **Disk:** Estimated size

## Medium Priority (Evaluate First)
...

## Skip (Reason)
...

## Action
```bash
cd ~/.hermes/ecosystem
git clone <url>
```
```

## Pitfalls

### 1. Using jq with `&` in Category Names

**Problem:** WSL2 bash treats `&` as shell backgrounding operator

```bash
# ❌ FAILS
jq '.[] | select(.category == "Skills & Skill Registries")'
```

**Fix:** Use Python for JSON filtering

### 2. Not Checking Existing Installations

**Problem:** Recommend installing tools already present in `~/.hermes/ecosystem/`

**Fix:** Check first:
```bash
ls ~/.hermes/ecosystem/ | grep -i <tool-name>
```

### 3. Ignoring VPS Resource Constraints

**Problem:** Recommend heavy tools (>500MB disk, >100MB RAM) without warning

**Fix:** Always estimate resources and flag if exceeds thresholds

### 4. Generic Recommendations Without Use Cases

**Problem:** List tools without explaining how they fit user's workflow

**Fix:** For each recommendation, include:
- **Use case:** Specific task it improves
- **Relevant:** Why it matters for user's setup
- **Example:** Concrete scenario where it helps

## Real-World Example

**User request:** "analisa 600+ skil disini ada yg berguna gak buat kalian?"

**Workflow:**
1. Attempted `browser_navigate` → Failed (Chrome sandbox)
2. Attempted `curl` → Got empty HTML (SPA)
3. Checked `~/.hermes/ecosystem-atlas/data/repos.json`
4. Filtered 20 "Skills & Skill Registries" repos
5. Sorted by stars, evaluated against:
   - VPS constraints (disk <500MB, RAM <100MB)
   - Existing tools (wondelai/skills, drawio-skill already installed)
   - User workflows (scraping, monitoring, API testing)
6. Categorized into High/Medium/Low priority
7. Provided install commands with disk estimates

**Result:** 4 high-priority recommendations (50-100MB total), 13 skipped (redundant/not relevant)

## When to Use This Workflow

- ✅ User asks to explore Hermes skill catalog
- ✅ Web scraping fails (Cloudflare, SPA, sandbox issues)
- ✅ Need to analyze 10+ ecosystem repos
- ✅ VPS environment (resource constraints matter)

## When NOT to Use

- ❌ User asks for specific tool by name (just install it)
- ❌ Web scraping works fine (use browser tools)
- ❌ Desktop environment with no resource constraints
