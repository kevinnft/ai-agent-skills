# Setup Script Patterns & Best Practices

Common patterns for creating robust, user-friendly setup scripts.

## Script Header

```bash
#!/bin/bash
# Project Name Setup Script
# Auto-installs and configures everything

set -e  # Exit on error
```

**Why `set -e`:**
- Stops execution on first error
- Prevents cascading failures
- User sees exactly where it failed

---

## Prerequisites Check

```bash
echo "🔍 Checking prerequisites..."

# Check for required command
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Installing..."
    sudo apt update && sudo apt install git -y
fi

# Check for required command (error if missing)
if ! command -v snap &> /dev/null; then
    echo "❌ Snap not found. Please install snapd first."
    exit 1
fi

echo "✅ Prerequisites OK"
echo ""
```

**Pattern:**
- Use `command -v` to check if command exists
- Redirect to `/dev/null` to suppress output
- Auto-install if possible, error if not

---

## User Input with Defaults

```bash
echo "📋 Configuration:"
read -p "GitHub username: " GITHUB_USER
read -p "Vault name (default: obsidian-vault): " VAULT_NAME
VAULT_NAME=${VAULT_NAME:-obsidian-vault}  # Use default if empty

echo ""
echo "🔑 Generate GitHub Personal Access Token:"
echo "   1. Open: https://github.com/settings/tokens/new?scopes=repo"
echo "   2. Click 'Generate token'"
echo "   3. Copy token (ghp_xxx...)"
echo ""
read -sp "Paste token here: " GITHUB_TOKEN  # -s = silent (no echo), -p = prompt
echo ""
echo ""
```

**Patterns:**
- `read -p "Prompt: " VAR` — Basic input
- `${VAR:-default}` — Use default if empty
- `read -sp "Prompt: " VAR` — Silent input (passwords/tokens)
- Provide clear instructions with links

---

## Conditional Installation

```bash
echo "📦 Installing Obsidian..."
if ! command -v obsidian &> /dev/null; then
    sudo snap install obsidian --classic
    echo "✅ Obsidian installed"
else
    echo "✅ Obsidian already installed"
fi
echo ""
```

**Pattern:**
- Check if already installed
- Install only if needed
- Provide feedback for both cases

---

## Config File Updates (No Duplicates)

```bash
# Setup GitHub authentication
echo "🔐 Configuring GitHub authentication..."
export GH_TOKEN="$GITHUB_TOKEN"

# Only add to bashrc if not already present
if ! grep -q "export GH_TOKEN=" ~/.bashrc 2>/dev/null; then
    echo "export GH_TOKEN='$GITHUB_TOKEN'" >> ~/.bashrc
    echo "✅ GitHub token saved to ~/.bashrc"
else
    # Update existing token
    sed -i "s|export GH_TOKEN=.*|export GH_TOKEN='$GITHUB_TOKEN'|" ~/.bashrc
    echo "✅ GitHub token updated in ~/.bashrc"
fi
echo ""
```

**Pattern:**
1. Check if entry exists: `grep -q "PATTERN" ~/.config`
2. If not: append with `>>`
3. If yes: update with `sed -i`
4. Different feedback for each case

**Why this matters:**
- Running script multiple times won't create duplicates
- Updates existing entries instead of appending
- User knows what happened (saved vs updated)

---

## Fallback Mechanisms

```bash
# Install obsidian-skills
echo "📦 Installing obsidian-skills..."
SKILLS_DIR="$HOME/.hermes/skills"
mkdir -p "$SKILLS_DIR"

if [ ! -d "$SKILLS_DIR/obsidian-skills" ]; then
    cd "$SKILLS_DIR"
    # Try cloning from GitHub first
    if git clone --depth 1 https://github.com/kepano/obsidian-skills.git 2>/dev/null; then
        echo "✅ obsidian-skills installed from GitHub (5 skills)"
    else
        # Fallback: copy from local repo
        echo "⚠️  GitHub clone failed, using bundled copy..."
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        cp -r "$SCRIPT_DIR/obsidian-skills" "$SKILLS_DIR/"
        echo "✅ obsidian-skills installed from bundle (5 skills)"
    fi
else
    echo "✅ obsidian-skills already installed"
fi
echo ""
```

**Pattern:**
1. Try primary method (GitHub clone)
2. If fails: use fallback (bundled copy)
3. Provide clear feedback for each path
4. No single point of failure

**Why this matters:**
- Works offline (after initial clone)
- Works if GitHub is down
- Works if repo is deleted/moved
- Resilient to network issues

---

## Creating Files with Variable Expansion

```bash
# Create initial files
cat > "00 Meta/Getting Started.md" << EOF
---
title: Getting Started
date: $(date +%Y-%m-%d)
tags:
  - meta
  - setup
---

# Getting Started

Welcome to your vault!

## 🚀 Next Steps

1. Open Obsidian: \`obsidian\`
2. Open this vault
3. Start creating notes!
EOF
```

**Key points:**
- Use `<< EOF` (no quotes) for variable expansion
- Date/variables expand: `$(date +%Y-%m-%d)`, `$USER`
- Escape backticks: `` \`command\` ``
- Escape dollar signs if needed: `\$100`

**Wrong (no expansion):**
```bash
cat > file.txt << 'EOF'  # ❌ Single quotes prevent expansion
date: $(date +%Y-%m-%d)
EOF
# Output: date: $(date +%Y-%m-%d)  ← LITERAL!
```

---

## Creating Files Without Expansion

```bash
# Create .gitignore (no expansion needed)
cat > .gitignore << 'EOF'
.obsidian/workspace.json
.obsidian/cache/
*.secret.md
*.private.md
.DS_Store
EOF
```

**Use `<< 'EOF'` when:**
- Content has many `$` or `` ` `` characters
- Writing shell scripts inside heredocs
- You want literal `$VARIABLE` in output

---

## Progress Indicators

```bash
echo "📦 Installing GitHub CLI..."
if ! command -v gh &> /dev/null; then
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>&1 | tail -1
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    sudo apt update 2>&1 | tail -1
    sudo apt install gh -y 2>&1 | tail -1
    echo "✅ GitHub CLI installed"
else
    echo "✅ GitHub CLI already installed"
fi
echo ""
```

**Pattern:**
- Use emoji for visual sections: 📦 🔍 ✅ ❌ ⚠️
- Suppress verbose output: `2>&1 | tail -1`
- Show only last line of long operations
- Clear section breaks with `echo ""`

---

## Summary Output

```bash
# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Summary:"
echo "   • Obsidian installed: ✅"
echo "   • Vault created: $VAULT_PATH"
echo "   • obsidian-skills installed: ✅ (5 skills)"
echo "   • GitHub repo: https://github.com/$GITHUB_USER/$VAULT_NAME"
echo "   • Hermes integration: ✅"
echo ""
echo "🎯 Next Steps:"
echo "   1. Open Obsidian: obsidian"
echo "   2. Open vault: $VAULT_PATH"
echo "   3. Start creating notes!"
echo ""
echo "📖 Documentation: https://github.com/$GITHUB_USER/$VAULT_NAME"
echo ""
```

**Pattern:**
- Visual separator (Unicode box drawing)
- Bullet points with emoji
- Show what was done
- Show next steps
- Provide links

---

## Error Handling

```bash
set -e  # Exit on error (at top of script)

# For operations that might fail but shouldn't stop script:
if ! some_command 2>/dev/null; then
    echo "⚠️  Warning: some_command failed, continuing..."
fi

# For critical operations:
if ! critical_command; then
    echo "❌ Error: critical_command failed"
    echo "Please check logs and try again"
    exit 1
fi
```

**Pattern:**
- Use `set -e` for automatic error handling
- Use `if !` for operations that might fail
- Provide helpful error messages
- Exit with non-zero code on critical failures

---

## Script Directory Detection

```bash
# Get directory where script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use for relative paths
cp -r "$SCRIPT_DIR/bundled-deps" "$DESTINATION/"
```

**Why:**
- Works regardless of where script is called from
- Allows bundling dependencies with script
- Enables fallback mechanisms

---

## Complete Template

```bash
#!/bin/bash
# Project Name Setup Script
# Auto-installs and configures everything

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Project Name Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Installing..."
    sudo apt update && sudo apt install git -y
fi
echo "✅ Prerequisites OK"
echo ""

# Get user input
echo "📋 Configuration:"
read -p "Username: " USERNAME
read -p "Project name (default: my-project): " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-my-project}
echo ""

# Install components
echo "📦 Installing components..."
if ! command -v component &> /dev/null; then
    sudo apt install component -y
    echo "✅ Component installed"
else
    echo "✅ Component already installed"
fi
echo ""

# Configure
echo "⚙️ Configuring..."
if ! grep -q "CONFIG_LINE" ~/.config 2>/dev/null; then
    echo "CONFIG_LINE" >> ~/.config
    echo "✅ Configuration saved"
else
    sed -i "s|OLD_CONFIG|NEW_CONFIG|" ~/.config
    echo "✅ Configuration updated"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Summary:"
echo "   • Component installed: ✅"
echo "   • Configuration: ✅"
echo ""
echo "🎯 Next Steps:"
echo "   1. Run: component --help"
echo "   2. Start using!"
echo ""
```

---

## Testing Setup Scripts

### Syntax Check
```bash
bash -n setup.sh
```

### Dry-Run Simulation
```bash
# Create test script that simulates without executing
# Check all paths, variables, logic
```

### Multiple Runs Test
```bash
# Run script twice
./setup.sh
./setup.sh

# Check for duplicates
grep -c "CONFIG_LINE" ~/.config  # Should be 1, not 2!
```

### Clean System Test
```bash
# Test on fresh VM or container
# Ensures all dependencies are captured
```

---

## Common Mistakes

1. **No duplicate check** → Config files grow with each run
2. **Single-quoted heredoc** → Variables don't expand
3. **No fallback** → Single point of failure
4. **Hardcoded paths** → Breaks on different systems
5. **No error handling** → Silent failures
6. **No user feedback** → User doesn't know what happened
7. **Verbose output** → Cluttered terminal

---

## Best Practices Summary

✅ **DO:**
- Check before appending to config files
- Use unquoted heredoc for variable expansion
- Provide fallback mechanisms
- Give clear user feedback
- Suppress verbose output
- Test by running multiple times
- Use `set -e` for error handling

❌ **DON'T:**
- Append to config files without checking
- Use single-quoted heredoc when you need expansion
- Rely on single source (no fallback)
- Use hardcoded paths
- Show verbose output for every command
- Assume script runs only once
