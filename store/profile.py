from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

from store.paths import profile_path

DEFAULT_PROFILE: dict[str, Any] = {
    "profile_id": "default",
    "topics": [],
    "relevance_criteria": [],
    "sources": [],
    "outputs": [{"id": "digest_file", "enabled": True}],
}


def empty_profile() -> dict[str, Any]:
    return deepcopy(DEFAULT_PROFILE)


def load_profile(path: Path | None = None) -> dict[str, Any]:
    p = path or profile_path()
    if not p.exists():
        return empty_profile()
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    merged = empty_profile()
    merged.update(data)
    if "outputs" not in data:
        merged["outputs"] = deepcopy(DEFAULT_PROFILE["outputs"])
    return merged


def save_profile(profile: dict[str, Any], path: Path | None = None) -> Path:
    p = path or profile_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    out = empty_profile()
    out.update(profile)
    p.write_text(
        yaml.safe_dump(out, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return p


def upsert_profile(updates: dict[str, Any], path: Path | None = None) -> dict[str, Any]:
    current = load_profile(path)
    for key, value in updates.items():
        if value is None:
            continue
        current[key] = value
    save_profile(current, path)
    return current


def enabled_outputs(profile: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for item in profile.get("outputs") or []:
        if isinstance(item, dict) and item.get("enabled"):
            oid = item.get("id")
            if oid:
                result.append(str(oid))
        elif isinstance(item, str):
            result.append(item)
    return result
