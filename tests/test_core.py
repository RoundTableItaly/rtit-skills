from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from rtit import archive, calendario, spese
from rtit.profile import (
    ProfileError,
    anno_sociale,
    calendar_is_ignored,
    classify_title,
    find_profile,
    inizio_anno_sociale,
    load_decisions,
    load_profile,
    save_decisions,
    title_similarity,
)

FIXTURES = Path(__file__).parent / "fixtures"


# --- profilo -----------------------------------------------------------------------


def test_anno_sociale_domenica_dopo_agm():
    # AGM 2026 = primo sabato di giugno (6/6): l'anno nuovo parte domenica 7/6
    assert inizio_anno_sociale(2026) == date(2026, 6, 7)
    assert anno_sociale(date(2026, 6, 6)) == "2025-2026"
    assert anno_sociale(date(2026, 6, 7)) == "2026-2027"
    assert anno_sociale(date(2026, 1, 15)) == "2025-2026"
    assert anno_sociale(date(2026, 12, 31)) == "2026-2027"
    # 2027: il primo sabato di giugno è il 5/6
    assert anno_sociale(date(2027, 6, 5)) == "2026-2027"
    assert anno_sociale(date(2027, 6, 6)) == "2027-2028"


def test_anno_sociale_agm_spostato():
    profile = {"agm": {"2025": "2025-06-14"}}
    assert inizio_anno_sociale(2025, profile) == date(2025, 6, 15)
    assert anno_sociale(date(2025, 6, 14), profile) == "2024-2025"
    assert anno_sociale(date(2025, 6, 15), profile) == "2025-2026"
    # senza override, il primo sabato di giugno 2025 è il 7/6
    assert anno_sociale(date(2025, 6, 8)) == "2025-2026"


def test_profile_agm_and_legacy_month(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    f = tmp_path / "p.yaml"
    # YAML legge chiavi e date senza virgolette come int e date: vanno normalizzate
    f.write_text("id: x\nmese_inizio_anno: 7\nagm:\n  2025: 2025-06-14\n", encoding="utf-8")
    p = load_profile(f)
    assert "mese_inizio_anno" not in p
    assert "mese_inizio_anno" in capsys.readouterr().err
    assert p["agm"] == {"2025": "2025-06-14"}
    assert anno_sociale(date(2025, 6, 14), p) == "2024-2025"
    f.write_text("id: x\nagm: {'2025': 'sabato'}\n", encoding="utf-8")
    with pytest.raises(ProfileError, match="agm"):
        load_profile(f)


def test_profile_defaults_and_lookup(profile_file: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("RTIT_PROFILO", str(profile_file))
    assert find_profile() == profile_file.resolve()
    p = load_profile()
    assert p["livello"] == "tavola"
    assert p["archivio"]["link"] == "markdown"
    assert archive.has_archive(p)
    assert p["app_rtit"]["soglia_punteggio"] == 90


def test_profile_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("RTIT_PROFILO", raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    with pytest.raises(ProfileError, match="rtit profilo nuovo"):
        find_profile()


def test_invalid_livello(tmp_path: Path):
    f = tmp_path / "p.yaml"
    f.write_text("id: x\nlivello: club\n", encoding="utf-8")
    with pytest.raises(ProfileError):
        load_profile(f)


@pytest.mark.parametrize(
    ("title", "kind"),
    [
        ("Ritrovo di giovedì", "ignora"),
        ("Consiglio di Tavola", "direttivo"),
        ("CD ottobre", "direttivo"),
        ("Cena di Natale RT 99", "sociale"),
        ("Visita al museo", "sociale"),
        ("Raccolta fondi in piazza", "altro"),
    ],
)
def test_classify_title(profile: dict, title: str, kind: str):
    assert classify_title(profile, title) == kind


def test_title_similarity_ignores_rt_prefix():
    assert title_similarity("RT 99 Cena da Mario", "Cena da Mario") == 1.0
    assert title_similarity("Grigliata da Mairo", "Grigliata da Mario") > 0.8


def test_decisions_live_next_to_profile(profile: dict, profile_file: Path):
    dec = load_decisions(profile)
    dec["calendario_ignora"].append({"titolo": "Aperitivo di benvenuto", "data": "2027-09-15", "uid": "u1"})
    path = save_decisions(profile, dec)
    assert path.parent == profile_file.parent
    assert calendar_is_ignored(load_decisions(profile), {"uid": "u1"})
    assert calendar_is_ignored(
        load_decisions(profile), {"summary": "aperitivo di BENVENUTO", "start_date": "2027-09-15"}
    )


# --- archivio e pack -------------------------------------------------------------------


def _new_event(profile: dict, d: date, title: str, pack: bool = True) -> archive.Event:
    root = archive.archive_root(profile)
    out = archive.write_event_note(profile, d, title, root, pack=pack, apply=True)
    assert out["action"] == "created"
    return archive.event_from_folder(profile, Path(out["note"]).parent, root)


def test_event_note_dry_run_does_not_write(profile: dict):
    root = archive.archive_root(profile)
    out = archive.write_event_note(profile, date(2026, 10, 10), "Cena", root)
    assert out["action"] == "would_create"
    assert not Path(out["note"]).exists()


def test_pack_roundtrip(profile: dict):
    root = archive.archive_root(profile)
    ev = _new_event(profile, date(2026, 10, 10), "Cena di inizio autunno")
    assert "Anni sociali/2026-2027/Eventi/2026-10-10 Cena di inizio autunno" in ev.folder.replace("\\", "/")
    written = archive.write_pack(profile, ev, root)
    assert set(written) == {"progetto.md", "invitati.md", "spese.md"}
    check = archive.validate_pack(Path(ev.folder))
    assert check["standard_ok"], check["issues"]
    assert "Completare dati evento" in check["open_todos"]
    progetto = Path(ev.folder, "progetto.md").read_text(encoding="utf-8")
    assert "[Nota evento](<2026-10-10 Cena di inizio autunno.md>)" in progetto
    assert "{{" not in progetto
    # non sovrascrive senza force
    assert archive.write_pack(profile, ev, root) == {}


def test_obsidian_links(profile: dict):
    profile["archivio"]["link"] = "wikilink"
    root = archive.archive_root(profile)
    ev = _new_event(profile, date(2026, 10, 10), "Cena")
    archive.write_pack(profile, ev, root)
    progetto = Path(ev.folder, "progetto.md").read_text(encoding="utf-8")
    assert "[[Anni sociali/2026-2027/Eventi/2026-10-10 Cena/2026-10-10 Cena|Nota evento]]" in progetto
    assert "[[Anni sociali/2026-2027/_Indice 2026-2027|Indice 2026-2027]]" in progetto


def test_scan_and_future(profile: dict):
    _new_event(profile, date(2020, 10, 10), "Passato")
    _new_event(profile, date(2099, 1, 10), "Futuro", pack=False)
    titles = [e.title for e in archive.scan_events(profile)]
    assert titles == ["Passato", "Futuro"]
    fut = archive.future_events(profile, on_or_after=date(2026, 1, 1))
    assert [e.title for e in fut] == ["Futuro"]
    assert archive.event_pack_required(fut[0].frontmatter) is False


def test_spese(profile: dict):
    root = archive.archive_root(profile)
    ev = _new_event(profile, date(2026, 10, 10), "Cena")
    archive.write_pack(profile, ev, root)
    inv = Path(ev.folder, "invitati.md")
    text = inv.read_text(encoding="utf-8").replace(
        "| | socio | tbd | | 25 | no | — | |",
        "| A | socio | sì | | 25 | sì | satispay | |\n| B | socio | sì | | 25 | no | — | |\n"
        "| C | esterno | tbd | | 30 | no | — | |",
    )
    inv.write_text(text, encoding="utf-8")
    res = spese.compute(Path(ev.folder))
    assert res["confermati"] == 2 and res["in_attesa"] == 1
    assert res["subtotale"] == 34.0  # (12 + 5) × 2
    assert res["totale_spesa"] == 37.4
    assert res["incasso_atteso"] == 50.0 and res["incassato"] == 25.0
    assert res["saldo"] == 12.6


# --- archivio condiviso: doppioni e struttura ----------------------------------------------


def test_event_creation_blocks_similar_folders(profile: dict):
    root = archive.archive_root(profile)
    _new_event(profile, date(2026, 10, 10), "Grigliata da Mairo")
    out = archive.write_event_note(profile, date(2026, 10, 10), "Grigliata da Mario", root, apply=True)
    assert out["action"] == "blocked_similar"
    assert out["similar"][0]["folder_name"] == "2026-10-10 Grigliata da Mairo"
    assert not Path(out["note"]).exists()
    forced = archive.write_event_note(profile, date(2026, 10, 10), "Grigliata da Mario", root, apply=True, force=True)
    assert forced["action"] == "created"
    assert archive.same_date_duplicates(profile) == [["2026-10-10 Grigliata da Mairo", "2026-10-10 Grigliata da Mario"]]


def test_find_similar_folders_other_date(profile: dict):
    root = archive.archive_root(profile)
    _new_event(profile, date(2026, 10, 10), "Cena d'autunno")
    similar = archive.find_similar_folders(profile, date(2026, 10, 24), "Cena di autunno", root)
    assert [s["folder_name"] for s in similar] == ["2026-10-10 Cena d'autunno"]
    assert similar[0]["reason"] == "fuzzy_title"
    assert archive.find_similar_folders(profile, date(2026, 10, 24), "Visita in cantina", root) == []
    out = archive.write_event_note(profile, date(2026, 10, 24), "Cena di autunno", root, apply=True)
    assert out["action"] == "blocked_similar"


def test_event_note_creates_event_subfolders(profile: dict):
    root = archive.archive_root(profile)
    dry = archive.write_event_note(profile, date(2027, 4, 17), "Visita in cantina", root)
    assert [Path(c).name for c in dry["cartelle"]] == ["Bollettini", "Form", "Altri documenti"]
    assert not Path(dry["note"]).parent.exists()
    ev = _new_event(profile, date(2027, 4, 17), "Visita in cantina")
    for sub in ("Bollettini", "Form", "Altri documenti"):
        assert (Path(ev.folder) / sub).is_dir()
    note = Path(ev.note_path).read_text(encoding="utf-8")
    assert "anno_sociale: 2026-2027" in note
    # una nota bollettino in Bollettini/ conta come bollettino e non diventa un evento
    assert not archive.has_bollettino(Path(ev.folder))
    (Path(ev.folder) / "Bollettini" / "Bollettino N.1.md").write_text(
        "---\ntipo: bollettino\nanno_sociale: 2026-2027\n---\n", encoding="utf-8"
    )
    (Path(ev.folder) / "Altri documenti" / "appunti.md").write_text("# Appunti\n", encoding="utf-8")
    assert archive.has_bollettino(Path(ev.folder))
    assert [e.title for e in archive.scan_events(profile)] == ["Visita in cantina"]
    assert archive.same_date_duplicates(profile) == []


def test_old_frontmatter_key_still_read(profile: dict):
    root = archive.archive_root(profile)
    ev = _new_event(profile, date(2026, 10, 10), "Cena")
    note = Path(ev.note_path)
    note.write_text(note.read_text(encoding="utf-8").replace("anno_sociale:", "anno_associativo:"), encoding="utf-8")
    assert archive.event_from_folder(profile, Path(ev.folder), root).anno_sociale == "2026-2027"


def test_legacy_profile_keys(tmp_path: Path):
    f = tmp_path / "p.yaml"
    f.write_text("id: x\narchivio: {tipo: obsidian, percorso: vault}\n", encoding="utf-8")
    p = load_profile(f)
    assert p["archivio"]["link"] == "wikilink" and archive.has_archive(p)
    f.write_text("id: x\narchivio: {tipo: nessuno, percorso: vault}\n", encoding="utf-8")
    assert not archive.has_archive(load_profile(f))


def test_year_structure(profile: dict):
    root = archive.archive_root(profile)
    dry = archive.ensure_year_structure(profile, "2026-2027", root)
    assert not any(e["esiste"] for e in dry["elementi"])
    assert not any(root.iterdir())
    archive.ensure_year_structure(profile, "2026-2027", root, apply=True)
    for sub in ("Statuto e regolamenti", "Fiscale e PEC", "Banca", "Loghi e modelli"):
        assert (root / "Documenti legali" / sub).is_dir()
    anno = root / "Anni sociali" / "2026-2027"
    assert sorted(p.name for p in anno.iterdir() if p.is_dir()) == ["Comunicazione", "Direttivo", "Eventi", "Tesoreria"]
    assert not (anno / "Bollettini").exists()
    indice = (anno / "_Indice 2026-2027.md").read_text(encoding="utf-8")
    for section in (
        "Eventi",
        "Bollettini",
        "Direttivo",
        "Tesoreria",
        "Comunicazione",
        "Note per il passaggio di consegne",
    ):
        assert f"## {section}\n" in indice
    # una seconda esecuzione non sovrascrive l'indice
    (anno / "_Indice 2026-2027.md").write_text("mio indice", encoding="utf-8")
    again = archive.ensure_year_structure(profile, "2026-2027", root, apply=True)
    assert all(e["esiste"] for e in again["elementi"])
    assert (anno / "_Indice 2026-2027.md").read_text(encoding="utf-8") == "mio indice"


# --- calendario ---------------------------------------------------------------------------


def test_calendar_parse_and_match(profile: dict):
    ics = (FIXTURES / "calendario.ics").read_bytes()
    events = calendario.parse_events(ics, "Europe/Rome", date(2026, 10, 1), date(2026, 12, 31))
    assert [e["summary"] for e in events] == [
        "Cena di inizio autunno",
        "Consiglio di Tavola",
        "Ritrovo",
        "Grigliata da Mario",
    ]
    assert events[0]["start"] == "2026-10-10T20:00:00+02:00"
    assert events[1]["all_day"] is True

    _new_event(profile, date(2026, 10, 10), "Cena inizio autunno")
    _new_event(profile, date(2026, 11, 7), "Grigliata da Mairo al lago")
    _new_event(profile, date(2026, 12, 1), "Solo archivio")
    matches = calendario.match_to_archive(events, archive.scan_events(profile))
    by_title = {(m["calendar"]["summary"] if m["calendar"] else m["archive"]["title"]): m["status"] for m in matches}
    assert by_title["Cena di inizio autunno"] == "in_archivio"
    assert by_title["Grigliata da Mario"] in {"in_archivio", "cambiato"}
    assert by_title["Consiglio di Tavola"] == "nuovo"
    assert by_title["Solo archivio"] == "solo_archivio"
