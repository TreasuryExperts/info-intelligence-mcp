# Profil-Fragebogen (für die KI)

Die KI stellt diese Fragen nacheinander und schreibt die Antworten in `data/profile.yaml`
(gleiches Schema wie `profile.example.yaml`). Alternativ: Vorlage selbst ausfüllen.

## Fragen

1. **Profil-ID** — Kurzname für dieses Profil? (z. B. `lena`, `annette`)
2. **Themen** — Welche Informationsthemen sollen beobachtet werden? (Liste mit Kurz-ID und Namen)
3. **Schlüsselwörter** — Pro Thema: welche Wörter/Signale erhöhen die Relevanz?
4. **Relevanzkriterien** — Woran merkst du, dass etwas wichtig ist? (Cashflow, Regulierung, Wettbewerb, …)
5. **Quellen** — Welche RSS-/Feed-URLs oder bekannten Quellen soll das Kit nutzen? (frei zugänglich)
6. **Output-Ziele** — Welche Ziele aktivieren? Mindestens `digest_file`. Optionale Plätze (z. B. `zoho`) nur markieren, wenn später gewünscht — in V1 nicht implementiert.
7. **Gewichtung** — Welche Themen haben höhere Priorität? (0–1)

## Regeln

- Keine Paywall-Scraping-Quellen.
- TTE-Zettelkasten ist kein Output-Ziel.
- Nach dem Fragebogen: Datei speichern, dann `python cli.py run`.
