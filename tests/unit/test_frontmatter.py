"""Tests for YAML frontmatter in agent and skill Markdown files."""

import re

import pytest

from tests.conftest import PLUGIN_ROOT, parse_frontmatter

AGENTS_DIR = PLUGIN_ROOT / "agents"
SKILLS_DIR = PLUGIN_ROOT / "skills"

AGENT_FILES = sorted(AGENTS_DIR.glob("*.md"))
SKILL_FILES = sorted(SKILLS_DIR.glob("*/SKILL.md"))

KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def _ids_agents(paths):
    return [p.stem for p in paths]


def _ids_skills(paths):
    return [p.parent.name for p in paths]


# ── Frontmatter presence ─────────────────────────────────────────────────────


def test_all_agents_have_frontmatter():
    for path in AGENT_FILES:
        fm, _ = parse_frontmatter(path)
        assert fm, f"{path.name} has no YAML frontmatter"


def test_all_skills_have_frontmatter():
    for path in SKILL_FILES:
        fm, _ = parse_frontmatter(path)
        assert fm, f"{path.parent.name}/SKILL.md has no YAML frontmatter"


# ── Required fields ──────────────────────────────────────────────────────────


@pytest.mark.parametrize("agent_file", AGENT_FILES, ids=_ids_agents(AGENT_FILES))
def test_agent_frontmatter_has_required_fields(agent_file):
    fm, _ = parse_frontmatter(agent_file)
    assert "name" in fm, f"{agent_file.name} missing 'name'"
    assert "description" in fm, f"{agent_file.name} missing 'description'"


@pytest.mark.parametrize("skill_file", SKILL_FILES, ids=_ids_skills(SKILL_FILES))
def test_skill_frontmatter_has_required_fields(skill_file):
    fm, _ = parse_frontmatter(skill_file)
    assert "description" in fm, f"{skill_file.parent.name}/SKILL.md missing 'description'"


# ── Naming conventions ───────────────────────────────────────────────────────


@pytest.mark.parametrize("agent_file", AGENT_FILES, ids=_ids_agents(AGENT_FILES))
def test_agent_names_are_kebab_case(agent_file):
    """Agent frontmatter 'name' must be kebab-case."""
    fm, _ = parse_frontmatter(agent_file)
    name = fm.get("name", "")
    assert KEBAB_RE.match(name), f"{agent_file.name}: name '{name}' is not kebab-case"


# ── Description quality ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "md_file",
    AGENT_FILES + SKILL_FILES,
    ids=_ids_agents(AGENT_FILES) + _ids_skills(SKILL_FILES),
)
def test_frontmatter_descriptions_are_nonempty(md_file):
    fm, _ = parse_frontmatter(md_file)
    desc = fm.get("description", "")
    assert desc and str(desc).strip(), f"{md_file.name} has an empty description"


# ── Tool scoping ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize("agent_file", AGENT_FILES, ids=_ids_agents(AGENT_FILES))
def test_agent_frontmatter_has_allowed_tools(agent_file):
    """Each agent must declare its allowed tools as a list under 'allowed-tools'."""
    fm, _ = parse_frontmatter(agent_file)
    assert "allowed-tools" in fm, f"{agent_file.name} missing 'allowed-tools'"
    assert isinstance(fm["allowed-tools"], list), f"{agent_file.name}: 'allowed-tools' should be a list"
