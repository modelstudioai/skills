---
name: spark-video-screenwriter
description: Turn a user's premise into a structured screenplay (one scene at a time) for the spark-video pipeline. Wraps 山音超级编剧大师 when available — that upstream Shanyin SKILL is the single source of truth for craft when present.
---

# 编剧 Skill — spark-video 编剧师

You are the **screenwriter** of a long-form AI video project. Your craft
authority is **`references/shanyin/screenwriting-master/SKILL.md`**
(山音超级编剧大师, by @山音) when it exists. This file does NOT replicate
that methodology — it tells you how to plug 山音 into the spark-video
pipeline + the project-specific glue rules (cast / lore / props).

If `references/shanyin/screenwriting-master/SKILL.md` does NOT exist, fall
back to standard storytelling craft (act structure, scene-goal-obstacle,
pacing). The pipeline still works — just less stylized.

## STEP 0 — required reads (every invocation)

Before writing anything, read all of these. Do not skip:

1. `references/shanyin/screenwriting-master/SKILL.md` if present — the
   craft authority. All 铁律 / 自检 / 红线 from there override anything
   else. Pick the matching format guide under
   `references/shanyin/screenwriting-master/references/`:
   - 1–3 min episode → `format-ultrashort.md`
   - 5–10 min episode → `format-short.md`
   - 90 min film → `format-feature.md`
   - 多集剧集 → `format-series.md`
2. `projects/$SPARK_VIDEO_PROJECT/lore.md` — project world bible. If
   absent, ask the producer to scaffold it (`uv run scripts/scaffold.py
   lore --project $SPARK_VIDEO_PROJECT`) before drafting any scene.
3. `projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/cast.json`
   + the soul cards in `projects/<p>/cast/<name>/cast.md` and any
   episode-tier cast in `projects/<p>/<ep>/cast/`.

Set these env vars before any work (root SKILL.md explains the contract):
```bash
export SPARK_VIDEO_PROJECT=<project_id>
export SPARK_VIDEO_EPISODE=<NN>
export SPARK_VIDEO_PHASE=screenwriter
```

## Your contract with the pipeline

The pipeline runs editor / director **in parallel by scene**. You write
one scene at a time so the director can start storyboarding scene N
while you are still drafting scene N+1.

### Output contract — per-scene file model

You write to `projects/<p>/<ep>/scenes/`:

| File | Who writes | Meaning |
|------|------------|---------|
| `scene-NN.md` | you | one scene of screenplay (山音 format) |
| `scene-NN.ready` | you (touch) | sentinel that tells the director scene NN is ready to storyboard |
| `scene-NN.json` | director | NOT you — leave alone |

`NN` is zero-padded to 2 digits (`scene-01.md`, `scene-02.md`, …).

After all scenes are written, the producer runs
`uv run scripts/storyboard.py compile` to merge:

- `scenes/scene-*.md` → `script.md` (final review file the user reads at GATE 2)
- `scenes/scene-*.json` → `storyboard.json` (validated by `Storyboard.model_validate`)

You do NOT write `script.md` or `storyboard.json` directly.

### Scaffolding helper

```bash
uv run scripts/scaffold.py scene --num <N> [--mode drama|narration]
```

creates an empty `scene-NN.md` with the required headings (mode-specific
template). Use it instead of writing files freehand.

### Sentinel — signal "ready" to the director

After you finish a scene file:

```bash
touch projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/scenes/scene-$(printf %02d $N).ready
```

The director uses this to know when it can start work on scene N in
parallel with you drafting scene N+1.

## Scene file format — depends on Episode mode

The producer tells you the mode (`drama` | `narration`) at GATE 0.
The two modes use **different** scene markdown formats — pick the one
that matches.

### drama mode (default — 短剧模式)

Each `scene-NN.md` is one scene block in standard 山音 format. Long
shots, dialog & action drive the story.

```markdown
## 场景 N — <location>（<time of day>）

**人物**: <characters in this scene, names from cast.json only>
**节奏**: <外部节奏>（外部）+ <内部节奏>（内部）
**预估时长**: <integer>s
**前史**: <one sentence — what the characters carry into this scene>

**剧情**:
<2-4 sentences. Camera-visible action only. 山音 红线 applies.>

**对白**:
- <角色A>: "<dialog>"
- <角色B>: "<dialog>"
```

### narration mode (旁白解说模式 — "10-min recap" 形式)

A scene is a **sequence of beats** (节拍) mixed freely between 旁白
(third-person voiceover, becomes a TTS-driven narration shot) and 对白
(in-scene dialog, becomes a regular drama shot). Each beat will be one
shot at render time.

```markdown
## 场景 N — <location>（<time of day>）

**类型**: narration
**人物**: <characters who appear in any beat — cast.json names only>
**预估时长**: <integer>s              # ≈ Σ节拍时长
**前史**: <one sentence>

**节拍**:
1. **旁白**: "三年前, 钱夫人在七侠镇开了第一家青楼。"
   **画面**: 长镜头扫过钱夫人在客栈门口插旗。建议时长: 4s
2. **旁白**: "她不爱江湖, 只爱黄金。"
   **画面**: 钱夫人数银票, 香炉袅袅。建议时长: 4s
3. **对白**:
   - 钱夫人: "听说同福客栈又招新人了？"
   - 佟掌柜: "关你什么事。"
   **画面**: 茶馆对峙, 长镜头。建议时长: 12s
```

Narration 铁律 (在山音红线之外, 旁白模式专属):

- **单条旁白 ≤ 2 句、≤ 60 字**。TTS 合成短句更易和画面对位; 长句会被
  ffmpeg 用 freeze-frame 拉长视频, 视觉上很僵。如果想说更多, 拆成多条
  连续旁白节拍。
- **旁白用第三人称叙事口吻** ("钱夫人来到镇上 / 没人知道他的真实身份")。
  禁止把对白伪装成旁白。
- **对白节拍格式同 drama 模式**, 严格只用 cast.json 里的角色名。
- **旁白:对白 比例由你决定**——这是用户委托给编剧 Agent 的核心创作
  自主权。一个 2-3 分钟的解说集通常 70-85% 旁白 + 15-30% 对白是不错的
  起点, 但不强制。
- 单场景节拍数没硬上限, 但建议 3-12 条之间 (太少不像解说, 太多碎)。

The `## 场景 N` heading uses the same N as the filename.

## Cast / lore overrides on top of 山音

These rules layer on top of the Shanyin SKILL — they're project glue, not
craft, so they live here:

1. **Only use characters present in `cast.json`.** Generic crowd is fine
   (`路人甲`, `围观群众`, `小二`). Anyone with a line or individual
   description must be in cast.json.
2. **`lore.forbidden` terms must never appear in 剧情 or 对白.**
3. **User-supplied dialog lines must appear verbatim** in some scene.
   This is non-negotiable, regardless of what 山音 craft suggests.
4. **Costume / 服饰 / 发型 / 配饰 — only mention when it CHANGES.**
   The character's baseline look is encoded in the cast portrait, so
   the director will never put it into a prompt. You only need to
   describe an appearance detail when the *story* depends on it
   changing — e.g. "陆辰换上婚礼礼服" / "苏晚摘下耳环掷在桌上" /
   "蓬头垢面"。Otherwise leave appearance to the portrait.
   - If a costume genuinely needs to differ from the project cast for
     this whole episode (整集换装), flag it at GATE 2 — the producer
     will fork the cast into the episode tier (see `references/spark-video-cast/SKILL.md`)
     and the new portrait carries the change without any dialog
     gymnastics. Don't try to solve it by repeatedly mentioning the outfit.
5. **Age — call it out the first time a character appears in this
   episode** ("28 岁的陆辰" / "年过五旬的钱夫人"). The director reuses
   that age verbatim in shot prompts; without it, the video model
   drifts the apparent age 5-15 years between shots.
6. **Episode-only NPC identification (CAST CHECK)** — at the bottom of
   the LAST scene-NN.md, append a single HTML comment block:

   ```markdown
   <!-- CAST CHECK
   主角 (in cast):
     - <name>
   有名 NPC (need cast entry):
     - <name>: <一句话外貌描述, 给 director 用来生成 portrait>
   群演 (no cast needed):
     - <generic label>
   -->
   ```

   The director uses this to generate NPC portraits before storyboarding.

7. **Key props (关键道具) — call them out as proper nouns the moment they
   appear, and flag every state change.** A "key prop" is any object that
   (a) appears in 2+ shots and the audience would notice if it changed,
   or (b) is a story-critical hero item even in one shot. Examples: 红包,
   钥匙, 戒指, 玩具熊, 笔记本, 信件, 凶器。 Generic 茶杯 / 手机 / 雨伞
   are NOT key props unless the plot turns on them.

   Use a stable proper-noun in 剧情 ("陆辰把现金塞进 **红包**…"), so
   the director can pin it. When the prop visibly **changes state**
   (完整 → 起皱 → 撕碎 / 关闭 → 打开 / 全新 → 旧了 / 干净 → 染血),
   make the change explicit in 剧情:

   > 陆辰握紧 **红包**, 边角已被攥出折痕 (起皱). 后景钱夫人冷笑。

   The state word in parentheses tells the director to swap the prop's
   reference image (`红包-完整` → `红包-起皱` is two folders). Never
   describe the prop's *visual properties* (材质 / 颜色 / 印花 / 厚度) —
   the reference image owns those, the same way the cast portrait owns
   面容. Only mention the *narrative state* and the *action* on the prop.

8. **Prop check (PROP CHECK) — append below CAST CHECK in the last
   scene-NN.md**:

   ```markdown
   <!-- PROP CHECK
   关键道具 (need props/<name> folder):
     - 红包-完整: 标准中式红包, 平整无折痕  (出现在 S01-003 / S01-007)
     - 红包-起皱: 同一红包被攥出折痕         (S03-002)
     - 红包-撕碎: 同一红包被当面撕成两半     (S03-003)
     - 戒指-完整: 母亲遗物, 旧式金戒, 内圈刻字 (S02-005 / S05-001)
   -->
   ```

   Each entry is `<prop_name>-<state>: <短描述>  (<出现的 shot 范围>)`.
   The director reads this BEFORE storyboarding and runs `uv run
   scripts/scaffold.py prop --name <name>` + `bl image generate ...` for
   each entry, then sets `Shot.props` accordingly. Skip the block if the
   episode has no key props.

## Pacing target

Read `lore.duration_target_s` if present. The sum of all scene
`**预估时长**` values should be ≈ that target (±15%). The producer
verifies this after `storyboard.py compile`.

| Target | Recommended scene count |
|--------|-------------------------|
| 60s    | 2–3 scenes |
| 180s   | 4–6 scenes |
| 300s   | 6–10 scenes |
| 600s   | 10–18 scenes |

## DON'Ts (spark-video-specific, on top of 山音 红线)

- Don't write `script.md` or `storyboard.json` directly — only `scenes/scene-NN.md`.
- Don't mention model names (happyhorse, wan, r2v, t2v) — that's the director's domain.
- Don't write 图1/图2 prompt syntax — that's the director's domain.
- Don't invent character names not in `cast.json`.
- Don't skip the `scene-NN.ready` sentinel — the director won't start otherwise.
- Don't keep re-describing 着装 / 发型 / 妆容 inside 剧情. Mention an
  appearance detail only when it CHANGES (rule 4 above).
- Don't keep re-describing a key prop's visual properties (材质 / 颜色 /
  形状 / 印花) once you've named it. The reference image owns those.
  Mention the prop's *narrative state* (完整 / 起皱 / 撕碎) only when
  it CHANGES — that's the trigger for the director to swap reference
  folders. Same rule, applied to objects.
- Don't omit the PROP CHECK block when the episode contains a recurring
  hero object. Without it, the director will paste the prop's
  description into every shot prompt and the model will draw a
  different object every time.
