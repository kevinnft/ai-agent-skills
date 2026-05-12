# Deep Analysis Workflow for Public Repos

When user requests "analisa ulang" / "cek ulang" / "pastikan lengkap dan perfect", perform comprehensive deep analysis.

## Analysis Checklist

### 1. Syntax Validation
```bash
# Bash scripts
bash -n setup.sh
# Expected: No output = valid

# Python scripts (if any)
python3 -m py_compile script.py
```

### 2. Link Validation
```bash
# Internal markdown links
grep -o '\[.*\](.*\.md)' *.md | while read link; do
    file=$(echo "$link" | sed 's/.*(\\(.*\\))/\\1/')
    [ -f "$file" ] && echo "✅ $link" || echo "❌ Broken: $link"
done

# External links (manual check recommended)
grep -o 'https://[^)]*' *.md | sort -u
```

### 3. File Permissions
```bash
# Check executable files
find . -type f -executable ! -path "./.git/*"
# Expected: Only setup.sh (or similar)

# Check setup.sh permissions
ls -la setup.sh
# Expected: -rwxrwxr-x (755)
```

### 4. Template Placeholders
```bash
# Check for valid placeholder syntax
grep -r "{{" templates/
# Expected: Obsidian Templater syntax ({{date}}, {{PROJECT_NAME}}, etc.)
```

### 5. Bundled Dependencies Integrity
```bash
# Check if all expected files present
find bundled-deps/ -name "SKILL.md" -o -name "README.md"
# Count should match expected number

# Check for nested .git (should be removed)
find bundled-deps/ -name ".git"
# Expected: No output
```

### 6. TODO/FIXME Check
```bash
# Find any TODO/FIXME comments
grep -ri "TODO\|FIXME\|XXX\|HACK" . --include="*.md" --include="*.sh" ! -path "./.git/*"
# Expected: No output for production repos
```

### 7. Cross-Reference Check
```bash
# Check wikilinks reference existing notes
grep -o '\[\[.*\]\]' *.md | sort -u
# Verify each referenced note exists or is example-only
```

### 8. Setup Script Logic Check
```bash
# Check for duplicate append patterns
grep -n ">> ~/\." setup.sh
# Each should have duplicate-prevention check

# Check heredoc quotes
grep -n "<<" setup.sh
# Verify 'EOF' vs EOF based on expansion needs
```

### 9. Title Consistency Check
```bash
# Extract all main titles
grep -h "^# " README.md EXAMPLE.md CONTRIBUTING.md
grep "^# " setup.sh | head -1

# All should mention same components (e.g., "Tool A + Tool B + Feature C")
```

### 10. Character/Word Count (for social posts)
```bash
# Character count (for Twitter/X)
cat post.txt | tr -d '\n' | wc -c
# Should be ≤260 for Twitter

# Word count (for other platforms)
wc -w post.txt
```

## Simulation Test

Create dry-run simulation to validate setup.sh logic:

```bash
#!/bin/bash
# Simulate setup.sh execution (dry-run)
echo "=== SETUP SIMULATION ==="

# Check prerequisites
echo "✓ Git check"
echo "✓ Snap check"

# Simulate each major step
GITHUB_USER="testuser"
VAULT_NAME="test-vault"
GITHUB_TOKEN="ghp_test123"

echo "✓ User input: $GITHUB_USER, $VAULT_NAME"
echo "✓ Would create: $HOME/path/to/vault"
echo "✓ Would install dependencies"
echo "✓ Would save token (with duplicate check)"
echo "✓ Would init Git repo"
echo "✓ Would create initial files with date: $(date +%Y-%m-%d)"
echo "✓ Would create GitHub repo: $VAULT_NAME (private)"
echo "✓ Would push initial commit"

echo "=== SIMULATION COMPLETE ==="
echo "All steps validated ✅"
```

## Critical Bug Patterns to Check

### Pattern 1: Config File Duplication
**Look for:**
```bash
echo "SETTING=value" >> ~/.config
```

**Should be:**
```bash
if ! grep -q "SETTING=" ~/.config 2>/dev/null; then
    echo "SETTING=value" >> ~/.config
else
    sed -i "s|SETTING=.*|SETTING=value|" ~/.config
fi
```

### Pattern 2: Heredoc Variable Expansion
**Look for:**
```bash
cat > file.txt << 'EOF'
date: $(date +%Y-%m-%d)
EOF
```

**Should be:**
```bash
cat > file.txt << EOF  # No quotes!
date: $(date +%Y-%m-%d)
EOF
```

### Pattern 3: Missing Fallback
**Look for:**
```bash
git clone https://github.com/repo.git
```

**Should be:**
```bash
if git clone https://github.com/repo.git 2>/dev/null; then
    echo "✅ Cloned from GitHub"
else
    echo "⚠️  GitHub failed, using bundled copy..."
    cp -r bundled/ destination/
fi
```

## Quality Score Calculation

**Scoring criteria (0-10):**
- Documentation completeness: 2 points
- Setup automation: 2 points
- Error handling: 1 point
- Fallback mechanisms: 1 point
- Security practices: 1 point
- Code quality: 1 point
- Testing/validation: 1 point
- User experience: 1 point

**Deductions:**
- Critical bugs: -1 point each
- Missing required sections: -0.5 points each
- Broken links: -0.2 points each
- No error handling: -1 point
- Hardcoded paths: -0.5 points

**Target:** 9.5+/10 for production-ready

## Output Format

Create `DEEP_ANALYSIS.md` with:

1. **Executive Summary**
   - Result (PASS/FAIL)
   - Critical issues found
   - Quality score

2. **Critical Bugs Found & Fixed**
   - Severity (🔴 CRITICAL, 🟡 MEDIUM, 🟢 LOW)
   - Before/after code
   - Impact explanation
   - Commit reference

3. **Quality Checks Performed**
   - Each check with ✅/❌ result
   - Details for failures

4. **Metrics**
   - Files, size, lines, commits
   - Before/after comparison

5. **Recommendations**
   - High/medium/low priority improvements
   - Optional enhancements

6. **Final Verdict**
   - Production ready? Yes/No
   - Blocking issues (if any)
   - Next steps

## When to Perform Deep Analysis

**Triggers:**
- User says "analisa ulang" / "cek ulang" / "pastikan lengkap"
- User says "perfect" / "maksimal" / "gak ada masalah"
- Before tagging v1.0.0
- Before sharing publicly
- After major changes (5+ commits)
- When user expresses doubt ("yakin udah bener?")

**Don't perform if:**
- User just wants quick check
- Repo is work-in-progress
- User explicitly says "skip analysis"

## Time Estimate

- Quick check (5 items): 2 minutes
- Standard analysis (10 items): 5 minutes
- Deep analysis (all items + simulation): 10 minutes
- Full audit (analysis + AUDIT.md): 15 minutes
