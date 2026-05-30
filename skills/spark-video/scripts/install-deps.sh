#!/usr/bin/env bash
# scripts/install-deps.sh — clone optional shanyin craft references.
# Failure is non-fatal: the pipeline runs without them (sub-skills fall
# back to their baked-in reference.md).

set -u
self_dir="$(cd "$(dirname "$0")" && pwd)"
repo_root="$(dirname "$self_dir")"
mkdir -p "$repo_root/references/shanyin"
cd "$repo_root/references/shanyin"

clone_or_pull() {
  local url="$1" target="$2"
  if [ -d "$target/.git" ]; then
    echo "[$target] already cloned — pulling latest"
    (cd "$target" && git pull --ff-only 2>&1 | head -5) || {
      echo "  ⚠ pull failed (continuing)" >&2
    }
  else
    echo "[$target] cloning $url"
    if git clone --depth 1 "$url" "$target" 2>&1 | head -10; then
      echo "  ✓ cloned"
    else
      echo "  ⚠ clone failed — sub-skill will fall back to baked-in reference.md" >&2
      rm -rf "$target"
    fi
  fi
}

clone_or_pull \
  "https://github.com/Shanyin-ai/shanyin-screenwriting-master.git" \
  "screenwriting-master"

clone_or_pull \
  "https://github.com/Shanyin-ai/shanyin-director-master.git" \
  "director-master"

echo
echo "Done. Verify with: ls $repo_root/references/shanyin/"
