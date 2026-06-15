"""
review.py — deterministic per-clip scoring (the engineering spine of Zone 3).

Historically the *mechanics* of scoring a rendered clip (build the
``./scripts/bl omni`` call, attach the right cast portraits, parse the
6-axis JSON, average it, decide ACCEPT/REJECT by threshold) lived only as
prose in ``references/spark-video-clip-review/SKILL.md``. Weak agents
sometimes skipped it entirely and a clip would sail through unscored.

This module moves all of that *non-judgment* work into deterministic code
so it cannot be skipped. The agent keeps the judgment: *how* to rewrite a
failing prompt, *when* to escalate, *what* to tell the director.

What stays the agent's job (NOT here):
  * rewriting the prompt on REJECT (creative, failure-mode specific)
  * writing the escalation report for the director
  * deciding best-of-N vs re-cut-the-shot-group when retries are exhausted

Design notes:
  * This module is imported by ``scripts/render_shot.py``, whose uv env
    only declares ``requests`` — so we deliberately avoid importing
    ``lib.config`` (it pulls in ``python-dotenv``). Config is read straight
    from the environment here.
  * We NEVER write ``shots_state.json`` (that file has exactly one writer,
    ``render_shot.py``, guarded by flock). We only write the per-attempt
    sidecar ``reviews/<shot>-ver<N>.json`` and return the review dict for
    the caller to embed into the locked state update.

Public API:
    review_enabled() -> bool
    threshold() -> float
    score_clip(...) -> dict | None
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_BL_WRAPPER = _REPO_ROOT / "scripts" / "bl"
_RUBRIC = _REPO_ROOT / "references" / "spark-video-clip-review" / "rubric.md"

# The six axes, in the canonical order the rubric emits them.
AXES = ("logic", "proportion", "physics", "style", "cast_match", "dialog_attribution")

_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


# --------------------------------------------------------------------------- config

def _env(*names: str, default: str = "") -> str:
    """First non-None env var among names (SPARK_VIDEO_* beats VIDEOGEN_*)."""
    for n in names:
        v = os.environ.get(n)
        if v is not None:
            return v
    return default


def review_enabled() -> bool:
    """Review runs unless the review model is explicitly cleared.

    Mirrors the .env.example contract: ``VIDEOGEN_REVIEW_MODEL=""`` disables
    review. ``SPARK_VIDEO_REVIEW_MODEL`` takes precedence when set.
    """
    raw = _env("SPARK_VIDEO_REVIEW_MODEL", "VIDEOGEN_REVIEW_MODEL", default="__unset__")
    if raw == "__unset__":
        return True  # default-on
    return bool(raw.strip())


def threshold() -> float:
    raw = _env("SPARK_VIDEO_REVIEW_THRESHOLD", "VIDEOGEN_REVIEW_THRESHOLD", default="7.0")
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 7.0


def _veto_floor() -> float:
    """Any single axis scoring at or below this floor triggers an automatic REJECT.

    Default 5.0 — a score of 5 or below on any axis means a critical defect
    (e.g. wrong action, broken anatomy, wrong identity) that should not pass
    regardless of how high other axes score.
    """
    raw = _env("SPARK_VIDEO_REVIEW_VETO_FLOOR", "VIDEOGEN_REVIEW_VETO_FLOOR", default="5.0")
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 5.0


def _timeout_s() -> int:
    try:
        return int(_env("SPARK_VIDEO_REVIEW_TIMEOUT_S",
                        "VIDEOGEN_REVIEW_TIMEOUT_S", default="300"))
    except (TypeError, ValueError):
        return 300


def _omni_model_override() -> str | None:
    """Advanced override: pass a concrete --model to ``bl omni``.

    Off by default — the documented working call lets the ``omni``
    subcommand pick its own model. Power users who want to pin a specific
    multimodal judge set ``SPARK_VIDEO_REVIEW_OMNI_MODEL``.
    """
    v = _env("SPARK_VIDEO_REVIEW_OMNI_MODEL", default="").strip()
    return v or None


# ----------------------------------------------------------------- cast portraits

def _resolve_cast_portraits(ep_dir: Path, characters: list[str]) -> tuple[list[Path], list[str]]:
    """Map shot.characters → portrait image paths via cast.json.

    Returns (resolved_paths, missing_names). Reuses the exact ``image_local``
    the renderer fed the model so cast_match compares like-for-like. Falls
    back to scanning cast folders if cast.json lacks an entry.
    """
    if not characters:
        return [], []
    cast_path = ep_dir / "cast.json"
    by_name: dict[str, str] = {}
    if cast_path.exists():
        try:
            data = json.loads(cast_path.read_text(encoding="utf-8"))
            for c in data.get("characters", []) or []:
                name = c.get("name")
                img = c.get("image_local")
                if name and img:
                    by_name[name] = img
        except (json.JSONDecodeError, OSError):
            pass

    resolved: list[Path] = []
    missing: list[str] = []
    for ch in characters:
        p = by_name.get(ch)
        path = Path(p) if p else None
        if path and path.exists():
            resolved.append(path)
            continue
        scanned = _scan_for_portrait(ep_dir, ch)
        if scanned:
            resolved.append(scanned)
        else:
            missing.append(ch)
    return resolved, missing


def _scan_for_portrait(ep_dir: Path, character: str) -> Path | None:
    """Best-effort: find a portrait under cast/<character>/ (episode then project)."""
    candidates = [
        ep_dir / "cast" / character,
        ep_dir.parent / "cast" / character,
    ]
    for folder in candidates:
        if not folder.is_dir():
            continue
        imgs = sorted(p for p in folder.iterdir()
                      if p.is_file() and p.suffix.lower() in _IMAGE_EXTS)
        if imgs:
            return imgs[0]
    return None


# ------------------------------------------------------------------- omni parsing

def _coerce_scores(obj: object) -> dict | None:
    """If obj is a mapping carrying all six axes, normalise it; else None."""
    if not isinstance(obj, dict):
        return None
    if not all(k in obj for k in AXES):
        return None
    breakdown: dict[str, float] = {}
    for k in AXES:
        try:
            breakdown[k] = float(obj[k])
        except (TypeError, ValueError):
            return None
    verdict = str(obj.get("verdict", "")).upper().strip()
    critique = obj.get("critique", "")
    return {
        "breakdown": breakdown,
        "verdict": verdict if verdict in ("ACCEPT", "REJECT") else "",
        "critique": critique if isinstance(critique, str) else "",
    }


def _iter_json_objects(text: str):
    """Yield top-level balanced ``{...}`` substrings from arbitrary text."""
    depth = 0
    start = -1
    in_str = False
    esc = False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    yield text[start:i + 1]


def _search_scores(node: object, _depth: int = 0) -> dict | None:
    """Recursively hunt for the 6-axis object inside parsed/embedded JSON."""
    if _depth > 6:
        return None
    direct = _coerce_scores(node)
    if direct:
        return direct
    if isinstance(node, dict):
        for v in node.values():
            found = _search_scores(v, _depth + 1)
            if found:
                return found
    elif isinstance(node, list):
        for v in node:
            found = _search_scores(v, _depth + 1)
            if found:
                return found
    elif isinstance(node, str):
        s = node.strip()
        # strip ```json fences the model sometimes adds despite instructions
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s).strip()
        if "{" in s:
            try:
                return _search_scores(json.loads(s), _depth + 1)
            except (json.JSONDecodeError, ValueError):
                for cand in _iter_json_objects(s):
                    try:
                        got = _coerce_scores(json.loads(cand))
                    except (json.JSONDecodeError, ValueError):
                        got = None
                    if got:
                        return got
    return None


def parse_omni_output(stdout: str) -> dict | None:
    """Extract the 6-axis review from ``bl omni`` stdout, however it's wrapped.

    Handles: raw model JSON, ``--output json`` envelopes that nest the model
    text under content/text/output/..., and fenced or prose-wrapped JSON.
    """
    text = (stdout or "").strip()
    if not text:
        return None
    try:
        return _search_scores(json.loads(text))
    except (json.JSONDecodeError, ValueError):
        pass
    # Not valid JSON as a whole — scan for embedded objects.
    for cand in _iter_json_objects(text):
        try:
            got = _coerce_scores(json.loads(cand))
        except (json.JSONDecodeError, ValueError):
            got = None
        if got:
            return got
    return None


# ------------------------------------------------------------------------- scoring

def _build_message(*, shot_id: str, characters: list[str], prompt: str,
                   duration: int, thr: float) -> str:
    chars = ", ".join(characters) if characters else "no specified characters (cast_match: undeclared characters should not appear)"
    return (
        f"Score this video on 6 axes (0-10). Output strict JSON: "
        f"{{logic, proportion, physics, style, cast_match, dialog_attribution, critique, verdict}}. "
        f"Threshold {thr:g} (six-axis average >= threshold -> ACCEPT, else REJECT). "
        f"Video duration ~{duration}s. Shot {shot_id}. Expected characters: {chars}. "
        f"Shot content and dialog (from storyboard prompt): {prompt}"
    )


def _run_omni(cmd: list[str], *, timeout: int) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, cwd=str(_REPO_ROOT),
    )


def score_clip(
    *,
    ep_dir: Path,
    shot_id: str,
    version: int,
    video_path: Path,
    characters: list[str] | None,
    prompt: str,
    duration: int,
) -> dict | None:
    """Score one rendered clip on the 6 rubric axes via ``./scripts/bl omni``.

    Returns a review dict ready to embed into the shot's attempt record, or
    ``None`` when review is disabled. On any hard failure it returns a review
    with ``verdict="ERROR"`` (and ``score=None``) rather than raising — a
    render must never be *lost* just because the judge was unreachable; the
    gate (scripts/gate.py) surfaces ERROR/UNKNOWN reviews so they aren't
    silently treated as passes.

    Side effect: writes the sidecar ``reviews/<shot>-ver<N>.json``.
    """
    if not review_enabled():
        return None

    characters = characters or []
    thr = threshold()
    ts = datetime.now(timezone.utc).isoformat()
    reviews_dir = ep_dir / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)

    def _finalize(review: dict) -> dict:
        review.setdefault("shot_id", shot_id)
        review.setdefault("version", version)
        review.setdefault("ts", ts)
        review.setdefault("threshold", thr)
        try:
            (reviews_dir / f"{shot_id}-ver{version}.json").write_text(
                json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8",
            )
        except OSError as e:
            print(f"warn: could not write review sidecar for {shot_id} v{version}: {e}",
                  file=sys.stderr)
        return review

    if not _RUBRIC.exists():
        return _finalize({
            "score": None, "verdict": "ERROR",
            "error": f"rubric not found at {_RUBRIC}",
        })
    if not _BL_WRAPPER.exists():
        return _finalize({
            "score": None, "verdict": "ERROR",
            "error": f"bl wrapper not found at {_BL_WRAPPER}",
        })
    if not Path(video_path).exists():
        return _finalize({
            "score": None, "verdict": "ERROR",
            "error": f"clip not found at {video_path}",
        })

    portraits, missing = _resolve_cast_portraits(ep_dir, characters)
    if missing:
        print(f"warn: review {shot_id} v{version}: no portrait for {missing} "
              f"(cast_match will be weaker)", file=sys.stderr)

    cmd: list[str] = [str(_BL_WRAPPER), "omni"]
    model = _omni_model_override()
    if model:
        cmd += ["--model", model]
    cmd += ["--system", _RUBRIC.read_text(encoding="utf-8")]
    cmd += ["--message", _build_message(
        shot_id=shot_id, characters=characters, prompt=prompt,
        duration=duration, thr=thr,
    )]
    cmd += ["--video", str(Path(video_path).resolve())]
    for p in portraits:
        cmd += ["--image", str(p.resolve())]
    cmd += ["--text-only", "--output", "json"]

    # Tag the bl-wrapper log line as a review call.
    os.environ["SPARK_VIDEO_PHASE"] = "review"
    os.environ["SPARK_VIDEO_SHOT"] = shot_id
    os.environ["SPARK_VIDEO_ATTEMPT"] = str(version)

    timeout = _timeout_s()
    last_err = ""
    # Up to 2 attempts: the model occasionally emits malformed / 5-axis JSON.
    for attempt in range(2):
        try:
            proc = _run_omni(cmd, timeout=timeout)
        except subprocess.TimeoutExpired:
            last_err = f"bl omni timed out after {timeout}s"
            continue
        if proc.returncode != 0:
            last_err = f"bl omni exited {proc.returncode}: {proc.stderr[-500:].strip()}"
            # If the model flag was rejected, retry once without it.
            if model and "--model" in cmd and "model" in (proc.stderr or "").lower():
                idx = cmd.index("--model")
                del cmd[idx:idx + 2]
                model = None
            continue
        parsed = parse_omni_output(proc.stdout)
        if parsed:
            breakdown = parsed["breakdown"]
            score = round(sum(breakdown.values()) / len(AXES), 2)
            # Single-axis veto: any axis <= 5 forces REJECT regardless of avg.
            veto_floor = _veto_floor()
            vetoed_axes = [k for k, v in breakdown.items() if v <= veto_floor]
            if vetoed_axes:
                verdict = "REJECT"
            elif score >= thr:
                verdict = "ACCEPT"
            else:
                verdict = "REJECT"
            return _finalize({
                "score": score,
                "breakdown": breakdown,
                "verdict": verdict,
                "model_verdict": parsed.get("verdict") or None,
                "critique": parsed.get("critique", ""),
                "vetoed_axes": vetoed_axes if vetoed_axes else None,
            })
        last_err = f"could not parse 6-axis JSON from omni output: {proc.stdout[-400:].strip()}"

    return _finalize({"score": None, "verdict": "ERROR", "error": last_err})
