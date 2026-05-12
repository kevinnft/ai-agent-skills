# Critical Bash Pitfalls in Setup Scripts

Common bugs found in production setup scripts that cause silent failures or duplicate configurations.

---

## 1. Token/Config Duplication in Bashrc

### Problem

Appending configuration to `~/.bashrc` without checking if it already exists.

**Impact:** Running setup script multiple times creates duplicate entries.

### Bad Code

```bash
echo "export GH_TOKEN='$GITHUB_TOKEN'" >> ~/.bashrc
```

**Result after 3 runs:**
```bash
export GH_TOKEN='ghp_abc123'
export GH_TOKEN='ghp_abc123'
export GH_TOKEN='ghp_abc123'
```

### Good Code

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

**Benefits:**
- First run: adds new line
- Subsequent runs: updates existing line (no duplicates)
- User feedback: different messages for add vs update

### Real-World Impact

**Repo:** mnemosyne-obsidian  
**Commit:** `9cfbf55` — "CRITICAL FIX: Prevent duplicate token in bashrc + fix date expansion in heredoc"  
**Severity:** 🔴 CRITICAL  
**Found by:** Deep analysis (manual code review)

---

## 2. Variable Expansion in Single-Quoted Heredoc

### Problem

Using single-quoted heredoc delimiter (`<< 'EOF'`) prevents variable expansion.

**Impact:** Variables and command substitutions appear as literal strings in output files.

### Bad Code

```bash
cat > "Getting Started.md" << 'EOF'
---
title: Getting Started
date: $(date +%Y-%m-%d)
---

# Getting Started

Run: `obsidian`
EOF
```

**Output:**
```markdown
---
title: Getting Started
date: $(date +%Y-%m-%d)  ← LITERAL STRING!
---

# Getting Started

Run: `obsidian`
```

### Good Code

```bash
cat > "Getting Started.md" << EOF
---
title: Getting Started
date: $(date +%Y-%m-%d)
---

# Getting Started

Run: \`obsidian\`
EOF
```

**Output:**
```markdown
---
title: Getting Started
date: 2026-05-12  ← ACTUAL DATE!
---

# Getting Started

Run: `obsidian`
```

**Key points:**
- Remove quotes from heredoc delimiter: `<< EOF` (not `<< 'EOF'`)
- Escape backticks in content: `` \`command\` ``
- Escape dollar signs if needed: `\$VAR`

### When to Use Single Quotes

Use `<< 'EOF'` when you want **literal** content (no expansion):

```bash
cat > script.sh << 'EOF'
#!/bin/bash
echo "Current user: $USER"  # Literal $USER, not expanded
EOF
```

**Output:**
```bash
#!/bin/bash
echo "Current user: $USER"  # Will expand when script runs
```

### Real-World Impact

**Repo:** mnemosyne-obsidian  
**Commit:** `9cfbf55` — "CRITICAL FIX: Prevent duplicate token in bashrc + fix date expansion in heredoc"  
**Severity:** 🟡 MEDIUM  
**Found by:** Deep analysis (manual code review)  
**User impact:** Getting Started note showed literal `$(date +%Y-%m-%d)` instead of actual date

---

## 3. Missing Error Handling in Conditional Blocks

### Problem

Not checking exit codes in conditional blocks can hide failures.

### Bad Code

```bash
if git clone https://github.com/external/tool.git; then
    echo "✅ Installed from GitHub"
else
    echo "⚠️  Using bundled copy"
    cp -r bundled-tool/ /install/path/
fi
```

**Issue:** If `cp` fails, script continues silently.

### Good Code

```bash
if git clone --depth 1 https://github.com/external/tool.git 2>/dev/null; then
    echo "✅ Installed from GitHub (latest)"
else
    echo "⚠️  GitHub clone failed, using bundled copy..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if ! cp -r "$SCRIPT_DIR/bundled-tool" "$INSTALL_DIR/"; then
        echo "❌ Failed to copy bundled tool"
        exit 1
    fi
    echo "✅ Installed from bundle"
fi
```

**Improvements:**
- `--depth 1` for faster clone
- `2>/dev/null` to suppress error output
- Check `cp` exit code
- Exit on failure (with `set -e` at top)

---

## 4. Path Expansion Issues

### Problem

Not quoting paths with spaces causes word splitting.

### Bad Code

```bash
VAULT_PATH=$HOME/Documents/Obsidian Vault
mkdir -p $VAULT_PATH
```

**Result:** Creates 3 directories: `~/Documents/Obsidian`, `Vault`, and current directory.

### Good Code

```bash
VAULT_PATH="$HOME/Documents/Obsidian Vault"
mkdir -p "$VAULT_PATH"
```

**Rule:** Always quote variables that contain paths.

---

## 5. Unsafe User Input

### Problem

Not validating user input can cause command injection or path traversal.

### Bad Code

```bash
read -p "Project name: " PROJECT_NAME
mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"
```

**Attack:** User enters `../../etc` → creates directory outside intended location.

### Good Code

```bash
read -p "Project name: " PROJECT_NAME

# Validate: alphanumeric, dash, underscore only
if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "❌ Invalid project name. Use only letters, numbers, dash, underscore."
    exit 1
fi

mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"
```

**Validation patterns:**
- Alphanumeric: `^[a-zA-Z0-9_-]+$`
- Email: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- URL: `^https?://[a-zA-Z0-9.-]+`

---

## Testing Checklist

Before releasing setup script:

- [ ] Run script multiple times (check for duplicates)
- [ ] Check generated files for literal `$VAR` or `$(command)`
- [ ] Test with paths containing spaces
- [ ] Test with invalid user input
- [ ] Test with network disconnected (fallback logic)
- [ ] Test with missing prerequisites
- [ ] Run `bash -n script.sh` (syntax check)
- [ ] Run `shellcheck script.sh` (if available)

---

## Quick Reference

| Issue | Bad | Good |
|-------|-----|------|
| **Bashrc duplication** | `echo "..." >> ~/.bashrc` | `if ! grep -q "..."; then echo "..." >> ~/.bashrc; fi` |
| **Heredoc expansion** | `<< 'EOF'` | `<< EOF` (escape backticks: `` \` ``) |
| **Path with spaces** | `$VAULT_PATH` | `"$VAULT_PATH"` |
| **User input** | `mkdir "$INPUT"` | Validate first: `[[ "$INPUT" =~ ^[a-zA-Z0-9_-]+$ ]]` |
| **Error handling** | `cp file dest` | `if ! cp file dest; then exit 1; fi` |

---

## Real-World Example

**Repo:** https://github.com/kevinnft/mnemosyne-obsidian  
**Bugs found:** 2 critical (token duplication, date expansion)  
**Fixed in:** Commit `9cfbf55`  
**Impact:** Setup script now idempotent (can run multiple times safely)
