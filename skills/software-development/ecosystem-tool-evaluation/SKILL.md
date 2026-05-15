---
name: ecosystem-tool-evaluation
description: Evaluate and install ecosystem tools (Hermes plugins, skills, integrations) — assess complexity vs. benefit before installation, show examples for visual tools, and avoid "cloned but not configured" states.
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [ecosystem, tools, installation, evaluation, user-preference]
    related_skills: [hermes-agent, spike]
origin: original
source_repo: kevinnft/ai-agent-skills
source_url: https://github.com/kevinnft/ai-agent-skills
source_license: MIT
language: en
---

# Ecosystem Tool Evaluation

When users ask to "install all useful tools" or explore an ecosystem, evaluate each tool's complexity vs. benefit BEFORE installing. Avoid leaving tools in "cloned but not configured" states.

## Core Principle

**Evaluate → Decide → Install (or Skip)**

Don't clone/install first and explain complexity later. The user's time and disk space are valuable.

## Evaluation Framework

For each tool, assess:

### 1. **Setup Complexity**

| Level | Description | Examples | Action |
|-------|-------------|----------|--------|
| **Low** | Single command, no dependencies | `npm install -g tool`, `pip install tool` | ✅ Install immediately |
| **Medium** | 2-3 commands, common dependencies | Install app + config file | ✅ Install with brief explanation |
| **High** | Multiple steps, external services | Docker + database + API keys + integration | ⚠️ Explain complexity, ask before proceeding |
| **Very High** | Infrastructure setup, ongoing maintenance | Self-hosted services, multi-component systems | ❌ Explain why it's complex, offer alternatives |

### 2. **Immediate Usability**

- **Ready after install?** (✅ tokscale, draw.io) → Install
- **Needs configuration?** (⚠️ API keys, config files) → Install + configure
- **Needs integration?** (❌ hindsight → Hermes) → Explain complexity first

### 3. **Value vs. Effort**

| Scenario | Setup Time | Value | Decision |
|----------|-----------|-------|----------|
| High value, low effort | 2-5 min | High | ✅ Install |
| High value, medium effort | 10-15 min | High | ✅ Install with explanation |
| High value, high effort | 30-60 min | High | ⚠️ Ask user first |
| Low value, any effort | Any | Low | ❌ Skip or explain why not worth it |
| Marginal value, high effort | 30+ min | Marginal | ❌ Skip, explain alternative |

## User Preference Patterns

### For "Gas" Users (Full Automation)

**User signal:** "gas dan otomatis aktif maksimal dan perfect lalu test pastikan sempurna"

**Pattern:** User wants FULL AUTOMATION with verification, not step-by-step confirmation.

**Workflow:**
```
1. Clone all repos
2. Install all skills
3. Configure automatically
4. Test & verify
5. Commit to git
6. Report results

NO intermediate confirmations.
NO "want me to proceed?" questions.
JUST DO IT and show final status.
```

**Example:**
```
❌ Bad:
"I found 4 trending skills repos. Want me to clone them?"
[waits for confirmation]
"Cloned. Want me to install?"
[waits for confirmation]

✅ Good:
"Gas! Cloning, installing, testing..."
[does everything]
"✅ COMPLETE: 64 skills installed, tested, committed (cdd7855)"
```

**When to use:**
- User says "gas" (go fast)
- User says "otomatis" (automatic)
- User says "maksimal" (maximize)
- User says "pastikan sempurna" (ensure perfect)

**What to do:**
1. Execute full workflow without asking
2. Test & verify at each step
3. Report final status with evidence
4. Only stop if critical error

**What NOT to do:**
- Don't ask "want me to proceed?"
- Don't wait for confirmation between steps
- Don't explain what you're about to do
- Just DO IT and report results

### For Visual/UI Tools

**Don't ask "want to install X?" without context.**

**Do show examples first:**

```
❌ Bad:
"Want me to install draw.io for diagram generation?"

✅ Good:
"draw.io can generate diagrams like this: [show 3-4 example images]
These are useful for architecture diagrams, flowcharts, network topology.
Want me to install it? (2 minutes setup)"
```

**Why:** Users can't evaluate visual tools without seeing output. Show, don't tell.

### For Complex Infrastructure

**Don't clone first, explain later.**

**Do evaluate complexity upfront:**

```
❌ Bad:
[clones hindsight]
"hindsight is cloned but not configured because it needs Docker + PostgreSQL..."

✅ Good:
"hindsight requires:
- Docker + PostgreSQL (30 min setup)
- LLM API key (additional costs)
- Hermes integration code
- Ongoing maintenance (server 24/7)

Current built-in memory is sufficient for single-user use.
Want to proceed anyway, or skip?"
```

**Why:** Avoid "cloned but not configured" states. Either install fully or don't install.

### For "Install All Useful" Requests

**Don't install everything blindly.**

**Do categorize by readiness:**

1. **Install immediately:** Low complexity, high value (tokscale, skills libraries)
2. **Install with explanation:** Medium complexity, high value (draw.io + xvfb)
3. **Explain and ask:** High complexity, high value (web dashboards, multi-agent)
4. **Skip and explain:** High complexity, marginal value (hindsight for single user)

### For Tool/Project Analysis Requests

**When user asks to analyze a tool/project, assess relevance FIRST before dumping features.**

**Pattern:**
1. **Immediate relevance check** — "Is this urgent/important for current workflow?"
2. **If not urgent** — Say so directly, then provide analysis
3. **If urgent** — Lead with why it matters, then details

**Example:**

```
❌ Bad:
User: "Analisa Obsidian"
Agent: [dumps 12KB feature list immediately]

✅ Good:
User: "Analisa Obsidian"
Agent: "Gak ada yang urgent untuk saat ini. Semua skills itu optional — buat upgrade workflow lo aja kalau mau.

Yang paling immediately useful kalau lo sering:
1. Debugging masalah → systematic-debugging
2. Scraping/automation → web-scraping
3. Bikin custom skills → hermes-agent-skill-authoring

[then full analysis if user wants details]"
```

**Why:** User time is valuable. Relevance assessment prevents "analysis paralysis" from feature overload. User can decide whether to invest time reading full analysis.

**User signal:** "Gak ada yg penting untuk saat ini?" = User wants honest assessment, not sales pitch.

## Decision Tree

```
User asks to install tool X
  ↓
Assess setup complexity
  ↓
Low (1-2 commands)?
  ├─ Yes → Install immediately
  └─ No → Continue
      ↓
Medium (3-5 commands)?
  ├─ Yes → Install with brief explanation
  └─ No → Continue
      ↓
High (10+ commands or external services)?
  ├─ Immediate value? → Explain complexity, ask user
  └─ Marginal value? → Explain why not worth it, offer alternative
```

## Common Pitfalls

### 1. **"Cloned but Not Configured"**

**Problem:** Tool is downloaded but unusable, wasting disk space and creating confusion.

**Example:**
```
hindsight (cloned) ⚠️ NOT CONFIGURED
  - Needs Docker + PostgreSQL
  - Needs integration code
  - User doesn't know what to do with it
```

**Fix:** Either configure fully or don't install. No half-states.

### 2. **Installing Without Showing Value**

**Problem:** User can't evaluate visual/UI tools without seeing examples.

**Example:**
```
❌ "draw.io generates diagrams. Want to install?"
   → User doesn't know what kind of diagrams or quality
```

**Fix:** Show 3-4 example outputs first, then ask.

### 3. **Ignoring Maintenance Costs**

**Problem:** Tool requires ongoing maintenance (server, updates, costs) but this isn't mentioned upfront.

**Example:**
```
❌ "hindsight provides better memory. Installing..."
   → User later discovers it needs server running 24/7 + LLM API costs
```

**Fix:** Mention maintenance requirements upfront: "Requires server running 24/7 and LLM API costs for reflect operation."

### 3a. **Installing More Than Requested**

**Problem:** User asks for specific tools, but installation script includes extras that consume resources.

**Example:**
```
❌ User: "Install Wiki + Ecosystem only"
   Agent: [runs script that installs Wiki + Ecosystem + HUD]
   User: "saya kan gak suruh install ini yg memakan ram"
   → HUD consumes 50MB RAM that user didn't want
```

**Fix:** 
- Read user request carefully — if they list specific tools, install ONLY those
- If using a batch install script, verify what it installs before running
- When user says "only X and Y", don't add Z even if it's in the "recommended" category
- Resource-consuming tools (RAM, CPU, disk) require explicit user consent

### 3a. **Installing More Than Requested**

**Problem:** User asks for specific tools, but installation script includes extras that consume resources.

**Example:**
```
❌ User: "Install Wiki + Ecosystem only"
   Agent: [runs script that installs Wiki + Ecosystem + HUD]
   User: "saya kan gak suruh install ini yg memakan ram"
   → HUD consumes 50MB RAM that user didn't want
```

**Fix:** 
- Read user request carefully — if they list specific tools, install ONLY those
- If using a batch install script, verify what it installs before running
- When user says "only X and Y", don't add Z even if it's in the "recommended" category
- Resource-consuming tools (RAM, CPU, disk) require explicit user consent

### 4. **Not Offering Alternatives**

**Problem:** Rejecting a complex tool without explaining what the user should use instead.

**Example:**
```
❌ "hindsight is too complex, skipping."
   → User doesn't know what to use for memory
```

**Fix:** "hindsight is too complex for single-user use. Current built-in memory (SQLite + FTS5) is sufficient. If you need advanced features later, consider Hindsight Cloud (managed service)."

## Verification Checklist

After installation, verify:

1. ✅ **Tool works** — Run basic test command
2. ✅ **Dependencies met** — All required components installed
3. ✅ **User can use it** — Clear usage instructions provided
4. ✅ **Documentation updated** — Installation logged in INSTALLED.md or similar

If any step fails, either fix it or remove the tool. No "partially installed" states.

## Examples

### Example 1: tokscale (Low Complexity, High Value)

```
✅ Install immediately:

1. npm install -g tokscale (2 min)
2. Verify: tokscale --version
3. Test: tokscale clients
4. Done — ready to use
```

### Example 2: draw.io (Medium Complexity, High Value)

```
✅ Show examples first, then install:

1. Show 3-4 diagram examples
2. Explain use cases (architecture, flowcharts, network)
3. Ask: "Want me to install? (2 min setup)"
4. If yes:
   - sudo snap install drawio
   - sudo apt-get install xvfb
   - Test export
   - Done
```

### Example 3: hindsight (High Complexity, Marginal Value)

```
❌ Explain complexity, offer alternative:

"hindsight requires:
- Docker + PostgreSQL (30 min)
- LLM API key (costs)
- Hermes integration
- Server 24/7

Current built-in memory is sufficient for your use case.

Alternative: Use built-in Hermes memory (SQLite + FTS5).
If you need advanced features later, consider Hindsight Cloud."

→ Skip installation
```

## Rules

1. **Evaluate before installing** — Don't clone first, explain later
2. **Show examples for visual tools** — Users can't evaluate without seeing output
3. **Explain complexity upfront** — Mention setup time, dependencies, maintenance
4. **Offer alternatives** — If rejecting a tool, explain what to use instead
5. **No half-states** — Either install fully or don't install
6. **Verify after install** — Test that tool actually works
7. **Document installations** — Update INSTALLED.md or similar

## When to Skip This Skill

- User explicitly says "just install X" (specific tool, not "all useful")
- Tool is trivial (single command, no dependencies)
- User is experienced and knows what they're asking for

## Advanced: Multi-Repo Ecosystem Analysis

For analyzing 5+ repos from a curated list (tweet, blog, awesome list), see:
- `references/batch-repo-analysis-workflow.md` — Systematic approach for batch evaluation, comparison tables, resource impact analysis, and delegation patterns
- `references/skill-registry-discovery.md` — Navigate local ecosystem-atlas data when web scraping fails (WSL2 sandbox issues, SPA rendering), filter by category, evaluate against VPS constraints
- `references/external-repo-evaluation.md` — Evaluate third-party repos from social media (Twitter/X, Reddit, HN) for AgentSkills compatibility, installation complexity, and use case fit

## Platform-Specific Installation Issues

### Ubuntu 24.04 / Debian 12+ pip Install Failures

See `references/ubuntu-2404-pip-workarounds.md` for:
- PEP 668 externally-managed-environment errors
- Zero-pip method (symlink plugins without pip)
- venv vs pipx vs --break-system-packages tradeoffs
- Mnemosyne case study (successful zero-pip installation)

## Memory Provider Migration

When switching Hermes memory providers (built-in → external, or external → external):

See `references/memory-provider-migration.md` for:
- Built-in → external provider migration workflow
- Python migration script template
- Post-migration verification checklist
- Performance benchmarking
- Rollback plan
- Provider-specific notes (Mnemosyne, Mem0, Honcho, Zep)

**Mnemosyne-specific:** See `references/mnemosyne-installation-migration.md` for:
- Zero-pip installation method (Ubuntu 24.04 PEP 668 workaround)
- Built-in → Mnemosyne migration script (complete working example)
- Performance benchmarks (5.61ms average query, 500x faster than cloud)
- Verification checklist (5-step post-migration validation)
- Comparison table (built-in vs Mnemosyne, 8 metrics)
