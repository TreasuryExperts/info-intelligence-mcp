from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.registry import deliver, list_output_targets
from pipeline.render import render_canonical


def test_list_targets_includes_optional_zoho():
    targets = list_output_targets()
    by_id = {t["id"]: t for t in targets}
    assert by_id["digest_file"]["status"] == "implemented"
    assert by_id["zoho"]["status"] == "optional_unimplemented"


def test_fanout_unavailable_zoho(tmp_path):
    result = render_canonical(
        {"profile_id": "t"},
        [
            {
                "theme_id": "makro",
                "headline": "Test",
                "fact": "Test",
                "interpretation": "x",
                "forecast": None,
                "relevance_score": 0.9,
                "sources": [],
                "uncertainty_flags": [],
            }
        ],
    )
    reports = deliver(["digest_file", "zoho"], result, tmp_path)
    statuses = {r["id"]: r["status"] for r in reports}
    assert statuses["digest_file"] == "ok"
    assert statuses["zoho"] == "unavailable"
    assert (tmp_path / "digest.md").exists()
