from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from store.paths import memory_path

DEFAULT_MEMORY: dict[str, Any] = {"themes": {}}


def load_memory(path: Path | None = None) -> dict[str, Any]:
    p = path or memory_path()
    if not p.exists():
        return deepcopy(DEFAULT_MEMORY)
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    themes = data.get("themes") or {}
    return {"themes": themes}


def save_memory(memory: dict[str, Any], path: Path | None = None) -> Path:
    p = path or memory_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        yaml.safe_dump(memory, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return p


def apply_feedback_to_memory(
    memory: dict[str, Any],
    theme_id: str,
    relevant: bool,
    reason: str = "",
) -> dict[str, Any]:
    themes = memory.setdefault("themes", {})
    entry = themes.setdefault(
        theme_id,
        {
            "priority": 0.5,
            "last_seen": None,
            "summary": "",
            "feedback": [],
        },
    )
    delta = 0.15 if relevant else -0.25
    entry["priority"] = max(0.0, min(1.0, float(entry.get("priority", 0.5)) + delta))
    entry.setdefault("feedback", []).append(
        {
            "relevant": relevant,
            "reason": reason,
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return memory


def note_theme_reported(
    memory: dict[str, Any],
    theme_id: str,
    summary: str,
) -> dict[str, Any]:
    themes = memory.setdefault("themes", {})
    entry = themes.setdefault(
        theme_id,
        {"priority": 0.5, "last_seen": None, "summary": "", "feedback": []},
    )
    entry["last_seen"] = datetime.now(timezone.utc).isoformat()
    entry["summary"] = summary
    return memory
