# model production

`model production` 是百炼平台中模型从训练、优化、导入到部署上线的全生命周期管理能力集合，覆盖微调（Fine-tuning）、模型压缩、自定义模型导入、专属部署及吞吐预留等核心环节。所有生产操作均通过统一 OpenAPI 接口提供，支持开发者在华北2（北京）地域完成端到端集成。关键能力围绕文本、图像、视频、语音四类生成式模型展开，但各模态在地域支持、部署方案和参数约束上存在显著差异，需严格按文档要求配置。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务，对应不同基准模型与训练范式：
  - 文本：`qwen3-14b`、`qwen3-32b` 等，支持 `sft`、`dpo_lora` 等训练类型；
  - 图像：`wan2.7-image-pro`、`qwen-image-2.0`，仅支持 `efficient_sft`；
  - 视频：`wan2.7-i2v`、`wan2.5-i2v-preview`，仅支持 `efficient_sft`；
  - 语音：`cosyvoice-v3-flash`，采用双网络（LM+FM）解耦训练。
  
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 的全参调优模型进行量化压缩，LoRA 模型不支持 [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)。

- **模型导入**：支持将 OSS 中存储的全参（`full`）或 LoRA（`lora`）调优模型导入平台，导入后可直接部署 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。

- **部署与吞吐预留**：提供三种部署模式：
  - `mu`（Model Unit）：资源专属，按实例时长计费，支持限流（`rpm_limit`/`tpm_limit`）与上下文扩展；
  - `lora`：共享推理资源，按 Token 用量计费，适用于 LoRA 微调模型；
  - `ptu`（Pre-reserved Throughput Unit）：预置吞吐容量，按输入/输出 TPM（Tokens Per Minute）购买，支持预付费与后付费 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)。

> **注意**：文档 16 与文档 19 对 `plan=lora` 的适用性描述存在矛盾——文档 16 明确 `lora` 仅适用于 LoRA 微调模型，而文档 19 却称“LoRA高效微调推荐为`lora`”，易被误解为所有图像模型均可选。实际应以模型类型为准：仅 LoRA 微调产出的图像模型（如 `wan2.7-image-pro-ft-xxx`）才支持 `lora` 部署；全参微调或基础模型必须使用 `mu`。

## 关键参数

| 参数 | 适用场景 | 必填 | 说明 |
|------|----------|------|------|
| `model_name` | 所有部署接口 | 是 | 非基础模型 ID，须为微调产出的 `finetuned_output`、导入任务的 `model_name` 或吞吐预留的 `deployed_model` |
| `plan` | 部署接口 | 是 | 取值 `mu`/`lora`/`ptu`；`mu` 需配 `deploy_spec` 和 `capacity`；`ptu` 需配 `ptu_capacity` |
| `ptu_capacity.input_tpm` / `output_tpm` | 吞吐预留 | 是 | 单位为 kTPM（1000 Tokens/分钟），非绝对 Token 数；扩缩容时传入目标绝对值，非增量 [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md) |
| `deploy_spec` | `mu` 部署 | 条件必填 | 如 `MU1`、`MU5`，决定硬件规格与 `capacity` 倍数约束（如 `MU2` 要求 `capacity` 为 8 的倍数） |
| `aigc_config` | 视频部署 | 必填 | 包含 `use_input_prompt`、`prompt`、`lora_prompt_default`，控制提示词生成逻辑，不可省略 [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md) |

## 使用方式

1. **准备环境**：仅华北2（北京）地域支持全部生产 API，必须使用该地域的 API Key，并配置 `Authorization: Bearer <key>` 与 `Content-Type: application/json`。
2. **训练/导入模型**：
   - 微调：调用 `/api/v1/fine-tunes` 创建任务，轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，提取 `finetuned_output`；
   - 导入：调用 `/api/v1/custom_models/import` 提交 OSS 路径，轮询 `/api/v1/custom_models/import/{job_id}` 直至 `status=SUCCESSED`，提取 `model_name`。
3. **部署服务**：
   - `mu`/`lora`：`POST /api/v1/deployments`，传入 `model_name` 与对应 `plan` 参数；
   - `ptu`：`POST /api/v1/deployments`，传入 `model_name`、`plan=ptu` 与 `ptu_capacity` 对象。
4. **验证状态**：调用 `GET /api/v1/deployments/{deployed_model}` 轮询，`status=RUNNING` 表示就绪。

> **注意**：文档 1 和文档 16 均使用 `/api/v1/deployments` 路径，但语义不同——文档 1（吞吐预留）中该路径用于创建 `ptu` 预留并返回 `deployed_model`（即 ModelCode）；文档 16（通用部署）中同路径用于创建 `mu`/`lora` 实例并返回 `deployed_model`。二者请求体结构与必填字段完全不同，开发者需根据 `plan` 值严格区分，不可混用。

## 限制和注意事项

- **地域强绑定**：所有微调、导入、压缩、部署 API（除吞吐预留外）**仅在北京地域可用**；吞吐预留 API 支持多地域，但需使用对应地域的 Endpoint 与 API Key。
- **模型兼容性**：
  - `ptu` 部署仅支持部分基础模型（如 `qwen-plus`），不支持自定义微调模型；
  - `lora` 部署仅支持 LoRA 微调产出的模型，全参微调模型必须用 `mu`；
  - 模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参微调模型，且产出模型部署时仍需指定 `mu` 方案。
- **状态检查**：HTTP 200 不代表操作成功。吞吐预留创建响应中需检查 `output.operation_status`；部署响应中需轮询 `GET /deployments/{id}` 确认 `status=RUNNING`；微调任务需检查 `output.status=SUCCEEDED`。
- **命名与唯一性**：部署时若需多次发布同一模型，必须设置 `suffix` 参数（最多 8 位小写字母/数字），否则因 ModelCode 冲突导致失败。

## 来源文档

- [吞吐预留 API参考](../../raw/model-api-reference/model-production/throughput-reservation-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/_short/model-compression-api-09615482a618bd21.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [视频生成-创建调优任务](../../raw/_short/video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/_short/voice-synthesis-create-fine-tuning-job-api-0ff3893c65aef5a2.md)
- [图像生成-创建调优任务](../../raw/_short/image-generation-create-fine-tuning-job-api-ae5bdcbb493e7a3e.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/_short/image-generation-deploy-model-api-5319791597a105b6.md)
- [视频生成-部署模型](../../raw/_short/video-generation-deploy-model-api-83485cc2bfb54b4c.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)


