# AI Agent Skills 🚀

> **189 production-ready skills for AI coding agents** — curated from industry experts (Andrej Karpathy, Matt Pocock, Addy Osmani, obra)

[![Skills](https://img.shields.io/badge/skills-189-blue)](#categories)
[![Categories](https://img.shields.io/badge/categories-26-green)](#categories)
[![Quality](https://img.shields.io/badge/quality-86%25%20good-green)](#automation-tools)
[![License](https://img.shields.io/badge/license-MIT-orange)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![CI](https://github.com/kevinnft/ai-agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/kevinnft/ai-agent-skills/actions/workflows/ci.yml)

---

## 🌟 Highlights

- **189 Skills** across 26 populated categories (31 skill directories)
- **4 Automation Tools** for repository management, quality monitoring, and skills distribution
- **Industry Experts**: Andrej Karpathy (ex-Tesla AI), Matt Pocock (TypeScript educator), Addy Osmani (Google Chrome), obra (Superpowers)
- **Production-Tested**: Battle-tested in real projects
- **Comprehensive Coverage**: Engineering, DevOps, MLOps, Creative, Research, GitHub
- **Auto-Install**: One-command installation for Hermes Agent
- **REST API**: Browse and install skills via API
- **Zero Dependencies**: Pure markdown skills, no external dependencies

---

## 🛠️ Automation Tools

This repository includes **4 production-ready automation tools**:

### ⚡ Release Automation
Auto-generate changelog, semantic versioning, GitHub releases
```bash
./scripts/release.py --patch    # 1.4.0 → 1.4.1
```
[📚 Documentation](docs/release-automation.md)

### 📊 Quality Dashboard
Real-time repository health monitoring with quality scores
```bash
./scripts/quality-dashboard.py
```
**Current Score:** 86/100 (Good) | [📚 Documentation](docs/quality-dashboard.md)

### 🏷️ Auto-Label Bot
Automatic PR/Issue labeling via GitHub Actions (35 labels, 6 categories)
- ✅ Active workflow
- ✅ Instant labeling (2 seconds)
- ✅ Zero cost, zero maintenance

[📚 Documentation](docs/auto-label-bot.md)

### 🛠️ Skills Manager API
Lightweight REST API for browsing and installing skills
```bash
./scripts/skills-api.py --port 5555
```
**API:** 189 skills, 26 populated categories | [📚 Documentation](docs/skills-api.md)

[📖 View All Tools](docs/AUTOMATION.md)

---

## 📦 Quick Start

### For Hermes Agent

```bash
# Clone repository
git clone https://github.com/kevinnft/ai-agent-skills.git
cd ai-agent-skills

# Install all skills
./scripts/install.sh

# Or install specific category
./scripts/install.sh --category addyosmani
./scripts/install.sh --category mattpocock
./scripts/install.sh --category superpowers
```

### For Other AI Agents

Skills are pure markdown with YAML frontmatter. Copy the `skills/` directory to your agent's skills folder.

**Claude Code:**
```bash
cp -r skills/* ~/.claude/skills/
```

**Cursor:**
```bash
cp -r skills/* ~/.cursor/skills/
```

**Custom Agent:**
```bash
cp -r skills/* /path/to/your/agent/skills/
```

---

## 🎯 Categories

### 🏆 Engineering (66 skills)

#### **addyosmani** (22 skills) — Production Engineering
- `code-review-and-quality` — Multi-axis code review
- `performance-optimization` — Web performance best practices
- `security-and-hardening` — Vulnerability prevention
- `spec-driven-development` — Specs before code
- `test-driven-development` — TDD workflow
- `incremental-implementation` — Incremental delivery
- `debugging-and-error-recovery` — Systematic debugging
- `api-and-interface-design` — Stable API design
- `frontend-ui-engineering` — Production-quality UIs
- `ci-cd-and-automation` — CI/CD pipeline setup
- `git-workflow-and-versioning` — Git best practices
- `documentation-and-adrs` — Decision records
- `shipping-and-launch` — Production launches
- `planning-and-task-breakdown` — Task decomposition
- `code-simplification` — Simplify code
- `context-engineering` — Agent context optimization
- `deprecation-and-migration` — Deprecation management
- `doubt-driven-development` — Adversarial review
- `browser-testing-with-devtools` — Browser testing
- `idea-refine` — Idea refinement
- `source-driven-development` — Source-driven patterns
- `using-agent-skills` — Meta-skill for skill discovery

#### **mattpocock** (28 skills) — TypeScript & Workflows
- `tdd` — Test-driven development
- `diagnose` — Systematic debugging
- `review` — Code review
- `prototype` — Throwaway prototypes
- `grill-me` — Stress-test plans
- `caveman` — Ultra-compressed communication
- `design-an-interface` — Multiple interface designs
- `edit-article` — Article editing
- `git-guardrails-claude-code` — Git safety hooks
- `handoff` — Context handoff
- `improve-codebase-architecture` — Architecture improvements
- `obsidian-vault` — Note management
- `qa` — Interactive QA session
- `request-refactor-plan` — Refactor planning
- `scaffold-exercises` — Exercise scaffolding
- `setup-matt-pocock-skills` — Setup
- `setup-pre-commit` — Pre-commit hooks
- `to-issues` — Plan → issues
- `to-prd` — Context → PRD
- `triage` — Issue workflow
- `ubiquitous-language` — DDD glossary
- `write-a-skill` — Skill creation
- `writing-beats` — Article beats
- `writing-fragments` — Writing fragments
- `writing-shape` — Shape articles
- `zoom-out` — Broader context
- `migrate-to-shoehorn` — Type assertion migration
- `grill-with-docs` — Grilling with docs

#### **superpowers** (14 skills) — Agentic Workflows
- `brainstorming` — Before creative work (MUST USE)
- `verification-before-completion` — Verify before claiming done
- `test-driven-development` — TDD with red-green-refactor
- `executing-plans` — Execute with review checkpoints
- `writing-skills` — Create new skills
- `finishing-a-development-branch` — Complete work
- `receiving-code-review` — Handle feedback
- `using-git-worktrees` — Isolated workspaces
- `using-superpowers` — Meta-skill
- `dispatching-parallel-agents` — Parallel tasks
- `requesting-code-review` — Pre-commit review
- `subagent-driven-development` — Subagent execution
- `systematic-debugging` — 4-phase debugging
- `writing-plans` — Implementation plans

#### **software-development** (16 skills)
- `api-testing` — REST/GraphQL API testing ⭐ NEW
- `systematic-debugging` — Root cause debugging
- `test-driven-development` — TDD enforcement
- `open-source-contribution` — OSS workflow
- `hermes-agent-skill-authoring` — Skill creation
- `plan` — Plan mode
- `debugging-hermes-tui-commands` — Hermes TUI debugging
- `ecosystem-tool-evaluation` — Tool evaluation
- `node-inspect-debugger` — Node.js debugging
- `python-debugpy` — Python debugging
- `requesting-code-review` — Pre-commit review
- `spike` — Throwaway experiments
- `subagent-driven-development` — Subagent execution
- `user-ryzen-preferences` — User preferences
- `writing-plans` — Implementation plans
- `contributing-to-ide-projects` — IDE contribution

---

### 🎨 Creative (22 skills)

Visual content generation, diagrams, and design tools:

- `architecture-diagram` — Dark-themed SVG diagrams
- `ascii-art` — ASCII art generation
- `ascii-video` — ASCII video conversion
- `drawio-headless` — Draw.io diagrams (headless)
- `excalidraw` — Hand-drawn diagrams
- `pixel-art` — Pixel art with era palettes
- `manim-video` — 3Blue1Brown-style animations
- `p5js` — Generative art sketches
- `claude-design` — HTML artifacts
- `sketch` — Throwaway HTML mockups
- `humanizer` — Humanize AI text
- `ideation` — Project idea generation
- `baoyu-comic` — Knowledge comics
- `baoyu-infographic` — Infographics
- `design-md` — Google DESIGN.md tokens
- `popular-web-designs` — 54 design systems
- `pretext` — DOM-free text layout
- `social-media-slideshow-video` — Slideshow videos
- `songwriting-and-ai-music` — Suno AI music
- `touchdesigner-mcp` — TouchDesigner control
- `visual-assets-generation` — Visual assets
- `comfyui` — ComfyUI image/video/audio

---

### 🤖 MLOps (15 skills)

Machine learning operations and AI workflows:

- `llama-cpp` — Local GGUF inference
- `axolotl` — YAML LLM fine-tuning
- `unsloth` — Fast LoRA training
- `serving-llms-vllm` — High-throughput serving
- `huggingface-hub` — Model management
- `fine-tuning-with-trl` — RLHF training
- `dspy` — Declarative LM programs
- `evaluating-llms-harness` — LLM benchmarking
- `weights-and-biases` — Experiment tracking
- `outlines` — Structured generation
- `obliteratus` — Abliterate refusals
- `segment-anything-model` — Image segmentation
- `audiocraft-audio-generation` — Music/sound generation
- `crypto-mining-setup` — AI-powered mining
- `windows-local-ai-services` — Windows AI services

---

### 🔧 DevOps (9 skills)

Infrastructure, deployment, and operations:

- `docker-compose` — Multi-container orchestration ⭐ NEW
- `vps-cleanup` — Systematic VPS cleanup
- `vps-security-hardening` — Security hardening
- `cloud-browser-automation` — Browserbase integration
- `tinyfish-integration` — Web toolkit
- `api-monitoring-bots` — Monitoring bots
- `kanban-orchestrator` — Kanban orchestration
- `kanban-worker` — Kanban worker patterns
- `webhook-subscriptions` — Event-driven runs

---

### 🐙 GitHub (10 skills)

GitHub workflows and repository management:

- `github-pr-workflow` — PR lifecycle
- `github-code-review` — Code review
- `public-repo-creation` — Production-ready repos
- `comprehensive-public-repo-setup` — Full repo setup
- `github-repo-visual-assets` — Visual assets
- `repo-quality-maksimalisasi` — Quality maximization
- `github-auth` — Authentication setup
- `github-issues` — Issue management
- `github-repo-management` — Repo operations
- `codebase-inspection` — Codebase analysis

---

### 🔬 Research (11 skills)

Research, analysis, and data extraction:

- `web-scraping` — Data extraction
- `arxiv` — Paper search
- `credential-pooling-analysis` — Business analysis
- `telegram-bot-security-analysis` — Security testing
- `crypto-token-analysis` — Token analysis
- `nft-analysis` — NFT project analysis
- `trending-repos-discovery` — Trending repos
- `blogwatcher` — RSS/Atom monitoring
- `llm-wiki` — Interlinked markdown KB
- `polymarket` — Polymarket queries
- `research-paper-writing` — ML paper writing

---

### 📝 Productivity (8 skills)

Productivity tools and integrations:

- `notion` — Notion API
- `google-workspace` — Gmail, Drive, Docs
- `linear` — Issue management
- `airtable` — Database API
- `powerpoint` — .pptx creation
- `ocr-and-documents` — PDF text extraction
- `nano-pdf` — PDF editing
- `maps` — Geocoding, routes

---

### 🎮 Other Categories

- **autonomous-ai-agents** (4 skills): claude-code, codex, hermes-agent, opencode
- **note-taking** (2 skills): obsidian, obsidian-mobile-sync
- **obsidian-skills** (5 skills): defuddle, json-canvas, obsidian-bases, obsidian-cli, obsidian-markdown
- **media** (5 skills): gif-search, heartmula, songsee, spotify, youtube-content
- **gaming** (2 skills): minecraft-modpack-server, pokemon-player
- **social-media** (2 skills): social-media-account-audit, xurl
- **smart-home** (1 skill): openhue
- **email** (1 skill): himalaya
- **mcp** (1 skill): native-mcp
- **red-teaming** (1 skill): godmode
- **data-science** (1 skill): jupyter-live-kernel
- **patent-disclosure-skill** (1 skill): patent-disclosure-skill
- **software-copyright** (2 skills): software-copyright-materials, docx-toolkit
- **prism** (5 skills): prism-3way, prism-discover, prism-full, prism-reflect, prism-scan
- **dogfood** (1 skill): dogfood
- **yuanbao** (1 skill): yuanbao

[See full category list →](./docs/categories.md)

---

## 🏆 Featured Skills

### From Andrej Karpathy (ex-Tesla AI Director)

**CLAUDE.md** — Behavioral guidelines to reduce common LLM coding mistakes

Key principles:
1. **Think Before Coding** — Don't assume, surface tradeoffs
2. **Simplicity First** — Minimum code, no speculation
3. **Surgical Changes** — Touch only what you must
4. **Goal-Driven Execution** — Define success criteria, loop until verified

Source: [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (125K ⭐)

---

### From Matt Pocock (TypeScript Educator)

**TDD** — Test-driven development with red-green-refactor loop
- Write failing test first
- Make it pass with minimal code
- Refactor while keeping tests green

**Diagnose** — Systematic debugging for hard bugs
- Reproduce → minimize → hypothesize → instrument → fix → regression-test

**Review** — Multi-axis code review
- Standards: Does code follow repo conventions?
- Spec: Does code match requirements?

Source: [mattpocock/skills](https://github.com/mattpocock/skills) (73K ⭐)

---

### From Addy Osmani (Google Chrome Team)

**Code Review & Quality** — Production-grade multi-axis review
- Correctness, security, performance, maintainability

**Performance Optimization** — Web performance best practices
- Core Web Vitals, bundle optimization, lazy loading

**Security & Hardening** — Vulnerability prevention
- Input validation, auth/authz, secure patterns

Source: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (39K ⭐)

---

### From obra (Superpowers Framework)

**Brainstorming** — MUST USE before any creative work
- Explores user intent, requirements, design before implementation

**Verification Before Completion** — Verify before claiming done
- Run verification commands, confirm output, evidence before assertions

**Executing Plans** — Execute with review checkpoints
- Written plan → separate session → review at checkpoints

Source: [obra/superpowers](https://github.com/obra/superpowers) (186K ⭐)

---

## 📚 Documentation

### Skills Documentation
- [Installation Guide](./docs/installation.md)
- [Usage Examples](./docs/usage.md)
- [Category Overview](./docs/categories.md)

### Automation Tools Documentation
- [Automation Overview](./docs/AUTOMATION.md)
- [Release Automation](./docs/release-automation.md)
- [Quality Dashboard](./docs/quality-dashboard.md)
- [Auto-Label Bot](./docs/auto-label-bot.md)
- [Skills Manager API](./docs/skills-api.md)

### Project Documentation
- [Contributing Guide](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)

---

## ✨ Features Comparison

| Feature | This Repo | Other Repos |
|---------|-----------|-------------|
| **Skills Count** | 189 | 20-50 |
| **Categories** | 31 | 5-10 |
| **Industry Experts** | 4 | 1-2 |
| **Auto-Install** | ✅ | ❌ |
| **Validation** | ✅ | ❌ |
| **Auto-Update** | ✅ | ❌ |
| **Release Automation** | ✅ | ❌ |
| **Quality Dashboard** | ✅ | ❌ |
| **Auto-Label Bot** | ✅ | ❌ |
| **REST API** | ✅ | ❌ |
| **CI/CD** | ✅ | ❌ |
| **Documentation** | Comprehensive | Basic |
| **License** | MIT | Varies |

---

## 🛠️ Tools & Scripts

### Installation Script

```bash
./scripts/install.sh [OPTIONS]

Options:
  --all                Install all skills (default)
  --category NAME      Install specific category
  --list               List available categories
  --validate           Validate skills before install
  --help               Show help message

Examples:
  ./scripts/install.sh --all
  ./scripts/install.sh --category addyosmani
  ./scripts/install.sh --category mattpocock --validate
```

### Validation Script

```bash
./scripts/validate.sh

Checks:
  ✓ SKILL.md exists
  ✓ Valid YAML frontmatter
  ✓ Required fields present
  ✓ No broken links
  ✓ Proper markdown formatting
```

### Update Script

```bash
./scripts/update.sh

Updates:
  ✓ Pull latest changes
  ✓ Backup existing skills
  ✓ Install new/updated skills
  ✓ Show changelog
```

---

## 🤝 Contributing

Contributions welcome! We accept:

- ✅ New skills (with examples and documentation)
- ✅ Improvements to existing skills
- ✅ Bug fixes
- ✅ Documentation improvements
- ✅ Translation to other languages

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](./LICENSE)

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

---

## 🙏 Credits

### Skills Curated From

- [obra/superpowers](https://github.com/obra/superpowers) (186K ⭐) — Agentic workflows
- [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (125K ⭐) — Coding guidelines
- [mattpocock/skills](https://github.com/mattpocock/skills) (73K ⭐) — TypeScript & engineering
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (39K ⭐) — Production engineering

### Industry Experts

- **Andrej Karpathy** — ex-Tesla AI Director, OpenAI founding member
- **Matt Pocock** — TypeScript educator, Total TypeScript
- **Addy Osmani** — Google Chrome team, web performance expert
- **Jesse Vincent (obra)** — Keyboard.io founder, Superpowers creator

### Community

Special thanks to all contributors and the Hermes Agent community.

---

## ⭐ Star History

If you find this useful, please star the repo!

[![Star History Chart](https://api.star-history.com/svg?repos=kevinnft/ai-agent-skills&type=Date)](https://star-history.com/#kevinnft/ai-agent-skills&Date)

---

## 📊 Stats

- **189 Skills** across 26 populated categories (31 skill directories)
- **4 Automation Tools** (Release, Quality, Auto-Label, API)
- **424K+ Combined Stars** from source repos
- **4 Industry Experts** contributing knowledge
- **Production-Tested** in real projects
- **Zero Dependencies** — pure markdown
- **Quality Score:** 86/100 (Good)

---

## 🔗 Links

- [Hermes Agent](https://github.com/nousresearch/hermes-agent)
- [Documentation](https://hermes-agent.nousresearch.com/docs)
- [Automation Tools](docs/AUTOMATION.md)
- [Issue Tracker](https://github.com/kevinnft/ai-agent-skills/issues)
- [Changelog](CHANGELOG.md)

---

**Made with ❤️ by the AI Agent community**

**189 skills + 4 automation tools to make your AI agent production-ready** 🚀
