#!/usr/bin/env bash
# spark-video-gate.sh — Cursor `stop` hook implementing Scheme D enforcement.
#
# When the agent tries to end a turn, this nudges it to finish the
# mandatory, NO-JUDGMENT artifacts of an in-progress episode (every clip
# scored + a winner promoted, a fresh viewer.html, no unresolved director
# escalation) — WITHOUT dictating how to do the creative work. It is the
# "verify, don't constrain" safety net for inferior agents that skip steps.
#
# Behaviour:
#   * Auto-detects the most-recently-touched in-progress episode under
#     projects/ (none → stays silent, so dev/code sessions are unaffected).
#   * Runs scripts/gate.py (stdlib-only, no uv needed) for the relevant gate.
#   * Gate passes → allow silently. Gate fails → returns a followup_message
#     listing exactly what's missing.
#   * FAILS OPEN: any error/timeout → allow silently. Never blocks the user.
#
# Disable: remove the `stop` entry from .cursor/hooks.json (or delete this
# file). loop_limit in hooks.json caps how many times it can re-nudge.

python3 - <<'PY' 2>/dev/null || printf '{}\n'
import glob, json, os, subprocess, sys

# Consume stdin (we derive state from the filesystem, not the event).
try:
    sys.stdin.read()
except Exception:
    pass

def allow():
    print("{}")
    raise SystemExit(0)

# Honor the same projects root gate.py uses, so detection and the check agree.
root = os.environ.get("VIDEOGEN_PROJECTS_DIR", "projects")
if not os.path.isdir(root):
    allow()

# Most-recently-modified episode that has a compiled storyboard.
sbs = glob.glob(os.path.join(root, "*", "episode-*", "storyboard.json"))
if not sbs:
    allow()
ep_path = max((os.path.dirname(s) for s in sbs), key=os.path.getmtime)
project = os.path.basename(os.path.dirname(ep_path))   # <p>
episode = os.path.basename(ep_path)                    # episode-<NNN>

# Only police the late gates that agents actually skip.
if glob.glob(os.path.join(ep_path, "final", "*.mp4")):
    gate = "final"
elif os.path.exists(os.path.join(ep_path, "shots_state.json")):
    gate = "render"
else:
    allow()

try:
    proc = subprocess.run(
        [sys.executable, "scripts/gate.py", "check", gate,
         "--project", project, "--episode", episode, "--json"],
        capture_output=True, text=True, timeout=60,
    )
    data = json.loads(proc.stdout)
except Exception:
    allow()

if data.get("passed"):
    allow()

failing = [c["name"] + (f" ({c['detail']})" if c.get("detail") else "")
           for g in data.get("gates", []) for c in g.get("checks", [])
           if c.get("severity") == "error" and not c.get("ok")]
if not failing:
    allow()

msg = (
    f"[spark-video gate:{gate}] {project}/{episode} has unfinished mandatory "
    f"steps before this gate:\n- " + "\n- ".join(failing) +
    f"\n\nFinish them (usually: re-run scripts/render_shot.py for the listed "
    f"shots so they get scored + promoted, or scripts/stitch.py to rebuild the "
    f"final cut + viewer.html), then verify with "
    f"`uv run scripts/gate.py check {gate}`. "
    f"If the user intentionally paused this production run, ignore this."
)
print(json.dumps({"followup_message": msg}))
PY
