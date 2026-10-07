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


def test_single_package(br, dist: Path):
    assert [p.name for p in dist.rglob("*.zip")] == ["rtit-skills.zip"]


def test_package_contents(br, dist: Path, tmp_path: Path):
    with zipfile.ZipFile(dist / "rtit-skills.zip") as z:
        names = z.namelist()
        z.extractall(tmp_path)
    # Claude carica lo zip come plugin solo con il manifest al primo livello
    assert ".claude-plugin/plugin.json" in names
    base = tmp_path
    for rel in br.PLUGIN_FILES:
        assert (base / rel).is_file(), rel
    claude = json.loads((base / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    codex = json.loads((base / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    gemini = json.loads((base / "gemini-extension.json").read_text(encoding="utf-8"))
    assert claude["name"] == codex["name"] == "rtit"
    assert claude["version"] == codex["version"] == gemini["version"]
    assert codex["skills"] == "./skills/"
    mcp = json.loads((base / ".mcp.json").read_text(encoding="utf-8"))
    assert mcp["mcpServers"]["App Round Table Italia"]["url"] == br.MCP_URL
    for skill in br.load_skills():
        assert (base / "skills" / skill.name / "SKILL.md").is_file()
        for asset in br.EXTRA_ASSETS.get(skill.name, []):
            assert (base / "skills" / skill.name / "assets" / asset.name).is_file()


def test_old_packages_are_removed(br, tmp_path: Path):
    (tmp_path / "skills").mkdir()
    (tmp_path / "skills" / "rt-vecchia.zip").write_bytes(b"x")
    (tmp_path / "rtit-chatgpt.zip").write_bytes(b"x")
    br.build(tmp_path)
    assert [p.name for p in tmp_path.rglob("*.zip")] == ["rtit-skills.zip"]


def test_build_is_reproducible(br, dist: Path, tmp_path: Path):
    br.build(tmp_path)
    assert (tmp_path / "rtit-skills.zip").read_bytes() == (dist / "rtit-skills.zip").read_bytes()
