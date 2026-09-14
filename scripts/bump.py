#!/usr/bin/env python3
"""Version CalVer du configurateur : bump + synchronisation avec l'interface.

La source de vérité reste le `VERSION` du hub (racine du dépôt). Ce script
l'incrémente et réécrit la constante `APP_VERSION` d'`index.html`, pour que la
version affichée dans l'interface ne puisse pas diverger du dépôt.

Usage:
    python3 bump.py              # incrémente le PATCH (01 si on change de mois)
    python3 bump.py 2026.10.01   # force une version
    python3 bump.py --check      # vérifie l'alignement VERSION <-> index.html
"""
import datetime
import pathlib
import re
import sys

TOOL_DIR = pathlib.Path(__file__).resolve().parent.parent / "Web"
HUB = TOOL_DIR.parent
HUB_VERSION = HUB / "VERSION"
READMES = (HUB / "README.md", HUB / "README_en.md")
INDEX = TOOL_DIR / "index.html"
PATTERN = re.compile(r'(const APP_VERSION = ")([0-9]{4}\.[0-9]{2}\.[0-9]+)(";)')
README_PATTERN = re.compile(r'(Version \*\*)([0-9]{4}\.[0-9]{2}\.[0-9]+)(\*\*)')


def read_hub_version() -> str:
    if not HUB_VERSION.exists():
        sys.exit(f"VERSION introuvable : {HUB_VERSION}")
    return HUB_VERSION.read_text().strip()


def read_app_version() -> str:
    match = PATTERN.search(INDEX.read_text())
    if not match:
        sys.exit("constante APP_VERSION introuvable dans index.html")
    return match.group(2)


def read_readme_versions() -> dict:
    out = {}
    for path in READMES:
        if not path.exists():
            continue
        match = README_PATTERN.search(path.read_text())
        out[path.name] = match.group(2) if match else "(pas de ligne de version)"
    return out


def next_version(current: str) -> str:
    year, month, patch = (int(part) for part in current.split("."))
    today = datetime.date.today()
    if (year, month) != (today.year, today.month):
        return f"{today.year}.{today.month:02d}.01"
    return f"{year}.{month:02d}.{patch + 1}"


def write_versions(version: str) -> None:
    HUB_VERSION.write_text(version + "\n")
    INDEX.write_text(PATTERN.sub(lambda m: m.group(1) + version + m.group(3), INDEX.read_text(), count=1))
    for path in READMES:
        if not path.exists():
            continue
        text = path.read_text()
        if README_PATTERN.search(text):
            path.write_text(README_PATTERN.sub(lambda m: m.group(1) + version + m.group(3), text, count=1))


def main() -> None:
    args = sys.argv[1:]
    hub, app, readmes = read_hub_version(), read_app_version(), read_readme_versions()

    if args and args[0] == "--check":
        mismatched = {name: v for name, v in readmes.items() if v != hub}
        if hub != app or mismatched:
            details = [f"VERSION={hub}", f"index.html={app}"] + [f"{n}={v}" for n, v in mismatched.items()]
            sys.exit("désynchronisé — " + ", ".join(details) + " (lancer bump.py <version>)")
        print(f"aligné : {hub} (VERSION, index.html, {', '.join(readmes)})")
        return

    target = args[0] if args else next_version(hub)
    if not re.fullmatch(r"[0-9]{4}\.[0-9]{2}\.[0-9]+", target):
        sys.exit(f"version invalide : {target} (attendu YYYY.MM.PATCH)")
    write_versions(target)
    print(f"VERSION {hub} -> {target} · index.html {app} -> {target} · "
          + " · ".join(f"{n} {v} -> {target}" for n, v in readmes.items()))


if __name__ == "__main__":
    main()
