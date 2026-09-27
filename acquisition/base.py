from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class RawItem:
    title: str
    url: str
    source: str
    published: str | None = None
    snippet: str = ""
    source_type: str = "rss"  # rss | http_json | other

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
