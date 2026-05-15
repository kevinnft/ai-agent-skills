---
name: comprehensive-public-repo-setup
description: "Create production-ready public repos with complete documentation, automated setup, bundled dependencies, and user-friendly installation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Documentation, Setup Scripts, Open Source, Repository Management]
    related_skills: [github-repo-management, github-pr-workflow, writing-plans]
origin: original
source_repo: kevinnft/ai-agent-skills
source_url: https://github.com/kevinnft/ai-agent-skills
source_license: MIT
language: en
---

# Comprehensive Public Repository Setup

Pattern for creating production-ready public repositories that others can clone and use immediately.

## When to Use

Creating a public repo that needs:
- Comprehensive documentation
- Automated setup (one-command install)
- Bundled dependencies (no external failures)
- Templates and examples
- Troubleshooting guide
- Installation verification

## Repository Structure

```
repo-name/
├── README.md (10-15KB, comprehensive)
├── setup.sh (automated installation)
├── LICENSE (MIT recommended)
├── CONTRIBUTING.md
├── TROUBLESHOOTING.md (20+ solutions)
├── CHECKLIST.md (20+ verification steps)
├── EXAMPLE.md (real-world workflow)
├── templates/
│   ├── template1.md
│   └── template2.md
└── bundled-dependencies/ (if applicable)
    └── external-tool/
```

## README.md Structure

Essential sections (in order):

1. **Title + Tagline** — with badges
2. **What is This?** — 2-3 sentence overview
3. **Features** — bullet points with emojis
4. **Quick Start** — 5-minute install
5. **Manual Setup** — step-by-step
6. **Workflow Example** — real-world use case
7. **Architecture** — ASCII diagram
8. **Use Cases** — when to use this
9. **Advanced Features** — optional capabilities
10. **Performance** — comparison if applicable
11. **Contributing** — link to CONTRIBUTING.md
12. **License** — MIT recommended
13. **Credits** — acknowledgments

Example template:

```markdown
# 🧠 Project Name

**One-line description highlighting key benefits.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What is This?

Brief overview (2-3 sentences).

## ✨ Features

- ⚡ **Feature 1** — description
- 🧠 **Feature 2** — description

## 🚀 Quick Start

\`\`\`bash
git clone https://github.com/user/repo.git
cd repo
./setup.sh
\`\`\`

## 📖 Manual Setup

Step-by-step instructions...
```

## setup.sh Pattern

Structure:

```bash
#!/bin/bash
set -e  # Exit on error

# Header
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 Project Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command -v tool &> /dev/null; then
    echo "❌ Tool not found. Installing..."
    # Install command
fi
echo "✅ Prerequisites OK"
echo ""

# 2. Get user input (interactive)
echo "📋 Configuration:"
read -p "Username: " USERNAME
read -sp "Token: " TOKEN
echo ""
echo ""

# 3. Install dependencies with fallback
echo "📦 Installing dependencies..."
if git clone --depth 1 https://github.com/external/dep.git 2>/dev/null; then
    echo "✅ Installed from GitHub (latest)"
else
    echo "⚠️  GitHub clone failed, using bundled copy..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cp -r "$SCRIPT_DIR/bundled-dep" "$INSTALL_DIR/"
    echo "✅ Installed from bundle"
fi
echo ""

# 4. Configure
echo "⚙️ Configuring..."
# Configuration steps
echo "✅ Configuration complete"
echo ""

# 5. Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Summary:"
echo "   • Component 1: ✅"
echo "   • Component 2: ✅"
echo ""
echo "🎯 Next Steps:"
echo "   1. Step one"
echo "   2. Step two"
echo ""
```

**Key principles:**
- Use `set -e` (exit on error)
- Check prerequisites before proceeding
- Interactive prompts only for user-specific values
- Fallback logic for external dependencies
- Clear progress indicators (emojis + messages)
- Summary at end with next steps

## Bundling External Dependencies

**Problem:** External repos can disappear, change, or be rate-limited.

**Solution:** Bundle critical dependencies with GitHub fallback.

**Pattern:**

```bash
# Try GitHub first (latest version)
if git clone --depth 1 https://github.com/external/tool.git 2>/dev/null; then
    echo "✅ Installed from GitHub (latest)"
else
    # Fallback: use bundled copy
    echo "⚠️  GitHub clone failed, using bundled copy..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cp -r "$SCRIPT_DIR/bundled-tool" "$INSTALL_DIR/"
    echo "✅ Installed from bundle"
fi
```

**When to bundle:**
- Critical dependencies (setup fails without them)
- Small size (<1MB preferred, <5MB acceptable)
- Stable APIs (won't break with old version)
- External repos with uncertain longevity

**When NOT to bundle:**
- Large dependencies (>10MB)
- Frequently updated tools
- OS packages (use package manager)

## TROUBLESHOOTING.md Structure

Sections:

1. **Installation Issues** — errors during setup
2. **Runtime Issues** — problems after installation
3. **Sync/Network Issues** — connectivity problems
4. **Performance Issues** — slow operations
5. **Security Issues** — token/permission problems
6. **Verification Checklist** — confirm installation

Format:

```markdown
### **"Error message"**

**Problem:** Brief description.

**Solution:**
\`\`\`bash
# Fix command
\`\`\`
```

Aim for 20-30 solutions covering common issues.

## CHECKLIST.md Pattern

Structure:

1. **Pre-installation** (5-10 checks)
2. **Post-installation** (10-15 verifications)
3. **Functional tests** (3-5 tests)
4. **Optional features**
5. **Success criteria**

Format:

```markdown
### **1. Component Installed**

\`\`\`bash
command --version
# Expected: version x.y.z
\`\`\`

- [ ] Command works
- [ ] Version displayed
```

Aim for 20-30 total verification steps.

## Commit Strategy

**Initial commit:**

```bash
git add .
git commit -m "Initial commit: README, setup script, examples, license"
git push origin main
```

**Subsequent commits:**
- One feature per commit
- Descriptive messages
- Group related changes

**Good commit messages:**
- "Add templates and troubleshooting guide"
- "Bundle dependencies with GitHub fallback"
- "Update documentation: add verification steps"

## Pitfalls

### ❌ Missing Bundled Dependencies

**Problem:** Setup script clones from GitHub, but external repo is deleted/unavailable.

**Solution:** Bundle critical dependencies in repo with fallback logic.

**Real example:** User caught missing bundled dependency: "Woi lu lupa masukin obsidian skill?"

### ❌ Too Many Confirmation Prompts

**Problem:** Script asks for confirmation at every step, slowing down installation.

**User feedback:** "Lo langsung buat token aja, kerjain semuannya sendiri jngn kbanyakan nanya"

**Solution:**
- Only prompt for user-specific values (username, token)
- Auto-proceed for standard operations
- Use `--yes` flags where applicable
- Show progress, don't ask permission

### ❌ Incomplete Documentation

**Problem:** README doesn't cover edge cases, troubleshooting, or verification.

**Solution:** Include:
- TROUBLESHOOTING.md (20-30 solutions)
- CHECKLIST.md (20-30 verification steps)
- EXAMPLE.md (real-world workflow)

### ❌ Single Point of Failure

**Problem:** Setup depends on external service being available.

**Solution:**
- Bundle dependencies
- Provide fallback methods
- Document manual alternatives

### ❌ No Verification Steps

**Problem:** User doesn't know if installation succeeded.

**Solution:**
- CHECKLIST.md with verification commands
- Setup script shows summary at end
- Include functional tests

### ❌ Token Duplication in Bashrc

**Problem:** Appending token to ~/.bashrc without checking if it already exists → multiple runs create duplicates.

**Bad:**
```bash
echo "export GH_TOKEN='$GITHUB_TOKEN'" >> ~/.bashrc
# Run setup.sh 10x → 10 duplicate tokens!
```

**Good:**
```bash
# Only add if not already present
if ! grep -q "export GH_TOKEN=" ~/.bashrc 2>/dev/null; then
    echo "export GH_TOKEN='$GITHUB_TOKEN'" >> ~/.bashrc
    echo "✅ Token saved to ~/.bashrc"
else
    # Update existing token
    sed -i "s|export GH_TOKEN=.*|export GH_TOKEN='$GITHUB_TOKEN'|" ~/.bashrc
    echo "✅ Token updated in ~/.bashrc"
fi
```

**Real impact:** Found in mnemosyne-obsidian repo (commit `9cfbf55`).

### ❌ Date Not Expanding in Heredoc

**Problem:** Single-quoted heredoc (`<< 'EOF'`) prevents variable expansion.

**Bad:**
```bash
cat > file.md << 'EOF'
date: $(date +%Y-%m-%d)
EOF
# Output: date: $(date +%Y-%m-%d)  ← LITERAL STRING!
```

**Good:**
```bash
cat > file.md << EOF  # Remove quotes!
date: $(date +%Y-%m-%d)
EOF
# Output: date: 2026-05-12  ← ACTUAL DATE!
```

**Note:** Escape backticks in content: `` \`command\` ``

**Real impact:** Found in mnemosyne-obsidian repo (commit `9cfbf55`).

## References

- **[CRITICAL_BASH_PITFALLS.md](references/CRITICAL_BASH_PITFALLS.md)** — Common bash bugs in setup scripts (token duplication, heredoc quoting, path expansion, input validation)

## Real-World Example

**Repo:** https://github.com/kevinnft/mnemosyne-obsidian

**Structure:**
- README.md (12KB) — comprehensive guide
- setup.sh (6KB) — automated installation
- EXAMPLE.md (3.7KB) — VPS cleanup workflow
- TROUBLESHOOTING.md (5.4KB) — 30+ solutions
- CHECKLIST.md (5.7KB) — 30+ verification steps
- templates/ (4 files) — starter templates
- obsidian-skills/ (340KB, 5 skills) — bundled dependency

**Key features:**
- ✅ One-command installation (`./setup.sh`)
- ✅ Bundled obsidian-skills with GitHub fallback
- ✅ Comprehensive documentation (7 files)
- ✅ 30+ troubleshooting solutions
- ✅ 30+ verification steps
- ✅ Real-world example workflow
- ✅ Works offline (after initial clone)

**Installation flow:**

```bash
git clone https://github.com/kevinnft/mnemosyne-obsidian.git
cd mnemosyne-obsidian
./setup.sh
# Enter username + token
# Wait 5 minutes
# Done!
```

## Pre-Push Checklist

Before pushing to GitHub:

- [ ] README.md comprehensive (10+ sections)
- [ ] setup.sh automated (5-minute install)
- [ ] LICENSE included (MIT recommended)
- [ ] CONTRIBUTING.md present
- [ ] TROUBLESHOOTING.md with 20+ solutions
- [ ] CHECKLIST.md with 20+ verification steps
- [ ] EXAMPLE.md with real-world workflow
- [ ] Templates directory (if applicable)
- [ ] Critical dependencies bundled
- [ ] Fallback logic for external deps
- [ ] Clear commit messages
- [ ] Repo description updated
- [ ] All titles consistent

## Social Media Posts

### Character Limits

**CRITICAL:** Social media platforms use **CHARACTER limits**, not word limits.

**Common mistake:** "260 kata" (260 words) vs "260 karakter" (260 characters)

**Platform limits:**
- Twitter/X: 280 characters
- LinkedIn: 3,000 characters (but 260 optimal for engagement)
- Reddit title: 300 characters

**Verification:**
```bash
# Count characters (excluding newlines)
cat post.txt | tr -d '\n' | wc -c
```

### Post Structure (Twitter/X)

**Format (under 260 chars):**
```
🧠 [Hook: problem + solution]

[Key feature 1]
[Key feature 2]
[Key feature 3]

Built on @mention1 by @mention2

[Repo URL]

#Tag1 #Tag2
```

**Example (258 chars):**
```
🧠 AI memory: 500x faster recall + rich notes + auto backup

Mnemosyne + Obsidian + GitHub = best of all worlds

✅ 1-cmd setup
✅ Works offline
✅ MIT license

Built on @nousresearch Hermes by @teknium

https://github.com/user/repo

#AI #Obsidian
```

### Comment Thread (Detailed Explanation)

**Structure (5 threads):**

1. **Problem** — What frustration does this solve?
2. **How It Works** — Technical overview (3 components)
3. **Real-World Example** — Concrete workflow (7 steps)
4. **Why Powerful** — Before/after comparison
5. **Installation + Features** — Quick start + feature list

**Each thread:** 1-2 paragraphs, code blocks where helpful, end with hashtags.

**Files to create:**
- `SOCIAL_POST_SHORT.md` — Main post (under 260 chars)
- `COMMENT_THREAD_EN.md` — English explanation (5 threads)
- `COMMENT_THREAD.md` — Indonesian version (if applicable)

## User Preferences (kevinnft)

**Communication style:**
- Responds in Indonesian informal ("Mantap", "Keren", "Gas")
- Wants autonomous action, minimal prompts
- Expects complete solutions, not options
- Direct feedback when something missing

**Workflow preferences:**
- Bundle dependencies (don't rely on external availability)
- Comprehensive documentation (README + TROUBLESHOOTING + CHECKLIST)
- Automated setup scripts (one command to install)
- Real-world examples (not toy demos)
- Verification steps (prove it works)

**Red flags:**
- "Woi lu lupa..." — caught missing component
- "jngn kbanyakan nanya" — too many confirmation prompts
- "Lo langsung buat..." — wants autonomous action
