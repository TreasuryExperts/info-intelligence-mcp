from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class Adapter(Protocol):
    id: str

    def deliver(self, result: dict[str, Any], run_dir: Path) -> dict[str, Any]:
        ...
