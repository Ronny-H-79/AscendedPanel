# Security Policy / Sicherheitsrichtlinie

## Supported versions / Unterstützte Versionen

Fixes landen auf `main` und im jeweils neuesten Release. Ältere Stände werden nicht separat gepflegt.
Security fixes go to `main` and the latest release only; older versions are not maintained separately.

## Reporting a vulnerability / Sicherheitslücke melden

Bitte nicht als öffentliches Issue. / Please do not open a public issue.

1. Bevorzugt / preferred: GitHub → Reiter *Security* → *Report a vulnerability* (private Meldung).
2. Alternativ / alternatively: E-Mail an `ronny79privat@gmx.de`, Betreff `[AscendedPanel] Security`.

Hilfreich sind / helpful details:

- Version oder Commit-Hash
- Betriebssystem und Installationsart (`install.sh`, manuell, Container)
- Schritte zum Nachstellen (PoC) und die beobachtete Auswirkung
- Ob Root-Rechte oder ein bereits gültiger Token vorausgesetzt werden

Rückmeldung bemühe ich mich innerhalb von 72 Stunden; bestätigte Fixes erscheinen im `CHANGELOG.md`.
I aim to respond within 72 hours; confirmed fixes are listed in `CHANGELOG.md`.

## In scope / Im Rahmen

- Code in `ascendedpanel/` (Web-UI, Auth/Token-Handling, Datei- und Instanzverwaltung, RCON/SFTP, Update-Mechanik)
- `install.sh` und mitgelieferte systemd-Units
- Rechte-Eskalation, Pfad-Traversal, Command-Injection, unsichere Defaults

## Out of scope / Außerhalb

- Fehlkonfiguration des Betreibers, insbesondere eine ohne HTTPS oder SSH-Tunnel öffentlich erreichbare Oberfläche
  (siehe `docs/zugriff.md`)
- Angriffe, die bereits Root-Rechte auf dem Host voraussetzen
- Schwachstellen in ARK/Steam-Servern, SteamCMD oder Mods selbst
- Reine Denial-of-Service-Tests gegen fremde Instanzen
