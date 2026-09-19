# model production

model production 指在百炼平台上完成模型的微调（Fine-tuning）、压缩、导入、部署及吞吐预留等全生命周期操作，将原始模型转化为可稳定、高效、规模化调用的生产级服务。该流程覆盖从训练任务创建、Checkpoint 管理、模型资产入库，到推理服务发布与容量保障的完整链路，所有核心能力均通过统一 OpenAPI 接口提供，支持开发者自动化集成。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类模态。各类型对应不同基准模型与训练范式：文本生成支持 `cpt`/`sft`/`dpo_full` 等多种训练方式；图像/视频/语音生成当前仅支持 `efficient_sft`（LoRA 高效微调）[文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参微调模型进行量化压缩，产出低显存、高吞吐的量化模型，不支持 LoRA 模型或已量化模型 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)。
- **模型导入**：支持从 OSS 导入全参（`full`）或 LoRA（`lora`）调优模型文件，完成结构校验后即可部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/custom-models-api.md)。
- **部署与吞吐预留**：提供三种部署模式：`mu`（模型单元，资源专属）、`lora`（LoRA 共享，按 [Token](../concepts/token.md) 计费）、`ptu`（预置吞吐量，按 kTPM 保底）；其中 `ptu` 即吞吐预留，用于保障稳定高并发推理能力 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：所有微调与部署 API（除吞吐预留外）目前**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key。跨地域调用将失败，此限制在多篇文档中反复强调（如[图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)、[语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)），无例外说明。

## 关键参数

| 参数 | 所属功能 | 说明 | 示例值 |
|--------|-----------|------|---------|
| `model_name` | 微调、部署、导入 | 基础模型 ID（微调输入）或微调/导入产出的模型 ID（部署输入）。部署时必须使用 `finetuned_output` 或 `model_name` 字段值，而非原始基础模型名 | `qwen3-14b`, `wan2.7-image-pro-ft-202507011122-xxxx` |
| `plan` | 部署 | 部署方案，决定计费与资源模型：`mu`（专属）、`lora`（共享）、`ptu`（吞吐预留） | `"mu"`, `"lora"`, `"ptu"` |
| `deploy_spec` / `capacity` | `mu` 部署 | `deploy_spec`（如 `"MU1"`）指定硬件规格；`capacity` 为该规格下的实例数量，需满足 `base_capacity` 的整数倍约束 | `"MU5"`, `1` |
| `ptu_capacity` | `ptu` 部署 | 吞吐预留容量配置对象，含 `input_tpm`（输入 kTPM）和 `output_tpm`（输出 kTPM），单位为千 [Token](../concepts/token.md)/分钟 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `aigc_config` | 视频/图像部署 | 提示词控制配置，含 `use_input_prompt`（是否启用用户传入 [prompt](../guides/prompt.md)）、`prompt`（自动生成模板）、`lora_prompt_default`（兜底模板） | `{ "use_input_prompt": false, "prompt": "根据图像内容..." }` |

## 使用方式

1. **微调训练**：调用 `/api/v1/fine-tunes` 创建任务，指定 `model`、`training_type` 和 `hyper_parameters`（如 `n_epochs`、`batch_size`）。任务成功后，`output.finetuned_output` 即为可部署模型 ID [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)。
2. **模型导入**：调用 `/api/v1/custom_models/import`，提供 `model_name`、`weight_type`（`full`/`lora`）及 `storage_info`（OSS bucket + object key）。
3. **模型部署**：
   - `lora` 模式：`POST /api/v1/deployments`，传 `model_name` + `"plan": "lora"` + `capacity`（通常为 `1`）；
   - `mu` 模式：同上，但需额外指定 `deploy_spec`、`capacity`、`billing_method`；
   - `ptu` 模式（吞吐预留）：同上，但 `plan` 设为 `"ptu"`，并传入 `ptu_capacity` 对象。
4. **吞吐预留管理**：独立于通用部署，使用 `/api/v1/deployments`（同一路径，但语义为“预留”），支持创建、查询、扩缩容、续订等操作，返回 `deployed_model` 作为调用标识。
5. **状态轮询**：所有[异步任务](../concepts/asynchronous-task.md)（微调、导入、部署、压缩）均需轮询对应 GET 接口（如 `/api/v1/fine-tunes/{job_id}`、`/api/v1/deployments/{deployed_model}`）直至 `status` 变为 `SUCCEEDED` 或 `RUNNING`。

## 限制和注意事项

- **地域强绑定**：微调、部署、导入、Checkpoint 管理等全部 API 仅在北京地域可用，吞吐预留 API 则支持多地域（含弗吉尼亚），但需使用对应地域的 Endpoint 和 API Key [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步接口即使返回 HTTP 200，其 `output.operation_status` 仍可能为 `FAILED`，**必须检查响应体中的状态字段**，不可仅依赖 HTTP 状态码 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性限制**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型；语音合成（CosyVoice）部署仅支持 `mu` 方案，不支持 `lora` 或 `ptu`；图像/视频部署推荐 `lora` 方案，而 `mu` 方案未在对应文档中明确支持。
- **命名与唯一性**：部署时若需多次部署同一模型，必须设置 `suffix` 参数以确保 `deployed_model` 全局唯一；模型导入的 `display_name` 最多 50 字符；压缩产出的 `output_model_suffix` 最多 8 字符且仅限小写字母与数字。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)


