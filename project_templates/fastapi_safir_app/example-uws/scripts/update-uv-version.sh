#!/bin/bash

# Update uv version references based on the frozen version from uv.lock.

# Bash "strict mode", to help catch problems and bugs in the shell script.
# Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for details.
set -euo pipefail

# Expand non-matching globs to the empty list instead of the glob so that
# packages that don't have one of the affected files can silently skip the
# uv version rewrite rule that doesn't apply.
shopt -s nullglob

# Determine the current uv release version.
uv_version=$(echo uv \
             | uv pip compile - --quiet --no-header --no-annotate --no-config \
             | sed -n 's/^uv==//p')

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
    sed "s/uv:[0-9][0-9.]*/uv:$uv_version/" "$f" >"${f}.n"
    if ! cmp -s "$f" "${f}.n"; then
        echo "Updating uv container version to $uv_version in $f"
        mv "${f}.n" "$f"
    else
        rm "${f}.n"
    fi
done
