# Memory Provider Migration Workflow

## Overview

When switching Hermes memory providers (built-in → external, or external → external), follow this workflow to preserve data and verify functionality.

## Built-in → External Provider Migration

### Step 1: Assess Built-in Memory Content

```bash
# Check if built-in memory exists
ls -lh ~/.hermes/memories/MEMORY.md ~/.hermes/memories/USER.md

# Count entries (§-delimited)
grep -c '§' ~/.hermes/memories/MEMORY.md
grep -c '§' ~/.hermes/memories/USER.md
```

**Decision point:**
- 0 entries → Skip migration, just activate new provider
- 1-20 entries → Migrate via Python script (see below)
- 20+ entries → Consider manual review before migration

### Step 2: Install and Activate New Provider

Follow provider-specific installation (see `references/ubuntu-2404-pip-workarounds.md` for Ubuntu 24.04).

```bash
# Example: Mnemosyne
hermes config set memory.provider mnemosyne
hermes memory status  # Verify active
```

### Step 3: Migrate Built-in Memory

Create migration script:

```python
#!/usr/bin/env python3
"""
Migrate Hermes built-in memory (MEMORY.md + USER.md) to external provider.
"""
import sys
from pathlib import Path

# Add provider to path (adjust for your provider)
sys.path.insert(0, str(Path.home() / '.hermes/ecosystem/provider'))

from provider import remember  # Import provider's API

def migrate_memory_md(path: Path):
    """Migrate MEMORY.md entries."""
    if not path.exists():
        return 0
    
    content = path.read_text()
    entries = [e.strip() for e in content.split('§') if e.strip()]
    
    count = 0
    for entry in entries:
        remember(
            content=entry,
            importance=0.95,
            source='hermes_builtin_memory',
            scope='global'
        )
        count += 1
        print(f"✅ Migrated memory entry {count}")
    
    return count

def migrate_user_md(path: Path):
    """Migrate USER.md entries."""
    if not path.exists():
        return 0
    
    content = path.read_text()
    entries = [e.strip() for e in content.split('§') if e.strip()]
    
    count = 0
    for entry in entries:
        remember(
            content=entry,
            importance=1.0,
            source='hermes_builtin_user',
            scope='global'
        )
        count += 1
        print(f"✅ Migrated user profile entry {count}")
    
    return count

def main():
    hermes_home = Path.home() / '.hermes/memories'
    
    print("🚀 Migrating Hermes built-in memory")
    print("=" * 50)
    
    memory_count = migrate_memory_md(hermes_home / 'MEMORY.md')
    user_count = migrate_user_md(hermes_home / 'USER.md')
    
    print("=" * 50)
    print(f"✅ Migration complete!")
    print(f"   - MEMORY.md: {memory_count} entries")
    print(f"   - USER.md: {user_count} entries")
    print(f"   - Total: {memory_count + user_count} entries")

if __name__ == '__main__':
    main()
```

Run migration:

```bash
python3 /tmp/migrate_builtin_to_provider.py
```

### Step 4: Verify Migration

```bash
# Provider-specific stats command
hermes mnemosyne stats --global  # Mnemosyne example
hermes mem0 stats                # Mem0 example

# Search test
hermes mnemosyne inspect "VPS"   # Should find migrated entries
```

**Verification checklist:**
- ✅ Entry count matches (built-in → provider)
- ✅ Search returns expected results
- ✅ High-importance entries preserved (user profile, system info)
- ✅ Scope preserved (global entries still global)

### Step 5: Backup and Cleanup (Optional)

```bash
# Export provider data
hermes mnemosyne export --output ~/.hermes/backups/provider_$(date +%Y%m%d).json

# Backup built-in memory (before clearing)
cp ~/.hermes/memories/MEMORY.md ~/.hermes/backups/MEMORY_$(date +%Y%m%d).md
cp ~/.hermes/memories/USER.md ~/.hermes/backups/USER_$(date +%Y%m%d).md

# Clear built-in memory (OPTIONAL — only if confident)
# hermes memory reset  # WARNING: Irreversible
```

**Recommendation:** Keep both active initially. Built-in memory as human-readable reference, external provider as production memory.

## External → External Provider Migration

### Step 1: Export from Old Provider

```bash
# Provider-specific export
hermes old_provider export --output /tmp/old_provider_export.json
```

### Step 2: Install New Provider

Follow provider-specific installation.

### Step 3: Import to New Provider

```bash
# Check if new provider supports direct import
hermes new_provider import --from old_provider --input /tmp/old_provider_export.json

# If not supported, write custom migration script
```

### Step 4: Verify and Cleanup

Same as Step 4-5 above.

## Provider-Specific Notes

### Mnemosyne

**API:**
```python
from mnemosyne import remember, recall

remember(content="...", importance=0.95, source="...", scope="global")
results = recall("query", top_k=5)
```

**Stats:**
```bash
hermes mnemosyne stats --global
```

**Export/Import:**
```bash
hermes mnemosyne export --output backup.json
hermes mnemosyne import --input backup.json
```

**Supported import sources:** mem0, letta, zep, cognee, honcho, supermemory

### Mem0

**API:**
```python
from mem0 import Memory

memory = Memory()
memory.add("...", user_id="...", metadata={...})
results = memory.search("query", user_id="...")
```

**Stats:** Via web dashboard or API

**Export/Import:** Via API (no CLI)

### Honcho

**API:**
```python
from honcho import Honcho

client = Honcho()
client.apps.users.sessions.messages.create(...)
```

**Stats:** Via API

**Export/Import:** Via API (no CLI)

## Common Pitfalls

### 1. **Losing Scope Information**

**Problem:** Migrating global entries as session-scoped

```python
❌ remember(content="...", scope="session")  # Should be global
```

**Fix:** Preserve scope from built-in memory:
- MEMORY.md entries → `scope="global"` (cross-session facts)
- USER.md entries → `scope="global"` (user profile)
- Session-specific notes → `scope="session"`

### 2. **Not Verifying Search**

**Problem:** Migration succeeds but search doesn't work

**Fix:** Test search with known queries:
```bash
hermes provider inspect "VPS"
hermes provider inspect "user machine"
hermes provider inspect "API provider"
```

### 3. **Forgetting to Backup**

**Problem:** Migration fails, data lost

**Fix:** Always export before migration:
```bash
# Backup built-in
cp ~/.hermes/memories/*.md ~/.hermes/backups/

# Export provider data
hermes provider export --output backup.json
```

### 4. **Clearing Built-in Too Early**

**Problem:** Cleared built-in memory before verifying migration

**Fix:** Keep built-in memory for 1-2 weeks after migration. Only clear after confirming external provider works reliably.

## Performance Benchmarking

After migration, benchmark query performance:

```python
import time
from provider import recall

queries = ['VPS', 'API provider', 'user machine', 'ecosystem', 'memory']
times = []

for query in queries:
    start = time.perf_counter()
    results = recall(query, top_k=5)
    elapsed = (time.perf_counter() - start) * 1000  # ms
    times.append(elapsed)
    print(f'{query:20s} → {len(results)} results in {elapsed:.2f}ms')

print(f'\nAverage: {sum(times)/len(times):.2f}ms')
```

**Expected performance:**
- Mnemosyne: 4-10ms (local SQLite)
- Mem0: 40-60ms (cloud API)
- Honcho: 50-80ms (cloud API)
- Zep: 60-90ms (cloud API)

## Maintenance After Migration

### Daily
```bash
# Check memory stats
hermes provider stats --global
```

### Weekly
```bash
# Consolidate old memories (if supported)
hermes provider sleep  # Mnemosyne

# Export backup
hermes provider export --output ~/.hermes/backups/provider_$(date +%Y%m%d).json
```

### Monthly
```bash
# Database maintenance (if SQLite-based)
# Checkpoint WAL, vacuum, analyze
```

## Rollback Plan

If migration fails or new provider doesn't work:

```bash
# 1. Disable new provider
hermes config set memory.provider built-in

# 2. Restore built-in memory from backup
cp ~/.hermes/backups/MEMORY_YYYYMMDD.md ~/.hermes/memories/MEMORY.md
cp ~/.hermes/backups/USER_YYYYMMDD.md ~/.hermes/memories/USER.md

# 3. Verify
hermes memory status
```

## References

- [Hermes Memory Providers](https://hermes-agent.nousresearch.com/docs/memory)
- [Mnemosyne Migration Guide](https://github.com/AxDSan/mnemosyne/blob/main/docs/hermes-integration.md)
- [PEP 668 Workarounds](./ubuntu-2404-pip-workarounds.md)
