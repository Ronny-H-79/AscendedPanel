# Changelog

Notable changes to noah. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows
[Semantic Versioning](https://semver.org/).

## [0.3.53] — 2026-11-08

### Fixed
- **Cached search results could hide the API results.** A fallback result (few hits, no key) was served
  for an hour even after a key had been set — the search kept showing 8 instead of 30 hits. The cache now
  separates keyed/unkeyed searches and the hit limit, and stores the total count.

## [0.3.52] — 2026-11-08

### Changed
- **Mod search lists up to 30 hits** instead of 10, with the hit count above it ("30 / 1,412 hits",
  total taken from the CurseForge response). The list scrolls instead of stretching the page.

## [0.3.51] — 2026-11-08

### Changed
- **`console.curseforge.com` in the "CurseForge API key" field is a link now** (opens in a new tab)
  instead of plain text.

## [0.3.50] — 2026-11-08

### Changed
- **Discord and PayPal icons are bigger and use the brand colours** (34 px box, 22 px glyph; Discord
  #5865F2, PayPal #003087) instead of small and monochrome.

## [0.3.49] — 2026-11-08

### Added
- **Discord and PayPal icons in the top right** — on every page (dashboard, instance page, mods,
  management). The icons are embedded, so no request goes to an external server unless someone clicks.

## [0.3.48] — 2026-11-08

### Added
- **Tabs in the settings form:** the 90 known INI values are sorted into nine groups — Server & access,
  Gameplay & rates, PvP & rules, Structures & decay, Dinos & breeding, Transfer & cluster, Display, MOTD
  and Game.ini. Each tab shows its count; the browser remembers the last choice.
- Saving still writes everything at once — fields on the other tabs are kept.

## [0.3.47] — 2026-11-08

### Changed
- **The button reads "Menu" and opens the instance directly** — label as requested, no intermediate step
  or dropdown.

## [0.3.46] — 2026-11-08

### Changed
- **Back to the direct route:** "Open" leads straight into the instance again; the menu button and dialog
  are gone.

## [0.3.45] — 2026-11-08

### Changed
- **No dropdown in the card any more:** a plain **"Menu"** button opens a choice of Overview, Settings,
  Mods and Management.

## [0.3.44] — 2026-11-08

### Changed
- **The selector in the card is labelled "Menu …"** instead of "Open …" — it is a choice, not a button.

## [0.3.43] — 2026-11-08

### Changed
- **Start page reordered:** "New instance" and "Note" sit on top now, the instances follow below — the
  creation form stays where it is even when instances are added.
- **"Open" is a menu:** pick Overview, Settings, Mods or Management; the detail page jumps to that tab.
- Card and log sizing back to 0.3.39 (log only for running instances, 9.5 px, cards from 300 px).

## [0.3.39] — 2026-11-08

### Changed
- **Running instances span two grid columns** on the dashboard (window width 900 px and up). Otherwise the
  card was too narrow and the log dropped below the metrics instead of sitting next to them.

## [0.3.38] — 2026-11-08

### Added
- **Live server log inside the dashboard card.** Next to status and metrics the last log lines scroll by
  (refresh every 2.5 s), so you can see what the server is doing without opening the detail page. On
  narrow cards the log moves below the metrics.
- The number of lines follows the card height; empty output shows as "no output".

## [0.3.37] — 2026-11-08

### Changed
- **The CPU tile now shows the server's share (0–100 %)** instead of the sum over all cores. 755 % on
  64 cores appears as "11.8 %"; the history graph ends at 100 % as well. The core breakdown ("7.6 of 64
  cores") moved to the tooltip, the raw value stays in the API as `cpu`.

## [0.3.36] — 2026-11-08

### Fixed
- **The CPU tooltip showed `undefined`/`NaN`** when the response carried no core count (older answer in
  the browser cache). The fallback is now the browser's core count, otherwise 1.

## [0.3.35] — 2026-11-08

### Fixed
- **Self-update did not restart the user service.** Without a login session (via `su`, `ssh` or from a
  script) `XDG_RUNTIME_DIR` and `DBUS_SESSION_BUS_ADDRESS` were missing, `systemctl --user` failed and
  the web interface kept running the old code. Both variables are set now, so the restart also works
  from a non-login session.

## [0.3.34] — 2026-11-08

### Fixed
- **Self-update could destroy the installation.** `apply()` deleted the live package directory and only
  then copied the new one in — if the copy aborted (or the target still existed), a half-written
  directory was left behind and `noah` would no longer start. The new package is now built completely
  next to the target and swapped in with `rename`; if the swap fails, the previous state is restored.
- **Backups accumulated without limit.** Every update created a `noah.bak-<timestamp>`. Now the last two
  are kept.

## [0.3.33] — 2026-11-08

### Fixed
- **The CPU graph clipped everything above 100 %.** The dashboard sparkline was pinned to 100 %, so an
  ARK server at 700 % load showed as a flat line at the top. It now scales to the observed maximum
  (at least 100 %).
- **The CPU figure needed an explanation.** It sums all threads (like `top`/`htop`) and can therefore
  exceed 100 %. The tile's tooltip now names cores and share of the server, e.g. "7.5 of 64 cores busy
  (11.8 % of the server)".

## [0.3.32] — 2026-11-08

### Fixed
- **`--user` left the files owned by root** when no web service was set up (`--no-web`), so the user could not
  write its own configs. Ownership is now fixed right after copying.

## [0.3.31] — 2026-11-08

### Fixed
- **`--user NAME` was not recognised** ("unknown option"): the argument loop could not read a second word with
  `shift`. It is a `while` loop now, so `--user noah` and `--user=noah` work (as does `--lang de`).

## [0.3.30] — 2026-11-08

### Fixed
- **Self-update could silently install the same state.** The archive was fetched via the `main` branch, which
  codeload serves from cache for minutes. It now downloads the archive **for the verified commit**
  (`/tar.gz/<sha>`), so what the check reports is what gets installed.

## [0.3.29] — 2026-11-08

### Added
- **`sudo ./install.sh --user noah`** — install under a dedicated service user. The installer creates the
  user and home, copies to `/home/noah/…`, fixes ownership, sets the UI up as a **user service** and enables
  `loginctl enable-linger` so it starts without a login. Nothing runs as root any more.

## [0.3.28] — 2026-11-08

### Fixed
- **The game server died when the UI restarted while noah runs as a normal user.** The dedicated systemd
  scope was only attempted on the system bus, which fails without root, so the start silently fell back to
  a plain child process. It now uses `systemd-run --user --scope` via the user manager (needs a one-time
  `loginctl enable-linger <user>`), so the server survives a UI restart.

## [0.3.27] — 2026-11-08

### Added
- **Port check before start.** If another program (e.g. an AMP server) holds the game, query or RCON port,
  noah stops with a clear message instead of starting a server nobody can reach — and instead of sending
  RCON requests to the wrong server.

## [0.3.26] — 2026-11-08

### Fixed
- **Launch line modelled on AMP.** Port, query port, RCON and password now live only in the map URL
  (`?listen?Port=…?QueryPort=…?RCONEnabled=True?RCONServerGameLogBuffer=600?RCONPort=…?ServerAdminPassword=…`),
  the password as the **last** option — otherwise ASA swallows the rest of the line. The separate
  `-port`/`-RCONPort` arguments are gone.
- `-SessionName` is no longer passed as an argument (spaces in the name split the line); the name comes from
  `[SessionSettings]` in the INI.

## [0.3.25] — 2026-11-08

### Fixed
- **RCON still said "wrong password" even with `RCONEnabled=True`.** ASA only takes the admin password from
  the command line; the map URL now carries `?ServerAdminPassword=…` (exactly like AMP). Note: as with any
  ARK server, the password is then visible in `ps`.

## [0.3.24] — 2026-11-08

### Fixed
- **RCON replied "wrong password" on freshly created instances.** noah passed only `-RCONPort` and relied on
  the INI to enable it; ASA only honours that with `?RCONEnabled=True` in the map URL (same as AMP). The URL
  now carries `?listen?Port=…?RCONEnabled=True?RCONServerGameLogBuffer=600?RCONPort=…`. The password stays in
  the INI, so it does not show up in the process list.

## [0.3.23] — 2026-11-08

### Changed
- Example cluster directory in the hint: `/home/Noah/arkcluster` instead of `/home/user/arkcluster`.

## [0.3.22] — 2026-11-08

### Changed
- **Cluster fields show their defaults inside the input** — cluster ID is the instance name, directory is
  `<instance>/clusters`. You see the path and only overwrite it when maps should share. The hint also names
  an example (`/home/user/arkcluster`).

## [0.3.21] — 2026-11-08

### Added
- **Cluster settings.** `-clusterid=noah` and a per-instance directory used to be hardcoded, so maps could
  never share anything. The Settings tab now has a **Cluster** card: cluster ID, shared directory and the
  "transfers without filter check" option (`-NoTransferFromFiltering`). Without your own values the old
  behaviour stays.
- **53 more INI settings** from the full ARK set: transfer locks (download/upload of survivors, items,
  dinos), offline raid protection, tribe alliances, structure decay and pickup, dino decay, tamed dinos per
  player, imprinting, hit markers plus food/torpor and harvesting multipliers. The form is now grouped by
  file **and** section.

## [0.3.20] — 2026-11-08

### Fixed
- **"leer" in the whitelist list** was still hardcoded German; now translated via `i18n.py` (`empty`).

## [0.3.19] — 2026-11-08

### Fixed
- **Two more German strings in the English UI:** "kein Snapshot vorhanden" and the language-save error were
  hardcoded. Both now come from `i18n.py`.

## [0.3.18] — 2026-11-08

### Fixed
- **Mod status was hardcoded German** ("nicht heruntergeladen", "für alte Engine gebacken") and stayed
  German in the English UI. `mods.py` now returns codes and `i18n.py` supplies the text —
  `not downloaded` / `built for an older engine`.

## [0.3.17] — 2026-11-08

### Added
- **English description:** a button next to "Changelog" opens `README.en.md` on GitHub. The README now links
  between German and English at the top.

## [0.3.16] — 2026-11-08

### Fixed (important)
- **The UI was dead after page load:** the update progress code (0.3.13) contained a raw newline inside a
  JavaScript string — a syntax error that invalidated the whole script. Tabs stopped switching and mod
  buttons, settings and everything else stopped responding. Replaced with `String.fromCharCode(10)`;
  JavaScript is now checked with `node --check` before pushing.

## [0.3.15] — 2026-11-08

### Fixed
- **The game server no longer lives inside the web service.** It used to start as a child of `noah-web`;
  Wine processes stayed in that unit's cgroup on stop ("Unit process … remains running after unit
  stopped") and blocked every restart of the UI. Each instance now runs in its own transient unit
  (`noah-<name>.scope` via `systemd-run --scope`), so the server survives a UI restart and vice versa.
  Without systemd noah falls back to the previous start (`NOAH_NO_SCOPE=1` forces it).

## [0.3.14] — 2026-11-08

### Changed
- **The RAM note on the dashboard was misleading** ("about 11.5 GB per running server"). Usage depends on
  mods, world size and players: about 4 GB empty without mods, 11-12 GB with mods and a world, more above
  that. Adjusted in the UI and `INSTALL.md`.

## [0.3.13] — 2026-11-08

### Added
- **Update progress is visible.** SteamCMD output used to go to the service journal, so the server log
  showed nothing during an update. noah now writes it to `.update.log` and the UI streams it while the
  update runs (`/api/update/progress`, polled every 2 s).

## [0.3.12] — 2026-11-08

### Fixed
- **The changelog button showed the initial install.** Self-update replaced only the package directory, so
  the `CHANGELOG*.md` files next to it stayed stale. The update now carries both files along, and the UI
  re-fetches the text when its own version is missing.

## [0.3.11] — 2026-11-08

### Fixed
- **`noah url` printed `127.0.0.1` on a server.** With access mode "ip" it now shows the address the UI is
  actually reachable at.

## [0.3.10] — 2026-11-08

### Fixed
- **Self-update failed silently.** A single `504 Gateway Timeout` while downloading the archive aborted the
  run and the UI reported nothing, so the button looked dead. Now: three attempts with backoff and a
  second source (`codeload.github.com`), plus the UI shows "Update failed: …" instead of silence.
- The update runs synchronously; the service restart happens a second later so the response still arrives.

## [0.3.9] — 2026-11-08

### Added
- **The build badge is a button.** On the instance page it only read `UP TO DATE 26515168`; the update
  could only be started from the overview. Now `UPDATE a→b` starts the update on click (confirmation,
  backup, stop), `UP TO DATE b` re-checks. Tooltips explain both, keyboard (Enter/Space) works too.

## [0.3.8] — 2026-11-08

### Security
- **Constant-time token comparison** (`hmac.compare_digest`) instead of `==`.
- **Security headers** on every response: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`,
  `Referrer-Policy: no-referrer` (keeps the token out of the Referer header) and a restrictive CSP.
- **Mod IDs are validated** (digits only, max 10) — previously the value went unfiltered into the server
  command line (`-mods=…`).
- **Player IDs** (whitelist/bans) only as Steam64 or hex UniqueNetId; newlines and special characters are
  rejected instead of being written to the file.

## [0.3.7] — 2026-11-08

### Changed
- **Mod search works without an instance.** `/api/mods/search`, `/api/mods/suggest` and saving the API key
  sat behind the instance check and answered "keine Instanz" when no instance existed.
- The Mods tab shows which mode is active: `CurseForge API active · searches titles and descriptions,
  sorted by downloads` (green, with a masked key) or `No API key · only exact mod ID or CurseForge link`.

## [0.3.6] — 2026-11-08

### Changed
- The version button shows the state in its label: `up to date` or `new build`, not only in the tooltip.

## [0.3.5] — 2026-11-08

### Changed
- When noah reports "same version, new build only", the button is no longer clickable — there is
  nothing to fetch. Changes that should reach users get a version bump.

## [0.3.4] — 2026-11-08

### Changed
- Copyright uses the handle `ronny79privat` only (no real name).

## [0.3.3] — 2026-11-08

### Changed
- Copyright notice in README and `LICENSE` (ronny79privat).
- Developer notes moved out of the technical docs into `docs/entwicklung.md` — irrelevant for users,
  still reachable for contributors.

## [0.3.2] — 2026-11-08

### Changed
- README trimmed to the essentials (111 instead of 420 lines). Features, access, operation and
  internals moved to `docs/funktionen.md`, `docs/zugriff.md`, `docs/betrieb.md` and `docs/technik.md`.

## [0.3.1] — 2026-11-08

### Changed
- README reordered: installation and removal first, then remote access and the token; feature list
  and screenshots follow further down.

## [0.3.0] — 2026-11-08

### Added
- **Changelog button** in the header: opens the changes as a popup in the configured language
  (German/English). Content is read from the local installation, no network needed.
- English version: `CHANGELOG.en.md`.

### Changed
- The update dialog shows the changes of the new version directly.
- Notifications: routine messages stay in the log, only events go to Discord.

## [0.2.9] — 2026-11-08

### Added
- **CHANGELOG.md** — what changed in each version.
- The update dialog shows the changes of the new version before you confirm.
- **`scripts/release.sh`**: set version, commit, tag, push (with `--release` also the GitHub
  release, if `gh` is installed).

## [0.2.8] — 2026-11-08

### Fixed
- Mod search with an API key returned **zero results**: the `classId` parameter restricted the
  CurseForge query to a category that holds no ARK ASA mods. Without it the expected results come back.
- Empty search results are no longer cached for an hour.

## [0.2.7] — 2026-11-08

### Changed
- Update check is **cached for 10 minutes** — GitHub allows only 60 requests per hour without a token.
  `noah version` and `noah self-update` still check fresh.

## [0.2.6] — 2026-11-08

### Added
- **"← Dashboard"** in the header of the instance page.

### Changed
- The instance update badge only appears on a reliable check (it used to say "UPDATE ?" forever
  while the server files were missing).
- `install.sh` restarts a running `noah-web` service after copying, so the new code is active
  immediately.

## [0.2.5] — 2026-11-08

### Changed
- Update button in badge style instead of a solid block.

## [0.2.4] — 2026-11-08

### Changed
- Update button is labelled: `noah update: 0.2.3 → 0.2.4` instead of bare version numbers.

## [0.2.3] — 2026-11-08

### Fixed
- Self-update fetched the source archive from `codeload.github.com`, which still serves the old
  state after a push. Now it uses the GitHub API.

## [0.2.2] — 2026-11-08

### Fixed
- Version check read `raw.githubusercontent.com` (up to 5 minutes stale) — now via the GitHub API.

## [0.2.1] — 2026-11-08

### Fixed
- `/api/selfupdate` was only reachable when an instance existed.

## [0.2.0] — 2026-11-08

### Added
- **Self-update**: button in the header (`noah update: old → new`) and `noah self-update`.
- **Mod search**: mod ID, CurseForge link or name; suggestions appear while typing with image,
  downloads and one click to add. Names require a CurseForge API key.
- **Mod updates at a glance**: installed file vs. newest file on CurseForge, marked "UPDATE".
- **Discord notifications**: crash, hang, update available, backup failure, scheduled restart —
  routine messages stay in the log.
- **Hang and crash detection** in the supervisor; a manual stop is respected.
- **`noah proxy`**: sets up nginx with HTTPS (certificate via certbot, optional basic auth),
  verifies with `nginx -t` and rolls back on errors.
- **HTTPS directly** in the web server (`--tls-cert` / `--tls-key`).
- **Delete instance** on the dashboard card (config to `.trash`, files only on request).
- **Update button** and **delete** directly on the card.
- **MOTD** as a multi-line form field.
- **Bilingual** (German/English): language question in the installer, button in the UI,
  `noah lang`.
- **Three access modes** in the installer: client-side via SSH tunnel, public via domain+HTTPS,
  direct via IP and port.
- The **supervisor service** is created automatically after installing an instance (a system
  service as root, starting at boot).

### Changed
- Instance page: server log at the top across the full width and resizable (48 % height, 150 lines);
  control buttons live on the dashboard card.
- The log jumps to the end when opened; the active tab survives a reload.
- Map background clearly visible (opacity 0.28 → 0.62).
- Settings: multi-line fields (textarea) supported.
- `settings.json` is written with `0600` because it holds the API key.

## [0.1.0] — 2026-11-07

First public release: create instances, start/stop/restart/update via SteamCMD, RCON console with
click commands, player management, mod management, config editor, world backups, snapshots,
whitelist/bans, schedule, live metrics and a web interface.