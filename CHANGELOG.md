# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-12

### Added

#### New Skills
- **docker-compose** (devops) — Multi-container Docker orchestration
- **api-testing** (software-development) — REST/GraphQL API testing

#### Curated Skills (191 total)
- **addyosmani** (22 skills) — Production engineering from Addy Osmani (Google Chrome)
- **mattpocock** (28 skills) — TypeScript & workflows from Matt Pocock
- **superpowers** (14 skills) — Agentic workflows from obra
- **creative** (22 skills) — Visual content generation
- **mlops** (15 skills) — ML/AI operations
- **devops** (9 skills) — Infrastructure & deployment
- **github** (10 skills) — GitHub workflows
- **research** (11 skills) — Research & analysis
- **productivity** (8 skills) — Productivity tools
- **software-development** (16 skills) — Development workflows
- **autonomous-ai-agents** (4 skills) — AI agent tools
- **note-taking** (2 skills) — Note management
- **obsidian-skills** (5 skills) — Obsidian integration
- **media** (5 skills) — Media tools
- **gaming** (2 skills) — Game servers
- **social-media** (2 skills) — Social media tools
- **smart-home** (1 skill) — Smart home control
- **email** (1 skill) — Email management
- **mcp** (1 skill) — MCP integration
- **red-teaming** (1 skill) — Security testing
- **data-science** (1 skill) — Data science tools
- **patent-disclosure-skill** (1 skill) — Patent disclosure
- **software-copyright** (2 skills) — Software copyright
- **prism** (5 skills) — Structural analysis
- **dogfood** (1 skill) — QA testing
- **yuanbao** (1 skill) — Yuanbao integration

#### Tools & Scripts
- **install.sh** — Auto-installation script with validation
- **validate.sh** — Skill validation script
- **update.sh** — Update script (coming soon)

#### Documentation
- **README.md** — Comprehensive documentation
- **CONTRIBUTING.md** — Contribution guidelines
- **LICENSE** — MIT License
- **CHANGELOG.md** — This file

#### Repository Structure
- Organized by categories (31 categories)
- Clear skill format with YAML frontmatter
- Examples and best practices
- Support files (templates, scripts, references)

### Credits

Skills curated from:
- [obra/superpowers](https://github.com/obra/superpowers) (186K ⭐)
- [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (125K ⭐)
- [mattpocock/skills](https://github.com/mattpocock/skills) (73K ⭐)
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (39K ⭐)

### Contributors

- [@kevinnft](https://github.com/kevinnft) — Repository creator & maintainer

---

## [1.1.0] - 2026-05-12

### Fixed

#### Bug Fixes (5 total)
- **BUG #1 (CRITICAL):** Missing documentation files — Created complete docs/ directory with installation.md, usage.md, and categories.md
- **BUG #2 (MEDIUM):** Large venv directory (195MB) — Removed venv, reduced repo size from 220MB to 25MB (88% reduction)
- **BUG #3 (LOW):** Subdirectories without SKILL.md — Documented complex skill structures
- **BUG #4 (LOW):** No update script — Created scripts/update.sh with auto-update functionality
- **BUG #5 (LOW):** No docs/ directory — Created complete documentation structure

### Added

#### Documentation (26KB total)
- **docs/installation.md** (5.8KB) — Complete installation guide with multiple methods, troubleshooting, and verification
- **docs/usage.md** (9.3KB) — Usage examples, workflows, best practices, and tips
- **docs/categories.md** (11KB) — All 31 categories documented with descriptions and recommendations

#### Tools
- **scripts/update.sh** (4.8KB) — Auto-update script with backup, changelog display, and verification

### Changed
- Repo size reduced from 220MB to 25MB (88% reduction)
- All README links now valid (fixed 4 broken links)
- Documentation complete and production-ready

---

## [Unreleased]

### Planned

- [ ] Video tutorials
- [ ] Community contributions
- [ ] Kubernetes deployment skill
- [ ] Database advanced patterns skill
- [ ] Monitoring setup skill
- [ ] Container optimization skill

---

[1.0.0]: https://github.com/kevinnft/ai-agent-skills/releases/tag/v1.0.0
