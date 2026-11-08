# noah — ARK: Survival Ascended server manager for Linux

English · [Deutsch](README.de.md) — the installer asks for the language up front, and the UI can switch
any time (button in the top right, `noah lang en` on the console).

[![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal&logoColor=white)](https://www.paypal.com/donate/?business=ronnyhase%40fn.de&item_name=noah%20Servermanager&currency_code=EUR)
[![Discord](https://img.shields.io/badge/Discord-Ark--ASA--ASE--Hilfe-5865F2?logo=discord&logoColor=white)](https://discord.gg/ark-ase-asa-hilfe)

**[Installation](#installation)** · [Uninstall](#uninstall) · [Features](docs/funktionen.md) · [Access](docs/zugriff.md)

Your own server manager for ARK ASA dedicated servers: start, stop, updates, mods, backups, settings
and player management through a web interface.

> **Not an app — no installer for Windows or macOS.** noah runs as a service on the Linux server and
> is used in a **browser**: from your PC, laptop, tablet or phone, on your LAN or over VPN. There is
> nothing to download and no file to launch — just an address with a token.

Plain Python (standard library only), SteamCMD for install and updates, Wine for the server process,
RCON for everything the server exposes.

![Dashboard](docs/screenshot-dashboard.png)

## Screenshots

| | |
|:--:|:--:|
| ![Settings](docs/screenshot-settings.png) | ![Mods](docs/screenshot-mods.png) |
| ![Overview](docs/screenshot-overview.png) | ![Management](docs/screenshot-manage.png) |

## Installation

```bash
git clone https://github.com/Ronny-H-79/Noah.git noah   # once
cd noah
./install.sh --check     # check what is missing (changes nothing)
./install.sh             # install
noah wizard              # create an instance, download the server, set up the service
```

**Requirements:** Linux, Python ≥ 3.10, Wine, `curl` and `tar`. Missing packages are offered by the
installer (`pacman`, `apt`, `dnf`, `zypper`). SteamCMD is downloaded automatically; root is only needed
to install Wine.

The installer asks, in order:

- **language** (German/English)
- whether missing packages (**Wine**, iproute2) should be installed
- **how the UI should be reachable:**
  **Tunnel** — client-side only over SSH,
  **Domain** — public with HTTPS (stored for later),
  **IP** — directly via IP and port (HTTP, open the port in your firewall)
- **only for "Domain"**: whether the UI should run permanently (`noah-web.service`) — as root a
  **system service** in `/etc/systemd/system` (starts at boot, no login or `linger` needed), as a normal
  user a user service in `~/.config/systemd/user`

With **"Tunnel"** the last question is skipped: no long-running service is needed, the UI starts with
`noah web` when you want it.

At the end you get the command that matches your choice: the SSH tunnel with your user and the
**server IP** (not the hostname — often not resolvable from outside), or
`sudo noah proxy --write --cert`, which uses the stored domain.
`--web` / `--no-web` skips the service question.

> **Security:** the UI is an admin console — whoever has the token controls everything. Mode `[3]`
> (direct via IP) is **unencrypted** and the token can be read on the wire. Use `[1]` (SSH tunnel) or
> `[2]` (HTTPS). Details: [docs/zugriff.md](docs/zugriff.md).

### When the install gets stuck

| Message | Cause | Fix |
|---|---|---|
| `fatal: destination path 'noah' already exists` | the folder is already there | `cd noah && git pull` instead of cloning again |
| `./install.sh: No such file or directory` **after** `cd noah` | you are in the package folder `noah/noah` — only `.py` files live there | `cd ..` — `install.sh` is one level up |
| `noah: command not found` | `~/.local/bin` is not in `PATH` | as root the installer links `/usr/local/bin/noah`; otherwise `export PATH="$HOME/.local/bin:$PATH"` and open a new shell |

Details, requirements and uninstall: [INSTALL.md](INSTALL.md)

## Uninstall

**The program only** (instances, backups and settings stay):

```bash
./install.sh --uninstall
```

This also stops and removes the systemd units (`noah-web`, `noah-*`) so nothing points at a missing
file afterwards. If the source folder is already gone:

```bash
systemctl --user disable --now noah-web.service noah-test.service
rm -f ~/.config/systemd/user/noah-*.service ~/.local/bin/noah
rm -rf ~/.local/share/noah
```

**Everything** — additionally config, token, backups and server files (about 24 GB):

```bash
rm -rf ~/.config/noah          # instances, token, mod cache
rm -rf ~/noah-backups          # world backups
rm -rf ~/noah-snapshots        # instance snapshots
rm -rf ~/arkserver             # the server files (12 GB)
rm -rf ~/.wine-arkserver       # Wine prefix
```

Only the last step is irreversible: worlds and configs live in `~/noah-backups` — keep those and you can
restore everything later.

## More

| Topic | File |
|---|---|
| **Features** — overview, screenshots, mod search, Discord notifications | [docs/funktionen.md](docs/funktionen.md) |
| **Access** — SSH tunnel, LAN, HTTPS via nginx, token | [docs/zugriff.md](docs/zugriff.md) |
| **Operation** — self-update, changelog, language | [docs/betrieb.md](docs/betrieb.md) |
| **Internals** — structure, console, stop order | [docs/technik.md](docs/technik.md) |

What changed between versions: [CHANGELOG.en.md](CHANGELOG.en.md) ·
Install details: [INSTALL.md](INSTALL.md)

## Help

Questions, problems or just other server admins: the
**[Ark-ASA-ASE-Hilfe](https://discord.gg/ark-ase-asa-hilfe)** community on Discord helps with settings,
mods and start-up problems. That is also the place for feedback on noah.

## Licence

**Free to use, all rights reserved.** Downloading, installing and running it on your own servers is free
of charge — including for a community. Redistribution, modification, selling it or offering it as a
download/service requires written permission. Details: [LICENSE](LICENSE).

© 2026 Ronny H.
