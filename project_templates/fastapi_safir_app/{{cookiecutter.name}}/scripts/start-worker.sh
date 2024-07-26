{%- if cookiecutter.uws_service == "True" %}
#!/bin/bash

# This script is installed in the worker image and starts the backend worker
# using arq.

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for details.
# set -u is omitted because the setup bash function does not support it.
set -eo pipefail

# Initialize the environment.
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib

# Start arq with the worker.
arq {{ cookiecutter.module_name }}.workers.{{ cookiecutter.module_name }}.WorkerSettings
{%- endif %}
