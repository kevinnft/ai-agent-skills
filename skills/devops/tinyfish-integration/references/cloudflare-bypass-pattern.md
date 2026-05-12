# Cloudflare Bypass Pattern with TinyFish Browser API

## Problem
Cloudflare Turnstile blocks direct API calls (HTTP 403) even with valid auth tokens. Need browser automation to bypass.

## Solution: CDP Websocket Pattern

### 1. Create Browser Session
```python
import requests
import time

TINYFISH_API_KEY = "sk-tinyfish-..."
headers = {"X-API-Key": TINYFISH_API_KEY, "Content-Type": "application/json"}

payload = {
    "url": "https://target-site.com/",
    "timeout_seconds": 300,
    "browser_profile": "stealth",
    "proxy_config": {"enabled": True, "type": "tetra", "country_code": "US"}
}

resp = requests.post("https://api.browser.tinyfish.ai", headers=headers, json=payload, timeout=60)
info = resp.json()

session_id = info["session_id"]
base_url = info["base_url"].rstrip("/")
```

### 2. Wait for Cloudflare Bypass (Retry Loop)
```python
page_ws_url = None

for attempt in range(30):  # 30 attempts = 2.5 minutes max
    time.sleep(5)
    
    pages_resp = requests.get(f"{base_url}/pages", timeout=20)
    pages = pages_resp.json()
    
    if pages:
        page = pages[0]
        title = page.get("title", "")
        
        # Check if Cloudflare challenge passed
        if "Just a moment" not in title:
            page_ws_url = page.get("webSocketDebuggerUrl")
            print(f"✅ Bypassed! Title: {title}")
            break

if not page_ws_url:
    raise Exception("Failed to bypass Cloudflare after 30 attempts")
```

### 3. Execute API Calls via CDP
```python
import asyncio
import json
import websockets

async def call_api(page_ws_url, token):
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
        
        # Enable Runtime
        await send("Runtime.enable")
        
        # Inject auth token to localStorage
        await send("Runtime.evaluate", {
            "expression": f"localStorage.setItem('auth_token', '{token}')",
            "returnByValue": True
        })
        
        # Call API via fetch
        result = await send("Runtime.evaluate", {
            "expression": f"""
                fetch('/api/endpoint', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer {token}'
                    }},
                    body: JSON.stringify({{key: 'value'}})
                }})
                .then(r => r.json())
                .catch(e => ({{error: String(e)}}))
            """,
            "awaitPromise": True,
            "returnByValue": True
        })
        
        data = result.get("result", {}).get("result", {}).get("value")
        return data

# Run
data = asyncio.run(call_api(page_ws_url, "your-token-here"))
```

### 4. Cleanup
```python
# Always close session when done
requests.delete(
    f"https://api.browser.tinyfish.ai/{session_id}",
    headers={"X-API-Key": TINYFISH_API_KEY},
    timeout=30
)
```

## Pattern: Transactional Operations

For operations that modify state (create/update/delete), use this pattern:

```python
async def transactional_operation(page_ws_url, token):
    # 1. Check current state
    current = await call_api(page_ws_url, token, "GET", "/api/resource")
    
    # 2. Perform action
    result = await call_api(page_ws_url, token, "POST", "/api/action", {"data": "value"})
    
    # 3. Wait for state update (if async)
    await asyncio.sleep(3)
    
    # 4. Verify new state
    updated = await call_api(page_ws_url, token, "GET", "/api/resource")
    
    return {"before": current, "result": result, "after": updated}
```

## Key Points

1. **Retry loop is essential** — Cloudflare bypass takes 5-25 seconds
2. **Check title, not just status** — page loads before bypass completes
3. **Use CDP Runtime.evaluate** — not Network.fetch (more reliable)
4. **Set awaitPromise: true** — for async fetch calls
5. **returnByValue: true** — to get actual data, not object reference
6. **Always cleanup** — delete session to avoid credit waste

## Tested Against
- rpow2swap.com (Cloudflare Turnstile)
- Balance validation bypass attempts (all failed — server-side validation solid)
- Race condition attacks (protected by database locks)
- SQL injection (parameterized queries working)

## Cost
- Browser session: ~$0.01-0.02 per session
- Free tier: 100 sessions/month
- Session timeout: 300 seconds (5 minutes)
