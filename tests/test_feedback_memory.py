from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from store.feedback import append_feedback
from store.memory import load_memory, save_memory
from store.profile import empty_profile, save_profile


def test_feedback_lowers_priority(tmp_path, monkeypatch):
    monkeypatch.setenv("INFO_INTEL_DATA", str(tmp_path))
    profile = empty_profile()
    profile["topics"] = [{"id": "makro", "name": "Makro", "keywords": ["ezb"], "weight": 0.8}]
    save_profile(profile)
    save_memory({"themes": {"makro": {"priority": 0.8, "summary": "", "feedback": []}}})

    append_feedback("makro", False, "nicht relevant für mich")
    mem = load_memory()
    assert mem["themes"]["makro"]["priority"] < 0.8
