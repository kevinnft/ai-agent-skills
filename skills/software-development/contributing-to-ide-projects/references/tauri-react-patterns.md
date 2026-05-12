# Tauri 2 + React 19 Integration Patterns

Patterns discovered during enowX-Coder contribution (9 PRs, May 2026).

## Rust Command Registration

```rust
// src-tauri/src/commands/mod.rs
pub mod git;
pub mod search;
pub mod terminal;

// src-tauri/src/lib.rs
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![
        commands::git::git_status,
        commands::git::git_commit,
        commands::search::search_in_files,
        commands::terminal::create_terminal_session,
    ])
```

## Frontend Invocation

```tsx
import { invoke } from '@tauri-apps/api/core';

// Async command
const result = await invoke<GitStatus[]>('git_status', { 
  repoPath: '/path/to/repo' 
});

// Error handling
try {
  await invoke('git_commit', { repoPath, message });
} catch (error) {
  console.error('Commit failed:', error);
  alert(`Failed: ${error}`);
}
```

## State Management (Zustand)

```tsx
// stores/useGitStore.ts
import { create } from 'zustand';

interface GitState {
  status: GitStatus[];
  setStatus: (status: GitStatus[]) => void;
}

export const useGitStore = create<GitState>((set) => ({
  status: [],
  setStatus: (status) => set({ status }),
}));
```

## Component Pattern

```tsx
export function GitPanel() {
  const { status, setStatus } = useGitStore();
  const [isLoading, setIsLoading] = useState(false);

  const refreshStatus = async () => {
    setIsLoading(true);
    try {
      const result = await invoke<GitStatus[]>('git_status', { repoPath });
      setStatus(result);
    } catch (error) {
      console.error('Failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshStatus();
  }, []);

  return (
    <div>
      {isLoading ? <Spinner /> : <StatusList items={status} />}
    </div>
  );
}
```

## TypeScript Error Patterns

### Unused Variables
```tsx
// ❌ Error: 'setSelectedFiles' is declared but never used
const [selectedFiles, setSelectedFiles] = useState<string[]>([]);

// ✅ Fix: Remove setter if not needed
const [selectedFiles] = useState<string[]>([]);
```

### Unused Imports
```tsx
// ❌ Error: 'FloppyDisk' is declared but never used
import { X, FloppyDisk, Circle } from '@phosphor-icons/react';

// ✅ Fix: Remove unused import
import { X, Circle } from '@phosphor-icons/react';
```

### Monaco Editor OnMount
```tsx
// ❌ Wrong signature
const handleEditorDidMount: OnMount = (editor) => {
  editorRef.current = editor;
};

// ✅ Correct signature (OnMount expects 2 params)
const handleEditorDidMount: OnMount = (monacoEditor, monaco) => {
  editorRef.current = monacoEditor;
  monacoEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, save);
};
```

## Cleanup Patterns

```tsx
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    // Handle shortcut
  };

  window.addEventListener('keydown', handleKeyDown);
  
  // ✅ Always cleanup
  return () => window.removeEventListener('keydown', handleKeyDown);
}, [dependencies]);
```

## File Operations (Rust)

```rust
use std::fs;
use std::path::Path;

#[command]
pub async fn read_file_content(path: String) -> Result<String, String> {
    fs::read_to_string(&path)
        .map_err(|e| format!("Failed to read: {}", e))
}

#[command]
pub async fn write_file_content(path: String, content: String) -> Result<(), String> {
    fs::write(&path, content)
        .map_err(|e| format!("Failed to write: {}", e))
}
```

## Search with Regex (Rust)

```rust
use regex::Regex;

#[command]
pub async fn search_in_files(
    root_path: String,
    query: String,
    case_sensitive: bool,
    use_regex: bool,
) -> Result<Vec<SearchResult>, String> {
    let pattern = if use_regex {
        query.clone()
    } else {
        regex::escape(&query)
    };
    
    let regex = if case_sensitive {
        Regex::new(&pattern)
    } else {
        Regex::new(&format!("(?i){}", pattern))
    }.map_err(|e| format!("Invalid regex: {}", e))?;
    
    // Search implementation...
}
```

## Terminal Integration (xterm.js)

```tsx
import { Terminal as XTerm } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';

const xtermRef = useRef<XTerm | null>(null);
const fitAddonRef = useRef<FitAddon | null>(null);

useEffect(() => {
  const xterm = new XTerm({ /* options */ });
  const fitAddon = new FitAddon();
  
  xterm.loadAddon(fitAddon);
  xterm.open(terminalRef.current!);
  fitAddon.fit();
  
  xtermRef.current = xterm;
  fitAddonRef.current = fitAddon;
  
  return () => {
    xterm.dispose();
  };
}, []);
```

## Git Commands (Rust)

```rust
use std::process::Command;

#[command]
pub async fn git_status(repo_path: String) -> Result<Vec<GitStatus>, String> {
    let output = Command::new("git")
        .args(&["status", "--porcelain"])
        .current_dir(&repo_path)
        .output()
        .map_err(|e| format!("Failed: {}", e))?;

    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).to_string());
    }

    // Parse output...
}
```

## Testing All Branches

```bash
# Test TypeScript on all feature branches
for branch in feat/command-palette feat/file-tree feat/terminal; do
  echo "Testing $branch..."
  git checkout $branch 2>&1 | grep -q "Switched" && \
  npx tsc --noEmit 2>&1 | grep -q "error" && \
  echo "❌ FAIL" || echo "✅ PASS"
done
```

## Common Pitfalls

1. **Missing cleanup** — Always return cleanup function from useEffect
2. **Wrong OnMount signature** — Monaco expects (editor, monaco), not just (editor)
3. **Unused variables** — TypeScript strict mode catches these
4. **Missing error handling** — Always try/catch Tauri invoke calls
5. **Cross-branch dependencies** — Use placeholders to avoid blocking
