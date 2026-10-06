"""CLI `rtit`: gli strumenti che le skill chiamano quando l'assistente ha un terminale.

Ogni comando è in sola lettura, tranne:

- `profilo nuovo` (crea il file profilo, non sovrascrive);
- `evento nuovo` e `archivio struttura` (scrivono solo con `--applica`);
- `evento pack` (crea progetto/invitati/spese mancanti; sovrascrive solo con `--force`);
- `bollettino` (scrive DOCX/PDF accanto alla nota o in `--out-dir`; sovrascrive solo con `--force`);
- `decisioni ignora-calendario` (aggiorna il file delle decisioni accanto al profilo).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Any

from . import __version__

EXAMPLE_PROFILE = Path(__file__).parent / "templates" / "profilo-esempio.yaml"


def _print(data: Any, as_json: bool = True) -> None:
    if not as_json and isinstance(data, dict) and "markdown" in data:
        print(data["markdown"])
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def _common() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--profilo", help="File profilo YAML (default: $RTIT_PROFILO o ./rtit-profilo.yaml)")
    p.add_argument("--archivio", help="Cartella dell'archivio condiviso (sovrascrive archivio.percorso)")
    p.add_argument("--json", action="store_true", help="Output JSON completo invece del markdown")
    return p


def build_parser() -> argparse.ArgumentParser:
    common = _common()
    parser = argparse.ArgumentParser(prog="rtit", description="Strumenti AI per i direttivi Round Table Italia")
    parser.add_argument("--version", action="version", version=f"rtit {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("profilo", parents=[common], help="Mostra o verifica il profilo")
    p.add_argument("azione", nargs="?", choices=["mostra", "verifica", "nuovo"], default="verifica")
    p.add_argument("destinazione", nargs="?", help="Per `nuovo`: dove creare il file (default ./rtit-profilo.yaml)")

    p = sub.add_parser("eventi", parents=[common], help="Elenca gli eventi dell'archivio")
    p.add_argument("--futuri", action="store_true")

    p = sub.add_parser("evento", parents=[common], help="Nota evento, pack progetto/invitati/spese, spese")
    ev = p.add_subparsers(dest="azione", required=True)
    q = ev.add_parser("nuovo", parents=[common], help="Crea cartella + nota evento (dry-run senza --applica)")
    q.add_argument("--data", required=True, help="AAAA-MM-GG")
    q.add_argument("--titolo", required=True)
    q.add_argument("--senza-pack", action="store_true", help="Evento solo bollettino (pack: none)")
    q.add_argument("--applica", action="store_true")
    q.add_argument("--force", action="store_true", help="Crea anche se esiste una cartella simile (solo su conferma)")
    q = ev.add_parser("pack", parents=[common], help="Scrive progetto/invitati/spese (non sovrascrive)")
    q.add_argument("cartella")
    q.add_argument("--force", action="store_true", help="Sovrascrive file esistenti (solo su conferma)")
    q = ev.add_parser("verifica", parents=[common], help="Controlla il pack di un evento")
    q.add_argument("cartella")
    q = ev.add_parser("spese", parents=[common], help="Calcola spese e saldo da spese.md + invitati.md")
    q.add_argument("cartella")
    q.add_argument("--n", type=int, default=None, help="Numero partecipanti (sovrascrive i confermati)")

    p = sub.add_parser("calendario", parents=[common], help="Legge il calendario iCal e lo confronta con l'archivio")
    p.add_argument("--url", help="URL iCal (sovrascrive calendario.ical_url)")
    p.add_argument("--giorni-indietro", type=int)
    p.add_argument("--giorni-avanti", type=int)
    p.add_argument("--no-cache", action="store_true")

    p = sub.add_parser("app-rtit", parents=[common], help="App RTIT: prossimi eventi e collisioni del Planner")
    ar = p.add_subparsers(dest="azione", required=True)
    q = ar.add_parser("report", parents=[common], help="Report completo")
    q.add_argument("--mesi", type=int)
    q.add_argument("--nazionali", action="store_true")
    q = ar.add_parser("prossimi", parents=[common], help="Prossimi eventi di zona/tavola")
    q.add_argument("--nazionali", action="store_true")
    q = ar.add_parser("planner", parents=[common], help="Giorni sensibili nei prossimi mesi")
    q.add_argument("--mesi", type=int)
    q = ar.add_parser("data", parents=[common], help="Collisioni per una data proposta")
    q.add_argument("giorno", help="AAAA-MM-GG")
    q = ar.add_parser("unita", parents=[common], help="Cerca l'id di una tavola o zona (onboarding)")
    q.add_argument("--cerca", required=True)

    p = sub.add_parser("archivio", parents=[common], help="Archivio condiviso: struttura dell'anno e doppioni")
    ac = p.add_subparsers(dest="azione", required=True)
    q = ac.add_parser("verifica", parents=[common], help="Cartelle evento con la stessa data (possibili doppioni)")
    q = ac.add_parser(
        "struttura", parents=[common], help="Documenti legali e cartelle dell'anno sociale (dry-run senza --applica)"
    )
    q.add_argument("--anno", help="AAAA-AAAA (default: anno sociale corrente)")
    q.add_argument("--applica", action="store_true")

    p = sub.add_parser(
        "bollettino",
        parents=[common],
        help="Genera DOCX/PDF del bollettino accanto alla nota (in <evento>/Bollettini/; scrive file)",
    )
    p.add_argument("--md", type=Path, help="Nota bollettino .md (di norma in <evento>/Bollettini/)")
    p.add_argument("--json-contesto", type=Path, help="Contesto JSON al posto della nota")
    p.add_argument(
        "--out-dir",
        type=Path,
        help="Cartella di uscita (default: la cartella della nota; per le prove usa una cartella di anteprima)",
    )
    p.add_argument("--basename")
    p.add_argument("--template", type=Path)
    p.add_argument("--no-pdf", action="store_true")
    p.add_argument("--force", action="store_true", help="Sovrascrive DOCX/PDF esistenti (solo su conferma)")

    p = sub.add_parser("cosa-fare", parents=[common], help="Report unico: eventi, archivio, calendario, App RTIT")
    p.add_argument("--salta-calendario", action="store_true")
    p.add_argument("--salta-app-rtit", action="store_true")

    p = sub.add_parser("decisioni", parents=[common], help="Decisioni salvate (eventi del calendario da ignorare)")
    dc = p.add_subparsers(dest="azione", required=True)
    dc.add_parser("mostra", parents=[common])
    q = dc.add_parser("ignora-calendario", parents=[common])
    q.add_argument("--titolo", required=True)
    q.add_argument("--data", required=True)
    q.add_argument("--uid")
    q.add_argument("--motivo", default="")

    return parser


def _root(args: argparse.Namespace) -> Path | None:
    return Path(args.archivio).expanduser().resolve() if getattr(args, "archivio", None) else None


def cmd_profilo(args: argparse.Namespace) -> int:
    from .profile import ProfileError, load_profile, public_view

    if args.azione == "nuovo":
        dest = Path(args.destinazione or "rtit-profilo.yaml")
        if dest.exists():
            print(f"Esiste già: {dest} (non lo sovrascrivo)", file=sys.stderr)
            return 1
        shutil.copy2(EXAMPLE_PROFILE, dest)
        print(f"Creato {dest}: compilalo (o fallo compilare dalla skill rt-primi-passi).")
        return 0
    try:
        profile = load_profile(args.profilo)
    except ProfileError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.azione == "mostra":
        _print(public_view(profile))
        return 0
    from .archive import ArchiveError, archive_root
    from .profile import direttivo_member

    try:
        archivio_ok = archive_root(profile, args.archivio).is_dir()
    except ArchiveError:
        archivio_ok = False
    checks = {
        "archivio": archivio_ok,
        "calendario": bool(profile["calendario"].get("ical_url")),
        "app_rtit": bool(profile["app_rtit"].get("organization_unit_id")),
        "firma_presidente": bool(direttivo_member(profile, "presidente")),
        "firma_segretario": bool(direttivo_member(profile, "segretario")),
        "intestazione": bool(profile["intestazione"]),
    }
    lines = [
        f"## Profilo `{profile['id']}` — {profile.get('nome', '')} ({profile['livello']})",
        "",
        f"File: `{profile['_path']}`",
        "",
    ]
    labels = {
        "archivio": "Archivio condiviso della tavola (rt-archivio, rt-evento, rt-cosa-fare)",
        "calendario": "Calendario iCal (rt-calendario)",
        "app_rtit": "App RTIT / Planner collisioni (rt-calendario)",
        "firma_presidente": "Firma Presidente nel direttivo (rt-bollettino)",
        "firma_segretario": "Firma Segretario nel direttivo (rt-bollettino)",
        "intestazione": "Intestazione bollettino (sede, ritrovi, charter…)",
    }
    lines += [f"- {'✅' if ok else '➖'} {labels[k]}" for k, ok in checks.items()]
    if profile["archivio"].get("percorso") and not archivio_ok:
        lines.append(
            "  - archivio.percorso è impostato ma la cartella non esiste: il client del cloud è avviato? "
            "Il percorso è giusto?"
        )
    _print({"profile": profile["id"], "checks": checks, "markdown": "\n".join(lines) + "\n"}, args.json)
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    args = build_parser().parse_args(argv)
    if args.cmd == "profilo":
        return cmd_profilo(args)

    from .profile import ProfileError, load_profile

    try:
        profile = load_profile(args.profilo)
    except ProfileError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    try:
        return _dispatch(args, profile)
    except Exception as exc:  # noqa: BLE001 — errore leggibile per l'assistente, non traceback
        name = type(exc).__name__
        if name in {"ArchiveError", "BollettinoError", "CalendarError", "AppRtitError", "FileNotFoundError"}:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
            return 1
        raise


def _dispatch(args: argparse.Namespace, profile: dict[str, Any]) -> int:
    from . import archive

    root = _root(args)

    if args.cmd == "eventi":
        r = root or archive.archive_root(profile)
        events = archive.future_events(profile, r) if args.futuri else archive.scan_events(profile, r)
        _print([e.to_dict() for e in events])
        return 0

    if args.cmd == "evento":
        r = root or archive.archive_root(profile)
        if args.azione == "nuovo":
            _print(
                archive.write_event_note(
                    profile,
                    date.fromisoformat(args.data),
                    args.titolo,
                    r,
                    pack=not args.senza_pack,
                    apply=args.applica,
                    force=args.force,
                )
            )
            return 0
        folder = Path(args.cartella).expanduser().resolve()
        if args.azione == "verifica":
            _print(archive.validate_pack(folder))
        elif args.azione == "pack":
            ev = archive.event_from_folder(profile, folder, r)
            _print(archive.write_pack(profile, ev, r, force=args.force))
        elif args.azione == "spese":
            from .spese import compute

            _print(compute(folder, args.n, float(profile.get("quota_default", 25))))
        return 0

    if args.cmd == "calendario":
        from . import calendario

        cal = calendario.fetch(
            profile,
            url=args.url,
            days_back=args.giorni_indietro,
            days_forward=args.giorni_avanti,
            use_cache=not args.no_cache,
        )
        if root or archive.has_archive(profile):
            matches = calendario.match_to_archive(cal["events"], archive.scan_events(profile, root))
            cal["matches"], cal["summary"] = matches, calendario.summarize(matches)
        from .profile import load_decisions
        from .report import calendar_markdown

        cal["markdown"] = calendar_markdown(cal, load_decisions(profile))
        _print(cal, args.json)
        return 0

    if args.cmd == "app-rtit":
        return _app_rtit(args, profile, root)

    if args.cmd == "archivio":
        r = root or archive.archive_root(profile)
        if args.azione == "verifica":
            groups = archive.same_date_duplicates(profile, r)
            _print({"archivio": str(r), "duplicati_stessa_data": groups})
            return 0
        from .profile import anno_sociale, today_in_tz

        anno = args.anno or anno_sociale(today_in_tz(profile), profile)
        _print(archive.ensure_year_structure(profile, anno, r, apply=args.applica))
        return 0

    if args.cmd == "bollettino":
        from . import bollettino

        ctx = json.loads(args.json_contesto.read_text(encoding="utf-8")) if args.json_contesto else None
        out = bollettino.render(
            profile,
            md=args.md.expanduser().resolve() if args.md else None,
            context=ctx,
            out_dir=args.out_dir,
            basename=args.basename,
            template=args.template,
            pdf=not args.no_pdf,
            force=args.force,
        )
        _print(out)
        return 0

    if args.cmd == "cosa-fare":
        from .report import cosa_fare

        out = cosa_fare(
            profile,
            root=root,
            skip_calendar=args.salta_calendario,
            skip_app_rtit=args.salta_app_rtit,
        )
        _print(out, args.json)
        return 0

    if args.cmd == "decisioni":
        from .profile import decisions_markdown, decisions_path, load_decisions, save_decisions

        dec = load_decisions(profile)
        if args.azione == "ignora-calendario":
            dec["calendario_ignora"].append(
                {
                    "uid": args.uid,
                    "titolo": args.titolo,
                    "data": args.data,
                    "motivo": args.motivo,
                    "deciso": date.today().isoformat(),
                }
            )
            save_decisions(profile, dec)
        path = decisions_path(profile)
        _print({"file": str(path), "decisioni": dec, "markdown": decisions_markdown(dec, path)}, args.json)
        return 0
    return 1


def _app_rtit(args: argparse.Namespace, profile: dict[str, Any], root: Path | None) -> int:
    from . import app_rtit, archive
    from .profile import today_in_tz

    cfg = app_rtit.config(profile)
    sess = app_rtit.session()
    base = cfg["base_url"]
    if args.azione == "unita":
        _print(app_rtit.search_units(sess, base, args.cerca))
        return 0
    if args.azione == "report":
        events = archive.future_events(profile, root) if (root or archive.has_archive(profile)) else []
        out = app_rtit.report(profile, events, months=args.mesi, include_national=args.nazionali)
        _print(out, args.json)
        return 1 if out["errors"] else 0
    today = today_in_tz(profile)
    if args.azione == "prossimi":
        out = {
            "upcoming_area": [
                app_rtit.summarize_activity(r) for r in app_rtit.fetch_upcoming_unit(sess, base, cfg["area_slug"])
            ],
            "upcoming_club": [
                app_rtit.summarize_activity(r)
                for r in app_rtit.fetch_upcoming_unit(sess, base, cfg["organization_unit_slug"], scope="exact")
            ],
            "upcoming_national": [
                app_rtit.summarize_activity(r) for r in app_rtit.fetch_national_upcoming(sess, base, today)
            ]
            if args.nazionali
            else [],
        }
        _print(out)
        return 0
    org_id = app_rtit.require_org_id(cfg)
    if args.azione == "planner":
        _print(
            app_rtit.build_heatmap(
                sess, base, org_id, today, int(args.mesi or cfg["mesi_planner"]), int(cfg["soglia_punteggio"])
            )
        )
        return 0
    raw = app_rtit.conflict_check_day(sess, base, org_id, date.fromisoformat(args.giorno))
    _print(
        {
            "date": args.giorno,
            "score": raw.get("score"),
            "punteggio": f"{raw.get('score')}/100",
            "conflicts": [app_rtit.summarize_conflict(c) for c in (raw.get("conflicts") or [])],
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
