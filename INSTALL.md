# noah installieren

Ein Installer für den eigenen ARK-ASA-Servermanager.
Alles läuft lokal, Python-Standardbibliothek plus SteamCMD und Wine.

## Voraussetzungen

| Was | Warum | Prüfen |
|---|---|---|
| Linux (x86_64) | getestet auf CachyOS/Arch | `uname -m` |
| Python ≥ 3.10 | Programm läuft damit | `python3 -V` |
| Wine ≥ 8 | führt die Windows-Serverdateien aus | `wine --version` |
| ~30 GB Platz pro Instanz | 12,4 GB Download + Sicherungen | `df -h ~` |
| ~4 GB RAM leer ohne Mods, 11–12 GB mit Mods/Welt/Spielern (nach oben offen) | ARK braucht das | `free -g` |

Fehlt Wine:

```bash
sudo pacman -S wine           # Arch / CachyOS
sudo apt install wine         # Debian / Ubuntu
```

SteamCMD wird beim ersten Installieren automatisch nach `~/steamcmd` geladen — kein root nötig.

## Sprache

Der Installer fragt zuerst:

```
Sprache / Language:  [1] Deutsch  [2] English   [1]
```

Ohne Rueckfrage: `./install.sh --lang en` oder `NOAH_LANG=en ./install.sh`.
Gespeichert wird das in `~/.config/noah/settings.json`. Spaeter jederzeit umstellbar:

- `noah lang en` / `noah lang de`
- Weboberflaeche: Knopf oben rechts (`EN` / `DE`)

## Installation

```bash
git clone https://github.com/Ronny-H-79/Noah.git noah   # oder Ordner kopieren
cd noah          # dieser Ordner enthaelt install.sh - NICHT noah/noah (das ist das Python-Paket)
cd noah
./install.sh --check        # nur pruefen, was fehlt (aendert nichts)
./install.sh                # installieren, fragt bei fehlenden Paketen nach
./install.sh --auto         # fehlende Pakete ohne Rueckfrage installieren (sudo)
./install.sh --wizard       # installieren und danach den Assistenten starten
```

Fehlende Pakete (z. B. Wine) erkennt der Installer über `pacman`, `apt`, `dnf` oder `zypper` und
installiert sie auf Wunsch per `sudo` nach. Ohne Rueckfrage laesst sich das mit `--auto` erzwingen.

Der Installer prüft Python und Wine, kopiert die Programmdateien, legt den Befehl `noah` an
und richtet `~/.config/noah` ein. Er braucht **keine** root-Rechte.

## Web-Dienst (optional)

Der Installer fragt: „Web-Oberflaeche automatisch starten (systemd-Dienst)?" Mit `j` legt er als
**root** einen Systemdienst `/etc/systemd/system/noah-web.service` an (`WantedBy=multi-user.target`,
startet beim Booten) — als normaler Benutzer stattdessen `~/.config/systemd/user/noah-web.service`
(`systemctl --user enable --now`).
Ohne Zustimmung startet man die Oberflaeche bei Bedarf mit `noah web`.

## Zugriff von woanders

Standardsmaessig nur `127.0.0.1`. Von einem anderen Rechner per SSH-Tunnel:
`ssh -N -L 8790:127.0.0.1:8790 nutzer@server`, dann `http://127.0.0.1:8790/?token=…` oeffnen.
Im LAN/VPN: `noah web --host 0.0.0.0`. Aus dem Internet per nginx mit HTTPS:
`sudo noah proxy --domain noah.example.de --write --cert` (schreibt die Config, prueft mit `nginx -t`,
laedt nginx neu und holt das Zertifikat). Ohne nginx geht auch HTTPS direkt:
`noah web --tls-cert cert.pem --tls-key key.pem`. Details im README.

## Sicherheit (kurz)

Die Oberflaeche ist eine Administrationskonsole: **wer den Token hat, kann alles steuern** - Server
starten, stoppen, loeschen, Mods eintragen, Konsolenbefehle absetzen. Deshalb:

- Client-Installation (Modus `[1]`) und Server mit Domain (Modus `[2]`): noah bleibt auf `127.0.0.1`,
  der Zugang laeuft ueber SSH-Tunnel bzw. nginx mit HTTPS. Nur Modus `[3]` bindet direkt nach aussen.
- **Nicht unverschluesselt ins Internet stellen.** Bei `--host 0.0.0.0` ohne TLS wandert der Token im
  Klartext ueber jede Zwischenstation. Fuer oeffentlichen Zugriff HTTPS per `noah proxy` oder TLS direkt.
- Der Installer warnt bei Modus `[3]` (IP und Port) und fragt vorher nach.

Ausfuehrlich, inklusive was noah selbst absichert: `docs/zugriff.md`, Abschnitt „Sicherheit".

## Der Token

Nach der Installation zeigt `noah url` die Adresse mit Token an, z. B.
`http://127.0.0.1:8790/?token=…`. Der Schlüssel liegt in `~/.config/noah/token` (Rechte 0600) und
schuetzt die Oberflaeche davor, dass eine beliebige Webseite in deinem Browser Befehle an
`127.0.0.1` schickt (ohne Token: `HTTP 401`). Details im README, Abschnitt „Der Token".
Token zuruecksetzen: Datei loeschen, beim naechsten Start entsteht ein neuer.

## Einrichten

```bash
noah wizard
```

Der Assistent fragt Name, Map, Port und Session-Name, legt die Instanz an und bietet an,
die Serverdateien zu laden (~12,4 GB, 10–30 Minuten) und einen systemd-Dienst einzurichten.

## Benutzen

```bash
noah web                    # Weboberfläche starten
noah url                    # fertige Adresse inklusive Token anzeigen
noah status                 # Prozess, RCON, letzte Logzeile
noah start --wait 240
noah stop                   # SaveWorld → DoExit → SIGTERM
noah update --check         # ist ein Steam-Build verfügbar?
noah supervise --all        # Auto-Restart, geplante Neustarts, Backups
```

Die Web-Oberfläche zeigt ein Dashboard mit allen Instanzen (Status, CPU, RAM, Spieler),
pro Instanz Start/Stop/Update, Klick-Befehle für RCON, Spielerverwaltung, Whitelist/Bans,
Mod-Verwaltung mit Bildern, Einstellungen als Formular, Backups, Snapshots und Zeitplan.

## Autostart

```bash
systemctl --user daemon-reload
systemctl --user enable --now noah-<name>
loginctl enable-linger $USER      # läuft auch ohne angemeldete Sitzung
```

## Deinstallieren

```bash
./install.sh --uninstall
```

Entfernt Programm und Launcher. **Bleiben:** Instanzen (`~/arkserver-*`), Einstellungen
(`~/.config/noah`), Backups (`~/noah-backups`), Snapshots (`~/noah-snapshots`).

## Wo was liegt

| Pfad | Inhalt |
|---|---|
| `~/.local/share/noah` | Programm |
| `~/.local/bin/noah` | Launcher |
| `~/.config/noah/<name>.json` | Instanz-Konfiguration |
| `~/.config/noah/token` | Web-Token (0600) |
| `~/arkserver-<name>` | Serverdateien der Instanz |
| `~/noah-backups/<name>` | Welt-Backups (tar.gz) |
| `~/noah-snapshots/<name>` | vollständige Instanz-Snapshots (Rollback nach Update) |
