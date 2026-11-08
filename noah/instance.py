"""Instanz-Konfiguration und Pfade."""
from __future__ import annotations

import configparser
import json
import os
from dataclasses import dataclass, asdict, field

SERVER_APP_ID = "2430930"
EXE_REL = os.path.join("ShooterGame", "Binaries", "Win64", "ArkAscendedServer.exe")
CONFIG_REL = os.path.join("ShooterGame", "Saved", "Config", "WindowsServer")
LOG_REL = os.path.join("ShooterGame", "Saved", "Logs", "ShooterGame.log")


@dataclass
class Instance:
    name: str
    directory: str
    map: str = "Ragnarok_WP"
    session_name: str = "ARK Test"
    port: int = 7790
    query_port: int = 27016
    rcon_port: int = 27025
    rcon_password: str = ""
    mods: list[int] = field(default_factory=list)
    wine_bin: str = "wine"
    wine_prefix: str = ""
    extra_args: str = ""
    max_players: int = 20
    admin_password: str = ""
    restart_times: list[str] = field(default_factory=list)
    backup_times: list[str] = field(default_factory=list)
    warn_minutes: int = 5
    backups_keep: int = 10
    exclusive_join: bool = False
    banned: list[str] = field(default_factory=list)
    hang_seconds: int = 300
    max_restarts_per_hour: int = 4
    webhook_url: str = ""
    headless: bool = True

    # ------------------------------------------------------------------ Pfade
    @property
    def exe(self) -> str:
        return os.path.join(self.directory, EXE_REL)

    @property
    def config_dir(self) -> str:
        return os.path.join(self.directory, CONFIG_REL)

    @property
    def gus_ini(self) -> str:
        return os.path.join(self.config_dir, "GameUserSettings.ini")

    @property
    def game_ini(self) -> str:
        return os.path.join(self.config_dir, "Game.ini")

    @property
    def log_path(self) -> str:
        return os.path.join(self.directory, LOG_REL)

    @property
    def pid_file(self) -> str:
        return os.path.join(self.directory, ".noah.pid")

    @property
    def console_log(self) -> str:
        return os.path.join(self.directory, ".noah-console.log")

    @property
    def mods_dir(self) -> str:
        return os.path.join(self.directory, "ShooterGame", "Binaries", "Win64", "ShooterGame", "Mods")

    # ------------------------------------------------------------------ Ini
    def write_ini(self) -> None:
        """Schreibt Ports/RCON/Mods in die GameUserSettings.ini (idempotent)."""
        os.makedirs(self.config_dir, exist_ok=True)
        cp = configparser.ConfigParser(strict=False)
        cp.optionxform = str
        metadata = ""
        if os.path.exists(self.gus_ini):
            with open(self.gus_ini, encoding="utf-8-sig") as fh:
                first = fh.readline().rstrip("\r\n")
            if first.startswith(";METADATA"):
                metadata = first
            cp.read(self.gus_ini, encoding="utf-8-sig")

        for section in ("ServerSettings", "SessionSettings", "MessageOfTheDay"):
            if not cp.has_section(section):
                cp.add_section(section)

        values = {
            "ServerSettings": {
                "RCONEnabled": "True",
                "RCONPort": str(self.rcon_port),
                "ServerAdminPassword": self.admin_password or self.rcon_password,
                "ServerPassword": "",
                "MaxPlayers": str(self.max_players),
                "ServerPVE": "True",
                "DifficultyOffset": "1.0",
                "ServerCrosshair": "True",
                "ShowMapPlayerLocation": "True",
            },
            "SessionSettings": {
                "SessionName": self.session_name,
                "Port": str(self.port),
                "QueryPort": str(self.query_port),
            },
        }
        for section, kv in values.items():
            for key, val in kv.items():
                cp.set(section, key, val)
        with open(self.gus_ini, "w", encoding="utf-8") as fh:
            if metadata:
                fh.write(metadata + "\n")
            cp.write(fh, space_around_delimiters=False)

        # Mods in Game.ini -> ActiveMods
        cp2 = configparser.ConfigParser(strict=False)
        cp2.optionxform = str
        if os.path.exists(self.game_ini):
            cp2.read(self.game_ini, encoding="utf-8-sig")
        if not cp2.has_section("/script/shootergame.shootergamemode"):
            cp2.add_section("/script/shootergame.shootergamemode")
        cp2.set(
            "/script/shootergame.shootergamemode",
            "ActiveMods",
            ",".join(str(m) for m in self.mods),
        )
        with open(self.game_ini, "w", encoding="utf-8") as fh:
            cp2.write(fh, space_around_delimiters=False)

    # ------------------------------------------------------------------ JSON
    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(asdict(self), fh, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: str) -> "Instance":
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})

    # ------------------------------------------------------------------ Start
    def launch_argv(self) -> list[str]:
        argv = [
            self.exe,
            self.map,
            "-server",
            "-log",
            "-NoBattlEye",
            "-servergamelog",
            "-servergamelogincludetribelogs",
            "-NoTransferFromFiltering",
            "-ClusterDirOverride=" + os.path.join(self.directory, "clusters"),
            "-clusterid=noah",
            "-port=%d" % self.port,
            "-QueryPort=%d" % self.query_port,
            "-RCONPort=%d" % self.rcon_port,
            "-ServerPlatform=All",
            "-MaxPlayers=%d" % self.max_players,
            "-SessionName=%s" % self.session_name,
        ]
        if self.exclusive_join:
            argv.append("-exclusivejoin")
        if self.mods:
            argv.append("-mods=%s" % ",".join(str(m) for m in self.mods))
        if self.extra_args:
            argv.extend(self.extra_args.split())
        return argv
