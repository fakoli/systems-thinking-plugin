# Testing Guide

## Quick Start

```bash
cd systems-thinking-plugin

# First time setup (installs uv if needed, syncs deps, runs validation)
./setup.sh

# Fast tests — no API key needed
uv run pytest tests/unit tests/contracts

# Eval tests — requires claude CLI and ANTHROPIC_API_KEY
uv run pytest tests/evals -m eval
```

## Test Layers

### Unit Tests (`tests/unit/`)

Validate hook prompts, frontmatter parsing, file structure, and internal logic. These run in milliseconds and are fully deterministic. No network calls, no API keys.

### Contract Tests (`tests/contracts/`)

Verify plugin layout conforms to spec: correct directory structure, valid agent/skill definitions, well-formed output contracts. Runs in seconds, deterministic, no external dependencies.

### Eval Tests (`tests/evals/`)

End-to-end scenario tests that invoke Claude CLI with specific prompts and grade the output. These take minutes, cost API credits, and require:

- `@anthropic-ai/claude-code` installed globally (`npm install -g @anthropic-ai/claude-code`)
- `ANTHROPIC_API_KEY` environment variable set

## Running Eval Tests Manually

Eval tests invoke the Claude CLI end-to-end and are **non-deterministic** — they depend on model output, can be slow, and may time out. They should be run manually rather than as part of automated CI gates.

```bash
# Run all eval tests
.venv/bin/python -m pytest tests/evals/ -v

# Run a single eval case
.venv/bin/python -m pytest tests/evals/test_evals.py::test_eval_case[complexity_mapper_basic] -v
.venv/bin/python -m pytest tests/evals/test_evals.py::test_eval_case[decision_brief_basic] -v
.venv/bin/python -m pytest tests/evals/test_evals.py::test_eval_case[hook_enforcement] -v

# With a longer timeout (default is 120s, which may not be enough)
.venv/bin/python -m pytest tests/evals/ -v --timeout=600
```

**Prerequisites:** `claude` CLI installed globally and `ANTHROPIC_API_KEY` set. Eval tests cost API credits.

**Expected behavior:** These tests may fail intermittently due to model output variability or timeouts. A single failure does not indicate a plugin bug — re-run the specific case before investigating.

## Adding New Tests

### Unit and Contract Tests

Add standard pytest functions to the appropriate directory. Follow existing naming conventions (`test_<subject>.py`). No special scaffolding needed — just import pytest and write assertions.

### Eval Tests

1. Create a YAML case file in `tests/evals/cases/`.
2. Add any supporting fixtures (mock repos, sample files) under `tests/evals/fixtures/`.
3. The eval runner picks up new `.yaml` files automatically.

## Eval Case Format

Each YAML case file defines a single evaluation scenario:

```yaml
name: descriptive-kebab-case-name
description: What this eval tests in one sentence.
prompt: |
  The exact prompt sent to Claude CLI.
context:
  files:
    - path: relative/path/to/file.py
      content: |
        File content provided as context.
  working_directory: optional/subdir
expected:
  grader: contains # which grader to use
  criteria:
    - "expected substring" # grader-specific criteria
    - "another expected output"
timeout: 120 # seconds, optional (default: 300)
tags:
  - eval
  - optional-additional-tag
```

### Field Reference

| Field                       | Required | Description                                  |
| --------------------------- | -------- | -------------------------------------------- |
| `name`                      | yes      | Unique identifier for the case               |
| `description`               | yes      | Human-readable summary                       |
| `prompt`                    | yes      | Input sent to Claude CLI                     |
| `context.files`             | no       | Virtual files available during the run       |
| `context.working_directory` | no       | CWD override for the CLI invocation          |
| `expected.grader`           | yes      | Grading strategy to apply                    |
| `expected.criteria`         | yes      | Grader-specific pass/fail criteria           |
| `timeout`                   | no       | Max seconds before the case is marked failed |
| `tags`                      | no       | Pytest markers applied to the case           |

## Graders

| Grader        | Behavior                                   | Criteria Format                       |
| ------------- | ------------------------------------------ | ------------------------------------- |
| `contains`    | Output must contain all listed substrings  | List of strings                       |
| `regex`       | Output must match all listed patterns      | List of regex patterns                |
| `json_schema` | Output must validate against a JSON schema | JSON schema object                    |
| `llm_judge`   | A second LLM call grades the output        | `{prompt: "...", passing_score: 0.8}` |
| `custom`      | Runs a Python function you provide         | `{module: "...", function: "..."}`    |

To add a new grader, implement a function with signature `(output: str, criteria: Any) -> GradeResult` in `tests/evals/graders/` and register it in the grader registry.

## CI Behavior

Three GitHub Actions jobs run on this repo:

| Job                         | Trigger                                       | What it does                                                                                               |
| --------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `unit-and-contract`         | Every push to `main`, every PR                | Runs unit + contract tests. Must pass.                                                                     |
| `evals`                     | PR with `run-evals` label, nightly at 2am UTC | Runs eval suite after unit/contract pass. Nightly failures warn but do not block. PR failures block merge. |
| `validate-plugin-structure` | Every push to `main`, every PR                | Checks `settings.json` validity, frontmatter in agent/skill files, file length warnings.                   |

Evals only run after unit and contract tests pass (dependency chain). To trigger evals on a PR, add the `run-evals` label.

## Common Issues

**"claude CLI not found"**
Install it: `npm install -g @anthropic-ai/claude-code`. If you only want to run unit/contract tests, skip evals with `pytest tests/unit tests/contracts`.

**"API key not set"**
Eval tests require `ANTHROPIC_API_KEY` in your environment. Unit and contract tests do not need it.

**Frontmatter parse errors**
Agent and skill `.md` files must start with a `---` line and have a matching closing `---`. Check for missing delimiters or leading whitespace before the first `---`.

**Timeout failures in evals**
Default timeout is 300 seconds. If a specific case needs more time, set `timeout` in the YAML case file. For local runs, you can also pass `--timeout=600` to pytest.
