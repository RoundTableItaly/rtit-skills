"""Archivio condiviso della tavola, zona o nazionale.

È una cartella su un qualsiasi cloud (Google Drive, OneDrive, SharePoint, Dropbox, Nextcloud…) sincronizzata
sul PC, oppure una cartella normale. Tutto il lavoro sta lì, così il direttivo lo condivide e il mandato
successivo lo ritrova. Struttura di default (configurabile in `archivio.*` del profilo):

    <archivio.percorso>/
        rtit-profilo.yaml · rtit-profilo.decisioni.yaml
        Documenti legali/                            (Statuto e regolamenti, Fiscale e PEC, Banca, Loghi e modelli)
        Anni sociali/AAAA-AAAA/
            _Indice AAAA-AAAA.md                     (indice dell'anno: eventi, bollettini, verbali…)
            Eventi/AAAA-MM-GG Nome/
                AAAA-MM-GG Nome.md                   (nota evento, `tipo: evento`)
                progetto.md · invitati.md · spese.md (pack, eventi conviviali)
                Bollettini/                          (nota .md + DOCX + PDF del bollettino)
                Form/ · Altri documenti/             (moduli; ricevute, foto, preventivi…)
            Direttivo/ · Tesoreria/ · Comunicazione/

`archivio.link: wikilink` produce link `[[...]]` (Obsidian); il default `markdown` produce link relativi.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from .markdown import extract_section, open_checkboxes, parse_frontmatter
from .profile import CARTELLE_ANNO, anno_sociale, resolve_path, title_similarity, today_in_tz

EVENT_DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(.+)$")
PACK_FILES = ("progetto.md", "invitati.md", "spese.md")
TEMPLATES_DIR = Path(__file__).parent / "templates" / "pack"

REQUIRED_PROGETTO_SECTIONS = ("Dati evento", "Descrizione", "Checklist operativa", "TODO", "Link")
REQUIRED_SPESE_SECTIONS = ("Parametri", "Voci di spesa", "Riepilogo")


class ArchiveError(Exception):
    """Archivio non configurato o non raggiungibile."""


@dataclass
class Event:
    date: str
    title: str
    folder: str
    note_path: str
    note_rel: str
    anno_sociale: str
    tablerworld_id: str | None = None
    frontmatter: dict[str, Any] = field(default_factory=dict)

    @property
    def folder_name(self) -> str:
        return Path(self.folder).name

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def archive_root(profile: dict[str, Any], override: str | Path | None = None) -> Path:
    if override:
        return Path(override).expanduser().resolve()
    root = resolve_path(profile, (profile.get("archivio") or {}).get("percorso"))
    if root is None:
        raise ArchiveError(
            "Nessun archivio configurato: indica in archivio.percorso la cartella condivisa della tavola "
            "(Drive, OneDrive, Dropbox… sincronizzata sul PC), oppure lavora tramite connettore o in chat."
        )
    if not root.is_dir():
        raise ArchiveError(
            f"Cartella dell'archivio non trovata: {root}. Il client di sincronizzazione del cloud è avviato?"
        )
    return root


def has_archive(profile: dict[str, Any]) -> bool:
    return bool((profile.get("archivio") or {}).get("percorso"))


def year_dir(profile: dict[str, Any], key: str, anno: str, root: Path | None = None) -> Path:
    """Cartella `archivio.<key>` (eventi, direttivo, tesoreria, comunicazione) per un anno sociale."""
    base = root or archive_root(profile)
    return base / profile["archivio"][key].format(anno=anno)


def eventi_dir(profile: dict[str, Any], anno: str, root: Path | None = None) -> Path:
    return year_dir(profile, "eventi", anno, root)


def find_similar_folders(
    profile: dict[str, Any], d: date, title: str, root: Path | None = None, threshold: float = 0.45
) -> list[dict[str, Any]]:
    """Cartelle evento con la stessa data o un titolo simile (per non creare doppioni)."""
    parent = eventi_dir(profile, anno_sociale(d, profile), root)
    if not parent.is_dir():
        return []
    target = f"{d.isoformat()} {title}"
    out = []
    for p in sorted(parent.iterdir()):
        m = EVENT_DIR_RE.match(p.name)
        if not p.is_dir() or not m or p.name == target:
            continue
        score = title_similarity(title, m.group(2))
        reasons = (["same_date"] if m.group(1) == d.isoformat() else []) + (
            ["fuzzy_title"] if score >= threshold else []
        )
        if reasons:
            out.append({"folder_name": p.name, "path": str(p), "reason": "+".join(reasons), "score": round(score, 3)})
    out.sort(key=lambda r: (-("same_date" in r["reason"]), -r["score"]))
    return out


def same_date_duplicates(profile: dict[str, Any], root: Path | None = None) -> list[list[str]]:
    """Gruppi di cartelle evento con la stessa data (possibili doppioni da riunire)."""
    base = root or archive_root(profile)
    pattern = profile["archivio"]["eventi"].replace("{anno}", "*").rstrip("/") + "/*"
    by_date: dict[str, list[str]] = {}
    for p in base.glob(pattern):
        m = EVENT_DIR_RE.match(p.name)
        if p.is_dir() and m:
            by_date.setdefault(m.group(1), []).append(p.name)
    return [sorted(v) for _, v in sorted(by_date.items()) if len(v) > 1]


def _plan_dir(path: Path, planned: list[dict[str, Any]], apply: bool) -> None:
    planned.append({"cartella": str(path), "esiste": path.is_dir()})
    if apply:
        path.mkdir(parents=True, exist_ok=True)


def ensure_year_structure(profile: dict[str, Any], anno: str, root: Path, apply: bool = False) -> dict[str, Any]:
    """Crea (o mostra) `Documenti legali/`, le cartelle standard dell'anno sociale e la nota indice.

    Non sovrascrive nulla: crea solo ciò che manca.
    """
    arch = profile["archivio"]
    planned: list[dict[str, Any]] = []
    legali_rel = arch.get("documenti_legali")
    if legali_rel:
        legali = root / legali_rel
        _plan_dir(legali, planned, apply)
        for name in arch.get("cartelle_legali") or []:
            _plan_dir(legali / name, planned, apply)
    if arch.get("anni"):
        _plan_dir(root / arch["anni"].format(anno=anno), planned, apply)
    for key in CARTELLE_ANNO:
        if arch.get(key):
            _plan_dir(year_dir(profile, key, anno, root), planned, apply)
    indice_rel = arch.get("indice_anno")
    if indice_rel:
        indice = root / indice_rel.format(anno=anno)
        planned.append({"file": str(indice), "esiste": indice.is_file()})
        if apply and not indice.exists():
            indice.parent.mkdir(parents=True, exist_ok=True)
            indice.write_text(render_template("indice-anno.md", {"anno": anno}), encoding="utf-8")
    return {"anno": anno, "applica": apply, "elementi": planned}


def event_folder_for(profile: dict[str, Any], d: date, title: str, root: Path | None = None) -> Path:
    return eventi_dir(profile, anno_sociale(d, profile), root) / f"{d.isoformat()} {title}"


def _anno_from_meta(meta: dict[str, Any]) -> str | None:
    """`anno_sociale` dal frontmatter; `anno_associativo` è il nome usato dalle note meno recenti."""
    value = meta.get("anno_sociale") or meta.get("anno_associativo")
    return str(value) if value else None


def _event_from_note(profile: dict[str, Any], note: Path, root: Path) -> Event | None:
    folder_name = note.parent.name
    m = EVENT_DIR_RE.match(folder_name)
    if not m or note.name in PACK_FILES:
        return None
    meta, _ = parse_frontmatter(note.read_text(encoding="utf-8", errors="replace"))
    tipo = meta.get("tipo")
    if tipo and tipo != "evento":
        return None
    if tipo != "evento" and note.stem != folder_name:
        return None
    ev_date = str(meta.get("data") or m.group(1))
    try:
        anno = str(_anno_from_meta(meta) or anno_sociale(date.fromisoformat(ev_date), profile))
    except ValueError:
        return None
    return Event(
        date=ev_date,
        title=m.group(2),
        folder=str(note.parent),
        note_path=str(note),
        note_rel=note.relative_to(root).as_posix(),
        anno_sociale=anno,
        tablerworld_id=str(meta["tablerworld_id"]) if meta.get("tablerworld_id") else None,
        frontmatter=meta,
    )


def scan_events(profile: dict[str, Any], root: Path | None = None) -> list[Event]:
    """Tutte le note evento dell'archivio (una per cartella, preferendo `tipo: evento`)."""
    base = root or archive_root(profile)
    if not base.is_dir():
        return []
    pattern = profile["archivio"]["eventi"].replace("{anno}", "*").rstrip("/") + "/*/*.md"
    by_folder: dict[str, Event] = {}
    for note in base.glob(pattern):
        ev = _event_from_note(profile, note, base)
        if ev is None:
            continue
        prev = by_folder.get(ev.folder)
        if prev is None or (ev.frontmatter.get("tipo") == "evento" and prev.frontmatter.get("tipo") != "evento"):
            by_folder[ev.folder] = ev
    return sorted(by_folder.values(), key=lambda e: (e.date, e.title.lower()))


def future_events(profile: dict[str, Any], root: Path | None = None, on_or_after: date | None = None) -> list[Event]:
    today = on_or_after or today_in_tz(profile)
    out = []
    for ev in scan_events(profile, root):
        try:
            if date.fromisoformat(ev.date) >= today:
                out.append(ev)
        except ValueError:
            continue
    return out


def event_from_folder(profile: dict[str, Any], folder: Path, root: Path) -> Event:
    m = EVENT_DIR_RE.match(folder.name)
    if not m:
        raise ArchiveError("Il nome della cartella deve essere 'AAAA-MM-GG Titolo'.")
    note = folder / f"{folder.name}.md"
    meta, _ = parse_frontmatter(note.read_text(encoding="utf-8")) if note.is_file() else ({}, "")
    anno = str(_anno_from_meta(meta) or anno_sociale(date.fromisoformat(m.group(1)), profile))
    try:
        rel = note.relative_to(root).as_posix()
    except ValueError:
        rel = note.name
    return Event(
        date=str(meta.get("data") or m.group(1)),
        title=m.group(2),
        folder=str(folder),
        note_path=str(note),
        note_rel=rel,
        anno_sociale=anno,
        tablerworld_id=str(meta["tablerworld_id"]) if meta.get("tablerworld_id") else None,
        frontmatter=meta,
    )


# --- link -------------------------------------------------------------------------


def make_link(profile: dict[str, Any], target: Path, display: str, from_dir: Path, root: Path) -> str:
    """Wikilink da root (Obsidian) oppure link markdown relativo (cartella)."""
    if profile["archivio"]["link"] == "wikilink":
        rel = target.relative_to(root).as_posix()
        return f"[[{rel.removesuffix('.md')}|{display}]]"
    import os

    rel = Path(os.path.relpath(target, from_dir)).as_posix()
    return f"[{display}](<{rel}>)"


def make_ref(profile: dict[str, Any], target: Path, display: str, root: Path) -> str:
    """Riferimento da mettere nel frontmatter (stringa YAML tra virgolette)."""
    if profile["archivio"]["link"] == "wikilink":
        rel = target.relative_to(root).as_posix()
        return f"[[{rel.removesuffix('.md')}|{display}]]"
    return target.name


# --- pack ---------------------------------------------------------------------------


def event_pack_required(meta: dict[str, Any]) -> bool:
    """False se la nota evento dice `pack: none` o `modalita: bollettino_semplice`."""
    modalita = str(meta.get("modalita") or "").lower()
    if modalita in {"bollettino_semplice", "bollettino-only", "bollettino_only", "solo_bollettino"}:
        return False
    pack = meta.get("pack")
    if pack in (False, 0):
        return False
    return not (isinstance(pack, str) and pack.lower() in {"none", "no", "false", "skip", "nessuno"})


def pack_paths(event_folder: Path) -> dict[str, Path]:
    return {name.removesuffix(".md"): event_folder / name for name in PACK_FILES}


def open_todos_from_progetto(text: str) -> list[str]:
    _, body = parse_frontmatter(text)
    todos: list[str] = []
    for section_name, prefix in (("TODO", ""), ("Checklist operativa", "[checklist] ")):
        section = extract_section(body, section_name)
        if section:
            todos.extend(prefix + item for item in open_checkboxes(section))
    return todos


def validate_pack(event_folder: Path) -> dict[str, Any]:
    paths = pack_paths(event_folder)
    missing = [name for name, p in paths.items() if not p.is_file()]
    issues: list[str] = []
    open_todos: list[str] = []
    if missing:
        issues.append(f"Pack incompleto: manca {', '.join(missing)}")
    else:
        text = paths["progetto"].read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if meta.get("tipo") != "progetto-evento":
            issues.append("progetto.md: frontmatter tipo != progetto-evento")
        if meta.get("standard_version") is None:
            issues.append("progetto.md: manca standard_version")
        for sec in REQUIRED_PROGETTO_SECTIONS:
            if extract_section(body, sec) is None:
                issues.append(f"progetto.md: manca sezione ## {sec}")
        inv_meta, _ = parse_frontmatter(paths["invitati"].read_text(encoding="utf-8"))
        if inv_meta.get("tipo") != "invitati":
            issues.append("invitati.md: frontmatter tipo != invitati")
        sp_meta, sp_body = parse_frontmatter(paths["spese"].read_text(encoding="utf-8"))
        if sp_meta.get("tipo") != "spese":
            issues.append("spese.md: frontmatter tipo != spese")
        for sec in REQUIRED_SPESE_SECTIONS:
            if extract_section(sp_body, sec) is None:
                issues.append(f"spese.md: manca sezione ## {sec}")
        open_todos = open_todos_from_progetto(text)
    return {
        "missing": missing,
        "issues": issues,
        "open_todos": open_todos,
        "standard_ok": not issues,
        "paths": {k: str(v) for k, v in paths.items()},
    }


def has_bollettino(folder: Path, subfolder: str = "Bollettini") -> bool:
    """True se nella cartella dell'evento o nella sua sottocartella `Bollettini/` c'è una nota bollettino."""
    notes = list(folder.glob("*.md")) + list((folder / subfolder).glob("*.md"))
    for md in notes:
        if md.name in PACK_FILES:
            continue
        if "bollettino" in md.name.lower():
            return True
        meta, _ = parse_frontmatter(md.read_text(encoding="utf-8", errors="replace"))
        if meta.get("tipo") == "bollettino":
            return True
    return False


def render_template(name: str, context: dict[str, str]) -> str:
    text = (TEMPLATES_DIR / name).read_text(encoding="utf-8")
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", str(value))
    return re.sub(r"\{\{[a-z_]+\}\}", "", text)


def build_pack_context(
    profile: dict[str, Any],
    ev: Event,
    root: Path,
    overrides: dict[str, str] | None = None,
) -> dict[str, str]:
    folder = Path(ev.folder)
    note = Path(ev.note_path)
    indice_rel = profile["archivio"].get("indice_anno")
    indice = root / indice_rel.format(anno=ev.anno_sociale) if indice_rel else None
    ctx = {
        "anno_sociale": ev.anno_sociale,
        "data": ev.date,
        "data_display": ev.date,
        "titolo": ev.title,
        "evento_ref": make_ref(profile, note, folder.name, root),
        "evento_link": make_link(profile, note, "Nota evento", folder, root),
        "invitati_link": make_link(profile, folder / "invitati.md", "Invitati", folder, root),
        "spese_link": make_link(profile, folder / "spese.md", "Spese", folder, root),
        "indice_link": (
            make_link(profile, indice, f"Indice {ev.anno_sociale}", folder, root) if indice is not None else "—"
        ),
        "oggi": today_in_tz(profile).isoformat(),
        "orario": "da definire",
        "location": "da definire",
        "maps": "",
        "dress_code": "da definire",
        "costo": "da definire",
        "scadenza": "da definire",
        "aperta_a": "da definire",
        "tablerworld_id": ev.tablerworld_id or "da definire",
        "cartella": folder.relative_to(root).as_posix() if folder.is_relative_to(root) else str(folder),
        "descrizione": "",
        "quota_persona": str(profile.get("quota_default", 25)),
    }
    if overrides:
        ctx.update(overrides)
    return ctx


def write_event_note(
    profile: dict[str, Any],
    d: date,
    title: str,
    root: Path,
    *,
    pack: bool = True,
    apply: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    """Crea cartella + nota evento + sottocartelle `archivio.cartelle_evento` (dry-run se apply=False).

    Non sovrascrive mai.

    Se esiste già una cartella con la stessa data o un titolo simile si ferma (`blocked_similar`):
    probabilmente è lo stesso evento scritto in un altro modo. `force` solo se l'utente conferma che è diverso.
    """
    folder = event_folder_for(profile, d, title, root)
    note = folder / f"{folder.name}.md"
    if note.exists():
        return {"action": "exists", "note": str(note)}
    similar = find_similar_folders(profile, d, title, root)
    if similar and not force:
        return {
            "action": "blocked_similar",
            "note": str(note),
            "similar": similar,
            "hint": "Esiste già una cartella simile: chiedi se è lo stesso evento (usa quella) o un altro (--force).",
        }
    anno = anno_sociale(d, profile)
    indice_rel = profile["archivio"].get("indice_anno")
    indice = root / indice_rel.format(anno=anno) if indice_rel else None
    text = render_template(
        "evento.md",
        {
            "data": d.isoformat(),
            "titolo": title,
            "anno_sociale": anno,
            "oggi": today_in_tz(profile).isoformat(),
            "pack_line": "" if pack else "pack: none\nmodalita: bollettino_semplice\n",
            "indice_link": (make_link(profile, indice, f"Indice {anno}", folder, root) if indice is not None else "—"),
        },
    )
    subfolders = [str(folder / name) for name in profile["archivio"].get("cartelle_evento") or []]
    if not apply:
        return {"action": "would_create", "note": str(note), "cartelle": subfolders, "preview": text}
    folder.mkdir(parents=True, exist_ok=True)
    for sub in subfolders:
        Path(sub).mkdir(exist_ok=True)
    note.write_text(text, encoding="utf-8")
    return {"action": "created", "note": str(note), "cartelle": subfolders}


def write_pack(
    profile: dict[str, Any],
    ev: Event,
    root: Path,
    overrides: dict[str, str] | None = None,
    force: bool = False,
) -> dict[str, str]:
    folder = Path(ev.folder)
    folder.mkdir(parents=True, exist_ok=True)
    ctx = build_pack_context(profile, ev, root, overrides)
    written: dict[str, str] = {}
    for filename in PACK_FILES:
        dest = folder / filename
        if dest.exists() and not force:
            continue
        dest.write_text(render_template(filename, ctx), encoding="utf-8")
        written[filename] = str(dest)
    return written
