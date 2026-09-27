#!/usr/bin/env python3
"""CLI entrypoint — primary interface (MCP optional)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure kit root is on path when run as script
KIT_ROOT = Path(__file__).resolve().parent
if str(KIT_ROOT) not in sys.path:
    sys.path.insert(0, str(KIT_ROOT))


def cmd_profile_show(_: argparse.Namespace) -> int:
    from store.profile import load_profile

    print(json.dumps(load_profile(), ensure_ascii=False, indent=2))
    return 0


def cmd_profile_init(_: argparse.Namespace) -> int:
    from store.paths import kit_root, profile_path
    from store.profile import empty_profile, save_profile

    example = kit_root() / "templates" / "profile.example.yaml"
    if example.exists() and not profile_path().exists():
        profile_path().write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        save_profile(empty_profile())
    print(f"Profil geschrieben: {profile_path()}")
    print(f"Fragebogen: {kit_root() / 'templates' / 'profile_questionnaire.md'}")
    return 0


def cmd_run(_: argparse.Namespace) -> int:
    from pipeline.run import run_pipeline

    result = run_pipeline()
    print(result["digest_markdown"])
    print("---")
    print(json.dumps(result.get("meta"), ensure_ascii=False, indent=2))
    return 0


def cmd_last(_: argparse.Namespace) -> int:
    from store.paths import last_result_path

    p = last_result_path()
    if not p.exists():
        print("Kein last_result.json — zuerst `run` ausführen.", file=sys.stderr)
        return 1
    print(p.read_text(encoding="utf-8"))
    return 0


def cmd_targets(_: argparse.Namespace) -> int:
    from adapters.registry import list_output_targets

    print(json.dumps(list_output_targets(), ensure_ascii=False, indent=2))
    return 0


def cmd_feedback(args: argparse.Namespace) -> int:
    from store.feedback import append_feedback

    relevant = args.relevant.lower() in ("1", "true", "yes", "y", "ja")
    record = append_feedback(args.theme_id, relevant, args.reason or "")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="info-intel",
        description="Portable Info Intelligence Kit (CLI-first, MCP optional)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("profile-show", help="Profil anzeigen")
    sp.set_defaults(func=cmd_profile_show)

    sp = sub.add_parser("profile-init", help="Profil aus Vorlage anlegen")
    sp.set_defaults(func=cmd_profile_init)

    sp = sub.add_parser("run", help="Info-Lauf starten")
    sp.set_defaults(func=cmd_run)

    sp = sub.add_parser("last-result", help="Letztes Ergebnis anzeigen")
    sp.set_defaults(func=cmd_last)

    sp = sub.add_parser("list-targets", help="Output-Ziele listen")
    sp.set_defaults(func=cmd_targets)

    sp = sub.add_parser("feedback", help="Feedback zu einem Thema speichern")
    sp.add_argument("theme_id")
    sp.add_argument("relevant", help="true/false oder ja/nein")
    sp.add_argument("--reason", default="")
    sp.set_defaults(func=cmd_feedback)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
