# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
scaffold.py — generate templates for episodes, scenes, lore, cast, sets, props.

Subcommands:
    episode --init          mkdir scaffold for projects/<p>/<ep>/
    lore --title "<title>"  scaffold projects/<p>/lore.md
    scene --num N           scaffold scenes/scene-NN.md (mode-specific)
    cast --name "陆辰"      scaffold cast folder + cast.md template
    cast --fork --name "陆辰" --drop-portraits   copy project cast to episode tier
    set --name "客栈-白天"   scaffold movie-set folder + set.md
    prop --name "红包-完整"  scaffold prop folder + prop.md
    cast-init               rebuild cast.json from project + episode tiers
    set-init                rebuild movie_set.json
    prop-init               rebuild props.json
    manifests               cast-init + set-init + prop-init
    mood-anchor             print lore.mood_anchor for piping into bl prompts

Respects SPARK_VIDEO_PROJECT / SPARK_VIDEO_EPISODE env vars.
Pass --episode to flag cast/set/prop as episode-tier.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))


def _projects_root() -> Path:
    return Path(os.environ.get("VIDEOGEN_PROJECTS_DIR", "./projects")).resolve()


def _project_dir() -> Path:
    proj = os.environ.get("SPARK_VIDEO_PROJECT")
    if not proj:
        print("ERROR: SPARK_VIDEO_PROJECT must be set", file=sys.stderr)
        sys.exit(2)
    return _projects_root() / proj


def _episode_dir(required: bool = True) -> Path:
    ep = os.environ.get("SPARK_VIDEO_EPISODE")
    if not ep and required:
        print("ERROR: SPARK_VIDEO_EPISODE must be set", file=sys.stderr)
        sys.exit(2)
    ep_id = ep if ep.startswith("episode-") else f"episode-{ep}"
    return _project_dir() / ep_id


# ----------------------------------------------------------- episode --init

def cmd_episode(args: argparse.Namespace) -> int:
    ep_dir = _episode_dir()
    for sub in ("scenes", "clips", "frames", "reviews", "logs", "final",
                "cast", "movie-set", "props"):
        (ep_dir / sub).mkdir(parents=True, exist_ok=True)
    proj_dir = _project_dir()
    for sub in ("cast", "movie-set", "props", "bgm"):
        (proj_dir / sub).mkdir(parents=True, exist_ok=True)
    print(f"scaffold ready at {ep_dir}/")
    return 0


# ---------------------------------------------------------------------- lore

LORE_TEMPLATE = """\
---
title: "{title}"
mood_anchor: "TBD — 一句话视觉风格锚, append到每个 shot prompt 末尾"
visual_style: "TBD — 整体美术风格 (写实 / 卡通 / 油画感 / 赛博朋克 / ...)"
genre: "TBD"
duration_target_s: 180
forbidden:
  - 血腥
  - 露骨
imagery_system:
  motifs: []
  highlight_elements: []
---

# {title}

## 世界观

(把项目的世界观、时代背景、核心设定写在这里)

## 主角弧线

(角色们的核心驱动力 / 长线弧线)

## 视觉锚

`mood_anchor` 是这个项目最重要的视觉一致性杠杆 —— 它会被附加到**每一个**
shot prompt 的末尾。写它的时候像在写一句产品 tagline:
- 太宽泛不行: "电影感"
- 太具体不行: "焦距 50mm, F1.8, 色温 5600K, 拜耳滤镜"
- 刚好: "暖黄路灯 + 浅景深 + 雨后湿地反光, 90 年代港片质感"
"""


def cmd_lore(args: argparse.Namespace) -> int:
    proj_dir = _project_dir()
    proj_dir.mkdir(parents=True, exist_ok=True)
    lore = proj_dir / "lore.md"
    if lore.exists() and not args.force:
        print(f"{lore} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1
    lore.write_text(LORE_TEMPLATE.format(title=args.title or proj_dir.name))
    print(f"wrote {lore} — edit mood_anchor before any drafting")
    return 0


def cmd_mood_anchor(args: argparse.Namespace) -> int:
    """Print lore.mood_anchor for piping into bl prompts."""
    lore = _project_dir() / "lore.md"
    if not lore.exists():
        print("", end="")
        return 0
    # Crude frontmatter parse — no PyYAML dep
    text = lore.read_text()
    if not text.startswith("---"):
        return 0
    try:
        end = text.index("---", 3)
        fm = text[3:end]
    except ValueError:
        return 0
    for line in fm.splitlines():
        line = line.strip()
        if line.startswith("mood_anchor:"):
            val = line.split(":", 1)[1].strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            print(val, end="")
            return 0
    return 0


# --------------------------------------------------------------------- scene

DRAMA_TEMPLATE = """\
## 场景 {n} — <location>（<time of day>）

**人物**: <characters from cast.json>
**节奏**: <外部节奏>（外部）+ <内部节奏>（内部）
**预估时长**: 30s
**前史**: <one sentence — what characters carry into this scene>

**剧情**:
<2-4 sentences. Camera-visible action only.>

**对白**:
- <角色A>: "<dialog>"
- <角色B>: "<dialog>"
"""

NARRATION_TEMPLATE = """\
## 场景 {n} — <location>（<time of day>）

**类型**: narration
**人物**: <characters appearing in any beat>
**预估时长**: 30s
**前史**: <one sentence>

**节拍**:
1. **旁白**: "<≤ 60 字第三人称叙事>"
   **画面**: <可拍画面 + 建议时长 4s>
2. **对白**:
   - <角色>: "<line>"
   **画面**: <可拍画面 + 建议时长 12s>
"""


def cmd_scene(args: argparse.Namespace) -> int:
    ep_dir = _episode_dir()
    (ep_dir / "scenes").mkdir(parents=True, exist_ok=True)
    n = int(args.num)
    f = ep_dir / "scenes" / f"scene-{n:02d}.md"
    if f.exists() and not args.force:
        print(f"{f} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1
    tpl = NARRATION_TEMPLATE if args.mode == "narration" else DRAMA_TEMPLATE
    f.write_text(tpl.format(n=n))
    print(f"wrote {f}")
    return 0


# ---------------------------------------------------------------------- cast

CAST_MD_TEMPLATE = """\
---
name: "{name}"
age: "TBD"
gender: "TBD"
visual_anchor: "TBD — 一句话外貌, 给 t2i 用"
voice_traits: "TBD"
dont:
  - "不能出现的形象/着装"
---

# {name}

## 性格

(三五句话写人物性格弧线、口头禅、动机)

## 视觉锚

`visual_anchor` 应可直接拼进 t2i prompt。
例: "28 岁青年, 短发, 深色 T 恤, 写实风格, 半身像"。
"""


def cmd_cast(args: argparse.Namespace) -> int:
    if args.fork:
        return _cast_fork(args)
    base = _episode_dir() if args.episode else _project_dir()
    cast_dir = base / "cast" / args.name
    cast_dir.mkdir(parents=True, exist_ok=True)
    md = cast_dir / "cast.md"
    if md.exists() and not args.force:
        print(f"{md} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1
    md.write_text(CAST_MD_TEMPLATE.format(name=args.name))
    print(f"scaffolded {cast_dir}/")
    print(f"  → edit {md}")
    print(f"  → drop one or more portrait images into {cast_dir}/")
    print(f"  → then run: uv run scripts/scaffold.py cast-init")
    return 0


def _cast_fork(args: argparse.Namespace) -> int:
    if not args.name:
        print("ERROR: --name required for --fork", file=sys.stderr)
        return 2
    src = _project_dir() / "cast" / args.name
    dst = _episode_dir() / "cast" / args.name
    if not src.exists():
        print(f"ERROR: project cast {src} does not exist", file=sys.stderr)
        return 2
    if dst.exists() and not args.force:
        print(f"{dst} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    if args.drop_portraits:
        for png in dst.glob("*.png"):
            png.unlink()
        for jpg in dst.glob("*.jpg"):
            jpg.unlink()
        print(f"  dropped portraits from {dst}/")
    print(f"forked {src} → {dst}")
    print(f"  next: ./scripts/bl image edit ... --out-dir {dst}/")
    print(f"        uv run scripts/scaffold.py cast-init")
    return 0


# ---------------------------------------------------------------------- set

SET_MD_TEMPLATE = """\
---
name: "{name}"
time_of_day: "TBD — 白天 | 黄昏 | 夜晚 | 凌晨"
season: "TBD"
color_grade: "TBD — 冷 / 暖 / 中性 / 高对比霓虹 / ..."
lighting: "TBD"
weather: "TBD"
---

# {name}

## 布景描述

(材质 / 布局 / 关键道具 / 视觉特征。一句话能复用进 t2i prompt 最好)
"""


def cmd_set(args: argparse.Namespace) -> int:
    base = _episode_dir() if args.episode else _project_dir()
    set_dir = base / "movie-set" / args.name
    set_dir.mkdir(parents=True, exist_ok=True)
    md = set_dir / "set.md"
    if md.exists() and not args.force:
        print(f"{md} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1
    md.write_text(SET_MD_TEMPLATE.format(name=args.name))
    print(f"scaffolded {set_dir}/")
    print(f"  → edit {md} (pin time_of_day / lighting / color_grade)")
    print(f"  → drop a reference image into {set_dir}/ (or use bl image generate)")
    print(f"  → then run: uv run scripts/scaffold.py set-init")
    return 0


# --------------------------------------------------------------------- prop

PROP_MD_TEMPLATE = """\
---
name: "{name}"
state: "TBD — 完整 / 起皱 / 撕碎 / 关闭 / 打开 / ..."
---

# {name}

## 道具描述

(材质 / 颜色 / 形状 / 关键细节)

⚠ 一个文件夹 = 一种叙事状态。如果同一物品有多个状态（完整→起皱→撕碎），
   每个状态都是一个**独立的文件夹**: 红包-完整 / 红包-起皱 / 红包-撕碎。
"""


def cmd_prop(args: argparse.Namespace) -> int:
    base = _episode_dir() if args.episode else _project_dir()
    prop_dir = base / "props" / args.name
    prop_dir.mkdir(parents=True, exist_ok=True)
    md = prop_dir / "prop.md"
    if md.exists() and not args.force:
        print(f"{md} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1
    md.write_text(PROP_MD_TEMPLATE.format(name=args.name))
    print(f"scaffolded {prop_dir}/")
    print(f"  → edit {md}")
    print(f"  → drop a reference image into {prop_dir}/ (or use bl image generate)")
    print(f"  → then run: uv run scripts/scaffold.py prop-init")
    return 0


# ------------------------------------------------- manifest rebuild commands

def _scan_tier_folders(tier_dir: Path, key_files: list[str]) -> dict[str, dict]:
    """Scan tier/<name>/ folders, return {name: {md_path, images, voice?}}."""
    out: dict[str, dict] = {}
    if not tier_dir.exists():
        return out
    for sub in sorted(tier_dir.iterdir()):
        if not sub.is_dir():
            continue
        md = None
        for kf in key_files:
            cand = sub / kf
            if cand.exists():
                md = cand
                break
        images = sorted([str(p) for p in sub.glob("*.png")] +
                        [str(p) for p in sub.glob("*.jpg")])
        voices = sorted([str(p) for p in sub.glob("*.mp3")] +
                        [str(p) for p in sub.glob("*.wav")] +
                        [str(p) for p in sub.glob("*.m4a")])
        out[sub.name] = {
            "name": sub.name,
            "md_path": str(md) if md else None,
            "images": images,
            "voices": voices,
            "tier": tier_dir.parent.name if tier_dir.parent.name.startswith("episode") else "project",
        }
    return out


def _merge_tiers(project_tier: dict, episode_tier: dict) -> dict:
    """Episode tier overrides project tier on name collision."""
    merged = dict(project_tier)
    merged.update(episode_tier)
    return merged


def cmd_cast_init(args: argparse.Namespace) -> int:
    proj = _scan_tier_folders(_project_dir() / "cast", ["cast.md", "soul.md"])
    ep_dir = _episode_dir(required=False) if os.environ.get("SPARK_VIDEO_EPISODE") else None
    epi = _scan_tier_folders(ep_dir / "cast", ["cast.md", "soul.md"]) if ep_dir else {}
    merged = _merge_tiers(proj, epi)
    out_path = (ep_dir or _project_dir()) / "cast.json"
    out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2))
    print(f"wrote {out_path} ({len(merged)} characters)")
    return 0


def cmd_set_init(args: argparse.Namespace) -> int:
    proj = _scan_tier_folders(_project_dir() / "movie-set", ["set.md"])
    ep_dir = _episode_dir(required=False) if os.environ.get("SPARK_VIDEO_EPISODE") else None
    epi = _scan_tier_folders(ep_dir / "movie-set", ["set.md"]) if ep_dir else {}
    merged = _merge_tiers(proj, epi)
    out_path = (ep_dir or _project_dir()) / "movie_set.json"
    out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2))
    print(f"wrote {out_path} ({len(merged)} sets)")
    return 0


def cmd_prop_init(args: argparse.Namespace) -> int:
    proj = _scan_tier_folders(_project_dir() / "props", ["prop.md"])
    ep_dir = _episode_dir(required=False) if os.environ.get("SPARK_VIDEO_EPISODE") else None
    epi = _scan_tier_folders(ep_dir / "props", ["prop.md"]) if ep_dir else {}
    merged = _merge_tiers(proj, epi)
    out_path = (ep_dir or _project_dir()) / "props.json"
    out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2))
    print(f"wrote {out_path} ({len(merged)} props)")
    return 0


def cmd_manifests(args: argparse.Namespace) -> int:
    rc = cmd_cast_init(args)
    rc |= cmd_set_init(args)
    rc |= cmd_prop_init(args)
    return rc


# ----------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ep = sub.add_parser("episode")
    p_ep.add_argument("--init", action="store_true")
    p_ep.set_defaults(fn=cmd_episode)

    p_lore = sub.add_parser("lore")
    p_lore.add_argument("--title", default=None)
    p_lore.add_argument("--force", action="store_true")
    p_lore.set_defaults(fn=cmd_lore)

    p_scene = sub.add_parser("scene")
    p_scene.add_argument("--num", required=True, type=int)
    p_scene.add_argument("--mode", choices=["drama", "narration"], default="drama")
    p_scene.add_argument("--force", action="store_true")
    p_scene.set_defaults(fn=cmd_scene)

    p_cast = sub.add_parser("cast")
    p_cast.add_argument("--name", required=True)
    p_cast.add_argument("--episode", action="store_true",
                        help="put under episode tier instead of project tier")
    p_cast.add_argument("--fork", action="store_true",
                        help="copy project cast to episode tier")
    p_cast.add_argument("--drop-portraits", action="store_true",
                        help="when --fork, delete copied portraits to force regen")
    p_cast.add_argument("--force", action="store_true")
    p_cast.set_defaults(fn=cmd_cast)

    p_set = sub.add_parser("set")
    p_set.add_argument("--name", required=True)
    p_set.add_argument("--episode", action="store_true")
    p_set.add_argument("--force", action="store_true")
    p_set.set_defaults(fn=cmd_set)

    p_prop = sub.add_parser("prop")
    p_prop.add_argument("--name", required=True)
    p_prop.add_argument("--episode", action="store_true")
    p_prop.add_argument("--force", action="store_true")
    p_prop.set_defaults(fn=cmd_prop)

    for name, fn in [("cast-init", cmd_cast_init), ("set-init", cmd_set_init),
                     ("prop-init", cmd_prop_init), ("manifests", cmd_manifests)]:
        p = sub.add_parser(name)
        p.set_defaults(fn=fn)

    p_ma = sub.add_parser("mood-anchor")
    p_ma.set_defaults(fn=cmd_mood_anchor)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
