<div align="center">

# AI Agent Skills

**An honest, attribution-first installer for 189 publicly available agent-skill markdown files.**

Hermes Agent · Claude Code · Cursor · OpenCode · any agent that reads `SKILL.md`.

[![License: MIT](https://img.shields.io/badge/license-MIT-orange.svg?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-189-blue?style=for-the-badge)](#-categories)
[![Categories](https://img.shields.io/badge/categories-26-green?style=for-the-badge)](./docs/categories.md)
[![CI](https://img.shields.io/github/actions/workflow/status/kevinnft/ai-agent-skills/ci.yml?style=for-the-badge&label=CI)](https://github.com/kevinnft/ai-agent-skills/actions/workflows/ci.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](./CONTRIBUTING.md)

[Quick start](#-quick-start) ·
[Categories](#-categories) ·
[Conflicts to know](#-conflicts--duplicates) ·
[Contributing](./CONTRIBUTING.md) ·
[Attribution (`NOTICE`)](./NOTICE)

</div>

---

## ⚡ The 30-second pitch

```
189 SKILL.md files  +  one-command installer  +  validation CI  +  REST API
                              ↓
                      drop into your agent
```

This is a **derivative work** — most skill content was authored by other people in their public repos. The value-add here is: aggregation, categorization, conflict detection, validation tooling, attribution metadata, and a portable installer. **Original authors did not contribute to or endorse this repo.** See [`NOTICE`](./NOTICE) for full attribution.

> [!IMPORTANT]
> If you want the canonical version of a specific author's skills, install from their repo directly. Links in [`NOTICE`](./NOTICE).

---

## 📦 Quick start

### Hermes Agent

```bash
git clone --recurse-submodules https://github.com/kevinnft/ai-agent-skills.git
cd ai-agent-skills
./scripts/install.sh                        # all 189 skills
./scripts/install.sh --category addyosmani  # one category
./scripts/install.sh --list                 # browse before installing
./scripts/install.sh --validate             # dry-run + lint
```

### Claude Code · Cursor · custom agent

```bash
cp -r skills/* ~/.claude/skills/      # Claude Code
cp -r skills/* ~/.cursor/skills/      # Cursor
cp -r skills/* /your/agent/skills/    # anything that reads SKILL.md
```

### Tip: install one category, see if it clicks

```bash
./scripts/install.sh --category superpowers   # 14 agentic-workflow skills
```

If you like the way it works, `--all`. If not, the rest is one `cp` away.

---

## 🎯 Categories

Verified counts (via `find skills -name SKILL.md` after `git submodule update --init`):

<table>
<tr>
<td valign="top">

**Engineering — 80 skills**
- [`addyosmani/`](skills/addyosmani) — 22 (production engineering)
- [`mattpocock/`](skills/mattpocock) — 28 (TypeScript & workflows)
- [`superpowers/`](skills/superpowers) — 14 (agentic patterns)
- [`software-development/`](skills/software-development) — 16 (mixed)

**Creative — 22 skills**
- Diagrams · ASCII · p5.js · ComfyUI · DESIGN.md tokens · pixel art · Manim · TouchDesigner

**MLOps — 15 skills**
- llama.cpp · Axolotl · Unsloth · vLLM · TRL · DSPy · lm-eval-harness

</td>
<td valign="top">

**Research — 11 skills**
- arXiv · web scraping · blogwatcher · polymarket · NFT/crypto analysis

**GitHub — 10 skills**
- PR workflow · code review · repo mgmt · auth · issues

**DevOps — 9 skills**
- Docker compose · VPS hardening · browser automation · kanban · webhooks

**Productivity — 8 skills**
- Notion · Google Workspace · Linear · Airtable · PowerPoint · OCR · maps

</td>
</tr>
</table>

Plus `media (5)` · `obsidian-skills (5, submodule)` · `apple (4)` · `autonomous-ai-agents (4)` · `note-taking, social-media, gaming, software-copyright (2 each)` · `data-science, dogfood, email, mcp, red-teaming, smart-home, yuanbao, patent-disclosure-skill (1 each)`.

📚 Full catalog: [`docs/categories.md`](./docs/categories.md)

---

## ⚠️ Conflicts & duplicates

Same-name skills exist under multiple categories. Pick **one** when installing — duplicates confuse the loader (last-write-wins).

| Skill | Locations | Recommended pick |
|---|---|---|
| `test-driven-development` | `addyosmani/`, `superpowers/`, `software-development/` | `superpowers/` (most explicit RED-GREEN-REFACTOR loop) |
| `systematic-debugging` | `superpowers/`, `software-development/` | `superpowers/` (4-phase) |
| `requesting-code-review` | `superpowers/`, `software-development/` | `superpowers/` |
| `subagent-driven-development` | `superpowers/`, `software-development/` | `superpowers/` |
| `writing-plans` | `superpowers/`, `software-development/` | `superpowers/` |

The installer currently does **not** auto-resolve these — auditing your `~/.hermes/skills/` (or equivalent) after a full install is recommended.

---

## 🛠️ Tooling (original to this repo)

| Script | Purpose |
|---|---|
| [`scripts/install.sh`](scripts/install.sh) | Copy skills into your agent's skills dir. `--all`, `--category`, `--list`, `--validate`. |
| [`scripts/validate.sh`](scripts/validate.sh) | Lint `SKILL.md` frontmatter + check broken links. Returns non-zero on invalid skill. |
| [`scripts/update.sh`](scripts/update.sh) | Pull latest, back up existing, apply updates. |
| [`scripts/release.py`](scripts/release.py) | Generate changelog + tag a semver release. |
| [`scripts/quality-dashboard.py`](scripts/quality-dashboard.py) | Compute a self-scored repo health metric. **Heuristic — not third-party validation.** |
| [`scripts/skills-api.py`](scripts/skills-api.py) | Local REST server (default `:5555`) for browsing skills programmatically. |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Validation runs on every push / PR. |
| [`.github/workflows/auto-label.yml`](.github/workflows/auto-label.yml) | PR/issue label automation. |

All MIT-licensed under the project root [`LICENSE`](./LICENSE).

---

## 📊 Stats

```
189  SKILL.md files            ✅
 26  populated categories      ✅
 64  skills with explicit      source_repo + source_url + source_license
                                in YAML frontmatter (addyosmani / mattpocock / superpowers)
  8  scripts under scripts/    install · validate · update · release · dashboard · skills-api · create-labels · helper
  2  GitHub Actions            CI · auto-label
  2  git submodules            obsidian-skills · patent-disclosure-skill
```

---

## 🤝 Contributing

PRs welcome — see [`CONTRIBUTING.md`](./CONTRIBUTING.md). Two contribution types with **different rules**:

1. **Original skills** — author your own. Required: `name`, `description`, `author`, `tags`. Tested in at least one real session.
2. **Aggregated skills** — pull in a public skill from another repo. Required: `source_repo`, `source_url`, `source_license`. Upstream license must permit redistribution.

We **reject** PRs that strip attribution or misrepresent upstream authorship as a contribution to this repo. Reviewers see the attribution checklist on every PR.

---

## ❓ FAQ

**Is this maintained by the named upstream authors?**
No. They have not contributed to or endorsed this repo. See [`NOTICE`](./NOTICE) for the non-affiliation disclaimer.

**Why not just install from upstream directly?**
You can — and should, if you only want one author's skills. The win here is one command for 189 skills across 26 categories, plus categorization, conflict detection, validation, and a REST API.

**The "Quality 86/100" dashboard score — what does it actually mean?**
It's a heuristic computed by `scripts/quality-dashboard.py` (this repo's own script) based on README presence, LICENSE, CI status, broken-link check, and a few other surface signals. Not third-party validation. Don't read it as endorsement.

**The repo description says "189" but I see "191+" elsewhere — which is right?**
Currently **189** (verified each release via `find skills -name SKILL.md`). Older docs may say "191+" — if you find one, please open a PR.

**Can I use this commercially?**
This repo's tooling: yes (MIT). Skill content from upstream: yes if their license permits — see per-skill `source_license` frontmatter or [`NOTICE`](./NOTICE).

---

## 📄 License & attribution

- **This repo's tooling, layout, aggregation work:** MIT — [`LICENSE`](./LICENSE).
- **Skill content from upstream repos:** each skill keeps its upstream license. See per-skill frontmatter and [`NOTICE`](./NOTICE).

If you are an upstream author and would like a skill removed, renamed, or attributed differently, please [open an issue](https://github.com/kevinnft/ai-agent-skills/issues/new).

---

<div align="center">

**Hermes Agent** · [docs](https://hermes-agent.nousresearch.com/docs) · [repo](https://github.com/nousresearch/hermes-agent)

[`NOTICE`](./NOTICE) · [`CHANGELOG`](./CHANGELOG.md) · [`SECURITY`](./SECURITY.md) · [Issues](https://github.com/kevinnft/ai-agent-skills/issues)

</div>
