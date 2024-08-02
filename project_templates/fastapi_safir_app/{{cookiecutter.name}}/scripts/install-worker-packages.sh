{%- if cookiecutter.flavor == "UWS" %}
#!/bin/bash

# Install or upgrade any operating system packages needed on worker images.
# This is done in a separate script to create a separate cached Docker image,
# which will help with iteration speed on the more interesting setup actions
# taken later in the build.

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for details.
set -euo pipefail

# Display each command as it's run.
set -x

# Upgrade the Red Hat packages.
#
# TODO(rra): Disabled for now because the version of CentOS used by the image
# is so old that the package repositories no longer exist. This will in theory
# soon be fixed by basing the image on AlmaLinux.
#yum -y upgrade
#yum clean all
{%- endif %}
