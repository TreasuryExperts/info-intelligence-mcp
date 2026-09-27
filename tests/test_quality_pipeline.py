from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from acquisition.base import RawItem
from pipeline.quality import build_theme_items, score_item


def test_irrelevant_low_score():
    profile = {
        "topics": [{"id": "makro", "name": "Makro", "keywords": ["ezb", "inflation"], "weight": 0.8}],
        "relevance_criteria": [],
    }
    memory = {"themes": {}}
    item = RawItem(
        title="Promi eröffnet Boutique",
        url="https://example.com/x",
        source="tabloid",
        snippet="Mode und Rotteppich",
        source_type="rss",
    )
    score, theme_id, flags = score_item(item, profile, memory)
    assert score < 0.25


def test_relevant_clusters():
    profile = {
        "topics": [{"id": "makro", "name": "Makro", "keywords": ["ezb", "zinsen"], "weight": 0.8}],
    }
    memory = {"themes": {}}
    items = [
        RawItem("EZB hält Zinsen", "https://a", "Tagesschau", snippet="Leitzins", source_type="rss"),
        RawItem("EZB-Aussagen zu Zinsen", "https://b", "BBC", snippet="Zinsen unverändert", source_type="rss"),
    ]
    themes = build_theme_items(items, profile, memory, min_score=0.2)
    assert len(themes) == 1
    assert themes[0]["theme_id"] == "makro"
    assert themes[0]["fact"]
    assert themes[0]["interpretation"]
    assert themes[0].get("forecast") is None
