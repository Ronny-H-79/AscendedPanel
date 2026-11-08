# Technik

Aufbau, Benutzung auf der Konsole, Stop-Reihenfolge und Hinweise für Entwickler.

[← zurück zum README](../README.de.md) · [English](technik.md)

## Benutzung

```bash
noah web               # Weboberfläche auf http://127.0.0.1:8790
noah url               # fertige Adresse inklusive Token
noah status            # Prozess, RCON, letzte Logzeile
noah start --wait 240
noah stop              # SaveWorld → DoExit → SIGTERM → SIGKILL
noah update --check    # ist ein neuer Steam-Build verfügbar?
noah supervise --all   # Auto-Restart, Zeitplan, Backups
```

## Aufbau

| Datei | Aufgabe |
|---|---|
| `noah/instance.py` | Instanz-Konfiguration (JSON), Pfade, INI-Schreiben, Startparameter |
| `noah/runner.py` | Start/Stop/Status/Update, RCON-Shutdown, Wartungssperre |
| `noah/consoled.py` | startet den Server am PTY, damit Wine kein Fenster öffnet |
| `noah/rcon.py` | eigener Source-RCON-Client |
| `noah/supervisor.py` | Health-Check, Auto-Restart, Zeitplan, Countdown |
| `noah/registry.py` | mehrere Instanzen, Portvergabe, Kennzahlen |
| `noah/mods.py` · `whitelist.py` · `config.py` · `backups.py` · `snapshots.py` | Fachmodule |
| `noah/webui.py` | Dashboard, Instanzseiten, JSON-API (stdlib `http.server`) |
| `noah/cli.py` | Kommandozeile inkl. `wizard` |

## Stop-Reihenfolge (bewusst so)

1. RCON `SaveWorld` — Spielstand sichern
2. RCON `DoExit` — reguläres Beenden
3. `SIGTERM` an die Prozessgruppe
4. `SIGKILL`

Ein `kill` ohne Schritt 1 kostet den Fortschritt seit dem letzten Autosave.

Hinweise für Mitentwickler: [entwicklung.md](entwicklung.md)
