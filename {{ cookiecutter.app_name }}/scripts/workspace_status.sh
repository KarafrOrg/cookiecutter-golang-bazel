#!/usr/bin/env bash
set -euo pipefail

commit=""
if git_rev="$(git rev-parse HEAD 2> /dev/null)"; then
  commit="${git_rev}"
fi

tree_state="clean"
if [[ -n "$(git status --porcelain 2> /dev/null || true)" ]]; then
  tree_state="dirty"
fi

echo "STABLE_GIT_COMMIT ${commit}"
echo "STABLE_GIT_TREE_STATE ${tree_state}"
