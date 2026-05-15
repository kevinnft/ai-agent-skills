#!/usr/bin/env python3
"""Backfill `origin: aggregated` + source_url for skills traceable to upstream.

This is a one-shot tool driven by the mapping in MAPPING below. Re-running is
idempotent: skills already marked aggregated with a matching source_url are
skipped.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"

# Upstream slug -> (source_repo, source_url_prefix, source_license)
UPSTREAMS = {
    "nousresearch": (
        "NousResearch/hermes-agent",
        "https://github.com/NousResearch/hermes-agent/tree/main/skills",
        "MIT",
    ),
    "baoyu": (
        "JimLiu/baoyu-skills",
        "https://github.com/JimLiu/baoyu-skills/tree/main/skills",
        "see upstream",
    ),
}

# skill path (relative to skills/) -> upstream slug
MAPPING = {
    # NousResearch/hermes-agent — verified via API contents lookup
    "creative/ascii-art": "nousresearch",
    "creative/ascii-video": "nousresearch",
    "creative/comfyui": "nousresearch",
    "creative/creative-ideation": "nousresearch",
    "creative/manim-video": "nousresearch",
    "creative/p5js": "nousresearch",
    "creative/pixel-art": "nousresearch",
    "creative/songwriting-and-ai-music": "nousresearch",
    "creative/touchdesigner-mcp": "nousresearch",
    "creative/claude-design": "nousresearch",
    "devops/kanban-orchestrator": "nousresearch",
    "devops/kanban-worker": "nousresearch",
    "devops/webhook-subscriptions": "nousresearch",
    "dogfood": "nousresearch",
    "gaming/minecraft-modpack-server": "nousresearch",
    "gaming/pokemon-player": "nousresearch",
    "media/heartmula": "nousresearch",
    "media/youtube-content": "nousresearch",
    "note-taking/obsidian": "nousresearch",
    "productivity/maps": "nousresearch",
    "productivity/powerpoint": "nousresearch",
    "social-media/xurl": "nousresearch",
    "yuanbao": "nousresearch",
    # JimLiu/baoyu-skills — original author repo
    "creative/baoyu-comic": "baoyu",
    "creative/baoyu-infographic": "baoyu",
}

FRONTMATTER_RE = re.compile(r"^(---\n)(.*?)(\n---\n)", re.DOTALL)


def update_frontmatter(text: str, *, source_repo: str, source_url: str, source_license: str) -> tuple[str, bool]:
    """Set origin: aggregated and source_* fields in the first frontmatter block."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return text, False
    head, fm, tail = m.group(1), m.group(2), m.group(3)

    def replace_or_append(field: str, value: str, body: str) -> str:
        pattern = re.compile(rf"^{field}:\s*.*$", re.MULTILINE)
        if pattern.search(body):
            return pattern.sub(f"{field}: {value}", body, count=1)
        # append at end of frontmatter block
        return body.rstrip() + f"\n{field}: {value}"

    new_fm = fm
    new_fm = replace_or_append("origin", "aggregated", new_fm)
    new_fm = replace_or_append("source_repo", source_repo, new_fm)
    new_fm = replace_or_append("source_url", source_url, new_fm)
    new_fm = replace_or_append("source_license", source_license, new_fm)

    if new_fm == fm:
        return text, False
    return head + new_fm + tail + text[m.end():], True


def main() -> int:
    changed = 0
    skipped = 0
    missing = []

    for rel, slug in MAPPING.items():
        repo, url_prefix, license_ = UPSTREAMS[slug]
        skill_path = SKILLS_DIR / rel / "SKILL.md"
        if not skill_path.exists():
            missing.append(rel)
            continue

        text = skill_path.read_text(encoding="utf-8")
        new_text, was_changed = update_frontmatter(
            text,
            source_repo=repo,
            source_url=f"{url_prefix}/{rel}",
            source_license=license_,
        )
        if was_changed:
            skill_path.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"  patched: {rel} -> {repo}")
        else:
            skipped += 1

    print(f"\nDone: {changed} patched, {skipped} unchanged, {len(missing)} missing")
    for rel in missing:
        print(f"  MISSING: skills/{rel}/SKILL.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
