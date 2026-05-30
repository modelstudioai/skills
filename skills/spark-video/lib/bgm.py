"""BGM (background music) module — discovery + filename resolution.

Two-tier model (same shape as cast / movie-set):

    projects/<id>/bgm/                ← project-shared library (sitcom-wide)
    projects/<id>/<episode>/bgm/      ← episode-only tracks

A BGM file is just an audio file (.mp3 / .wav / .m4a / .flac / .ogg / .aac)
dropped into one of those folders. Filename (without extension) is the
**track id** referenced from ``storyboard.bgm.tracks[].file`` and from
``Scene.bgm_track``.

This module is intentionally narrow:

* No upload — BGM stays local, mixed onto the final video by ffmpeg at
  stitch time. We don't send it to DashScope.
* No transcoding — ffmpeg ``mix_bgm`` handles re-encoding when it mixes.

Public API:

* ``discover(project_id, episode_id)`` → list of available tracks with
  ``source: project | episode``. Episode wins when filenames collide.
* ``resolve_track(project_id, episode_id, name)`` → absolute ``Path`` to
  the audio file, or ``None`` if not found.
* ``project_bgm_dir`` / ``episode_bgm_dir`` — directory accessors.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from lib import state

BGM_FOLDER = "bgm"
BGM_AUDIO_EXTS: frozenset[str] = frozenset({
    ".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac",
})

Source = Literal["project", "episode"]


def project_bgm_dir(project_id: str) -> Path:
    """``projects/<id>/bgm/``. Created lazily by callers when they need it."""
    return state.project_dir(project_id) / BGM_FOLDER


def episode_bgm_dir(project_id: str, episode_id: str) -> Path:
    """``projects/<id>/<episode>/bgm/``."""
    return state.episode_dir(project_id, episode_id) / BGM_FOLDER


def _scan(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() in BGM_AUDIO_EXTS:
            out.append(p)
    return out


def discover(project_id: str, episode_id: str) -> list[dict]:
    """Return all BGM tracks visible to one episode.

    Each entry: ``{"name", "file", "path", "source", "size_bytes"}``.
    ``name`` is the filename stem (no extension) — that's what the
    storyboard / scene references. ``file`` is the basename with
    extension. Episode-tier wins on filename-stem collisions (mirrors
    cast / movie-set semantics).
    """
    seen: dict[str, dict] = {}
    for p in _scan(project_bgm_dir(project_id)):
        seen[p.stem] = {
            "name": p.stem,
            "file": p.name,
            "path": str(p),
            "source": "project",
            "size_bytes": p.stat().st_size,
        }
    for p in _scan(episode_bgm_dir(project_id, episode_id)):
        seen[p.stem] = {
            "name": p.stem,
            "file": p.name,
            "path": str(p),
            "source": "episode",
            "size_bytes": p.stat().st_size,
        }
    return list(seen.values())


def has_any(project_id: str, episode_id: str) -> bool:
    """Cheap existence check used by the producer at GATE 0.5."""
    return bool(discover(project_id, episode_id))


def resolve_track(
    project_id: str,
    episode_id: str,
    name: str,
) -> Path | None:
    """Look up a track by name (stem). Episode tier wins.

    ``name`` may be passed as either the stem (``main-theme``) or with
    extension (``main-theme.mp3``) — we strip the extension before
    matching so storyboards can be lenient.
    """
    if not name:
        return None
    stem = Path(name).stem
    for tier_dir in (
        episode_bgm_dir(project_id, episode_id),
        project_bgm_dir(project_id),
    ):
        if not tier_dir.is_dir():
            continue
        for p in tier_dir.iterdir():
            if not p.is_file():
                continue
            if p.suffix.lower() not in BGM_AUDIO_EXTS:
                continue
            if p.stem == stem:
                return p
    return None


def forbid_directive() -> str:
    """Tail snippet appended to shot prompts when the storyboard forbids
    model-generated BGM. Kept here so every provider injects the same
    string and the video reviewer can detect drift.
    """
    return "（不要生成任何背景音乐 / 配乐 / 旋律, 只保留人声台词与环境音）"


def forbid_negative_terms() -> str:
    """Negative-prompt terms appended on providers that support negative
    prompts (currently Wan). Same purpose as ``forbid_directive`` but in
    the negative-prompt vocabulary the model expects there.
    """
    return "背景音乐, 配乐, 旋律, BGM, 音乐, soundtrack, music"
