#!/usr/bin/env python3
"""Régénère symbols.js (tables sep.* / icon.* d'OMP) depuis le binaire `omp` installé.

Usage:
    python3 extract-symbols.py [chemin/vers/omp]

Les tables vivent dans le bundle JS du binaire (module `.../status-line/symbols.ts`,
une table par preset : unicode, nerd, ascii). On les retrouve en cherchant les lignes
`"icon.omp": ...` puis en remontant/descendant la série contiguë de paires clé/valeur.
"""
import datetime
import json
import pathlib
import re
import shutil
import subprocess
import sys

PAIR = re.compile(r'^\s*"([a-zA-Z]+\.[A-Za-z0-9]+)":\s*"(.*?)",?$')
PRESETS = ("unicode", "nerd", "ascii")
OUT = pathlib.Path(__file__).with_name("symbols.js")


def resolve_binary(arg):
    """Chemin du binaire : argument, sinon `omp` du PATH (résolu à travers les symlinks)."""
    if arg:
        return arg
    found = shutil.which("omp")
    if not found:
        sys.exit("omp introuvable : passer le chemin du binaire en argument")
    return str(pathlib.Path(found).resolve())


def combine_surrogates(value: str) -> str:
    """\\uDB83\\uDD57 -> un seul caractère (les paires UTF-16 ne sont pas fusionnées
    par unicode_escape)."""
    return value.encode("utf-16-le", "surrogatepass").decode("utf-16-le")


def resolve_version(binary: str) -> tuple[str, str]:
    """Version d'OMP : `<binaire> --version` (« omp v18.1.19 »), sinon le dossier de
    version du chemin (`.../Cellar/omp/18.1.19/bin/omp`). Retourne (version, source)."""
    try:
        out = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=20).stdout
        match = re.search(r"(\d+\.\d+\.\d+)", out)
        if match:
            return match.group(1), "--version"
    except (OSError, subprocess.SubprocessError):
        pass
    match = re.search(r"/(\d+\.\d+\.\d+)/", binary)
    if match:
        return match.group(1), "chemin du binaire"
    return "inconnue", "indéterminée"


def main() -> None:
    binary = resolve_binary(sys.argv[1] if len(sys.argv) > 1 else None)
    dump = subprocess.run(
        ["strings", "-a", binary], capture_output=True, text=True, check=True
    ).stdout.splitlines()

    anchors = [i for i, line in enumerate(dump) if re.match(r'^\s*"icon\.omp":', line)]
    if len(anchors) != len(PRESETS):
        sys.exit(f"attendu {len(PRESETS)} tables de symboles, trouvé {len(anchors)}")

    tables: dict[str, dict[str, str]] = {}
    for preset, anchor in zip(PRESETS, anchors):
        start = anchor
        while start > 0 and PAIR.match(dump[start - 1]):
            start -= 1
        end = anchor
        while end < len(dump) - 1 and PAIR.match(dump[end + 1]):
            end += 1
        raw = {}
        for line in dump[start : end + 1]:
            match = PAIR.match(line)
            if match:
                raw[match.group(1)] = match.group(2).encode().decode("unicode_escape")
        tables[preset] = {
            key: combine_surrogates(value)
            for key, value in raw.items()
            if key.startswith(("sep.", "icon."))
        }

    missing = [k for k in ("sep.dot", "icon.omp", "icon.session") if k not in tables["nerd"]]
    if missing:
        sys.exit(f"clés manquantes dans la table nerd : {missing}")

    version, source = resolve_version(binary)
    build = {
        "version": version,
        "source": source,
        "binary": binary,
        "extractedAt": datetime.date.today().isoformat(),
    }
    header = (
        f"// Tables de symboles extraites d'omp {version} ({source}) — régénérer avec extract-symbols.py\n"
        "// clés = sep.* (séparateurs) et icon.* (glyphes des segments), par preset de symboles.\n"
    )
    OUT.write_text(
        header
        + "window.OMP_BUILD = "
        + json.dumps(build, ensure_ascii=False, indent=1, sort_keys=True)
        + ";\n\n"
        + "window.OMP_SYMBOLS = "
        + json.dumps(tables, ensure_ascii=False, indent=1, sort_keys=True)
        + ";\n"
    )
    print(f"{OUT} écrit — omp {version} ({source}), {len(tables['nerd'])} clés par preset ({', '.join(PRESETS)})")


if __name__ == "__main__":
    main()
