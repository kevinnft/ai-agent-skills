---
name: web-scraping
description: Extract data from websites, including JavaScript-rendered SPAs and dynamic content
triggers:
  - scrape website data
  - extract content from web page
  - get data from JavaScript site
  - parse SPA content
  - headless browser automation
origin: unknown
source_license: see upstream
language: en
---

# Web Scraping

Extract structured data from websites, handling both static HTML and JavaScript-rendered content (React, Next.js, Vue, etc.).

## When to Use

- User asks to "scrape", "extract", or "get data from" a website
- Target site uses client-side rendering (SPA frameworks)
- Need to interact with dynamic content (infinite scroll, lazy loading)
- API endpoints are not available or documented

## Approach Selection

### 1. Static HTML (curl + parsing)
**Use when:** Site serves complete HTML without JavaScript rendering.

```bash
curl -sL 'https://example.com' | grep -oP 'pattern'
# or with jq for JSON APIs
curl -s 'https://api.example.com/data' | jq '.items[]'
```

**Pros:** Fast, lightweight, no dependencies  
**Cons:** Fails on JS-rendered content

### 2. Headless Browser (Puppeteer/Playwright)
**Use when:** Content is rendered client-side (React, Next.js, Vue, Angular).

**Node.js + Puppeteer** (recommended for WSL2/containers):
```javascript
const puppeteer = require('puppeteer');

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']  // Required in WSL2/containers
});

const page = await browser.newPage();
await page.goto('https://example.com', {
  waitUntil: 'networkidle2',
  timeout: 60000
});

// Wait for dynamic content
await new Promise(resolve => setTimeout(resolve, 3000));

// Extract text
const content = await page.evaluate(() => document.body.innerText);

// Extract structured data
const data = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('.title')?.innerText,
    value: el.querySelector('.value')?.innerText
  }));
});

await browser.close();
```

**Pros:** Handles all JS rendering, can interact with page  
**Cons:** Slower, heavier resource usage

### 3. API Inspection (DevTools Network tab)
**Use when:** Site loads data via XHR/fetch calls.

1. Open browser DevTools → Network tab
2. Filter by XHR/Fetch
3. Find API endpoint
4. Replicate with curl/fetch

**Pros:** Fastest, most reliable  
**Cons:** Requires manual inspection, may need auth tokens

**Alternative: Reverse-engineer from minified JS** (when browser access blocked):

**Method A: Direct curl (if no Cloudflare)**
```bash
# Download main JS bundle
curl -s "https://example.com/assets/main-[hash].js" > /tmp/bundle.js

# Search for API patterns
grep -oP '"/[a-z_/-]{3,}"' /tmp/bundle.js | sort -u
strings /tmp/bundle.js | grep -i 'keyword' | head -20
```

**Method B: TinyFish browser automation (if Cloudflare protected)**

When curl fails due to Cloudflare Turnstile, use TinyFish to bypass protection and download JS via Chrome DevTools Protocol:

```python
# 1. Create TinyFish browser session (bypasses Cloudflare)
# 2. Wait for challenge completion
# 3. Connect to browser via CDP WebSocket
# 4. Use Runtime.evaluate to fetch JS files
# 5. Extract API endpoints from minified code
```

See `references/tinyfish-js-reverse-engineering.md` for full workflow (tested on rpow2swap.com May 2026).

**Trial-error common paths with size check:**
```bash
for path in /api/listings /api/orders /listings /tokens /api/stats; do
  echo "Testing: https://example.com$path"
  timeout 3 curl -s -m 3 -o /dev/null -w "HTTP %{http_code} | Size: %{size_download} bytes\\n" \
    "https://example.com$path" 2>&1 || echo "Timeout/Error"
done

# Look for large responses (>10KB = likely data endpoint, <2KB = likely SPA HTML)
```

**Success indicators:**
- Response size >10KB → likely JSON data endpoint
- Response size <2KB → likely SPA HTML fallback
- Timeout → endpoint exists but slow/protected

See `references/spa-api-discovery.md` for full technique (tested on rpow2swap.com May 2026).

**Success case (rpow2swap.com, May 2026):**
```bash
# 1. Try common API paths with timeout
for path in /api/listings /api/tokens /listings /tokens /api/orderbook; do
  timeout 3 curl -s -m 3 -o /dev/null -w "HTTP %{http_code} | Size: %{size_download}\\n" \
    "https://example.com$path"
done

# Result: /api/listings returned 65KB (200 OK) — found it!

# 2. Fetch and inspect data
curl -s "https://example.com/api/listings" | head -c 2000
# Returns JSON array with full listing data

# 3. Build monitoring bot
# State-based change detection: track seen IDs, alert on new entries
```

**Key insight:** Many SPAs use predictable REST paths (`/api/<resource>`). Trial-error with timeout is faster than reverse-engineering minified JS.

### 3.5. Third-Party APIs (Twitter/X)
**Use when:** Scraping Twitter/X content (tweets, profiles, media).

**Primary: vxtwitter API** (no auth, works from terminal)
```bash
# Get tweet data
curl -s "https://api.vxtwitter.com/Twitter/status/{tweet_id}" | jq -r '.tweet | {text, author, likes, retweets, replies, media}'

# Get account info
curl -s "https://api.vxtwitter.com/{handle}" | jq -r '.user | {name, description, followers, website}'

# Extract quoted tweet (QRT)
curl -s "https://api.vxtwitter.com/Twitter/status/{tweet_id}" | jq -r '.qrt | {text, author, likes}'
```

**Fallback: fxtwitter API** (same structure)
```bash
curl -s "https://api.fxtwitter.com/{handle}/status/{tweet_id}"
```

**Pros:** No auth, fast, structured JSON, includes media URLs  
**Cons:** Rate limited, may lag behind real-time data

**Note:** Twitter's official API requires auth and has strict rate limits. Use vxtwitter/fxtwitter for read-only access.

### 4. Cloud Browser Services (Cloudflare bypass)
**Use when:** Site has Cloudflare Turnstile, bot detection, or anti-scraping measures.

**Browserbase** (recommended, tested May 2026):
```python
import requests

# Create session
response = requests.post(
    "https://www.browserbase.com/v1/sessions",
    headers={"X-BB-API-Key": API_KEY, "Content-Type": "application/json"},
    json={"projectId": PROJECT_ID}
)

session = response.json()
debug_url = f"https://www.browserbase.com/v1/sessions/{session['id']}/debug"
```

See `references/browserbase-api.md` for full API reference.

**Browser Use Cloud** (alternative, had 404 issues May 2026):
```python
response = requests.post(
    "https://api.browser-use.com/api/v1/run-task",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"task": "Go to protected-site.com and extract data"}
)
```

See `references/browser-use-cloud-api.md` for troubleshooting.

**Pros:** Bypasses Cloudflare, residential proxies, no local resources  
**Cons:** Paid service, requires API key, SDK needed for automation

## WSL2 / Container Considerations

**Chrome sandbox issues** are common in WSL2 and Docker. Always use:
```javascript
args: ['--no-sandbox', '--disable-setuid-sandbox']
```

**Python venv issues:** WSL2 Ubuntu may lack `python3-venv`. Use Node.js approach instead or install:
```bash
sudo apt install python3.12-venv
```

## Workflow

1. **Try curl first** — check if content is in initial HTML
2. **Inspect Network tab** — look for API endpoints
3. **Use headless browser** — if content is JS-rendered
4. **Extract incrementally** — get raw text first, then refine selectors

## Pitfalls

- **Don't assume static HTML** — modern sites often use SSR/CSR hybrid (Next.js)
- **Wait for content** — add delays after page load for dynamic content
- **Check robots.txt** — respect crawling policies
- **Rate limiting** — add delays between requests for bulk scraping
- **User-Agent** — some sites block default headless browser UA
- **Cloudflare protection** — sites with Cloudflare Turnstile/challenge pages block curl and standard browsers. Use Browser Use Cloud or stealth browser libraries.
- **VPS browser limitations** — Hermes browser tool may fail on VPS with sandbox errors. Use `--no-sandbox` flag or cloud browser services.
- **Browser Use API confusion** — Browser Use has TWO APIs: open-source library (local, free) vs Cloud API (managed, paid). Cloud API endpoint structure is confusing (examples use `/api/v1/`, docs say `/v3/`). If getting 404 errors, see `references/browser-use-cloud-api.md` for troubleshooting.

## Verification

- Print raw extracted content first to verify data is present
- Use `console.log(JSON.stringify(data, null, 2))` for structured output
- Check for empty arrays/null values — indicates selector mismatch

## Example: Next.js Site Scraping

See `references/nextjs-ssr-scraping.md` for full example from MegaETH KPIs extraction.

## References

- `references/spa-api-discovery.md` — API endpoint discovery from minified JS (rpow2swap.com case study)
- `references/tinyfish-js-reverse-engineering.md` — TinyFish browser automation + CDP for JS download + minified code analysis (Cloudflare bypass, tested May 2026)
- `references/cloudflare-turnstile-bypass.md` — escalation ladder for Cloudflare Turnstile v2 (curl → TinyFish → Puppeteer stealth → Browserbase → manual). Key lesson: stealth plugins fail against Turnstile, skip to Browserbase or manual.
- `references/race-condition-order-matching.md` — debugging "order reappeared" bugs in trading/marketplace systems (database races, cache invalidation, frontend state)
- `references/security-audit-pattern.md` — structured web app security audits for responsible disclosure
- `references/browserbase-api.md` — Browserbase cloud browser API reference
- `references/browser-use-cloud-api.md` — Browser Use Cloud troubleshooting

