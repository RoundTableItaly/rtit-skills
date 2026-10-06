"""Profilo di tavola, zona o nazionale: caricamento, default, anno sociale, decisioni."""

from __future__ import annotations

import os
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

PROFILE_ENV = "RTIT_PROFILO"
PROFILE_FILENAMES = ("rtit-profilo.yaml", "rtit-profilo.yml")
LIVELLI = ("tavola", "zona", "nazionale")
LINK_STILI = ("markdown", "wikilink")
# Cartelle standard di un anno sociale nell'archivio condiviso (chiavi di `archivio.*`)
CARTELLE_ANNO = ("eventi", "direttivo", "tesoreria", "comunicazione")
# Default di `archivio.*`: percorsi relativi alla cartella principale dell'archivio condiviso
DEFAULT_ARCHIVIO: dict[str, Any] = {
    "documenti_legali": "Documenti legali",
    "cartelle_legali": ["Statuto e regolamenti", "Fiscale e PEC", "Banca", "Loghi e modelli"],
    "anni": "Anni sociali/{anno}",
    "eventi": "Anni sociali/{anno}/Eventi",
    "direttivo": "Anni sociali/{anno}/Direttivo",
    "tesoreria": "Anni sociali/{anno}/Tesoreria",
    "comunicazione": "Anni sociali/{anno}/Comunicazione",
    "indice_anno": "Anni sociali/{anno}/_Indice {anno}.md",
    "cartelle_evento": ["Bollettini", "Form", "Altri documenti"],
}

DEFAULT_CLASSIFICAZIONE: dict[str, list[str]] = {
    # Nessuna cartella evento, nessun pack.
    "ignora": ["ritrovo", "riunione mensile"],
    # Solo verbale/nota direttivo: mai Eventi, pack, bollettino.
    "direttivo": [
        "consiglio di tavola",
        "consiglio direttivo",
        "consiglio di zona",
        r"\bconsiglio\b",
        "direttivo",
        r"\bcd\b",
    ],
    # Nota evento + bollettino semplice, senza pack organizzativo.
    "solo_bollettino": [],
    # Evento conviviale: nota evento + pack completo.
    "sociale": ["cena", "aperitivo", "visita", "gita", "festa", "grigliata"],
}


class ProfileError(Exception):
    """Profilo mancante o non valido."""


def find_profile(path: str | Path | None = None, cwd: Path | None = None) -> Path:
    """Risolve il file profilo: argomento, poi $RTIT_PROFILO, poi ./rtit-profilo.yaml, poi ~/.rtit/."""
    candidates: list[Path] = []
    if path:
        candidates.append(Path(path).expanduser())
    elif os.environ.get(PROFILE_ENV):
        candidates.append(Path(os.environ[PROFILE_ENV]).expanduser())
    else:
        base = cwd or Path.cwd()
        candidates.extend(base / name for name in PROFILE_FILENAMES)
        candidates.extend(Path.home() / ".rtit" / name for name in PROFILE_FILENAMES)
    for cand in candidates:
        if cand.is_file():
            return cand.resolve()
    tried = ", ".join(str(c) for c in candidates)
    raise ProfileError(
        f"Profilo non trovato (cercato: {tried}). Crealo con la skill rt-primi-passi "
        f"oppure con `rtit profilo nuovo` e poi passa --profilo <file> (o imposta {PROFILE_ENV})."
    )


def _setdefaults(data: dict[str, Any]) -> dict[str, Any]:
    data.setdefault("versione", 1)
    data.setdefault("livello", "tavola")
    if data["livello"] not in LIVELLI:
        raise ProfileError(f"livello deve essere uno di {LIVELLI}, non {data['livello']!r}")
    data.setdefault("fuso_orario", "Europe/Rome")
    if "mese_inizio_anno" in data:
        data.pop("mese_inizio_anno")
        print(
            "Avviso: `mese_inizio_anno` nel profilo è ignorato. L'anno sociale inizia la domenica dopo l'AGM "
            "(di solito il primo sabato di giugno); per un AGM in altra data usa `agm` nel profilo.",
            file=sys.stderr,
        )
    data["agm"] = _normalize_agm(data.get("agm"))
    data.setdefault("sigla", data.get("nome", data["id"]))
    data.setdefault("nome_esteso", data.get("nome", data["sigla"]))
    data.setdefault("citta", "")
    data.setdefault("zona", "")
    data.setdefault("quota_default", 25)
    data.setdefault("intestazione", {})
    data.setdefault("direttivo", {})
    data["direttivo"].setdefault("membri", [])
    data.setdefault("bollettino", {})
    arch = data.setdefault("archivio", {})
    # compatibilità: `tipo: obsidian` → link wikilink; `tipo: nessuno` → nessun archivio
    legacy = arch.pop("tipo", None)
    if legacy == "nessuno":
        arch.pop("percorso", None)
    arch.setdefault("servizio", "cartella")  # google-drive | onedrive | dropbox | sharepoint | nextcloud | cartella
    arch.setdefault("link", "wikilink" if legacy == "obsidian" else "markdown")
    if arch["link"] not in LINK_STILI:
        raise ProfileError(f"archivio.link deve essere uno di {LINK_STILI}, non {arch['link']!r}")
    for key, default in DEFAULT_ARCHIVIO.items():
        arch.setdefault(key, list(default) if isinstance(default, list) else default)
    cal = data.setdefault("calendario", {})
    cal.setdefault("giorni_indietro", 7)
    cal.setdefault("giorni_avanti", 120)
    app = data.setdefault("app_rtit", {})
    app.setdefault("base_url", "https://app.roundtable.it/api/v1")
    app.setdefault("mesi_planner", 3)
    app.setdefault("soglia_punteggio", 90)
    cls = data.setdefault("classificazione", {})
    for key, default in DEFAULT_CLASSIFICAZIONE.items():
        cls.setdefault(key, list(default))
    prom = data.setdefault("promemoria", {})
    prom.setdefault("bollettino_giorni", 14)
    prom.setdefault("tablerworld_giorni", 21)
    return data


def _normalize_agm(raw: Any) -> dict[str, str]:
    """`agm: {"2025": "2025-06-14"}` → chiavi stringa e date ISO (YAML può leggere anni e date come tipi nativi)."""
    if not raw:
        return {}
    if not isinstance(raw, dict):
        raise ProfileError('agm deve essere una mappa anno → data, per esempio agm: {"2027": "2027-06-05"}')
    out: dict[str, str] = {}
    for anno, giorno in raw.items():
        try:
            d = giorno if isinstance(giorno, date) else date.fromisoformat(str(giorno))
        except ValueError as exc:
            raise ProfileError(f"agm.{anno}: data non valida {giorno!r} (serve AAAA-MM-GG)") from exc
        out[str(anno)] = d.isoformat()
    return out


def load_profile(path: str | Path | None = None) -> dict[str, Any]:
    """Carica il profilo YAML e applica i default. Aggiunge `_path` (file sorgente)."""
    p = find_profile(path)
    with p.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict) or not data.get("id"):
        raise ProfileError(f"Profilo non valido (serve almeno `id`): {p}")
    data = _setdefaults(data)
    data["_path"] = str(p)
    return data


def profile_dir(profile: dict[str, Any]) -> Path:
    return Path(profile["_path"]).parent if profile.get("_path") else Path.cwd()


def resolve_path(profile: dict[str, Any], value: str | None) -> Path | None:
    """Percorso assoluto oppure relativo alla cartella del profilo."""
    if not value:
        return None
    p = Path(str(value)).expanduser()
    return p if p.is_absolute() else (profile_dir(profile) / p).resolve()


def public_view(profile: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in profile.items() if not k.startswith("_")}


# --- tempo e anno sociale -------------------------------------------------------
#
# L'anno sociale inizia la domenica dopo l'AGM. L'AGM si tiene di sabato, di solito il primo sabato
# di giugno, salvo diverse indicazioni del Comitato Nazionale: in quel caso la data va in `agm` nel profilo.
# Le date esatte di ogni anno sono nell'App RTIT (strumento MCP `list_statutory_years`).


def today_in_tz(profile: dict[str, Any]) -> date:
    return datetime.now(ZoneInfo(profile.get("fuso_orario", "Europe/Rome"))).date()


def data_agm(anno_solare: int, profile: dict[str, Any] | None = None) -> date:
    """Data dell'AGM di un anno solare: `agm[anno]` del profilo se c'è, altrimenti il primo sabato di giugno."""
    override = _normalize_agm((profile or {}).get("agm")).get(str(anno_solare))
    if override:
        return date.fromisoformat(override)
    primo_giugno = date(anno_solare, 6, 1)
    return primo_giugno + timedelta(days=(5 - primo_giugno.weekday()) % 7)


def inizio_anno_sociale(anno_solare: int, profile: dict[str, Any] | None = None) -> date:
    """Primo giorno dell'anno sociale che inizia nell'anno solare dato: la domenica dopo l'AGM."""
    agm = data_agm(anno_solare, profile)
    return agm + timedelta(days=(6 - agm.weekday()) % 7 or 7)


def anno_sociale(d: date, profile: dict[str, Any] | None = None) -> str:
    """Anno sociale `AAAA-AAAA` a cui appartiene la data `d`."""
    if d >= inizio_anno_sociale(d.year, profile):
        return f"{d.year}-{d.year + 1}"
    return f"{d.year - 1}-{d.year}"


# --- titoli ---------------------------------------------------------------------


def normalize_title(title: str) -> str:
    t = unicodedata.normalize("NFKD", title)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"\b(rt\s*\d+|round\s*table)\b", " ", t)
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_similarity(a: str, b: str) -> float:
    """Massimo tra Jaccard sulle parole e SequenceMatcher (stdlib) sui titoli normalizzati."""
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    sa, sb = set(na.split()), set(nb.split())
    jaccard = (len(sa & sb) / len(sa | sb)) if sa and sb else 0.0
    return max(jaccard, SequenceMatcher(None, na, nb).ratio())


def classify_title(profile: dict[str, Any], title: str) -> str:
    """Restituisce ignora | direttivo | solo_bollettino | sociale | altro."""
    n = normalize_title(title)
    cls = profile.get("classificazione") or {}
    for kind in ("ignora", "direttivo", "solo_bollettino", "sociale"):
        for pat in cls.get(kind) or []:
            if re.search(pat, n, re.I):
                return kind
    return "altro"


# --- direttivo e firme ---------------------------------------------------------


def direttivo_member(profile: dict[str, Any], ruolo: str) -> dict[str, Any] | None:
    for m in (profile.get("direttivo") or {}).get("membri") or []:
        if isinstance(m, dict) and str(m.get("ruolo", "")).strip().lower() == ruolo.lower():
            return m
    return None


# --- decisioni persistenti (accanto al profilo, mai nella cartella della skill) ------


def decisions_path(profile: dict[str, Any]) -> Path:
    if profile.get("_path"):
        p = Path(profile["_path"])
        return p.with_name(f"{p.stem}.decisioni.yaml")
    return Path.cwd() / f"{profile['id']}.decisioni.yaml"


def load_decisions(profile: dict[str, Any]) -> dict[str, Any]:
    path = decisions_path(profile)
    data: dict[str, Any] = {}
    if path.is_file():
        with path.open(encoding="utf-8") as fh:
            loaded = yaml.safe_load(fh) or {}
        data = loaded if isinstance(loaded, dict) else {}
    data.setdefault("versione", 1)
    data.setdefault("profilo", profile["id"])
    data.setdefault("calendario_ignora", [])
    data.setdefault("note", [])
    return data


def save_decisions(profile: dict[str, Any], data: dict[str, Any]) -> Path:
    path = decisions_path(profile)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {**data, "profilo": profile["id"], "versione": int(data.get("versione") or 1)}
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh, allow_unicode=True, sort_keys=False)
    return path


def calendar_is_ignored(decisions: dict[str, Any], cal_event: dict[str, Any]) -> bool:
    uid = (cal_event.get("uid") or "").strip()
    summary = (cal_event.get("summary") or "").strip()
    start = (cal_event.get("start_date") or "").strip()
    for row in decisions.get("calendario_ignora") or []:
        if not isinstance(row, dict):
            continue
        if uid and row.get("uid") and str(row["uid"]) == uid:
            return True
        if (
            row.get("data")
            and row.get("titolo")
            and str(row["data"]) == start
            and normalize_title(str(row["titolo"])) == normalize_title(summary)
        ):
            return True
    return False


def decisions_markdown(decisions: dict[str, Any], path: Path | None = None) -> str:
    lines = ["## Decisioni salvate", ""]
    if path:
        lines += [f"File: `{path}`", ""]
    ignores = decisions.get("calendario_ignora") or []
    notes = decisions.get("note") or []
    if not (ignores or notes):
        return "\n".join(lines + ["- (nessuna decisione salvata)", ""])
    if ignores:
        lines += ["### Calendario — eventi ignorati", ""]
        for row in ignores:
            if isinstance(row, dict):
                reason = f" — {row['motivo']}" if row.get("motivo") else ""
                lines.append(f"- `{row.get('data') or '?'}` {row.get('titolo') or '?'}{reason}")
        lines.append("")
    if notes:
        lines += ["### Note", ""] + [f"- {n}" for n in notes] + [""]
    return "\n".join(lines)
