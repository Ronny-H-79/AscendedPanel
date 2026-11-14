## [0.16] — 2026-11-14

### Added
- **File browser inside the panel.** The "Files" tab of an instance shows its directory in the
  browser: open folders, upload files (several at once), download, rename, delete and create new
  folders. Everything stays inside the instance directory — paths with `..` are rejected and
  downloads are streamed. **Read and edit files:** clicking a name opens the content in the browser
  (text up to 2 MB, binary files rejected), "Save" writes it back and keeps a `.bak` copy — handy for
  `GameUserSettings.ini` right inside the panel.
- **Per-instance SFTP access.** Every instance card offers "SFTP einschalten" (enable): own user,
  generated password, port from `sftp_base_port + running number` (default 2225), chroot to the
  instance directory — FileZilla compatible (SFTP, not FTP). "New password" creates one instantly and
  copies it to the clipboard, "off" closes the port again.
- The service runs as `ascendedpanel-sftp` (systemd, user or system service). When no user bus is
  reachable — e.g. the panel started via `nohup` — it starts detached with a PID file `sftp.pid` so the
  access still works.
- **Requirement:** `asyncssh` (`apt install python3-asyncssh`). Without it the panel keeps working;
  only the SFTP service reports the missing module in the panel log.

### Changed
- **Token stays the same.** The web token is generated on the very first start only and read from
  `~/.config/ascendedpanel/token` afterwards — restarts, updates and self-updates do not change it, so
  old links keep working. A new token is only created when that file is deleted.
- The instance JSON gained `sftp_enabled`, `sftp_user`, `sftp_password`, `sftp_port`; the card shows
  `sftp://user@host:port`.

## [0.15] — 2026-11-14

### Added
- **AsaApi support.** An instance can now start through the ArkApi loader: when `asaapi` is set and
  `ArkApi/AsaApiLoader.exe` exists inside the instance, the panel launches the loader instead of
  `ArkAscendedServer.exe`, which is what makes in-game plugins work (e.g. the quest plugin with
  `!quests`/`!argy`). Install detection and the start guard still check the real server binary, so an
  instance without a loader is not reported as "not installed".

### Changed
- **Tribe logs over RCON.** The start command now also passes `-ServerRCONOutputTribeLogs`; together
  with `-servergamelog` and `-servergamelogincludetribelogs` claim/tame lines reach both the server log
  file and the RCON log buffer (CrossArkChat).

## [0.14] — 2026-11-13

### Fixed
- **No empty entries on the instance card.** If the map or the RCON port is missing, the line no longer
  shows a bare "·" but only the values that exist (`<map> · Port <n> · RCON <n>`).

## [0.13] — 2026-11-13

### New
- **Download speed in the install window.** Alongside step and percentage the current rate in MB/s is
  shown — computed from the byte counters in the steamcmd lines and smoothed so the number does not
  jump around.

## [0.12] — 2026-11-13

### Fixed
- **Instances no longer start by themselves after installation.** The supervisor was enabled right
  after the install; as a freshly installed server never ran, it read "process gone" as a crash and
  started it immediately. The instance is now marked as "stopped" (`runner.mark_stopped`) before the
  service starts — starting only happens via "Start" in the panel. The marker is cleared on start, so
  crash detection works as before, and an instance that was never started also stays off after a
  system boot.

## [0.11] — 2026-11-13


### Overview
Rough summary of what the panels contain.

- **Two panels, one base:** AscendedPanel for ARK: Survival Ascended, PolyPanel for ASA, ASE,
  Satisfactory, 7 Days to Die and Space Engineers. Browser UI, service on the server.
- **Dashboard:** instance cards with status, map, ports, build, CPU/RAM, players and uptime; start,
  restart, update, stop and delete right on the card, buttons locked by state (while stopping only
  the menu stays available, and so on).
- **Instance page:** live log, config editor with backup and validation (INI values as a form or
  raw), mod management with CurseForge search and update check, backups, snapshots, schedule and an
  RCON console with one-click commands.
- **Players:** list with kick, ban, whitelist and giving items — catalogue with search and a
  quantity window; the required player id (ARKID) is read from the `.arkprofile` files because ARK
  only exposes the EOS id over RCON.
- **Bans:** its own "banned players" window with per-row unban and an honest note on why ARK does
  not hand out its ban list over RCON.
- **Operation:** crash detection with automatic restart, Discord notifications, German/English
  switchable at any time, several instances in one process.
- **Bug reports:** button in the panel, report goes to the operator (webhook, console-only) with
  version, instance, system and log excerpt, passwords stripped.

### Fixed
- **The install progress bar ran backwards or froze.** SteamCMD restarts every phase at 0 %
  (download → verify → commit), so the bar jumped back. It now shows the overall progress across the
  three steps and never drops below its previous maximum.
- **`/api/install/progress` raised an error** as soon as a progress line appeared in the install log:
  the phase table `_PHASE_STEP` was used but never defined, which left the bar stuck.
- **"Install" shows the progress again.** If the remembered tab was "Settings", it covered the install
  panel — the click looked like it landed in the settings while the install ran in the background.
- **Deleting no longer blocks the UI.** Stopping (the server saves first) and removing several GB now
  run as a background job; the card shows "stopping the server …", then "deleting server files …" and
  finally the freed size. Every delete is logged with timestamp and freed MB in `panel.log`.
- **Wine is installed without asking** — like Xvfb. The "install Wine?" question was answered with
  "no" in practice, and afterwards no Windows game started.