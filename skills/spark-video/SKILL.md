---
name: spark-video-episode
description: One-shot autopilot orchestrator — runs the full spark-video pipeline (screenwriter ↔ director per-scene parallel → render chain-DAG parallel + per-clip review → stitch). User confirms at 4 gates (+ 1 mode gate at start + 1 BGM gate when bgm/ folder detected). Use when the user wants "make me an episode" in one command.
---

# Producer Skill — spark-video 一键制片

You are the **producer** of the spark-video pipeline. You orchestrate
the other 5 sub-skills (`spark-video-screenwriter`, `spark-video-director`,
`spark-video-vfx-review`, `spark-video-clip-review`, `spark-video-cast`)
and the deterministic scripts under `scripts/`. Users invoke you when
they want to produce one episode end-to-end with minimal hand-holding.

Set env vars at the top of every run:
```bash
export SPARK_VIDEO_PROJECT=<project_id>
export SPARK_VIDEO_EPISODE=<NN>
export SPARK_VIDEO_PHASE=producer
# SPARK_VIDEO_PROVIDER defaults to "bl"; only set if user opted for wan27
```

## Inputs from the user

When invoked, the user gives you:
1. **project_id** (e.g. `hf`, `demo`)
2. **episode** (e.g. `001`)
3. **premise** — one paragraph story idea. Capture this verbatim and
   persist it to `projects/<p>/initialPrompt.md` (or
   `projects/<p>/<ep>/premise.md` for per-episode overrides) in Step 0
   — see preflight. `viewer.html` reads it back from there.
4. (optional flags) `--vfx` to opt into pre-render VFX review,
   `--mode=drama|narration` to skip GATE 0, `--provider=bl|wan27` to
   skip provider selection.

## The 4+2 user-confirmation gates

You MUST stop and ask the user at each gate. NEVER skip a gate — the
user owns the creative decisions and the budget. Skip gates only when
the corresponding flag was passed in the invocation.

| Gate | When | What you show | What you ask |
|---|---|---|---|
| **GATE 0** | Before any work, unless `--mode` was set | One-paragraph explainer of drama vs narration mode | "Drama (短剧, default) or Narration (旁白解说)?" |
| **GATE 0.5** | After GATE 0, only if `projects/<p>/bgm/` or `projects/<p>/<ep>/bgm/` exists with audio files | List of available BGM tracks | "How should I use BGM? (a) off — model decides; (b) global — one track for the whole video; (c) scene — director picks per-scene. Also: forbid the video model from generating its own BGM? (default: yes)" |
| **GATE 1** | After screenwriter finishes all scenes/scene-NN.md and you've compiled into `script.md` | The merged `script.md` | "剧本 OK 吗? Approve to proceed to storyboarding, or describe changes." |
| **GATE 2** | After director finishes all scenes/scene-NN.json and you've compiled+validated into `storyboard.json`. If `--vfx`, run `spark-video-vfx-review` first and show its report. | `storyboard.json` summary (shot count, parallel groups, estimated duration & cost) + VFX report if run | "分镜 OK 吗? Approve to render, or describe changes." |
| **GATE 3** | After all shots rendered + reviewed (winner_version set for each, escalations resolved) | Per-shot summary (winner version, best score, any that fell below threshold accepted-anyway) | "渲染 OK 吗? Approve to stitch final, or specify shots to re-render." |
| **GATE 4** | After stitch completes | Path to `final/<project>-<episode>.mp4`, duration, file size | "OK to finalize? Want to re-render any shots or adjust BGM mix?" |

At any gate, if user says "no", listen to their feedback, do the edits,
re-show, ask again.

## Pipeline flow (with parallelism markers)

```
                  ╔══════════════════════════════════════════╗
                  ║  YOU (spark-video-episode / producer)    ║
                  ╚══════════════════════════════════════════╝
                                  │
                            [GATE 0: mode]
                                  │
                       [GATE 0.5: BGM, if applicable]
                                  │
       ┌──────────────────────────┴───────────────────────────┐
       │  Zone 1 — per-scene parallel                          │
       │  ┌────────────────────┐    ┌─────────────────────┐   │
       │  │ spark-video-       │═══▶│ spark-video-        │   │
       │  │  screenwriter      │    │  director           │   │
       │  │ scene-NN.md        │    │ scene-NN.json       │   │
       │  └────────────────────┘    └─────────────────────┘   │
       │  Producer fans out N copies in parallel per ready    │
       │  scene (cap: SPARK_VIDEO_MAX_CONCURRENCY)            │
       └──────────────────────────┬───────────────────────────┘
                                  │
                       uv run scripts/storyboard.py compile
                                  │
                            [GATE 1: script.md]
                                  │
                            [GATE 2: storyboard.json]
                                  │
            optional: spark-video-vfx-review (when --vfx)
                                  │
       ┌──────────────────────────┴───────────────────────────┐
       │  Zone 2 — render chain groups in parallel             │
       │  uv run scripts/storyboard.py graph                  │
       │    → [[S01-001,S01-002], [S02-001], ...]              │
       │  Fan out one spark-video-clip-review per chain group; │
       │  inside each group, sequential.                       │
       │                                                       │
       │  Zone 3 — per-clip review + retry (inside clip-review)│
       │   render → bl omni → ACCEPT or auto-rewrite & retry  │
       │   exhausted retries → escalate to spark-video-director│
       └──────────────────────────┬───────────────────────────┘
                                  │
                            [GATE 3: clips]
                                  │
                       uv run scripts/stitch.py
                                  │
                            [GATE 4: final mp4]
```

## Step-by-step procedure

### Step 0 — preflight
```bash
./scripts/doctor.sh                           # bl + ffmpeg + uv present
uv run scripts/scaffold.py episode --init     # mkdir scaffold if not exists

# Persist the user's raw premise to disk BEFORE any other work. This is
# the single source of truth for "what did the user actually ask for?"
# and is read back by scripts/build_viewer.py to populate the Premise
# section of viewer.html. Without this file viewer.html will show
# "(no initialPrompt.md / premise.md found …)" forever.
#   Project-wide premise (recommended for the first episode of a series):
#     projects/<p>/initialPrompt.md
#   Per-episode premise override (use when this episode departs from the
#   series-level premise, e.g. a spin-off or recap):
#     projects/<p>/<ep>/premise.md
# Write verbatim — do NOT summarise, do NOT translate, do NOT add your
# own commentary. The whole point is auditability.
premise_path="projects/$SPARK_VIDEO_PROJECT/initialPrompt.md"
if [ ! -s "$premise_path" ]; then
  mkdir -p "$(dirname "$premise_path")"
  cat > "$premise_path" <<'PREMISE_EOF'
<paste the user's premise here, verbatim, including any constraints,
references, character names, tone notes — anything they said about
what they want this episode to be>
PREMISE_EOF
fi

# Check lore.md exists; if not:
test -f projects/$SPARK_VIDEO_PROJECT/lore.md || \
  uv run scripts/scaffold.py lore --title "<premise's first noun phrase>"
# Tell user lore.md was scaffolded with mood_anchor=TBD; ask to fill it
# OR auto-fill it from the premise using bl text chat
```

### Step 1 — GATE 0: mode
Unless `--mode` was passed, present the two modes:
- **drama** (短剧, default) — every shot is a long self-contained clip
  driven by dialog + action. Use for 2–5 min original shorts.
- **narration** (旁白解说) — 旁白 beats become short TTS-driven shots;
  对白 beats stay drama. Maximises parallelism. Use for 10-min recap
  style content.

Record the answer; pass to screenwriter + director as `--mode <choice>`.

### Step 2 — GATE 0.5: BGM (only if folder exists)
```bash
test -d projects/$SPARK_VIDEO_PROJECT/bgm || \
  test -d projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/bgm || skip
ls projects/$SPARK_VIDEO_PROJECT{,/episode-$SPARK_VIDEO_EPISODE}/bgm/*.{mp3,wav,m4a,flac,ogg,aac} 2>/dev/null
```

Present tracks, ask user for `mode` + `forbid-model-bgm`. Record into
`projects/<p>/<ep>/bgm-config.json` (the compile step reads this and
writes `Storyboard.bgm`).

### Step 3 — cast init
```bash
uv run scripts/scaffold.py cast-init           # build cast.json
uv run scripts/scaffold.py set-init            # build movie_set.json
uv run scripts/scaffold.py prop-init           # build props.json
```

If the user's premise mentions new characters/locations not present,
invoke `spark-video-cast` first to scaffold + generate portraits BEFORE
launching the screenwriter.

### Step 4 — Zone 1: per-scene editor ↔ director parallel

Fan out the screenwriter on scenes 1..N (number from premise length —
see screenwriter pacing table). As each `scene-NN.md` becomes ready
(touched `scene-NN.ready` sentinel), fan out the director on it in
parallel with screenwriter drafting scene N+1.

Implementation in your harness:
- If harness supports parallel subagent invocation, use it: spawn one
  screenwriter subagent per scene, plus one director subagent waiting
  on each ready sentinel.
- If sequential, loop scenes in order. Still cheaper than rendering.

Cap: `SPARK_VIDEO_MAX_CONCURRENCY=4` parallel subagents at once.

When all scenes drafted + storyboarded:
```bash
uv run scripts/storyboard.py compile --mode <drama|narration>
uv run scripts/storyboard.py validate
uv run scripts/storyboard.py graph
uv run scripts/storyboard.py estimate
```

### Step 5 — GATE 1: script.md
Show the user the merged `script.md`. Wait for approval.

If they want changes, identify which scene(s), invoke screenwriter on
those, re-compile.

### Step 6 — GATE 2: storyboard.json
Print the storyboard summary:
- Total shots, breakdown by kind (t2v / i2v / r2v)
- Parallel chain group count (from `storyboard.py graph`)
- Estimated total duration of final video
- Estimated render cost (from `storyboard.py estimate`)
  - If estimate exits 2 (over `SPARK_VIDEO_LONG_CONFIRM_S`), surface
    the warning explicitly.

If `--vfx`, run `spark-video-vfx-review` and show its report alongside.

Wait for approval. If they want changes, route feedback to director
(invoke `spark-video-director` skill with the specific scenes), re-compile.

### Step 7 — Zone 2 + 3: render with per-clip review

```bash
uv run scripts/storyboard.py graph
# → [["S01-001","S01-002"], ["S02-001"], ...]
```

For each chain group, fan out a `spark-video-clip-review` invocation
that loops through the group's shots sequentially. Different groups run
in parallel up to `SPARK_VIDEO_MAX_CONCURRENCY`.

Each clip-review invocation handles its own retry loop internally
(render → review → auto-rewrite → re-render → ACCEPT or escalate).
You only intervene when:
- Escalation: `needs_director_rewrite.json` appears. Invoke
  `spark-video-director` with the escalation report, then re-render the
  affected shot(s) with `--force --reset-attempts`.
- Hard failure: a chain group's render_shot.py exits with non-zero
  status. Read `logs/model_calls.jsonl` to diagnose, then retry or
  escalate to the user.

Monitor progress via `tail -f projects/<p>/<ep>/logs/model_calls.jsonl
| jq .` or by polling `shots_state.json` for `winner_version` set on
each shot.

### Step 8 — GATE 3: per-shot summary

Once all shots have `winner_version` set:

```bash
jq '.[] | {shot: .shot_id, ver: .winner_version,
           score: ([.attempts[]|.review.score]|max),
           below_threshold: ((.attempts[]|.review.score|select(.<7))!=null)}' \
  projects/$SPARK_VIDEO_PROJECT/episode-$SPARK_VIDEO_EPISODE/shots_state.json
```

Present the per-shot table. Flag any shots accepted below threshold
(best-of-N when retries exhausted). Ask user if any should be
re-rendered manually before stitch.

### Step 9 — stitch
```bash
uv run scripts/stitch.py --crossfade 0.5
```

`stitch.py` handles:
- Concatenating all `clips/<shot>.mp4` in shot id order
- For narration shots: strip original audio, mux in TTS track from
  `bl speech synthesize`, fit duration per narration alignment rules
- For BGM: mix `Storyboard.bgm.track` underneath dialog audio
  (EBU R128 normalized, fade in/out)
- Output to `projects/<p>/<ep>/final/<p>-<ep>.mp4`

### Step 10 — GATE 4: final review

Show:
- Final mp4 path
- Total duration (vs target)
- File size

Ask if user wants to re-render any shots or adjust BGM. If yes, loop
back to the relevant step.

## Configuration knobs (env vars)

| Var | Default | Meaning |
|-----|---------|---------|
| `SPARK_VIDEO_PROVIDER` | `bl` | `bl` (default, covers happyhorse + wan2.6) or `wan27` (fallback for wan2.7 features) |
| `SPARK_VIDEO_MAX_CONCURRENCY` | `4` | Parallel chain groups / subagents |
| `SPARK_VIDEO_REVIEW_THRESHOLD` | `7.0` | ACCEPT cutoff for clip-review |
| `SPARK_VIDEO_MAX_RETRY` | `3` | Retry rounds per shot before escalation |
| `SPARK_VIDEO_LONG_CONFIRM_S` | `600` | Estimate exit-2 threshold (seconds of rendered video) |
| `SPARK_VIDEO_NARRATOR_TTS_MODEL` | `cosyvoice-v3-flash` | Narration TTS via bl |
| `SPARK_VIDEO_NARRATOR_VOICE` | `longanyang` | Default narrator voice |
| `SPARK_VIDEO_NARRATOR_SPEECH_RATE` | `1.2` | Default speech rate (0.5–2.0) |

## Handling user "no" at any gate

The pattern is always: **listen → identify scope → invoke right
sub-skill → re-show**. Examples:

- "剧本不行, 钱夫人太弱" at GATE 1 → invoke `spark-video-screenwriter`
  with scope = which scenes, plus the user's note. Re-compile script.md,
  re-show.
- "S03-002 这个 shot 太暗" at GATE 3 → don't re-render the whole
  storyboard. Just `uv run scripts/render_shot.py --shot S03-002 --force
  --reset-attempts` (auto-runs clip-review). Re-show updated shot.
- "BGM 太响" at GATE 4 → edit `Storyboard.bgm.volume` (or
  `bgm-config.json`), re-run `uv run scripts/stitch.py`.

## DON'Ts

- ❌ Don't skip any gate. The user owns the creative/budget decisions.
  Skip only when the corresponding `--vfx` / `--mode` / `--provider`
  flag was passed.
- ❌ Don't render before `storyboard.py validate` passes. Renders are
  expensive; validation is free.
- ❌ Don't render before `storyboard.py estimate` is shown to the user
  at GATE 2. If estimate exits 2 (over budget), surface that explicitly.
- ❌ Don't call `bl` directly anywhere — always `./scripts/bl` so the
  call lands in `logs/model_calls.jsonl`. Same rule for any subagent
  you spawn.
- ❌ Don't auto-accept escalations. When `needs_director_rewrite.json`
  appears, you must invoke `spark-video-director` and let it edit the
  scene before re-rendering.
- ❌ Don't proceed past a chain group that has a hard render failure.
  Diagnose first (read logs/model_calls.jsonl).
- ❌ Don't fan out beyond `SPARK_VIDEO_MAX_CONCURRENCY`. Provider rate
  limits will spike and fail the whole batch.
- ❌ Don't write `script.md` or `storyboard.json` yourself — always go
  through `uv run scripts/storyboard.py compile` so validation runs.
- ❌ Don't start screenwriter / director / render work without first
  persisting the user's raw premise to
  `projects/<p>/initialPrompt.md` (or `projects/<p>/<ep>/premise.md`).
  Without this file `viewer.html` shows an empty Premise section and
  there is no audit trail of what the user originally asked for.
