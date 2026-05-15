#!/usr/bin/env python3
"""Inject `origin:` metadata into SKILL.md files based on classification.

origin values:
  original  - authored for this repo's ecosystem (Hermes/Nous/Orchestra/community)
  adapted   - derivative work; source_url filled where author string identifies upstream
  unknown   - author present but no clear upstream link; flagged for review

Idempotent: only adds keys if not already present.
"""
import json, re, os, sys

with open("scripts/backfill/classification.json") as f:
    data = json.load(f)

# Map adapted authors → upstream repo URLs
ADAPTED_MAP = {
    "obra/superpowers": ("obra/superpowers", "https://github.com/obra/superpowers", "MIT"),
    "obra/superpowers + MorAlekss": ("obra/superpowers", "https://github.com/obra/superpowers", "MIT"),
    "gsd-build/get-shit-done": ("gsd-build/get-shit-done", "https://github.com/gsd-build/get-shit-done", "MIT"),
    "Hyaxia/blogwatcher": ("Hyaxia/blogwatcher", "https://github.com/Hyaxia/blogwatcher", "MIT"),
    "VoltAgent/awesome-design-md": ("VoltAgent/awesome-design-md", "https://github.com/VoltAgent/awesome-design-md", "MIT"),
    "blader/humanizer": ("blader/humanizer", "https://github.com/blader/humanizer", "MIT"),
}

def detect_upstream(author):
    for needle, triple in ADAPTED_MAP.items():
        if needle in author:
            return triple
    # heuristic: parse "fork of X" / "adapted from X"
    m = re.search(r"(?:fork of|adapted from|sourced from)\s+([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", author)
    if m:
        slug = m.group(1)
        return (slug, f"https://github.com/{slug}", "MIT")
    return None

def insert_into_frontmatter(text, kvs):
    """Insert keys into YAML frontmatter just before closing ---. Skip already-present keys."""
    m = re.match(r"^(---\n)(.*?)(\n---)", text, re.S)
    if not m:
        return text, False
    head, body, tail = m.group(1), m.group(2), m.group(3)
    additions = []
    for k, v in kvs.items():
        if re.search(rf"^\s*{re.escape(k)}\s*:", body, re.M):
            continue
        additions.append(f"{k}: {v}")
    if not additions:
        return text, False
    new_body = body.rstrip() + "\n" + "\n".join(additions)
    return text.replace(m.group(0), head + new_body + tail, 1), True

stats = {"patched_original": 0, "patched_adapted": 0, "flagged_unknown": 0}

for entry in data["original"]:
    path = entry["path"]
    with open(path) as f:
        text = f.read()
    new_text, changed = insert_into_frontmatter(text, {
        "origin": "original",
        "source_repo": "kevinnft/ai-agent-skills",
        "source_url": "https://github.com/kevinnft/ai-agent-skills",
        "source_license": "MIT",
    })
    if changed:
        with open(path, "w") as f:
            f.write(new_text)
        stats["patched_original"] += 1

for entry in data["adapted"]:
    path = entry["path"]
    upstream = detect_upstream(entry["author"])
    if not upstream:
        continue
    repo, url, lic = upstream
    with open(path) as f:
        text = f.read()
    new_text, changed = insert_into_frontmatter(text, {
        "origin": "adapted",
        "source_repo": repo,
        "source_url": url,
        "source_license": lic,
    })
    if changed:
        with open(path, "w") as f:
            f.write(new_text)
        stats["patched_adapted"] += 1

# unknown: still mark with origin: unknown so users see the gap
for entry in data["unknown"]:
    path = entry["path"]
    with open(path) as f:
        text = f.read()
    new_text, changed = insert_into_frontmatter(text, {
        "origin": "unknown",
        "source_license": "see upstream",
    })
    if changed:
        with open(path, "w") as f:
            f.write(new_text)
        stats["flagged_unknown"] += 1

print(json.dumps(stats, indent=2))
