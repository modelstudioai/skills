"""Movie-set (布景) management — folder-per-set.

Why this exists: AI video models have no cross-shot memory, so two
shots set in the "same" location (e.g. 同福客栈大堂) often render as
two completely different rooms. The fix mirrors what we already do for
characters — pin a *reference image* of the location and feed it into
every r2v shot in that scene.

Filesystem convention (one folder per set):

    projects/<id>/movie-set/<name>/             ← project-level (shared, e.g. sitcom rooms)
        set.md                                  ← description card (front-matter + body)
        <anything>.{jpg,png,webp}               ← reference images (>=1 required)

    projects/<id>/<episode>/movie-set/<name>/   ← episode-level (one-off locations)
        set.md
        <ref>.png

The folder name is the set's display name. Anything inside the folder
belongs to that set.

Two-tier discovery (per episode build) — exactly the cast model:

  1. **Episode tier**  ``projects/<id>/<episode>/movie-set/`` — adds + overrides
  2. **Project tier**  ``projects/<id>/movie-set/``           — shared baseline

If the same set appears in both tiers, the episode set's images are
*prepended* (so they are picked first as reference_image), and the
episode set.md overrides the project one. This is exactly how a sitcom
can keep one shared "客栈大堂" set forever, while a special episode
("失火的客栈") drops in a charred override under the episode folder.

Composites and ASCII-renamed singletons are written to
``projects/<id>/<episode>/movie_set_built/`` per episode (never mutating
user input). Multi-image sets get a 2/4/9-pane grid PNG, identical to
cast.

Renderer integration: see ``providers/wan.py`` and
``providers/happyhorse.py`` — when a shot's scene has ``set_id`` and
the active provider supports r2v ``reference_image``, the set's image
is appended to ``media[]`` after the cast portraits.
"""
from __future__ import annotations

import hashlib
import re
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml
from PIL import Image
from pydantic import BaseModel, ConfigDict, Field
from rich.console import Console

from lib import state
from lib.config import SETTINGS
from lib.soul import _split_frontmatter

class _UploadStub:
    @staticmethod
    def upload(*a, **kw):
        raise NotImplementedError(
            'lib.upload removed; bl auto-uploads. This path is unused by '
            'scripts/scaffold.py — call with do_upload=False.'
        )
up = _UploadStub()

console = Console()

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
SET_FILENAME = "set.md"

_SKIP_BASENAMES = {"readme.md", "readme", ".gitkeep", ".ds_store", "thumbs.db"}
_ID_OK = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class SetFront(BaseModel):
    """Validated YAML front-matter for a set card."""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    id: str | None = Field(
        default=None,
        description="Optional ASCII slug used for OSS upload paths; "
                    "auto-derived from name if absent. Must match [a-z0-9_-]+.",
    )
    type: str | None = Field(
        default=None,
        description="interior | exterior | vehicle | other (informational only)",
    )
    # The four "lighting state" axes — together they define this set's
    # identity. The director SKILL forbids reusing one set across
    # different values of any of these. See SET_TEMPLATE.
    time_of_day: str | None = Field(
        default=None,
        description="白天 | 黄昏 | 夜晚 | 凌晨 | 全天 (one folder = one value)",
    )
    season: str | None = Field(
        default=None,
        description="春 | 夏 | 秋 | 冬 | 不分季节 (one folder = one value)",
    )
    color_grade: str | None = Field(
        default=None,
        description="暖色 | 冷色 | 中性 | 高对比 | 低饱和 (one folder = one value)",
    )
    lighting: str | None = Field(
        default=None,
        description="自然光 | 钨丝灯暖黄 | LED 冷白 | 霓虹 | 烛光 | 月光",
    )
    weather: str | None = None
    description: str | None = Field(
        default=None,
        description=(
            "One-line set description. The director SKILL pastes this into "
            "scene.description (which gets woven into shot prompts), so the "
            "renderer also keeps a textual fallback for t2v shots that "
            "can't take a reference image."
        ),
    )
    palette: list[str] = Field(default_factory=list)
    forbidden: list[str] = Field(default_factory=list)
    notes: str | None = None


@dataclass
class SetCard:
    """Parsed set card."""
    path: str
    front: SetFront
    body: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "front": self.front.model_dump(exclude_none=True),
            "body": self.body,
        }


def parse_set_card(path: str | Path) -> SetCard:
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
        front = SetFront.model_validate(data)
    else:
        front = SetFront()
    return SetCard(path=str(p.resolve()), front=front, body=body.strip())


@dataclass
class MovieSet:
    """Resolved set ready for renderer/upload."""
    name: str
    id: str = ""
    images_local: list[str] = field(default_factory=list)
    card_local: str | None = None
    image_local: str | None = None  # final local file we upload (always ASCII)
    image_url: str | None = None
    card: dict[str, Any] | None = None
    composite_image: bool = False
    source: str = "project"  # "project" | "episode"


# ---------------------------------------------------------------------------
# Helpers (mirror cast.py)
# ---------------------------------------------------------------------------


def _is_ascii_safe(s: str) -> bool:
    return bool(s) and all(c.isascii() and (c.isalnum() or c in "_-") for c in s)


def derive_id(name: str, *, card_id: str | None = None) -> str:
    """Pick an ASCII slug for OSS paths.

    Priority: front-matter id (validated) → name if ASCII-safe → set_<6hash>.
    """
    if card_id:
        sid = card_id.strip().lower()
        if _ID_OK.match(sid):
            return sid
        console.print(f"[yellow]set id {card_id!r} ignored: must match [a-z0-9_-]+[/]")
    if _is_ascii_safe(name):
        return name.lower()
    h = hashlib.sha256(name.encode("utf-8")).hexdigest()[:6]
    return f"set_{h}"


def _scan_set_folder(set_dir: Path) -> tuple[list[Path], Path | None]:
    """Walk one set folder; return (images, card_path). Subdirs ignored."""
    images: list[Path] = []
    card: Path | None = None
    for p in sorted(set_dir.iterdir()):
        if p.is_dir():
            continue
        if p.name.lower() in _SKIP_BASENAMES:
            continue
        ext = p.suffix.lower()
        if ext in IMAGE_EXTS:
            images.append(p)
        elif p.name == SET_FILENAME:
            card = p
    return images, card


def _scan_root(root: Path, source: str) -> dict[str, dict[str, Any]]:
    """Return ``{set_name: {images, card, source}}`` for one tier."""
    out: dict[str, dict[str, Any]] = {}
    if not root.exists() or not root.is_dir():
        return out
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name.lower() in _SKIP_BASENAMES:
            continue
        images, card = _scan_set_folder(child)
        if not images and not card:
            console.print(
                f"[yellow]skip {source}/{child.name}: no reference image and no {SET_FILENAME}[/]"
            )
            continue
        out[child.name] = {"images": images, "card": card, "source": source}
    return out


def _merge(project_buckets: dict, episode_buckets: dict) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for name, b in project_buckets.items():
        merged[name] = {
            "images": list(b["images"]),
            "card": b["card"],
            "source": "project",
        }
    for name, eb in episode_buckets.items():
        if name in merged:
            pb = merged[name]
            pb["images"] = list(eb["images"]) + pb["images"]
            if eb["card"]:
                pb["card"] = eb["card"]
            pb["source"] = "episode"
        else:
            merged[name] = {
                "images": list(eb["images"]),
                "card": eb["card"],
                "source": "episode",
            }
    return merged


def _build_grid(images: list[Path], out: Path, *, max_side: int = 1280) -> Path:
    """Compose N (>=2) reference images of the same set into a grid PNG."""
    if len(images) < 2:
        raise ValueError("_build_grid expects 2+ images of the same set.")
    out.parent.mkdir(parents=True, exist_ok=True)
    n = len(images)
    if n == 2:
        cols, rows = 2, 1
    elif n <= 4:
        cols, rows = 2, 2
    else:
        cols, rows = 3, 3
    cell_w = max_side // cols
    cell_h = max_side // rows
    canvas = Image.new("RGB", (cell_w * cols, cell_h * rows), color=(20, 20, 20))
    for i, p in enumerate(images[: cols * rows]):
        try:
            im = Image.open(p).convert("RGB")
        except Exception as e:
            console.print(f"[yellow]grid: skip {p.name} ({e})[/]")
            continue
        im.thumbnail((cell_w, cell_h), Image.LANCZOS)
        x = (i % cols) * cell_w + (cell_w - im.width) // 2
        y = (i // cols) * cell_h + (cell_h - im.height) // 2
        canvas.paste(im, (x, y))
    canvas.save(out, format="PNG", optimize=True)
    return out


def _ensure_ascii_basename(src: Path, build_dir: Path, *, sid: str) -> Path:
    if _is_ascii_safe(src.stem) and _is_ascii_safe(src.suffix.lstrip(".")):
        return src
    dst = build_dir / f"{sid}{src.suffix.lower()}"
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return dst


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def project_set_dir(project_id: str) -> Path:
    return state.project_dir(project_id) / "movie-set"


def episode_set_dir(project_id: str, episode_id: str) -> Path:
    return state.episode_dir(project_id, episode_id) / "movie-set"


def discover(project_id: str, episode_id: str) -> list[MovieSet]:
    """Layered discovery — episode tier overrides project tier."""
    proj_buckets = _scan_root(project_set_dir(project_id), "project")
    ep_buckets = _scan_root(episode_set_dir(project_id, episode_id), "episode")
    merged = _merge(proj_buckets, ep_buckets)

    sets: list[MovieSet] = []
    for name, b in sorted(merged.items()):
        images: list[Path] = b.get("images", []) or []
        if not images:
            console.print(f"[yellow]skip set {name}: no reference image[/]")
            continue

        card_path: Path | None = b.get("card")
        card_dict: dict | None = None
        if card_path:
            try:
                card_dict = parse_set_card(card_path).to_dict()
            except Exception as e:
                console.print(f"[red]set card parse failed for {name}: {e}[/]")

        sets.append(
            MovieSet(
                name=name,
                images_local=[str(p) for p in images],
                card_local=str(card_path) if card_path else None,
                card=card_dict,
                source=b.get("source", "project"),
            )
        )
    return sets


def init_episode(
    project_id: str,
    episode_id: str,
    *,
    do_upload: bool = False,
) -> dict:
    """Build movie_set.json for one episode.

    Scans both tiers, merges by set name, builds grids per-set, uploads
    one image per set to OSS, writes
    ``projects/<id>/<episode>/movie_set.json``.

    Unlike cast.init_episode, an episode with zero sets is a no-op (not
    an error) — sets are optional. The renderer just won't inject any
    set reference images for shots in scenes without ``set_id``.
    """
    sets = discover(project_id, episode_id)
    payload_sets: list[dict] = []
    if sets:
        build_dir = state.episode_dir(project_id, episode_id) / "movie_set_built"
        build_dir.mkdir(parents=True, exist_ok=True)

        seen_ids: dict[str, str] = {}
        for s in sets:
            card_id = (s.card or {}).get("front", {}).get("id") if s.card else None
            s.id = derive_id(s.name, card_id=card_id)
            if s.id in seen_ids and seen_ids[s.id] != s.name:
                extra = hashlib.sha256(s.name.encode("utf-8")).hexdigest()[6:10]
                s.id = f"{s.id}_{extra}"
            seen_ids[s.id] = s.name

            if len(s.images_local) == 1:
                src = Path(s.images_local[0])
                s.image_local = str(_ensure_ascii_basename(src, build_dir, sid=s.id))
            else:
                grid = build_dir / f"{s.id}.grid.png"
                _build_grid([Path(p) for p in s.images_local], grid)
                s.image_local = str(grid)
                s.composite_image = True
                console.print(
                    f"[cyan]· set {s.name} ({s.id}): composed "
                    f"{len(s.images_local)}-pane grid[/]"
                )

            if do_upload and s.image_local:
                console.print(f"[cyan]uploading set {s.name} ({s.id})…[/]")
                s.image_url = up.upload(s.image_local)

        payload_sets = [asdict(s) for s in sets]

    payload = {
        "project_id": project_id,
        "episode_id": state.normalize_episode_id(episode_id),
        "project_set_dir": str(project_set_dir(project_id).resolve()),
        "episode_set_dir": str(episode_set_dir(project_id, episode_id).resolve()),
        "sets": payload_sets,
    }
    state.write_json(project_id, "movie_set.json", payload, episode_id=episode_id)
    state.merge_state(project_id, {
        "set_count": len(payload_sets),
        "set_uploaded": do_upload and bool(payload_sets),
        "set_episode_only": sum(1 for s in sets if s.source == "episode"),
    }, episode_id=episode_id)
    return payload


def load(project_id: str, episode_id: str) -> dict:
    """Load movie_set.json. Returns an empty bucket if the file is missing
    (sets are optional — never mandatory)."""
    data = state.read_json(project_id, "movie_set.json", episode_id=episode_id)
    if not data:
        return {
            "project_id": project_id,
            "episode_id": state.normalize_episode_id(episode_id),
            "sets": [],
        }
    return data


# ---------------------------------------------------------------------------
# Templates / scaffolding
# ---------------------------------------------------------------------------

SET_TEMPLATE = """\
---
# Set card for {name}.
#
# ⚠ HARD RULE: ONE FOLDER = ONE LIGHTING STATE.
# AI video models read the reference image *literally* — feed a noon-lit
# 客栈 photo into a 夜晚 shot and you'll get a noon-lit dream sequence
# with characters acting "tired". The fix is mandatory:
#
#   • Same physical place, different time-of-day  → TWO folders
#       projects/<id>/movie-set/同福客栈大堂-白天/
#       projects/<id>/movie-set/同福客栈大堂-夜晚/
#   • Same place, different season / weather       → separate folders
#       (柳树满枝-春, 飘雪-冬, 暴雨-夏)
#   • Same place, different color grade            → separate folders
#       (回忆冷灰, 现实暖黄)
#
# Use `time_of_day` + `season` + `color_grade` below as the suffix
# convention so folder names stay self-explanatory.
#
# The folder name IS the set's display name — scenes reference it via
# `Scene.set_id` (or per-shot `Shot.set_id`) in the storyboard.

name: {name}
# id: ascii_slug   ← optional. ASCII-only filename used for OSS uploads.
#                    Auto-derived from `name` if omitted (or hashed if
#                    `name` is non-ASCII).

# type: interior   ← optional: interior | exterior | vehicle | other.

# === LIGHTING STATE — together these define this set's identity ===
# A lock on each axis means "this set ONLY renders in this state".
# If the story needs a different state, scaffold a separate folder.

# 时段: 白天 | 黄昏 | 夜晚 | 凌晨 | 全天(慎用 — 仅当镜头都在均匀室内灯下)
time_of_day:

# 季节: 春 | 夏 | 秋 | 冬 | 不分季节
season:

# 色调: 暖色 | 冷色 | 中性 | 高对比 | 低饱和 | (or any concise tag)
color_grade:

# 灯光: 自然光 | 钨丝灯暖黄 | LED 冷白 | 霓虹 | 烛光 | 月光
lighting:

# 天气: 晴 | 阴 | 雨 | 雪 | 雾 (省略 = 不限制 / 室内不适用)
weather:

# Single-line description woven into scene prompts whenever the
# director writes a t2v shot in this location (t2v can't take a
# reference image, so the textual fallback matters there). Keep it
# concrete: 材质 / 灯光 / 关键道具 / 空间轮廓.
# Example: "明清木质客栈大堂, 二层木楼梯, 红灯笼, 八仙桌三张, 暖色调灯光, 白昼"
description:

# Optional: dominant colors (informational, surfaced to director).
palette: []

# Optional: things that must NEVER appear in this set, especially
# OTHER lighting states ("夜景" for a 白天 set, "室外阳光" for an
# interior at night, "雪" for a 夏 set).
forbidden: []

# Optional free-form notes (camera angles to prefer, props that move
# between scenes, etc.).
notes:
---

# 详细描述

(自由文本: 平面布局、可走机位、灯光预设、固定道具、可移动道具、镜头偏好。
 director 会读这段。务必确认与 frontmatter 的 time_of_day/season/color_grade
 在文字上一致 —— "黄昏" 写在 frontmatter 但本体里描述 "正午阳光" 会让
 reviewer 也跟着混乱。)

## 视觉锚点

- 材质 / 颜色:
- 关键道具:
- 灯光基调 (与 frontmatter 的 lighting 字段呼应):
- 不要拍到的东西 (尤其其他时段 / 季节 / 色调):
"""
