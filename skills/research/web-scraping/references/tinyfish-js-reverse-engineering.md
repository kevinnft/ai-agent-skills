# TinyFish Browser Automation for API Reverse Engineering

**Use case:** Extract API endpoints from Cloudflare-protected SPAs when direct curl/fetch fails.

**Tested:** rpow2swap.com (May 2026) — Cloudflare Turnstile v2 blocked all automated approaches except TinyFish browser automation.

## Workflow

### 1. TinyFish Browser Session (Cloudflare Bypass)

```python
import requests
import time

TINYFISH_API_KEY = "sk-tinyfish-..."
headers = {"X-API-Key": TINYFISH_API_KEY, "Content-Type": "application/json"}

# Create stealth browser session with proxy
payload = {
    "url": "https://target-site.com/",
    "timeout_seconds": 180,
    "browser_profile": "stealth",
    "proxy_config": {"enabled": True, "type": "tetra", "country_code": "US"}
}

resp = requests.post("https://api.browser.tinyfish.ai", headers=headers, json=payload, timeout=60)
session_info = resp.json()

session_id = session_info["session_id"]
base_url = session_info["base_url"].rstrip("/")

# Wait for Cloudflare challenge to complete
for attempt in range(20):
    time.sleep(5)
    pages_resp = requests.get(f"{base_url}/pages", timeout=20)
    pages = pages_resp.json()
    
    if pages:
        title = pages[0].get("title", "")
        if "Just a moment" not in title:
            page_ws_url = pages[0]["webSocketDebuggerUrl"]
            print(f"✅ Cloudflare bypassed! Title: {title}")
            break
```

**Key insight:** TinyFish's stealth profile + residential proxy (Tetra) bypasses Cloudflare Turnstile where Puppeteer stealth plugins fail.

### 2. Download JavaScript via CDP (Chrome DevTools Protocol)

```python
import asyncio
import websockets
import json

async def download_js(page_ws_url):
    async with websockets.connect(page_ws_url, max_size=20_000_000) as ws:
        counter = 0
        
        async def send(method, params=None):
            nonlocal counter
            counter += 1
            await ws.send(json.dumps({"id": counter, "method": method, "params": params or {}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == counter:
                    return msg
        
        await send("Runtime.enable")
        
        # Get script URLs from page
        result = await send("Runtime.evaluate", {
            "expression": """
                Array.from(document.querySelectorAll('script[src]'))
                    .map(s => s.src)
                    .filter(src => src.includes('target-site.com'))
            """,
            "returnByValue": True
        })
        
        script_urls = result["result"]["result"]["value"]
        
        # Fetch main JS bundle
        js_url = script_urls[0]  # Usually index-[hash].js or main-[hash].js
        fetch_result = await send("Runtime.evaluate", {
            "expression": f"fetch('{js_url}').then(r => r.text())",
            "awaitPromise": True,
            "returnByValue": True
        })
        
        js_content = fetch_result["result"]["result"]["value"]
        return js_content

js_code = asyncio.run(download_js(page_ws_url))
```

**Why CDP instead of curl:** Cloudflare blocks direct JS file downloads. CDP uses the already-authenticated browser session.

### 3. Extract API Endpoints from Minified JS

```bash
# Save JS to file
echo "$js_code" > /tmp/bundle.js

# Method 1: Grep for API paths
grep -oE 'api/[a-zA-Z0-9_/-]+' /tmp/bundle.js | sort -u

# Method 2: Search for specific function names
grep -B 5 -A 5 'withdraw' /tmp/bundle.js | head -50

# Method 3: Find all string literals (API endpoints often quoted)
grep -oP '"/[a-zA-Z0-9_/-]{3,}"' /tmp/bundle.js | sort -u
```

**rpow2swap.com results:**
```
api/listings
api/auth/connect
api/auth/verify
api/me
api/trades
api/withdraw
api/analytics/exchange
```

### 4. Analyze Function Definitions

```bash
# Find function that calls /api/withdraw
grep 'api/withdraw' /tmp/bundle.js

# Output (minified):
# JE=t=>Xn("api/withdraw",{method:"POST",body:{amount:t}})
```

**Decoded:**
- Function name: `JE` (minified)
- Endpoint: `POST /api/withdraw`
- Body: `{"amount": <number>}`
- Uses helper function `Xn` (likely axios/fetch wrapper with auth headers)

### 5. Find Authentication Flow

```bash
# Search for token storage
grep -i 'localstorage' /tmp/bundle.js | grep -i 'token'

# Output:
# localStorage.setItem("rpow2x_token",y.token)
# localStorage.getItem("rpow2x_token")
```

**Auth pattern discovered:**
1. User connects Solana wallet → gets wallet address
2. User enters email → backend sends verification code
3. User submits code → backend returns JWT token
4. Token stored in `localStorage` with key `rpow2x_token`
5. All API calls include `Authorization: Bearer <token>` header

### 6. Reconstruct API Call

```python
import requests

# Assuming you have a valid token (from login flow)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://rpow2swap.com/api/withdraw",
    headers=headers,
    json={"amount": 100000}
)

print(response.json())
```

## Cleanup

```python
# Always close TinyFish session to avoid charges
requests.delete(
    f"https://api.browser.tinyfish.ai/{session_id}",
    headers={"X-API-Key": TINYFISH_API_KEY},
    timeout=30
)
```

## Key Lessons

1. **Cloudflare Turnstile v2 is strong** — Puppeteer stealth plugins fail, TinyFish succeeds
2. **CDP > curl for JS downloads** — Cloudflare blocks direct file access
3. **Minified JS is readable** — grep for keywords, function names, and string literals
4. **Auth tokens are in localStorage** — check for `setItem`/`getItem` calls
5. **REST APIs follow patterns** — `/api/<resource>` is common, try common verbs (GET/POST/PUT/DELETE)

## Pitfalls

- **Don't retry failed Cloudflare bypasses** — each attempt costs TinyFish credits. If stealth profile fails, escalate to manual browser inspection.
- **Minified variable names change** — `JE` today might be `KF` tomorrow. Search by string literals (`"api/withdraw"`) not variable names.
- **JWT tokens expire** — tokens from reverse engineering are short-lived. Automate full auth flow if building a bot.
- **Rate limiting** — even with valid tokens, APIs may rate-limit. Add delays between requests.

## When NOT to Use This Approach

- **Public API exists** — check for official docs first
- **Terms of Service prohibit** — respect ToS, use for research/personal use only
- **Simple static site** — curl + grep is faster
- **No Cloudflare protection** — use Puppeteer directly, cheaper than TinyFish

## Cost Estimate (TinyFish)

- Browser session creation: ~$0.01
- Session duration: ~2 minutes for full workflow
- Total cost per reverse engineering session: ~$0.02-0.05

**Optimization:** Reuse session for multiple operations instead of creating new session per request.
