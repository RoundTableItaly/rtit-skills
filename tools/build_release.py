"""Crea in dist/ i pacchetti di rilascio per Claude, ChatGPT e Gemini.

    dist/skills/<skill>.zip       una skill per zip, da caricare su Claude.ai / Claude Desktop
    dist/rtit-skills-tutte.zip    tutte le skill insieme, una cartella per skill
    dist/rtit-claude-plugin.zip   plugin Claude Code installabile da file
    dist/rtit-chatgpt.zip         GPT personalizzato: istruzioni + file di conoscenza + guida
    dist/rtit-gemini.zip          Gem: istruzioni + file di conoscenza (accorpati) + guida

Le istruzioni per ChatGPT e Gemini si generano dai frontmatter delle skill. Lo script è
deterministico (stesso input, stessi byte), non usa la rete e si ferma se un limite non è rispettato.

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

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "src" / "rtit" / "templates"

# File del pacchetto Python da includere negli zip delle skill (per chi le usa senza la CLI)
EXTRA_ASSETS: dict[str, list[Path]] = {
    "rt-bollettino": [TEMPLATES / "bollettino" / n for n in ("generico.docx", "logo-sinistra.png", "logo-destra.png")],
    "rt-primi-passi": [TEMPLATES / "profilo-esempio.yaml"],
    "rt-evento": [TEMPLATES / "pack" / n for n in ("progetto.md", "invitati.md", "spese.md", "evento.md")],
    "rt-archivio": [TEMPLATES / "pack" / "indice-anno.md"],
}

# Contenuto del plugin Claude Code (percorsi relativi alla radice del repository)
PLUGIN_FILES = (
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".mcp.json",
    "README.md",
    "LICENSE",
)

MCP_URL = "https://app.roundtable.it/mcp/"
RELEASES_URL = "https://github.com/RoundTableItaly/rtit-skills/releases"

# Limiti delle piattaforme (verificati a ottobre 2026; se cambiano, aggiornali qui)
MAX_ISTRUZIONI = 8000  # caratteri delle istruzioni di un GPT personalizzato (usiamo lo stesso tetto per i Gem)
MAX_FILE_CHATGPT = 20  # file di conoscenza di un GPT
MAX_FILE_GEMINI = 10  # file allegabili a un Gem
MAX_FILE_CONOSCENZA = 2_000_000  # byte per file di conoscenza (margine ampio sotto i limiti delle piattaforme)

# Accorpamenti tematici usati solo quando i file di conoscenza superano il limite della piattaforma
GRUPPI_TEMATICI: tuple[tuple[str, ...], ...] = (
    ("rt-primi-passi", "rt-cosa-fare"),
    ("rt-evento", "rt-bollettino"),
    ("rt-calendario", "rt-app-rtit"),
    ("rt-archivio", "rt-direttivo"),
    ("rt-comunicazione", "rt-logo"),
    ("rt-presidente", "rt-conoscenza"),
)

# Data fissa nelle voci degli zip: rende i pacchetti riproducibili
ZIP_DATE = (2026, 1, 1, 0, 0, 0)
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt"}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


class BuildError(Exception):
    """Un limite non è rispettato o manca un file."""


@dataclass
class Skill:
    name: str
    path: Path
    description: str
    body: str
    files: list[Path] = field(default_factory=list)


# --- lettura delle skill ---------------------------------------------------------------


def load_skills(root: Path = ROOT) -> list[Skill]:
    skills = []
    for folder in sorted((root / "skills").iterdir()):
        skill_md = folder / "SKILL.md"
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        meta = yaml.safe_load(m.group(1)) if m else None
        if not isinstance(meta, dict) or not meta.get("name") or not meta.get("description"):
            raise BuildError(f"{skill_md}: il frontmatter deve avere name e description")
        if meta["name"] != folder.name:
            raise BuildError(f"{skill_md}: name {meta['name']!r} diverso dalla cartella {folder.name!r}")
        files = sorted(p for p in folder.rglob("*") if p.is_file())
        skills.append(
            Skill(
                name=folder.name,
                path=folder,
                description=" ".join(str(meta["description"]).split()),
                body=text[m.end() :].strip() + "\n",
                files=files,
            )
        )
    if not skills:
        raise BuildError("Nessuna skill trovata in skills/")
    return skills


# --- zip riproducibili ---------------------------------------------------------------------


def _write_zip(out: Path, entries: dict[str, bytes]) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, entries[name])
    return out


def skill_entries(skill: Skill, prefix: str = "") -> dict[str, bytes]:
    entries = {f"{prefix}{skill.name}/{p.relative_to(skill.path).as_posix()}": p.read_bytes() for p in skill.files}
    for asset in EXTRA_ASSETS.get(skill.name, []):
        if not asset.is_file():
            raise BuildError(f"Asset mancante per {skill.name}: {asset}")
        entries[f"{prefix}{skill.name}/assets/{asset.name}"] = asset.read_bytes()
    return entries


def plugin_entries(skills: list[Skill], root: Path = ROOT) -> dict[str, bytes]:
    base = "rtit-claude-plugin/"
    entries: dict[str, bytes] = {}
    for rel in PLUGIN_FILES:
        src = root / rel
        if not src.is_file():
            raise BuildError(f"File del plugin mancante: {rel}")
        entries[base + rel] = src.read_bytes()
    for skill in skills:
        for p in skill.files:
            entries[f"{base}skills/{skill.name}/{p.relative_to(skill.path).as_posix()}"] = p.read_bytes()
    plugin = json.loads(entries[base + ".claude-plugin/plugin.json"])
    if not plugin.get("name") or not plugin.get("version"):
        raise BuildError("plugin.json: servono name e version")
    return entries


# --- conoscenza per ChatGPT e Gemini ----------------------------------------------------------


def knowledge_text(skill: Skill) -> str:
    """SKILL.md + references (+ modelli testuali) in un unico markdown con intestazioni chiare."""
    parts = [
        f"# Skill {skill.name}",
        "",
        f"Quando usarla: {skill.description}",
        "",
        "I file `references/…` citati nelle istruzioni sono riportati più sotto, in questo stesso file.",
        "I comandi `rtit …` e i percorsi locali valgono solo con un terminale: qui segui il percorso in chat.",
        "",
        f"## {skill.name} — istruzioni (SKILL.md)",
        "",
        skill.body.strip(),
        "",
    ]
    extra = [p for p in skill.files if p.name != "SKILL.md" and p.suffix.lower() in TEXT_SUFFIXES]
    extra += [a for a in EXTRA_ASSETS.get(skill.name, []) if a.suffix.lower() in TEXT_SUFFIXES]
    for p in extra:
        rel = p.relative_to(skill.path).as_posix() if p.is_relative_to(skill.path) else f"assets/{p.name}"
        content = p.read_text(encoding="utf-8").strip()
        parts += [f"## {skill.name} — file {rel}", ""]
        if p.suffix.lower() == ".md" and p.is_relative_to(skill.path):
            parts += [content, ""]
        else:  # modelli e file di dati: tra recinti, così le intestazioni non si confondono con le istruzioni
            lang = {".md": "markdown", ".json": "json"}.get(p.suffix.lower(), "yaml")
            parts += [f"````{lang}", content, "````", ""]
    return "\n".join(parts).rstrip() + "\n"


def group_skills(skills: list[Skill], limit: int) -> list[list[Skill]]:
    """Un file per skill; oltre il limite accorpa per tema (un gruppo alla volta), poi i due file più piccoli."""
    groups: list[list[Skill]] = [[s] for s in skills]
    for tema in GRUPPI_TEMATICI:
        if len(groups) <= limit:
            break
        members = [g for g in groups if len(g) == 1 and g[0].name in tema]
        if len(members) > 1:
            groups = [g for g in groups if g not in members] + [[g[0] for g in members]]
    sizes = {s.name: len(knowledge_text(s)) for s in skills}
    while len(groups) > limit:
        groups.sort(key=lambda g: (sum(sizes[s.name] for s in g), min(s.name for s in g)))
        groups = [groups[0] + groups[1]] + groups[2:]
    groups = [sorted(g, key=lambda s: s.name) for g in groups]
    return sorted(groups, key=lambda g: g[0].name)


def group_filename(group: list[Skill]) -> str:
    return "_".join(s.name for s in group) + ".md"


def _shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[: max(limit - 1, 0)].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "…"


def instructions(skills: list[Skill], groups: list[list[Skill]], piattaforma: str) -> str:
    """Istruzioni del GPT o del Gem, generate dai frontmatter e tenute sotto MAX_ISTRUZIONI caratteri."""
    file_of = {s.name: group_filename(g) for g in groups for s in g}
    if piattaforma == "chatgpt":
        app = (
            "- Dati dell'App RTIT (eventi di altre tavole, sovrapposizioni di date, statistiche): usa il connettore "
            "MCP «App Round Table Italia» se è collegato; altrimenti rimanda a https://app.roundtable.it."
        )
    else:
        app = (
            "- Dati dell'App RTIT (eventi di altre tavole, sovrapposizioni di date, statistiche): qui non hai un "
            "connettore; chiedi all'utente di controllare su https://app.roundtable.it e incollarti i dati."
        )
    head = [
        "Sei l'assistente per chi fa parte di un direttivo di Round Table Italia (tavola, zona o nazionale): "
        "presidenti, segretari, tesorieri, P.R.O. (responsabili comunicazione) e consiglieri. "
        "Rispondi in italiano semplice, dai del tu, fai una o due domande alla volta.",
        "",
        "Come lavori:",
        "- Prima di rispondere scegli la skill pertinente nell'elenco qui sotto e leggi il suo file di conoscenza "
        "(cartella dei file caricati). Segui le istruzioni di quel file; se servono più skill, leggile tutte.",
        "- Se manca il profilo della tavola (nome, zona, direttivo, firme), parti dalla skill rt-primi-passi.",
        "- I comandi `rtit …` citati nei file richiedono un terminale: qui non funzionano. Usa il percorso «solo chat» "
        "e prepara testi, tabelle e file da scaricare.",
        app,
        "",
        "Regole:",
        "- Non pubblicare, inviare o modificare nulla senza conferma esplicita: mostra prima un'anteprima.",
        "- Non inventare date, importi, link, nomi o regole statutarie: chiedi, oppure dì che il dato va verificato.",
        "- In caso di dubbio prevalgono i documenti ufficiali di Round Table Italia e le indicazioni del Comitato "
        "Nazionale.",
        "- Privacy: chiedi solo i dati che servono; i dati sanitari (allergie, intolleranze) sono minimi e non si "
        "inoltrano; non riportare dati di soci in testi pubblici senza conferma; il token di Tabler World e "
        "l'indirizzo iCal segreto non vanno mai scritti in chat.",
        "- L'anno sociale inizia la domenica dopo l'AGM (di solito il primo sabato di giugno) e si scrive AAAA-AAAA.",
        "",
        "Skill (nome — file di conoscenza — quando usarla):",
    ]
    fixed = "\n".join(head)
    prefixes = [f"- {s.name} — {file_of[s.name]} — " for s in skills]
    budget = MAX_ISTRUZIONI - len(fixed) - 2 - sum(len(p) + 1 for p in prefixes)
    # tetto comune alle descrizioni: il più alto che fa stare tutto nel limite (le brevi restano intere)
    lengths = [len(s.description) for s in skills]
    cap = max(lengths)
    while cap > 0 and sum(min(n, cap) for n in lengths) > budget:
        cap -= 10
    if cap <= 40:
        raise BuildError(f"Istruzioni {piattaforma}: troppe skill per il limite di {MAX_ISTRUZIONI} caratteri")
    lines = [p + _shorten(s.description, cap) for p, s in zip(prefixes, skills, strict=True)]
    text = fixed + "\n" + "\n".join(lines) + "\n"
    if len(text) > MAX_ISTRUZIONI:
        raise BuildError(f"Istruzioni {piattaforma}: {len(text)} caratteri, oltre il limite di {MAX_ISTRUZIONI}")
    return text


def _readme_chatgpt(groups: list[list[Skill]]) -> str:
    return f"""# Round Table Italia — GPT personalizzato (ChatGPT)

ChatGPT non carica le skill come file: si crea un **GPT personalizzato** con le istruzioni e i file di
conoscenza di questo pacchetto. Serve un piano che permetta di creare GPT.

## Creare il GPT

1. Estrai questo zip in una cartella.
2. In ChatGPT apri **Esplora GPT → Crea** e passa alla scheda **Configura**.
3. **Nome**: per esempio "Assistente direttivo RT".
   **Descrizione**: "Aiuta il direttivo di una tavola Round Table Italia".
4. **Istruzioni**: incolla tutto il contenuto di `ISTRUZIONI.txt` (resta sotto gli {MAX_ISTRUZIONI} caratteri ammessi).
5. **Conoscenza**: carica tutti i file della cartella `conoscenza/` ({len(groups)} file).
6. **Funzionalità**: attiva **Interprete di codice e analisi dei dati** (serve per tabelle, conti e file Word).
7. Salva il GPT con visibilità **Solo io** oppure **Chiunque abbia il link**, se lo condividi col direttivo.

## Collegare l'App Round Table Italia (connettore MCP)

Dove il piano lo consente (connettori personalizzati o modalità sviluppatore), aggiungi un connettore MCP:

- URL: `{MCP_URL}`
- autenticazione: nessuna
- guida ufficiale: https://app.roundtable.it/ai-agents

Il connettore dà eventi di tavole e zone, sovrapposizioni di date e statistiche. Senza connettore il GPT
ti chiederà di controllare tu sull'App.

## Il profilo della tavola

Alla prima conversazione scrivi: *"Configura la mia tavola"*. Il GPT prepara il profilo (tavola, zona,
direttivo e firme): salvalo e incollalo all'inizio delle conversazioni successive, oppure caricalo come file
di conoscenza in più. Il profilo contiene nomi e telefoni del direttivo: condividi il GPT solo col direttivo.

## Cosa non funziona in ChatGPT

- La CLI `rtit` (comandi da terminale) non funziona: il GPT prepara testi, tabelle e file da scaricare.
- Il GPT non scrive direttamente nell'archivio condiviso della tavola: i file si salvano a mano.
- Il modello Word del bollettino non è incluso: per il Word usa Claude oppure compila a mano il modello della
  tavola con il testo preparato dal GPT.

Aggiornamenti: {RELEASES_URL}
"""


def _readme_gemini(groups: list[list[Skill]]) -> str:
    return f"""# Round Table Italia — Gem (Gemini)

Gemini non carica le skill come file: si crea un **Gem** con le istruzioni e i file di conoscenza di questo
pacchetto. I Gem accettano pochi file, quindi le skill sono accorpate in {len(groups)} file.

## Creare il Gem

1. Estrai questo zip in una cartella.
2. In Gemini (https://gemini.google.com) apri **Gem manager → Nuovo Gem**.
3. **Nome**: per esempio "Assistente direttivo RT".
4. **Istruzioni**: incolla tutto il contenuto di `ISTRUZIONI.txt`.
5. **Conoscenza**: carica tutti i file della cartella `conoscenza/`.
6. Salva. Puoi condividere il Gem con il direttivo, se il tuo account lo consente.

## Il profilo della tavola

Alla prima conversazione scrivi: *"Configura la mia tavola"*. Il Gem prepara il profilo (tavola, zona,
direttivo e firme): salvalo e incollalo all'inizio delle conversazioni successive. Contiene nomi e telefoni
del direttivo: condividi il Gem solo col direttivo.

## Cosa manca rispetto a Claude

- **Niente connettore MCP** nell'app Gemini: i dati dell'App Round Table Italia (eventi, sovrapposizioni di
  date, statistiche) vanno controllati a mano su https://app.roundtable.it.
  Il server MCP (`{MCP_URL}`) funziona invece in **Gemini CLI**, installando il repository come estensione:
  `gemini extensions install https://github.com/RoundTableItaly/rtit-skills`.
- La CLI `rtit` (comandi da terminale) non funziona nel Gem: prepara testi e tabelle da copiare.
- Il Gem non scrive nell'archivio condiviso della tavola e non genera il Word del bollettino dal modello.

Aggiornamenti: {RELEASES_URL}
"""


def chat_entries(skills: list[Skill], piattaforma: str) -> tuple[dict[str, bytes], dict[str, object]]:
    limit = MAX_FILE_CHATGPT if piattaforma == "chatgpt" else MAX_FILE_GEMINI
    groups = group_skills(skills, limit)
    base = f"rtit-{piattaforma}/"
    entries: dict[str, bytes] = {}
    for g in groups:
        text = "\n\n".join(knowledge_text(s).rstrip() for s in g) + "\n"
        data = text.encode("utf-8")
        if len(data) > MAX_FILE_CONOSCENZA:
            raise BuildError(f"{piattaforma}: {group_filename(g)} supera {MAX_FILE_CONOSCENZA} byte")
        entries[f"{base}conoscenza/{group_filename(g)}"] = data
    if len(groups) > limit:
        raise BuildError(f"{piattaforma}: {len(groups)} file di conoscenza, oltre il limite di {limit}")
    istruzioni = instructions(skills, groups, piattaforma)
    entries[f"{base}ISTRUZIONI.txt"] = istruzioni.encode("utf-8")
    readme = _readme_chatgpt(groups) if piattaforma == "chatgpt" else _readme_gemini(groups)
    entries[f"{base}LEGGIMI.md"] = readme.encode("utf-8")
    return entries, {"file_conoscenza": len(groups), "caratteri_istruzioni": len(istruzioni)}


# --- build ------------------------------------------------------------------------------------


def build(dist: Path, root: Path = ROOT) -> dict[str, object]:
    skills = load_skills(root)
    if (dist / "skills").is_dir():
        shutil.rmtree(dist / "skills")  # niente zip di skill rinominate o rimosse
    report: dict[str, object] = {"skill": [s.name for s in skills], "zip": []}
    zips: list[Path] = []
    tutte: dict[str, bytes] = {}
    for skill in skills:
        entries = skill_entries(skill)
        zips.append(_write_zip(dist / "skills" / f"{skill.name}.zip", entries))
        tutte.update(skill_entries(skill, prefix="rtit-skills/"))
    zips.append(_write_zip(dist / "rtit-skills-tutte.zip", tutte))
    zips.append(_write_zip(dist / "rtit-claude-plugin.zip", plugin_entries(skills, root)))
    for piattaforma in ("chatgpt", "gemini"):
        entries, info = chat_entries(skills, piattaforma)
        zips.append(_write_zip(dist / f"rtit-{piattaforma}.zip", entries))
        report[piattaforma] = info
    report["zip"] = [p.relative_to(dist).as_posix() for p in zips]
    return report


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
    for piattaforma in ("chatgpt", "gemini"):
        info = report[piattaforma]
        print(f"{piattaforma}: {info['file_conoscenza']} file, istruzioni {info['caratteri_istruzioni']} caratteri")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
