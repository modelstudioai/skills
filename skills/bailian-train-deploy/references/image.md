# Image Generation Model Reference

> This file supplements [`SKILL.md`](../SKILL.md) with the modality-specific details of the image generation fine-tuning pipeline (data format, models, hyperparameters, inference). See SKILL.md for the generic flow.

## Applicable scenarios

The user wants to fine-tune an image generation model, training a custom style or a scenario-specific text-to-image/image-to-image model from their own image data. Currently supported base models:

| Base model | Notes |
|---|---|
| `wan2.7-image-pro` | Wan2.7 image generation Pro edition, higher quality |
| `wan2.7-image` | Wan2.7 image generation standard edition, faster |

## Data format

Image generation data is a **ZIP package** (not .jsonl), containing:

```
data.zip
├── data.jsonl           # annotation file
├── img_001.png          # image files (flat, no subdirectories)
├── img_002.jpg
└── ...
```

**T2I (text-to-image)** per-line JSONL format:
```json
{"prompt": "A beautiful landscape", "img_path": "./img_001.png"}
```

**I2I (image-to-image)** per-line JSONL format:
```json
{"prompt": "Transform this scene", "input_img": "./in_001.jpg", "img_path": "./out_001.jpg"}
```

Requirements:
- Image formats: BMP, JPEG, PNG, WEBP
- Each image ≤ 20MB, resolution ≤ 4096×4096
- File names support **English characters only** (ASCII)
- **Files must be laid out flat**; subdirectories are forbidden (unlike the audio TTS `train/` structure)
- At least **25 images** recommended (50+ preferred)
- ZIP package ≤ 1GB (vs 300MB for text/audio)
- Dataset schema is `image` (the CLI auto-detects it via the `img_path` field)

### Validation

```bash
bl dataset validate --file <zip-path>               # auto-detect image schema
bl dataset validate --file <zip-path> --schema image  # explicit
```

Validation covers: ZIP structure (data.jsonl exists, ≥25 images, valid file references, flat layout) + JSONL content (image schema: every line must have prompt + img_path; I2I may include input_img).

## Create a training job

```bash
bl finetune image create \
  --base-model wan2.7-image-pro \
  --datasets <zip-path-or-file-id> \
  --output json
```

I2I (image-to-image) mode is **auto-detected** — as soon as the JSONL contains the `input_img` field, the CLI automatically recognizes it as I2I and adjusts hyperparameters (`max_pixels`/`val_img_size` switch from "2k" to "1k"); no extra flag needed:

```bash
bl finetune image create \
  --base-model wan2.7-image-pro \
  --datasets <i2i-zip-path-or-file-id> \
  --output json
```

Key points:
- Image fine-tuning is fixed to `sft-lora` (mapped to `efficient_sft`) — `finetune image create` **does not expose `--training-type`**; there is no need and no way to pass it; full-parameter sft / dpo / cpt are not supported
- **No manual hyperparameters needed** — the 12 image-specific hyperparameters are auto-injected with default values
- T2I/I2I is auto-inferred from the data content (first row has `input_img` → I2I, otherwise T2I), and `max_pixels`/`val_img_size` adjust automatically
- Text hyperparameters such as `--n-epochs` / `--batch-size` have no effect on image — do not pass them
- The capability check may show `supports.sft=false`; this is a known contradiction and the CLI already skips it automatically

Record from the response: `output.job_id`, `output.finetuned_output` (shaped like `wan2.7-image-pro-ft-<ts>-<id>`).

## Expected training duration

Image training duration depends on `max_steps` (default 800 steps). Actual duration depends on GPU resources and image resolution (`max_pixels`).

## Deployment

```bash
bl deploy image create \
  --model-name <finetuned_output> \
  --display-name <display-name> \
  --plan lora \
  --capacity 1 \
  --output json
```

Key points:
- Image generation fine-tuned models **only support the `lora` plan** (not `mu` / `ptu`)
- `--capacity`: default 1
- No `--deploy-spec` needed (the lora plan does not require a deployment spec)

## Inference and invocation

Image generation is an **async invocation** (not `text chat` or `speech synthesize`):

```bash
# Submit the generation task asynchronously
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'X-DashScope-Async: enable' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "<DEPLOYED_MODEL>",
    "input": {
      "prompt": "s86b5p a cat sitting on a sofa"
    },
    "parameters": {
      "size": "1024*1024",
      "n": 1
    }
  }'
```

Key points:
- `model` must be the `deployed_model` from the `deploy image create` response, **not** `finetuned_output`
- The request must carry the `X-DashScope-Async: enable` header (async mode)
- The `prompt` **must contain the trigger word** (communicated by the platform after training completes, shaped like `s86b5p`)
- It returns a `task_id`; poll for the result
- Generated image URLs are valid for **24 hours**

### Polling for results

```bash
# Query the result with the returned task_id
curl -X GET "https://dashscope.aliyuncs.com/api/v1/tasks/<task_id>" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Status transitions: `PENDING` → `RUNNING` → `SUCCEEDED` (contains the image URL)

## Known limitations

- Only the Beijing region is supported
- File names support English characters only (ASCII)
- The prompt must contain the trigger word assigned during training
- Image URLs expire after 24 hours
- The capability API returns `supports.sft=false` for the wan2.7 series, but the API actually accepts training — the CLI already skips this check automatically
- Image models cannot be deployed with the `mu` / `ptu` plans
