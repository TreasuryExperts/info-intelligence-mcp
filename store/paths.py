from __future__ import annotations

import os
from pathlib import Path


def kit_root() -> Path:
    return Path(__file__).resolve().parents[1]


def data_root(override: str | None = None) -> Path:
    if override:
        root = Path(override)
    else:
        env = os.environ.get("INFO_INTEL_DATA")
        root = Path(env) if env else kit_root() / "data"
    root.mkdir(parents=True, exist_ok=True)
    return root


def profile_path(data: Path | None = None) -> Path:
    return (data or data_root()) / "profile.yaml"


def memory_path(data: Path | None = None) -> Path:
    return (data or data_root()) / "memory.yaml"


def feedback_path(data: Path | None = None) -> Path:
    return (data or data_root()) / "feedback.jsonl"


def runs_dir(data: Path | None = None) -> Path:
    d = (data or data_root()) / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def last_result_path(data: Path | None = None) -> Path:
    return (data or data_root()) / "last_result.json"
