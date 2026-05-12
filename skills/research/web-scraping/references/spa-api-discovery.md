# SPA API Discovery Techniques

When scraping Single Page Applications (React, Vue, Next.js), the data often comes from API endpoints rather than being embedded in HTML. Here's how to find them.

## Session Context: rpow2swap.com (May 2026)

**Challenge:** React SPA with minified JS, no obvious API endpoints in HTML source.

**Solution:** Reverse-engineer API from minified bundle.

## Technique 1: Search Minified JS for Patterns

```bash
# Download the main JS bundle
curl -s "https://example.com/assets/main-[hash].js" > /tmp/bundle.js

# Search for common API patterns
grep -oP 'https?://[^"'\'']+' /tmp/bundle.js | sort -u

# Search for relative paths (fetch calls)
grep -oP '"/[a-z_/-]{3,}"' /tmp/bundle.js | sort -u

# Search for template literals with paths
grep -oP '\`/[^`]+\`' /tmp/bundle.js | head -20

# Search for specific keywords
strings /tmp/bundle.js | grep -i 'order\|trade\|token\|price\|list' | head -20
```

**rpow2swap.com example:**
```bash
curl -s "https://rpow2swap.com/pub/main/rpow2-exchange/assets/index-DIVxzcRT.js" > /tmp/rpow2.min.js

# Found data structure in minified code:
strings /tmp/rpow2.min.js | grep -i 'order' | grep -v 'border'
# Output: activeListings, listedRpow2, bestAsk, rateMin, rateMax

# Trial-error common paths:
for path in /api/listings /api/orders /listings /tokens; do
  curl -s -m 3 -o /dev/null -w "HTTP %{http_code}\n" "https://rpow2swap.com$path"
done
# Result: /api/listings returned 200 with 65KB data
```

## Technique 2: Browser DevTools Network Tab

**When to use:** Site is live and you can interact with it.

1. Open site in browser
2. Open DevTools → Network tab
3. Filter by `Fetch/XHR`
4. Interact with page (scroll, click, navigate)
5. Look for JSON responses
6. Right-click request → Copy as cURL

**Pros:** Most reliable, shows auth headers  
**Cons:** Requires manual interaction

## Technique 3: Search for Base URL Variables

Minified JS often has a base URL constant:

```bash
# Common patterns
grep -oP 'const [a-zA-Z_$][a-zA-Z0-9_$]*\s*=\s*"https?://[^"]+"' /tmp/bundle.js
grep -oP 'API_URL\s*=\s*"[^"]+"' /tmp/bundle.js
grep -oP 'baseURL:\s*"[^"]+"' /tmp/bundle.js

# rpow2swap.com had:
grep -oP 'const qE=[^;]+' /tmp/rpow2.min.js
# Output: const qE=""
# Meaning: relative paths, base URL is same domain
```

## Technique 4: Trial-Error Common Paths

If no obvious endpoints found, try standard REST patterns:

```bash
# Common API paths
/api/v1/items
/api/items
/items
/data
/api/data

# Common resource names
/api/users
/api/products
/api/orders
/api/listings
/api/tokens
/api/trades
```

**Optimization:** Use timeout to avoid hanging:
```bash
for path in /api/listings /api/orders /listings; do
  echo "Testing: $path"
  timeout 3 curl -s -m 3 -o /dev/null -w "HTTP %{http_code} | Size: %{size_download} bytes\n" \
    "https://example.com$path" 2>&1 || echo "Timeout/Error"
done
```

## Technique 5: Search for Data Structure Keywords

If you know what data you're looking for:

```bash
# Search for specific field names
grep -oP '\{[^}]*"amount"[^}]*\}' /tmp/bundle.js | head -5
grep -oP '\{[^}]*"price"[^}]*\}' /tmp/bundle.js | head -5

# Search for localStorage keys (often reveal API structure)
grep -oP 'localStorage\.(get|set)Item\([^)]+\)' /tmp/bundle.js
```

**rpow2swap.com example:**
```bash
grep -oP '"rpow2[^"]*"' /tmp/rpow2.min.js
# Output: "rpow2x_token", "rpow2_email", "rpow2Volume"
# Indicates: auth token in localStorage, volume metric exists
```

## Technique 6: WebSocket Discovery

Some SPAs use WebSocket for real-time data:

```bash
# Search for WebSocket URLs
grep -oP 'wss?://[^"'\'']+' /tmp/bundle.js

# Search for WebSocket constructor
grep -oP 'new WebSocket\([^)]+\)' /tmp/bundle.js
```

**Note:** WebSocket scraping requires different approach (see `references/websocket-scraping.md`).

## Verification

Once you find a potential endpoint:

```bash
# Test with curl
curl -s "https://example.com/api/listings" | jq '.' | head -20

# Check response size
curl -s -o /dev/null -w "Size: %{size_download} bytes\n" "https://example.com/api/listings"

# Check response headers
curl -sI "https://example.com/api/listings"
```

## Pitfalls

- **Empty base URL** (`const API_URL = ""`) means relative paths on same domain
- **Minified variable names** make patterns hard to find — use `strings` command
- **Gzip-encoded responses** — curl auto-decodes, but check with `file` command if saving to disk
- **CORS restrictions** — API may work in browser but block curl (add proper headers)
- **Rate limiting** — don't hammer endpoints during discovery, use timeouts

## Success Indicators

- **Large response size** (>10KB) usually means data endpoint, not HTML
- **JSON content-type** in response headers
- **Array structure** in response body
- **Timestamp fields** (`created_at`, `updated_at`) indicate database records

## rpow2swap.com Case Study

**Final working endpoint:** `https://rpow2swap.com/api/listings`

**Response structure:**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "type": "sell",
    "amount": 10000,
    "sol_price": 10,
    "status": "active",
    "created_at": "2026-05-10 02:43:08",
    "updated_at": "2026-05-10 02:43:08",
    "solana_wallet_address": "..."
  }
]
```

**Discovery path:**
1. Tried browser navigation → timeout (Cloudflare protection suspected)
2. Downloaded minified JS bundle
3. Searched for "order", "trade", "token" keywords
4. Found data structure hints: `activeListings`, `bestAsk`
5. Trial-error common paths: `/api/listings` returned 200 with 65KB
6. Verified with curl → got JSON array of 220+ listings
