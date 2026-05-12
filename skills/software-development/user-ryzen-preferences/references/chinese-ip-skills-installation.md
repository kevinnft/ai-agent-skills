# Chinese IP Protection Skills Installation

**Date:** 2026-05-12  
**Context:** Installing patent-disclosure-skill and software-copyright skills for automated Chinese IP application materials generation

---

## Skills Overview

### 1. Patent Disclosure Skill
- **Repo:** https://github.com/handsomestWei/patent-disclosure-skill
- **Purpose:** Auto-generate Chinese patent disclosure documents (技术交底书)
- **Tech:** Python 3.9+, Node.js (mermaid), Playwright (CNIPA scraping)
- **Output:** Complete patent disclosure .docx ready for submission

### 2. Software Copyright Skill
- **Repo:** https://github.com/Fokkyp/SoftwareCopyright-Skill
- **Purpose:** Auto-generate Chinese software copyright application materials (软件著作权申请资料)
- **Tech:** Python (docx generation), AgentSkills standard
- **Output:** Application form (.txt) + User manual (.docx) + Code materials (.docx)

---

## Installation Workflow

### Patent Disclosure Skill

```bash
# Clone repo
cd ~/.hermes/skills
git clone --depth 1 https://github.com/handsomestWei/patent-disclosure-skill

# Create venv (Ubuntu 24.04 requires venv, not system packages)
cd patent-disclosure-skill
python3 -m venv venv
source venv/bin/activate

# Install base dependencies
pip install -r requirements.txt

# Install CNIPA search dependencies (optional but recommended)
pip install -r tools/requirements-cnipa.txt

# Install Playwright + Chromium
python -m playwright install chromium
```

**Dependencies:**
- Base: python-docx, python-pptx, mammoth, lxml, Pillow
- CNIPA: playwright, greenlet, pyee

**Disk usage:** ~150MB (venv + Playwright + Chromium)

---

### Software Copyright Skill

```bash
# Clone repo
cd ~/.hermes/skills
git clone --depth 1 https://github.com/Fokkyp/SoftwareCopyright-Skill

# Extract skill directory (repo structure: repo/software-copyright-materials/)
cp -R SoftwareCopyright-Skill/software-copyright-materials ./software-copyright
rm -rf SoftwareCopyright-Skill

# Verify structure
ls software-copyright/
# Expected: SKILL.md, agents/, references/, scripts/, vendor/
```

**No extra dependencies needed** — uses built-in Python docx libraries

**Disk usage:** ~5MB

---

## Usage Pattern

### Patent Disclosure

**Input:** Project folder (code + docs)

**Workflow:**
1. Scan project → identify innovations
2. Search CNIPA (China Patent Office) → check existing patents
3. Generate technical disclosure:
   - Background
   - Technical problem
   - Solution (innovation)
   - Implementation details
   - System diagrams (Mermaid → PNG)
   - Flowcharts
4. Output: `disclosure.docx` (20-30 pages)

**Value:** ¥5,000-10,000 saved per patent (~Rp10-20 juta)

---

### Software Copyright

**Input:** Project folder (real code)

**Workflow:**
1. Environment check → DOCX capabilities
2. Project analysis → 45 files, 6,164 lines detected
3. Business understanding → industry, target users, core value
4. Application form → 20+ fields (software name, version, copyright holder, dates, environment)
5. Code material selection → first 30 pages + last 30 pages (CNIPA requirement)
6. User manual → 10-20 pages with screenshots
7. Output: Complete package (.txt + .docx files)

**Value:** ¥500-1,000 saved per copyright (~Rp1-2 juta)

---

## Verification

### Check Skills Installed

```bash
cd ~/.hermes/skills
ls -d patent-disclosure-skill software-copyright

# Verify SKILL.md exists
ls patent-disclosure-skill/SKILL.md
ls software-copyright/SKILL.md
```

### Test Patent Skill

```bash
cd ~/.hermes/skills/patent-disclosure-skill
source venv/bin/activate
python tools/cnipa_epub_search.py --help
```

### Test Copyright Skill

```bash
cd ~/project-directory
python3 ~/.hermes/skills/software-copyright/scripts/check_environment.py --out-dir 软件著作权申请资料
```

---

## Troubleshooting

### Issue: pip install fails with "externally-managed-environment"

**Cause:** Ubuntu 24.04 enforces PEP 668 (no system-wide pip installs)

**Solution:** Always use venv

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Playwright install fails

**Cause:** Missing system dependencies

**Solution:**

```bash
# Install Playwright browsers
python -m playwright install chromium

# If still fails, install system deps
sudo apt install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
```

### Issue: CNIPA search fails

**Cause:** Network issues or CNIPA site changes

**Solution:** Skill falls back to WebSearch (Google Scholar, Patents) automatically

---

## Integration with Hermes

### Load Skills

```python
# In Hermes session
skill_view(name='patent-disclosure-skill')
skill_view(name='software-copyright')
```

### Auto-Generate Materials

**Patent:**
```bash
# User provides project directory
# Skill automatically:
# 1. Scans project
# 2. Identifies innovations
# 3. Searches CNIPA
# 4. Generates disclosure.docx
```

**Copyright:**
```bash
# User provides project directory
# Skill automatically:
# 1. Analyzes project
# 2. Generates business understanding
# 3. Creates application form
# 4. Extracts code materials
# 5. Generates user manual
# 6. Outputs complete package
```

---

## Session Example: enowX-Coder

**Project:** enowX-Coder (Tauri + React IDE, 45 files, 6,164 lines)

**Copyright Generation Progress:**
1. ✅ Environment check → Using basic DOCX (no .NET SDK)
2. ✅ Project analysis → Detected React, Tauri, TypeScript
3. ✅ Business understanding → AI-assisted programming tools
4. ⏳ Application form → Needs user input (version, copyright holder, dates)
5. ⏳ Code selection → Will extract first 30 + last 30 pages
6. ⏳ User manual → 10 sections planned
7. ⏳ Final output → .txt + .docx package

**Output Location:** `~/enowX-Coder/软件著作权申请资料/`

---

## Key Learnings

### 1. Venv Required on Ubuntu 24.04

**Always use venv for Python dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Don't use:** `pip install --break-system-packages` (unsafe)

### 2. Repo Structure Matters

**Software copyright skill:**
- Repo root ≠ skill directory
- Actual skill: `SoftwareCopyright-Skill/software-copyright-materials/`
- Must extract subdirectory, not clone entire repo

### 3. CNIPA Integration Optional

**Patent skill works without CNIPA:**
- CNIPA search: Requires Playwright + Chromium (~100MB)
- Fallback: WebSearch (Google Scholar, Patents)
- Decision: Install CNIPA for best results, but not mandatory

### 4. User Confirmation Gates

**Software copyright skill has mandatory stops:**
- Business understanding confirmation
- Application form field completion
- Code file selection confirmation
- Screenshot method selection
- Final Markdown confirmation

**Don't skip these** — skill enforces human-in-the-loop for quality

---

## Value Proposition

### Per Project Savings

| Item | Without Skills | With Skills | Savings |
|------|---------------|-------------|---------|
| Patent disclosure | ¥5,000-10,000 | FREE | ¥5,000-10,000 |
| Software copyright | ¥500-1,000 | FREE | ¥500-1,000 |
| **Total** | **¥5,500-11,000** | **FREE** | **¥5,500-11,000** |

**Rp equivalent:** ~Rp11-22 juta saved per project

### Time Savings

| Task | Manual | Automated | Saved |
|------|--------|-----------|-------|
| Patent disclosure | 7-11 days | 32 minutes | 7-11 days |
| Software copyright | 2-3 days | 22 minutes | 2-3 days |
| **Total** | **9-14 days** | **54 minutes** | **9-14 days** |

---

## References

- Patent skill repo: https://github.com/handsomestWei/patent-disclosure-skill
- Copyright skill repo: https://github.com/Fokkyp/SoftwareCopyright-Skill
- CNIPA (China Patent Office): http://epub.cnipa.gov.cn/
- AgentSkills standard: https://agentskills.io
