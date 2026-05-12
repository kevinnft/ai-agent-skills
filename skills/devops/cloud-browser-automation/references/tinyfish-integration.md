# TinyFish Integration

TinyFish is a **REST API service** for cloud browser automation, NOT an MCP server. Don't confuse it with Browserbase.

## API Configuration

```bash
API_KEY="sk-tinyfish-4pSzJ2SfN47DF8y1trM9Uw3dshdtaaLJ"
BASE_URL="https://api.browser.tinyfish.ai"
```

## Session Creation

```python
import requests
import time

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "url": "https://target-site.com/",
    "timeout_seconds": 180,
    "browser_profile": "stealth",
    "proxy_config": {
        "enabled": True,
        "type": "tetra",
        "country_code": "US"
    }
}

resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)
info = resp.json()

session_id = info["session_id"]
base_url = info["base_url"].rstrip("/")
```

## Cloudflare Bypass Pattern

**CRITICAL:** TinyFish sessions start with Cloudflare challenge. Must wait for bypass before using.

```python
import time

page_ws_url = None
for attempt in range(20):
    time.sleep(5)
    pages_resp = requests.get(f"{base_url}/pages", timeout=20)
    pages = pages_resp.json()
    
    if pages:
        page = pages[0]
        title = page.get("title", "")
        if "Just a moment" not in title:
            page_ws_url = page.get("webSocketDebuggerUrl")
            print(f"✅ Bypassed! Title: {title}")
            break

if not page_ws_url:
    print("❌ Failed to bypass Cloudflare")
    # Clean up
    requests.delete(f"{BASE_URL}/{session_id}", headers={"X-API-Key": API_KEY})
    sys.exit(1)
```

**Why this works:**
- TinyFish automatically solves Cloudflare challenges
- Takes 5-30 seconds depending on challenge complexity
- Page title changes from "Just a moment..." to actual page title when done
- `webSocketDebuggerUrl` becomes available for CDP connection

## Chrome DevTools Protocol (CDP) Usage

Once bypassed, use CDP via WebSocket:

```python
import asyncio
import json
import websockets

async def execute_js(page_ws_url, js_code):
    async with websockets.connect(page_ws_url, max_size=20_000_000) as ws:
        counter = 0
        
        async def send(method, params=None):
            nonlocal counter
            counter += 1
            msg_id = counter
            await ws.send(json.dumps({
                "id": msg_id,
                "method": method,
                "params": params or {}
            }))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == msg_id:
                    return msg
        
        # Enable Runtime
        await send("Runtime.enable")
        
        # Execute JavaScript
        result = await send("Runtime.evaluate", {
            "expression": js_code,
            "awaitPromise": True,
            "returnByValue": True
        })
        
        return result.get("result", {}).get("result", {}).get("value")

# Example: Fetch API data
data = asyncio.run(execute_js(page_ws_url, """
    fetch('/api/listings?type=sell')
        .then(r => r.json())
        .catch(e => ({error: String(e)}))
"""))
```

## Session Cleanup

**ALWAYS close sessions:**

```python
try:
    # Do work
    data = scrape_with_tinyfish(session_id, base_url)
finally:
    # Always close
    requests.delete(
        f"{BASE_URL}/{session_id}",
        headers={"X-API-Key": API_KEY},
        timeout=30
    )
```

## Common Pitfalls

### 1. Treating TinyFish as MCP Server

**WRONG:**
```bash
# This is for Browserbase, NOT TinyFish
npx -y install-mcp@latest https://agent.tinyfish.ai/mcp --client hermes
```

**RIGHT:**
```python
# TinyFish is REST API + CDP
import requests
resp = requests.post("https://api.browser.tinyfish.ai", ...)
```

### 2. Not Waiting for Cloudflare Bypass

**WRONG:**
```python
# Immediate CDP connection fails
resp = requests.post(BASE_URL, ...)
ws_url = resp.json()["pages"][0]["webSocketDebuggerUrl"]  # ❌ Not ready yet
```

**RIGHT:**
```python
# Wait for bypass first
for attempt in range(20):
    time.sleep(5)
    pages = requests.get(f"{base_url}/pages").json()
    if pages and "Just a moment" not in pages[0]["title"]:
        ws_url = pages[0]["webSocketDebuggerUrl"]  # ✅ Ready
        break
```

### 3. Forgetting to Close Sessions

**WRONG:**
```python
session = create_tinyfish_session()
data = scrape(session)
# Session left running ❌
```

**RIGHT:**
```python
session = create_tinyfish_session()
try:
    data = scrape(session)
finally:
    close_tinyfish_session(session)  # ✅ Always close
```

## When to Use TinyFish vs Browserbase

**Use TinyFish when:**
- ✅ Need Cloudflare bypass
- ✅ JavaScript-heavy sites
- ✅ API calls behind Cloudflare protection
- ✅ User already has TinyFish API key

**Use Browserbase when:**
- ✅ Need Playwright/Selenium SDK
- ✅ Complex multi-step automation
- ✅ Screenshot/PDF generation
- ✅ User already has Browserbase account

**Both solve same problem, different APIs.**

## Real-World Example: RPOW2Swap API

```python
#!/usr/bin/env python3
import requests
import asyncio
import json
import websockets

TINYFISH_API_KEY = "sk-tinyfish-..."
TARGET_URL = "https://rpow2swap.com/"

async def fetch_listings(page_ws_url):
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
                fetch('/api/listings?type=sell')
                    .then(r => r.json())
                    .catch(e => ({error: String(e)}))
            """,
            "awaitPromise": True,
            "returnByValue": True
        })
        
        return result.get("result", {}).get("result", {}).get("value")

def main():
    headers = {"X-API-Key": TINYFISH_API_KEY, "Content-Type": "application/json"}
    
    # Create session
    payload = {
        "url": TARGET_URL,
        "timeout_seconds": 180,
        "browser_profile": "stealth",
        "proxy_config": {"enabled": True, "type": "tetra", "country_code": "US"}
    }
    resp = requests.post("https://api.browser.tinyfish.ai", headers=headers, json=payload, timeout=60)
    info = resp.json()
    
    session_id = info["session_id"]
    base_url = info["base_url"].rstrip("/")
    
    # Wait for Cloudflare bypass
    page_ws_url = None
    for attempt in range(20):
        time.sleep(5)
        pages = requests.get(f"{base_url}/pages", timeout=20).json()
        if pages and "Just a moment" not in pages[0].get("title", ""):
            page_ws_url = pages[0]["webSocketDebuggerUrl"]
            break
    
    if not page_ws_url:
        print("❌ Cloudflare bypass failed")
        requests.delete(f"https://api.browser.tinyfish.ai/{session_id}", headers={"X-API-Key": TINYFISH_API_KEY})
        return
    
    try:
        # Fetch data
        listings = asyncio.run(fetch_listings(page_ws_url))
        print(json.dumps(listings, indent=2))
    finally:
        # Always close
        requests.delete(f"https://api.browser.tinyfish.ai/{session_id}", headers={"X-API-Key": TINYFISH_API_KEY})

if __name__ == "__main__":
    main()
```

## Setup Instructions

When user asks to "setup TinyFish":

1. **Ask for API key** (or check memory)
2. **Write Python script** using pattern above
3. **NO MCP commands** — TinyFish is not MCP

**DON'T say:**
```bash
hermes mcp add tinyfish ...
npx install-mcp ...
```

**DO say:**
```python
# Here's a Python script to use TinyFish API
import requests
...
```
