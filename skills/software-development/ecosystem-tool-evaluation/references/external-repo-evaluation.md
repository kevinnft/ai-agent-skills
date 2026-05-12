# External Repo Evaluation (Social Media Sources)

When user shares a repo link from Twitter/X, Reddit, HackerNews, or other social media, evaluate it systematically before recommending installation.

## Evaluation Framework

### 1. **Clone & Inspect**

```bash
cd /tmp
git clone --depth 1 <repo-url>
cd <repo-name>
ls -la
cat README.md | head -100
```

**Look for:**
- README quality (comprehensive vs minimal)
- LICENSE file (MIT, Apache, GPL, proprietary)
- Documentation (INSTALL.md, docs/, examples/)
- Tests (tests/, test/, __tests__/)
- Dependencies (requirements.txt, package.json, Cargo.toml)

### 2. **Assess Quality Signals**

| Signal | Good | Bad |
|--------|------|-----|
| **README** | Comprehensive, examples, screenshots | Minimal, no examples |
| **License** | MIT, Apache 2.0, BSD | No license, proprietary |
| **Docs** | INSTALL.md, docs/, examples/ | No docs |
| **Tests** | tests/ directory, CI badges | No tests |
| **Dependencies** | Listed, pinned versions | Unlisted, vague |
| **Activity** | Recent commits, active issues | Abandoned, no updates |
| **Stars/Forks** | 100+ stars, 10+ forks | <10 stars, 0 forks |

### 3. **AgentSkills Compatibility**

Check if repo follows AgentSkills standard:

```bash
# Look for SKILL.md
ls -la | grep SKILL.md

# Check structure
ls -la prompts/
ls -la tools/
ls -la references/
```

**AgentSkills markers:**
- ✅ `SKILL.md` at root
- ✅ `prompts/` directory (step-by-step prompts)
- ✅ `tools/` directory (Python/Node scripts)
- ✅ `references/` directory (docs, examples)
- ✅ Mentions "AgentSkills", "Claude Code", "Cursor", "Hermes"

### 4. **Installation Complexity**

| Level | Indicators | Action |
|-------|-----------|--------|
| **Low** | Single `pip install` or `npm install` | ✅ Recommend |
| **Medium** | 2-3 commands, common deps | ✅ Recommend with setup notes |
| **High** | Docker, databases, API keys | ⚠️ Explain complexity first |
| **Very High** | Infrastructure, ongoing maintenance | ❌ Explain why not suitable |

### 5. **Use Case Fit**

**Ask:**
- Does this solve a problem user has NOW?
- Is it better than existing tools?
- Does it integrate with user's workflow?

**Example:**
```
❌ Bad: "This is cool, install it!"
✅ Good: "This solves X problem you mentioned. Better than Y because Z. Want to install?"
```

## Evaluation Template

Use this structure for analysis:

```markdown
## 🔍 REPO ANALYSIS: <repo-name>

**URL:** <github-url>

### 🎯 Purpose:
<1-2 sentence description>

### ✅ Quality Signals:
- ✅/❌ README: <comprehensive/minimal>
- ✅/❌ License: <MIT/Apache/None>
- ✅/❌ Docs: <yes/no>
- ✅/❌ Tests: <yes/no>
- ✅/❌ Activity: <active/abandoned>

### 🛠️ Tech Stack:
- Language: <Python/Node/Rust/etc>
- Dependencies: <list key deps>
- Platform: <Linux/Mac/Windows/All>

### 📦 Installation:
- Complexity: <Low/Medium/High>
- Steps: <1-2 commands or "see INSTALL.md">
- Time: <2 min / 10 min / 30 min>

### 🎯 Use Case:
<When would user need this?>

### 🏆 Verdict:
<RECOMMEND / CONDITIONAL / SKIP>

**Reason:** <1-2 sentences>
```

## Case Study: Chinese IP Automation Skills

**Context:** User shared Twitter thread about patent-disclosure-skill and SoftwareCopyright-Skill.

**Evaluation:**

### patent-disclosure-skill

**Quality:**
- ✅ Comprehensive README (7KB)
- ✅ MIT License
- ✅ INSTALL.md + SKILL.md
- ✅ Examples + tests
- ✅ AgentSkills compatible

**Installation:**
- Medium complexity (pip + playwright + Node.js)
- 5-10 minutes setup
- Clear instructions

**Use Case:**
- Auto-generate Chinese patent disclosure documents
- Saves ¥5,000-10,000 per patent
- Useful for innovative projects

**Verdict:** ✅ RECOMMEND
- Production-ready
- Solves expensive problem
- AgentSkills compatible

### SoftwareCopyright-Skill

**Quality:**
- ✅ Comprehensive README (10KB)
- ✅ MIT License
- ✅ Demo included (6 screenshots)
- ✅ AgentSkills compatible
- ✅ Explicitly FREE (no paid services)

**Installation:**
- Low complexity (copy to skills dir)
- 2 minutes setup
- No extra dependencies

**Use Case:**
- Auto-generate Chinese software copyright materials
- Saves ¥500-1,000 + 2-3 days work
- Useful for ALL software projects

**Verdict:** ✅ RECOMMEND
- Production-ready
- Solves tedious problem
- Zero setup friction

## Common Pitfalls

### 1. **Recommending Without Inspecting**

❌ Bad:
```
User: "Check this repo"
Agent: "Looks good, install it!"
```

✅ Good:
```
User: "Check this repo"
Agent: [clones, reads README, checks structure]
Agent: "This is a <description>. Quality: <signals>. Use case: <when>. Verdict: <recommend/skip>"
```

### 2. **Ignoring Installation Complexity**

❌ Bad:
```
"This tool is great! Installing..."
[30 minutes later]
"Needs Docker + PostgreSQL + API keys..."
```

✅ Good:
```
"This tool requires Docker + PostgreSQL + API keys (30 min setup).
Use case: <when>. Worth it? Or skip?"
```

### 3. **Not Checking AgentSkills Compatibility**

❌ Bad:
```
"This is a Python script, should work."
```

✅ Good:
```
"This follows AgentSkills standard (SKILL.md + prompts/).
Compatible with Hermes/Claude Code/Cursor."
```

### 4. **Missing Use Case Fit**

❌ Bad:
```
"This tool does X, Y, Z. Install?"
```

✅ Good:
```
"This tool does X, Y, Z.
Use case: When you need <specific problem>.
You mentioned <related problem> earlier — this solves it.
Install?"
```

## Social Media Source Patterns

### Twitter/X

**Pattern:** User shares tweet with repo link

**Approach:**
1. Extract repo URL from tweet
2. Clone and inspect
3. Check tweet context (why was it shared?)
4. Evaluate quality + use case
5. Provide verdict

**Example:**
```
Tweet: "知识产权全面沦陷" (IP completely collapsed)
Links: patent-disclosure-skill, SoftwareCopyright-Skill

Analysis:
- Both are Chinese IP automation tools
- High quality (MIT, docs, examples)
- AgentSkills compatible
- Solve expensive problems (¥5k-10k saved)
- Verdict: RECOMMEND both
```

### Reddit/HackerNews

**Pattern:** User shares discussion thread

**Approach:**
1. Read thread comments (community feedback)
2. Extract repo links
3. Check upvotes/engagement
4. Evaluate quality + community sentiment
5. Provide verdict

### GitHub Awesome Lists

**Pattern:** User shares awesome-* list

**Approach:**
1. Scan list for relevant tools
2. Filter by category
3. Evaluate top 3-5 tools
4. Compare and recommend best fit

## Rules

1. **Always clone and inspect** — Don't recommend based on description alone
2. **Check AgentSkills compatibility** — Look for SKILL.md, prompts/, tools/
3. **Assess installation complexity** — Mention setup time upfront
4. **Evaluate use case fit** — Does user need this NOW?
5. **Provide verdict** — RECOMMEND / CONDITIONAL / SKIP with reason
6. **Show examples** — For visual tools, show output samples
7. **Compare alternatives** — If skipping, suggest what to use instead

## When to Use This Reference

- User shares repo link from Twitter/X, Reddit, HN
- User asks "is this good?" about external tool
- User wants to evaluate multiple repos from curated list
- User asks for installation recommendation

## Related Skills

- `ecosystem-tool-evaluation` — Main skill (this is a reference)
- `hermes-agent` — For Hermes-specific tool evaluation
- `spike` — For experimental tool testing
