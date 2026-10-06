"""Calendario Google (iCal pubblico o indirizzo segreto) e confronto con l'archivio eventi."""

from __future__ import annotations

import hashlib
import tempfile
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .archive import Event
from .profile import classify_title, title_similarity, today_in_tz

CACHE_TTL_SEC = 15 * 60


class CalendarError(Exception):
    pass


def _cache_path(url: str) -> Path:
    return Path(tempfile.gettempdir()) / f"rtit_ical_{hashlib.sha256(url.encode()).hexdigest()[:16]}.ics"


def fetch_ics(url: str, use_cache: bool = True) -> bytes:
    import requests

    cache = _cache_path(url)
    if use_cache and cache.is_file() and (time.time() - cache.stat().st_mtime) < CACHE_TTL_SEC:
        return cache.read_bytes()
    resp = requests.get(url, timeout=30, headers={"User-Agent": "rtit-skills"})
    if resp.status_code in (403, 404):
        raise CalendarError(
            f"Il calendario ha risposto {resp.status_code}. Rendilo pubblico (Google Calendar → Impostazioni "
            "del calendario → Autorizzazioni di accesso → Rendi disponibile pubblicamente) oppure usa "
            "l'«Indirizzo segreto in formato iCal» nel profilo (calendario.ical_url)."
        )
    resp.raise_for_status()
    cache.write_bytes(resp.content)
    return resp.content


def _as_date(value: Any, tz: ZoneInfo) -> tuple[str, str | None, bool]:
    if value is None:
        return "", None, True
    dt = value.dt if hasattr(value, "dt") else value
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz)
        local = dt.astimezone(tz)
        return local.date().isoformat(), local.replace(microsecond=0).isoformat(), False
    if isinstance(dt, date):
        return dt.isoformat(), None, True
    return str(dt)[:10], None, True


def parse_events(ics_bytes: bytes, tz_name: str, start_min: date, start_max: date) -> list[dict[str, Any]]:
    from icalendar import Calendar

    tz = ZoneInfo(tz_name)
    out: list[dict[str, Any]] = []
    for component in Calendar.from_ical(ics_bytes).walk():
        if component.name != "VEVENT":
            continue
        if str(component.get("status", "") or "").upper() == "CANCELLED":
            continue
        start_date, start_dt, all_day = _as_date(component.get("dtstart"), tz)
        end_date, end_dt, _ = _as_date(component.get("dtend"), tz)
        if not start_date:
            continue
        d = date.fromisoformat(start_date)
        if d < start_min or d > start_max:
            continue
        out.append(
            {
                "uid": str(component.get("uid", "") or ""),
                "summary": str(component.get("summary", "") or ""),
                "start_date": start_date,
                "end_date": end_date or start_date,
                "start": start_dt,
                "end": end_dt,
                "all_day": all_day,
                "location": str(component.get("location", "") or ""),
                "description": str(component.get("description", "") or ""),
            }
        )
    out.sort(key=lambda e: (e["start_date"], e["summary"].lower()))
    return out


def fetch(
    profile: dict[str, Any],
    *,
    url: str | None = None,
    days_back: int | None = None,
    days_forward: int | None = None,
    use_cache: bool = True,
) -> dict[str, Any]:
    cal = profile.get("calendario") or {}
    url = url or cal.get("ical_url")
    if not url:
        raise CalendarError("Manca calendario.ical_url nel profilo.")
    today = today_in_tz(profile)
    start_min = today - timedelta(days=days_back if days_back is not None else int(cal["giorni_indietro"]))
    start_max = today + timedelta(days=days_forward if days_forward is not None else int(cal["giorni_avanti"]))
    events = parse_events(fetch_ics(url, use_cache), profile["fuso_orario"], start_min, start_max)
    for ev in events:
        ev["kind"] = classify_title(profile, ev["summary"])
    return {"from": start_min.isoformat(), "to": start_max.isoformat(), "count": len(events), "events": events}


def match_to_archive(
    cal_events: list[dict[str, Any]],
    archive_events: list[Event],
    title_threshold: float = 0.4,
) -> list[dict[str, Any]]:
    """Abbina eventi del calendario all'archivio; ogni cartella al massimo una volta.

    Passo 1: stessa data e titolo simile (>= soglia), migliori punteggi prima.
    Passo 2: se in una data resta un solo evento di calendario e una sola cartella libera, li abbina
    (titoli scritti diversamente, es. soprannomi).
    """
    by_date: dict[str, list[Event]] = {}
    for ae in archive_events:
        by_date.setdefault(ae.date, []).append(ae)

    used: set[str] = set()
    assignments: dict[int, tuple[Event, float]] = {}
    scored: list[tuple[float, int, Event]] = []
    for i, ce in enumerate(cal_events):
        for ae in by_date.get(ce.get("start_date") or "") or []:
            score = title_similarity(ce.get("summary") or "", ae.title)
            if score >= title_threshold:
                scored.append((score, i, ae))
    scored.sort(key=lambda t: t[0], reverse=True)
    for score, i, ae in scored:
        if i not in assignments and ae.folder not in used:
            assignments[i] = (ae, score)
            used.add(ae.folder)

    unmatched_by_date: dict[str, list[int]] = {}
    for i, ce in enumerate(cal_events):
        if i not in assignments:
            unmatched_by_date.setdefault(ce.get("start_date") or "", []).append(i)
    for c_date, idxs in unmatched_by_date.items():
        free = [ae for ae in (by_date.get(c_date) or []) if ae.folder not in used]
        if len(idxs) == 1 and len(free) == 1:
            ae = free[0]
            assignments[idxs[0]] = (ae, title_similarity(cal_events[idxs[0]].get("summary") or "", ae.title))
            used.add(ae.folder)

    results: list[dict[str, Any]] = []
    for i, ce in enumerate(cal_events):
        if i in assignments:
            ae, score = assignments[i]
            status = "in_archivio" if score >= 0.75 else "cambiato"
            results.append({"status": status, "score": round(score, 3), "calendar": ce, "archive": ae.to_dict()})
        else:
            results.append({"status": "nuovo", "score": 0.0, "calendar": ce, "archive": None})
    for ae in archive_events:
        if ae.folder not in used:
            results.append({"status": "solo_archivio", "score": 1.0, "calendar": None, "archive": ae.to_dict()})
    return results


def summarize(matches: list[dict[str, Any]]) -> dict[str, int]:
    keys = ("nuovo", "cambiato", "in_archivio", "solo_archivio")
    return {k: sum(1 for m in matches if m["status"] == k) for k in keys}
