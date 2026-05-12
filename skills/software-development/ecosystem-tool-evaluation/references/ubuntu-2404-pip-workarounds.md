# Ubuntu 24.04 PEP 668 pip Install Workarounds

## Problem

Ubuntu 24.04 (and Debian 12+) enforce PEP 668 externally-managed-environment protection, blocking `pip install` to system Python:

```bash
$ pip install mnemosyne-memory
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
```

This affects **all** pip installs, including `--user` flag.

## Root Cause

- System Python is marked as "externally managed" via `/usr/lib/python3.12/EXTERNALLY-MANAGED`
- Prevents accidental breakage of system packages
- Enforced by default in Ubuntu 24.04, Debian 12+

## Workaround Hierarchy

### 1. **Zero-pip Method (Preferred for Hermes Plugins)**

For tools that provide Hermes plugin integration via symlink:

```bash
# Clone to permanent location
mkdir -p ~/.hermes/ecosystem
cd ~/.hermes/ecosystem
git clone https://github.com/user/tool.git

# Symlink plugin directory
ln -s ~/.hermes/ecosystem/tool/hermes_memory_provider ~/.hermes/plugins/tool

# Configure
hermes config set memory.provider tool
```

**Pros:**
- No pip needed
- No venv overhead
- Works on any Ubuntu 24.04 system
- Survives across reboots (if cloned to permanent location)

**Cons:**
- Only works for tools with Hermes plugin structure
- Requires manual dependency management if tool needs extras

**Example:** Mnemosyne memory provider

### 2. **Virtual Environment (Standard Python Practice)**

```bash
# Create venv
python3 -m venv ~/.venv/project
source ~/.venv/project/bin/activate

# Install
pip install package[all]

# Use
python script.py
```

**Pros:**
- Standard Python practice
- Isolated dependencies
- Works for any Python package

**Cons:**
- Must activate venv every time
- Hermes must run inside same venv
- Adds ~50-100MB per venv

**When to use:** Installing Python libraries for development/scripting

### 3. **pipx (For CLI Tools)**

```bash
# Install pipx
sudo apt install pipx
pipx ensurepath

# Install tool
pipx install package
```

**Pros:**
- Automatic venv management
- CLI tools available globally
- Clean uninstall

**Cons:**
- Only for CLI tools (not libraries)
- Adds overhead per tool

**When to use:** Installing standalone CLI tools (e.g., `black`, `ruff`, `poetry`)

### 4. **--break-system-packages (NOT RECOMMENDED)**

```bash
pip install --break-system-packages package
```

**Pros:**
- Works immediately
- No venv needed

**Cons:**
- ⚠️ Can break system Python
- ⚠️ Conflicts with apt packages
- ⚠️ Security risk
- ⚠️ Not reversible easily

**When to use:** Never in production. Only for throwaway containers/VMs.

## Decision Tree

```
Need to install Python package on Ubuntu 24.04?
  ↓
Is it a Hermes plugin with symlink support?
  ├─ Yes → Use zero-pip method (clone + symlink)
  └─ No → Continue
      ↓
Is it a CLI tool?
  ├─ Yes → Use pipx
  └─ No → Continue
      ↓
Is it for development/scripting?
  ├─ Yes → Use venv
  └─ No → Reconsider if you need it
```

## Mnemosyne Case Study

**Problem:** `pip install mnemosyne-memory[all]` fails on Ubuntu 24.04

**Solution:** Zero-pip method

```bash
# 1. Clone to permanent location (NOT /tmp)
mkdir -p ~/.hermes/ecosystem
cd ~/.hermes/ecosystem
git clone https://github.com/AxDSan/mnemosyne.git

# 2. Symlink plugin
rm -f ~/.hermes/plugins/mnemosyne  # remove old if exists
ln -s ~/.hermes/ecosystem/mnemosyne/hermes_memory_provider ~/.hermes/plugins/mnemosyne

# 3. Configure
hermes config set memory.provider mnemosyne

# 4. Verify
hermes memory status
hermes mnemosyne stats
```

**Why this works:**
- Mnemosyne provides `hermes_memory_provider/` directory
- Hermes loads plugins from `~/.hermes/plugins/` via symlink
- No pip needed — Python imports work via `sys.path` manipulation
- Survives reboots (cloned to `~/.hermes/ecosystem/`, not `/tmp`)

**Pitfalls avoided:**
- ❌ Cloning to `/tmp/mnemosyne` → symlink breaks after reboot (tmpfs cleared)
- ✅ Cloning to `~/.hermes/ecosystem/mnemosyne` → permanent location
- ❌ Running `deploy_hermes_provider.sh` from `/tmp` → script expects to be run from repo root
- ✅ Clone first, then run script from cloned directory OR manually symlink

## Common Mistakes

### 1. **Cloning to /tmp**

```bash
❌ cd /tmp && git clone ...
   ln -s /tmp/tool ~/.hermes/plugins/tool
   # Breaks after reboot — /tmp is cleared
```

**Fix:** Clone to permanent location (`~/.hermes/ecosystem/`)

### 2. **Using --user Flag**

```bash
❌ pip install --user package
   # Still fails on Ubuntu 24.04 — PEP 668 blocks this too
```

**Fix:** Use venv or zero-pip method

### 3. **Forgetting to Activate venv**

```bash
❌ python3 -m venv .venv
   pip install package  # Installs to system, fails
```

**Fix:** Always `source .venv/bin/activate` first

## Verification

After workaround, verify:

```bash
# For Hermes plugins
hermes memory status  # Should show plugin active

# For CLI tools
which tool  # Should show path

# For libraries
python -c "import package; print(package.__version__)"
```

## References

- [PEP 668](https://peps.python.org/pep-0668/) — Marking Python base environments as "externally managed"
- [Ubuntu 24.04 Release Notes](https://discourse.ubuntu.com/t/noble-numbat-release-notes/39890) — Python externally-managed-environment
- [Mnemosyne deploy script](https://github.com/AxDSan/mnemosyne/blob/main/deploy_hermes_provider.sh) — Zero-pip installation example
