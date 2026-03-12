"""Tests for YAML frontmatter in agent and skill Markdown files."""

import re

import pytest

from tests.conftest import PLUGIN_ROOT, parse_frontmatter


AGENTS_DIR = PLUGIN_ROOT / ".claude" / "agents"
SKILLS_DIR = PLUGIN_ROOT / ".claude" / "skills"

AGENT_FILES = sorted(AGENTS_DIR.glob("*.md"))
SKILL_FILES = sorted(SKILLS_DIR.glob("*.md"))

KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def _ids(paths):
    return [p.stem for p in paths]


# ── Frontmatter presence ─────────────────────────────────────────────────────


def test_all_agents_have_frontmatter():
    for path in AGENT_FILES:
        fm, _ = parse_frontmatter(path)
        assert fm, f"{path.name} has no YAML frontmatter"


def test_all_skills_have_frontmatter():
    for path in SKILL_FILES:
        fm, _ = parse_frontmatter(path)
        assert fm, f"{path.name} has no YAML frontmatter"


# ── Required fields ──────────────────────────────────────────────────────────


@pytest.mark.parametrize("agent_file", AGENT_FILES, ids=_ids(AGENT_FILES))
def test_agent_frontmatter_has_required_fields(agent_file):
    fm, _ = parse_frontmatter(agent_file)
    assert "name" in fm, f"{agent_file.name} missing 'name'"
    assert "description" in fm, f"{agent_file.name} missing 'description'"


@pytest.mark.parametrize("skill_file", SKILL_FILES, ids=_ids(SKILL_FILES))
def test_skill_frontmatter_has_required_fields(skill_file):
    fm, _ = parse_frontmatter(skill_file)
    assert "name" in fm, f"{skill_file.name} missing 'name'"
    assert "description" in fm, f"{skill_file.name} missing 'description'"


# ── Naming conventions ───────────────────────────────────────────────────────


@pytest.mark.parametrize("agent_file", AGENT_FILES, ids=_ids(AGENT_FILES))
def test_agent_names_are_kebab_case(agent_file):
    """Agent frontmatter 'name' must be kebab-case."""
    fm, _ = parse_frontmatter(agent_file)
    name = fm.get("name", "")
    assert KEBAB_RE.match(name), (
        f"{agent_file.name}: name '{name}' is not kebab-case"
    )


# ── Description quality ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "md_file",
    AGENT_FILES + SKILL_FILES,
    ids=_ids(AGENT_FILES + SKILL_FILES),
)
def test_frontmatter_descriptions_are_nonempty(md_file):
    fm, _ = parse_frontmatter(md_file)
    desc = fm.get("description", "")
    assert desc and str(desc).strip(), (
        f"{md_file.name} has an empty description"
    )


# ── Tool scoping ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize("agent_file", AGENT_FILES, ids=_ids(AGENT_FILES))
def test_agent_frontmatter_has_allowed_tools(agent_file):
    """Each agent must declare its allowed tools as a list."""
    fm, _ = parse_frontmatter(agent_file)
    tools_key = "allowed_tools" if "allowed_tools" in fm else "tools"
    assert tools_key in fm, (
        f"{agent_file.name} missing 'allowed_tools' or 'tools'"
    )
    assert isinstance(fm[tools_key], list), (
        f"{agent_file.name}: {tools_key} should be a list"
    )
