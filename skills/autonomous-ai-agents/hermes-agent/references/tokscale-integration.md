# tokscale Integration — Token Usage Tracking for Hermes

**Tool:** tokscale v2.1.0  
**Author:** junhoyeo  
**Stars:** 1,690  
**Purpose:** Track token usage and costs across AI coding tools (Hermes, Code Assistant, Codex, Cursor, etc.)

---

## Installation

```bash
# Install via npm (Hermes uses custom node install)
npm install -g tokscale

# Verify installation
~/.hermes/node/bin/tokscale --version
# Output: tokscale 2.1.0
```

**Path resolution:** Hermes npm installs to `~/.hermes/node/bin/`, NOT the system default. The `tokscale` binary will be at `~/.hermes/node/bin/tokscale`.

---

## Setup

### Add alias for convenience

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'alias tokscale="$HOME/.hermes/node/bin/tokscale"' >> ~/.bashrc
source ~/.bashrc

# Now you can use:
tokscale models
```

### Auto-detection

tokscale automatically detects Hermes sessions by scanning `~/.hermes/state.db`. No configuration needed.

**Verification:**
```bash
tokscale clients
# Should show:
#   Hermes Agent
#   sessions: ~/.hermes/state.db ✓
#   messages: 3.3K
```

---

## Usage

### Basic commands

```bash
# Usage by model
tokscale models

# Monthly report
tokscale monthly

# Hourly breakdown
tokscale hourly

# Interactive TUI
tokscale tui

# Check detected clients
tokscale clients

# Export as JSON
tokscale models --json
```

### Example output

```bash
$ tokscale models
```

```
AI token usage analytics

┌─────────────────────────────┬──────────┬────────────┬──────────┬────────┐
│ Model                       │ Messages │ Input      │ Output   │ Cost   │
├─────────────────────────────┼──────────┼────────────┼──────────┼────────┤
│ claude-opus-4-6             │ 1,508    │ 15.2M      │ 214K     │ $81.51 │
│ claude-sonnet-4-5           │ 1,446    │ 5.0M       │ 100K     │ $16.55 │
│ claude-sonnet-4-5-thinking  │ 348      │ 0          │ 80K      │ $1.20  │
├─────────────────────────────┼──────────┼────────────┼──────────┼────────┤
│ Total                       │ 3,302    │ 20.2M      │ 395K     │ $99.26 │
└─────────────────────────────┴──────────┴────────────┴──────────┴────────┘
```

### JSON export for analysis

```bash
# Export current stats
tokscale models --json > ~/token-usage-$(date +%Y%m%d).json

# Example output:
{
  "groupBy": "client,model",
  "entries": [
    {
      "client": "hermes",
      "model": "claude-opus-4-6",
      "provider": "custom",
      "input": 15227082,
      "output": 214863,
      "messageCount": 1508,
      "cost": 81.50698499999997
    }
  ],
  "totalInput": 20242549,
  "totalOutput": 395233,
  "totalMessages": 3302,
  "totalCost": 99.25893599999998
}
```

---

## Integration with Hermes Workflow

### Daily check

```bash
# Morning routine
tokscale models

# Check if costs are trending up
tokscale monthly
```

### Cost optimization

1. **Identify expensive models:**
   ```bash
   tokscale models --json | jq '.entries | sort_by(.cost) | reverse | .[0:3]'
   ```

2. **Track usage patterns:**
   ```bash
   tokscale hourly
   # Identify peak usage times
   ```

3. **Set budget alerts** (manual):
   ```bash
   # Export daily, compare to threshold
   COST=$(tokscale models --json | jq '.totalCost')
   if (( $(echo "$COST > 100" | bc -l) )); then
     echo "Warning: Token costs exceeded $100"
   fi
   ```

### Multi-tool tracking

tokscale tracks all AI coding tools in one place:
- Hermes Agent
- Code Assistant
- Codex CLI
- Cursor IDE
- OpenCode
- Copilot CLI
- And 15+ others

**View all:**
```bash
tokscale clients
```

---

## Troubleshooting

### Command not found after install

**Symptom:**
```bash
$ tokscale --version
bash: tokscale: command not found
```

**Cause:** Hermes npm is not in default PATH.

**Fix:**
```bash
# Option 1: Use full path
~/.hermes/node/bin/tokscale --version

# Option 2: Add alias (recommended)
echo 'alias tokscale="$HOME/.hermes/node/bin/tokscale"' >> ~/.bashrc
source ~/.bashrc

# Option 3: Add to PATH
echo 'export PATH="$HOME/.hermes/node/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Shows 0 messages for Hermes

**Symptom:**
```bash
$ tokscale clients
Hermes Agent
sessions: ~/.hermes/state.db ✗
messages: 0
```

**Cause:** Session database not found or not readable.

**Fix:**
```bash
# Check if database exists
ls -lh ~/.hermes/state.db

# Check permissions
chmod 644 ~/.hermes/state.db

# Verify Hermes is using the default location
hermes config path
```

### JSON export fails

**Symptom:**
```bash
$ tokscale models --json
Error: ...
```

**Cause:** Old version or corrupted data.

**Fix:**
```bash
# Update tokscale
npm install -g tokscale@latest

# Clear cache (if needed)
rm -rf ~/.config/tokscale/cache
```

---

## Advanced Usage

### Headless capture (for Codex CLI only)

tokscale can capture token usage from subprocess output:

```bash
tokscale headless codex chat -q "Hello"
```

**Note:** Headless capture only works for Codex CLI. Hermes usage is tracked automatically via `state.db`.

### Social platform (optional)

tokscale has a social platform for sharing usage stats:

```bash
# Login (opens browser for GitHub auth)
tokscale login

# Submit usage data
tokscale submit

# Generate year-in-review
tokscale wrapped
```

**Privacy:** Submission is opt-in. Local tracking works without login.

---

## Maintenance

### Update tokscale

```bash
npm install -g tokscale@latest
```

### Check for new features

```bash
tokscale --help
```

### Backup usage data

tokscale stores data in `~/.config/tokscale/`. Backup if needed:

```bash
tar -czf tokscale-backup-$(date +%Y%m%d).tar.gz ~/.config/tokscale/
```

---

## Integration Checklist

After installing tokscale:

- [ ] Add alias to `~/.bashrc` for convenience
- [ ] Run `tokscale clients` to verify Hermes detection
- [ ] Run `tokscale models` to see current usage
- [ ] Set up daily check routine (e.g., morning `tokscale models`)
- [ ] (Optional) Export JSON for custom analysis
- [ ] (Optional) Set up budget alerts

---

## References

- **GitHub:** https://github.com/junhoyeo/tokscale
- **NPM:** https://www.npmjs.com/package/tokscale
- **Hermes npm location:** `~/.hermes/node/bin/`
- **Session database:** `~/.hermes/state.db`
