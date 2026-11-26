## [0.44] - 2026-11-26

- Zeilennummern stehen jetzt als eigene Spalte links neben dem Text. Beim ersten Anlauf wurden sie
  als Zahlenreihe ueber der Datei angezeigt, weil der CSS-Block auf der Instanzseite nicht geladen
  wurde — die Abmessungen stehen jetzt direkt am Element und greifen damit auf jeder Seite.

## [0.43] - 2026-11-26

- Zeilennummern in der Datei-Ansicht: links am Rand, mitlaufend beim Scrollen und Tippen. Gilt im
  Editor des Instanz-Reiters und in der Vollansicht. Zeilenumbrueche sind dort abgeschaltet, damit
  Nummer und Zeile exakt auf einer Hoehe stehen.

## [0.42] - 2026-11-25

- Neuer Schalter unter Mods: startet den Server ohne AsaApi, wenn der Loader nach einem ARK-Update
  nicht mehr passt. Der Server bleibt damit erreichbar; im Spiel fehlen dann Quests, Startpaket und
  Kill-Zaehlung. Zurueckstellen, sobald der Loader wieder laeuft.

## [0.41] - 2026-11-25

- Vor jedem Löschen kommt jetzt eine Rückfrage: Datei, Mod, Mod-Dateien, Snapshot, Backup und
  Whitelist-Eintrag. Die Texte stehen in beiden Sprachen, bisher waren sie fest auf Deutsch.

## [0.40] - 2026-11-24

- Dateien im Editor: lange Zeilen werden nicht mehr umbrochen, sondern seitlich gescrollt. Die
  Ini unter Bjarnheim hat eine Zeile mit 13.896 Zeichen, die bisher über den halben Bildschirm
  umgebrochen wurde.

## [0.39] - 2026-11-24

- Tests statt „läuft bei mir". 27 Prüfungen mit der Standardbibliothek (`tests/`): Ini-Behandlung
  (doppelte Schlüssel, Kommentare, CRLF, Idempotenz), Mod-Reihenfolge und Anpinnen, Update-Entscheidung
  (kein Rückwärts-Angebot), Vollständigkeit der Routen und ein Rauchtest, der den Webserver in einem
  temporären Verzeichnis startet und Anmeldung, Kernrouten und Instanzverwaltung prüft.
- **GitHub Actions** (`.github/workflows/ci.yml`): bei jedem Push und Pull Request auf Python 3.10,
  3.12 und 3.13 - Stilprüfung, Textprüfung, Tests.
- **`ruff` sauber** mit Konfiguration in `pyproject.toml`; dabei gefundene echte Fehler behoben:
  doppelte Textschlüssel (der zweite Eintrag hat den ersten still überschrieben), unbenutzte
  Zuweisungen, fehlendes `raise … from`, mehrdeutige Variablennamen.
- Der POST-Handler ist zerlegt. Statt einer 559-Zeilen-Kette gibt es jetzt 22 Methoden je
  Fachthema (Mods, Dateien, Backups, Zeitplan …) und eine Route-Tabelle `_POST_ROUTES`. Verhalten
  unverändert: gegen die Vorgängerfassung wurden 31 Anfragen verglichen, keine Abweichung.
- `CONTRIBUTING.md` beschreibt Testlauf, Regeln für Änderungen und Fehlermeldungen.

## [0.38] - 2026-11-24

- Freie Lizenz: MIT. Das Projekt stand bisher unter „alle Rechte vorbehalten". Ab jetzt darf
  jeder es nutzen, ändern, weitergeben und auch kommerziell einsetzen - Bedingung ist nur, dass
  Copyright-Hinweis und Haftungsausschluss erhalten bleiben. `LICENSE` enthält den vollständigen
  Text, README und Dokumentation sind angepasst, die Fußzeile zeigt „MIT-Lizenz".

## [0.37] - 2026-11-24

- Dateiliste auf dem Handy ohne Seitwärts-Scrollen. Jede Zeile ist jetzt ein kleiner Block:
  Dateiname oben links, Größe oben rechts, Datum unten links, die vier Aktions-Kästchen unten
  rechts. Statt die 520-px-Tabelle seitlich zu schieben, passt alles in die Bildschirmbreite.

## [0.36] - 2026-11-24

- Aktions-Kästchen auf dem Handy 36 × 36 px. Beim Aufräumen war die Vergrößerung für schmale
  Bildschirme verloren gegangen; die Felder bleiben jetzt auch mobil groß genug für den Daumen.

## [0.35] - 2026-11-24

- Streuklammer im Stylesheet. Nach dem Umbau der Handy-Regeln blieb eine überzählige `}` in
  den Basisstilen stehen; die Dateiliste verlor dadurch ihr `overflow-x` und schob die Seite auf
  543 px. Regel sitzt jetzt im Handy-Block, die Seite bleibt bei 375 px.

## [0.34] - 2026-11-24

- Dateiliste schob die Seite in die Breite. Die Tabelle mit 520 px Mindestbreite zwang die
  ganze Seite auf 556 px, obwohl der Bildschirm 390 px hat - man musste die Seite seitlich
  schieben. Abschnitte und Karten dürfen jetzt schrumpfen (`min-width:0`), die Tabelle scrollt
  nur in ihrem eigenen Kasten.

## [0.33] - 2026-11-24

- Server-Log auf dem Handy lesbar. Schrift von winzig auf 12 px, mehr Zeilenhöhe und ein
  höherer Logkasten (58 vh), damit man nicht zoomen muss. Statusabzeichen in der Kopfzeile sind
  etwas größer und besser zu treffen.

## [0.32] - 2026-11-24

- Kopfzeile auf dem Handy ist eine Zeile. CPU, RAM, Version, Changelog, Panel-Neustart und
  Sprachwahl stehen nebeneinander und lassen sich seitlich wischen, statt in vier Zeilen
  untereinander zu laufen. Der Kopf schrumpft dadurch von 227 auf rund 90 Pixel.

## [0.31] - 2026-11-24

- Handy-Regeln griffen nicht. Der Mobile-Block stand mitten im Stylesheet und wurde von
  späteren Basisregeln überschrieben - Eingabefelder blieben bei 14 px (und das iPhone zoomt beim
  Antippen hinein), die Kopfzeile blieb 248 px hoch. Die Regeln stehen jetzt als eigener Block am
  Ende des Stylesheets und gelten sicher.

## [0.30] - 2026-11-24

- Handy-Ansicht aufgeräumt. Unter 720 px Breite: einspaltiges Layout, Karten und Abschnitte
  in voller Breite, Kennzahlen 2×2 statt 4 nebeneinander, Einstellungen mit Beschriftung über dem
  Feld statt daneben, Tabs waagerecht scrollbar, Knöpfe mindestens 40 px hoch und Eingabefelder
  mit 16 px Schrift (verhindert das Hineinzoomen auf dem iPhone). Kopfzeile bricht um, statt
  über den Rand zu laufen.

## [0.29] - 2026-11-24

- Aktions-Symbole in der Dateiliste sind jetzt Kästchen. Statt nackter kleiner Symbole steht
  jede Aktion in einem eigenen Feld (30×30 px, auf dem Handy 34×34): Herunterladen grün umrandet,
  Löschen rot. Dadurch sind sie mit dem Finger sicher zu treffen.
- Die Dateiliste scrollt auf schmalen Bildschirmen waagerecht, statt Spalten zu quetschen.

## [0.28] - 2026-11-24

- Vollansicht lag im falschen Abschnitt. Das Overlay stand im Übersichts-Reiter (der beim
  Öffnen ausgeblendet ist) statt außerhalb der Tabs - dadurch blieb es unsichtbar, obwohl der
  Inhalt geladen wurde. Es hängt jetzt direkt hinter `<main>` und deckt die Seite unabhängig vom
  aktiven Reiter ab.

## [0.27] - 2026-11-24

- Dateien herunterladen. Jede Datei hat in der Liste einen eigenen Download-Pfeil (⬇) - ein
  echter Link, der Browser speichert die Datei direkt, ohne Umweg über den Editor. Endung und
  Name bleiben erhalten (`Content-Disposition`).
- Direkte Vollansicht. Das Symbol ⤢ öffnet die Datei im Vollbild über die ganze Seite: großer
  Editor, Speichern, Herunterladen, Schließen. `Esc` schließt sie wieder. Der kleine Vorschaukasten
  darunter bleibt für den schnellen Blick.

- Aktionsspalte in der Dateiliste. Herunterladen, Vollansicht, Umbenennen und Löschen stehen
  jetzt als eigene Symbole rechts in der Zeile statt zwischen Dateinamen und Größe.

## [0.26] - 2026-11-24

- Die Update-Anzeige bot einen Rückschritt an. Stand lokal schon eine neuere Version als auf
  GitHub (eigener Deploy vor dem Push), meldete das Panel „update 0.25 → 0.24“ - also ein
  Downgrade als Update. Jetzt gilt nur noch eine **höhere** GitHub-Version als Update; ist die
  eigene Fassung voraus, bleibt die Anzeige auf „aktuell“.
- Veralteter Cache hielt die alte Anzeige fest. Der 10-Minuten-Cache wurde auch dann
  ausgeliefert, wenn die darin vermerkte „neue“ Version älter war als die installierte. Solche
  Einträge werden jetzt verworfen und frisch geprüft.
- Die Build-Datei wird nicht mehr mitgeliefert. `.build` lag im Repo und wurde bei jedem
  Deploy mit einer uralten Fassung (0.3.34) überschrieben - dadurch meldete das Panel dauerhaft
  „neuer Build verfügbar“, obwohl Version und Commit schon stimmten. Die Datei entsteht jetzt nur
  noch beim Update bzw. Deploy.

## [0.25] - 2026-11-24

- Aktionsleiste der Instanzkarten. Statt sechs grauer Textknöpfe steht auf jeder Karte eine
  farbige Pille mit drei Gruppen - wie in einem Dateimanager: **rot** anhalten und löschen,
  **blau** Menü, Update, AsaApi, **grün** starten und neu starten. Die Symbole tragen den Text als
  Tooltip, gesperrte Aktionen bleiben sichtbar (blass) statt zu verschwinden, und ein kleiner Punkt
  am AsaApi-Symbol zeigt an, dass dort ein Update wartet.

## [0.24] - 2026-11-24

- Mods sortieren und anpinnen. Im Mods-Reiter lassen sich aktive Mods mit ▲/▼ oder per
  Drag & Drop umsortieren; ein Pin (📍) hält eine Mod dauerhaft oben (📌) - etwa Stacking-Mods, die
  früh laden müssen. Die Reihenfolge ist die **Ladeliste**: sie wandert in `-mods=` der Startzeile
  und in `ActiveMods` der Game.ini. Eine reine Umsortierung schreibt nur diese eine Zeile.

- Die Game.ini wird nicht mehr neu geschrieben. `write_ini()` hat sie über `configparser`
  komplett neu erzeugt; der Parser hält je Sektion nur einen Wert pro Schlüssel und wirft
  Wiederholungen weg. In einer echten ARK-Datei verschwanden so 795 `EngramEntryAutoUnlocks`,
  156 `ConfigOverrideItemMaxQuantity` und 99 `OverridePlayerLevelEngramPoints` - aus 1.182 Zeilen
  und 121 KB wurden 128 Zeilen und 18 KB. Werte wurden zusätzlich umgeschrieben (`true` → `True`,
  `DifficultyOffset=4` → `1.0`). Jetzt werden nur einzelne Zeilen gesetzt; alles andere bleibt Byte
  für Byte erhalten, inklusive Kommentaren, Reihenfolge und CRLF.
- Admin-Werte in der GameUserSettings.ini bleiben stehen. `ServerPVE`, `DifficultyOffset`,
  `ServerCrosshair` und `ShowMapPlayerLocation` werden nur noch eingetragen, wenn der Schlüssel
  fehlt. RCON, Passwörter, Ports und `MaxPlayers` setzt das Panel weiterhin durch.
- INI-Sicherungen landen im Unterordner `backup/` neben den INIs statt als `.bak` daneben
  (je Datei die letzten 20 Fassungen). Der Config-Ordner sammelt keine Sicherungsdateien mehr.
- Zeilenenden bleiben erhalten. Gespeicherte INIs wurden mit LF statt CRLF geschrieben und
  schrumpften dabei um ein Byte je Zeile.
- Backups „vor Update“ heißen so statt unter „älter“ zu laufen.

## [0.23] - 2026-11-22

- Speichern-Knopf im Snapshot-Bereich. Snapshot-Uhrzeiten und „Auto-Snapshots behalten" hatten
  kein eigenes Speichern; man musste zum Zeitplan scrollen. Ein eigener Knopf schreibt jetzt nur diese
  beiden Werte (`/api/schedule` mit `snaptimes`/`snapkeep`) und laesst Neustart-, Backup- und
  Vorwarnzeiten unangetastet.
- **Backup-Box ist zurueck** (0.22). Im Tab „Verwaltung" stehen wieder Welt-Backups (Liste, „Jetzt
  sichern", Einspielen, Loeschen). Die JavaScript-Funktionen waren vorhanden, das HTML-Geruest fehlte;
  die Liste laedt jetzt beim Wechsel auf „Verwaltung". Ein Hinweis daneben nennt die
  Instanz-Snapshots als Weg fuer einen Ruecksprung auf die alte Serverversion.

### Geaendert
- **Neue Instanzen** bekommen `OverrideOfficialDifficulty=10.0` (wilde Dinos bis Level 300) und
  `bServerRCONOutputTribeLogs`/`bServerGameLogIncludeTribeLogs` (Tribe-Logs an RCON/Gamelog,
  Voraussetzung fuer Tame-/Claim-Quests).

## [0.21] - 2026-11-16

- Die Karte zeigt, was gerade läuft. Bisher stand bei einem laufenden Update nur „AUS". Jetzt
  erscheint eine Hinweiszeile (⏳ UPDATE LÄUFT, INSTALLATION LÄUFT, NEUSTART LÄUFT, WIRD GESTOPPT,
  WIRD GELÖSCHT, ASAPI WIRD EINGERICHTET) aus den laufenden Aktionen des Panels; `runner.stop()` meldet
  seinen Zustand mit, damit der Stopp sichtbar wird. Die Statusabzeichen nennen den Vorgang auch auf
  der Detailseite („FÄHRT HERUNTER" gelb statt bis zuletzt „LÄUFT"), die Knöpfe bleiben bis zum Ende
  gesperrt.

- **Mod-Beschreibungen** werden vollständig übersetzt (kein Abschneiden bei 400 Zeichen mehr, Stücke
  mit Wiederholung, Ausweichdienst bei Google-Rate-Limit, keine englischen Texte mehr im Cache) und
  lesbar umbrochen: Rollenangaben („Primary roles", „Hauptfunktionen", „Hauptaufgaben") und lange
  Sätze auf eigenen Zeilen; in der Trefferliste bis zu fünf Zeilen statt hartem Schnitt bei 90 Zeichen.

## [0.18] - 2026-11-15

- Kein zusätzliches Fenster mehr beim Anlegen und Installieren. Das Anlegen bleibt in der
  Übersicht (die neue Karte erscheint dort), die Installation zeigt ihren Fortschritt im selben Tab.

- Server-Passwort bleibt erhalten. `write_ini()` hat `ServerPassword` bei jedem Start fest auf leer
  gesetzt; ein eingetragenes Beitrittspasswort war damit nach dem nächsten Start weg. Jetzt steht es in
  der Instanz, wandert in die INI und als `?ServerPassword=` in die Startzeile (Admin-Passwort bleibt
  die letzte Option, sonst schluckt sie den Rest).
- Munition im Gegenstands-Dialog. Alle Munitionseinträge zeigten auf `Items/…`, die Assets liegen
  aber unter `Weapons/…` - Geben scheiterte stillschweigend. Pfade korrigiert, fehlende Munition
  ergänzt (u. a. Einfache Gewehrmunition). Beschriftung berichtigt: `OneShotRifle` ist das
  Longneck-Gewehr, die Schrotflinte (`PrimalItem_WeaponShotgun`) fehlte ganz.

## [0.17] - 2026-11-14

- AsaApi gehört zur Installation. Nach dem SteamCMD-Lauf richtet das Panel AsaApi automatisch ein
  (komplettes Release inklusive `config.json` und der mitgelieferten DLLs) und startet die Instanz
  danach über `AsaApiLoader.exe`. Der Knopf **„API"** auf der Karte installiert oder aktualisiert die
  API jederzeit von Hand; er erscheint nur, wenn er etwas zu tun hat, und trägt bei einem neueren
  Release ein Badge mit der Version. Im Reiter „Mods" schaltet eine Checkbox die API samt Plugins
  wieder aus (Start ohne Loader). Schlägt die Installation fehl, bleibt der Server installiert und der
  Knopf ist der Nachhol-Weg. Installationsprüfung und Startschutz orientieren sich weiter an der
  echten Server-EXE, damit eine Instanz ohne Loader nicht als „nicht installiert" gilt.
- Firewall wird mitgemacht. Beim Start trägt das Panel Spiel- und Query-Port (UDP) in `ufw` ein,
  beim Löschen der Instanz werden die Regeln wieder entfernt. Für `ufw` legt der Installer eine eng
  begrenzte `sudo`-Regel an (nur `/usr/sbin/ufw`); fehlt sie, startet der Server trotzdem und das
  Panel-Log nennt den Grund.
- Mod-IDs direkt eintragen. Im Reiter „Mods" gibt es ein Feld für die Mod-IDs (Komma, Semikolon
  oder Leerzeichen als Trenner). Es zeigt die aktive Liste und ersetzt sie beim Speichern.
- Datei-Browser im Panel. Der Reiter „Dateien" zeigt den Instanzordner: Ordner öffnen, mehrere
  Dateien gleichzeitig hochladen, herunterladen, umbenennen, löschen, Ordner anlegen. Pfade mit `..`
  werden abgewiesen, Downloads laufen als Stream. Klick auf den Namen öffnet Textdateien bis 2 MB im
  Browser (Binärdateien abgewiesen), „Speichern" schreibt zurück und legt eine `.bak`-Sicherung an.
- SFTP-Zugang pro Instanz. Eigener Benutzer, generiertes Passwort, Port aus
  `sftp_base_port + laufender Nummer` (Standard 2225), Chroot auf den Instanzordner -
  FileZilla-kompatibel (SFTP, kein FTP). „Neues Passwort" kopiert es in die Zwischenablage, „aus"
  schließt den Port. Der Dienst läuft als `ascendedpanel-sftp`; ist kein Benutzerbus erreichbar (Panel
  per `nohup`), startet er abgekoppelt mit `sftp.pid`. Voraussetzung: `asyncssh` - fehlt es, läuft das
  Panel weiter und nur der SFTP-Dienst meldet im Panel-Log, was fehlt.

- Metriken zählen alle Prozesse der Instanz. Unter Wine/Proton und mit API-Loader hängt der
  Serverprozess nicht an der Starter-PID, deshalb erschienen CPU und RAM als 0; jetzt werden alle
  Prozesse der Instanz über ihre Kommandozeile gefunden und summiert.
- SessionName und MaxPlayers bleiben erhalten (Werte aus `GameUserSettings.ini` wandern zurück in
  die Instanz), und die Sektion in der `Game.ini` wird unabhängig von der Schreibweise erkannt.
- Token bleibt gleich. Der Web-Token wird nur beim allerersten Start erzeugt und danach aus
  `~/.config/ascendedpanel/token` gelesen - Neustart, Update und Selbst-Update ändern ihn nicht; ein
  neuer entsteht erst, wenn die Datei gelöscht wird. Das Instanz-JSON kennt dafür `sftp_enabled`,
  `sftp_user`, `sftp_password`, `sftp_port` und zeigt `sftp://***@host:port`.
- Tribe-Logs über RCON. Der Startbefehl enthält zusätzlich `-ServerRCONOutputTribeLogs`; zusammen
  mit `-servergamelog` und `-servergamelogincludetribelogs` landen Claim-/Tame-Zeilen in der
  Serverlogdatei und im RCON-Logpuffer.

- Start über `AsaApiLoader.exe` brach mit „LoaderFailed, Reason: UnknownLoaderResult" ab, wenn im
  Win64-Ordner die `config.json` des API-Releases fehlte.
- Eine doppelte `ActiveMods`-Zeile konnte dafür sorgen, dass eingetragene Mods beim Start
  stillschweigend ignoriert wurden.

## [0.14] - 2026-11-13

- Download-Geschwindigkeit im Installationsfenster. Neben Schritt und Prozent steht die aktuelle
  Rate in MB/s - aus den Byte-Zahlen der steamcmd-Zeilen berechnet und geglättet, damit die Anzeige
  nicht springt.

- Instanzen starten nach der Installation nicht mehr von selbst. Der Supervisor wurde direkt nach
  der Installation aktiviert und deutete „Prozess weg" beim nie gestarteten Server als Absturz. Jetzt
  wird die Instanz vor dem Dienststart als „gestoppt" markiert (`runner.mark_stopped`); Start nur über
  „Start" im Panel, auch nach einem Systemstart.
- Installationsbalken und Fortschritts-API. Der Balken sprang zurück, weil SteamCMD jede Phase bei
  0 % beginnt - er zeigt jetzt den Gesamtfortschritt und fällt nie unter den Höchstwert.
  `/api/install/progress` warf einen Fehler, sobald eine Fortschrittszeile im Log stand (die
  Phasentabelle `_PHASE_STEP` wurde benutzt, aber nie definiert). „Installieren" öffnet wieder den
  Fortschritt, auch wenn zuletzt der Reiter „Einstellungen" offen war.
- Löschen blockiert die Oberfläche nicht mehr. Stoppen und Entfernen mehrerer GB laufen als
  Hintergrund-Job; die Karte zeigt „Server wird gestoppt …", dann „Serverdateien werden gelöscht …" und
  die freigegebene Größe. Jeder Löschvorgang steht mit Zeitstempel und MB im `panel.log`.
- Instanzkarte ohne leere Angaben. Fehlt die Karte oder der RCON-Port, erscheint kein nacktes „·"
  mehr, sondern nur `<Karte> · Port <n> · RCON <n>`.
- Wine wird im Installer ohne Rückfrage installiert - wie Xvfb. Die Frage „Wine installieren?"
  wurde erfahrungsgemäß mit „nein" beantwortet, danach startete kein Windows-Spiel.

## Überblick

Grobe Zusammenfassung dessen, was im Panel steckt.

- Ein Panel, ein Unterbau: AscendedPanel für ARK: Survival Ascended, Bedienung im Browser, Dienst
  auf dem Server.
- **Dashboard:** Instanzkarten mit Status, Karte, Ports, Build, CPU/RAM, Spielern und Laufzeit; Start,
  Restart, Update, Stop und Löschen direkt auf der Karte, Knöpfe sperren sich nach Zustand.
- **Instanzseite:** Live-Log, Konfigurationseditor mit Sicherung und Prüfung (INI-Werte als Formular
  oder roh), Mod-Verwaltung mit CurseForge-Suche/Update-Prüfung, Backups, Snapshots, Zeitplan,
  RCON-Konsole mit Ein-Klick-Befehlen, Datei-Browser und SFTP.
- **Spieler:** Liste mit Kick, Ban, Whitelist und Gegenstände verteilen - Katalog mit Suche und
  Mengenfenster; die nötige Spieler-ID (ARKID) wird aus den `.arkprofile`-Dateien gelesen, weil ARK
  per RCON nur die EOS-ID liefert.
- **Sperren:** eigenes Fenster „Gesperrte Spieler" mit Entbannen je Zeile und ehrlichem Hinweis, warum
  ARK seine Ban-Liste nicht über RCON herausgibt.
- **Betrieb:** Absturz-Erkennung mit automatischem Neustart, Discord-Benachrichtigungen, Sprache
  Deutsch/Englisch jederzeit umschaltbar, mehrere Instanzen in einem Prozess.
- **Fehlermeldungen:** Knopf im Panel, Meldung geht an den Betreiber (Webhook, nur auf der Konsole
  setzbar) - mit Version, Instanz, System und Logauszug, Passwörter entfernt.
