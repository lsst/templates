#!/bin/bash

# Determine the tag for Docker images.  Takes the Git ref as its only
# argument.

set -eo pipefail

if [ -z "$1" ]; then
    echo 'Usage: scripts/docker-tag.sh $GITHUB_REF' >&2
    exit 1
fi

echo "$1" | sed -E 's,refs/(heads|tags)/,,' | sed -E 's,/,-,g'
