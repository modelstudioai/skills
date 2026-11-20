# Video Generation Model Reference

> This file supplements [`SKILL.md`](../SKILL.md) with the modality-specific details of the video generation fine-tuning pipeline (data format, models, hyperparameters, deployment, inference). See SKILL.md for the generic flow.

## Applicable scenarios

The user wants to fine-tune a video generation model, training a custom-effect, motion, or style LoRA model from their own video data. Currently supported base models:

| Base model | Type | Notes |
|---|---|---|
| `wan2.7-i2v` | first-frame image-to-video | Recommended, latest generation, highest quality |
| `wan2.5-i2v-preview` | first-frame image-to-video | Previous generation |
| `wan2.2-i2v-flash` | first-frame image-to-video | Lightweight and fast |
| `wan2.2-kf2v-flash` | first-and-last-frame image-to-video | Given the first frame + last frame, generates the intermediate transition video |

## Data format

Video generation data is a **ZIP package** (not .jsonl), containing an annotation file and media files.

### First-frame (i2v) dataset

```
i2v-dataset.zip
├── data.jsonl           # annotation file
├── image_1.jpeg         # first-frame image (flat)
├── video_1.mp4          # training target video
├── image_2.jpeg
└── video_2.mp4
```

Per-line JSONL format:
```json
{"prompt": "The video opens with...", "first_frame_path": "image_1.jpg", "video_path": "video_1.mp4"}
```

### First-and-last-frame (kf2v) dataset

```
kf2v-dataset.zip
├── data.jsonl
├── image/
│   ├── image_1_first.jpg
│   └── image_1_last.jpg
└── video/
    └── video_1.mp4
```

Per-line JSONL format:
```json
{"prompt": "The video opens with...", "first_frame_path": "image/image_1_first.jpg", "last_frame_path": "image/image_1_last.jpg", "video_path": "video/video_1.mp4"}
```

### Validation set (optional)

The validation set only needs first-frame images (kf2v needs first + last frames), **no videos**. During training, the system automatically generates preview videos at each eval step.

```json
{"prompt": "The video opens with...", "first_frame_path": "image_1.jpg"}
```

### Data requirements

- Image formats: BMP, JPEG, PNG, WEBP, resolution ≤ 4096×4096
- Video formats: MP4, MOV, resolution ≤ 4096×4096
- Video duration: 2-5 seconds recommended for wan2.2; 2-10 seconds for wan2.5/2.7
- File names support **English characters only** (ASCII)
- At least **10 samples** recommended (20-100 preferred)
- ZIP package ≤ 1GB
- Dataset schema is `video` (the CLI auto-detects it via the `first_frame_path`/`video_path` fields)

### Validation

Video ZIPs do **not** go through `bl dataset validate` (that command's `--schema` only supports chatml/dpo/cpt/tts/image). Just run `bl dataset upload --file <zip-path>`: the CLI auto-detects the video schema from the `first_frame_path`/`video_path` fields in `data.jsonl` and validates the file references inside the ZIP at upload time.

## Create a training job

```bash
bl finetune video create \
  --base-model wan2.7-i2v \
  --datasets <zip-path-or-file-id> \
  --output json
```

### Hyperparameter defaults (auto-adapted per model)

| Parameter | wan2.7 | wan2.5 | wan2.2 |
|---|---|---|---|
| `batch_size` | 1 | 4 | 4 |
| `max_pixels` | 102400 | 36864 | 262144 |
| `n_epochs` | 50 | 50 | 50 |
| `learning_rate` | 2e-5 | 2e-5 | 2e-5 |
| `eval_epochs` | 20 | 20 | 20 |
| `lora_rank` | 32 | 32 | 32 |
| `lora_alpha` | 32 | 32 | 32 |
| `split` | 0.5 | 0.5 | 0.5 |

Users can override the defaults via `--n-epochs`, `--batch-size`, and `--learning-rate`.

### Small-dataset caveat

With a small dataset (< 10 samples), the default `split=0.5` may leave the validation set ≤ batch_size and cause an error. Fixes:
- Use `--batch-size 1` to lower batch_size
- Or upload a separate validation set with `--validations <file-id>`

## Wait for training to finish

```bash
bl finetune watch --job-id <job_id> --follow
```

Video training usually takes **several hours**. When finished, it outputs `finetuned_output` (e.g. `wan2.7-i2v-ft-202608061949-48ca`) — this is the model name used for deployment.

## Deployment

```bash
bl deploy image create \
  --model-name <finetuned_output> \
  --display-name my-video-lora \
  --plan lora \
  --output json
```

Video LoRA deployment uses `plan=lora` (token-billed). The deployment reaches RUNNING in about 5-10 minutes.

```bash
bl deploy get --deployed-model <deployed_model>
```

## Inference and invocation

Once the deployment is RUNNING, invoke with `bl video generate`:

### First frame (i2v) — all versions

```bash
bl video generate \
  --model <deployed_model> \
  --image https://example.com/first_frame.png \
  --prompt "Description text" \
  --prompt-extend false
```

### First-and-last-frame (kf2v) — wan2.2-kf2v

```bash
bl video generate \
  --model <deployed_model> \
  --image https://example.com/first_frame.png \
  --last-frame https://example.com/last_frame.png \
  --prompt "Description text" \
  --prompt-extend false
```

`--last-frame` triggers kf2v mode, automatically switching to the `image2video/video-synthesis` endpoint.

### Key parameters

| Parameter | Notes |
|---|---|
| `--prompt-extend false` | Recommended to disable prompt rewriting for LoRA models |
| `--resolution 720P` | Output resolution (480P / 720P; wan2.7 supports 1080P) |
| `--download <path>` | Download the video locally |
| `--async` | Only return a task_id, do not wait |

## Prompt-writing guidance

Video fine-tuning prompt structure: `[subject description] + [background description] + [trigger word] + [motion description]`

- **Trigger word**: a meaningless rare token (e.g. `s86b5p`) that serves as the "visual anchor" of the effect
- **Consistency**: for all samples containing the same effect, keep the motion-description part identical
- **Diversity**: the richer the subjects and scenes, the better; avoid the model overfitting to a single background

## Billing

- **Training**: token-billed; check `usage_tokens` and `training_cost` with `bl finetune get --job-id <id>`
- **Deployment**: plan=lora is free (no idle billing)
- **Inference calls**: billed at the base model's standard price
