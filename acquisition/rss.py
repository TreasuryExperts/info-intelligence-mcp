from __future__ import annotations

from typing import Any

import feedparser

from acquisition.base import RawItem


def fetch_rss(url: str, source_name: str | None = None, limit: int = 20) -> list[RawItem]:
    parsed = feedparser.parse(url)
    name = source_name or getattr(parsed.feed, "title", None) or url
    items: list[RawItem] = []
    for entry in (parsed.entries or [])[:limit]:
        title = getattr(entry, "title", "") or ""
        link = getattr(entry, "link", "") or ""
        summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
        published = getattr(entry, "published", None) or getattr(entry, "updated", None)
        items.append(
            RawItem(
                title=title.strip(),
                url=link.strip(),
                source=str(name),
                published=str(published) if published else None,
                snippet=str(summary).strip()[:500],
                source_type="rss",
            )
        )
    return items


def fetch_sources(sources: list[Any]) -> tuple[list[RawItem], list[str]]:
    """Fetch configured sources; isolate failures per source."""
    items: list[RawItem] = []
    errors: list[str] = []
    for src in sources or []:
        if isinstance(src, str):
            url, name, stype = src, src, "rss"
        elif isinstance(src, dict):
            url = str(src.get("url") or "")
            name = str(src.get("name") or url)
            stype = str(src.get("type") or "rss")
        else:
            continue
        if not url:
            continue
        try:
            if stype in ("rss", "atom"):
                items.extend(fetch_rss(url, name))
            else:
                errors.append(f"unsupported source type '{stype}' for {url}")
        except Exception as exc:  # noqa: BLE001 — isolate source failures
            errors.append(f"{url}: {exc}")
    return items, errors
