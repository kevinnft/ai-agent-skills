# Mnemosyne + Obsidian Visual Assets Example

This is a complete example of visual assets created for the mnemosyne-obsidian repository.

## Project Context

**Repository:** https://github.com/kevinnft/mnemosyne-obsidian  
**Purpose:** Integration tool combining Mnemosyne (AI memory), Obsidian (knowledge base), and GitHub (backup)  
**Key Features:**
- 500x faster recall (2ms average)
- Rich markdown notes with wikilinks
- Automatic GitHub backup
- 5 bundled Obsidian skills

## Assets Created

### 1. Architecture Diagram (1200x800px)

**File:** `assets/diagrams/architecture.html`  
**Size:** 13.7 KB

**Components shown:**
- USER (top) — gray external component
- HERMES AGENT (center) — cyan frontend/agent
- MNEMOSYNE (left) — cyan fast recall system
- OBSIDIAN (right) — emerald rich content system
- GITHUB BACKUP (bottom) — violet database/backup

**Flow:**
1. User → Hermes Agent
2. Hermes → Mnemosyne (fast recall) + Obsidian (rich content)
3. Both → GitHub (automatic backup)

**Features:**
- Dark grid background
- Color-coded arrows (cyan, emerald, violet)
- Component details (features, specs)
- Legend at bottom
- 3 info cards below diagram

### 2. Social Media Card (1200x630px)

**File:** `assets/social/social-card.html`  
**Size:** 7.0 KB

**Content:**
- Logo: 🧠 (brain emoji)
- Title: "Mnemosyne + Obsidian"
- Subtitle: "Integration Tool"
- Tagline: "AI memory system with 500x faster recall, automatic GitHub backup, and rich markdown notes"
- 4 feature boxes:
  - ⚡ 500x Faster Recall (2ms average query time)
  - 📝 Rich Markdown Notes (Wikilinks, databases, diagrams)
  - ☁️ Auto GitHub Backup (Version control & multi-device sync)
  - 🎯 One-Command Install (Production-ready in 1 minute)
- Footer badges: v1.1.0, MIT License, Production Ready
- URL: github.com/kevinnft/mnemosyne-obsidian

**Design:**
- Gradient background (slate-900 to slate-800)
- Radial gradient overlays (cyan + violet)
- Feature boxes with colored icons
- Professional, clean layout

### 3. README Banner (1200x300px)

**File:** `assets/images/banner.html`  
**Size:** 4.6 KB

**Content:**
- Logo: 🧠 (80x80px, gradient background)
- Title: "Mnemosyne + Obsidian" (56px)
- Subtitle: "Integration Tool for AI Memory & Knowledge Management"
- Tagline: "500x faster recall • Rich markdown notes • Automatic GitHub backup"
- 5 badges:
  - ⚡ 2ms Recall Time
  - 📝 5 Skills Bundled
  - ☁️ Auto Backup
  - ✅ Production Ready
  - 🔓 MIT License

**Design:**
- Wide banner format (1200x300)
- Gradient background with radial overlays
- Horizontal layout (logo left, content right)
- Badge row at bottom

## Design System Used

### Colors

| Component | Color | Hex | Usage |
|-----------|-------|-----|-------|
| Frontend/Agent | Cyan | `#22d3ee` | Hermes Agent, Mnemosyne |
| Backend/Storage | Emerald | `#34d399` | Obsidian |
| Database/Backup | Violet | `#a78bfa` | GitHub |
| External | Slate | `#94a3b8` | User |

### Typography

- **Font:** JetBrains Mono (monospace)
- **Title:** 48-56px, weight 700
- **Subtitle:** 20-24px, weight 400
- **Body:** 14-18px, weight 400
- **Small:** 9-13px, weight 400

### Background

- **Primary:** `#0f172a` (slate-950)
- **Secondary:** `#1e293b` (slate-800)
- **Border:** `#334155` (slate-700)
- **Grid:** 40px with `#1e293b` lines

## Workflow Used

1. **Created assets directory:**
   ```bash
   mkdir -p assets/{diagrams,images,social}
   ```

2. **Generated HTML files:**
   - architecture.html (13.7 KB)
   - social-card.html (7.0 KB)
   - banner.html (4.6 KB)

3. **Created assets README:**
   - Directory structure
   - How to view/convert
   - Design system reference
   - Usage instructions

4. **Sent to user for review:**
   - Via MEDIA: in Telegram
   - User reviews in browser
   - Waits for approval before pushing

5. **After approval (not done yet):**
   - Convert HTML to PNG via headless Chrome
   - Add PNGs to README
   - Upload social card to GitHub settings
   - Commit and push

## Key Learnings

### 1. Review Before Push
User wants to review visual assets before they go public. Always send HTML files first, wait for approval.

### 2. HTML Works Well
HTML with inline CSS/SVG is perfect for:
- Easy to generate (no external tools)
- Works in any browser
- Can be converted to PNG
- Small file size (< 15 KB each)

### 3. Standard Sizes Matter
- Architecture: 1200x800px (good for docs)
- Social card: 1200x630px (Twitter/LinkedIn/GitHub standard)
- Banner: 1200x300px (wide format for README)

### 4. Design System Consistency
Using consistent colors, fonts, and layout across all assets creates professional branding.

### 5. Assets README Essential
Users need instructions on how to use HTML files. Always include `assets/README.md` with:
- How to view (open in browser)
- How to convert to PNG
- How to add to README
- Design system reference

## File Sizes

| File | Size | Type |
|------|------|------|
| architecture.html | 13.7 KB | HTML+SVG |
| social-card.html | 7.0 KB | HTML+CSS |
| banner.html | 4.6 KB | HTML+CSS |
| README.md | 6.1 KB | Markdown |
| **Total** | **31.4 KB** | **Very small!** |

## Result

Professional visual assets created in < 5 minutes, ready for review. User can open in browser, see exactly how they look, and approve before pushing to public repo.

**Status:** Awaiting user approval (as of 2026-05-12).
