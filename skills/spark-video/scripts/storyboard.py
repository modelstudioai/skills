# /// script
# requires-python = ">=3.10"
# dependencies = ["pydantic>=2.5"]
# ///
"""
storyboard.py — storyboard operations (validate / compile / estimate / graph).

Subcommands:
    validate            Validate per-scene JSON fragments and/or full storyboard.json
    compile             Merge scenes/scene-*.{md,json} → script.md + storyboard.json
    estimate            Print render duration & cost estimate. Exit 2 if over budget.
    graph               Print chain-DAG parallel groups (JSON array of arrays).

All commands respect SPARK_VIDEO_PROJECT / SPARK_VIDEO_EPISODE env vars.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from lib.storyboard import Storyboard, Scene, Shot  # noqa: E402
from lib.render_graph import compute_chain_groups   # noqa: E402


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


# ------------------------------------------------------------------ validate

def cmd_validate(args: argparse.Namespace) -> int:
    ep_dir = _episode_dir()
    if args.scene is not None:
        # Validate one scene fragment
        sf = ep_dir / "scenes" / f"scene-{int(args.scene):02d}.json"
        if not sf.exists():
            print(f"ERROR: {sf} not found", file=sys.stderr)
            return 2
        data = json.loads(sf.read_text())
        # Construct a minimal Storyboard to validate the fragment
        sb_data = {
            "title": "validate-only",
            "scenes": [data["scene"]],
            "shots": data["shots"],
        }
        try:
            Storyboard.model_validate(sb_data)
        except Exception as e:
            print(f"VALIDATION FAILED for scene {args.scene}:\n{e}",
                  file=sys.stderr)
            return 1
        print(f"OK: scene-{int(args.scene):02d}.json validates")
        return 0

    # Validate full storyboard.json
    sb_path = ep_dir / "storyboard.json"
    if not sb_path.exists():
        print(f"ERROR: {sb_path} not found. Run `storyboard.py compile` first.",
              file=sys.stderr)
        return 2
    try:
        sb = Storyboard.model_validate(json.loads(sb_path.read_text()))
    except Exception as e:
        print(f"VALIDATION FAILED:\n{e}", file=sys.stderr)
        return 1

    # Lint warnings (non-fatal)
    warns = _lint(sb, ep_dir)
    for w in warns:
        print(f"WARN: {w}", file=sys.stderr)
    print(f"OK: {sb_path} validates ({len(sb.scenes)} scenes, "
          f"{len(sb.shots)} shots, {len(warns)} warnings)")
    return 0


def _lint(sb: Storyboard, ep_dir: Path) -> list[str]:
    """Cross-fragment lints that pure schema can't catch."""
    warns: list[str] = []

    # Load manifests if present
    cast_path = ep_dir / "cast.json"
    set_path = ep_dir / "movie_set.json"
    prop_path = ep_dir / "props.json"
    cast = _safe_load_json(cast_path)
    sets = _safe_load_json(set_path)
    props = _safe_load_json(prop_path)
    cast_names = _extract_names(cast)
    set_names = _extract_names(sets)
    prop_names = _extract_names(props)

    # Shot-level lints
    for shot in sb.shots:
        # Unknown characters
        for ch in (shot.characters or []):
            if cast_names and ch not in cast_names:
                warns.append(f"{shot.id}: character '{ch}' not in cast.json")
        # Unknown props
        for p in (shot.props or []):
            if prop_names and p not in prop_names:
                warns.append(f"{shot.id}: prop '{p}' not in props.json")
        # Props on t2v/i2v
        if shot.props and shot.kind in ("t2v", "i2v"):
            warns.append(f"{shot.id}: props attached to {shot.kind} shot "
                         "(no media[] slot — silently dropped)")
        # Unknown set_id
        sid = shot.set_id
        if sid and set_names and sid not in set_names:
            warns.append(f"{shot.id}: set_id '{sid}' not in movie_set.json")

    # Scene-level
    for sc in sb.scenes:
        if sc.set_id and set_names and sc.set_id not in set_names:
            warns.append(f"scene {sc.id}: set_id '{sc.set_id}' not in movie_set.json")

    # Chain-group lighting consistency
    groups = compute_chain_groups(sb)
    shot_by_id = {s.id: s for s in sb.shots}
    scene_by_id = {sc.id: sc for sc in sb.scenes}
    for group in groups:
        sets_seen = set()
        for sid in group:
            shot = shot_by_id.get(sid)
            if not shot or shot.kind != "r2v":
                continue
            effective_set = shot.set_id
            if effective_set is None:
                # inherit from scene
                sc = scene_by_id.get(shot.scene)
                effective_set = sc.set_id if sc else None
            if effective_set:
                sets_seen.add(effective_set)
        if len(sets_seen) > 1:
            warns.append(f"chain group {group[0]}..{group[-1]} mixes set_ids "
                         f"{sorted(sets_seen)} (灯光统一铁律: split the chain)")

    return warns


def _safe_load_json(p: Path) -> dict | None:
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def _extract_names(manifest: dict | None) -> set[str]:
    if not manifest:
        return set()
    # cast.json / movie_set.json / props.json share `{"<name>": {...}}` shape
    if isinstance(manifest, dict):
        # Some manifests nest under a top-level key
        for key in ("cast", "sets", "props", "entries", "items"):
            if isinstance(manifest.get(key), dict):
                return set(manifest[key].keys())
        return set(manifest.keys())
    return set()


# ------------------------------------------------------------------- compile

def cmd_compile(args: argparse.Namespace) -> int:
    ep_dir = _episode_dir()
    scenes_dir = ep_dir / "scenes"
    if not scenes_dir.exists():
        print(f"ERROR: {scenes_dir} not found", file=sys.stderr)
        return 2

    md_files = sorted(scenes_dir.glob("scene-*.md"))
    json_files = sorted(scenes_dir.glob("scene-*.json"))

    if not md_files:
        print("ERROR: no scene-*.md found", file=sys.stderr)
        return 1
    if len(json_files) != len(md_files):
        print(f"WARN: {len(md_files)} md vs {len(json_files)} json — "
              "director may not be done", file=sys.stderr)

    # Merge .md → script.md
    script_md = ep_dir / "script.md"
    parts = []
    proj = os.environ.get("SPARK_VIDEO_PROJECT")
    ep = os.environ.get("SPARK_VIDEO_EPISODE")
    parts.append(f"# {proj} / {ep}\n")
    for f in md_files:
        parts.append(f.read_text())
        parts.append("\n\n---\n\n")
    script_md.write_text("".join(parts).rstrip() + "\n")
    print(f"wrote {script_md}", file=sys.stderr)

    # Merge .json → storyboard.json
    scenes: list[dict] = []
    shots: list[dict] = []
    for f in json_files:
        try:
            frag = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            print(f"ERROR: {f.name} is not valid JSON: {e}", file=sys.stderr)
            return 1
        scenes.append(frag["scene"])
        shots.extend(frag["shots"])

    sb_data = {
        "title": proj or "untitled",
        "scenes": scenes,
        "shots": shots,
        "mode": args.mode,
        "provider": args.provider,
    }
    if args.narrator_voice:
        sb_data["narrator_voice"] = args.narrator_voice

    # Apply BGM config if present
    bgm_cfg_path = ep_dir / "bgm-config.json"
    if bgm_cfg_path.exists():
        sb_data["bgm"] = json.loads(bgm_cfg_path.read_text())

    try:
        sb = Storyboard.model_validate(sb_data)
    except Exception as e:
        print(f"VALIDATION FAILED during compile:\n{e}", file=sys.stderr)
        return 1

    sb_path = ep_dir / "storyboard.json"
    sb_path.write_text(json.dumps(sb.model_dump(), ensure_ascii=False, indent=2))
    print(f"wrote {sb_path} ({len(sb.scenes)} scenes, {len(sb.shots)} shots)",
          file=sys.stderr)
    return 0


# ------------------------------------------------------------------ estimate

def cmd_estimate(args: argparse.Namespace) -> int:
    ep_dir = _episode_dir()
    sb_path = ep_dir / "storyboard.json"
    sb = Storyboard.model_validate(json.loads(sb_path.read_text()))

    total_sec = sum(int(s.duration) for s in sb.shots)
    n_shots = len(sb.shots)
    groups = compute_chain_groups(sb)
    max_concurrency = int(os.environ.get("SPARK_VIDEO_MAX_CONCURRENCY", "4"))
    # Naive wall-clock: longest group's serialized time / concurrency
    group_times = [sum(int(_lookup(sb, sid).duration) for sid in g) for g in groups]
    wall_clock_factor = 1.5  # render_time ≈ 1.5x clip duration (rough)
    est_serial = sum(group_times) * wall_clock_factor
    est_parallel = max(group_times) * wall_clock_factor if groups else 0
    est_with_cap = est_parallel * max(1, len(groups) / max_concurrency)

    long_confirm = int(os.environ.get("SPARK_VIDEO_LONG_CONFIRM_S", "600"))

    out = {
        "shots": n_shots,
        "total_clip_seconds": total_sec,
        "parallel_groups": len(groups),
        "estimated_render_seconds_serial": int(est_serial),
        "estimated_render_seconds_parallel": int(est_parallel),
        "estimated_render_seconds_with_concurrency_cap": int(est_with_cap),
        "concurrency_cap": max_concurrency,
        "long_confirm_threshold_s": long_confirm,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

    if total_sec > long_confirm:
        print(f"\nWARN: total clip duration {total_sec}s exceeds "
              f"SPARK_VIDEO_LONG_CONFIRM_S={long_confirm}s — get user confirm.",
              file=sys.stderr)
        return 2
    return 0


def _lookup(sb: Storyboard, shot_id: str) -> Shot:
    for s in sb.shots:
        if s.id == shot_id:
            return s
    raise KeyError(shot_id)


# --------------------------------------------------------------------- graph

def cmd_graph(args: argparse.Namespace) -> int:
    ep_dir = _episode_dir()
    sb_path = ep_dir / "storyboard.json"
    sb = Storyboard.model_validate(json.loads(sb_path.read_text()))
    groups = compute_chain_groups(sb)
    if args.json:
        print(json.dumps(groups, ensure_ascii=False))
    else:
        print(f"# {len(groups)} parallel chain groups, max group size = "
              f"{max(len(g) for g in groups) if groups else 0}")
        for i, g in enumerate(groups, 1):
            print(f"{i:3d}. [{len(g)} shots] {' → '.join(g)}")
    return 0


# ----------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate")
    p_val.add_argument("--scene", type=int, default=None,
                       help="validate one scene fragment instead of full storyboard")
    p_val.set_defaults(fn=cmd_validate)

    p_cmp = sub.add_parser("compile")
    p_cmp.add_argument("--mode", choices=["drama", "narration"], default="drama")
    p_cmp.add_argument("--provider", default=None,
                       help="default: $SPARK_VIDEO_PROVIDER or 'bl'")
    p_cmp.add_argument("--narrator-voice", default=None)
    p_cmp.set_defaults(fn=cmd_compile)

    p_est = sub.add_parser("estimate")
    p_est.set_defaults(fn=cmd_estimate)

    p_gr = sub.add_parser("graph")
    p_gr.add_argument("--json", action="store_true",
                      help="output JSON array of arrays")
    p_gr.set_defaults(fn=cmd_graph)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
