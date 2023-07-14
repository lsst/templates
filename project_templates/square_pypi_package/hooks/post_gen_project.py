"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.
"""

import os
from pathlib import Path

# These variables are interpolated by cookiecutter before this hook is run
github_org = '{{ cookiecutter.github_org }}'

print("(post-gen hook) Symlinking changelog to docs")
changelog_doc_path = Path("docs") / "changelog.md"
if changelog_doc_path.is_symlink():
    changelog_doc_path.unlink(missing_ok=True)
changelog_doc_path.symlink_to("../CHANGELOG.md")

# Remove the empty dependency update GitHub Actions workflow if the GitHub
# organization is not lsst-sqre.
if github_org != "lsst-sqre":
    print("(post-gen hook) Removing empty dependency update workflow")
    os.remove(".github/workflows/dependencies.yaml")
