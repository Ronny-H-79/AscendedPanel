## [0.43] - 2026-11-26

- Line numbers in the file view: on the left margin, following scroll and typing. Applies to the
  editor in the instance tab and to the full-screen view. Line wrapping is off there so numbers and
  lines stay exactly aligned.

## [0.42] - 2026-11-25

- New switch under Mods: start the server without AsaApi when the loader does not match after an
  ARK update. The server stays reachable; quests, starter kit and kill counting are missing in game.
  Switch it back once the loader works again.

## [0.41] - 2026-11-25

- Every delete now asks first: file, mod, mod files, snapshot, backup and whitelist entry. The texts
  exist in both languages; they used to be hard-coded German.

## [0.40] - 2026-11-24

- File editor: long lines are no longer wrapped but scroll sideways. The Bjarnheim ini has a single
  line of 13,896 characters that used to wrap across the screen.

## [0.39] - 2026-11-24

- Tests instead of "works on my machine". 27 checks using the standard library (`tests/`): ini
  handling (duplicate keys, comments, CRLF, idempotence), mod order and pinning, update decision
  (never offer a downgrade), route-table completeness, and a smoke test that starts the web server
  in a temporary directory and exercises login, core routes and instance management.
- **GitHub Actions** (`.github/workflows/ci.yml`): on every push and pull request, Python 3.10, 3.12
  and 3.13 - style check, text check, tests.
- **`ruff` clean** with configuration in `pyproject.toml`; real bugs it found are fixed: duplicated
  translation keys (the second entry silently overrode the first), unused assignments, missing
  `raise … from`, ambiguous variable names.
- The POST handler is split up. Instead of one 559-line chain there are now 22 methods per topic
  (mods, files, backups, schedule …) and a `_POST_ROUTES` table. Behaviour unchanged: 31 requests
  were compared against the previous version, no difference.
- `CONTRIBUTING.md` covers the test run, change rules and bug reports.

## [0.38] - 2026-11-24

- Free licence: MIT. The project was "all rights reserved" until now. From here on anyone may
  use, modify, redistribute and also sell it - the only condition is that the copyright notice and
  the warranty disclaimer stay. `LICENSE` holds the full text, README and docs are updated, the
  footer shows "MIT licence".

## [0.37] - 2026-11-24

- File list on phones without sideways scrolling. Each row is a small block now: filename top
  left, size top right, date bottom left, the four action boxes bottom right. Instead of panning a
  520 px table, everything fits the screen width.

## [0.36] - 2026-11-24

- Action boxes are 36 × 36 px on phones. The mobile enlargement got lost while tidying up; the
  fields are large enough for a thumb again.

## [0.35] - 2026-11-24

- Stray brace in the stylesheet. Reworking the mobile rules left an extra `}` in the base
  styles; the file list lost its `overflow-x` and pushed the page to 543 px. The rule now sits in
  the mobile block and the page stays at 375 px.

## [0.34] - 2026-11-24

- The file list pushed the page wider. The 520 px minimum table width forced the whole page to
  556 px on a 390 px screen, so you had to pan sideways. Sections and cards may shrink now
  (`min-width:0`); the table scrolls inside its own box only.

## [0.33] - 2026-11-24

- Readable server log on phones. Font raised to 12 px with more line height and a taller log
  box (58 vh) so you don't have to zoom. The status badges in the header are slightly larger and
  easier to hit.

## [0.32] - 2026-11-24

- The header is a single row on phones. CPU, RAM, version, changelog, panel restart and the
  language switch sit side by side and scroll horizontally instead of stacking into four rows.
  That shrinks the header from 227 to roughly 90 pixels.

## [0.31] - 2026-11-24

- The mobile rules did not apply. The mobile block sat in the middle of the stylesheet and was
  overridden by later base rules - inputs stayed at 14 px (which makes iOS zoom in on tap) and the
  header stayed 248 px tall. The rules are now a separate block at the end of the stylesheet and
  apply reliably.

## [0.30] - 2026-11-24

- Mobile layout tidied up. Below 720 px: single column, cards and sections full width, stats in
  a 2×2 grid instead of four across, settings with the label above the field, tabs scroll
  horizontally, buttons at least 40 px tall and inputs at 16 px (so iOS does not zoom in). The
  header wraps instead of running over the edge.

## [0.29] - 2026-11-24

- The action icons in the file list are boxes now. Instead of bare little glyphs each action
  sits in its own field (30×30 px, 34×34 on phones): download outlined in green, delete in red.
  That makes them easy to hit with a finger.
- The file list scrolls horizontally on narrow screens instead of squeezing columns.

## [0.28] - 2026-11-24

- The full view sat in the wrong section. The overlay lived inside the overview tab (hidden on
  open) instead of outside the tabs, so it stayed invisible although the content loaded. It now
  sits right after `<main>` and covers the page regardless of the active tab.

## [0.27] - 2026-11-24

- Download files. Each file in the list gets its own download arrow (⬇) - a real link, so the
  browser saves it straight away instead of routing it through the editor. Name and extension are
  preserved (`Content-Disposition`).
- Direct full view. The ⤢ icon opens the file full-screen: a large editor with save, download
  and close. `Esc` closes it again. The small preview box below stays for a quick look.

- Action column in the file list. Download, full view, rename and delete now sit as their own
  icons at the right of each row instead of between filename and size.

## [0.26] - 2026-11-24

- The update badge offered a downgrade. When the local build was already newer than GitHub
  (own deploy before the push), the panel reported “update 0.25 → 0.24” - a downgrade as an
  update. Only a **higher** GitHub version counts as an update now; if the local build is ahead,
  the badge stays on “up to date”.
- A stale cache pinned the old reading. The 10-minute cache was served even when the “newer”
  version it recorded was older than the installed one. Such entries are dropped and re-checked.
- The build file is no longer shipped. `.build` was tracked in the repo and overwritten with a
  stale version (0.3.34) on every deploy, so the panel kept reporting “new build available” even
  though version and commit already matched. The file is now only written on update or deploy.

## [0.25] - 2026-11-24

- Action bar on the instance cards. Instead of six grey text buttons each card now carries a
  coloured pill with three groups - like a file manager: **red** stop and delete, **blue** menu,
  update, AsaApi, **green** start and restart. The icons keep the text as a tooltip, disabled
  actions stay visible (faded) instead of disappearing, and a small dot on the AsaApi icon marks a
  pending update.

## [0.24] - 2026-11-24

- Sort and pin mods. In the mods tab, active mods can be reordered with ▲/▼ or by drag & drop;
  a pin (📍) keeps a mod at the top for good (📌) - stacking mods, for instance, which have to load
  early. The order is the **load order**: it goes into `-mods=` on the command line and into
  `ActiveMods` in Game.ini. A pure reorder rewrites that single line only.

- Game.ini is no longer rewritten. `write_ini()` used to regenerate it through `configparser`,
  which keeps only one value per key and section and drops duplicates. In a real ARK file this
  removed 795 `EngramEntryAutoUnlocks`, 156 `ConfigOverrideItemMaxQuantity` and 99
  `OverridePlayerLevelEngramPoints` entries - 1,182 lines and 121 KB became 128 lines and 18 KB.
  Values were normalised as well (`true` → `True`, `DifficultyOffset=4` → `1.0`). Now only single
  lines are touched; everything else is preserved byte for byte, including comments, order and CRLF.
- Admin values in GameUserSettings.ini survive. `ServerPVE`, `DifficultyOffset`,
  `ServerCrosshair` and `ShowMapPlayerLocation` are only written when the key is missing. RCON,
  passwords, ports and `MaxPlayers` are still enforced by the panel.
- INI backups go into the `backup/` subfolder next to the INIs instead of a `.bak` file beside
  them (last 20 versions per file). The config folder no longer collects backup files.
- Line endings are preserved. Saved INIs were written with LF instead of CRLF, shrinking them by
  one byte per line.
- “Before update” backups are labelled as such instead of showing up as “older”.

## [0.23] - 2026-11-22

### New
- Save button in the snapshot section. Snapshot times and "keep auto-snapshots" had no save
  control of their own; users had to scroll to the schedule. The new button writes only those two
  values (`/api/schedule` with `snaptimes`/`snapkeep`) and leaves restart, backup and warning times
  untouched.
- **The backup box is back** (0.22). The "Manage" tab lists world backups again (list, "Back up now",
  restore, delete). The JavaScript functions existed, the HTML container was missing; the list loads
  when the tab opens. A hint next to it points to instance snapshots for rolling back the server
  version.

- **New instances** get `OverrideOfficialDifficulty=10.0` (wild dinos up to level 300) and
  `bServerRCONOutputTribeLogs`/`bServerGameLogIncludeTribeLogs` (tribe logs to RCON/gamelog, required
  for tame/claim quests).

## [0.21] - 2026-11-16

### New
- The card shows what is happening. Previously an update in progress showed only "STOPPED". Now
  a hint line appears (⏳ UPDATING, INSTALLING, RESTARTING, STOPPING, DELETING, SETTING UP ASAPI)
  sourced from the panel's running actions; `runner.stop()` reports its state so the stop is visible.
  The status badges also name the action on the detail page ("SHUTTING DOWN" in yellow instead of
  "RUNNING" until the end), and the buttons stay locked until it finishes.

- **Mod descriptions** are translated completely (no 400-character cut, chunked with retry,
  fallback service on Google rate limits, no English text cached) and wrapped for readability:
  role sections ("Primary roles", "Hauptfunktionen", "Hauptaufgaben") and long sentences get their
  own lines; up to five lines in the result list instead of a hard 90-character cut.

## [0.18] - 2026-11-15

- No extra window when creating or installing. Creating stays on the overview (the new card
  appears there), and the installation shows its progress in the same tab.

- Server password survives. `write_ini()` hard-coded `ServerPassword` to empty on every start, so
  a configured join password was gone after the next start. It now lives in the instance, is written
  to the INI and passed as `?ServerPassword=` on the command line (admin password stays the last
  option, otherwise it swallows the rest).
- Ammo in the item dialog. All ammo entries pointed at `Items/…` while the assets live under
  `Weapons/…` - giving failed silently. Paths corrected, missing ammo added (simple rifle ammo among
  them). Label fixed: `OneShotRifle` is the longneck rifle, the shotgun (`PrimalItem_WeaponShotgun`)
  was missing entirely.

## [0.17] - 2026-11-14

### New
- AsaApi is part of the installation. After the SteamCMD run the panel sets up AsaApi
  automatically (the complete release including `config.json` and the bundled DLLs) and starts the
  instance through `AsaApiLoader.exe` from then on. The **"API"** button on the card installs or
  updates the API by hand at any time; it only appears when there is something to do and shows a
  version badge for a newer release. A checkbox in the "Mods" tab turns the API and its plugins off
  again (starting without the loader). If the setup fails, the server stays installed and the button
  is the way to catch up. Install detection and the start guard still check the real server binary,
  so an instance without a loader is not reported as "not installed".
- Firewall comes along. On start the panel adds the game and query port (UDP) to `ufw`, and
  removes those rules when the instance is deleted. For `ufw` the installer creates a tightly scoped
  `sudo` rule (only `/usr/sbin/ufw`); if it is missing, the server still starts and the panel log
  names the reason.
- Paste mod IDs directly. The "Mods" tab has a field for mod IDs (comma, semicolon or space as
  separator). It shows the active list and replaces it on save.
- File browser inside the panel. The "Files" tab shows the instance directory: open folders,
  upload several files at once, download, rename, delete, create folders. Paths with `..` are
  rejected, downloads are streamed. Clicking a name opens text files up to 2 MB in the browser
  (binary files rejected); "Save" writes it back and keeps a `.bak` copy.
- Per-instance SFTP access. Own user, generated password, port from `sftp_base_port + running
  number` (default 2225), chroot to the instance directory - FileZilla compatible (SFTP, not FTP).
  "New password" copies it to the clipboard, "off" closes the port. The service runs as
  `ascendedpanel-sftp`; when no user bus is reachable (panel started via `nohup`) it starts detached
  with `sftp.pid`. Requirement: `asyncssh` - without it the panel keeps working and only the SFTP
  service reports the missing module in the panel log.

- Metrics count every process of the instance. Under Wine/Proton and with the API loader the
  server process is not attached to the starter PID, which is why CPU and RAM showed as 0; all
  processes of the instance are now found via their command line and summed up.
- SessionName and MaxPlayers survive (values from `GameUserSettings.ini` are carried back into the
  instance), and the section in `Game.ini` is recognised regardless of its capitalisation.
- Token stays the same. The web token is generated on the very first start only and read from
  `~/.config/ascendedpanel/token` afterwards - restarts, updates and self-updates do not change it; a
  new one is only created when that file is deleted. The instance JSON gained `sftp_enabled`,
  `sftp_user`, `sftp_password`, `sftp_port` and the card shows `sftp://***@host:port`.
- Tribe logs over RCON. The start command now also passes `-ServerRCONOutputTribeLogs`; together
  with `-servergamelog` and `-servergamelogincludetribelogs` claim/tame lines reach both the server
  log file and the RCON log buffer.

- Starting through `AsaApiLoader.exe` aborted with "LoaderFailed, Reason: UnknownLoaderResult" when
  the API release's `config.json` was missing in the Win64 directory.
- A duplicate `ActiveMods` line could make the server silently ignore configured mods on start.

## [0.14] - 2026-11-13

### New
- Download speed in the install window. Alongside step and percentage the current rate in MB/s is
  shown - computed from the byte counters in the steamcmd lines and smoothed so the number does not
  jump around.

- Instances no longer start by themselves after installation. The supervisor was enabled right
  after the install and read "process gone" on a server that never ran as a crash. The instance is
  now marked as "stopped" before the service starts (`runner.mark_stopped`); starting only happens via
  "Start" in the panel, also after a system boot.
- Install progress bar and progress API. The bar jumped back because SteamCMD restarts every phase
  at 0 % - it now shows the overall progress and never drops below its previous maximum.
  `/api/install/progress` raised an error as soon as a progress line appeared in the log (the phase
  table `_PHASE_STEP` was used but never defined). "Install" shows the progress again even if the
  "Settings" tab was open last.
- Deleting no longer blocks the UI. Stopping and removing several GB run as a background job; the
  card shows "stopping the server …", then "deleting server files …" and the freed size. Every delete
  is logged with timestamp and freed MB in `panel.log`.
- No empty entries on the instance card. If the map or the RCON port is missing, there is no bare
  "·" but only `<map> · Port <n> · RCON <n>`.
- Wine is installed without asking: like Xvfb. The "install Wine?" question was answered with
  "no" in practice, and afterwards no Windows game started.

## Overview

Rough summary of what the panel contains.

- One panel, one base: AscendedPanel for ARK: Survival Ascended, browser UI, service on the
  server.
- **Dashboard:** instance cards with status, map, ports, build, CPU/RAM, players and uptime; start,
  restart, update, stop and delete right on the card, buttons locked by state.
- Instance page: live log, config editor with backup and validation (INI values as a form or raw),
  mod management with CurseForge search and update check, backups, snapshots, schedule, an RCON
  console with one-click commands, file browser and SFTP.
- **Players:** list with kick, ban, whitelist and giving items - catalogue with search and a quantity
  window; the required player id (ARKID) is read from the `.arkprofile` files because ARK only
  exposes the EOS id over RCON.
- **Bans:** its own "banned players" window with per-row unban and an honest note on why ARK does not
  hand out its ban list over RCON.
- **Operation:** crash detection with automatic restart, Discord notifications, German/English
  switchable at any time, several instances in one process.
- Bug reports: button in the panel, report goes to the operator (webhook, console-only) with
  version, instance, system and log excerpt, passwords stripped.
