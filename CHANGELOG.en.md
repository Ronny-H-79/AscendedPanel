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
