# Changelog

Notable changes to noah. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows
[Semantic Versioning](https://semver.org/).

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
