"""Crea in dist/ il pacchetto di rilascio: un solo zip con tutte le skill.

    dist/rtit-skills.zip    le skill e i manifest dei plugin, alla radice dello zip

I manifest stanno alla radice perché Claude (app e claude.ai) carica lo zip come plugin solo se
`.claude-plugin/plugin.json` è al primo livello. Lo zip, o la cartella in cui lo estrai, è insieme:

- un plugin Claude (`.claude-plugin/`): si carica nell'app o si aggiunge a Claude Code come marketplace locale;
- un plugin Codex (`.codex-plugin/`, marketplace in `.agents/plugins/`);
- un plugin Antigravity CLI, `agy` (`plugin.json` e `mcp_config.json` alla radice);
- la raccolta delle skill (`skills/<skill>/SKILL.md`) per chi le carica a mano.

ChatGPT (GPT personalizzati) e l'app Gemini (Gem) non hanno un formato di pacchetto: non c'è nulla
da generare per loro. Lo script è deterministico (stesso input, stessi byte) e non usa la rete.

Uso: python tools/build_release.py [--dist <cartella>]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))  # per importare bump_version anche dai test
import bump_version  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "src" / "rtit" / "templates"
PACKAGE = "rtit-skills"  # nome dello zip; il contenuto sta alla radice, senza cartella intermedia

# File del pacchetto Python da includere nelle skill (per chi le usa senza la CLI)
EXTRA_ASSETS: dict[str, list[Path]] = {
    "rt-bollettino": [TEMPLATES / "bollettino" / n for n in ("generico.docx", "logo-sinistra.png", "logo-destra.png")],
    "rt-primi-passi": [TEMPLATES / "profilo-esempio.yaml"],
    "rt-evento": [TEMPLATES / "pack" / n for n in ("progetto.md", "invitati.md", "spese.md", "evento.md")],
    "rt-archivio": [TEMPLATES / "pack" / "indice-anno.md"],
}

# Manifest e file di contorno (percorsi relativi alla radice del repository)
PLUGIN_FILES = (
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".codex-plugin/mcp.json",
    ".agents/plugins/marketplace.json",
    "assets/logo-rtit.png",
    "assets/logo-rtit.svg",
    "plugin.json",
    "mcp_config.json",
    "GEMINI.md",
    "AGENTS.md",
    ".mcp.json",
    "README.md",
    "LICENSE",
)
# Manifest dei plugin: devono avere un nome (la versione la controlla bump_version)
MANIFESTS = (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "plugin.json")

MCP_URL = "https://app.roundtable.it/mcp/"

# Data fissa nelle voci dello zip: rende il pacchetto riproducibile
ZIP_DATE = (2026, 1, 1, 0, 0, 0)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


class BuildError(Exception):
    """Manca un file o un manifest non è coerente."""


@dataclass
class Skill:
    name: str
    path: Path
    description: str
    files: list[Path] = field(default_factory=list)


def load_skills(root: Path = ROOT) -> list[Skill]:
    skills = []
    for folder in sorted((root / "skills").iterdir()):
        skill_md = folder / "SKILL.md"
        if not skill_md.is_file():
            continue
        m = FRONTMATTER_RE.match(skill_md.read_text(encoding="utf-8"))
        meta = yaml.safe_load(m.group(1)) if m else None
        if not isinstance(meta, dict) or not meta.get("name") or not meta.get("description"):
            raise BuildError(f"{skill_md}: il frontmatter deve avere name e description")
        if meta["name"] != folder.name:
            raise BuildError(f"{skill_md}: name {meta['name']!r} diverso dalla cartella {folder.name!r}")
        files = sorted(p for p in folder.rglob("*") if p.is_file())
        skills.append(
            Skill(name=folder.name, path=folder, description=" ".join(str(meta["description"]).split()), files=files)
        )
    if not skills:
        raise BuildError("Nessuna skill trovata in skills/")
    return skills


def _write_zip(out: Path, entries: dict[str, bytes]) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, entries[name])
    return out


def skill_entries(skill: Skill, prefix: str) -> dict[str, bytes]:
    entries = {f"{prefix}{skill.name}/{p.relative_to(skill.path).as_posix()}": p.read_bytes() for p in skill.files}
    for asset in EXTRA_ASSETS.get(skill.name, []):
        if not asset.is_file():
            raise BuildError(f"Asset mancante per {skill.name}: {asset}")
        entries[f"{prefix}{skill.name}/assets/{asset.name}"] = asset.read_bytes()
    return entries


def package_entries(skills: list[Skill], root: Path = ROOT) -> dict[str, bytes]:
    base = ""
    entries: dict[str, bytes] = {}
    for rel in PLUGIN_FILES:
        src = root / rel
        if not src.is_file():
            raise BuildError(f"File del pacchetto mancante: {rel}")
        entries[base + rel] = src.read_bytes()
    for rel in MANIFESTS:
        if not json.loads(entries[base + rel]).get("name"):
            raise BuildError(f"{rel}: serve name")
    try:
        bump_version.current_version(root)  # stessa versione in tutti i file
    except bump_version.VersionError as exc:
        raise BuildError(str(exc)) from exc
    for skill in skills:
        entries.update(skill_entries(skill, prefix=f"{base}skills/"))
    return entries


def build(dist: Path, root: Path = ROOT) -> dict[str, object]:
    skills = load_skills(root)
    # niente pacchetti di versioni precedenti dello script
    if (dist / "skills").is_dir():
        shutil.rmtree(dist / "skills")
    for old in dist.glob("*.zip") if dist.is_dir() else ():
        old.unlink()
    out = _write_zip(dist / f"{PACKAGE}.zip", package_entries(skills, root))
    return {"skill": [s.name for s in skills], "zip": [out.relative_to(dist).as_posix()]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dist", type=Path, default=ROOT / "dist", help="Cartella di uscita (default: dist/)")
    args = parser.parse_args(argv)
    try:
        report = build(args.dist.resolve())
    except BuildError as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 1
    for name in report["zip"]:
        print(args.dist / name)
    print(f"{len(report['skill'])} skill")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
