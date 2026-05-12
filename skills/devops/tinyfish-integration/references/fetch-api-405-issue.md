# Fetch API 405 Method Not Allowed Issue

**Date:** 2026-05-10  
**Status:** Unresolved  
**API Key:** Confirmed working for Search API

## Symptom

```bash
curl -H "X-API-Key: sk-tinyfish-..." \
  "https://api.fetch.tinyfish.ai?url=https://example.com/"
# HTTP/2 405
```

## Investigation

### Test 1: GET Request (Current Implementation)
```bash
curl -v -H "X-API-Key: sk-tinyfish-4pSzJ2SfN47DF8y1trM9Uw3dshdtaaLJ" \
  "https://api.fetch.tinyfish.ai?url=https://example.com/" 2>&1 | grep "< HTTP"
# < HTTP/2 405
```

**Result:** 405 Method Not Allowed

### Test 2: Response Body
```bash
curl -s -H "X-API-Key: sk-tinyfish-..." \
  "https://api.fetch.tinyfish.ai?url=https://example.com/"
# (empty response)
```

**Result:** No error message in body, just empty response with 405 status.

### Test 3: Search API (Control)
```bash
curl -s -H "X-API-Key: sk-tinyfish-..." \
  "https://api.search.tinyfish.ai?query=test" | jq .
# {
#   "query": "test",
#   "results": [...],
#   "total_results": 8,
#   "page": 0
# }
```

**Result:** ✅ Search API works perfectly with same API key and GET method.

## Hypotheses

### 1. POST Required
Fetch API may require POST request with JSON body instead of GET with query params.

**Test needed:**
```bash
curl -X POST -H "X-API-Key: ..." -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/"}' \
  https://api.fetch.tinyfish.ai
```

### 2. Different Endpoint Structure
Docs show `https://api.fetch.tinyfish.ai?url=...` but actual endpoint might be:
- `https://api.fetch.tinyfish.ai/fetch?url=...`
- `https://api.fetch.tinyfish.ai/v1/fetch`
- Different base domain

### 3. SDK-Only Feature
Fetch API might only be accessible via official SDKs (Python/TypeScript), not raw HTTP.

**Evidence:** TinyFish docs show SDK examples but curl examples only for Search API.

### 4. Beta/Restricted Feature
Fetch API might require:
- Different API key tier
- Explicit feature enablement
- Credits (despite docs saying "free")

## Documentation References

**TinyFish Fetch API Docs:** https://docs.tinyfish.ai/fetch-api

**Documented example (from docs):**
```typescript
const client = new TinyFish();
const response = await client.fetch.extract({
  url: "https://example.com/"
});
```

**cURL example (from docs):**
```bash
curl "https://api.fetch.tinyfish.ai?url=https://example.com/" \
  -H "X-API-Key: $TINYFISH_API_KEY"
```

**Note:** Docs show GET request with query param, but actual API returns 405.

## Next Steps

1. Test POST request with JSON body
2. Check TinyFish Discord/GitHub for known issues
3. Contact TinyFish support for clarification
4. Try official Python SDK to see actual HTTP requests
5. Check if API key needs Fetch feature enabled

## Workaround

Use Search API for now (confirmed working). For content extraction:
- Use Hermes built-in `web` toolset (fetch tool)
- Use Browserbase for Cloudflare-protected sites
- Use TinyFish Agent API (requires credits)

## Related

- Search API: ✅ Working
- Agent API: Untested (requires credits)
- Browser API: Untested (requires credits)
- MCP Server: ❌ Requires OAuth (incompatible with Hermes)
