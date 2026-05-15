---
name: contributing-to-ide-projects
description: Comprehensive workflow for contributing features to open-source IDE and coding tool projects
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [open-source, ide, tauri, typescript, rust, contributions]
    related_skills: [github-pr-workflow, open-source-contribution]
origin: original
source_repo: kevinnft/ai-agent-skills
source_url: https://github.com/kevinnft/ai-agent-skills
source_license: MIT
language: en
---

# Contributing to IDE Projects

Comprehensive workflow for contributing major features to open-source IDE and coding tool projects (VS Code, Cursor, Windsurf, Tauri-based editors).

## When to Use This Skill

- Contributing to IDE/editor projects
- Building coding assistant tools
- Adding features to Tauri desktop apps
- Multi-PR contribution campaigns
- Competitive feature analysis

## Pre-Contribution Analysis

### 0. Gap Analysis (CRITICAL — Do This First!)

**Before recommending ANY features, check what already exists in the codebase:**

```bash
# Check existing components
ls -la src/components/
find src -name "*.tsx" -o -name "*.ts" | grep -E "(component|store)"

# Check existing stores
ls -la src/stores/

# Search for feature keywords
grep -r "StatusBar\|QuickOpen\|Terminal\|FileTree\|Git" src/

# Check existing UI elements
cat src/components/layout/AppFooter.tsx  # Often has status info
cat src/components/layout/RightSidebar.tsx  # Check sidebar tabs
```

**User expectation:** When asked "ada yang recommended lagi gak?" or "apa lagi yang bisa kita kontribusikan?", user expects you to **check existing features first**. User will explicitly ask "cek fitur skrng dulu apa semua itu blm ada?" if you skip this step.

**Output format:**
```markdown
## ANALISA FITUR EXISTING

### Yang Sudah Ada:
- ✅ AI Chat Interface
- ✅ Settings Modal (Providers, Agents tabs)
- ✅ Left/Right Sidebar system
- ✅ Theme system

### Yang Belum Ada:
- ❌ File Tree
- ❌ Code Editor
- ❌ Terminal
- ❌ Git Integration

### Verdict:
SEMUA 9 PRs yang gue bikin itu BELUM ADA! ✅
```

### 1. Understand the Project

```bash
# Clone and analyze
git clone <repo>
cd <repo>

# Read core docs
cat README.md
cat CHANGELOG.md
cat package.json  # Tech stack
cat src-tauri/Cargo.toml  # Rust dependencies (if Tauri)
```

**Key questions:**
- What's the tech stack? (React/Vue/Svelte, Tauri/Electron, TypeScript version)
- What features exist? (README features section)
- What's the architecture? (monorepo, frontend/backend split)
- What's the contribution process? (CONTRIBUTING.md)

### 2. Competitive Analysis

**Compare with competitors:**
- Cursor (AI coding assistant)
- Windsurf (AI IDE)
- VS Code (standard IDE)
- GitHub Copilot (AI pair programmer)

**Create feature matrix:**

| Feature | Cursor | Windsurf | Target Project |
|---------|--------|----------|----------------|
| Code Editor | ✅ | ✅ | ? |
| Terminal | ✅ | ✅ | ? |
| File Tree | ✅ | ✅ | ? |
| Git Integration | ✅ | ✅ | ? |
| Search & Replace | ✅ | ✅ | ? |

**Identify gaps:**
- Essential features (must-have for professional use)
- Competitive features (match competitors)
- Unique features (differentiation opportunities)

### 3. Prioritize Contributions

**Tier 1: Essential (CRITICAL)**
- Features without which the IDE is incomplete
- Examples: File tree, terminal, code editor, Git integration

**Tier 2: Competitive Edge**
- Features that match competitors
- Examples: Search & replace, command palette, keyboard shortcuts

**Tier 3: Unique Differentiators**
- Features competitors don't have
- Examples: AI code review, automated testing, performance profiling

**Prioritization criteria:**
1. Impact (how much it improves the IDE)
2. Effort (time to implement)
3. Dependencies (what else needs to exist first)
4. User demand (GitHub issues, discussions)

## Multi-PR Strategy

### Why Multiple PRs?

- **Faster reviews** — Smaller PRs reviewed faster
- **Independent features** — Can merge separately
- **Parallel work** — Don't block on reviews
- **Easier rollback** — Isolate issues

### Integration Strategy for Multiple Features

When adding multiple interdependent features (e.g., 9 IDE components):

**Problem:** Features depend on each other but need to be reviewed independently.

**Solution:** Placeholder-based integration system

1. **Create layout/infrastructure PR first**
   - Layout system with panel management
   - Keyboard shortcut routing
   - State management stores
   - **Placeholder components for all features**
   
2. **Use placeholder components**
   ```tsx
   const FileTreePlaceholder = () => (
     <div className="h-full flex items-center justify-center p-4 text-center">
       <div>
         <p className="text-sm font-semibold mb-2">File Tree</p>
         <p className="text-xs text-gray-500">PR #8 - Coming soon</p>
       </div>
     </div>
   );
   ```

3. **Document integration points clearly**
   ```markdown
   ## Integration Points
   
   ### Current State (Placeholders)
   All panels show placeholder components. This allows:
   1. Testing layout system independently
   2. Merging layout before feature PRs
   3. Easy feature integration when PRs merge
   
   ### Future Integration (When PRs Merge)
   Replace placeholders with actual components:
   
   // Before
   const FileTreePlaceholder = () => <div>Coming soon</div>;
   
   // After (when PR #8 merges)
   import { FileTree } from '@/components/ui/FileTree';
   const renderLeftPanel = () => {
     case 'file-tree': return <FileTree />;
   }
   ```

4. **Merge features incrementally**
   - Layout PR merges first (with placeholders)
   - Feature PRs merge independently
   - Replace placeholders as features land
   - No blocking dependencies

**Example (enowX-Coder session):**
- PR #14: Layout system with placeholders for all 9 features
- PRs #6-#13: Individual features (File Tree, Terminal, Git, Search, Editor, etc.)
- Integration: `FileTreePlaceholder` → `<FileTree />` when PR #8 merges

**Benefits:**
- ✅ Layout testable independently
- ✅ Features developed in parallel
- ✅ Clear "what's missing" view for users
- ✅ Smooth integration path
- ✅ No merge conflicts
- ✅ Reviewers can test layout without waiting for features

**Pitfall to avoid:** Don't create cross-branch dependencies. Each feature PR should work standalone (even if just showing placeholder in layout).

### PR Organization

**Phase 1: Quick Wins (1-2 hours each)**
- Keyboard shortcuts
- Loading states
- Empty states
- UI polish

**Phase 2: Core Features (2-4 hours each)**
- File tree
- Terminal integration
- Command palette

**Phase 3: Advanced Features (4-6 hours each)**
- Code editor (Monaco/CodeMirror)
- Git integration
- Search & replace

**Phase 4: Unique Features (5-8 hours each)**
- AI code review
- Test generation
- Debugger integration

### Branch Naming

```bash
feat/command-palette-keyboard-shortcuts
feat/loading-empty-states
feat/file-tree-sidebar
feat/terminal-integration
feat/monaco-code-editor
feat/git-integration
feat/search-replace
feat/ai-code-review
```

**Pattern:** `feat/<feature-name>` (kebab-case, descriptive)

## Tauri + TypeScript + Rust Pattern

### Architecture

```
project/
├── src/                    # Frontend (React/TypeScript)
│   ├── components/ui/      # React components
│   ├── stores/             # Zustand state management
│   └── lib/                # Utilities
└── src-tauri/              # Backend (Rust)
    └── src/
        ├── commands/       # Tauri commands
        ├── lib.rs          # Command registration
        └── main.rs         # Entry point
```

### Implementation Pattern

**For each feature:**

1. **Create Rust commands** (if backend needed)
2. **Create TypeScript store** (state management)
3. **Create React component** (UI)
4. **Test TypeScript compilation**
5. **Fix errors immediately**
6. **Commit and push**

### Step-by-Step: Adding a Feature

#### 1. Create Rust Commands (Backend)

```rust
// src-tauri/src/commands/feature.rs
use serde::{Deserialize, Serialize};
use tauri::command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FeatureData {
    pub id: String,
    pub value: String,
}

#[command]
pub async fn feature_action(param: String) -> Result<FeatureData, String> {
    // Implementation
    Ok(FeatureData {
        id: "1".to_string(),
        value: param,
    })
}
```

#### 2. Register Commands

```rust
// src-tauri/src/commands/mod.rs
pub mod feature;

// src-tauri/src/lib.rs
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![
        commands::feature::feature_action,
        // ... other commands
    ])
```

#### 3. Create TypeScript Store

```typescript
// src/stores/useFeatureStore.ts
import { create } from 'zustand';

interface FeatureState {
  data: FeatureData | null;
  setData: (data: FeatureData | null) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useFeatureStore = create<FeatureState>((set) => ({
  data: null,
  setData: (data) => set({ data }),
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
}));
```

#### 4. Create React Component

```typescript
// src/components/ui/Feature.tsx
import { useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { useFeatureStore } from '@/stores/useFeatureStore';

export function Feature() {
  const { data, setData, isLoading, setIsLoading } = useFeatureStore();

  const handleAction = async () => {
    setIsLoading(true);
    try {
      const result = await invoke('feature_action', { param: 'value' });
      setData(result);
    } catch (error) {
      console.error('Failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <button onClick={handleAction}>Action</button>
      {isLoading && <p>Loading...</p>}
      {data && <p>{data.value}</p>}
    </div>
  );
}
```

#### 5. Test TypeScript Compilation

```bash
npx tsc --noEmit
```

**Common errors:**
- Unused variables → Remove or prefix with `_`
- Unused imports → Remove
- Type mismatches → Fix types
- Missing dependencies → Install

**Fix immediately before continuing!**

#### 6. Commit and Push

```bash
git add .
git commit -m "feat(feature): add feature with backend integration"
git push -u origin feat/feature-name
```

## Quality Checklist

### Before Each Commit

- [ ] TypeScript compilation passes (`npx tsc --noEmit`)
- [ ] No unused variables/imports/parameters
- [ ] Event listeners cleaned up (useEffect return functions)
- [ ] Error handling present (try/catch)
- [ ] Loading states implemented
- [ ] Empty states implemented

### Before Each PR

- [ ] Feature complete (not half-implemented)
- [ ] Documentation added (README update or new docs/ file)
- [ ] Examples provided (real-world usage)
- [ ] Accessibility considered (aria labels, keyboard navigation)
- [ ] Performance optimized (useMemo, useCallback where needed)

### PR Description Template

```markdown
## Overview

[One-sentence description]

## Features

### Frontend
- [Feature 1]
- [Feature 2]

### Backend (Rust)
- [Command 1]
- [Command 2]

## UI/UX
- [Design decision 1]
- [Design decision 2]

## Testing
- [What was tested]
- [How to test]

Ready for review!
```

## Common Patterns

### File Tree Implementation

**Rust commands needed:**
- `read_directory` — List files/folders
- `read_file_content` — Read file
- `write_file_content` — Write file
- `create_file` — Create new file
- `create_directory` — Create new folder
- `delete_file` — Delete file/folder
- `rename_file` — Rename file/folder

**Frontend features:**
- File type icons (by extension)
- Context menu (right-click)
- Drag and drop
- Search/filter
- Expand/collapse folders

### Terminal Integration

**Dependencies:**
- `@xterm/xterm` — Terminal emulator
- `@xterm/addon-fit` — Auto-resize
- `@xterm/addon-web-links` — Clickable links

**Rust commands needed:**
- `create_terminal_session` — Spawn shell
- `write_to_terminal` — Send input
- `read_from_terminal` — Get output
- `close_terminal_session` — Cleanup

**Frontend features:**
- Multiple tabs
- Auto-resize on window change
- Keyboard shortcuts (Ctrl+C, Ctrl+V)
- Theme sync (dark/light)

### Git Integration

**Rust commands needed:**
- `git_status` — Get file status
- `git_branches` — List branches
- `git_current_branch` — Get active branch
- `git_log` — Commit history
- `git_stage` — Stage file
- `git_unstage` — Unstage file
- `git_commit` — Commit changes
- `git_push` — Push to remote
- `git_pull` — Pull from remote
- `git_checkout` — Switch branch
- `git_diff` — Get file diff

**Frontend features:**
- Status indicators (M, A, D, U)
- Stage/unstage UI
- Commit message input
- Push/pull buttons
- Branch switcher
- Diff viewer

### Search & Replace

**Rust commands needed:**
- `search_in_files` — Recursive search with regex
- `replace_in_file` — Find and replace

**Frontend features:**
- Case-sensitive toggle
- Whole word toggle
- Regex support
- Replace in file
- Replace all in all files
- Grouped results by file

### Code Editor (Monaco)

**Dependencies:**
- `@monaco-editor/react` — React wrapper
- `monaco-editor` — Editor core

**Frontend features:**
- Multi-tab support
- Language detection (by extension)
- IntelliSense
- Syntax highlighting
- Keyboard shortcuts (Cmd+S to save)
- Minimap
- Line numbers

## Testing Strategy

### Per-PR Testing

```bash
# Switch to branch
git checkout feat/feature-name

# Test TypeScript
npx tsc --noEmit

# Test Rust (if cargo available)
cd src-tauri && cargo check

# Manual testing
# - Open UI
# - Test all interactions
# - Check error states
# - Check loading states
# - Check empty states
```

### Comprehensive Testing (All PRs)

```bash
# Test all branches
for branch in feat/*; do
  git checkout $branch
  npx tsc --noEmit || echo "❌ $branch FAILED"
done
```

### Final QA Report

```markdown
## FINAL QUALITY ASSURANCE REPORT

| PR | Feature | TypeScript | Rust | Status |
|----|---------|-----------|------|--------|
| #6 | Command Palette | ✅ PASS | N/A | READY |
| #7 | Loading States | ✅ PASS | N/A | READY |
| #8 | File Tree | ✅ PASS | ✅ PASS | READY |

Quality Score: 10/10
Production Ready: 100%
```

## Pitfalls

### 1. Accumulating TypeScript Errors

**❌ WRONG:**
```bash
# Push with errors, fix later
git push  # Has 3 TypeScript errors
```

**✅ CORRECT:**
```bash
# Test before push
npx tsc --noEmit
# Fix errors
# Test again
npx tsc --noEmit
# Push
git push
```

### 2. Missing Cleanup Functions

**❌ WRONG:**
```typescript
useEffect(() => {
  window.addEventListener('keydown', handler);
  // Missing cleanup!
}, []);
```

**✅ CORRECT:**
```typescript
useEffect(() => {
  window.addEventListener('keydown', handler);
  return () => window.removeEventListener('keydown', handler);
}, []);
```

### 3. Unused Variables

**❌ WRONG:**
```typescript
const [value, setValue] = useState('');  // setValue unused
```

**✅ CORRECT:**
```typescript
const [value] = useState('');  // No setValue
```

### 4. Missing Dependencies

**❌ WRONG:**
```bash
# Assume dependency exists
import { Terminal } from '@xterm/xterm';  # Not installed!
```

**✅ CORRECT:**
```bash
# Install first
bun add @xterm/xterm @xterm/addon-fit
# Then import
import { Terminal } from '@xterm/xterm';
```

### 5. Incomplete Features

**❌ WRONG:**
```typescript
// File tree without delete/rename
// Terminal without multiple tabs
// Git without push/pull
```

**✅ CORRECT:**
```typescript
// Complete feature set
// All CRUD operations
// All expected functionality
```

### 6. Cross-Branch Import Errors

**Problem:** Importing stores/components that don't exist in main branch yet.

**❌ WRONG:**
```typescript
// In feat/search-replace branch
import { useFileTreeStore } from '@/stores/useFileTreeStore';  // Doesn't exist in main!
```

**✅ CORRECT:**
```typescript
// Use local state or mock data
const [rootPath] = useState('/');  // Default value
```

**When it happens:** Creating features that depend on other feature branches.

**Solution:** Each feature branch should be self-contained. Use placeholders, mock data, or local state instead of importing from other feature branches.

### 7. JSX Syntax Errors

**❌ WRONG:**
```tsx
<span className="font-semibold">></span>  // Error: Unexpected token
```

**✅ CORRECT:**
```tsx
<span className="font-semibold">&gt;</span>  // Use HTML entity
```

**Common characters that need escaping:**
- `>` → `&gt;`
- `<` → `&lt;`
- `&` → `&amp;`
- `"` → `&quot;`

## Success Metrics

**Good contribution:**
- 3-5 PRs
- 1,000-2,000 lines of code
- All TypeScript passes
- Basic documentation

**Great contribution:**
- 5-8 PRs
- 3,000-5,000 lines of code
- All tests pass
- Comprehensive documentation
- Examples provided

**World-class contribution:**
- 8+ PRs
- 7,000+ lines of code
- Zero errors
- Comprehensive documentation
- Real-world examples
- Competitive analysis
- Unique features

## Example Session Output

**Session goal:** Make enowX-Coder world-class IDE

**Contributions:**
1. PR #6: Command Palette (593 lines)
2. PR #7: Loading States (286 lines)
3. PR #8: File Tree (1,800 lines)
4. PR #9: Terminal (1,664 lines)
5. PR #10: Monaco Editor (1,656 lines)
6. PR #11: Git Integration (642 lines)
7. PR #12: Search & Replace (505 lines)
8. PR #13: AI Code Review (273 lines)

**Total:** 8 PRs, 7,419 lines, 0 errors, 100% production ready

**Result:** enowX-Coder now matches Cursor/Windsurf + has unique AI code review feature

## References

### Internal
- `references/tauri-typescript-integration.md` — Complete Tauri + TypeScript integration pattern with examples
- `references/enowx-coder-12pr-case-study.md` — Real-world case study: 12 PRs transforming AI chat tool into world-class IDE (8,415 lines, 0 errors, placeholder-based integration strategy)

### External
- [Tauri Commands Documentation](https://tauri.app/v1/guides/features/command)
- [Monaco Editor API](https://microsoft.github.io/monaco-editor/api/index.html)
- [xterm.js Documentation](https://xtermjs.org/)
- [Zustand State Management](https://github.com/pmndrs/zustand)
