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
    """Visual motif system (山音"意象体系").

    The director should land each motif in the storyboard at least N times
    (short film: N>=2). Highlight elements are the *parts* of frame the
    camera should isolate (props, body parts, costume details).
    """

    model_config = ConfigDict(extra="allow")

    motifs: list[str] = Field(default_factory=list)
    highlight_elements: list[str] = Field(default_factory=list)


class DualPacing(BaseModel):
    """Dual-track pacing (山音"双轨节奏").

    *external* describes plot tightness (起承转合 + 快慢中).
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

    # ── 山音融合：导演定调系统 ──────────────────────────────
    # One-sentence dramatic action: the *engine* of the story.
    # Example: "钱夫人为找回面子, 反复挑衅郭芙蓉, 终被一拳放倒"
    dramatic_action: str | None = None

    # Visual motif system; richer than mood_anchor.
    imagery_system: ImagerySystem | None = None

    # Director-style reference fusion.
    # Example: "宁浩式群像喜剧节奏 + 张艺谋色彩饱和度"
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
        parts.append(f"# 世界观: {' · '.join(head_bits)}")

    if f.mood_anchor:
        parts.append(f"- 风格锚词 (每段 prompt 末尾必带): \"{f.mood_anchor}\"")
    if f.dramatic_action:
        parts.append(f"- 核心戏剧动作: {f.dramatic_action}")
    if f.director_reference:
        parts.append(f"- 导演定调: {f.director_reference}")
    if f.dual_pacing and (f.dual_pacing.external or f.dual_pacing.internal):
        ext = f.dual_pacing.external or "—"
        intn = f.dual_pacing.internal or "—"
        parts.append(f"- 双轨节奏: 外部「{ext}」/ 内部「{intn}」")
    if f.imagery_system:
        if f.imagery_system.motifs:
            parts.append(
                "- 视觉母题 (storyboard 中至少落地 2 次): "
                + "; ".join(f.imagery_system.motifs)
            )
        if f.imagery_system.highlight_elements:
            parts.append(
                "- 强化视觉元素: " + "; ".join(f.imagery_system.highlight_elements)
            )
    if f.visual_style:
        parts.append(f"- 视觉风格: {f.visual_style}")
    if f.camera_language:
        parts.append(f"- 镜头语言: {f.camera_language}")
    if f.palette:
        parts.append(f"- 色板: {', '.join(f.palette)}")
    if f.forbidden:
        parts.append(f"- 严禁出现: " + "; ".join(f.forbidden))
    if f.allowed:
        parts.append(f"- 明确允许: " + "; ".join(f.allowed))

    defaults: list[str] = []
    if f.duration_target_s: defaults.append(f"目标时长 {f.duration_target_s}s")
    if f.default_shot_duration: defaults.append(f"单段默认 {f.default_shot_duration}s")
    if f.default_resolution: defaults.append(f"分辨率 {f.default_resolution}")
    if f.default_ratio: defaults.append(f"宽高比 {f.default_ratio}")
    if defaults:
        parts.append(f"- 默认参数: {', '.join(defaults)}")

    if lore.body:
        parts.append("")
        parts.append("## 设定正文 (供 Skill 阅读)")
        parts.append(lore.body)

    return "\n".join(parts)


LORE_TEMPLATE = """\
---
# Story bible for {title}. Fill what you know; leave the rest blank.
# The director Skill reads this BEFORE writing the script, and carries
# mood_anchor through every shot prompt for visual cohesion.

title: {title}
genre: []          # e.g. [武侠喜剧, 情景喜剧]  /  [科幻, 悬疑]
era:               # 时空背景, e.g. 明朝架空 / 2049 近未来 / 维多利亚时代蒸汽朋克
location:          # 主要发生地, e.g. 七侠镇 · 同福客栈

# --- visual / camera direction ---
visual_style:      # 一句话描述, e.g. 暖色调, 喜剧光线, 略夸张的肢体语言
camera_language:   # e.g. 中近景为主, 偶尔大特写抓表情, 摇镜代替剪辑
palette: []        # color names or hex, e.g. [warm-amber, faded-red, ink-black]

# --- mood_anchor: single sentence appended to EVERY shot prompt ---
# Keep it short, concrete, and constant across the whole project.
# Example: "明朝架空, 喜剧光线, 暖色调, 略夸张的肢体语言"
mood_anchor:

# --- 山音融合：导演定调系统（可选，留空向后兼容）------------------
# 一句话核心戏剧动作 —— 故事的引擎。
# Example: "钱夫人为找回面子, 反复挑衅郭芙蓉, 终被一拳放倒"
dramatic_action:

# 视觉母题系统 —— 比 mood_anchor 更具故事性的"符号"。
# 导演会让母题在 storyboard 中至少落地 2 次（短片）。
# imagery_system:
#   motifs:                 # 贯穿全片的视觉意象
#     - "搓动的围裙"
#     - "翻飞的红盖头"
#   highlight_elements:     # 需要镜头特别强化的元素
#     - "发饰特写"
#     - "权杖象征"
imagery_system:
  motifs: []
  highlight_elements: []

# 导演风格融合 —— 用 1-2 位真实导演的方法论锚定调性。
# Example: "宁浩式群像喜剧节奏 + 张艺谋色彩饱和度"
director_reference:

# 双轨节奏 —— 外部情节松紧 + 内部情感曲线。
# 错位是高级叙事手法（外部慢但内部紧 / 外部紧但内部空）。
# dual_pacing:
#   external: "起-缓 / 承-紧 / 转-爆 / 合-顿"
#   internal: "面子-愠怒-爆发-错愕"
dual_pacing:
  external:
  internal:
# --- /山音融合 -------------------------------------------------

# --- world rules ---
forbidden: []      # e.g. [真实历史人物姓名, IP 直接同名, 血腥镜头]
allowed: []        # e.g. [夸张武打, 第四面墙吐槽]

# --- defaults the storyboard can pick up ---
duration_target_s: 180
default_shot_duration: 8
default_resolution: 720P
default_ratio: "16:9"
---

# 世界观

(几句话讲清这是个什么世界、什么调性、为什么有趣。LLM 写剧本前会先读这段。)

## 视觉风格参考

- 灯光:
- 服饰:
- 道具/场景质感:

## 镜头语言原则

- 喜剧/紧张/惊悚的节奏处理:
- 群戏 vs 双人戏的镜头偏好:
- 转场习惯:

## 写作禁区与口味

- 严禁:
- 我喜欢:

## 视觉母题说明 (可选)

(简单说明每个 motif 在故事里承载的含义。例如 "搓动的围裙" 承载
钱夫人的紧张与虚荣 —— 每次出现都强化她想维持体面但已经心虚的状态。)
"""
