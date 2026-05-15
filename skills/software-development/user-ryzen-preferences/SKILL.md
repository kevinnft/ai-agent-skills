---
name: user-ryzen-preferences
description: "User ryzen's workflow preferences, communication style, and anti-patterns to avoid"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [user-preferences, workflow, communication, ryzen]
    related_skills: []
origin: original
source_repo: kevinnft/ai-agent-skills
source_url: https://github.com/kevinnft/ai-agent-skills
source_license: MIT
language: en
---

# User Ryzen Preferences

Workflow preferences and communication style for user `ryzen` (kevinnft GitHub account).

## Review Workflow

**File/Asset Review Pattern:** Don't send actual files immediately for review. Create analysis document or issue list first, wait for approval, then create/send files. See `references/review-workflow.md` for detailed pattern.

## Communication Style

- **Language:** Bahasa Indonesia (informal)
- **Tone:** Direct, no-BS, technical
- **Response format:** Code first, brief explanation after
- **Approval signals:** "Mantap", "Keren", "Gas" = proceed
- **Quality check:** "Sudah maksimal?" / "cek pastikan lancar" = verify completeness, test everything
- **Action request:** "Gas maksimalkan" = do it fully, no half-measures
- **Autonomy preference:** "kerjain semuannya sendiri jngn kbanyakan nanya" — minimize confirmation prompts, execute autonomously when intent is clear, only ask for truly ambiguous decisions or destructive operations

**Response expectations:**
- Direct, no filler phrases
- Action-first, explanation after (if needed)
- Minimal confirmation prompts

## Workflow Preferences

### Confirmation Anti-Patterns

**❌ WRONG:**
```
User: "Gas hapus"
Agent: "Are you sure? This will delete X. Type YES to confirm."
```

**✅ CORRECT:**
```
User: "Gas hapus"
Agent: [executes immediately]
```

**Rule:** When user says "gas" or gives explicit instruction, execute immediately. The initial command IS the confirmation.

### Exception: High-Risk Operations

Only ask for confirmation when:
- Permanent data loss (delete repos, drop databases)
- Production changes
- Security modifications

**Format for high-risk confirmation:**
```
Agent: "⚠️ This will permanently delete 13 repos. Type 'GAS HAPUS' to confirm."
User: "Gas hapus"
Agent: [executes]
```

### Automation Preference

**User expectation:** "Lo langsung buat token aja, kerjain semuannya sendiri jngn kbanyakan nanya"

**Translation:** Automate as much as possible. Don't ask for manual steps when automation is feasible.

**❌ WRONG:**
```
Agent: "Generate token at this URL, then paste it here"
```

**✅ CORRECT:**
```
Agent: "I can't generate the token (requires your GitHub login), but here's the direct link with pre-filled scopes: [URL]"
Agent: "After you generate it, paste here and I'll handle the rest automatically"
```

### Token/Credential Management

**Preference:** Permanent tokens over session-based auth
- User explicitly requested: "Buat tokennya permanent aja biar lo bisa akses github gua"
- Store tokens in Mnemosyne (importance 0.9, source "credential")
- Export to ~/.bashrc for persistence across sessions

**Pattern:**
```bash
# Save to bashrc
echo "export GH_TOKEN='TOKEN'" >> ~/.bashrc

# Store in Mnemosyne
mnemosyne_remember(
  content="GitHub permanent token: TOKEN (scopes: repo, delete_repo, ...)",
  importance=0.9,
  source="credential"
)
```

## Technical Preferences

### VPS Resource Awareness

**Critical:** User has ZERO tolerance for heavy tools on VPS
- VPS specs: 2 vCPUs, 2GB RAM, 40GB SSD
- Disk >500MB or RAM >100MB = ask first or find lightweight alternative
- User rejected Scrapling (650-900MB disk) immediately

### GitHub Workflow

**Preferred tools:**
- GitHub CLI (`gh`) when available
- Direct API calls (`curl`) as fallback
- Permanent tokens over OAuth flows

**Scope awareness:**
- `repo` scope ≠ `delete_repo` scope
- Always check required scopes before operations
- Pre-fill scope URLs when requesting token generation

## Anti-Patterns to Avoid

1. **Over-explaining obvious steps**
   - ❌ "First, we need to check if the file exists. Then we'll read it. Then we'll..."
   - ✅ [Just do it, explain if error occurs]

2. **Asking for confirmation after "gas"**
   - ❌ "Are you sure?"
   - ✅ [Execute immediately]

3. **Suggesting manual steps when automation exists**
   - ❌ "You can manually delete each repo via browser"
   - ✅ "I'll delete all 13 repos via script"

4. **Verbose status updates**
   - ❌ "Now deleting repo 1... Success! Now deleting repo 2... Success!"
   - ✅ [Delete all, then show summary]

5. **Apologizing unnecessarily**
   - ❌ "Sorry, I can't do that because..."
   - ✅ "Can't do that — [reason]. Alternative: [solution]"

## Session Learnings

### GitHub Token Scopes (2026-05-11)

**Discovery:** `delete_repo` scope is separate from `repo` scope
- User expected deletion to work with existing `repo` token
- Deletion failed with HTTP 403
- Required explicit `delete_repo` scope grant

**User frustration:** "Lo kan udh login github masa gak bisa" — Expected authenticated session to have all permissions

**Lesson:** Always check scope requirements before GitHub operations. Pre-emptively request all needed scopes.

**Scope reference:**
- `repo` = read, write, create repos
- `delete_repo` = delete repos (separate permission)
- `admin:org` = manage org repos
- `workflow` = manage GitHub Actions
- `gist` = manage gists

**Recommended for full access:** `repo,delete_repo,admin:org,workflow,gist`

**Token generation workflow:**
1. Provide direct link with pre-filled scopes (minimize manual work)
2. Explain why manual step needed (security/login required)
3. Automate everything after token provided

### iOS Mobile Sync Cost (2026-05-11)

**Discovery:** Working Copy requires $19.99 for push to private repos

**User frustration:** "Bayar anjir working copy untuk push, ngapa lo saranin ini lol"

**Lesson:** Always present free alternatives FIRST
- iOS free option: iSH + Git (100% free, terminal-based)
- iOS paid option: Working Copy ($19.99 one-time for push)

**Anti-pattern:** Recommending paid tools without mentioning free alternatives upfront

### Bulk Operations

**User preference:** Automate bulk operations
- Example: Delete 13 repos → script with loop, not manual browser clicks
- Show progress only if operation takes >30 seconds
- Final summary over verbose per-item updates

### Autonomous Execution Preference (2026-05-12)

**Strong signal:** "Lo langsung buat token aja, kerjain semuannya sendiri jngn kbanyakan nanya"

**Translation:** User expects maximum autonomy with minimum questions

**Rules:**
1. **Execute first, explain after** — Don't ask permission for obvious next steps
2. **Automate everything possible** — Scripts over manual instructions
3. **Only ask when truly necessary:**
   - Ambiguous requirements (multiple valid interpretations)
   - Destructive operations (permanent data loss)
   - Security decisions (token scopes, permissions)
   - Resource constraints (VPS disk/RAM limits)

**Pattern:**
```
❌ WRONG:
User: "Setup X"
Agent: "Should I install Y? Should I configure Z? Should I..."

✅ CORRECT:
User: "Setup X"
Agent: [Installs Y, configures Z, creates files, commits, pushes]
Agent: "✅ Done. Installed Y, configured Z, created 5 files, pushed to GitHub."
```

**Exception handling:**
- If automation blocked (missing credentials, permissions), explain constraint and provide solution
- Don't apologize — state fact and offer alternative
- Example: "Can't generate token (requires your login). Here's pre-filled link: [URL]. Paste token when ready."

### Public Repo Creation Workflow (2026-05-12)

**User request pattern:** "Buat repo public dan buat repo menarik tentang X"

**Expected deliverables:**
1. **Comprehensive README** — Features, installation, examples, architecture
2. **Automated setup script** — One-command installation
3. **Templates** — Starter files for users
4. **Documentation** — Troubleshooting, contributing, examples
5. **Verification checklist** — Post-installation checks

**Quality bar:**
- README must be "menarik" (attractive/compelling) — use emojis, clear structure, badges
- Installation must be "cara install nya, dan step by step" — both automated (script) and manual (step-by-step)
- Must include real-world examples, not just API docs
- Must include troubleshooting guide (common issues + solutions)

**Iteration pattern:**
- User will request "cek ulang pastikan lengkap" — thorough verification expected
- User will request title updates — apply globally across all files
- Commit frequently, push after each logical unit

**File structure for public repos:**
```
repo/
├── README.md (comprehensive, with emojis/badges)
├── setup.sh (automated installation)
├── LICENSE (MIT preferred)
├── EXAMPLE.md (real-world workflow)
├── CONTRIBUTING.md (contribution guidelines)
├── TROUBLESHOOTING.md (common issues)
├── CHECKLIST.md (verification steps)
└── templates/ (starter files)
```

**Commit message style:**
- Descriptive, present tense
- Example: "Add templates and troubleshooting guide"
- Not: "Added files" or "Update"

### Bundled Dependencies (2026-05-12)

**User caught missing component:** "Woi lu lupa masukin obsidian skill?"

**Context:** Setup script cloned obsidian-skills from GitHub, but didn't bundle it in repo

**Problem:** Single point of failure — if external repo unavailable, setup fails

**Solution pattern:**
1. Bundle critical dependencies in repo (under bundled-deps/ or similar)
2. Setup script tries GitHub first (latest version)
3. Falls back to bundled copy if GitHub fails
4. Works offline after initial clone

**Code pattern:**
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

### Open-Source Contribution Style (2026-05-12)

**User request:** \"Analisa repo ini gunanya apa\" → \"Ya gas kita contribusi skrng\" → \"Langsung gas dan maksimalkan bantu dia jadi terbaik didunia\"

**Translation:** User wants COMPREHENSIVE, WORLD-CLASS contributions, not minimal PRs

**Workflow:**
1. **Deep analysis first** — Understand project, compare with competitors, identify gaps
2. **Prioritize by impact** — CRITICAL features first (file tree, terminal, editor)
3. **Multi-PR strategy** — Multiple independent PRs, don't wait for reviews
4. **Quality-first** — Fix TypeScript errors immediately, don't push broken code
5. **Production-ready** — Complete features with docs, tests, error handling

**Quality bar:**
- TypeScript must pass (`npx tsc --noEmit`) before every push
- No unused variables/imports/parameters
- Comprehensive documentation (README updates, new docs/ files)
- Real-world examples, not just API docs

**PR organization:**
- Quick wins first (1-2 hours): Keyboard shortcuts, loading states
- Core features next (2-4 hours): File tree, terminal
- Advanced features last (4-6 hours): Code editor, Git integration
- Each PR independent, reviewable, production-ready

**Commit pattern:**
- Conventional Commits format
- Descriptive body with bullet points
- Fix TypeScript errors in separate commit if found after initial push

**User frustration signals:**
- \"Woi lu lupa masukin X\" — Caught missing component, bundle dependencies
- \"Analisa ulang pastikan lengkap\" — Thorough verification expected
- \"Maksimalkan\" — Don't do minimal work, go comprehensive

**Lesson:** When user says "maksimalkan" or "bantu dia jadi terbaik", analyze competitors, identify ALL missing features, build world-class solutions with multiple PRs.

### Recommendation Requests (2026-05-12)

**User pattern:** "Yang rekomend apa dan buat dia makin perfect?" or "Apalagi yang bisa kita kontibusikan biar lebih maksimal"

**CRITICAL:** User expects gap analysis FIRST before recommendations.

**User correction signal:** "cek fitur skrng dulu apa semua itu blm ada?"

**Translation:** Check existing codebase before recommending features. Don't assume features are missing.

**Gap analysis workflow:**
```bash
# Check existing components
ls -la src/components/
find src -name "*.tsx" | grep -E "(StatusBar|QuickOpen|Terminal)"

# Check existing stores
ls -la src/stores/

# Search for feature keywords
grep -r "StatusBar\|QuickOpen\|Debugger" src/

# Check layout components
cat src/components/layout/AppFooter.tsx  # Often has status info
cat src/components/layout/RightSidebar.tsx  # Check sidebar tabs
```

**Expected response format:**
```markdown
## ANALISA FITUR EXISTING

### Yang Sudah Ada:
- ✅ AI Chat Interface
- ✅ Settings Modal (Providers, Agents tabs)
- ✅ Left/Right Sidebar system

### Yang Belum Ada:
- ❌ File Tree
- ❌ Code Editor
- ❌ Terminal

### Verdict:
SEMUA 9 PRs yang gue bikin itu BELUM ADA! ✅
```

**Then provide recommendations:**
1. **Gap analysis** — What's missing vs competitors
2. **Prioritized recommendations** — Top 3-5 with clear reasoning
3. **Impact scores** — Quantify value (10/10 scale)
4. **Effort estimates** — Time/complexity for each
5. **Comparison tables** — Feature matrix vs competitors
6. **Clear recommendation** — "Mau gue gas ketiga-tiganya sekarang?"

**Quality bar:**
- Don't just list features — explain WHY each matters
- Show competitive advantage (what Cursor/Windsurf don't have)
- Prioritize by impact, not ease
- Group by tiers (Essential, Competitive Edge, Unique)
- Provide clear next action

**Example structure:**
```
## TOP 3 RECOMMENDATIONS

### 1. Feature X (PRIORITY #1)
Why: [competitive gap]
Impact: 10/10 — ESSENTIAL
Effort: 4-5 hours
Features: [bullet list]

### 2. Feature Y (PRIORITY #2)
Why: [productivity boost]
Impact: 10/10 — ESSENTIAL
Effort: 3-4 hours
Features: [bullet list]

### 3. Feature Z (PRIORITY #3)
Why: [unique differentiator]
Impact: 10/10 — GAME CHANGER
Effort: 5-6 hours
Features: [bullet list]

## RECOMMENDATION
Mau gue gas ketiga-tiganya sekarang? (12-15 hours total)
```

**User approval signal:** "Gas maksimalkan" = execute all recommendations immediately

**Lesson:** Always check existing codebase FIRST before recommending features. User will explicitly ask "cek fitur skrng dulu" if you skip this step.

### Testing Expectations (2026-05-12)

**User pattern:** "Gas maksimalkan dan langsung test pastikan lancar" or "Pastikan gak ada eror dan bekerja maksimal"

**Expected workflow:**
1. **Build each feature** — Complete implementation
2. **Test immediately** — TypeScript compilation after each PR
3. **Fix errors before continuing** — Don't accumulate technical debt
4. **Comprehensive final test** — Test all PRs together at end
5. **Quality report** — Summary with pass/fail for each PR

**Testing checklist per PR:**
- ✅ TypeScript compilation (`npx tsc --noEmit`)
- ✅ No unused variables/imports
- ✅ Rust syntax valid (if applicable)
- ✅ Event listeners cleaned up
- ✅ Memory leaks checked
- ✅ Integration points verified

**Final report format:**
```
## FINAL QUALITY ASSURANCE REPORT

| PR | Feature | TypeScript | Rust | Status |
|----|---------|-----------|------|--------|
| #6 | Feature | ✅ PASS   | N/A  | READY  |
| #7 | Feature | ✅ PASS   | ✅   | READY  |

Quality Score: 10/10
Production Ready: 100%
```

**Lesson:** "Pastikan lancar" means comprehensive testing with detailed pass/fail report, not just "looks good".

### Obsidian Vault Backup Security (2026-05-12) — 🔴 CRITICAL RULE

**⚠️ ZERO TOLERANCE RULE:** Session notes and personal memori MUST ONLY be saved to PRIVATE repo. This rule CANNOT be violated under ANY circumstances.

**User correction:** "jangan ke repo public, ke repo private dong yg khusus memori" → "pastikan kalo simpan memori ke private jngn ke public ingat itu jngn sampai dilanggar"

**Repos:**
- **PRIVATE:** `kevinnft/obsidian-vault` — Session notes, personal memori, sensitive data ✅
- **PUBLIC:** `kevinnft/mnemosyne-obsidian` — Documentation, setup scripts, templates ONLY ✅

**Backup workflow:**
```bash
# ✅ CORRECT: Save to private repo
cd ~/obsidian-vault
mkdir -p "02 Projects/AI Sessions"
# Create session note with date: YYYY-MM-DD-Topic.md
git add .
git commit -m "docs: session summary (PRIVATE)"
git push origin master
```

**❌ NEVER DO THIS:**
```bash
# ❌ WRONG: Save to public repo
cd ~/mnemosyne-obsidian
mkdir -p sessions/
# Create session note  ← FORBIDDEN — WILL VIOLATE ZERO TOLERANCE RULE
```

**Mandatory verification before push:**
```bash
# ALWAYS check repo privacy before pushing session notes
gh repo view kevinnft/obsidian-vault --json isPrivate
# Expected: {"isPrivate": true} ✅

gh repo view kevinnft/mnemosyne-obsidian --json isPrivate
# Expected: {"isPrivate": false} ✅
```

**Rule enforcement:**
- ✅ Session notes → `~/obsidian-vault/02 Projects/AI Sessions/YYYY-MM-DD-Topic.md`
- ✅ Personal memori → `~/obsidian-vault/` (any directory)
- ✅ Sensitive data → `~/obsidian-vault/` (any directory)
- ✅ Documentation → `~/mnemosyne-obsidian/` (public repo)
- ✅ Setup scripts → `~/mnemosyne-obsidian/` (public repo)
- ✅ Templates → `~/mnemosyne-obsidian/` (public repo)
- ❌ Session notes → `~/mnemosyne-obsidian/` ← **FORBIDDEN**
- ❌ Personal memori → `~/mnemosyne-obsidian/` ← **FORBIDDEN**

**User emphasis:** "jngn sampai dilanggar" = **ZERO TOLERANCE** for violations

**Consequence:** Violating this rule breaks user trust and exposes private data. This is a CRITICAL security preference.

**Lesson:** Security rules are FIRST-CLASS preferences. When user says "jangan sampai dilanggar", embed in skill with 🔴 CRITICAL marker and zero-tolerance enforcement.

**Memory vs Skill distinction:**
- Mnemosyne memory = facts about current state, user identity, environment
- Skills = HOW to do tasks, including security rules and preferences
- Security preferences belong in BOTH: memory for quick recall, skill for enforcement

**Enforcement in code:**
- Always verify repo privacy before pushing session notes
- Use `gh repo view REPO --json isPrivate` to check
- Abort if attempting to push session notes to public repo
- Log security rule violations for audit

## References

- `references/github-contribution-mastery.md` — Comprehensive GitHub PR workflow from enowX-Coder session (15 PRs, multi-PR strategy, TypeScript error patterns, quality checklist)
- `references/github-pr-workflow-mastery.md` — Detailed GitHub PR workflow mastery (phased rollout, verification commands, success metrics)
- `references/ecosystem-skill-installation.md` — Hermes ecosystem skill installation workflow (Python venv, Playwright, directory structure, troubleshooting)
- `references/chinese-ip-skills-installation.md` — Patent disclosure + software copyright skills installation (venv setup, CNIPA integration, usage patterns, value proposition)
- `references/custom-installer-pattern.md` — Smart installer pattern with detection logic (idempotent, auto-detect, comparison table, mnemosyne-obsidian example)

**Note:** For systematic bug fixing workflow (verification, prioritization, testing, release), see the `systematic-debugging` skill which covers root-cause analysis and fix verification patterns.

## Session Patterns Documented

### Chinese IP Protection Skills (2026-05-12)

**Installed skills:**
- `patent-disclosure-skill` — Auto-generate Chinese patent disclosure documents
- `software-copyright` — Auto-generate Chinese software copyright application materials

**Installation pattern:**
1. Clone repos to ~/.hermes/skills/
2. Create Python venv (Ubuntu 24.04 requires venv)
3. Install dependencies (base + optional CNIPA)
4. Install Playwright + Chromium for web scraping
5. Verify with check scripts

**Value:** ¥5,500-11,000 saved per project (~Rp11-22 juta)

### Custom Installer Pattern (2026-05-12)

**Pattern:** Transform documentation repo → smart installer tool

**Key improvements:**
1. **Smart detection** — Check existing setup first, skip if complete
2. **Auto-detection** — Eliminate user input by detecting from config
3. **Minimal installation** — Skip unnecessary components (Obsidian app)
4. **Idempotent** — Safe to re-run, completes partial setups

**Example:** mnemosyne-obsidian repo → install-custom.sh (6.6KB)
- Detects existing vault, Mnemosyne, GitHub sync
- Auto-detects username from gh CLI
- Skips Obsidian desktop app (not needed for CLI)
- Creates vault structure only if missing
- Initializes Git only if not initialized
- Creates GitHub repo only if not exists

**Time saved:** 30-60 minutes manual setup → 1 minute automated

### Visual Assets Review Workflow (2026-05-12)

**User preference:** "jngn langsung push ke gituhubnya" — Review visual assets before pushing to GitHub

**Pattern:** Generate → Review → Approve → Push

**Workflow:**
1. **Generate HTML assets** — Create architecture diagrams, social cards, banners as HTML files
2. **Send to user for review** — Via MEDIA: in Telegram or file path
3. **Wait for approval** — User opens in browser, reviews design
4. **After approval only** — Convert to PNG, add to README, push to GitHub

**Why:** Visual assets represent project branding. User must approve design before it goes public.

**❌ WRONG:**
```
Agent: [generates HTML]
Agent: [converts to PNG]
Agent: [adds to README]
Agent: [commits and pushes]
```

**✅ CORRECT:**
```
Agent: [generates HTML]
Agent: "Files created in assets/. Open in browser to review."
Agent: [sends files via MEDIA:]
User: [reviews in browser]
User: "approve" or "ubah X jadi Y"
Agent: [converts to PNG and pushes] OR [updates and re-sends]
```

**Applies to:**
- Architecture diagrams
- Social media cards
- README banners
- Logo designs
- Any visual branding assets

**Lesson:** Visual/branding assets require explicit approval before going public. Don't assume user will like the design.

### Code Review Workflow (2026-05-12)

**User correction:** "Jngn send file hanya buatkan list yg perlu diperbaiki"

**Context:** Agent was about to send 6 files via MEDIA: for review. User wanted issues list FIRST, not files.

**Pattern:** Issues list → Review → Fix → Send files (if needed)

**Workflow:**
1. **Analyze code/assets** — Check for bugs, issues, improvements needed
2. **Create issues list** — Prioritized by severity (Critical → Medium → Minor)
3. **Send issues list to user** — Let user decide what to fix
4. **Wait for decision** — User chooses: fix all, fix critical only, or skip
5. **After decision only** — Fix issues and send files

**❌ WRONG:**
```
Agent: [analyzes code]
Agent: [sends 6 files via MEDIA:]
Agent: "Review these files!"
```

**✅ CORRECT:**
```
Agent: [analyzes code]
Agent: [creates issues list with priorities]
Agent: "Found 7 bugs (3 critical, 2 medium, 2 minor). Want me to fix all?"
User: "Fix all" or "Fix critical only"
Agent: [fixes issues]
Agent: [sends files if requested]
```

**Applies to:**
- Code review (bug fixes, refactoring)
- Visual assets review (design changes)
- Documentation review (content updates)
- Configuration review (settings changes)

**Why:** User wants to see WHAT needs fixing before seeing HOW it's fixed. Issues list gives context and allows prioritization.

**Format for issues list:**
```markdown
## 🔴 Critical Issues (Must Fix)
1. Bug #1 — Description, impact, fix
2. Bug #2 — Description, impact, fix

## 🟡 Medium Issues (Should Fix)
3. Bug #3 — Description, impact, fix

## 🟢 Minor Issues (Nice to Have)
4. Bug #4 — Description, impact, fix

## Recommendation
Fix all 7 bugs? Or critical only?
```

**Lesson:** When reviewing code/assets, provide issues list FIRST. Let user decide scope before sending files or making changes.
