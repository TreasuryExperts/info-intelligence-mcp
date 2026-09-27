from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from store.profile import empty_profile, enabled_outputs, load_profile, save_profile


def test_profile_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("INFO_INTEL_DATA", str(tmp_path))
    # reload paths binding via explicit path arg
    profile = empty_profile()
    profile["profile_id"] = "test"
    profile["topics"] = [{"id": "x", "name": "X", "keywords": ["x"], "weight": 0.6}]
    path = tmp_path / "profile.yaml"
    save_profile(profile, path)
    loaded = load_profile(path)
    assert loaded["profile_id"] == "test"
    assert enabled_outputs(loaded) == ["digest_file"]


def test_unknown_output_id_persistable(tmp_path):
    profile = empty_profile()
    profile["outputs"] = [
        {"id": "digest_file", "enabled": True},
        {"id": "zoho", "enabled": True},
    ]
    path = tmp_path / "profile.yaml"
    save_profile(profile, path)
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    ids = [o["id"] for o in loaded["outputs"]]
    assert "zoho" in ids
