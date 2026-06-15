#!/usr/bin/env bash
# scripts/doctor.sh — verify spark-video runtime dependencies.
# Exit 0 = ready, 1 = something missing or wrong.

set -u
ok=true
warn() { echo "  ⚠ $*"; ok=false; }
err()  { echo "  ✗ $*"; ok=false; }
good() { echo "  ✓ $*"; }

echo "spark-video doctor"
echo "=================="

# bl
echo "[bl CLI]"
if command -v bl >/dev/null 2>&1; then
  ver="$(bl --version 2>&1 | head -1 || echo 'unknown')"
  good "bl found ($ver)"
  if bl auth status >/dev/null 2>&1; then
    good "bl auth OK"
  else
    warn "bl auth NOT logged in — run: bl auth login"
  fi
else
  err "bl not found. Install (see https://bailian.aliyun.com/cli/install.md):"
  err "  npm install -g bailian-cli && npx skills add modelstudioai/skills --all -g"
fi

# ffmpeg + ffprobe
echo "[ffmpeg]"
for bin in ffmpeg ffprobe; do
  if command -v "$bin" >/dev/null 2>&1; then
    good "$bin found ($("$bin" -version 2>&1 | head -1 | cut -d, -f1))"
  else
    err "$bin not found. Install: brew install ffmpeg (macOS) or apt install ffmpeg"
  fi
done

# uv
echo "[uv]"
if command -v uv >/dev/null 2>&1; then
  good "uv found ($(uv --version 2>&1))"
else
  err "uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# scripts/bl wrapper
echo "[scripts/bl wrapper]"
self_dir="$(cd "$(dirname "$0")" && pwd)"
if [ -x "$self_dir/bl" ]; then
  good "scripts/bl is executable"
else
  err "scripts/bl missing or not executable. Run: chmod +x scripts/bl"
fi

# Python 3.10+
echo "[python]"
if command -v python3 >/dev/null 2>&1; then
  pyver="$(python3 -c 'import sys; print(sys.version_info[:2])')"
  py_major="$(python3 -c 'import sys; print(sys.version_info[0])')"
  py_minor="$(python3 -c 'import sys; print(sys.version_info[1])')"
  if [ "$py_major" -ge 3 ] && [ "$py_minor" -ge 10 ]; then
    good "python3 found ($pyver)"
  else
    err "python3 too old ($pyver). Need 3.10+"
  fi
else
  err "python3 not found"
fi

# Shanyin references (optional)
echo "[shanyin craft references — optional]"
sh_sw="$(dirname "$self_dir")/references/shanyin/screenwriting-master/SKILL.md"
sh_dir="$(dirname "$self_dir")/references/shanyin/director-master/SKILL.md"
[ -f "$sh_sw" ] && good "shanyin-screenwriting-master present" || echo "  · not installed (optional). Run: ./scripts/install-deps.sh"
[ -f "$sh_dir" ] && good "shanyin-director-master present"     || echo "  · not installed (optional). Run: ./scripts/install-deps.sh"

# sub-skills present
echo "[sub-skills]"
for s in screenwriter director cast vfx-review clip-review episode; do
  f="$(dirname "$self_dir")/references/spark-video-$s/SKILL.md"
  [ -f "$f" ] && good "spark-video-$s SKILL.md present" || err "spark-video-$s SKILL.md MISSING"
done

echo
if $ok; then
  echo "All checks passed. spark-video is ready."
  exit 0
else
  echo "Some checks failed. Fix the ✗ items above before running the pipeline."
  exit 1
fi
