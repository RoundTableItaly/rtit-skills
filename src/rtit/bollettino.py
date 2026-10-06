"""Bollettino: dalla nota markdown (o da un JSON) al DOCX/PDF con il template docxtpl.

Il template generico ha intestazione, Consiglio Direttivo, destinatari e firme come variabili:
tutto arriva dal profilo, niente è scritto nel codice.

La nota del bollettino sta nella cartella `Bollettini/` dell'evento
(`Anni sociali/AAAA-AAAA/Eventi/AAAA-MM-GG Nome/Bollettini/`); DOCX e PDF vengono scritti accanto alla nota.
Nessuna copia altrove: l'indice dell'anno elenca i bollettini.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

from .markdown import extract_section, parse_frontmatter
from .profile import direttivo_member, resolve_path

TEMPLATE_DIR = Path(__file__).parent / "templates" / "bollettino"
DEFAULT_TEMPLATE = TEMPLATE_DIR / "generico.docx"
LOGO_PLACEHOLDERS = (TEMPLATE_DIR / "logo-sinistra.png", TEMPLATE_DIR / "logo-destra.png")

DEFAULT_APERTA_A = "Tablers, ex Tablers, aspiranti e amici"

INVITO_LINE_RE = re.compile(r"\*\*(.+?),\s*ore\s+([^*]+)\*\*\s*[—–-]\s*(.+)", re.IGNORECASE)
TABLE_ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)
FIRMA_RE = re.compile(r"-\s*\*\*(Presidente|Segretario)\*\*\s*:\s*(.+?)\s*[—–-]\s*(.+)\s*$", re.MULTILINE | re.I)
APERTA_BULLET_RE = re.compile(r"^-\s*Aperta a:\s*(.+)$", re.MULTILINE | re.IGNORECASE)


class BollettinoError(Exception):
    pass


def iso_to_it(iso: str) -> str:
    return date.fromisoformat(iso).strftime("%d/%m/%Y")


def default_destinatari(profile: dict[str, Any]) -> list[str]:
    """Destinatari "e p.c." di default per livello (sovrascrivibili con bollettino.destinatari_pc)."""
    zona = profile.get("zona") or "Zona"
    livello = profile.get("livello", "tavola")
    nazionali = ["al Presidente Nazionale RTIT", "al Vice Presidente Nazionale RTIT", "al Segretario Nazionale RTIT"]
    if livello == "tavola":
        return nazionali + [f"al Comitato di {zona}", f"ai Presidenti delle Tavole della {zona}"]
    if livello == "zona":
        return nazionali + [f"ai Presidenti delle Tavole della {zona}"]
    return ["ai Presidenti di Zona", "ai Presidenti di Tavola"]


def header_context(profile: dict[str, Any], anno: str) -> dict[str, Any]:
    intest = profile.get("intestazione") or {}
    boll = profile.get("bollettino") or {}
    destinatari = list(boll.get("destinatari_pc") or default_destinatari(profile))
    if destinatari and not destinatari[0].lower().startswith("e p.c."):
        destinatari[0] = f"e p.c. {destinatari[0]}"
    sede = intest.get("sede") or []
    if isinstance(sede, str):
        sede = [s.strip() for s in sede.split(",") if s.strip()]
    direttivo = (profile.get("direttivo") or {}).get("membri") or []
    return {
        "nome_tavola_maiuscolo": str(profile.get("nome") or profile.get("sigla") or "").upper(),
        "nome_esteso": profile.get("nome_esteso") or profile.get("nome") or "",
        "sigla": profile.get("sigla") or "",
        "citta": profile.get("citta") or "",
        "sito": intest.get("sito") or "—",
        "ritrovi": intest.get("ritrovi") or "—",
        "sede_righe": sede or ["—"],
        "charter": intest.get("charter") or "—",
        "tavola_madrina": intest.get("tavola_madrina") or "—",
        "anno_direttivo": (profile.get("direttivo") or {}).get("anno") or anno,
        "direttivo": [
            {"ruolo": str(m.get("ruolo", "")), "nome": str(m.get("nome", ""))} for m in direttivo if isinstance(m, dict)
        ],
        "destinatari_pc": destinatari,
    }


def _firma(firme: dict[str, tuple[str, str]], profile: dict[str, Any], ruolo: str) -> tuple[str, str]:
    if ruolo in firme:
        return firme[ruolo]
    member = direttivo_member(profile, ruolo)
    if member and member.get("nome"):
        return str(member["nome"]), str(member.get("telefono") or "")
    raise BollettinoError(
        f"Manca la firma del {ruolo.capitalize()}: aggiungila alla sezione ## Firme della nota "
        f"oppure in direttivo.membri del profilo."
    )


def _parse_table(invito: str) -> dict[str, str]:
    return {m.group(1).strip().lower(): m.group(2).strip() for m in TABLE_ROW_RE.finditer(invito)}


def build_context_from_md(md_path: Path, profile: dict[str, Any]) -> dict[str, Any]:
    fm, body = parse_frontmatter(md_path.read_text(encoding="utf-8"))
    if fm.get("tipo") != "bollettino":
        raise BollettinoError(f"La nota non è un bollettino (tipo={fm.get('tipo')!r}): {md_path}")
    numero = fm.get("numero")
    data_emissione = str(fm.get("data_emissione") or "")
    # `anno_associativo` è il nome usato dalle note meno recenti
    anno = str(fm.get("anno_sociale") or fm.get("anno_associativo") or "")
    missing = [k for k, v in (("numero", numero), ("data_emissione", data_emissione), ("anno_sociale", anno)) if not v]
    if missing:
        raise BollettinoError(f"Frontmatter incompleto: manca {', '.join(missing)}")

    invito = extract_section(body, "Invito") or ""
    m = INVITO_LINE_RE.search(invito)
    if not m:
        raise BollettinoError("Sezione ## Invito: serve la riga '**Giorno data, ore HH:MM** — Titolo'")
    table = _parse_table(invito)
    location = table.get("location")
    dress = table.get("dress code")
    costo = table.get("costo")
    scadenza = table.get("prenotazione entro") or table.get("conferma entro") or table.get("scadenza")
    gaps = [
        n
        for n, v in (
            ("Location", location),
            ("Dress code", dress),
            ("Costo", costo),
            ("Prenotazione/Conferma entro", scadenza),
        )
        if not v
    ]
    if gaps:
        raise BollettinoError(f"Tabella dell'invito incompleta: manca {', '.join(gaps)}")

    aperta = APERTA_BULLET_RE.search(invito)
    corpo = INVITO_LINE_RE.sub("", invito, count=1)
    corpo = APERTA_BULLET_RE.sub("", corpo)
    corpo = re.sub(r"^\|.*\|\s*$", "", corpo, flags=re.MULTILINE)
    righe = [
        ln.strip()[2:].strip() if ln.strip().startswith("- ") else ln.strip() for ln in corpo.splitlines() if ln.strip()
    ]

    firme = {
        fm_.group(1).lower(): (fm_.group(2).strip(), fm_.group(3).strip())
        for fm_ in FIRMA_RE.finditer(extract_section(body, "Firme") or "")
    }
    presidente, tel_pres = _firma(firme, profile, "presidente")
    segretario, tel_seg = _firma(firme, profile, "segretario")

    ctx = header_context(profile, anno)
    ctx.update(
        {
            "data_emissione_it": iso_to_it(data_emissione),
            "numero": str(numero),
            "anno_slash": anno.replace("-", "/"),
            "anno_sociale": anno,
            "data_evento_it": m.group(1).strip(),
            "ora": m.group(2).strip(),
            "titolo": m.group(3).strip().rstrip(".").upper(),
            "corpo_righe": righe or [""],
            "aperta_a": aperta.group(1).strip()
            if aperta
            else (profile.get("bollettino") or {}).get("aperta_a") or DEFAULT_APERTA_A,
            "location": location,
            "dress_code": dress,
            "costo": costo,
            "link_prenotazione": table.get("maps") or table.get("link prenotazione") or "—",
            "scadenza": scadenza,
            "presidente": presidente,
            "tel_presidente": tel_pres,
            "segretario": segretario,
            "tel_segretario": tel_seg,
        }
    )
    return ctx


def template_path(profile: dict[str, Any], override: Path | None = None) -> Path:
    if override:
        return override
    custom = resolve_path(profile, (profile.get("bollettino") or {}).get("template"))
    return custom or DEFAULT_TEMPLATE


def render_docx(template: Path, context: dict[str, Any], out_docx: Path, profile: dict[str, Any]) -> None:
    from docxtpl import DocxTemplate

    tpl = DocxTemplate(str(template))
    if template == DEFAULT_TEMPLATE:
        loghi = (profile.get("intestazione") or {}).get("loghi") or []
        for placeholder, logo in zip(LOGO_PLACEHOLDERS, loghi, strict=False):
            logo_path = resolve_path(profile, logo)
            if logo_path and logo_path.is_file():
                tpl.replace_media(str(placeholder), str(logo_path))
    tpl.render({k: v for k, v in context.items() if not k.startswith("_")})
    out_docx.parent.mkdir(parents=True, exist_ok=True)
    tpl.save(str(out_docx))


def _soffice() -> str | None:
    return shutil.which("soffice") or shutil.which("libreoffice")


def convert_pdf(docx_path: Path, pdf_path: Path) -> tuple[bool, str]:
    """Word (docx2pdf, Windows/macOS) se disponibile, altrimenti LibreOffice headless."""
    if sys.platform in ("win32", "darwin"):
        try:
            from docx2pdf import convert

            convert(str(docx_path), str(pdf_path))
            if pdf_path.is_file():
                return True, "word"
        except Exception as exc:  # noqa: BLE001 — Word assente o errore COM: si prova LibreOffice
            print(f"WARN: conversione con Word non riuscita: {exc}", file=sys.stderr)
    office = _soffice()
    if office:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [office, "--headless", "--convert-to", "pdf", "--outdir", tmp, str(docx_path)],
                capture_output=True,
                timeout=180,
                check=False,
            )
            produced = Path(tmp) / f"{docx_path.stem}.pdf"
            if produced.is_file():
                pdf_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(produced), pdf_path)
                return True, "libreoffice"
    return False, "nessun convertitore (installa Word o LibreOffice, oppure esporta il PDF a mano)"


def render(
    profile: dict[str, Any],
    *,
    md: Path | None = None,
    context: dict[str, Any] | None = None,
    out_dir: Path | None = None,
    basename: str | None = None,
    template: Path | None = None,
    pdf: bool = True,
    force: bool = False,
) -> dict[str, Any]:
    """Genera DOCX (+PDF) in `out_dir`, di default la cartella della nota (`<evento>/Bollettini/`).

    Non copia nulla altrove: con `out_dir` su una cartella di anteprima l'archivio resta intatto.
    """
    if context is None:
        if md is None:
            raise BollettinoError("Serve --md (nota bollettino) oppure --json-contesto (contesto JSON).")
        context = build_context_from_md(md, profile)
    else:
        anno = str(context.get("anno_sociale") or context.get("anno_associativo") or "")
        context = {**header_context(profile, anno), **context}
    tpl = template_path(profile, template)
    if not tpl.is_file():
        raise BollettinoError(f"Template non trovato: {tpl}")
    out_dir = (out_dir or (md.parent if md else Path.cwd())).expanduser().resolve()
    basename = basename or (md.stem if md else f"Bollettino N.{context.get('numero')}")
    out_docx = out_dir / f"{basename}.docx"
    out_pdf = out_dir / f"{basename}.pdf"
    existing = [str(p) for p in (out_docx, out_pdf) if p.exists()]
    if existing and not force:
        raise BollettinoError(
            "File già presenti, non li sovrascrivo senza --force: "
            + ", ".join(existing)
            + ". Per una prova usa --out-dir su una cartella di anteprima."
        )
    render_docx(tpl, context, out_docx, profile)
    result: dict[str, Any] = {"docx": str(out_docx), "pdf": None, "pdf_via": None}
    if pdf:
        ok, via = convert_pdf(out_docx, out_pdf)
        result["pdf"] = str(out_pdf) if ok else None
        result["pdf_via"] = via
    return result
