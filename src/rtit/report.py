"""Report «cosa c'è da fare»: eventi futuri, archivio, calendario e App RTIT insieme (sola lettura)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from . import app_rtit, calendario
from .archive import (
    ArchiveError,
    Event,
    event_pack_required,
    future_events,
    has_archive,
    has_bollettino,
    same_date_duplicates,
    scan_events,
    validate_pack,
)
from .profile import calendar_is_ignored, decisions_markdown, decisions_path, load_decisions, today_in_tz


def todo_rows(profile: dict[str, Any], events: list[Event], today: date) -> list[dict[str, Any]]:
    prom = profile.get("promemoria") or {}
    rows = []
    for ev in events:
        folder = Path(ev.folder)
        required = event_pack_required(ev.frontmatter or {})
        pack = (
            validate_pack(folder)
            if required
            else {
                "missing": [],
                "issues": [],
                "open_todos": [],
                "standard_ok": True,
                "skipped": True,
            }
        )
        t_days = (date.fromisoformat(ev.date) - today).days
        warnings = []
        bollettino = has_bollettino(folder)
        if not bollettino and t_days <= int(prom.get("bollettino_giorni", 14)):
            warnings.append(f"bollettino mancante a {t_days} giorni dall'evento")
        if required and not ev.tablerworld_id and t_days <= int(prom.get("tablerworld_giorni", 21)):
            warnings.append("evento non ancora su Tabler World (tablerworld_id assente)")
        rows.append(
            {
                "date": ev.date,
                "title": ev.title,
                "folder_name": folder.name,
                "folder": str(folder),
                "t_days": t_days,
                "pack_required": required,
                "has_bollettino": bollettino,
                "pack": pack,
                "warnings": warnings,
            }
        )
    return rows


def todo_markdown(rows: list[dict[str, Any]], today: date) -> str:
    if not rows:
        return f"## Eventi futuri\n\nNessun evento futuro in archivio (oggi {today.isoformat()}).\n"
    lines = [f"## Eventi futuri ({len(rows)})", "", f"Oggi {today.isoformat()}", ""]
    for r in rows:
        lines.append(f"### {r['folder_name']} (tra {r['t_days']} giorni)")
        for w in r["warnings"]:
            lines.append(f"- ⚠ {w}")
        if not r["pack_required"]:
            lines.append("- Modalità: bollettino semplice (pack non richiesto)")
            lines.append(f"- Bollettino: {'presente' if r['has_bollettino'] else 'mancante'}")
        else:
            pack = r["pack"]
            if pack["missing"]:
                lines.append(f"- Pack: manca {', '.join(pack['missing'])}")
            elif pack["standard_ok"]:
                lines.append("- Pack: conforme")
            else:
                lines.append("- Pack: non conforme")
                lines += [f"  - {i}" for i in pack["issues"]]
            if pack["open_todos"]:
                lines.append("- TODO aperti:")
                lines += [f"  - [ ] {t}" for t in pack["open_todos"]]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def calendar_markdown(cal: dict[str, Any], decisions: dict[str, Any]) -> str:
    lines = ["## Calendario", ""]
    if cal.get("summary"):
        s = cal["summary"]
        lines.append(
            f"- nuovi: {s['nuovo']} · cambiati: {s['cambiato']} · già in archivio: {s['in_archivio']} · "
            f"solo in archivio: {s['solo_archivio']}"
        )
        rows = [m for m in cal["matches"] if m["status"] in {"nuovo", "cambiato"}]
    else:
        lines.append(f"- {cal['count']} eventi tra {cal['from']} e {cal['to']} (archivio non configurato)")
        rows = [{"status": "nuovo", "calendar": e} for e in cal["events"]]
    actionable, by_kind, by_decision = [], [], []
    for m in rows:
        ce = m["calendar"]
        line = f"- **{m['status']}** [{ce.get('kind')}] {ce.get('start_date')} — {ce.get('summary')}"
        if calendar_is_ignored(decisions, ce):
            by_decision.append(line)
        elif ce.get("kind") in {"ignora", "direttivo"}:
            by_kind.append(line + " (niente cartella evento né pack)")
        elif ce.get("kind") == "solo_bollettino":
            actionable.append(line + " (nota + bollettino semplice, niente pack)")
        else:
            actionable.append(line)
    if actionable:
        lines += ["", "Da gestire:"] + actionable
    if by_kind:
        lines += ["", "Ignorati per tipo (ritrovi, direttivi):"] + by_kind
    if by_decision:
        lines += ["", "Ignorati per decisione salvata:"] + by_decision
    return "\n".join(lines) + "\n"


def duplicates_markdown(groups: list[list[str]]) -> str:
    lines = ["## Archivio — possibili doppioni", ""]
    for g in groups:
        lines.append("- stessa data: " + " · ".join(f"`{n}`" for n in g) + " → chiedi se è lo stesso evento e riunisci")
    return "\n".join(lines) + "\n"


def cosa_fare(
    profile: dict[str, Any],
    *,
    root: Path | None = None,
    skip_calendar: bool = False,
    skip_app_rtit: bool = False,
) -> dict[str, Any]:
    today = today_in_tz(profile)
    decisions = load_decisions(profile)
    report: dict[str, Any] = {
        "profile": profile["id"],
        "today": today.isoformat(),
        "decisions_file": str(decisions_path(profile)),
        "errors": [],
    }
    sections = [f"# Cosa c'è da fare — {profile.get('sigla')}", "", decisions_markdown(decisions).rstrip(), ""]

    events: list[Event] = []
    if has_archive(profile) or root:
        try:
            events = future_events(profile, root, on_or_after=today)
            rows = todo_rows(profile, events, today)
            report["todo"] = rows
            sections.append(todo_markdown(rows, today))
        except ArchiveError as exc:
            report["errors"].append({"step": "archivio", "error": str(exc)})
    else:
        sections.append(
            "## Eventi futuri\n\nNessun archivio configurato (archivio.percorso): i controlli sui pack sono saltati.\n"
        )

    if not skip_calendar and (profile.get("calendario") or {}).get("ical_url"):
        try:
            cal = calendario.fetch(profile)
            if has_archive(profile) or root:
                matches = calendario.match_to_archive(cal["events"], scan_events(profile, root))
                cal["matches"] = matches
                cal["summary"] = calendario.summarize(matches)
            report["calendar"] = cal
            sections.append(calendar_markdown(cal, decisions))
        except Exception as exc:  # noqa: BLE001 — rete o feed non valido: si riporta e si prosegue
            report["errors"].append({"step": "calendario", "error": str(exc)})

    if has_archive(profile) or root:
        try:
            groups = same_date_duplicates(profile, root)
            if groups:
                report["duplicati"] = groups
                sections.append(duplicates_markdown(groups))
        except ArchiveError:
            pass

    if not skip_app_rtit and (profile.get("app_rtit") or {}).get("organization_unit_id"):
        try:
            rep = app_rtit.report(profile, events)
            report["app_rtit"] = rep
            sections.append(rep["markdown"])
            report["errors"] += [{"step": f"app_rtit.{e['step']}", "error": e["error"]} for e in rep["errors"]]
        except Exception as exc:  # noqa: BLE001
            report["errors"].append({"step": "app_rtit", "error": str(exc)})

    if report["errors"]:
        sections += ["## Errori", ""] + [f"- {e['step']}: {e['error']}" for e in report["errors"]] + [""]
    report["markdown"] = "\n".join(sections).rstrip() + "\n"
    return report
