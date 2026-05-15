---
name: public-repo-creation
description: Create production-ready public GitHub repositories with comprehensive documentation, automated setup, and quality assurance
tags: [github, documentation, open-source, repository, automation]
version: 1.0.0
origin: unknown
source_license: see upstream
language: en
---

# Public Repository Creation

Create production-ready public GitHub repositories with comprehensive documentation, automated setup scripts, templates, and quality assurance processes.

## When to Use

- Creating new open-source projects
- Publishing tools, libraries, or frameworks
- Building educational resources or examples
- Sharing integrations or automation scripts
- Any public-facing repository that needs professional polish

## Core Components

### 1. Documentation Files (Required)

**README.md** (comprehensive):
- Clear title with emoji
- Badges (license, stars, build status)
- "What is This?" section
- Features (with subsections)
- Quick start (5-10 minutes)
- Manual setup (step-by-step)
- Example workflows
- Architecture diagram (ASCII or image)
- Folder structure
- Use cases
- Advanced features
- Performance metrics (if applicable)
- Contributing section
- License section
- Credits
- Support section

**LICENSE** (required):
- MIT recommended for maximum adoption
- Include copyright year and author

**CONTRIBUTING.md**:
- Quick start for contributors
- Code style guidelines
- Commit message format
- PR process
- Bug report template
- Feature request template

**TROUBLESHOOTING.md**:
- Installation issues (5+ solutions)
- Runtime issues (4+ solutions)
- Common errors with fixes
- Verification checklist

**CHECKLIST.md** (optional but recommended):
- Pre-installation checks
- Post-installation verification (10+ steps)
- Functional tests
- Success criteria

### 2. Automated Setup Script

**setup.sh** (or equivalent):
- Shebang (`#!/bin/bash`)
- Error handling (`set -e`)
- Prerequisites check
- Interactive prompts (with defaults)
- Conditional logic (skip if already installed)
- Fallback mechanisms
- Progress indicators
- Summary output
- Comments for each section

**Critical Patterns:**

```bash
# Prevent duplicate entries in config files
if ! grep -q "PATTERN" ~/.config 2>/dev/null; then
    echo "NEW_LINE" >> ~/.config
else
    sed -i "s|OLD_PATTERN|NEW_PATTERN|" ~/.config
fi

# Variable expansion in heredocs
cat > file.txt << EOF  # NO quotes for expansion
date: $(date +%Y-%m-%d)
EOF

# Fallback mechanism
if command_from_internet; then
    echo "✅ Installed from source"
else
    echo "⚠️  Source failed, using bundled copy..."
    cp -r bundled/ destination/
fi
```

### 3. Templates

**templates/** directory:
- Getting started template
- Daily/project note templates (if applicable)
- Configuration file templates
- .gitignore template

### 4. Examples

**EXAMPLE.md** or **examples/** directory:
- Real-world use case
- Step-by-step breakdown
- Code examples with syntax highlighting
- Expected output
- Benefits explanation

### 5. Quality Assurance

**Pre-commit checks:**
```bash
# Syntax validation
bash -n setup.sh

# Link validation
grep -o '\[.*\](.*\.md)' *.md | while read link; do
    file=$(echo "$link" | sed 's/.*(\\(.*\\))/\\1/')
    [ -f "$file" ] && echo "✅ $link" || echo "❌ Broken: $link"
done

# TODO/FIXME check
grep -ri "TODO\|FIXME\|XXX\|HACK" . --include="*.md" --include="*.sh"

# File permissions
ls -la setup.sh  # Should be executable
```

**AUDIT.md** (optional but professional):
- File inventory
- Quality checks performed
- Security analysis
- Performance metrics
- Recommendations

## Workflow

### Phase 1: Planning (5 minutes)

1. Define repository purpose (one sentence)
2. Identify target audience
3. List core features (3-5 main features)
4. Choose license (MIT recommended)
5. Plan folder structure

### Phase 2: Core Setup (15 minutes)

1. Create GitHub repo (public)
2. Clone locally
3. Create README.md with title, description, badges
4. Create LICENSE file
5. Create .gitignore
6. Initial commit + push

### Phase 3: Documentation (30 minutes)

1. Expand README.md:
   - Features section
   - Quick start
   - Manual setup
   - Examples
   - Architecture
2. Create CONTRIBUTING.md
3. Create TROUBLESHOOTING.md
4. Create EXAMPLE.md

### Phase 4: Automation (30 minutes)

1. Create setup.sh:
   - Prerequisites check
   - Interactive prompts
   - Installation steps
   - Configuration
   - Summary output
2. Test setup.sh syntax: `bash -n setup.sh`
3. Make executable: `chmod +x setup.sh`
4. Test dry-run simulation

### Phase 5: Templates & Examples (15 minutes)

1. Create templates/ directory
2. Add starter templates
3. Add example files
4. Document template usage in README

### Phase 6: Quality Assurance (20 minutes)

1. Run syntax checks
2. Validate all links
3. Check file permissions
4. Test setup script (if possible)
5. Create CHECKLIST.md
6. Optional: Create AUDIT.md

### Phase 7: Polish (10 minutes)

1. Add badges to README
2. Add architecture diagram
3. Add performance metrics (if applicable)
4. Add star history chart
5. Final commit + push

**Total Time:** ~2 hours for production-ready repo

## Critical Pitfalls

### 1. Token/Config Duplication
**Problem:** Appending to config files without checking for duplicates.

**Wrong:**
```bash
echo "export TOKEN='xxx'" >> ~/.bashrc
# Run twice → duplicate entries!
```

**Right:**
```bash
if ! grep -q "export TOKEN=" ~/.bashrc 2>/dev/null; then
    echo "export TOKEN='xxx'" >> ~/.bashrc
else
    sed -i "s|export TOKEN=.*|export TOKEN='xxx'|" ~/.bashrc
fi
```

### 2. Heredoc Variable Expansion
**Problem:** Using single-quoted heredoc prevents variable expansion.

**Wrong:**
```bash
cat > file.txt << 'EOF'
date: $(date +%Y-%m-%d)
EOF
# Output: date: $(date +%Y-%m-%d)  ← LITERAL!
```

**Right:**
```bash
cat > file.txt << EOF  # No quotes!
date: $(date +%Y-%m-%d)
EOF
# Output: date: 2026-05-12  ← EXPANDED!
```

### 3. Hardcoded Paths
**Problem:** Hardcoding paths that may vary across systems.

**Consider:**
- Use `$HOME` instead of `/home/username`
- Use `$(dirname "${BASH_SOURCE[0]}")` for script directory
- Make paths configurable via prompts or environment variables

### 4. Missing Fallback Mechanisms
**Problem:** Single point of failure (e.g., GitHub clone only).

**Solution:**
```bash
if git clone https://github.com/repo.git 2>/dev/null; then
    echo "✅ Cloned from GitHub"
else
    echo "⚠️  GitHub failed, using bundled copy..."
    cp -r bundled/ destination/
fi
```

### 5. Incomplete Documentation
**Problem:** Missing critical sections in README.

**Must-have sections:**
- What is This?
- Features
- Quick Start
- Installation
- Examples
- Troubleshooting
- Contributing
- License

### 6. No Quality Checks
**Problem:** Pushing without validation.

**Always check:**
- Syntax: `bash -n setup.sh`
- Links: Validate all internal links
- Permissions: Ensure setup.sh is executable
- TODOs: No TODO/FIXME in production

### 7. Character Count Confusion
**Problem:** Misunderstanding "260 kata" (words) vs "260 karakter" (characters).

**Context:** Indonesian "kata" = word, "karakter" = character.

**Check:**
```bash
# Word count
wc -w post.txt

# Character count (excluding newlines)
cat post.txt | tr -d '\n' | wc -c
```

**Limits:**
- Twitter/X: 280 characters (use 260 for safety)
- LinkedIn: 3,000 characters
- Reddit title: 300 characters
- Blog post: No strict limit (aim for 500-1000 words)

**Always clarify with user:** "260 words or 260 characters?"
### 8. Broken Internal Links
**Problem:** Referencing files that don't exist.

**Check:**
```bash
grep -o '\[.*\](.*\.md)' README.md | while read link; do
    file=$(echo "$link" | sed 's/.*(\\(.*\\))/\\1/')
    [ -f "$file" ] || echo "❌ Broken: $link"
done
```

## Title Consistency

When creating repos with multiple components (e.g., "Tool A + Tool B + Feature C"):

1. **Update ALL titles** to include all components:
   - README.md title
   - setup.sh comment header
   - EXAMPLE.md title
   - CONTRIBUTING.md title
   - GitHub repo description

2. **Check consistency:**
```bash
grep -h "^#.*Tool.*Feature" README.md EXAMPLE.md CONTRIBUTING.md setup.sh
```

## Bundling Dependencies

When including third-party code (e.g., skills, libraries):

1. **Bundle in repo** (don't rely on external availability)
2. **Remove nested .git** directories
3. **Implement fallback logic:**
   - Try fetching latest from source
   - Fall back to bundled copy if source unavailable
4. **Document in README:**
   - Mention bundled version
   - Explain fallback mechanism

## Security Considerations

1. **Credentials:**
   - Never commit tokens/passwords
   - Use `read -sp` for sensitive input (no echo)
   - Store in user-only readable files (~/.bashrc, ~/.config)
   - Add to .gitignore: `*.secret.md`, `*.private.md`

2. **Permissions:**
   - setup.sh: 755 (executable)
   - Templates: 644 (readable)
   - No world-writable files

3. **Token Scopes:**
   - Use minimal scopes (e.g., `repo` only)
   - Provide token generation link with pre-selected scopes
   - Document required scopes in README

## User Experience

**Good UX:**
- 5 or fewer user actions required
- Clear prompts with defaults
- Progress indicators
- Summary output at end
- Helpful error messages
- Verification checklist

**Bad UX:**
- 20+ manual steps
- No defaults (user must type everything)
- Silent failures
- Cryptic errors
- No way to verify success

## Quality Metrics & Maximization

### Quality Scoring Framework (7/10 → 10/10)

**Scoring Categories (10 points each):**

| Category | 7/10 (Good) | 10/10 (Perfect) |
|----------|-------------|-----------------|
| **Documentation** | README + basic docs | README + CHANGELOG + FAQ + 10+ docs |
| **Installers** | Working setup script | Multiple installers + smart detection |
| **Templates** | Basic templates | Complete template set |
| **CI/CD** | None | GitHub Actions + automated tests |
| **Examples** | Basic examples | Screenshots + demos + videos |
| **Badges** | License only | CI + License + Version + Stars + Forks |
| **Changelog** | None | Semantic versioning + release notes |
| **Releases** | None | Tagged releases + GitHub releases |
| **Issue Templates** | None | Bug report + feature request + PR template |
| **Tests** | None | Comprehensive test suite + passing CI |

**Total Score Calculation:**
- Sum all categories (max 100 points)
- Divide by 10 for final score
- **7/10 = Good** (production-ready but basic)
- **10/10 = Perfect** (world-class open source)

### Production-Ready Checklist (7/10)

**Minimum requirements:**
- ✅ Comprehensive README (10KB+)
- ✅ Automated setup script (5KB+)
- ✅ Real-world examples
- ✅ Troubleshooting guide (20+ solutions)
- ✅ Installation checklist (20+ checks)
- ✅ Templates (3+ files)
- ✅ License (MIT recommended)
- ✅ Contributing guide
- ✅ All syntax valid
- ✅ All links working
- ✅ No TODOs in production

### Perfect Repo Checklist (10/10)

**Additional requirements for 10/10:**

#### **1. CI/CD (GitHub Actions)**
```yaml
# .github/workflows/ci.yml
name: github-public-repo-creation
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate syntax
        run: bash -n setup.sh
      - name: Run tests
        run: ./tests/test-suite.sh
```

#### **2. Comprehensive Test Suite**
```bash
# tests/test-suite.sh
#!/bin/bash
set -e

echo "🧪 Running tests..."

# Test 1: Syntax validation
bash -n setup.sh && echo "✅ Syntax OK"

# Test 2: File existence
test -f README.md && echo "✅ README exists"
test -f CHANGELOG.md && echo "✅ CHANGELOG exists"

# Test 3: Documentation completeness
grep -q "Quick Start" README.md && echo "✅ Has Quick Start"
grep -q "FAQ" README.md && echo "✅ Has FAQ"

# Test 4: Installer detection (if applicable)
# ... custom tests ...

echo "✅ ALL TESTS PASSED!"
```

#### **3. Issue Templates**

**Bug Report** (`.github/ISSUE_TEMPLATE/bug_report.md`):
```markdown
---
name: Bug report
about: Create a report to help us improve
---

## Bug Description
Clear description of the bug.

## To Reproduce
Steps to reproduce.

## Expected Behavior
What you expected.

## Environment
- OS: [e.g. Ubuntu 24.04]
- Version: [e.g. 1.0.0]
```

**Feature Request** (`.github/ISSUE_TEMPLATE/feature_request.md`):
```markdown
---
name: Feature request
about: Suggest an idea
---

## Feature Description
Clear description of the feature.

## Motivation
Why is this needed?

## Proposed Solution
How should it work?
```

#### **4. PR Template**

**`.github/pull_request_template.md`:**
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
```

#### **5. CHANGELOG.md**

**Format:** [Keep a Changelog](https://keepachangelog.com/)

```markdown
# Changelog

## [1.1.0] - 2026-05-12
### Added
- New feature X
- Improvement Y

### Fixed
- Bug Z

## [1.0.0] - 2026-05-11
### Added
- Initial release
```

#### **6. GitHub Releases**

```bash
# Create release
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0
gh release create v1.1.0 --title "v1.1.0 - Feature Name" --notes "Release notes here"
```

#### **7. Badges**

```markdown
[![CI](https://github.com/user/repo/workflows/CI/badge.svg)](https://github.com/user/repo/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/github/v/release/user/repo)](https://github.com/user/repo/releases)
[![Stars](https://img.shields.io/github/stars/user/repo?style=social)](https://github.com/user/repo/stargazers)
[![Forks](https://img.shields.io/github/forks/user/repo?style=social)](https://github.com/user/repo/network/members)
```

#### **8. FAQ Section**

**Add to README.md:**
```markdown
## ❓ FAQ

### Q: Common question 1?
**A:** Answer with details.

### Q: Common question 2?
**A:** Answer with details.

... (10+ questions)
```

### Maximization Workflow (7/10 → 10/10)

**Time: 1.5-2 hours**

#### **Phase 1: CHANGELOG + Release (15 min)**
1. Create CHANGELOG.md with version history
2. Tag current version: `git tag -a v1.0.0 -m "Initial release"`
3. Create GitHub release: `gh release create v1.0.0`

#### **Phase 2: Badges + FAQ (20 min)**
4. Add 5 badges to README (CI, License, Version, Stars, Forks)
5. Add FAQ section with 10+ common questions

#### **Phase 3: CI/CD + Tests (40 min)**
6. Create `.github/workflows/ci.yml`
7. Create `tests/test-suite.sh` with 6+ tests
8. Verify CI passes

#### **Phase 4: Issue Templates (15 min)**
9. Create bug report template
10. Create feature request template
11. Create PR template

#### **Phase 5: Verification (10 min)**
12. Run test suite locally
13. Check CI status on GitHub
14. Verify all badges display correctly
15. Final quality score: 10/10 ✅

### Quality Verification Commands

```bash
# 1. Check file count
find . -type f ! -path './.git/*' | wc -l

# 2. Check repo size
du -sh . --exclude=.git

# 3. Run tests
./tests/test-suite.sh

# 4. Check CI status
gh run list --limit 1

# 5. Verify badges
curl -s https://github.com/user/repo | grep -o 'img.shields.io' | wc -l

# 6. Count documentation
ls -1 *.md | wc -l

# 7. Verify release
gh release list

# 8. Check templates
ls -1 .github/ISSUE_TEMPLATE/ .github/pull_request_template.md
```

### Critical Success Factors

**For 10/10 Perfect Score:**
1. ✅ **CI/CD:** GitHub Actions workflow + passing tests
2. ✅ **Tests:** Comprehensive test suite (6+ tests)
3. ✅ **Templates:** Bug report + feature request + PR template
4. ✅ **CHANGELOG:** Semantic versioning + release notes
5. ✅ **Release:** Tagged release + GitHub release page
6. ✅ **Badges:** 5+ badges (CI, License, Version, Stars, Forks)
7. ✅ **FAQ:** 10+ common questions answered
8. ✅ **Documentation:** 12+ comprehensive docs

**User Preference (from session):**
- User says "gas maksimalkan" → Do full 10/10 transformation, not incremental
- User says "pastikan perfect" → Test everything, verify thoroughly
- User expects immediate action → No hesitation, execute workflow
- User wants comprehensive results → Not minimal viable, but production-ready excellence

## Example Structure

```
repo-name/
├── README.md              # Comprehensive guide (10KB+)
├── setup.sh               # Automated setup (executable)
├── LICENSE                # MIT or other
├── CONTRIBUTING.md        # Contribution guidelines
├── TROUBLESHOOTING.md     # Common issues + fixes
├── CHECKLIST.md           # Verification steps
├── EXAMPLE.md             # Real-world use case
├── AUDIT.md               # Quality audit (optional)
├── templates/
│   ├── getting-started.md
│   ├── config-template.yml
│   └── gitignore
├── examples/              # Additional examples (optional)
│   └── advanced-usage.md
└── bundled-deps/          # Bundled dependencies (if any)
    └── third-party-lib/
```

## Post-Creation Checklist

- [ ] All titles consistent (include all components)
- [ ] README comprehensive (10+ sections)
- [ ] setup.sh syntax valid (`bash -n setup.sh`)
- [ ] setup.sh executable (`chmod +x setup.sh`)
- [ ] All internal links valid
- [ ] No TODO/FIXME comments
- [ ] License file present
- [ ] .gitignore excludes secrets
- [ ] Templates included
- [ ] Examples included
- [ ] Troubleshooting guide present
- [ ] Installation checklist present
- [ ] Quality audit performed (optional)
- [ ] GitHub repo description updated
- [ ] All commits pushed
- [ ] Ready to share

## References

- [repo-maximization-checklist.md](references/repo-maximization-checklist.md) — Complete checklist for transforming 7/10 repo → 10/10 perfect (CI/CD, tests, templates, badges, FAQ)
- [critical-bugs-mnemosyne-obsidian.md](references/critical-bugs-mnemosyne-obsidian.md) — Critical bugs found and fixed: token duplication + heredoc expansion
- [setup-script-patterns.md](references/setup-script-patterns.md) — Complete patterns for robust setup scripts with examples
- [deep-analysis-workflow.md](references/deep-analysis-workflow.md) — Comprehensive deep analysis checklist (10 checks + simulation + quality scoring)

## See Also

- `github-pr-workflow` — For contributing to existing repos
- `comprehensive-public-repo-setup` — Alternative approach (may overlap)
- `github-repo-management` — For managing existing repos
