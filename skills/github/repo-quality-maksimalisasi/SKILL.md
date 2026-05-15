---
name: repo-quality-maksimalisasi
description: Evaluate and maximize GitHub repo quality from 7/10 to 10/10 perfect
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Quality, CI/CD, Testing, Documentation, Templates]
    related_skills: [github-repo-management, github-pr-workflow]
origin: original
source_repo: kevinnft/ai-agent-skills
source_url: https://github.com/kevinnft/ai-agent-skills
source_license: MIT
language: en
---

# Repository Quality Evaluation & Maksimalisasi

Transform GitHub repos from good (7/10) to perfect (10/10) production-ready state.

## When to Use

- User says "gas maksimalkan" or "pastikan perfect"
- Repo needs professional polish for public release
- Want comprehensive CI/CD, tests, and templates
- Preparing repo for community contributions

## Quality Scoring Framework

Evaluate across 10 categories (0-10 each):

| Category | Weight | What to Check |
|----------|--------|---------------|
| **Documentation** | 10% | README completeness, examples, architecture docs |
| **Installers/Setup** | 10% | Automated setup, clear instructions, idempotent |
| **Templates** | 5% | Starter files, boilerplate, examples |
| **CI/CD** | 15% | GitHub Actions, automated testing, status badges |
| **Examples** | 5% | Screenshots, demos, video tutorials |
| **Badges** | 5% | CI, license, version, stars, forks |
| **Changelog** | 10% | CHANGELOG.md, semantic versioning, release notes |
| **Releases** | 10% | GitHub releases, tags, versioned artifacts |
| **Issue Templates** | 15% | Bug report, feature request, PR templates |
| **Tests** | 15% | Test suite, coverage, automated validation |

**Scoring:**
- 0-3: Missing or broken
- 4-6: Basic/minimal
- 7-8: Good/functional
- 9-10: Excellent/comprehensive

**Total Score = Average of all categories**

---

## Maksimalisasi Workflow

### Phase 1: CHANGELOG + Release (15 min)

1. **Create CHANGELOG.md**
   ```bash
   cat > CHANGELOG.md << 'EOF'
   # Changelog
   
   ## [1.1.0] - YYYY-MM-DD
   ### Added
   - Feature A
   - Feature B
   
   ## [1.0.0] - YYYY-MM-DD
   ### Added
   - Initial release
   EOF
   ```

2. **Create GitHub release**
   ```bash
   git tag -a v1.1.0 -m "v1.1.0 - Description"
   git push origin v1.1.0
   gh release create v1.1.0 --title "v1.1.0 - Title" --notes "Release notes"
   ```

### Phase 2: Badges + FAQ (20 min)

3. **Add badges to README**
   ```markdown
   [![CI](https://github.com/owner/repo/workflows/CI/badge.svg)](https://github.com/owner/repo/actions)
   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
   [![Version](https://img.shields.io/github/v/release/owner/repo)](https://github.com/owner/repo/releases)
   [![GitHub stars](https://img.shields.io/github/stars/owner/repo?style=social)](https://github.com/owner/repo/stargazers)
   [![GitHub forks](https://img.shields.io/github/forks/owner/repo?style=social)](https://github.com/owner/repo/network/members)
   ```

4. **Add FAQ section** (before Contributing)
   ```markdown
   ## ❓ FAQ
   
   ### **Q: Common question 1?**
   **A:** Clear answer with examples.
   
   ### **Q: Common question 2?**
   **A:** Clear answer with code snippets.
   
   [Add 8-10 questions based on user feedback]
   ```

### Phase 3: CI/CD + Tests (40 min)

5. **Create GitHub Actions workflow**
   ```yaml
   # .github/workflows/ci.yml
   name: CI
   
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       
       steps:
       - uses: actions/checkout@v3
       
       - name: Check Bash syntax
         run: |
           for script in *.sh; do
             bash -n "$script"
           done
         
       - name: Validate documentation
         run: |
           test -f README.md || exit 1
           test -f CHANGELOG.md || exit 1
           test -f LICENSE || exit 1
           
       - name: Run tests
         run: |
           if [ -f tests/test.sh ]; then
             ./tests/test.sh
           fi
   ```

6. **Create test suite**
   ```bash
   mkdir -p tests
   cat > tests/test.sh << 'EOF'
   #!/bin/bash
   set -e
   
   echo "=== Running Tests ==="
   
   # Test 1: Syntax validation
   echo "Test 1: Syntax validation..."
   bash -n script.sh && echo "✅ Syntax OK" || exit 1
   
   # Test 2: File existence
   echo "Test 2: Required files..."
   test -f README.md && echo "✅ README exists" || exit 1
   
   # Test 3: Documentation completeness
   echo "Test 3: Documentation..."
   grep -q "Quick Start" README.md && echo "✅ Has Quick Start" || exit 1
   
   echo "✅ ALL TESTS PASSED!"
   EOF
   chmod +x tests/test.sh
   ```

7. **Verify CI passes**
   ```bash
   git add .github/workflows/ci.yml tests/
   git commit -m "feat: add CI/CD and test suite"
   git push
   # Wait for CI to pass
   gh run list --limit 1
   ```

### Phase 4: Templates (15 min)

8. **Bug report template**
   ```bash
   mkdir -p .github/ISSUE_TEMPLATE
   cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
   ---
   name: Bug report
   about: Create a report to help us improve
   title: '[BUG] '
   labels: bug
   ---
   
   ## 🐛 Bug Description
   Clear description of the bug.
   
   ## 📋 To Reproduce
   Steps to reproduce:
   1. Run command '...'
   2. See error '...'
   
   ## ✅ Expected Behavior
   What you expected to happen.
   
   ## 💻 Environment
   - OS: [e.g. Ubuntu 24.04]
   - Version: [e.g. 1.0.0]
   
   ## 🔍 Error Logs
   ```
   Paste logs here
   ```
   EOF
   ```

9. **Feature request template**
   ```bash
   cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
   ---
   name: Feature request
   about: Suggest an idea
   title: '[FEATURE] '
   labels: enhancement
   ---
   
   ## 🚀 Feature Description
   Clear description of the feature.
   
   ## 💡 Motivation
   Why is this needed?
   
   ## 📋 Proposed Solution
   How should it work?
   
   ## ✅ Acceptance Criteria
   - [ ] Criterion 1
   - [ ] Criterion 2
   EOF
   ```

10. **PR template**
    ```bash
    cat > .github/pull_request_template.md << 'EOF'
    ## 📋 Description
    Brief description of changes.
    
    ## 🎯 Type of Change
    - [ ] 🐛 Bug fix
    - [ ] ✨ New feature
    - [ ] 💥 Breaking change
    - [ ] 📝 Documentation
    
    ## ✅ Checklist
    - [ ] Code follows style guidelines
    - [ ] Self-review completed
    - [ ] Documentation updated
    - [ ] Tests pass
    EOF
    ```

---

## Pitfalls

1. **Don't skip CI verification**: Always wait for CI to pass before declaring complete
2. **Test idempotency**: Installers should be safe to run multiple times
3. **Mock dependencies in tests**: CI environment may not have all tools
4. **Badge order matters**: CI badge first (shows quality), then license, version, social proof
5. **FAQ placement**: Before Contributing section, after main content
6. **Release notes**: Use `--generate-notes` for automatic changelog from commits
7. **Template labels**: Use YAML frontmatter for auto-labeling issues/PRs
8. **User preference (ryzen)**: "gas maksimalkan" = comprehensive production-ready approach, not incremental patches

---

## Example: mnemosyne-obsidian Transformation

**Before (7/10):**
- ✅ Good documentation
- ✅ Two installers
- ❌ No CI/CD
- ❌ No tests
- ❌ No templates

**After (10/10):**
- ✅ Excellent documentation
- ✅ Two installers (tested)
- ✅ CI/CD (GitHub Actions, passing)
- ✅ Test suite (6 tests, 100% pass)
- ✅ Issue templates (bug, feature)
- ✅ PR template
- ✅ CHANGELOG.md
- ✅ GitHub release (v1.1.0)
- ✅ FAQ (10 questions)
- ✅ 5 badges

**Time:** 1.5 hours  
**Commits:** 3 commits  
**Lines:** 288 lines added  
**Result:** Production-ready, world-class repo

**Full case study:** See `references/mnemosyne-obsidian-case-study.md` for detailed breakdown, lessons learned, and reusable patterns.

---

## Quick Checklist

- [ ] CHANGELOG.md created
- [ ] GitHub release published
- [ ] 5 badges added to README
- [ ] FAQ section added (10+ questions)
- [ ] GitHub Actions CI workflow
- [ ] Test suite created and passing
- [ ] Bug report template
- [ ] Feature request template
- [ ] PR template
- [ ] CI badge shows passing status
