# Unified Promise Registry (UPR)

## Ziel
Eine gemeinsame, datenschutzkonforme Brücke zwischen GPT und Perplexity, um Versprechen, Aufgaben und Statusmeldungen transparent und automatisiert zu verwalten.

---

## Struktur der Datei `open_promises.json`
Jedes Element repräsentiert ein offenes oder abgeschlossenes Versprechen.

### Felder
| Feld | Bedeutung |
|------|------------|
| `id` | Eindeutige Kennung für das Versprechen |
| `context` | Themenbereich oder Projektname |
| `owner` | System, das das Versprechen erstellt hat |
| `partner` | System, das ebenfalls Zugriff auf den Eintrag hat |
| `description` | Kurzbeschreibung der Aufgabe |
| `created_at` / `last_checked` | Zeitstempel für Erstellung und letzte Prüfung |
| `deadline` | Optionales Fälligkeitsdatum |
| `condition` | Logische Bedingung, wann als erledigt gilt |
| `status` | open, in_progress, done, irrelevant |
| `relevance` | high, medium, low, none |
| `notes` | Hinweise oder Zusatzinfos |
| `last_action_by` | Wer zuletzt geändert hat |
| `history` | Protokoll der Statusänderungen |

---

## Logik
1. Beide Systeme (GPT & Perplexity) dürfen die Datei lesen und schreiben.
2. Polling-Intervall: Empfohlen alle 1–5 Minuten.
3. Wenn `condition` erfüllt ist → `status = done`.
4. Wenn `relevance = none` → Eintrag wird gelöscht oder archiviert.
5. Alle Änderungen werden in `history` dokumentiert.

---

## Nutzung
- Speicherung z. B. in gemeinsamem Cloud-Ordner oder via API.
- Keine personenbezogenen Daten.
- Änderungen sind transparent und versionierbar.

---

© 2025 Unified Prototype – Open Agent Collaboration
