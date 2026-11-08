# Changelog

Alle nennenswerten Änderungen an noah. Format nach
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionierung nach
[Semantic Versioning](https://semver.org/lang/de/).

## [0.3.11] — 2026-11-08

### Behoben
- **`noah url` zeigte auf einem Server `127.0.0.1`.** Bei Zugriffsart „IP" steht jetzt die Adresse,
  unter der die Oberfläche wirklich erreichbar ist (die lokale Adresse ermittelt noah selbst).

## [0.3.10] — 2026-11-08

### Behoben
- **Selbst-Update scheiterte stillschweigend.** Ein einzelner `504 Gateway Timeout` beim Archiv-Download
  beendete den Vorgang, die Oberfläche meldete trotzdem nichts — der Knopf wirkte wirkungslos. Jetzt:
  drei Versuche mit Pause und ein zweiter Weg über `codeload.github.com`, und die Oberfläche zeigt
  „Update fehlgeschlagen: …" statt Stille.
- Das Einspielen läuft synchron; der Neustart des Dienstes passiert eine Sekunde später, damit die
  Antwort noch ankommt.

## [0.3.9] — 2026-11-08

### Neu
- **Der Build-Badge ist ein Knopf.** Auf der Instanzseite stand bisher nur `AKTUELL 26515168` — das
  Update ließ sich nur von der Übersicht starten. Jetzt gilt: `UPDATE a→b` anklicken startet das Update
  (mit Rückfrage, Sicherung und Stop), `AKTUELL b` prüft beim Klick erneut. Tooltip erklärt beides,
  per Tastatur (Enter/Leertaste) genauso bedienbar.

## [0.3.8] — 2026-11-08

### Sicherheit
- **Token-Vergleich in konstanter Zeit** (`hmac.compare_digest`) statt `==`.
- **Sicherheits-Header** auf jeder Antwort: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`,
  `Referrer-Policy: no-referrer` (damit der Token nicht über die Herkunftsangabe abfließt) und eine
  restriktive `Content-Security-Policy`.
- **Mod-IDs werden geprüft** (nur Ziffern, max. 10 Stellen). Vorher landete der Wert ungefiltert in der
  Server-Kommandozeile (`-mods=…`).
- **Spieler-IDs** (Whitelist/Bans) nur als Steam64 (Ziffern) oder Hex-UniqueNetId — Zeilenumbrüche und
  Sonderzeichen werden abgelehnt, statt in die Textdatei zu wandern.

## [0.3.7] — 2026-11-08

### Geändert
- **Mod-Suche funktioniert ohne Instanz.** `/api/mods/search`, `/api/mods/suggest` und das Speichern des
  API-Keys hingen hinter der Instanz-Prüfung und antworteten ohne angelegte Instanz mit „keine Instanz".
- Der Mods-Reiter zeigt, womit gesucht wird: `CurseForge-API aktiv · Suche nach Titel und Beschreibung,
  sortiert nach Downloads` (grün, mit maskiertem Key) oder `Kein API-Key · nur genaue Mod-ID oder
  CurseForge-Link, keine Volltextsuche`.

## [0.3.6] — 2026-11-08

### Geändert
- Der Versionsknopf zeigt den Zustand im Text: `aktueller Stand` bzw. `neuer Stand`, nicht nur
  im Tooltip.

## [0.3.5] — 2026-11-08

### Geändert
- Meldet noah „gleiche Version, nur neuer Build", ist der Knopf nicht mehr klickbar — es gibt
  nichts zu holen. Änderungen, die ankommen sollen, bekommen einen Versionssprung.

## [0.3.4] — 2026-11-08

### Geändert
- Copyright nur noch unter dem Handle `ronny79privat` (statt Klarname).

## [0.3.3] — 2026-11-08

### Geändert
- Copyright-Hinweis im README und in der `LICENSE` (ronny79privat).
- „Für Entwickler" aus der Technik-Doku ausgelagert nach `docs/entwicklung.md` — für Anwender
  unwichtig, für Mitlesende weiterhin erreichbar.

## [0.3.2] — 2026-11-08

### Geändert
- README auf das Wesentliche gekürzt (111 statt 420 Zeilen). Funktionen, Zugriff, Betrieb und
  Technik stehen jetzt in `docs/funktionen.md`, `docs/zugriff.md`, `docs/betrieb.md` und
  `docs/technik.md`.

## [0.3.1] — 2026-11-08

### Geändert
- README neu sortiert: Installation und Deinstallation stehen oben, danach Zugriff von außen und
  der Token; Feature-Liste und Screenshots folgen weiter unten.

## [0.3.0] — 2026-11-08

### Hinzugefügt
- **Changelog-Knopf** im Kopf: öffnet die Änderungen als Popup, in der eingestellten Sprache
  (Deutsch/Englisch). Der Inhalt kommt aus der eigenen Installation, kein Netzzugriff nötig.
- Englische Fassung: `CHANGELOG.en.md`.

### Geändert
- Der Update-Dialog zeigt die Änderungen der neuen Version direkt an.
- Benachrichtigungen: Routine-Meldungen bleiben im Log, nur Ereignisse gehen an Discord.

## [0.2.9] — 2026-11-08

### Hinzugefügt
- **CHANGELOG.md** — was sich je Version geändert hat.
- Der Update-Dialog zeigt die Änderungen der neuen Version an, bevor man zustimmt.
- **`scripts/release.sh`**: Version setzen, committen, taggen, pushen (mit `--release` auch das
  GitHub-Release, sofern `gh` installiert ist).

## [0.2.8] — 2026-11-08

### Behoben
- Modsuche lieferte mit API-Key **null Treffer**: der Parameter `classId` schränkte die
  CurseForge-Abfrage auf eine Kategorie ein, die für ARK-ASA-Mods nichts liefert. Ohne
  Einschränkung kommen die erwarteten Ergebnisse.
- Leere Suchergebnisse werden nicht mehr eine Stunde zwischengespeichert.

## [0.2.7] — 2026-11-08

### Geändert
- Update-Prüfung wird **10 Minuten gecacht** — GitHub erlaubt ohne Token nur 60 Anfragen pro Stunde.
  `noah version` und `noah self-update` prüfen weiterhin frisch.

## [0.2.6] — 2026-11-08

### Hinzugefügt
- **„← Dashboard"** im Kopf der Instanzseite.

### Geändert
- Das Update-Badge der Instanz erscheint nur noch bei belastbarer Prüfung (vorher stand dort
  dauerhaft „UPDATE ?", solange die Serverdateien fehlten).
- `install.sh` startet einen laufenden `noah-web`-Dienst nach dem Kopieren neu, damit der neue
  Code sofort aktiv ist.

## [0.2.5] — 2026-11-08

### Geändert
- Update-Knopf im Badge-Stil statt als vollflächiger Block.

## [0.2.4] — 2026-11-08

### Geändert
- Update-Knopf ist beschriftet: `noah update: 0.2.3 → 0.2.4` statt nur Versionsnummern.

## [0.2.3] — 2026-11-08

### Behoben
- Selbst-Update holte das Quellarchiv über `codeload.github.com`, das nach einem Push noch den
  alten Stand ausliefert. Jetzt über die GitHub-API.

## [0.2.2] — 2026-11-08

### Behoben
- Versionsprüfung las `raw.githubusercontent.com` (bis zu 5 Minuten veraltet) — jetzt über die
  GitHub-API.

## [0.2.1] — 2026-11-08

### Behoben
- `/api/selfupdate` war nur mit vorhandener Instanz erreichbar.

## [0.2.0] — 2026-11-08

### Hinzugefügt
- **Selbst-Update**: Knopf im Kopf (`noah update: alt → neu`) und `noah self-update`.
- **Modsuche**: Mod-ID, CurseForge-Link oder Name; Vorschläge erscheinen beim Tippen, mit Bild,
  Downloads und einem Klick zum Übernehmen. Namen brauchen einen CurseForge-API-Key.
- **Mod-Updates im Blick**: installed-Datei vs. neueste Datei auf CurseForge, Kennzeichen „UPDATE".
- **Discord-Benachrichtigungen**: Absturz, Hänger, Update verfügbar, Backup-Fehler, geplanter
  Neustart — Routine bleibt im Log.
- **Hänger- und Absturzerkennung** im Supervisor; ein manueller Stop wird respektiert.
- **`noah proxy`**: richtet nginx mit HTTPS ein (Zertifikat per certbot, optional Basic Auth),
  prüft mit `nginx -t` und rollt bei Fehlern zurück.
- **HTTPS direkt** im Webserver (`--tls-cert` / `--tls-key`).
- **Instanz löschen** auf der Dashboard-Karte (Config ins `.trash`, Dateien nur auf Wunsch).
- **Update-Knopf** und **Löschen** direkt auf der Karte.
- **MOTD** als mehrzeiliges Formularfeld.
- **Zweisprachig** (Deutsch/Englisch): Sprachwahl im Installer, Knopf in der Oberfläche,
  `noah lang`.
- **Drei Zugriffswege** im Installer: client-seitig per SSH-Tunnel, öffentlich per Domain+HTTPS,
  direkt über IP und Port.
- Der **Supervisor-Dienst** wird nach der Installation einer Instanz automatisch eingerichtet
  (als root ein Systemdienst, der beim Booten startet).

### Geändert
- Instanzseite: Server-Log oben über die volle Breite und ziehbar (48 % Höhe, 150 Zeilen),
  Steuerknöpfe liegen auf der Dashboard-Karte.
- Server-Log springt beim Öffnen ans Ende; der aktive Reiter bleibt beim Neuladen erhalten.
- Kartenhintergrund deutlich sichtbar (Deckkraft 0.28 → 0.62).
- Einstellungen: mehrzeilige Felder (Textarea) möglich.
- `settings.json` wird mit `0600` geschrieben, weil sie den API-Key enthält.

## [0.1.0] — 2026-11-07

Erster öffentlicher Stand: Instanzen anlegen, Start/Stop/Restart/Update über SteamCMD, RCON-Konsole
mit Klick-Befehlen, Spielerverwaltung, Mod-Verwaltung, Config-Editor, Welt-Backups, Snapshots,
Whitelist/Bans, Zeitplan, Live-Metriken und Weboberfläche.
