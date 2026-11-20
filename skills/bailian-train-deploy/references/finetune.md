# Fine-tuning Parameter Reference

> This file supplements Step 2 "Create the fine-tuning job" in [`SKILL.md`](../SKILL.md) with `--training-type` values and hyperparameter details. For flow orchestration and pitfall avoidance see SKILL.md. For modality-specific details (data format, model list, inference commands) see [`text.md`](text.md) / [`audio.md`](audio.md) / [`image.md`](image.md).

## training-type values and mapping

The CLI uses the `<method>` / `<method>-lora` convention and maps it to server-side fields at the CLI boundary on submission (always pass CLI values, never server-side strings):

| CLI value | Server-side | Applicable modalities | Notes |
|---|---|---|---|
| `sft-lora` | efficient_sft | text / audio / image | **Default**, LoRA, cheap and fast, suits most scenarios |
| `sft` | full-parameter SFT | text | Higher quality ceiling, significantly higher cost |
| `dpo-lora` / `dpo` | dpo_lora / dpo_full | text | Preference alignment, requires preference data |
| `cpt` | continued pretraining | text | Injects domain knowledge, requires non-conversational data |

> `cpt` has no server-side `-lora` variant, only full-parameter; the other methods (sft / dpo) each have both a `<method>` and a `<method>-lora` variant.
> Audio TTS and image generation only use `sft-lora` (mapped to `efficient_sft`) and do not support other training types; moreover, `finetune audio create` / `finetune image create` **do not expose the `--training-type` flag** (internally fixed to sft-lora) — only `finetune text create` accepts it.

## Hyperparameter recommendations

### Text models

- `n-epochs` defaults to 3. Small datasets (a few hundred samples) are fine with 3; reduce to 1-2 if overfitting.
- `batch-size` adapts to data volume (<100KB auto-sets 8); generally do not set it manually.
- `learning-rate` must be passed as a **string** to avoid JSON precision loss, e.g. `"1e-4"`. The LoRA default is `3e-4` (the platform's setting for small datasets); reduce it if overfitting.
- `--validations <path>` is optional — pass a validation set to watch metrics.

### Audio TTS models

- The 8 audio-specific hyperparameters (lm_max_epoch, fm_max_epoch, etc.) are auto-injected with default values by the CLI; no need to pass them manually.
- Text hyperparameters (`n-epochs` / `learning-rate` / `batch-size`) have no effect on audio — do not pass them.

### Image generation models

- The 12 image-specific hyperparameters are auto-injected with default values by the CLI. Core parameters:
  - `max_steps` (800), `eval_steps` (200), `learning_rate` (3e-5), `lora_rank` (32)
  - `max_pixels` / `val_img_size`: T2I defaults to `"2k"`, I2I defaults to `"1k"` (auto-inferred from the data; no manual setting needed)
  - `generation_type`: auto-inferred from the data — if the first row has an `input_img` field it is `"i2i"`, otherwise `"t2i"`
  - `split` (0.9): automatically splits a validation set from the training set (only takes effect when `--validations` is not specified)
- Text hyperparameters (`n-epochs` / `batch-size`) have no effect on image — do not pass them.

## Required flags

- `--base-model`: base model name (e.g. `qwen3-8b` for text, `cosyvoice-v3-flash` for audio, `wan2.7-image-pro` for image).
- `--datasets`: file-id or local file path (comma-separated for multiple); local paths are validated and uploaded first, then the file-id is used. Text takes `.jsonl`; audio/image take `.zip`.

## Pre-submission validation

Before submitting, `bl finetune <modality> create` validates the model against listFoundationModels for the chosen training type and fails fast if unsupported (without consuming quota). If the number of training samples ≤ batch_size, the job is rejected before upload/quota consumption. Use `bl finetune capability --base-model <base>` to confirm in advance.

> **Known contradiction**: capability for cosyvoice-v3-flash and the wan2.7 series returns `supports.sft=false`, but the API actually accepts `efficient_sft` training requests. The CLI automatically skips this check for the audio and image modalities.
