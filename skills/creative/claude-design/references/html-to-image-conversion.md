# HTML to Image Conversion — Tool Fallback Chain

## Problem

Need to convert HTML file to PNG/JPG image (e.g., for social media graphics, promotional materials).

## Tool Priority (Try in Order)

### 1. Chrome/Chromium Headless (Best Quality)

```bash
google-chrome --headless --disable-gpu \
  --screenshot=/path/to/output.png \
  --window-size=853,1280 \
  file:///path/to/input.html
```

**Pros:**
- Best rendering quality
- Full CSS3/JS support
- Accurate fonts and layout

**Cons:**
- Often not installed on servers
- Large dependency

**Check availability:**
```bash
which google-chrome || which chromium-browser
```

---

### 2. Playwright (Good Quality, Programmable)

```bash
# Install
pip install playwright
playwright install chromium

# Screenshot
playwright screenshot \
  --viewport-size=853,1280 \
  --full-page \
  file:///path/to/input.html \
  output.png
```

**Pros:**
- Good rendering quality
- Programmable (Python/Node.js)
- Cross-browser support

**Cons:**
- Need install browsers (~200MB)
- Slower than native Chrome

**Check availability:**
```bash
which playwright
```

---

### 3. wkhtmltoimage (Fallback, Acceptable Quality)

```bash
# Install
sudo apt-get install -y wkhtmltopdf

# Screenshot
wkhtmltoimage \
  --width 853 \
  --height 1280 \
  --quality 100 \
  file:///path/to/input.html \
  output.png
```

**Pros:**
- Easy to install (apt package)
- Fast
- Small footprint

**Cons:**
- Older WebKit engine
- Some CSS3 features not supported
- Font rendering less accurate

**Check availability:**
```bash
which wkhtmltoimage
```

---

### 4. Puppeteer (Node.js, Good Quality)

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 853, height: 1280 });
  await page.goto('file:///path/to/input.html');
  await page.screenshot({ path: 'output.png' });
  await browser.close();
})();
```

**Pros:**
- Excellent quality (Chrome engine)
- Full control via API
- Popular in Node.js ecosystem

**Cons:**
- Need Node.js + npm install
- Larger dependency

---

## Automated Fallback Script

```python
import subprocess
import os

def html_to_image(html_path, output_path, width=853, height=1280):
    """Convert HTML to image with automatic tool fallback."""
    
    # Try Chrome/Chromium
    for chrome in ['google-chrome', 'chromium-browser', 'chromium']:
        result = subprocess.run(['which', chrome], capture_output=True)
        if result.returncode == 0:
            print(f"Using {chrome}...")
            subprocess.run([
                chrome, '--headless', '--disable-gpu',
                f'--screenshot={output_path}',
                f'--window-size={width},{height}',
                f'file://{html_path}'
            ])
            if os.path.exists(output_path):
                return True
    
    # Try Playwright
    result = subprocess.run(['which', 'playwright'], capture_output=True)
    if result.returncode == 0:
        print("Using playwright...")
        subprocess.run([
            'playwright', 'screenshot',
            f'--viewport-size={width},{height}',
            '--full-page',
            f'file://{html_path}',
            output_path
        ])
        if os.path.exists(output_path):
            return True
    
    # Try wkhtmltoimage
    result = subprocess.run(['which', 'wkhtmltoimage'], capture_output=True)
    if result.returncode == 0:
        print("Using wkhtmltoimage...")
        subprocess.run([
            'wkhtmltoimage',
            '--width', str(width),
            '--height', str(height),
            '--quality', '100',
            f'file://{html_path}',
            output_path
        ])
        if os.path.exists(output_path):
            return True
    
    print("❌ No HTML-to-image tool available!")
    print("Install one of: google-chrome, playwright, wkhtmltopdf")
    return False

# Usage
html_to_image('/home/ubuntu/promo.html', '/home/ubuntu/promo.png')
```

---

## Common Issues

### Issue 1: File URL Not Working

**Problem:** `file:///path/to/file.html` not loading

**Solution:** Use absolute path
```bash
# Wrong
file://relative/path.html

# Right
file:///home/ubuntu/absolute/path.html
```

---

### Issue 2: Fonts Not Rendering

**Problem:** Custom fonts (Google Fonts, etc.) not showing

**Solution:** Ensure internet access or embed fonts
```html
<!-- Option 1: CDN (need internet) -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">

<!-- Option 2: Embed (offline) -->
<style>
@font-face {
  font-family: 'Poppins';
  src: url('data:font/woff2;base64,...');
}
</style>
```

---

### Issue 3: Transparent Background

**Problem:** Want transparent background, getting white

**Solution:** Set body background to transparent
```css
body {
  background: transparent;
}
```

Then use PNG format (not JPG).

---

### Issue 4: Image Too Large

**Problem:** Output file is 10MB+

**Solution:** Optimize with ImageMagick
```bash
# Install
sudo apt-get install imagemagick

# Optimize
convert input.png -quality 85 -strip output.png
```

---

## Quality Comparison

| Tool | Rendering | Speed | Size | Best For |
|------|-----------|-------|------|----------|
| Chrome | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Large | Production graphics |
| Playwright | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Large | Automated testing |
| wkhtmltoimage | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Small | Quick conversions |
| Puppeteer | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Large | Node.js projects |

---

## Recommendation

**For VPS/Server:**
1. Try wkhtmltoimage first (easy install, good enough)
2. If quality issues, install Playwright
3. If need best quality, install Chrome

**For Local Development:**
1. Use Chrome/Chromium (already installed)
2. Or Puppeteer if Node.js project

**For CI/CD:**
1. Use Playwright (Docker images available)
2. Or Chrome in Docker
