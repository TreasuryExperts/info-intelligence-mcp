# Portable Info Intelligence Kit

Setup-unabhängiges Kit für persönliche Informationsbeschaffung aus dem Internet.

**CLI ist der Standardweg. MCP ist optional.** Kein Cursor-Zwang. Kein TTE-Zettelkasten. Zoho nur Optionsplatz (nicht implementiert).

## Voraussetzungen

- Python 3.11+
- Internetzugang für Feeds

```bash
cd tools/info-intelligence-mcp   # oder Clone dieses Repos
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

## Schnellstart (ohne MCP)

1. Profil anlegen (Vorlage):

```bash
python cli.py profile-init
```

2. Oder **Fragebogen**: `templates/profile_questionnaire.md` — die KI stellt die Fragen und schreibt `data/profile.yaml`.

3. Profil prüfen / anpassen: `data/profile.yaml`

4. Lauf starten:

```bash
python cli.py run
```

5. Ergebnis: `data/runs/<run_id>/digest.md` und `result.json`

6. Feedback:

```bash
python cli.py feedback makro nein --reason "zu allgemein"
```

Weitere Befehle: `profile-show`, `last-result`, `list-targets`.

Datenverzeichnis: Standard `./data`, oder `INFO_INTEL_DATA=...`.

## Optional: MCP

Wenn der Client MCP kann:

```bash
python server.py
```

Tools: `get_profile`, `upsert_profile`, `run_now`, `get_last_result`, `submit_feedback`, `list_output_targets`.

Dieselben Dateien wie die CLI — kein zweites Silo.

## Architektur

| Schicht | Aufgabe |
|--------|---------|
| A `acquisition/` | RSS/HTTP-Rohdaten |
| B `pipeline/` | Quality, Digest+JSON, Run |
| `adapters/` | Registry; V1: `digest_file` |
| `store/` | Profil, Gedächtnis, Feedback |
| `cli.py` | Pflicht-Einstieg |
| `server.py` | Optionaler MCP-Spiegel |

## Tests

```bash
pytest
```

## Lizenz / Weitergabe

Mitnehmbar für FFC und andere Setups. GitHub ist die Quellcode-Wahrheit.
