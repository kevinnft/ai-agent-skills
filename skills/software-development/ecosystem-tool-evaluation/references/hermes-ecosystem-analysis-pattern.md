# Hermes Ecosystem Analysis Pattern

## Context

When user asks to analyze multiple GitHub repos from a curated list (e.g., tweet, blog post, awesome list), use this systematic approach to evaluate tools before recommending installation.

## Pattern: Deep Multi-Repo Analysis

### Phase 1: Batch Clone & Inspect

```bash
mkdir -p ~/analysis-workspace
cd ~/analysis-workspace

# Clone all repos in parallel (use subagent for efficiency)
for repo in repo1 repo2 repo3; do
  git clone https://github.com/owner/$repo &
done
wait
```

### Phase 2: Structured Analysis

For each repo, extract:

1. **Purpose** — What problem does it solve?
2. **Features** — Key capabilities (from README)
3. **Tech stack** — Languages, frameworks, dependencies
4. **Maturity** — Version, last commit, stars, issues
5. **Size** — Disk space (du -sh), estimated RAM usage
6. **Setup complexity** — Installation steps count, external dependencies
7. **Usefulness** — Does it solve user's actual problems?
8. **Performance impact** — RAM, CPU, disk, network
9. **Worth installing?** — Critical / Nice-to-have / Skip

### Phase 3: Comparison & Recommendation

Create structured outputs:

1. **Executive summary** (1 paragraph per repo)
2. **Comparison table** (all repos side-by-side)
3. **Categorized recommendations**:
   - ✅ Install now (critical, low cost)
   - 🟡 Install later (nice-to-have, defer until needed)
   - ❌ Skip (duplicate, experimental, high cost)
4. **Performance impact analysis** (before/after resource usage)
5. **Installation script** (for approved repos only)

### Phase 4: Visual Summary

Generate diagram showing:
- Repos by category (install now / later / skip)
- Resource requirements (disk, RAM)
- Use cases and benefits
- Decision rationale

## Example: Hermes Agent Ecosystem (10 repos)

**Input:** Tweet listing 10 Hermes-related GitHub repos

**Output:**
- `ANALYSIS_REPORT.md` (18KB) — Full detailed analysis
- `QUICK_SUMMARY.md` (5KB) — TL;DR version
- `COMPARISON_TABLE.md` (8.5KB) — Side-by-side comparison
- `install-recommended.sh` (3KB) — One-command installer
- Diagrams (PNG) — Visual decision guide

**Recommendation structure:**
```
Install Now (3 repos):
  1. Hermes-Wiki (1.1MB, 0 RAM) — Documentation
  2. hermes-ecosystem (62MB, 0 RAM) — Discovery tool
  3. hermes-hud (1.3MB, 50MB RAM) — Monitoring TUI

Install Later (3 repos):
  4. hermes-skill-factory (292KB) — Auto skill generation
  5. hermes-control-interface (33MB, 150MB RAM) — Web dashboard
  6. maestro (42MB, 50MB RAM) — Multi-agent coordination

Skip (4 repos):
  7. hermes-agent-camel — Research fork (duplicate)
  8. hermes-alpha — Bug bounty experiment (wrong deployment)
  9. NousResearch/hermes-agent — Already installed (core)
  10. awesome-hermes-agent — Already installed
```

## Key Principles

1. **Delegate to subagent** — Multi-repo analysis is time-consuming, use delegate_task
2. **Analyze before install** — Don't clone everything then explain complexity
3. **Consider user constraints** — VPS specs (RAM, disk), use case, skill level
4. **Provide actionable output** — Not just analysis, but clear install/skip decisions
5. **Include resource impact** — Show before/after memory/disk usage
6. **Respect user's explicit requests** — If they say "only X and Y", don't install Z

## Anti-Patterns

❌ **Installing without analysis**
```
User: "Analyze these 10 repos"
Agent: [installs all 10 repos]
Agent: "Here's what I installed..."
```

❌ **Generic recommendations**
```
"All repos are useful, install what you need"
→ User doesn't know what they need
```

❌ **Ignoring resource constraints**
```
User has 2GB RAM, 1220MB available
Agent recommends 5 tools totaling 500MB RAM
→ System will be under memory pressure
```

❌ **Installing more than requested**
```
User: "Install Wiki + Ecosystem only"
Agent: [installs Wiki + Ecosystem + HUD]
→ HUD consumes 50MB RAM user didn't want
```

## Success Criteria

✅ User gets clear install/skip decisions
✅ Resource impact is transparent (disk, RAM)
✅ Recommendations match user's constraints
✅ Installation script works (if provided)
✅ User can make informed decisions

## Tools Used

- `delegate_task` — Offload multi-repo analysis to subagent
- `git clone` — Batch clone repos
- `du -sh` — Measure disk usage
- `jq` — Parse JSON metadata (repos.json, package.json)
- `skill_manage` — Create analysis reports as skills (if reusable pattern)

## When to Use This Pattern

- User shares curated list of repos (tweet, blog, awesome list)
- User asks "which tools should I install?"
- User wants ecosystem overview before committing
- Multiple repos need evaluation (5+ repos)

## When NOT to Use

- User explicitly says "just install X" (specific tool)
- Single repo evaluation (use simpler analysis)
- User is experienced and knows what they want
