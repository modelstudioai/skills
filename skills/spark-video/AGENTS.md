# AGENTS.md — working on the spark-video codebase

Guidance for AI agents (and humans) **editing this repository**. If you
instead want to *use* spark-video to make a video, that runbook lives in
[`SKILL.md`](SKILL.md) — this file is about changing the code behind it.

## What this project is

spark-video is **a skill, not a standalone CLI**. The whole product is a
set of `SKILL.md` prompt files plus deterministic Python scripts. Any
skill-aware agent (Claude Code, Cursor, Qwen Code, Codex, …) loads the
markdown as prompts and calls the scripts as tools. There is no server,
no daemon, no installed binary of our own — keep it that way.

Two design invariants drive almost every decision here:

1. **Cross-shot consistency** — faces, sets, props, and style must not
   drift between independently generated clips.
2. **Narrative coherence** — 20+ separate ~8s clips must read as one
   story.

Both are solved with *engineering constraints around the model*, not by
trusting the model. Read [`docs/architecture.md`](docs/architecture.md)
for the full rationale before making structural changes.

## Repo map

```
SKILL.md                     ← root router skill (runtime entry point + install runbook)
README.md / README.zh.md     ← user-facing intro (EN / Chinese)
docs/architecture.md         ← the "why" — design philosophy & consistency model
references/
  spark-video-episode/       ← producer (one-shot orchestrator, the 4+2 gates)
  spark-video-screenwriter/  ← premise → scene-NN.md
  spark-video-director/      ← scene-NN.md → scene-NN.json (storyboard fragment)
  spark-video-cast/          ← cast / movie-set / prop reference-asset generation
  spark-video-vfx-review/    ← opt-in pre-render static quality gate
  spark-video-clip-review/   ← post-render scorer + retry state machine (+ rubric.md)
scripts/                     ← deterministic tools (the "tools" the skills call)
  bl                         ← REQUIRED wrapper around the `bl` CLI (logs every call)
  doctor.sh                  ← dependency check (bl + ffmpeg + uv + python3.10+)
  storyboard.py              ← compile / validate / estimate / graph
  render_shot.py             ← render one shot; auto-scores + promotes winner; owns shots_state.json
  render_all.py              ← batch-render all/failed/rejected shots; chain-group parallel; media auto-resolve
  gate.py                    ← deterministic gate verifier (verify-don't-constrain)
  stitch.py                  ← concat + TTS narration + BGM mix → final mp4
  scaffold.py · build_viewer.py · tts_qwen.py · install-deps.sh · install-hooks.sh · pre-commit
  providers/                 ← pluggable backends: bl.py (default), dashscope_wan27.py
lib/                         ← Pydantic data models + infra (storyboard, lore, cast,
                               movie_set, prop, soul, render_graph, state, bgm, config,
                               review, …)
.cursor/hooks.json + hooks/  ← optional Cursor `stop` hook running gate.py (Scheme D)
.qwen/commands/*.toml        ← Qwen Code slash-command shims that map to the skills
```

`projects/` and `cast/` are runtime output dirs — **git-ignored except
`.gitkeep` / `README.md`** (the pre-commit hook enforces this).

## Dev setup & running

- **Python**: 3.10+. Scripts use PEP 723 inline script metadata and are
  run with `uv` — never `python script.py` directly. Each script
  declares its own deps in a `# /// script` header.

```bash
./scripts/doctor.sh                 # verify bl + ffmpeg + uv + python + sub-skills
uv run scripts/storyboard.py --help # run any script (uv resolves inline deps)
cp .env.example .env                # then fill in DASHSCOPE_API_KEY
```

- Runtime config is read from env vars in [`lib/config.py`](lib/config.py)
  (the `VIDEOGEN_*` family, e.g. `DASHSCOPE_API_KEY`,
  `VIDEOGEN_VIDEO_PROVIDER`, `VIDEOGEN_REVIEW_THRESHOLD`). The skills
  additionally set per-run `SPARK_VIDEO_*` vars (project / episode /
  phase / concurrency). When adding a knob, add it to **both**
  `lib/config.py` and `.env.example` with a comment.
- Install the git hook once: `./scripts/install-hooks.sh`.

There is no test suite or `pyproject.toml`. The closest things to CI are:

- `uv run scripts/storyboard.py validate` — schema/lint check on a storyboard.
- `uv run scripts/gate.py check <script|storyboard|render|final|all>` —
  cross-artifact completeness check (every clip scored + won, viewer fresh,
  …). stdlib-only; `--json` for a dashboard. This is the deterministic
  backstop for "an agent skipped a step".
- `./scripts/doctor.sh` — environment + sub-skill presence check.

Run both after changing `lib/` models or `scripts/storyboard.py`.

## Conventions you must follow

- **Never call `bl` directly. Always go through `./scripts/bl`.** The
  wrapper appends every model call to `logs/model_calls.jsonl` — that
  audit trail is a core feature. This applies to scripts, skills, and
  any subagent you spawn.
- **`shots_state.json` has exactly one writer: `scripts/render_shot.py`,
  via an exclusive `flock`.** Every other script reads it. Do not add a
  second writer or you reintroduce the lost-attempt race. (`lib/review.py`
  scores clips but never touches `shots_state.json` — it returns the review
  dict for `render_shot.py` to commit under the lock, and only writes the
  `reviews/<shot>-ver<N>.json` sidecar.)
- **No-judgment steps go in code; judgment stays in the skill.** This is
  why scoring/promotion live in `render_shot.py` + `lib/review.py` (an
  inferior model can't skip them) while *how* to rewrite a failing prompt
  or *when* to escalate stays in `spark-video-clip-review`. When adding a
  step, ask "does this need a model's judgment?" — if no, make it a
  deterministic, idempotent tool call and let `gate.py` verify it.
- **`render_shot.py` imports `lib.review` but NOT `lib.config`.** Its uv
  env only declares `requests`; `lib.config` pulls in `python-dotenv`. Keep
  `lib/review.py` dependency-light (stdlib) and read env directly there.
- **Don't hand-write `script.md` or `storyboard.json`.** Produce them
  through `uv run scripts/storyboard.py compile` so validation runs.
- **Consistency comes from assets, not prompts.** One folder = one
  visual state (`cast/<name>/`, `movie-set/<name>/`, `props/<name>/`).
  Appearance (hair/costume/face) is locked by the reference portrait;
  prompts describe only action + emotion. Don't "fix" drift by stuffing
  wardrobe text into prompts — fork the asset folder instead.
- **Provider-agnostic core.** `lib/` and the director skill emit generic
  shot kinds (`t2v` / `i2v` / `r2v`); concrete model names live only in
  `scripts/providers/*`. New backends go in `scripts/providers/` behind
  the same interface — don't leak model names upward.
- **Keep skills framework-neutral.** `SKILL.md` files are plain Markdown
  + YAML front-matter with no runtime binding. Don't add
  framework-specific syntax.
- Match existing style: scripts open with a docstring + usage block and
  `from __future__ import annotations`; `lib/` models are Pydantic v2.

## Never commit

The pre-commit hook (`scripts/pre-commit`) blocks these, but know them:

- Anything under `cast/` or `projects/` except `.gitkeep` / `README.md`
  (portraits, voices, rendered clips, frames, `cast.json`, `lore.md`, …
  are all local-only).
- Any blob > 5 MB.
- Secrets — `.env`, API keys. Only `.env.example` is tracked.

## Where to make a change

| You want to change… | Edit here |
|---|---|
| How a stage *thinks* (creative judgment, gates, contracts) | the relevant `references/*/SKILL.md` |
| Deterministic behavior (compile, render, stitch, scoring math) | `scripts/*.py` |
| Clip scoring mechanics (omni call, parse, average, promote) | `lib/review.py` |
| Gate completeness checks (what must exist before a gate) | `scripts/gate.py` |
| Data shape / validation rules | `lib/*.py` (Pydantic models) |
| A new video/image backend | `scripts/providers/` |
| The review rubric / scoring axes | `references/spark-video-clip-review/rubric.md` |
| Default config knobs | `lib/config.py` **and** `.env.example` |
| Design rationale / docs | `docs/architecture.md`, `README*.md` |

When in doubt, prefer pushing *judgment* into the skill prompt and
keeping the script a thin, deterministic, reproducible tool.
