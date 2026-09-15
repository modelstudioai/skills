# model production

`model production` 指在百炼平台将训练/调优后的模型转化为可稳定、可扩展、可计费的在线推理服务的完整流程，涵盖模型微调（Fine-tuning）、模型导入（Import）、模型压缩（Quantization）和[模型部署](../concepts/model-deployment.md)（Deployment）四大核心环节。该流程支持文本、图像、视频、语音等多模态模型，并提供 PTU（预置吞吐量）、MU（模型单元）和 LoRA 共享部署等多种生产化方案。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持文本生成（[文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)）、图像生成（[图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)）、视频生成（[视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)）和语音合成（[语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)）四类任务，均**仅限华北2（北京）地域**使用对应地域的 API Key。
- **模型导入**：支持将 OSS 中存储的全参或 LoRA 调优模型文件导入平台（[模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)），导入后可直接部署。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 基础模型的全参调优产出进行量化压缩（[模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)），不支持 LoRA 模型或已量化模型。
- **[模型部署](../concepts/model-deployment.md)**：支持将微调产出、导入模型或压缩模型发布为在线 API 服务，覆盖文本（[文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)）、图像（[图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)）、视频（[视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)）和语音（[语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)）全场景，**所有部署接口均仅在华北2（北京）地域开放**。

> **注意**：文档 15（`model-deployment-api.md`）称“[模型部署](../concepts/model-deployment.md)”为通用能力，但其子文档（16、18、21、23）及文档 22（`get-deployment-api.md`）均明确限定“仅在华北2（北京）地域可用”，且文档 1 的 TPM 预留接口（`tpm-reserved-openapi.md`）未限定地域，说明 PTU 部署是跨地域的，而 MU/LoRA 部署目前仅限北京。此为地域能力差异，非矛盾。

## 关键参数

| 参数 | 适用场景 | 必填性 | 说明 |
|--------|-----------|---------|------|
| `model_name` | 所有微调与部署请求 | 是 | 微调时为基准模型 ID（如 `qwen3-14b`）；部署时为微调产出 ID（如 `qwen3-14b-ft-xxx`）或导入模型名。 |
| `plan` | 部署请求 | 是 | `mu`（专属资源）、`lora`（共享推理）、`ptu`（预置吞吐量）。不同模型类型支持不同 plan（如 CosyVoice 仅支持 `mu`，图像微调推荐 `lora`）。 |
| `deploy_spec` | `plan=mu` 时 | 是 | 指定硬件规格模板（如 `MU1`, `MU5`），决定 `capacity` 的倍数约束（如 `MU2` 要求 `capacity` 为 8 的倍数）。 |
| `capacity` | `plan=mu` 或 `plan=lora` 时 | 是 | `mu` 下为模型单元数量；`lora` 下为实例数量（通常为 1）。 |
| `ptu_capacity` | `plan=ptu` 时 | 否（默认 `input_tpm=10000`, `output_tpm=1000`） | 对象，含 `input_tpm` 和 `output_tpm`（单位：kTPM），表示每分钟最大输入/输出 Token 量。 |
| `aigc_config` | 视频部署（`plan=lora`） | 是 | 包含 `use_input_prompt`, `prompt`, `lora_prompt_default`，用于控制提示词生成逻辑（[视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)）。 |

## 使用方式

1. **准备环境**：获取并配置华北2（北京）地域的 API Key（[获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md)），确保子账号已授予 `AliyunBailianFullAccess` 或最小必要权限。
2. **训练/准备模型**：
   - 微调：调用 `/api/v1/fine-tunes` 创建任务，轮询 `/api/v1/fine-tunes/{job_id}` 确认 `status=SUCCEEDED`，从 `output.finetuned_output` 获取模型 ID。
   - 导入：调用 `/api/v1/custom_models/import` 提交 OSS 模型路径，轮询状态至 `SUCCESSED`，从 `output.model_name` 获取模型 ID。
   - 压缩：先确保有 `qwen3.5-flash-2026-02-23` 全参调优模型，再调用 `/api/v1/fine-tunes/compress/jobs`，成功后取 `output.quantized_output`。
3. **部署模型**：向 `/api/v1/deployments` 发送 POST 请求，按 `plan` 类型填充对应参数（`deploy_spec`+`capacity` for `mu`；`capacity` for `lora`；`ptu_capacity` for `ptu`）。
4. **验证服务**：调用 `/api/v1/deployments/{deployed_model}` 查询状态，待 `status=RUNNING` 后即可通过 `deployed_model` 调用推理 API。

## 限制和注意事项

- **地域限制**：所有微调（Fine-tuning）、模型导入（Custom Models）、模型压缩（Compression）及 MU/LoRA 部署（Deployments）API **仅支持华北2（北京）地域**；TPM 预留（PTU）部署则支持多地域（见 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)）。
- **HTTP 成功 ≠ 操作成功**：所有异步操作（创建、扩缩容、部署）返回 HTTP 200 仅表示请求被接收，必须检查响应体中 `output.operation_status` 或 `output.status` 字段（如 `FAILED`, `SUCCEEDED`），否则可能调用未就绪服务。
- **容量单位**：TPM 预留中 `ptu_capacity` 单位为 kTPM（1000 Tokens/分钟），非原始 TPM；`rpm_limit`/`tpm_limit` 在 MU 部署中为硬性限流阈值，超限请求将被拒绝。
- **模型兼容性**：模型压缩仅支持 `qwen3.5-flash-2026-02-23` 全参调优模型；CosyVoice 部署强制要求 `plan=mu`；视频部署 `aigc_config.prompt` 会完全覆盖用户调用时传入的 [prompt](../guides/prompt.md)，需谨慎设计模板。

## 来源文档

- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [Checkpoint 管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)


