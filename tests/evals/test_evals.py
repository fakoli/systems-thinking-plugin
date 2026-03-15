"""Pytest wrapper for eval cases. Runs evals as parametrized pytest tests.

Discovers all .yaml eval case files in the cases/ directory and runs each
as an individual parametrized test. Tests are marked with ``@pytest.mark.eval``
and ``@pytest.mark.slow`` so they can be selected or excluded via pytest
markers.

Usage:
    pytest tests/evals/test_evals.py -v
    pytest tests/evals/test_evals.py -v -m eval
    pytest tests/evals/test_evals.py -v -k complexity_mapper
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
import yaml

from tests.evals.graders.composite import grade_composite
from tests.evals.graders.cross_reference_consistency import grade_cross_reference_consistency
from tests.evals.graders.evidence_labels import grade_evidence_labels
from tests.evals.graders.file_exists import grade_files_exist
from tests.evals.graders.forbidden_check import (
    grade_no_forbidden_files,
    grade_no_forbidden_patterns,
)
from tests.evals.graders.quantitative_claims import grade_quantitative_claims
from tests.evals.graders.schema_match import grade_markdown_structure
from tests.evals.graders.section_check import grade_sections
from tests.evals.graders.source_anchor_coverage import grade_source_anchor_coverage

HARNESS_DIR = Path(__file__).resolve().parent
CASES_DIR = HARNESS_DIR / "cases"
FIXTURES_DIR = HARNESS_DIR / "fixtures"


def _discover_case_files() -> list[Path]:
    """Find all .yaml case files in the cases directory."""
    if not CASES_DIR.exists():
        return []
    return sorted(CASES_DIR.glob("*.yaml"))


def _load_case(case_path: Path) -> dict:
    """Load a case YAML file."""
    with open(case_path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _claude_available() -> bool:
    """Check whether the ``claude`` CLI is available on PATH."""
    return shutil.which("claude") is not None


def _run_setup(case: dict, workdir: Path) -> None:
    """Execute setup steps from the case definition."""
    for step in case.get("setup", []):
        if "copy_fixture" in step:
            src = HARNESS_DIR / step["copy_fixture"]
            dest = workdir / step["to"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


def _resolve_file(file_ref: str, workdir: Path) -> Path:
    """Resolve a file reference to an absolute path."""
    return workdir / file_ref


def _run_graders(case: dict, workdir: Path) -> list[dict]:
    """Run all graders for a case."""
    results: list[dict] = []

    for outcome in case.get("expected_outcomes", []):
        result = _run_single_grader(outcome, workdir, expected=True)
        results.append(result)

    for outcome in case.get("forbidden_outcomes", []):
        result = _run_single_grader(outcome, workdir, expected=False)
        results.append(result)

    return results


def _run_single_grader(outcome: dict, workdir: Path, expected: bool) -> dict:
    """Execute a single grader check."""
    outcome_type = outcome["type"]

    if outcome_type == "file_exists":
        if not expected:
            return grade_no_forbidden_files(workdir, outcome["files"])
        return grade_files_exist(workdir, outcome["files"])

    if outcome_type == "section_check":
        filepath = _resolve_file(outcome["file"], workdir)
        return grade_sections(filepath, outcome["sections"])

    if outcome_type == "forbidden_patterns":
        filepath = _resolve_file(outcome["file"], workdir)
        return grade_no_forbidden_patterns(filepath, outcome["patterns"])

    if outcome_type == "markdown_structure":
        filepath = _resolve_file(outcome["file"], workdir)
        return grade_markdown_structure(filepath, outcome["headings"])

    if outcome_type == "source_anchor_coverage":
        filepath = _resolve_file(outcome["file"], workdir)
        config = {"min_coverage": outcome.get("min_coverage", 0.5)}
        return grade_source_anchor_coverage(filepath, config)

    if outcome_type == "evidence_labels":
        filepath = _resolve_file(outcome["file"], workdir)
        config = {
            "min_source_labels": outcome.get("min_source_labels", 3),
            "min_inferred_labels": outcome.get("min_inferred_labels", 1),
        }
        return grade_evidence_labels(filepath, config)

    if outcome_type == "quantitative_claims":
        filepath = _resolve_file(outcome["file"], workdir)
        config = {"claims": outcome.get("claims", [])}
        return grade_quantitative_claims(filepath, config)

    if outcome_type == "cross_reference_consistency":
        filepath = _resolve_file(outcome["file"], workdir)
        config = {
            "sections_to_cross_check": outcome.get("sections_to_cross_check", []),
            "min_overlap": outcome.get("min_overlap", 0.3),
        }
        return grade_cross_reference_consistency(filepath, config)

    return {
        "pass": False,
        "score": 0.0,
        "error": f"Unknown outcome type: {outcome_type}",
    }


# Collect case files for parametrization
_case_files = _discover_case_files()
_case_ids = [p.stem for p in _case_files]


@pytest.mark.eval
@pytest.mark.slow
@pytest.mark.parametrize("case_path", _case_files, ids=_case_ids)
def test_eval_case(case_path: Path) -> None:
    """Run a single eval case end-to-end.

    Loads the case YAML, sets up a temporary working directory, invokes the
    Claude CLI with the case prompt, and runs all configured graders against
    the output.

    The test is automatically skipped if the ``claude`` CLI is not found on
    PATH.
    """
    if not _claude_available():
        pytest.skip("Claude CLI not available on PATH")

    case = _load_case(case_path)
    workdir = Path(tempfile.mkdtemp(prefix=f"eval_{case['name']}_"))

    try:
        _run_setup(case, workdir)

        timeout = case.get("timeout", 120)
        proc = subprocess.run(
            [
                "claude",
                "--print",
                "--dangerously-skip-permissions",
                "-p",
                case["prompt"],
            ],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        # Write stdout for graders referencing _stdout
        stdout_path = workdir / "_stdout"
        stdout_path.write_text(proc.stdout or "", encoding="utf-8")

        grader_results = _run_graders(case, workdir)
        composite = grade_composite(grader_results)

        if not composite["pass"]:
            failure_details: list[str] = []
            for failed in composite["failed"]:
                failure_details.append(str(failed))
            detail_str = "\n".join(failure_details)
            pytest.fail(
                f"Eval '{case['name']}' failed "
                f"({composite['passed_checks']}/{composite['total_checks']} checks passed).\n"
                f"Failures:\n{detail_str}"
            )

    finally:
        shutil.rmtree(workdir, ignore_errors=True)
