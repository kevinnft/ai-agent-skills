# Mnemosyne + Obsidian Integration Examples

Real workflow examples from production use.

## Integration Strategy

**Mnemosyne (40%):** Fast recall, pointers, agent state  
**Obsidian (60%):** Rich content, documentation, knowledge base

## Pattern: Pointer Storage

### Good Example
```python
mnemosyne_remember(
  content="VPS cleanup checklist: [[VPS Cleanup]]",
  importance=0.7,
  source="reference"
)
```

Agent workflow:
1. User: "Cleanup VPS"
2. Mnemosyne recalls: "VPS cleanup checklist: [[VPS Cleanup]]"
3. Agent: `read_file(path="~/Documents/Obsidian Vault/03 Areas/VPS Cleanup.md")`
4. Agent executes checklist
5. Agent updates note with results

### Bad Example
```python
mnemosyne_remember(
  content="VPS cleanup: 1. df -h, 2. apt clean, 3. journalctl --vacuum-time=7d, 4. docker system prune...",
  importance=0.7,
  source="reference"
)
```

Problems:
- Duplicates Obsidian content
- Wastes Mnemosyne memory
- Hard to update (must update both places)
- No rich formatting (no code blocks, tables, etc.)

## Workflow Examples

### Example 1: VPS Cleanup

**Mnemosyne:**
```python
mnemosyne_remember(
  content="VPS cleanup: [[VPS Cleanup]]",
  importance=0.7,
  source="reference"
)
```

**Obsidian:** `03 Areas/VPS Cleanup.md`
```markdown
---
title: VPS Cleanup
tags: [vps, devops, checklist]
---

# VPS Cleanup

## Checklist
- [ ] Check disk: `df -h`
- [ ] Clean apt: `sudo apt clean`
- [ ] Rotate logs: `sudo journalctl --vacuum-time=7d`
- [ ] Docker cleanup: `docker system prune -a -f`

## Last Run
**Date:** 2026-05-11
**Space freed:** 78MB
```

### Example 2: Task Management

**Mnemosyne:**
```python
mnemosyne_remember(
  content="Active tasks: [[tasks.base]]",
  importance=0.8,
  source="task_management"
)
```

**Obsidian:** `03 Areas/tasks.base`
```yaml
filters:
  tag: task

formulas:
  priority_score:
    formula: "if(property.priority == 'high', 3, if(property.priority == 'medium', 2, 1))"

views:
  - type: table
    order:
      - property.title
      - property.priority
      - formula.priority_score
    sort:
      - formula.priority_score
      - desc
```

### Example 3: Project Architecture

**Mnemosyne:**
```python
mnemosyne_remember(
  content="Project Alpha architecture: [[Architecture/Project Alpha Canvas]]",
  importance=0.8,
  source="architecture"
)
```

**Obsidian:** `Architecture/Project Alpha.canvas`
```json
{
  "nodes": [
    {"id": "1", "type": "text", "text": "Frontend", "x": 0, "y": 0},
    {"id": "2", "type": "text", "text": "Backend", "x": 300, "y": 0}
  ],
  "edges": [
    {"id": "e1", "fromNode": "1", "toNode": "2", "label": "REST API"}
  ]
}
```

### Example 4: Research Papers

**Mnemosyne:**
```python
mnemosyne_remember(
  content="LLM research paper: [[Papers/LLM Research]]",
  importance=0.6,
  source="research"
)
```

**Obsidian:** `Papers/LLM Research.md`
```markdown
---
title: LLM Research Paper
date: 2026-05-11
tags: [research, llm, arxiv]
source: https://arxiv.org/abs/2401.12345
---

# LLM Research Paper

[Content extracted via defuddle]
```

## Use Cases by Category

### Agent Preferences → Mnemosyne
```python
mnemosyne_remember(
  content="User prefers direct, no-BS responses in Bahasa Indonesia",
  importance=0.8,
  source="preference"
)
```

### Environment Facts → Mnemosyne
```python
mnemosyne_remember(
  content="WSL2 gateway IP: 172.17.16.1 (may change on reboot)",
  importance=0.7,
  source="system_config"
)
```

### Tool Quirks → Mnemosyne
```python
mnemosyne_remember(
  content="Browserbase: 3-session limit, close immediately after use",
  importance=0.6,
  source="tool_quirk"
)
```

### Project Documentation → Obsidian
```markdown
# Project Alpha

## Overview
Full-stack web application with React frontend and FastAPI backend.

## Architecture
See: [[Architecture/Project Alpha Canvas]]

## Progress
- [x] Initial setup
- [ ] Backend API
- [ ] Frontend UI
```

### Technical Notes → Obsidian
```markdown
# Python asyncio Patterns

## Event Loop
...

## Async Context Managers
...

## Related
- [[Python Best Practices]]
- [[FastAPI Patterns]]
```

### Task Management → Obsidian (Bases)
```yaml
# tasks.base
filters:
  tag: task

views:
  - type: table
    order: [property.title, property.priority]
```

### Visual Diagrams → Obsidian (Canvas)
```json
{
  "nodes": [...],
  "edges": [...]
}
```

## Best Practices

### 1. Use Wikilinks in Mnemosyne Pointers
```python
# Good
mnemosyne_remember(content="VPS cleanup: [[VPS Cleanup]]", ...)

# Bad
mnemosyne_remember(content="VPS cleanup: see VPS Cleanup.md", ...)
```

### 2. Store Metadata in Mnemosyne, Content in Obsidian
```python
# Good
mnemosyne_remember(content="Project Alpha docs: [[Projects/Project Alpha]]", ...)

# Bad
mnemosyne_remember(content="Project Alpha: React + FastAPI, started 2026-01-15, status: in progress, team: 3 people...", ...)
```

### 3. Use Obsidian for Structured Data
Don't store tables/lists in Mnemosyne — use Obsidian Bases or Markdown tables.

### 4. Cross-Reference Liberally
```markdown
# Project Alpha

Related:
- [[Credential Pooling]]
- [[VPS Security]]
- [[Architecture/Project Alpha Canvas]]
```

### 5. Update Both When Content Changes
If Obsidian note is renamed/moved, update Mnemosyne pointer:
```python
# Old
mnemosyne_remember(content="VPS cleanup: [[VPS Cleanup]]", ...)

# After rename
mnemosyne_remember(content="VPS cleanup: [[DevOps/VPS Cleanup]]", ...)
```

## Troubleshooting

### Pointer Not Found
```
User: "Cleanup VPS"
Mnemosyne: "VPS cleanup: [[VPS Cleanup]]"
Agent: read_file(path="~/Documents/Obsidian Vault/VPS Cleanup.md")
Error: File not found
```

**Solution:** Note was moved/renamed. Search for it:
```python
search_files(pattern="VPS Cleanup", path="~/Documents/Obsidian Vault", target="files")
```

### Duplicate Content
```
Mnemosyne: "VPS cleanup steps: 1. df -h, 2. apt clean..."
Obsidian: VPS Cleanup.md with same content
```

**Solution:** Delete Mnemosyne entry, keep only pointer:
```python
mnemosyne_invalidate(memory_id="...")
mnemosyne_remember(content="VPS cleanup: [[VPS Cleanup]]", ...)
```

### Stale Pointer
```
Mnemosyne: "Project Alpha: [[Projects/Project Alpha]]"
Obsidian: Note archived to 05 Archive/Project Alpha.md
```

**Solution:** Update pointer:
```python
mnemosyne_remember(content="Project Alpha (archived): [[05 Archive/Project Alpha]]", ...)
```
