"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.
"""

from pathlib import Path

print("(post-gen hook) Symlinking changelog to docs")

changelog_doc_path = Path("docs") / "changelog.md"
if changelog_doc_path.is_symlink():
    changelog_doc_path.unlink(missing_ok=True)
changelog_doc_path.symlink_to("../CHANGELOG.md")