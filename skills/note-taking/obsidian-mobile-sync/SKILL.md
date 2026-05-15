---
name: obsidian-mobile-sync
description: Setup Obsidian mobile sync via GitHub (free) or Obsidian Sync (paid). Includes GitHub CLI automation, MGit/Working Copy setup, and Mnemosyne integration patterns.
origin: unknown
source_license: see upstream
language: en
---

# Obsidian Mobile Sync

Setup mobile access to Obsidian vault via GitHub sync (free) or Obsidian Sync (paid).

## CRITICAL Pitfall

**"Obsidian doesn't need login"** — WRONG for mobile sync.

- Desktop-only: No account needed
- Mobile sync: Requires authentication (Obsidian Sync OR Git sync)

Always clarify sync requirements when user asks about mobile access.

## Sync Options

**ALWAYS present free options FIRST.** Users expect cost-free solutions by default.

### Option 1: Git Sync (Free) ⭐ RECOMMENDED

**Cost:** $0 (100% free)  
**Setup:** Push to GitHub → Install Obsidian Git plugin (desktop)  
**Mobile:**
- **Android:** MGit (free) — full Git functionality
- **iOS:** Working Copy (free for pull, $19.99 for push) OR iSH + Git (free, terminal-based)

**Pros:** Free, version control, forever history, no vendor lock-in  
**Cons:** Manual sync on mobile (2-3 taps per session)

**iOS Free Alternative:** iSH app + Git CLI (100% free, no purchase needed)

### Option 2: Obsidian Sync (Paid)

**Cost:** $10/month or $96/year  
**Setup:** Create account → Subscribe → Enable sync  
**Mobile:** Install app → Sign in → Select vault  
**Pros:** Auto-sync, conflict resolution, E2E encrypted, zero manual work  
**Cons:** Paid subscription ($120/year)

**When to recommend:** User explicitly values convenience over cost, or has budget for premium tools.

## GitHub CLI Setup (Recommended)

**Install:**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh -y
```

**Login:**
```bash
gh auth login
# Select: GitHub.com → HTTPS → Yes → Login with browser
```

**Scope Management:** `gh auth login` grants basic scopes (`repo`, `workflow`, `read:org`). If you need to delete repos later, add `delete_repo` scope:
```bash
gh auth refresh -h github.com -s delete_repo
```
This prevents "HTTP 403: needs delete_repo scope" errors when running `gh repo delete`.

**Create repo + push (one command):**
```bash
cd ~/Documents/Obsidian\ Vault
gh repo create obsidian-vault --private --source=. --remote=origin --push
```

## Obsidian Git Plugin (Desktop Auto-Sync)

**Install:** Settings → Community plugins → Browse → "Obsidian Git"

**Configure:**
- Vault backup interval: 10 minutes
- Auto push interval: 30 minutes
- Auto pull interval: 10 minutes
- Commit message: `vault backup: {{date}}`

**Result:** Zero manual work on desktop.

## Mobile Setup

### Android (MGit)

1. Install Obsidian + MGit from Play Store
2. MGit → Clone repository:
   - URL: `https://github.com/USERNAME/obsidian-vault.git`
   - Path: `/storage/emulated/0/Obsidian/vault`
   - Auth: Username + Personal Access Token
3. Obsidian → Open folder as vault → Select cloned folder

**Sync:** Pull before edit, Commit + Push after edit

### iOS Option A: iSH + Git (Free) ⭐

**100% free, no purchase needed.**

1. Install Obsidian + iSH Shell from App Store (both free)
2. In iSH terminal:
   ```bash
   apk add git
   cd ~
   git clone https://USERNAME:TOKEN@github.com/USERNAME/obsidian-vault.git
   ```
3. Obsidian → Open folder as vault → On My iPhone → iSH → obsidian-vault

**Sync workflow:**
```bash
# Pull (before edit)
cd ~/obsidian-vault && git pull

# Push (after edit)
cd ~/obsidian-vault
git add .
git commit -m "Update from iOS"
git push
```

**Pros:** Free, full Git functionality  
**Cons:** Terminal-based (not GUI)

### iOS Option B: Working Copy (Paid for Push)

**Free for pull, $19.99 one-time for push to private repos.**

1. Install Obsidian + Working Copy from App Store
2. Working Copy → Clone → URL → Paste repo URL → Auth with token
3. Obsidian → Open folder as vault → Working Copy → Select repo

**Sync:** Pull before edit, Commit + Push after edit (requires Pro)

## Mnemosyne Integration Pattern

Store **pointers** in Mnemosyne, not full content:

```python
# Good: Store pointer
mnemosyne_remember(
  content="VPS cleanup: [[VPS Cleanup]]",
  importance=0.7,
  source="reference"
)

# Bad: Store full content
mnemosyne_remember(
  content="VPS cleanup steps: 1. df -h, 2. apt clean...",
  importance=0.7,
  source="reference"
)
```

**Strategy:**
- Mnemosyne (40%): Preferences, environment facts, **pointers**
- Obsidian (60%): Project docs, notes, tasks, diagrams

**Workflow:**
1. User asks about topic
2. Mnemosyne recalls pointer: "See [[Note Name]]"
3. Agent reads full content: `read_file(path="~/Documents/Obsidian Vault/Note Name.md")`

See `references/mnemosyne-integration-examples.md` for real workflow examples.

**Complete setup workflow:** Full Mnemosyne + Obsidian + GitHub integration takes ~30 minutes. Components: Obsidian (Snap), obsidian-skills (5 skills), GitHub CLI, Git, Mnemosyne. Result: 40% Mnemosyne (fast recall, pointers) + 60% Obsidian (rich content, Bases, Canvas) + GitHub backup. Production ready, zero maintenance, permanent.

**GitHub token for autonomous operations:** See `references/github-token-permanent-access.md` for permanent token setup (enables autonomous repo operations without repeated auth prompts).

## Automation Script

```bash
#!/bin/bash
# Save as ~/setup_obsidian_github.sh
set -e

gh auth status || { echo "Run: gh auth login"; exit 1; }
USERNAME=$(gh api user -q .login)
cd ~/Documents/Obsidian\ Vault
git remote remove origin 2>/dev/null || true

gh repo create obsidian-vault \
    --private \
    --source=. \
    --remote=origin \
    --push \
    --description="Obsidian vault with Mnemosyne integration"

echo "✅ Repo: https://github.com/$USERNAME/obsidian-vault"
```

Run: `chmod +x ~/setup_obsidian_github.sh && ~/setup_obsidian_github.sh`

## Conflict Resolution

If merge conflict:
1. Pull shows conflict
2. Open file, look for markers:
   ```
   <<<<<<< HEAD
   Your changes
   =======
   Remote changes
   >>>>>>> origin/master
   ```
3. Edit to resolve
4. Commit + Push

## Pitfalls

**Recommending paid solutions first** — Users expect free options by default. Always present Git sync (free) before Obsidian Sync (paid). Only recommend paid when user explicitly values convenience or has budget.

**iOS: Recommending Working Copy without mentioning cost** — Working Copy is free for pull but requires $19.99 Pro for push to private repos. **User frustration signal:** "Bayar anjir working copy untuk push, ngapa lo saranin ini lol" — Always present iSH + Git (100% free) as primary option, Working Copy as secondary paid alternative.

**Using GitHub password** — Deprecated. Use Personal Access Token (https://github.com/settings/tokens/new with `repo` scope).

**Not pulling before editing** — Always pull first on mobile to avoid conflicts.

**Storing full content in Mnemosyne** — Wastes memory. Store wikilink pointers instead.

**Claiming no login needed** — True for desktop-only, false for mobile sync.
