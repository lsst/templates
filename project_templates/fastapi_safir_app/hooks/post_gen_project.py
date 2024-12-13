"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.
"""

import os
import shutil

# These variables are interpolated by cookiecutter before this hook is run
uws_service = True if '{{ cookiecutter.flavor }}' == 'UWS' else False
module_name = '{{ cookiecutter.module_name }}'
github_org = '{{ cookiecutter.github_org }}'

# Remove unused files if the application will not be using UWS.
if not uws_service:
    print(f"(post-gen hook) Removing unused UWS support files")
    shutil.rmtree(f"src/{module_name}/workers")
    os.remove("Dockerfile.worker")
    os.remove("scripts/install-worker.sh")
    os.remove("scripts/install-worker-packages.sh")
    os.remove("scripts/start-worker.sh")
    os.remove(f"src/{module_name}/dependencies.py")
    os.remove(f"src/{module_name}/domain.py")
