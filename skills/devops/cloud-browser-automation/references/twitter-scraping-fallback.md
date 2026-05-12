# Twitter Scraping Fallback (No Browserbase Needed)

## Context

Twitter/X embeds full tweet data in `window.__INITIAL_STATE__` JSON within the HTML response. For simple tweet reads (no interaction, no auth), direct curl scraping is faster and cheaper than Browserbase.

## When to Use

**Use direct curl for:**
- ✅ Reading public tweet text
- ✅ Extracting media URLs
- ✅ Getting engagement metrics (likes, retweets, replies)
- ✅ Finding URLs in tweets

**Use Browserbase for:**
- ❌ Login-required content
- ❌ Infinite scroll / pagination
- ❌ JavaScript-heavy interactions
- ❌ Rate-limited endpoints

## Technique

### Step 1: Fetch HTML

```bash
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://x.com/USERNAME/status/TWEET_ID" > /tmp/tweet.html
```

**Key points:**
- Use `-A` (User-Agent) to avoid bot detection
- Twitter returns full HTML with embedded JSON
- No authentication needed for public tweets

### Step 2: Extract JSON Data

Tweet data is in `<script>` tag with `window.__INITIAL_STATE__=...`

**Pattern 1: Direct grep (fast, fragile)**
```bash
grep -o 'window.__INITIAL_STATE__={.*}' /tmp/tweet.html | sed 's/window.__INITIAL_STATE__=//'
```

**Pattern 2: Extract from HTML (reliable)**
```python
import re
import json

with open('/tmp/tweet.html', 'r') as f:
    html = f.read()

# Find the script tag with tweet data
match = re.search(r'window\.__INITIAL_STATE__=({.*?})</script>', html, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    
    # Navigate to tweet
    tweets = data['entities']['tweets']['entities']
    for tweet_id, tweet in tweets.items():
        print(f"Text: {tweet['full_text']}")
        print(f"Likes: {tweet['favorite_count']}")
        print(f"Retweets: {tweet['retweet_count']}")
```

### Step 3: Parse Tweet Content

**Tweet structure in JSON:**
```json
{
  "entities": {
    "tweets": {
      "entities": {
        "TWEET_ID": {
          "full_text": "Tweet content here",
          "favorite_count": 123,
          "retweet_count": 45,
          "reply_count": 12,
          "entities": {
            "urls": [{"expanded_url": "https://..."}],
            "media": [{"media_url_https": "https://..."}]
          }
        }
      }
    }
  }
}
```

## Example: Session 2026-05-05

**Task:** Analyze tweet about HyperFrames (https://x.com/heygen/status/2051697813554405384)

**Approach:**
1. ❌ Tried local browser → failed (WSL sandbox)
2. ❌ Tried Browserbase → no SDK available
3. ✅ Used curl → succeeded

**Command:**
```bash
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://x.com/heygen/status/2051697813554405384" > /tmp/twitter_response.html
```

**Result:**
- 271KB HTML response
- Full tweet text extracted
- Media URLs found
- No Browserbase credits used
- 2 seconds vs 30+ seconds for Browserbase

## Pitfalls

### 1. Rate Limiting

**Problem:** Twitter may rate-limit direct requests

**Solution:**
- Add delays between requests (1-2 seconds)
- Rotate User-Agent strings
- Use residential proxies if needed
- Escalate to Browserbase only if blocked

### 2. JSON Parsing Errors

**Problem:** `window.__INITIAL_STATE__` may be malformed or missing

**Solution:**
```python
try:
    data = json.loads(match.group(1))
except json.JSONDecodeError:
    # Fallback: search for tweet text in HTML
    text_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    if text_match:
        tweet_text = text_match.group(1)
```

### 3. Login-Required Content

**Problem:** Some tweets require authentication

**Solution:**
- Check response for "This Tweet is unavailable"
- If found, escalate to Browserbase with cookies
- Or use Twitter API with bearer token

## Cost Comparison

| Method | Time | Cost | Success Rate |
|--------|------|------|--------------|
| curl | 2s | Free | 95% (public tweets) |
| Browserbase | 30s+ | $0.01/min | 99% (all tweets) |

**Recommendation:** Always try curl first, escalate to Browserbase only if blocked.

## Integration with Escalation Ladder

Update the escalation ladder in main SKILL.md:

```
1. Try curl for Twitter (if public tweet)
   ↓ (if rate limited or login required)
2. Try Hermes browser
   ↓ (if blocked by Cloudflare or sandbox issues)
3. Use cloud browser (Browserbase)
```

## Verification

After scraping:
```bash
# Verify JSON extracted
jq '.' /tmp/tweet_data.json

# Verify tweet text found
grep -i "tweet_text" /tmp/tweet_data.json

# Check file size (should be >1KB for valid response)
ls -lh /tmp/twitter_response.html
```
