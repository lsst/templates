#!/bin/bash

# Update uv version references based on the frozen version from uv.lock.

# Bash "strict mode", to help catch problems and bugs in the shell script.
# Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for details.
set -euo pipefail

# Determine the current frozen uv version. uv must be part of the lint
# dependency group in pyproject.toml.
uv_version=$(uv export -q --no-hashes --only-group lint \
             | grep ^uv== | sed 's/.*=//')

# Replace the version in the env variables in GitHub Actions workflows.
for f in .github/workflows/*.yaml; do
    sed "s/UV_VERSION: .*/UV_VERSION: \"$uv_version\"/" "$f" >"$f.n"
    if ! cmp -s "$f" "${f}.n"; then
        echo "Updating UV_VERSION to $uv_version in $f"
        mv "${f}.n" "$f"
    else
        rm "${f}.n"
    fi
done

# Replace the version in any Dockerfiles. Allow for copying this script into
# packages that have no Dockerfile.
for f in Dockerfile*; do
    if [ -f "$f" ]; then
        sed "s/uv:[0-9][0-9.]*/uv:$uv_version/" "$f" >"${f}.n"
        if ! cmp -s "$f" "${f}.n"; then
            echo "Updating uv container version to $uv_version in $f"
            mv "${f}.n" "$f"
        else
            rm "${f}.n"
        fi
    fi
done
