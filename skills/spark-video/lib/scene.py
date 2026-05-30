"""Per-scene file pipeline — the contract between screenwriter and director.

The screenwriter writes one scene at a time so the director can start
storyboarding scene N while screenwriter is still drafting scene N+1.

Files in `projects/<id>/<episode>/scenes/`:
  scene-NN.md    ← screenwriter output (single scene block)
  scene-NN.ready ← sentinel: screenwriter touched it after writing .md
  scene-NN.json  ← director output (one Scene + its Shots)

`scene compile` then merges all fragments into the canonical
`script.md` + `storyboard.json` that the rest of the CLI consumes.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from lib.config import SETTINGS
from lib import state
from lib.storyboard import EpisodeMode, Scene, Shot, Storyboard

SCENE_NUM_RE = re.compile(r"^scene-(\d{2,3})\.md$")
SCENE_FRAGMENT_RE = re.compile(r"^scene-(\d{2,3})\.json$")


def scenes_dir(project_id: str, episode_id: str) -> Path:
    edir = state.episode_dir(project_id, episode_id)
    p = edir / "scenes"
    p.mkdir(parents=True, exist_ok=True)
    return p


def scene_md_path(project_id: str, episode_id: str, num: int) -> Path:
    return scenes_dir(project_id, episode_id) / f"scene-{num:02d}.md"


def scene_ready_path(project_id: str, episode_id: str, num: int) -> Path:
    return scenes_dir(project_id, episode_id) / f"scene-{num:02d}.ready"


def scene_json_path(project_id: str, episode_id: str, num: int) -> Path:
    return scenes_dir(project_id, episode_id) / f"scene-{num:02d}.json"


SCENE_TEMPLATE_DRAMA = """\
## 场景 {n} — <location>（<time of day>）

**人物**: <characters in this scene, names from cast.json only>
**节奏**: <外部节奏>（外部）+ <内部节奏>（内部）
**预估时长**: <integer>s
**前史**: <one sentence — what the characters carry into this scene>

**剧情**:
<2-4 sentences. Camera-visible action only. 山音 红线 applies.>

**对白**:
- <角色A>: "<dialog>"
- <角色B>: "<dialog>"
"""

# Narration mode — beats are an ordered sequence of 旁白/对白 mixes.
# Each 旁白 beat becomes ONE narration shot at render time (TTS replaces
# audio). Each 对白 beat becomes a regular drama shot.
SCENE_TEMPLATE_NARRATION = """\
## 场景 {n} — <location>（<time of day>）

**类型**: narration
**人物**: <characters that appear in any beat — names from cast.json only>
**预估时长**: <integer>s   # ≈ Σ节拍时长
**前史**: <one sentence>

**节拍**:
1. **旁白**: "<≤2句、≤60字的解说词>"
   **画面**: <一句话描述; 建议时长 4s>
2. **旁白**: "<下一句解说>"
   **画面**: <画面描述; 建议时长 4s>
3. **对白**:
   - <角色A>: "<dialog>"
   - <角色B>: "<dialog>"
   **画面**: <画面描述; 建议时长 12s>
"""

# Back-compat alias — old code path used SCENE_TEMPLATE.
SCENE_TEMPLATE = SCENE_TEMPLATE_DRAMA


def scaffold_scene(
    project_id: str,
    episode_id: str,
    num: int,
    *,
    force: bool = False,
    mode: EpisodeMode = "drama",
) -> Path:
    """Create an empty scenes/scene-NN.md template. No-op if file exists unless --force."""
    out = scene_md_path(project_id, episode_id, num)
    if out.exists() and not force:
        return out
    template = SCENE_TEMPLATE_NARRATION if mode == "narration" else SCENE_TEMPLATE_DRAMA
    out.write_text(template.format(n=num), encoding="utf-8")
    return out


def mark_scene_ready(project_id: str, episode_id: str, num: int) -> Path:
    """Touch scenes/scene-NN.ready — sentinel that tells the director scene NN is done."""
    md = scene_md_path(project_id, episode_id, num)
    if not md.exists():
        raise FileNotFoundError(
            f"cannot mark scene-{num:02d}.ready before scene-{num:02d}.md exists"
        )
    sentinel = scene_ready_path(project_id, episode_id, num)
    sentinel.touch()
    return sentinel


@dataclass
class CompileResult:
    script_path: Path
    storyboard_path: Path
    scenes: int
    shots: int
    total_duration_s: int
    warnings: list[str]


def _list_scene_md(project_id: str, episode_id: str) -> list[tuple[int, Path]]:
    out: list[tuple[int, Path]] = []
    for p in sorted(scenes_dir(project_id, episode_id).iterdir()):
        if not p.is_file():
            continue
        m = SCENE_NUM_RE.match(p.name)
        if not m:
            continue
        out.append((int(m.group(1)), p))
    out.sort(key=lambda t: t[0])
    return out


def _list_scene_json(project_id: str, episode_id: str) -> list[tuple[int, Path]]:
    out: list[tuple[int, Path]] = []
    for p in sorted(scenes_dir(project_id, episode_id).iterdir()):
        if not p.is_file():
            continue
        m = SCENE_FRAGMENT_RE.match(p.name)
        if not m:
            continue
        out.append((int(m.group(1)), p))
    out.sort(key=lambda t: t[0])
    return out


def compile_episode(
    project_id: str,
    episode_id: str,
    *,
    title: str | None = None,
    synopsis: str | None = None,
    target_duration_s: int | None = None,
    resolution: str | None = None,
    ratio: str | None = None,
    provider: str | None = None,
    mode: EpisodeMode | None = None,
    narrator_voice: str | None = None,
) -> CompileResult:
    """Merge scenes/scene-*.md + scenes/scene-*.json into script.md + storyboard.json.

    Validates the merged storyboard via Storyboard.model_validate. Surfaces
    soft warnings via storyboard.lint().
    """
    edir = state.episode_dir(project_id, episode_id)

    md_files = _list_scene_md(project_id, episode_id)
    if not md_files:
        raise FileNotFoundError(
            f"no scenes/scene-*.md under {edir} — run "
            f"`SPARK_VIDEO_PROJECT={project_id} SPARK_VIDEO_EPISODE={episode_id} "
            f"uv run scripts/scaffold.py scene --num 1` first."
        )

    json_files = _list_scene_json(project_id, episode_id)
    md_nums = {n for n, _ in md_files}
    json_nums = {n for n, _ in json_files}
    missing_storyboards = sorted(md_nums - json_nums)
    extra_storyboards = sorted(json_nums - md_nums)

    if missing_storyboards:
        raise FileNotFoundError(
            f"director output missing for scene(s): "
            f"{', '.join(f'scene-{n:02d}.json' for n in missing_storyboards)}. "
            f"The director skill needs to process these scenes before compile."
        )

    # 1. Merge .md → script.md
    title = title or _guess_title(project_id, episode_id, md_files)
    synopsis = synopsis or ""
    parts: list[str] = [f"# {title}", ""]
    if synopsis:
        parts += [synopsis, ""]
    for _n, p in md_files:
        body = p.read_text(encoding="utf-8").rstrip()
        parts.append(body)
        parts.append("")
        parts.append("---")
        parts.append("")
    script_text = "\n".join(parts).rstrip() + "\n"
    script_path = edir / "script.md"
    script_path.write_text(script_text, encoding="utf-8")

    # 2. Merge .json → storyboard.json
    scenes: list[dict] = []
    shots: list[dict] = []
    for _n, p in json_files:
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"{p} is not valid JSON: {e}") from e
        if "scene" not in payload or "shots" not in payload:
            raise ValueError(
                f"{p} must have top-level 'scene' (object) + 'shots' (array). "
                f"See video-director SKILL.md schema."
            )
        scenes.append(payload["scene"])
        shots.extend(payload["shots"])

    # Provider resolution: explicit arg → env default → leave None and let
    # render-time fallback fill it in.
    resolved_provider = provider or SETTINGS.video_provider or None
    resolved_mode: EpisodeMode = mode or "drama"
    sb_dict: dict = {
        "project_id": project_id,
        "title": title,
        "synopsis": synopsis,
        "target_duration_s": target_duration_s or _infer_target_from_scenes(md_files) or 180,
        "resolution": resolution or SETTINGS.resolution,
        "ratio": ratio or SETTINGS.ratio,
        "provider": resolved_provider,
        "mode": resolved_mode,
        "scenes": scenes,
        "shots": shots,
    }
    if narrator_voice:
        sb_dict["narrator_voice"] = narrator_voice

    # Validate via pydantic — this is the schema gate.
    sb = Storyboard.model_validate(sb_dict)

    storyboard_path = edir / "storyboard.json"
    storyboard_path.write_text(
        json.dumps(sb.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    warnings = sb.lint()
    if extra_storyboards:
        warnings.append(
            f"director wrote storyboard fragments without matching script files: "
            f"{', '.join(f'scene-{n:02d}.json' for n in extra_storyboards)}"
        )

    return CompileResult(
        script_path=script_path,
        storyboard_path=storyboard_path,
        scenes=len(sb.scenes),
        shots=len(sb.shots),
        total_duration_s=sb.total_duration(),
        warnings=warnings,
    )


_TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_SCENE_HEADER_RE = re.compile(r"^##\s+场景\s*\d+\s*[—\-:：]?\s*(.+)$", re.MULTILINE)
_DURATION_RE = re.compile(r"\*\*预估时长\*\*[:：]\s*(\d+)")


def _guess_title(project_id: str, episode_id: str, md_files: list[tuple[int, Path]]) -> str:
    """Title from explicit lore.title if available, else project-episode label."""
    from . import lore as lore_mod

    lore = lore_mod.load(project_id, projects_dir=SETTINGS.projects_dir)
    if lore and lore.front.title:
        return lore.front.title
    ep_norm = state.normalize_episode_id(episode_id)
    return f"{project_id} · {ep_norm}"


def _infer_target_from_scenes(md_files: list[tuple[int, Path]]) -> int | None:
    """Sum every scene's `**预估时长**` value as the script's intended target."""
    total = 0
    found = False
    for _n, p in md_files:
        text = p.read_text(encoding="utf-8")
        for m in _DURATION_RE.finditer(text):
            total += int(m.group(1))
            found = True
    return total if found else None


def status(project_id: str, episode_id: str) -> dict:
    """Snapshot for human / agent: which scenes have md / ready / json yet."""
    md = {n for n, _ in _list_scene_md(project_id, episode_id)}
    js = {n for n, _ in _list_scene_json(project_id, episode_id)}
    ready_files = scenes_dir(project_id, episode_id).glob("scene-*.ready")
    ready: set[int] = set()
    for r in ready_files:
        m = re.match(r"^scene-(\d{2,3})\.ready$", r.name)
        if m:
            ready.add(int(m.group(1)))
    all_nums = sorted(md | js | ready)
    return {
        "episode_id": state.normalize_episode_id(episode_id),
        "scenes": [
            {
                "num": n,
                "md": n in md,
                "ready": n in ready,
                "json": n in js,
            }
            for n in all_nums
        ],
    }
