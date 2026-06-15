"""Lore — per-project story background / world bible.

Sits at ``projects/<id>/lore.md``. Like soul cards but project-scoped:
*soul* answers "who is this character", *lore* answers "what world are they in".

The director Skill reads lore BEFORE writing the script, then carries
``mood_anchor`` (a single style sentence) through every shot prompt for
visual cohesion.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from lib.soul import _split_frontmatter  # reuse the same parser

LORE_FILENAME = "lore.md"


class ImagerySystem(BaseModel):
    """Visual motif system (Shanyin "imagery system").

    The director should land each motif in the storyboard at least N times
    (short film: N>=2). Highlight elements are the *parts* of frame the
    camera should isolate (props, body parts, costume details).
    """

    model_config = ConfigDict(extra="allow")

    motifs: list[str] = Field(default_factory=list)
    highlight_elements: list[str] = Field(default_factory=list)


class DualPacing(BaseModel):
    """Dual-track pacing (Shanyin "dual-track pacing").

    *external* describes plot tightness (setup-develop-turn-resolve + fast/medium/slow).
    *internal* describes the protagonist's emotional curve.
    Mismatch between the two is a hallmark of mature storytelling.
    """

    model_config = ConfigDict(extra="allow")

    external: str | None = None
    internal: str | None = None


class LoreFront(BaseModel):
    """Validated YAML front-matter for a lore card."""

    model_config = ConfigDict(extra="allow")

    # identity
    title: str | None = None
    genre: list[str] = Field(default_factory=list)
    era: str | None = None
    location: str | None = None

    # visual / camera direction
    visual_style: str | None = None
    camera_language: str | None = None
    palette: list[str] = Field(default_factory=list)

    # The single style sentence the director Skill should append to EVERY
    # shot prompt for cohesion. Keep it short (<60 chars).
    mood_anchor: str | None = None

    # ── Shanyin fusion: director tone system ──────────────────────────────
    # One-sentence dramatic action: the *engine* of the story.
    # Example: "钱夫人 keeps provoking 郭芙蓉 to save face, until one punch ends it"
    dramatic_action: str | None = None

    # Visual motif system; richer than mood_anchor.
    imagery_system: ImagerySystem | None = None

    # Director-style reference fusion.
    # Example: "Ning Hao-style ensemble comedy pacing + Zhang Yimou color saturation"
    director_reference: str | None = None

    # External plot pacing + internal emotional pacing (two tracks).
    dual_pacing: DualPacing | None = None
    # ──────────────────────────────────────────────────────

    # World rules — fed into negative_prompt-ish guidance and content checks.
    forbidden: list[str] = Field(default_factory=list)
    allowed: list[str] = Field(default_factory=list)

    # Optional defaults that storyboard authors can pick up.
    duration_target_s: int | None = None
    default_shot_duration: int | None = None
    default_resolution: str | None = None
    default_ratio: str | None = None


@dataclass
class Lore:
    path: str
    front: LoreFront
    body: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "front": self.front.model_dump(exclude_none=True),
            "body": self.body,
        }


def parse(path: str | Path) -> Lore:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    front_raw, body = _split_frontmatter(text)
    if front_raw:
        try:
            data = yaml.safe_load(front_raw) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"{p}: invalid YAML front-matter: {e}") from e
        if not isinstance(data, dict):
            raise ValueError(f"{p}: front-matter must be a mapping, got {type(data).__name__}")
        front = LoreFront.model_validate(data)
    else:
        front = LoreFront()
    return Lore(path=str(p.resolve()), front=front, body=body.strip())


def load(project_id: str, *, projects_dir: Path) -> Lore | None:
    p = projects_dir / project_id / LORE_FILENAME
    if not p.exists():
        return None
    return parse(p)


def render_for_prompt(lore: Lore) -> str:
    """Return a compact text the director Skill can paste into context."""
    f = lore.front
    parts: list[str] = []

    head_bits: list[str] = []
    if f.title: head_bits.append(f.title)
    if f.genre: head_bits.append("/".join(f.genre))
    if f.era: head_bits.append(f.era)
    if f.location: head_bits.append(f.location)
    if head_bits:
        parts.append(f"# World: {' · '.join(head_bits)}")

    if f.mood_anchor:
        parts.append(f"- Style anchor (append to every prompt): \"{f.mood_anchor}\"")
    if f.dramatic_action:
        parts.append(f"- Core dramatic action: {f.dramatic_action}")
    if f.director_reference:
        parts.append(f"- Director tone: {f.director_reference}")
    if f.dual_pacing and (f.dual_pacing.external or f.dual_pacing.internal):
        ext = f.dual_pacing.external or "—"
        intn = f.dual_pacing.internal or "—"
        parts.append(f"- Dual-track pacing: external「{ext}」/ internal「{intn}」")
    if f.imagery_system:
        if f.imagery_system.motifs:
            parts.append(
                "- Visual motifs (land at least 2× in storyboard): "
                + "; ".join(f.imagery_system.motifs)
            )
        if f.imagery_system.highlight_elements:
            parts.append(
                "- Highlight elements: " + "; ".join(f.imagery_system.highlight_elements)
            )
    if f.visual_style:
        parts.append(f"- Visual style: {f.visual_style}")
    if f.camera_language:
        parts.append(f"- Camera language: {f.camera_language}")
    if f.palette:
        parts.append(f"- Palette: {', '.join(f.palette)}")
    if f.forbidden:
        parts.append(f"- Forbidden: " + "; ".join(f.forbidden))
    if f.allowed:
        parts.append(f"- Explicitly allowed: " + "; ".join(f.allowed))

    defaults: list[str] = []
    if f.duration_target_s: defaults.append(f"target duration {f.duration_target_s}s")
    if f.default_shot_duration: defaults.append(f"default shot {f.default_shot_duration}s")
    if f.default_resolution: defaults.append(f"resolution {f.default_resolution}")
    if f.default_ratio: defaults.append(f"aspect ratio {f.default_ratio}")
    if defaults:
        parts.append(f"- Defaults: {', '.join(defaults)}")

    if lore.body:
        parts.append("")
        parts.append("## Lore body (for Skill reading)")
        parts.append(lore.body)

    return "\n".join(parts)


LORE_TEMPLATE = """\
---
# Story bible for {title}. Fill what you know; leave the rest blank.
# The director Skill reads this BEFORE writing the script, and carries
# mood_anchor through every shot prompt for visual cohesion.

title: {title}
genre: []          # e.g. [wuxia comedy, sitcom] / [sci-fi, thriller]
era:               # setting, e.g. Ming-era alt-history / 2049 near-future / Victorian steampunk
location:          # primary location, e.g. Qixia Town · Tongfu Inn

# --- visual / camera direction ---
visual_style:      # one-line, e.g. warm tones, comedic lighting, slightly exaggerated body language
camera_language:   # e.g. medium close-ups, occasional big close-ups for expressions, pans over cuts
palette: []        # color names or hex, e.g. [warm-amber, faded-red, ink-black]

# --- mood_anchor: single sentence appended to EVERY shot prompt ---
# Keep it short, concrete, and constant across the whole project.
# Example: "Ming-era alt-history, comedy lighting, warm tones, slightly exaggerated body language"
mood_anchor:

# --- Shanyin fusion: director tone system (optional, blank for back-compat) ---
# One-sentence core dramatic action — the engine of the story.
# Example: "钱夫人 keeps provoking 郭芙蓉 to save face, until one punch ends it"
dramatic_action:

# Visual motif system — story symbols richer than mood_anchor.
# The director lands each motif in the storyboard at least 2× (short film).
# imagery_system:
#   motifs:                 # recurring visual imagery
#     - "wrung apron"
#     - "fluttering red veil"
#   highlight_elements:     # elements the camera should emphasize
#     - "hair ornament close-up"
#     - "scepter as symbol"
imagery_system:
  motifs: []
  highlight_elements: []

# Director style fusion — anchor tone with 1-2 real directors' methods.
# Example: "Ning Hao-style ensemble comedy pacing + Zhang Yimou color saturation"
director_reference:

# Dual-track pacing — external plot tightness + internal emotional curve.
# Misalignment is advanced storytelling (slow outside / tight inside, etc.).
# dual_pacing:
#   external: "setup-slow / develop-tight / turn-burst / resolve-pause"
#   internal: "face-pride / simmer / explode / stunned"
dual_pacing:
  external:
  internal:
# --- / Shanyin fusion -------------------------------------------------

# --- world rules ---
forbidden: []      # e.g. [real historical figures by name, direct IP names, gore]
allowed: []        # e.g. [exaggerated martial arts, fourth-wall jokes]

# --- defaults the storyboard can pick up ---
duration_target_s: 180
default_shot_duration: 8
default_resolution: 720P
default_ratio: "16:9"
---

# World

(A few sentences on what world this is, its tone, and why it's interesting.
The LLM reads this before writing the script.)

## Visual style reference

- Lighting:
- Costumes:
- Prop / set texture:

## Camera language principles

- Comedy / tension / thriller pacing:
- Group vs two-shot preferences:
- Transition habits:

## Writing taboos and taste

- Forbidden:
- I like:

## Visual motif notes (optional)

(Briefly explain what each motif means in the story. E.g. "wrung apron" carries
钱夫人's tension and vanity — each appearance reinforces her need to keep
face while already feeling guilty.)
"""
