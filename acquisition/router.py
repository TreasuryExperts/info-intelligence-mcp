from __future__ import annotations

from typing import Any

from acquisition.base import RawItem
from acquisition.rss import fetch_sources


def fetch_for_profile(profile: dict[str, Any]) -> tuple[list[RawItem], list[str]]:
    sources = list(profile.get("sources") or [])
    # If no explicit sources, use topic-linked source hints when present
    if not sources:
        for topic in profile.get("topics") or []:
            if isinstance(topic, dict) and topic.get("source_url"):
                sources.append(
                    {
                        "url": topic["source_url"],
                        "name": topic.get("name") or topic.get("id") or "topic",
                        "type": "rss",
                    }
                )
    return fetch_sources(sources)
