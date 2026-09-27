#!/usr/bin/env python3
"""Optional MCP server — mirrors CLI operations. Not required to use the kit."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

KIT_ROOT = Path(__file__).resolve().parent
if str(KIT_ROOT) not in sys.path:
    sys.path.insert(0, str(KIT_ROOT))

try:
    from mcp.server.mcpserver import MCPServer
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "mcp package missing. Install requirements or use CLI only: python cli.py --help"
    ) from exc

server = MCPServer(
    "info-intelligence",
    instructions=(
        "Portable Info Intelligence Kit. "
        "Profil, Lauf, Ergebnis und Feedback. "
        "CLI ist der Standardweg; dieser MCP-Server ist optional."
    ),
)


@server.tool(name="get_profile", description="Aktuelles Nutzerprofil laden")
def get_profile() -> dict[str, Any]:
    from store.profile import load_profile

    return load_profile()


@server.tool(name="upsert_profile", description="Profilfelder aktualisieren (JSON-Objekt)")
def upsert_profile(updates_json: str) -> dict[str, Any]:
    from store.profile import upsert_profile as _upsert

    updates = json.loads(updates_json)
    return _upsert(updates)


@server.tool(name="run_now", description="Info-Lauf jetzt starten")
def run_now() -> dict[str, Any]:
    from pipeline.run import run_pipeline

    return run_pipeline()


@server.tool(name="get_last_result", description="Letztes kanonisches Ergebnis")
def get_last_result() -> dict[str, Any]:
    from store.paths import last_result_path

    p = last_result_path()
    if not p.exists():
        return {"error": "no_result"}
    return json.loads(p.read_text(encoding="utf-8"))


@server.tool(name="submit_feedback", description="Feedback zu einem theme_id")
def submit_feedback(theme_id: str, relevant: bool, reason: str = "") -> dict[str, Any]:
    from store.feedback import append_feedback

    return append_feedback(theme_id, relevant, reason)


@server.tool(name="list_output_targets", description="Output-Ziele inkl. Optionsplätze")
def list_output_targets() -> dict[str, Any]:
    from adapters.registry import list_output_targets as _list

    return {"targets": _list()}


if __name__ == "__main__":
    server.run()
