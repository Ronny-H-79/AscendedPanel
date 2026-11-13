# Installing AscendedPanel

An installer for your own ARK ASA server manager. Everything runs locally: Python standard library plus
SteamCMD and Wine.

[← back to the README](README.md) · [Deutsch](INSTALL.de.md)

## Requirements

| What | Why | Check |
|---|---|---|
| Linux (x86_64) | tested on CachyOS/Arch | `uname -m` |
| Python ≥ 3.10 | the program runs on it | `python3 -V` |
| Wine ≥ 8 | runs the Windows server files | `wine --version` |
| ~30 GB disk per instance | 12.4 GB download + backups | `df -h ~` |
| ~10 GB RAM without mods, more with mods and players (no upper limit) | ARK needs it | `free -g` |

Missing Wine:

```bash
sudo pacman -S wine           # Arch / CachyOS
sudo apt install wine         # Debian / Ubuntu
```

SteamCMD is downloaded automatically to `~/steamcmd` on first install — no root needed.

## Language

The installer asks first:

```
Sprache / Language:  [1] Deutsch  [2] English   [1]
```

Non-interactive: `./install.sh --lang en` or `NOAH_LANG=en ./install.sh`.
It is stored in `~/.config/ascendedpanel/settings.json`. Changeable later at any time:

- `ascendedpanel lang en` / `ascendedpanel lang de`
- web UI: button in the top right (`EN` / `DE`)

## Installation

On a **server**, use a dedicated service user so nothing runs as root:

```bash
sudo ./install.sh --user ascendedpanel      # creates the user, installs to /home/AscendedPanel, user service + linger
```

Normal install (inside your own account):

```bash
git clone https://github.com/Ronny-H-79/AscendedPanel.git ascendedpanel   # or copy the folder
cd ascendedpanel          # this folder contains install.sh - NOT AscendedPanel/ascendedpanel (that is the Python package)
./install.sh --check        # only check what is missing (changes nothing)
./install.sh                # install, asks before adding missing packages
./install.sh --auto         # install missing packages without asking (sudo)
./install.sh --wizard       # install and start the wizard afterwards
```

The installer detects missing packages (e.g. Wine) via `pacman`, `apt`, `dnf` or `zypper` and installs them
with `sudo` on request. `--auto` forces that without asking.

It checks Python and Wine, copies the program files, creates the `ascendedpanel` command and sets up
`~/.config/ascendedpanel`. It needs **no** root rights.

## Web service (optional)

The installer asks: "start the web UI automatically (systemd service)?" Answering yes creates a **system
service** `/etc/systemd/system/ascendedpanel-web.service` as root (`WantedBy=multi-user.target`, starts at boot) —
or as a normal user `~/.config/systemd/user/ascendedpanel-web.service` (`systemctl --user enable --now`).
Without it, start the UI when you need it: `ascendedpanel web`.

## Access from elsewhere

By default `127.0.0.1` only. From another machine via SSH tunnel:
`ssh -N -L 8790:127.0.0.1:8790 user@server`, then open `http://127.0.0.1:8790/?token=…`.
In a LAN/VPN: `ascendedpanel web --host 0.0.0.0`. From the internet via nginx with HTTPS:
`sudo ascendedpanel proxy --domain AscendedPanel.example.de --write --cert` (writes the config, tests with `nginx -t`,
reloads nginx and fetches the certificate). Without nginx, HTTPS also works directly:
`ascendedpanel web --tls-cert cert.pem --tls-key key.pem`. Details in the README.

## Security (short)

The UI is an admin console: **whoever has the token controls everything** — start, stop and delete servers,
add mods, send console commands. Therefore:

- Client install (mode `[1]`) and server with a domain (mode `[2]`): ascendedpanel stays on `127.0.0.1`, access goes
  through the SSH tunnel or nginx with HTTPS. Only mode `[3]` binds directly to the outside.
- **Never expose it unencrypted to the internet.** With `--host 0.0.0.0` and no TLS the token travels in
  clear text through every hop. For public access use HTTPS via `ascendedpanel proxy` or TLS directly.
- The installer warns about mode `[3]` (IP and port) and asks before continuing.

In detail, including what ascendedpanel protects itself: `docs/zugriff.md`, section "Security".

## The token

After installation `ascendedpanel url` shows the address with token, e.g.
`http://127.0.0.1:8790/?token=…`. The key lives in `~/.config/ascendedpanel/token` (mode 0600) and protects the UI
against any website in your browser sending commands to `127.0.0.1` (without token: `HTTP 401`). Details in
the README, section "The token". Reset: delete the file, a new one is created on the next start.

## Set up

**Normal way — in the browser:**

```bash
ascendedpanel web
```

Open the printed address with token, enter an instance name, pick the map, press **Anlegen / Create**,
then **Install** on the new card. That downloads the server files (~12.4 GB) and registers the service.

**Optional, console only — the wizard:**

```bash
ascendedpanel wizard
```

This runs in the **terminal on the server** — over SSH (`ssh user@server`) or on the console itself.
The wizard asks questions, so it needs an interactive session. It is not required: the same steps are
in the web interface (name, map, **Anlegen**, **Installieren**).

The wizard asks for name, map, port and session name, creates the instance and offers to download the
server files (~12.4 GB, 10–30 minutes) and to set up a systemd service.

Without prompts, e.g. for scripts:

```bash
ascendedpanel init --name test --dir ~/arkserver-test --map Ragnarok_WP --port 7790 --rcon-port 27025
ascendedpanel update      # download the server files, then ascendedpanel start
```

## Using it

```bash
ascendedpanel web                    # start the web UI
ascendedpanel url                    # show the ready-made address including token
ascendedpanel status                 # process, RCON, last log line
ascendedpanel start --wait 240
ascendedpanel stop                   # SaveWorld → DoExit → SIGTERM
ascendedpanel update --check         # is a Steam build available?
ascendedpanel supervise --all        # auto-restart, scheduled restarts, backups
```

The UI shows a dashboard with all instances (status, CPU, RAM, players), per instance start/stop/update,
one-click RCON commands, player management, whitelist/bans, mod management with images, settings as a form,
backups, snapshots and a schedule.

## Autostart

```bash
systemctl --user daemon-reload
systemctl --user enable --now ascendedpanel-<name>
loginctl enable-linger $USER      # keeps running without a logged-in session
```

## Uninstall

```bash
cd ~/ascendedpanel      # your clone of the repo
./install.sh --uninstall
```

Removes the program and launcher. **Kept:** instances (`~/arkserver-*`), settings (`~/.config/ascendedpanel`),
backups (`~/ascendedpanel-backups`), snapshots (`~/ascendedpanel-snapshots`).

**SteamCMD** (`~/steamcmd`, `~/.steam`, `~/Steam`) is removed by `--uninstall` as well.

### Remove everything (instances and worlds too)

```bash
cd ~/ascendedpanel      # your clone of the repo
./install.sh --uninstall
rm -rf ~/arkserver-* ~/.config/ascendedpanel ~/ascendedpanel-backups ~/ascendedpanel-snapshots
rm -f /etc/systemd/system/ascendedpanel-*.service
systemctl daemon-reload
```

Where things live: program `~/.local/share/ascendedpanel` and `~/.local/bin/ascendedpanel`, settings and
token `~/.config/ascendedpanel`, instances with worlds `~/arkserver-<name>`, SteamCMD `~/steamcmd`,
`~/.steam` and `~/Steam`.

## Where things are

| Path | Content |
|---|---|
| `~/.local/share/ascendedpanel` | program |
| `~/.local/bin/ascendedpanel` | launcher |
| `~/.config/ascendedpanel/<name>.json` | instance configuration |
| `~/.config/ascendedpanel/token` | web token (0600) |
| `~/arkserver-<name>` | server files of the instance |
| `~/ascendedpanel-backups/<name>` | world backups (tar.gz) |
| `~/ascendedpanel-snapshots/<name>` | full instance snapshots (rollback after an update) |
