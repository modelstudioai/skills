---
name: bailian-train-deploy
description: >-
  Use the Bailian CLI (`bl`) to run the full closed loop of "data → fine-tuning → export →
  deployment → invocation", or skip training and deploy a base model directly. Supports
  fine-tuning text models (SFT/DPO/CPT), audio TTS models (CosyVoice), image generation
  models (Wan2.7), and video generation models (Wan i2v/kf2v). Covers dataset
  validation/upload, creating fine-tuning jobs, waiting for training, exporting the best
  checkpoint, creating inference deployments, waiting until ready, and providing call
  examples. Activate this skill whenever the user mentions "train a model" / 训练模型,
  "fine-tune" / "fine-tune" / "finetune" / 微调, "deploy a model" / 部署模型, "put the
  model online" / 模型上线, "run/call my fine-tuned model" / 把微调模型跑起来,
  "train a reasoning model" / 训练一个推理模型, "continued pretraining" / 继续预训练,
  "LoRA/SFT/DPO training" / LoRA/SFT/DPO 训练, "speech synthesis model" / 语音合成模型,
  "TTS fine-tuning" / TTS 微调, "CosyVoice", "voice cloning" / 声音克隆,
  "image generation fine-tuning" / 图像生成微调, "text-to-image" / 文生图,
  "image-to-image" / 图生图, "Wan2.7", "image model training" / 图像模型训练,
  "video generation fine-tuning" / 视频生成微调, "image-to-video" / 图生视频,
  "first-frame-to-video" / 首帧生视频, "first-and-last-frame" / 首尾帧, "kf2v", "i2v",
  "Wan video" / Wan视频, or "video effect training" / 视频特效训练 on Bailian / DashScope /
  Alibaba Cloud Model Studio. Even if the user does not explicitly say "use bl", as long
  as the intent is training or deployment on the Bailian platform, use this skill instead
  of assembling commands yourself.
---

# Bailian Model Training → Deployment Closed Loop (`bl`)

Use the Bailian CLI `bl` to turn a model into a callable dedicated inference service — you can fine-tune first and then deploy, or skip training and deploy a base model directly. Four modalities are supported: text, audio TTS, image generation, and video generation. The two "wait" points use asynchronous Monitor polling and never block the main flow.

```
Link A (train first, then deploy):
dataset → finetune <modality> create → wait for SUCCEEDED → export model (usually automatic) → deploy <modality> create → wait for RUNNING → invoke

Link B (deploy a base model directly, skipping training):
choose a base model → deploy <modality> create → wait for RUNNING → invoke
```

Link B fits "I just want to run some base model as my own deployment service" — in terms of inference it is essentially the same as calling the API directly, but you get a dedicated deployment instance with configurable rate/billing that is under your own operations. **Take this route only when the user explicitly says no training / skip training / deploy the base model directly**; when the user simply has not mentioned training details, default to guiding them through Link A and never skip training on your own initiative.

**Modality dispatch**: The generic flow in this skill applies to all modalities, but data format, hyperparameters, and inference commands differ by modality. Once the user's intent is clear, consult the matching reference file:
- **Text models** (chat/reasoning) → [`references/text.md`](references/text.md)
- **Audio TTS models** (speech synthesis/CosyVoice) → [`references/audio.md`](references/audio.md)
- **Image generation models** (text-to-image/image-to-image/Wan2.7) → [`references/image.md`](references/image.md)
- **Video generation models** (image-to-video/first-and-last-frame/Wan i2v/kf2v) → [`references/video.md`](references/video.md)
- Future modalities = add a matching reference file; this flow skeleton stays unchanged

> This skill assumes `bl` (bailian-cli) is already installed. Command/flag details are governed by `bl <cmd> --help`; this skill focuses on **flow orchestration and pitfall avoidance**.

## Write-operation guardrails (read before creating anything)

`bl finetune <modality> create` and `bl deploy <modality> create` are real write operations that create billable resources (fine-tuning + inference deployment). `bl` has **no `--dry-run`**, so use **pre-check commands** instead of a dry run, and gate reserved resources with **billing confirmation**. Any write operation must pass these three gates first:

1. **Pre-checks instead of dry-run** (must run before creation; write only once feasibility is confirmed). These pre-check commands themselves require authentication via the [pre-flight checks](#pre-flight-checks-start-of-the-action-flow-1) below — if not authenticated, run `bl auth login` first, then pre-check:
   - Before training: `bl finetune capability --base-model <base>` — confirm the base model supports your chosen training-type (unsupported combos fail fast without consuming quota; `create` re-validates at submission).
   - Before deployment: `bl deploy models --source custom` (Link A fine-tuned output) or `--source base` (Link B base model) — confirm the target model is deployable, see the available plans, then decide `--plan`.
   - Reuse detection: `bl deploy list --status RUNNING` — if a RUNNING deployment already references the same `finetuned_output`, reuse its `deployed_model` and **do not create a second billable instance**.
2. **Hard billing-confirmation gate (mu/ptu)**:
   - `lora` (default; token-billed; idle usually not billed) — the safe default, can be created directly.
   - `mu` / `ptu` are **reserved/exclusive resources that bill even when idle** — before creating them you **must** explain the billing model to the user and get their confirmation. In non-interactive environments (agent / CI) you **must not auto-provision reserved resources**. When mu/ptu applies, hand "this will incur idle billing" together with the command back to a real human for terminal confirmation (`bl` currently offers no `--yes` flag to skip confirmation; confirmation is entirely human-controlled).
3. **Account readiness check**: `bl auth status` — if `authenticated: false`, stop and provide `bl auth login --api-key sk-...`. Bailian authenticates with API key / access token and has **no separate real-name gate**; `auth status` is the account readiness check.

## Reverse-trigger table (intents that do not belong to this skill, with full commands)

| User intent | Route to | Full example command |
|---|---|---|
| Just want to try a model / one-off chat | `bailian-cli` | `bl text chat --model qwen3-8b --message "..."` |
| Model already chosen, only need how to call it | `bailian-cli` | `bl text chat --model <model> --message "..."` |
| Don't know which base model to pick / model selection | `bailian-model-recommend` | (let that skill recommend per scenario) |
| Pure lookup of model specs / pricing / context window | `bailian-docs-llm-wiki` | (query the model data catalog) |
| Already have a deployment, only want a call example | `bailian-cli` | `bl text chat --model <deployed_model> --message "..."` or `bl speech synthesize --model <deployed_model> --voice default --text "..."` or the async API + trigger word (image generation, see [image.md](references/image.md#inference-and-invocation)) |
| Query/delete existing jobs or deployments (lifecycle) | `bl` directly | `bl finetune list` / `bl deploy list` / `bl deploy delete --deployed-model <id>` |

> This skill only owns the closed loop of "create a training job + create a deployment + deliver invocation". **Full lifecycle management** of jobs and deployments (list / stop / delete historical jobs, delete deployments, etc.) is outside this skill's flow — operate directly with `bl finetune list` / `bl deploy list` / `bl deploy delete`.

## Anti-hallucination checklist

- **`--base-model` / `--model-name` / `--model` belong to different commands; never reuse them**:
  - `bl finetune <modality> create --base-model` → base model name (text `qwen3-8b`, audio `cosyvoice-v3-flash`, image `wan2.7-image-pro`).
  - `bl deploy <modality> create --model-name` → exported model name (Link A: `qwen3-8b-ft-...` / `cosyvoice-v3-flash-ft-...` / `wan2.7-image-pro-ft-...`; Link B: the base model name).
  - Inference command `--model` → must be the `deployed_model` from the `deploy <modality> create` response, **not** the name you passed to `deploy <modality> create`.
- **`--training-type` exhaustive values**: `sft` / `sft-lora` (default) / `dpo` / `dpo-lora` / `cpt`. The mapping happens at the CLI boundary (`sft-lora`→`efficient_sft`); always pass CLI values, never server-side strings. `cpt` has no `-lora` variant. Audio TTS and image generation only use `sft-lora` — `finetune audio create` / `finetune image create` **do not expose this flag**; only `finetune text create` accepts it.
- **`--plan` exhaustive values**: `lora` (default, token-billed) / `ptu` (requires `--input-tpm`/`--output-tpm`) / `mu` (requires `--deploy-spec`/`--capacity`). Link B base models usually **do not support `lora`**. Audio TTS fine-tuned models **only support `mu`**. Image generation fine-tuned models **only support `lora`**.
- **`--deploy-spec`** (not ~~template-id~~): the deployment-spec flag for the mu plan. The CLI reads `template_id` from the catalog and sends it as `deploy_spec` in the request body.
- **`--source` exhaustive values** (`bl deploy models`): `custom` (fine-tuned output) / `base` (base model) / `public`.
- **`--learning-rate` must be a string**: pass `"3e-4"`, not the number `3e-4`, to avoid JSON precision loss (applies to text; audio/image do not take this parameter).
- **Inference commands differ by modality**: text models use `bl text chat`, audio TTS uses `bl speech synthesize --voice default`, image generation uses the async API + trigger word (see [`references/image.md`](references/image.md#inference-and-invocation)).
- **These flags/subcommands do not exist**: `bl` has no `--dry-run`, no bare `finetune create`/`deploy create` (**the modality segment is mandatory**: `finetune text|audio|image create`, `deploy text|audio|image create`), no `finetune start`, no `deploy stop` (use `bl deploy pause` / `bl deploy resume` to disable/restore; pause stops billing for mu/ptu).
- **Required**: `--base-model` / `--datasets` on `finetune <modality> create`; `--model-name` / `--display-name` on `deploy <modality> create`.

## Pre-flight checks (start of the action flow)

- Authentication: `bl auth status`; confirm an API key is configured (`DASHSCOPE_API_KEY` or `bl auth login --api-key sk-...`).
- Base model selection: query training capability with `bl finetune capability` (queries listFoundationModels via API key; no console login needed):
  - `bl finetune capability --base-model <base>` — which training types this model supports.
  - `bl finetune capability --training-type sft-lora` — reverse lookup: which models support that training type (returns a `models` list with Chinese names).
  - Once a base model is chosen, go straight to Step 2; `bl finetune <modality> create` re-validates against listFoundationModels before submission and fails fast if unsupported.
  - For text reasoning, the Qwen3 series is recommended (`qwen3-8b` / `qwen3-14b` / `qwen3.6-flash`); audio TTS uses `cosyvoice-v3-flash`; image generation uses `wan2.7-image-pro` / `wan2.7-image`.

## Step 1: Prepare the dataset

Three data sources are supported; choose flexibly based on user intent rather than hardcoding an interaction flow — you can proactively ask questions: once you know the options, naturally confirm with the user:

1. **Local dataset** — the user provides a local file path; use it directly.
2. **Already-uploaded dataset** — pick from existing Bailian datasets (`bl dataset list`).
3. **Generated sample data** — with the user's consent, generate a small sample dataset just to walk the flow through (limited quality; tell the user honestly).

**Data format differs by modality**; see the matching reference file:
- **Text models**: `.jsonl` file (ChatML/DPO/CPT schema), see [`references/text.md`](references/text.md#data-format).
- **Audio TTS**: `.zip` package (containing `data.jsonl` + `train/*.wav`), see [`references/audio.md`](references/audio.md#data-format).
- **Image generation**: `.zip` package (containing `data.jsonl` + image files laid out flat), see [`references/image.md`](references/image.md#data-format).

Before submitting training, validate with `bl dataset validate --file <path>` and continue only after it passes (the CLI auto-detects the schema; you can also explicitly pass `--schema tts` / `--schema image` / `--schema chatml`).

## Step 2: Create the fine-tuning job

```bash
bl finetune <modality> create \
  --base-model <base-model> \
  --datasets <path-or-file-id> \
  --output json
```

**training-type values and mapping**: see [`references/finetune.md`](references/finetune.md). **Modality-specific hyperparameters**: see the matching reference file:
- Text models (`finetune text create`): accepts `--training-type` / `--n-epochs` / `--learning-rate`, etc.; see [`references/text.md`](references/text.md#create-a-training-job).
- Audio TTS (`finetune audio create`): **does not expose `--training-type`** (internally fixed to `sft-lora`); hyperparameters are auto-injected by the CLI; see [`references/audio.md`](references/audio.md#create-a-training-job).
- Image generation (`finetune image create`): **does not expose `--training-type`** (internally fixed to `sft-lora`); hyperparameters are auto-injected by the CLI; see [`references/image.md`](references/image.md#create-a-training-job).

Record from the response: `output.job_id`, `output.finetuned_output` (the output model name, shaped like `<base>-ft-<ts>-<id>`).

## Step 3: Wait for training to finish (asynchronous)

Use the Monitor tool to run this skill's bundled wait script — it notifies on status changes and exits at a terminal state:

```
Monitor command: bash <this-skill-directory>/scripts/wait.sh finetune <JOB_ID>
```

`<this-skill-directory>` is this skill's base directory (provided when the skill is loaded, containing `scripts/wait.sh`); substitute the actual path. The script polls every 30s; terminal states are `SUCCEEDED`/`FAILED`/`CANCELED`/`PARTIALLY_SUCCEEDED`.

⚠️ **Pitfall: never hand-write a `status=...` polling loop in zsh.** `status` is a read-only zsh built-in variable; assigning to it raises `read-only variable` and makes the script exit 1. Use this skill's bash script (`#!/usr/bin/env bash`) to avoid it, or rename the variable to something like `st` if you write your own.

## Step 4: Export the best model (usually skippable)

After the job reaches SUCCEEDED, the platform **automatically exports the best checkpoint** as a deployable model — go straight to Step 5; no manual export needed.

Export explicitly only when deploying a checkpoint that is **not the best**:
```bash
bl finetune checkpoints --job-id <JOB_ID>          # list available checkpoints
bl finetune export --job-id <JOB_ID> --checkpoint <name> --model-name <custom-name>
```

## Step 5: Create the deployment

> Before creating, pass the [write-operation guardrails](#write-operation-guardrails-read-before-creating-anything): `bl deploy list --status RUNNING` to check for a reusable deployment of the same model; `bl deploy models --source custom|base` to confirm available plans; for `mu`/`ptu`, obtain the user's billing confirmation first.

⚠️ **Key pitfall: a fine-tuned model cannot be invoked directly by its fine-tuned output name — you get 404 `Model not exist`. You must create a deployment first.** (Same for Link B base deployments — direct calls go through public inference and bypass your deployment instance.)

```bash
bl deploy <modality> create \
  --model-name <finetuned-output> \   # fine-tuned output name (Link A) or base model name (Link B)
  --display-name <display-name> \
  --plan <lora|ptu|mu> \              # see notes below
  --output json
```

- The **modality segment** (`text` / `audio` / `image`) must match the deployed model's modality; the three modality subcommands share identical flags.
- `--model-name`: Link A passes the `finetuned_output` from Step 2; Link B passes the base model name directly.
- `--plan`:
  - Text fine-tuned models default to `lora` (token-billed); `mu` is also available.
  - **Audio TTS fine-tuned models only support `mu`** (not `lora` / `ptu`), requiring `--deploy-spec` + `--capacity`.
  - **Image generation fine-tuned models only support `lora`** (not `mu` / `ptu`).
  - Link B base models usually only support `ptu`/`mu`, **not `lora`**.
  - Required parameters and billing details per plan: see [`references/deploy.md`](references/deploy.md).
- `--deploy-spec`: deployment spec for the mu plan (e.g. `dps-20260521172224-1vabse`); if omitted, it is auto-matched from the catalog.
- Not sure which plans are supported: Link A uses `bl deploy models --source custom`, Link B uses `bl deploy models --source base`; pick from the returned `plans`.

⚠️ **Pitfall (most frequent error): `--model-name` and the inference command's `--model` mean different things** — `deploy <modality> create --model-name` takes the exported model name, while `output.deployed_model` in the response is the deployment instance id; the inference command's `--model` must use `deployed_model`, **do not reuse the other name**. See [`references/deploy.md`](references/deploy.md).

Record from the response: `output.deployed_model`.

## Step 6: Wait for the deployment to be ready (asynchronous)

```
Monitor command: bash <this-skill-directory>/scripts/wait.sh deploy <DEPLOYED_MODEL>
```

`<this-skill-directory>` is the same as in Step 3. Polls every 15s; `RUNNING` means ready (`FAILED`/`STOPPED` are terminal).

⚠️ **Pitfall: status-propagation delay.** Calling immediately after a deployment first reaches `RUNNING` may briefly return 404 `Model not exist` — this is server-side state-propagation delay, not a wrong model name. `bl deploy get` may also still show `PENDING`. It stabilizes within about a minute; on 404, wait a dozen seconds and retry. If 404 persists, first verify you are using `deployed_model` rather than the fine-tuned output name.

## Step 7: Invoke and deliver

**Inference commands differ by modality**:

Text model:
```bash
bl text chat --model <DEPLOYED_MODEL> --message "Your question"
```

Audio TTS model:
```bash
bl speech synthesize --model <DEPLOYED_MODEL> --voice default --text "The text to synthesize" --out result.mp3
```

Image generation model (async API, trigger word required):
```bash
# See references/image.md — requires the X-DashScope-Async header + a prompt containing the trigger word
```

> `--model` must be the `deployed_model` from the `deploy <modality> create` response, **not** the fine-tuned output name. Audio TTS `--voice` is fixed to `default`. Image generation requires async invocation and a prompt containing the trigger word. See the matching modality reference file.

When delivering to the user, provide:
- **The deployment instance id** (`deployed_model`) — use this for invocation, not the fine-tuned output name
- One directly runnable inference example command
- Common ops commands: `bl deploy get --deployed-model <id>` to check status; `bl deploy delete --deployed-model <id>` to delete the deployment; `bl finetune list` for historical jobs.

## Wrap-up notes

- **Idle billing and deletion**: `lora` is usually not billed when idle; `mu`/`ptu` bill even when idle — clean them up when unused; `bl deploy delete` can only delete STOPPED/FAILED deployments; for RUNNING mu/ptu, first `bl deploy pause` (stops billing), then delete. Details in [`references/deploy.md`](references/deploy.md#billing-and-ops-details).
- **Reuse datasets**: when training multiple times on the same data, first `bl dataset upload` to get a file-id, then use `--datasets <file-id>` to avoid repeated uploads.
- **Poor results**: add data first (quantity and quality), then tune `n-epochs`/`learning-rate`, and only consider full-parameter `sft` last. Small datasets (<100 samples) have a limited quality ceiling — manage expectations.
