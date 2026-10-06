"""Calcolo spese evento da spese.md + invitati.md (nessuna scrittura: solo risultato JSON)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .markdown import extract_section, parse_frontmatter

YES = {"sì", "si", "yes", "true", "1", "ok", "x"}


def _num(raw: str, default: float = 0.0) -> float:
    try:
        return float(str(raw).replace("€", "").replace(",", ".").strip())
    except ValueError:
        return default


def _table_rows(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or set(cells[0]) <= {"-", ":"}:
            continue
        if cells[0].lower() in {"parametro", "voce", "metrica", "nome"}:
            continue
        rows.append(cells)
    return rows


def count_invitati(invitati_text: str) -> dict[str, float]:
    _, body = parse_frontmatter(invitati_text)
    confermati = in_attesa = 0
    quote_attese = incassato = 0.0
    for cells in _table_rows(body):
        if len(cells) < 6 or not cells[0]:
            continue
        conferma = cells[2].lower()
        quota = _num(cells[4]) if cells[4] else 0.0
        if conferma in YES:
            confermati += 1
            quote_attese += quota
            if cells[5].lower() in YES:
                incassato += quota
        elif conferma in {"tbd", "?", ""}:
            in_attesa += 1
    return {
        "confermati": confermati,
        "in_attesa": in_attesa,
        "quote_attese": quote_attese,
        "incassato": incassato,
    }


def parse_parametri(spese_text: str, quota_default: float = 25) -> dict[str, float]:
    _, body = parse_frontmatter(spese_text)
    params: dict[str, float] = {"N_confermati": 0, "N_stimati": 0, "Buffer_%": 10, "Quota_persona": quota_default}
    section = extract_section(body, "Parametri")
    for cells in _table_rows(section or ""):
        if len(cells) >= 2 and "da invitati" not in cells[1].lower():
            try:
                params[cells[0]] = float(cells[1].replace(",", "."))
            except ValueError:
                continue
    return params


def parse_voci(spese_text: str, n: int) -> list[dict[str, Any]]:
    """Voci `per_persona` moltiplicano per N; voci `fisso` per la quantità indicata (default 1)."""
    _, body = parse_frontmatter(spese_text)
    voci = []
    for cells in _table_rows(extract_section(body, "Voci di spesa") or ""):
        if len(cells) < 4:
            continue
        unit = _num(cells[1])
        tipo = cells[2].lower()
        qty_raw = cells[3].strip()
        if tipo == "per_persona" or qty_raw.upper() in {"=N", "N"}:
            qty = float(n)
        else:
            qty = _num(qty_raw, 1.0)
        voci.append({"voce": cells[0], "unit": unit, "tipo": tipo, "qty": qty, "totale": round(unit * qty, 2)})
    return voci


def compute(event_folder: Path, n_override: int | None = None, quota_default: float = 25) -> dict[str, Any]:
    spese = event_folder / "spese.md"
    invitati = event_folder / "invitati.md"
    if not spese.is_file():
        raise FileNotFoundError(f"Manca {spese}")
    spese_text = spese.read_text(encoding="utf-8")
    params = parse_parametri(spese_text, quota_default)
    inv = (
        count_invitati(invitati.read_text(encoding="utf-8"))
        if invitati.is_file()
        else {"confermati": 0, "in_attesa": 0, "quote_attese": 0.0, "incassato": 0.0}
    )
    n = (
        n_override
        if n_override is not None
        else int(inv["confermati"] or params.get("N_stimati") or params.get("N_confermati") or 0)
    )
    buffer_pct = float(params.get("Buffer_%") or 10)
    quota = float(params.get("Quota_persona") or quota_default)
    voci = parse_voci(spese_text, n)
    subtotale = round(sum(v["totale"] for v in voci), 2)
    buffer_val = round(subtotale * buffer_pct / 100.0, 2)
    totale_spesa = round(subtotale + buffer_val, 2)
    incasso = inv["quote_attese"] or round(n * quota, 2)
    return {
        "n": n,
        "confermati": inv["confermati"],
        "in_attesa": inv["in_attesa"],
        "voci": voci,
        "subtotale": subtotale,
        "buffer_pct": buffer_pct,
        "buffer": buffer_val,
        "totale_spesa": totale_spesa,
        "incasso_atteso": incasso,
        "incassato": inv["incassato"],
        "saldo": round(incasso - totale_spesa, 2),
        "quota_persona": quota,
    }
