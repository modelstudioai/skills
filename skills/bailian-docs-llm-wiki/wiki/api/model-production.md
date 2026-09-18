# model production

`model production` 是百炼平台中模型从训练、优化、导入到部署上线的全生命周期管理能力集合，涵盖微调（Fine-tuning）、模型压缩、吞吐预留（PTU）、专属部署（MU/LORA）等核心环节。所有生产操作均通过统一 OpenAPI 接口驱动，支持文本、图像、视频、语音等多模态模型，但多数功能当前仅在华北2（北京）地域可用。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务，每类均有专用 API 和差异化超参体系。例如，文本生成支持 `sft`/`dpo_lora` 等训练类型，而视频生成当前仅支持 `efficient_sft` [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)；图像生成需指定 `generation_type`（`t2i` 或 `i2i`）[图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 全参调优模型进行量化压缩，不支持 LoRA 模型或已量化模型 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)。
- **模型导入**：支持将 OSS 中的全参（`full`）或 LoRA（`lora`）调优模型文件导入平台，导入成功后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **部署方式**：提供三种计费与资源模型：
  - `mu`（Model Unit）：按专属算力单元（如 `MU1`/`MU5`）计费，支持细粒度扩缩容与限流；
  - `lora`：LoRA 共享部署，按 Token 用量计费，适用于轻量级、多租户场景；
  - `ptu`（Pre-provisioned Throughput Unit）：按预置吞吐量（kTPM）计费，保障稳定推理性能。

> **注意**：文档中 `DTU 独占算力部署` 明确说明“暂不支持通过本组 API 创建与管理”，需在控制台操作，与 `mu`/`ptu` 的 API 驱动模式存在显著差异。

## 关键参数

| 参数 | 适用场景 | 说明 | 示例值 |
|--------|-----------|------|---------|
| `training_type` | 所有微调任务 | 训练方法，不同模态支持不同值：文本支持 `sft`/`dpo_lora`；图像/视频/语音当前仅支持 `efficient_sft` | `"efficient_sft"` |
| `plan` | 部署接口 | 必填，决定计费与资源模型 | `"mu"`, `"lora"`, `"ptu"` |
| `deploy_spec` | `plan=mu` 时必填 | 部署模板规格，约束 `capacity` 取值步长（如 `MU2` 要求 `capacity` 为 8 的倍数） | `"MU5"` |
| `ptu_capacity` | `plan=ptu` 时生效 | 吞吐容量配置，单位为 kTPM（1000 Tokens/分钟） | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `aigc_config` | 视频生成部署 | 提示词生成策略，含 `use_input_prompt`（是否启用用户传入 [prompt](../guides/prompt.md)）等字段 | `{"use_input_prompt": false, "prompt": "..."}` |

## 使用方式

1. **准备环境**：确保使用华北2（北京）地域的 API Key，并完成 RAM 权限配置（模型调用、训练、部署）[调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)。
2. **启动训练**：调用 `/api/v1/fine-tunes` 创建微调任务，传入 `model`、`training_type` 和 `hyper_parameters`（各模态必填项不同，详见对应文档）。
3. **监控与导出**：轮询 `/api/v1/fine-tunes/{job_id}` 查询状态；任务成功后，`output.finetuned_output` 即为可部署模型 ID；如需导出 Checkpoint，使用 `/api/v1/fine-tunes/{job_id}/checkpoints` [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)。
4. **部署服务**：调用 `/api/v1/deployments`，根据 `plan` 填写对应参数：
   - `mu`：必填 `deploy_spec`、`capacity`、`billing_method`；
   - `lora`：仅需 `model_name`、`plan`、`capacity`（推荐为 1）；
   - `ptu`：填写 `ptu_capacity`，`charge_type`（`pre_paid`/`post_paid`）及 `pre_paid_info`（预付费时）。
5. **验证与调用**：轮询 `/api/v1/deployments/{deployed_model}`，待 `status` 变为 `RUNNING` 后即可调用。

## 限制和注意事项

- **地域强绑定**：微调、部署、压缩、Checkpoint 管理等绝大多数 API **仅在华北2（北京）地域可用**，跨地域调用将失败。吞吐预留 API 虽支持多地域 Endpoint（如弗吉尼亚），但其模型与购买限制仍以目标地域为准。
- **HTTP 200 ≠ 操作成功**：吞吐预留等异步操作返回 HTTP 200 仅表示请求接收成功，实际状态需检查响应体中的 `output.operation_status` 字段，可能为 `FAILED` [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。
- **模型兼容性限制**：
  - 模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参模型；
  - CosyVoice 语音合成模型部署**仅支持 `mu` 方式**，不支持 `lora` 或 `ptu`；
  - 图像/视频生成部署推荐 `lora`，而语音合成必须用 `mu`。
- **资源与配额**：`capacity` 取值受 `deploy_spec` 严格约束（如 `MU2` 要求为 8 的倍数），且 `ptu` 的 `input_tpm`/`output_tpm` 需满足模型要求的步长与范围，不可任意设置。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)


