from __future__ import annotations

import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]


@pytest.fixture(scope="module")
def br():
    spec = importlib.util.spec_from_file_location("build_release", ROOT / "tools" / "build_release.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_release"] = module  # serve alle dataclass del modulo
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def dist(br, tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("dist")
    br.build(out)
    return out


def _names(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        return z.namelist()


def _read(path: Path, name: str) -> str:
    with zipfile.ZipFile(path) as z:
        return z.read(name).decode("utf-8")


def test_all_packages_exist(br, dist: Path):
    skills = [s.name for s in br.load_skills()]
    assert sorted(p.stem for p in (dist / "skills").glob("*.zip")) == skills
    for name in ("rtit-skills-tutte", "rtit-claude-plugin", "rtit-chatgpt", "rtit-gemini"):
        assert (dist / f"{name}.zip").is_file(), name


def test_skill_zips_contain_skill_md(br, dist: Path):
    for skill in br.load_skills():
        names = _names(dist / "skills" / f"{skill.name}.zip")
        assert f"{skill.name}/SKILL.md" in names
        for asset in br.EXTRA_ASSETS.get(skill.name, []):
            assert f"{skill.name}/assets/{asset.name}" in names
    tutte = _names(dist / "rtit-skills-tutte.zip")
    assert all(f"rtit-skills/{s.name}/SKILL.md" in tutte for s in br.load_skills())


def test_plugin_zip(br, dist: Path, tmp_path: Path):
    with zipfile.ZipFile(dist / "rtit-claude-plugin.zip") as z:
        z.extractall(tmp_path)
    base = tmp_path / "rtit-claude-plugin"
    plugin = json.loads((base / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert plugin["name"] == "rtit"
    mcp = json.loads((base / ".mcp.json").read_text(encoding="utf-8"))
    assert mcp["mcpServers"]["round-table-italia"]["url"] == br.MCP_URL
    for name in ("README.md", "LICENSE"):
        assert (base / name).is_file()
    assert all((base / "skills" / s.name / "SKILL.md").is_file() for s in br.load_skills())


@pytest.mark.parametrize(("piattaforma", "limite"), [("chatgpt", 20), ("gemini", 10)])
def test_chat_packages_limits(br, dist: Path, piattaforma: str, limite: int):
    path = dist / f"rtit-{piattaforma}.zip"
    names = _names(path)
    base = f"rtit-{piattaforma}/"
    istruzioni = _read(path, base + "ISTRUZIONI.txt")
    assert len(istruzioni) <= br.MAX_ISTRUZIONI
    assert base + "LEGGIMI.md" in names
    conoscenza = [n for n in names if n.startswith(base + "conoscenza/")]
    assert 0 < len(conoscenza) <= limite
    # ogni skill compare nelle istruzioni, con un file di conoscenza che esiste davvero
    for skill in br.load_skills():
        line = next(ln for ln in istruzioni.splitlines() if ln.startswith(f"- {skill.name} — "))
        filename = line.split(" — ")[1]
        assert base + "conoscenza/" + filename in names
        assert f"# Skill {skill.name}" in _read(path, base + "conoscenza/" + filename)


def test_grouping_respects_limit(br):
    skills = br.load_skills()
    for limit in (len(skills), 10, 5, 1):
        groups = br.group_skills(skills, limit)
        assert len(groups) <= limit
        assert sorted(s.name for g in groups for s in g) == sorted(s.name for s in skills)


def test_build_is_reproducible(br, dist: Path, tmp_path: Path):
    br.build(tmp_path)
    for zip_path in dist.rglob("*.zip"):
        assert (tmp_path / zip_path.relative_to(dist)).read_bytes() == zip_path.read_bytes(), zip_path.name
