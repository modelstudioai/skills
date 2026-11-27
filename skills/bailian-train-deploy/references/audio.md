# Audio TTS Model Reference

> This file supplements [`SKILL.md`](../SKILL.md) with the modality-specific details of the audio TTS fine-tuning pipeline (data format, models, hyperparameters, inference). See SKILL.md for the generic flow.

## Applicable scenarios

The user wants to fine-tune a speech synthesis (TTS) model, training a custom voice from their own voice data. Currently supported base model:

| Base model | Notes |
|---|---|
| `cosyvoice-v3-flash` | CosyVoice v3 Flash, Chinese/multilingual TTS, lightweight and fast |

## Data format

Audio TTS data is a **ZIP package** (not .jsonl), containing:

```
data.zip
├── data.jsonl           # annotation file, one {"wav_fn": "train/xxx.wav", "text": "the corresponding text"} per line
└── train/
    ├── sample_001.wav   # audio files
    ├── sample_002.wav
    └── ...
```

Requirements:
- Audio format `.wav`, sample rate ≥ 16kHz, duration 2-30s
- `wav_fn` paths in `data.jsonl` must point to files under the `train/` subdirectory
- Dataset schema is `tts` (the CLI auto-detects it via the `wav_fn` field)

### Validation

```bash
bl dataset validate --file <zip-path>             # auto-detect tts schema
bl dataset validate --file <zip-path> --schema tts  # explicit
```

Validation covers: ZIP structure (data.jsonl exists, train/ directory, valid wav references) + JSONL content (tts schema: every line must have wav_fn + text).

### Generate sample data

If the user has no ready-made data, use `edge-tts` (a Python library) to generate Chinese speech-synthesis test data:

```bash
pip install edge-tts
```

Script idea: synthesize mp3 with the `zh-CN-XiaoxiaoNeural` voice → convert to 16kHz mono wav with ffmpeg → package the ZIP. Quality is limited (a synthetic voice fine-tuned on synthetic voice); only for walking the flow through.

## Create a training job

```bash
bl finetune audio create \
  --base-model cosyvoice-v3-flash \
  --datasets <zip-path-or-file-id> \
  --output json
```

Key points:
- Audio fine-tuning is fixed to `sft-lora` (mapped to `efficient_sft`) — `finetune audio create` **does not expose `--training-type`**; there is no need and no way to pass it; full-parameter sft / dpo / cpt are not supported
- **No manual hyperparameters needed** — the 8 audio-specific hyperparameters (lm_max_epoch, fm_max_epoch, etc.) are auto-injected with default values by the CLI
- Text hyperparameters such as `--n-epochs` / `--learning-rate` / `--batch-size` have no effect on audio — do not pass them
- The capability check may show `supports.sft=false`; this is a known contradiction (API metadata inconsistent with actual behavior) and the CLI already skips it automatically

Record from the response: `output.job_id`, `output.finetuned_output` (shaped like `cosyvoice-v3-flash-ft-<ts>-<id>`).

## Expected training duration

Audio TTS training is significantly slower than text SFT. 10 cosyvoice-v3-flash samples (3 epochs) take about 2.5 hours. Duration grows linearly with sample count.

## Deployment

```bash
bl deploy audio create \
  --model-name <finetuned_output> \
  --display-name <display-name> \
  --plan mu \
  --deploy-spec <spec-id> \
  --capacity 1 \
  --output json \
  --yes
```

- `--yes` is required (high-risk command): preview with `--dry-run` first, then add `--yes` only after the user confirms

Key points:
- Audio TTS fine-tuned models **only support the `mu` plan** (not `lora` / `ptu`)
- `--deploy-spec`: look up available specs with `bl deploy models --source custom`; common values such as `dps-20260521172224-1vabse` (single-node deployment on MU5)
- `--capacity`: default 1
- Deployment takes about 6 minutes to go from PENDING to RUNNING

## Inference and invocation

Audio TTS uses `bl speech synthesize` (not `text chat`):

```bash
bl speech synthesize \
  --model <DEPLOYED_MODEL> \
  --voice default \
  --text "The text to synthesize" \
  --out result.mp3
```

Key points:
- `--model` must be the `deployed_model` from the `deploy audio create` response (e.g. `cosyvoice-v3-flash-9d4f3eeb27ca`), **not** `finetuned_output`
- `--voice` must be `default` (the fine-tuned model has only this one voice)
- The output is an audio file (mp3/wav/pcm/opus); specify with `--format`
- Inference returns within seconds

### Available parameters

`--format` (mp3/pcm/wav/opus), `--sample-rate` (e.g. 24000), `--volume` (0-100), `--rate` (0.5-2.0), `--pitch` (0.5-2.0), `--seed` (reproducible), `--language` (zh/en, etc.).

## Known limitations

- Only the Beijing region is supported
- Voice is fixed to `default`
- The capability API returns `supports.sft=false` for cosyvoice-v3-flash, but the API actually accepts training — the CLI already skips this check automatically
- Audio models cannot be deployed with the `lora` / `ptu` plans
