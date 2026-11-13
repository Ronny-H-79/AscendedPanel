## [0.4.57] — 2026-11-13

### Geändert
- **Kein Test-Versand mehr für Fehlermeldungen** — weder in der Oberfläche noch auf der Konsole
  (`report-test` entfallen). Der Melde-Knopf schickt nur noch echte Meldungen.

## [0.4.56] — 2026-11-13

### Geändert
- **Melde-Webhook ist jetzt reine Betreiber-Sache.** Das Feld, der Speichern- und der
  Test-Knopf sind aus der Oberfläche verschwunden; gesetzt wird die Adresse nur noch auf der
  Konsole: `ascendedpanel report-webhook https://discord.com/api/webhooks/…` (ohne Wert zeigt sie
  die maskierte Adresse, `-` entfernt sie), Test mit `ascendedpanel report-test`.
- Der Abschnitt „Fehler melden" erscheint nur, wenn ein Webhook hinterlegt ist — ohne Adresse ist
  die Funktion für Nutzer unsichtbar, statt mit Fehlermeldung dazustehen. Die API-Wege zum Setzen
  und Testen sind entfallen, damit niemand über die Oberfläche an die Adresse kommt.

## [0.4.55] — 2026-11-13

### Geändert
- **Melde-Webhook wird jetzt maskiert angezeigt** (`https://discord.com/api/webhooks/…`).
  Das Eingabefeld bleibt leer — die vollständige Adresse wird nie an den Browser geschickt;
  neben den Knöpfen steht, welche Adresse hinterlegt ist. Leer speichern entfernt sie.

## [0.4.54] — 2026-11-13

### Neu
- **Fehler melden aus der Oberfläche.** Einstellungen → „Fehler melden": kurzes Fenster mit
  „Was ist passiert?" und optional „Wie kam es dazu?"; die Meldung geht an einen Discord-Webhook.
  Mitgeschickt werden automatisch Panel-Version, Instanz und Karte, Betriebssystem und Python sowie
  die letzten 30 Logzeilen. Passwörter, RCON- und Admin-Passwörter, Token und API-Keys werden vorher
  entfernt (`ServerAdminPassword=…`, `password: …` → `[entfernt]`); Logfelder sind auf das
  Discord-Limit gekürzt.
- Der Melde-Webhook ist eine **Panel**-Einstellung (`settings.json`, eine Adresse für alle Instanzen),
  getrennt vom Instanz-Webhook für Abstürze. Dazu **Testmeldung**, und bei Ablehnung durch Discord
  steht die Antwort im Fehlertext statt nur „HTTP 400".

## [0.4.53] — 2026-11-13

### Behoben
- **Mengen-Fenster lag hinter dem Katalog-Fenster.** Beide teilten sich `z-index: 60`;
  das Mengen-Fenster liegt jetzt auf 75, damit es beim Öffnen vorne steht.

## [0.4.52] — 2026-11-13

### Geändert
- **Mengen-Abfrage als eigenes Fenster.** Klick auf „geben" öffnet ein kleines Fenster
  „Menge für <Gegenstand>" mit Zahlenfeld, **Geben** und **Abbrechen** (Enter bestätigt).
  Das Zahlenfeld in der Kopfzeile ist entfallen. Beim Weg **„eigener Blueprint"** bleibt es
  bei den zwei Rückfragen (Blueprint und Menge) — dort kommt kein zusätzliches Fenster.

## [0.4.51] — 2026-11-13

### Geändert
- **Mengen-Abfrage im Item-Dialog deutlich gemacht.** Das Zahlenfeld hat jetzt die Beschriftung
  „Menge"; ist es leer oder 0, fragt das Panel vor dem Geben nach (Eingabe abbrechen = kein
  Versand). Die Rückfrage nennt den Gegenstand, die Meldung danach zeigt die Menge (`×N`).

## [0.4.50] — 2026-11-13

### Behoben
- **Spieler-ID aus dem `.arkprofile` lesen.** Auf Servern, die unter
  `Saved/SavedArks/<Map>/` speichern, gibt es keine `PlayerCache.sav`. Die ARKID steht aber
  in der Datei `<EOS-ID>.arkprofile` als Property `PlayerDataID` (UInt64) — der Parser liest
  sie jetzt direkt (UE-Property-Kopf: Größe 8, optional GUID, dann 8 Byte Wert).
  Fallback bleibt das Server-Log (`AdminCmd: … ARKID: … PlatformID: …`) und, auf älteren
  Servern, `PlayerCache.sav`/`AwesomeAdminTools/Logs.sav`.
  Gegenprobe: EOS `00023634…` → `840709058`, Name `sorbid79` → `840709058`.

## [0.4.49] — 2026-11-13

### Neu
- **ID-Diagnose im Item-Dialog.** Neben „eigener Blueprint" sitzt jetzt ein Knopf, der zeigt, wo
  das Panel sucht: Instanzordner, gefundene Speicherdateien und Anzahl zugeordneter Spieler.
  Das macht sichtbar, ob der Pfad nicht passt oder die Save noch fehlt.
- **Notfallsuche im Benutzerordner.** Liegt im Instanzordner keine `PlayerCache.sav`, sucht das
  Panel begrenzt (20.000 Ordner / 5 Sekunden) im Home weiter — für Server mit anderem Aufbau
  oder Wine-Prefix.

## [0.4.48] — 2026-11-13

### Behoben
- **Give speichert die Welt vorher, wenn die ID fehlt.** `PlayerCache.sav` wird nur beim
  Welt-Speichern geschrieben — ein frisch gejointer Spieler fehlte dort bis zum nächsten
  Autosave (Standard 15 Minuten). Findet das Panel keine dauerhafte ID, löst es jetzt einmal
  `SaveWorld` aus, wartet kurz und versucht die Zuordnung erneut.

## [0.4.47] — 2026-11-13

### Behoben
- **ID-Ermittlung ohne `strings` und mit Diagnose.** Die Speicherdateien werden jetzt direkt in
  Python gelesen (ASCII **und** UTF-16LE, so wie UE seine Strings ablegt) — vorher hing die
  Auflösung an `strings` aus binutils, das auf schlanken Servern fehlt und dann stillschweigend
  nichts fand. Die Fehlermeldung nennt zusätzlich, wie viele Speicherdateien gefunden und wie
  viele Spieler zugeordnet wurden.

## [0.4.46] — 2026-11-13

### Behoben
- **„Item geben" lieferte nichts ins Inventar.** `GiveItemToPlayer` verlangt die
  **dauerhafte** Spieler-ID (z. B. `761591001`), nicht die EOS-ID aus `ListPlayers`
  (`00023634…`). Mit der falschen ID meldet RCON „ok", im Inventar landet nichts. Das Panel
  ermittelt die dauerhafte ID jetzt aus `PlayerCache.sav` und `AwesomeAdminTools/Logs.sav`
  der Instanz (neues Modul `playerids.py`, Cache 2 Minuten). Ist der Spieler unbekannt, kommt
  eine klare Meldung statt eines stillen Fehlschlags.
- Auf der Instanzseite bleibt eine Spielerliste jetzt bei jedem Refresh der Übersicht
  verfügbar, damit das Give-Ziel auch beim Geben bekannt ist.

## [0.4.45] — 2026-11-13

### Geändert
- **Knopf „Spielerliste" aus dem Befehlsbereich entfernt.** Die Liste steht auf der
  Instanzseite und im Dashboard-Fenster — als RCON-Knopf war sie doppelt.

## [0.4.44] — 2026-11-13

### Geändert
- **RAM-Hinweis ohne Kartenbezug.** Statt „The Island ohne Mods ca. 10 GB" steht dort jetzt
  „ab ca. 10 GB (ohne Mods), mit Mods und Spielern mehr" — die 10 GB gelten allgemein, nicht
  für eine bestimmte Karte. Auch in `INSTALL.md` korrigiert.
- **Bannen-Knopf aus dem Whitelist-Tab entfernt.** Gebannt wird in der Spielerliste bzw. im
  Dashboard-Fenster; im Whitelist-Tab bleibt nur das Eintragen.

## [0.4.43] — 2026-11-13

### Geändert
- **Überschrift „Whitelist & Bans" → „Whitelist".** Die Ban-Liste steht jetzt im eigenen
  Fenster; der Verwaltungs-Tab enthält nur noch Whitelist und das Bannen per ID.

## [0.4.42] — 2026-11-13

### Geändert
- **Doppelte Ban-Liste in „Verwaltung" entfernt.** Dort stand noch eine zweite Liste
  („Gebannt (über …)"), die aus dem alten Instanz-Register kam — ohne Namen und ohne
  Zeitpunkt. Die Liste gibt es jetzt nur einmal, im Fenster „Gesperrte Spieler". Bannen über
  die ID im Verwaltungs-Tab trägt sich weiterhin ein und erscheint dort mit Namen.

## [0.4.41] — 2026-11-13

### Geändert
- **Hinweis im Ban-Fenster umformuliert.** Statt „Nur Sperren, die über dieses Panel gesetzt
  wurden" heißt es jetzt „Hier stehen nur Spieler, die über dieses Panel gesperrt wurden" —
  es geht um Personen, nicht um Sperren.

## [0.4.40] — 2026-11-13

### Behoben
- **Ban aus der Spielerliste funktionierte nicht mehr.** Mein Fehler: Der Name wurde als
  `JSON.stringify` direkt in den `onclick` geschrieben — ein Anführungszeichen im Spielernamen
  hat damit das Attribut zerrissen und der Klick lief ins Leere. Der Name kommt jetzt über eine
  JS-Map (`window.PNAMES`) bzw. ein maskiertes `data`-Attribut, nie unmaskiert ins HTML.

## [0.4.39] — 2026-11-13

### Neu
- **Hinweis zur Ban-Liste.** Im Fenster steht jetzt, dass dort nur Sperren aus dem Panel
  erscheinen — ARK gibt die Liste nicht über RCON her. Außerhalb gebannte Spieler lassen sich
  über das EOS-ID-Feld entbannen.

## [0.4.38] — 2026-11-13

### Neu
- **Fenster „Gesperrte Spieler" auf der Instanzseite.** Zeigt alle über das Panel gebannten
  Spieler mit Name, EOS-ID und Zeitpunkt — jeweils mit **Entbannen**-Knopf. Nötig, weil ARK
  die Ban-Liste nicht über RCON liefert (`ListBannedPlayers` antwortet leer); das Panel führt
  die Liste deshalb selbst in `bans.json` neben der Instanz. Wer außerhalb des Panels bannt,
  bleibt über das EOS-Feld entbannbar.

## [0.4.37] — 2026-11-13

### Geändert
- **RAM-Hinweis korrigiert.** Die Angabe „ohne Mods ca. 4 GB, mit Mods 11–12 GB" war deutlich zu
  niedrig: The Island braucht **schon ohne Mods rund 10 GB**, mit Mods und Spielern entsprechend
  mehr. Der Hinweis nennt jetzt den gemessenen Wert; eine Obergrenze gibt es nicht.

## [0.4.36] — 2026-11-13

### Neu
- **Item-Dialog mit Liste statt Freitext.** Statt den Blueprint-Pfad zu tippen, öffnet der
  Knopf „Item" eine durchsuchbare Liste bekannter Gegenstände (Werkzeuge, Waffen, Munition,
  Verbrauch, Rohstoffe, Rüstungen) samt Menge. Der vollständige Pfad steckt in
  `ascendedpanel/catalog.py`; ein eigener Blueprint lässt sich weiterhin eingeben.
- Neuer Endpunkt `/api/catalog?q=` für die Suche.
- **Entbannen-Fenster auf der Instanzseite.** Über der Spielerliste öffnet „Entbannen" ein
  Fenster für die EOS-ID eines gesperrten Spielers — nötig, weil man Offline-Spieler nicht
  anklicken kann und ARK keine Ban-Liste über RCON liefert.

### Geändert
- **Ungenutzte Log-Styles entfernt** (`.logwrap`, `.loghead`, `.cardlog`) — Reste des
  Karten-Logfensters von der Startseite.

## [0.4.35] — 2026-11-13

### Geändert
- **Kein Logfenster mehr auf der Startseite.** Bei vielen Instanzen wurde die Übersicht zu
  voll, und jede Karte hat zusätzlich alle 2,5 Sekunden Logzeilen nachgeladen. Das Log steht
  weiterhin auf der Instanzseite; die Karten zeigen nur noch Status, Auslastung und Aktionen.

## [0.4.34] — 2026-11-13

### Geändert
- **Menü bleibt immer bedienbar.** Auch während Stop, Start, Restart oder Update ist der
  Menü-Knopf aktiv — Log, Konfiguration und Seiten bleiben erreichbar, gesperrt sind nur die
  Aktionen, die gerade nicht sinnvoll sind.

## [0.4.33] — 2026-11-13

### Neu
- **Spielerfenster in der Übersicht.** Ein Klick auf die Spielerzahl öffnet ein Fenster mit
  allen Spielern der Instanz: Name, **EOS-ID** und die Aktionen **Kick**, **Ban** und **Unban**.
  Ban fragt vorher nach; nach jeder Aktion wird die Liste neu geladen.

## [0.4.32] — 2026-11-13

### Geändert
- **Update ist auch bei gestoppter Instanz bedienbar.** Genau dann werden die
  Serverdateien getauscht — vorher war der Knopf im gestoppten Zustand gesperrt.

## [0.4.31] — 2026-11-13

### Behoben
- **Spielerzahl stand dauerhaft auf 0, obwohl Spieler online waren.** Die Erkennung der
  `ListPlayers`-Zeilen akzeptierte als Spieler-ID nur 15–17 Ziffern (SteamID-Format). ARK:
  Survival Ascended liefert dort aber die **32-stellige EOS-ID in Hex** — keine Zeile passte,
  die Liste blieb leer. Dashboard-Kachel, Prozess-Zeile und `/api/players` akzeptieren jetzt
  beide Formate und auch Namen mit Sonderzeichen (`RunGunTeufel | Teufelswerk`).

### Geändert
- **Knöpfe sperren sich passend zum Zustand.** Läuft ein Stop, sind alle Knöpfe unbedienbar.
  Läuft Start, Restart oder Update (oder fährt die Instanz noch hoch), bleibt **nur Stop**
  bedienbar — zum Abbrechen. Der Zustand kommt vom Server (`action` in `/api/instances`) und wird
  beim Klick sofort lokal gesetzt, damit Doppelklicks nicht durchrutschen.
- **„1 Instanzen" statt „1 Instanz".** Die Anzahl auf dem Dashboard nutzt jetzt die Einzahl,
  wenn genau eine Instanz existiert (neuer Textschlüssel `dash.instance_single`).


## [0.4.29] — 2026-11-11

### Behoben
- **„Restart" verhielt sich wie „Stop" — der Server kam nicht wieder hoch.** Der Neustart lief als
  Folge `stop(); sleep(3); start()` in einem Thread ohne Fehlerbehandlung: scheiterte der Start (z. B.
  weil Wine die Ports noch hielt), blieb der Server einfach aus, ohne jede Meldung. Jetzt gibt es
  `runner.restart()`: Stop, warten bis Spiel-, Query- und RCON-Port wirklich frei sind (eigene
  Wine-Reste werden dabei beendet), Start mit einem Wiederholungsversuch. Klappt es nicht, nennt die
  Fehlermeldung alle Schritte und den blockierenden Port.
- **Fehlschläge von Start/Restart/Update sind sichtbar.** Sie landen in `<instanz>/.start.log`, im
  Supervisor-Log und als Ereignis in Discord — vorher verschluckte der Thread die Ausnahme still.
- **Zeitplan-Aufgabe „Restart" tat nichts** (fiel auf „unbekannte Aktion"). Sie nutzt jetzt denselben
  Ablauf.
- Die Installation über die Oberfläche schickte nach der Erfolgsmeldung noch eine 404-Antwort
  hinterher.

## [0.4.28] — 2026-11-11

### Behoben
- **Das Admin-Passwort war nach jedem Neustart (und damit nach jedem Update) wieder das alte.**
  Die Startzeile bekam immer das RCON-Passwort (`?ServerAdminPassword=<rcon_password>`), in die
  `GameUserSettings.ini` wurde dagegen das Admin-Passwort geschrieben. ASA liest den Wert aus der
  Startzeile und überschreibt damit beim Start die INI — ein gesetztes Admin-Passwort war also nach dem
  nächsten Start weg. Startzeile, INI und RCON-Anmeldung nutzen jetzt dieselbe Quelle
  (`Instance.admin_pw`: Admin-Passwort, sonst RCON-Passwort).
- **Ein im Konfig-Editor gesetztes Admin-Passwort landet jetzt in der Instanz.** Bisher galt es nur bis
  zum nächsten Start; `config.set_value` und `config.write` (Formular und Roh-INI) übernehmen den Wert
  in die Instanz-Config und damit in die Startzeile.
- **RCON-Anmeldung nutzt dieselbe Quelle** (Konsole, Spielerliste, Backups, Broadcast, CLI `rcon`).
  Sonst antwortet RCON „Passwort falsch", sobald Admin- und RCON-Passwort auseinanderlaufen.
- Hinweis am Feld korrigiert: „leer = RCON-Passwort" statt „leer = kein Admin-Zugang".

## [0.4.27] — 2026-11-11

### Neu
- **Fortschrittsbalken bei der Installation.** SteamCMD meldet während des Downloads
  `Update state (0x61) downloading, progress: 42.31`. Diese Zeile wird jetzt ausgewertet
  (`GET /api/install/progress`) und die Oberfläche zeigt darüber einen Balken mit Phase und Prozentwert
  — bei „preallocating"/„verifying" ohne Prozentwert steht die Phase als Text. Am Ende läuft der Balken
  auf 100 % und blendet sich aus. Das Installationsprotokoll zeigt statt 10 jetzt die letzten 40 Zeilen.
- Die erste Phase (Steam-API, Client-Konfiguration) hat keinen Prozentwert — der Balken erscheint
  erst, wenn der eigentliche Download beginnt.

### Geändert
- **Prüfskript für die Installer-Texte** (`tools/check_texts.py`): vergleicht jeden Aufruf
  `$(t SCHLUESSEL …)` mit den Platzhaltern im Text und meldet fehlende Argumente sowie unbekannte
  Schlüssel. Genau diese Klasse Fehler hatte die Abfrage ohne Paketnamen erzeugt.
- **Die Build-Anzeige verschwand bisher stillschweigend.** Wenn der Server noch nicht installiert war
  oder die Steam-Abfrage scheiterte (z. B. fehlende 32-Bit-Bibliotheken), wurde das Abzeichen einfach
  ausgeblendet — es sah aus, als würde die Update-Prüfung gar nicht laufen. Jetzt steht dort
  „UPDATE-STATUS UNBEKANNT" mit Begründung im Tooltip („noch nicht installiert" bzw. „Steam-Abfrage
  fehlgeschlagen"), und ein Klick fragt sofort neu an.
- **Update-Prüfung fragt nicht mehr jede Minute bei Steam nach.** Jede offene Browserseite rief alle
  60 Sekunden `/api/update` auf, und der Server startete dafür jedes Mal einen eigenen
  `steamcmd`-Prozess (`+app_info_print`, Timeout bis 180 s). Das Ergebnis wird jetzt **15 Minuten**
  zwischengespeichert, die Oberfläche fragt nur noch alle **5 Minuten** nach. Ein Klick auf die
  Build-Anzeige erzwingt eine frische Abfrage bei Steam.

### Behoben
- **Seite war nach dem Update tot.** Der eingefügte Fehlertext enthielt ein echtes Zeilenende im JavaScript-String; damit war der ganze `<script>`-Block ungültig (SyntaxError) und keine Schaltfläche reagierte mehr. Der Text ist jetzt korrekt maskiert (`\\n`), `node --check` über alle Vorlagen läuft fehlerfrei.
- **„Start" tat scheinbar nichts.** Die Oberfläche verschluckte jede Fehlermeldung
  (`catch(e){}`), also blieb bei belegtem Port, fehlenden Serverdateien oder einem Problem mit dem
  Supervisor einfach alles stumm. Jetzt erscheint ein Hinweis mit dem echten Text, z. B.
  „Port 7780 ist schon belegt …" oder „Server nicht installiert".
- **Bei „… fehlt. Jetzt installieren?" stand kein Paketname davor.** Der Aufruf übergab ein leeres
  Argument an die Textfunktion (`t missing_ask "" "$label"`), die Meldung liest aber `$2` — dadurch
  blieb der Name leer. Betraf jede fehlende Abhängigkeit (Wine, iproute2, 32-Bit-Bibliotheken).
  Jetzt steht dort z. B. „Wine fehlt. Jetzt installieren? [j/N]"; für die Bibliotheken gibt es einen
  eigenen Satz („32-Bit-Bibliotheken fuer SteamCMD fehlen. …"), damit die Grammatik stimmt.
- **Fehlender Text beim Sprachwechsel.** Die Oberfläche zeigte bei einem Fehler im Sprachwechsel
  `undefined` plus Fehlertext, weil der Schlüssel `msg.lang_failed` im Katalog fehlte. Jetzt steht
  dort „Sprache wechseln fehlgeschlagen:" bzw. „language switch failed:".
- **Selbst-Update tat nichts: „Panel wird nicht aktualisiert".** `apply()` suchte den Paketordner im
  GitHub-Archiv unter dem Repo-Namen (`AscendedPanel/`), installiert heißt er aber `ascendedpanel/`.
  Auf Linux sind das zwei verschiedene Ordner — das Update brach mit „Paketordner fehlt im Archiv"
  ab, während die Anzeige weiter „update verfügbar" meldete. Der Ordner wird jetzt ohne Rücksicht
  auf Groß-/Kleinschreibung gesucht, damit greift das Update wieder und die Kopfzeile zeigt danach
  die neue Version.
- **Beim Installieren blieb das Protokoll leer.** SteamCMD meldet den Download-Fortschritt mit
  Wagenrücklauf (`\r`) ohne Zeilenumbruch. Der Installer las zeilenweise und bekam deshalb erst nach
  dem kompletten Download eine Zeile — bei 10–15 GB sieht das aus wie „es passiert nichts".
  Jetzt wird blockweise gelesen, an `\r` und `\n` getrennt, ANSI-Farbcode entfernt und jede
  Fortschrittszeile sofort ins `.install.log` geschrieben (`flush` je Zeile). Auch das Laden von
  SteamCMD und der genaue Befehl stehen jetzt im Protokoll.
- **Update-Protokoll zeigt jetzt ebenfalls Zeilen statt einer Riesenzeile** — derselbe Weg wie bei
  der Installation.
- **SteamCMD scheiterte auf frischen Servern mit `Exit 127`.** Ursache waren fehlende
  32-Bit-Bibliotheken (`ld-linux.so.2`, `libstdc++.so.6` i386) — ein Anfaengerfehler, den das
  Programm selbst abfangen muss. Der Installer prueft die i386-Bibliotheken jetzt in `--check`,
  installiert sie mit `--auto` (apt: `dpkg --add-architecture i386` + `lib32gcc-s1`,
  `lib32stdc++6`, `libc6:i386`; dnf: `glibc.i686`; zypper: `glibc-32bit`;
  pacman: `lib32-glibc`) und nennt sonst den genauen Befehl, der von Hand noetig ist.

0.4.7] — 2026-11-10

### Behoben
- **`ascendedpanel web` warf bei belegtem Port einen Traceback.** Wer den Web-Dienst schon laufen hatte,
  bekam `OSError: [Errno 98] Address already in use` samt Stacktrace. Jetzt erscheint eine klare
  Meldung mit drei Wegen — Dienst prüfen (`systemctl --user status ascendedpanel-web`), anderer Port
  (`ascendedpanel web --port <frei>`), oder nur die Adresse holen (`ascendedpanel url`) — und Exit-Code 1.
- **Anleitung startete den Dienst doppelt.** Nach `install.sh` läuft der Dienst bereits; in der
  Installationsanleitung stand trotzdem noch `ascendedpanel web`. Dort steht jetzt `ascendedpanel url`,
  das nur die fertige Adresse mit Token ausgibt.
- **`xvfb` gehört jetzt zur Installation.** Fehlt der virtuelle Bildschirm, bricht der ARK-Ascended-Server unter Wine ab, bevor er ins Log schreibt — Startknopf ohne Wirkung, leeres Protokoll. Installer prüft `Xvfb` jetzt wie Wine, installiert es mit `--auto` (apt `xvfb`, dnf `xorg-x11-server-Xvfb`, pacman `xorg-server-xvfb`, zypper `xvfb`).
- **Server ließ sich nicht starten.** `runner.start()` rief den Supervisor als `-m AscendedPanel.consoled` auf, das Modul heißt aber `ascendedpanel.consoled` — auf Linux startet der Prozess damit gar nicht, es entsteht keine Console-Logdatei, und `stderr` ging zusätzlich nach `/dev/null`: kein Prozess, kein Log, keine Meldung. Der Aufruf ist korrigiert, und Startausgaben landen jetzt in `<instanz>/.start.log` statt im Nichts.
- **Installation brach mit `Failed to install app '2430930' (Missing configuration)` ab.** ARK Ascended hat keinen Linux-Server; SteamCMD lädt den Windows-Zweig nur mit `+@sSteamCmdForcePlatformType windows`. Der Schalter wird jetzt bei ASA automatisch mitgegeben — bei ASE, 7D2D, Satisfactory und Space Engineers bleibt die Kommandozeile unverändert. Gilt für Installation und Update.
- **Installation lässt sich abbrechen.** Während des Downloads steht ein Knopf „Installation abbrechen“ über dem Protokoll (`POST /api/install/cancel`); er beendet die SteamCMD-Prozessgruppe, schreibt einen Vermerk ins Log und räumt den Fortschritt ab. Der halb geladene Stand bleibt liegen und wird beim nächsten Versuch weiterverwendet.
- **`Xvfb` wird ohne Rückfrage installiert.** Die Nachfrage „virtueller Bildschirm" klang entbehrlich — ohne Xvfb startet der ARK-Ascended-Server unter Wine aber gar nicht. Der Installer zieht das Paket jetzt still mit (auch als root ohne `sudo`), `--check` meldet es nur. Schlägt die Installation fehl, steht der Paketname als Hinweis da.
- **SteamCMD repariert sich jetzt selbst.** Vor jeder Installation läuft ein Selbsttest (`steamcmd +quit`); scheitert er oder meldet SteamCMD `Missing configuration`, wird der Client automatisch neu geladen und der Versuch **einmal** wiederholt — ohne Handarbeit. Nur so ließ sich die Installation auf einem frischen VPS zuverlässig durchziehen.
- **`--uninstall` räumt jetzt auch SteamCMD weg** (`~/steamcmd`, `~/.steam`) — vorher blieben die
  mehrere GB großen Clientdateien liegen, obwohl das Panel weg war.
- **Suchfeld in den Einstellungen.** Über den Reitern liegt jetzt ein Suchfeld; es filtert alle Gruppen gleichzeitig nach Name oder ini-Schlüssel (`NoTributeDownloads`), blendet leere Abschnitte aus und stellt beim Leeren den vorher gewählten Reiter wieder her.
## [0.4.6] — 2026-11-10

### Geändert
- **Zugriffsabfrage warnt jetzt vorab.** In der Frage steht bei `[3] direkt ueber IP und Port` nun
  „HTTP, nicht empfohlen". Die ausführliche Warnung samt Rückfrage (`Trotzdem so einrichten? [j/N]`)
  kommt wie bisher direkt nach der Wahl von `[3]`; wer `[1]` (SSH-Tunnel) nimmt, sieht sie bewusst
  nicht — dabei ist nichts aus dem Netz erreichbar.

## [0.4.5] — 2026-11-10

### Behoben
- **Installationsanleitung führte in die falsche Schreibweise.** `git clone … ascendedpanel` legt den
  Ordner klein an, die Anleitung verlangte danach aber `cd AscendedPanel`. Auf einem case-sensitiven
  Dateisystem bricht die Installation dort mit `No such file or directory` ab. Alle Befehle, die
  Fehlerbehebungstabelle und die Falle mit dem gleichnamigen Paketordner nennen jetzt
  `ascendedpanel`; die doppelte `cd`-Zeile in `INSTALL.de.md` ist entfernt.

## [0.4.4] — 2026-11-10

### Behoben
- **Frische Installation war nach dem Rename kaputt.** `install.sh` verwies an neun Stellen auf
  `$BIN/AscendedPanel`, `$SRC/AscendedPanel`, `/usr/local/bin/AscendedPanel` und den Unit-Glob
  `AscendedPanel-*.service` — beim Umbenennen war nur die Kleinschreibung im Paketordner angekommen.
  Folge: `cp: .../opt/AscendedPanel fehlt` bzw. `~/.config/AscendedPanel/settings.json` (Großbuchstabe)
  und damit Abbruch der Installation. Jetzt überall `ascendedpanel`, inklusive Config-Pfaden und
  Backup-/Snapshot-Ordnern.
- In einem leeren Home nachgestellt: `install.sh --check`, `--no-web --auto`, Launcher, Web-Start
  (HTTP 200), Instanz anlegen, 90 Einstellungsfelder — alles ohne Fehler.

## [0.4.3] — 2026-11-10

### Geändert
- **Knopf „Englische Website" aus der Kopfzeile entfernt.** Er öffnete nur die englische README auf
  GitHub; der englische Text ist über die README im Repo erreichbar, der Platz im Kopf gehört den
  Statusanzeigen.

## [0.4.2] — 2026-11-10

### Geändert
- **Kopfzeilen-Knopf heißt jetzt „Englische Website" / „English website"** statt nur „English" — er
  öffnet die englische README auf GitHub, das war ohne das Wort nicht erkennbar.

## [0.4.1] — 2026-11-10

### Behoben
- **Englische Oberfläche zeigte deutsche Feldnamen in den Einstellungen.** `i18n.setting()` war
  implementiert, wurde aber nie aufgerufen. Jetzt übersetzt `_uebersetzte_settings()` jedes Feld:
  kuratierte Tabelle `SET_EN` zuerst, sonst der lesbar gemachte Schlüsselname
  („EnablePvPStructureDecay" → „Enable PvP structure decay"). Deutsch bleibt unverändert.

## [0.4.0] — 2026-11-10

### Geändert
- **Das Projekt heißt jetzt AscendedPanel.** Reines ASA-Werkzeug, der Name sagt es: Befehl
  `ascendedpanel` (auch als `python3 -m ascendedpanel`), Dienst `ascendedpanel-web.service`,
  Konfiguration unter `~/.config/ascendedpanel`, Backups/Snapshots unter
  `~/ascendedpanel-backups` bzw. `~/ascendedpanel-snapshots`.
- **Bestehende Installationen werden automatisch übernommen:** liegt noch `~/.config/noah` herum und
  `~/.config/ascendedpanel` existiert nicht, wird das Verzeichnis beim ersten Start umbenannt
  (gleiche Partition) bzw. kopiert — Instanzen, Token und Einstellungen bleiben also erhalten.

## [0.3.76] — 2026-11-10

### Geändert
- **Knopf „Dinos speichern" entfernt.** Er sendete denselben Befehl wie „Welt speichern"
  (`SaveWorld`); ARK kennt keinen eigenen Dino-Save. Der Hinweis an „Welt speichern" nennt jetzt,
  dass alle gezähmten Dinos mitgespeichert werden.

## [0.3.75] — 2026-11-10

### Behoben
- **Nicht installierte Instanzen ließen sich nicht löschen.** Die Karte zeigte nur „Installieren";
  jetzt steht dort auch `Löschen`, ohne Rückfrage nach Serverdateien (es gibt keine, der leere
  Instanzordner wird mit entfernt).
- **`delInst()` prüfte `r.ok` auf einer Textantwort** — nach dem Löschen lud die Karte nie neu und
  eine Fehlermeldung blieb unsichtbar. Jetzt wird die JSON-Antwort gelesen und die freigegebenen
  GB/MB angezeigt.

## [0.3.74] — 2026-11-10

### Geändert
- **Der Mods-Reiter ist oben mit „Installierte Mods" überschrieben** (mit Anzahl). Die Liste war
  schon immer die installierte Liste, stand aber ohne Beschriftung über der Suche — jetzt ist auf
  einen Blick klar, was installiert ist und was die Suche darunter ist.

## [0.3.73] — 2026-11-10

### Geändert
- **Der Wizard steht nicht mehr im normalen Installationsablauf.** README und INSTALL nennen jetzt
  `noah web` als Weg (Instanz im Browser anlegen und installieren); der Konsolen-Assistent ist ein
  eigener, ausdrücklich optionaler Absatz („nur Konsole"). Die falsche Aussage „die Web-Oberfläche
  kann keine Instanz anlegen" ist raus.
- `install.sh` nennt in den Abschlusshinweisen zuerst `noah web`, der Wizard steht als optionale
  Zeile darunter (eigener Übersetzungsschlüssel).

## [0.3.72] — 2026-11-10

### Neu
- **Mod-Beschreibungen automatisch auf Deutsch.** In der deutschen Oberfläche werden Suchtreffer und
  Vorschläge der Mod-Suche übersetzt. Übersetzungen liegen unter `~/.config/noah/cache/translations`
  und werden wiederverwendet; scheitert die Übersetzung, bleibt der Originaltext stehen. Bereits
  deutsche Texte werden erkannt und nicht erneut übersetzt.

## [0.3.71] — 2026-11-10

### Geändert
- **Mod-Vorschläge beim Tippen**: sie kommen weiterhin ohne Enter (kurze Pause nach dem letzten
  Zeichen), aber ohne CurseForge-API-Key blieb die Liste stumm. Jetzt steht an der Stelle der
  Hinweis, dass Vorschläge einen Key brauchen — mit Link zu `console.curseforge.com` und zum
  Key-Feld im Reiter.
- **Veraltete Antworten werden verworfen.** Wer schnell weitertippt, konnte bisher eine ältere
  Antwort über die neuere bekommen; jetzt trägt jeder Aufruf eine Sequenznummer und nur die
  letzte Antwort wird angezeigt.

## [0.3.70] — 2026-11-09

### Geändert
- **Stop ist deutlich schneller und meldet die Dauer.** Bisher wurde nur die PID des Starters
  beobachtet: der verschwindet zuerst, während `ArkAscendedServer.exe` und `wineserver` noch liefen —
  deshalb wartete noah die volle Kulanzzeit ab (bis 90 s) und ließ Reste stehen. Jetzt werden alle
  Prozesse der Instanz über die Kommandozeile gefunden, das Warten endet, sobald wirklich keiner mehr
  läuft, und die Meldung nennt die gebrauchte Zeit („beendet nach 6 s"). Notausstieg bleibt:
  SIGTERM an die Gruppe, danach SIGKILL auf die Reste.

## [0.3.68] — 2026-11-08

### Geändert
- **Die Backup-Box ist ganz entfernt.** Welt-Sicherungen laufen ausschließlich als Aufgabe im Zeitplan
  (Aktion „Backup"); Snapshots bleiben in ihrer Box. Über die Oberfläche lassen sich damit auch keine
  Backups mehr einzeln zurückholen — die Dateien unter `~/noah-backups` und die API bleiben bestehen.

## [0.3.67] — 2026-11-08

### Geändert
- **„Backup-Uhrzeiten" ist entfallen** — Backups laufen ausschließlich als Aufgabe im Zeitplan
  (Aktion „Backup"), damit es nicht zwei Stellen mit derselben Wirkung gibt. Die Backup-Box zeigt jetzt
  den Hinweis darauf und behält „Jetzt sichern" für eine sofortige Welt-Sicherung.

## [0.3.66] — 2026-11-08

### Behoben
- **Geleerte Uhrzeiten-Felder wurden ignoriert:** ein leer gelassenes Feld (Neustart, Backup, Snapshot)
  kam beim Server gar nicht an, weil leere Query-Werte wegfielen — die alten Zeiten blieben stehen und
  ließen sich so nicht abschalten. Jetzt werden leere Werte mitgesendet und leeren die Liste.

## [0.3.65] — 2026-11-08

### Geändert
- **Snapshots haben eigene Uhrzeiten** („Snapshot-Uhrzeiten" in der Snapshot-Box, kommagetrennt wie bei
  den Backups) statt einer Aktion im Zeitplan. Der Zeitplan bleibt für die übrigen Aktionen.
- „Auto-Snapshots behalten" bleibt unverändert und greift weiter für die automatischen Sicherungen.

## [0.3.64] — 2026-11-08

### Geändert
- **„Auto-Snapshots behalten" steht jetzt unter dem Knopf** statt darüber, und der Hinweis nennt die
  Platzrechnung (3 = ein Tag bei 3 pro Tag, 15 ≈ 180 GB).

## [0.3.63] — 2026-11-08

### Neu
- **Snapshots lassen sich jetzt ebenfalls per Zeitplan anlegen** (Aktion „Snapshot"), z. B. sonntags
  04:00. Damit die 12-GB-Kopien nicht auflaufen, bleiben nur die letzten drei Auto-Snapshots; die Zahl
  steht als „Auto-Snapshots behalten" bei der Snapshot-Box.
- Manuelle Snapshots werden dabei nie angefasst — aufgeräumt werden nur die mit dem Namen `auto_*`,
  sortiert nach Änderungszeit.
- **Zwei Snapshots in derselben Sekunde** hätten sich überschrieben (`FileExistsError`); der Name bekommt
  jetzt einen Zähler.

## [0.3.62] — 2026-11-08

### Geändert
- **Der Zeitplan nimmt die volle Breite ein**, die Backup-Box steht jetzt darunter. Damit haben die
  Aufgabenzeilen Platz für Aktion, Uhrzeit, Tage, Argument und Schalter in einer Zeile.
- „Backup-Uhrzeiten" bleibt in der Backup-Box (Backups sind keine Snapshots).

## [0.3.61] — 2026-11-08

### Geändert
- **„Backup-Uhrzeiten" steht jetzt bei den Snapshots** statt in der Backup-Box — dort, wo die Sicherungen
  hingehören. Der Hinweis nennt zusätzlich die neue Zeitplan-Aufgabe „Backup" als Alternative.

## [0.3.60] — 2026-11-08

### Behoben
- **Der Supervisor las den Zeitplan nur beim Start.** In der Oberfläche gespeicherte Aufgaben wurden erst
  nach einem Supervisor-Neustart ausgeführt. Er liest die Zeitplan-Felder jetzt bei jeder Runde neu,
  sobald sich die Instanzdatei geändert hat (Ports und Mods bleiben bewusst unberührt).
- **Das Selbst-Update startete den Supervisor nicht mit** — er lief weiter mit altem Code. Jetzt werden
  `noah-web` und `noah-supervise` neu gestartet, sofern sie laufen.

## [0.3.59] — 2026-11-08

### Behoben
- **Zeitplan-Aufgaben konnten dieselbe ID bekommen**, wenn sie in derselben Millisekunde angelegt wurden
  (z. B. beim Senden der ganzen Liste). Die ID ist jetzt zusätzlich durchnummeriert — sonst hätte der
  Supervisor zwei Aufgaben als „schon gelaufen" verwechselt.

## [0.3.58] — 2026-11-08

### Neu
- **Zeitplan mit Aufgaben** (Verwaltung → Zeitplan), ähnlich den Scheduled Tasks in AMP: je Aufgabe
  **Aktion, Uhrzeit, Wochentage** (leer = täglich) und ein Freitextfeld für Broadcast oder RCON-Befehl.
  Aktionen: Neustart, Start, Stop, Update + Neustart, Backup, Welt speichern, wilde Dinos löschen,
  Broadcast, freier RCON-Befehl.
- Neustart-Aufgaben nutzen die Vorwarnung (Countdown im Spiel), die übrigen laufen sofort; jede
  Ausführung geht an den Discord-Webhook, Fehler als Fehlermeldung.
- Die alten „Neustart-Uhrzeiten" bleiben als Rückfallebene erhalten.

## [0.3.57] — 2026-11-08

### Geändert
- **Der Hinweis nennt jetzt den Grund:** „Die CurseForge-API liefert höchstens 50 Treffer pro Abfrage —
  mehr lässt sich technisch nicht abrufen." An der Trefferzeile entsprechend
  „CurseForge-API: maximal 50 pro Abfrage".

## [0.3.56] — 2026-11-08

### Neu
- **Hinweis zur Trefferbegrenzung** unter dem Suchfeld: maximal 50 Treffer pro Suche, für mehr den
  Begriff eingrenzen. Steht zusätzlich an der Trefferzeile, sobald die Liste abgeschnitten ist
  („50 / 7.291 Treffer · mehr pro Suche nicht möglich").

## [0.3.55] — 2026-11-08

### Geändert
- **Mod-Suche holt 50 Treffer** statt 30 (mehr erlaubt die CurseForge-Suche pro Abfrage nicht).
  Für gezieltes Suchen reicht das; sonst den Begriff eingrenzen.

## [0.3.54] — 2026-11-08

### Geändert
- **Trefferzahl steht jetzt deutlich über der Mod-Liste** (12,5 px, Akzentfarbe statt 11 px gedämpft):
  „30 / 7.290 Treffer". Auch die Vorschlagsliste beim Tippen nennt ihre Anzahl.

## [0.3.53] — 2026-11-08

### Behoben
- **Zwischengespeicherte Suchergebnisse konnten die API-Suche verdecken.** Ein Ergebnis vom Notbehelf
  (wenige Treffer, ohne Key) wurde eine Stunde lang auch dann ausgeliefert, wenn inzwischen ein Key
  gesetzt war — die Suche zeigte weiter 8 statt 30 Treffer. Der Cache unterscheidet jetzt Key/ohne Key
  und die Trefferzahl; die Gesamtzahl wird mitgespeichert. Alte Cache-Dateien werden ignoriert.

## [0.3.52] — 2026-11-08

### Geändert
- **Mod-Suche zeigt bis zu 30 Treffer** statt 10, mit Trefferzahl darüber („30 / 1.412 Treffer",
  Gesamtzahl aus der CurseForge-Antwort). Die Liste ist scrollbar, statt die Seite zu verlängern.

## [0.3.51] — 2026-11-08

### Geändert
- **`console.curseforge.com` im Feld „CurseForge-API-Key" ist jetzt ein Link** (öffnet in neuem Tab),
  statt nur als Text dazustehen.

## [0.3.50] — 2026-11-08

### Geändert
- **Discord- und PayPal-Symbol größer und in den Markenfarben** (34 px Feld, 22 px Symbol; Discord
  #5865F2, PayPal #003087) statt einfarbig klein.

## [0.3.49] — 2026-11-08

### Neu
- **Discord und PayPal als Symbole oben rechts** — auf jeder Seite (Dashboard, Instanzseite, Mods,
  Verwaltung). Die Symbole sind eingebettet, es geht keine Anfrage an fremde Server, solange niemand
  klickt.

## [0.3.48] — 2026-11-08

### Neu
- **Reiter im Einstellungs-Formular:** die 90 bekannten INI-Werte sind in neun Gruppen sortiert —
  Server & Zugang, Spiel & Tempo, PvP & Regeln, Strukturen & Verfall, Dinos & Zucht, Transfer & Cluster,
  Anzeige, MOTD und Game.ini. Jeder Reiter nennt seine Anzahl; die Auswahl merkt sich der Browser.
- Gespeichert wird weiterhin alles auf einmal — die Felder der anderen Reiter bleiben erhalten.

## [0.3.47] — 2026-11-08

### Geändert
- **Der Knopf heißt „Menü" und führt direkt in die Instanz** — Beschriftung wie gewünscht, ohne
  Zwischenschritt oder Aufklappliste.

## [0.3.46] — 2026-11-08

### Geändert
- **Zurück zum direkten Weg:** „Öffnen" führt wieder ohne Zwischenschritt in die Instanz; Menü-Knopf und
  Dialog sind entfernt.

## [0.3.45] — 2026-11-08

### Geändert
- **Kein Dropdown mehr in der Karte:** ein einfacher Knopf **„Menü"** öffnet eine Auswahl mit Übersicht,
  Einstellungen, Mods und Verwaltung.

## [0.3.44] — 2026-11-08

### Geändert
- **Das Auswahlfeld in der Karte heißt „Menü …"** statt „Öffnen …" — es ist ja eine Auswahl, kein Knopf.

## [0.3.43] — 2026-11-08

### Geändert
- **Startseite neu geordnet:** „Neue Instanz" und „Hinweis" stehen jetzt oben, darunter die Instanzen —
  die Erzeugung bleibt damit immer an derselben Stelle und wandert nicht, wenn Instanzen dazukommen.
- **„Öffnen" ist ein Menü:** Übersicht, Einstellungen, Mods oder Verwaltung direkt anwählen; die
  Detailseite springt in den passenden Reiter.
- Karten- und Log-Größen wieder wie in 0.3.39 (Log nur bei laufenden Instanzen, 9,5 px, Karten ab 300 px).

## [0.3.39] — 2026-11-08

### Geändert
- **Laufende Instanzen nehmen im Dashboard zwei Spalten ein** (ab 900 px Fensterbreite). Sonst war die
  Karte so schmal, dass das Log unter die Kennzahlen rutschte statt daneben zu stehen.

## [0.3.38] — 2026-11-08

### Neu
- **Lebendes Server-Log in der Dashboard-Karte.** Rechts neben Status und Kennzahlen laufen die
  letzten Logzeilen mit (Aktualisierung alle 2,5 s), damit man ohne die Detailseite sieht, was der
  Server gerade tut. Bei schmalen Karten rutscht das Log unter die Kennzahlen.
- Die angezeigte Zeilenzahl folgt der Kartenhöhe; leere Ausgabe erscheint als „keine Ausgabe".

## [0.3.37] — 2026-11-08

### Geändert
- **CPU-Kachel zeigt jetzt den Anteil des Servers (0–100 %)** statt der Summe über alle Kerne.
  755 % auf 64 Kernen erscheint damit als „11,8 %"; der Verlaufsgraph endet ebenfalls bei 100 %.
  Die Kern-Aufschlüsselung („7,6 von 64 Kernen") steht im Tooltip, der Rohwert bleibt in der API
  unter `cpu` erhalten.

## [0.3.36] — 2026-11-08

### Behoben
- **CPU-Tooltip zeigte `undefined`/`NaN`**, wenn die Gegenstelle keine Kernzahl liefert (ältere
  Antwort im Browser-Cache). Ersatzwert ist jetzt die Kernzahl des Browsers, sonst 1.

## [0.3.35] — 2026-11-08

### Behoben
- **Selbst-Update startete den Benutzerdienst nicht neu.** Ohne angemeldete Sitzung (per `su`, `ssh`
  oder aus einem Skript) fehlten `XDG_RUNTIME_DIR` und `DBUS_SESSION_BUS_ADDRESS`, `systemctl --user`
  scheiterte und die Oberfläche lief weiter mit dem alten Code. Beide Variablen werden jetzt gesetzt,
  der Dienststart klappt damit auch aus einer Nicht-Login-Sitzung.

## [0.3.34] — 2026-11-08

### Behoben
- **Selbst-Update konnte die Installation zerstören.** `apply()` löschte das laufende Paketverzeichnis
  und kopierte erst danach das neue hinein — brach der Kopiervorgang ab (oder existierte das Ziel noch),
  blieb ein halbes Verzeichnis zurück und `noah` war nicht mehr startbar. Das neue Paket wird jetzt
  vollständig daneben aufgebaut und per `rename` getauscht; schlägt der Tausch fehl, wird der alte
  Stand zurückgerollt.
- **Sicherungen sammelten sich unbegrenzt.** Bei jedem Update entstand ein `noah.bak-<Zeitstempel>`.
  Es bleiben jetzt die letzten zwei.

## [0.3.33] — 2026-11-08

### Behoben
- **CPU-Graph schnitt alles über 100 % ab.** Die Sparkline im Dashboard war fest auf 100 % skaliert,
  ein ARK-Server mit 700 % Last erschien als flache Linie am oberen Rand. Sie skaliert jetzt auf den
  tatsächlichen Höchstwert (mindestens 100 %).
- **CPU-Zahl war erklärungsbedürftig.** Der Wert ist der Summenwert über alle Threads (wie `top`/`htop`),
  kann also deutlich über 100 % liegen. Die Kachel nennt im Tooltip jetzt Kerne und Anteil am Server,
  z. B. „7,5 von 64 Kernen ausgelastet (11,8 % des Servers)".

## [0.3.32] — 2026-11-08

### Behoben
- **`--user` ließ die Dateien root gehören**, wenn kein Web-Dienst eingerichtet wurde (`--no-web`) — der
  Benutzer konnte danach seine eigenen Configs nicht schreiben. Die Rechte werden jetzt direkt nach dem
  Kopieren gesetzt.

## [0.3.31] — 2026-11-08

### Behoben
- **`--user NAME` wurde nicht erkannt** („Unbekannte Option"): die Argumentschleife konnte mit `shift` kein
  zweites Wort lesen. Sie läuft jetzt als `while`-Schleife, damit funktionieren `--user noah` und
  `--user=noah` (ebenso `--lang de`).

## [0.3.30] — 2026-11-08

### Behoben
- **Selbst-Update konnte stillschweigend denselben Stand einspielen.** Das Archiv wurde über den Branch
  `main` geladen; codeload liefert dafür minutenlang eine zwischengespeicherte Fassung. Jetzt wird das
  Archiv **zum geprüften Commit** geladen (`/tar.gz/<sha>`) — was die Prüfung meldet, wird auch installiert.

## [0.3.29] — 2026-11-08

### Neu
- **`sudo ./install.sh --user noah`** — Installation unter einem eigenen Dienst-Benutzer. Der Installer legt
  den Benutzer samt Home an, kopiert nach `/home/noah/…`, setzt die Rechte, richtet die Oberfläche als
  **User-Dienst** ein und aktiviert `loginctl enable-linger`, damit sie ohne Login startet. Damit läuft
  kein Teil mehr als root (empfohlen für Server).

## [0.3.28] — 2026-11-08

### Behoben
- **Spielserver starb beim Neustart der Oberfläche, wenn noah als normaler Benutzer läuft.** Die eigene
  systemd-Scope wurde nur auf dem System-Bus versucht, was ohne root scheitert — der Start fiel still auf
  einen normalen Kindprozess zurück. Jetzt läuft sie als `systemd-run --user --scope` über den
  Benutzer-Manager (dafür einmalig `loginctl enable-linger <benutzer>`), damit der Server einen
  Web-Neustart überlebt.

## [0.3.27] — 2026-11-08

### Neu
- **Portprüfung vor dem Start.** Belegt ein fremdes Programm (z. B. ein AMP-Server) den Spiel-, Query-
  oder RCON-Port, bricht noah mit einer klaren Meldung ab, statt einen Server zu starten, der nicht
  erreichbar ist — und statt RCON-Anfragen versehentlich an den falschen Server zu schicken.

## [0.3.26] — 2026-11-08

### Behoben
- **Startzeile nach AMP-Vorbild.** Port, Query-Port, RCON und Passwort stehen jetzt ausschließlich in der
  Map-URL (`?listen?Port=…?QueryPort=…?RCONEnabled=True?RCONServerGameLogBuffer=600?RCONPort=…?ServerAdminPassword=…`),
  das Passwort als **letzte** Option — ASA liest sonst den Rest der Zeile mit hinein. Die getrennten
  `-port`/`-RCONPort`-Argumente sind entfallen.
- `-SessionName` wird nicht mehr als Argument übergeben (Leerzeichen im Namen zerlegten die Zeile);
  der Name kommt aus `[SessionSettings]` der INI.

## [0.3.25] — 2026-11-08

### Behoben
- **RCON blieb trotz `RCONEnabled=True` bei „Passwort falsch".** ASA übernimmt das Admin-Passwort nur aus
  der Kommandozeile; jetzt steht `?ServerAdminPassword=…` in der Map-URL (genau wie bei AMP). Hinweis:
  damit ist das Passwort wie bei jedem ARK-Server in `ps` sichtbar.

## [0.3.24] — 2026-11-08

### Behoben
- **RCON antwortete auf frisch angelegten Instanzen mit „Passwort falsch".** noah übergab nur
  `-RCONPort` und verließ sich beim Aktivieren auf die INI; ASA wertet das aber erst mit
  `?RCONEnabled=True` in der Map-URL aus (so macht es auch AMP). Die URL enthält jetzt
  `?listen?Port=…?RCONEnabled=True?RCONServerGameLogBuffer=600?RCONPort=…`. Das Passwort bleibt in der
  INI — es taucht damit nicht in der Prozessliste auf.

## [0.3.23] — 2026-11-08

### Geändert
- Beispiel für das Cluster-Verzeichnis im Hinweis: `/home/Noah/arkcluster` statt `/home/benutzer/arkcluster`.

## [0.3.22] — 2026-11-08

### Geändert
- **Cluster-Felder zeigen ihre Vorgabewerte direkt im Feld** — Cluster-ID ist der Instanzname, Verzeichnis
  ist `<instanz>/clusters`. Man sieht also den Pfad, muss ihn nur überschreiben, wenn geteilt werden soll.
  Der Hinweis nennt zusätzlich ein Beispiel (`/home/benutzer/arkcluster`).

## [0.3.21] — 2026-11-08

### Neu
- **Cluster-Einstellungen.** Bisher steckten `-clusterid=noah` und ein Verzeichnis pro Instanz fest im Code —
  Karten konnten also nie etwas teilen. Jetzt gibt es im Reiter Einstellungen eine eigene Karte **Cluster**:
  Cluster-ID, gemeinsames Verzeichnis und die Option „Übertragungen ohne Filterprüfung"
  (`-NoTransferFromFiltering`). Ohne eigene Angabe bleibt es beim alten Verhalten.
- **53 weitere INI-Einstellungen** aus dem vollen ARK-Satz, u. a. Transfer-Sperren (Download/Upload von
  Spielern, Items, Dinos), Offline-Raid-Schutz, Tribe-Allianzen, Struktur-Verfall und -Aufheben,
  Dino-Verfall, gezähmte Dinos pro Spieler, Prägung, Treffer-Markierungen sowie Futter-/Torpor- und
  Ernteschaden-Multiplikatoren. Das Formular ist jetzt nach Datei **und** Abschnitt gruppiert.

## [0.3.20] — 2026-11-08

### Behoben
- **„leer" in der Whitelist-Liste** war noch fest deutsch; läuft jetzt über `i18n.py` (`empty`).

## [0.3.19] — 2026-11-08

### Behoben
- **Zwei weitere deutsche Texte in der englischen Oberfläche:** „kein Snapshot vorhanden" und die
  Meldung beim Speichern der Sprache kamen fest verdrahtet aus dem Code. Beide laufen jetzt über `i18n.py`.

## [0.3.18] — 2026-11-08

### Behoben
- **Mod-Status war fest auf Deutsch** („nicht heruntergeladen", „für alte Engine gebacken") und blieb
  auch in der englischen Oberfläche deutsch. Jetzt kommen Codes aus `mods.py` und die Übersetzung aus
  `i18n.py` — `not downloaded` / `built for an older engine`.

## [0.3.17] — 2026-11-08

### Neu
- **Englische Beschreibung:** eigener Knopf im Kopfbereich (neben „Changelog") öffnet
  `README.en.md` auf GitHub. Das README verlinkt jetzt oben zwischen Deutsch und English.

## [0.3.16] — 2026-11-08

### Behoben (wichtig)
- **Die Oberfläche war tot, sobald die Seite geladen war:** im Update-Fortschritt (0.3.13) stand ein
  Zeilenumbruch als echtes Zeichen im JavaScript, das war ein Syntaxfehler — damit war das ganze Skript
  ungültig. Folge: Reiter ließen sich nicht wechseln, Mod-Knöpfe, Einstellungen und alles andere
  reagierten nicht. Ersetzt durch `String.fromCharCode(10)`, JavaScript wird jetzt vor dem Push mit
  `node --check` geprüft.

## [0.3.15] — 2026-11-08

### Behoben
- **Der Spielserver hängt nicht mehr am Web-Dienst.** Bisher startete er als Kindprozess von
  `noah-web`; Wine-Prozesse blieben beim Stoppen in dessen Prozessgruppe zurück („Unit process …
  remains running after unit stopped") und blockierten jeden Neustart der Oberfläche. Jetzt läuft jede
  Instanz in einer eigenen transienten Unit (`noah-<name>.scope`, via `systemd-run --scope`), damit
  überlebt der Server einen Neustart der Oberfläche und umgekehrt. Ohne systemd fällt noah auf den
  bisherigen Start zurück (`NOAH_NO_SCOPE=1` erzwingt das).

## [0.3.14] — 2026-11-08

### Geändert
- **RAM-Hinweis im Dashboard war irreführend** („ca. 11,5 GB pro laufendem Server"). Der Wert hängt an
  Mods, Weltgröße und Spielerzahl: leer und ohne Mods sind es rund 4 GB, mit Mods und Welt 11–12 GB,
  nach oben offen. Text in Oberfläche und `INSTALL.md` entsprechend korrigiert.

## [0.3.13] — 2026-11-08

### Neu
- **Update-Fortschritt ist sichtbar.** Bisher ging die SteamCMD-Ausgabe an das Dienst-Protokoll, im
  Server-Log stand während des Updates nichts. Jetzt schreibt noah sie nach `.update.log` und die
  Oberfläche zeigt sie im Ausgabefeld, während das Update läuft (`/api/update/progress`, Abfrage alle 2 s).

## [0.3.12] — 2026-11-08

### Behoben
- **Der Changelog-Knopf zeigte den Stand der Erstinstallation.** Das Selbst-Update ersetzt nur das
  Paketverzeichnis, die `CHANGELOG*.md` daneben blieben liegen. Jetzt zieht das Update beide Dateien mit,
  und die Oberfläche holt den Text frisch, wenn die eigene Version darin fehlt.

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
