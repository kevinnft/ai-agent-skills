#!/usr/bin/env python3
"""Classify each unattributed SKILL.md as original / adapted / unknown.

Rules
-----
- "adapted from X" / "fork of X" / "ported by Hermes Agent" / "derived" → adapted
- "Hermes Agent", "Nous Research", "Orchestra Research", "community", "Hermes Agent + Teknium"
  alone → original (this repo's ecosystem)
- Empty or other authors → needs review
"""
import os, re, sys, json, glob

SKILL_FILES = glob.glob("skills/**/SKILL.md", recursive=True)

ORIGINAL_AUTHORS = {
    "Hermes Agent", "Nous Research", "Orchestra Research",
    "Hermes Agent + Teknium", "community", "Hugging Face",
}

ADAPTED_PATTERNS = re.compile(
    r"adapted from|fork of|ported by|derived|sourced from", re.I
)

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    return m.group(1)

def get_field(fm, name):
    m = re.search(rf"^{name}:\s*(.+?)$", fm or "", re.M)
    return m.group(1).strip().strip('"\'') if m else ""

def has_source_repo(fm):
    return bool(re.search(r"^\s*source_repo\s*:", fm or "", re.M))

results = {"original": [], "adapted": [], "unknown": [], "attributed": []}

for path in sorted(SKILL_FILES):
    with open(path) as f:
        text = f.read()
    fm = parse_frontmatter(text)
    if has_source_repo(fm):
        results["attributed"].append(path)
        continue
    author = get_field(fm, "author")
    if ADAPTED_PATTERNS.search(author):
        results["adapted"].append({"path": path, "author": author})
    elif author in ORIGINAL_AUTHORS:
        results["original"].append({"path": path, "author": author})
    else:
        results["unknown"].append({"path": path, "author": author or "(empty)"})

print(json.dumps({
    "total": len(SKILL_FILES),
    "attributed": len(results["attributed"]),
    "original": len(results["original"]),
    "adapted": len(results["adapted"]),
    "unknown": len(results["unknown"]),
}, indent=2))

with open("scripts/backfill/classification.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved scripts/backfill/classification.json")
print("\n--- adapted samples ---")
for r in results["adapted"][:10]:
    print(f"  {r['path']}: {r['author']}")
print("\n--- unknown samples ---")
for r in results["unknown"][:15]:
    print(f"  {r['path']}: {r['author']}")
