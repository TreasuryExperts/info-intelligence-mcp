from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from acquisition.router import fetch_for_profile
from adapters.registry import deliver
from pipeline.quality import build_theme_items
from pipeline.render import render_canonical
from store.memory import load_memory, note_theme_reported, save_memory
from store.paths import last_result_path, runs_dir
from store.profile import enabled_outputs, load_profile


def run_pipeline(data_dir: Path | None = None) -> dict[str, Any]:
    profile = load_profile()
    memory = load_memory()
    raw_items, errors = fetch_for_profile(profile)
    themes = build_theme_items(raw_items, profile, memory)
    result = render_canonical(
        profile,
        themes,
        meta_extra={
            "raw_count": len(raw_items),
            "theme_count": len(themes),
            "acquisition_errors": errors,
        },
    )

    for theme in themes:
        note_theme_reported(memory, theme["theme_id"], theme["headline"])
    save_memory(memory)

    run_id = result["run_id"]
    out_dir = runs_dir(data_dir) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "digest.md").write_text(result["digest_markdown"], encoding="utf-8")
    (out_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    last_result_path(data_dir).write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    delivery = deliver(enabled_outputs(profile), result, out_dir)
    result["meta"]["delivery"] = delivery
    # refresh saved artifacts with delivery meta
    (out_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    last_result_path(data_dir).write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return result
