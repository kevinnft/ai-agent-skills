#!/usr/bin/env python3
"""Generate docs/index.html — a searchable single-page skill catalog for GitHub Pages.

Reads all SKILL.md files under skills/, parses YAML frontmatter, and produces
a modern dark-themed HTML page with inline CSS+JS (zero external dependencies).
"""
from __future__ import annotations

import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
OUT = REPO_ROOT / "docs" / "index.html"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def first(field: str, fm: str) -> str | None:
    m = re.search(rf"^{field}:\s*(.+)$", fm, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip().strip("\"'")
    if val in {">", "|", ">-", "|-"}:
        idx_line = next(
            i for i, line in enumerate(fm.split("\n"))
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


def parse_tags(fm: str) -> list[str]:
    m = re.search(r"^tags:\s*\[(.+?)\]", fm, re.MULTILINE)
    if m:
        return [t.strip().strip("\"'") for t in m.group(1).split(",") if t.strip()]
    # Try multiline list format
    m = re.search(r"^tags:\s*$", fm, re.MULTILINE)
    if m:
        tags = []
        start = fm.find("tags:")
        for line in fm[start:].split("\n")[1:]:
            if line.strip().startswith("- "):
                tags.append(line.strip()[2:].strip().strip("\"'"))
            elif line.strip() == "":
                continue
            else:
                break
        return tags
    return []


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
        "source_repo": first("source_repo", fm) or "",
        "source_license": first("source_license", fm) or "",
        "author": first("author", fm) or "",
        "language": first("language", fm) or "en",
        "tags": parse_tags(fm),
        "category": str(path.relative_to(SKILLS_DIR)).split("/")[0],
    }


def short(desc: str, limit: int = 160) -> str:
    desc = re.sub(r"\s+", " ", desc).strip()
    if len(desc) <= limit:
        return desc
    return desc[: limit - 1].rstrip(",.;: ") + "…"


def build_html(skills: list[dict], categories: dict[str, int]) -> str:
    skills_json = json.dumps(skills, ensure_ascii=False)
    sorted_cats = sorted(categories.items(), key=lambda x: (-x[1], x[0]))
    total = len(skills)
    all_tags = sorted(set(t for s in skills for t in s["tags"]))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Agent Skills Catalog</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0d1117;--surface:#161b22;--surface2:#21262d;--border:#30363d;
  --text:#e6edf3;--text-muted:#8b949e;--accent:#58a6ff;--accent2:#3fb950;
  --accent3:#d2a8ff;--radius:8px;--shadow:0 2px 8px rgba(0,0,0,.3);
}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}}
a{{color:var(--accent);text-decoration:none}}
a:hover{{text-decoration:underline}}

/* Layout */
.layout{{display:grid;grid-template-columns:260px 1fr;min-height:100vh}}
@media(max-width:900px){{.layout{{grid-template-columns:1fr}}.sidebar{{display:none}}.mobile-toggle{{display:flex!important}}}}

/* Header */
header{{grid-column:1/-1;background:var(--surface);border-bottom:1px solid var(--border);
  padding:1.2rem 2rem;display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap}}
header h1{{font-size:1.4rem;font-weight:700;white-space:nowrap}}
header h1 span{{color:var(--accent)}}
.stats{{color:var(--text-muted);font-size:.85rem;white-space:nowrap}}

/* Search */
.search-wrap{{flex:1;min-width:200px;max-width:500px;position:relative}}
.search-wrap input{{width:100%;padding:.6rem 1rem .6rem 2.4rem;border-radius:var(--radius);
  border:1px solid var(--border);background:var(--surface2);color:var(--text);font-size:.9rem;
  outline:none;transition:border-color .2s}}
.search-wrap input:focus{{border-color:var(--accent)}}
.search-wrap svg{{position:absolute;left:.7rem;top:50%;transform:translateY(-50%);
  width:16px;height:16px;fill:var(--text-muted)}}

/* Sidebar */
.sidebar{{background:var(--surface);border-right:1px solid var(--border);padding:1.2rem 0;
  overflow-y:auto;position:sticky;top:0;height:100vh}}
.sidebar h3{{padding:0 1.2rem;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;
  color:var(--text-muted);margin-bottom:.5rem}}
.sidebar ul{{list-style:none}}
.sidebar li a{{display:flex;justify-content:space-between;padding:.4rem 1.2rem;
  font-size:.85rem;color:var(--text-muted);transition:all .15s;border-left:3px solid transparent}}
.sidebar li a:hover,.sidebar li a.active{{color:var(--text);background:var(--surface2);
  border-left-color:var(--accent);text-decoration:none}}
.sidebar .count{{font-size:.75rem;background:var(--surface2);padding:1px 6px;border-radius:10px}}
.sidebar li a.active .count{{background:var(--accent);color:var(--bg)}}

/* Mobile toggle */
.mobile-toggle{{display:none;position:fixed;bottom:1.5rem;right:1.5rem;z-index:100;
  width:48px;height:48px;border-radius:50%;background:var(--accent);color:var(--bg);
  align-items:center;justify-content:center;border:none;cursor:pointer;box-shadow:var(--shadow);
  font-size:1.2rem}}
.mobile-menu{{display:none;position:fixed;inset:0;z-index:99;background:var(--surface);
  padding:2rem;overflow-y:auto}}
.mobile-menu.open{{display:block}}

/* Main */
main{{padding:1.5rem 2rem 3rem}}
@media(max-width:900px){{main{{padding:1rem}}}}
.filter-bar{{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.2rem}}
.filter-btn{{padding:.3rem .7rem;border-radius:20px;border:1px solid var(--border);
  background:transparent;color:var(--text-muted);font-size:.78rem;cursor:pointer;transition:all .15s}}
.filter-btn:hover{{border-color:var(--accent);color:var(--accent)}}
.filter-btn.active{{background:var(--accent);border-color:var(--accent);color:var(--bg)}}

/* Grid */
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1rem}}
@media(max-width:600px){{.grid{{grid-template-columns:1fr}}}}

/* Cards */
.card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:1.2rem;transition:border-color .2s,transform .15s;display:flex;flex-direction:column;gap:.6rem}}
.card:hover{{border-color:var(--accent);transform:translateY(-2px)}}
.card-header{{display:flex;align-items:flex-start;justify-content:space-between;gap:.5rem}}
.card-name{{font-weight:600;font-size:.95rem;word-break:break-word}}
.card-origin{{font-size:.7rem;padding:2px 8px;border-radius:10px;white-space:nowrap;font-weight:500}}
.origin-aggregated{{background:rgba(88,166,255,.15);color:var(--accent)}}
.origin-original{{background:rgba(63,185,80,.15);color:var(--accent2)}}
.origin-adapted{{background:rgba(210,168,255,.15);color:var(--accent3)}}
.origin-unknown{{background:var(--surface2);color:var(--text-muted)}}
.card-desc{{font-size:.85rem;color:var(--text-muted);flex:1}}
.card-meta{{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}}
.card-cat{{font-size:.72rem;color:var(--accent);background:rgba(88,166,255,.08);
  padding:2px 7px;border-radius:4px}}
.card-tag{{font-size:.7rem;color:var(--text-muted);background:var(--surface2);
  padding:1px 6px;border-radius:4px}}
.card-link{{font-size:.78rem;margin-top:.3rem}}

/* Empty state */
.empty{{text-align:center;padding:4rem 1rem;color:var(--text-muted)}}
.empty svg{{width:48px;height:48px;fill:var(--text-muted);margin-bottom:1rem}}
.empty p{{font-size:1.1rem}}

/* Scrollbar */
::-webkit-scrollbar{{width:8px}}
::-webkit-scrollbar-track{{background:var(--bg)}}
::-webkit-scrollbar-thumb{{background:var(--border);border-radius:4px}}
::-webkit-scrollbar-thumb:hover{{background:var(--text-muted)}}
</style>
</head>
<body>
<div class="layout">
<header>
  <h1>🤖 <span>AI Agent Skills</span> Catalog</h1>
  <div class="stats">{total} skills · {len(sorted_cats)} categories</div>
  <div class="search-wrap">
    <svg viewBox="0 0 16 16"><path d="M11.5 7a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Zm-.82 4.74a6 6 0 1 1 1.06-1.06l3.04 3.04a.75.75 0 1 1-1.06 1.06l-3.04-3.04Z"/></svg>
    <input type="text" id="search" placeholder="Search skills by name, description, tag..." autocomplete="off">
  </div>
</header>

<aside class="sidebar" id="sidebar">
  <h3>Categories</h3>
  <ul>
    <li><a href="#" data-cat="all" class="active">All Skills <span class="count">{total}</span></a></li>
    {"".join(f'<li><a href="#" data-cat="{html.escape(cat)}">{html.escape(cat)} <span class="count">{count}</span></a></li>' for cat, count in sorted_cats)}
  </ul>
</aside>

<main>
  <div class="filter-bar" id="filterBar">
    <button class="filter-btn active" data-origin="all">All Origins</button>
    <button class="filter-btn" data-origin="aggregated">🟦 Aggregated</button>
    <button class="filter-btn" data-origin="original">🟩 Original</button>
    <button class="filter-btn" data-origin="adapted">🟧 Adapted</button>
  </div>
  <div class="grid" id="grid"></div>
  <div class="empty" id="empty" style="display:none">
    <svg viewBox="0 0 16 16"><path d="M11.5 7a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Zm-.82 4.74a6 6 0 1 1 1.06-1.06l3.04 3.04a.75.75 0 1 1-1.06 1.06l-3.04-3.04Z"/></svg>
    <p>No skills match your search.</p>
  </div>
</main>
</div>

<button class="mobile-toggle" id="mobileToggle" aria-label="Toggle categories">☰</button>
<div class="mobile-menu" id="mobileMenu">
  <h3 style="color:var(--text-muted);font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;margin-bottom:1rem">Categories</h3>
  <ul style="list-style:none">
    <li style="margin-bottom:.5rem"><a href="#" data-cat="all" style="color:var(--text);font-size:.9rem">All Skills ({total})</a></li>
    {"".join(f'<li style="margin-bottom:.5rem"><a href="#" data-cat="{html.escape(cat)}" style="color:var(--text-muted);font-size:.9rem">{html.escape(cat)} ({count})</a></li>' for cat, count in sorted_cats)}
  </ul>
</div>

<script>
(function(){{
const skills={skills_json};
const grid=document.getElementById('grid');
const empty=document.getElementById('empty');
const searchInput=document.getElementById('search');
const sidebar=document.getElementById('sidebar');
const filterBar=document.getElementById('filterBar');
const mobileToggle=document.getElementById('mobileToggle');
const mobileMenu=document.getElementById('mobileMenu');

let currentCat='all';
let currentOrigin='all';
let searchTerm='';

function originClass(o){{return'origin-'+(o||'unknown')}}

function renderCard(s){{
  const tags=s.tags.map(t=>`<span class="card-tag">${{esc(t)}}</span>`).join('');
  const link=s.source_url&&s.source_url.startsWith('http')
    ?`<div class="card-link"><a href="${{esc(s.source_url)}}" target="_blank" rel="noopener">View source →</a></div>`:'';
  return`<div class="card">
    <div class="card-header">
      <span class="card-name">${{esc(s.name)}}</span>
      <span class="card-origin ${{originClass(s.origin)}}">${{esc(s.origin)}}</span>
    </div>
    <div class="card-desc">${{esc(s.description)}}</div>
    <div class="card-meta">
      <span class="card-cat">${{esc(s.category)}}</span>${{tags}}
    </div>
    ${{link}}
  </div>`;
}}

function esc(s){{
  const d=document.createElement('div');d.textContent=s||'';return d.innerHTML;
}}

function render(){{
  const term=searchTerm.toLowerCase();
  const filtered=skills.filter(s=>{{
    if(currentCat!=='all'&&s.category!==currentCat)return false;
    if(currentOrigin!=='all'&&s.origin!==currentOrigin)return false;
    if(term){{
      const haystack=(s.name+' '+s.description+' '+s.tags.join(' ')+' '+s.category).toLowerCase();
      return haystack.includes(term);
    }}
    return true;
  }});
  if(filtered.length===0){{
    grid.innerHTML='';empty.style.display='block';
  }}else{{
    empty.style.display='none';
    grid.innerHTML=filtered.map(renderCard).join('');
  }}
}}

// Search
let debounce;
searchInput.addEventListener('input',function(){{
  clearTimeout(debounce);
  debounce=setTimeout(()=>{{searchTerm=this.value;render();}},150);
}});

// Category sidebar
sidebar.addEventListener('click',function(e){{
  const a=e.target.closest('a[data-cat]');
  if(!a)return;
  e.preventDefault();
  currentCat=a.dataset.cat;
  sidebar.querySelectorAll('a').forEach(x=>x.classList.remove('active'));
  a.classList.add('active');
  render();
}});

// Origin filter
filterBar.addEventListener('click',function(e){{
  const btn=e.target.closest('.filter-btn');
  if(!btn)return;
  currentOrigin=btn.dataset.origin;
  filterBar.querySelectorAll('.filter-btn').forEach(x=>x.classList.remove('active'));
  btn.classList.add('active');
  render();
}});

// Mobile menu
mobileToggle.addEventListener('click',()=>{{
  mobileMenu.classList.toggle('open');
}});
mobileMenu.addEventListener('click',function(e){{
  const a=e.target.closest('a[data-cat]');
  if(!a)return;
  e.preventDefault();
  currentCat=a.dataset.cat;
  mobileMenu.classList.remove('open');
  render();
}});

// Initial render
render();
}})();
</script>
</body>
</html>"""


def main() -> int:
    skills = []
    categories: dict[str, int] = defaultdict(int)

    for path in sorted(SKILLS_DIR.rglob("SKILL.md")):
        skill = parse_skill(path)
        if not skill:
            continue
        skill["description"] = short(skill["description"])
        skills.append(skill)
        categories[skill["category"]] += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_html(skills, categories), encoding="utf-8")
    print(f"✓ Generated {OUT.relative_to(REPO_ROOT)} — {len(skills)} skills, {len(categories)} categories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
