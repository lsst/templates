"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.

This is used to remove the ``manifests`` directory if the project is using
Helm rather than Kustomize.
"""

import shutil

# These variables are interpolated by cookiecutter before this hook is run
uses_helm = True if '{{ cookiecutter.uses_helm }}' == 'True' else False

# Remove the Kustomize configuration if the package will be using Helm.
if uses_helm:
    print(f"(post-gen hook) Removing manifests directory")
    shutil.rmtree("manifests", ignore_errors=True)
