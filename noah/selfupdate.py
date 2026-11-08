"""Selbst-Update: pruefen, ob es eine neue noah-Version gibt, und einspielen.

Es wird kein git vorausgesetzt - noah laedt das Quellarchiv von GitHub und ersetzt
nur das Paketverzeichnis. Einstellungen, Instanzen und Backups bleiben unberuehrt.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import time
import urllib.request

REPO = "Ronny-H-79/Noah"
BRANCH = "main"
API_COMMIT = "https://api.github.com/repos/%s/commits/%s" % (REPO, BRANCH)
RAW_INIT = "https://raw.githubusercontent.com/%s/%s/noah/__init__.py" % (REPO, BRANCH)
CONTENTS = "https://api.github.com/repos/%s/contents/noah/__init__.py?ref=%s" % (REPO, BRANCH)
TARBALL = "https://api.github.com/repos/%s/tarball/%s" % (REPO, BRANCH)


def package_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def installed_version() -> str:
    try:
        from . import __version__
        return __version__
    except Exception:  # noqa: BLE001
        return "?"


def _tuple(version: str) -> tuple:
    parts = []
    for piece in (version or "").split("."):
        num = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(num) if num else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def _parse_version(text: str) -> str:
    for line in text.splitlines():
        if line.strip().startswith("__version__"):
            return line.split("=", 1)[1].strip().strip("\"'")
    return ""


def _get(url: str, timeout: int = 10) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "noah-selfupdate",
                                               "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


CACHE = os.path.expanduser("~/.config/noah/cache/selfupdate.json")
CACHE_TTL = 600          # 10 Minuten: GitHub erlaubt ohne Token nur 60 Anfragen/Stunde


def _cache_read() -> dict:
    try:
        with open(CACHE, encoding="utf-8") as fh:
            data = json.load(fh)
        if time.time() - data.get("_t", 0) < CACHE_TTL:
            return data
    except (OSError, ValueError):
        pass
    return {}


def _cache_write(info: dict) -> None:
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        payload = dict(info)
        payload["_t"] = time.time()
        with open(CACHE, "w", encoding="utf-8") as fh:
            json.dump(payload, fh)
    except OSError:
        pass


BUILD_FILE = os.path.join(package_dir(), ".build")


def remote_commit(timeout: int = 10) -> str:
    """Aktueller Commit auf GitHub (kurz).

    Zuerst `git ls-remote` - das unterliegt nicht dem API-Limit von 60 Anfragen/Stunde.
    """
    try:
        out = subprocess.run(
            ["git", "ls-remote", "https://github.com/%s.git" % REPO, "refs/heads/%s" % BRANCH],
            capture_output=True, text=True, timeout=timeout,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.split()[0][:7]
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        return json.loads(_get(API_COMMIT, timeout).decode())["sha"][:7]
    except Exception:  # noqa: BLE001
        return ""


def local_build() -> dict:
    """Welcher Commit liegt hier installiert? (von install.sh oder apply() geschrieben)"""
    try:
        with open(BUILD_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def write_build(sha: str, version: str) -> None:
    try:
        with open(BUILD_FILE, "w", encoding="utf-8") as fh:
            json.dump({"sha": sha, "version": version, "written": time.strftime("%F %T")}, fh)
    except OSError:
        pass


def check(timeout: int = 10, force: bool = False) -> dict:
    """Vergleicht die installierte Version mit der auf GitHub (10 Minuten gecacht)."""
    local = installed_version()
    if not force:
        cached = _cache_read()
        if cached and cached.get("installed") == local:
            cached.pop("_t", None)
            return cached
    remote = ""
    try:
        # API liefert immer den aktuellen Stand (raw.githubusercontent.com cached bis zu 5 Minuten)
        import base64
        data = json.loads(_get(CONTENTS, timeout).decode("utf-8"))
        remote = _parse_version(base64.b64decode(data.get("content", "")).decode("utf-8", "replace"))
    except Exception:  # noqa: BLE001
        try:
            remote = _parse_version(_get(RAW_INIT, timeout).decode("utf-8", "replace"))
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": "%s: %s" % (exc.__class__.__name__, exc),
                    "installed": local, "available": "", "update": False}
    newer = bool(remote) and _tuple(remote) > _tuple(local)
    local_sha = local_build().get("sha", "")
    commit = remote_commit(timeout)
    changed = bool(commit and local_sha and commit != local_sha)
    info = {"ok": True, "installed": local, "available": remote, "update": newer or changed,
            "commit": commit, "local_commit": local_sha,
            "url": "https://github.com/%s" % REPO}
    _cache_write(info)
    return info


CHANGELOG = "https://api.github.com/repos/%s/contents/CHANGELOG.md?ref=%s" % (REPO, BRANCH)


def _local_changelog(name: str) -> str:
    """Changelog aus der eigenen Installation lesen (kein Netz noetig)."""
    for base in (package_dir(), os.path.dirname(package_dir())):
        path = os.path.join(base, name)
        try:
            with open(path, encoding="utf-8") as fh:
                return fh.read()
        except OSError:
            continue
    return ""


def _changelog_cache(name: str) -> str:
    path = os.path.expanduser("~/.config/noah/cache/%s" % name)
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def _store_changelog(name: str, text: str) -> None:
    try:
        path = os.path.expanduser("~/.config/noah/cache/%s" % name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    except OSError:
        pass


def changelog(lang: str = "de", timeout: int = 10) -> dict:
    """Komplettes Changelog in der gewuenschten Sprache - lokal zuerst, sonst GitHub."""
    import base64
    name = "CHANGELOG.en.md" if (lang or "").lower().startswith("en") else "CHANGELOG.md"
    local = _local_changelog(name) or _changelog_cache(name)
    if local:
        return {"ok": True, "lang": lang, "file": name, "text": local,
                "url": "https://github.com/%s/blob/%s/%s" % (REPO, BRANCH, name)}

    url = "https://api.github.com/repos/%s/contents/%s?ref=%s" % (REPO, name, BRANCH)
    try:
        data = json.loads(_get(url, timeout).decode("utf-8"))
        text = base64.b64decode(data.get("content", "")).decode("utf-8", "replace")
        _store_changelog(name, text)
        return {"ok": True, "lang": lang, "file": name, "text": text,
                "url": "https://github.com/%s/blob/%s/%s" % (REPO, BRANCH, name)}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": "%s: %s" % (exc.__class__.__name__, exc), "text": ""}


def notes(version: str = "", timeout: int = 10) -> dict:
    """Aenderungen einer Version aus CHANGELOG.md holen (lokal zuerst)."""
    import base64
    text = _local_changelog("CHANGELOG.md") or _changelog_cache("CHANGELOG.md")
    if not text:
        try:
            data = json.loads(_get(CHANGELOG, timeout).decode("utf-8"))
            text = base64.b64decode(data.get("content", "")).decode("utf-8", "replace")
            _store_changelog("CHANGELOG.md", text)
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": "%s: %s" % (exc.__class__.__name__, exc), "text": ""}

    version = (version or installed_version()).lstrip("v")
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and ("[%s]" % version) in line:
            start = i
            break
    if start is None:
        return {"ok": True, "version": version, "text": ""}

    out = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    body = "\n".join(out).strip()
    body = "\n".join(l for l in body.splitlines() if not l.startswith("### "))
    return {"ok": True, "version": version, "text": body}


def apply(target: str = "", timeout: int = 60) -> dict:
    """Neue Version herunterladen und das Paketverzeichnis ersetzen."""
    target = target or package_dir()
    work = tempfile.mkdtemp(prefix="noah-update-")
    try:
        archive = os.path.join(work, "src.tar.gz")
        with open(archive, "wb") as fh:
            fh.write(_get(TARBALL, timeout))

        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(work, filter="data")

        roots = [d for d in os.listdir(work) if os.path.isdir(os.path.join(work, d))]
        if not roots:
            return {"ok": False, "error": "Archiv enthaelt kein Verzeichnis"}
        new_pkg = os.path.join(work, roots[0], "noah")
        if not os.path.isdir(new_pkg):
            return {"ok": False, "error": "Paketordner noah/ fehlt im Archiv"}

        old_version = installed_version()
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup = "%s.bak-%s" % (target.rstrip("/"), stamp)
        if os.path.isdir(target):
            shutil.copytree(target, backup, dirs_exist_ok=True)
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(new_pkg, target)

        for name in os.listdir(target):
            if name == "__pycache__":
                shutil.rmtree(os.path.join(target, name), ignore_errors=True)

        new_version = ""
        try:
            with open(os.path.join(target, "__init__.py"), encoding="utf-8") as fh:
                new_version = _parse_version(fh.read())
        except OSError:
            pass
        write_build(remote_commit(), new_version)
        return {"ok": True, "from": old_version, "to": new_version, "backup": backup}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": "%s: %s" % (exc.__class__.__name__, exc)}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def restart_service() -> dict:
    """Web-Dienst neu starten, damit der neue Code laeuft."""
    candidates = [
        (["systemctl", "restart", "noah-web"], "system"),
        (["systemctl", "--user", "restart", "noah-web"], "user"),
    ]
    for cmd, kind in candidates:
        try:
            done = subprocess.run(cmd, capture_output=True, timeout=30)
            if done.returncode == 0:
                return {"ok": True, "scope": kind}
        except (OSError, subprocess.SubprocessError):
            continue
    return {"ok": False, "error": "kein noah-web-Dienst gefunden"}
