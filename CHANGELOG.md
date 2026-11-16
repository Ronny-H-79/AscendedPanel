## [0.21] — 2026-11-16

### Neu
- **Die Karte zeigt, was gerade läuft.** Bisher stand bei einem laufenden Update nur „AUS". Jetzt
  erscheint eine Hinweiszeile (⏳ UPDATE LÄUFT, INSTALLATION LÄUFT, NEUSTART LÄUFT, WIRD GESTOPPT,
  WIRD GELÖSCHT, ASAPI WIRD EINGERICHTET) aus den laufenden Aktionen des Panels; `runner.stop()` meldet
  seinen Zustand mit, damit der Stopp sichtbar wird. Die Statusabzeichen nennen den Vorgang auch auf
  der Detailseite („FÄHRT HERUNTER" gelb statt bis zuletzt „LÄUFT"), die Knöpfe bleiben bis zum Ende
  gesperrt.

### Geändert
- **Mod-Beschreibungen** werden vollständig übersetzt (kein Abschneiden bei 400 Zeichen mehr, Stücke
  mit Wiederholung, Ausweichdienst bei Google-Rate-Limit, keine englischen Texte mehr im Cache) und
  lesbar umbrochen: Rollenangaben („Primary roles", „Hauptfunktionen", „Hauptaufgaben") und lange
  Sätze auf eigenen Zeilen; in der Trefferliste bis zu fünf Zeilen statt hartem Schnitt bei 90 Zeichen.

## [0.18] — 2026-11-15

### Geändert
- **Kein zusätzliches Fenster mehr beim Anlegen und Installieren.** Das Anlegen bleibt in der
  Übersicht (die neue Karte erscheint dort), die Installation zeigt ihren Fortschritt im selben Tab.

### Behoben
- **Server-Passwort bleibt erhalten.** `write_ini()` hat `ServerPassword` bei jedem Start fest auf leer
  gesetzt; ein eingetragenes Beitrittspasswort war damit nach dem nächsten Start weg. Jetzt steht es in
  der Instanz, wandert in die INI und als `?ServerPassword=` in die Startzeile (Admin-Passwort bleibt
  die letzte Option, sonst schluckt sie den Rest).
- **Munition im Gegenstands-Dialog.** Alle Munitionseinträge zeigten auf `Items/…`, die Assets liegen
  aber unter `Weapons/…` — Geben scheiterte stillschweigend. Pfade korrigiert, fehlende Munition
  ergänzt (u. a. Einfache Gewehrmunition). Beschriftung berichtigt: `OneShotRifle` ist das
  Longneck-Gewehr, die Schrotflinte (`PrimalItem_WeaponShotgun`) fehlte ganz.

## [0.17] — 2026-11-14

### Neu
- **AsaApi gehört zur Installation.** Nach dem SteamCMD-Lauf richtet das Panel AsaApi automatisch ein
  (komplettes Release inklusive `config.json` und der mitgelieferten DLLs) und startet die Instanz
  danach über `AsaApiLoader.exe`. Der Knopf **„API"** auf der Karte installiert oder aktualisiert die
  API jederzeit von Hand; er erscheint nur, wenn er etwas zu tun hat, und trägt bei einem neueren
  Release ein Badge mit der Version. Im Reiter „Mods" schaltet eine Checkbox die API samt Plugins
  wieder aus (Start ohne Loader). Schlägt die Installation fehl, bleibt der Server installiert und der
  Knopf ist der Nachhol-Weg. Installationsprüfung und Startschutz orientieren sich weiter an der
  echten Server-EXE, damit eine Instanz ohne Loader nicht als „nicht installiert" gilt.
- **Firewall wird mitgemacht.** Beim Start trägt das Panel Spiel- und Query-Port (UDP) in `ufw` ein,
  beim Löschen der Instanz werden die Regeln wieder entfernt. Für `ufw` legt der Installer eine eng
  begrenzte `sudo`-Regel an (nur `/usr/sbin/ufw`); fehlt sie, startet der Server trotzdem und das
  Panel-Log nennt den Grund.
- **Mod-IDs direkt eintragen.** Im Reiter „Mods" gibt es ein Feld für die Mod-IDs (Komma, Semikolon
  oder Leerzeichen als Trenner). Es zeigt die aktive Liste und ersetzt sie beim Speichern.
- **Datei-Browser im Panel.** Der Reiter „Dateien" zeigt den Instanzordner: Ordner öffnen, mehrere
  Dateien gleichzeitig hochladen, herunterladen, umbenennen, löschen, Ordner anlegen. Pfade mit `..`
  werden abgewiesen, Downloads laufen als Stream. Klick auf den Namen öffnet Textdateien bis 2 MB im
  Browser (Binärdateien abgewiesen), „Speichern" schreibt zurück und legt eine `.bak`-Sicherung an.
- **SFTP-Zugang pro Instanz.** Eigener Benutzer, generiertes Passwort, Port aus
  `sftp_base_port + laufender Nummer` (Standard 2225), Chroot auf den Instanzordner —
  FileZilla-kompatibel (SFTP, kein FTP). „Neues Passwort" kopiert es in die Zwischenablage, „aus"
  schließt den Port. Der Dienst läuft als `ascendedpanel-sftp`; ist kein Benutzerbus erreichbar (Panel
  per `nohup`), startet er abgekoppelt mit `sftp.pid`. Voraussetzung: `asyncssh` — fehlt es, läuft das
  Panel weiter und nur der SFTP-Dienst meldet im Panel-Log, was fehlt.

### Geändert
- **Metriken zählen alle Prozesse der Instanz.** Unter Wine/Proton und mit API-Loader hängt der
  Serverprozess nicht an der Starter-PID, deshalb erschienen CPU und RAM als 0; jetzt werden alle
  Prozesse der Instanz über ihre Kommandozeile gefunden und summiert.
- **SessionName und MaxPlayers bleiben erhalten** (Werte aus `GameUserSettings.ini` wandern zurück in
  die Instanz), und die Sektion in der `Game.ini` wird unabhängig von der Schreibweise erkannt.
- **Token bleibt gleich.** Der Web-Token wird nur beim allerersten Start erzeugt und danach aus
  `~/.config/ascendedpanel/token` gelesen — Neustart, Update und Selbst-Update ändern ihn nicht; ein
  neuer entsteht erst, wenn die Datei gelöscht wird. Das Instanz-JSON kennt dafür `sftp_enabled`,
  `sftp_user`, `sftp_password`, `sftp_port` und zeigt `sftp://***@host:port`.
- **Tribe-Logs über RCON.** Der Startbefehl enthält zusätzlich `-ServerRCONOutputTribeLogs`; zusammen
  mit `-servergamelog` und `-servergamelogincludetribelogs` landen Claim-/Tame-Zeilen in der
  Serverlogdatei und im RCON-Logpuffer.

### Behoben
- Start über `AsaApiLoader.exe` brach mit „LoaderFailed, Reason: UnknownLoaderResult" ab, wenn im
  Win64-Ordner die `config.json` des API-Releases fehlte.
- Eine doppelte `ActiveMods`-Zeile konnte dafür sorgen, dass eingetragene Mods beim Start
  stillschweigend ignoriert wurden.

## [0.14] — 2026-11-13

### Neu
- **Download-Geschwindigkeit im Installationsfenster.** Neben Schritt und Prozent steht die aktuelle
  Rate in MB/s — aus den Byte-Zahlen der steamcmd-Zeilen berechnet und geglättet, damit die Anzeige
  nicht springt.

### Behoben
- **Instanzen starten nach der Installation nicht mehr von selbst.** Der Supervisor wurde direkt nach
  der Installation aktiviert und deutete „Prozess weg" beim nie gestarteten Server als Absturz. Jetzt
  wird die Instanz vor dem Dienststart als „gestoppt" markiert (`runner.mark_stopped`); Start nur über
  „Start" im Panel, auch nach einem Systemstart.
- **Installationsbalken und Fortschritts-API.** Der Balken sprang zurück, weil SteamCMD jede Phase bei
  0 % beginnt — er zeigt jetzt den Gesamtfortschritt und fällt nie unter den Höchstwert.
  `/api/install/progress` warf einen Fehler, sobald eine Fortschrittszeile im Log stand (die
  Phasentabelle `_PHASE_STEP` wurde benutzt, aber nie definiert). „Installieren" öffnet wieder den
  Fortschritt, auch wenn zuletzt der Reiter „Einstellungen" offen war.
- **Löschen blockiert die Oberfläche nicht mehr.** Stoppen und Entfernen mehrerer GB laufen als
  Hintergrund-Job; die Karte zeigt „Server wird gestoppt …", dann „Serverdateien werden gelöscht …" und
  die freigegebene Größe. Jeder Löschvorgang steht mit Zeitstempel und MB im `panel.log`.
- **Instanzkarte ohne leere Angaben.** Fehlt die Karte oder der RCON-Port, erscheint kein nacktes „·"
  mehr, sondern nur `<Karte> · Port <n> · RCON <n>`.
- **Wine wird im Installer ohne Rückfrage installiert** — wie Xvfb. Die Frage „Wine installieren?"
  wurde erfahrungsgemäß mit „nein" beantwortet, danach startete kein Windows-Spiel.

## Überblick

Grobe Zusammenfassung dessen, was im Panel steckt.

- **Ein Panel, ein Unterbau:** AscendedPanel für ARK: Survival Ascended, Bedienung im Browser, Dienst
  auf dem Server.
- **Dashboard:** Instanzkarten mit Status, Karte, Ports, Build, CPU/RAM, Spielern und Laufzeit; Start,
  Restart, Update, Stop und Löschen direkt auf der Karte, Knöpfe sperren sich nach Zustand.
- **Instanzseite:** Live-Log, Konfigurationseditor mit Sicherung und Prüfung (INI-Werte als Formular
  oder roh), Mod-Verwaltung mit CurseForge-Suche/Update-Prüfung, Backups, Snapshots, Zeitplan,
  RCON-Konsole mit Ein-Klick-Befehlen, Datei-Browser und SFTP.
- **Spieler:** Liste mit Kick, Ban, Whitelist und Gegenstände verteilen — Katalog mit Suche und
  Mengenfenster; die nötige Spieler-ID (ARKID) wird aus den `.arkprofile`-Dateien gelesen, weil ARK
  per RCON nur die EOS-ID liefert.
- **Sperren:** eigenes Fenster „Gesperrte Spieler" mit Entbannen je Zeile und ehrlichem Hinweis, warum
  ARK seine Ban-Liste nicht über RCON herausgibt.
- **Betrieb:** Absturz-Erkennung mit automatischem Neustart, Discord-Benachrichtigungen, Sprache
  Deutsch/Englisch jederzeit umschaltbar, mehrere Instanzen in einem Prozess.
- **Fehlermeldungen:** Knopf im Panel, Meldung geht an den Betreiber (Webhook, nur auf der Konsole
  setzbar) — mit Version, Instanz, System und Logauszug, Passwörter entfernt.
