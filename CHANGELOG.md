## [0.16] — 2026-11-14

### Neu
- **SFTP-Zugang pro Instanz.** Jede Instanzkarte bietet „SFTP einschalten": eigener Benutzer,
  generiertes Passwort, Port aus `sftp_base_port + laufender Nummer` (Standard 2225), Chroot auf den
  Instanzordner — FileZilla-kompatibel (SFTP, kein FTP). „Neues Passwort" erzeugt sofort eines und
  kopiert es in die Zwischenablage, „aus" schließt den Port wieder.
- Der Dienst läuft als `ascendedpanel-sftp` (systemd, Benutzer- oder Systemdienst). Ist kein
  Benutzerbus erreichbar — etwa weil das Panel per `nohup` läuft — startet er sich abgekoppelt mit
  PID-Datei `sftp.pid`, damit der Zugang trotzdem steht.
- **Voraussetzung:** `asyncssh` (`apt install python3-asyncssh`). Fehlt es, läuft das Panel
  unverändert weiter; nur der SFTP-Dienst meldet im Panel-Log, was fehlt.

### Geändert
- **Token bleibt gleich.** Der Web-Token wird nur beim allerersten Start erzeugt und danach immer aus
  `~/.config/ascendedpanel/token` gelesen — Neustart, Update und Selbst-Update ändern ihn nicht.
  Alte Links funktionieren weiter; ein neuer Token entsteht erst, wenn die Datei gelöscht wird.
- Instanz-JSON kennt `sftp_enabled`, `sftp_user`, `sftp_password`, `sftp_port`; die Karte zeigt
  `sftp://benutzer@host:port`.

## [0.15] — 2026-11-14

### Neu
- **AsaApi-Unterstuetzung.** Eine Instanz kann jetzt über den ArkApi-Lader starten: Ist `asaapi`
  gesetzt und liegt `ArkApi/AsaApiLoader.exe` in der Instanz, wird dieser statt
  `ArkAscendedServer.exe` gestartet. Damit laufen Plugins im Spiel (z. B. das QuestPlugin mit
  `!quests`/`!argy`). Die Installationsprüfung und der Startschutz orientieren sich weiterhin an
  der echten Server-EXE, damit eine Instanz ohne Loader nicht als „nicht installiert" gilt.

### Geändert
- **Tribe-Logs über RCON.** Der Startbefehl enthält zusätzlich `-ServerRCONOutputTribeLogs`; zusammen
  mit `-servergamelog` und `-servergamelogincludetribelogs` kommen Claim-/Tame-Zeilen sowohl in die
  Serverlogdatei als auch in den RCON-Logpuffer (CrossArkChat).

## [0.14] — 2026-11-13

### Behoben
- **Instanzkarte ohne leere Angaben.** Fehlt die Karte oder gibt es keinen RCON-Port, steht dort kein
  nacktes „·" mehr, sondern nur die vorhandenen Werte (`<Karte> · Port <n> · RCON <n>`).

## [0.13] — 2026-11-13

### Neu
- **Download-Geschwindigkeit im Installationsfenster.** Neben Schritt und Prozent steht jetzt die
  aktuelle Rate in MB/s — berechnet aus den Byte-Zahlen der steamcmd-Zeilen und geglättet, damit
  die Anzeige nicht springt.

## [0.12] — 2026-11-13

### Behoben
- **Instanzen starten nach der Installation nicht mehr von selbst.** Der Supervisor wurde direkt
  nach der Installation aktiviert; weil ein frisch installierter Server noch nie lief, deutete er
  „Prozess weg" als Absturz und fuhr den Server sofort hoch. Jetzt wird die Instanz vor dem
  Dienststart als „gestoppt" markiert (`runner.mark_stopped`) — Start nur noch über „Start" im
  Panel. Der Marker verschwindet beim Start, die Absturz-Erkennung arbeitet danach wie gewohnt;
  auch nach einem Systemstart bleibt eine nie gestartete Instanz aus.

## [0.11] — 2026-11-13


### Überblick
Grobe Zusammenfassung dessen, was in den Panels steckt.

- **Zwei Panels, ein Unterbau:** AscendedPanel für ARK: Survival Ascended, PolyPanel für ASA, ASE,
  Satisfactory, 7 Days to Die und Space Engineers. Bedienung im Browser, Dienst auf dem Server.
- **Dashboard:** Instanzkarten mit Status, Karte, Ports, Build, CPU/RAM, Spielern und Laufzeit;
  Start, Restart, Update, Stop und Löschen direkt auf der Karte, Knöpfe sperren sich nach Zustand
  (läuft Stop, ist nur noch Menü frei usw.).
- **Instanzseite:** Live-Log, Konfigurationseditor mit Sicherung und Prüfung (INI-Werte als Formular
  oder roh), Mod-Verwaltung mit CurseForge-Suche/Update-Prüfung, Backups, Snapshots, Zeitplan und
  RCON-Konsole mit Ein-Klick-Befehlen.
- **Spieler:** Liste mit Kick, Ban, Whitelist und Gegenstände verteilen — Katalog mit Suche und
  Mengenfenster; die nötige Spieler-ID (ARKID) wird aus den `.arkprofile`-Dateien gelesen, weil
  ARK per RCON nur die EOS-ID liefert.
- **Sperren:** eigenes Fenster „Gesperrte Spieler" mit Entbannen je Zeile und ehrlichem Hinweis,
  warum ARK seine Ban-Liste nicht über RCON herausgibt.
- **Betrieb:** Absturz-Erkennung mit automatischem Neustart, Discord-Benachrichtigungen,
  Sprache Deutsch/Englisch jederzeit umschaltbar, mehrere Instanzen in einem Prozess.
- **Fehlermeldungen:** Knopf im Panel, Meldung geht an den Betreiber (Webhook, nur auf der Konsole
  setzbar) — mit Version, Instanz, System und Logauszug, Passwörter entfernt.

### Behoben
- **Installationsbalken lief rückwärts bzw. blieb stehen.** SteamCMD beginnt jede Phase wieder bei
  0 % (Download → Prüfen → Abschluss), der Balken sprang deshalb zurück. Er zeigt jetzt den
  Gesamtfortschritt über die drei Schritte und wird nie kleiner als der bisherige Höchstwert.
- **`/api/install/progress` warf einen Fehler**, sobald eine Fortschrittszeile im Installationslog
  stand: die Phasentabelle `_PHASE_STEP` wurde benutzt, aber nie definiert. Damit blieb der Balken
  im Installationsfenster stehen.
- **„Installieren" öffnet wieder den Fortschritt.** Lag der zuletzt gemerkte Reiter auf
  „Einstellungen", verdeckte er das Installationsfenster — der Klick wirkte, als lande man in den
  Einstellungen, während im Hintergrund korrekt installiert wurde.
- **Löschen blockiert die Oberfläche nicht mehr.** Stoppen (Server speichert vorher) und das
  Entfernen mehrerer GB laufen als Hintergrund-Job; die Karte zeigt „Server wird gestoppt …", dann
  „Serverdateien werden gelöscht …" und am Ende die freigegebene Größe. Jeder Löschvorgang steht mit
  Zeitstempel und freigegebenen MB im `panel.log`.
- **Wine wird im Installer ohne Rückfrage installiert** — wie Xvfb. Die Frage „Wine installieren?"
  wurde erfahrungsgemäß mit „nein" beantwortet, danach startete kein Windows-Spiel.