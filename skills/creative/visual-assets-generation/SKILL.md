---
name: visual-assets-generation
description: Generate visual assets (ASCII art, diagrams, banners) for repos and documentation
tags: [ascii-art, diagrams, visualization, documentation, marketing]
related_skills: [architecture-diagram, ascii-art, excalidraw]
origin: unknown
source_license: see upstream
language: en
---

# Visual Assets Generation

Generate visual assets for repositories and documentation — ASCII art, diagrams, banners, social cards.

## When to Use

- User asks "bikin gambar", "buat visual", "generate banner"
- Repo needs visual improvements (README header, architecture diagram)
- Social media sharing (Twitter/LinkedIn cards)
- Documentation needs diagrams (workflow, architecture, comparison)

## Workflow

### Step 1: Create ASCII Preview First ⭐

**ALWAYS create TXT preview before generating real images:**

**Why:**
- Faster iteration (no image generation wait)
- User can review before committing
- Works everywhere (no image dependencies)
- Easy to edit and refine

**Format:**
```
VISUAL_ASSETS_PREVIEW.txt
├── ASCII Art Banner
├── Architecture Diagram
├── Workflow Diagram
├── Comparison Tables
├── Folder Structure
├── Performance Metrics
├── Quick Start Guide
└── Social Media Preview
```

---

### Step 2: Generate Comprehensive Preview

Include multiple visual types in one file:

1. **ASCII Art Banner/Logo**
   - Use box-drawing characters (╔═╗║╚╝)
   - Use block characters (█▀▄▌▐)
   - Include tagline and URL

2. **Architecture Diagram**
   - System components
   - Data flow (arrows: → ↓ ↑ ←)
   - Integration points

3. **Workflow Diagram**
   - Step-by-step process
   - Decision points
   - Outcomes

4. **Comparison Tables**
   - Feature comparison
   - Before/After
   - Options comparison

5. **Folder Structure**
   - Tree view (├── └── │)
   - Annotations
   - Purpose explanations

6. **Performance Metrics**
   - Bar charts (█ blocks)
   - Speed comparisons
   - Size comparisons

7. **Quick Start Guide**
   - Installation steps
   - Usage examples
   - Success criteria

8. **Social Media Preview**
   - Title + tagline
   - Key features (emoji bullets)
   - Call to action
   - URL

---

### Step 3: Offer Options

After creating preview, present choices:

**Option A: Use ASCII Directly**
```bash
# Add to README.md
cat VISUAL_ASSETS_PREVIEW.txt >> README.md
```
- ✅ Works everywhere
- ✅ No dependencies
- ✅ Easy to maintain
- ❌ Less visually appealing

**Option B: Convert to Real Images**
- SVG architecture diagram (dark theme)
- PNG social card (1200x630)
- PNG banner (for README header)
- ✅ Professional appearance
- ✅ Better for social sharing
- ❌ Requires image generation
- ❌ Harder to maintain

**Option C: Both** ⭐ **RECOMMENDED**
- ASCII in README (works everywhere)
- Real images in `/assets` folder
- Best of both worlds

---

## Templates

### ASCII Art Banner

**Box-drawing style:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    PROJECT NAME                             │
│                  Tagline goes here                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Block character style:**
```
███╗   ███╗██╗   ██╗    ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
████╗ ████║╚██╗ ██╔╝    ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
██╔████╔██║ ╚████╔╝     ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   
██║╚██╔╝██║  ╚██╔╝      ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   
██║ ╚═╝ ██║   ██║       ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   
╚═╝     ╚═╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   
```

---

### Architecture Diagram

```
                                USER
                                 │
                                 │ Request
                                 ▼
                ┌────────────────────────────────┐
                │                                │
                │      COMPONENT A               │
                │   (Description)                │
                │                                │
                └────────────────────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
    ┌───────────────────┐           ┌───────────────────┐
    │                   │           │                   │
    │   COMPONENT B     │           │   COMPONENT C     │
    │   (Description)   │           │   (Description)   │
    │                   │           │                   │
    └───────────────────┘           └───────────────────┘
                │                                 │
                └────────────────┬────────────────┘
                                 │
                                 ▼
                ┌────────────────────────────────┐
                │                                │
                │      OUTPUT                    │
                │   (Result)                     │
                │                                │
                └────────────────────────────────┘
```

---

### Comparison Table

```
┌──────────────────┬─────────────┬─────────────┬─────────────┐
│                  │   OPTION A  │   OPTION B  │   OPTION C  │
├──────────────────┼─────────────┼─────────────┼─────────────┤
│ Feature 1        │ ✅ Yes      │ ❌ No       │ ✅ Yes      │
│ Feature 2        │ ❌ No       │ ✅ Yes      │ ✅ Yes      │
│ Speed            │ Fast        │ Slow        │ Medium      │
│ Cost             │ Free        │ $10/mo      │ Free        │
└──────────────────┴─────────────┴─────────────┴─────────────┘
```

---

### Folder Structure

```
project-root/
├── src/                    # Source code
│   ├── components/         # React components
│   └── utils/              # Utility functions
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                   # Documentation
│   ├── README.md           # Main docs
│   └── API.md              # API reference
├── .github/                # GitHub config
│   ├── workflows/          # CI/CD
│   └── ISSUE_TEMPLATE/     # Issue templates
└── package.json            # Dependencies
```

---

### Performance Metrics

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  SPEED COMPARISON                                           │
│                                                             │
│  Option A:     ████ 2ms                                     │
│  Option B:     ████████████████████████████ 1000ms          │
│                                                             │
│  Speed Improvement: 500x faster                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Pitfalls

### ❌ DON'T: Generate Images Without Preview

**Problem:** User can't review before committing, wastes time if design needs changes.

**Solution:**
- Create TXT preview first
- Get user approval
- Then generate real images

---

### ❌ DON'T: Use Complex Unicode That Breaks

**Problem:** Some terminals don't support all Unicode characters.

**Solution:**
- Test in common terminals (bash, zsh, Windows Terminal)
- Use widely-supported box-drawing characters
- Provide fallback ASCII version

---

### ❌ DON'T: Make Diagrams Too Wide

**Problem:** Diagrams break on narrow terminals or mobile GitHub.

**Solution:**
- Keep width ≤ 80 characters (safe)
- Max 120 characters (acceptable)
- Test on mobile GitHub view

---

### ❌ DON'T: Forget to Include File Header

**Problem:** User doesn't know what the file contains or how to use it.

**Solution:**
```
# PROJECT NAME
# Visual Assets Preview

This file contains ASCII art previews for:
1. Banner/Logo
2. Architecture Diagram
3. Workflow Diagram
[...]

Generated: 2026-05-12
Repo: https://github.com/user/repo
```

---

## Examples

### Example 1: Simple Banner

**Input:** "bikin banner untuk repo mnemosyne-obsidian"

**Output:**
```
███╗   ███╗███╗   ██╗███████╗███╗   ███╗ ██████╗ ███████╗██╗   ██╗███╗   ██╗███████╗
████╗ ████║████╗  ██║██╔════╝████╗ ████║██╔═══██╗██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝
██╔████╔██║██╔██╗ ██║█████╗  ██╔████╔██║██║   ██║███████╗ ╚████╔╝ ██╔██╗ ██║█████╗  
██║╚██╔╝██║██║╚██╗██║██╔══╝  ██║╚██╔╝██║██║   ██║╚════██║  ╚██╔╝  ██║╚██╗██║██╔══╝  
██║ ╚═╝ ██║██║ ╚████║███████╗██║ ╚═╝ ██║╚██████╔╝███████║   ██║   ██║ ╚████║███████╗
╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝

                         + OBSIDIAN + GITHUB BACKUP
                   500x Faster Recall • Rich Markdown Notes
                        https://github.com/user/mnemosyne-obsidian
```

---

### Example 2: Architecture Diagram

**Input:** "bikin diagram arsitektur untuk integration tool"

**Output:**
```
                                    USER
                                     │
                                     │ "Show VPS cleanup"
                                     ▼
                    ┌────────────────────────────────┐
                    │                                │
                    │      HERMES AGENT              │
                    │   (AI Assistant)               │
                    │                                │
                    └────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
        ┌───────────────────────┐       ┌───────────────────────┐
        │                       │       │                       │
        │   MNEMOSYNE           │       │   OBSIDIAN            │
        │   (Fast Recall)       │       │   (Rich Content)      │
        │                       │       │                       │
        │ • SQLite DB (3.7MB)   │       │ • Markdown files      │
        │ • 500x faster         │       │ • Wikilinks           │
        │ • Temporal scoring    │       │ • Database views      │
        │                       │       │                       │
        └───────────────────────┘       └───────────────────────┘
                    │                                 │
                    └────────────────┬────────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │                                │
                    │      GITHUB BACKUP             │
                    │   (Version Control)            │
                    │                                │
                    └────────────────────────────────┘
```

---

### Example 3: Comprehensive Preview File

**Input:** "bikin semua visual untuk repo"

**Output:** `VISUAL_ASSETS_PREVIEW.txt` with:
- ASCII art banner
- Architecture diagram
- Workflow diagram (5 steps)
- Features comparison table
- Installation comparison
- Folder structure
- Performance metrics
- Quick start guide
- Bundled skills list
- Badges & status
- Social media preview

**Size:** ~30 KB  
**Time:** 5 minutes  
**User can review:** All visuals in one file

---

## User Preference Pattern (from session 2026-05-12)

**User workflow:**
1. Asks for visual: "bikin gambar/banner/diagram"
2. Wants preview first: "buatkan contohnya dulu dalam file txt"
3. Reviews preview
4. Decides: use ASCII, generate images, or both

**Key insight:**
- User prefers TXT preview before committing to images
- Allows review and iteration without image generation overhead
- Can decide format after seeing content

---

## Related Skills

- `architecture-diagram` — Dark-themed SVG diagrams
- `ascii-art` — ASCII art generation (pyfiglet, cowsay)
- `excalidraw` — Hand-drawn style diagrams
- `sketch` — HTML mockups for social cards

---

## References

- Box-drawing characters: https://en.wikipedia.org/wiki/Box-drawing_character
- Block elements: https://en.wikipedia.org/wiki/Block_Elements
- ASCII art generators: https://patorjk.com/software/taag/
