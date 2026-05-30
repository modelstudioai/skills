"""Storyboard schema — provider-agnostic.

Each shot will be turned into one DashScope video-synthesis request by
``videogen render``. The shot itself only declares a generic *kind*
(``t2v`` | ``i2v`` | ``r2v``). Mapping to a concrete model name is the
provider's job — see ``scripts/providers/``.

Per-kind duration ceilings (worst case across providers; the active
provider may impose a tighter cap of its own):

    t2v  → 2..15s
    i2v  → 2..15s
    r2v  → 2..15s

We default each shot to 15s — the max for our active models — to minimize
cuts and maximize cross-shot continuity. Override per shot if you genuinely
need a quick beat. Each provider also enforces its own duration *floor*
(Wan: 2s, HappyHorse: 3s).

Backward-compat: if ``Shot`` JSON still carries the old ``model`` field
with a ``wan2.7-*`` or ``happyhorse-1.0-*`` literal, we transparently
translate it to the new ``kind`` field on validate.
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


def _is_cjk_char(ch: str) -> bool:
    o = ord(ch)
    return (
        0x4E00 <= o <= 0x9FFF
        or 0x3400 <= o <= 0x4DBF
        or 0x20000 <= o <= 0x2A6DF
        or 0x3000 <= o <= 0x303F
    )


def estimate_narration_audio_seconds(
    text: str,
    *,
    speech_rate: float | None = None,
) -> float:
    """Heuristic wall-clock seconds for narration audio after speech_rate.

    Used by Storyboard's validation pass to warn when a narration shot's
    duration is way under the TTS length.
    """
    import os
    rate = speech_rate if speech_rate is not None else float(
        os.environ.get("SPARK_VIDEO_NARRATOR_SPEECH_RATE", "1.2")
    )
    rate = max(0.05, float(rate))
    s = (text or "").strip()
    if not s:
        return 0.0
    cjk = sum(1 for ch in s if _is_cjk_char(ch))
    non_cjk = max(0, len(s) - cjk)
    natural_sec = max(0.35, cjk / 3.0 + non_cjk / 12.0)
    return natural_sec / rate


ShotKind = Literal["t2v", "i2v", "r2v"]
ProviderName = Literal["bl", "wan27"]

# Episode-level mode. ``drama`` (default) is the legacy behaviour: every
# shot is a self-contained video that already carries its own dialog/audio
# (or is silent on HappyHorse). ``narration`` is the "10-min recap" mode —
# short visual beats whose original audio is stripped and replaced by a
# qwen3-tts-flash voiceover synthesised from ``Shot.narration_text``.
EpisodeMode = Literal["drama", "narration"]

# Per-shot role. In drama-mode storyboards every shot must be ``drama``.
# In narration-mode storyboards a shot can be either ``narration`` (TTS
# post-pass replaces audio) or ``drama`` (the regular long-form path).
ShotRole = Literal["drama", "narration"]

# Per-kind worst-case duration ceiling. Provider-specific ceilings live on
# the provider class itself; this is the schema-level fallback.
KIND_MAX_DURATION: dict[str, int] = {"t2v": 15, "i2v": 15, "r2v": 15}
DEFAULT_DURATION = 15
DURATION_FLOOR = 2

# Legacy provider-specific model strings that may still appear in old
# ``storyboard.json`` files. Mapped to (kind, provider) on read so the
# whole pipeline keeps working without manual migration.
LEGACY_MODEL_TO_KIND: dict[str, tuple[ShotKind, ProviderName]] = {
    "wan2.7-r2v":              ("r2v", "wan27"),
    "wan2.7-i2v-2026-04-25":   ("i2v", "wan27"),
    "wan2.7-t2v-2026-04-25":   ("t2v", "wan27"),
    "happyhorse-1.0-r2v":      ("r2v", "bl"),
    "happyhorse-1.0-i2v":      ("i2v", "bl"),
    "happyhorse-1.0-t2v":      ("t2v", "bl"),
}


class Shot(BaseModel):
    id: str = Field(description="shot id, e.g. 'S01-001' (scene-shot)")
    scene: str = Field(description="logical scene id, e.g. 'S01'")
    duration: int = Field(
        default=DEFAULT_DURATION,
        ge=DURATION_FLOOR,
        le=15,
        description="seconds. Default = 15. Auto-clamped to provider ceiling/floor at render time.",
    )
    prompt: str = Field(description="video prompt — describe action, camera, mood")
    negative_prompt: str | None = Field(
        default=None,
        description=(
            "Optional negative prompt. Honored by Wan only — HappyHorse "
            "ignores it (the render driver logs a warning)."
        ),
    )

    # ── 山音融合 ──────────────────────────────────────────
    # Why this shot exists in the story. Specific to visual means
    # (e.g. "用低角度仰拍 + 缓慢推近放大钱夫人的优越感"), not vague labels
    # (e.g. "展现冲突"). The CLI doesn't render this — it's metadata for
    # the director's own discipline + VFX reviewer's quality gate.
    narrative_purpose: str | None = Field(
        default=None,
        description=(
            "山音融合：每个 shot 必填。具体到视听手段, 不写'展现冲突'等空话。"
        ),
    )
    # Optional shot-group affiliation (山音"镜头组"概念)。同组镜头共同
    # 完成一个叙事单元 (蒙太奇组 / 递进组 / 因果组 / 对比组)。
    shot_group_id: str | None = Field(default=None, description="e.g. 'G01'")
    shot_group_role: Literal[
        "建立", "递进", "反应", "对比", "收尾"
    ] | None = None
    # ──────────────────────────────────────────────────────

    # Character references — names must match cast.json
    characters: list[str] = Field(default_factory=list, description="cast names featured")

    # Key-prop references — names must match props.json. Each prop's
    # reference_image is appended to media[] for r2v shots, after cast
    # portraits and after the scene's set image. Empty list = no prop
    # locking for this shot. The director SKILL forbids re-mentioning
    # the prop's appearance in the prompt — the reference image owns it.
    props: list[str] = Field(
        default_factory=list,
        description=(
            "Key-prop names featured in this shot. Names must match a "
            "folder under projects/<id>/props/<name>/ or "
            "projects/<id>/<episode>/props/<name>/. The renderer "
            "appends each prop's reference image to r2v shots; t2v / "
            "i2v shots ignore this field (no media slot)."
        ),
    )

    # Continuity
    use_prev_last_frame_as_first: bool = Field(
        default=True,
        description="If true, ffmpeg extracts last frame of previous successful shot and feeds as first_frame.",
    )

    kind: ShotKind = Field(
        default="r2v",
        description=(
            "Generic shot kind. The active provider (wan / happyhorse) maps "
            "this to a concrete model name at render time. Choose r2v for "
            "character-driven shots with cast references, t2v for "
            "establishing shots with no cast lock, i2v for first-frame "
            "continuation within a chain group."
        ),
    )

    seed: int | None = None
    candidates: int = Field(default=1, ge=1, le=4, description="N抽卡候选")

    set_id: str | None = Field(
        default=None,
        description=(
            "Per-shot movie-set override. Falls back to "
            "``Scene.set_id`` when omitted. Use this when one logical "
            "scene legitimately spans multiple location/lighting states "
            "(common in narration mode: 工地·夜 → 婚车·日 → 酒店·黄昏 are "
            "three beats inside one scene, each needs its own set image). "
            "**One set folder = one lighting state**: never reuse a "
            "白天客栈 set for a 夜晚客栈 shot — scaffold a second set "
            "instead. Setting set_id to empty string ('') explicitly "
            "disables the fallback for this shot."
        ),
    )

    # ── narration mode ────────────────────────────────────────────────────
    role: ShotRole = Field(
        default="drama",
        description=(
            "Shot role. ``drama`` (default) = today's long-form clip with "
            "its own audio. ``narration`` = short beat whose audio is "
            "stripped and replaced by a TTS voiceover; only allowed when "
            "the storyboard's mode is ``narration``."
        ),
    )
    narration_text: str | None = Field(
        default=None,
        description=(
            "Voiceover line for narration-role shots. Required iff "
            "``role == 'narration'``. Synthesised at render time via "
            "qwen3-tts-flash and muxed onto the rendered clip."
        ),
    )
    narrator_voice: str | None = Field(
        default=None,
        description=(
            "Per-shot voice override. Falls back to "
            "``Storyboard.narrator_voice`` then ``VIDEOGEN_NARRATOR_VOICE``."
        ),
    )
    # ──────────────────────────────────────────────────────────────────────

    @model_validator(mode="before")
    @classmethod
    def _migrate_legacy_model(cls, data: Any) -> Any:
        """Translate legacy ``model: "wan2.7-*" | "happyhorse-1.0-*"`` to ``kind``.

        Old storyboards predate the provider abstraction — they wrote out
        the concrete model name directly. We accept those silently so users
        don't have to hand-edit storyboard.json.
        """
        if not isinstance(data, dict):
            return data
        if "kind" in data and data["kind"]:
            # Already in new format. Drop a stale ``model`` key if present.
            data.pop("model", None)
            return data
        legacy = data.pop("model", None)
        if legacy is None:
            return data
        mapping = LEGACY_MODEL_TO_KIND.get(str(legacy))
        if mapping is None:
            raise ValueError(
                f"unknown legacy model {legacy!r}. Valid legacy values: "
                f"{sorted(LEGACY_MODEL_TO_KIND)}. Migrate this shot to use "
                f"the new ``kind`` field (t2v|i2v|r2v)."
            )
        kind, _provider = mapping
        data["kind"] = kind
        return data

    @field_validator("prompt")
    @classmethod
    def _no_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("prompt is empty")
        return v

    @model_validator(mode="after")
    def _clamp_duration_to_kind(self) -> "Shot":
        ceiling = KIND_MAX_DURATION.get(self.kind, 15)
        if self.duration > ceiling:
            object.__setattr__(self, "duration", ceiling)
        return self

    @model_validator(mode="after")
    def _check_narration_fields(self) -> "Shot":
        if self.role == "narration":
            if not self.narration_text or not self.narration_text.strip():
                raise ValueError(
                    f"shot {self.id}: role='narration' requires "
                    f"non-empty narration_text"
                )
        else:
            # drama role must not carry narration metadata.
            if self.narration_text:
                raise ValueError(
                    f"shot {self.id}: role='drama' must not set "
                    f"narration_text (only narration-role shots get the "
                    f"TTS post-pass)"
                )
        return self


class Scene(BaseModel):
    """A logical scene — one location + time + situation.

    The director defines all scenes BEFORE writing individual shots.
    Every shot in a scene inherits its environment description, ensuring
    visual consistency even though the video model has no memory.
    """
    id: str = Field(description="scene id, e.g. 'S01'. Must match shot.scene references.")
    name: str = Field(description="short human label, e.g. '七侠镇戏台子·白天'")
    description: str = Field(
        description=(
            "Detailed environment description (50-150 chars). Includes: "
            "location, time of day, lighting, props, atmosphere. "
            "This is prepended/woven into EVERY shot prompt in this scene."
        )
    )
    characters_present: list[str] = Field(
        default_factory=list,
        description="All characters who appear at some point in this scene (for recall).",
    )
    props_present: list[str] = Field(
        default_factory=list,
        description=(
            "All key props that appear at some point in this scene "
            "(for recall — mirrors characters_present). The validate "
            "step warns when shots reference props not listed here."
        ),
    )
    bgm_track: str | None = Field(
        default=None,
        description=(
            "Optional BGM track name (matches a file under "
            "``projects/<id>/bgm/`` or ``projects/<id>/<episode>/bgm/``, "
            "without extension). Only used when ``Storyboard.bgm.mode == "
            "'scene'`` — the stitcher mixes this track underneath every "
            "clip in this scene at ``Storyboard.bgm.volume``. Director "
            "picks the track based on the scene's emotional beat (煽情 "
            "→ slow piano, 惊悚 → low drone, 轻喜 → upbeat ukulele, …). "
            "Leave null to skip BGM on this scene."
        ),
    )
    set_id: str | None = Field(
        default=None,
        description=(
            "Optional movie-set name (matches a folder under "
            "``projects/<id>/movie-set/<name>/`` or "
            "``projects/<id>/<episode>/movie-set/<name>/``). When set, the "
            "renderer appends that set's reference image to every r2v shot "
            "in this scene, locking the location's appearance the same way "
            "cast portraits lock characters. t2v shots can't take a "
            "reference image — for those, the director should still weave "
            "the set's textual description into the prompt."
        ),
    )
    seed: int | None = Field(
        default=None,
        description="Shared seed for all shots in this scene (Rule 4 of continuity).",
    )

    @field_validator("description")
    @classmethod
    def _desc_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("scene description is empty")
        return v


BGMMode = Literal["off", "global", "scene"]


class BGMConfig(BaseModel):
    """Background music configuration for one episode.

    Populated by the producer at GATE 0.5 (``/episode``) after a BGM
    folder is detected under ``projects/<id>/bgm/`` or
    ``projects/<id>/<episode>/bgm/``. The renderer reads
    ``forbid_model_bgm`` to inject a no-music directive into every shot
    prompt; the stitcher reads ``mode`` + ``track`` (+ per-scene
    ``Scene.bgm_track``) to mix audio onto the final concatenated MP4.

    Modes:

    * ``off`` — BGM detected but the user opted not to use it. We still
      keep the entry around so the producer doesn't re-ask on rerun.
    * ``global`` — one track plays under the entire final video. The
      track filename (stem) lives in ``track``.
    * ``scene`` — per-scene assignment. The director writes
      ``Scene.bgm_track`` on each scene that should carry BGM; scenes
      with ``bgm_track=None`` stay silent (no BGM under those clips).
      ``track`` is ignored in this mode.
    """

    enabled: bool = Field(
        default=False,
        description=(
            "Master switch. False when the user explicitly skips BGM or "
            "no BGM folder was found. When False the stitcher does not "
            "mix any music; ``forbid_model_bgm`` is still honoured "
            "(useful when the user has no BGM file yet but still wants "
            "clean clips for later mixing in a DAW)."
        ),
    )
    mode: BGMMode = Field(
        default="off",
        description=(
            "How to apply BGM. ``off`` | ``global`` (one track for the "
            "whole video) | ``scene`` (per-scene via ``Scene.bgm_track``)."
        ),
    )
    forbid_model_bgm: bool = Field(
        default=False,
        description=(
            "When True the renderer appends a 'no BGM / no soundtrack' "
            "directive to every shot prompt (and to negative_prompt on "
            "providers that support it) so the video model doesn't "
            "generate competing music that would fight the stitched "
            "BGM. Recommended whenever ``enabled`` is True. Independent "
            "of ``enabled`` — you can forbid model music even when not "
            "stitching your own BGM (clean clips for later mixing)."
        ),
    )
    track: str | None = Field(
        default=None,
        description=(
            "Track name (filename stem, no extension) used in ``global`` "
            "mode. Must resolve under ``projects/<id>/bgm/`` or "
            "``projects/<id>/<episode>/bgm/``. Ignored in ``scene`` mode."
        ),
    )
    volume: float = Field(
        default=0.25,
        ge=0.0,
        le=1.0,
        description=(
            "Linear gain applied to the BGM stream before mixing with "
            "the (dialog) audio of each clip. 0.25 ≈ underscore. "
            "Use 0.0 to silence (debug)."
        ),
    )
    fade_in_s: float = Field(
        default=0.5,
        ge=0.0,
        le=10.0,
        description="Fade-in duration applied to the BGM track in seconds.",
    )
    fade_out_s: float = Field(
        default=1.0,
        ge=0.0,
        le=10.0,
        description="Fade-out duration applied to the BGM track in seconds.",
    )


class Storyboard(BaseModel):
    project_id: str | None = None
    title: str
    synopsis: str | None = None
    target_duration_s: int = Field(default=180, ge=2, description="user's intended target; informational only")
    resolution: str = "720P"
    ratio: str = "16:9"
    provider: ProviderName | None = Field(
        default=None,
        description=(
            "Video model family for this episode (bl | wan27). When absent, "
            "the renderer falls back to the SPARK_VIDEO_PROVIDER env var, then "
            "the built-in default (bl)."
        ),
    )
    mode: EpisodeMode = Field(
        default="drama",
        description=(
            "Episode mode. ``drama`` (default, back-compat): every shot is "
            "a long self-contained clip. ``narration``: storyboard mixes "
            "short narration shots (TTS voiceover) with optional drama "
            "shots — the '10-min recap' format."
        ),
    )
    narrator_voice: str | None = Field(
        default=None,
        description=(
            "Default TTS voice for narration-mode voiceovers. Falls back "
            "to VIDEOGEN_NARRATOR_VOICE env var. Per-shot override via "
            "``Shot.narrator_voice``."
        ),
    )
    scenes: list[Scene] = Field(
        default_factory=list,
        description=(
            "Explicit scene definitions. Each scene carries a detailed environment "
            "description that MUST be woven into every shot in that scene. "
            "If empty (legacy), shots still work but lose scene-level consistency."
        ),
    )
    bgm: BGMConfig | None = Field(
        default=None,
        description=(
            "Background music configuration. Set by the producer at "
            "``/episode`` GATE 0.5 when a ``bgm/`` folder is detected. "
            "When ``None``, the stitcher does not mix any BGM and the "
            "renderer doesn't inject the no-music directive — same as "
            "passing ``mode='off'`` with ``forbid_model_bgm=False``."
        ),
    )
    shots: list[Shot]

    @model_validator(mode="before")
    @classmethod
    def _infer_legacy_provider(cls, data: Any) -> Any:
        """If the storyboard predates the provider field, infer it from the
        first shot's legacy ``model`` so re-rendering an old episode
        deterministically picks the original family."""
        if not isinstance(data, dict):
            return data
        if data.get("provider"):
            return data
        for shot in data.get("shots") or []:
            if isinstance(shot, dict) and shot.get("model"):
                mapping = LEGACY_MODEL_TO_KIND.get(str(shot["model"]))
                if mapping:
                    data["provider"] = mapping[1]
                    break
        return data

    @model_validator(mode="after")
    def _check_bgm_consistency(self) -> "Storyboard":
        bgm = self.bgm
        if bgm is None:
            return self
        if bgm.mode == "global" and bgm.enabled and not bgm.track:
            raise ValueError(
                "storyboard.bgm.mode='global' but bgm.track is empty — "
                "set bgm.track to a filename (without extension) that "
                "exists under projects/<id>/bgm/ or "
                "projects/<id>/<episode>/bgm/, or switch the mode."
            )
        if bgm.mode == "scene" and bgm.enabled:
            tagged = [s.id for s in self.scenes if s.bgm_track]
            if not tagged:
                raise ValueError(
                    "storyboard.bgm.mode='scene' but no scene has "
                    "bgm_track set — either tag at least one Scene with "
                    "bgm_track=<track-name>, switch to mode='global', "
                    "or disable BGM (enabled=false)."
                )
        return self

    @model_validator(mode="after")
    def _check_mode_role_consistency(self) -> "Storyboard":
        if self.mode == "drama":
            bad = [s.id for s in self.shots if s.role == "narration"]
            if bad:
                raise ValueError(
                    f"storyboard.mode='drama' but {len(bad)} shot(s) have "
                    f"role='narration': {', '.join(bad[:5])}"
                    f"{'…' if len(bad) > 5 else ''}. "
                    f"Either change those shots to role='drama' (and clear "
                    f"narration_text) or set storyboard.mode='narration'."
                )
        return self

    def total_duration(self) -> int:
        return sum(s.duration for s in self.shots)

    def estimated_wall_clock_min(self, *, avg_per_shot_s: int = 180) -> float:
        """Sequential render assumption — each shot waits 1–5 min upstream."""
        return (len(self.shots) * avg_per_shot_s) / 60.0

    def scene_map(self) -> dict[str, Scene]:
        """Return {scene.id: Scene} for quick lookup."""
        return {s.id: s for s in self.scenes}

    def lint(self) -> list[str]:
        """Soft continuity / pacing checks. Never blocks render."""
        warnings: list[str] = []

        # 山音融合: every shot should have a non-trivial narrative_purpose.
        # Soft warning only — never blocks render. VFX reviewer enforces.
        _vague = {
            "", "展现冲突", "推进剧情", "推进故事", "建立场景",
            "渲染气氛", "表现情绪", "tbd", "TBD", "todo", "TODO",
        }
        missing_purpose: list[str] = []
        vague_purpose: list[str] = []
        for s in self.shots:
            if not s.narrative_purpose or not s.narrative_purpose.strip():
                missing_purpose.append(s.id)
            elif s.narrative_purpose.strip() in _vague or len(s.narrative_purpose.strip()) < 8:
                vague_purpose.append(s.id)
        if missing_purpose:
            warnings.append(
                f"narrative_purpose missing on {len(missing_purpose)} shot(s): "
                f"{', '.join(missing_purpose[:5])}"
                f"{'...' if len(missing_purpose) > 5 else ''}. "
                f"山音铁律：每个 shot 必填具体叙事目的。"
            )
        if vague_purpose:
            warnings.append(
                f"narrative_purpose too vague on {len(vague_purpose)} shot(s): "
                f"{', '.join(vague_purpose[:5])}"
                f"{'...' if len(vague_purpose) > 5 else ''}. "
                f"要具体到视听手段, 例如 '用低角度仰拍 + 缓慢推近放大钱夫人的优越感'。"
            )

        # Narration-shot recommendations (soft — never block render).
        if self.mode == "narration":
            for s in self.shots:
                if s.role != "narration":
                    continue
                if s.use_prev_last_frame_as_first:
                    warnings.append(
                        f"{s.id}: narration shot has "
                        f"use_prev_last_frame_as_first=true — narration "
                        f"shots should break the chain (false) so they "
                        f"render in parallel."
                    )
                if not (3 <= s.duration <= 6):
                    warnings.append(
                        f"{s.id}: narration shot duration {s.duration}s "
                        f"out of recommended 3-6s; keep narration beats "
                        f"short — TTS length drives the final clip length."
                    )
                if s.narration_text:
                    est = estimate_narration_audio_seconds(s.narration_text)
                    if est > float(s.duration) + 0.55:
                        warnings.append(
                            f"{s.id}: narration_text may run ~{est:.1f}s (heuristic) "
                            f"after default speech-rate post-process, but shot "
                            f"duration is {s.duration}s — rendered picture may "
                            f"freeze on the last frame while audio finishes. "
                            f"Shorten the line, raise duration, or split the beat."
                        )
        elif self.narrator_voice:
            warnings.append(
                "narrator_voice set but mode='drama' — value will be "
                "ignored. Switch to mode='narration' to enable TTS."
            )

        # First shot cannot chain.
        if self.shots and self.shots[0].use_prev_last_frame_as_first:
            warnings.append(
                f"first shot {self.shots[0].id}: use_prev_last_frame_as_first=true "
                f"but no previous shot exists — set it to false."
            )
        # i2v shots that need a previous frame but the previous shot doesn't chain.
        for s in self.shots:
            if s.kind == "i2v" and not s.use_prev_last_frame_as_first:
                warnings.append(
                    f"{s.id}: i2v with use_prev_last_frame_as_first=false will fail "
                    f"unless you supply media manually (not currently supported)."
                )
        # Duplicate shot ids.
        ids: dict[str, int] = {}
        for s in self.shots:
            ids[s.id] = ids.get(s.id, 0) + 1
        for sid, n in ids.items():
            if n > 1:
                warnings.append(f"duplicate shot id {sid!r} appears {n} times")

        # Orphaned action chains: 3+ consecutive shots with no characters
        # in the same scene usually means the protagonist dropped out.
        run_start = -1
        for i, s in enumerate(self.shots):
            if not s.characters and s.kind != "t2v":
                if run_start < 0:
                    run_start = i
            else:
                if run_start >= 0 and (i - run_start) >= 3:
                    ids_str = ", ".join(self.shots[j].id for j in range(run_start, i))
                    warnings.append(
                        f"protagonist dropout: {i - run_start} consecutive shots "
                        f"({ids_str}) have no characters — if this is an action "
                        f"sequence, the subject (e.g. the person being attacked) "
                        f"must stay in frame. Add them to characters[] and use r2v."
                    )
                run_start = -1
        # Check tail
        if run_start >= 0 and (len(self.shots) - run_start) >= 3:
            ids_str = ", ".join(self.shots[j].id for j in range(run_start, len(self.shots)))
            warnings.append(
                f"protagonist dropout: {len(self.shots) - run_start} consecutive shots "
                f"({ids_str}) have no characters at the end of the storyboard."
            )

        # set_id sanity — scenes that name a set but no shot in that scene
        # is r2v get a warning (set reference image only attaches to r2v).
        scene_lookup = self.scene_map()
        for sc in self.scenes:
            if not sc.set_id:
                continue
            r2v_in_scene = [
                s for s in self.shots
                if s.scene == sc.id and s.kind == "r2v"
                and _effective_set(s, sc) == sc.set_id
            ]
            if not r2v_in_scene:
                warnings.append(
                    f"scene {sc.id} declares set_id={sc.set_id!r} but no "
                    f"r2v shot inherits it (every r2v shot in this scene "
                    f"either overrides set_id or is t2v/i2v). The scene's "
                    f"set reference image will never attach — drop "
                    f"Scene.set_id, or remove the per-shot overrides."
                )

        # 灯光统一铁律 — within ONE chain group, every r2v shot must
        # resolve to the SAME effective set_id (or no set at all).
        # Mixing 客栈-白天 + 客栈-夜晚 inside one chain produces a
        # discontinuous lighting flicker (the chained first_frame is
        # already locked to the previous shot's lighting, but the new
        # set image fights it). Splits between chain groups are fine —
        # those are independent chain groups by definition.
        cur_chain_set: tuple[str, str | None] | None = None  # (first_shot_id, set_id)
        for s in self.shots:
            sc = scene_lookup.get(s.scene)
            eff = _effective_set(s, sc)
            starts_new_chain = (
                cur_chain_set is None or not s.use_prev_last_frame_as_first
            )
            if starts_new_chain:
                cur_chain_set = (s.id, eff if s.kind == "r2v" else None)
            else:
                if s.kind != "r2v":
                    continue
                anchor_shot, anchor_set = cur_chain_set
                if anchor_set is None:
                    # First r2v in this chain sets the anchor.
                    cur_chain_set = (anchor_shot, eff)
                elif eff != anchor_set:
                    warnings.append(
                        f"{s.id}: chain rooted at {anchor_shot} uses "
                        f"set_id={anchor_set!r} but this shot resolves to "
                        f"set_id={eff!r}. Within one chain group every "
                        f"r2v shot must share the same set (灯光/色调/时段 "
                        f"必须统一). Split the chain "
                        f"(use_prev_last_frame_as_first=false on this shot) "
                        f"or align the set_id."
                    )

        # Scene definition checks
        scene_map = self.scene_map()
        if self.scenes:
            shot_scene_ids = {s.scene for s in self.shots}
            defined_ids = {s.id for s in self.scenes}
            # Shots referencing undefined scenes
            undefined = shot_scene_ids - defined_ids
            if undefined:
                warnings.append(
                    f"shots reference undefined scenes: {', '.join(sorted(undefined))}. "
                    f"Add them to the 'scenes' array."
                )
            # Defined scenes with no shots
            unused = defined_ids - shot_scene_ids
            if unused:
                warnings.append(
                    f"scenes defined but never used by any shot: {', '.join(sorted(unused))}"
                )
            # Characters in shots but not in scene.characters_present
            for s in self.shots:
                sc = scene_map.get(s.scene)
                if sc and s.characters:
                    missing = set(s.characters) - set(sc.characters_present)
                    if missing:
                        warnings.append(
                            f"{s.id}: characters {missing} appear in shot but not in "
                            f"scene {sc.id}.characters_present — add them for recall."
                        )
                if sc and s.props:
                    missing_props = set(s.props) - set(sc.props_present)
                    if missing_props:
                        warnings.append(
                            f"{s.id}: props {missing_props} appear in shot but not in "
                            f"scene {sc.id}.props_present — add them for recall."
                        )

        # Props on non-r2v shots have no effect — the renderer can't
        # attach reference_image to t2v/i2v media[]. Soft warn.
        for s in self.shots:
            if s.props and s.kind != "r2v":
                warnings.append(
                    f"{s.id}: kind={s.kind} cannot accept prop reference "
                    f"images (only r2v has media[reference_image]). Either "
                    f"change kind to r2v or move the prop description into "
                    f"the prompt manually."
                )

        return warnings


# Public helper — also used by render-time providers via their own copies
# (kept duplicated there to avoid circular imports in the hot path).
def _effective_set(shot: Shot, scene: Scene | None) -> str | None:
    """Resolve set_id for one shot, honouring per-shot override:

      shot.set_id is None  → inherit scene.set_id
      shot.set_id == ""    → explicit opt-out (no set, even if scene has one)
      shot.set_id == "x"   → use 'x' regardless of scene.set_id
    """
    if shot.set_id is not None:
        return shot.set_id or None
    if scene is None:
        return None
    return scene.set_id or None
