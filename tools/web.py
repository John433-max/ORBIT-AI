"""
Web search / fetch abstraction.

Providers:
  - DuckDuckGoSearchProvider  — live HTML search (no API key)
  - StubSearchProvider        — honest offline message
  - AutoSearchProvider        — try live, fall back to stub
"""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from tools.base import BaseTool, ToolResult

USER_AGENT = (
    "Mozilla/5.0 (compatible; ORBIT/2.0; +https://github.com/local/orbit) "
    "AppleWebKit/537.36 (KHTML, like Gecko)"
)
HTTP_TIMEOUT = 12


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    content: str = ""
    source: str = "stub"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        ...

    def fetch(self, url: str) -> SearchResult:
        return SearchResult(title="", url=url, snippet="", content="", source="unsupported")


class StubSearchProvider(SearchProvider):
    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        return [
            SearchResult(
                title="[web search unavailable]",
                url="",
                snippet=f"No live web search configured. Query was: {query!r}",
                content="",
                source="stub",
            )
        ]


def _http_get(url: str, timeout: float = HTTP_TIMEOUT) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        charset = "utf-8"
        ctype = resp.headers.get("Content-Type", "")
        m = re.search(r"charset=([\w-]+)", ctype, re.I)
        if m:
            charset = m.group(1)
        return raw.decode(charset, errors="replace")


def _strip_tags(text: str) -> str:
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class DuckDuckGoSearchProvider(SearchProvider):
    source_name = "duckduckgo"

    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        query = (query or "").strip()
        if not query:
            return [
                SearchResult(
                    title="[empty query]", url="",
                    snippet="Provide a non-empty search query.", source=self.source_name,
                )
            ]
        results: List[SearchResult] = []
        results.extend(self._instant_answer(query))
        results.extend(self._html_results(query, max_results=max_results))
        seen = set()
        unique: List[SearchResult] = []
        for r in results:
            key = r.url or r.title
            if key in seen:
                continue
            seen.add(key)
            unique.append(r)
            if len(unique) >= max_results:
                break
        if not unique:
            raise RuntimeError(f"DuckDuckGo returned no results for {query!r}")
        return unique

    def _instant_answer(self, query: str) -> List[SearchResult]:
        out: List[SearchResult] = []
        try:
            url = "https://api.duckduckgo.com/?" + urllib.parse.urlencode({
                "q": query, "format": "json", "no_redirect": "1",
                "no_html": "1", "skip_disambig": "1",
            })
            data = json.loads(_http_get(url, timeout=8))
            heading = (data.get("Heading") or "").strip()
            abstract = (data.get("AbstractText") or "").strip()
            abs_url = (data.get("AbstractURL") or "").strip()
            if abstract:
                out.append(SearchResult(
                    title=heading or query, url=abs_url,
                    snippet=abstract[:500], content=abstract,
                    source=self.source_name + "+ia",
                ))
            for topic in (data.get("RelatedTopics") or [])[:3]:
                if not isinstance(topic, dict):
                    continue
                text = (topic.get("Text") or "").strip()
                first = topic.get("FirstURL") or ""
                if text:
                    out.append(SearchResult(
                        title=text[:80], url=first, snippet=text[:300],
                        source=self.source_name + "+ia",
                    ))
        except Exception:
            pass
        return out

    def _html_results(self, query: str, max_results: int = 5) -> List[SearchResult]:
        out: List[SearchResult] = []
        url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
        page = _http_get(url)
        link_pat = re.compile(
            r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S,
        )
        snip_pat = re.compile(
            r'class="result__snippet"[^>]*>(.*?)</(?:a|td|div|span)', re.I | re.S,
        )
        links = list(link_pat.finditer(page))
        snips = list(snip_pat.finditer(page))
        snip_i = 0
        for m in links:
            if len(out) >= max_results:
                break
            raw_href = html.unescape(m.group(1))
            title = _strip_tags(m.group(2))
            real_url = raw_href
            if "uddg=" in raw_href:
                parsed = urllib.parse.urlparse(
                    raw_href if raw_href.startswith("http") else "https:" + raw_href
                )
                qs = urllib.parse.parse_qs(parsed.query)
                if "uddg" in qs:
                    real_url = urllib.parse.unquote(qs["uddg"][0])
            snippet = ""
            while snip_i < len(snips) and snips[snip_i].start() < m.start():
                snip_i += 1
            if snip_i < len(snips):
                snippet = _strip_tags(snips[snip_i].group(1))
                snip_i += 1
            if not title and not snippet:
                continue
            out.append(SearchResult(
                title=title or real_url, url=real_url,
                snippet=snippet[:400], source=self.source_name,
            ))
        return out

    def fetch(self, url: str) -> SearchResult:
        url = (url or "").strip()
        if not url.startswith(("http://", "https://")):
            return SearchResult(
                title="", url=url,
                snippet="URL must start with http:// or https://",
                content="", source=self.source_name,
            )
        try:
            page = _http_get(url, timeout=15)
            title_m = re.search(r"(?is)<title[^>]*>(.*?)</title>", page)
            title = _strip_tags(title_m.group(1)) if title_m else url
            text = _strip_tags(page)
            return SearchResult(
                title=title, url=url, snippet=text[:400],
                content=text[:6000], source=self.source_name + "+fetch",
            )
        except Exception as e:
            return SearchResult(
                title="", url=url, snippet=f"Fetch failed: {e}",
                content="", source=self.source_name + "+fetch",
            )


class AutoSearchProvider(SearchProvider):
    def __init__(self):
        self.live = DuckDuckGoSearchProvider()
        self.stub = StubSearchProvider()

    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        try:
            return self.live.search(query, max_results=max_results)
        except Exception as e:
            results = self.stub.search(query, max_results=max_results)
            results[0].snippet = (
                f"Live web search failed ({type(e).__name__}: {e}). Query was: {query!r}"
            )
            results[0].source = "stub+error"
            return results

    def fetch(self, url: str) -> SearchResult:
        try:
            return self.live.fetch(url)
        except Exception as e:
            return SearchResult(
                title="", url=url, snippet=f"Fetch failed: {e}",
                content="", source="stub+error",
            )


class WebSearchTool(BaseTool):
    name = "web.search"
    description = (
        "Search the public web for up-to-date information. "
        "Args: query (required string), max_results (optional int, default 5)."
    )
    permission_level = "NETWORK"
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "max_results": {"type": "integer", "default": 5},
        },
        "required": ["query"],
    }
    timeout_s = 25.0

    def __init__(self, provider: Optional[SearchProvider] = None):
        self.provider = provider or AutoSearchProvider()

    def execute(self, query: str = "", max_results: int = 5, **_) -> ToolResult:
        try:
            results = self.provider.search(query, max_results=int(max_results or 5))
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))
        lines = []
        for i, r in enumerate(results, 1):
            line = f"{i}. {r.title}"
            if r.snippet:
                line += f" — {r.snippet}"
            if r.url:
                line += f"\n   {r.url}"
            lines.append(line)
        return ToolResult(
            ok=True,
            content="\n".join(lines) if lines else "No results.",
            data=[r.to_dict() for r in results],
        )


class WebFetchTool(BaseTool):
    name = "web.fetch"
    description = "Fetch and extract readable text from a public HTTP(S) URL."
    permission_level = "NETWORK"
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Full http(s) URL"},
        },
        "required": ["url"],
    }
    timeout_s = 30.0

    def __init__(self, provider: Optional[SearchProvider] = None):
        self.provider = provider or AutoSearchProvider()

    def execute(self, url: str = "", **_) -> ToolResult:
        r = self.provider.fetch(url)
        if not r.content and r.snippet.startswith("Fetch failed"):
            return ToolResult(ok=False, content=r.snippet, error=r.snippet, data=r.to_dict())
        return ToolResult(
            ok=True,
            content=r.content or r.snippet,
            data=r.to_dict(),
        )
