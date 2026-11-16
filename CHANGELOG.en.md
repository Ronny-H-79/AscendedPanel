## [0.21] — 2026-11-16

### New
- **The card shows what is happening.** Previously an update in progress showed only "STOPPED". Now
  a hint line appears (⏳ UPDATING, INSTALLING, RESTARTING, STOPPING, DELETING, SETTING UP ASAPI)
  sourced from the panel's running actions; `runner.stop()` reports its state so the stop is visible.
  The status badges also name the action on the detail page ("SHUTTING DOWN" in yellow instead of
  "RUNNING" until the end), and the buttons stay locked until it finishes.

### Changed
- **Mod descriptions** are translated completely (no 400-character cut, chunked with retry,
  fallback service on Google rate limits, no English text cached) and wrapped for readability:
  role sections ("Primary roles", "Hauptfunktionen", "Hauptaufgaben") and long sentences get their
  own lines; up to five lines in the result list instead of a hard 90-character cut.

## [0.18] — 2026-11-15

### Changed
- **No extra window when creating or installing.** Creating stays on the overview (the new card
  appears there), and the installation shows its progress in the same tab.

### Fixed
- **Server password survives.** `write_ini()` hard-coded `ServerPassword` to empty on every start, so
  a configured join password was gone after the next start. It now lives in the instance, is written
  to the INI and passed as `?ServerPassword=` on the command line (admin password stays the last
  option, otherwise it swallows the rest).
- **Ammo in the item dialog.** All ammo entries pointed at `Items/…` while the assets live under
  `Weapons/…` — giving failed silently. Paths corrected, missing ammo added (simple rifle ammo among
  them). Label fixed: `OneShotRifle` is the longneck rifle, the shotgun (`PrimalItem_WeaponShotgun`)
  was missing entirely.

## [0.17] — 2026-11-14

### New
- **AsaApi is part of the installation.** After the SteamCMD run the panel sets up AsaApi
  automatically (the complete release including `config.json` and the bundled DLLs) and starts the
  instance through `AsaApiLoader.exe` from then on. The **"API"** button on the card installs or
  updates the API by hand at any time; it only appears when there is something to do and shows a
  version badge for a newer release. A checkbox in the "Mods" tab turns the API and its plugins off
  again (starting without the loader). If the setup fails, the server stays installed and the button
  is the way to catch up. Install detection and the start guard still check the real server binary,
  so an instance without a loader is not reported as "not installed".
- **Firewall comes along.** On start the panel adds the game and query port (UDP) to `ufw`, and
  removes those rules when the instance is deleted. For `ufw` the installer creates a tightly scoped
  `sudo` rule (only `/usr/sbin/ufw`); if it is missing, the server still starts and the panel log
  names the reason.
- **Paste mod IDs directly.** The "Mods" tab has a field for mod IDs (comma, semicolon or space as
  separator). It shows the active list and replaces it on save.
- **File browser inside the panel.** The "Files" tab shows the instance directory: open folders,
  upload several files at once, download, rename, delete, create folders. Paths with `..` are
  rejected, downloads are streamed. Clicking a name opens text files up to 2 MB in the browser
  (binary files rejected); "Save" writes it back and keeps a `.bak` copy.
- **Per-instance SFTP access.** Own user, generated password, port from `sftp_base_port + running
  number` (default 2225), chroot to the instance directory — FileZilla compatible (SFTP, not FTP).
  "New password" copies it to the clipboard, "off" closes the port. The service runs as
  `ascendedpanel-sftp`; when no user bus is reachable (panel started via `nohup`) it starts detached
  with `sftp.pid`. Requirement: `asyncssh` — without it the panel keeps working and only the SFTP
  service reports the missing module in the panel log.

### Changed
- **Metrics count every process of the instance.** Under Wine/Proton and with the API loader the
  server process is not attached to the starter PID, which is why CPU and RAM showed as 0; all
  processes of the instance are now found via their command line and summed up.
- **SessionName and MaxPlayers survive** (values from `GameUserSettings.ini` are carried back into the
  instance), and the section in `Game.ini` is recognised regardless of its capitalisation.
- **Token stays the same.** The web token is generated on the very first start only and read from
  `~/.config/ascendedpanel/token` afterwards — restarts, updates and self-updates do not change it; a
  new one is only created when that file is deleted. The instance JSON gained `sftp_enabled`,
  `sftp_user`, `sftp_password`, `sftp_port` and the card shows `sftp://***@host:port`.
- **Tribe logs over RCON.** The start command now also passes `-ServerRCONOutputTribeLogs`; together
  with `-servergamelog` and `-servergamelogincludetribelogs` claim/tame lines reach both the server
  log file and the RCON log buffer.

### Fixed
- Starting through `AsaApiLoader.exe` aborted with "LoaderFailed, Reason: UnknownLoaderResult" when
  the API release's `config.json` was missing in the Win64 directory.
- A duplicate `ActiveMods` line could make the server silently ignore configured mods on start.

## [0.14] — 2026-11-13

### New
- **Download speed in the install window.** Alongside step and percentage the current rate in MB/s is
  shown — computed from the byte counters in the steamcmd lines and smoothed so the number does not
  jump around.

### Fixed
- **Instances no longer start by themselves after installation.** The supervisor was enabled right
  after the install and read "process gone" on a server that never ran as a crash. The instance is
  now marked as "stopped" before the service starts (`runner.mark_stopped`); starting only happens via
  "Start" in the panel, also after a system boot.
- **Install progress bar and progress API.** The bar jumped back because SteamCMD restarts every phase
  at 0 % — it now shows the overall progress and never drops below its previous maximum.
  `/api/install/progress` raised an error as soon as a progress line appeared in the log (the phase
  table `_PHASE_STEP` was used but never defined). "Install" shows the progress again even if the
  "Settings" tab was open last.
- **Deleting no longer blocks the UI.** Stopping and removing several GB run as a background job; the
  card shows "stopping the server …", then "deleting server files …" and the freed size. Every delete
  is logged with timestamp and freed MB in `panel.log`.
- **No empty entries on the instance card.** If the map or the RCON port is missing, there is no bare
  "·" but only `<map> · Port <n> · RCON <n>`.
- **Wine is installed without asking** — like Xvfb. The "install Wine?" question was answered with
  "no" in practice, and afterwards no Windows game started.

## Overview

Rough summary of what the panel contains.

- **One panel, one base:** AscendedPanel for ARK: Survival Ascended, browser UI, service on the
  server.
- **Dashboard:** instance cards with status, map, ports, build, CPU/RAM, players and uptime; start,
  restart, update, stop and delete right on the card, buttons locked by state.
- **Instance page:** live log, config editor with backup and validation (INI values as a form or raw),
  mod management with CurseForge search and update check, backups, snapshots, schedule, an RCON
  console with one-click commands, file browser and SFTP.
- **Players:** list with kick, ban, whitelist and giving items — catalogue with search and a quantity
  window; the required player id (ARKID) is read from the `.arkprofile` files because ARK only
  exposes the EOS id over RCON.
- **Bans:** its own "banned players" window with per-row unban and an honest note on why ARK does not
  hand out its ban list over RCON.
- **Operation:** crash detection with automatic restart, Discord notifications, German/English
  switchable at any time, several instances in one process.
- **Bug reports:** button in the panel, report goes to the operator (webhook, console-only) with
  version, instance, system and log excerpt, passwords stripped.
