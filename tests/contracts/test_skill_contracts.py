"""Tests that skill files meet the systems-thinking-plugin spec."""

import re

import pytest

from tests.conftest import PLUGIN_ROOT, parse_frontmatter


SKILLS_DIR = PLUGIN_ROOT / ".claude" / "skills"

SKILL_FILES = [
    "pattern-remix.md",
    "complexity-mapper.md",
    "context-sharding.md",
    "decision-brief.md",
    "architecture-risk-review.md",
]

AGENT_NAMES = [
    "doc-indexer",
    "doc-reader",
    "caveat-extractor",
    "cost-capacity-analyst",
    "architecture-dependency-mapper",
    "pattern-remix-planner",
    "synthesis-brief-writer",
]


def _read_body(filename):
    _, body = parse_frontmatter(SKILLS_DIR / filename)
    return body


# ── When-to-use guidance ─────────────────────────────────────────────────────


@pytest.mark.parametrize("filename", SKILL_FILES)
def test_skills_have_when_to_use(filename):
    body = _read_body(filename).lower()
    assert "when to use" in body or "## when" in body, (
        f"{filename} missing 'When to Use' section"
    )


# ── Inputs section ───────────────────────────────────────────────────────────


@pytest.mark.parametrize("filename", SKILL_FILES)
def test_skills_have_inputs_section(filename):
    body = _read_body(filename).lower()
    assert "input" in body, f"{filename} does not mention inputs"


# ── Process steps ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("filename", SKILL_FILES)
def test_skills_have_process_steps(filename):
    """Skills should describe their process as numbered steps or a Process section."""
    body = _read_body(filename)
    has_numbered_steps = bool(re.search(r"^\s*\d+\.\s", body, re.MULTILINE))
    has_process_heading = bool(
        re.search(r"^#{2,3}\s+(Process|Steps)", body, re.MULTILINE)
    )
    assert has_numbered_steps or has_process_heading, (
        f"{filename} missing numbered steps or ## Process/Steps section"
    )


# ── Output format ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("filename", SKILL_FILES)
def test_skills_have_output_format(filename):
    """Skills should specify their output format or reference an output contract."""
    body = _read_body(filename).lower()
    assert "output" in body, (
        f"{filename} does not mention output format or output contract"
    )


# ── Failure modes ────────────────────────────────────────────────────────────


@pytest.mark.parametrize("filename", SKILL_FILES)
def test_skills_have_failure_modes(filename):
    """Skills should mention failure modes, cautions, or warnings."""
    body = _read_body(filename).lower()
    keywords = ["failure", "caution", "warning"]
    found = [kw for kw in keywords if kw in body]
    assert found, (
        f"{filename} should mention at least one of: {keywords}"
    )


# ── Agent references ────────────────────────────────────────────────────────


@pytest.mark.parametrize("filename", SKILL_FILES)
def test_skills_reference_agents(filename):
    """Every skill should reference at least one agent by name."""
    body = _read_body(filename).lower()
    referenced = [name for name in AGENT_NAMES if name in body]
    assert referenced, (
        f"{filename} does not reference any agent. Expected at least one of: {AGENT_NAMES}"
    )
