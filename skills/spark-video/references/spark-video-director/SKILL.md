---
name: spark-video-director
description: Translate a screenplay (one scene at a time) into a provider-agnostic storyboard fragment for the spark-video pipeline. Wraps Shanyin Super Director Master when available — the upstream Shanyin SKILL is the single source of truth for craft when present.
---

# Director Skill — spark-video Storyboarder

You are the **director** of a long-form AI video shoot. Your craft
authority is **`references/shanyin/director-master/SKILL.md`** (Shanyin Super
Director Master, by @山音) when it exists. This file does NOT replicate that
methodology — it tells you how to plug Shanyin into the spark-video pipeline
+ the **provider-agnostic shot kind surface** (`t2v` / `i2v` / `r2v`).

If `references/shanyin/director-master/SKILL.md` does NOT exist, fall
back to standard film-direction craft (framing / pacing / camera movement / editing). The
pipeline still works — just less stylized.

## STEP 0 — required reads (every invocation)

1. `references/shanyin/director-master/SKILL.md` if present — craft
   authority (director tone → pacing → fine-tuning → storyboard). Plus the genre / form
   references under `references/shanyin/director-master/references/`.
2. `projects/$SPARK_VIDEO_PROJECT/lore.md` — project world bible.
3. `projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/cast.json`
   — per-episode cast.
4. The screenplay scene you are storyboarding (see Workflow below).
5. `projects/<p>/<ep>/movie_set.json` — per-episode movie-set (set dressing)
   bundle. Read BEFORE you decide which scenes get a `set_id`.
6. `projects/<p>/<ep>/props.json` — per-episode key-prop
   bundle. Read BEFORE writing shot prompts so you know which named
   props are pinned and what their valid `Shot.props` names are.
7. The **active provider** — read `$SPARK_VIDEO_PROVIDER` (default `bl`).
   See § "Provider capability table" for behavioral differences.

Set env vars before any work:
```bash
export SPARK_VIDEO_PROJECT=<project_id>
export SPARK_VIDEO_EPISODE=<NN>
export SPARK_VIDEO_PHASE=director
```

## Your contract with the pipeline

The pipeline runs editor / director **in parallel by scene**. You do
NOT receive the whole script at once — you process one scene as soon as
the screenwriter signals it ready, while they keep drafting the next.

### Inputs you read per invocation

For each scene the producer hands you a scene number `N`. You must:

1. Verify `projects/<p>/<ep>/scenes/scene-NN.ready` exists. If not,
   wait — the screenwriter has not signaled "ready" yet.
2. Read `projects/<p>/<ep>/scenes/scene-NN.md` (the screenplay).
3. Read `projects/<p>/<ep>/direction.json` if it exists (the per-episode
   "director tone" — see below). If absent and this is scene 01, produce it
   first.

### Output you write per scene

Write **one file**: `projects/<p>/<ep>/scenes/scene-NN.json`.

Schema:

```json
{
  "scene": {
    "id": "S<NN>",
    "name": "...",
    "description": "...",
    "characters_present": ["..."],
    "props_present": ["..."],
    "set_id": "<set name from movie_set.json, or null>",
    "bgm_track": "<track stem when storyboard.bgm.mode='scene', else null>",
    "seed": <int|null>
  },
  "shots": [
    {
      "id": "S<NN>-001",
      "scene": "S<NN>",
      "narrative_purpose": "...",
      "prompt": "...",
      "duration": 15,
      "kind": "r2v",
      "role": "drama",
      "characters": ["..."],
      "props": ["..."],
      "set_id": "<override scene.set_id, or null to inherit>",
      "use_prev_last_frame_as_first": true,
      "shot_group_id": "G01",
      "shot_group_role": "establish",
      "negative_prompt": "...",
      "seed": <int|null>,
      "candidates": 1
    }
  ]
}
```

The shape MUST match `Scene` and `Shot` in `lib/storyboard.py`. Validate
after every write:

```bash
uv run scripts/storyboard.py validate --scene $N
```

**Use `kind`, NOT a vendor-specific model name.** The renderer maps
`kind` → the active provider's concrete model at submit time.

**Shot id convention**: `S<NN>-<ZZZ>` where `NN` is scene number and
`ZZZ` is 1-based shot index inside that scene (`S01-001`, `S01-002`,
`S02-001`, …). This makes the chain-DAG renderer's grouping reliable.

### Continuity flag — `use_prev_last_frame_as_first`

This drives parallelism in the renderer. **Do not set it `true` for the
first shot of a scene** unless you genuinely want this scene's first
frame to chain off the previous scene's last frame (rare).

| Situation | `use_prev_last_frame_as_first` | Why |
|-----------|--------------------------------|-----|
| First shot of project | `false` | nothing to chain |
| First shot of a new scene | `false` (default) | scene cuts open new chain group → can render in parallel with other scenes |
| Continuing the same beat inside one scene | `true` | last-frame chain → forced sequential within the chain group |

The renderer slices the storyboard into **chain groups** by this flag
and renders different groups concurrently. **Maximize the number of
groups.** Every `false` you set unlocks a parallel render slot.

### Director tone — `direction.json`

The "director tone" stage from Shanyin maps to a single per-episode file:
`projects/<p>/<ep>/direction.json`. Produce it once before scene 01.
It captures the seven viewing decisions, imagery system, and dual-pacing
curve. Subsequent scenes read it and stay consistent.

## Mode-aware shot generation

The producer tells you the **episode mode** when invoking this skill.
The mode is also persisted in `Storyboard.mode` after compile.

| mode | What you write |
|------|---------------|
| `drama` (default — short drama) | Every shot has `role: "drama"` (the schema default). Long r2v shots, dialog-driven. |
| `narration` (voiceover recap) | Each scene-NN.md is a list of `**Beats**`. Map each beat to one shot, with mode-specific roles: |

### Beat → shot mapping (narration mode)

| Beat type in scene-NN.md | Resulting shot fields |
|--------------------------|------------------------|
| `**Narration**: "<line>"` | `role: "narration"`, `narration_text: "<line>"`, `kind: "t2v"` (or `r2v` if the **Visual** line explicitly references a cast member's face), `duration: 4` (range 3-6), `use_prev_last_frame_as_first: false`, `characters: []` (or just the locked face if r2v) |
| `**Dialog**: ...` | `role: "drama"` (default), follow drama rules — long r2v shot, full cast list, longer duration (12-15s) |

Rules that matter for narration shots:

- **Always break the chain** (`use_prev_last_frame_as_first: false`).
  Narration shots are visually independent — every one of them is its
  own chain group, which is exactly what we want for parallel render.
- **Default `kind: "t2v"`**. Lock a face only when the **Visual** description
  explicitly names a cast member visible in this beat — in that case
  use `r2v` and put just that one character in `characters`.
- **Default `duration: 4`s.** TTS length drives the final clip duration.
  Only go higher (5-6s) when the **Visual** needs noticeable motion.
- **Narration–video alignment rules**:
  - The render pipeline targets final duration in `[TTS length, TTS length + 1s]`: when video is longer than narration,
    keep at most **1s** of silent tail; when narration is longer than video, pad with at most **1s** freeze frame,
    trimming excess narration beyond that.
  - **Video < narration** (gap ≤ 20%): prefer nudging TTS speech rate to speed up narration
    to match video. E.g. 4s video + 4.6s narration → rate × 1.15.
  - **Video ≪ narration** (gap > 20% or >1s): `duration` was underestimated —
    raise that beat's `duration` to ≈ TTS length, or narration tail gets cut off.
  - **Narration exceeds provider per-shot cap** (e.g. happyhorse-1.0-r2v hard cap
    10s, narration is 17s): bumping `duration` won't break the provider cap.
    Solution: **render a continuation segment** — second segment lands at
    `clips/<shot_id>b.mp4` (e.g. `clips/S01-002b.mp4`). `stitch.py` automatically
    xfade-joins a + b into one segment, then aligns narration — no A/V drift in the middle.
    Continuation uses the same character / set references as the main shot; prompt describes this shot's
    "second half" action (e.g. main shot "walks into office", continuation "already at floor-to-ceiling window");
    a + b total duration should be slightly longer than narration, with 0.3-1s buffer.
  - Core rule: **single-shot freeze hold ≤ 1s**; for longer pauses use silent tail before the next narration beat,
    not infinite freeze.
- **Do NOT set `narration_text` on `role: "drama"` shots.** The schema rejects it.
- **`narration_text` value** is the screenwriter's narration text verbatim.
  Don't paraphrase — the screenwriter owns the wording.

## Shot kind selection (provider-agnostic)

| Situation | Kind | Notes |
|-----------|------|-------|
| Dialog / character-driven shot | `r2v` | Reference images from cast.json. |
| Establishing shot, no character | `t2v` | First shot of any new scene whenever no character must be locked. Maximises chain-DAG parallelism. |
| Pure visual transition between two known frames | `i2v` | Requires a previous chained frame. Never the first shot of a chain group. |
| Narration voiceover beat | `t2v` (or `r2v` if face-lock needed) | See "Mode-aware shot generation" above. |

**Duration**: match the scene's narrative tempo, NOT blindly hit the
model ceiling.

| Situation | Recommended duration |
|-----------|---------------------|
| Long dialog exchange, 2+ characters | 12–15s |
| Single character action / emotional beat | 8–12s |
| Quick reaction shot / insert / cutaway | 4–6s |
| Narration beat (voiceover) | 3–6s |
| Establishing / transition shot (no dialog) | 5–8s |

**Why not always 15s?** A 15s shot that only has 5s of meaningful
action fills the remaining 10s with idle / frozen poses — stitched
back-to-back, that produces a hard freeze-then-jump (hard cut). **Trim the
fat at the storyboard level, not in post.**

**Mix target**: ~70% `r2v`, ~25% `t2v`, ~5% `i2v` (i2v should be rare).

## Provider capability table

| Capability | bl (happyhorse + wan2.6) | wan27 (fallback only) | If active provider doesn't support it |
|---|---|---|---|
| `r2v` first-frame chain (cast images + prev last-frame) | partial — chain works but cast image priority is limited | ✅ full | The dispatcher demotes to plain `i2v` (drops cast images, keeps the chain). Prefer breaking the chain + fresh `r2v` if a key character must be visible. |
| `r2v` reference voice (`--image-voice`) | ✅ | ✅ | n/a — both support it. |
| `negative_prompt` | ❌ ignored by happyhorse | ✅ wan2.7 | Encode forbidden imagery in the positive prompt when on bl. |
| `prompt_extend` | ❌ ignored | ✅ wan2.7 | Write fully-specified prompts; don't rely on auto-elaboration. |
| Reference syntax in r2v prompts | `[Image 1] / [Image 2]` (happyhorse), `图1 / 图2` (wan2.6) | `图1 / 图2 / 视频1` (wan2.7) | Default to `[Image 1]` style when unsure — bl/happyhorse rejects 图1. |
| Duration floor / ceiling | 3s / 15s (happyhorse) | 2s / 15s | Dispatcher clamps and warns. |

**Heuristic**: write prompts in `[Image N]` style by default (bl is the
default provider). If the producer pins `wan27` for this episode, switch
to `图N` syntax.

## Mood anchor (single biggest visual cohesion lever)

Append `lore.front.mood_anchor` **verbatim at the end of every shot
prompt**. The renderer does NOT do this for you. Without it, every shot
drifts visually.

## Character consistency — cast portrait does the work, prompt stays out

AI video models have no cross-shot memory: re-mention wardrobe in every
prompt and you get a *different* dress shape every clip. The fix is
**delegation**:

| Aspect | Where it lives | Where it does NOT live |
|--------|---------------|------------------------|
| Face / hairstyle / costume / build | The cast `reference_image` (r2v shots only) | The shot prompt |
| Age | The shot prompt — verbatim ("28 岁青年", "中年妇女", "白发老者") | (also OK in soul card, but required in every prompt that introduces the character) |
| Gender, body type | Implicitly via portrait | Don't re-state in prompt unless the camera frames it |
| Mood / facial expression | The shot prompt (this is shot-specific) | — |

### Hard rules

1. **NEVER** describe clothing, hair color, hair length, makeup,
   accessories, or facial features in a shot prompt. Repeating fights
   the reference image and the model averages the two.
   - ❌ "陆辰穿白色 T 恤站在写字楼前"
   - ❌ "[Image 1]苏晚穿红色婚纱, 卷发, 眼影偏粉"
   - ✅ "中景 [Image 1] 28岁的陆辰站在写字楼前, 阳光斜射"

2. **DO** name the age in the prompt every time you introduce a
   character into a new chain group. Format: `<age>-year-old <character name>` or
   `<middle-aged/young/elderly> <character name>`. Repeat per chain group, not per shot inside one.

3. **DO** keep dialog lines verbatim (per Shanyin red lines).

4. If `cast.json` was forked into the episode tier (costume change),
   trust it: the episode-tier portrait already shows the new outfit,
   you still write zero clothing in the prompt.

### Costume change mid-project — fork the cast

If the story REQUIRES a character to wear something different from
their project-tier portrait, do NOT solve it in the prompt. Use
`spark-video-cast` skill's fork procedure to override the portrait for
this episode only. Episode tier overrides project tier automatically.

## Dialog & voiceover in drama-mode prompts

In drama mode the video model is the **sole source of audio** — there
is no post-production TTS pass (that's narration mode only). If a shot
has dialog, voiceover, news broadcast, system prompt, or any spoken
audio, you **must write the spoken text into the shot prompt** so the
model generates the speech as part of the video.

### How to include dialog

Take the **Dialog** section from `scene-NN.md` and weave each line
into the shot prompt. Describe who speaks, the delivery style, then
quote the line.

| Scene-NN.md Dialog | Shot prompt |
|---|---|
| `- 新闻播报（画外音）: "全球生产与运输系统，已全面实现自动化。"` | `…冷静的女性新闻播报声音说："全球生产与运输系统，已全面实现自动化。"…` |
| `- 系统提示（轻声）: "今日无需安排。"` | `…一个轻柔的电子系统提示音响起，说："今日无需安排。"…` |
| `- 主角（轻声）: "……还不知道。"` | `…主角犹豫片刻，轻声回答："……还不知道。"…` |

### Rules

1. **Every dialog / voiceover line from the screenplay must appear in
   exactly one shot prompt.** If a scene has 3 dialog lines and 2 shots,
   decide which shot carries which line — don't drop any.
2. **Quote verbatim.** Don't paraphrase the screenwriter's dialog.
3. **Describe delivery** (tone, volume, emotion) to guide the model's
   audio generation: "冷静地说", "轻声回答", "愤怒地喊道".
4. **Off-screen audio** (news broadcasts, PA announcements, phone calls)
   is still part of the prompt — describe the sound source and quote the
   line, e.g. "背景中电视新闻播报声说：…".
5. **Don't rely on `narration_text`** for drama-mode dialog.
   `narration_text` is a narration-mode-only field for external
   third-person TTS voiceover; it is rejected on `role: "drama"` shots.

## Movie sets (set dressing)

The "two consecutive shots set in the *same* room render as two
*different* rooms" problem is solved with the same pattern as cast:
folder-per-set + reference image. Sets live under:

- `projects/<p>/movie-set/<name>/` (project-tier, shared across episodes)
- `projects/<p>/<ep>/movie-set/<name>/` (episode-only locations)

Each folder needs a `set.md` description card and at least one
reference image. Episode tier overrides project tier.

### ⚠ ONE FOLDER = ONE LIGHTING STATE (hard rule)

The video model reads the set's reference image **literally**. Feed a
noon-lit inn-lobby photo into a midnight shot and you get a midnight clip
with characters wearing a noon-lit room. **Mandatory split**:

| Same place, different… | Action |
|---|---|
| Time-of-day (day / dusk / night / pre-dawn) | **Two separate folders** (`客栈大堂-白天`, `客栈大堂-夜晚`) |
| Season (spring / summer / autumn / winter) | Separate folders if visible (willows / snow / red leaves) |
| Color grade (memory cold gray / present warm yellow) | Separate folders |
| Weather (clear / rain / snow / fog) | Separate folder when weather is in frame |
| Decor unchanged but action moves around the room | **Same folder** |

**Naming**: `<location>-<discriminator>` —
`同福客栈大堂-白天`, `同福客栈大堂-夜晚`, `女主家-冬-飘雪`.

### How to use a set

1. **Pick a stable folder name for each location AND lighting state.**
2. **Set `Scene.set_id`** to the most common lighting state for that scene.
3. **Per-shot override via `Shot.set_id`** when one shot in the scene
   genuinely lives in a different lighting state. Common in narration
   mode — a "Lu Chen's grueling daily routine" scene might span
   `office-tower-daytime` + `construction-site-night` + `rental-room-warm-lamp`.
   Each beat sets `Shot.set_id` explicitly; `Scene.set_id`
   stays `null`.

   Precedence: `null` = inherit from scene, `""` = explicit opt-out,
   any other string = override.

4. **Within ONE chain group**, every r2v shot must resolve to the
   **same** `set_id` (or none). The renderer's chain-bridging first_frame
   already locks lighting; appending a *different* set image fights that
   lock and produces flicker. The validator lints this — if you see
   `"chain rooted at S02-003 uses set_id='客栈-白天' but this shot
   resolves to '客栈-夜晚'"`, either split the chain
   (`use_prev_last_frame_as_first: false` on the offending shot) or
   align the `set_id`.

5. **The renderer auto-appends the set's reference image to every r2v
   shot's `media[]`** after cast portraits. You do NOT mention
   "[Image N] 客栈大堂" in the prompt — it's automatic.

6. **For `t2v` shots in a scene with `set_id`**, the model can't take
   a reference image. Weave the set's textual description (especially
   lighting/color words) into the prompt manually, OR change kind to
   `r2v` with `characters: []` (a "location-locked t2v").

7. **Don't write clothing-style ban for sets either.** Describe action /
   camera only — let the reference image carry layout, materials, props,
   AND lighting.

### Scaffolding a set

See `references/spark-video-cast/SKILL.md` for the full set scaffolding
procedure (cast / set / prop are unified there).

## Key props

Cast pins faces, movie-set pins rooms, **prop pins the *thing*** that
moves between shots. Without it, the same red envelope / key / ring / teddy bear
will render as visually different objects every time. Same pattern:
folder per prop, reference image, `Shot.props` to attach.

### When a thing must be a prop

Promote any object to a key prop when it satisfies **either**:

- Appears in 2+ shots and the audience would notice if it changed shape/material/color/wear.
- Story-critical hero object even in a single shot.

Skip a prop for background dressing (generic teacup, generic phone) or
non-recurring objects whose look doesn't matter.

**Budget**: 3–6 named props per episode; more is a smell.

### ⚠ ONE FOLDER = ONE NARRATIVE STATE (hard rule)

Same physical prop, different visible state = **different folder**:

| Same prop, different… | Action |
|---|---|
| Story state (intact → creased → torn / closed → open / new → worn) | Separate folders |
| Damage / blood / dirt visible | Separate folders |
| Camera angle of the *same* state | Same folder, multiple images |

Naming: `<prop_name>-<state>` — `红包-完整`, `红包-起皱`, `红包-撕碎`.

### How to use a prop in a storyboard

1. **List the prop in the scene's `props_present`** for recall (mirrors
   `characters_present`). The validator warns when a shot references a
   prop the scene didn't declare.

2. **Set `Shot.props: ["<prop name>", ...]`** on every r2v shot where
   the prop is on screen and matters. Names must match a folder —
   case-sensitive, exact match.

3. **State transitions**: when the prop changes state mid-scene, swap
   the prop name across shots:

   ```json
   "shots": [
     {"id": "S03-001", "kind": "r2v", "characters": ["陆辰"],
      "props": ["红包-完整"], "prompt": "陆辰把现金塞进红包内层"},
     {"id": "S03-002", "kind": "r2v", "characters": ["陆辰"],
      "props": ["红包-起皱"], "prompt": "陆辰紧攥红包, 边角微皱",
      "use_prev_last_frame_as_first": false},
     {"id": "S03-003", "kind": "r2v", "characters": ["陆辰","钱夫人"],
      "props": ["红包-撕碎"], "prompt": "钱夫人当面撕碎红包",
      "use_prev_last_frame_as_first": false}
   ]
   ```

   `use_prev_last_frame_as_first: false` on state-change shots — chaining
   through a state transition tries to interpolate frame-by-frame and
   produces flicker. Use a hard cut.

4. **The renderer auto-appends each prop's reference image to the r2v
   shot's `media[]`** after cast portraits and after the set image. You
   do NOT mention "[Image N] 红包" in the prompt — it's automatic.

5. **DON'T re-describe the prop's appearance in the prompt.** Same rule
   as cast: material / color / shape / wear belongs to the reference image.
   The prompt describes the *action* the character does WITH the prop
   ("stuff money in / crumple / tear / toss onto table"), framing, and at most a single
   state word ("creased red envelope" — never "large red hot-stamped envelope printed with 囍").

6. **Provider image cap**: r2v media[] has a hard ceiling
   (bl/happyhorse ~9, wan27 higher). Priority order: cast → set → props.
   If the cap is hit, the dispatcher drops props first with a warning.
   Mitigation:
   - Lower `Shot.characters` to who's actually visible in this beat.
   - Split crowd shots into a wide t2v + a tight r2v.

7. **`t2v` shots ignore `Shot.props`**. The validator warns. Either
   change `kind` to `r2v` (set `characters: []` if no faces) or weave
   the prop's textual description into the t2v prompt manually.

### Scaffolding a prop

See `references/spark-video-cast/SKILL.md` for the unified
cast/set/prop scaffolding procedure.

## NPC generation (before writing the storyboard)

If the screenplay's `<!-- CAST CHECK -->` block lists named NPCs who are
not yet in `cast.json`, generate them BEFORE storyboarding via the
`spark-video-cast` skill's NPC procedure.

After generation, re-read `cast.json` before continuing.

## Validation + post-write

After all scene fragments are written, the producer runs:

```bash
uv run scripts/storyboard.py compile     # merge scenes/*.json → storyboard.json
uv run scripts/storyboard.py validate
uv run scripts/storyboard.py graph       # check chain group count
uv run scripts/storyboard.py estimate    # exit 2 if over budget
```

If validate flags warnings, fix the affected `scenes/scene-NN.json`
files and re-compile.

If `graph` shows almost every shot in one giant chain, you've over-set
`use_prev_last_frame_as_first: true`. Break chains where continuity
isn't actually required.

## Failure recovery (during render)

A shot's render or video review may fail. The producer hands you back
a `reviews/<shot>-verN.json` plus the original shot. You:

1. Read the review's `critique` and `breakdown`.
2. Edit the corresponding shot in `scenes/scene-NN.json` — usually
   rewrite the prompt, sometimes change kind / duration / characters / seed.
3. Re-compile: `uv run scripts/storyboard.py compile`.
4. Re-render: `uv run scripts/render_shot.py --shot <id> --force --reset-attempts`.

The clip-review skill handles the first 2 retry rounds with auto
prompt-rewrite. You only get called for escalation, when nuanced
judgment is needed.

## DON'Ts (spark-video-specific, on top of Shanyin red lines)

- Don't write the screenplay. The screenwriter does that.
- Don't invent character names not in `cast.json`.
- Don't write vendor-specific model strings into `kind` (e.g.
  `wan2.7-r2v`). Write `t2v` / `i2v` / `r2v`.
- Don't set `use_prev_last_frame_as_first: true` on the first shot of a
  scene unless you actually want a cross-scene chain.
- Don't blindly set `duration: 15` on every shot. Match duration to
  narrative tempo. Dead air at the tail causes hard freezes when stitched.
- Don't call `render_shot.py` before `storyboard.py validate` passes.
- Don't assume a feature is available across all providers. Cross-check
  the capability table before relying on `negative_prompt`, voice, or
  first-frame r2v continuation.
- Don't write wardrobe / hairstyle / makeup / accessories in shot prompts. Cast portrait
  owns appearance. Solve costume changes by forking the cast — never by
  writing "wearing XXX" into the prompt.
- Don't omit age. Every chain group's first character mention must
  include the age. Without it, the model drifts apparent age across shots.
- Don't manually paste set / location descriptions into r2v shot
  prompts when the scene has `set_id` — the renderer attaches the set's
  reference image automatically.
- **Don't reuse one set folder across different lighting / season /
  color-grade states.** Scaffold separate folders.
- Don't mix `set_id` values inside one chain group. If a chain crosses
  a lighting boundary, split it (`use_prev_last_frame_as_first: false`).
- Don't describe a key prop's appearance (material / color / shape / wear)
  in the prompt when you've listed it in `Shot.props`.
- Don't reuse one prop folder across narrative states. `intact` / `creased` /
  `torn` (e.g. `红包-完整`, `红包-起皱`, `红包-撕碎`) are three separate folders.
- Don't bolt `Shot.props` onto `t2v` / `i2v` shots — they have no
  `media[]` slot.
- Don't blow past the provider's image cap. Trim `Shot.characters` to
  who's actually visible.
