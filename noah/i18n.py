"""Sprachverwaltung: Katalog, Einstellungen, Uebersetzung."""
from __future__ import annotations

import json
import os

CONFIG_PATH = os.path.expanduser("~/.config/noah/settings.json")
LANGS = ("de", "en")
DEFAULT = "de"

T: dict[str, dict[str, str]] = {
    # ---------------------------------------------------------------- allgemein
    "app.tagline": {"de": "ARK: Survival Ascended Servermanager",
                    "en": "ARK: Survival Ascended server manager"},
    "common.start": {"de": "Start", "en": "Start"},
    "common.stop": {"de": "Stop", "en": "Stop"},
    "common.restart": {"de": "Restart", "en": "Restart"},
    "common.update": {"de": "Update", "en": "Update"},
    "common.open": {"de": "Öffnen", "en": "Open"},
    "common.save": {"de": "Speichern", "en": "Save"},
    "common.delete": {"de": "Löschen", "en": "Delete"},
    "common.remove": {"de": "Entfernen", "en": "Remove"},
    "common.add": {"de": "Hinzufügen", "en": "Add"},
    "common.enable": {"de": "Aktivieren", "en": "Enable"},
    "common.disable": {"de": "Deaktivieren", "en": "Disable"},
    "common.send": {"de": "Senden", "en": "Send"},
    "common.info": {"de": "Info", "en": "Info"},
    "common.loading": {"de": "lädt …", "en": "loading …"},
    "common.none": {"de": "keine", "en": "none"},
    "common.yes": {"de": "ja", "en": "yes"},
    "common.no": {"de": "nein", "en": "no"},
    "common.back": {"de": "zurück", "en": "back"},
    "common.back_dashboard": {"de": "← Dashboard", "en": "← Dashboard"},
    "inst.control_hint": {"de": "Start, Restart, Stop und Update liegen auf dem Dashboard - hier siehst du, was die Instanz gerade tut.",
                          "en": "Start, restart, stop and update live on the dashboard - this page shows what the instance is doing."},
    "common.of": {"de": "von", "en": "of"},
    # ---------------------------------------------------------------- Status
    "status.running": {"de": "LÄUFT", "en": "RUNNING"},
    "status.starting": {"de": "STARTET", "en": "STARTING"},
    "status.off": {"de": "AUS", "en": "STOPPED"},
    "status.ready": {"de": "BEREIT", "en": "READY"},
    "status.current": {"de": "AKTUELL", "en": "UP TO DATE"},
    "status.update_available": {"de": "UPDATE", "en": "UPDATE"},
    # ---------------------------------------------------------------- Dashboard
    "dash.instances": {"de": "Instanzen", "en": "instances"},
    "dash.dashboard": {"de": "Dashboard", "en": "Dashboard"},
    "dash.new_instance": {"de": "Neue Instanz", "en": "New instance"},
    "dash.name_ph": {"de": "Name (z. B. valguero)", "en": "Name (e.g. valguero)"},
    "dash.port_ph": {"de": "Port (leer = automatisch)", "en": "Port (empty = automatic)"},
    "dash.session_ph": {"de": "Session-Name (leer = ARK name)", "en": "Session name (empty = ARK name)"},
    "dash.create": {"de": "Anlegen", "en": "Create"},
    "dash.install": {"de": "Installieren", "en": "Install"},
    "dash.not_installed": {"de": "nicht installiert", "en": "not installed"},
    "dash.note": {"de": "Hinweis", "en": "Note"},
    "dash.install_size": {"de": "SteamCMD lädt ~12,4 GB pro Instanz",
                          "en": "SteamCMD downloads ~12.4 GB per instance"},
    "dash.ports": {"de": "Spiel-Port UDP, RCON TCP — automatisch frei gewählt",
                   "en": "Game port UDP, RCON TCP — picked automatically"},
    "dash.memory": {"de": "ca. 11,5 GB RAM pro laufendem Server",
                    "en": "about 11.5 GB RAM per running server"},
    "dash.cpu": {"de": "CPU", "en": "CPU"},
    "dash.ram": {"de": "RAM", "en": "RAM"},
    "dash.players": {"de": "Spieler", "en": "Players"},
    "dash.uptime": {"de": "Laufzeit", "en": "Uptime"},
    "dash.peak": {"de": "Spitze", "en": "peak"},
    "dash.memory_label": {"de": "Speicher", "en": "Memory"},
    "dash.install_label": {"de": "Installation", "en": "Installation"},
    "dash.ports_label": {"de": "Ports", "en": "Ports"},
    # ---------------------------------------------------------------- Instanz
    "tabs.overview": {"de": "Übersicht", "en": "Overview"},
    "tabs.settings": {"de": "Einstellungen", "en": "Settings"},
    "tabs.mods": {"de": "Mods", "en": "Mods"},
    "tabs.manage": {"de": "Verwaltung", "en": "Management"},
    "inst.control": {"de": "Steuerung", "en": "Control"},
    "inst.commands": {"de": "Befehle", "en": "Commands"},
    "inst.players": {"de": "Spieler", "en": "Players"},
    "inst.log": {"de": "Server-Log", "en": "Server log"},
    "inst.no_players": {"de": "keine Spieler online", "en": "no players online"},
    "inst.rcon_free": {"de": "freier RCON-Befehl, z.B. GetChat",
                       "en": "free RCON command, e.g. GetChat"},
    "inst.kick": {"de": "Kick", "en": "Kick"},
    "inst.ban": {"de": "Bannen", "en": "Ban"},
    "inst.whitelist": {"de": "Whitelist", "en": "Whitelist"},
    "inst.item": {"de": "Item", "en": "Item"},
    # ---------------------------------------------------------------- Mods
    "mods.active": {"de": "Aktiv", "en": "Active"},
    "mods.inactive": {"de": "Inaktiv / auf Platte", "en": "Inactive / on disk"},
    "mods.none_active": {"de": "keine aktiven Mods", "en": "no active mods"},
    "mods.none_inactive": {"de": "keine weiteren Mods gefunden",
                           "en": "no other mods found"},
    "mods.id_ph": {"de": "Mod-ID (CurseForge), z.B. 947033",
                   "en": "Mod ID (CurseForge), e.g. 947033"},
    "mods.loaded": {"de": "geladen", "en": "loaded"},
    "mods.old_engine": {"de": "alte Engine", "en": "old engine"},
    "mods.unknown": {"de": "unbekannt", "en": "unknown"},
    "mods.no_desc": {"de": "keine Beschreibung", "en": "no description"},
    "mods.search": {"de": "Suchen", "en": "Search"},
    "mods.search_ph": {"de": "Mod suchen oder ID eingeben", "en": "search a mod or enter its ID"},
    "mods.search_empty": {"de": "nichts gefunden", "en": "nothing found"},
    "mods.search_failed": {"de": "Suche fehlgeschlagen", "en": "search failed"},
    "mods.add_hit": {"de": "Hinzufügen", "en": "Add"},
    "mods.key": {"de": "CurseForge-API-Key", "en": "CurseForge API key"},
    "mods.key_hint": {"de": "optional — ohne Key ist die Suche unzuverlässig; Key gibt es kostenlos auf console.curseforge.com",
                      "en": "optional — without a key the search is unreliable; free key at console.curseforge.com"},
    "mods.outdated": {"de": "UPDATE", "en": "UPDATE"},
    "mods.updated_ago": {"de": "neu seit", "en": "new for"},
    "mods.days": {"de": "Tagen", "en": "days"},
    "mods.on_disk": {"de": "auf Platte", "en": "on disk"},
    "mods.downloads": {"de": "Downloads", "en": "downloads"},
    "mods.open_curseforge": {"de": "Auf CurseForge öffnen", "en": "Open on CurseForge"},
    # ---------------------------------------------------------------- Settings
    "set.gui": {"de": "Einstellungen (GUI)", "en": "Settings (GUI)"},
    "set.raw": {"de": "INI direkt bearbeiten", "en": "Edit INI directly"},
    "set.save_changes": {"de": "Änderungen speichern", "en": "Save changes"},
    "set.no_changes": {"de": "keine Änderungen", "en": "no changes"},
    # ---------------------------------------------------------------- Whitelist
    "wl.title": {"de": "Whitelist & Bans", "en": "Whitelist & bans"},
    "wl.id_ph": {"de": "Steam-/EOS-ID", "en": "Steam/EOS ID"},
    "wl.add": {"de": "Auf Whitelist", "en": "Add to whitelist"},
    "wl.ban": {"de": "Bannen", "en": "Ban"},
    "wl.list": {"de": "Whitelist", "en": "Whitelist"},
    "wl.banned": {"de": "Gebannt (über noah)", "en": "Banned (via noah)"},
    "wl.banned_list": {"de": "Gebannt (über noah)", "en": "Banned (via noah)"},
    "wl.empty": {"de": "leer", "en": "empty"},
    "wl.none": {"de": "keine", "en": "none"},
    "wl.on": {"de": "AN", "en": "ON"},
    "wl.off": {"de": "AUS", "en": "OFF"},
    "wl.entries": {"de": "Einträge", "en": "entries"},
    "wl.file_present": {"de": "Datei vorhanden", "en": "file present"},
    "wl.file_missing": {"de": "Datei fehlt", "en": "file missing"},
    "mods.size_on_disk": {"de": "auf Platte", "en": "on disk"},
    # ---------------------------------------------------------------- Backups
    "bk.title": {"de": "Backups", "en": "Backups"},
    "bk.now": {"de": "Jetzt sichern", "en": "Back up now"},
    "bk.restore": {"de": "Einspielen", "en": "Restore"},
    "bk.none": {"de": "keine Backups", "en": "no backups"},
    "bk.none_dash": {"de": "keine", "en": "none"},
    "bk.times": {"de": "Backup-Uhrzeiten", "en": "Backup times"},
    "bk.times_hint": {"de": "kommagetrennt, z. B. 03:00 — leer = kein geplantes Backup",
                      "en": "comma separated, e.g. 03:00 — empty = no scheduled backup"},
    "bk.kind_manual": {"de": "manuell", "en": "manual"},
    "bk.kind_auto": {"de": "geplant", "en": "scheduled"},
    "bk.kind_pre_restore": {"de": "vor Restore", "en": "before restore"},
    "bk.kind_old": {"de": "älter", "en": "older"},
    "bk.times_hint": {"de": "kommagetrennt, z. B. 03:00 — leer = kein geplantes Backup",
                      "en": "comma separated, e.g. 03:00 — empty = no scheduled backup"},
    "sched.restart_hint": {"de": "kommagetrennt, z. B. 05:00,17:00 — leer = kein geplanter Neustart",
                           "en": "comma separated, e.g. 05:00,17:00 — empty = no scheduled restart"},
    "sched.warn_hint": {"de": "Minuten, in denen vorher im Spiel gewarnt wird",
                        "en": "minutes of in-game warning beforehand"},
    "sched.keep_hint": {"de": "ältere Sicherungen werden automatisch gelöscht",
                        "en": "older backups are cleaned up automatically"},
    "snap.hint_text": {"de": "Komplette Kopie der Serverdateien inklusive Mods — für den Fall, dass ein ARK-Update die Installation zerschießt. Platzbedarf: ca. 12 GB pro Snapshot.",
                       "en": "Full copy of the server files including mods — in case an ARK update breaks the installation. Needs about 12 GB per snapshot."},
    # ---------------------------------------------------------------- Snapshots
    "snap.title": {"de": "Instanz-Snapshot (Rollback)", "en": "Instance snapshot (rollback)"},
    "snap.hint": {"de": "Komplette Kopie der Serverdateien inklusive Mods – für den Fall, dass ein ARK-Update die Installation zerschießt. Platzbedarf: ca. 12 GB pro Snapshot.",
                  "en": "Full copy of the server files including mods — for when an ARK update breaks the installation. Needs about 12 GB per snapshot."},
    "snap.create": {"de": "Snapshot erstellen", "en": "Create snapshot"},
    "snap.restore": {"de": "Zurückspielen", "en": "Roll back"},
    "snap.none": {"de": "kein Snapshot vorhanden", "en": "no snapshot yet"},
    # ---------------------------------------------------------------- Zeitplan
    "sched.title": {"de": "Zeitplan (Neustart)", "en": "Schedule (restart)"},
    "sched.restart_times": {"de": "Neustart-Uhrzeiten", "en": "Restart times"},
    "sched.restart_hint": {"de": "kommagetrennt, z. B. 05:00,17:00 — leer = kein geplanter Neustart",
                           "en": "comma separated, e.g. 05:00,17:00 — empty = no scheduled restart"},
    "sched.warn": {"de": "Vorwarnung vor Neustart", "en": "Warn before restart"},
    "sched.warn_hint": {"de": "Minuten, in denen vorher im Spiel gewarnt wird",
                        "en": "minutes of in-game warning before the restart"},
    "sched.keep": {"de": "Backups behalten", "en": "Keep backups"},
    "sched.keep_hint": {"de": "ältere Sicherungen werden automatisch gelöscht",
                        "en": "older backups are cleaned up automatically"},
    # ---------------------------------------------------------------- Meldungen
    "msg.restart_needed": {"de": "wirksam nach Neustart", "en": "takes effect after restart"},
    "self.new_build": {"de": "neuer Stand", "en": "new build"},
    "self.current_build": {"de": "aktueller Stand", "en": "up to date"},
    "self.build_only": {"de": "gleiche Version, nur ein neuer Build - kein Update nötig",
                        "en": "same version, only a new build - no update needed"},
    "self.changelog": {"de": "Changelog", "en": "Changelog"},
    "self.on_github": {"de": "Auf GitHub öffnen", "en": "Open on GitHub"},
    "self.up_to_date": {"de": "noah ist aktuell", "en": "noah is up to date"},
    "self.click_update": {"de": "neue noah-Version verfügbar - klicken zum Aktualisieren",
                          "en": "new noah version available - click to update"},
    "self.confirm": {"de": "noah auf Version {v} aktualisieren? Die Oberfläche startet dabei neu.",
                     "en": "update noah to version {v}? The interface restarts during this."},
    "self.done": {"de": "Update eingespielt - die Seite lädt in ein paar Sekunden neu.",
                  "en": "update installed - the page reloads in a few seconds."},
    "msg.update_started": {"de": "Update gestartet - der Server stoppt, SteamCMD prüft die Dateien und startet neu. Das dauert einige Minuten.",
                           "en": "Update started - the server stops, SteamCMD verifies the files and starts again. This takes a few minutes."},
    "msg.confirm_update": {"de": "Server stoppen, updaten und neu starten?",
                           "en": "Stop the server, update and restart?"},
    "msg.confirm_restore": {"de": "Backup einspielen? Der Server wird gestoppt und neu gestartet.",
                            "en": "Restore backup? The server will be stopped and restarted."},
    "msg.confirm_snapshot": {"de": "Installation durch Snapshot ersetzen? Server wird gestoppt und neu gestartet.",
                             "en": "Replace the installation with this snapshot? The server will be stopped and restarted."},
    "msg.confirm_instance_delete": {"de": "Instanz „{n}“ entfernen? Der Eintrag verschwindet, die Serverdateien bleiben zunächst auf der Platte.",
                                    "en": "Remove instance \"{n}\"? The entry goes away, the server files stay on disk for now."},
    "msg.confirm_instance_files": {"de": "Auch die Serverdateien von „{n}“ löschen ({size} GB)? Das lässt sich nicht rückgängig machen.",
                                   "en": "Also delete the server files of \"{n}\" ({size} GB)? This cannot be undone."},
    "msg.confirm_delete": {"de": "Wirklich löschen?", "en": "Really delete?"},
    "msg.really_run": {"de": "Wirklich ausführen?", "en": "Really run it?"},
    "notify.title": {"de": "Benachrichtigungen (Discord)", "en": "Notifications (Discord)"},
    "notify.hint": {"de": "Webhook-Adresse aus Discord (Servereinstellungen → Integrationen → Webhooks). Meldungen: Absturz, Hänger-Neustart, neues Server-Update, Backup-Fehler.",
                    "en": "Webhook address from Discord (Server Settings → Integrations → Webhooks). Events: crash, hang restart, new server update, backup failure."},
    "notify.url": {"de": "Webhook-URL", "en": "Webhook URL"},
    "notify.url_hint": {"de": "leer = keine Meldungen", "en": "empty = no notifications"},
    "notify.url_ph": {"de": "https://discord.com/api/webhooks/…", "en": "https://discord.com/api/webhooks/…"},
    "notify.test": {"de": "Test senden", "en": "Send test"},
    "notify.test_ok": {"de": "Test angekommen", "en": "Test delivered"},
    "notify.test_fail": {"de": "Test fehlgeschlagen", "en": "Test failed"},
    "notify.saved": {"de": "gespeichert", "en": "saved"},
    "notify.failed": {"de": "nicht gespeichert", "en": "not saved"},
    # ---------------------------------------------------------------- Befehle
    "cmd.group.maintenance": {"de": "Wartung", "en": "Maintenance"},
    "cmd.group.comms": {"de": "Kommunikation", "en": "Communication"},
    "cmd.group.world": {"de": "Welt", "en": "World"},
    "cmd.group.info": {"de": "Info", "en": "Info"},
}

# Befehls- und Einstellungsnamen (Katalog der Klick-Buttons / Formularfelder)
LABELS: dict[str, dict[str, str]] = {
    "save": {"de": "Welt speichern", "en": "Save world"},
    "save_all_dinos": {"de": "Dinos speichern", "en": "Save dinos"},
    "broadcast": {"de": "Broadcast", "en": "Broadcast"},
    "chat": {"de": "Chat-Nachricht", "en": "Chat message"},
    "motd": {"de": "MOTD zeigen", "en": "Show MOTD"},
    "time": {"de": "Tageszeit", "en": "Time of day"},
    "wipe_dinos": {"de": "Wilde Dinos löschen", "en": "Wipe wild dinos"},
    "players": {"de": "Spielerliste", "en": "Player list"},
    "getchat": {"de": "Chat abrufen", "en": "Fetch chat"},
    "gameday": {"de": "Spieltag", "en": "Game day"},
}


# Assistent und Kommandozeile
WIZ: dict[str, dict[str, str]] = {
    "wiz.intro": {"de": "noah - Einrichtung", "en": "noah - setup"},
    "wiz.name": {"de": "Name der Instanz [{d}]:", "en": "Instance name [{d}]:"},
    "wiz.maps": {"de": "Maps:", "en": "Maps:"},
    "wiz.map": {"de": "Map waehlen [{d}]:", "en": "Choose map [{d}]:"},
    "wiz.port": {"de": "Spiel-Port (leer = automatisch):", "en": "Game port (empty = automatic):"},
    "wiz.port_bad": {"de": "Port {p} ungueltig (1024-65535) - wird automatisch gewaehlt",
                     "en": "Port {p} invalid (1024-65535) - picking one automatically"},
    "wiz.session": {"de": "Session-Name [{d}]:", "en": "Session name [{d}]:"},
    "wiz.created": {"de": "Instanz angelegt: {n}", "en": "Instance created: {n}"},
    "wiz.download_q": {"de": "Serverdateien jetzt herunterladen (~12,4 GB)? [j/N]:",
                       "en": "Download server files now (~12.4 GB)? [y/N]:"},
    "wiz.downloading": {"de": "Starte Installation - das dauert je nach Leitung 10-30 Minuten ...",
                        "en": "Starting download - this takes 10-30 minutes depending on your line ..."},
    "wiz.done": {"de": "Installation {r} (Log: {l})", "en": "Installation {r} (log: {l})"},
    "wiz.service_q": {"de": "systemd-Dienst einrichten (Autostart)? [j/N]:",
                      "en": "Set up a systemd service (autostart)? [y/N]:"},
    "wiz.web": {"de": "Fertig. Web-Oberflaeche:", "en": "Done. Web interface:"},
    "wiz.wine_missing": {"de": "! Wine fehlt. Ohne Wine startet der Server nicht.",
                         "en": "! Wine is missing. The server will not start without it."},
    "cli.lang_now": {"de": "Sprache: {l}", "en": "Language: {l}"},
    "cli.lang_set": {"de": "Sprache auf {l} gesetzt", "en": "Language set to {l}"},
    "cli.lang_bad": {"de": "unbekannte Sprache - erlaubt: de, en",
                     "en": "unknown language - allowed: de, en"},
    "cli.url": {"de": "Web-Adresse", "en": "Web address"},
    "cli.token_file": {"de": "Token-Datei: {path} (nur fuer deinen Benutzer lesbar)",
                       "en": "token file: {path} (readable by your user only)"},
    "cli.access_https": {"de": "HTTPS-Adresse", "en": "HTTPS address"},
    "cli.access_tunnel_hint": {"de": "Zugriff von einem anderen Rechner: ssh -N -L 8790:127.0.0.1:8790 {user}@{host}",
                               "en": "access from another machine: ssh -N -L 8790:127.0.0.1:8790 {user}@{host}"},
    "cli.domain_q": {"de": "Domain fuer HTTPS (optional, leer = nur lokal):",
                     "en": "Domain for HTTPS (optional, empty = local only):"},
    "cli.domain_saved": {"de": "Domain gespeichert: {d} - HTTPS einrichten mit: sudo noah proxy --write --cert",
                         "en": "domain saved: {d} - set up HTTPS with: sudo noah proxy --write --cert"},
    "cli.domain_none": {"de": "keine Domain gesetzt - noah proxy --domain <name> --write --cert",
                        "en": "no domain set - noah proxy --domain <name> --write --cert"},
    "cli.https_url": {"de": "HTTPS-Adresse", "en": "HTTPS address"},
    "cli.token_remote": {"de": "auf einem Server: ssh {host} noah url  (gibt die Adresse mit Token aus)",
                         "en": "on a server: ssh {host} noah url  (prints the address including the token)"},
    "cli.tunnel_hint": {"de": "von einem anderen Rechner: ssh -N -L {port}:127.0.0.1:{port} nutzer@server  (dann im Browser den Link oben oeffnen)",
                        "en": "from another machine: ssh -N -L {port}:127.0.0.1:{port} user@server  (then open the link above in your browser)"},
    "cli.proxy_next_steps": {"de": "Naechste Schritte:\n  1) Zertifikat:  sudo certbot --nginx -d {domain}\n  2) optional Anmeldung:  sudo htpasswd -c /etc/nginx/.htpasswd-noah deinname\n     dann erneut mit --auth-file /etc/nginx/.htpasswd-noah aufrufen\n  3) schreiben:  sudo noah proxy --domain {domain} --write [--cert]\n  noah bleibt auf 127.0.0.1, Port {port} muss nicht nach aussen offen sein.",
                            "en": "Next steps:\n  1) certificate:  sudo certbot --nginx -d {domain}\n  2) optional login:  sudo htpasswd -c /etc/nginx/.htpasswd-noah yourname\n     then run again with --auth-file /etc/nginx/.htpasswd-noah\n  3) write it:  sudo noah proxy --domain {domain} --write [--cert]\n  noah stays on 127.0.0.1, port {port} does not need to be open to the internet."},
    "cli.proxy_written": {"de": "nginx-Konfiguration geschrieben: {file} (nginx neu geladen)",
                          "en": "nginx configuration written: {file} (nginx reloaded)"},
    "cli.proxy_failed": {"de": "Proxy-Einrichtung fehlgeschlagen: {err}",
                         "en": "proxy setup failed: {err}"},
    "cli.proxy_cert_ok": {"de": "Zertifikat geholt (certbot).", "en": "certificate obtained (certbot)."},
    "cli.proxy_cert_fail": {"de": "certbot: {out}", "en": "certbot: {out}"},
    "cli.exposed_warning": {"de": "Achtung: Port {port} ist im Netzwerk erreichbar. Der Token schuetzt die Oberflaeche, die Uebertragung ist aber unverschluesselt (HTTP) - fuer Zugriff aus dem Internet einen Reverse-Proxy mit HTTPS davorsetzen.",
                            "en": "Warning: port {port} is reachable on the network. The token protects the UI, but traffic is unencrypted (HTTP) - put a reverse proxy with HTTPS in front before exposing it to the internet."},
    "cli.status_instance": {"de": "Instanz", "en": "Instance"},
    "cli.status_process": {"de": "Prozess", "en": "Process"},
    "cli.status_ready": {"de": "Bereit", "en": "Ready"},
    "cli.status_rcon": {"de": "RCON", "en": "RCON"},
    "cli.status_log": {"de": "Log", "en": "Log"},
    "cli.off": {"de": "aus", "en": "off"},
    "cli.yes": {"de": "ja", "en": "yes"},
    "cli.no": {"de": "nein", "en": "no"},
}


def load() -> dict:
    try:
        with open(CONFIG_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def lang() -> str:
    value = str(load().get("lang", DEFAULT)).lower()
    return value if value in LANGS else DEFAULT


def get(key: str, default: str = "") -> str:
    return str(load().get(key, default) or default)


def put(key: str, value: str) -> None:
    data = load()
    data[key] = value
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    os.chmod(CONFIG_PATH, 0o600)      # enthaelt ggf. den API-Key


def domain() -> str:
    return get("domain", "")


def set_domain(value: str) -> None:
    put("domain", value.strip())


def set_lang(value: str) -> str:
    value = value.lower()
    if value not in LANGS:
        raise ValueError("unbekannte Sprache: %s" % value)
    data = load()
    data["lang"] = value
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    os.chmod(CONFIG_PATH, 0o600)
    return value


def t(key: str, **kwargs) -> str:
    entry = T.get(key) or WIZ.get(key)
    if not entry:
        return key
    text = entry.get(lang()) or entry.get(DEFAULT) or key
    return text.format(**kwargs) if kwargs else text


def catalog() -> dict[str, str]:
    """Alle Texte der aktuellen Sprache als flaches dict (fuer die Weboberflaeche)."""
    current = lang()
    out = {key: (entry.get(current) or entry.get(DEFAULT, "")) for key, entry in T.items()}
    out.update({("cmd." + key): (entry.get(current) or entry.get(DEFAULT, ""))
                for key, entry in LABELS.items()})
    out.update({("wiz." + key): (entry.get(current) or entry.get(DEFAULT, ""))
                for key, entry in WIZ.items()})
    out["lang"] = current
    return out


# --------------------------------------------------------------- Formularfelder
SET_EN: dict[str, tuple[str, str]] = {
    "ServerPVE": ("PvE mode", "PvP off, PvE on"),
    "ServerHardcore": ("Hardcore", "death = character lost"),
    "DifficultyOffset": ("Difficulty", "0.0 - 1.0 (1.0 = max level)"),
    "OverrideOfficialDifficulty": ("Override official difficulty", "e.g. 5.0"),
    "MaxPlayers": ("Max players", "1 - 70 (on Steam)"),
    "ServerAdminPassword": ("Admin password", "empty = no admin access"),
    "ServerPassword": ("Server password", "empty = server open"),
    "RCONEnabled": ("RCON enabled", "must be true for this manager"),
    "RCONPort": ("RCON port", "TCP port"),
    "AutoSavePeriodMinutes": ("Autosave (minutes)", "default 15"),
    "TamingSpeedMultiplier": ("Taming speed", "1.0 = official, 5.0 = 5x"),
    "XPMultiplier": ("XP multiplier", "1.0 = official"),
    "HarvestAmountMultiplier": ("Harvest amount", "1.0 = official"),
    "HarvestHealthMultiplier": ("Harvest health", "higher = more per hit"),
    "DinoCharacterFoodDrainMultiplier": ("Dino food drain", "1.0 = official"),
    "PlayerCharacterFoodDrainMultiplier": ("Player hunger", "1.0 = official"),
    "PlayerCharacterWaterDrainMultiplier": ("Player thirst", "1.0 = official"),
    "DinoCountMultiplier": ("Dino density", "1.0 = official"),
    "DayTimeSpeedScale": ("Day speed", "1.0 = official"),
    "NightTimeSpeedScale": ("Night speed", "1.0 = official"),
    "AllowThirdPersonPlayer": ("Allow third person", ""),
    "ShowMapPlayerLocation": ("Show own position on map", ""),
    "AllowCaveBuildingPvE": ("Cave building (PvE)", ""),
    "KickIdlePlayersPeriod": ("Idle kick after (seconds)", "3600 = 1 hour"),
    "AdminLogging": ("Log admin commands in chat", ""),
    "SessionName": ("Session name", "name in the server list"),
    "Message": ("MOTD text", "shown when connecting, multiple lines allowed"),
    "Duration": ("MOTD duration (seconds)", "default 60"),
    "MatingIntervalMultiplier": ("Mating interval", "1.0 = official"),
    "EggHatchSpeedMultiplier": ("Egg hatch speed", "1.0 = official"),
    "BabyMatureSpeedMultiplier": ("Baby maturation", "1.0 = official"),
    "BabyFoodConsumptionSpeedMultiplier": ("Baby food consumption", "1.0 = official"),
    "BabyImprintingStatScaleMultiplier": ("Imprinting bonus", "1.0 = official"),
    "CropGrowthSpeedMultiplier": ("Crop growth", "1.0 = official"),
    "LayEggIntervalMultiplier": ("Egg interval", "1.0 = official"),
    "StructureDamageMultiplier": ("Structure damage", "1.0 = official"),
    "PerLevelStatsMultiplier_DinoTamed_Add[0]": ("Dino HP per level (additive)", "1.0 = official"),
}

CMD_EN: dict[str, tuple[str, str]] = {
    "save": ("Save world", "immediate save - wise before every restart"),
    "save_all_dinos": ("Save dinos", "alias for SaveWorld (includes dino state)"),
    "broadcast": ("Broadcast", "message shown in the middle of every player's screen"),
    "chat": ("Chat message", "appears as a server message in chat"),
    "motd": ("Show MOTD", "message of the day"),
    "time": ("Time of day", "set the in-game time"),
    "wipe_dinos": ("Wipe wild dinos", "removes all wild creatures - be careful"),
    "players": ("Player list", "who is online right now"),
    "getchat": ("Fetch chat", "last chat lines"),
    "gameday": ("Game day", "current day number"),
}

GROUP_EN = {"Wartung": "Maintenance", "Kommunikation": "Communication",
            "Welt": "World", "Info": "Info"}

ARG_EN = {
    "Nachricht an alle Spieler": "Message to all players",
    "Server-Neustart in 5 Minuten": "Server restart in 5 minutes",
    "Nachricht im Chat": "Message in chat",
    "Willkommen auf dem Server": "Welcome to the server",
    "Uhrzeit (hh:mm)": "Time (hh:mm)",
}


def setting(ini_key: str, label: str, hint: str) -> tuple[str, str]:
    """Label und Hinweis eines Formularfelds in der aktuellen Sprache."""
    if lang() == "en" and ini_key in SET_EN:
        return SET_EN[ini_key]
    return label, hint


def command(entry: dict) -> dict:
    """Kopie eines Befehls mit uebersetzten Texten."""
    if lang() != "en":
        return entry
    out = dict(entry)
    label, note = CMD_EN.get(entry["id"], (entry["label"], entry.get("note", "")))
    out["label"] = label
    out["note"] = note
    out["group"] = GROUP_EN.get(entry["group"], entry["group"])
    if entry.get("args"):
        out["args"] = [(a[0], ARG_EN.get(a[1], a[1]), ARG_EN.get(a[2], a[2])) for a in entry["args"]]
    return out
