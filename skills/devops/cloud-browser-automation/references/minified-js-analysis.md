# Analyzing Minified JS Bundles for API Patterns

When curl successfully fetches a SPA but returns minified JavaScript instead of data, you can often extract API endpoints and data structures without needing Browserbase.

## When to Use

- ✅ Site returns HTML with `<script src="/assets/index-HASH.js">`
- ✅ JS bundle is accessible via direct curl
- ✅ You need to find API endpoints, WebSocket URLs, or data structures
- ❌ Don't use if the bundle is obfuscated/encrypted (rare, but happens)

## Technique: Grep-Based Pattern Extraction

### 1. Download the Bundle

```bash
# Extract script URL from HTML
SCRIPT_URL=$(curl -s "https://example.com" | grep -oP 'src="[^"]+\.js"' | head -1 | cut -d'"' -f2)

# Download bundle
curl -s "https://example.com${SCRIPT_URL}" > /tmp/bundle.min.js
```

### 2. Search for API Patterns

**Common patterns to grep for:**

```bash
# API base URLs
grep -oP 'https?://[^"'\'']+api[^"'\'']*' /tmp/bundle.min.js | sort -u

# Relative API paths
grep -oP '"/[a-z_/-]{3,}"' /tmp/bundle.min.js | grep -E '(api|order|trade|token|price|list)' | sort -u

# WebSocket URLs
grep -oP 'wss?://[^"'\'']+' /tmp/bundle.min.js

# Fetch/axios calls
grep -oP 'fetch\([^)]+\)' /tmp/bundle.min.js | head -20

# localStorage keys (often reveal token names)
grep -oP 'localStorage\.(get|set)Item\([^)]+\)' /tmp/bundle.min.js
```

### 3. Find Data Structures

**Look for object literals with known field names:**

```bash
# Search for specific fields
strings /tmp/bundle.min.js | grep -i 'orderbook\|bestAsk\|bestBid'

# Extract variable assignments
grep -oP 'const [a-zA-Z_$][a-zA-Z0-9_$]*=\{[^}]{0,200}\}' /tmp/bundle.min.js | grep 'price\|order'
```

### 4. Identify Base URL Variables

Minified code often uses short variable names for base URLs:

```bash
# Find base URL assignments (common patterns)
grep -oP 'const [a-zA-Z]{1,3}="https?://[^"]+"' /tmp/bundle.min.js
grep -oP 'const [a-zA-Z]{1,3}=""' /tmp/bundle.min.js  # Empty = relative paths

# Example: const qE="" means relative paths like `${qE}/api/orders`
```

### 5. Trace Authentication Patterns

```bash
# Find token storage
grep -oP '[a-z_]+_token' /tmp/bundle.min.js | sort -u

# Find Authorization headers
grep -oP 'Authorization[^,;]{0,50}' /tmp/bundle.min.js
```

## Real Example: rpow2swap.com

**Site:** https://rpow2swap.com/  
**Bundle:** `/pub/main/rpow2-exchange/assets/index-DIVxzcRT.js`

**Findings:**

```bash
# 1. Found localStorage token
$ grep -oP '"[a-z_]+_token"' bundle.js
"rpow2x_token"

# 2. Found data structure fields
$ strings bundle.js | grep -E '(bestAsk|bestBid|activeListings)'
{label:"Best Ask",value:i.bestAsk?`${i.bestAsk.toFixed(6)} SOL`:"
{label:"Active Listings",value:i.activeListings.toLocaleString()}

# 3. Found base URL pattern
$ grep -oP 'const qE=[^;]+' bundle.js
const qE=""  # Empty = relative paths

# 4. Found fetch pattern
$ grep -oP 'fetch\(`\$\{[^}]+\}[^`]+`' bundle.js
fetch(`${qE}${t}`,{...e,headers:r,body:e.body?JSON.stringify(e.body)
```

**Conclusion:** API uses relative paths, likely `/api/orderbook` or similar. Data structure includes `bestAsk`, `activeListings`, `listedRpow2`.

## Pitfalls

### 1. Gzip-Encoded Responses

**Problem:** curl returns binary gzip data instead of text

**Solution:**
```bash
# Check file type first
file /tmp/bundle.js  # Should show "ASCII text" not "gzip compressed"

# If gzipped, decompress
curl -s --compressed "https://example.com/bundle.js" > /tmp/bundle.js
```

### 2. Source Maps Available

**Opportunity:** Some sites ship `.js.map` files with original variable names

**Check:**
```bash
# Try appending .map to bundle URL
curl -s "https://example.com/assets/index-HASH.js.map" | jq '.sources'

# If exists, download and search the unminified sources
```

### 3. Dynamic API URLs

**Problem:** API URL constructed at runtime from `window.location` or config

**Solution:**
```bash
# Look for window.location usage
grep -oP 'window\.location[^;]{0,50}' /tmp/bundle.js

# Look for config objects
grep -oP 'API_URL[^,;]{0,50}' /tmp/bundle.js
```

## When to Escalate to Browserbase

Only escalate if:
- ❌ Bundle is obfuscated (variable names like `_0x1a2b3c`)
- ❌ API endpoints are encrypted/encoded
- ❌ Need to capture actual network traffic (not just code analysis)
- ❌ Site uses WebSocket with complex handshake

Otherwise, grep-based analysis is faster and free.

## Bot Monitoring Pattern

Once you've found the data structure, build a polling bot:

```python
import requests
import time

def check_orderbook():
    # Try common endpoint patterns
    for path in ["/api/orderbook", "/api/orders", "/orderbook"]:
        try:
            r = requests.get(f"https://example.com{path}", timeout=5)
            if r.status_code == 200:
                return r.json()
        except:
            continue
    return None

def detect_anomaly(data, threshold=0.0001):
    """Alert if price drops below threshold"""
    if data.get("bestAsk") and data["bestAsk"] < threshold:
        return f"🚨 ALERT: Abnormal price {data['bestAsk']} SOL"
    return None

while True:
    data = check_orderbook()
    if data:
        alert = detect_anomaly(data)
        if alert:
            print(alert)  # Replace with Telegram/Discord webhook
    time.sleep(10)
```

## VPS Considerations

**Resource cost:** Near-zero (curl + grep = <1MB RAM, no disk)

**vs Browserbase:**
- Browserbase: ~$0.01/min, 100-200MB RAM (cloud)
- Curl + grep: Free, <1MB RAM (local)

**Recommendation:** Always try curl + grep first. Only use Browserbase if this fails.
