# Internals

Structure, console usage, stop order and notes for developers.

[← back to the README](../README.md) · [Deutsch](technik.de.md)

## Usage

```bash
noah web               # web UI on http://127.0.0.1:8790
noah url               # ready-made address including the token
noah status            # process, RCON, last log line
noah start --wait 240
noah stop              # SaveWorld → DoExit → SIGTERM → SIGKILL
noah update --check    # is a new Steam build available?
noah supervise --all   # auto-restart, schedule, backups
```

## Structure

| File | Purpose |
|---|---|
| `noah/instance.py` | instance configuration (JSON), paths, writing INI files, start parameters |
| `noah/runner.py` | start/stop/status/update, RCON shutdown, maintenance lock |
| `noah/consoled.py` | starts the server on a PTY so Wine opens no window |
| `noah/rcon.py` | own Source RCON client |
| `noah/supervisor.py` | health check, auto-restart, schedule, countdown |
| `noah/registry.py` | several instances, port picking, metrics |
| `noah/mods.py` · `whitelist.py` · `config.py` · `backups.py` · `snapshots.py` | feature modules |
| `noah/webui.py` | dashboard, instance pages, JSON API (stdlib `http.server`) |
| `noah/cli.py` | command line including `wizard` |

## Stop order (deliberate)

1. RCON `SaveWorld` — save the game state
2. RCON `DoExit` — regular shutdown
3. `SIGTERM` to the process group
4. `SIGKILL`

A `kill` without step 1 costs everything since the last autosave.
