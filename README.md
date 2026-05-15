<div align="center">

<a href="#-quick-start"><img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,2,30,16&height=200&section=header&text=AI%20Agent%20Skills&fontSize=70&fontAlignY=38&fontColor=ffffff&desc=189%20attribution-first%20skills%20for%20any%20agent%20that%20reads%20SKILL.md&descAlignY=62&descSize=14&animation=fadeIn" alt="AI Agent Skills banner" /></a>

<p>
  <em>One installer. 189 skills. 26 categories. Zero borrowed credibility.</em><br/>
  <sub>Hermes Agent · Claude Code · Cursor · OpenCode · anything that reads <code>SKILL.md</code></sub>
</p>

<p>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A8E6CF?style=for-the-badge&labelColor=2D3748" /></a>
  <a href="#-categories"><img alt="189 skills" src="https://img.shields.io/badge/skills-189-7AB8FF?style=for-the-badge&labelColor=2D3748" /></a>
  <a href="./docs/categories.md"><img alt="26 categories" src="https://img.shields.io/badge/categories-26-FFB3BA?style=for-the-badge&labelColor=2D3748" /></a>
  <a href="https://github.com/kevinnft/ai-agent-skills/actions/workflows/ci.yml"><img alt="CI status" src="https://img.shields.io/github/actions/workflow/status/kevinnft/ai-agent-skills/ci.yml?style=for-the-badge&label=CI&labelColor=2D3748&color=B5EAD7" /></a>
  <a href="./CONTRIBUTING.md"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-FFD93D?style=for-the-badge&labelColor=2D3748" /></a>
  <a href="./NOTICE"><img alt="Attribution NOTICE" src="https://img.shields.io/badge/attribution-NOTICE-C7B6FF?style=for-the-badge&labelColor=2D3748" /></a>
</p>

<p>
  <a href="#-quick-start"><b>Quick start</b></a> ·
  <a href="#-categories">Categories</a> ·
  <a href="#-provenance">Provenance</a> ·
  <a href="#%EF%B8%8F-conflicts--duplicates">Conflicts</a> ·
  <a href="./docs/sync.md">Sync strategy</a> ·
  <a href="./CONTRIBUTING.md">Contributing</a> ·
  <a href="#-faq">FAQ</a>
</p>

</div>

---

## ⚡ The 30-second pitch

```text
   ┌─ obra/superpowers ─────┐
   ├─ mattpocock/skills ────┤      189 SKILL.md files
   ├─ addyosmani/agent-… ──→│  →   one-command installer  →   ~/.hermes/skills/
   ├─ kepano/obsidian-skills┤      validation CI                ~/.claude/skills/
   ├─ original (Hermes/Nous)┤      REST API (:5555)             ~/.cursor/skills/
   └─ community + adapted ──┘      attribution metadata
```

**Derivative work, full attribution.** Most skill content was authored by other people in their public repos. The value-add here is the aggregation, categorization, conflict detection, validation tooling, attribution metadata, and a portable installer. The named upstream authors did not contribute to or endorse this repo — see [`NOTICE`](./NOTICE) and per-skill `source_url:` frontmatter.

> [!IMPORTANT]
> Want the canonical version of one author's skills? Install directly from their repo. Links in [`NOTICE`](./NOTICE).

---

## 📦 Quick start

<table>
<tr><th width="200">Agent</th><th>Command</th></tr>
<tr><td>

🜲 **Hermes Agent**

</td><td>

```bash
git clone --recurse-submodules https://github.com/kevinnft/ai-agent-skills.git
cd ai-agent-skills && ./scripts/install.sh
```

</td></tr>
<tr><td>

🟧 **Claude Code**

</td><td>

```bash
cp -r skills/* ~/.claude/skills/
```

</td></tr>
<tr><td>

🟦 **Cursor**

</td><td>

```bash
cp -r skills/* ~/.cursor/skills/
```

</td></tr>
<tr><td>

🟪 **Anything else**

</td><td>

```bash
cp -r skills/* /path/to/your/agent/skills/
```

</td></tr>
</table>

### Installer flags

```bash
./scripts/install.sh --list                  # browse before installing
./scripts/install.sh --category superpowers  # install just one category
./scripts/install.sh --validate              # dry-run + lint
./scripts/install.sh --help
```

> **Tip:** start with one category (`--category superpowers` is 14 well-tested agentic-workflow skills). If you like it, `--all`. If not, the rest is one `cp` away.

---

## 🎯 Categories

Counts verified at every release with `find skills -name SKILL.md` after `git submodule update --init`.

<table>
<tr>
<td valign="top" width="50%">

#### 🛠️ Engineering — 80
- 🔵 [`addyosmani/`](skills/addyosmani) — **22** &nbsp; production engineering
- 🟣 [`mattpocock/`](skills/mattpocock) — **28** &nbsp; TypeScript & workflows
- 🟢 [`superpowers/`](skills/superpowers) — **14** &nbsp; agentic patterns
- 🟡 [`software-development/`](skills/software-development) — **16** &nbsp; mixed

#### 🎨 Creative — 22
Diagrams · ASCII art · p5.js · ComfyUI · DESIGN.md tokens · pixel art · Manim · TouchDesigner · Excalidraw

#### 🤖 MLOps — 15
llama.cpp · Axolotl · Unsloth · vLLM · TRL · DSPy · lm-eval-harness · Hugging Face Hub

</td>
<td valign="top" width="50%">

#### 🔬 Research — 11
arXiv · web scraping · blogwatcher · polymarket · NFT/crypto analysis · trending repos

#### 🐙 GitHub — 10
PR workflow · code review · repo mgmt · auth · issues · visual assets

#### ⚙️ DevOps — 9
Docker compose · VPS hardening · browser automation · kanban · webhooks

#### 📋 Productivity — 8
Notion · Google Workspace · Linear · Airtable · PowerPoint · OCR · maps

</td>
</tr>
</table>

<sub>Plus `media (5)` · `obsidian-skills (5, submodule)` · `apple (4)` · `autonomous-ai-agents (4)` · `note-taking, social-media, gaming, software-copyright (2 each)` · `data-science, dogfood, email, mcp, red-teaming, smart-home, yuanbao, patent-disclosure-skill (1 each)`</sub>

📚 Full per-skill catalog → [`docs/categories.md`](./docs/categories.md)

---

## 📊 Provenance

Every `SKILL.md` declares where it came from. Run `grep -h "^origin:" skills/**/SKILL.md | sort | uniq -c` to verify.

```text
       ┌─────────────────────────────────────────────────────────────┐
   89  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                        │  aggregated
   61  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                    │  original
   22  │ ▓▓▓▓▓▓▓▓▓                                                   │  unknown ⚠
   11  │ ▓▓▓▓                                                        │  adapted
       └─────────────────────────────────────────────────────────────┘
                                                          189 total*
```

<sub>*189 SKILL.md files total. 6 are inside the obsidian-skills / patent-disclosure-skill git submodules — those keep upstream-owned frontmatter and are excluded from the `origin:` provenance contract.</sub>

| `origin:` | Count | Meaning |
|---|--:|---|
| 🟦 `aggregated` | **89** | Top-level frontmatter copied from a named upstream repo with full attribution (`addyosmani/`, `mattpocock/`, `superpowers/`, `NousResearch/hermes-agent`, `JimLiu/baoyu-skills`) |
| 🟩 `original` | **61** | Authored for this repo's ecosystem (Hermes / Nous Research / Orchestra / community) |
| 🟧 `adapted` | **11** | Materially edited from a named upstream — see `source_url` |
| 🟥 `unknown` | **22** | Author present in frontmatter but upstream repo not yet identified — **help wanted!** |

> **🤝 Help wanted on the remaining `unknown`-origin skills.** Down from 53 in v1.6.0 — community-traceable upstream identified for 31 skills (25 from `NousResearch/hermes-agent`, 6 from named author repos). If you recognize one of the [remaining 22](./docs/categories.md), open a PR adding `source_repo` / `source_url` / `source_license` to the frontmatter.

---

## ⚠️ Conflicts & duplicates

Same-name skills exist under multiple categories. Pick **one** when installing — duplicates confuse the loader (last-write-wins).

| Skill | Locations | Recommended pick |
|---|---|---|
| `test-driven-development` | `addyosmani/`, `superpowers/`, `software-development/` | 🥇 `superpowers/` — most explicit RED-GREEN-REFACTOR loop |
| `systematic-debugging` | `superpowers/`, `software-development/` | 🥇 `superpowers/` — 4-phase |
| `requesting-code-review` | `superpowers/`, `software-development/` | 🥇 `superpowers/` |
| `subagent-driven-development` | `superpowers/`, `software-development/` | 🥇 `superpowers/` |
| `writing-plans` | `superpowers/`, `software-development/` | 🥇 `superpowers/` |

The installer does **not** auto-resolve these — auditing your `~/.hermes/skills/` after a full install is recommended. See [`docs/sync.md`](./docs/sync.md) for the upstream-drift strategy.

---

## 🛠️ Tooling (original to this repo)

| Script | Purpose | Notes |
|---|---|---|
| [`install.sh`](scripts/install.sh) | Copy skills to your agent's skills dir | `--all`, `--category`, `--list`, `--validate` |
| [`validate.sh`](scripts/validate.sh) | Lint frontmatter + broken links | Non-zero exit on failure |
| [`update.sh`](scripts/update.sh) | Pull latest, back up existing, apply | Safe re-run |
| [`release.py`](scripts/release.py) | Generate changelog + tag semver | Tested ✅ |
| [`quality-dashboard.py`](scripts/quality-dashboard.py) | Self-scored repo health metric | **Heuristic — not third-party validation** |
| [`skills-api.py`](scripts/skills-api.py) | Local REST server (`:5555`) | `GET /api/skills`, `GET /api/skills/search?q=...` |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Validation + pytest on push/PR | 22 unit tests |
| [`.github/workflows/upstream-sync-check.yml`](.github/workflows/upstream-sync-check.yml) | Weekly drift report from upstream sources | Mondays 06:17 UTC |
| [`.github/workflows/auto-label.yml`](.github/workflows/auto-label.yml) | PR/issue auto-labeling | 35 labels |

All tooling MIT-licensed under [`LICENSE`](./LICENSE).

---

## 📈 Stats at a glance

```text
  189  SKILL.md files                            ✅ verified each release
   26  populated categories                      ✅
  161  skills with source_repo metadata          (89 aggregated + 11 adapted + 61 original-self-link)
   22  skills awaiting upstream identification   🤝 help wanted
    9  scripts under scripts/
    3  GitHub Actions workflows                  CI · auto-label · upstream-sync-check
   28  pytest unit tests                         scripts/release · skills-api · quality-dashboard
    2  git submodules                            obsidian-skills · patent-disclosure-skill
```

---

## 🤝 Contributing

PRs welcome — see [`CONTRIBUTING.md`](./CONTRIBUTING.md). Two contribution types with **different rules**:

| Type | Required frontmatter | What we check |
|---|---|---|
| 🟢 **Original skill** | `name`, `description`, `author`, `tags` | Tested in at least one real session — describe how in the PR |
| 🟡 **Aggregated skill** | `source_repo`, `source_url`, `source_license` (in addition to the above) | Upstream license permits redistribution; you didn't strip credit |

We **reject** PRs that strip attribution or misrepresent upstream authorship. Reviewers see the attribution checklist on every PR.

---

## ❓ FAQ

<details>
<summary><b>Is this maintained by the named upstream authors (Karpathy / Pocock / Osmani / obra)?</b></summary>
<br/>

No. They have not contributed to or endorsed this repo. See [`NOTICE`](./NOTICE) for the non-affiliation disclaimer.
</details>

<details>
<summary><b>Why not just install from upstream directly?</b></summary>
<br/>

You can — and should, if you only want one author's skills. The win here is one command for 189 skills across 26 categories, plus categorization, conflict detection, validation, and a REST API. We diff against upstream weekly (see [`docs/sync.md`](./docs/sync.md)) and surface drift via [`upstream-sync-check.yml`](./.github/workflows/upstream-sync-check.yml).
</details>

<details>
<summary><b>The "Quality 86/100" dashboard score — what does it actually mean?</b></summary>
<br/>

It's a heuristic computed by [`scripts/quality-dashboard.py`](scripts/quality-dashboard.py) (this repo's own script) based on README presence, LICENSE, CI status, broken-link check, and a few other surface signals. Not third-party validation. Don't read it as endorsement.
</details>

<details>
<summary><b>The repo description says "189" but older docs say "191+" — which is right?</b></summary>
<br/>

**189** (verified each release via `find skills -name SKILL.md`). Older docs may say "191+" — open a PR if you find one.
</details>

<details>
<summary><b>How fresh are the vendored skills vs. upstream?</b></summary>
<br/>

A weekly GitHub Action (Mondays 06:17 UTC) opens or updates a tracking issue with the upstream HEAD SHA of each source repo. If you see drift you care about, open a sync PR — full strategy in [`docs/sync.md`](./docs/sync.md).
</details>

<details>
<summary><b>Can I use this commercially?</b></summary>
<br/>

This repo's tooling: yes (MIT). Skill content from upstream: yes if their license permits — see per-skill `source_license` frontmatter or [`NOTICE`](./NOTICE).
</details>

---

## 📄 License & attribution

- **This repo's tooling, layout, aggregation work:** MIT — [`LICENSE`](./LICENSE)
- **Skill content from upstream repos:** each skill keeps its upstream license — see per-skill frontmatter and [`NOTICE`](./NOTICE)

If you are an upstream author and would like a skill removed, renamed, or attributed differently, please [open an issue](https://github.com/kevinnft/ai-agent-skills/issues/new).

---

<div align="center">

<sub>Made for the agent ecosystem · powered by community work · attribution-first.</sub>

**Hermes Agent** · [docs](https://hermes-agent.nousresearch.com/docs) · [repo](https://github.com/nousresearch/hermes-agent)

[`NOTICE`](./NOTICE) · [`CHANGELOG`](./CHANGELOG.md) · [`SECURITY`](./SECURITY.md) · [Sync strategy](./docs/sync.md) · [Issues](https://github.com/kevinnft/ai-agent-skills/issues)

<a href="#"><img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,2,30,16&height=80&section=footer&animation=fadeIn" alt="footer" /></a>

</div>
