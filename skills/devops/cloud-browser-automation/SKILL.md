---
name: cloud-browser-automation
description: Use cloud browser services (Browserbase) for Cloudflare bypass, JavaScript rendering, and stealth scraping when local tools fail
tags: [browserbase, cloudflare, scraping, automation, cloud]
related_skills: [web-scraping]
origin: unknown
source_license: see upstream
language: en
---

# Cloud Browser Automation

Use cloud browser services (Browserbase, Browser Use Cloud) for web scraping when local tools fail due to Cloudflare protection, JavaScript rendering requirements, or anti-bot measures.

## Usage Strategy

**CRITICAL: On-demand only, close immediately**

Always follow this pattern:
1. Create session ONLY when needed
2. Do the task (scrape/navigate/extract)
3. Close session IMMEDIATELY after done
4. Never leave sessions running idle

Why:
- Save credits (pay per minute)
- Avoid hitting concurrent session limits (e.g., Browserbase max 3)
- Clean resource usage
- No waste

## When to Use

**Escalation ladder** (always try cheapest/fastest first):

```
1. Try Hermes web_fetch first
   ↓ (if fails or empty content)
2. Try direct curl with proper headers (Pattern 0 — works for most static sites)
   ↓ (if blocked or needs JS)
3. Try Hermes browser
   ↓ (if blocked by Cloudflare or sandbox issues)
4. Use cloud browser (Browserbase)
```

**Use cloud browser when:**
- ✅ Cloudflare Turnstile blocking requests
- ✅ JavaScript-heavy sites (SPA, dynamic content)
- ✅ Anti-bot detection (fingerprinting, TLS checks)
- ✅ Complex multi-step automation (login, navigate, extract)

**DON'T use cloud browser when:**
- ❌ Simple HTTP requests (use web_fetch)
- ❌ Static content (use web_fetch)
- ❌ Cost-sensitive tasks (cloud = pay per minute)

## Browserbase Setup

### API Configuration

```bash
# Credentials (saved in memory)
API_KEY="bb_live_O6tVgdzl8B6WquBSj1XpuaC5hMc"
PROJECT_ID="a5008864-bbaa-4966-96e2-2272497b003d"
BASE_URL="https://www.browserbase.com/v1"

# Limits
MAX_CONCURRENT_SESSIONS=3
SESSION_TIMEOUT=5  # minutes (default)
```

### Session Management

**CRITICAL USER PREFERENCE:**

> "gini jadi lo pakai browserbase saat dibutuhkan aja, nah sesi langsung close saat beres"

**Translation:** Use on-demand only, close immediately after done.

**Why:**
- ✅ Save credits (pay per minute)
- ✅ Avoid hitting concurrent limit (max 3)
- ✅ Clean resource usage
- ✅ No waste

**Pattern:**
```python
# 1. Create session ONLY when needed
session = create_session()

# 2. Do the task
data = scrape_page(session)

# 3. Close IMMEDIATELY after done
close_session(session)
```

**DON'T:**
- ❌ Create session at start of script "just in case"
- ❌ Leave sessions running between tasks
- ❌ Reuse sessions across multiple unrelated tasks
- ❌ Forget to close sessions

## Workflow

### Step 1: Create Session

```bash
curl -X POST "https://www.browserbase.com/v1/sessions" \
  -H "X-BB-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "'$PROJECT_ID'",
    "browserSettings": {
      "viewport": {"width": 1920, "height": 1080}
    }
  }'
```

**Response:**
```json
{
  "id": "session-id-here",
  "status": "RUNNING",
  "connectUrl": "wss://connect-v2.usw2.browserbase.com/?signingKey=...",
  "seleniumRemoteUrl": "http://connect-v2.usw2.browserbase.com/webdriver",
  "expiresAt": "2026-05-03T13:00:00.000Z"
}
```

### Step 2: Automate (Requires SDK)

**Option A: Playwright** (Python)
```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp(connect_url)
    page = await browser.new_page()
    await page.goto("https://example.com")
    data = await page.evaluate("() => document.body.innerText")
    await browser.close()
```

**Option B: Selenium** (Python)
```python
from selenium import webdriver

options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor=selenium_remote_url,
    options=options
)
driver.get("https://example.com")
data = driver.find_element(By.TAG_NAME, "body").text
driver.quit()
```

**Option C: Manual (Fallback)**
```bash
# Get debug URL
curl "https://www.browserbase.com/v1/sessions/$SESSION_ID/debug" \
  -H "X-BB-API-Key: $API_KEY"

# Open debug URL in browser
# Navigate manually
# Screenshot/extract data manually
```

### Step 3: Close Session

```bash
curl -X POST "https://www.browserbase.com/v1/sessions/$SESSION_ID/stop" \
  -H "X-BB-API-Key: $API_KEY"
```

**ALWAYS close, even if task fails:**
```python
try:
    data = scrape_with_browserbase()
finally:
    close_session()  # Always close!
```

## VPS Constraints

**Problem:** Ubuntu 24.04 strict package management blocks `pip install playwright/selenium`.

**Solutions:**

### Option 1: Use Docker (Recommended)
```bash
# Run Playwright in container
docker run -it mcr.microsoft.com/playwright/python:v1.40.0-jammy \
  python3 /tmp/scraper.py
```

**Pros:** Isolated, no pip conflicts
**Cons:** Need Docker (~500MB)

### Option 2: Manual Fallback
```bash
# Create session
SESSION_ID=$(curl -X POST ... | jq -r '.id')

# Get debug URL
DEBUG_URL=$(curl ... | jq -r '.debuggerFullscreenUrl')

# User opens URL manually
echo "Open: $DEBUG_URL"
echo "Navigate to target site"
echo "Screenshot and send to me"

# Close session
curl -X POST ".../sessions/$SESSION_ID/stop" ...
```

### Option 3: Delegate to Subagent
```python
# If automation blocked, delegate research
delegate_task(
    goal="Research [topic] via web search",
    toolsets=["web", "terminal"]
)
```

## Common Patterns

### Pattern 0: Direct Curl for Static Sites (No Browserbase)

**Challenge:** Site returns HTML but might have Cloudflare or anti-bot checks

**Solution:**
```bash
# Direct curl with proper headers (often bypasses basic protection)
curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.5" \
  -H "Connection: keep-alive" \
  -H "Upgrade-Insecure-Requests: 1" \
  "https://example.com" > /tmp/page.html

# If response is gzip-encoded, check file type first
file /tmp/page.html  # Should show "HTML document" not "gzip compressed"

# Extract data with grep/sed/python
grep -oP '<title>\K[^<]+' /tmp/page.html
```

**When to use:**
- ✅ Static HTML sites (marketing pages, landing pages)
- ✅ Sites with basic Cloudflare (not Turnstile)
- ✅ Public content (no login required)
- ✅ VPS without Docker/Playwright

**When to escalate:**
- ❌ Cloudflare Turnstile challenge appears
- ❌ JavaScript-heavy SPA (empty body in curl response)
- ❌ Login-required content

### Pattern 0b: TinyFish Browser for Cloudflare Bypass (Recommended)

**Challenge:** API returns Cloudflare challenge page, need full browser automation

**Solution:**
```python
import requests
import asyncio
import websockets
import json
import time

TINYFISH_API_KEY = "your-api-key"

async def fetch_via_tinyfish(url):
    # 1. Create browser session
    headers = {"X-API-Key": TINYFISH_API_KEY, "Content-Type": "application/json"}
    payload = {
        "url": url,
        "timeout_seconds": 300,
        "browser_profile": "stealth",
        "proxy_config": {"enabled": True, "type": "tetra", "country_code": "US"}
    }
    resp = requests.post("https://api.browser.tinyfish.ai", headers=headers, json=payload, timeout=60)
    
    info = resp.json()
    session_id = info["session_id"]
    base_url = info["base_url"].rstrip("/")
    
    # 2. Wait for Cloudflare bypass (CRITICAL: 30 attempts × 6 seconds)
    page_ws_url = None
    for attempt in range(30):  # Not 20!
        time.sleep(6)  # Not 5!
        try:
            pages_resp = requests.get(f"{base_url}/pages", timeout=20)
            pages = pages_resp.json()
            
            if pages:
                page = pages[0]
                title = page.get("title", "")
                url_check = page.get("url", "")
                
                # Check BOTH title AND url (not just title!)
                if "Just a moment" not in title and url in url_check:
                    page_ws_url = page.get("webSocketDebuggerUrl")
                    break
        except:
            pass
    
    if not page_ws_url:
        requests.delete(f"https://api.browser.tinyfish.ai/{session_id}", headers={"X-API-Key": TINYFISH_API_KEY})
        raise Exception("Failed to bypass Cloudflare after 30 attempts")
    
    # 3. Execute via CDP
    async with websockets.connect(page_ws_url, max_size=20_000_000) as ws:
        counter = 0
        
        async def send(method, params=None):
            nonlocal counter
            counter += 1
            msg_id = counter
            await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == msg_id:
                    return msg
        
        await send("Runtime.enable")
        
        result = await send("Runtime.evaluate", {
            "expression": """
                fetch('/api/endpoint')
                .then(r => r.json())
                .catch(e => ({error: String(e)}))
            """,
            "awaitPromise": True,
            "returnByValue": True
        })
        
        data = result.get("result", {}).get("result", {}).get("value")
    
    # 4. Close session immediately
    requests.delete(f"https://api.browser.tinyfish.ai/{session_id}", headers={"X-API-Key": TINYFISH_API_KEY})
    
    return data

# Usage
data = asyncio.run(fetch_via_tinyfish("https://example.com"))
```

**CRITICAL Cloudflare Bypass Settings:**
- **30 attempts** (not 20) — Cloudflare can take 2-3 minutes
- **6 second delay** (not 5) — Faster polling causes false negatives
- **Check both title AND url** — Title alone insufficient for SPA sites
- **max_size=20_000_000** for websocket — Large responses need bigger buffer

**When to use:**
- ✅ Cloudflare Turnstile v2 (most reliable bypass)
- ✅ JavaScript-heavy SPA (full browser context)
- ✅ Login-required content (can handle auth flows)
- ✅ Production monitoring (stable, proven)

**When to escalate to Browserbase:**
- ❌ Need persistent sessions (TinyFish auto-closes)
- ❌ Need screenshots/video recording
- ❌ Complex multi-page workflows (TinyFish better for single-page scrapes)

**Real-world example:** RPOW2Swap API monitoring (see `references/rpow2swap-cloudflare-bypass.md`)

**Pattern 0a: Analyzing Minified JS Bundles**

If curl returns a SPA with minified JavaScript, you can often extract API patterns without Browserbase. See `references/minified-js-analysis.md` for grep-based techniques to find:
- API endpoints and base URLs
- Data structures (orderbook, pricing, etc.)
- Authentication patterns (localStorage tokens, headers)
- WebSocket URLs

This works for most modern SPAs (React, Vue, Next.js) and costs zero resources vs Browserbase.

### Pattern 1: Twitter/X Scraping (No Browserbase)

**Challenge:** Need to read public tweet content

**Solution:**
```bash
# Direct curl scraping (faster + free)
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://x.com/USERNAME/status/TWEET_ID" > /tmp/tweet.html

# Extract JSON data
grep -o 'window.__INITIAL_STATE__={.*}' /tmp/tweet.html | \
  sed 's/window.__INITIAL_STATE__=//' > /tmp/tweet.json

# Parse with jq or Python
jq '.entities.tweets.entities' /tmp/tweet.json
```

**When to use:**
- ✅ Public tweets (no login required)
- ✅ Simple text/media extraction
- ✅ Cost-sensitive tasks

**When to escalate to Browserbase:**
- ❌ Rate limited (429 errors)
- ❌ Login-required content
- ❌ Need to interact (like, retweet, reply)

See `references/twitter-scraping-fallback.md` for full technique.

### Pattern 1: OpenSea NFT Scraping

**Challenge:** OpenSea blocks direct HTTP (403 Cloudflare)

**Solution:**
```python
# 1. Create session
session = create_browserbase_session()

# 2. Navigate with Playwright
page = await connect_to_session(session)
await page.goto("https://opensea.io/collection/xyz")
await page.wait_for_selector('[data-testid="floor-price"]')

# 3. Extract data
floor_price = await page.text_content('[data-testid="floor-price"]')
volume = await page.text_content('[data-testid="volume"]')

# 4. Close immediately
await browser.close()
close_browserbase_session(session)
```

### Pattern 2: Cloudflare-Protected Sites

**Challenge:** Site uses Cloudflare Turnstile

**Solution:**
```python
# Browserbase automatically solves Cloudflare challenges
# Just navigate normally, no special handling needed

page = await connect_to_session(session)
await page.goto("https://cloudflare-protected-site.com")
# Browserbase handles Turnstile automatically
await page.wait_for_load_state("networkidle")
content = await page.content()
```

### Pattern 3: JavaScript-Heavy SPAs

**Challenge:** Content loaded via JavaScript, web_fetch returns empty

**Solution:**
```python
# Wait for content to load
page = await connect_to_session(session)
await page.goto("https://spa-site.com")
await page.wait_for_selector('.content-loaded')  # Wait for JS
data = await page.evaluate("() => window.appData")
```

## Error Handling

### Rate Limit (429)

**Error:**
```json
{
  "statusCode": 429,
  "error": "Too Many Requests",
  "message": "You've exceeded your max concurrent sessions limit (limit 3, currently 3)"
}
```

**Solution:**
```bash
# List running sessions
curl "https://www.browserbase.com/v1/sessions" \
  -H "X-BB-API-Key: $API_KEY" \
  | jq '.[] | select(.status=="RUNNING") | .id'

# Close old sessions
for sid in $(list_running_sessions); do
  curl -X POST ".../sessions/$sid/stop" ...
done
```

### Session Expired

**Error:** Session expires after 5 minutes (default)

**Solution:**
- Create session right before use (not at script start)
- Use `keepAlive: true` for longer tasks
- Close and recreate if task takes > 5 min

### SDK Not Available (VPS)

**Error:** `pip install playwright` blocked by Ubuntu 24.04

**Solution:**
- Use Docker (Option 1)
- Use manual fallback (Option 2)
- Delegate to subagent with web search (Option 3)

## Cost Optimization

**Browserbase pricing:** Pay per minute of session time

**Optimization strategies:**

1. **Create session late**
   ```python
   # ❌ BAD: Create at start
   session = create_session()
   # ... 2 minutes of prep work ...
   scrape(session)  # Wasted 2 minutes!
   
   # ✅ GOOD: Create right before use
   # ... prep work ...
   session = create_session()
   scrape(session)  # No waste!
   close_session(session)
   ```

2. **Close immediately**
   ```python
   # ❌ BAD: Leave running
   session = create_session()
   scrape(session)
   # ... session still running ...
   
   # ✅ GOOD: Close ASAP
   session = create_session()
   scrape(session)
   close_session(session)  # Immediately!
   ```

3. **Batch operations**
   ```python
   # ❌ BAD: One session per page
   for url in urls:
       session = create_session()
       scrape(url, session)
       close_session(session)
   
   # ✅ GOOD: One session for all pages
   session = create_session()
   for url in urls:
       scrape(url, session)
   close_session(session)
   ```

4. **Use escalation ladder**
   ```python
   # Try cheap methods first
   try:
       data = web_fetch(url)  # Free, fast
   except CloudflareError:
       try:
           data = hermes_browser(url)  # Free, slower
       except SandboxError:
           session = create_browserbase_session()  # Paid, last resort
           data = scrape_with_browserbase(url, session)
           close_session(session)
   ```

## Pitfalls

### 1. Forgetting to Close Sessions

**Problem:** Sessions left running, hit rate limit, waste credits

**Solution:**
- Always use `try/finally` to ensure closure
- Close in error handlers
- Verify closure with API call

### 2. Creating Sessions Too Early

**Problem:** Session created at script start, expires before use

**Solution:**
- Create session right before scraping
- Not at script initialization

### 3. Not Checking Rate Limits

**Problem:** Hit 429 error, script fails

**Solution:**
- Check running sessions before creating new one
- Close old sessions if at limit
- Implement retry with exponential backoff

### 4. Using for Simple Tasks

**Problem:** Use Browserbase for static sites, waste money

**Solution:**
- Always try web_fetch first
- Only escalate to Browserbase when needed
- Follow escalation ladder

### 5. Not Handling SDK Unavailability

**Problem:** Assume Playwright/Selenium available, script fails on VPS

**Solution:**
- Check if SDK available before using
- Have fallback plan (Docker, manual, delegate)
- Document VPS constraints in skill

## Verification

After using Browserbase:

```bash
# Verify session closed
curl "https://www.browserbase.com/v1/sessions" \
  -H "X-BB-API-Key: $API_KEY" \
  | jq '.[] | select(.status=="RUNNING")'

# Should return empty or sessions you intentionally left running

# Check data extracted
cat /tmp/scraped_data.json
jq '.' /tmp/scraped_data.json  # Validate JSON

# Verify files cleaned
ls /tmp/browserbase* /tmp/scrape*
# Should be empty or cleaned up
```

## References

- Browserbase Docs: https://docs.browserbase.com
- Playwright Python: https://playwright.dev/python/
- Selenium Python: https://selenium-python.readthedocs.io/
- TinyFish Integration: `references/tinyfish-integration.md` (REST API, not MCP)
