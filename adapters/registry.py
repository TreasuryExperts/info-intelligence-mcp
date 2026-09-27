from __future__ import annotations

from pathlib import Path
from typing import Any

from adapters.digest_file import DigestFileAdapter

IMPLEMENTED = {
    DigestFileAdapter.id: DigestFileAdapter(),
}

# Documented optional slots — not implemented in V1
OPTIONAL_UNIMPLEMENTED = {
    "zoho": "CRM/Zoho connector — optional, not shipped in V1",
}


def list_output_targets() -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    for adapter_id, adapter in IMPLEMENTED.items():
        targets.append(
            {
                "id": adapter_id,
                "status": "implemented",
                "description": type(adapter).__name__,
            }
        )
    for oid, desc in OPTIONAL_UNIMPLEMENTED.items():
        targets.append({"id": oid, "status": "optional_unimplemented", "description": desc})
    return targets


def deliver(
    enabled_ids: list[str],
    result: dict[str, Any],
    run_dir: Path,
) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for oid in enabled_ids:
        adapter = IMPLEMENTED.get(oid)
        if adapter is None:
            reports.append(
                {
                    "id": oid,
                    "status": "unavailable",
                    "reason": OPTIONAL_UNIMPLEMENTED.get(
                        oid, "No adapter registered for this output id"
                    ),
                }
            )
            continue
        reports.append(adapter.deliver(result, run_dir))
    return reports
