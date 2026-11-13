"""Pfade und einmalige Uebernahme der alten ``noah``-Konfiguration.

Beim Umbenennen auf AscendedPanel bleiben die Daten, wo sie sind: liegt noch
``~/.config/noah`` herum und ``~/.config/ascendedpanel`` existiert nicht, wird das
alte Verzeichnis beim ersten Start umbenannt (gleiche Partition) bzw. kopiert.
"""
from __future__ import annotations

import os
import shutil

ALT = os.path.expanduser("~/.config/noah")
CONF_DIR = os.path.expanduser(os.environ.get("ASCENDEDPANEL_CONFIG", "~/.config/ascendedpanel"))
TOKEN_PATH = os.path.join(CONF_DIR, "token")
# Fertige Adresse inklusive Token - praktisch, wenn die Konsole laengst gescrollt ist.
URL_PATH = os.path.join(CONF_DIR, "url")
SETTINGS_PATH = os.path.join(CONF_DIR, "settings.json")
CACHE_DIR = os.path.join(CONF_DIR, "cache")


def migriere_config() -> str:
    """Alte Konfiguration uebernehmen, falls noch nicht geschehen. Gibt CONF_DIR zurueck."""
    if os.path.isdir(CONF_DIR) or not os.path.isdir(ALT):
        return CONF_DIR
    try:
        os.makedirs(os.path.dirname(CONF_DIR), exist_ok=True)
        shutil.move(ALT, CONF_DIR)          # gleiche Partition: reines Umbenennen
    except OSError:
        try:
            shutil.copytree(ALT, CONF_DIR, dirs_exist_ok=True)
        except OSError:
            pass
    return CONF_DIR


migriere_config()
