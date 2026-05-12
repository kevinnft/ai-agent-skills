# Ecosystem Skill Installation Workflow

Reference for installing Hermes ecosystem skills with Python dependencies, Playwright, and proper directory structure.

## Session Context

**Date:** 2026-05-12  
**Skills Installed:**
- `patent-disclosure-skill` — Chinese patent disclosure generator
- `software-copyright` — Chinese software copyright materials generator

**Source:** Twitter recommendation from @frxiaobei

---

## Installation Pattern

### 1. Clone to Skills Directory

```bash
cd ~/.hermes/skills
git clone --depth 1 https://github.com/USER/SKILL_NAME
```

**Why `--depth 1`:** Saves disk space, faster clone (only latest commit)

---

### 2. Python Dependencies with venv

**Problem:** Ubuntu 24.04 blocks system-wide pip installs (PEP 668)

**Solution:** Use Python venv per skill

```bash
cd ~/.hermes/skills/SKILL_NAME
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Pattern for skills with multiple requirements files:**

```bash
# Base requirements
pip install -r requirements.txt

# Optional requirements (e.g., web scraping)
pip install -r tools/requirements-cnipa.txt
```

---

### 3. Playwright Installation

**For skills that need browser automation:**

```bash
source venv/bin/activate
pip install playwright
python -m playwright install chromium
```

**Why chromium only:** Saves disk space (~200MB vs ~600MB for all browsers)

---

### 4. Directory Structure Cleanup

**Some repos have nested skill directories:**

```bash
# Example: SoftwareCopyright-Skill
git clone https://github.com/Fokkyp/SoftwareCopyright-Skill
cp -R SoftwareCopyright-Skill/software-copyright-materials ./software-copyright
rm -rf SoftwareCopyright-Skill
```

**Rule:** Skill directory must contain `SKILL.md` at root level

---

### 5. Verification

```bash
# Check SKILL.md exists
ls ~/.hermes/skills/SKILL_NAME/SKILL.md

# Check venv created
ls ~/.hermes/skills/SKILL_NAME/venv/

# Check dependencies installed
source ~/.hermes/skills/SKILL_NAME/venv/bin/activate
pip list | grep -E "(playwright|python-docx|lxml)"
```

---

## Complete Example: Patent Disclosure Skill

```bash
# 1. Clone
cd ~/.hermes/skills
git clone --depth 1 https://github.com/handsomestWei/patent-disclosure-skill

# 2. Create venv and install base deps
cd patent-disclosure-skill
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Install optional deps (CNIPA web scraping)
pip install -r tools/requirements-cnipa.txt

# 4. Install Playwright + Chromium
python -m playwright install chromium

# 5. Verify
ls SKILL.md  # Should exist
pip list | grep playwright  # Should show playwright 1.59.0
```

---

## Complete Example: Software Copyright Skill

```bash
# 1. Clone
cd ~/.hermes/skills
git clone --depth 1 https://github.com/Fokkyp/SoftwareCopyright-Skill

# 2. Extract nested skill directory
cp -R SoftwareCopyright-Skill/software-copyright-materials ./software-copyright
rm -rf SoftwareCopyright-Skill

# 3. Verify (no extra deps needed)
ls software-copyright/SKILL.md  # Should exist
ls software-copyright/scripts/  # Should have Python scripts
```

---

## Troubleshooting

### Issue: "error: externally-managed-environment"

**Cause:** Ubuntu 24.04 blocks system-wide pip installs

**Solution:** Use venv (see step 2 above)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Issue: Playwright install fails

**Cause:** Missing system dependencies

**Solution:** Install system deps first

```bash
# Ubuntu/Debian
sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2

# Then retry
python -m playwright install chromium
```

---

### Issue: Skill not detected by Hermes

**Cause:** `SKILL.md` not at root level

**Solution:** Check directory structure

```bash
# WRONG:
~/.hermes/skills/REPO_NAME/skill-dir/SKILL.md

# CORRECT:
~/.hermes/skills/SKILL_NAME/SKILL.md
```

**Fix:** Extract nested directory or move SKILL.md to root

---

## VPS Resource Considerations

**User has ZERO tolerance for heavy tools on VPS:**
- VPS specs: 2 vCPUs, 2GB RAM, 40GB SSD
- Disk >500MB or RAM >100MB = ask first

**Playwright disk usage:**
- Chromium only: ~200MB
- All browsers: ~600MB
- **Recommendation:** Install chromium only on VPS

**Python venv disk usage:**
- Base venv: ~20MB
- With dependencies: 50-150MB (varies by skill)
- **Acceptable** for most skills

---

## Skill Discovery

**After installation, verify Hermes detects the skill:**

```bash
hermes skills list | grep -E "(patent|copyright)"
```

**Expected output:**
```
patent-disclosure-skill: 中国专利.skill，从项目文档到可交付的技术交底书
software-copyright: Generate guided Chinese software copyright application materials
```

---

## Usage Pattern

**Load skill before use:**

```python
skill_view(name='software-copyright')
```

**Then follow skill workflow:**

```bash
# Example: Software copyright generation
cd ~/PROJECT
python3 ~/.hermes/skills/software-copyright/scripts/check_environment.py --out-dir 软件著作权申请资料
python3 ~/.hermes/skills/software-copyright/scripts/analyze_project.py --project . --out 软件著作权申请资料/analysis/project.json
# ... continue workflow
```

---

## Session Outcome

**Skills installed:** 2  
**Time:** ~10 minutes  
**Disk usage:** ~250MB (both skills + deps)  
**Status:** ✅ Both skills working  
**Value:** ¥5,500-11,000 saved per project (~Rp11-22 juta)

---

## Related Skills

- `ecosystem-tool-evaluation` — Evaluate ecosystem tools before installation
- `vps-cleanup` — VPS resource management and cleanup

---

## References

- Patent skill: https://github.com/handsomestWei/patent-disclosure-skill
- Copyright skill: https://github.com/Fokkyp/SoftwareCopyright-Skill
- Twitter source: https://x.com/frxiaobei/status/2053827716605169804
