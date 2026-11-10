# Technik

Aufbau, Benutzung auf der Konsole, Stop-Reihenfolge und Hinweise für Entwickler.

[← zurück zum README](../README.de.md) · [English](technik.md)

## Benutzung

```bash
ascendedpanel web               # Weboberfläche auf http://127.0.0.1:8790
ascendedpanel url               # fertige Adresse inklusive Token
ascendedpanel status            # Prozess, RCON, letzte Logzeile
ascendedpanel start --wait 240
ascendedpanel stop              # SaveWorld → DoExit → SIGTERM → SIGKILL
ascendedpanel update --check    # ist ein neuer Steam-Build verfügbar?
ascendedpanel supervise --all   # Auto-Restart, Zeitplan, Backups
```

## Aufbau

| Datei | Aufgabe |
|---|---|
| `AscendedPanel/instance.py` | Instanz-Konfiguration (JSON), Pfade, INI-Schreiben, Startparameter |
| `AscendedPanel/runner.py` | Start/Stop/Status/Update, RCON-Shutdown, Wartungssperre |
| `AscendedPanel/consoled.py` | startet den Server am PTY, damit Wine kein Fenster öffnet |
| `AscendedPanel/rcon.py` | eigener Source-RCON-Client |
| `AscendedPanel/supervisor.py` | Health-Check, Auto-Restart, Zeitplan, Countdown |
| `AscendedPanel/registry.py` | mehrere Instanzen, Portvergabe, Kennzahlen |
| `AscendedPanel/mods.py` · `whitelist.py` · `config.py` · `backups.py` · `snapshots.py` | Fachmodule |
| `AscendedPanel/webui.py` | Dashboard, Instanzseiten, JSON-API (stdlib `http.server`) |
| `AscendedPanel/cli.py` | Kommandozeile inkl. `wizard` |

## Stop-Reihenfolge (bewusst so)

1. RCON `SaveWorld` — Spielstand sichern
2. RCON `DoExit` — reguläres Beenden
3. `SIGTERM` an die Prozessgruppe
4. `SIGKILL`

Ein `kill` ohne Schritt 1 kostet den Fortschritt seit dem letzten Autosave.

Hinweise für Mitentwickler: [entwicklung.md](entwicklung.md)
