# bailian-train-deploy

> [中文版 / Chinese →](README.zh.md)

End-to-end **train → deploy → call** skill for **Alibaba Cloud Model Studio (Bailian)** — drives the full closed loop with the Bailian CLI (`bl`): dataset validation/upload → SFT/DPO/CPT fine-tune (text) or CosyVoice TTS fine-tune (audio) or Wan2.7 image generation fine-tune → wait for training → export checkpoint → create inference deployment → wait for ready → hand off a callable example. Can also skip training and deploy a base model directly.

## What it does

Tell your agent "train a model" or "deploy my fine-tuned model on Bailian," and this skill will:

1. **Pre-check** — verify auth (`bl auth status`) and query training capabilities (`bl finetune capability`) to pick a supported base model and training type
2. **Prepare data** — local file, an already-uploaded dataset, or a generated sample; validate with `bl dataset validate` before submitting
3. **Create the fine-tune job** — `bl finetune <modality> create` with the right `--training-type` (`sft-lora` / `sft` / `dpo` / `cpt`) and sensible hyperparameters. Audio TTS uses `sft-lora` → `efficient_sft` with auto-injected audio hyperparams. Image generation also uses `sft-lora` with auto-injected Wan2.x hyperparams (max_steps, lora_rank, etc.)
4. **Wait asynchronously** — poll training status via a Monitor script (non-blocking), exit on `SUCCEEDED` / `FAILED` / `CANCELED`
5. **Deploy** — `bl deploy <modality> create` to turn the fine-tuned (or base) model into a dedicated inference instance
6. **Wait for ready** — poll deployment status until `RUNNING`
7. **Hand off** — a ready-to-run example: `bl text chat` for text models, `bl speech synthesize --voice default` for audio TTS, async API + trigger word for image generation

## When to use

**Explicit training/deployment:**
- "Fine-tune a model on my data and deploy it"
- "Train an SFT/LoRA/DPO model on Bailian"
- "Deploy my fine-tuned model so I can call it"
- "Fine-tune a CosyVoice TTS model with my voice data"
- "Fine-tune a Wan2.7 image generation model"

**Implicit (describe a goal, the skill runs the loop):**
- "Train a reasoning model on my customer Q&A"
- "Continued-pretrain on my domain docs"
- "I want my own deployed Qwen instance"
- "Train a voice synthesis model using my own voice"
- "Train a text-to-image model with my own pictures"

**Direct base-model deployment (skip training):**
- "Just deploy `qwen3-8b` as my own service"

**Not for this skill (reverse-trigger routing):**
- Just want to try a model / one-off chat → `bailian-cli`: `bl text chat --model qwen3-8b --message "..."`
- Don't know which base model to pick → `bailian-model-recommend`
- Pure parameter / pricing / context-window lookup → `bailian-docs-llm-wiki`
- Lifecycle management of existing jobs/deployments (list/pause/resume/delete) → `bl` directly: `bl finetune list` / `bl deploy list` / `bl deploy pause` / `bl deploy resume` / `bl deploy delete`
- Quantization (`bl finetune compress`) and throughput-reservation / ModelCode capacity (`bl deploy capacity`) → `bailian-finetune`

## Safety guardrails

`bl finetune <modality> create` and `bl deploy <modality> create` are real write operations that create billable resources. Both accept `--dry-run`: the skill previews every request with `--dry-run`, then runs real pre-checks and applies a billing gate:

1. **Pre-checks + dry run** — `bl finetune capability --base-model <base>` (training support), `bl deploy models --source custom|base` (deployable + available plans), `bl deploy list --status RUNNING` (reuse an existing deployment of the same model instead of creating a second billable instance).
2. **Billing gate on `mu`/`ptu`** — `lora` (token-billed, idle usually free) is the safe default; `mu`/`ptu` are reserved resources that bill even when idle, so the skill **asks the user for explicit confirmation before creating them** and never auto-approves reserved resources in non-interactive (agent/CI) contexts. `bl deploy <modality> create` is high-risk: it stops without `--yes`, which is added only after a `--dry-run` preview and the user's confirmation.
3. **Account readiness** — `bl auth status` first; stop if not authenticated.

## Prerequisites

- `bl` (bailian-cli) installed and authenticated (`bl auth status`, or `bl auth login --api-key sk-...`)
- Recommended base for text reasoning: Qwen3 series (`qwen3-8b` / `qwen3-14b` / `qwen3.6-flash`)
- Recommended base for audio TTS: `cosyvoice-v3-flash`
- Recommended base for image generation: `wan2.7-image-pro` / `wan2.7-image`

## Example

```
I have a local jsonl of customer-service Q&A (ChatML format).
Fine-tune qwen3-8b with LoRA, 3 epochs, then deploy it so I can
call it like a normal model.
```

The skill walks the two-link pipeline, polling at the two wait points via Monitor:

```
Link A (train then deploy):
dataset → finetune <modality> create → wait SUCCEEDED → (auto-export) → deploy <modality> create → wait RUNNING → text chat

Link B (deploy base, skip training):
base model → deploy <modality> create → wait RUNNING → text chat
```

It captures the right IDs at each step (`job_id` / `finetuned_output` → `deployed_model`) and steers around the common pitfalls (e.g. calling the fine-tuned model by its `qwen3-8b-ft-...` name returns 404 — you must deploy first and call the `deployed_model` instance id).

## How it works under the hood

```
User request
  → Pre-check auth + training capability (listFoundationModels via API key)
  → Modality dispatch: text → text.md | audio TTS → audio.md | image → image.md
  → Prepare & validate dataset (text .jsonl / audio .zip / image .zip)
  → finetune <modality> create (sft-lora default; CLI value → server field; audio/image hyperparams auto-injected)
  → Monitor wait.sh finetune <JOB_ID>   (30s poll, async)
  → Auto-export best checkpoint (usually skip manual export)
  → deploy <modality> create (pick plan by model source + modality: text ft → lora/mu, audio TTS → mu, image → lora)
  → Monitor wait.sh deploy <DEPLOYED_MODEL>  (15s poll, async)
  → Call: text → text chat | audio TTS → speech synthesize | image → async API + trigger word
```

The skill encodes the full orchestration plus the gotchas (zsh `status` is read-only, `--model` means different things in `deploy <modality> create` vs inference commands, state-propagation 404 right after `RUNNING`, idle-billing differences between `lora` / `mu` / `ptu`, audio TTS only supports `mu` plan, image generation only supports `lora` plan, image prompt requires trigger word) so the agent doesn't have to rediscover them.

## Modality extension architecture

The skill uses a **generic flow + per-modality reference file** layered design to avoid bloat as modalities grow:

- `SKILL.md` — generic 7-step flow skeleton (shared across all modalities)
- `references/text.md` — text model specifics (data format, hyperparams, inference command)
- `references/audio.md` — audio TTS specifics (ZIP format, CosyVoice hyperparams, speech synthesize)
- `references/image.md` — image generation specifics (ZIP format, Wan2.x hyperparams, async API + trigger word)
- `references/finetune.md` — training-type mapping table (cross-modality)
- `references/deploy.md` — plan/deploy-spec reference (cross-modality)

Adding a new modality = one new `references/<modality>.md` file; the main flow skeleton stays unchanged.

## License

Apache-2.0
