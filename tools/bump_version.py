"""Versione del progetto: aggiornarla, controllarla, estrarre le note di rilascio.

La versione sta in sei file e deve essere identica (vedi docs/rilasci.md):
pyproject.toml, src/rtit/__init__.py, .claude-plugin/plugin.json,
.claude-plugin/marketplace.json, .codex-plugin/plugin.json, gemini-extension.json.

Uso:
    python tools/bump_version.py X.Y.Z          aggiorna i file e chiude "Non rilasciato" nel changelog
    python tools/bump_version.py --check        verifica che i file coincidano e che il changelog abbia la sezione
    python tools/bump_version.py --check vX.Y.Z come sopra, e la versione deve coincidere con il tag
    python tools/bump_version.py --note X.Y.Z   stampa la sezione del changelog (testo della release)
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = "CHANGELOG.md"
UNRELEASED = "## [Non rilasciato]"

# file → espressione che cattura il numero di versione (una sola occorrenza per file)
VERSION_FILES: dict[str, str] = {
    "pyproject.toml": r'(?m)^(version = ")([^"]+)(")',
    "src/rtit/__init__.py": r'(?m)^(__version__ = ")([^"]+)(")',  # `rtit --version` e User-Agent
    ".claude-plugin/plugin.json": r'("version": ")([^"]+)(")',
    ".claude-plugin/marketplace.json": r'("version": ")([^"]+)(")',
    ".codex-plugin/plugin.json": r'("version": ")([^"]+)(")',
    "gemini-extension.json": r'("version": ")([^"]+)(")',
}
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


class VersionError(Exception):
    """Versione non valida, file non coerenti o changelog incompleto."""


def parse(version: str) -> tuple[int, int, int]:
    m = SEMVER_RE.match(version)
    if not m:
        raise VersionError(f"Versione non valida: {version!r} (serve X.Y.Z)")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def read_versions(root: Path = ROOT) -> dict[str, str]:
    versions = {}
    for rel, pattern in VERSION_FILES.items():
        path = root / rel
        if not path.is_file():
            raise VersionError(f"File mancante: {rel}")
        found = re.findall(pattern, path.read_text(encoding="utf-8"))
        if len(found) != 1:
            raise VersionError(f"{rel}: attesa una sola riga di versione, trovate {len(found)}")
        versions[rel] = found[0][1]
    return versions


def current_version(root: Path = ROOT) -> str:
    versions = read_versions(root)
    if len(set(versions.values())) != 1:
        raise VersionError(f"Versioni diverse nei file: {versions}")
    return next(iter(versions.values()))


def release_notes(version: str, root: Path = ROOT) -> str:
    """Testo della sezione `## [version]` del changelog, senza il titolo."""
    path = root / CHANGELOG
    if not path.is_file():
        raise VersionError(f"File mancante: {CHANGELOG}")
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"(?m)^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.DOTALL)
    if not m:
        raise VersionError(f"{CHANGELOG}: manca la sezione [{version}]")
    notes = m.group(1).strip()
    if not notes:
        raise VersionError(f"{CHANGELOG}: la sezione [{version}] è vuota")
    return notes + "\n"


def check(tag: str | None = None, root: Path = ROOT) -> str:
    version = current_version(root)
    if tag is not None and tag.removeprefix("v") != version:
        raise VersionError(f"Il tag {tag} non coincide con la versione {version} dei file")
    release_notes(version, root)
    return version


def bump(new: str, root: Path = ROOT, today: date | None = None) -> str:
    old = current_version(root)
    if parse(new) <= parse(old):
        raise VersionError(f"La nuova versione {new} deve essere maggiore di {old}")
    path = root / CHANGELOG
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if text.count(UNRELEASED) != 1:
        raise VersionError(f'{CHANGELOG}: serve una sola sezione "{UNRELEASED}"')
    head, rest = text.split(UNRELEASED, 1)
    m = re.search(r"(?m)^## \[", rest)
    pending, older = (rest[: m.start()], rest[m.start() :]) if m else (rest, "")
    if not pending.strip():
        raise VersionError(f'{CHANGELOG}: la sezione "{UNRELEASED}" è vuota, non c\'è nulla da rilasciare')
    day = (today or date.today()).isoformat()
    path.write_text(
        f"{head}{UNRELEASED}\n\n## [{new}] - {day}\n\n{pending.strip()}\n\n{older}",
        encoding="utf-8",
        newline="\n",
    )
    for rel, pattern in VERSION_FILES.items():
        file = root / rel
        file.write_text(
            re.sub(pattern, rf"\g<1>{new}\g<3>", file.read_text(encoding="utf-8")), encoding="utf-8", newline="\n"
        )
    return new


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("versione", nargs="?", help="Nuova versione X.Y.Z")
    parser.add_argument("--check", nargs="?", const="", metavar="TAG", help="Verifica i file (e il tag, se indicato)")
    parser.add_argument("--note", metavar="X.Y.Z", help="Stampa la sezione del changelog di quella versione")
    args = parser.parse_args(argv)
    try:
        if args.note:
            sys.stdout.write(release_notes(args.note.removeprefix("v")))
        elif args.check is not None:
            print(f"Versione {check(args.check or None)}: file e changelog coerenti")
        elif args.versione:
            print(f"Versione portata a {bump(args.versione)}: rileggi {CHANGELOG} prima del commit")
        else:
            parser.error("indica una versione, --check o --note")
    except VersionError as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
