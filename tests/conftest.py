from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

EXAMPLE = Path(__file__).parents[1] / "src" / "rtit" / "templates" / "profilo-esempio.yaml"
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def profile_file(tmp_path: Path) -> Path:
    data = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    data["archivio"]["percorso"] = "archivio"
    (tmp_path / "archivio").mkdir()
    dest = tmp_path / "rtit-profilo.yaml"
    dest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return dest


@pytest.fixture
def profile(profile_file: Path) -> dict:
    from rtit.profile import load_profile

    return load_profile(profile_file)


@pytest.fixture
def bollettino_md(tmp_path: Path) -> Path:
    dest = tmp_path / "2027-04-03 Bollettino N.1 Visita in cantina.md"
    shutil.copy(FIXTURES / "bollettino.md", dest)
    return dest
