"""TinyFish Search API integration for Hermes Agent."""

import json
import os
import urllib.parse
import urllib.request
from typing import Optional

from tools.registry import registry


def check_requirements() -> bool:
    """Check if TinyFish API key is configured."""
    return bool(os.getenv("TINYFISH_API_KEY"))


def tinyfish_search(
    query: str,
    location: Optional[str] = None,
    language: Optional[str] = None,
    page: int = 0,
    task_id: str = None,
) -> str:
    """
    Search the web using TinyFish Search API.
    
    Args:
        query: Search query string
        location: Optional 2-letter country code (e.g., "US", "FR", "ID")
        language: Optional 2-letter language code (e.g., "en", "fr", "id")
        page: Page number for pagination (default: 0)
        task_id: Internal task tracking ID
    
    Returns:
        JSON string with search results
    """
    api_key = os.getenv("TINYFISH_API_KEY")
    if not api_key:
        return json.dumps({
            "error": "TINYFISH_API_KEY environment variable not set"
        })
    
    # Build query parameters
    params = {"query": query, "page": str(page)}
    if location:
        params["location"] = location
    if language:
        params["language"] = language
    
    url = f"https://api.search.tinyfish.ai?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header("X-API-Key", api_key)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8")
            return data
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else str(e)
        return json.dumps({
            "error": f"HTTP {e.code}: {e.reason}",
            "details": error_body
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


def tinyfish_fetch(url: str, task_id: str = None) -> str:
    """
    Fetch and extract clean content from any URL using TinyFish Fetch API.
    
    Args:
        url: URL to fetch and extract content from
        task_id: Internal task tracking ID
    
    Returns:
        JSON string with extracted content
    """
    api_key = os.getenv("TINYFISH_API_KEY")
    if not api_key:
        return json.dumps({
            "error": "TINYFISH_API_KEY environment variable not set"
        })
    
    fetch_url = f"https://api.fetch.tinyfish.ai?url={urllib.parse.quote(url)}"
    
    try:
        req = urllib.request.Request(fetch_url)
        req.add_header("X-API-Key", api_key)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8")
            return data
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else str(e)
        return json.dumps({
            "error": f"HTTP {e.code}: {e.reason}",
            "details": error_body
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


# Register search tool
registry.register(
    name="tinyfish_search",
    toolset="tinyfish",
    schema={
        "name": "tinyfish_search",
        "description": "Search the web and get structured results. Returns title, URL, snippet, and site name for each result. Free to use with no credit cost.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "location": {
                    "type": "string",
                    "description": "Optional 2-letter country code for geo-targeted results (e.g., 'US', 'FR', 'ID')"
                },
                "language": {
                    "type": "string",
                    "description": "Optional 2-letter language code (e.g., 'en', 'fr', 'id')"
                },
                "page": {
                    "type": "integer",
                    "description": "Page number for pagination (default: 0)"
                }
            },
            "required": ["query"]
        }
    },
    handler=lambda args, **kw: tinyfish_search(
        query=args.get("query", ""),
        location=args.get("location"),
        language=args.get("language"),
        page=args.get("page", 0),
        task_id=kw.get("task_id")
    ),
    check_fn=check_requirements,
    requires_env=["TINYFISH_API_KEY"],
)

# Register fetch tool
registry.register(
    name="tinyfish_fetch",
    toolset="tinyfish",
    schema={
        "name": "tinyfish_fetch",
        "description": "Fetch and extract clean content from any URL. Returns structured text content without ads, navigation, or clutter. Free to use with no credit cost.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to fetch and extract content from"
                }
            },
            "required": ["url"]
        }
    },
    handler=lambda args, **kw: tinyfish_fetch(
        url=args.get("url", ""),
        task_id=kw.get("task_id")
    ),
    check_fn=check_requirements,
    requires_env=["TINYFISH_API_KEY"],
)
