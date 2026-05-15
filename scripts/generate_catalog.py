#!/usr/bin/env python3
"""Generate docs/categories.md from SKILL.md frontmatter.

Pulls name + description + origin + source_url + language from each
SKILL.md and emits a single, always-fresh catalog. Run before each
release.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
OUT = REPO_ROOT / "docs" / "categories.md"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def first(field: str, fm: str) -> str | None:
    m = re.search(rf"^{field}:\s*(.+)$", fm, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip().strip("\"'")
    if val in {">", "|", ">-", "|-"}:
        # YAML folded scalar — collect indented continuation.
        idx_line = next(
            i
            for i, line in enumerate(fm.split("\n"))
            if line.startswith(f"{field}:")
        )
        body = []
        for line in fm.split("\n")[idx_line + 1:]:
            if line.startswith(" ") or line.startswith("\t"):
                body.append(line.strip())
            else:
                break
        return " ".join(body)
    return val


def parse_skill(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm = m.group(1)
    return {
        "name": first("name", fm) or path.parent.name,
        "description": first("description", fm) or "",
        "origin": first("origin", fm) or "unknown",
        "source_url": first("source_url", fm) or "",
        "language": first("language", fm) or "en",
        "path": str(path.parent.relative_to(SKILLS_DIR)),
    }


def short(desc: str, limit: int = 140) -> str:
    desc = re.sub(r"\s+", " ", desc).strip()
    if len(desc) <= limit:
        return desc
    return desc[: limit - 1].rstrip(",.;: ") + "…"


def origin_badge(origin: str) -> str:
    return {
        "aggregated": "🟦",
        "original": "🟩",
        "adapted": "🟧",
        "unknown": "🟥",
    }.get(origin, "⬜")


def build() -> str:
    skills_by_cat: dict[str, list[dict]] = defaultdict(list)
    total = 0
    for path in sorted(SKILLS_DIR.rglob("SKILL.md")):
        skill = parse_skill(path)
        if not skill:
            continue
        category = skill["path"].split("/")[0]
        skills_by_cat[category].append(skill)
        total += 1

    out = []
    out.append("# Categories Overview\n")
    out.append("Auto-generated catalog of every skill, grouped by category.")
    out.append(
        "Run `python3 scripts/generate_catalog.py` to refresh after editing "
        "frontmatter.\n"
    )
    out.append(
        f"**Totals:** {total} skills across {len(skills_by_cat)} categories.\n"
    )
    out.append("Legend: 🟦 aggregated · 🟩 original · 🟧 adapted · 🟥 unknown · 🇨🇳 zh\n")
    out.append("---\n")

    for category in sorted(skills_by_cat, key=lambda c: (-len(skills_by_cat[c]), c)):
        skills = sorted(skills_by_cat[category], key=lambda s: s["name"])
        out.append(f"## `{category}/` — {len(skills)} skill(s)\n")
        out.append("| Skill | Description | Origin |")
        out.append("|---|---|:--:|")
        for s in skills:
            badge = origin_badge(s["origin"])
            lang_flag = " 🇨🇳" if s["language"] == "zh" else ""
            link = (
                f"[{s['name']}]({s['source_url']})"
                if s["source_url"].startswith("http")
                else f"`{s['name']}`"
            )
            out.append(
                f"| {link}{lang_flag} | {short(s['description'])} | {badge} |"
            )
        out.append("")

    out.append("---")
    out.append(
        "_Last regenerated automatically. Edit `SKILL.md` frontmatter, then "
        "run `python3 scripts/generate_catalog.py`._"
    )
    return "\n".join(out) + "\n"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
