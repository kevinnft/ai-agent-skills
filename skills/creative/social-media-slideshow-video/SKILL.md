---
name: social-media-slideshow-video
description: "PIL + ffmpeg slideshow videos: product reviews, promos, TikTok/Reels/Shorts."
origin: unknown
source_license: see upstream
language: en
---

# Social Media Slideshow Video Generator

## When to use

Use when users request: product review videos, promotional slideshow videos, TikTok/Reels/Shorts content from static images, photo-based video with text overlays, hijab/fashion/beauty review videos, unboxing recap videos, or any image-to-video social media content with designed slides.

## Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Imaging | Pillow (PIL) | Slide design, text rendering, image manipulation |
| Encoding | ffmpeg (CLI) | Frame sequence → MP4 encoding |
| Core | Python 3 | Orchestration |

No GPU, no moviepy, no heavy dependencies needed.

## Architecture: File-Based Frame Pipeline

**Critical: Do NOT store all frames as numpy arrays in memory.** A 15-second 1080×1920 video at 24fps = 360 frames × ~6MB each = 2.1GB RAM → OOM kill.

### Correct approach:
```
1. Render each SLIDE as a static PIL Image (5-10 slides in memory is fine)
2. For each slide, generate per-frame variations (fade, zoom) and SAVE AS PNG to tmpdir
3. Feed the PNG sequence to ffmpeg via -i pattern
4. Clean up temp files
```

### Why not pipe to ffmpeg stdin?
Piping raw RGB frames to ffmpeg stdin causes deadlocks and broken pipe errors in many environments. The file-based approach is robust and debuggable.

## Resolution Presets

| Platform | Resolution | Aspect | FPS |
|----------|-----------|--------|-----|
| TikTok / Reels / Shorts | 1080×1920 | 9:16 | 24 |
| YouTube landscape | 1920×1080 | 16:9 | 24-30 |
| Instagram square | 1080×1080 | 1:1 | 24 |
| Story/Status | 1080×1920 | 9:16 | 24 |

## Slide Types & Design Patterns

### 1. Title Slide
- Gradient background (soft, matching product color)
- Hero photo in rounded-rect or circular frame with colored border
- Product name + subtitle text centered below
- Tag/category text above photo

### 2. Detail/Review Slide
- Blurred photo as background (`GaussianBlur(radius=20)` + dark blend at 0.55)
- Photo at top with gradient fade mask at bottom edge
- Semi-transparent card overlay (`RGBA` with alpha ~220) with rounded corners
- Bullet points + rating text

### 3. Verdict/Score Slide
- Gradient background
- Circular photo with colored border
- Large score text (e.g., "9.5/10")
- Verdict text + CTA

## Key Techniques

### Gradient Background
```python
def gradient_bg(w, h, c1, c2):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        r = y / h
        for x in range(w):
            px[x, y] = (int(c1[0]*(1-r)+c2[0]*r), ...)
    return img
```

### Photo with Rounded/Circular Mask
```python
mask = Image.new("L", (size, size), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, size, size], radius=35, fill=255)
# or .ellipse([0, 0, size, size], fill=255) for circular
frame.paste(photo, (x, y), mask)
```

### Colored Border Around Photo
```python
bdr = 8
border_img = Image.new("RGB", (size+bdr*2, size+bdr*2), border_color)
border_mask = Image.new("L", border_img.size, 0)
ImageDraw.Draw(border_mask).rounded_rectangle([0,0,...], radius=40, fill=255)
frame.paste(border_img, (x-bdr, y-bdr), border_mask)
frame.paste(photo, (x, y), photo_mask)  # photo on top
```

### Semi-Transparent Card Overlay
```python
card = Image.new("RGBA", (cw, ch), (255, 248, 240, 220))
cmask = Image.new("L", (cw, ch), 0)
ImageDraw.Draw(cmask).rounded_rectangle([0,0,cw,ch], radius=25, fill=220)
frame_rgba = frame.convert("RGBA")
frame_rgba.paste(card, (x, y), cmask)
frame = frame_rgba.convert("RGB")
```

### Blurred Photo Background
```python
bg = prepare_photo(WIDTH, HEIGHT, zoom=1.5)
bg = bg.filter(ImageFilter.GaussianBlur(radius=20))
dark = Image.new("RGB", (WIDTH, HEIGHT), (40, 30, 30))
frame = Image.blend(bg, dark, 0.55)
```

### Gradient Fade Mask (photo fading to transparent at bottom)
```python
gmask = Image.new("L", (w, h), 255)
gd = ImageDraw.Draw(gmask)
for y in range(h - fade_height, h):
    alpha = int(255 * (1 - (y - (h - fade_height)) / fade_height))
    gd.rectangle([(0, y), (w, y)], fill=alpha)
frame.paste(photo, (0, 0), gmask)
```

### Fade Transitions Between Slides
```python
black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
if frame_idx < TRANSITION_FRAMES:
    alpha = frame_idx / TRANSITION_FRAMES
    out = Image.blend(black, slide_img, alpha)
elif frame_idx > total - TRANSITION_FRAMES:
    alpha = (total - frame_idx) / TRANSITION_FRAMES
    out = Image.blend(black, slide_img, alpha)
```

## ffmpeg Encoding Command

```python
cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(tmpdir, "frame_%05d.png"),
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "23",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    output_path,
]
subprocess.run(cmd, capture_output=True, text=True, timeout=300)
```

## Font Handling

```python
def get_font(size, bold=False):
    fp = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold \
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if os.path.exists(fp):
        return ImageFont.truetype(fp, size)
    return ImageFont.load_default()
```

Center text: `bbox = draw.textbbox((0,0), text, font=f); x = (WIDTH - (bbox[2]-bbox[0])) // 2`

## Typical Duration & Pacing

| Slide type | Duration | Transition |
|-----------|----------|------------|
| Title | 3-4s | 0.3s fade |
| Detail | 3-3.5s | 0.3s fade |
| Verdict | 3.5-4s | 0.3s fade |
| **Total** | 15-20s | — |

## Pitfalls

1. **OOM Kill**: Never accumulate all frames as numpy arrays. Use file-based pipeline.
2. **ffmpeg stdin pipe**: Deadlocks on long videos. Use PNG sequence input instead.
3. **pip on Ubuntu 24.04+**: Needs `--break-system-packages` flag.
4. **Emoji/Unicode in text**: DejaVu fonts don't render emoji. Use text descriptions or install emoji fonts.
5. **Color matching**: Extract dominant color from product photo to build cohesive palette.
6. **Text centering**: Always use `textbbox()` for accurate width measurement before centering.

## Verification

After generating, extract mid-slide frames to verify (not transition frames):
```bash
# Extract frame from middle of each slide (not transitions which are black)
ffmpeg -i output.mp4 -vf "select='eq(n\,36)+eq(n\,108)...'" -vsync vfr preview_%d.jpg
ffprobe -v quiet -print_format json -show_format -show_streams output.mp4
```
