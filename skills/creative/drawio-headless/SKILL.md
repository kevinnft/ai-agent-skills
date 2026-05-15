---
name: drawio-headless
description: Generate architecture diagrams with draw.io in headless/server environments (WSL2, VPS, Docker)
version: 1.0.0
dependencies:
  - draw.io desktop (snap or .deb)
  - xvfb (X virtual framebuffer)
platforms:
  - linux
tags:
  - diagrams
  - architecture
  - visualization
  - headless
  - wsl2
origin: unknown
source_license: see upstream
language: en
---

# Draw.io Headless Diagram Generation

Generate professional architecture diagrams from .drawio XML files in headless environments (WSL2, VPS, Docker) where GUI is not available.

## When to Use

- Server/VPS without X11 display
- WSL2 Ubuntu (no native GUI)
- Docker containers
- CI/CD pipelines
- Automated diagram generation

## Prerequisites

**Required packages:**
```bash
# Install draw.io (snap - easiest)
sudo snap install drawio

# Install Xvfb (virtual framebuffer for headless rendering)
sudo apt-get update
sudo apt-get install -y xvfb
```

**Alternative: .deb package**
```bash
# Download latest .deb
wget https://github.com/jgraph/drawio-desktop/releases/download/v28.2.5/drawio-amd64-28.2.5.deb

# Install
sudo dpkg -i drawio-amd64-28.2.5.deb
sudo apt-get install -f  # Fix dependencies
```

## Verification

```bash
# Check draw.io installation
which drawio
# Expected: /snap/bin/drawio or /usr/bin/drawio

# Test with xvfb-run
xvfb-run -a drawio --version
# Expected: draw.io version number (e.g., 28.2.5)
```

## Usage

### Basic Export

```bash
# Export .drawio to PNG
xvfb-run -a drawio -x -f png -o output.png input.drawio

# Export to SVG
xvfb-run -a drawio -x -f svg -o output.svg input.drawio

# Export to PDF
xvfb-run -a drawio -x -f pdf -o output.pdf input.drawio
```

### Flags Explained

- `xvfb-run -a` — Run in virtual framebuffer (headless)
- `-x` — Export mode
- `-f <format>` — Output format (png, svg, pdf, jpg)
- `-o <output>` — Output file path
- `<input>` — Input .drawio file

## Pitfalls

### 1. Snap Confinement (File Access)

**Problem:** Snap-installed draw.io cannot access `/tmp` or arbitrary directories due to confinement.

**Solution:** Use home directory or snap-accessible paths:
```bash
# ❌ FAILS (snap cannot access /tmp)
xvfb-run -a drawio -x -f png -o /tmp/diagram.png /tmp/input.drawio

# ✅ WORKS (home directory accessible)
cd ~/diagrams
xvfb-run -a drawio -x -f png -o diagram.png input.drawio
```

**Snap-accessible paths:**
- `~/` (home directory)
- `/home/<user>/`
- `/media/` (removable media)
- `/mnt/` (mounted filesystems)

### 2. OpenGL/dbus Warnings

**Symptoms:** Errors like:
```
libGL error: No matching fbConfigs or visuals found
dbus[]: Failed to connect to socket
```

**Impact:** These are **warnings only** — export still succeeds. Safe to ignore in headless environments.

**Suppress (optional):**
```bash
xvfb-run -a drawio -x -f png -o output.png input.drawio 2>/dev/null
```

### 3. Missing Xvfb

**Symptom:**
```
Error: Cannot open display: :99
```

**Fix:**
```bash
sudo apt-get install -y xvfb
```

### 4. Large Diagrams (Memory)

**Problem:** Complex diagrams with many elements may consume significant memory.

**Solution:** Monitor memory usage, increase if needed:
```bash
# Check available memory before export
free -h

# For very large diagrams, consider SVG (vector, smaller memory footprint)
xvfb-run -a drawio -x -f svg -o output.svg input.drawio
```

### 5. Premature Deletion (CRITICAL)

**Problem:** Deleting diagram files immediately after generation but before user confirms receipt.

**Symptom:** User reports "diagram not received" but files already deleted.

**Root cause:** Telegram/messaging platforms may have delivery lag. Deleting before send confirmation = data loss.

**Solution:**
```bash
# ❌ WRONG — Delete immediately after MEDIA: path returned
xvfb-run -a drawio -x -f png -o diagram.png diagram.drawio
echo "MEDIA:/path/to/diagram.png"
rm diagram.png diagram.drawio  # TOO EARLY!

# ✅ CORRECT — Keep files, cleanup weekly
xvfb-run -a drawio -x -f png -o ~/diagrams/analysis_$(date +%Y%m%d).png diagram.drawio
echo "MEDIA:~/diagrams/analysis_20260505.png"
# Files remain for user reference

# Weekly cleanup (manual or cron)
find ~/diagrams -name "*.png" -mtime +7 -delete
```

**Policy:** Never auto-delete diagrams after sending. User may need to reference them later or delivery may fail silently.

## Diagram Types Supported

- **Architecture diagrams** (microservices, cloud, infrastructure)
- **Flowcharts** (process flows, decision trees)
- **Sequence diagrams** (API calls, interactions)
- **Network diagrams** (topology, connections)
- **ER diagrams** (database schemas)
- **UML diagrams** (class, component, deployment)

## Example Workflow

### 1. Create .drawio XML

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Example">
    <mxGraphModel dx="1200" dy="900">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Add your diagram elements here -->
        <mxCell id="box1" value="Service A" 
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;" 
                vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 2. Export to PNG

```bash
xvfb-run -a drawio -x -f png -o diagram.png diagram.drawio
```

### 3. Verify Output

```bash
ls -lh diagram.png
file diagram.png
# Expected: PNG image data, ...
```

## Integration with Hermes

When generating diagrams in Hermes workflows:

1. **Create .drawio XML** programmatically (Python, script, template)
2. **Export via xvfb-run** in execute_code or terminal tool
3. **Return path** via `MEDIA:/path/to/diagram.png` for Telegram
4. **DO NOT auto-delete** — Keep diagrams for user reference (cleanup weekly, not per-send)

## Performance

**Typical export times:**
- Simple diagram (5-10 elements): 2-3 seconds
- Medium diagram (20-50 elements): 4-6 seconds
- Complex diagram (100+ elements): 8-12 seconds

**Memory usage:**
- draw.io process: ~100-200 MB during export
- Xvfb overhead: ~10-20 MB

## Troubleshooting

### Export produces blank/empty PNG

**Cause:** Invalid XML structure or missing geometry.

**Fix:** Validate .drawio XML structure, ensure all cells have geometry.

### "Command not found: drawio"

**Cause:** Snap bin directory not in PATH.

**Fix:**
```bash
# Add to ~/.bashrc
export PATH="/snap/bin:$PATH"

# Or use full path
xvfb-run -a /snap/bin/drawio -x -f png -o output.png input.drawio
```

### Permission denied

**Cause:** Output directory not writable or snap confinement.

**Fix:** Use home directory or check permissions:
```bash
# Use home directory
cd ~/diagrams

# Or check permissions
ls -ld /path/to/output/directory
```

## References

- `references/system-services-diagram-pattern.md` — Pattern for mapping running services to comprehensive diagrams
- `references/electricity-consumption-analysis.md` — Household/office electricity analysis with AC-focused breakdown and savings scenarios

## See Also

- `architecture-diagram` skill — Dark-themed SVG architecture diagrams as HTML
- `excalidraw` skill — Hand-drawn style diagrams (JSON format)
- draw.io GitHub: https://github.com/jgraph/drawio-desktop
