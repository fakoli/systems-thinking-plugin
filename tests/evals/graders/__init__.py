"""Graders for systems-thinking-plugin eval framework.

Each grader returns a result dict with at minimum:
    - "pass": bool
    - "score": float (0.0 to 1.0)

Additional fields vary by grader type.
"""

from .composite import grade_composite
from .file_exists import grade_files_exist
from .forbidden_check import grade_no_forbidden_files, grade_no_forbidden_patterns
from .schema_match import grade_json_schema, grade_markdown_structure
from .section_check import grade_sections

__all__ = [
    "grade_files_exist",
    "grade_sections",
    "grade_json_schema",
    "grade_markdown_structure",
    "grade_no_forbidden_patterns",
    "grade_no_forbidden_files",
    "grade_composite",
]
