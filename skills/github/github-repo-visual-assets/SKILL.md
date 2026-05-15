---
name: github-repo-visual-assets
description: Create professional visual assets for GitHub repositories — architecture diagrams, social cards, and README banners.
version: 1.0.0
author: Hermes Agent
license: MIT
dependencies: []
metadata:
  hermes:
    tags: [github, visual-assets, design, branding, documentation]
    related_skills: [architecture-diagram, comprehensive-public-repo-setup]
origin: original
source_repo: kevinnft/ai-agent-skills
source_url: https://github.com/kevinnft/ai-agent-skills
source_license: MIT
language: en
---

# GitHub Repository Visual Assets

Create professional visual assets for GitHub repositories to improve presentation, social sharing, and documentation quality.

## Scope

**Best suited for:**
- Open source projects needing professional branding
- Repositories requiring architecture documentation
- Projects optimized for social media sharing (Twitter, LinkedIn, Reddit)
- README files needing visual headers

**Assets covered:**
1. **Architecture Diagram** (1200x800px) — System architecture visualization
2. **Social Media Card** (1200x630px) — Twitter/LinkedIn/GitHub social preview
3. **README Banner** (1200x300px) — Repository header image

## Design System

### Color Palette

Use semantic color mapping for technical components:

| Component Type | Fill (rgba) | Stroke (Hex) | Use Case |
|----------------|-------------|--------------|----------|
| **Frontend/Agent** | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan-400) | UI, client-side, agents |
| **Backend/Storage** | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) | APIs, servers, storage |
| **Database/Backup** | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) | Databases, backups |
| **Cloud/External** | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) | Cloud services, external |

### Typography

- **Font:** JetBrains Mono (monospace) — loaded from Google Fonts
- **Sizes:**
  - Title: 48-56px
  - Subtitle: 20-24px
  - Body: 14-18px
  - Small: 9-13px

### Background

- **Primary:** `#0f172a` (slate-950)
- **Secondary:** `#1e293b` (slate-800)
- **Border:** `#334155` (slate-700)
- **Grid Pattern:** 40px grid with `#1e293b` lines

## Workflow

### Step 1: Create Assets Directory

```bash
mkdir -p assets/{diagrams,images,social}
```

### Step 2: Generate HTML Assets

Create three HTML files with inline CSS/SVG:

1. **Architecture Diagram** (`assets/diagrams/architecture.html`)
   - Size: 1200x800px
   - Shows system flow with components
   - Color-coded by type
   - Includes legend and info cards

2. **Social Media Card** (`assets/social/social-card.html`)
   - Size: 1200x630px (Twitter/LinkedIn standard)
   - Logo + title + tagline
   - Key features (4 items)
   - Badges (version, license, status)

3. **README Banner** (`assets/images/banner.html`)
   - Size: 1200x300px
   - Wide banner format
   - Logo + title + subtitle + badges

### Step 3: Review Before Pushing

**CRITICAL:** Always let user review visual assets before pushing to GitHub.

**Review workflow:**
1. Generate HTML files
2. Send files to user (via MEDIA: or file path)
3. User opens in browser to review
4. Wait for approval or change requests
5. Only after approval: convert to PNG and push

**Why:** Visual assets represent the project's brand. User must approve design before it goes public.

### Step 4: Convert to PNG (After Approval)

Use headless browser to convert HTML to PNG:

```bash
# Chrome (recommended)
google-chrome --headless --screenshot=architecture.png --window-size=1200,800 assets/diagrams/architecture.html
google-chrome --headless --screenshot=social-card.png --window-size=1200,630 assets/social/social-card.html
google-chrome --headless --screenshot=banner.png --window-size=1200,300 assets/images/banner.html

# Firefox (alternative)
firefox --headless --screenshot architecture.png --window-size=1200,800 assets/diagrams/architecture.html
firefox --headless --screenshot social-card.png --window-size=1200,630 assets/social/social-card.html
firefox --headless --screenshot banner.png --window-size=1200,300 assets/images/banner.html

# Move PNGs to assets
mv architecture.png assets/diagrams/
mv social-card.png assets/social/
mv banner.png assets/images/
```

### Step 5: Update README

Add visual assets to README.md:

```markdown
![Banner](assets/images/banner.png)

# Project Title

Description...

## Architecture

![Architecture Diagram](assets/diagrams/architecture.png)
```

### Step 6: Upload Social Card to GitHub

1. Go to repository settings
2. Scroll to "Social preview"
3. Upload `assets/social/social-card.png`
4. Save

Now when shared on Twitter/LinkedIn, the card appears automatically.

## Asset Templates

### Architecture Diagram Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Architecture Diagram</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        /* Dark theme styles */
        body { font-family: 'JetBrains Mono', monospace; background: #020617; }
        /* Component boxes, arrows, legend */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>System Architecture</h1>
        </div>
        <div class="diagram-card">
            <svg viewBox="0 0 1200 800">
                <!-- Grid, arrows, components -->
            </svg>
        </div>
        <div class="info-grid">
            <!-- Info cards -->
        </div>
    </div>
</body>
</html>
```

### Social Card Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Social Card</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        /* 1200x630 card with gradient background */
        .card { width: 1200px; height: 630px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="content">
            <div class="header">
                <div class="icon">🧠</div>
                <h1>Project Title</h1>
            </div>
            <div class="tagline">Key value proposition</div>
            <div class="features">
                <!-- 4 feature boxes -->
            </div>
            <div class="footer">
                <!-- Badges + URL -->
            </div>
        </div>
    </div>
</body>
</html>
```

### Banner Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Banner</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        /* 1200x300 banner */
        .banner { width: 1200px; height: 300px; }
    </style>
</head>
<body>
    <div class="banner">
        <div class="content">
            <div class="logo-section">
                <div class="logo">🧠</div>
                <h1>Project Title</h1>
            </div>
            <div class="tagline">Key features</div>
            <div class="badges">
                <!-- Feature badges -->
            </div>
        </div>
    </div>
</body>
</html>
```

## Pitfalls

### 1. Pushing Without Review
**Problem:** User wants to review visual assets before they go public.  
**Solution:** Always send HTML files to user first, wait for approval, then convert and push.

### 2. Wrong Sizes
**Problem:** Social media platforms have specific size requirements.  
**Solution:** Use standard sizes:
- Architecture: 1200x800px
- Social card: 1200x630px (Twitter/LinkedIn/GitHub standard)
- Banner: 1200x300px

### 3. Missing Google Fonts
**Problem:** HTML files don't load fonts offline.  
**Solution:** Include Google Fonts CDN link in `<head>`. Files work offline after first load (browser cache).

### 4. Inconsistent Branding
**Problem:** Colors/fonts don't match across assets.  
**Solution:** Use the design system color palette and JetBrains Mono font consistently.

### 5. No Assets README
**Problem:** User doesn't know how to use the HTML files.  
**Solution:** Always create `assets/README.md` with:
- Directory structure
- How to view (open in browser)
- How to convert to PNG
- How to add to README
- Design system reference

## Related Skills

- **architecture-diagram** — For detailed SVG architecture diagrams
- **comprehensive-public-repo-setup** — For complete repo setup including visual assets
- **github-repo-management** — For managing GitHub repositories

## Examples

See `references/mnemosyne-obsidian-example.md` for a complete example from the mnemosyne-obsidian repository.
