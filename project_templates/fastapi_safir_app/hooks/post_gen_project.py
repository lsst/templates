"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.
"""

import os
import shutil

# These variables are interpolated by cookiecutter before this hook is run
github_org = '{{ cookiecutter.github_org }}'
