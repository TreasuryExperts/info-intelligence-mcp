from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from acquisition.base import RawItem
from acquisition.rss import fetch_sources


def test_fetch_rss_fixture(monkeypatch):
    class FakeFeed:
        feed = type("F", (), {"title": "Fixture"})()
        entries = [
            type(
                "E",
                (),
                {
                    "title": "EZB hält Zinsen",
                    "link": "https://example.com/1",
                    "summary": "Leitzins unverändert",
                    "published": "2026-09-01",
                },
            )()
        ]

    monkeypatch.setattr("acquisition.rss.feedparser.parse", lambda url: FakeFeed())
    items, errors = fetch_sources(
        [{"url": "https://example.com/rss", "name": "Fixture", "type": "rss"}]
    )
    assert not errors
    assert items[0].title.startswith("EZB")
    assert items[0].source_type == "rss"


def test_source_failure_isolated(monkeypatch):
    def boom(url):
        raise RuntimeError("network")

    monkeypatch.setattr("acquisition.rss.feedparser.parse", boom)
    items, errors = fetch_sources(
        [{"url": "https://bad.example/rss", "name": "Bad", "type": "rss"}]
    )
    assert items == []
    assert errors
