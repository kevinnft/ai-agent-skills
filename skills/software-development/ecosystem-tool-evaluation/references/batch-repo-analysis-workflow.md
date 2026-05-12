# Batch Repository Analysis Workflow

When analyzing 5+ repos from a curated list (tweet, blog post, awesome list), use this systematic approach.

## Context

**Scenario:** User shares a tweet/post with 10 GitHub repos and asks "analisa ini" or "which ones are useful?"

**Goal:** Provide comprehensive analysis with actionable recommendations, not just a list of features.

## Workflow

### Phase 1: Extract Repo List

```bash
# From tweet API or manual extraction
repos=(
  "owner1/repo1"
  "owner2/repo2"
  # ... more repos
)
```

### Phase 2: Clone All Repos

```bash
mkdir analysis-workspace
cd analysis-workspace

for repo in "${repos[@]}"; do
  git clone "https://github.com/$repo"
done
```

**Why clone all first:**
- Parallel analysis possible
- Offline inspection
- Can grep across all repos

### Phase 3: Analyze Each Repo

For each repo, extract:

**1. Basic Info**
```bash
# Size
du -sh repo-name/

# README
cat repo-name/README.md | head -50

# Structure
tree -L 2 repo-name/

# Tech stack
ls repo-name/ | grep -E '(package.json|requirements.txt|Cargo.toml|go.mod)'
```

**2. Maturity Indicators**
- Stars (from GitHub API or README)
- Last commit date: `git log -1 --format=%cd`
- Release tags: `git tag | tail -5`
- CI/CD: `.github/workflows/`, `.gitlab-ci.yml`
- Tests: `tests/`, `__tests__/`, `*.test.*`

**3. Installation Complexity**
- Dependencies count
- External services required (Docker, DB, API keys)
- Setup steps in README
- Configuration files needed

**4. Resource Impact**
- Disk: `du -sh`
- RAM: Check if daemon/service (estimate from docs)
- CPU: Check if background process

**5. Usefulness for User**
- Does it solve user's problem?
- Does it duplicate existing tools?
- Is it worth the setup effort?

### Phase 4: Create Comparison Table

**Format:**

| Repo | Size | RAM | Maturity | Complexity | Usefulness | Decision |
|------|------|-----|----------|------------|------------|----------|
| repo1 | 1MB | 0 | Production | Low | High | ✅ Install |
| repo2 | 50MB | 150MB | Beta | High | Medium | 🟡 Defer |
| repo3 | 100MB | 0 | Alpha | High | Low | ❌ Skip |

### Phase 5: Write Analysis Report

**Structure:**

```markdown
# [Ecosystem] Analysis Report

## Executive Summary
- Total repos analyzed: X
- Recommend install: Y
- Defer: Z
- Skip: W

## Detailed Analysis

### 1. [Repo Name]
**Status:** ✅ Install / 🟡 Defer / ❌ Skip
**Size:** X MB (disk), Y MB (RAM)
**Maturity:** Production/Beta/Alpha

**What it is:**
[1-2 sentence description]

**Why install/defer/skip:**
[Specific reasons based on user's context]

**Installation:**
```bash
[exact commands]
```

[Repeat for each repo]

## Performance Impact

### Current State
- Memory: X MB used, Y MB available
- Disk: X GB used, Y GB free

### After Phase 1 (Install Now)
- Disk: +X MB
- RAM: +Y MB
- Available: Z MB (still comfortable)

### After Phase 2 (Install Later)
- Disk: +X MB
- RAM: +Y MB
- Available: Z MB (monitor if add more)

## Recommendations

1. Install now: [list with reasons]
2. Install later: [list with conditions]
3. Skip: [list with reasons]
```

### Phase 6: Generate Diagrams

**Visual summary:**
- Comparison chart (all repos)
- Resource impact (before/after)
- Decision matrix (install/defer/skip)

Use draw.io or similar for visual clarity.

### Phase 7: Create Install Script

**For "install now" repos:**

```bash
#!/bin/bash
# install-recommended.sh

echo "Installing critical repos..."

# Repo 1
git clone https://github.com/owner/repo1 ~/.target/repo1
cd ~/.target/repo1
./install.sh

# Repo 2
git clone https://github.com/owner/repo2 ~/.target/repo2
# ... setup steps

echo "✅ Installation complete!"
```

**IMPORTANT:** Verify script installs ONLY what user requested, not extras.

## User Context Considerations

### For RAM-Conscious Users

**Indicators:**
- VPS with limited RAM (< 4GB)
- User mentions "yang gak makan RAM" or "lightweight"
- User removes tools that consume RAM

**Adjust recommendations:**
- Prioritize 0 RAM tools (static docs, CLI tools)
- Flag RAM-consuming tools clearly
- Offer alternatives (TUI vs web dashboard)

**Example:**
```
❌ hermes-control-interface (150MB RAM)
   → Too heavy for 2GB VPS
   
✅ hermes-hud (50MB RAM)
   → Lightweight alternative
```

### For Disk-Conscious Users

**Indicators:**
- VPS with limited disk (< 40GB)
- User asks about disk usage
- User cleans up regularly

**Adjust recommendations:**
- Show disk impact clearly
- Suggest cleanup after analysis
- Prioritize small tools

### For Performance-Conscious Users

**Indicators:**
- User asks "apakah ningkatin performa?"
- User wants optimization
- User tracks metrics

**Adjust recommendations:**
- Explain direct vs indirect benefits
- Quantify improvements when possible
- Prioritize tools with measurable impact

## Pitfalls

### 1. Installing More Than Requested

**Problem:** User asks for specific repos, script installs extras.

**Example:**
```
User: "Install Wiki + Ecosystem only"
Script: Installs Wiki + Ecosystem + HUD
User: "saya kan gak suruh install ini yg memakan ram"
```

**Fix:**
- Read user request carefully
- Verify script contents before running
- When user lists specific tools, install ONLY those
- Resource-consuming tools need explicit consent

### 2. Not Considering User's VPS Constraints

**Problem:** Recommend tools without checking available resources.

**Example:**
```
Recommend: 5 tools totaling 500MB RAM
User VPS: 2GB RAM, 1.2GB available
Result: System becomes slow
```

**Fix:**
- Check current resource usage first
- Calculate cumulative impact
- Recommend in phases (critical → nice-to-have)

### 3. Generic Analysis Without Context

**Problem:** List features without explaining relevance to user.

**Example:**
```
❌ "hermes-hud has 9 tabs and 4 themes"
   → User doesn't know if they need it
```

**Fix:**
```
✅ "hermes-hud shows memory usage, skill growth, session history
   → Useful for debugging memory issues you mentioned
   → 50MB RAM (acceptable for your 2GB VPS)"
```

### 4. Not Delegating Large Analysis

**Problem:** Analyze 10+ repos in main context, consume token budget.

**Solution:**
- Use delegate_task for analysis (preserve main context)
- Subagent does deep dive, returns summary
- Main agent presents results to user

## Delegation Pattern

**When to delegate:**
- 5+ repos to analyze
- Deep investigation needed (clone, inspect, test)
- Want to preserve main context for interaction

**How to delegate:**

```python
delegate_task(
    goal="Analyze 10 Hermes repos, create comparison table + recommendations",
    context="User has 2GB RAM VPS, wants lightweight tools",
    toolsets=["terminal", "file", "web"]
)
```

**Subagent deliverables:**
- ANALYSIS_REPORT.md (full details)
- QUICK_SUMMARY.md (TL;DR)
- COMPARISON_TABLE.md (side-by-side)
- install-recommended.sh (one-command install)

**Main agent role:**
- Present summary to user
- Answer questions
- Execute installation if approved

## Success Criteria

- ✅ All repos analyzed (not just listed)
- ✅ Clear recommendations (install/defer/skip with reasons)
- ✅ Resource impact calculated (disk, RAM)
- ✅ User context considered (VPS constraints, preferences)
- ✅ Actionable output (install script, commands)
- ✅ Visual summary (diagrams, tables)

## Example Output Structure

```
/home/ubuntu/analysis-workspace/
├─ repo1/                    # Cloned repos
├─ repo2/
├─ ...
├─ ANALYSIS_REPORT.md        # Full analysis (18KB)
├─ QUICK_SUMMARY.md          # TL;DR (5KB)
├─ COMPARISON_TABLE.md       # Side-by-side (8KB)
└─ install-recommended.sh    # One-command install (3KB)
```

## Time Estimates

| Repos | Analysis Time | Report Writing | Total |
|-------|---------------|----------------|-------|
| 5 repos | 10-15 min | 5-10 min | 15-25 min |
| 10 repos | 20-30 min | 10-15 min | 30-45 min |
| 20 repos | 40-60 min | 20-30 min | 60-90 min |

**Optimization:** Use subagent for 10+ repos to parallelize work.
