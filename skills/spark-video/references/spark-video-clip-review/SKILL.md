---
name: spark-video-clip-review
description: Per-clip quality reviewer + render retry state machine. After each rendered shot, score it on 6 axes via `bl omni` (qwen3.5-omni-plus), then decide ACCEPT / REJECT-and-rewrite / REJECT-and-escalate. Handles up to N retry rounds with auto prompt rewriting; escalates to spark-video-director when retries are exhausted.
---

# Clip Review + Re-Render Skill — spark-video On-Set QA

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

## Scoring is automatic — you drive the *judgment*, not the mechanics

**`render_shot.py` now scores every clip itself.** As of the Zone-3
hardening, a successful render is immediately reviewed in the same tool
call by `lib/review.py`: it builds the `bl omni` call, attaches the
cast portraits for `shot.characters`, parses the 6-axis JSON, averages
it, writes `reviews/<shot>-ver<N>.json`, embeds the review into
`shots_state.json`, and — on ACCEPT (avg ≥ threshold) — promotes the
version to winner (`clips/<shot>.mp4`). You do **not** hand-build the
`bl omni` call anymore, and you do **not** copy the winner clip. That
deterministic spine cannot be skipped.

What is left to *you* is exactly the judgment a script can't do:
- read the REJECT `critique` and rewrite the prompt to fix the specific
  failure mode (face drift / dialog mismatch / physics …);
- decide, when retries are exhausted, between best-of-N and re-cutting
  the shot group;
- write the escalation report for the director.

## The state machine (single source of truth)

For each shot the renderer hands you, run this loop:

```
ver = 1
while ver <= max_retry:                # default max_retry = 3, env: SPARK_VIDEO_MAX_RETRY
    out = render_shot.py --shot <id> ...          # renders AND scores AND
                                                  # auto-promotes winner on ACCEPT
    verdict = out.review.verdict                  # ACCEPT | REJECT | ERROR
    if verdict == ACCEPT:
        # render_shot already set winner_version + copied clips/<id>.mp4. DONE.
        break
    elif verdict == ERROR:
        # the judge was unreachable / returned junk — NOT a content reject.
        # inspect logs/model_calls.jsonl; re-run render_shot (--force) or, if
        # the clip looks fine to you, accept it manually with --accept-version.
        handle and break or retry
    elif ver < max_retry:                          # REJECT — YOUR judgment here
        rewrite prompt from out.review.critique (bl text chat)   # SPARK_VIDEO_PHASE=rewrite
        update scenes/scene-NN.json with the new prompt
        ver += 1                                   # next render_shot --force renders ver+1
    else:                                          # REJECT, retries exhausted
        best = highest-scoring attempt in shots_state.json
        render_shot.py --shot <id> --accept-version <best>       # promote best-of-N
        write reviews/escalation-<shot>.md + needs_director_rewrite.json
        exit with escalation signal
```

The producer reads the escalation file and invokes the
`spark-video-director` skill with it as input.

## How to render + review one attempt

### 1. Render (scoring happens automatically)
```bash
export SPARK_VIDEO_SHOT=S01-002
export SPARK_VIDEO_PHASE=render
uv run scripts/render_shot.py \
  --shot $SPARK_VIDEO_SHOT \
  --kind r2v --duration 12 \
  --prompt "<from storyboard.json>" \
  --media projects/$SPARK_VIDEO_PROJECT/cast/陆辰/portrait1.png \
          projects/$SPARK_VIDEO_PROJECT/movie-set/客栈大堂-夜晚/set1.png

# stdout (JSON) now includes the review verdict:
# {"shot_id":"S01-002","version":1,"video_path":"...","duration_s":12.0,
#  "provider":"bl","model":"happyhorse-1.0-r2v","elapsed_s":47.2,
#  "review":{"score":6.2,"verdict":"REJECT","breakdown":{...},"critique":"..."},
#  "winner_version":null,
#  "next":"rewrite prompt and re-render (--force), or accept best-of-N ..."}
```

In one call the script: writes `clips/S01-002-ver1.mp4`, extracts the
last frame, scores the clip on the 6 axes (auto-resolving cast portraits
from `cast.json`), writes `reviews/S01-002-ver1.json`, embeds the review
into `shots_state.json`, and — if `verdict == ACCEPT` — promotes the
version to winner (`clips/S01-002.mp4`). **You only read the verdict from
stdout.** You never write `shots_state.json`, build the `bl omni` call,
or copy the winner clip.

Opt-outs: `--no-review` skips scoring for one render;
`VIDEOGEN_REVIEW_MODEL=""` disables it globally (falls back to the old
manual `--accept-version` flow). `--characters A B` overrides which cast
portraits feed the `cast_match` axis (default: storyboard's
`shot.characters`).

### 2. The review record (written for you)

`reviews/<shot>-ver<N>.json` and `shots_state.json`'s
`attempts[].review` carry the same object — this is what `viewer.html`
(and a future progress console) renders:

```json
{
  "shot_id": "S01-002",
  "version": 1,
  "score": 6.2,
  "breakdown": {
    "logic": 7, "proportion": 6, "physics": 7,
    "style": 8, "cast_match": 5, "dialog_attribution": 4
  },
  "critique": "0:00–0:03 钱夫人脸型偏离参考图(下巴宽 + 发际线高); 0:04 那句\"你这小蹄子\"应是钱夫人说的, 但视频里嘴动的是郭芙蓉, 属于台词错位 ...",
  "verdict": "REJECT",
  "ts": "<ISO8601>"
}
```

`verdict = "ACCEPT"` iff `score >= threshold` (default 7.0, env:
`SPARK_VIDEO_REVIEW_THRESHOLD` / `VIDEOGEN_REVIEW_THRESHOLD`). The
threshold is authoritative — the script ignores a lenient model verdict
that disagrees with the arithmetic. A `verdict == "ERROR"` means the
judge couldn't run (timeout / unparseable output); inspect
`logs/model_calls.jsonl` rather than treating it as a content reject.

### 3. On REJECT — rewrite the prompt (this is YOUR job)

```bash
export SPARK_VIDEO_PHASE=rewrite
./scripts/bl text chat \
  --model qwen-plus \
  --system "$(cat references/spark-video-clip-review/rewrite-system.md)" \
  --message "Original prompt: <prompt>\nScore: 6.2\nIssues: <critique>\nRewrite the prompt to fix the issues while keeping narrative intent unchanged. Output only the new prompt text, no explanation."

# Update scenes/scene-NN.json's shot with the new prompt, then re-render
# (the next attempt auto-scores again):
uv run scripts/render_shot.py --shot $SPARK_VIDEO_SHOT --kind r2v \
  --duration 12 --prompt "<rewritten>" --media ... --force
```

### 4. Best-of-N when retries are exhausted

```bash
# Promote the highest-scoring attempt (no re-render, no re-score):
uv run scripts/render_shot.py --shot $SPARK_VIDEO_SHOT --accept-version 2
```

Then write the escalation report (next section).

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
| **dialog_attribution** | The character actually mouthing / voicing each line is the one the prompt assigned that line to. **A's line delivered by B / B's mouth moves for A's line** is a hard 0-3. Shots with no dialog → 10. |

**Default threshold**: `7.0` (env: `SPARK_VIDEO_REVIEW_THRESHOLD`).

The detailed rubric the rubric.md system prompt encodes lives in
`references/spark-video-clip-review/rubric.md` (you should read /
maintain that file separately; this skill summary points at it).

## Escalation — when retries exhausted

After `max_retry` REJECT rounds, write a structured handoff for the
director under
`projects/<p>/<ep>/reviews/escalation-<shot>.md`:

```markdown
# Escalation to Director · S01-002

## Three scoring rounds
| ver | score | logic | prop | phys | style | cast | dialog |
|-----|-------|-------|------|------|-------|------|--------|
| 1   | 6.2   | 7     | 6    | 7    | 8     | 5    | 4      |
| 2   | 6.5   | 7.5   | 6    | 7    | 8     | 6    | 4      |
| 3   | 6.6   | 7     | 6    | 7    | 8     | 6    | 6      |

## Recurring issues
- (List problems that appeared in all three rounds — one sentence with timecode + frame position)
- ...

## Fix attempts already tried
- ver2 → ver3 main prompt changes: ...
  Result: ...

## Suggested director changes
- (Specific to storyboard.json fields — prompt / kind / duration / characters / seed / scene.description / set_id / props)
- Priority order
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

For full-episode batch rendering, use `render_all.py` instead of
manually fanning out per chain group:

```bash
uv run scripts/render_all.py --reset
# Or after prompt rewrites:
uv run scripts/render_all.py --rejected-only
```

It handles chain-group parallelism, media resolution, and first-frame
chaining internally. You only intervene for prompt rewrites on REJECT.

## DON'Ts

- ❌ Don't modify `storyboard.json` or `scenes/scene-NN.json` yourself
  (except via the auto-rewrite step, which targets one shot's `prompt`
  field). Structural changes are the director's job.
- ❌ Don't override `winner_path` manually — `render_shot.py` maintains it.
- ❌ Don't re-implement scoring by hand. `render_shot.py` already scores
  every render via `lib/review.py` (cast portraits, 6-axis parse,
  averaging, sidecar, promotion). Read the verdict from its stdout. The
  only reason to call the judge yourself is debugging.
- ❌ Don't `--no-review` or set `VIDEOGEN_REVIEW_MODEL=""` to "speed
  things up". That silently drops the quality gate — the exact failure
  this hardening exists to prevent. Disable review only on explicit user
  request, and tell them.
- ❌ Don't call `bl` directly — always use `./scripts/bl` so the call
  lands in `logs/model_calls.jsonl` (every prompt is part of the PE
  audit trail).
- ❌ Don't escalate before exhausting `max_retry`. Trust the auto-rewrite.
- ❌ Don't widen the threshold to mask problems. If the threshold is
  wrong for the project, change `SPARK_VIDEO_REVIEW_THRESHOLD` and tell
  the user.
- ❌ Don't treat a `verdict == "ERROR"` as a content REJECT. It means the
  judge couldn't run — diagnose via `logs/model_calls.jsonl`, don't
  burn a rewrite round on it.
