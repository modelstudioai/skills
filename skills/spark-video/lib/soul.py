"""Soul cards — character profiles that ride alongside ./cast/<name>.{jpg,mp3}.

A soul card is a markdown file with optional YAML front-matter:

    cast/钱夫人.md
    ---
    name: 钱夫人
    archetype: 跋扈反派 / 笑点担当
    voice_style: 嗓门大, 拖长音, 喜欢用反问
    catchphrases: ["嗯哼? 你再说一遍?"]
    mannerisms: [双手叉腰, 用扇子戳人胸口]
    relationships:
      - target: 佟掌柜
        type: 死对头
    do: [大场合一定要抢话]
    dont: [不会真的下死手]
    ---

    # 人物小传
    钱夫人原是江南绸缎商家千金...

The YAML half is structured (validated below). The markdown half is free-form
narrative — fed verbatim into the director Skill so the LLM gets full context.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

# Top frontmatter delimiter. Tolerates LF or CRLF.
_FM_OPEN = "---"
_FM_CLOSE = "---"


class Relationship(BaseModel):
    model_config = ConfigDict(extra="allow")
    target: str | None = None
    type: str | None = None
    backstory: str | None = None

    def is_filled(self) -> bool:
        return bool(self.target or self.type or self.backstory)


class SoulFront(BaseModel):
    """Validated YAML front-matter portion of a soul card."""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    id: str | None = Field(
        default=None,
        description="Optional ASCII slug used for OSS upload paths; "
                    "auto-derived from name if absent. Must match [a-z0-9_-]+.",
    )
    aliases: list[str] = Field(default_factory=list)
    age: int | str | None = None
    gender: str | None = None
    occupation: str | None = None
    archetype: str | None = None
    voice_style: str | None = None
    catchphrases: list[str] = Field(default_factory=list)
    mannerisms: list[str] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    do: list[str] = Field(default_factory=list)
    dont: list[str] = Field(default_factory=list)


@dataclass
class Soul:
    """Parsed soul card."""

    path: str
    front: SoulFront
    body: str  # the markdown after front-matter, fed to the LLM

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "front": self.front.model_dump(exclude_none=True),
            "body": self.body,
        }


def parse(path: str | Path) -> Soul:
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
        front = SoulFront.model_validate(data)
    else:
        front = SoulFront()
    return Soul(path=str(p.resolve()), front=front, body=body.strip())


def _split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter_yaml_or_None, body_markdown)."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != _FM_OPEN:
        return None, text
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == _FM_CLOSE:
            front = "".join(lines[1:i])
            body = "".join(lines[i + 1:])
            return front, body
    # Opening --- but no closing → treat whole file as body to be safe.
    return None, text


def discover(cast_dir: Path) -> dict[str, Soul]:
    """Map character stem → Soul for every .md found in cast_dir."""
    cast_dir = Path(cast_dir).resolve()
    out: dict[str, Soul] = {}
    if not cast_dir.exists():
        return out
    for p in cast_dir.iterdir():
        if p.suffix.lower() == ".md" and p.name.lower() != "readme.md":
            out[p.stem] = parse(p)
    return out


def render_for_prompt(soul: Soul, *, indent: str = "") -> str:
    """Render a soul into compact text the LLM can paste into prompts/context.

    Used by the director Skill — keeps token cost bounded.
    """
    f = soul.front
    parts: list[str] = []

    head_bits = []
    if f.archetype: head_bits.append(f.archetype)
    if f.occupation: head_bits.append(f.occupation)
    if f.age: head_bits.append(f"{f.age}岁")
    if f.gender: head_bits.append(f.gender)
    if head_bits:
        parts.append(f"{indent}- 设定: {' · '.join(map(str, head_bits))}")

    if f.voice_style:
        parts.append(f"{indent}- 说话风格: {f.voice_style}")
    if f.catchphrases:
        parts.append(f"{indent}- 口头禅: " + " / ".join(f'"{c}"' for c in f.catchphrases))
    if f.mannerisms:
        parts.append(f"{indent}- 习惯动作: " + ", ".join(f.mannerisms))
    rels = [r for r in f.relationships if r.is_filled()]
    if rels:
        for r in rels:
            target = r.target or "(unknown)"
            line = f"{target}({r.type or '关系'})"
            if r.backstory:
                line += f": {r.backstory}"
            parts.append(f"{indent}- 与 {line}")
    if f.do:
        parts.append(f"{indent}- DO: " + "; ".join(f.do))
    if f.dont:
        parts.append(f"{indent}- DON'T: " + "; ".join(f.dont))
    if soul.body:
        parts.append(f"{indent}- 小传:")
        for line in soul.body.splitlines():
            parts.append(f"{indent}    {line}")
    return "\n".join(parts)
