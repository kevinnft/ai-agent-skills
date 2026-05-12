# Headless GUI Apps in WSL2

Running GUI applications (draw.io, Electron apps, browser automation) in headless WSL2 requires a virtual display server.

## Problem

GUI apps fail with:
```
ERROR:ui/ozone/platform/x11/ozone_platform_x11.cc:250] Missing X server or $DISPLAY
ERROR:ui/aura/env.cc:257] The platform failed to initialize. Exiting.
```

## Solution: Xvfb (X Virtual Framebuffer)

Xvfb creates a virtual display that GUI apps can render to without a physical screen.

### Installation

```bash
sudo apt-get update
sudo apt-get install -y xvfb
```

### Usage

Wrap GUI commands with `xvfb-run`:

```bash
# Basic usage
xvfb-run -a <command>

# Example: draw.io export
xvfb-run -a drawio -x -f png -o output.png input.drawio

# Example: Electron app
xvfb-run -a electron-app --headless
```

**Flags:**
- `-a`: Auto-select display number (avoids conflicts)
- `-s`: Screen options (e.g., `-s "-screen 0 1920x1080x24"`)

### Common Issues

#### 1. OpenGL/GPU Errors

**Symptom:**
```
libGL error: MESA-LOADER: failed to open swrast
libGL error: failed to load driver: swrast
ERROR: ANGLE Display::initialize error 12289: Could not create a backing OpenGL context.
```

**Impact:** Usually harmless warnings. The app still works for headless export/automation.

**Fix (if needed):**
```bash
# Install software rendering
sudo apt-get install -y libgl1-mesa-dri
```

#### 2. Snap Confinement

**Symptom:** Snap-installed apps can't access `/tmp` or other directories.

**Fix:** Use home directory or explicitly allowed paths:
```bash
# ❌ Fails (snap can't access /tmp)
cd /tmp && xvfb-run -a drawio -x -f png -o test.png test.drawio

# ✅ Works (snap can access ~/)
cd ~ && xvfb-run -a drawio -x -f png -o test.png test.drawio
```

#### 3. DBus Errors

**Symptom:**
```
ERROR:dbus/bus.cc:408] Failed to connect to the bus
```

**Impact:** Usually harmless. Most headless operations don't need DBus.

**Fix (if needed):**
```bash
# Start a DBus session
eval $(dbus-launch --sh-syntax)
xvfb-run -a <command>
```

## Verification

Test Xvfb installation:

```bash
# Install a simple GUI app
sudo apt-get install -y x11-apps

# Test with xclock (should exit cleanly without display)
xvfb-run -a xclock -display :99 &
sleep 2
pkill xclock

# If no errors, Xvfb is working
```

## Real-World Example: draw.io

```bash
# 1. Install draw.io (snap)
sudo snap install drawio

# 2. Install Xvfb
sudo apt-get install -y xvfb

# 3. Create test diagram
cat > test.drawio << 'EOF'
<mxfile host="app.diagrams.net">
  <diagram name="Test">
    <mxGraphModel dx="800" dy="600">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="Hello" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
EOF

# 4. Export to PNG
xvfb-run -a drawio -x -f png -o test.png test.drawio

# 5. Verify
ls -lh test.png  # Should show ~2-5KB file
```

## When to Use

Use Xvfb for:
- ✅ Diagram generation (draw.io, PlantUML, Graphviz)
- ✅ Browser automation (Puppeteer, Playwright, Selenium)
- ✅ Screenshot tools
- ✅ Electron apps in headless mode
- ✅ PDF generation from HTML

Don't use for:
- ❌ Interactive GUI apps (use WSLg or X11 forwarding instead)
- ❌ Apps that need GPU acceleration (use native Windows or WSLg)
