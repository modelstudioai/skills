# /// script
# requires-python = ">=3.10"
# dependencies = ["pydantic>=2.5"]
# ///
"""
render_all.py — batch-render all (or a subset of) shots in one command.

Reads storyboard.json, resolves media from cast.json / movie_set.json /
props.json, computes chain groups for parallelism, and invokes
render_shot.py per shot with correct arguments. Chain groups run in
parallel; shots within a chain run sequentially with first-frame bridging.

Usage:
    # Full reset — re-render everything from scratch:
    uv run scripts/render_all.py --reset --ratio 9:16

    # Only re-render shots that failed or have no winner:
    uv run scripts/render_all.py --failed-only

    # Only re-render shots whose review verdict was REJECT:
    uv run scripts/render_all.py --rejected-only

    # Re-render specific shots:
    uv run scripts/render_all.py --shot S01-002 --shot S03-004

    # Adjust concurrency:
    uv run scripts/render_all.py --reset --concurrency 8

Stdout: JSON summary {"accepted": N, "rejected": N, "failed": N, "total": N}
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from lib.storyboard import Storyboard  # noqa: E402
from lib.render_graph import compute_chain_groups  # noqa: E402


def _projects_root() -> Path:
    return Path(os.environ.get("VIDEOGEN_PROJECTS_DIR", "./projects")).resolve()


def _episode_dir() -> Path:
    proj = os.environ.get("SPARK_VIDEO_PROJECT")
    ep = os.environ.get("SPARK_VIDEO_EPISODE")
    if not proj or not ep:
        print("ERROR: SPARK_VIDEO_PROJECT and SPARK_VIDEO_EPISODE must be set",
              file=sys.stderr)
        sys.exit(2)
    ep_id = ep if ep.startswith("episode-") else f"episode-{ep}"
    return _projects_root() / proj / ep_id


def _load_json(p: Path):
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _resolve_media(shot, scenes_by_id: dict, cast_index: dict,
                   set_index: dict, prop_index: dict) -> list[str]:
    """Build the --media list for one shot: cast portraits → set image → props."""
    if shot.kind == "t2v":
        return []

    media = []

    for char in shot.characters:
        path = cast_index.get(char)
        if path and Path(path).exists():
            media.append(path)

    effective_set_id = shot.set_id
    if effective_set_id is None:
        scene = scenes_by_id.get(shot.scene)
        if scene:
            effective_set_id = scene.get("set_id")
    if effective_set_id and effective_set_id in set_index:
        path = set_index[effective_set_id]
        if path and Path(path).exists():
            media.append(path)

    for prop_name in (shot.props or []):
        path = prop_index.get(prop_name)
        if path and Path(path).exists():
            media.append(path)

    return media


_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def _parse_render_stdout(stdout: str) -> dict | None:
    """Extract the render result JSON from render_shot.py stdout.

    render_shot.py prints one JSON line as its result, but uv/pip install
    messages or _refresh_viewer() output may appear before or after it.
    We scan lines in reverse and return the first valid JSON with "shot_id".
    """
    if not stdout or not stdout.strip():
        return None
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict) and ("shot_id" in obj or "video_path" in obj):
                return obj
        except (json.JSONDecodeError, ValueError):
            continue
    return None


def _scan_first_image(folder: Path) -> str | None:
    """Return the first image file in a folder, or None."""
    if not folder.is_dir():
        return None
    for f in sorted(folder.iterdir()):
        if f.is_file() and f.suffix.lower() in _IMAGE_EXTS:
            return str(f)
    return None


def _build_cast_index(ep_dir: Path) -> dict[str, str]:
    """Map character name → portrait path from cast.json, with folder fallback."""
    proj_dir = ep_dir.parent
    data = _load_json(ep_dir / "cast.json")
    idx = {}
    if data:
        for c in data.get("characters", []) or []:
            name = c.get("name")
            img = c.get("image_local")
            if name and img:
                idx[name] = img
    if not idx:
        for d in [ep_dir / "cast", proj_dir / "cast"]:
            if not d.is_dir():
                continue
            for char_dir in sorted(d.iterdir()):
                if not char_dir.is_dir() or char_dir.name in idx:
                    continue
                img = _scan_first_image(char_dir)
                if img:
                    idx[char_dir.name] = img
    return idx


def _build_set_index(ep_dir: Path) -> dict[str, str]:
    """Map set name → set image path from movie_set.json, with folder fallback."""
    proj_dir = ep_dir.parent
    data = _load_json(ep_dir / "movie_set.json")
    idx = {}
    if data:
        for s in data.get("sets", []) or []:
            name = s.get("name")
            img = s.get("image_local")
            if name and img:
                idx[name] = img
    if not idx:
        for d in [ep_dir / "movie-set", proj_dir / "movie-set"]:
            if not d.is_dir():
                continue
            for set_dir in sorted(d.iterdir()):
                if not set_dir.is_dir() or set_dir.name in idx:
                    continue
                img = _scan_first_image(set_dir)
                if img:
                    idx[set_dir.name] = img
    return idx


def _build_prop_index(ep_dir: Path) -> dict[str, str]:
    """Map prop name → prop image path from props.json, with folder fallback."""
    proj_dir = ep_dir.parent
    data = _load_json(ep_dir / "props.json")
    idx = {}
    if data:
        for p in data.get("props", []) or []:
            name = p.get("name")
            img = p.get("image_local")
            if name and img:
                idx[name] = img
    if not idx:
        for d in [ep_dir / "props", proj_dir / "props"]:
            if not d.is_dir():
                continue
            for prop_dir in sorted(d.iterdir()):
                if not prop_dir.is_dir() or prop_dir.name in idx:
                    continue
                img = _scan_first_image(prop_dir)
                if img:
                    idx[prop_dir.name] = img
    return idx


def _should_render(shot_id: str, state: dict, *, mode: str) -> bool:
    """Decide whether a shot should be rendered based on filter mode."""
    if mode == "reset":
        return True
    entry = state.get(shot_id)
    if not entry:
        return True
    if mode == "failed-only":
        if entry.get("winner_version"):
            winner_path = entry.get("winner_path")
            if winner_path and Path(winner_path).exists():
                return False
        attempts = entry.get("attempts", [])
        if not attempts:
            return True
        last = attempts[-1]
        if last.get("status") == "FAILED":
            return True
        if not entry.get("winner_version"):
            return True
        return False
    if mode == "rejected-only":
        if entry.get("winner_version"):
            return False
        attempts = entry.get("attempts", [])
        if not attempts:
            return True
        last = attempts[-1]
        review = last.get("review", {})
        if review.get("verdict") == "REJECT":
            return True
        if last.get("status") == "FAILED":
            return True
        return False
    return True


def _render_chain_group(
    group: list[str],
    shots_by_id: dict,
    scenes_by_id: dict,
    cast_index: dict,
    set_index: dict,
    prop_index: dict,
    state: dict,
    *,
    mode: str,
    target_shots: list[str] | None = None,
    ratio: str | None,
    provider: str | None,
    no_review: bool,
) -> list[dict]:
    """Render one chain group sequentially, passing first-frame between shots."""
    results = []
    prev_last_frame: str | None = None

    for shot_id in group:
        if not _should_render(shot_id, state, mode=mode):
            results.append({"shot_id": shot_id, "skipped": True})
            entry = state.get(shot_id, {})
            attempts = entry.get("attempts", [])
            if attempts:
                last_ok = [a for a in attempts if a.get("last_frame_path")]
                if last_ok:
                    prev_last_frame = last_ok[-1]["last_frame_path"]
            continue

        shot = shots_by_id.get(shot_id)
        if not shot:
            results.append({"shot_id": shot_id, "error": "not in storyboard"})
            continue

        media = _resolve_media(shot, scenes_by_id, cast_index, set_index, prop_index)

        cmd = [
            "uv", "run", str(_HERE / "render_shot.py"),
            "--shot", shot_id,
            "--kind", shot.kind,
            "--prompt", shot.prompt,
            "--duration", str(shot.duration),
        ]
        if mode == "reset" and not target_shots:
            cmd.append("--reset-attempts")
        else:
            cmd.append("--force")

        if media:
            cmd.append("--media")
            cmd.extend(media)
        if ratio:
            cmd.extend(["--ratio", ratio])
        if provider:
            cmd.extend(["--provider", provider])
        if no_review:
            cmd.append("--no-review")
        if shot.seed is not None:
            cmd.extend(["--seed", str(shot.seed)])
        if shot.negative_prompt:
            cmd.extend(["--negative-prompt", shot.negative_prompt])
        if shot.characters:
            cmd.append("--characters")
            cmd.extend(shot.characters)

        if prev_last_frame and shot.use_prev_last_frame_as_first:
            if Path(prev_last_frame).exists():
                cmd.extend(["--first-frame", prev_last_frame])

        print(f"[render] {shot_id} ({shot.kind}, {shot.duration}s, "
              f"{len(shot.characters)} chars)", flush=True)

        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=600,
            )
            parsed = _parse_render_stdout(proc.stdout)
            if proc.returncode == 0 and parsed:
                parsed["shot_id"] = shot_id
                results.append(parsed)
                prev_last_frame = parsed.get("last_frame_path")
            else:
                stderr_tail = (proc.stderr or "")[-500:].strip()
                print(f"[render_all] {shot_id} failed (exit {proc.returncode}): "
                      f"{stderr_tail[:200]}", file=sys.stderr, flush=True)
                results.append({
                    "shot_id": shot_id,
                    "error": stderr_tail or f"exit {proc.returncode}",
                    "exit_code": proc.returncode,
                })
                prev_last_frame = None
        except subprocess.TimeoutExpired:
            print(f"[render_all] {shot_id} timed out (600s)", file=sys.stderr, flush=True)
            results.append({"shot_id": shot_id, "error": "timeout (600s)"})
            prev_last_frame = None
        except Exception as e:
            print(f"[render_all] {shot_id} exception: {e}", file=sys.stderr, flush=True)
            results.append({"shot_id": shot_id, "error": str(e)})
            prev_last_frame = None

    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--reset", action="store_true", default=True,
                       help="clear state and re-render all (default)")
    group.add_argument("--failed-only", action="store_true",
                       help="only re-render FAILED or winner-less shots")
    group.add_argument("--rejected-only", action="store_true",
                       help="only re-render REJECT verdict shots")
    ap.add_argument("--shot", action="append", default=[],
                    help="render specific shot(s) only; repeatable")
    ap.add_argument("--concurrency", type=int, default=None,
                    help="max parallel chain groups (default: SPARK_VIDEO_MAX_CONCURRENCY or 4)")
    ap.add_argument("--ratio", default=None, help="aspect ratio override (e.g. 9:16)")
    ap.add_argument("--provider", default=None, help="provider override")
    ap.add_argument("--no-review", action="store_true", help="skip auto-review")
    args = ap.parse_args()

    if args.failed_only:
        mode = "failed-only"
    elif args.rejected_only:
        mode = "rejected-only"
    else:
        mode = "reset"

    ep_dir = _episode_dir()
    sb_path = ep_dir / "storyboard.json"
    state_path = ep_dir / "shots_state.json"

    if not sb_path.exists():
        print("ERROR: storyboard.json not found. Run `storyboard.py compile` first.",
              file=sys.stderr)
        return 2

    sb = Storyboard.model_validate(json.loads(sb_path.read_text()))

    if mode == "reset" and not args.shot:
        state_path.write_text("{}")
        state = {}
        print("[render_all] state reset — rendering all shots from scratch")
    else:
        state = _load_json(state_path) or {}
        if args.shot:
            print(f"[render_all] re-rendering {args.shot} (preserving version history)")

    cast_index = _build_cast_index(ep_dir)
    set_index = _build_set_index(ep_dir)
    prop_index = _build_prop_index(ep_dir)

    shots_by_id = {s.id: s for s in sb.shots}
    scenes_by_id = {sc.id: {"set_id": sc.set_id} for sc in sb.scenes}

    groups = compute_chain_groups(sb)

    if args.shot:
        target_set = set(args.shot)
        groups = [[sid for sid in g if sid in target_set] for g in groups]
        groups = [g for g in groups if g]
        if not groups:
            print(f"ERROR: none of {args.shot} found in storyboard chain groups",
                  file=sys.stderr)
            return 2

    max_workers = args.concurrency or int(
        os.environ.get("SPARK_VIDEO_MAX_CONCURRENCY", "4"))

    total_shots = sum(len(g) for g in groups)
    print(f"[render_all] {total_shots} shots in {len(groups)} chain groups, "
          f"concurrency={max_workers}, mode={mode}")

    all_results = []

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = {}
        for i, group in enumerate(groups):
            future = pool.submit(
                _render_chain_group,
                group, shots_by_id, scenes_by_id,
                cast_index, set_index, prop_index, state,
                mode=mode, target_shots=args.shot or None,
                ratio=args.ratio, provider=args.provider,
                no_review=args.no_review,
            )
            futures[future] = i

        for future in as_completed(futures):
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                group_idx = futures[future]
                print(f"[render_all] chain group {group_idx} failed: {e}",
                      file=sys.stderr)

    # Ground-truth summary from shots_state.json (render_shot.py is the
    # single writer, so this is authoritative even if our stdout parsing
    # missed a result).
    final_state = _load_json(state_path) or {}
    rendered_ids = set()
    for g in groups:
        rendered_ids.update(g)

    accepted, rejected, failed, skipped = 0, 0, 0, 0
    rejected_details = []
    for sid in sorted(rendered_ids):
        proc_result = next((r for r in all_results if r.get("shot_id") == sid), None)
        if proc_result and proc_result.get("skipped"):
            skipped += 1
            continue
        entry = final_state.get(sid)
        if not entry or not entry.get("attempts"):
            failed += 1
            continue
        if entry.get("winner_version"):
            accepted += 1
            continue
        last_attempt = entry["attempts"][-1]
        if last_attempt.get("status") == "FAILED":
            failed += 1
            continue
        review = last_attempt.get("review", {})
        if review.get("verdict") == "REJECT":
            rejected += 1
            rejected_details.append({
                "shot_id": sid,
                "score": review.get("score"),
                "critique": review.get("critique", ""),
                "vetoed_axes": review.get("vetoed_axes"),
            })
        else:
            failed += 1

    summary = {
        "total": total_shots,
        "accepted": accepted,
        "rejected": rejected,
        "failed": failed,
        "skipped": skipped,
    }
    if rejected_details:
        summary["rejected_shots"] = rejected_details

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
