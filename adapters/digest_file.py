from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DigestFileAdapter:
    id = "digest_file"

    def deliver(self, result: dict[str, Any], run_dir: Path) -> dict[str, Any]:
        md = run_dir / "digest.md"
        js = run_dir / "result.json"
        md.write_text(result.get("digest_markdown") or "", encoding="utf-8")
        js.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "id": self.id,
            "status": "ok",
            "paths": {"digest": str(md), "json": str(js)},
        }
