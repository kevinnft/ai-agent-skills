# Browser Use Cloud API Reference

Browser Use Cloud is a managed browser automation service for bypassing anti-bot protections (Cloudflare Turnstile, bot detection) and scraping protected sites.

## Two Different Products

**1. Open-Source Library** (local, free)
- Install: `pip install browser-use`
- No API key needed
- Runs locally on your machine
- RAM: 200-400MB per browser session
- Disk: ~500MB (Chromium install)

**2. Cloud API** (managed, paid)
- API key required (starts with `bu_`)
- Get key: https://cloud.browser-use.com/settings?tab=api-keys&new=1
- Runs on Browser Use infrastructure
- No local resources needed

## Cloud API Usage (Correct)

### Endpoint
```
POST https://api.browser-use.com/api/v1/run-task
```

### Authentication
```python
headers = {
    "Authorization": f"Bearer {API_KEY}",  # NOT X-Browser-Use-API-Key!
    "Content-Type": "application/json"
}
```

### Request Payload
```python
{
    "task": "Go to example.com and extract prices",
    "llm_model": "gemini-3-flash",  # or "gpt-4.1-mini", "claude-sonnet-4.6"
    "max_agent_steps": 15,
    "enable_public_share": True  # Get shareable execution URL
}
```

### Response
```python
{
    "id": "task_abc123",
    "status": "running"  # or "finished", "failed", "stopped"
}
```

### Polling for Results
```python
GET https://api.browser-use.com/api/v1/task/{task_id}
```

Returns:
```python
{
    "id": "task_abc123",
    "status": "finished",
    "output": "Extracted data...",
    "steps": [...],
    "live_url": "https://...",  # Watch browser in real-time
    "public_share_url": "https://..."  # Share execution recording
}
```

## Common Errors

### 404 Not Found
**Cause:** Invalid API key or wrong endpoint
**Fix:** 
- Verify API key is valid (test at https://cloud.browser-use.com)
- Use correct endpoint: `/api/v1/run-task` (NOT `/v3/sessions`)
- Use `Bearer` auth (NOT `X-Browser-Use-API-Key` header)

### API Key Invalid
**Cause:** Key expired, revoked, or account suspended
**Fix:** Generate new key at https://cloud.browser-use.com/settings?tab=api-keys&new=1

## When to Use Cloud vs Open-Source

**Use Cloud API when:**
- Need Cloudflare bypass (Turnstile, challenges)
- VPS has limited RAM (< 2GB)
- Want zero local setup
- Need residential proxies

**Use Open-Source when:**
- No Cloudflare protection
- Have sufficient RAM (2GB+)
- Want full control
- Free tier sufficient

## Example: OpenSea Scraping

OpenSea uses Cloudflare protection → requires Cloud API or stealth browser.

```python
import requests
import time

API_KEY = "bu_..."
BASE_URL = "https://api.browser-use.com/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Create task
response = requests.post(
    f"{BASE_URL}/run-task",
    headers=HEADERS,
    json={
        "task": "Go to https://opensea.io/collection/xyz/analytics and extract floor price",
        "llm_model": "gemini-3-flash",
        "max_agent_steps": 10
    }
)

task_id = response.json()["id"]

# Poll for completion
while True:
    result = requests.get(f"{BASE_URL}/task/{task_id}", headers=HEADERS).json()
    if result["status"] in ["finished", "failed"]:
        print(result["output"])
        break
    time.sleep(5)
```

## Cost Estimation

- **gemini-3-flash:** ~$0.04 per task (10 steps)
- **gpt-4.1-mini:** ~$0.08 per task (10 steps)
- **claude-sonnet-4.6:** ~$0.20 per task (10 steps)

## References

- Official docs: https://docs.browser-use.com/cloud/quickstart
- GitHub examples: https://github.com/browser-use/browser-use/tree/main/examples/cloud
- API reference: https://docs.browser-use.com/cloud/api-reference
