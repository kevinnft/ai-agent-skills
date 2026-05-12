# VPS Resource Visualization Pattern

**Context:** Generate visual diagrams for VPS resource usage (RAM, disk, processes, system stats)  
**Session:** 2026-05-05  
**Output:** Dark-themed draw.io diagram exported to PNG

---

## Use Case

User asks: "Buat diagram" (make a diagram) after resource analysis.

**When to use:**
- After VPS resource audit
- After cleanup operations
- When presenting system status
- For documentation/reports

---

## Pattern: Resource Usage Diagram

### Components

1. **Title bar** — VPS specs (CPU, RAM, disk)
2. **RAM usage bar** — Segmented by process/category
3. **Disk usage bar** — Used vs. free
4. **Top processes list** — Memory consumers with values
5. **System stats grid** — Uptime, load, swap, status
6. **Legend** — Color coding explanation
7. **Footer** — Timestamp, status, key metrics

### Visual Design

**Color scheme (dark theme):**
- Background: `#1a1a1a` (dark gray)
- Hermes Gateway: `#1976d2` (blue)
- enowxai Proxy: `#388e3c` (green)
- System Services: `#f57c00` (orange)
- Buff/Cache: `#455a64` (gray, reclaimable)
- Free space: `#37474f` (dark gray)
- Status OK: `#1b5e20` (dark green)
- Status warning: `#d32f2f` (red)
- Text: `#ffffff` (white)
- Labels: `#4fc3f7` (cyan)

**Layout:**
- Width: 1200px
- Height: 800px
- Grid: 10px
- Margins: 50px

### Data Mapping

**RAM bar (proportional):**
```
Total width: 1100px
Each segment width = (value / total) * 1100

Example (1.9GB total):
- Hermes 250MB = (250/1900) * 1100 = 145px
- enowxai 195MB = (195/1900) * 1100 = 113px
- System 200MB = (200/1900) * 1100 = 116px
- Cache 1200MB = (1200/1900) * 1100 = 695px
- Free 119MB = (119/1900) * 1100 = 69px
```

**Disk bar (proportional):**
```
Total width: 1100px
Used 16GB / 40GB = (16/40) * 1100 = 440px
Free 22GB / 40GB = (22/40) * 1100 = 605px
```

---

## Implementation

### Step 1: Collect Data

```bash
# RAM
free -h

# Disk
df -h /

# Top processes
ps aux --sort=-%mem | head -10

# System stats
uptime
cat /proc/loadavg
```

### Step 2: Generate draw.io XML

**Template structure:**
```xml
<mxfile host="app.diagrams.net">
  <diagram name="VPS Resource Usage">
    <mxGraphModel dx="1400" dy="900" background="#1a1a1a">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Title -->
        <mxCell id="title" value="VPS Resource Usage — X vCPU / XGB RAM / XGB Disk"
                style="text;fontSize=20;fontColor=#ffffff;"/>
        
        <!-- RAM Section -->
        <mxCell id="ram-title" value="RAM Usage (XGB Total)"
                style="text;fontSize=16;fontColor=#4fc3f7;"/>
        
        <!-- RAM Bar Background -->
        <mxCell id="ram-bar-bg" 
                style="fillColor=#263238;strokeColor=#546e7a;"
                geometry="x=50 y=140 width=1100 height=60"/>
        
        <!-- RAM Segments (proportional) -->
        <mxCell id="ram-hermes" value="Hermes Gateway\nXMB (X%)"
                style="fillColor=#1976d2;fontColor=#ffffff;"
                geometry="x=50 y=140 width=[calculated] height=60"/>
        
        <!-- ... more segments ... -->
        
        <!-- Disk Section -->
        <!-- ... similar structure ... -->
        
        <!-- Top Processes -->
        <!-- ... list with values ... -->
        
        <!-- System Stats Grid -->
        <!-- ... stat boxes ... -->
        
        <!-- Legend -->
        <!-- ... color boxes + labels ... -->
        
        <!-- Footer -->
        <mxCell id="footer" value="Generated: YYYY-MM-DD HH:MM UTC | Status: ✅ HEALTHY | Available RAM: XGB (X%)"
                style="text;fontSize=11;fontColor=#546e7a;"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Step 3: Export to PNG

```bash
# Copy to home directory (snap confinement)
cp /tmp/diagram.drawio ~/diagram.drawio

# Export with xvfb-run
cd ~
xvfb-run -a drawio -x -f png -o diagram.png diagram.drawio 2>&1 | tail -5

# Verify
ls -lh ~/diagram.png
file ~/diagram.png

# Copy to image cache for delivery
cp ~/diagram.png ~/.hermes/image_cache/diagram_$(date +%Y%m%d_%H%M%S).png
```

### Step 4: Deliver

```
MEDIA:/home/ubuntu/.hermes/image_cache/diagram_YYYYMMDD_HHMMSS.png
```

---

## Pitfalls

### 1. Snap Confinement

**Problem:** draw.io snap cannot access `/tmp/`

**Solution:** Always work in home directory
```bash
# ❌ FAILS
xvfb-run -a drawio -x -f png -o /tmp/diagram.png /tmp/input.drawio

# ✅ WORKS
cd ~
xvfb-run -a drawio -x -f png -o diagram.png input.drawio
```

### 2. OpenGL Warnings

**Symptoms:** Errors like:
```
ERROR:ui/gl/gl_display.cc:680] eglInitialize OpenGL failed
ERROR:components/viz/service/main/viz_main_impl.cc:184] Exiting GPU process
```

**Impact:** These are warnings only — export still succeeds

**Solution:** Ignore or suppress:
```bash
xvfb-run -a drawio -x -f png -o output.png input.drawio 2>&1 | tail -5
```

### 3. Proportional Width Calculation

**Problem:** Manual calculation error causes misaligned bars

**Solution:** Use Python for precision:
```python
total_width = 1100
total_ram = 1900  # MB

segments = {
    'hermes': 250,
    'enowxai': 195,
    'system': 200,
    'cache': 1200,
    'free': 119
}

x = 50  # Start position
for name, value in segments.items():
    width = int((value / total_ram) * total_width)
    print(f"{name}: x={x} width={width}")
    x += width
```

### 4. Text Overflow

**Problem:** Long labels overflow box boundaries

**Solution:**
- Use `\n` for line breaks
- Truncate long values
- Adjust font size if needed

---

## Example Output

**2026-05-05 VPS Resource Diagram:**
- File size: 85KB
- Resolution: 1104x742
- Format: PNG
- Components:
  - RAM bar (5 segments)
  - Disk bar (2 segments)
  - Top 4 processes
  - 6 stat boxes
  - Legend (3 colors)
  - Footer with timestamp

**Key metrics displayed:**
- RAM: 775MB used, 1.1GB available (58%)
- Disk: 16GB used, 22GB free (57%)
- Load: 0.04 (idle)
- Status: ✅ HEALTHY

---

## Variations

### Minimal (RAM only)
- Title + RAM bar + footer
- Quick status check

### Standard (RAM + Disk)
- Title + RAM bar + Disk bar + footer
- Most common use case

### Full (All components)
- Title + RAM + Disk + Processes + Stats + Legend + Footer
- Comprehensive report

### Time-series (Multiple snapshots)
- Before/after comparison
- Trend visualization
- Requires multiple diagrams

---

## References

- Session: 2026-05-05 05:35-05:38 UTC
- User: ryzen (VPS: 2 vCPU, 2GB RAM, 40GB disk)
- Output: `~/.hermes/image_cache/vps_resources_20260505_053807.png`
- Source: `~/vps_resources.drawio`
