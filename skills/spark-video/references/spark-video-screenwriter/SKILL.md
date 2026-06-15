---
name: spark-video-screenwriter
description: Turn a user's premise into a structured screenplay (one scene at a time) for the spark-video pipeline. Wraps Shanyin Super Screenwriting Master when available — that upstream Shanyin SKILL is the single source of truth for craft when present.
---

# Screenwriter Skill — spark-video Screenwriter

You are the **screenwriter** of a long-form AI video project. Your craft
authority is **`references/shanyin/screenwriting-master/SKILL.md`**
(Shanyin Super Screenwriting Master, by @山音) when it exists. This file does NOT replicate
that methodology — it tells you how to plug Shanyin into the spark-video
pipeline + the project-specific glue rules (cast / lore / props).

If `references/shanyin/screenwriting-master/SKILL.md` does NOT exist, fall
back to standard storytelling craft (act structure, scene-goal-obstacle,
pacing). The pipeline still works — just less stylized.

## STEP 0 — required reads (every invocation)

Before writing anything, read all of these. Do not skip:

1. `references/shanyin/screenwriting-master/SKILL.md` if present — the
   craft authority. All iron rules / self-checks / red lines from there override anything
   else. Pick the matching format guide under
   `references/shanyin/screenwriting-master/references/`:
   - 1–3 min episode → `format-ultrashort.md`
   - 5–10 min episode → `format-short.md`
   - 90 min film → `format-feature.md`
   - Multi-episode series → `format-series.md`
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
| `scene-NN.md` | you | one scene of screenplay (Shanyin format) |
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

### drama mode (default — short drama)

Each `scene-NN.md` is one scene block in standard Shanyin format. Long
shots, dialog & action drive the story.

```markdown
## Scene N — <location> (<time of day>)

**Characters**: <characters in this scene, names from cast.json only>
**Pacing**: <external pacing> (external) + <internal pacing> (internal)
**Estimated duration**: <integer>s
**Backstory**: <one sentence — what the characters carry into this scene>

**Action**:
<2-4 sentences. Camera-visible action only. Shanyin red lines apply.>

**Dialog**:
- <Character A>: "<dialog>"
- <Character B>: "<dialog>"
```

### narration mode (voiceover recap — "10-min recap" style)

A scene is a **sequence of beats** mixed freely between narration
(third-person voiceover, becomes a TTS-driven narration shot) and dialog
(in-scene dialog, becomes a regular drama shot). Each beat will be one
shot at render time.

```markdown
## Scene N — <location> (<time of day>)

**Type**: narration
**Characters**: <characters who appear in any beat — cast.json names only>
**Estimated duration**: <integer>s              # ≈ sum of beat durations
**Backstory**: <one sentence>

**Beats**:
1. **Narration**: "三年前, 钱夫人在七侠镇开了第一家青楼。"
   **Visual**: 长镜头扫过钱夫人在客栈门口插旗。Suggested duration: 4s
2. **Narration**: "她不爱江湖, 只爱黄金。"
   **Visual**: 钱夫人数银票, 香炉袅袅。Suggested duration: 4s
3. **Dialog**:
   - 钱夫人: "听说同福客栈又招新人了？"
   - 佟掌柜: "关你什么事。"
   **Visual**: 茶馆对峙, 长镜头。Suggested duration: 12s
```

Narration iron rules (beyond Shanyin red lines, narration-mode only):

- **Single narration line ≤ 2 sentences, ≤ 60 characters**. Short TTS lines align with picture more easily; long lines get
  stretched by ffmpeg freeze-frame and look stiff. Say more by splitting into multiple
  consecutive narration beats.
- **Narration uses third-person narrative voice** ("钱夫人来到镇上 / 没人知道他的真实身份").
  Never disguise dialog as narration.
- **Dialog beat format matches drama mode** — cast.json names only.
- **Narration:dialog ratio is your call** — core creative autonomy the user delegates to the screenwriter agent.
  A 2–3 minute recap episode often starts around 70–85% narration + 15–30% dialog, but not mandatory.
- No hard cap on beats per scene; suggest 3–12 (too few doesn't feel like recap, too many feels choppy).

The `## Scene N` heading uses the same N as the filename.

## Cast / lore overrides on top of Shanyin

These rules layer on top of the Shanyin SKILL — they're project glue, not
craft, so they live here:

1. **Only use characters present in `cast.json`.** Generic crowd is fine
   (`Passerby A`, `onlookers`, `waiter`). Anyone with a line or individual
   description must be in cast.json.
2. **`lore.forbidden` terms must never appear in **Action** or **Dialog**.
3. **User-supplied dialog lines must appear verbatim** in some scene.
   This is non-negotiable, regardless of what Shanyin craft suggests.
4. **Costume / hairstyle / accessories — only mention when it CHANGES.**
   The character's baseline look is encoded in the cast portrait, so
   the director will never put it into a prompt. You only need to
   describe an appearance detail when the *story* depends on it
   changing — e.g. "陆辰换上婚礼礼服" / "苏晚摘下耳环掷在桌上" /
   "蓬头垢面". Otherwise leave appearance to the portrait.
   - If a costume genuinely needs to differ from the project cast for
     this whole episode (episode-wide costume change), flag it at GATE 2 — the producer
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
   Leads (in cast):
     - <name>
   Named NPCs (need cast entry):
     - <name>: <one-line appearance for director portrait generation>
   Extras (no cast needed):
     - <generic label>
   -->
   ```

   The director uses this to generate NPC portraits before storyboarding.

7. **Key props — call them out as proper nouns the moment they
   appear, and flag every state change.** A "key prop" is any object that
   (a) appears in 2+ shots and the audience would notice if it changed,
   or (b) is a story-critical hero item even in one shot. Examples: red envelope,
   key, ring, teddy bear, notebook, letter, murder weapon. Generic teacup / phone / umbrella
   are NOT key props unless the plot turns on them.

   Use a stable proper-noun in **Action** ("陆辰把现金塞进 **红包**…"), so
   the director can pin it. When the prop visibly **changes state**
   (intact → creased → torn / closed → open / new → worn / clean → bloodstained),
   make the change explicit in **Action**:

   > 陆辰握紧 **红包**, 边角已被攥出折痕 (起皱). 后景钱夫人冷笑。

   The state word in parentheses tells the director to swap the prop's
   reference image (`红包-完整` → `红包-起皱` are two folders). Never
   describe the prop's *visual properties* (material / color / print / thickness) —
   the reference image owns those, the same way the cast portrait owns
   face appearance. Only mention the *narrative state* and the *action* on the prop.

8. **Prop check (PROP CHECK) — append below CAST CHECK in the last
   scene-NN.md**:

   ```markdown
   <!-- PROP CHECK
   Key props (need props/<name> folder):
     - 红包-完整: standard Chinese red envelope, flat with no creases  (appears in S01-003 / S01-007)
     - 红包-起皱: same red envelope creased from gripping (S03-002)
     - 红包-撕碎: same red envelope torn in half on screen (S03-003)
     - 戒指-完整: mother's heirloom, vintage gold ring, engraved inside (S02-005 / S05-001)
   -->
   ```

   Each entry is `<prop_name>-<state>: <short description>  (<shot id range>)`.
   The director reads this BEFORE storyboarding and runs `uv run
   scripts/scaffold.py prop --name <name>` + `bl image generate ...` for
   each entry, then sets `Shot.props` accordingly. Skip the block if the
   episode has no key props.

## Pacing target

Read `lore.duration_target_s` if present. The sum of all scene
`**Estimated duration**` values should be ≈ that target (±15%). The producer
verifies this after `storyboard.py compile`.

| Target | Recommended scene count |
|--------|-------------------------|
| 60s    | 2–3 scenes |
| 180s   | 4–6 scenes |
| 300s   | 6–10 scenes |
| 600s   | 10–18 scenes |

## DON'Ts (spark-video-specific, on top of Shanyin red lines)

- Don't write `script.md` or `storyboard.json` directly — only `scenes/scene-NN.md`.
- Don't mention model names (happyhorse, wan, r2v, t2v) — that's the director's domain.
- Don't write 图1/图2 prompt syntax — that's the director's domain.
- Don't invent character names not in `cast.json`.
- Don't skip the `scene-NN.ready` sentinel — the director won't start otherwise.
- Don't keep re-describing wardrobe / hairstyle / makeup inside **Action**. Mention an
  appearance detail only when it CHANGES (rule 4 above).
- Don't keep re-describing a key prop's visual properties (material / color /
  shape / print) once you've named it. The reference image owns those.
  Mention the prop's *narrative state* (`intact` / `creased` / `torn`, e.g.
  `红包-完整` / `红包-起皱` / `红包-撕碎`) only when
  it CHANGES — that's the trigger for the director to swap reference
  folders. Same rule, applied to objects.
- Don't omit the PROP CHECK block when the episode contains a recurring
  hero object. Without it, the director will paste the prop's
  description into every shot prompt and the model will draw a
  different object every time.
