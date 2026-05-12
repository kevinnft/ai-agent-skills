# Browserbase Cloud API Reference

**Service:** https://www.browserbase.com  
**Docs:** https://docs.browserbase.com  
**Status:** ✅ Working (tested May 2026)

## Overview

Browserbase provides cloud-hosted Chromium browsers with stealth mode, residential proxies, and live debugging. Better reliability than Browser Use Cloud (no 404 errors).

## Authentication

```bash
X-BB-API-Key: bb_live_...
```

API keys start with `bb_live_` (production) or `bb_test_` (development).

## Base URL

```
https://www.browserbase.com/v1
```

## Core Endpoints

### 1. Create Session

```bash
POST /v1/sessions
Content-Type: application/json
X-BB-API-Key: bb_live_...

{
  "projectId": "a5008864-bbaa-4966-96e2-2272497b003d",
  "keepAlive": true,
  "browserSettings": {
    "viewport": {
      "width": 1920,
      "height": 1080
    }
  }
}
```

**Response (201 Created):**
```json
{
  "id": "4b90c7ad-0c0b-4f7d-a4e3-18e21c1ba14b",
  "status": "RUNNING",
  "projectId": "a5008864-bbaa-4966-96e2-2272497b003d",
  "region": "us-west-2",
  "startedAt": "2026-05-03T12:53:37.151+00:00",
  "expiresAt": "2026-05-03T12:58:37.151+00:00",
  "connectUrl": "wss://connect-v2.usw2.browserbase.com/?signingKey=...",
  "seleniumRemoteUrl": "http://connect-v2.usw2.browserbase.com/webdriver"
}
```

**Note:** Status code **201** is SUCCESS, not error! (Common mistake: checking `!= 200`)

### 2. List Sessions

```bash
GET /v1/sessions
X-BB-API-Key: bb_live_...
```

**Response:**
```json
[
  {
    "id": "...",
    "status": "RUNNING",
    "startedAt": "...",
    "expiresAt": "..."
  }
]
```

### 3. Get Debug URL

```bash
GET /v1/sessions/{sessionId}/debug
X-BB-API-Key: bb_live_...
```

**Response:**
```json
{
  "debuggerFullscreenUrl": "https://www.browserbase.com/devtools-fullscreen/inspector.html?wss=..."
}
```

**Use case:** Open in browser for live debugging, manual navigation, screenshot.

### 4. Stop Session

```bash
POST /v1/sessions/{sessionId}/stop
X-BB-API-Key: bb_live_...
```

**Response:** 200 OK

## Automation (Requires SDK)

Browserbase sessions can be controlled via:

1. **Playwright** (Python/Node.js)
2. **Puppeteer** (Node.js)
3. **Selenium** (Python/Java/etc.)

### Playwright Example

```python
from playwright.async_api import async_playwright

CONNECT_URL = "wss://connect-v2.usw2.browserbase.com/?signingKey=..."

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp(CONNECT_URL)
    context = browser.contexts[0]
    page = await context.new_page()
    
    await page.goto("https://example.com")
    content = await page.content()
    
    await browser.close()
```

### Selenium Example

```python
from selenium import webdriver

SELENIUM_URL = "http://connect-v2.usw2.browserbase.com/webdriver"
SIGNING_KEY = "eyJhbG..."

options = webdriver.ChromeOptions()
options.add_argument(f"--browserbase-signing-key={SIGNING_KEY}")

driver = webdriver.Remote(
    command_executor=SELENIUM_URL,
    options=options
)

driver.get("https://example.com")
content = driver.page_source
driver.quit()
```

## VPS Constraints

**Problem:** Ubuntu 24.04 strict package management blocks `pip install playwright` and `pip install selenium`.

**Solutions:**

1. **Docker** (recommended for automation):
   ```bash
   docker run -it mcr.microsoft.com/playwright/python:v1.40.0-jammy \
     python3 /tmp/scraper.py
   ```

2. **Manual debugging** (no SDK needed):
   - Create session via REST API
   - Get debug URL
   - Open in browser manually
   - Navigate and screenshot

3. **Cloud API only** (no local automation):
   - Use REST API to create sessions
   - Sessions run in cloud
   - No local browser/SDK needed

## Rate Limits

**Free tier:** 3 concurrent sessions max

**Error when exceeded:**
```json
{
  "statusCode": 429,
  "error": "Too Many Requests",
  "message": "You've exceeded your max concurrent sessions limit (limit 3, currently 3)"
}
```

**Solution:** Stop old sessions before creating new ones.

## Session Lifecycle

1. **Create** → Status: `RUNNING`
2. **Use** → Browser active in cloud
3. **Expire** → Auto-stop after 5 minutes (default)
4. **Stop** → Manual termination

**keepAlive:** Set `true` to extend session lifetime (still has max duration).

## Comparison: Browser Use vs Browserbase

| Feature | Browser Use Cloud | Browserbase |
|---------|-------------------|-------------|
| **API reliability** | ❌ 404 errors (May 2026) | ✅ Working |
| **Endpoint structure** | Confusing (v1/v2/v3) | Clear (/v1/) |
| **Status codes** | Inconsistent | Standard (201 = created) |
| **Debug UI** | Unknown | ✅ Live browser view |
| **SDK support** | Python only | Playwright/Puppeteer/Selenium |
| **Free tier** | Unknown | 3 concurrent sessions |
| **Documentation** | Scattered | Clear |

**Recommendation:** Use Browserbase for production scraping.

## Troubleshooting

### 404 Not Found

**Cause:** Wrong endpoint or API key.

**Check:**
- Base URL: `https://www.browserbase.com/v1` (not `/api/v1/`)
- Header: `X-BB-API-Key` (not `Authorization: Bearer`)
- API key format: `bb_live_...` or `bb_test_...`

### 429 Too Many Requests

**Cause:** Exceeded concurrent session limit.

**Solution:**
```bash
# List running sessions
curl -s "https://www.browserbase.com/v1/sessions" \
  -H "X-BB-API-Key: bb_live_..." | jq '.[] | select(.status=="RUNNING") | .id'

# Stop each session
curl -X POST "https://www.browserbase.com/v1/sessions/{sessionId}/stop" \
  -H "X-BB-API-Key: bb_live_..."
```

### Session Expired

**Cause:** Sessions expire after 5 minutes by default.

**Solution:**
- Set `keepAlive: true` when creating
- Create new session if expired
- Use session immediately after creation

### SDK Installation Blocked (Ubuntu 24.04)

**Cause:** `pip install` blocked by system package manager.

**Solutions:**
1. Use Docker (isolated environment)
2. Use manual debugging (no SDK needed)
3. Use REST API only (no automation)

## Example: Full Scraping Workflow

```python
import requests
import json

API_KEY = "bb_live_..."
PROJECT_ID = "a5008864-bbaa-4966-96e2-2272497b003d"

# 1. Create session
response = requests.post(
    "https://www.browserbase.com/v1/sessions",
    headers={"X-BB-API-Key": API_KEY, "Content-Type": "application/json"},
    json={"projectId": PROJECT_ID, "keepAlive": True}
)

if response.status_code != 201:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit(1)

session = response.json()
session_id = session["id"]
print(f"Session created: {session_id}")

# 2. Get debug URL
response = requests.get(
    f"https://www.browserbase.com/v1/sessions/{session_id}/debug",
    headers={"X-BB-API-Key": API_KEY}
)

debug_url = response.json()["debuggerFullscreenUrl"]
print(f"Debug URL: {debug_url}")

# 3. Manual step: Open debug URL, navigate, screenshot

# 4. Stop session when done
requests.post(
    f"https://www.browserbase.com/v1/sessions/{session_id}/stop",
    headers={"X-BB-API-Key": API_KEY}
)
print("Session stopped")
```

## Key Learnings (May 2026 Session)

1. **Status code 201 = SUCCESS** (not error!)
   - Common mistake: checking `response.status_code != 200`
   - Correct: check `response.status_code >= 400` for errors

2. **Rate limits enforced strictly**
   - Free tier: 3 concurrent sessions max
   - Must stop old sessions before creating new ones

3. **VPS pip restrictions**
   - Ubuntu 24.04 blocks `pip install` (system packages protected)
   - Docker is best solution for SDK automation
   - Manual debugging works without SDK

4. **Browserbase > Browser Use**
   - More reliable (no 404 errors)
   - Better documentation
   - Clearer API structure

## References

- Official docs: https://docs.browserbase.com
- GitHub examples: https://github.com/browserbase/examples
- Playwright docs: https://playwright.dev
- Selenium docs: https://www.selenium.dev
