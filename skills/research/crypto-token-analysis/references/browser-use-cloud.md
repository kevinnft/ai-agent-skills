# Browser Use Cloud — AI-Powered Browser Automation

**Use when:** Need to scrape Cloudflare-protected sites (OpenSea, DeFiLlama, etc.) on resource-constrained VPS.

## Why Browser Use > Scrapling

| Feature | Scrapling | Browser Use Cloud |
|---------|-----------|-------------------|
| **Cloudflare bypass** | ✅ StealthyFetcher | ✅ Stealth browser |
| **Setup** | 650-900 MB install | ❌ API call only |
| **RAM usage** | 200-400 MB/session | ❌ 0 MB (cloud) |
| **Disk usage** | 650-900 MB | ❌ 0 MB (cloud) |
| **Maintenance** | Self-hosted | ✅ Managed |
| **Proxies** | Manual setup | ✅ Built-in (195+ countries) |
| **Cost** | Free (self-host) | Pay per use |

**Verdict:** Browser Use Cloud = **PERFECT** for VPS with 2GB RAM or less.

## API v3 Endpoints

**Base URL:** `https://api.browser-use.com`

**Authentication:** `X-Browser-Use-API-Key: bu_...` header

### Create Session

```bash
curl -X POST "https://api.browser-use.com/v3/sessions" \
  -H "X-Browser-Use-API-Key: bu_..." \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://opensea.io/collection/numismatis/analytics",
    "task": "Extract floor price, volume (24h/7d/30d), holders, supply, recent sales. Return as JSON.",
    "model": "gpt-4o-mini",
    "max_steps": 15
  }'
```

**Response:**
```json
{
  "id": "session_abc123",
  "status": "running",
  "created_at": "2026-05-03T19:00:00Z"
}
```

### Get Session Result

```bash
curl -X GET "https://api.browser-use.com/v3/sessions/{session_id}" \
  -H "X-Browser-Use-API-Key: bu_..."
```

**Response (completed):**
```json
{
  "id": "session_abc123",
  "status": "completed",
  "result": {
    "floor_price": "0.0034 ETH",
    "volume_24h": "1.099 ETH",
    "holders": 285,
    ...
  },
  "recording_url": "https://...",
  "created_at": "2026-05-03T19:00:00Z",
  "completed_at": "2026-05-03T19:01:30Z"
}
```

**Status values:**
- `running`: Task in progress
- `completed`: Task finished successfully
- `failed`: Task failed (check error message)

### Poll Pattern

```python
import time
import requests

def wait_for_session(session_id, api_key, max_wait=120):
    """Poll session until completed or timeout"""
    start = time.time()
    while time.time() - start < max_wait:
        response = requests.get(
            f"https://api.browser-use.com/v3/sessions/{session_id}",
            headers={"X-Browser-Use-API-Key": api_key}
        )
        data = response.json()
        
        if data["status"] == "completed":
            return data["result"]
        elif data["status"] == "failed":
            raise Exception(f"Session failed: {data.get('error')}")
        
        time.sleep(5)  # Poll every 5 seconds
    
    raise TimeoutError("Session timeout")
```

## Self-Registration (No Human Required)

AI agents can create free accounts autonomously:

### Step 1: Request Challenge

```bash
curl -X POST "https://api.browser-use.com/cloud/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "ai-agent@temp.mail", "name": "AI Agent"}'
```

**Response:**
```json
{
  "challenge_id": "uuid",
  "challenge_text": "TwO tRaInS t#ReS . cIeNtO. * mIlEs..."
}
```

### Step 2: Solve Challenge with LLM

**IMPORTANT:** Use LLM reasoning, NOT deterministic code.

**Example challenge:**
```
"TwO tRaInS t#ReS . cIeNtO. * mIlEs ApArT..."
→ Clean: "Two trains tres ciento miles apart..."
→ Parse: "Two trains 300 miles apart at 23 mph and 34 mph, bird flies at 143 mph"
→ Solve: Bird distance = 143 * (300 / (23 + 34)) = 752.63 miles
```

**Answer format:** String with 2 decimal places (e.g., `"752.63"`)

### Step 3: Verify Challenge

```bash
curl -X POST "https://api.browser-use.com/cloud/signup/verify" \
  -H "Content-Type: application/json" \
  -d '{"challenge_id": "uuid", "answer": "752.63"}'
```

**Response (success):**
```json
{
  "api_key": "bu_x2E...n4nU"
}
```

**Response (failure):**
```json
{
  "detail": "Incorrect answer"
}
```

**Note:** Challenge expires after ~5 minutes. Request new one if expired.

## Common Pitfalls

### Pitfall 1: Wrong Endpoint

**Problem:** Using `/v3/agent/tasks` (doesn't exist)

**Solution:** Use `/v3/sessions`

### Pitfall 2: Ubuntu 24.04 pip Restrictions

**Problem:** `pip install browser-use-sdk` fails with "externally-managed-environment"

**Solution:** Use direct REST API calls (curl/requests), not SDK

### Pitfall 3: Challenge Expiration

**Problem:** Challenge expires before verification

**Solution:** Solve quickly (<5 min) or request new challenge

### Pitfall 4: Deterministic Challenge Solving

**Problem:** Using hardcoded formulas instead of LLM reasoning

**Solution:** Always use LLM to parse obfuscated text, then calculate

## Example: NFT Collection Scraping

```python
import requests
import time

API_KEY = "bu_..."
BASE_URL = "https://api.browser-use.com"

# Create session
response = requests.post(
    f"{BASE_URL}/v3/sessions",
    headers={
        "X-Browser-Use-API-Key": API_KEY,
        "Content-Type": "application/json"
    },
    json={
        "url": "https://opensea.io/collection/numismatis/analytics",
        "task": """
        Extract the following data:
        1. Current floor price (ETH and USD)
        2. 24h, 7d, 30d trading volume
        3. Total volume (all-time)
        4. Number of holders
        5. Total supply
        6. Recent sales (last 5-10 with prices)
        
        Return as structured JSON.
        """,
        "model": "gpt-4o-mini",
        "max_steps": 15
    }
)

session_id = response.json()["id"]
print(f"Session created: {session_id}")

# Poll for completion
while True:
    time.sleep(5)
    result = requests.get(
        f"{BASE_URL}/v3/sessions/{session_id}",
        headers={"X-Browser-Use-API-Key": API_KEY}
    ).json()
    
    if result["status"] == "completed":
        print("Data:", result["result"])
        break
    elif result["status"] == "failed":
        print("Failed:", result.get("error"))
        break
```

## Resources

- **Dashboard:** https://cloud.browser-use.com
- **API Keys:** https://cloud.browser-use.com/settings?tab=api-keys
- **Docs:** https://docs.browser-use.com
- **OpenAPI Spec:** https://docs.browser-use.com/cloud/openapi/v3.json
- **llms.txt:** https://docs.browser-use.com/cloud/llms.txt
