# Feedback-Checkliste (ohne MCP / ohne Cursor)

Nach einem Lauf (`data/runs/<run_id>/digest.md`):

Für jedes Thema:

```text
theme_id: <aus dem Digest>
relevant: ja | nein
reason: <kurz warum>
```

Dann CLI:

```bash
python cli.py feedback <theme_id> ja --reason "..."
# oder
python cli.py feedback <theme_id> nein --reason "..."
```

Oder Zeilen in `data/feedback.jsonl` — CLI ist der unterstützte Weg.
