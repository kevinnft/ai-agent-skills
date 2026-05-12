# Hermes Ecosystem Analysis

**Last Updated:** 2026-05-03  
**Source:** hermesatlas.com (ksimback/hermes-ecosystem)  
**Total Repositories:** 84 (quality-filtered)

---

## Overview

The Hermes ecosystem contains 80+ third-party repositories across 12 categories. This analysis provides maturity ratings, relevance scores, and installation priorities for each category.

**Maturity Levels:**
- **Production** — Battle-tested, stable APIs, used in production
- **Beta** — Functional but evolving, breaking changes possible
- **Experimental** — Proof-of-concept, use with caution

**Relevance Scores (for typical Hermes user):**
- ⭐⭐⭐⭐⭐ Very High — Immediate value, low friction
- ⭐⭐⭐⭐ High — Significant benefit, moderate setup
- ⭐⭐⭐ Medium — Situational value, higher complexity
- ⭐⭐ Low — Niche use case
- ⭐ Very Low — Not relevant for most users

---

## Category Breakdown

### 1. Skills & Skill Registries (15 repos)

**Purpose:** Pre-made skill libraries and discovery platforms

**Top Picks:**

- **wondelai/skills** ⭐ 480 | Production | ⭐⭐⭐⭐⭐
  - 42 business/product/design skills (UX, marketing, code quality, architecture)
  - Based on industry frameworks (Clean Code, Lean Startup, Jobs to Be Done)
  - Cross-platform (Code Assistant + Hermes compatible)
  - Zero setup, load on-demand

- **mukul975/Cybersecurity-Skills** ⭐ 4,132 | Production | ⭐⭐⭐
  - 754 cybersecurity skills mapped to MITRE ATT&CK, NIST CSF 2.0
  - Security auditing, penetration testing, threat analysis
  - Niche but comprehensive for security work

- **conorbronsdon/avoid-ai-writing** ⭐ 759 | Production | ⭐⭐⭐⭐
  - Audit and rewrite content to avoid AI detection
  - Humanize AI-generated text, bypass AI detectors
  - Useful for content writing, documentation

- **chigwell/skilldock.io** ⭐ 50 | Production | ⭐⭐⭐⭐
  - Registry for browsing and discovering skills
  - Check before creating new skills (avoid duplication)

- **smartcontractkit/chainlink-agent-skills** ⭐ 85 | Beta | ⭐⭐
  - Blockchain oracle & smart contract interaction
  - Web3 development, smart contract testing
  - Niche (blockchain-specific)

---

### 2. Workspaces & GUIs (8 repos)

**Purpose:** Web interfaces for Hermes (chat, admin, development)

**Top Picks:**

- **nesquena/hermes-webui** ⭐ 2,479 | Production | ⭐⭐
  - Best chat interface (like ChatGPT)
  - Mobile-friendly, file upload, voice input
  - Redundant if using Telegram/Discord gateway

- **outsourc-e/hermes-workspace** ⭐ 830 | Beta | ⭐⭐⭐⭐
  - All-in-one dev environment (chat + terminal + memory + skills + inspector)
  - Ideal for skill development and debugging
  - Higher setup complexity

- **xaspx/hermes-control-interface** ⭐ 323 | Beta | ⭐⭐⭐⭐
  - Self-hosted admin dashboard
  - Browser-based terminal, file explorer, cron management, system metrics
  - Useful for remote management

- **EKKOLearnAI/hermes-web-ui** ⭐ 1,844 | Beta | ⭐⭐⭐
  - Enterprise dashboard (multi-platform, analytics, usage tracking)
  - Overkill for single user, good for teams

- **itq5/OpenClaw-Admin** ⭐ 669 | Beta | ⭐⭐⭐
  - Dual-gateway management (OpenClaw + Hermes)
  - Vue 3, bilingual (Chinese/English)
  - Only relevant if using both frameworks

---

### 3. Memory & Context (8 repos)

**Purpose:** Enhanced memory systems beyond built-in SQLite

**Top Picks:**

- **vectorize-io/hindsight** ⭐ 8,362 | Production | ⭐⭐⭐⭐⭐
  - State-of-the-art memory system (benchmark leader)
  - Retain/recall/reflect workflows
  - Complex monorepo, consider Hindsight Cloud (managed service)
  - Significant improvement over built-in memory

- **greyhaven-ai/autocontext** ⭐ 711 | Beta | ⭐⭐⭐⭐
  - Recursive self-improving context harness
  - Agents learn from experience, optimize over time
  - Good for long-term tasks, autonomous systems

- **hermes-lcm** ⭐ 178 | Beta | ⭐⭐⭐⭐
  - Lossless Context Management (DAG-based)
  - Perfect context retention, no message loss
  - Improves reliability for critical conversations

- **yoloshii/ClawMem** ⭐ 86 | Beta | ⭐⭐⭐
  - On-device memory engine (local-first, no cloud)
  - Privacy-focused, offline capability
  - Good for privacy-critical tasks

---

### 4. Plugins & Extensions (7 repos)

**Purpose:** Extend Hermes functionality

**Top Picks:**

- **robbyczgw-cla/hermes-web-search-plus** ⭐ 21 | Beta | ⭐⭐⭐⭐⭐
  - Multi-provider web search (Serper, Tavily, Exa, Querit, Perplexity)
  - Auto-routing and fallback
  - Significantly improves search reliability and quality

- **42-evey/hermes-plugins** ⭐ 16 | Beta | ⭐⭐⭐⭐
  - Multi-plugin suite (goal management, inter-agent bridge, model selection, cost control)
  - Productivity boost, cost optimization

- **prompt-security/clawshell** ⭐ 255 | Beta | ⭐⭐⭐
  - Runtime security layer (PII & credential protection)
  - Prevent sensitive data leaks
  - Good for production deployment

---

### 5. Multi-Agent & Orchestration (7 repos)

**Purpose:** Coordinate multiple agents

**Top Picks:**

- **builderz-labs/mission-control** ⭐ 3,875 | Beta | ⭐⭐⭐
  - Self-hosted agent orchestration (dispatch tasks, workflows, monitoring)
  - Good for complex multi-agent systems

- **swarmclawai/swarmclaw** ⭐ 285 | Beta | ⭐⭐⭐
  - Build autonomous agent swarms
  - Multi-agent collaboration, swarm intelligence
  - Advanced use case

---

### 6. Developer Tools & Utilities (9 repos)

**Purpose:** Development utilities, token trackers

**Top Picks:**

- **junhoyeo/tokscale** ⭐ 1,690 | Production | ⭐⭐⭐⭐⭐
  - Token usage tracker (Code Assistant, OpenClaw, Hermes, Codex)
  - Real-time cost monitoring, analytics by model/time
  - Zero config, auto-detects Hermes sessions
  - **Must-have for cost visibility**

- **joeynyc/hermes-skins** ⭐ 76 | Beta | ⭐⭐
  - Community CLI skins and themes
  - Cosmetic only

---

### 7. Deployment & Infrastructure (7 repos)

**Purpose:** VPS management, containers, reproducible builds

**Top Picks:**

- **1Panel-dev/1Panel** ⭐ 35,253 | Production | ⭐⭐⭐
  - Modern VPS control panel with native AI agent support
  - Native Hermes Agent support, Ollama integration
  - Good for self-hosting on VPS

- **numtide/llm-agents.nix** ⭐ 967 | Production | ⭐
  - Nix packages for AI agents (including Hermes)
  - Only relevant for NixOS users

- **TheAiSingularity/hermesclaw** ⭐ 16 | Experimental | ⭐⭐
  - Hermes sandboxed with hardware-level enforcement
  - Advanced security, experimental

---

### 8. Integrations & Bridges (6 repos)

**Purpose:** Connect Hermes to other platforms

**Top Picks:**

- **raulvidis/hermes-android** ⭐ 38 | Beta | ⭐⭐
  - Android device control (bridge app + Python toolset)
  - Mobile automation, device control
  - Niche use case

- **gizdusum/hermes-blockchain-oracle** ⭐ 3 | Experimental | ⭐⭐
  - Solana blockchain intelligence MCP server
  - On-chain analytics, wallet tracking
  - Very niche (blockchain-specific)

---

### 9. Domain Applications (10 repos)

**Purpose:** Specialized applications built on Hermes

**Top Picks:**

- **ucsandman/DashClaw** ⭐ 204 | Beta | ⭐⭐⭐
  - Decision infrastructure with guard policies and risk assessment
  - Safe decision-making, risk management
  - Good for high-stakes decisions

- **Christabel337/job-scout-agent** ⭐ 11 | Beta | ⭐
  - Autonomous job hunting (scan listings, write cover letters, track)
  - Very niche

- **bigph00t/hermescraft** ⭐ 8 | Beta | ⭐
  - Minecraft companion agent
  - Gaming only

---

### 10. Guides & Documentation (6 repos)

**Purpose:** Tutorials, best practices, learning resources

**Top Picks:**

- **0xNyk/awesome-hermes-agent** ⭐ 898 | Production | ⭐⭐⭐⭐⭐
  - Curated list of awesome resources
  - Quality-filtered, organized by category
  - **Essential reference for ecosystem discovery**

- **alchaincyf/hermes-agent-orange-book** ⭐ 315 | Beta | ⭐⭐
  - Practical guide (Chinese language)
  - Only relevant for Chinese speakers

---

### 11. Specialized Skills & Tools (3 repos)

**Purpose:** Task-specific tools

**Top Picks:**

- **Agents365-ai/drawio-skill** ⭐ 131 | Beta | ⭐⭐⭐⭐⭐
  - Generate draw.io diagrams from natural language
  - Architecture diagrams, flowcharts, UML
  - Requires draw.io desktop app
  - **High value for documentation and system design**

- **LetsFG/LetsFG** ⭐ 867 | Beta | ⭐⭐
  - Agent-native flight search & booking
  - 400+ airlines, price comparison
  - Niche (travel-specific)

---

### 12. Security & Optimization (2 repos)

**Purpose:** Security hardening, performance optimization

**Top Picks:**

- **prompt-security/clawsec** ⭐ 967 | Beta | ⭐⭐⭐
  - Complete security suite for AI agents
  - Protect SOUL.md, drift detection, automated audits
  - Good for production deployment

- **greyhaven-ai/autocontext** ⭐ 711 | Beta | ⭐⭐⭐⭐
  - (Also listed under Memory & Context)
  - Self-improving context harness

---

## Installation Priority Matrix

### Tier S — Must Explore (Immediate Value)

1. **tokscale** — Token usage tracking (zero setup)
2. **wondelai/skills** — 42 business/product/design skills (zero setup)
3. **awesome-hermes-agent** — Curated resource list (zero setup)
4. **drawio-skill** — Diagram generation (requires draw.io desktop)
5. **hermes-web-search-plus** — Better search (plugin install)

### Tier A — High Value (Worth Exploring)

6. **hindsight** — Enhanced memory (complex setup, consider cloud)
7. **hermes-workspace** — Dev environment (moderate setup)
8. **hermes-control-interface** — Admin dashboard (moderate setup)
9. **autocontext** — Self-improvement (moderate setup)
10. **hermes-plugins** — Productivity suite (plugin install)

### Tier B — Medium Value (Situational)

11. **hermes-lcm** — Lossless context (moderate setup)
12. **skilldock.io** — Skill registry (zero setup)
13. **clawshell** — Security layer (plugin install)
14. **DashClaw** — Decision infrastructure (moderate setup)
15. **ClawMem** — Privacy-focused memory (moderate setup)

### Tier C — Low Value (Niche)

16. **1Panel** — VPS management (only if self-hosting)
17. **mission-control** — Multi-agent orchestration (advanced)
18. **swarmclaw** — Agent swarms (advanced)
19. **avoid-ai-writing** — Humanize content (niche)
20. **Cybersecurity-Skills** — Security skills (niche)

---

## Common Installation Patterns

### Pattern 1: Zero-Setup Discovery

```bash
mkdir -p ~/.hermes/ecosystem
cd ~/.hermes/ecosystem

# Clone read-only repos
git clone --depth 1 https://github.com/wondelai/skills.git
git clone --depth 1 https://github.com/0xNyk/awesome-hermes-agent.git

# Browse
cat wondelai/skills/README.md
cat awesome-hermes-agent/README.md
```

### Pattern 2: CLI Tool Installation

```bash
# tokscale (npm global)
npm install -g tokscale

# Add alias
echo 'alias tokscale="/path/to/tokscale"' >> ~/.bashrc
source ~/.bashrc

# Test
tokscale models
```

### Pattern 3: Desktop App Dependency

```bash
# drawio-skill requires draw.io desktop
git clone --depth 1 https://github.com/Agents365-ai/drawio-skill.git ~/.hermes/ecosystem/drawio-skill

# Install draw.io
brew install --cask drawio  # macOS
# Or download from https://github.com/jgraph/drawio-desktop/releases

# Verify
draw.io --version
```

### Pattern 4: Plugin Installation

```bash
# hermes-web-search-plus (plugin)
git clone https://github.com/robbyczgw-cla/hermes-web-search-plus.git ~/.hermes/plugins/web-search-plus

# Configure in config.yaml
hermes config edit
# Add to plugins section

# Restart Hermes
hermes gateway restart  # or exit CLI and relaunch
```

### Pattern 5: Complex Service Setup

```bash
# hindsight (complex monorepo)
git clone https://github.com/vectorize-io/hindsight.git ~/.hermes/ecosystem/hindsight
cd ~/.hermes/ecosystem/hindsight

# Read docs first
cat README.md
cat hindsight-docs/docs/integration.md

# Consider Hindsight Cloud instead
# https://ui.hindsight.vectorize.io/signup
```

---

## Troubleshooting

### npm global install not in PATH

**Symptom:** `tokscale: command not found`

**Cause:** Hermes uses custom node install at `~/.hermes/node/`

**Fix:**
```bash
# Use full path
/home/user/.hermes/node/bin/tokscale --version

# Or add to PATH
export PATH="$HOME/.hermes/node/bin:$PATH"
echo 'export PATH="$HOME/.hermes/node/bin:$PATH"' >> ~/.bashrc
```

### draw.io not found

**Symptom:** `draw.io: command not found`

**Cause:** Desktop app not installed

**Fix:**
```bash
# macOS
brew install --cask drawio

# Linux
# Download .deb/.rpm from https://github.com/jgraph/drawio-desktop/releases
# Do NOT use snap (AppArmor sandbox issues)

# Verify
draw.io --version
```

### Skills not loading

**Symptom:** Skill file exists but doesn't load

**Cause:** Wrong directory structure or missing YAML frontmatter

**Fix:**
```bash
# Check structure
ls -la ~/.hermes/ecosystem/skills/clean-code/
# Should have: SKILL.md, references/ (optional)

# Check frontmatter
head -20 ~/.hermes/ecosystem/skills/clean-code/SKILL.md
# Should start with:
# ---
# name: clean-code
# description: '...'
# ---
```

### Token tracker shows 0 messages

**Symptom:** `tokscale clients` shows Hermes but 0 messages

**Cause:** Session DB not detected or not readable

**Fix:**
```bash
# Check DB exists
ls -lh ~/.hermes/state.db

# Check permissions
chmod 644 ~/.hermes/state.db

# Restart tokscale scan
tokscale clients
```

---

## Maintenance

### Update all ecosystem repos

```bash
cd ~/.hermes/ecosystem
for repo in */; do
  echo "Updating $repo..."
  git -C "$repo" pull --ff-only
done
```

### Check for new skills

```bash
cd ~/.hermes/ecosystem/skills
git pull
ls -d */
```

### Monitor token usage

```bash
# Daily check
tokscale models

# Weekly check
tokscale monthly

# Export for analysis
tokscale models --json > ~/token-usage-$(date +%Y%m%d).json
```

---

## Further Reading

- **hermesatlas.com** — Official ecosystem catalog
- **awesome-hermes-agent** — Curated resource list
- **Hermes docs** — https://hermes-agent.nousresearch.com/docs/
- **Skills catalog** — https://hermes-agent.nousresearch.com/docs/reference/skills-catalog
