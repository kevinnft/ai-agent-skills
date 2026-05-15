---
name: vps-cleanup
description: Systematic VPS cleanup — analyze files, categorize by importance, safely delete temporary/old data to free disk space
tags: [vps, cleanup, disk-space, maintenance, linux]
related_skills: [vps-security-hardening]
origin: unknown
source_license: see upstream
language: en
---

# VPS Cleanup

Systematic approach to cleaning up VPS disk space — analyze files, categorize by importance, safely delete temporary/old data without losing critical files.

## When to Use

- User asks "apa yang gak penting?" or "what can I delete?"
- Disk space running low (> 80% used)
- Home directory cluttered with temporary files
- After completing projects (cleanup workspace)

## Workflow

### Phase 1: Analyze Current State

```bash
# Check disk usage
df -h /

# Analyze home directory
cd /home/ubuntu
du -sh * 2>/dev/null | sort -h

# Check large directories
du -h --max-depth=1 | sort -h | tail -20
```

### Phase 2: Categorize Files

For each file/directory, assess:

| Category | Keep? | Examples |
|----------|-------|----------|
| **Backups** | ✅ Keep | `*.zip`, `*.tar.gz` with "backup" in name |
| **System** | ✅ Keep | `snap/`, `.cache/`, `.local/` |
| **Active projects** | ✅ Keep | Current development work |
| **Temporary workspaces** | ❌ Delete | Analysis folders, test directories |
| **Old archives** | ❌ Delete | Extracted folders + their `.tar.gz` (duplicates) |
| **Generated outputs** | 🟡 Optional | PNGs, reports (if source exists) |
| **Source files** | 🟡 Optional | `.html` if `.png` generated, `.drawio` if exported |

### Phase 3: Build Decision Matrix

Create analysis table:

```python
files = {
    'file.zip': {
        'size': '135M',
        'type': 'backup',
        'keep': True,
        'reason': 'Important backup'
    },
    'temp-workspace/': {
        'size': '538M',
        'type': 'workspace',
        'keep': False,
        'reason': 'Temporary analysis, reports done'
    },
    # ... more files
}
```

Calculate:
- Total size
- Deletable size
- Keep size
- Percentage reclaimable

### Phase 4: Present Analysis

Show user:

1. **Summary stats** (total, keep, delete, %)
2. **Keep list** (sorted by size, with reasons)
3. **Delete list** (sorted by size, with reasons)
4. **Recommendations** (phased approach)

**Format:**
```
✅ KEEP (IMPORTANT)
  135M  backup.zip        Important backup
  2.4M  snap/             System directory

❌ CAN DELETE (NOT IMPORTANT)
  538M  temp-workspace/   Temporary, work done
  1.2M  diagrams/         PNGs generated
```

### Phase 5: Confirm with User

**CRITICAL:** Always confirm before deleting, especially for:
- Large directories (> 100 MB)
- Project directories (might have uncommitted work)
- Anything user-created (not system files)

**Ask:**
- "Mau gue delete sekarang?" (Want me to delete now?)
- "Ada yang mau keep?" (Anything you want to keep?)

### Phase 6: Safe Deletion

```bash
# Delete directories
rm -rf ~/temp-workspace/
rm -rf ~/old-project/

# Delete files
rm ~/old-archive.tar.gz
rm ~/report.md

# Verify
ls -lh ~/
df -h /
```

**Safety checks:**
- Use `rm -rf` only for confirmed directories
- Delete one category at a time (easier to undo if mistake)
- Verify disk space freed after deletion

## User Preference Patterns

### For "Delete All Unimportant"

When user says "delete semua yang gak penting" or "delete all unimportant":

**DO:**
- ✅ Analyze and categorize first
- ✅ Present full list with reasons
- ✅ Ask about ambiguous items (projects, large files)
- ✅ Delete after confirmation

**DON'T:**
- ❌ Delete immediately without analysis
- ❌ Skip showing what will be deleted
- ❌ Delete backups or system files
- ❌ Delete active projects without asking

### For Safety Confirmation

When presenting cleanup plan, user may respond:
- **"Aman di bersihkan?"** (Safe to clean?) → User wants reassurance
  - ✅ Confirm: "100% AMAN" + list what won't be deleted
  - ✅ Explain worst-case scenario (e.g., "cache can be regenerated")
  - ✅ Emphasize zero data loss
  - ✅ Then ask: "Gas cleanup?" (Ready to proceed?)

- **"Ya"** (Yes) → Proceed immediately
  - ✅ Execute cleanup commands
  - ✅ Show progress for each step
  - ✅ Verify results (before/after disk usage)
  - ✅ Celebrate success: "✅ Cleanup complete! Freed XMB"

**User's decision-making pattern:**
1. Asks for analysis → wants to see what's unused
2. Asks "aman?" → wants safety confirmation
3. Says "ya" → ready to execute
4. Expects immediate action after confirmation (no further questions)

### For Ambiguous Items

**Projects (e.g., oh-my-china/):**
```
🟡 AMBIGUOUS: oh-my-china/ (340 MB)
   Type: Project
   Question: "Masih aktif develop atau cuma testing?"
   
   If active → KEEP
   If testing → DELETE
```

**Generated outputs:**
```
🟡 OPTIONAL: diagram.png (4 MB)
   Type: Output
   Question: "Masih perlu atau gak?"
   
   If needed → KEEP
   If done → DELETE
```

## Common File Types

### Temporary Workspaces (DELETE)

**Patterns:**
- `*-analysis/`, `*-test/`, `*-workspace/`
- Cloned repos for one-time analysis
- Temporary diagram folders

**Indicators:**
- Reports already generated
- Work completed
- No uncommitted changes

**Example:**
```bash
hermes-analysis/  # 538 MB
├─ 10 cloned repos
├─ ANALYSIS_REPORT.md (done)
└─ install script (used)

→ DELETE (reports done, repos installed elsewhere)
```

### Old Archives + Extracted (DELETE)

**Pattern:** Both `.tar.gz` AND extracted folder exist

**Example:**
```bash
gmail_research/              # 100 KB (extracted)
gmail_research_2026-05-01.tar.gz  # 20 KB (archive)

→ DELETE BOTH (duplicate, old data)
```

### Temporary Reports (DELETE)

**Patterns:**
- `*_REPORT.md`, `*_AUDIT.md`
- Generated for one-time review
- Info already applied

**Example:**
```bash
VPS_SECURITY_AUDIT_REPORT.md      # 12 KB
VPS_SECURITY_HARDENING_REPORT.md  # 12 KB

→ DELETE (hardening done, info applied)
```

### Source Files (OPTIONAL)

**Pattern:** Source exists, output generated

**Example:**
```bash
ai-promo.html     # 16 KB (source)
ai-promo.png      # 4 MB (output)

→ DELETE SOURCE (output is final)
```

### Backups (KEEP)

**Patterns:**
- `*-backup-*.zip`, `*.tar.gz` with dates
- Named with "backup" or "archive"

**Example:**
```bash
hermes-backup-2026-05-03.zip  # 135 MB

→ KEEP (important backup!)
```

### System Directories (KEEP)

**Patterns:**
- `snap/`, `.cache/`, `.local/`, `.config/`
- Hidden directories (`.hermes/`, `.ssh/`)

**Example:**
```bash
snap/        # 2.4 MB
.hermes/     # 2.6 GB

→ KEEP (system/application data)
```

## Resource Evaluation for Tool Installation

**CRITICAL:** Before recommending ANY tool installation, evaluate resource cost against VPS constraints.

### VPS Resource Constraints (User: ryzen, VPS: 2GB RAM, 40GB disk)

**User tolerance:**
- ❌ **ZERO tolerance** for heavy tools
- ❌ Disk > 500 MB = instant rejection
- ❌ RAM > 100 MB = ask first or find lightweight alternative
- ✅ Prefer API/cloud services over local installation

**Evaluation criteria:**

| Resource | Threshold | Action |
|----------|-----------|--------|
| **Disk < 50 MB** | ✅ Safe | Install without asking |
| **Disk 50-500 MB** | 🟡 Moderate | Ask first, explain cost |
| **Disk > 500 MB** | 🔴 Heavy | Find alternative or skip |
| **RAM < 50 MB** | ✅ Safe | Install without asking |
| **RAM 50-100 MB** | 🟡 Moderate | Ask first, explain cost |
| **RAM > 100 MB** | 🔴 Heavy | Find alternative or skip |

**Example rejection (Scrapling, session 2026-05-12):**
```
User: "Cek Scrapling bagus gak?"
Analysis:
- Disk: 650-900 MB (7.0 MB library + browser dependencies)
- RAM: 200-400 MB per session (browser automation)
- VPS: 2GB RAM, 40GB disk
- Features: Powerful (adaptive parsing, Cloudflare bypass, spider framework)

Comparison with TinyFish:
- TinyFish: 0 MB disk, 0 MB RAM (cloud API)
- Scrapling: 650-900 MB disk, 200-400 MB RAM (local)

User response: "gede banget makan emori dan ram"
Decision: SKIP ❌ → Recommend TinyFish instead

Lesson: User has ZERO tolerance for heavy tools.
Always check resource cost BEFORE recommending.
When tool is heavy, immediately suggest lightweight alternative (API/cloud).
```

**User's exact rejection pattern:**
- **"gede banget makan emori dan ram"** = instant rejection, no discussion
- When user says this, STOP immediately — don't offer workarounds, don't suggest "minimal install", don't explain benefits
- Acknowledge rejection, move on to lightweight alternatives
- This phrase signals: resource cost is deal-breaker, not negotiable

**Alternative strategies:**
1. **Cloud API** (Browserbase, Browser Use Cloud) — 0 MB local cost
2. **Lightweight alternatives** (requests + BeautifulSoup vs Scrapling)
3. **Docker** (isolated, but still heavy)
4. **Skip feature** (if not critical)

**Common heavy tools and their costs:**

| Tool | Disk | RAM (idle) | RAM (active) | Alternative |
|------|------|------------|--------------|-------------|
| **Chrome/Chromium** | 300-400 MB | 0 MB | 150-300 MB/instance | Browserbase (cloud) |
| **Scrapling** | 650-900 MB | 50 MB | 200-400 MB | requests + BeautifulSoup |
| **Playwright** | 400-500 MB | 0 MB | 200-300 MB | Browserbase (cloud) |
| **Selenium** | 350-450 MB | 0 MB | 150-250 MB | Browserbase (cloud) |

**enowxai v1.2.0 specific:**
- Requires Chrome/Chromium (300-400 MB disk)
- Worker pool spawns multiple Chrome instances
- Risk: OOM on 2GB RAM VPS with concurrent workers
- Mitigation: Limit concurrent workers to 2-3 max

## Pitfalls

### 0. Recommending Deletion Without Thorough Analysis

**Problem:** Suggesting file cleanup without checking references, purpose, or user preference.

**Solution:**
- **ALWAYS analyze before recommending deletion:**
  - Check if files are referenced elsewhere (`grep -r filename`)
  - Verify file purpose (marketing, docs, tools, assets)
  - Consider total size impact (is cleanup worth it?)
  - Assess user's attachment to files
- **Present analysis, let user decide:**
  - Show: file list + sizes + purposes + references
  - Explain: why each file might be kept or deleted
  - Ask: "Mau gue hapus atau keep semua?" (Delete or keep all?)
- **User preference pattern:**
  - "jangan hapus kalo berguna" = user wants to keep useful files
  - "brarti semua aman?" = user wants confirmation, not assumptions
  - When in doubt, present analysis and ASK

**Example (from session 2026-05-12):**
```
User: "hapus file2 yang gak perlu"
❌ WRONG: Immediately recommend deleting marketing files
✅ RIGHT: Analyze all files, check references, present findings:
  - Marketing files (7.5 KB): Not referenced, but useful for sharing
  - Deep docs (42 KB): Redundant with README, but valuable for advanced users
  - Total size: 284 KB (tiny, not worth cleanup)
  - Recommendation: Keep all (every file has purpose, size is negligible)
```

### 1. Deleting Backups

**Problem:** User says "delete all", you delete backups too.

**Solution:**
- Always categorize backups as KEEP
- Highlight backups in analysis
- Confirm separately if user wants to delete backups

### 2. Deleting Active Projects

**Problem:** Large project directory looks like temporary workspace.

**Solution:**
- Check for `.git/` (active repo)
- Check last modified date (recent = active)
- Ask user if unsure

### 3. Not Showing Reasons

**Problem:** User doesn't understand why something is kept/deleted.

**Solution:**
- Always include reason in analysis
- Be specific: "Temporary workspace, reports done" not just "temporary"

### 4. Deleting Without Confirmation

**Problem:** User says "delete unimportant", you delete immediately.

**Solution:**
- Always show analysis first
- Get explicit confirmation
- Especially for large items (> 100 MB)

### 5. Not Verifying Disk Space Freed

**Problem:** Delete files but don't show impact.

**Solution:**
- Show disk usage before/after
- Confirm space was actually freed
- Celebrate success: "✅ Freed 884 MB!"

## Verification

After cleanup:

```bash
# Check disk space
df -h /

# Check home directory
ls -lh ~/

# Verify critical files still exist
ls ~/.hermes/
ls ~/snap/
```

**Success criteria:**
- ✅ Disk space freed (check df -h)
- ✅ Critical files intact (backups, system dirs)
- ✅ User satisfied with cleanup
- ✅ No accidental deletions

## Advanced: Cleanup ~/.hermes/

**CAUTION:** Only clean `~/.hermes/` if user explicitly requests or disk critically low.

```bash
# Check size
du -sh ~/.hermes/

# Analyze subdirectories
du -h ~/.hermes/ --max-depth=1 | sort -h

# Safe to clean:
- Old sessions: hermes sessions prune --older-than 30d
- Cache: rm -rf ~/.hermes/.cache/
- Logs: rm ~/.hermes/*.log

# DO NOT delete:
- config.yaml
- memories/
- skills/
- sessions.db (unless pruning)
```

**Hermes Ecosystem Audit:** See `references/hermes-ecosystem-audit.md` for:
- Systematic audit methodology (4-phase process)
- Common cleanup targets (state snapshots, WAL files, logs, caches)
- **Unused vs. inactive distinction** (CRITICAL — bundled plugins are inactive, not unused)
- Audit report template
- Maintenance schedule (weekly/monthly tasks)
- Key learnings from 2026-05-05 audit (78MB cleanup, zero data loss)

**Key insight from audit:** "Installed" ≠ "Active" ≠ "Consuming resources"
- Bundled code (plugins, toolsets) has zero cost until executed
- Only active processes consume RAM
- Only written files consume disk (code is static)
- Example: 8 memory provider plugins installed = 1.2MB disk, 0MB RAM (inactive, not unused)

## Examples

### Example 1: Simple Cleanup (540 MB freed)

```
Analysis:
- hermes-analysis/ (538 MB) → Temporary workspace
- drawio-test/ (1.2 MB) → Temporary diagrams
- old reports (24 KB) → Info applied

Decision: DELETE ALL (safe, no data loss)

Result: 540 MB freed ✅
```

### Example 2: Cleanup with Confirmation (884 MB freed)

```
Analysis:
- hermes-analysis/ (538 MB) → DELETE
- oh-my-china/ (340 MB) → ASK USER (project?)
- ai-promo.png (4 MB) → ASK USER (still need?)

User: "delete semua yang gak penting"

Confirm:
- oh-my-china/ → "Masih develop?" → "Cuma testing" → DELETE
- ai-promo.png → "Masih perlu?" → "Gak" → DELETE

Result: 884 MB freed ✅
```

## References

- `df` man page: https://man7.org/linux/man-pages/man1/df.1.html
- `du` man page: https://man7.org/linux/man-pages/man1/du.1.html
- Safe deletion practices: https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html
- Scrapling vs TinyFish comparison: `references/scrapling-vs-tinyfish-comparison.md` (tool evaluation for VPS constraints)
