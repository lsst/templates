"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.

This is used to remove the ``manifests`` directory if the project is using
Helm rather than Kustomize, and remove empty files that aren't relevant in
some configuration cases.
"""

import os
import shutil

# These variables are interpolated by cookiecutter before this hook is run
uses_helm = True if '{{ cookiecutter.uses_helm }}' == 'True' else False
github_org = '{{ cookiecutter.github_org }}'

# Remove the Kustomize configuration if the package will be using Helm.
if uses_helm:
    print(f"(post-gen hook) Removing manifests directory")
    shutil.rmtree("manifests", ignore_errors=True)

# Remove the empty dependency update GitHub Actions workflow if the GitHub
# organization is not lsst-sqre.
if github_org != "lsst-sqre":
    print("(post-gen hook) Removing empty dependency update workflow")
    os.remove(".github/workflows/dependencies.yaml")
