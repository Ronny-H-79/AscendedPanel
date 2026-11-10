# Betrieb

ascendedpanel aktuell halten, Sprache umstellen.

[← zurück zum README](../README.de.md) · [English](betrieb.md)

## ascendedpanel aktuell halten

Was sich zwischen den Versionen geändert hat, steht in [CHANGELOG.md](../CHANGELOG.md) — und beim
Update-Klick zeigt der Dialog die Änderungen der neuen Version direkt an.


Oben rechts steht die Version (`v0.2.3`). Liegt auf GitHub eine neuere, wird der Knopf farbig und
zeigt beide Stände: **`v0.2.2 → 0.2.3`**. Ein Klick lädt das neue Paket, ersetzt nur das
Programmverzeichnis und startet den Web-Dienst neu — Instanzen, Backups und Einstellungen bleiben
unberührt. Der vorherige Stand bleibt als `AscendedPanel.bak-<zeitstempel>` daneben liegen.

Auf der Konsole:

```bash
ascendedpanel version        # installiert + verfügbar
ascendedpanel self-update    # einspielen (Dienst wird neu gestartet)
```

Geprüft wird über die GitHub-API (Version aus `AscendedPanel/__init__.py`). Kein git nötig, auch eine
Installation aus einem Archiv lässt sich so aktualisieren.

**Ältere Installationen** (vor 0.2.1) kennen `self-update` noch nicht — dort einmalig von Hand:

```bash
cd ~/ascendedpanel && git pull && ./install.sh
```

Danach steht `ascendedpanel self-update` zur Verfügung.

## Sprache

| | |
|---|---|
| **Beim Installieren** | `./install.sh` fragt „Sprache / Language" — oder direkt `./install.sh --lang en` |
| **Später wechseln** | `ascendedpanel lang en` / `ascendedpanel lang de` (schreibt `~/.config/ascendedpanel/settings.json`) |
| **In der Weboberfläche** | Knopf `EN` / `DE` oben rechts, Seite lädt neu |

Alle Beschriftungen, Formularfelder, Befehlsschaltflächen, Rückfragen und Meldungen liegen in
`AscendedPanel/i18n.py` (Deutsch und Englisch). Neue Texte brauchen nur einen weiteren Eintrag im Katalog.

![Dashboard englisch](screenshot-dashboard-de.png)

