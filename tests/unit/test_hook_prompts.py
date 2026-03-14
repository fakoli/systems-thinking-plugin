"""Tests for hook prompts defined in hooks/hooks.json."""

import json

import pytest


@pytest.fixture
def settings(settings_path):
    return json.loads(settings_path.read_text(encoding="utf-8"))


@pytest.fixture
def hooks(settings):
    return settings["hooks"]


@pytest.fixture
def preflight_hook(hooks):
    entry = hooks["UserPromptSubmit"][0]
    # Support nested format: entry may have a "hooks" array wrapping the actual hook
    if "hooks" in entry and isinstance(entry["hooks"], list):
        return entry["hooks"][0]
    return entry


@pytest.fixture
def completion_hook(hooks):
    entry = hooks["Stop"][0]
    if "hooks" in entry and isinstance(entry["hooks"], list):
        return entry["hooks"][0]
    return entry


# ── Structure tests ──────────────────────────────────────────────────────────


def test_settings_json_is_valid_json(settings_path):
    """settings.json must parse as valid JSON."""
    text = settings_path.read_text(encoding="utf-8")
    json.loads(text)  # raises on invalid JSON


def test_hooks_key_exists(settings):
    assert "hooks" in settings


def test_user_prompt_submit_hook_exists(hooks):
    assert "UserPromptSubmit" in hooks
    assert len(hooks["UserPromptSubmit"]) >= 1


def test_stop_hook_exists(hooks):
    assert "Stop" in hooks
    assert len(hooks["Stop"]) >= 1


def test_preflight_hook_is_prompt_type(preflight_hook):
    assert preflight_hook["type"] == "prompt"


def test_completion_hook_is_prompt_type(completion_hook):
    assert completion_hook["type"] == "prompt"


# ── Content tests ────────────────────────────────────────────────────────────


def test_preflight_prompt_mentions_extraction_synthesis(preflight_hook):
    prompt = preflight_hook["prompt"].lower()
    assert "extraction" in prompt, "Preflight prompt should mention extraction"
    assert "synthesis" in prompt, "Preflight prompt should mention synthesis"


def test_preflight_prompt_mentions_source_anchors(preflight_hook):
    prompt = preflight_hook["prompt"].lower()
    assert "source" in prompt, "Preflight prompt should mention source"


def test_completion_prompt_mentions_assumptions(completion_hook):
    prompt = completion_hook["prompt"].lower()
    assert "assumptions" in prompt


def test_completion_prompt_mentions_risks(completion_hook):
    prompt = completion_hook["prompt"].lower()
    assert "risks" in prompt


def test_completion_prompt_mentions_unresolved(completion_hook):
    prompt = completion_hook["prompt"].lower()
    assert "unresolved" in prompt


# ── Quality constraints ──────────────────────────────────────────────────────


def _flatten_hooks(entries):
    """Yield individual hook dicts, handling both flat and nested formats."""
    for entry in entries:
        if "hooks" in entry and isinstance(entry["hooks"], list):
            yield from entry["hooks"]
        else:
            yield entry


def test_hook_prompts_are_concise(hooks):
    """Each hook prompt should be under 500 characters to stay focused."""
    for hook_type, entries in hooks.items():
        for i, hook in enumerate(_flatten_hooks(entries)):
            if "prompt" in hook:
                length = len(hook["prompt"])
                assert length < 500, f"{hook_type}[{i}] prompt is {length} chars (max 500)"


def test_no_bash_hooks(hooks):
    """v1 should not define any bash hooks."""
    for hook_type, entries in hooks.items():
        for i, hook in enumerate(_flatten_hooks(entries)):
            assert hook.get("type") != "bash", (
                f"{hook_type}[{i}] has type 'bash'; bash hooks are not allowed in v1"
            )
