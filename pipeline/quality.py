from __future__ import annotations

import hashlib
import re
from typing import Any

from acquisition.base import RawItem


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß]+", "-", text.lower()).strip("-")
    return s[:60] or "theme"


def _topic_terms(profile: dict[str, Any]) -> list[tuple[str, float, list[str]]]:
    """Return (topic_id, weight, keywords)."""
    out: list[tuple[str, float, list[str]]] = []
    for topic in profile.get("topics") or []:
        if isinstance(topic, str):
            out.append((topic, 0.5, [topic.lower()]))
            continue
        if not isinstance(topic, dict):
            continue
        tid = str(topic.get("id") or topic.get("name") or "topic")
        weight = float(topic.get("weight", 0.5))
        keywords = topic.get("keywords") or [topic.get("name") or tid]
        kws = [str(k).lower() for k in keywords if k]
        criteria = profile.get("relevance_criteria") or []
        for c in criteria:
            if isinstance(c, str):
                kws.append(c.lower())
        out.append((tid, weight, kws))
    return out


def score_item(
    item: RawItem,
    profile: dict[str, Any],
    memory: dict[str, Any],
) -> tuple[float, str, list[str]]:
    """Return relevance score, matched theme_id, uncertainty flags."""
    text = f"{item.title} {item.snippet}".lower()
    flags: list[str] = []
    if item.source_type not in ("rss", "atom", "http_json"):
        flags.append("non_structured_source")

    topics = _topic_terms(profile)
    best_id = "general"
    best = 0.15  # base curiosity score
    if not topics:
        best = 0.4
        best_id = _slug(item.title) or "general"
    else:
        for tid, weight, kws in topics:
            hits = sum(1 for k in kws if k and k in text)
            if hits:
                score = min(1.0, 0.3 + 0.2 * hits) * (0.5 + weight)
                if score > best:
                    best = score
                    best_id = tid

    themes = (memory or {}).get("themes") or {}
    mem = themes.get(best_id) or {}
    priority = float(mem.get("priority", 0.5))
    best = max(0.0, min(1.0, best * (0.6 + 0.8 * priority)))

    # Repeat suppression: same headline already summarized
    last_summary = str(mem.get("summary") or "").lower()
    if last_summary and item.title.lower() in last_summary:
        best *= 0.35
        flags.append("possible_repeat")

    if not item.url:
        flags.append("missing_url")
        best *= 0.5

    return best, best_id, flags


def build_theme_items(
    raw_items: list[RawItem],
    profile: dict[str, Any],
    memory: dict[str, Any],
    min_score: float = 0.25,
) -> list[dict[str, Any]]:
    buckets: dict[str, list[tuple[float, RawItem, list[str]]]] = {}
    for item in raw_items:
        score, theme_id, flags = score_item(item, profile, memory)
        if score < min_score:
            continue
        buckets.setdefault(theme_id, []).append((score, item, flags))

    themes_out: list[dict[str, Any]] = []
    for theme_id, rows in buckets.items():
        rows.sort(key=lambda r: r[0], reverse=True)
        top_score, top_item, flags = rows[0]
        sources = []
        for score, item, _ in rows[:5]:
            sources.append(
                {
                    "title": item.title,
                    "url": item.url,
                    "source": item.source,
                    "published": item.published,
                    "source_type": item.source_type,
                }
            )
        fact = top_item.title.strip()
        interpretation = (
            f"Passend zu Profil-Thema '{theme_id}' "
            f"(Relevanz {top_score:.2f}, {len(rows)} Meldung(en))."
        )
        themes_out.append(
            {
                "theme_id": theme_id,
                "headline": fact,
                "fact": fact,
                "interpretation": interpretation,
                "forecast": None,
                "relevance_score": round(top_score, 3),
                "sources": sources,
                "uncertainty_flags": sorted(set(flags)),
            }
        )

    themes_out.sort(key=lambda t: t["relevance_score"], reverse=True)
    return themes_out
