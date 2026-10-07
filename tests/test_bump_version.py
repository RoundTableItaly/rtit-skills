from __future__ import annotations

import importlib.util
import shutil
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]


@pytest.fixture(scope="module")
def bv():
    spec = importlib.util.spec_from_file_location("bump_version", ROOT / "tools" / "bump_version.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["bump_version"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def repo(bv, tmp_path: Path) -> Path:
    """Copia dei soli file di versione, con un changelog di prova."""
    for rel in bv.VERSION_FILES:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / rel, tmp_path / rel)
    old = bv.current_version(ROOT)
    (tmp_path / bv.CHANGELOG).write_text(
        f"# Changelog\n\n{bv.UNRELEASED}\n\n### Aggiunto\n\n- Una novità.\n\n## [{old}] - 2026-01-01\n\n- Prima.\n",
        encoding="utf-8",
    )
    return tmp_path


def test_repository_is_coherent(bv):
    version = bv.check(root=ROOT)
    assert bv.parse(version)
    assert bv.UNRELEASED in (ROOT / bv.CHANGELOG).read_text(encoding="utf-8")


def test_bump_updates_every_file_and_changelog(bv, repo: Path):
    major, minor, patch = bv.parse(bv.current_version(repo))
    new = f"{major}.{minor}.{patch + 1}"
    bv.bump(new, root=repo, today=date(2026, 12, 24))
    assert set(bv.read_versions(repo).values()) == {new}
    text = (repo / bv.CHANGELOG).read_text(encoding="utf-8")
    assert f"{bv.UNRELEASED}\n\n## [{new}] - 2026-12-24\n\n### Aggiunto\n\n- Una novità.\n\n## [" in text
    assert bv.release_notes(new, repo) == "### Aggiunto\n\n- Una novità.\n"
    assert bv.check(f"v{new}", repo) == new


def test_bump_rejects_bad_versions(bv, repo: Path):
    old = bv.current_version(repo)
    for bad in (old, "0.0.1", "1.2", "v9.9.9", "abc"):
        with pytest.raises(bv.VersionError):
            bv.bump(bad, root=repo)
    assert set(bv.read_versions(repo).values()) == {old}


def test_bump_needs_unreleased_entries(bv, repo: Path):
    path = repo / bv.CHANGELOG
    path.write_text(path.read_text(encoding="utf-8").replace("### Aggiunto\n\n- Una novità.\n\n", ""), encoding="utf-8")
    with pytest.raises(bv.VersionError, match="vuota"):
        bv.bump("9.9.9", root=repo)


def test_check_detects_mismatches(bv, repo: Path):
    with pytest.raises(bv.VersionError, match="non coincide"):
        bv.check("v9.9.9", repo)
    pyproject = repo / "pyproject.toml"
    pyproject.write_text(
        pyproject.read_text(encoding="utf-8").replace(f'version = "{bv.current_version(repo)}"', 'version = "9.9.9"'),
        encoding="utf-8",
    )
    with pytest.raises(bv.VersionError, match="diverse"):
        bv.check(root=repo)


def test_release_notes_need_a_section(bv, repo: Path):
    with pytest.raises(bv.VersionError, match="manca la sezione"):
        bv.release_notes("9.9.9", repo)
