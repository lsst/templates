{%- if cookiecutter.uws_service == "True" %}
#!/bin/bash

# This script updates and installs the necessary prerequisites for a backend
# worker starting with a stack container. It takes one parameter, the
# directory in which to do the installation.

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for details.
# set -u is omitted because the setup bash function does not support it.
set -eo pipefail

# Enable the stack. This should be done before set -x because it will
# otherwise spew a bunch of nonsense no one cares about into the logs.
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib

# Display each command as it's run.
set -x

# Install Python dependencies and the {{ cookiecutter.name }} code.
cd "$1"
pip install --no-cache-dir google-cloud-storage safir-arq
pip install --no-cache-dir --no-deps .
{%- endif %}
