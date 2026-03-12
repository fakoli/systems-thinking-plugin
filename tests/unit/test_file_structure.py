"""Tests for file naming conventions and structural rules."""

import re

import pytest

from tests.conftest import PLUGIN_ROOT, parse_frontmatter


AGENTS_DIR = PLUGIN_ROOT / ".claude" / "agents"
SKILLS_DIR = PLUGIN_ROOT / ".claude" / "skills"

AGENT_FILES = sorted(AGENTS_DIR.glob("*.md"))
SKILL_FILES = sorted(SKILLS_DIR.glob("*.md"))

KEBAB_FILENAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")


def _ids(paths):
    return [p.stem for p in paths]


# ── Filename conventions ─────────────────────────────────────────────────────


@pytest.mark.parametrize("agent_file", AGENT_FILES, ids=_ids(AGENT_FILES))
def test_all_agent_filenames_are_kebab_case(agent_file):
    assert KEBAB_FILENAME_RE.match(agent_file.name), (
        f"Agent filename '{agent_file.name}' is not kebab-case"
    )


@pytest.mark.parametrize("skill_file", SKILL_FILES, ids=_ids(SKILL_FILES))
def test_all_skill_filenames_are_kebab_case(skill_file):
    assert KEBAB_FILENAME_RE.match(skill_file.name), (
        f"Skill filename '{skill_file.name}' is not kebab-case"
    )


# ── Uniqueness ───────────────────────────────────────────────────────────────


def test_no_duplicate_agent_names():
    names = []
    for path in AGENT_FILES:
        fm, _ = parse_frontmatter(path)
        names.append(fm.get("name", path.stem))
    assert len(names) == len(set(names)), (
        f"Duplicate agent names found: {[n for n in names if names.count(n) > 1]}"
    )


def test_no_duplicate_skill_names():
    names = []
    for path in SKILL_FILES:
        fm, _ = parse_frontmatter(path)
        names.append(fm.get("name", path.stem))
    assert len(names) == len(set(names)), (
        f"Duplicate skill names found: {[n for n in names if names.count(n) > 1]}"
    )


# ── Content size ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize("agent_file", AGENT_FILES, ids=_ids(AGENT_FILES))
def test_agent_files_are_not_empty(agent_file):
    _, body = parse_frontmatter(agent_file)
    assert len(body.strip()) > 100, (
        f"{agent_file.name} body is too short ({len(body.strip())} chars)"
    )


@pytest.mark.parametrize("skill_file", SKILL_FILES, ids=_ids(SKILL_FILES))
def test_skill_files_are_not_empty(skill_file):
    _, body = parse_frontmatter(skill_file)
    assert len(body.strip()) > 100, (
        f"{skill_file.name} body is too short ({len(body.strip())} chars)"
    )
