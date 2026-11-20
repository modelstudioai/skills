# Deployment Parameter Reference

> This file supplements Step 5 "Create the deployment" in [`SKILL.md`](../SKILL.md) with `--plan` options, the `--model-name` ambiguity, and billing/ops details. For flow orchestration and pitfall avoidance see SKILL.md.

## --plan options (vary by model source)

Available plans **vary by model source — do not blindly use `lora`**:

| Model source | Available plans | Notes |
|---|---|---|
| Link A text fine-tuned output | `lora` (default) / `mu` | `lora` is token-billed, good for validation/low load |
| Link A audio TTS fine-tuned output | `mu` (**only**) | `lora` / `ptu` not supported |
| Link A image generation fine-tuned output | `lora` (**only**) | `mu` / `ptu` not supported |
| Link B (base model, e.g. `qwen3-8b`) | `ptu` / `mu`, **no `lora`** | `ptu` reserves throughput; `mu` is an exclusive resource |

Required parameters per plan:

- `lora`: no extra required parameters, token-billed, idle usually not billed (safe default).
- `ptu`: requires `--input-tpm` / `--output-tpm` (reserved throughput; bills even when idle).
- `mu`: requires `--deploy-spec` / `--capacity` (exclusive resource; bills even when idle); if `--deploy-spec` is omitted, it is auto-fetched from `bl deploy models`.

Not sure which plans are supported: Link A uses `bl deploy models --source custom`, Link B uses `bl deploy models --source base`; pick from the returned `plans`.

## --deploy-spec (mu plan only)

`--deploy-spec <spec-id>` specifies the deployment spec (e.g. `dps-20260521172224-1vabse`, `MU2`). If omitted, the CLI automatically queries `bl deploy models` and matches a suitable spec by `billing_method` (default POST_PAY).

> Internal mechanism: the CLI reads the `template_id` field from the template object in the `GET /deployments/models` response and sends it as `deploy_spec` in the POST request body. The CLI flag is `--deploy-spec`; do not pass `--template-id`.

## --source values (`bl deploy models`)

`custom` (fine-tuned output) / `base` (base model) / `public`.

## --model-name vs inference --model mean different things (most frequent error; never mix them up)

- `bl deploy <modality> create --model-name` takes the **exported model name** (`qwen3-8b-ft-...`, from `finetuned_output` in Step 2 for Link A; the base model name `qwen3-8b` directly for Link B).
- `output.deployed_model` in the response (e.g. `qwen3-8b-b98a331831a7`) is the **deployment instance id**.
- The next-step inference command (`bl text chat` / `bl speech synthesize` / async API) must use `deployed_model` from the response for `--model`, **not** the name you passed to `deploy <modality> create --model-name`. `--model-name` and inference `--model` point to different values — do not reuse them.

## Billing and ops details

- **Idle billing**: `lora` is token-billed and usually not billed when idle, so keeping it is harmless; `mu` / `ptu` are reserved resources that bill even when idle — clean them up promptly if unused.
- **Deletion constraint**: `bl deploy delete` can only delete deployments in `STOPPED` / `FAILED` status. For `RUNNING` deployments, first disable with `bl deploy pause --deployed-model <id>` (stops billing for mu/ptu), then delete; or try `bl deploy delete --deployed-model <id> --skip-precheck` (skips the local pre-check, but the server may still refuse to delete a RUNNING deployment). After pausing, restore service with `bl deploy resume --deployed-model <id>`.
- **Status-propagation delay**: calling immediately after a deployment first reaches `RUNNING` may briefly return 404 `Model not exist`; this is server-side state-propagation delay that stabilizes within about a minute — on 404, wait a dozen seconds and retry; if 404 persists, first verify you are using `deployed_model` rather than the fine-tuned output name.

## Required flags (`bl deploy <modality> create`)

- `--model-name`: the exported model name (see the ambiguity notes above).
- `--display-name`: the display name in the console.
