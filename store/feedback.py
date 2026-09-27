from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from store.memory import apply_feedback_to_memory, load_memory, save_memory
from store.paths import feedback_path
from store.profile import load_profile, save_profile


def append_feedback(
    theme_id: str,
    relevant: bool,
    reason: str = "",
    path: Path | None = None,
) -> dict[str, Any]:
    record = {
        "theme_id": theme_id,
        "relevant": relevant,
        "reason": reason,
        "at": datetime.now(timezone.utc).isoformat(),
    }
    p = path or feedback_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    memory = load_memory()
    apply_feedback_to_memory(memory, theme_id, relevant, reason)
    save_memory(memory)

    # Soft-adjust topic weights in profile when topic id matches a topic name/id
    profile = load_profile()
    topics = profile.get("topics") or []
    changed = False
    for topic in topics:
        if not isinstance(topic, dict):
            continue
        tid = str(topic.get("id") or topic.get("name") or "")
        if tid != theme_id:
            continue
        weight = float(topic.get("weight", 0.5))
        weight = max(0.0, min(1.0, weight + (0.1 if relevant else -0.2)))
        topic["weight"] = weight
        changed = True
    if changed:
        save_profile(profile)

    return record
