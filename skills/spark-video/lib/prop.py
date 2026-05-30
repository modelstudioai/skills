"""Key prop (关键道具) management — folder-per-prop.

Why this exists: AI video models have no cross-shot memory, so the
*same* 红包 / 戒指 / 钥匙 / 玩具熊 in two consecutive shots renders as
two visually different objects. The fix mirrors what we do for cast
and movie_set — pin a *reference image* of the prop and feed it into
every r2v shot in which the prop appears.

Filesystem convention (one folder per prop):

    projects/<id>/props/<name>/             ← project-level (recurring props)
        prop.md                             ← description card (front-matter + body)
        <anything>.{jpg,png,webp}           ← reference images (>=1 required)

    projects/<id>/<episode>/props/<name>/   ← episode-level (one-off props)
        prop.md
        <ref>.png

Two-tier discovery (per episode build) — same as cast / movie_set:

  1. **Episode tier**  ``projects/<id>/<episode>/props/`` — adds + overrides
  2. **Project tier**  ``projects/<id>/props/``           — shared baseline

If the same prop name appears in both tiers, the episode prop's images
are *prepended* (so they are picked first as reference_image), and the
episode prop.md overrides the project one.

State changes (完整的红包 → 起皱的红包 → 撕碎的红包) are SEPARATE
folders, not multiple images in one folder. Multiple images in one
folder are only for showing the *same state* from different angles
(grid composite, just like cast portraits). Naming convention for
state-bearing props: ``<name>-<state>``  e.g. ``红包-完整``,
``红包-起皱``, ``红包-撕碎``.

Renderer integration: see ``providers/wan.py`` and
``providers/happyhorse.py`` — when a shot's ``props`` list names one
or more props, the resolved image_url for each is appended to
``media[]`` after cast portraits and after the scene's set image.
HappyHorse r2v caps total media at 9; the provider truncates with a
warning when the cast + set + props slot count exceeds it.
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
PROP_FILENAME = "prop.md"

_SKIP_BASENAMES = {"readme.md", "readme", ".gitkeep", ".ds_store", "thumbs.db"}
_ID_OK = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class PropFront(BaseModel):
    """Validated YAML front-matter for a prop card."""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    id: str | None = Field(
        default=None,
        description="Optional ASCII slug used for OSS upload paths; "
                    "auto-derived from name if absent. Must match [a-z0-9_-]+.",
    )
    category: str | None = Field(
        default=None,
        description="container | weapon | document | jewelry | clothing | "
                    "food | electronic | toy | other (informational only)",
    )
    state: str | None = Field(
        default=None,
        description=(
            "If this prop folder represents one specific narrative STATE "
            "of the prop (完整 / 起皱 / 撕碎 / 损坏 / 染血 etc.), name it "
            "here. State change = different folder, not different prop."
        ),
    )
    size_class: str | None = Field(
        default=None,
        description="hand-held | pocketable | room-scale | wearable | other",
    )
    description: str | None = Field(
        default=None,
        description=(
            "One-line concrete description (材质 / 颜色 / 形状 / 关键细节). "
            "Used as a textual fallback in t2v shots that can't take a "
            "reference image."
        ),
    )
    forbidden: list[str] = Field(
        default_factory=list,
        description=(
            "Things this prop must NEVER be drawn as — especially OTHER "
            "states of the same prop (e.g. for 红包-完整: '揉皱', '破损')."
        ),
    )
    notes: str | None = None


@dataclass
class PropCard:
    path: str
    front: PropFront
    body: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "front": self.front.model_dump(exclude_none=True),
            "body": self.body,
        }


def parse_prop_card(path: str | Path) -> PropCard:
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
        front = PropFront.model_validate(data)
    else:
        front = PropFront()
    return PropCard(path=str(p.resolve()), front=front, body=body.strip())


@dataclass
class Prop:
    """Resolved prop ready for renderer/upload."""
    name: str
    id: str = ""
    images_local: list[str] = field(default_factory=list)
    card_local: str | None = None
    image_local: str | None = None  # final local file uploaded (always ASCII)
    image_url: str | None = None
    card: dict[str, Any] | None = None
    composite_image: bool = False
    source: str = "project"  # "project" | "episode"


# ---------------------------------------------------------------------------
# Helpers (mirror movie_set.py)
# ---------------------------------------------------------------------------


def _is_ascii_safe(s: str) -> bool:
    return bool(s) and all(c.isascii() and (c.isalnum() or c in "_-") for c in s)


def derive_id(name: str, *, card_id: str | None = None) -> str:
    if card_id:
        sid = card_id.strip().lower()
        if _ID_OK.match(sid):
            return sid
        console.print(f"[yellow]prop id {card_id!r} ignored: must match [a-z0-9_-]+[/]")
    if _is_ascii_safe(name):
        return name.lower()
    h = hashlib.sha256(name.encode("utf-8")).hexdigest()[:6]
    return f"prop_{h}"


def _scan_prop_folder(prop_dir: Path) -> tuple[list[Path], Path | None]:
    images: list[Path] = []
    card: Path | None = None
    for p in sorted(prop_dir.iterdir()):
        if p.is_dir():
            continue
        if p.name.lower() in _SKIP_BASENAMES:
            continue
        ext = p.suffix.lower()
        if ext in IMAGE_EXTS:
            images.append(p)
        elif p.name == PROP_FILENAME:
            card = p
    return images, card


def _scan_root(root: Path, source: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if not root.exists() or not root.is_dir():
        return out
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name.lower() in _SKIP_BASENAMES:
            continue
        images, card = _scan_prop_folder(child)
        if not images and not card:
            console.print(
                f"[yellow]skip {source}/{child.name}: no reference image and no {PROP_FILENAME}[/]"
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
    """Compose N (>=2) reference images of the SAME prop state into a grid PNG.

    Use this for multi-angle shots of one prop in one state. Different
    states (完整 / 起皱) belong in DIFFERENT folders; never grid them.
    """
    if len(images) < 2:
        raise ValueError("_build_grid expects 2+ images of the same prop.")
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


def _ensure_ascii_basename(src: Path, build_dir: Path, *, pid: str) -> Path:
    if _is_ascii_safe(src.stem) and _is_ascii_safe(src.suffix.lstrip(".")):
        return src
    dst = build_dir / f"{pid}{src.suffix.lower()}"
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return dst


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def project_props_dir(project_id: str) -> Path:
    return state.project_dir(project_id) / "props"


def episode_props_dir(project_id: str, episode_id: str) -> Path:
    return state.episode_dir(project_id, episode_id) / "props"


def discover(project_id: str, episode_id: str) -> list[Prop]:
    """Layered discovery — episode tier overrides project tier."""
    proj_buckets = _scan_root(project_props_dir(project_id), "project")
    ep_buckets = _scan_root(episode_props_dir(project_id, episode_id), "episode")
    merged = _merge(proj_buckets, ep_buckets)

    props: list[Prop] = []
    for name, b in sorted(merged.items()):
        images: list[Path] = b.get("images", []) or []
        if not images:
            console.print(f"[yellow]skip prop {name}: no reference image[/]")
            continue

        card_path: Path | None = b.get("card")
        card_dict: dict | None = None
        if card_path:
            try:
                card_dict = parse_prop_card(card_path).to_dict()
            except Exception as e:
                console.print(f"[red]prop card parse failed for {name}: {e}[/]")

        props.append(
            Prop(
                name=name,
                images_local=[str(p) for p in images],
                card_local=str(card_path) if card_path else None,
                card=card_dict,
                source=b.get("source", "project"),
            )
        )
    return props


def init_episode(
    project_id: str,
    episode_id: str,
    *,
    do_upload: bool = False,
) -> dict:
    """Build props.json for one episode.

    Same shape as cast / movie_set init. An episode with zero props is
    a no-op (not an error) — props are optional.
    """
    props = discover(project_id, episode_id)
    payload_props: list[dict] = []
    if props:
        build_dir = state.episode_dir(project_id, episode_id) / "props_built"
        build_dir.mkdir(parents=True, exist_ok=True)

        seen_ids: dict[str, str] = {}
        for p in props:
            card_id = (p.card or {}).get("front", {}).get("id") if p.card else None
            p.id = derive_id(p.name, card_id=card_id)
            if p.id in seen_ids and seen_ids[p.id] != p.name:
                extra = hashlib.sha256(p.name.encode("utf-8")).hexdigest()[6:10]
                p.id = f"{p.id}_{extra}"
            seen_ids[p.id] = p.name

            if len(p.images_local) == 1:
                src = Path(p.images_local[0])
                p.image_local = str(_ensure_ascii_basename(src, build_dir, pid=p.id))
            else:
                grid = build_dir / f"{p.id}.grid.png"
                _build_grid([Path(x) for x in p.images_local], grid)
                p.image_local = str(grid)
                p.composite_image = True
                console.print(
                    f"[cyan]· prop {p.name} ({p.id}): composed "
                    f"{len(p.images_local)}-pane grid[/]"
                )

            if do_upload and p.image_local:
                console.print(f"[cyan]uploading prop {p.name} ({p.id})…[/]")
                p.image_url = up.upload(p.image_local)

        payload_props = [asdict(p) for p in props]

    payload = {
        "project_id": project_id,
        "episode_id": state.normalize_episode_id(episode_id),
        "project_props_dir": str(project_props_dir(project_id).resolve()),
        "episode_props_dir": str(episode_props_dir(project_id, episode_id).resolve()),
        "props": payload_props,
    }
    state.write_json(project_id, "props.json", payload, episode_id=episode_id)
    state.merge_state(project_id, {
        "prop_count": len(payload_props),
        "prop_uploaded": do_upload and bool(payload_props),
        "prop_episode_only": sum(1 for p in props if p.source == "episode"),
    }, episode_id=episode_id)
    return payload


def load(project_id: str, episode_id: str) -> dict:
    """Load props.json. Returns an empty bucket if the file is missing
    (props are optional — never mandatory)."""
    data = state.read_json(project_id, "props.json", episode_id=episode_id)
    if not data:
        return {
            "project_id": project_id,
            "episode_id": state.normalize_episode_id(episode_id),
            "props": [],
        }
    return data


# ---------------------------------------------------------------------------
# Templates / scaffolding
# ---------------------------------------------------------------------------

PROP_TEMPLATE = """\
---
# Prop card for {name}.
#
# ⚠ HARD RULE: ONE FOLDER = ONE NARRATIVE STATE.
# 同一个道具的不同故事状态 (完整 → 起皱 → 撕碎 / 干净 → 染血 / 关闭 →
# 打开) 必须用 *不同* 的文件夹, 不要把多张状态图塞进同一个文件夹。
# 模型会平均化文件夹里的所有图片, 输出一个不伦不类的中间态。
#
# Naming convention: <prop_name>-<state>
#   props/红包-完整/
#   props/红包-起皱/
#   props/红包-撕碎/
#
# 同一个文件夹里的多张图只能是 *同一状态* 的不同视角 (正面/侧面/特写),
# 这种情况 CLI 会自动拼成 grid 合成图。
#
# The folder name IS the prop's display name — shots reference it via
# `Shot.props` in the storyboard.

name: {name}
# id: ascii_slug   ← optional. ASCII-only filename used for OSS uploads.
#                    Auto-derived from `name` if omitted.

# category: container | weapon | document | jewelry | clothing |
#           food | electronic | toy | other  (informational only)
category:

# Narrative state, if this folder represents one specific story state.
# Examples: 完整 | 起皱 | 撕碎 | 染血 | 关闭 | 打开 | 全新 | 旧了
# Leave blank if the prop has only one state across the whole episode.
state:

# Rough physical scale — helps the director choose 景别.
# size_class: hand-held | pocketable | room-scale | wearable | other
size_class:

# Single-line concrete description (材质 / 颜色 / 形状 / 关键细节).
# Used as the textual fallback for t2v shots that can't take a
# reference image. Example for 红包-完整:
#   "标准中式红包, 大红色烫金底纹, 印有'囍'字, 平整无折痕, 厚度适中"
description:

# Optional: things this prop must NEVER be drawn as. Especially other
# states of the same prop. Example for 红包-完整:
#   forbidden: ["揉皱", "破损", "边角磨损"]
forbidden: []

# Optional free-form notes (where it appears, who handles it, etc.).
notes:
---

# 详细描述

(自由文本: 道具的来历、谁拥有、在剧情中的关键时刻、与其他道具/角色
 的互动方式。director 会读这段。如果有 state 字段, 务必在本体里再说
 一次具体状态, 让 reviewer 也清楚。)

## 视觉锚点

- 材质 / 颜色 / 反光特性:
- 关键细节 (logo / 刻字 / 磨损位置 / 装饰):
- 拿在手里的尺寸感:
- 不要画成的样子 (尤其其他状态):
"""
