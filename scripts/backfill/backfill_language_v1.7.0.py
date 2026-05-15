#!/usr/bin/env python3
"""Add a `language:` tag to every non-submodule SKILL.md frontmatter.

Default = "en". Skills detected as predominantly Chinese based on a
unicode-script heuristic get "zh". Idempotent — re-running yields zero
changes once tags exist.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
SUBMODULE_PATHS = (
    SKILLS_DIR / "obsidian-skills",
    SKILLS_DIR / "patent-disclosure-skill",
)

# Skills explicitly known to be in Chinese (based on the v1.6 audit).
KNOWN_ZH = {
    "yuanbao",
    "creative/baoyu-comic",
    "creative/baoyu-infographic",
    "software-copyright",
    "software-copyright/vendor/docx-toolkit",
}

FRONTMATTER_RE = re.compile(r"^(---\n)(.*?)(\n---\n)", re.DOTALL)
LANGUAGE_LINE = re.compile(r"^language:\s*.*$", re.MULTILINE)


def detect_language(text: str, rel: str) -> str:
    if rel in KNOWN_ZH:
        return "zh"
    # Strip frontmatter to avoid false positives on "name: ..." metadata.
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    han_chars = sum(1 for ch in body if "一" <= ch <= "鿿")
    ascii_alpha = sum(1 for ch in body if ch.isascii() and ch.isalpha())
    if han_chars > 200 and han_chars > ascii_alpha * 0.4:
        return "zh"
    return "en"


def is_in_submodule(path: Path) -> bool:
    return any(s in path.parents or path == s for s in SUBMODULE_PATHS)


def patch(text: str, lang: str) -> tuple[str, bool]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return text, False
    head, fm, tail = m.group(1), m.group(2), m.group(3)
    if LANGUAGE_LINE.search(fm):
        new_fm = LANGUAGE_LINE.sub(f"language: {lang}", fm, count=1)
    else:
        new_fm = fm.rstrip() + f"\nlanguage: {lang}"
    if new_fm == fm:
        return text, False
    return head + new_fm + tail + text[m.end():], True


def main() -> int:
    changed = 0
    by_lang = {"en": 0, "zh": 0}
    for skill_file in sorted(SKILLS_DIR.rglob("SKILL.md")):
        if is_in_submodule(skill_file):
            continue
        rel = str(skill_file.parent.relative_to(SKILLS_DIR))
        text = skill_file.read_text(encoding="utf-8")
        lang = detect_language(text, rel)
        new_text, was_changed = patch(text, lang)
        if was_changed:
            skill_file.write_text(new_text, encoding="utf-8")
            changed += 1
        by_lang[lang] += 1

    print(f"Patched: {changed}")
    print(f"Distribution: en={by_lang['en']}, zh={by_lang['zh']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
