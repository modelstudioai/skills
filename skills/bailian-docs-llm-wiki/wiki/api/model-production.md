# model production

`model production` 指在百炼平台上完成模型的微调训练、压缩优化、导入部署及高性能推理服务的全生命周期管理。该流程覆盖文本、图像、视频、语音等多模态模型，支持从定制化训练到生产级服务发布的完整链路，核心能力包括 Fine-tuning、Model Import、Model Compression 和 Deployment。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持文本生成、图像生成、视频生成、语音合成（CosyVoice）四类任务。文本生成支持 `cpt`/`sft`/`dpo_full` 等多种训练类型；图像与视频生成当前仅支持 `efficient_sft`（LoRA）；语音合成要求 `cosyvoice-v3-flash` 基准模型 [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)。
- **模型导入**：支持将 OSS 中存储的全参（`full`）或 LoRA（`lora`）调优模型文件导入平台，导入后可部署为服务 [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)。
- **模型压缩**：当前仅支持对 `qwen3.5-flash-2026-02-23` 的自定义全参调优模型进行量化压缩，不支持 LoRA 或已量化模型 [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)。
- **部署方式**：提供三种计费与资源模型：
  - `mu`（Model Unit）：专属资源、可调规格（如 `MU1`/`MU5`）、支持限流与扩缩容；
  - `lora`：共享资源、按 [Token](../concepts/token.md) 用量计费、低延迟高性价比；
  - `ptu`（Pre-provisioned Throughput Unit）：预置吞吐量，按输入/输出 TPM 预留容量。

> **注意**：所有微调与部署 API 当前**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key。其他地域用户需通过控制台操作，详见各文档适用范围说明 [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)。

## 关键参数

| 功能 | 必填参数 | 说明 |
|------|----------|------|
| **微调创建** | `model`, `training_type`, `hyper_parameters` | `hyper_parameters` 中必填项因模型而异：文本需 `n_epochs`/`batch_size`/`max_length`；图像需 `max_steps`/`learning_rate`/`generation_type`；视频需 `n_epochs`/`batch_size`/`learning_rate`；语音需 `lm_max_epoch`/`fm_max_epoch` 等双网络参数。 |
| **模型导入** | `model_name`, `weight_type`, `source`, `storage_info` | `weight_type` 必须为 `full` 或 `lora`；`storage_info` 包含 `bucket_name` 和 `object_key`（路径需以 `/` 结尾）。 |
| **部署创建** | `model_name`, `plan`, `capacity`（`mu`/`lora`）或 `ptu_capacity`（`ptu`） | `plan=mu` 时还需 `deploy_spec` 和 `billing_method`；`plan=lora` 时 `capacity` 固定为 1；`plan=ptu` 时 `ptu_capacity` 默认为 `input_tpm=10000`, `output_tpm=1000`。 |
| **视频部署特有** | `aigc_config` | 必须包含 `use_input_prompt`, `prompt`, `lora_prompt_default`，用于控制提示词生成逻辑。 |

## 使用方式

1. **微调训练**：调用 `POST /api/v1/fine-tunes` 创建任务（如 [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)），轮询 `GET /api/v1/fine-tunes/{job_id}` 确认状态为 `SUCCEEDED`，获取 `finetuned_output`。
2. **模型导入**：调用 `POST /api/v1/custom_models/import` 提交 OSS 路径，轮询 `GET /api/v1/custom_models/import/{job_id}` 直至 `SUCCESSED`，获得可部署模型名。
3. **模型压缩**：先 `GET /api/v1/fine-tunes/compress/templates` 获取模板，再 `POST /api/v1/fine-tunes/compress/jobs` 创建任务，轮询至 `SUCCEEDED` 后取 `quantized_output`。
4. **部署服务**：调用 `POST /api/v1/deployments`，传入上一步所得模型名及对应 `plan` 参数。部署后轮询 `GET /api/v1/deployments/{deployed_model}`，待 `status` 变为 `RUNNING` 即可调用。
5. **TPM 预留（PTU）**：使用 `POST /api/v1/deployments`（同部署接口），但 `plan=ptu` 且携带 `ptu_capacity` 对象，无需 `model_name` —— 此为纯容量预留，不绑定具体模型 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。

## 限制和注意事项

- **地域强约束**：微调、导入、压缩、部署（除 TPM 预留外）所有 API 均**仅支持华北2（北京）地域**；TPM 预留虽支持多地域（如弗吉尼亚），但需使用对应地域的 Endpoint 和 API Key。
- **模型兼容性**：
  - 视频/图像微调仅支持指定基准模型（如 `wan2.7-i2v`, `wan2.7-image-pro`），不可混用；
  - 模型压缩**仅支持 `qwen3.5-flash-2026-02-23` 的全参调优模型**，LoRA 模型无法压缩；
  - 语音合成部署**仅支持 `plan=mu`**，不支持 `lora` 或 `ptu`。
- **部署规格约束**：
  - `mu` 部署中 `capacity` 必须为 `deploy_spec` 的 `base_capacity` 整数倍（如 `MU2` 要求 `capacity` 为 8 的倍数）；
  - `lora` 部署 `capacity` 固定为 1，不可调整；
  - `ptu` 部署的 `input_tpm`/`output_tpm` 单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟），扩缩容为绝对值变更，非增量。
- **计费与状态**：HTTP 200 不代表操作成功。TPM 预留创建响应中 `output.operation_status` 可能为 `FAILED`；部署/微调任务需检查 `status` 字段（如 `SUCCEEDED`/`RUNNING`），而非仅依赖 HTTP 状态码。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [文本生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api.md)
- [文本生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)
- [模型导入](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)
- [图像生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api.md)
- [视频生成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api.md)
- [图像生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-image-generation-api/image-generation-create-fine-tuning-job-api.md)
- [视频生成-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-video-generation-api/video-generation-create-fine-tuning-job-api.md)
- [语音合成（CosyVoice）-创建调优任务](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api/voice-synthesis-create-fine-tuning-job-api.md)
- [语音合成](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-speech-synthesis-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [文本生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api.md)
- [文本生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)
- [图像生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api.md)
- [图像生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-image-generation-api/image-generation-deploy-model-api.md)
- [视频生成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api.md)
- [调优任务管理](../../raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)
- [语音合成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api/tts-deploy-model-api.md)
- [部署模型管理](../../raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)
- [视频生成-部署模型](../../raw/model-api-reference/model-production/deployments-api/model-deployment-video-generation-api/video-generation-deploy-model-api.md)
- [语音合成](../../raw/model-api-reference/model-production/deployments-api/model-deployment-speech-synthesis-api.md)


