---
name: tinyfish-integration
description: Integrate TinyFish web toolkit (search, fetch, browser automation) into Hermes Agent
tags: [web, search, scraping, api, integration]
version: 1.0.0
origin: unknown
source_license: see upstream
language: en
---

# TinyFish Integration

TinyFish is a web toolkit for AI agents that provides search, fetch, and browser automation capabilities. Search and fetch are **free** for every account — no credits, no cost.

## Available Tools

### tinyfish_search
Search the live web and get structured, agent-ready results.

**Use cases:**
- Current information, news, prices
- Finding URLs before fetching content
- Anything that changes over time

**Parameters:**
- `query` (required): Search query string
- `location` (optional): 2-letter country code (e.g., "US", "FR", "ID")
- `language` (optional): 2-letter language code (e.g., "en", "fr", "id")
- `page` (optional): Page number for pagination (default: 0)

**Example:**
```python
tinyfish_search(query="Hermes Agent AI", location="US", language="en")
```

**Response format:**
```json
{
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "snippet": "Description text...",
      "site_name": "Example Site"
    }
  ]
}
```

### tinyfish_fetch
Pull the full content of any web page as clean extracted text.

**Use cases:**
- Reading articles, docs, product pages
- Extracting content without ads/navigation
- Batch processing multiple URLs (max 10)

**Parameters:**
- `urls` (required): Single URL or comma-separated list (max 10)

**Examples:**
```python
# Single URL
tinyfish_fetch(urls="https://example.com")

# Multiple URLs
tinyfish_fetch(urls="https://site1.com, https://site2.com, https://site3.com")
```

**Response format:**
```json
{
  "results": [
    {
      "url": "https://example.com",
      "final_url": "https://example.com",
      "title": "Page Title",
      "description": "Meta description",
      "language": "en",
      "text": "# Heading\n\nClean extracted content..."
    }
  ],
  "errors": []
}
```

## Setup

### 1. Get API Key
Visit https://agent.tinyfish.ai/api-keys to get your API key.

### 2. Configure Hermes
Add to `~/.hermes/.env`:
```bash
TINYFISH_API_KEY=sk-tinyfish-YOUR_KEY_HERE
```

### 3. Enable Toolset
Add to `~/.hermes/config.yaml`:
```yaml
toolsets:
  - tinyfish
```

### 4. Verify Installation
```bash
hermes chat -q "Search for 'Hermes Agent' using tinyfish_search"
```

## Tool Implementation

The TinyFish tools are implemented in `~/.hermes/hermes-agent/tools/tinyfish_search.py`:

- **tinyfish_search**: GET request to `https://api.search.tinyfish.ai`
- **tinyfish_fetch**: POST request to `https://api.fetch.tinyfish.ai` with JSON body

Both tools:
- Use `X-API-Key` header for authentication
- Return JSON responses
- Handle errors gracefully
- Support 60-second timeout for fetch (30s for search)

## When to Use Each Tool

| Tool | Use When |
|------|----------|
| **tinyfish_search** | You need to find URLs or get current information |
| **tinyfish_fetch** | You already know the URL and need the content |
| **Agent API** | TinyFish should perform multi-step workflows |
| **Browser API** | You need direct browser control from your code |

## Supported Content Types (Fetch)

- ✅ HTML pages (clean text extraction)
- ✅ PDF files (text extraction)
- ✅ JSON endpoints (raw JSON)
- ❌ Binary files (images, video) — returns error

## Limitations

- **Search**: No explicit rate limit documented
- **Fetch**: Max 10 URLs per request
- **Timeout**: 60 seconds for fetch, 30 seconds for search
- **Free tier**: Search and fetch are free with no credit cost

## Troubleshooting

### "TINYFISH_API_KEY environment variable not set"
- Check `~/.hermes/.env` has the key
- Restart Hermes after adding the key

### "HTTP 401: Unauthorized"
- Verify API key is correct
- Check key hasn't expired at https://agent.tinyfish.ai/api-keys

### "HTTP 405: Method Not Allowed"
- This was the old bug — fetch now uses POST correctly
- Update to latest tool version if you see this

### Timeout errors
- Fetch has 60s timeout — some pages may be slow
- Try fetching fewer URLs at once
- Check if the target site is accessible

## Advanced Usage

### Batch Fetch with Error Handling
```python
# Fetch multiple URLs — errors don't affect other URLs
result = tinyfish_fetch(urls="https://site1.com, https://site2.com, https://invalid-url.com")

# Response includes both results and errors
{
  "results": [...],  # Successful fetches
  "errors": [...]    # Failed URLs with error messages
}
```

### Geo-Targeted Search
```python
# Search from specific country
tinyfish_search(query="best pizza", location="IT", language="it")
```

### Pagination
```python
# Get page 2 of results
tinyfish_search(query="AI agents", page=1)
```

## Browser Automation (Advanced)

For sites protected by Cloudflare or requiring JavaScript execution, use the **Browser API** with CDP websocket automation.

**See:** `references/cloudflare-bypass-pattern.md` for complete workflow including:
- Cloudflare Turnstile bypass with retry loop
- CDP websocket automation via Runtime.evaluate
- Token injection via localStorage
- Transactional operation patterns (check → act → verify)

**Key pattern:**
1. Create browser session → wait for Cloudflare bypass (30 retries, 5s interval)
2. Connect to CDP websocket → inject auth tokens
3. Execute API calls via `Runtime.evaluate` with `fetch()`
4. Always cleanup session when done

## References

- TinyFish Docs: https://docs.tinyfish.ai/
- API Keys: https://agent.tinyfish.ai/api-keys
- Cookbook: https://github.com/tinyfish-io/tinyfish-cookbook
- Cloudflare Bypass Pattern: `references/cloudflare-bypass-pattern.md`
