# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
gate.py — deterministic "did we actually do it?" verifier for the pipeline.

This is the *verify-don't-constrain* half of the stability story. It does
NOT tell an agent how to do its work and it does NOT replace the human
confirmation gates — it just checks that the mandatory, no-judgment
artifacts a stage is supposed to leave behind actually exist and are
internally consistent. Inferior agents that "forget" to score a clip or
to build the viewer get caught here instead of shipping a broken episode.

It reads only files (stdlib, no pydantic / no network) so it can run
anywhere — in a skill step, in a CI check, or wired to a framework "stop"
hook (Cursor / Claude Code) so the agent cannot end its turn while a
mandatory artifact is missing. Full schema validation still lives in
`storyboard.py validate`; this is cross-artifact completeness.

Gates (mirror the producer's user-confirmation gates):
    script      GATE 1 — script.md present
    storyboard  GATE 2 — storyboard.json present + structurally sane
    render      GATE 3 — every shot rendered, scored, and won (or escalated)
    final       GATE 4 — final mp4 + a fresh viewer.html exist
    all         run every gate and report a matrix

Usage:
    SPARK_VIDEO_PROJECT=hf SPARK_VIDEO_EPISODE=001 \\
        uv run scripts/gate.py check render
    uv run scripts/gate.py check all --json
    uv run scripts/gate.py check render --project hf --episode 001 --json

Exit codes:
    0 = gate passed (all error-severity checks ok)
    1 = gate failed (at least one error-severity check failed)
    2 = usage / precondition error (e.g. project/episode not set)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

GATES = ("script", "storyboard", "render", "final")


def _projects_root() -> Path:
    return Path(os.environ.get("VIDEOGEN_PROJECTS_DIR", "./projects")).resolve()


def _normalize_episode(ep: str) -> str:
    ep = ep.strip()
    return ep if ep.startswith("episode-") or ep.startswith("episode_") else f"episode-{ep}"


def _threshold() -> float:
    for n in ("SPARK_VIDEO_REVIEW_THRESHOLD", "VIDEOGEN_REVIEW_THRESHOLD"):
        v = os.environ.get(n)
        if v:
            try:
                return float(v)
            except ValueError:
                pass
    return 7.0


def _load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _shots(sb: dict) -> list[dict]:
    """Pull the flat shot list from a compiled storyboard (top-level or nested)."""
    if isinstance(sb.get("shots"), list):
        return [s for s in sb["shots"] if isinstance(s, dict)]
    out: list[dict] = []
    for sc in sb.get("scenes", []) or []:
        if isinstance(sc, dict) and isinstance(sc.get("shots"), list):
            out.extend(s for s in sc["shots"] if isinstance(s, dict))
    return out


# --------------------------------------------------------------------------- model

@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""
    severity: str = "error"  # "error" blocks the gate; "warn" is advisory


@dataclass
class GateResult:
    gate: str
    checks: list[Check] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.ok for c in self.checks if c.severity == "error")

    def add(self, name: str, ok: bool, detail: str = "", severity: str = "error") -> None:
        self.checks.append(Check(name, ok, detail, severity))


# --------------------------------------------------------------------------- gates

def gate_script(ep_dir: Path) -> GateResult:
    r = GateResult("script")
    script = ep_dir / "script.md"
    text = script.read_text(encoding="utf-8") if script.exists() else ""
    r.add("script.md exists & non-empty", bool(text.strip()),
          str(script) if not text.strip() else f"{len(text)} chars")

    scenes_dir = ep_dir / "scenes"
    md = sorted(scenes_dir.glob("scene-*.md")) if scenes_dir.exists() else []
    js = sorted(scenes_dir.glob("scene-*.json")) if scenes_dir.exists() else []
    r.add("at least one scene-*.md", bool(md), f"{len(md)} found", severity="warn")
    r.add("director done (scene-*.json count == scene-*.md count)",
          bool(md) and len(js) == len(md), f"{len(md)} md / {len(js)} json",
          severity="warn")
    return r


def gate_storyboard(ep_dir: Path) -> GateResult:
    r = GateResult("storyboard")
    sb_path = ep_dir / "storyboard.json"
    if not sb_path.exists():
        r.add("storyboard.json exists", False,
              f"{sb_path} missing — run storyboard.py compile")
        return r
    r.add("storyboard.json exists", True, str(sb_path))
    sb = _load_json(sb_path)
    if sb is None:
        r.add("storyboard.json is valid JSON", False, "parse error")
        return r
    r.add("storyboard.json is valid JSON", True)

    shots = _shots(sb)
    r.add("has at least one shot", bool(shots), f"{len(shots)} shots")

    # Light structural checks (full schema check = `storyboard.py validate`).
    bad = [s.get("id", "<no-id>") for s in shots
           if not s.get("id") or not (s.get("prompt") or "").strip()]
    r.add("every shot has id + non-empty prompt", not bad,
          f"offenders: {bad[:5]}" if bad else "")
    ids = [s.get("id") for s in shots if s.get("id")]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    r.add("no duplicate shot ids", not dupes, f"dupes: {dupes}" if dupes else "")
    r.add("run `storyboard.py validate` for full schema lint", True,
          "reminder", severity="warn")
    return r


def gate_render(ep_dir: Path) -> GateResult:
    r = GateResult("render")
    sb = _load_json(ep_dir / "storyboard.json")
    if sb is None:
        r.add("storyboard.json present", False, "compile the storyboard first")
        return r
    shots = _shots(sb)
    if not shots:
        r.add("storyboard has shots", False)
        return r

    state = _load_json(ep_dir / "shots_state.json")
    if state is None:
        r.add("shots_state.json present", False, "nothing has been rendered yet")
        return r
    r.add("shots_state.json present", True)

    clips_dir = ep_dir / "clips"
    thr = _threshold()
    not_won: list[str] = []
    missing_clip: list[str] = []
    unscored: list[str] = []          # winner has no numeric review score
    review_errors: list[str] = []     # review ran but verdict ERROR/unknown
    below_thr: list[str] = []         # accepted under threshold (best-of-N)

    for shot in shots:
        sid = shot.get("id")
        if not sid:
            continue
        entry = state.get(sid) or {}
        winner = entry.get("winner_version")
        if not winner:
            not_won.append(sid)
            continue
        if not (clips_dir / f"{sid}.mp4").exists():
            missing_clip.append(sid)
        attempts = entry.get("attempts", []) or []
        wa = next((a for a in attempts if a.get("version") == winner), None)
        review = (wa or {}).get("review") or {}
        score = review.get("score")
        verdict = review.get("verdict")
        if isinstance(score, (int, float)):
            if score < thr:
                below_thr.append(f"{sid}({score})")
        elif verdict in ("ERROR", None, ""):
            # No numeric score AND no clean verdict → scoring was skipped or failed.
            (review_errors if verdict == "ERROR" else unscored).append(sid)

    n = len(shots)
    r.add("every shot has a winner_version", not not_won,
          f"{n - len(not_won)}/{n} won; missing: {not_won[:8]}" if not_won
          else f"{n}/{n}")
    r.add("every winner clip exists on disk", not missing_clip,
          f"missing clips/<id>.mp4: {missing_clip[:8]}" if missing_clip else "")
    r.add("every winner is scored (review.score present)", not unscored,
          f"UNSCORED (scoring skipped?): {unscored[:8]}" if unscored else "")
    r.add("no winner left with a failed review", not review_errors,
          f"review ERROR: {review_errors[:8]}" if review_errors else "",
          severity="warn")
    r.add("accepted-below-threshold shots (best-of-N)", True,
          f"{below_thr[:8]} (threshold {thr:g})" if below_thr
          else f"none under {thr:g}", severity="warn")

    esc = _load_json(ep_dir / "needs_director_rewrite.json")
    open_esc = (esc or {}).get("shots") if isinstance(esc, dict) else None
    r.add("no unresolved director escalation", not open_esc,
          f"needs_director_rewrite.json open for: {open_esc}" if open_esc else "")
    return r


def gate_final(ep_dir: Path) -> GateResult:
    r = GateResult("final")
    final_dir = ep_dir / "final"
    mp4s = [p for p in final_dir.glob("*.mp4") if p.stat().st_size > 0] \
        if final_dir.exists() else []
    r.add("final/*.mp4 exists & non-empty", bool(mp4s),
          f"{[p.name for p in mp4s]}" if mp4s else "run stitch.py")

    viewer = ep_dir / "viewer.html"
    r.add("viewer.html exists", viewer.exists(),
          str(viewer) if not viewer.exists() else "")
    if viewer.exists() and mp4s:
        newest_mp4 = max(p.stat().st_mtime for p in mp4s)
        fresh = viewer.stat().st_mtime >= newest_mp4 - 1  # 1s slack
        r.add("viewer.html is newer than final mp4", fresh,
              "viewer is stale — re-run build_viewer.py / stitch.py" if not fresh
              else "", severity="warn")
    return r


_GATE_FNS = {
    "script": gate_script,
    "storyboard": gate_storyboard,
    "render": gate_render,
    "final": gate_final,
}


# ---------------------------------------------------------------------------- output

_MARK = {("error", True): "[ ok ]", ("error", False): "[FAIL]",
         ("warn", True): "[ ok ]", ("warn", False): "[warn]"}


def _print_human(results: list[GateResult]) -> None:
    for res in results:
        status = "PASS" if res.passed else "FAIL"
        print(f"GATE {res.gate}: {status}")
        for c in res.checks:
            mark = _MARK[(c.severity, c.ok)]
            line = f"  {mark} {c.name}"
            if c.detail:
                line += f" — {c.detail}"
            print(line)
        print()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check", help="verify a gate's mandatory artifacts")
    p.add_argument("gate", choices=[*GATES, "all"])
    p.add_argument("--project", default=None, help="default: $SPARK_VIDEO_PROJECT")
    p.add_argument("--episode", default=None, help="default: $SPARK_VIDEO_EPISODE")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    project = args.project or os.environ.get("SPARK_VIDEO_PROJECT")
    episode = args.episode or os.environ.get("SPARK_VIDEO_EPISODE")
    if not project or not episode:
        print("ERROR: set SPARK_VIDEO_PROJECT and SPARK_VIDEO_EPISODE "
              "(or pass --project/--episode)", file=sys.stderr)
        return 2

    ep_dir = _projects_root() / project / _normalize_episode(episode)
    if not ep_dir.exists():
        print(f"ERROR: episode dir not found: {ep_dir}", file=sys.stderr)
        return 2

    gates = list(GATES) if args.gate == "all" else [args.gate]
    results = [_GATE_FNS[g](ep_dir) for g in gates]
    overall = all(res.passed for res in results)

    if args.json:
        print(json.dumps({
            "project": project,
            "episode": _normalize_episode(episode),
            "requested": args.gate,
            "passed": overall,
            "gates": [{
                "gate": res.gate,
                "passed": res.passed,
                "checks": [vars(c) for c in res.checks],
            } for res in results],
        }, ensure_ascii=False, indent=2))
    else:
        _print_human(results)
        if not overall:
            failed = [c.name for res in results for c in res.checks
                      if c.severity == "error" and not c.ok]
            print(f"FAILED checks: {failed}", file=sys.stderr)

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
