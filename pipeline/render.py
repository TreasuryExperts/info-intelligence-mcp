from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def render_canonical(
    profile: dict[str, Any],
    themes: list[dict[str, Any]],
    meta_extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    lines = [
        f"# Info Digest — {run_id}",
        "",
        f"Profil: `{profile.get('profile_id', 'default')}`",
        "",
    ]
    if not themes:
        lines.append("_Keine Themen oberhalb der Relevanzschwelle._")
    for i, theme in enumerate(themes, 1):
        lines.append(f"## {i}. {theme['headline']}")
        lines.append("")
        lines.append(f"- **Fakt:** {theme['fact']}")
        if theme.get("interpretation"):
            lines.append(f"- **Einordnung:** {theme['interpretation']}")
        if theme.get("forecast"):
            lines.append(f"- **Prognose:** {theme['forecast']}")
        else:
            lines.append("- **Prognose:** — (keine)")
        lines.append(f"- **Relevanz:** {theme['relevance_score']}")
        flags = theme.get("uncertainty_flags") or []
        if flags:
            lines.append(f"- **Unsicherheit:** {', '.join(flags)}")
        for src in theme.get("sources") or []:
            lines.append(f"- Quelle: [{src.get('source')}]({src.get('url')})")
        lines.append("")

    digest = "\n".join(lines).strip() + "\n"
    return {
        "run_id": run_id,
        "profile_id": profile.get("profile_id", "default"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "items": themes,
        "digest_markdown": digest,
        "structured": {"items": themes},
        "meta": meta_extra or {},
    }


def dumps_canonical(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)
