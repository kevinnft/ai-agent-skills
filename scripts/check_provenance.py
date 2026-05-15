#!/usr/bin/env python3
"""Check that every SKILL.md (outside submodules) declares an `origin` field.

Submodule skills are treated as upstream-owned and skipped. Run from the
repo root or via `python3 scripts/check_provenance.py`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# Skills shipped via git submodules — we cannot edit upstream frontmatter
# from this repo, so skip provenance checks for them.
SUBMODULE_PATHS = (
    SKILLS_DIR / "obsidian-skills",
    SKILLS_DIR / "patent-disclosure-skill",
)

ALLOWED_ORIGINS = {"original", "aggregated", "adapted", "unknown"}
ORIGIN_PATTERN = re.compile(r"^origin:\s*(?P<value>\S+)", re.MULTILINE)


def is_in_submodule(path: Path) -> bool:
    return any(submodule in path.parents or path == submodule for submodule in SUBMODULE_PATHS)


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"FAIL: skills directory not found at {SKILLS_DIR}")
        return 1

    missing: list[Path] = []
    invalid: list[tuple[Path, str]] = []
    checked = 0

    for skill_file in sorted(SKILLS_DIR.rglob("SKILL.md")):
        if is_in_submodule(skill_file):
            continue

        checked += 1
        # Only inspect the first frontmatter block.
        text = skill_file.read_text(encoding="utf-8", errors="replace")
        front_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not front_match:
            missing.append(skill_file)
            continue

        frontmatter = front_match.group(1)
        match = ORIGIN_PATTERN.search(frontmatter)
        if not match:
            missing.append(skill_file)
            continue

        value = match.group("value").strip("\"'").lower()
        if value not in ALLOWED_ORIGINS:
            invalid.append((skill_file, value))

    print(f"Checked {checked} non-submodule SKILL.md files")
    if missing:
        print(f"\nFAIL: {len(missing)} skill(s) missing `origin:` field:")
        for path in missing:
            print(f"  - {path.relative_to(REPO_ROOT)}")
    if invalid:
        print(f"\nFAIL: {len(invalid)} skill(s) with unrecognized origin value:")
        for path, value in invalid:
            print(f"  - {path.relative_to(REPO_ROOT)} -> {value!r}")
        print(f"  allowed: {', '.join(sorted(ALLOWED_ORIGINS))}")

    if missing or invalid:
        return 1

    print("PASS: all non-submodule skills declare a recognized origin.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
