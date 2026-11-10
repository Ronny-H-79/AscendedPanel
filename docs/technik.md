# Internals

Structure, console usage, stop order and notes for developers.

[← back to the README](../README.md) · [Deutsch](technik.de.md)

## Usage

```bash
ascendedpanel web               # web UI on http://127.0.0.1:8790
ascendedpanel url               # ready-made address including the token
ascendedpanel status            # process, RCON, last log line
ascendedpanel start --wait 240
ascendedpanel stop              # SaveWorld → DoExit → SIGTERM → SIGKILL
ascendedpanel update --check    # is a new Steam build available?
ascendedpanel supervise --all   # auto-restart, schedule, backups
```

## Structure

| File | Purpose |
|---|---|
| `AscendedPanel/instance.py` | instance configuration (JSON), paths, writing INI files, start parameters |
| `AscendedPanel/runner.py` | start/stop/status/update, RCON shutdown, maintenance lock |
| `AscendedPanel/consoled.py` | starts the server on a PTY so Wine opens no window |
| `AscendedPanel/rcon.py` | own Source RCON client |
| `AscendedPanel/supervisor.py` | health check, auto-restart, schedule, countdown |
| `AscendedPanel/registry.py` | several instances, port picking, metrics |
| `AscendedPanel/mods.py` · `whitelist.py` · `config.py` · `backups.py` · `snapshots.py` | feature modules |
| `AscendedPanel/webui.py` | dashboard, instance pages, JSON API (stdlib `http.server`) |
| `AscendedPanel/cli.py` | command line including `wizard` |

## Stop order (deliberate)

1. RCON `SaveWorld` — save the game state
2. RCON `DoExit` — regular shutdown
3. `SIGTERM` to the process group
4. `SIGKILL`

A `kill` without step 1 costs everything since the last autosave.
