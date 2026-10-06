"""Blocca dati personali e riferimenti privati prima che finiscano nel repository pubblico.

Controlla testi e contenuti di DOCX/ZIP. Termini privati aggiuntivi (nomi, sigle di tavole,
ID di calendari) si passano con la variabile RTIT_LEAK_DENYLIST, separati da virgole: la lista
non va mai scritta nel repository.

Uso: python tools/check_leaks.py [percorso ...]
"""

from __future__ import annotations

import os
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "dist", "build"}
SKIP_FILES = {"LICENSE", "check_leaks.py"}
TEXT_EXT = {".md", ".py", ".yaml", ".yml", ".json", ".toml", ".txt", ".ics", ".cfg", ".ini", ""}
BINARY_ZIP_EXT = {".docx", ".xlsx", ".pptx", ".zip"}

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # Telefoni italiani reali (consentiti solo i fittizi +39 000 …)
    ("telefono", re.compile(r"\+39[\s.]?(?!0{3})\d{3}[\s.]?\d{2,4}[\s.]?\d{2,4}(?:[\s.]?\d{1,3})?")),
    ("cellulare", re.compile(r"(?<![\d.])3\d{2}[\s.]?\d{3}[\s.]?\d{4}(?!\d)")),
    # Email di persone (consentiti domini istituzionali e di esempio)
    ("email", re.compile(r"[\w.+-]+@(?!roundtable\.it\b|example\.\w+|esempio\.\w+|anthropic\.com)[\w-]+\.[\w.-]+")),
    ("percorso utente", re.compile(r"[A-Z]:\\Users\\(?!<utente>)[\w.-]+", re.I)),
    ("unità Drive", re.compile(r"\bG:\\\\?(?:My Drive|Il mio Drive)", re.I)),
    ("calendario Google", re.compile(r"[\w%]+(?:@|%40)group\.calendar\.google\.com")),
    ("modulo Google", re.compile(r"forms\.gle/\w+")),
]


def denylist() -> list[str]:
    raw = os.environ.get("RTIT_LEAK_DENYLIST", "")
    return [t.strip().lower() for t in raw.split(",") if t.strip()]


def iter_files(paths: list[Path]):
    for base in paths:
        if base.is_file():
            yield base
            continue
        for p in base.rglob("*"):
            if p.is_file() and not (set(p.relative_to(base).parts) & SKIP_DIRS) and p.name not in SKIP_FILES:
                yield p


def texts_of(path: Path):
    ext = path.suffix.lower()
    if ext in BINARY_ZIP_EXT:
        try:
            with zipfile.ZipFile(path) as z:
                for name in z.namelist():
                    if name.endswith((".xml", ".rels", ".txt", ".md", ".json")):
                        yield f"{path}!{name}", z.read(name).decode("utf-8", errors="replace")
        except zipfile.BadZipFile:
            yield str(path), ""
    elif ext in TEXT_EXT:
        yield str(path), path.read_text(encoding="utf-8", errors="replace")


def scan(paths: list[Path]) -> list[str]:
    deny = denylist()
    findings: list[str] = []
    for f in iter_files(paths):
        for label, text in texts_of(f):
            plain = re.sub(r"<[^>]+>", "", text) if "!" in label else text
            for kind, rx in PATTERNS:
                for m in rx.finditer(plain):
                    findings.append(f"{label}: {kind}: {m.group(0)!r}")
            low = plain.lower()
            for term in deny:
                if term in low:
                    findings.append(f"{label}: termine privato: {term!r}")
    return findings


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] or [ROOT]
    findings = scan(paths)
    for line in findings:
        print(line)
    if findings:
        print(f"\n{len(findings)} possibili dati personali o riferimenti privati.", file=sys.stderr)
        return 1
    print("Nessuna fuga di dati trovata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
