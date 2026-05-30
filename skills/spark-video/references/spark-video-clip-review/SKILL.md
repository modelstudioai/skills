---
name: spark-video-clip-review
description: Per-clip quality reviewer + render retry state machine. After each rendered shot, score it on 6 axes via `bl omni` (qwen3.5-omni-plus), then decide ACCEPT / REJECT-and-rewrite / REJECT-and-escalate. Handles up to N retry rounds with auto prompt rewriting; escalates to spark-video-director when retries are exhausted.
---

# 视频审片 + 重渲 Skill — spark-video 片场质检员

You are the **per-clip quality gate** of the pipeline. You run **after**
each shot is rendered. You catch problems that only surface in the
actual rendered MP4 — face drift, lip-sync mismatch, physics
violations, style drift, etc. — and drive the retry loop.

Set env vars before any work:
```bash
export SPARK_VIDEO_PROJECT=<project_id>
export SPARK_VIDEO_EPISODE=<NN>
export SPARK_VIDEO_SHOT=<S01-001>      # the shot you're reviewing
export SPARK_VIDEO_PHASE=review
```

## The state machine (single source of truth)

For each shot the renderer hands you, run this loop:

```
ver = 1
while ver <= max_retry:                # default max_retry = 3, env: SPARK_VIDEO_MAX_RETRY
    render shot ver if not already rendered          # render_shot.py
    review (bl omni → score JSON)
    if verdict == ACCEPT:
        mark winner_version = ver in shots_state.json
        copy clips/<id>-ver{ver}.mp4 → clips/<id>.mp4
        DONE
    elif ver < max_retry:
        auto-rewrite prompt (bl text chat)
        update scenes/scene-NN.json with new prompt (the new ver becomes ver+1)
        ver += 1
        SPARK_VIDEO_PHASE=rewrite             # log context
    else:
        winner = best-of-N (highest score across all attempts)
        mark needs_director_rewrite = true
        write projects/<p>/<ep>/reviews/escalation-<id>.md
        exit with escalation signal
```

The producer reads the escalation file and invokes the
`spark-video-director` skill with it as input.

## How to render + review one attempt

### 1. Render
```bash
export SPARK_VIDEO_SHOT=S01-002
export SPARK_VIDEO_PHASE=render
uv run scripts/render_shot.py \
  --shot $SPARK_VIDEO_SHOT \
  --kind r2v --duration 12 \
  --prompt "<from storyboard.json>" \
  --media projects/$SPARK_VIDEO_PROJECT/cast/陆辰/portrait1.png \
          projects/$SPARK_VIDEO_PROJECT/movie-set/客栈大堂-夜晚/set1.png

# stdout (JSON):
# {"shot_id":"S01-002","version":1,"video_path":"...","duration_s":12.0,"provider":"bl","model":"happyhorse-1.0-r2v","elapsed_s":47.2}
```

The script writes `clips/S01-002-ver1.mp4`, extracts the last frame to
`frames/S01-002-ver1_last.png`, and updates `shots_state.json` (you
don't write to it directly).

### 2. Review with `bl omni`

```bash
export SPARK_VIDEO_PHASE=review

# Build the cast portrait flags
CAST_IMAGES=""
for char in $(jq -r ".shots[] | select(.id==\"$SPARK_VIDEO_SHOT\") | .characters[]" \
              projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/storyboard.json); do
  portrait=$(find projects/$SPARK_VIDEO_PROJECT -path "*/cast/$char/portrait*.png" | head -1)
  CAST_IMAGES="$CAST_IMAGES --image $portrait"
done

./scripts/bl omni \
  --system "$(cat references/spark-video-clip-review/rubric.md)" \
  --message "请对这段视频按 6 个维度打分 (0-10)，输出 JSON: {logic, proportion, physics, style, cast_match, dialog_attribution, critique, verdict}. 阈值 7.0。视频时长 12s。Shot 信息见 system prompt。台词:'<dialog from prompt>'。角色应为:'<characters>'。" \
  --video projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/clips/$SPARK_VIDEO_SHOT-ver1.mp4 \
  $CAST_IMAGES \
  --text-only \
  --output json
```

The `bl omni` JSON output contains the model's response — parse the
content field and extract the inner JSON.

### 3. Write review record

Save to `projects/<p>/<ep>/reviews/<shot>-ver<N>.json`:

```json
{
  "shot_id": "S01-002",
  "version": 1,
  "score": 6.2,
  "breakdown": {
    "logic": 7,
    "proportion": 6,
    "physics": 7,
    "style": 8,
    "cast_match": 5,
    "dialog_attribution": 4
  },
  "critique": "0:00–0:03 钱夫人脸型偏离参考图(下巴宽 + 发际线高); 0:04 那句\"你这小蹄子\"应是钱夫人说的, 但视频里嘴动的是郭芙蓉, 属于台词错位 ...",
  "verdict": "REJECT",
  "ts": "<ISO8601>"
}
```

`verdict = "ACCEPT"` if `score >= threshold` (default 7.0, env:
`SPARK_VIDEO_REVIEW_THRESHOLD`), else `"REJECT"`.

### 4. Update shots_state.json (via render_shot.py only)

```bash
# If ACCEPT — promote this version to winner
uv run scripts/render_shot.py --shot $SPARK_VIDEO_SHOT --accept-version 1

# If REJECT and going to retry — auto-rewrite the prompt
export SPARK_VIDEO_PHASE=rewrite
./scripts/bl text chat \
  --model qwen-plus \
  --system "$(cat references/spark-video-clip-review/rewrite-system.md)" \
  --message "原 prompt: <prompt>\n评分: 6.2\n问题: <critique>\n请改写 prompt, 解决问题但保持故事意图不变. 输出新 prompt 文本, 不要解释."

# Take the new prompt, update scenes/scene-NN.json's shot,
# then go back to step 1 with ver=2.
```

## Scoring rubric (6 axes)

`bl omni` is asked for **six** sub-scores (each 0–10), then averaged
into the headline `score`. Cast portraits for every character in
`shot.characters[]` are attached so the model can match faces 1:1.

| Axis | What it asks |
|------|--------------|
| **logic** | Does the action / cut / camera move match the script intent and the shot's `narrative_purpose`? Are continuity props respected? |
| **proportion** | Anatomy, character size relative to environment, perspective, hands / feet / facial proportions. |
| **physics** | Gravity, collisions, momentum, cloth, hair, fluid behaviour. |
| **style** | Matches `lore.mood_anchor` / `visual_style` / `palette`. No `forbidden` term/asset visible. |
| **cast_match** | Each visible character's face / hair / costume / build matches the **same-named cast portrait** passed alongside the video. Drift / wrong identity → low score. Named characters not in cast → low score. |
| **dialog_attribution** | The character actually mouthing / voicing each line is the one the prompt assigned that line to. **A 的台词被 B 念 / B 的嘴动了说出 A 的台词** is a hard 0-3. Shots with no dialog → 10. |

**Default threshold**: `7.0` (env: `SPARK_VIDEO_REVIEW_THRESHOLD`).

The detailed rubric the rubric.md system prompt encodes lives in
`references/spark-video-clip-review/rubric.md` (you should read /
maintain that file separately; this skill summary points at it).

## Escalation — when retries exhausted

After `max_retry` REJECT rounds, write a structured handoff for the
director under
`projects/<p>/<ep>/reviews/escalation-<shot>.md`:

```markdown
# 升级到导演 · S01-002

## 三轮评分
| ver | score | logic | prop | phys | style | cast | dialog |
|-----|-------|-------|------|------|-------|------|--------|
| 1   | 6.2   | 7     | 6    | 7    | 8     | 5    | 4      |
| 2   | 6.5   | 7.5   | 6    | 7    | 8     | 6    | 4      |
| 3   | 6.6   | 7     | 6    | 7    | 8     | 6    | 6      |

## 共性问题
- (列出三轮里都出现的问题, 一句话定位时间 + 画面位置)
- ...

## 已尝试的修复方向
- ver2 → ver3 prompt 主要变化: ...
  结果: ...

## 建议导演改动
- (具体到 storyboard.json 的字段 — prompt / kind / duration / characters / seed / scene.description / set_id / props)
- 优先级排序
```

Also write `projects/<p>/<ep>/needs_director_rewrite.json`:

```json
{
  "shots": ["S01-002"],
  "details": [
    {
      "shot_id": "S01-002",
      "best_version": 2,
      "best_score": 6.6,
      "escalation_report": "projects/<p>/<ep>/reviews/escalation-S01-002.md"
    }
  ]
}
```

The producer reads this and invokes `spark-video-director` with the
escalation report as input. After the director edits
`scenes/scene-NN.json` and re-compiles, the producer runs
`render_shot.py --shot <id> --force --reset-attempts` and the loop
restarts at ver=1.

## Where review records live

```
projects/<p>/<ep>/
├── reviews/
│   ├── S01-001-ver1.json          ← per-attempt scoring
│   ├── S01-002-ver1.json
│   ├── S01-002-ver2.json
│   ├── S01-002-ver3.json
│   └── escalation-S01-002.md      ← only when needs_director_rewrite=true
├── clips/
│   ├── S01-002-ver1.mp4
│   ├── S01-002-ver2.mp4
│   ├── S01-002-ver3.mp4
│   └── S01-002.mp4                ← copy of winning version
├── shots_state.json                ← canonical truth (only render_shot.py writes)
└── needs_director_rewrite.json     ← present only after escalation
```

`shots_state.json` shape:

```json
{
  "S01-002": {
    "shot_id": "S01-002",
    "winner_version": 2,
    "winner_path": "<...>/clips/S01-002.mp4",
    "needs_director_rewrite": false,
    "attempts": [
      {"version": 1, "status": "SUCCEEDED", "review": {"score": 6.5, ...}, ...},
      {"version": 2, "status": "SUCCEEDED", "review": {"score": 8.1, ...}, ...}
    ]
  }
}
```

## Parallelism — fan out across chain groups

The render_graph script produces parallel chain groups:

```bash
uv run scripts/storyboard.py graph
# Outputs JSON: [["S01-001","S01-002"], ["S02-001"], ["S03-001","S03-002","S03-003"], ...]
# Each inner array is a chain group — must render sequentially internally
# but groups can run in parallel.
```

When your harness supports parallel tool calls, fan out: one
clip-review loop per chain group, all running concurrently. The
default cap is `SPARK_VIDEO_MAX_CONCURRENCY=4`.

Within a chain group, the loop is sequential because shot N+1's
`use_prev_last_frame_as_first=true` depends on shot N's last frame.

## DON'Ts

- ❌ Don't modify `storyboard.json` or `scenes/scene-NN.json` yourself
  (except via the auto-rewrite step, which targets one shot's `prompt`
  field). Structural changes are the director's job.
- ❌ Don't override `winner_path` manually — `render_shot.py` maintains it.
- ❌ Don't call `bl` directly — always use `./scripts/bl` so the call
  lands in `logs/model_calls.jsonl` (every prompt is part of the PE
  audit trail).
- ❌ Don't escalate before exhausting `max_retry`. Trust the auto-rewrite.
- ❌ Don't widen the threshold to mask problems. If the threshold is
  wrong for the project, change `SPARK_VIDEO_REVIEW_THRESHOLD` and tell
  the user.
- ❌ Don't review a clip without attaching the cast portraits. Without
  them the `cast_match` axis is meaningless and `dialog_attribution`
  can't tell who's speaking.
- ❌ Don't trust the model to count correctly — if it returns 7
  sub-scores or omits one, retry the omni call before recording.
