from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from docx import Document

from rtit import app_rtit, archive, bollettino
from rtit.cli import main


def _docx_text(path: Path) -> str:
    doc = Document(str(path))
    texts = [p.text for p in doc.paragraphs]
    for box in doc.element.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}txbxContent"):
        texts += [
            "".join(t.text or "" for t in box.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"))
        ]
    return "\n".join(texts)


def test_bollettino_context_uses_profile_for_missing_signature(profile: dict, bollettino_md: Path):
    ctx = bollettino.build_context_from_md(bollettino_md, profile)
    assert ctx["presidente"] == "Mario Rossi"
    assert ctx["segretario"] == "Giovanni Neri"  # dal direttivo nel profilo
    assert ctx["titolo"] == "VISITA IN CANTINA (CON DEGUSTAZIONE)"
    assert ctx["aperta_a"] == "Tablers, ex Tablers e aspiranti"
    assert ctx["corpo_righe"] == [
        "Visita guidata e degustazione con i produttori.",
        "Posti limitati: conferma entro la scadenza",
    ]
    assert ctx["anno_sociale"] == "2026-2027"
    assert ctx["destinatari_pc"][0] == "e p.c. al Presidente Nazionale RTIT"
    assert ctx["destinatari_pc"][-1] == "ai Presidenti delle Tavole della Zona N"


def test_bollettino_default_aperta_a(profile: dict, bollettino_md: Path):
    profile["bollettino"].pop("aperta_a", None)
    text = bollettino_md.read_text(encoding="utf-8").replace("- Aperta a: Tablers, ex Tablers e aspiranti\n", "")
    bollettino_md.write_text(text, encoding="utf-8")
    assert bollettino.build_context_from_md(bollettino_md, profile)["aperta_a"] == bollettino.DEFAULT_APERTA_A
    assert bollettino.DEFAULT_APERTA_A == "Tablers, ex Tablers, aspiranti e amici"


def test_bollettino_requires_md_or_json_contesto(profile: dict):
    with pytest.raises(bollettino.BollettinoError, match="--json-contesto"):
        bollettino.render(profile)


def test_bollettino_requires_signature(profile: dict, bollettino_md: Path):
    profile["direttivo"]["membri"] = []
    text = bollettino_md.read_text(encoding="utf-8").replace("- **Presidente**: Mario Rossi — +39 000 000 0001", "")
    bollettino_md.write_text(text, encoding="utf-8")
    with pytest.raises(bollettino.BollettinoError, match="Presidente"):
        bollettino.build_context_from_md(bollettino_md, profile)


def test_bollettino_render_docx(profile: dict, bollettino_md: Path, tmp_path: Path):
    root = archive.archive_root(profile)
    before = sorted(p.relative_to(root) for p in root.rglob("*"))
    out = bollettino.render(profile, md=bollettino_md, out_dir=tmp_path / "out", pdf=False)
    assert "copie" not in out
    assert Path(out["docx"]).parent == tmp_path / "out"
    assert sorted(p.relative_to(root) for p in root.rglob("*")) == before  # l'anteprima non tocca l'archivio
    text = _docx_text(Path(out["docx"]))
    for expected in (
        "ROUND TABLE N.99 ESEMPIO",
        "Esempio, 03/04/2027",
        "Bollettino N. 1 anno 2026/2027",
        "Hotel Esempio",
        "Vicepresidente",
        "Luca Bianchi",
        "Presidente RT 99 Esempio",
        "e p.c. al Presidente Nazionale RTIT",
        "Round Table 99 – Esempio",
        "Cantina Esempio",
        "Tablers, ex Tablers e aspiranti",
    ):
        assert expected in text, expected
    assert "{{" not in text and "{%" not in text
    with pytest.raises(bollettino.BollettinoError, match="--force"):
        bollettino.render(profile, md=bollettino_md, out_dir=tmp_path / "out", pdf=False)


def test_bollettino_written_in_event_bollettini_folder(profile_file: Path, profile: dict, bollettino_md: Path):
    root = archive.archive_root(profile)
    created = archive.write_event_note(profile, date(2027, 4, 17), "Visita in cantina", root, apply=True)
    boll_dir = Path(created["note"]).parent / "Bollettini"
    md = boll_dir / bollettino_md.name
    md.write_text(bollettino_md.read_text(encoding="utf-8"), encoding="utf-8")
    assert main(["bollettino", "--profilo", str(profile_file), "--md", str(md), "--no-pdf"]) == 0
    assert sorted(p.name for p in boll_dir.iterdir()) == sorted([md.name, f"{md.stem}.docx"])
    # nessuna copia altrove nell'archivio
    docx = [p for p in root.rglob("*.docx")]
    assert docx == [boll_dir / f"{md.stem}.docx"]
    assert archive.has_bollettino(Path(created["note"]).parent)


def test_cli_bollettino_has_no_copy_flag(profile_file: Path, bollettino_md: Path):
    with pytest.raises(SystemExit):
        main(["bollettino", "--profilo", str(profile_file), "--md", str(bollettino_md), "--no-copia"])


def test_app_rtit_report_offline(profile: dict, monkeypatch: pytest.MonkeyPatch):
    profile["app_rtit"].update(
        {"organization_unit_id": 1, "organization_unit_slug": "rt-99-esempio", "area_slug": "zona-esempio"}
    )
    today = date.today().isoformat()

    def fake_get(sess, base, path, params=None):
        if path.startswith("organization-units/"):
            return {
                "results": [
                    {"id": 1, "name": "Cena di zona", "slug": "cena", "start_date": today, "organization_name": "RT 98"}
                ],
                "next": None,
            }
        if path == "conflict-check/month/":
            return {
                today: {
                    "score": 30,
                    "has_events": True,
                    "conflicts": [
                        {"name": "AGM", "severity": "danger", "organizer": "RTIT", "reason": "Evento nazionale"}
                    ],
                }
            }
        return {"score": 100, "conflicts": []}

    monkeypatch.setattr(app_rtit, "_get", fake_get)
    rep = app_rtit.report(profile, [])
    assert rep["errors"] == []
    assert rep["heatmap"]["interesting_days"][0]["score"] == 30
    assert "30/100" in rep["markdown"]
    assert "Cena di zona" in rep["markdown"]


def test_cli_profilo_and_cosa_fare(profile_file: Path, capsys: pytest.CaptureFixture[str]):
    assert main(["profilo", "verifica", "--profilo", str(profile_file), "--json"]) == 0
    checks = json.loads(capsys.readouterr().out)["checks"]
    assert checks["archivio"] and checks["firma_presidente"] and not checks["app_rtit"]

    assert (
        main(
            ["evento", "nuovo", "--profilo", str(profile_file), "--data", "2099-05-01", "--titolo", "Cena", "--applica"]
        )
        == 0
    )
    capsys.readouterr()
    assert main(["cosa-fare", "--profilo", str(profile_file), "--salta-calendario", "--salta-app-rtit"]) == 0
    out = capsys.readouterr().out
    assert "2099-05-01 Cena" in out
    assert "Pack: manca" in out


def test_cli_profilo_verifica_archivio_mancante(profile_file: Path, capsys: pytest.CaptureFixture[str]):
    (profile_file.parent / "archivio").rmdir()
    assert main(["profilo", "verifica", "--profilo", str(profile_file)]) == 0
    out = capsys.readouterr().out
    assert "➖ Archivio condiviso" in out and "client del cloud" in out
    assert main(["profilo", "verifica", "--profilo", str(profile_file), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["checks"]["archivio"] is False


def test_cli_archivio_struttura_e_verifica(profile_file: Path, capsys: pytest.CaptureFixture[str]):
    root = profile_file.parent / "archivio"
    base = ["archivio", "struttura", "--profilo", str(profile_file), "--anno", "2026-2027"]
    assert main(base) == 0
    dry = json.loads(capsys.readouterr().out)
    assert dry["applica"] is False and not any(root.iterdir())
    assert main([*base, "--applica"]) == 0
    capsys.readouterr()
    assert (root / "Documenti legali" / "Banca").is_dir()
    assert (root / "Anni sociali" / "2026-2027" / "Comunicazione").is_dir()
    assert (root / "Anni sociali" / "2026-2027" / "_Indice 2026-2027.md").is_file()

    nuovo = ["evento", "nuovo", "--profilo", str(profile_file), "--data", "2027-04-17", "--applica"]
    assert main([*nuovo, "--titolo", "Visita in cantina"]) == 0
    assert json.loads(capsys.readouterr().out)["action"] == "created"
    assert main([*nuovo, "--titolo", "Visita alla cantina"]) == 0
    assert json.loads(capsys.readouterr().out)["action"] == "blocked_similar"
    assert main(["archivio", "verifica", "--profilo", str(profile_file)]) == 0
    assert json.loads(capsys.readouterr().out)["duplicati_stessa_data"] == []
    assert main([*nuovo, "--titolo", "Visita alla cantina", "--force"]) == 0
    assert json.loads(capsys.readouterr().out)["action"] == "created"
    assert main(["archivio", "verifica", "--profilo", str(profile_file)]) == 0
    assert json.loads(capsys.readouterr().out)["duplicati_stessa_data"] == [
        ["2027-04-17 Visita alla cantina", "2027-04-17 Visita in cantina"]
    ]


def test_cli_profilo_nuovo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    assert main(["profilo", "nuovo"]) == 0
    assert (tmp_path / "rtit-profilo.yaml").is_file()
    assert main(["profilo", "nuovo"]) == 1
