"""App Round Table Italia (app.roundtable.it): prossimi eventi e collisioni del Planner.

API pubblica in sola lettura, nessuna autenticazione. Schema: https://app.roundtable.it/api/schema/
Il punteggio del Planner è su scala 0–100 (più alto = meno sovrapposizioni): mostrarlo sempre come N/100.
"""

from __future__ import annotations

import os
from datetime import date
from typing import Any
from urllib.parse import urljoin

from . import __version__
from .archive import Event
from .profile import today_in_tz

DEFAULT_BASE = "https://app.roundtable.it/api/v1"
TIMEOUT = 30
WARN_SEVERITIES = frozenset({"danger", "warning"})
USER_AGENT = f"rtit-skills/{__version__} (+https://github.com/RoundTableItaly/rtit-skills)"


class AppRtitError(Exception):
    pass


def config(profile: dict[str, Any]) -> dict[str, Any]:
    cfg = dict(profile.get("app_rtit") or {})
    cfg["base_url"] = (os.environ.get("APP_RTIT_BASE_URL") or cfg.get("base_url") or DEFAULT_BASE).rstrip("/")
    cfg.setdefault("organization_unit_slug", "")
    cfg.setdefault("area_slug", "")
    cfg.setdefault("mesi_planner", 3)
    cfg.setdefault("soglia_punteggio", 90)
    return cfg


def require_org_id(cfg: dict[str, Any]) -> int:
    if not cfg.get("organization_unit_id"):
        raise AppRtitError(
            "Manca app_rtit.organization_unit_id nel profilo. Usa `rtit app-rtit unita --cerca <nome>` per trovarlo."
        )
    return int(cfg["organization_unit_id"])


def session():
    import requests

    s = requests.Session()
    s.headers.update({"Accept": "application/json", "User-Agent": USER_AGENT})
    return s


def _get(sess, base: str, path: str, params: dict[str, Any] | None = None) -> Any:
    resp = sess.get(urljoin(base.rstrip("/") + "/", path.lstrip("/")), params=params or {}, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _paginate(sess, base: str, path: str, params: dict[str, Any], max_pages: int = 50) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for page in range(1, max_pages + 1):
        data = _get(sess, base, path, {**params, "page": page, "page_size": 100})
        if isinstance(data, list):
            return results + data
        results.extend(data.get("results") or [])
        if not data.get("next"):
            break
    return results


def search_units(sess, base: str, query: str) -> list[dict[str, Any]]:
    """Cerca tavole/zone per nome o slug (per l'onboarding)."""
    rows = _paginate(sess, base, "organization-units/", {"search": query}, max_pages=5)
    q = query.lower()
    out = []
    for r in rows:
        name = str(r.get("name") or "")
        slug = str(r.get("slug") or "")
        if q in name.lower() or q in slug.lower() or not q:
            out.append({k: r.get(k) for k in ("id", "name", "slug", "type", "parent", "parent_slug") if k in r})
    return out


def fetch_upcoming_unit(sess, base: str, slug: str, *, scope: str = "subtree") -> list[dict[str, Any]]:
    if not slug:
        return []
    return _paginate(
        sess,
        base,
        f"organization-units/{slug}/activities/",
        {"time_scope": "upcoming", "scope": scope, "ordering": "start_date"},
    )


def fetch_national_upcoming(sess, base: str, today: date) -> list[dict[str, Any]]:
    """L'elenco nazionale non ha time_scope: si scorre per data crescente tenendo solo il futuro."""
    results: list[dict[str, Any]] = []
    for page in range(1, 81):
        data = _get(sess, base, "activities/", {"ordering": "start_date", "page": page, "page_size": 100})
        batch = data.get("results") or []
        if not batch:
            break
        try:
            last_d = date.fromisoformat((batch[-1].get("start_date") or "")[:10])
        except ValueError:
            last_d = today
        if last_d >= today:
            for row in batch:
                try:
                    if date.fromisoformat((row.get("start_date") or "")[:10]) >= today:
                        results.append(row)
                except ValueError:
                    continue
        if not data.get("next") or len(results) >= 200:
            break
    return results


def conflict_check_day(sess, base: str, org_id: int, day: date) -> dict[str, Any]:
    return _get(sess, base, "conflict-check/", {"date": day.isoformat(), "organization_unit_id": org_id})


def conflict_check_month(sess, base: str, org_id: int, year: int, month: int) -> dict[str, Any]:
    return _get(sess, base, "conflict-check/month/", {"year": year, "month": month, "organization_unit_id": org_id})


def month_iter(start: date, months: int) -> list[tuple[int, int]]:
    out = []
    y, m = start.year, start.month
    for _ in range(max(1, months)):
        out.append((y, m))
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out


def day_is_interesting(day_data: dict[str, Any], soglia: int) -> bool:
    try:
        score = int(day_data.get("score", 100))
    except (TypeError, ValueError):
        score = 100
    if score < soglia:
        return True
    for c in day_data.get("conflicts") or []:
        if isinstance(c, dict) and (c.get("severity") in WARN_SEVERITIES or int(c.get("impact") or 0) <= -10):
            return True
    return False


def summarize_activity(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "slug": row.get("slug"),
        "start_date": row.get("start_date"),
        "end_date": row.get("end_date"),
        "organization_name": row.get("organization_name"),
        "organization_unit_slug": row.get("organization_unit_slug"),
        "location": row.get("location"),
        "type": row.get("type"),
        "url": f"/activity/{row['slug']}/" if row.get("slug") else None,
    }


def summarize_conflict(c: Any) -> dict[str, Any] | str:
    if not isinstance(c, dict):
        return str(c)
    keys = ("event_id", "name", "organizer", "zone", "distance", "impact", "reason", "severity", "url", "start_time")
    return {k: c.get(k) for k in keys}


def build_heatmap(sess, base: str, org_id: int, today: date, months: int, soglia: int) -> dict[str, Any]:
    interesting: list[dict[str, Any]] = []
    keys = []
    for y, m in month_iter(today, months):
        keys.append(f"{y:04d}-{m:02d}")
        for day_key, day_data in sorted(conflict_check_month(sess, base, org_id, y, m).items()):
            if day_key >= today.isoformat() and day_is_interesting(day_data, soglia):
                interesting.append(
                    {
                        "date": day_key,
                        "score": day_data.get("score"),
                        "has_events": day_data.get("has_events"),
                        "conflicts": [summarize_conflict(c) for c in (day_data.get("conflicts") or [])],
                    }
                )
    return {"months": keys, "interesting_days": interesting}


def check_dates(sess, base: str, org_id: int, events: list[Event], soglia: int) -> list[dict[str, Any]]:
    rows = []
    for ev in events:
        try:
            d = date.fromisoformat(ev.date)
        except ValueError:
            continue
        raw = conflict_check_day(sess, base, org_id, d)
        rows.append(
            {
                "date": ev.date,
                "title": ev.title,
                "folder": ev.folder_name,
                "score": raw.get("score"),
                "at_risk": day_is_interesting(
                    {"score": raw.get("score", 100), "conflicts": raw.get("conflicts")}, soglia
                ),
                "conflicts": [summarize_conflict(c) for c in (raw.get("conflicts") or [])],
            }
        )
    return rows


def _conflict_lines(conflicts: list[Any], limit: int) -> list[str]:
    out = []
    for c in conflicts[:limit]:
        if isinstance(c, dict):
            out.append(f"  - [{c.get('severity')}] {c.get('name')} ({c.get('organizer')}) — {c.get('reason')}")
        else:
            out.append(f"  - {c}")
    return out


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "## App RTIT — Planner",
        "",
        f"Unità `{report.get('organization_unit_slug')}` (id {report.get('organization_unit_id')}) · "
        f"oggi {report.get('today')}",
        "",
    ]
    area = report.get("upcoming_area") or []
    lines += [f"### Prossimi eventi — zona ({len(area)})", ""]
    lines += [
        f"- {(a.get('start_date') or '')[:10]} — **{a.get('organization_name')}**: {a.get('name')}" for a in area[:20]
    ]
    if not area:
        lines.append("- (nessuno)")
    lines.append("")
    club = report.get("upcoming_club") or []
    if club:
        lines += [f"### Prossimi eventi — tavola ({len(club)})", ""]
        lines += [f"- {(a.get('start_date') or '')[:10]} — {a.get('name')}" for a in club[:10]]
        lines.append("")
    checks = report.get("date_checks") or []
    at_risk = [r for r in checks if r.get("at_risk")]
    lines += [f"### Collisioni sulle nostre date ({len(at_risk)} a rischio su {len(checks)})", ""]
    if not checks:
        lines.append("- Nessuna data futura da controllare (archivio vuoto o non configurato).")
    elif not at_risk:
        lines.append("- Nessuna collisione rilevante sulle nostre date.")
    for r in at_risk:
        lines.append(f"- **{r['date']}** {r.get('title')} — punteggio {r.get('score')}/100")
        lines += _conflict_lines(r.get("conflicts") or [], 3)
    lines.append("")
    interesting = (report.get("heatmap") or {}).get("interesting_days") or []
    lines += [f"### Giorni sensibili nei prossimi mesi ({len(interesting)})", ""]
    if not interesting:
        lines.append("- Nessun giorno sotto soglia.")
    for d in interesting[:25]:
        lines.append(f"- **{d['date']}** punteggio {d.get('score')}/100")
        lines += _conflict_lines(d.get("conflicts") or [], 2)
    lines.append("")
    national = report.get("upcoming_national") or []
    if national:
        lines += [f"### Prossimi eventi nazionali ({min(len(national), 15)} di {len(national)})", ""]
        lines += [
            f"- {(a.get('start_date') or '')[:10]} — **{a.get('organization_name')}**: {a.get('name')}"
            for a in national[:15]
        ]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def report(
    profile: dict[str, Any],
    events: list[Event],
    *,
    months: int | None = None,
    include_national: bool = False,
) -> dict[str, Any]:
    import requests

    cfg = config(profile)
    org_id = require_org_id(cfg)
    base = cfg["base_url"]
    today = today_in_tz(profile)
    soglia = int(cfg["soglia_punteggio"])
    months = int(months or cfg["mesi_planner"])
    sess = session()
    errors: list[dict[str, str]] = []
    out: dict[str, Any] = {
        "today": today.isoformat(),
        "base_url": base,
        "organization_unit_id": org_id,
        "organization_unit_slug": cfg.get("organization_unit_slug"),
        "area_slug": cfg.get("area_slug"),
        "soglia_punteggio": soglia,
        "mesi_planner": months,
        "upcoming_area": [],
        "upcoming_club": [],
        "upcoming_national": [],
        "heatmap": {"months": [], "interesting_days": []},
        "date_checks": [],
    }
    steps = [
        ("upcoming_area", lambda: [summarize_activity(r) for r in fetch_upcoming_unit(sess, base, cfg["area_slug"])]),
        (
            "upcoming_club",
            lambda: [
                summarize_activity(r)
                for r in fetch_upcoming_unit(sess, base, cfg["organization_unit_slug"], scope="exact")
            ],
        ),
        ("heatmap", lambda: build_heatmap(sess, base, org_id, today, months, soglia)),
        ("date_checks", lambda: check_dates(sess, base, org_id, events, soglia)),
    ]
    if include_national:
        steps.append(
            ("upcoming_national", lambda: [summarize_activity(r) for r in fetch_national_upcoming(sess, base, today)])
        )
    for key, fn in steps:
        try:
            out[key] = fn()
        except requests.RequestException as exc:
            errors.append({"step": key, "error": str(exc)})
    out["errors"] = errors
    out["markdown"] = render_markdown(out)
    return out
