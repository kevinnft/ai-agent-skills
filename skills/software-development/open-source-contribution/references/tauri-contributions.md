# Tauri Contribution Patterns

Tauri-specific patterns for contributing to Tauri desktop apps (Rust backend + web frontend).

## Architecture

**Tauri = Rust backend + Web frontend**
- Frontend: React/Vue/Svelte (TypeScript/JavaScript)
- Backend: Rust (Tauri commands)
- IPC: `invoke()` from frontend → Rust command
- Events: Rust emits → frontend listens

## Adding Rust Commands

### 1. Create Command Module

**File:** `src-tauri/src/commands/your_module.rs`

```rust
use tauri::command;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct YourData {
    pub id: String,
    pub value: String,
}

#[command]
pub async fn your_command(param: String) -> Result<YourData, String> {
    // Implementation
    Ok(YourData {
        id: "123".to_string(),
        value: param,
    })
}
```

**Key patterns:**
- `#[command]` macro required
- `async fn` for async operations
- Return `Result<T, String>` for error handling
- Use `serde` for serialization

### 2. Register in `commands/mod.rs`

```rust
pub mod your_module;
```

### 3. Register in `lib.rs`

```rust
.invoke_handler(tauri::generate_handler![
    // ... existing commands
    commands::your_module::your_command,
])
```

### 4. Call from Frontend

```typescript
import { invoke } from '@tauri-apps/api/core';

const result = await invoke<YourData>('your_command', { param: 'value' });
```

## File Operations

### Read Directory (Recursive)

```rust
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileNode {
    pub name: String,
    pub path: String,
    #[serde(rename = "type")]
    pub node_type: String, // "file" or "directory"
    pub children: Option<Vec<FileNode>>,
}

#[command]
pub async fn read_directory(path: String, recursive: bool) -> Result<Vec<FileNode>, String> {
    let path = Path::new(&path);
    
    if !path.exists() {
        return Err(format!("Path does not exist: {}", path.display()));
    }
    
    read_dir_recursive(path, recursive)
}

fn read_dir_recursive(path: &Path, recursive: bool) -> Result<Vec<FileNode>, String> {
    let mut nodes = Vec::new();
    
    let entries = fs::read_dir(path)
        .map_err(|e| format!("Failed to read directory: {}", e))?;
    
    for entry in entries {
        let entry = entry.map_err(|e| format!("Failed to read entry: {}", e))?;
        let path = entry.path();
        let name = entry.file_name().to_string_lossy().to_string();
        
        // Skip hidden files
        if name.starts_with('.') {
            continue;
        }
        
        let metadata = entry.metadata()
            .map_err(|e| format!("Failed to read metadata: {}", e))?;
        
        let node_type = if metadata.is_dir() { "directory" } else { "file" };
        
        let children = if metadata.is_dir() && recursive {
            Some(read_dir_recursive(&path, recursive).unwrap_or_default())
        } else {
            None
        };
        
        nodes.push(FileNode {
            name,
            path: path.to_string_lossy().to_string(),
            node_type: node_type.to_string(),
            children,
        });
    }
    
    // Sort: directories first, then alphabetically
    nodes.sort_by(|a, b| {
        match (a.node_type.as_str(), b.node_type.as_str()) {
            ("directory", "file") => std::cmp::Ordering::Less,
            ("file", "directory") => std::cmp::Ordering::Greater,
            _ => a.name.to_lowercase().cmp(&b.name.to_lowercase()),
        }
    });
    
    Ok(nodes)
}
```

### Read/Write File

```rust
#[command]
pub async fn read_file_content(path: String) -> Result<String, String> {
    fs::read_to_string(&path)
        .map_err(|e| format!("Failed to read file: {}", e))
}

#[command]
pub async fn write_file_content(path: String, content: String) -> Result<(), String> {
    fs::write(&path, content)
        .map_err(|e| format!("Failed to write file: {}", e))
}
```

## Terminal/PTY Integration

### Basic Shell Spawning

```rust
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use std::collections::HashMap;
use tauri::{AppHandle, Emitter};
use std::io::{BufRead, BufReader, Write};
use std::thread;

type SessionMap = Arc<Mutex<HashMap<String, Child>>>;

#[command]
pub async fn create_terminal_session(
    app: AppHandle,
    session_id: String,
    cwd: String,
) -> Result<(), String> {
    let sessions: tauri::State<SessionMap> = app.state();
    
    // Cross-platform shell detection
    #[cfg(target_os = "windows")]
    let shell = "powershell.exe";
    #[cfg(not(target_os = "windows"))]
    let shell = std::env::var("SHELL").unwrap_or_else(|_| "/bin/bash".to_string());
    
    let mut child = Command::new(shell)
        .current_dir(&cwd)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to spawn shell: {}", e))?;
    
    let stdout = child.stdout.take().ok_or("Failed to get stdout")?;
    let stderr = child.stderr.take().ok_or("Failed to get stderr")?;
    
    // Stream stdout to frontend
    let session_id_clone = session_id.clone();
    let app_clone = app.clone();
    thread::spawn(move || {
        let reader = BufReader::new(stdout);
        for line in reader.lines() {
            if let Ok(line) = line {
                let _ = app_clone.emit(&format!("terminal-output-{}", session_id_clone), line);
            }
        }
    });
    
    // Stream stderr to frontend
    let session_id_clone = session_id.clone();
    let app_clone = app.clone();
    thread::spawn(move || {
        let reader = BufReader::new(stderr);
        for line in reader.lines() {
            if let Ok(line) = line {
                let _ = app_clone.emit(&format!("terminal-output-{}", session_id_clone), line);
            }
        }
    });
    
    sessions.lock().unwrap().insert(session_id, child);
    Ok(())
}

#[command]
pub async fn write_to_terminal(
    app: AppHandle,
    session_id: String,
    data: String,
) -> Result<(), String> {
    let sessions: tauri::State<SessionMap> = app.state();
    let mut sessions = sessions.lock().unwrap();
    
    if let Some(child) = sessions.get_mut(&session_id) {
        if let Some(stdin) = child.stdin.as_mut() {
            stdin.write_all(data.as_bytes())
                .map_err(|e| format!("Failed to write: {}", e))?;
            stdin.flush()
                .map_err(|e| format!("Failed to flush: {}", e))?;
        }
    }
    Ok(())
}
```

### Initialize State in `lib.rs`

```rust
.setup(|app| {
    // ... existing setup
    
    // Initialize terminal session map
    let terminal_sessions: std::collections::HashMap<String, std::process::Child> = 
        std::collections::HashMap::new();
    app.manage(std::sync::Arc::new(std::sync::Mutex::new(terminal_sessions)));
    
    Ok(())
})
```

### Frontend Integration

```typescript
import { listen } from '@tauri-apps/api/event';

// Create terminal
await invoke('create_terminal_session', { sessionId: 'term-1', cwd: '/home/user' });

// Listen for output
const unlisten = await listen<string>(`terminal-output-term-1`, (event) => {
  xterm.write(event.payload + '\r\n');
});

// Write input
xterm.onData((data) => {
  invoke('write_to_terminal', { sessionId: 'term-1', data: data + '\n' });
});

// Cleanup
unlisten();
await invoke('close_terminal_session', { sessionId: 'term-1' });
```

## Event System

### Emit from Rust

```rust
use tauri::{AppHandle, Emitter};

#[command]
pub async fn do_something(app: AppHandle) -> Result<(), String> {
    // Emit event to frontend
    app.emit("my-event", "payload data")
        .map_err(|e| format!("Failed to emit: {}", e))?;
    Ok(())
}
```

### Listen in Frontend

```typescript
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen<string>('my-event', (event) => {
  console.log('Received:', event.payload);
});

// Cleanup
unlisten();
```

## Common Pitfalls

### 1. Missing Command Registration

**Error:** `Command not found: your_command`

**Fix:** Register in `lib.rs`:
```rust
.invoke_handler(tauri::generate_handler![
    commands::your_module::your_command,  // Add this
])
```

### 2. Type Mismatch (Rust ↔ TypeScript)

**Error:** `Failed to deserialize`

**Fix:** Ensure types match:
```rust
// Rust
#[derive(Serialize, Deserialize)]
pub struct Data {
    pub id: String,  // String, not &str
    pub count: i32,  // i32, not usize
}
```

```typescript
// TypeScript
interface Data {
  id: string;
  count: number;
}
```

### 3. Async Command Without `async`

**Error:** `Command must be async`

**Fix:** Add `async`:
```rust
#[command]
pub async fn your_command() -> Result<(), String> {
    // ...
}
```

### 4. Missing State Initialization

**Error:** `State not found`

**Fix:** Initialize in `setup()`:
```rust
.setup(|app| {
    let state = YourState::new();
    app.manage(state);
    Ok(())
})
```

### 5. Path Handling (Cross-Platform)

**Error:** Windows paths fail on Unix

**Fix:** Use `Path` and `PathBuf`:
```rust
use std::path::{Path, PathBuf};

let path = Path::new(&path_string);
let new_path = path.join("subdir");
```

## Testing Rust Commands

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_your_command() {
        let result = your_command("test".to_string()).await;
        assert!(result.is_ok());
    }
}
```

### Integration Tests

```bash
# Run Rust tests
cd src-tauri
cargo test
```

## Performance Tips

1. **Use `async` for I/O operations** (file, network, database)
2. **Use `Arc<Mutex<T>>` for shared state** (thread-safe)
3. **Spawn threads for long-running tasks** (don't block main thread)
4. **Use channels for communication** (tokio::sync::mpsc)
5. **Avoid cloning large data** (use references where possible)

## Security

1. **Validate all inputs** (path traversal, command injection)
2. **Use allowlist for file operations** (restrict to app directory)
3. **Sanitize shell commands** (avoid user input in shell)
4. **Use Tauri's built-in security features** (CSP, allowlist)

## Example: Complete Feature

**File Tree Sidebar (Rust + TypeScript)**

1. Create `src-tauri/src/commands/file_commands.rs` (see "File Operations" above)
2. Register in `commands/mod.rs`: `pub mod file_commands;`
3. Register in `lib.rs`: `commands::file_commands::read_directory,`
4. Create frontend component:

```typescript
// src/components/FileTree.tsx
import { invoke } from '@tauri-apps/api/core';

interface FileNode {
  name: string;
  path: string;
  type: 'file' | 'directory';
  children?: FileNode[];
}

const loadDirectory = async (path: string) => {
  const nodes = await invoke<FileNode[]>('read_directory', {
    path,
    recursive: true,
  });
  return nodes;
};
```

## Resources

- [Tauri Command Documentation](https://tauri.app/v1/guides/features/command)
- [Tauri Events Documentation](https://tauri.app/v1/guides/features/events)
- [Rust Serde Documentation](https://serde.rs/)
