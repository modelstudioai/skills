# model production

`model production` 是百炼平台面向模型全生命周期的生产级能力集合，覆盖模型微调、压缩、导入、部署及吞吐预留等关键环节。所有能力均通过统一 OpenAPI 接口提供，支持开发者在生产环境中构建、验证和规模化交付定制化模型服务。核心流程为：训练（fine-tuning）→ 产出模型 → （可选）压缩/导入 → 部署（deployment）→ （可选）吞吐预留（throughput reservation）。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务，每类均有专用 API 和差异化超参数体系。例如，文本生成支持 `sft`/`dpo_full` 等多种训练类型，而图像生成当前仅支持 `efficient_sft` [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)；视频生成则需按首帧/首尾帧模式选择对应基准模型 [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型进行量化压缩，LoRA 模型不支持 [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)。
- **模型导入**：支持从 OSS 导入全参（`full`）或 LoRA（`lora`）调优模型，导入后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型部署**：支持 `mu`（模型单元）、`lora`（LoRA 共享）、`ptu`（预置吞吐）三种部署方案，适配不同性能、成本与隔离性需求。
- **吞吐预留**：提供独立于部署的容量预留能力，用于保障高优先级推理请求的确定性延迟与吞吐，与部署解耦 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：所有微调与部署 API 均**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key。其他地域用户需通过控制台操作或切换地域接入点，此限制在[调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)、[文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)等多份文档中反复强调，属强约束而非建议。

## 关键参数

| 参数 | 所属场景 | 说明 | 示例值 |
|------|----------|------|--------|
| `model_name` | 微调、部署、导入 | 基础模型 ID（微调输入）或调优产出模型 ID（部署/导入输入）。部署时必须为已成功训练（`status=SUCCEEDED`）的模型 ID。 | `qwen3-14b`, `wan2.7-image-pro-ft-202507011122-xxxx` |
| `plan` | 部署 | 部署方案。`mu`（专属资源）、`lora`（共享资源）、`ptu`（吞吐预留绑定）。语音合成模型强制要求 `mu` [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)。 | `"mu"`, `"lora"`, `"ptu"` |
| `ptu_capacity` | 吞吐预留 / PTU 部署 | 吞吐容量配置对象，单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟）。`input_tpm` 和 `output_tpm` 为必填绝对值，非增量。 | `{ "input_tpm": 10000, "output_tpm": 1000 }` |
| `deploy_spec` & `capacity` | MU 部署 | `deploy_spec`（如 `MU1`, `MU5`）定义硬件规格，`capacity` 必须为其 `base_capacity` 的整数倍（如 `MU2` 要求 `capacity` 为 8 的倍数） [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。 | `"MU5"`, `1` |
| `aigc_config` | 视频/图像部署 | 图像/视频生成模型部署时必需的提示词模板配置，控制生成逻辑是否依赖输入 [prompt](../guides/prompt.md) 或强制使用预设模板 [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)。 | `{ "use_input_prompt": false, "prompt": "..." }` |

## 使用方式

1. **微调**：调用 `/api/v1/fine-tunes` 创建任务，传入 `model`、`training_type` 及领域特定超参数（如文本的 `n_epochs`、图像的 `max_pixels`、语音的 `lm_max_epoch`）。任务状态需轮询 `/api/v1/fine-tunes/{job_id}` 查询，`status=SUCCEEDED` 后获取 `finetuned_output`。
2. **导入/压缩**：若模型来自外部，调用 `/api/v1/custom_models/import` 导入 OSS 模型；若需压缩，先查模板 `/api/v1/fine-tunes/compress/templates`，再创建压缩任务 `/api/v1/fine-tunes/compress/jobs`，成功后获取 `quantized_output`。
3. **部署**：调用 `/api/v1/deployments`，根据 `plan` 选择参数：
   - `mu`: 必填 `deploy_spec`, `capacity`, `billing_method`
   - `lora`: 必填 `capacity`（通常为 `1`）
   - `ptu`: 可选 `ptu_capacity`，否则使用默认值（10k input / 1k output）
4. **吞吐预留**：独立于部署，调用 `/api/v1/deployments`（同部署路径，但语义为预留），指定 `model_name`, `plan=ptu`, `ptu_capacity`, `charge_type`（`pre_paid`/`post_paid`）。
5. **验证与调用**：部署后轮询 `/api/v1/deployments/{deployed_model}`，待 `status=RUNNING` 即可使用 `deployed_model` 作为 ModelCode 调用推理 API。

## 限制和注意事项

- **地域强绑定**：微调、部署、导入、压缩、Checkpoint 管理等全部 API 仅支持华北2（北京）地域，跨地域调用将失败。吞吐预留 API 虽支持多地域（如弗吉尼亚），但其 `model_name` 必须与目标地域可用模型一致 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求被接收，实际结果需检查响应体中的 `output.operation_status` 字段，可能为 `FAILED` [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性**：`ptu` 部署方案与吞吐预留共享 `ptu_capacity` 语义，但 `ptu` 部署本身不创建预留实例；`ptu` 预留的 ModelCode 可直接用于推理调用，无需额外部署。
- **资源约束**：`MU2` 部署的 `capacity` 必须为 8 的倍数，`MU5` 可为 1 的倍数；`ptu_default` 标速支持 8 小时时段预付费，`ptu_fast` 高速不支持 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **权限与配置**：所有 API 调用均需正确配置 `Authorization: Bearer <api-key>` 及 `Content-Type: application/json`，子账号需授予 `model:Invoke`, `model:Train`, `model:Deploy` 等细粒度权限 [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)


