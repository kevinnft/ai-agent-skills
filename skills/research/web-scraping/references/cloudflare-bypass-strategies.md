# Cloudflare Bypass Strategies

When a site returns Cloudflare challenge page ("Just a moment...") or 403 errors on all endpoints, standard scraping tools fail. This document covers escalation strategies.

## Detection

**Cloudflare challenge page:**
```html
<!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title>
<meta http-equiv="refresh" content="360">
```

**403 on all endpoints:**
```bash
curl -s https://example.com/api/listings -o /dev/null -w "HTTP %{http_code}\n"
# Output: HTTP 403
```

**Bot detection error from cloud services:**
```json
{"results":[],"errors":[{"url":"https://example.com/","error":"bot_blocked"}]}
```

## Escalation Ladder

### Level 1: Headers + User-Agent (Success Rate: ~20%)

```bash
curl -s -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.5" \
  -H "Accept-Encoding: gzip, deflate, br" \
  -H "Connection: keep-alive" \
  "https://example.com/api/listings"
```

**When it works:** Basic bot detection that only checks User-Agent.  
**When it fails:** Cloudflare Turnstile, fingerprinting, or IP reputation checks.

### Level 2: TinyFish Fetch API (Success Rate: ~40%)

```bash
curl -X POST https://api.fetch.tinyfish.ai \
  -H "X-API-Key: $TINYFISH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/"]}'
```

**When it works:** Sites with moderate Cloudflare protection.  
**When it fails:** Advanced bot detection, Turnstile challenges, or IP-based blocks.

**rpow2swap.com result (May 2026):**
```json
{"results":[],"errors":[{"url":"https://rpow2swap.com/","error":"bot_blocked"}]}
```

### Level 3: Browserbase Cloud Browser (Success Rate: ~70%)

Requires API key from https://browserbase.com/

```python
import requests

# Create session
response = requests.post(
    "https://www.browserbase.com/v1/sessions",
    headers={"X-BB-API-Key": API_KEY, "Content-Type": "application/json"},
    json={"projectId": PROJECT_ID}
)

session = response.json()
session_id = session['id']

# Navigate to page
requests.post(
    f"https://www.browserbase.com/v1/sessions/{session_id}/navigate",
    headers={"X-BB-API-Key": API_KEY, "Content-Type": "application/json"},
    json={"url": "https://example.com"}
)

# Get page content
content = requests.get(
    f"https://www.browserbase.com/v1/sessions/{session_id}/content",
    headers={"X-BB-API-Key": API_KEY}
).text
```

**When it works:** Most Cloudflare-protected sites (uses real Chrome with residential proxies).  
**When it fails:** Sites with advanced fingerprinting or manual review.

**Cost:** Paid service, ~$0.01-0.05 per session.

### Level 4: Stealth Browser Libraries (Success Rate: ~60%)

**Puppeteer with stealth plugin:**
```javascript
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

const page = await browser.newPage();
await page.goto('https://example.com', {waitUntil: 'networkidle2'});
const content = await page.content();
```

**When it works:** Sites that check for headless browser markers.  
**When it fails:** Cloudflare Turnstile (requires human interaction).

**Note:** May fail on VPS with sandbox errors — use `--no-sandbox` flag.

### Level 5: Manual Browser + DevTools (Success Rate: 100%)

When all automation fails, use real browser:

1. Open site in Chrome/Firefox
2. Open DevTools → Network tab
3. Filter by `Fetch/XHR`
4. Interact with page (scroll, click, navigate)
5. Find API endpoint in Network tab
6. Right-click → Copy as cURL
7. Extract auth headers/cookies
8. Replicate in script

**When to use:** High-value targets, one-time scraping, or when automation is blocked.

**Limitation:** Not scalable, requires manual intervention.

## rpow2swap.com Case Study (May 2026)

**Protection level:** Cloudflare with bot detection

**Attempts:**
1. ❌ curl with User-Agent → 403
2. ❌ TinyFish Fetch API → `bot_blocked`
3. ❌ Hermes browser tool → timeout (stuck on challenge)
4. ⏸️ Browserbase → not configured (API key missing)
5. ✅ Manual browser inspection → **recommended approach**

**Outcome:** Site requires manual browser access for initial API discovery. Once endpoint found, may be accessible via curl with proper headers/cookies.

**Next steps for automation:**
1. Use manual browser to find API endpoint
2. Extract auth headers/cookies from DevTools
3. Test endpoint with curl + headers
4. If works → automate with curl
5. If fails → use Browserbase for automation

## Decision Tree

```
Site returns Cloudflare challenge?
├─ Yes → Try TinyFish Fetch
│   ├─ Works → Use TinyFish
│   └─ Fails → Try Browserbase (if configured)
│       ├─ Works → Use Browserbase
│       └─ Fails → Manual browser + DevTools
└─ No → Use curl with User-Agent
```

## Cost-Benefit Analysis

| Method | Cost | Speed | Success Rate | Scalability |
|--------|------|-------|--------------|-------------|
| curl + headers | Free | Fast | 20% | High |
| TinyFish | Free | Medium | 40% | High |
| Browserbase | $0.01-0.05/req | Slow | 70% | Medium |
| Stealth browser | Free | Slow | 60% | Medium |
| Manual browser | Free | Very slow | 100% | None |

## Pitfalls

- **Don't retry failed methods** — if curl fails, TinyFish likely fails too (same IP reputation)
- **Cloudflare learns** — repeated automation attempts may trigger stricter protection
- **Session cookies expire** — manual browser approach requires periodic re-authentication
- **Rate limiting** — even successful bypass may trigger rate limits on API endpoints
- **Legal considerations** — bypassing protection may violate ToS (check robots.txt and terms)

## When to Give Up

If all methods fail and manual browser is not feasible:
1. Check if site has official API
2. Contact site owner for API access
3. Use alternative data sources
4. Accept that automation is not possible

**Red flags:**
- Site requires CAPTCHA on every request
- IP gets banned after 1-2 requests
- Site uses device fingerprinting + IP reputation
- Manual browser access also gets blocked

## References

- TinyFish Docs: https://docs.tinyfish.ai/
- Browserbase Docs: https://docs.browserbase.com/
- Puppeteer Stealth: https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth
