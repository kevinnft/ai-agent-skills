# Upstream sync

This repo aggregates skill content from public upstream repositories. To keep the trade-off honest, we surface drift instead of hiding it.

## Strategy

| Source | Vendored path | Strategy | Why |
|---|---|---|---|
| [`obra/superpowers`](https://github.com/obra/superpowers) | `skills/superpowers/` | vendored copy | Hand-picked subset; we don't want every superpowers skill |
| [`mattpocock/skills`](https://github.com/mattpocock/skills) | `skills/mattpocock/` | vendored copy | Stable, slow-moving; periodic manual sync is fine |
| [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) | `skills/addyosmani/` | vendored copy | Mostly stable; we patch frontmatter |
| [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills) | `skills/obsidian-skills/` | git submodule | Single-author repo, fast track-record |
| [`handsomestWei/patent-disclosure-skill`](https://github.com/handsomestWei/patent-disclosure-skill) | `skills/patent-disclosure-skill/` | git submodule | Self-contained skill, simple submodule |

## Drift detection

A weekly GitHub Action ([`upstream-sync-check.yml`](../.github/workflows/upstream-sync-check.yml)) opens (or updates) a tracking issue every Monday at 06:17 UTC with the upstream HEAD SHA of each source repo.

If a vendored copy has visibly diverged from upstream — and the divergence is **not** intentional — open a sync PR.

If the divergence **is** intentional (we patched a bug, fixed an example, made the skill match Hermes Agent's loader), we mark the skill with:

```yaml
origin: adapted
derived_from: <upstream-slug>@<upstream-sha>
```

so the trace is auditable from inside the SKILL.md frontmatter alone.

## Manual sync

```bash
# Pull a fresh copy of an upstream skill repo
git clone https://github.com/obra/superpowers /tmp/superpowers

# Diff against the vendored copy
diff -ru /tmp/superpowers/skills/test-driven-development \
        skills/superpowers/test-driven-development

# Apply changes you want, preserve frontmatter we added
```

## Why not all submodules?

We tried. Three problems:
1. Some upstream repos contain skills we don't want (or contain non-skill content)
2. Submodules confuse `cp -r` workflows in our Quick start
3. Many users install via tarball download, where submodule pointers are useless

Vendoring + sync detection is the trade-off that keeps the install one-command while staying honest about source.

## Per-skill provenance

Every `SKILL.md` has an `origin:` field. Counts as of v1.6.0:

| Origin | Count | Meaning |
|---|--:|---|
| `aggregated` | 64 | Top-level frontmatter copied from named upstream repo (full attribution) |
| `original` | 61 | Authored for this repo's ecosystem (Hermes / Nous / Orchestra / community) |
| `adapted` | 11 | Materially edited from a named upstream — see `source_url` |
| `unknown` | 53 | Author present but upstream repo not yet identified — help wanted |
