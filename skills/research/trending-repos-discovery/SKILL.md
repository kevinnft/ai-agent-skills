---
name: trending-repos-discovery
description: Discover and analyze trending GitHub repositories from TrendShift and other sources — evaluate usefulness, extract learnings, and identify valuable skills/tools
tags: [github, trending, research, discovery, skills]
related_skills: [github-repo-management, ecosystem-tool-evaluation]
origin: unknown
source_license: see upstream
language: en
---

# Trending Repos Discovery

Discover and analyze trending GitHub repositories from TrendShift and other sources. Evaluate usefulness, extract learnings, and identify valuable skills/tools for adoption.

## When to Use

- User asks "apa yang trending?" or "what's trending?"
- User wants to discover new tools/libraries
- User asks about specific trending repo
- Looking for inspiration or best practices
- Evaluating whether to adopt new tools

## Sources

### 1. TrendShift (Primary)

**URL:** https://trendshift.io/

**What it tracks:**
- GitHub's most-discussed open-source projects
- Daily engagement rankings
- Real-time mentions from X/Twitter
- Discussions from Reddit and Hacker News

**How to fetch:** See `references/trendshift-fetch-methods.md` for TinyFish and GitHub API examples

### 2. GitHub Trending (Alternative)

**URL:** https://github.com/trending

**Languages:**
- All languages: https://github.com/trending
- Python: https://github.com/trending/python
- TypeScript: https://github.com/trending/typescript
- Rust: https://github.com/trending/rust

### 3. GitHub API (For Details)

See `references/trendshift-fetch-methods.md` for API usage examples.

**Rate limit:** 60 requests/hour (unauthenticated), 5000/hour (authenticated)

## Analysis Workflow

### Phase 1: Fetch Trending List

1. **Fetch from TrendShift** (primary source)
2. **Extract repo names** (owner/repo format)
3. **Get first 10-20 repos** (manageable batch)

### Phase 2: Get Repo Details

For each repo, fetch from GitHub API:
- Stars, forks, watchers
- Description
- Language
- Topics
- Created/updated dates

**Batch strategy:**
- Fetch 10 repos at a time
- If rate limited, wait or use cached data

### Phase 3: Categorize by Usefulness

For each repo, assess:

#### A. Relevance Score

| Factor | Weight | Criteria |
|--------|--------|----------|
| **Stars** | 30% | > 10K = high, 1K-10K = medium, < 1K = low |
| **Description match** | 30% | Keywords match user's interests |
| **Language** | 20% | User's tech stack (Python, TypeScript, Rust) |
| **Recency** | 10% | Updated in last 30 days |
| **Topics** | 10% | Relevant tags (ai, agent, skills, tools) |

#### B. Usefulness Categories

**✅ Highly Useful:**
- Directly applicable to user's projects
- Solves current problems
- Fills gaps in toolset
- High stars (> 10K) + active development

**🟡 Potentially Useful:**
- Interesting but not immediate need
- Requires evaluation/testing
- Medium stars (1K-10K)
- Niche use case

**❌ Not Useful:**
- Wrong tech stack (e.g., Mac-only for Linux user)
- Too niche (e.g., biology tools for software dev)
- Duplicate of existing tools
- Low stars (< 1K) + no clear value

### Phase 4: Extract Learnings

For useful repos, identify:

#### 1. Skills/Patterns
- What skills does it provide?
- What patterns does it use?
- What best practices does it demonstrate?

**Example (obra/superpowers):**
- Skills framework architecture
- Agentic workflow patterns
- Production-ready methodology

#### 2. Tools/Libraries
- What tools does it introduce?
- What dependencies does it use?
- What integrations does it support?

**Example (addyosmani/agent-skills):**
- Production-grade engineering patterns
- Web performance optimization
- Chrome DevTools expertise

#### 3. Concepts/Ideas
- What problems does it solve?
- What approaches does it take?
- What innovations does it introduce?

**Example (andrej-karpathy-skills):**
- LLM coding pitfalls
- AI code quality patterns
- Production AI best practices

### Phase 5: Present Analysis

**Format:**

```markdown
## 🔥 TOP TRENDING REPOS

### 1. owner/repo ⭐ X,XXX stars 🏆

**Description:** [One-line description]

**Berguna?** ✅ SANGAT / 🟡 MUNGKIN / ❌ TIDAK

**Why:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Use Case:** [How user can use it]

**Action:** [What to do next]

---

## 🎯 RECOMMENDED ACTIONS

### Priority 1: MUST CHECK 🔥
1. [Repo 1] - [Why]
2. [Repo 2] - [Why]

### Priority 2: WORTH CHECKING ✅
3. [Repo 3] - [Why]

### Priority 3: MAYBE ⚠️
5. [Repo 5] - [Why]

## ❌ SKIP THESE
- [Repo X] - [Why not useful]
```

## User Preference Patterns

### For "Analisa trending repos"

When user asks to analyze trending repos:

**DO:**
- ✅ Fetch from TrendShift (most comprehensive)
- ✅ Get details for top 10-20 repos
- ✅ Categorize by usefulness (✅ 🟡 ❌)
- ✅ Explain WHY each is useful/not useful
- ✅ Provide actionable recommendations
- ✅ Group by priority (must check, worth checking, maybe, skip)

**DON'T:**
- ❌ Just list repo names (no value)
- ❌ Skip usefulness assessment
- ❌ Recommend everything (no filtering)
- ❌ Ignore user's tech stack/constraints

### For "Ada yang berguna gak?"

When user asks if trending repos are useful:

**Response pattern:**
1. **Quick verdict:** "ADA YANG BERGUNA? ✅ BANYAK!" or "❌ TIDAK ADA"
2. **Top picks:** List 3-5 most useful repos
3. **Why useful:** Explain specific benefits
4. **Action:** What to do next (clone, study, adapt)

**Example:**
```
✅ ADA YANG MENARIK — review dulu sebelum klaim apapun

1. obra/superpowers — Skills framework
2. andrej-karpathy-skills — coding guidelines
3. mattpocock/skills — TypeScript / engineering workflows
4. addyosmani/agent-skills — frontend & performance practices

Mention star counts only when reporting raw findings; do not aggregate
them into "X K combined stars" or claim authors as contributors to a
downstream repo. Authors of upstream public skill repos have not endorsed
or contributed to any aggregator unless they explicitly say so.

MAU GUE CLONE & ANALISA SEKARANG? 🚀
```

## Evaluation Criteria

### For Skills Repos

**Look for:**
- ✅ SKILL.md or .claude directory (skills format)
- ✅ High stars (> 10K = trusted)
- ✅ Industry expert author (Karpathy, Pocock, Osmani)
- ✅ Production-tested (not toy examples)
- ✅ Applicable to user's work (coding, AI, web dev)

**Red flags:**
- ❌ Low stars (< 1K) + unknown author
- ❌ Toy examples only
- ❌ Outdated (not updated in 6+ months)
- ❌ Wrong tech stack (e.g., Java for Python user)

### For Tools/Libraries

**Look for:**
- ✅ Solves real problem
- ✅ Active development (commits in last 30 days)
- ✅ Good documentation (README, examples)
- ✅ Compatible with user's stack
- ✅ **Resource cost acceptable** (< 500 MB disk, < 100 MB RAM for VPS users)

**Red flags:**
- ❌ Heavy resource usage (> 500 MB disk, > 100 MB RAM)
- ❌ Platform-specific (Mac-only for Linux user)
- ❌ Duplicate of existing tools
- ❌ Poor documentation

### For Frameworks

**Look for:**
- ✅ Clear architecture
- ✅ Best practices demonstrated
- ✅ Production-ready
- ✅ Extensible/adaptable
- ✅ Good examples

**Red flags:**
- ❌ Over-engineered
- ❌ Too opinionated
- ❌ Hard to adapt
- ❌ No examples

## Common Patterns

### Skills Repos (High Value)

**Pattern:**
- Name: `*-skills`, `skills`, `agent-skills`
- Format: SKILL.md, .claude directory, or markdown files
- Author: Industry experts (Karpathy, Pocock, Osmani)
- Stars: > 10K
- Content: Production-tested patterns, best practices

**Examples:**
- obra/superpowers (186K stars) - Skills framework
- forrestchang/andrej-karpathy-skills (125K stars) - Coding quality
- mattpocock/skills (73K stars) - TypeScript mastery
- addyosmani/agent-skills (39K stars) - Performance

**Action:**
1. Clone repo
2. Study SKILL.md files
3. Identify useful patterns
4. Adapt to Hermes skills
5. Test in projects

### Tool Repos (Medium Value)

**Pattern:**
- Name: Tool/library name
- Format: Python package, npm package, CLI tool
- Stars: 1K-10K
- Content: Specific functionality

**Examples:**
- antirez/ds4 (7.5K stars) - DeepSeek inference (Mac-only)
- huangserva/3DCellForge (1.5K stars) - 3D cell generation (niche)

**Action:**
1. Check resource cost (disk, RAM)
2. Check compatibility (OS, dependencies)
3. Evaluate usefulness (solves problem?)
4. If useful + lightweight → install
5. If heavy → find alternative

### Framework Repos (High Value if Applicable)

**Pattern:**
- Name: Framework name
- Format: Full project structure
- Stars: > 10K
- Content: Architecture, patterns, examples

**Examples:**
- github/spec-kit (96K stars) - Spec-Driven Development

**Action:**
1. Study architecture
2. Understand patterns
3. Evaluate applicability
4. Adapt concepts (not full framework)
5. Document learnings

## Pitfalls

### 1. Recommending Everything

**Problem:** User asks "ada yang berguna?", you list all 20 repos.

**Solution:**
- Filter by usefulness (✅ 🟡 ❌)
- Recommend top 3-5 only
- Group by priority
- Explain why each is useful

### 2. Ignoring Resource Constraints

**Problem:** Recommend heavy tool (> 500 MB) for VPS user.

**Solution:**
- **ALWAYS check resource cost first**
- If heavy → find lightweight alternative
- If no alternative → skip
- See `vps-cleanup` skill for thresholds

### 3. Not Explaining Why

**Problem:** List repos without explaining usefulness.

**Solution:**
- Always explain WHY useful
- Specific benefits (not generic "good tool")
- How user can use it
- What problem it solves

### 4. Recommending Wrong Tech Stack

**Problem:** Recommend Mac-only tool for Linux user.

**Solution:**
- Check compatibility (OS, dependencies)
- Check user's tech stack (Python, TypeScript, Rust)
- Skip incompatible tools
- Mention incompatibility in analysis

### 5. Not Providing Next Steps

**Problem:** User says "mantap" but doesn't know what to do.

**Solution:**
- Always end with action items
- "MAU GUE CLONE & ANALISA SEKARANG?" (Want me to clone & analyze now?)
- Specific commands (git clone, study, adapt)
- Clear next steps

## Examples

See `references/top-4-skills-repos-case-study.md` for detailed example from session 2026-05-12.

## References

- TrendShift: https://trendshift.io/
- GitHub Trending: https://github.com/trending
- GitHub API: https://docs.github.com/en/rest
- Fetch methods: `references/trendshift-fetch-methods.md`
- Case study: `references/top-4-skills-repos-case-study.md`
