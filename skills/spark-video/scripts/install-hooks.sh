#!/usr/bin/env bash
# Installs project git hooks. Run once after cloning:
#   bash scripts/install-hooks.sh
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -d .git ]]; then
  echo "not a git repo (no .git/) — skipping hook install"
  exit 0
fi

mkdir -p .git/hooks
ln -sf ../../scripts/pre-commit .git/hooks/pre-commit
chmod +x scripts/pre-commit
echo "✓ pre-commit hook installed → .git/hooks/pre-commit"
