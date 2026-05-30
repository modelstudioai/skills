---
name: spark-video-cast
description: Scaffold and generate reference assets for characters (cast), locations (movie-set / 布景), and key props (关键道具) — the three pillars of visual consistency in spark-video. Wraps bl image generate / edit for portrait creation. Use when adding new characters/locations/props or when costume/state changes are needed.
---

# Cast / Set / Prop Skill — spark-video 美术 (三合一)

You are the **art department** of the pipeline. Your job is to scaffold
folder structures and generate reference images for the three things
that pin visual consistency:

| Pillar | Pins | Folder pattern |
|---|---|---|
| **Cast** (角色) | Faces, 发型, 服饰, 体态 | `cast/<name>/` |
| **Movie-set** (布景) | Locations, lighting, decor | `movie-set/<name>/` |
| **Prop** (关键道具) | Hero objects that recur or change state | `props/<name>/` |

All three follow the **same mental model**: one folder = one reference
image = one frozen visual state. State changes (day→night, intact→torn,
casual→formal) = **separate folders**.

Set env vars:
```bash
export SPARK_VIDEO_PROJECT=<project_id>
export SPARK_VIDEO_EPISODE=<NN>
export SPARK_VIDEO_PHASE=portrait
```

## Two-tier model — project vs episode

Both cast, set, and prop live under two tiers. Episode tier overrides
project tier on name collision:

```
projects/<p>/
├── cast/<name>/          ← project mains (shared across all episodes)
├── movie-set/<name>/     ← project recurring locations (sitcom rooms)
├── props/<name>/         ← project recurring hero objects
└── <episode>/
    ├── cast/<name>/      ← episode NPCs OR project-cast overrides (fork)
    ├── movie-set/<name>/ ← one-off locations for this episode
    └── props/<name>/     ← one-off or state-overrides for this episode
```

Use the **project tier** when an asset is shared across episodes
(sitcom recurring rooms, series mains). Use the **episode tier** for
one-off NPCs / locations / state-changes (整集换装 forks, episode-only
hero items, one-off rooms).

## ⚠ THE ONE-FOLDER-ONE-STATE RULE (hard rule, applies to all 3)

The video model reads reference images **literally**. Mixing two
visual states into one folder produces a muddy averaged intermediate.

| Pillar | "Same X, different…" → separate folder |
|---|---|
| Cast | 整集换装 (婚礼礼服 / 重伤包扎 / 古装变现代) → fork into episode tier |
| Set | 时段 (白天/夜晚), 季节 (春/秋), 色调 (冷/暖), 天气 (晴/雨) |
| Prop | 状态 (完整/起皱/撕碎), 损伤 (干净/染血), 开合 (关闭/打开) |

Naming convention: `<base_name>-<discriminator>`:
- `同福客栈大堂-白天` / `同福客栈大堂-夜晚`
- `红包-完整` / `红包-起皱` / `红包-撕碎`
- `陆辰-汉服` (forked from `陆辰` for one episode)

## Procedure 1 — scaffold a cast (角色)

### 1.1 主角 / 项目级角色

```bash
# Scaffold the folder + soul card template
uv run scripts/scaffold.py cast --name "陆辰"
# Edit projects/<p>/cast/陆辰/cast.md to fill: 年龄、性别、性格、口头禅、
# 视觉锚点 (1 句话外貌)、do / don't
```

Then generate the portrait via bl:

```bash
./scripts/bl image generate \
  --model wan2.6-t2i \
  --prompt "28岁青年, 短发, 深色T恤, 写实风格, 半身像, $(uv run scripts/scaffold.py mood-anchor)" \
  --size 16:9 \
  --out-dir projects/$SPARK_VIDEO_PROJECT/cast/陆辰/ \
  --out-prefix portrait
```

Notes:
- **Default model `wan2.6-t2i`**: produces stable cast portraits compatible
  with downstream r2v. `qwen-image-2.0` is newer but visual style differs;
  test before switching.
- **Append `lore.mood_anchor`** to every portrait prompt so the visual
  style matches the rest of the production. The `scaffold.py mood-anchor`
  helper prints lore's mood_anchor for piping.
- **Drop one ground-truth photo** into the folder if you have one (real
  actor reference, hand-drawn concept art) — it overrides the generated
  portrait at r2v time.

Optional: voice reference for reference-voice r2v (Wan / bl both support):
- Drop a 5–10s clean speech sample as `voice.mp3` in the cast folder.

### 1.2 NPC (episode-only)

```bash
uv run scripts/scaffold.py cast --name "钱夫人" --episode
# → projects/<p>/<ep>/cast/钱夫人/

./scripts/bl image generate \
  --model wan2.6-t2i \
  --prompt "中年妇女, 富态, 深色绸缎汉服, 头戴金步摇, 表情精明世故, $(uv run scripts/scaffold.py mood-anchor)" \
  --out-dir projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/cast/钱夫人/ \
  --out-prefix portrait
```

Then re-init the merged cast.json:
```bash
uv run scripts/scaffold.py cast-init   # merges project + episode tiers
```

### 1.3 Cast fork — 整集换装 (costume change for one episode)

When a character needs a different outfit for THIS episode only (婚礼,
古装, 战损版), DO NOT solve it in shot prompts. Fork the portrait:

```bash
# Deep-copy the project cast folder into the episode, drop old portrait
uv run scripts/scaffold.py cast --fork --name "陆辰" --drop-portraits

# Regenerate the portrait with the new appearance
./scripts/bl image edit \
  --image projects/$SPARK_VIDEO_PROJECT/cast/陆辰/portrait1.png \
  --prompt "把人物服装改为大红色中式喜服, 头戴红色喜帽, 其余面容/发型保持不变, $(uv run scripts/scaffold.py mood-anchor)" \
  --out-dir projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/cast/陆辰/ \
  --out-prefix portrait

uv run scripts/scaffold.py cast-init
```

`bl image edit` preserves face identity better than `bl image generate`
for forks — always prefer edit when you have a project-tier portrait to
base from.

For pixel-perfect face identity (edit can still drift slightly), drop
a hand-edited PNG into the episode cast folder instead of using bl.

## Procedure 2 — scaffold a movie-set (布景)

### 2.1 When to scaffold a set

Scaffold whenever:
- Two or more shots happen in the same location with the same lighting.
- The location matters enough that drift would be noticeable (recurring
  sitcom rooms, hero locations, key emotional spaces).
- A location returns under DIFFERENT lighting → scaffold one new folder
  per lighting state.

Skip for one-shot pass-throughs or pure outdoors with no fixed landmarks.

### 2.2 Naming — lighting state in the folder name

| Same physical place, different… | Action |
|---------------------------------|--------|
| Time-of-day (白天 / 黄昏 / 夜晚 / 凌晨) | **Separate folders** (`客栈大堂-白天`, `客栈大堂-夜晚`) |
| Season (春 / 夏 / 秋 / 冬) | Separate if visible (柳树 / 飘雪 / 红叶) |
| Color grade (回忆冷灰 / 现实暖黄 / 高对比霓虹) | Separate folders |
| Weather (晴 / 雨 / 雪 / 雾) | Separate when weather is in frame |
| Decor unchanged, action just moves around the room | **Same folder** |

### 2.3 Scaffold + generate

```bash
# Project-tier sitcom recurring room
uv run scripts/scaffold.py set --name "同福客栈大堂-白天"

# Episode-tier one-off
uv run scripts/scaffold.py set --name "出租屋客厅-暖灯" --episode

# Generate the reference image (description MUST include the lighting/
# season/tone you committed to in the folder name)
./scripts/bl image generate \
  --model wan2.6-t2i \
  --prompt "明清木质客栈大堂, 二层木楼梯, 红灯笼, 八仙桌三张, 白天自然光从窗户透入, 暖黄色调, $(uv run scripts/scaffold.py mood-anchor)" \
  --size 16:9 \
  --out-dir projects/$SPARK_VIDEO_PROJECT/movie-set/同福客栈大堂-白天/ \
  --out-prefix set

# Rebuild movie_set.json
uv run scripts/scaffold.py set-init
```

The `set.md` frontmatter has explicit `time_of_day` / `season` /
`color_grade` / `lighting` / `weather` axes — fill them in. They're
informational today, but they're the contract that prevents a future
director from reusing a 白天 set in a 夜 shot.

## Procedure 3 — scaffold a prop (关键道具)

### 3.1 When to promote an object to a key prop

Promote any object to a key prop when it satisfies **either**:
- It appears in 2+ shots and the audience would notice if it changed
  shape/material/color/wear (the 红包 in S01-003 → S01-007 → S04-002).
- It's a story-critical hero object even in a single shot (the 戒指
  proposal close-up; the 钥匙 reveal).

Skip for background dressing or non-recurring objects whose look doesn't
matter to the plot. **Budget: 3–6 named props per episode**, more is a smell.

### 3.2 Scaffold + generate

```bash
# Project-tier recurring prop (family heirloom)
uv run scripts/scaffold.py prop --name "戒指-完整"

# Episode-tier one-off or state-change
uv run scripts/scaffold.py prop --name "红包-起皱" --episode

# Generate a clean product-style reference image when no photo exists
./scripts/bl image generate \
  --model wan2.6-t2i \
  --prompt "标准中式红包, 大红色烫金底纹, 印有'囍'字, 平整无折痕, 纯白背景, 产品摄影风格, $(uv run scripts/scaffold.py mood-anchor)" \
  --size 1:1 \
  --out-dir projects/$SPARK_VIDEO_PROJECT/props/红包-完整/ \
  --out-prefix prop

# State change — produce 起皱 as a separate folder + image
./scripts/bl image edit \
  --image projects/$SPARK_VIDEO_PROJECT/props/红包-完整/prop1.png \
  --prompt "把红包做出明显的折痕、攥皱过的痕迹, 其余颜色/印花/形状保持完全不变" \
  --out-dir projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/props/红包-起皱/ \
  --out-prefix prop

# Rebuild props.json
uv run scripts/scaffold.py prop-init
```

For state changes, **always prefer `bl image edit`** with the base state
image as input — preserves shape/印花/material continuity. `bl image
generate` from scratch will draw a different-looking 红包 each time.

## Generation tips (apply to all three)

### Mood anchor — append it to every t2i prompt

```bash
# Helper that prints lore's mood_anchor for piping:
uv run scripts/scaffold.py mood-anchor
```

Without it, your asset visual style won't match the rendered shots.

### Aspect ratio defaults

| Asset type | `--size` |
|---|---|
| Cast portrait (half-body) | `16:9` or `3:4` |
| Cast portrait (full-body) | `9:16` |
| Set establishing | `16:9` |
| Prop (product-style) | `1:1` |

### Batch generation in parallel

`bl image generate` supports `--n N --concurrent K` — useful when
scaffolding many NPCs or sets at once. Each `--n` produces a candidate;
keep the best, delete the rest.

```bash
./scripts/bl image generate --n 3 --concurrent 3 \
  --model wan2.6-t2i \
  --prompt "..." \
  --out-dir projects/.../cast/陆辰/ \
  --out-prefix candidate
# → candidate1.png, candidate2.png, candidate3.png; rename winner to portrait1.png
```

### Multi-image merge (cast fork only)

`bl image edit` accepts multiple `--image` flags. Useful when forking a
cast with a costume reference photo:

```bash
./scripts/bl image edit \
  --image cast/陆辰/portrait1.png \
  --image refs/汉服参考.png \
  --prompt "把图1的人物穿上图2参考图的汉服, 其余面容/发型保持不变" \
  --out-dir projects/.../episode-X/cast/陆辰/
```

## After scaffolding — rebuild manifests

The merged manifests (`cast.json`, `movie_set.json`, `props.json`)
must be rebuilt after any folder change. They drive the director's
shot-id lookups and the renderer's media[] resolution:

```bash
uv run scripts/scaffold.py cast-init
uv run scripts/scaffold.py set-init
uv run scripts/scaffold.py prop-init
# or all three:
uv run scripts/scaffold.py manifests
```

Tell the director (or the producer at GATE 2) when you've added new
assets — they need to read the updated manifests before storyboarding
any scene that references them.

## DON'Ts

- ❌ Don't put two lighting states (day + night) in the same set folder.
  The model averages and produces "neutral gray noon-night" garbage.
- ❌ Don't put two prop states (完整 + 起皱) in the same prop folder.
  Same reason.
- ❌ Don't solve a costume change by writing "穿着 XXX" in shot prompts.
  Fork the cast portrait instead.
- ❌ Don't omit the mood_anchor in t2i prompts. Visual cohesion will
  break across shots vs portraits.
- ❌ Don't use generic names like `cast/护士` — name by role+story-id
  (`cast/护士小李`). When two episodes both have "护士", you can't tell
  whose portrait is whose.
- ❌ Don't generate reference images with `--watermark`. The watermark
  becomes a baked-in artifact that drifts into rendered shots.
- ❌ Don't skip `scaffold.py *-init` after adding folders. The manifests
  are the only thing the rest of the pipeline reads.
