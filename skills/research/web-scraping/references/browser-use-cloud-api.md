# Browser Use Cloud API — Troubleshooting Guide

**Last Updated:** May 3, 2026  
**API Version:** v3 (current), v1 (examples), v2 (legacy)

## Overview

Browser Use Cloud is a managed API for AI browser automation with stealth browsers, CAPTCHA solving, and residential proxies. However, there's confusion between the **open-source library examples** (which use `/api/v1/`) and the **actual Cloud API** (which uses `/v3/`).

## API Versions & Endpoints

### Open-Source Library Examples (GitHub)
```
Base URL: https://api.browser-use.com/api/v1
Auth: Authorization: Bearer {API_KEY}
Endpoint: POST /api/v1/run-task

Example: examples/cloud/01_basic_task.py
```

### Cloud API v3 (Actual API)
```
Base URL: https://api.browser-use.com
Auth: X-Browser-Use-API-Key: {API_KEY}
Endpoint: POST /v3/sessions

Docs: https://docs.browser-use.com/cloud/openapi/v3.json
```

### Cloud API v2 (Legacy)
```
Status: Deprecated, do not use for new projects
```

## Common Issues

### Issue 1: 404 Not Found on All Endpoints

**Symptoms:**
```bash
curl -X POST "https://api.browser-use.com/api/v1/run-task" \
  -H "Authorization: Bearer bu_..." \
  -d '{"task": "...", "llm_model": "gemini-3-flash"}'

# Returns: {"detail":"Not Found"}
```

**Possible causes:**
1. **API key invalid/expired** — Most common cause
2. **Account not activated** — New keys may need verification
3. **Service down** — Check https://cloud.browser-use.com/status
4. **Wrong endpoint** — Examples use `/api/v1/`, actual API uses `/v3/`
5. **Payment method required** — Some accounts need payment setup

**Troubleshooting steps:**
```bash
# 1. Test account endpoint
curl "https://api.browser-use.com/api/v1/account" \
  -H "Authorization: Bearer bu_..."

# 2. Try v3 endpoint with different auth
curl -X POST "https://api.browser-use.com/v3/sessions" \
  -H "X-Browser-Use-API-Key: bu_..." \
  -d '{"task": "...", "model": "gemini-3-flash"}'

# 3. Check dashboard
# Go to: https://cloud.browser-use.com/settings
# Verify: Account status, API key status, payment method

# 4. Generate new API key
# URL: https://cloud.browser-use.com/settings?tab=api-keys&new=1
```

### Issue 2: Confusion Between Library and Cloud API

**Problem:** GitHub examples show `/api/v1/` but docs say use `/v3/`

**Explanation:**
- **Open-source library** (`pip install browser-use`) — Self-hosted, no API key needed
- **Cloud API** — Managed service, requires API key, different endpoints

**When to use which:**
- Use **open-source** if: Need custom tools, deep integration, self-host
- Use **Cloud API** if: Want managed service, stealth browsers, easy scaling

### Issue 3: API Key Format

**Valid format:**
```
bu_PostDDJEga4nfhtZQcTNoIonYSFQ063RCeJV8CYVnr4
bu_osZYjCKF6-D2FUXUVilNMD8om5qBeKlkJ2eg7jSI1sg

Pattern: bu_[A-Za-z0-9_-]{40,50}
```

**Invalid:**
- Keys not starting with `bu_`
- Keys with special chars (except `-` and `_`)
- Expired or revoked keys

## Working Example (Open-Source Library)

```python
#!/usr/bin/env python3
import requests
import json
import time

API_KEY = "bu_..."
BASE_URL = "https://api.browser-use.com/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_task(instructions):
    payload = {
        "task": instructions,
        "llm_model": "gemini-3-flash",  # Fast and cheap
        "max_agent_steps": 15,
        "enable_public_share": True
    }
    
    response = requests.post(
        f"{BASE_URL}/run-task",
        headers=HEADERS,
        json=payload,
        timeout=30
    )
    
    return response.json()

def get_task_details(task_id):
    response = requests.get(
        f"{BASE_URL}/task/{task_id}",
        headers=HEADERS,
        timeout=30
    )
    
    return response.json()

def wait_for_completion(task_id, poll_interval=5):
    while True:
        details = get_task_details(task_id)
        status = details.get("status")
        
        if status == "finished":
            return details
        elif status in ["failed", "stopped"]:
            return details
        
        time.sleep(poll_interval)

# Usage
task = create_task("Go to google.com and tell me the page title")
result = wait_for_completion(task["id"])
print(result["output"])
```

## Alternative: Use Open-Source Library Locally

If Cloud API has issues, use the open-source library:

```bash
# Install
pip install browser-use

# No API key needed, runs locally
python3 scraper.py
```

**Pros:**
- ✅ FREE (no API cost)
- ✅ No API key needed
- ✅ Full control

**Cons:**
- ⚠️ Need Chromium (~500MB disk)
- ⚠️ RAM: 200-400MB per session
- ⚠️ No managed stealth/proxies

## Resources

- **Dashboard:** https://cloud.browser-use.com
- **API Keys:** https://cloud.browser-use.com/settings?tab=api-keys&new=1
- **Docs:** https://docs.browser-use.com
- **OpenAPI Spec:** https://docs.browser-use.com/cloud/openapi/v3.json
- **GitHub:** https://github.com/browser-use/browser-use
- **Examples:** https://github.com/browser-use/browser-use/tree/main/examples/cloud

## When to Give Up on Cloud API

If after trying all troubleshooting steps the API still returns 404:

1. **Check service status** — May be down for maintenance
2. **Contact support** — API key may need manual activation
3. **Use open-source library** — Self-host instead of Cloud
4. **Use alternative** — Scrapling, Playwright, Puppeteer

**Don't waste time** if API is clearly broken — pivot to alternatives quickly.
