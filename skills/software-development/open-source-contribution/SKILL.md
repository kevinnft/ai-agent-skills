---
name: open-source-contribution
description: Comprehensive workflow for contributing to open-source projects with quality checks
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Open-Source, Quality, TypeScript, Contribution]
    related_skills: [github-pr-workflow, github-code-review]
origin: original
source_repo: kevinnft/ai-agent-skills
source_url: https://github.com/kevinnft/ai-agent-skills
source_license: MIT
language: en
---

# Open-Source Contribution Workflow

Complete workflow for contributing high-quality PRs to open-source projects.

## User Preference: Comprehensive Contributions

**When user says "langsung gas dan maksimalkan" or "contribusi maksimal" or "bantu dia jadi terbaik":**
- Build COMPREHENSIVE features, not minimal PRs
- Multiple related features in one PR is OK if cohesive
- Production-ready quality (tests, docs, error handling)
- Think like a 10-year veteran engineer
- **Maximize impact:** Analyze competitors, identify missing features, build world-class solutions
- **Multi-phase approach:** Quick wins first (1-2 hours), then game changers (4-5 hours)
- **Quality over speed:** Fix TypeScript errors immediately, don't push broken code

## Pre-Contribution Analysis

### 1. Analyze the Project

**Before forking, understand what's missing:**

```bash
# Clone to analyze
git clone https://github.com/owner/repo.git
cd repo

# Check structure
ls -la
find src -name "*.tsx" | head -20

# Check existing features
grep -r "TODO\|FIXME" src/

# Check open issues/PRs
gh issue list --repo owner/repo
gh pr list --repo owner/repo
```

**Compare with competitors:**
- What do similar tools have that this doesn't?
- What are the ESSENTIAL missing features?
- What would make this project world-class?

**Prioritize by impact:**
- 🔥 CRITICAL: Features without which the tool is unusable (file tree, terminal, editor)
- 🎯 HIGH: Features that significantly improve UX (keyboard shortcuts, search)
- ✨ NICE: Polish and quality-of-life improvements (loading states, empty states)

### 2. Fork and Clone

```bash
# Fork via GitHub CLI
gh repo fork owner/repo --remote

# Or manually fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/repo.git
cd repo
git remote add upstream https://github.com/owner/repo.git
```

### 2. Star the Original Repo

**Always star before contributing:**

```bash
# Check if already starred
gh repo view owner/repo --json viewerHasStarred

# Star the repo
gh api --method PUT /user/starred/owner/repo
```

### 3. Check Open PRs (Avoid Duplicates)

```bash
gh pr list --repo owner/repo --json number,title,author
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout main
git pull upstream main
git checkout -b feat/your-feature-name
```

### 2. Make Changes

Use file tools (`write_file`, `patch`) to implement features.

### 3. **CRITICAL: Quality Checks BEFORE Committing**

#### TypeScript/JavaScript

```bash
# Type check (fast, low memory)
npx tsc --noEmit

# Common errors to fix:
# - TS6133: Unused variable/import/parameter
# - TS2304: Cannot find name
# - TS2345: Type mismatch
```

**Fix unused variables:**
```typescript
// ❌ Bad
const { data, error } = useQuery();  // error unused
return <div>{data}</div>;

// ✅ Good
const { data } = useQuery();
return <div>{data}</div>;
```

**Fix unused imports:**
```typescript
// ❌ Bad
import { useState, useEffect } from 'react';  // useEffect unused

// ✅ Good
import { useState } from 'react';
```

**Fix unused parameters:**
```typescript
// ❌ Bad
items.map((item, idx) => <div key={item.id}>{item.name}</div>);  // idx unused

// ✅ Good
items.map((item) => <div key={item.id}>{item.name}</div>);
```

#### Python

```bash
mypy src/
ruff check .
```

#### Rust

```bash
cargo clippy -- -D warnings
cargo fmt --check
```

### 4. Commit with Conventional Commits

```bash
git add .
git commit -m "feat(scope): add feature

- Detailed change 1
- Detailed change 2
- Detailed change 3

Closes #issue_number"
```

**Commit types:**
- `feat:` — New feature
- `fix:` — Bug fix
- `refactor:` — Code restructure
- `docs:` — Documentation
- `test:` — Tests
- `chore:` — Maintenance

### 5. Push and Create PR

```bash
git push -u origin feat/your-feature-name

gh pr create --repo owner/repo \
  --title "feat: Add Feature Name" \
  --body "## Overview
  
Comprehensive description of changes.

## Features
- Feature 1
- Feature 2

## Testing
- Test approach

See docs/FEATURE.md for details."
```

### 6. Fix TypeScript Errors in PR

If CI fails with TypeScript errors:

```bash
# Check errors
npx tsc --noEmit

# Fix errors (use patch/write_file)

# Commit fix
git add .
git commit -m "fix: remove unused variables (TypeScript errors)"
git push
```

## Quality Standards

### Code Quality
- ✅ No TypeScript errors (`npx tsc --noEmit` passes)
- ✅ No unused variables/imports/parameters
- ✅ Proper error handling
- ✅ Type-safe (no `any`, no `@ts-ignore`)

### Documentation
- ✅ README updated if needed
- ✅ Add docs/ files for complex features
- ✅ Code comments for non-obvious logic
- ✅ Examples in documentation

### Testing
- ✅ Unit tests for new features
- ✅ Integration tests if applicable
- ✅ Manual testing documented

### PR Description
- ✅ Clear overview
- ✅ List of changes
- ✅ Testing approach
- ✅ Screenshots/demos if UI changes

## Multi-Feature Contributions

**When building comprehensive features (user says "gas semua" or "maksimalkan"):**

### Strategy: Phased Approach

**Phase 1: Quick Wins (1-2 hours each)**
- Essential features that are fast to implement
- High impact, low complexity
- Example: Keyboard shortcuts, loading states

**Phase 2: Core Features (2-4 hours each)**
- Essential features that require more work
- Game-changing functionality
- Example: File tree, terminal integration

**Phase 3: Advanced Features (4-6 hours each)**
- Complex features that complete the experience
- Example: Code editor (Monaco), Git integration

### PR Organization

1. **Group related features** in one PR if cohesive
   - Example: Command Palette + Keyboard Shortcuts (related)
   - Not: Command Palette + Git Integration (separate concerns)

2. **Create multiple PRs** for independent features
   - PR #1: Command Palette + Keyboard Shortcuts
   - PR #2: Loading States + Empty States
   - PR #3: File Tree Sidebar
   - PR #4: Terminal Integration
   - PR #5: Code Editor (Monaco)

3. **Each PR should be:**
   - Self-contained (works independently)
   - Reviewable (not too large, <1000 lines ideal)
   - Production-ready (complete, tested, documented)
   - **Quality-checked:** TypeScript passes, no unused variables

### Workflow for Multiple PRs

```bash
# PR #1
git checkout main
git checkout -b feat/command-palette
# Implement, test, commit
npx tsc --noEmit  # CRITICAL: Check before push
git push -u origin feat/command-palette
gh pr create --repo owner/repo --title "..." --body "..."

# PR #2 (don't wait for #1 review)
git checkout main
git checkout -b feat/loading-states
# Implement, test, commit
npx tsc --noEmit  # CRITICAL: Check before push
git push -u origin feat/loading-states
gh pr create --repo owner/repo --title "..." --body "..."

# Continue for all features
```

**Benefits:**
- Maintainer can review/merge independently
- Faster iteration (parallel review)
- Easier to revert if needed
- Clear git history

## Common Pitfalls

### ❌ Don't:
- Submit PR with TypeScript errors
- Leave unused variables/imports
- Skip documentation
- Make PRs too large (>1000 lines)
- Mix unrelated features

### ✅ Do:
- Run `npx tsc --noEmit` before every commit
- Clean up unused code
- Add comprehensive docs
- Split large features into multiple PRs
- Keep each PR focused

## Example: Full Contribution

```bash
# 1. Fork and star
gh repo fork owner/repo --remote
gh api --method PUT /user/starred/owner/repo

# 2. Check existing PRs
gh pr list --repo owner/repo

# 3. Create branch
git checkout -b feat/command-palette

# 4. Implement feature (use file tools)

# 5. Quality check
npx tsc --noEmit
# Fix any errors

# 6. Commit
git add .
git commit -m "feat(ui): add command palette with keyboard shortcuts"

# 7. Push
git push -u origin feat/command-palette

# 8. Create PR
gh pr create --repo owner/repo \
  --title "feat(ui): Add Command Palette and Keyboard Shortcuts" \
  --body "Comprehensive command palette with 8 global shortcuts..."

# 9. Fix CI errors if any
npx tsc --noEmit
# Fix, commit, push

# 10. Repeat for next feature
git checkout main
git pull upstream main
git checkout -b feat/loading-states
```

## Troubleshooting

### Build OOM (Out of Memory)

```bash
# ❌ Don't use full build on low-memory systems
npm run build  # May crash with OOM

# ✅ Use type check only
npx tsc --noEmit  # Fast, low memory
```

### TypeScript Errors After Merge

```bash
# Pull latest from upstream
git checkout main
git pull upstream main

# Rebase your branch
git checkout feat/your-feature
git rebase main

# Fix conflicts, then:
npx tsc --noEmit
```

## Success Metrics

**High-quality contribution:**
- ✅ TypeScript passes (`npx tsc --noEmit`)
- ✅ CI passes (all checks green)
- ✅ Comprehensive documentation
- ✅ Production-ready code
- ✅ Positive maintainer feedback

**Impact:**
- Small PR: 1 feature, <200 lines
- Medium PR: 2-3 related features, 200-500 lines
- Large PR: Comprehensive feature set, 500-1000 lines (split if >1000)

## Post-Contribution Review

**After submitting PRs, perform deep quality review:**

### Systematic Review Process

**Check each PR in order:**

1. **TypeScript/JavaScript errors**
2. **Rust syntax (if applicable)**
3. **Runtime logic bugs**
4. **Accessibility issues**
5. **Performance issues**
6. **Integration issues**
7. **Documentation gaps**

### 1. TypeScript Error Check

```bash
# Switch to branch
git checkout feat/your-feature

# Check for TypeScript errors
npx tsc --noEmit 2>&1 | head -30

# Common errors:
# - TS6133: Unused variable/import/parameter
# - TS2304: Cannot find name
# - TS2345: Type mismatch
```

**Common fixes:**

```typescript
// ❌ Unused variable
const { data, error } = useQuery();  // error unused
return <div>{data}</div>;

// ✅ Fixed
const { data } = useQuery();
return <div>{data}</div>;

// ❌ Unused import
import { useState, useEffect } from 'react';  // useEffect unused

// ✅ Fixed
import { useState } from 'react';

// ❌ Unused parameter
items.map((item, idx) => <div key={item.id}>{item.name}</div>);  // idx unused

// ✅ Fixed
items.map((item) => <div key={item.id}>{item.name}</div>);
```

### 2. Rust Syntax Check

```bash
# Check Rust syntax (if cargo available)
cd src-tauri
cargo check 2>&1 | tail -30

# If cargo not available, check manually:
grep -n "pub async fn" src-tauri/src/commands/*.rs
# Ensure all commands are registered in lib.rs
```

### 3. Runtime Logic Bugs

**Check for common patterns:**

#### Out-of-bounds index after filtering

```typescript
// ❌ Bad: selectedIndex might be out of bounds
const filteredItems = useMemo(() => items.filter(...), [items, search]);
// selectedIndex still points to old array

// ✅ Good: Reset index when filtered items change
useEffect(() => {
  setSelectedIndex(0);
}, [filteredItems]);
```

#### Stale state in event listeners

```typescript
// ❌ Bad: Captures stale state
useEffect(() => {
  const handler = () => console.log(count); // Stale count
  window.addEventListener('click', handler);
}, []); // Empty deps

// ✅ Good: Include dependencies
useEffect(() => {
  const handler = () => console.log(count);
  window.addEventListener('click', handler);
  return () => window.removeEventListener('click', handler);
}, [count]); // Include count
```

#### Missing cleanup in useEffect

```typescript
// ❌ Bad: No cleanup
useEffect(() => {
  window.addEventListener('keydown', handler);
}, []);

// ✅ Good: Cleanup
useEffect(() => {
  window.addEventListener('keydown', handler);
  return () => window.removeEventListener('keydown', handler);
}, []);
```

**Check for cleanup:**

```bash
# Find all addEventListener without cleanup
grep -A5 "addEventListener" src/components/**/*.tsx | grep -v "removeEventListener"
```

### 4. Accessibility Check

```bash
# Check for aria attributes
grep -n "aria-\|role=" src/components/**/*.tsx
```

**Common fixes:**

```typescript
// ✅ Add aria-label to loading spinners
<CircleNotch aria-label="Loading" className="animate-spin" />

// ✅ Add role/aria-modal to overlays
<div 
  role="dialog" 
  aria-modal="true" 
  aria-label="Loading"
  className="fixed inset-0 ..."
>

// ✅ Add aria-hidden to decorative elements
<div aria-hidden="true" className="skeleton">
```

### 5. Performance Check

**Check for memory leaks:**

```bash
# Count useEffect cleanup functions
grep -A5 "useEffect" src/components/**/*.tsx | grep -c "return () =>"

# Should match number of useEffect hooks with side effects
```

**Check for unnecessary re-renders:**

```typescript
// ✅ Use useMemo for expensive computations
const filteredItems = useMemo(() => 
  items.filter(item => item.name.includes(search)),
  [items, search]
);

// ✅ Use useCallback for event handlers passed to children
const handleClick = useCallback(() => {
  // ...
}, [deps]);
```

### 6. Integration Check

**Check cross-component integration:**

```bash
# Check event emission
grep -n "dispatchEvent\|new CustomEvent" src/components/**/*.tsx

# Check event listeners
grep -n "addEventListener.*file-selected" src/components/**/*.tsx
```

**Verify integration:**
- FileTree dispatches `file-selected` event
- CodeEditor listens to `file-selected` event
- Terminal emits output via Tauri events
- Components properly clean up listeners

### 7. Dependency Check

```bash
# Check for missing imports
grep -r "import.*from" src/ | grep "ComponentName"

# If component doesn't exist in branch, use inline alternative
# Example: Replace <LoadingSpinner /> with <CircleNotch className="animate-spin" />
```

### Commit Fixes Immediately

**After finding issues, fix and commit:**

```bash
# Fix TypeScript errors
git add .
git commit -m "fix: remove unused variables (TypeScript errors)

- Remove unused 'mainView' in App.tsx
- Remove unused 'formatShortcut' import in CommandPalette.tsx
- Remove unused 'idx' parameter in CommandPalette.tsx

All TypeScript errors resolved."
git push

# Fix accessibility
git add .
git commit -m "fix(a11y): add aria labels to loading components

- Add aria-label to LoadingSpinner for screen readers
- Add role=dialog, aria-modal, aria-label to LoadingOverlay
- Improves accessibility for visually impaired users"
git push

# Fix dependencies
git add .
git commit -m "fix: remove LoadingSpinner dependency, use inline CircleNotch

FileTree now uses CircleNotch directly instead of importing LoadingSpinner
(which doesn't exist in this branch). Keeps the component self-contained."
git push

# Fix runtime bugs
git add .
git commit -m "fix(ui): reset selectedIndex when filtered commands change

Prevents out-of-bounds index when search filters commands.
Ensures arrow key navigation always works correctly."
git push
```

### Quality Checklist

**Before marking PR as ready:**

- [ ] TypeScript passes (`npx tsc --noEmit`)
- [ ] No unused variables/imports/parameters
- [ ] All useEffect hooks have cleanup (if needed)
- [ ] Accessibility attributes present (aria-label, role, etc.)
- [ ] No memory leaks (event listeners cleaned up)
- [ ] Integration tested (events dispatched/received)
- [ ] Dependencies resolved (no missing imports)
- [ ] Documentation updated
- [ ] Commit messages follow convention

### Multi-PR Review

**When submitting multiple PRs, review systematically:**

```bash
# Review PR #1
git checkout feat/command-palette
npx tsc --noEmit
# Fix issues, commit, push

# Review PR #2
git checkout feat/loading-states
npx tsc --noEmit
# Fix issues, commit, push

# Review PR #3
git checkout feat/file-tree
npx tsc --noEmit
# Fix issues, commit, push

# Continue for all PRs
```

**Track review status:**

| PR | TypeScript | Rust | Logic | A11y | Perf | Integration | Status |
|---|---|---|---|---|---|---|---|
| #6 | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | **READY** |
| #7 | ✅ | N/A | N/A | ✅ | ✅ | ✅ | **READY** |
| #8 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **READY** |
| #9 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **READY** |
| #10 | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | **READY** |

## References

- `references/tauri-contributions.md` — Tauri-specific patterns (Rust commands, IPC, file operations, common pitfalls)
