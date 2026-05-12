# Tauri + TypeScript Integration Pattern

Complete pattern for adding features to Tauri apps with TypeScript frontend and Rust backend.

## Pattern Overview

```
Feature Request
    ↓
1. Create Rust commands (src-tauri/src/commands/feature.rs)
    ↓
2. Register commands (mod.rs + lib.rs)
    ↓
3. Create TypeScript store (src/stores/useFeatureStore.ts)
    ↓
4. Create React component (src/components/ui/Feature.tsx)
    ↓
5. Test TypeScript (npx tsc --noEmit)
    ↓
6. Fix errors immediately
    ↓
7. Commit and push
```

## 1. Rust Commands

### File Structure

```
src-tauri/src/commands/
├── mod.rs              # Module exports
├── feature.rs          # Your feature commands
├── git.rs              # Git commands
├── search.rs           # Search commands
└── terminal.rs         # Terminal commands
```

### Command Template

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

#[command]
pub async fn feature_list() -> Result<Vec<FeatureData>, String> {
    // Implementation
    Ok(vec![])
}
```

### Error Handling Pattern

```rust
#[command]
pub async fn feature_action(param: String) -> Result<FeatureData, String> {
    // Use map_err to convert errors to String
    let result = some_operation()
        .map_err(|e| format!("Failed to do X: {}", e))?;
    
    Ok(result)
}
```

## 2. Register Commands

### Update mod.rs

```rust
// src-tauri/src/commands/mod.rs
pub mod agent;
pub mod chat;
pub mod feature;  // Add your module
pub mod git;
pub mod search;
```

### Update lib.rs

```rust
// src-tauri/src/lib.rs
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![
        // Existing commands
        commands::agent::list_agent_configs,
        commands::agent::agent_permission_response,
        // Your new commands
        commands::feature::feature_action,
        commands::feature::feature_list,
    ])
    .setup(|app| {
        // Setup code
        Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

## 3. TypeScript Store (Zustand)

### Store Template

```typescript
// src/stores/useFeatureStore.ts
import { create } from 'zustand';

export interface FeatureData {
  id: string;
  value: string;
}

interface FeatureState {
  // Data
  items: FeatureData[];
  setItems: (items: FeatureData[]) => void;
  
  // Selected item
  selectedItem: FeatureData | null;
  setSelectedItem: (item: FeatureData | null) => void;
  
  // Loading state
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  
  // Actions
  addItem: (item: FeatureData) => void;
  removeItem: (id: string) => void;
  updateItem: (id: string, updates: Partial<FeatureData>) => void;
}

export const useFeatureStore = create<FeatureState>((set) => ({
  // Initial state
  items: [],
  setItems: (items) => set({ items }),
  
  selectedItem: null,
  setSelectedItem: (item) => set({ selectedItem: item }),
  
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
  
  // Actions
  addItem: (item) =>
    set((state) => ({ items: [...state.items, item] })),
  
  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id),
    })),
  
  updateItem: (id, updates) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.id === id ? { ...item, ...updates } : item
      ),
    })),
}));
```

## 4. React Component

### Component Template

```typescript
// src/components/ui/Feature.tsx
import { useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { useFeatureStore, FeatureData } from '@/stores/useFeatureStore';
import { MagnifyingGlass, Plus, X } from '@phosphor-icons/react';

export function Feature() {
  const {
    items,
    setItems,
    selectedItem,
    setSelectedItem,
    isLoading,
    setIsLoading,
    addItem,
    removeItem,
  } = useFeatureStore();

  // Load data on mount
  useEffect(() => {
    loadItems();
  }, []);

  const loadItems = async () => {
    setIsLoading(true);
    try {
      const result = await invoke<FeatureData[]>('feature_list');
      setItems(result);
    } catch (error) {
      console.error('Failed to load items:', error);
      alert(`Failed to load: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAction = async (param: string) => {
    try {
      const result = await invoke<FeatureData>('feature_action', { param });
      addItem(result);
    } catch (error) {
      console.error('Action failed:', error);
      alert(`Action failed: ${error}`);
    }
  };

  const handleRemove = async (id: string) => {
    try {
      await invoke('feature_remove', { id });
      removeItem(id);
    } catch (error) {
      console.error('Remove failed:', error);
      alert(`Remove failed: ${error}`);
    }
  };

  return (
    <div className="h-full flex flex-col bg-[var(--background)]">
      {/* Header */}
      <div className="p-3 border-b border-[var(--border)]">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold">Feature</h3>
          <button
            onClick={() => handleAction('new')}
            className="p-1 hover:bg-[var(--surface-hover)] rounded"
          >
            <Plus size={16} />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center h-32">
            <MagnifyingGlass size={24} className="animate-spin text-[var(--accent)]" />
          </div>
        ) : items.length === 0 ? (
          <div className="p-4 text-center text-sm text-[var(--text-secondary)]">
            No items
          </div>
        ) : (
          <div className="p-2">
            {items.map((item) => (
              <div
                key={item.id}
                className="flex items-center gap-2 px-2 py-1 hover:bg-[var(--surface-hover)] rounded cursor-pointer"
                onClick={() => setSelectedItem(item)}
              >
                <span className="flex-1">{item.value}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleRemove(item.id);
                  }}
                  className="p-1 hover:bg-red-500/10 rounded"
                >
                  <X size={14} className="text-red-500" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
```

## 5. Testing

### TypeScript Compilation

```bash
# Test TypeScript
npx tsc --noEmit

# Common errors and fixes:
# - "TS6133: 'X' is declared but never used"
#   → Remove variable or prefix with underscore: _X
# - "TS2307: Cannot find module"
#   → Install dependency: bun add <package>
# - "TS2345: Argument of type X is not assignable to Y"
#   → Fix type mismatch
```

### Rust Compilation (if cargo available)

```bash
cd src-tauri
cargo check

# Common errors:
# - "cannot find X in this scope"
#   → Add use statement or fix typo
# - "mismatched types"
#   → Fix type conversion
```

## Common Patterns

### File Operations

```rust
// Read file
use std::fs;

#[command]
pub async fn read_file(path: String) -> Result<String, String> {
    fs::read_to_string(&path)
        .map_err(|e| format!("Failed to read file: {}", e))
}

// Write file
#[command]
pub async fn write_file(path: String, content: String) -> Result<(), String> {
    fs::write(&path, content)
        .map_err(|e| format!("Failed to write file: {}", e))
}

// List directory
#[command]
pub async fn list_directory(path: String) -> Result<Vec<String>, String> {
    let entries = fs::read_dir(&path)
        .map_err(|e| format!("Failed to read directory: {}", e))?;
    
    let mut files = Vec::new();
    for entry in entries {
        let entry = entry.map_err(|e| format!("Failed to read entry: {}", e))?;
        files.push(entry.path().to_string_lossy().to_string());
    }
    
    Ok(files)
}
```

### Shell Commands

```rust
use std::process::Command;

#[command]
pub async fn run_command(cmd: String, args: Vec<String>) -> Result<String, String> {
    let output = Command::new(&cmd)
        .args(&args)
        .output()
        .map_err(|e| format!("Failed to run command: {}", e))?;
    
    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).to_string());
    }
    
    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}
```

### Git Commands

```rust
#[command]
pub async fn git_status(repo_path: String) -> Result<Vec<String>, String> {
    let output = Command::new("git")
        .args(&["status", "--porcelain"])
        .current_dir(&repo_path)
        .output()
        .map_err(|e| format!("Failed to run git status: {}", e))?;
    
    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).to_string());
    }
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    Ok(stdout.lines().map(|s| s.to_string()).collect())
}
```

### Event Emission (Tauri → Frontend)

```rust
use tauri::{AppHandle, Emitter};

#[command]
pub async fn start_process(app: AppHandle) -> Result<(), String> {
    // Do work...
    
    // Emit event to frontend
    app.emit("process-update", "50% complete")
        .map_err(|e| format!("Failed to emit event: {}", e))?;
    
    Ok(())
}
```

```typescript
// Frontend: Listen for events
import { listen } from '@tauri-apps/api/event';

useEffect(() => {
  const unlisten = listen('process-update', (event) => {
    console.log('Update:', event.payload);
  });
  
  return () => {
    unlisten.then((fn) => fn());
  };
}, []);
```

## Pitfalls

### 1. Missing Cleanup in useEffect

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

### 2. Unused Variables

**❌ WRONG:**
```typescript
const [value, setValue] = useState('');  // setValue unused
```

**✅ CORRECT:**
```typescript
const [value] = useState('');  // No setValue
// OR
const [value, _setValue] = useState('');  // Prefix with underscore
```

### 3. Missing Error Handling

**❌ WRONG:**
```typescript
const result = await invoke('command');  // No try/catch
```

**✅ CORRECT:**
```typescript
try {
  const result = await invoke('command');
  // Use result
} catch (error) {
  console.error('Failed:', error);
  alert(`Failed: ${error}`);
}
```

### 4. Forgetting to Register Commands

**❌ WRONG:**
```rust
// Created command but forgot to add to invoke_handler
#[command]
pub async fn new_command() -> Result<(), String> { Ok(()) }
```

**✅ CORRECT:**
```rust
// Add to lib.rs invoke_handler
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![
        commands::feature::new_command,  // Register here!
    ])
```

### 5. Type Mismatches

**❌ WRONG:**
```typescript
// Rust returns Vec<String>, TypeScript expects string[]
const result = await invoke<string>('list_items');  // Wrong type!
```

**✅ CORRECT:**
```typescript
const result = await invoke<string[]>('list_items');  // Correct type
```

## Testing Checklist

Before each commit:
- [ ] `npx tsc --noEmit` passes
- [ ] No unused variables/imports
- [ ] Event listeners cleaned up
- [ ] Error handling present
- [ ] Loading states implemented
- [ ] Empty states implemented
- [ ] Commands registered in lib.rs
- [ ] Module exported in mod.rs

## Example: Complete Feature

See the main skill document for complete examples of:
- File Tree (7 Rust commands, full CRUD)
- Terminal Integration (4 commands, xterm.js)
- Git Integration (11 commands, full workflow)
- Search & Replace (2 commands, regex support)
