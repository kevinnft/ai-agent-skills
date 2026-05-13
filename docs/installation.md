# Installation Guide

Complete guide to installing AI Agent Skills for various AI coding agents.

---

## 🎯 Quick Start

### For Hermes Agent (Recommended)

```bash
# Clone repository
git clone https://github.com/kevinnft/ai-agent-skills.git
cd ai-agent-skills

# Install all skills
./scripts/install.sh

# Restart Hermes
# Skills will auto-load on next session
```

---

## 📦 Installation Methods

### Method 1: Auto-Install Script (Recommended)

The installation script handles everything automatically:

```bash
# Install all skills
./scripts/install.sh --all

# Install specific category
./scripts/install.sh --category addyosmani

# Validate before installing
./scripts/install.sh --all --validate

# List available categories
./scripts/install.sh --list
```

**Features:**
- ✅ Automatic target detection
- ✅ Validation before install
- ✅ Progress tracking
- ✅ Error handling
- ✅ Colored output

---

### Method 2: Manual Installation

#### For Hermes Agent

```bash
# Copy all skills
cp -r skills/* ~/.hermes/skills/

# Or copy specific category
cp -r skills/addyosmani ~/.hermes/skills/
```

#### For Claude Code

```bash
# Copy all skills
cp -r skills/* ~/.claude/skills/

# Or use install script
./scripts/install.sh --agent claude
```

#### For Cursor

```bash
# Copy all skills
cp -r skills/* ~/.cursor/skills/

# Or use install script
./scripts/install.sh --agent cursor
```

#### For Custom Agent

```bash
# Specify custom target directory
./scripts/install.sh --target /path/to/your/agent/skills
```

---

## 🔧 Installation Options

### Install All Skills

```bash
./scripts/install.sh --all
```

Installs all 189 skills across 26 populated categories.

---

### Install Specific Category

```bash
# Install addyosmani skills (22 skills)
./scripts/install.sh --category addyosmani

# Install mattpocock skills (28 skills)
./scripts/install.sh --category mattpocock

# Install superpowers skills (14 skills)
./scripts/install.sh --category superpowers
```

---

### Install with Validation

```bash
# Validate before installing
./scripts/install.sh --all --validate

# Validates:
# - YAML frontmatter
# - Required fields
# - Markdown structure
# - Name format
```

---

### List Available Categories

```bash
./scripts/install.sh --list
```

Shows all populated categories with skill counts.

---

## ✅ Verification

### Verify Installation

#### For Hermes Agent

```bash
# List installed skills
hermes skills list

# Check specific category
hermes skills list | grep addyosmani

# Test a skill
hermes chat -q "Use brainstorming to design a feature"
```

#### Manual Verification

```bash
# Count installed skills
find ~/.hermes/skills -name "SKILL.md" | wc -l

# Should show 189 (if all installed)
```

---

## 🔄 Updating Skills

### Update to Latest Version

```bash
cd ai-agent-skills

# Pull latest changes
git pull origin main

# Reinstall
./scripts/install.sh --all
```

### Update Specific Category

```bash
# Pull latest
git pull origin main

# Reinstall category
./scripts/install.sh --category addyosmani
```

---

## 🐛 Troubleshooting

### Skills Not Loading

**Problem:** Skills don't appear after installation

**Solution:**
1. Restart your AI agent
2. Check target directory:
   ```bash
   ls ~/.hermes/skills/
   ```
3. Verify SKILL.md files exist:
   ```bash
   find ~/.hermes/skills -name "SKILL.md" | wc -l
   ```

---

### Permission Denied

**Problem:** `Permission denied` when running install script

**Solution:**
```bash
# Make script executable
chmod +x scripts/install.sh

# Run again
./scripts/install.sh
```

---

### Validation Errors

**Problem:** Validation fails during installation

**Solution:**
1. Check which skills failed:
   ```bash
   ./scripts/validate.sh
   ```
2. Report issue on GitHub
3. Install without validation:
   ```bash
   ./scripts/install.sh --all
   ```

---

### Wrong Target Directory

**Problem:** Skills installed to wrong location

**Solution:**
```bash
# Specify correct target
./scripts/install.sh --target ~/.hermes/skills

# Or specify agent type
./scripts/install.sh --agent hermes
```

---

## 📋 Requirements

### System Requirements

- **OS:** Linux, macOS, Windows (WSL)
- **Shell:** Bash 4.0+
- **Disk Space:** ~25 MB
- **Dependencies:** None (pure markdown)

### Agent Requirements

#### Hermes Agent
- Version: Any
- Config: Skills auto-load from `~/.hermes/skills/`

#### Claude Code
- Version: Any
- Config: Skills auto-load from `~/.claude/skills/`

#### Cursor
- Version: Any
- Config: Skills auto-load from `~/.cursor/skills/`

---

## 🎯 Post-Installation

### Next Steps

1. **Restart your agent** — Skills load on startup
2. **Test a skill** — Try `brainstorming` or `tdd`
3. **Read documentation** — Check [Usage Guide](./usage.md)
4. **Explore categories** — See [Categories](./categories.md)

### Recommended Skills to Try First

#### For Engineering:
- `addyosmani/code-review-and-quality` — Multi-axis code review
- `mattpocock/tdd` — Test-driven development
- `superpowers/brainstorming` — Before creative work

#### For Creative Work:
- `creative/architecture-diagram` — SVG diagrams
- `creative/excalidraw` — Hand-drawn diagrams
- `creative/ascii-art` — ASCII art generation

#### For DevOps:
- `devops/docker-compose` — Multi-container orchestration
- `devops/vps-security-hardening` — Security hardening

#### For Research:
- `research/web-scraping` — Data extraction
- `research/arxiv` — Paper search

---

## 🤝 Getting Help

### Documentation
- [Usage Guide](./usage.md)
- [Categories Overview](./categories.md)
- [Contributing Guide](../CONTRIBUTING.md)

### Support
- [GitHub Issues](https://github.com/kevinnft/ai-agent-skills/issues)
- [Discussions](https://github.com/kevinnft/ai-agent-skills/discussions)

---

## 📄 License

MIT License - see [LICENSE](../LICENSE)

---

**Installation complete!** 🎉

Start using your 189 production-ready skills now!
