# Critical Bugs Found in mnemosyne-obsidian Repository

**Session:** 2026-05-12  
**Repository:** https://github.com/kevinnft/mnemosyne-obsidian  
**Context:** Creating production-ready public repo for Mnemosyne + Obsidian + GitHub Backup integration

## Bug #1: Token Duplication in ~/.bashrc

**Severity:** 🔴 CRITICAL  
**Impact:** Running setup.sh multiple times appends duplicate tokens to ~/.bashrc

### Problem Code

```bash
# setup.sh line 98 (BROKEN)
echo "export GH_TOKEN='$GITHUB_TOKEN'" >> ~/.bashrc
```

**What happens:**
- First run: Adds token to ~/.bashrc ✅
- Second run: Adds ANOTHER token to ~/.bashrc ❌
- After 10 runs: 10 duplicate tokens in ~/.bashrc ❌

### Root Cause

Using `>>` (append) without checking if entry already exists.

### Fix

```bash
# Only add to bashrc if not already present
if ! grep -q "export GH_TOKEN=" ~/.bashrc 2>/dev/null; then
    echo "export GH_TOKEN='$GITHUB_TOKEN'" >> ~/.bashrc
    echo "✅ GitHub token saved to ~/.bashrc"
else
    # Update existing token
    sed -i "s|export GH_TOKEN=.*|export GH_TOKEN='$GITHUB_TOKEN'|" ~/.bashrc
    echo "✅ GitHub token updated in ~/.bashrc"
fi
```

**Key points:**
1. Check if pattern exists: `grep -q "export GH_TOKEN=" ~/.bashrc`
2. If not found: append new line
3. If found: update existing line with `sed -i`
4. Provide different feedback (saved vs updated)

### General Pattern

```bash
# Pattern for any config file
if ! grep -q "PATTERN" ~/.config 2>/dev/null; then
    echo "NEW_LINE" >> ~/.config  # Add new
else
    sed -i "s|OLD_PATTERN|NEW_PATTERN|" ~/.config  # Update existing
fi
```

**Use cases:**
- Adding environment variables to ~/.bashrc
- Adding aliases to ~/.bash_aliases
- Adding entries to ~/.ssh/config
- Adding lines to any config file that might be run multiple times

---

## Bug #2: Date Not Expanding in Heredoc

**Severity:** 🟡 MEDIUM  
**Impact:** Getting Started.md shows literal `$(date +%Y-%m-%d)` instead of actual date

### Problem Code

```bash
# setup.sh line 117-120 (BROKEN)
cat > "00 Meta/Getting Started.md" << 'EOF'
---
title: Getting Started
date: $(date +%Y-%m-%d)
tags:
  - meta
  - setup
---
EOF
```

**Output in file:**
```yaml
date: $(date +%Y-%m-%d)  # ❌ LITERAL STRING!
```

### Root Cause

Single-quoted heredoc delimiter (`<< 'EOF'`) prevents variable and command expansion.

**Bash heredoc rules:**
- `<< EOF` — Variables and commands expand
- `<< 'EOF'` — No expansion (literal)
- `<< "EOF"` — Variables expand, commands expand

### Fix

```bash
# Remove quotes from heredoc delimiter
cat > "00 Meta/Getting Started.md" << EOF
---
title: Getting Started
date: $(date +%Y-%m-%d)
tags:
  - meta
  - setup
---

# Getting Started

1. Open Obsidian: \`obsidian\`  # Escape backticks!
2. Open this vault
3. Start creating notes!
EOF
```

**Output in file:**
```yaml
date: 2026-05-12  # ✅ ACTUAL DATE!
```

**Key points:**
1. Use `<< EOF` (no quotes) for expansion
2. Escape special characters that should be literal: `` \`backticks\` ``
3. Variables expand: `$HOME`, `$USER`, `$VAULT_PATH`
4. Commands expand: `$(date +%Y-%m-%d)`, `$(whoami)`

### When to Use Each

**Use `<< 'EOF'` (no expansion):**
- When content has many `$` or `` ` `` characters
- When writing shell scripts inside heredocs
- When you want literal `$VARIABLE` in output

**Use `<< EOF` (with expansion):**
- When you need current date/time
- When you need environment variables
- When you need computed values

**Example comparison:**

```bash
# No expansion (literal)
cat > script.sh << 'EOF'
#!/bin/bash
echo "User: $USER"  # Will print: User: $USER
EOF

# With expansion
cat > config.txt << EOF
#!/bin/bash
echo "User: $USER"  # Will print: User: ubuntu
EOF
```

### Escaping in Expanded Heredocs

When using `<< EOF` but need some literals:

```bash
cat > file.txt << EOF
# These expand:
Date: $(date +%Y-%m-%d)
User: $USER

# These are literal (escaped):
Price: \$100
Command: \`ls -la\`
Variable: \$HOME
EOF
```

**Output:**
```
Date: 2026-05-12
User: ubuntu
Price: $100
Command: `ls -la`
Variable: $HOME
```

---

## Testing & Prevention

### Syntax Check

```bash
bash -n setup.sh
# Should output nothing if syntax is valid
```

### Simulation Test

```bash
# Test date expansion
echo "Date: $(date +%Y-%m-%d)"
# Should output: Date: 2026-05-12

# Test heredoc expansion
cat << EOF
Date: $(date +%Y-%m-%d)
EOF
# Should output: Date: 2026-05-12
```

### Duplicate Prevention Test

```bash
# Run twice and check
./setup.sh  # First run
grep -c "export GH_TOKEN=" ~/.bashrc  # Should be 1

./setup.sh  # Second run
grep -c "export GH_TOKEN=" ~/.bashrc  # Should STILL be 1 (not 2!)
```

---

## Lessons Learned

1. **Always check before appending** to config files
2. **Use unquoted heredoc** (`<< EOF`) when you need expansion
3. **Test setup scripts** by running them multiple times
4. **Validate output** — check that dates/variables actually expanded
5. **Provide user feedback** — "saved" vs "updated" messages

---

## Related Patterns

See also:
- `setup-script-patterns.md` — More setup script best practices
- Skill: `public-repo-creation` — Full workflow for creating repos
