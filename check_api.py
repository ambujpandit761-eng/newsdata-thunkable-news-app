#!/usr/bin/env python3
"""Print what the app would receive from newsdata.io for a category.

Usage: NEWSDATA_API_KEY=... python3 check_api.py [category]
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

URL = "https://newsdata.io/api/1/latest"


def main() -> int:
    key = os.environ.get("NEWSDATA_API_KEY")
    if not key:
        print("Set NEWSDATA_API_KEY first.", file=sys.stderr)
        return 1
    category = sys.argv[1] if len(sys.argv) > 1 else "top"
    query = urllib.parse.urlencode({"apikey": key, "language": "en", "category": category})
    try:
        with urllib.request.urlopen(f"{URL}?{query}", timeout=20) as resp:
            code, body = resp.status, resp.read()
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read()
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return 1

    if code == 401:
        print("HTTP 401: invalid API key")
        return 1
    if code == 429:
        print("HTTP 429: rate limit reached, try again later")
        return 1
    if code != 200:
        print(f"HTTP {code}: {body[:200].decode('utf-8', 'replace')}")
        return 1

    data = json.loads(body)
    results = data.get("results") or []
    print(f"HTTP {code}, status={data.get('status')}, {len(results)} results")
    if not results:
        print("No articles found.")
        return 0
    for i, item in enumerate(results, 1):
        kws = item.get("keywords")
        kw_text = ", ".join(kws) if isinstance(kws, list) and kws else "(none)"
        sent = item.get("sentiment") or "(not returned on this plan)"
        print(f"{i}. {item.get('title') or '(untitled)'}")
        print(f"   keywords: {kw_text}")
        print(f"   sentiment: {sent}")
    print(f"nextPage cursor: {'present' if data.get('nextPage') else 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
