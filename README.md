# AI Agent Skills

> An aggregated installer of publicly available agent-skill markdown files for AI coding agents (Hermes Agent, Claude Code, Cursor, etc.). 189 skills across 26 categories, sourced from open-source skill repositories.

[![Skills](https://img.shields.io/badge/skills-189-blue)](#categories)
[![Categories](https://img.shields.io/badge/categories-26-green)](#categories)
[![License](https://img.shields.io/badge/license-MIT-orange)](./LICENSE)
[![Attribution](https://img.shields.io/badge/attribution-NOTICE-yellow)](./NOTICE)
[![CI](https://github.com/kevinnft/ai-agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/kevinnft/ai-agent-skills/actions/workflows/ci.yml)

---

## What this is

A curated, installable bundle of agent-skill markdown files (the `SKILL.md` format used by Hermes Agent, Claude Code's skills, and similar) drawn from publicly available open-source skill repositories. The value-add is the **aggregation, categorization, validation tooling, and one-command installer** — not the skill content itself.

> [!IMPORTANT]
> **Attribution & honesty notice.** Several category directories (`addyosmani/`, `mattpocock/`, `superpowers/`) are named after well-known authors of public skill repos. Those authors are not affiliated with this repository and have not contributed to it. See [`NOTICE`](./NOTICE) for the full attribution and source-license table. Per-skill `source:` frontmatter is being added progressively.

## What this is NOT

- Not a curation by the named authors (Karpathy, Pocock, Osmani, obra) — they did not endorse, contribute to, or review this repo.
- Not "production-tested in real projects" beyond what the upstream skill files say about themselves.
- Not a replacement for reading the original repos if you want the latest version of a given skill.

If you want the canonical version of a specific author's skills, install directly from their repo (linked in [`NOTICE`](./NOTICE)).

---

## Stats

- **189** `SKILL.md` files across **26** categories
- **2** git submodules (`obsidian-skills`, `patent-disclosure-skill`) — pull with `git submodule update --init`
- **5** known same-name skills present in multiple categories — see [Conflicts & duplicates](#conflicts--duplicates)
- **6** automation scripts under `scripts/` (install, validate, update, release, quality-dashboard, skills-api) — original to this repo
- **MIT** licensed (this repo's added layout + tooling); upstream skills retain their own licenses (see [`NOTICE`](./NOTICE))

---

## Quick start

### Hermes Agent

```bash
git clone --recurse-submodules https://github.com/kevinnft/ai-agent-skills.git
cd ai-agent-skills
./scripts/install.sh                          # install all
./scripts/install.sh --category addyosmani    # or one category
./scripts/install.sh --list                   # see categories
```

### Claude Code

```bash
cp -r skills/* ~/.claude/skills/
```

### Cursor

```bash
cp -r skills/* ~/.cursor/skills/
```

### Custom agent

```bash
cp -r skills/* /path/to/your/agent/skills/
```

---

## Categories

All counts verified by scanning `find skills -name SKILL.md` after `git submodule update --init`. Numbers match this repo's actual contents at the latest commit on `main`.

### Engineering buckets (80 skills)

#### `addyosmani/` (22) — production engineering practices
Sourced from [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) (MIT). Topics: code review, performance, security, TDD, spec-driven development, debugging, planning, deprecation.

#### `mattpocock/` (28) — TypeScript & engineering workflows
Sourced from [`mattpocock/skills`](https://github.com/mattpocock/skills) (MIT). Topics: TDD, diagnose, review, refactor planning, PRD generation, ubiquitous language, pre-commit hooks, article writing.

#### `superpowers/` (14) — agentic workflows
Sourced from [`obra/superpowers`](https://github.com/obra/superpowers) (MIT). Topics: brainstorming, verification-before-completion, executing plans, writing skills, parallel dispatch, code-review feedback, git worktrees.

#### `software-development/` (16) — original + community-curated
Mix of original skills authored for this repo and additions from the broader Hermes Agent community. Topics: API testing, systematic debugging, Hermes-specific debugging, ecosystem evaluation, IDE contribution, plan mode, spike experiments.

### Other categories

| Category | Count | Notes |
|---|--:|---|
| `creative` | 22 | Diagrams, ASCII, p5.js, ComfyUI, design tools |
| `mlops` | 15 | llama.cpp, Axolotl, Unsloth, vLLM, HF Hub, TRL, DSPy, lm-eval-harness |
| `research` | 11 | Web scraping, arXiv, blogwatcher, polymarket, crypto/NFT analysis |
| `github` | 10 | PR workflow, code review, repo management, auth, issues |
| `devops` | 9 | Docker compose, VPS hardening, browser automation, kanban |
| `productivity` | 8 | Notion, Google Workspace, Linear, Airtable, PowerPoint, OCR |
| `media` | 5 | Spotify, YouTube, GIF search, Suno-style music, audio analysis |
| `obsidian-skills` | 5 | Git submodule from [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills) |
| `apple` | 4 | macOS-specific tooling |
| `autonomous-ai-agents` | 4 | Claude Code, Codex, OpenCode, Hermes-Agent meta-skills |
| `mlops` (deeper) | — | Plus subcategory specs |
| `note-taking`, `social-media`, `gaming`, `software-copyright` | 2 each | |
| `data-science`, `dogfood`, `email`, `mcp`, `red-teaming`, `smart-home`, `yuanbao`, `patent-disclosure-skill` | 1 each | |

See [`docs/categories.md`](./docs/categories.md) for the full per-skill list.

---

## Conflicts & duplicates

The same skill name appears under multiple category directories. Pick **one** to install per machine — having two skills with the same name confuses Hermes Agent's loader. The differences are usually upstream-author flavor.

| Skill name | Locations | Suggested pick |
|---|---|---|
| `test-driven-development` | `addyosmani/`, `superpowers/`, `software-development/` | `superpowers/` (most detailed RED-GREEN-REFACTOR loop) or `addyosmani/` (more breadth) |
| `systematic-debugging` | `superpowers/`, `software-development/` | `superpowers/` (4-phase) |
| `requesting-code-review` | `superpowers/`, `software-development/` | `superpowers/` |
| `subagent-driven-development` | `superpowers/`, `software-development/` | `superpowers/` |
| `writing-plans` | `superpowers/`, `software-development/` | `superpowers/` |

The installer (`scripts/install.sh`) currently does **not** auto-resolve these — it copies all of them, last-write-wins. If you install everything, double-check `~/.hermes/skills/` after.

---

## Tooling

Original to this repo, MIT-licensed under the project root `LICENSE`.

### `scripts/install.sh`
Copies skills into your agent's skills directory. Supports `--all`, `--category NAME`, `--list`, `--validate`, `--help`.

### `scripts/validate.sh`
Lints `SKILL.md` files for required YAML frontmatter and broken links.

### `scripts/update.sh`
Pulls latest changes, backs up existing skills, applies updates.

### `scripts/release.py`
Generates changelog entries and tags a semver release.

### `scripts/quality-dashboard.py`
Computes a self-scored quality metric. **Note:** the score is a heuristic produced by this repo's own script — do not interpret it as third-party validation.

### `scripts/skills-api.py`
Local REST server (default port 5555) for browsing skills programmatically.

### CI: `.github/workflows/ci.yml`
Runs `validate.sh` on every push/PR.

### Auto-label bot
`.github/workflows/` includes label automation for PRs and issues.

---

## Contributing

PRs welcome. See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Two kinds of contributions:

1. **Original skills** — author your own `SKILL.md`. Include `author:` and a brief license note in frontmatter.
2. **Aggregated skills** — pull in a public skill from another repo. Include `source:`, `source_url:`, and `source_license:` in the frontmatter so attribution is preserved.

We **do not** accept contributions that misrepresent authorship or strip attribution from upstream sources.

---

## License

This repo's tooling, layout, and aggregation work: **MIT** ([`LICENSE`](./LICENSE)).

Skill content sourced from upstream repos: each skill retains its upstream license. See [`NOTICE`](./NOTICE) for the source/license table.

---

## Links

- [Hermes Agent](https://github.com/nousresearch/hermes-agent)
- [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs)
- [Issue tracker](https://github.com/kevinnft/ai-agent-skills/issues)
- [`NOTICE` — full attribution](./NOTICE)
- [`CHANGELOG`](./CHANGELOG.md)
